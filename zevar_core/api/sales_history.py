"""
Sales History API - Query and filter past transactions
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate, add_days, add_months


@frappe.whitelist()
def get_sales_history(
	from_date: str | None = None,
	to_date: str | None = None,
	customer: str | None = None,
	salesperson: str | None = None,
	warehouse: str | None = None,
	status: str | None = None,
	search: str | None = None,
	page: int = 1,
	page_size: int = 20,
):
	"""
	Get paginated sales history with filters.

	Args:
	    from_date: Start date (YYYY-MM-DD)
	    to_date: End date (YYYY-MM-DD)
	    customer: Customer name filter
	    salesperson: Salesperson name filter
	    warehouse: Warehouse filter
	    status: Invoice status filter
	    search: Search term for invoice ID or customer
	    page: Page number (1-indexed)
	    page_size: Items per page

	Returns:
	    Paginated list of sales invoices
	"""
	frappe.has_permission("Sales Invoice", "read", throw=True)

	# Default date range: last 30 days
	if not from_date:
		from_date = add_days(getdate(), -30)
	if not to_date:
		to_date = getdate()

	# Build filters
	filters = {
		"is_pos": 1,
		"docstatus": 1,
		"posting_date": ["between", [from_date, to_date]],
	}

	if customer:
		filters["customer"] = ["like", f"%{customer}%"]

	if warehouse:
		filters["warehouse"] = warehouse

	if status:
		filters["status"] = status

	# Get total count for pagination
	count_filters = filters.copy()
	total_count = frappe.db.count("Sales Invoice", count_filters)

	# Calculate offset
	offset = (page - 1) * page_size

	# Build query with search
	base_query = """
		SELECT
			si.name,
			si.customer,
			si.posting_date,
			si.posting_time,
			si.grand_total,
			si.outstanding_amount,
			si.status,
			si.currency,
			si.owner,
			si.custom_salesperson_1,
			si.custom_salesperson_2,
			si.custom_layaway_reference,
			si.custom_trade_in_count
		FROM `tabSales Invoice` si
		WHERE si.is_pos = 1
		AND si.docstatus = 1
		AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
	"""

	params = {"from_date": from_date, "to_date": to_date}

	if customer:
		base_query += " AND si.customer LIKE %(customer)s"
		params["customer"] = f"%{customer}%"

	if warehouse:
		base_query += " AND EXISTS (SELECT 1 FROM `tabSales Invoice Item` sii WHERE sii.parent = si.name AND sii.warehouse = %(warehouse)s)"
		params["warehouse"] = warehouse

	if salesperson:
		base_query += " AND (si.custom_salesperson_1 = %(salesperson)s OR si.custom_salesperson_2 = %(salesperson)s)"
		params["salesperson"] = salesperson

	if status:
		base_query += " AND si.status = %(status)s"
		params["status"] = status

	if search:
		base_query += " AND (si.name LIKE %(search)s OR si.customer LIKE %(search)s)"
		params["search"] = f"%{search}%"

	base_query += " ORDER BY si.posting_date DESC, si.posting_time DESC"
	base_query += f" LIMIT {page_size} OFFSET {offset}"

	sales = frappe.db.sql(base_query, params, as_dict=True)

	# Enrich with item count
	for sale in sales:
		sale.item_count = frappe.db.count("Sales Invoice Item", {"parent": sale.name})
		sale.grand_total = flt(sale.grand_total)
		sale.outstanding_amount = flt(sale.outstanding_amount)

	return {
		"sales": sales,
		"pagination": {
			"page": page,
			"page_size": page_size,
			"total_count": total_count,
			"total_pages": (total_count + page_size - 1) // page_size,
		},
	}


@frappe.whitelist()
def get_sales_summary(
	from_date: str | None = None,
	to_date: str | None = None,
	salesperson: str | None = None,
	warehouse: str | None = None,
):
	"""
	Get sales summary statistics.

	Args:
	    from_date: Start date (YYYY-MM-DD)
	    to_date: End date (YYYY-MM-DD)
	    salesperson: Salesperson name filter
	    warehouse: Warehouse filter

	Returns:
	    Summary statistics for the period
	"""
	frappe.has_permission("Sales Invoice", "read", throw=True)

	# Default: today
	if not from_date:
		from_date = getdate()
	if not to_date:
		to_date = getdate()

	# Build base conditions
	conditions = "si.is_pos = 1 AND si.docstatus = 1 AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s"
	params = {"from_date": from_date, "to_date": to_date}

	if salesperson:
		conditions += " AND (si.custom_salesperson_1 = %(salesperson)s OR si.custom_salesperson_2 = %(salesperson)s)"
		params["salesperson"] = salesperson

	if warehouse:
		conditions += " AND EXISTS (SELECT 1 FROM `tabSales Invoice Item` sii WHERE sii.parent = si.name AND sii.warehouse = %(warehouse)s)"
		params["warehouse"] = warehouse

	# Get summary
	summary = frappe.db.sql(
		f"""
		SELECT
			COUNT(*) as transaction_count,
			COALESCE(SUM(si.grand_total), 0) as total_sales,
			COALESCE(SUM(si.outstanding_amount), 0) as outstanding_amount,
			COALESCE(AVG(si.grand_total), 0) as average_sale,
			COUNT(DISTINCT si.customer) as unique_customers
		FROM `tabSales Invoice` si
		WHERE {conditions}
	""",
		params,
		as_dict=True,
	)[0]

	# Get payment breakdown
	payment_breakdown = frappe.db.sql(
		f"""
		SELECT
			sip.mode_of_payment,
			COALESCE(SUM(sip.amount), 0) as total_amount,
			COUNT(*) as transaction_count
		FROM `tabSales Invoice Payment` sip
		JOIN `tabSales Invoice` si ON sip.parent = si.name
		WHERE {conditions}
		GROUP BY sip.mode_of_payment
		ORDER BY total_amount DESC
	""",
		params,
		as_dict=True,
	)

	# Get hourly breakdown
	hourly = frappe.db.sql(
		f"""
		SELECT
			HOUR(si.posting_time) as hour,
			COUNT(*) as count,
			COALESCE(SUM(si.grand_total), 0) as total
		FROM `tabSales Invoice` si
		WHERE {conditions}
		GROUP BY HOUR(si.posting_time)
		ORDER BY hour
	""",
		params,
		as_dict=True,
	)

	return {
		"period": {"from_date": str(from_date), "to_date": str(to_date)},
		"summary": {
			"transaction_count": summary.transaction_count or 0,
			"total_sales": flt(summary.total_sales),
			"outstanding_amount": flt(summary.outstanding_amount),
			"average_sale": flt(summary.average_sale),
			"unique_customers": summary.unique_customers or 0,
		},
		"payment_breakdown": payment_breakdown,
		"hourly_breakdown": hourly,
	}


@frappe.whitelist()
def get_transaction_details(invoice_name: str):
	"""
	Get detailed information about a specific transaction.

	Args:
	    invoice_name: Sales Invoice name

	Returns:
	    Complete invoice details including items, payments, salespersons
	"""
	frappe.has_permission("Sales Invoice", "read", throw=True)

	if not frappe.db.exists("Sales Invoice", invoice_name):
		frappe.throw(_("Sales Invoice '{0}' not found.").format(invoice_name))

	invoice = frappe.get_doc("Sales Invoice", invoice_name)

	# Get items
	items = []
	for item in invoice.items:
		items.append(
			{
				"item_code": item.item_code,
				"item_name": item.item_name,
				"qty": flt(item.qty),
				"rate": flt(item.rate),
				"amount": flt(item.amount),
				"warehouse": item.warehouse,
			}
		)

	# Get payments
	payments = []
	for payment in invoice.payments:
		payments.append(
			{
				"mode_of_payment": payment.mode_of_payment,
				"amount": flt(payment.amount),
			}
		)

	# Get salespersons
	salespersons = []
	for i in range(1, 5):
		sp = invoice.get(f"custom_salesperson_{i}")
		split = invoice.get(f"custom_salesperson_{i}_split")
		if sp:
			salespersons.append({"name": sp, "split": flt(split)})

	# Get trade-ins
	trade_ins = []
	if hasattr(invoice, "custom_trade_ins"):
		for ti in invoice.custom_trade_ins:
			trade_ins.append(
				{
					"original_item": ti.original_item_code,
					"trade_in_value": flt(ti.trade_in_value),
					"new_item": ti.new_item_code,
				}
			)

	return {
		"invoice": {
			"name": invoice.name,
			"customer": invoice.customer,
			"posting_date": str(invoice.posting_date),
			"posting_time": str(invoice.posting_time),
			"grand_total": flt(invoice.grand_total),
			"subtotal": flt(invoice.total),
			"tax": flt(invoice.total_taxes_and_charges),
			"discount": flt(invoice.discount_amount),
			"outstanding_amount": flt(invoice.outstanding_amount),
			"status": invoice.status,
			"currency": invoice.currency,
			"owner": invoice.owner,
			"layaway_reference": invoice.custom_layaway_reference if hasattr(invoice, "custom_layaway_reference") else None,
		},
		"items": items,
		"payments": payments,
		"salespersons": salespersons,
		"trade_ins": trade_ins,
	}


@frappe.whitelist()
def void_transaction(invoice_name: str, reason: str):
	"""
	Void a POS transaction (cancel the invoice).

	Args:
	    invoice_name: Sales Invoice name
	    reason: Reason for voiding

	Returns:
	    Success status
	"""
	frappe.only_for(["Sales Manager", "System Manager"])

	if not frappe.db.exists("Sales Invoice", invoice_name):
		frappe.throw(_("Sales Invoice '{0}' not found.").format(invoice_name))

	invoice = frappe.get_doc("Sales Invoice", invoice_name)

	if invoice.docstatus != 1:
		frappe.throw(_("Only submitted invoices can be voided."))

	if invoice.status == "Cancelled":
		frappe.throw(_("Invoice is already cancelled."))

	# Cancel the invoice
	invoice.cancel()

	# Log the void
	frappe.log_error(
		f"Transaction Voided: {invoice_name}",
		f"Reason: {reason}\nUser: {frappe.session.user}",
	)

	return {
		"success": True,
		"message": _("Transaction {0} has been voided.").format(invoice_name),
		"invoice_name": invoice_name,
		"status": "Cancelled",
	}


@frappe.whitelist()
def get_customer_purchase_history(customer: str, limit: int = 20):
	"""
	Get purchase history for a specific customer.

	Args:
	    customer: Customer name
	    limit: Maximum records to return

	Returns:
	    List of customer's purchases
	"""
	frappe.has_permission("Sales Invoice", "read", throw=True)

	if not frappe.db.exists("Customer", customer):
		frappe.throw(_("Customer '{0}' not found.").format(customer))

	purchases = frappe.get_all(
		"Sales Invoice",
		filters={"customer": customer, "is_pos": 1, "docstatus": 1},
		fields=[
			"name",
			"posting_date",
			"grand_total",
			"status",
			"custom_layaway_reference",
		],
		order_by="posting_date desc",
		limit_page_length=limit,
	)

	# Get summary stats
	stats = frappe.db.sql(
		"""
		SELECT
			COUNT(*) as total_visits,
			COALESCE(SUM(grand_total), 0) as total_spent,
			COALESCE(AVG(grand_total), 0) as average_purchase
		FROM `tabSales Invoice`
		WHERE customer = %s AND is_pos = 1 AND docstatus = 1
	""",
		(customer,),
		as_dict=True,
	)[0]

	return {
		"customer": customer,
		"purchases": purchases,
		"stats": {
			"total_visits": stats.total_visits or 0,
			"total_spent": flt(stats.total_spent),
			"average_purchase": flt(stats.average_purchase),
		},
	}
