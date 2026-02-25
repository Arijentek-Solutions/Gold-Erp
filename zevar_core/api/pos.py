"""
POS API - Invoice creation and settings
"""

import frappe
from frappe import _

from zevar_core.constants import DEFAULT_TAX_RATES, PAYMENT_MODES


@frappe.whitelist(methods=["POST"])
def create_pos_invoice(
	items: str,
	payments: str,
	customer: str,
	warehouse: str,
	discount_amount: float = 0,
	tax_exempt: str | bool = False,
	salespersons: str | None = None,
	layaway_reference: str | None = None,
) -> dict:
	"""
	Create a complete POS Invoice with:
	- Stock reservation/deduction
	- Multiple payment modes (split tender)
	- Tax calculation based on warehouse/store location
	- Salesperson tracking (up to 4 with split percentages)
	- Commission calculation trigger (on submit)
	"""
	from frappe.utils import flt

	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	items_list = frappe.parse_json(items) if isinstance(items, str) else items
	payments_list = frappe.parse_json(payments) if isinstance(payments, str) else payments

	if not items_list:
		frappe.throw(_("At least one item is required."))

	if not payments_list:
		frappe.throw(_("At least one payment mode is required."))

	for item in items_list:
		if not item.get("item_code"):
			frappe.throw(_("Each item must have an item_code."))
		if flt(item.get("qty", 0)) <= 0:
			frappe.throw(_("Item {0}: quantity must be greater than zero.").format(item.get('item_code')))
		if flt(item.get("rate", 0)) <= 0:
			frappe.throw(_("Item {0}: rate must be greater than zero.").format(item.get('item_code')))

	if not warehouse or not frappe.db.exists("Warehouse", warehouse):
		frappe.throw(_("Warehouse '{0}' not found.").format(warehouse))

	salesperson_data = []
	if salespersons:
		salesperson_data = frappe.parse_json(salespersons) if isinstance(salespersons, str) else salespersons
		total_split = sum(flt(sp.get("split")) for sp in salesperson_data[:4])
		if salesperson_data and abs(total_split - 100) > 0.01:
			frappe.throw(_("Salesperson splits must total 100%. Current total: {0}%").format(total_split))

	is_tax_exempt = str(tax_exempt).lower() in ["true", "1", "t", "y", "yes"]

	if not customer:
		customer = frappe.db.get_single_value("Global Defaults", "default_customer") or "Walk-In Customer"

	if not frappe.db.exists("Customer", customer):
		frappe.throw(_("Customer '{0}' not found.").format(customer))

	try:
		si = frappe.new_doc("Sales Invoice")
		si.is_pos = 1
		si.update_stock = 1
		si.customer = customer
		si.set_posting_time = 1

		company = frappe.defaults.get_user_default("Company") or frappe.db.get_single_value(
			"Global Defaults", "default_company"
		)
		if company:
			si.company = company

		# Find POS profile and Tax Template from Store Location by Warehouse
		store_location = frappe.get_all(
			"Store Location",
			filters={"default_warehouse": warehouse, "is_active": 1},
			fields=["pos_profile", "tax_template", "county_tax_rate"],
			limit=1,
		)

		tax_template = None
		if store_location:
			store_info = store_location[0]
			if store_info.get("pos_profile"):
				si.pos_profile = store_info.get("pos_profile")
			tax_template = store_info.get("tax_template")

		for item in items_list:
			si.append(
				"items",
				{
					"item_code": item.get("item_code"),
					"qty": flt(item.get("qty", 1)),
					"rate": flt(item.get("rate")),
					"warehouse": warehouse,
				},
			)

		if flt(discount_amount) > 0:
			si.apply_discount_on = "Grand Total"
			si.discount_amount = flt(discount_amount)

		if not is_tax_exempt and tax_template:
			si.taxes_and_charges = tax_template
			si.custom_no_tax_override = 0
		else:
			si.custom_no_tax_override = 1 if is_tax_exempt else 0

		for idx, sp in enumerate(salesperson_data[:4]):
			si.set(f"custom_salesperson_{idx + 1}", sp.get("salesperson") or sp.get("employee"))
			si.set(f"custom_salesperson_{idx + 1}_split", flt(sp.get("split")))

		if layaway_reference:
			si.custom_layaway_reference = layaway_reference

		for pay in payments_list:
			si.append(
				"payments",
				{
					"mode_of_payment": pay.get("mode_of_payment") or pay.get("mode"),
					"amount": flt(pay.get("amount")),
				},
			)

		si.insert(ignore_permissions=True)
		si.submit()

		return {
			"success": True,
			"invoice_name": si.name,
			"status": si.status,
			"grand_total": si.grand_total,
			"outstanding_amount": si.outstanding_amount,
			"message": f"Successfully created invoice {si.name}",
		}

	except Exception as e:
		frappe.log_error("POS Invoice Creation Failed", frappe.get_traceback())
		raise frappe.ValidationError(f"Failed to create POS Invoice: {e!s}")


@frappe.whitelist()
def get_pos_settings(warehouse: str | None = None):
	"""
	Fetch POS settings including tax rates and payment modes.

	Args:
	    warehouse: Warehouse name to determine tax rate by location

	Returns:
	    POS settings dictionary
	"""
	# Determine tax rate based on warehouse location
	tax_rate = 0.0
	if warehouse:
		# Simple location detection (enhance with actual warehouse location field)
		warehouse_lower = warehouse.lower()
		for location, rate in DEFAULT_TAX_RATES.items():
			if location.lower() in warehouse_lower:
				tax_rate = rate
				break

	# Default company
	company = frappe.defaults.get_user_default("Company") or frappe.db.get_single_value(
		"Global Defaults", "default_company"
	)

	return {"tax_rate": tax_rate, "currency": "USD", "company": company, "payment_modes": PAYMENT_MODES}


@frappe.whitelist()
def calculate_invoice_totals(
	items: str, tax_exempt: bool = False, discount_amount: float = 0, warehouse: str | None = None
):
	"""
	Calculate invoice totals.

	Args:
	    items: JSON string of items [{item_code, qty, rate}]
	    tax_exempt: Whether customer is tax exempt
	    discount_amount: Discount amount to apply
	    warehouse: Warehouse for tax rate determination

	Returns:
	    Totals dictionary
	"""
	items_list = frappe.parse_json(items) if isinstance(items, str) else items

	# Calculate subtotal
	subtotal = sum(float(item.get("rate", 0)) * float(item.get("qty", 1)) for item in items_list)

	# Apply discount
	discount = max(0.0, float(discount_amount))
	subtotal_after_discount = max(0.0, subtotal - discount)

	# Calculate tax
	tax = 0.0
	if not tax_exempt:
		settings = get_pos_settings(warehouse)
		tax_rate = settings.get("tax_rate", 0)
		tax = (subtotal_after_discount * tax_rate) / 100

	# Grand total
	grand_total = subtotal_after_discount + tax

	return {
		"subtotal": subtotal,
		"discount": discount,
		"subtotal_after_discount": subtotal_after_discount,
		"tax": tax,
		"grand_total": grand_total,
	}
