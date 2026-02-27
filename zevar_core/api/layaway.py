"""
Layaway API - Contract creation, payments, and cancellation
"""

import frappe
from frappe import _
from frappe.utils import add_months, flt, today


@frappe.whitelist(methods=["GET"])
def get_layaway_details(layaway_id: str) -> dict:
	"""Return full details of a Layaway Contract including items and schedule."""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	if not layaway_id or not frappe.db.exists("Layaway Contract", layaway_id):
		frappe.throw(_("Layaway Contract '{0}' not found.").format(layaway_id))

	doc = frappe.get_doc("Layaway Contract", layaway_id)

	return {
		"layaway_id": doc.name,
		"customer": doc.customer,
		"status": doc.status,
		"contract_date": str(doc.contract_date),
		"target_completion_date": str(doc.target_completion_date),
		"duration_months": doc.maximum_duration_months,
		"total_amount": flt(doc.total_amount),
		"deposit_amount": flt(doc.deposit_amount),
		"balance_amount": flt(doc.balance_amount),
		"cancellation_refund_type": doc.cancellation_refund_type,
		"store_credit_reference": doc.store_credit_reference,
		"items": [
			{
				"item_code": row.item_code,
				"qty": flt(row.qty),
				"rate": flt(row.rate),
				"amount": flt(row.amount),
			}
			for row in doc.items
		],
		"payment_schedule": [
			{
				"payment_date": str(row.payment_date),
				"expected_amount": flt(row.expected_amount),
				"paid_amount": flt(row.paid_amount),
				"status": row.status,
			}
			for row in doc.payment_schedule
		],
	}


@frappe.whitelist(methods=["GET"])
def get_customer_layaways(customer: str) -> list:
	"""Return all Layaway Contracts for a customer, newest first."""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	if not customer or not frappe.db.exists("Customer", customer):
		frappe.throw(_("Customer '{0}' not found.").format(customer))

	contracts = frappe.get_all(
		"Layaway Contract",
		filters={"customer": customer, "docstatus": ["!=", 2]},
		fields=[
			"name",
			"status",
			"contract_date",
			"target_completion_date",
			"total_amount",
			"deposit_amount",
			"balance_amount",
		],
		order_by="creation desc",
	)
	return contracts


@frappe.whitelist(methods=["POST"])
def create_layaway(
	customer: str,
	items: str,
	deposit_amount: float,
	duration_months: int,
	warehouse: str | None = None,
) -> dict:
	"""Create a new Layaway Contract with deposit and payment schedule."""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	items_list = frappe.parse_json(items) if isinstance(items, str) else items

	# --- Input validation ---
	if not items_list:
		frappe.throw(_("At least one item is required."))

	if not customer or not frappe.db.exists("Customer", customer):
		frappe.throw(_("Customer '{0}' not found.").format(customer))

	if int(duration_months) not in (3, 6, 9, 12):
		frappe.throw(_("Duration must be 3, 6, 9, or 12 months."))

	if not warehouse:
		store_loc = frappe.db.get_value("Store Location", {"is_active": 1}, "default_warehouse")
		if store_loc:
			warehouse = store_loc

	if not warehouse or not frappe.db.exists("Warehouse", warehouse):
		frappe.throw(_("Warehouse '{0}' not found. Please ensure a store location has an active default warehouse.").format(warehouse))

	for item in items_list:
		if not item.get("item_code"):
			frappe.throw(_("Each item must have an item_code."))
		if flt(item.get("rate", 0)) <= 0:
			frappe.throw(_("Item {0}: rate must be greater than zero.").format(item.get("item_code")))

	deposit = flt(deposit_amount)
	total_amount = sum(flt(i.get("qty", 1)) * flt(i.get("rate")) for i in items_list)

	if deposit <= 0:
		frappe.throw(_("Deposit amount must be greater than zero."))

	if deposit >= total_amount:
		frappe.throw(_("Deposit cannot equal or exceed total amount. Use a regular sale instead."))

	# --- Build contract ---
	try:
		doc = frappe.new_doc("Layaway Contract")
		doc.customer = customer
		doc.contract_date = today()
		doc.maximum_duration_months = str(duration_months)
		doc.target_completion_date = add_months(today(), int(duration_months))
		doc.cancellation_refund_type = "Store Credit Only"

		for item in items_list:
			qty = flt(item.get("qty", 1))
			rate = flt(item.get("rate"))
			doc.append(
				"items",
				{
					"item_code": item.get("item_code"),
					"qty": qty,
					"rate": rate,
					"amount": qty * rate,
				},
			)

		doc.total_amount = total_amount
		doc.deposit_amount = deposit
		doc.balance_amount = total_amount - deposit

		# Initial deposit entry in schedule
		doc.append(
			"payment_schedule",
			{
				"payment_date": today(),
				"expected_amount": deposit,
				"paid_amount": deposit,
				"status": "Paid",
			},
		)

		# Generate remaining monthly schedule
		remaining_months = int(duration_months) - 1
		if remaining_months > 0 and doc.balance_amount > 0:
			monthly_payment = doc.balance_amount / remaining_months
			for i in range(1, remaining_months + 1):
				doc.append(
					"payment_schedule",
					{
						"payment_date": add_months(today(), i),
						"expected_amount": monthly_payment,
						"paid_amount": 0,
						"status": "Pending",
					},
				)

		doc.status = "Active"
		doc.insert(ignore_permissions=True)
		doc.submit()

		return {
			"success": True,
			"layaway_id": doc.name,
			"message": "Layaway created successfully",
		}
	except Exception as e:
		frappe.log_error("Layaway Creation Failed", frappe.get_traceback())
		raise frappe.ValidationError(f"Failed to create layaway: {e!s}")


@frappe.whitelist(methods=["POST"])
def process_layaway_payment(layaway_id: str, payment_amount: float, mode_of_payment: str) -> dict:
	"""Process a payment towards a layaway balance."""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	if not layaway_id or not frappe.db.exists("Layaway Contract", layaway_id):
		frappe.throw(_("Layaway Contract '{0}' not found.").format(layaway_id))

	doc = frappe.get_doc("Layaway Contract", layaway_id)

	if doc.status != "Active":
		frappe.throw(_("Layaway is {0}, cannot process payment.").format(doc.status))

	amount = flt(payment_amount)
	if amount <= 0:
		frappe.throw(_("Payment amount must be greater than zero."))

	if amount > flt(doc.balance_amount):
		frappe.throw(_("Payment amount cannot exceed balance amount."))

	if not mode_of_payment:
		frappe.throw(_("Mode of payment is required."))

	try:
		# Distribute payment across pending schedule rows
		remaining = amount
		for row in doc.payment_schedule:
			if row.status == "Pending" and remaining > 0:
				needed = flt(row.expected_amount) - flt(row.paid_amount)
				applied = min(remaining, needed)
				row.paid_amount += applied
				remaining -= applied

				if row.paid_amount >= row.expected_amount:
					row.status = "Paid"

		doc.balance_amount -= amount
		doc.deposit_amount += amount

		if doc.balance_amount <= 0:
			doc.status = "Completed"

		doc.save(ignore_permissions=True)

		return {
			"success": True,
			"new_balance": doc.balance_amount,
			"status": doc.status,
			"message": "Payment processed successfully",
		}
	except Exception as e:
		frappe.log_error("Layaway Payment Failed", frappe.get_traceback())
		raise frappe.ValidationError(f"Failed to process layaway payment: {e!s}")


@frappe.whitelist(methods=["POST"])
def cancel_layaway(layaway_id: str) -> dict:
	"""Cancel an active layaway. Generates a Gift Card as strict Store Credit."""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	if not layaway_id or not frappe.db.exists("Layaway Contract", layaway_id):
		frappe.throw(_("Layaway Contract '{0}' not found.").format(layaway_id))

	doc = frappe.get_doc("Layaway Contract", layaway_id)

	if doc.status != "Active":
		frappe.throw(_("Layaway is {0}, cannot cancel.").format(doc.status))

	if flt(doc.deposit_amount) <= 0:
		frappe.throw(_("No payments to refund."))

	try:
		gc = frappe.new_doc("Gift Card")
		gc.customer = doc.customer
		gc.initial_value = doc.deposit_amount
		gc.balance = doc.deposit_amount
		gc.source = "Layaway Cancellation"
		gc.issue_date = today()
		gc.status = "Active"
		gc.insert(ignore_permissions=True)
		gc.submit()

		doc.status = "Cancelled"
		doc.store_credit_reference = gc.name
		doc.save(ignore_permissions=True)

		return {
			"success": True,
			"store_credit_id": gc.name,
			"amount_refunded": doc.deposit_amount,
			"message": f"Layaway cancelled. Store Credit {gc.name} generated.",
		}
	except Exception as e:
		frappe.log_error("Layaway Cancellation Failed", frappe.get_traceback())
		raise frappe.ValidationError(f"Failed to cancel layaway: {e!s}")
