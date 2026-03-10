"""
Quick Layaway API - Fast layaway creation and preview
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate, add_months, now_datetime


@frappe.whitelist()
def get_layaway_preview(
	items: str,
	customer: str,
	down_payment_percent: float = 20,
	term_months: int = 3,
	discount_amount: float = 0,
):
	"""
	Preview a layaway plan before creating it.

	Args:
	    items: JSON string of items [{item_code, qty, rate}]
	    customer: Customer name
	    down_payment_percent: Percentage for down payment (default 20%)
	    term_months: Duration in months (3, 6, 9, or 12)
	    discount_amount: Discount to apply

	Returns:
	    Layaway preview with payment schedule
	"""
	frappe.has_permission("Layaway Contract", "read", throw=True)

	items_list = frappe.parse_json(items) if isinstance(items, str) else items

	if not items_list:
		frappe.throw(_("At least one item is required."))

	# Validate term
	valid_terms = [3, 6, 9, 12]
	if term_months not in valid_terms:
		frappe.throw(_("Term must be one of: {0}").format(", ".join(map(str, valid_terms))))

	# Calculate totals
	subtotal = sum(flt(item.get("rate", 0)) * flt(item.get("qty", 1)) for item in items_list)
	discount = flt(discount_amount)
	total_after_discount = max(0, subtotal - discount)
	down_payment = (total_after_discount * flt(down_payment_percent)) / 100
	balance = total_after_discount - down_payment

	# Calculate monthly payment
	monthly_payment = balance / term_months

	# Generate payment schedule
	payment_schedule = []
	today = getdate()

	for i in range(term_months):
		due_date = add_months(today, i + 1)
		amount = round(monthly_payment, 2) if i < term_months - 1 else round(balance - sum(p["amount"] for p in payment_schedule), 2)
		payment_schedule.append(
			{
				"installment": i + 1,
				"due_date": str(due_date),
				"amount": flt(amount),
				"status": "Pending",
			}
		)
		balance -= amount

	return {
		"preview": {
			"customer": customer,
			"items": items_list,
			"item_count": len(items_list),
			"subtotal": flt(subtotal),
			"discount": flt(discount),
			"total": flt(total_after_discount),
			"down_payment_percent": flt(down_payment_percent),
			"down_payment": flt(down_payment),
			"balance": flt(total_after_discount - down_payment),
			"term_months": term_months,
			"monthly_payment": flt(monthly_payment),
		},
		"payment_schedule": payment_schedule,
		"valid_terms": valid_terms,
	}


@frappe.whitelist(methods=["POST"])
def create_quick_layaway(
	items: str,
	customer: str,
	down_payment_percent: float = 20,
	term_months: int = 3,
	discount_amount: float = 0,
	initial_payment: float = 0,
	initial_payment_mode: str = "Cash",
	warehouse: str | None = None,
	salesperson: str | None = None,
	notes: str | None = None,
):
	"""
	Create a layaway contract quickly with minimal input.

	Args:
	    items: JSON string of items [{item_code, qty, rate}]
	    customer: Customer name
	    down_payment_percent: Percentage for down payment (default 20%)
	    term_months: Duration in months (3, 6, 9, or 12)
	    discount_amount: Discount to apply
	    initial_payment: Initial payment amount (if any)
	    initial_payment_mode: Mode of initial payment
	    warehouse: Warehouse for items
	    salesperson: Salesperson name
	    notes: Additional notes

	Returns:
	    Created layaway contract details
	"""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	items_list = frappe.parse_json(items) if isinstance(items, str) else items

	if not items_list:
		frappe.throw(_("At least one item is required."))

	# Validate customer
	if not frappe.db.exists("Customer", customer):
		frappe.throw(_("Customer '{0}' not found.").format(customer))

	# Validate term
	valid_terms = [3, 6, 9, 12]
	if term_months not in valid_terms:
		frappe.throw(_("Term must be one of: {0}").format(", ".join(map(str, valid_terms))))

	# Get preview for calculations
	preview = get_layaway_preview(
		items=items,
		customer=customer,
		down_payment_percent=down_payment_percent,
		term_months=term_months,
		discount_amount=discount_amount,
	)

	preview_data = preview["preview"]

	# Determine warehouse
	if not warehouse:
		warehouse = frappe.db.get_value("Store Location", {"is_active": 1}, "default_warehouse")
	if not warehouse:
		frappe.throw(_("No warehouse found. Please specify a warehouse."))

	# Get company
	company = frappe.defaults.get_user_default("Company") or frappe.db.get_single_value(
		"Global Defaults", "default_company"
	)

	# Create layaway contract
	contract = frappe.new_doc("Layaway Contract")
	contract.customer = customer
	contract.company = company
	contract.contract_date = getdate()
	contract.term_months = term_months
	contract.down_payment_percent = flt(down_payment_percent)
	contract.total_amount = preview_data["total"]
	contract.down_payment_amount = preview_data["down_payment"]
	contract.balance_amount = preview_data["balance"]
	contract.status = "Draft"
	contract.warehouse = warehouse

	if salesperson:
		contract.salesperson = salesperson

	if notes:
		contract.notes = notes

	# Add items
	for item in items_list:
		contract.append(
			"items",
			{
				"item_code": item.get("item_code"),
				"qty": flt(item.get("qty", 1)),
				"rate": flt(item.get("rate")),
				"amount": flt(item.get("rate")) * flt(item.get("qty", 1)),
			},
		)

	# Add payment schedule
	for schedule in preview["payment_schedule"]:
		contract.append(
			"payment_schedule",
			{
				"due_date": schedule["due_date"],
				"amount": schedule["amount"],
				"status": "Pending",
			},
		)

	contract.insert(ignore_permissions=True)

	# Process initial payment if provided
	if flt(initial_payment) > 0:
		contract.status = "Active"
		contract.paid_amount = flt(initial_payment)
		contract.balance_amount = preview_data["balance"] - flt(initial_payment)

		# Create payment entry
		try:
			from zevar_core.api.layaway import process_layaway_payment

			process_layaway_payment(
				contract_name=contract.name,
				amount=flt(initial_payment),
				payment_mode=initial_payment_mode,
			)
		except Exception:
			# If payment processing fails, still return the contract
			frappe.log_error("Quick Layaway Payment Failed", frappe.get_traceback())

	contract.save(ignore_permissions=True)

	return {
		"success": True,
		"contract_name": contract.name,
		"status": contract.status,
		"total_amount": flt(contract.total_amount),
		"down_payment_amount": flt(contract.down_payment_amount),
		"balance_amount": flt(contract.balance_amount),
		"term_months": contract.term_months,
		"message": _("Layaway contract {0} created successfully.").format(contract.name),
	}


@frappe.whitelist()
def get_quick_layaway_defaults():
	"""
	Get default values for quick layaway creation.

	Returns:
	    Default settings for layaway creation
	"""
	# Get from Gold Settings or default values
	settings = frappe.get_single("Gold Settings") if frappe.db.exists("DocType", "Gold Settings") else None

	return {
		"default_down_payment_percent": flt(settings.default_down_payment_percent) if settings else 20,
		"default_term_months": 3,
		"valid_terms": [3, 6, 9, 12],
		"valid_payment_modes": ["Cash", "Credit Card", "Debit Card", "Check"],
	}


@frappe.whitelist()
def validate_item_for_layaway(item_code: str):
	"""
	Check if an item is eligible for layaway.

	Args:
	    item_code: Item code to check

	Returns:
	    Eligibility status and item details
	"""
	frappe.has_permission("Item", "read", throw=True)

	if not frappe.db.exists("Item", item_code):
		frappe.throw(_("Item '{0}' not found.").format(item_code))

	item = frappe.get_doc("Item", item_code)

	# Check if item can be put on layaway
	eligible = True
	reasons = []

	# Check if item is disabled
	if item.disabled:
		eligible = False
		reasons.append("Item is disabled")

	# Check if item is a stock item with sufficient quantity
	if item.is_stock_item:
		stock_qty = frappe.db.get_value("Bin", {"item_code": item_code}, "actual_qty") or 0
		if stock_qty <= 0:
			eligible = False
			reasons.append("No stock available")

	return {
		"item_code": item_code,
		"item_name": item.item_name,
		"eligible": eligible,
		"reasons": reasons,
		"standard_rate": flt(item.standard_rate),
		"stock_uom": item.stock_uom,
	}
