"""
Gift Card API - Balance lookup, payment processing
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate, today


@frappe.whitelist(methods=["GET"])
def get_gift_card_balance(gift_card_number: str) -> dict:
	"""Fetch balance and validate status of a Gift Card."""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	if not gift_card_number or not frappe.db.exists("Gift Card", gift_card_number):
		return {"valid": False, "message": "Invalid Gift Card Number"}

	doc = frappe.get_doc("Gift Card", gift_card_number)

	if doc.status in ("Used", "Cancelled"):
		return {"valid": False, "message": f"Gift Card is {doc.status}"}

	if doc.expiry_date and getdate(doc.expiry_date) < getdate(today()):
		return {"valid": False, "message": "Gift Card is Expired"}

	return {
		"valid": True,
		"balance": flt(doc.balance),
		"initial_value": flt(doc.initial_value),
		"customer": doc.customer,
		"source": doc.source,
		"status": doc.status,
		"message": "Gift Card is valid",
	}


@frappe.whitelist(methods=["POST"])
def process_gift_card_payment(gift_card_number: str, amount: float) -> dict:
	"""Process a deduction against a Gift Card balance."""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	amount_flt = flt(amount)
	if amount_flt <= 0:
		frappe.throw(_("Payment amount must be greater than zero."))

	if not gift_card_number or not frappe.db.exists("Gift Card", gift_card_number):
		frappe.throw(_("Gift Card '{0}' not found.").format(gift_card_number))

	doc = frappe.get_doc("Gift Card", gift_card_number)

	if doc.status != "Active":
		frappe.throw(_("Gift Card is {0}. Cannot process payment.").format(doc.status))

	if doc.expiry_date and getdate(doc.expiry_date) < getdate(today()):
		doc.status = "Expired"
		doc.save(ignore_permissions=True)
		frappe.throw(_("Gift Card has expired."))

	if amount_flt > flt(doc.balance):
		frappe.throw(_("Insufficient funds. Current balance: ${0:,.2f}").format(flt(doc.balance)))

	try:
		doc.balance -= amount_flt

		if doc.balance <= 0:
			doc.status = "Used"

		doc.save(ignore_permissions=True)

		return {
			"success": True,
			"deducted_amount": amount_flt,
			"remaining_balance": flt(doc.balance),
			"status": doc.status,
			"message": "Gift Card Payment processed successfully",
		}
	except Exception as e:
		frappe.log_error("Gift Card Payment Error", frappe.get_traceback())
		raise frappe.ValidationError(f"Failed to process Gift Card payment: {e!s}")
