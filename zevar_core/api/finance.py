"""
Finance API - In-House Finance account payments and scheduled charges
"""

import frappe
from frappe.utils import flt, today


@frappe.whitelist(methods=["GET"])
def get_customer_finance_account(customer: str) -> dict:
	"""Return the In-House Finance Account details for a customer."""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	if not customer or not frappe.db.exists("Customer", customer):
		frappe.throw(f"Customer '{customer}' not found.")

	accounts = frappe.get_all(
		"In-House Finance Account",
		filters={"customer": customer},
		limit=1,
	)
	if not accounts:
		return {"exists": False}

	doc = frappe.get_doc("In-House Finance Account", accounts[0].name)

	return {
		"exists": True,
		"account_id": doc.name,
		"customer": doc.customer,
		"status": doc.status,
		"credit_limit": flt(doc.credit_limit),
		"current_balance": flt(doc.current_balance),
		"available_credit": flt(doc.available_credit),
		"interest_rate": flt(doc.interest_rate),
		"minimum_payment_percent": flt(doc.minimum_payment_percent),
		"ledger_entries": [
			{
				"entry_date": str(row.entry_date),
				"entry_type": row.entry_type,
				"description": row.description,
				"debit": flt(row.debit),
				"credit": flt(row.credit),
				"balance": flt(row.balance),
			}
			for row in (doc.ledger_entries or [])
		],
	}


@frappe.whitelist(methods=["POST"])
def process_finance_payment(account_id: str, amount: float, mode_of_payment: str) -> dict:
	"""Process a payment towards an In-House Finance Account balance."""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	amount_flt = flt(amount)
	if amount_flt <= 0:
		frappe.throw("Payment amount must be greater than zero.")

	if not mode_of_payment:
		frappe.throw("Mode of payment is required.")

	if not account_id or not frappe.db.exists("In-House Finance Account", account_id):
		frappe.throw(f"Finance Account '{account_id}' not found.")

	doc = frappe.get_doc("In-House Finance Account", account_id)

	if doc.status in ("Closed", "Suspended"):
		frappe.throw(f"Account is {doc.status}. Cannot process payment.")

	if amount_flt > flt(doc.current_balance):
		frappe.throw("Payment amount cannot exceed current balance.")

	try:
		doc.append(
			"ledger_entries",
			{
				"entry_date": today(),
				"entry_type": "Payment",
				"description": f"Payment via {mode_of_payment}",
				"credit": amount_flt,
			},
		)

		doc.current_balance -= amount_flt
		doc.available_credit = flt(doc.credit_limit) - flt(doc.current_balance)

		doc.save(ignore_permissions=True)

		return {
			"success": True,
			"new_balance": doc.current_balance,
			"available_credit": doc.available_credit,
			"message": "Finance Payment processed successfully",
		}
	except Exception as e:
		frappe.log_error("Finance Payment Error", frappe.get_traceback())
		raise frappe.ValidationError(f"Failed to process Finance Payment: {e!s}")


@frappe.whitelist(methods=["GET"])
def generate_monthly_statement(account_id: str, month: int, year: int) -> dict:
	"""Generate a monthly statement for an In-House Finance Account."""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	if not account_id or not frappe.db.exists("In-House Finance Account", account_id):
		frappe.throw(f"Finance Account '{account_id}' not found.")

	month = int(month)
	year = int(year)
	if month < 1 or month > 12:
		frappe.throw("Month must be between 1 and 12.")

	doc = frappe.get_doc("In-House Finance Account", account_id)

	# Filter ledger entries for the requested month
	from frappe.utils import getdate

	entries = []
	total_debits = 0.0
	total_credits = 0.0

	for row in doc.ledger_entries or []:
		entry_date = getdate(row.entry_date)
		if entry_date.month == month and entry_date.year == year:
			total_debits += flt(row.debit)
			total_credits += flt(row.credit)
			entries.append(
				{
					"entry_date": str(row.entry_date),
					"entry_type": row.entry_type,
					"description": row.description,
					"debit": flt(row.debit),
					"credit": flt(row.credit),
				}
			)

	# Compute opening balance (sum of all entries before this month)
	opening_balance = 0.0
	for row in doc.ledger_entries or []:
		entry_date = getdate(row.entry_date)
		if entry_date.year < year or (entry_date.year == year and entry_date.month < month):
			opening_balance += flt(row.debit) - flt(row.credit)

	closing_balance = opening_balance + total_debits - total_credits

	return {
		"account_id": doc.name,
		"customer": doc.customer,
		"month": month,
		"year": year,
		"opening_balance": opening_balance,
		"total_debits": total_debits,
		"total_credits": total_credits,
		"closing_balance": closing_balance,
		"entries": entries,
	}


def apply_finance_charges():
	"""
	Scheduled Job: apply monthly interest to active accounts with balances.
	Not whitelisted — called only by scheduler.
	"""
	accounts = frappe.get_all(
		"In-House Finance Account",
		filters={"status": ["in", ["Active", "Collections"]], "current_balance": [">", 0]},
		fields=["name", "interest_rate", "current_balance"],
	)

	for acc in accounts:
		interest_rate = flt(acc.interest_rate)
		if interest_rate <= 0:
			continue

		monthly_rate = interest_rate / 12 / 100
		charge_amount = flt(acc.current_balance * monthly_rate, 2)

		if charge_amount > 0:
			try:
				doc = frappe.get_doc("In-House Finance Account", acc.name)

				doc.append(
					"ledger_entries",
					{
						"entry_date": today(),
						"entry_type": "Finance Charge",
						"description": f"Monthly Finance Charge ({interest_rate}% APR)",
						"debit": charge_amount,
					},
				)

				doc.current_balance += charge_amount
				doc.available_credit = flt(doc.credit_limit) - doc.current_balance

				doc.save(ignore_permissions=True)
			except Exception:
				frappe.log_error(f"Finance Charge Error for {acc.name}", frappe.get_traceback())
