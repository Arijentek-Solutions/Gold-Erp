"""
POS Session API - Opening and closing cash register sessions
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate, now_datetime, nowdate


@frappe.whitelist(methods=["POST"])
def open_pos_session(
	pos_profile: str,
	opening_balance: float = 0,
	cash_breakdown: str | None = None,
	notes: str | None = None,
):
	"""
	Open a new POS session (cash register opening).

	Args:
	    pos_profile: Name of the POS profile
	    opening_balance: Starting cash amount
	    cash_breakdown: JSON string with cash denomination breakdown
	    notes: Optional opening notes

	Returns:
	    Session details
	"""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	# Validate POS profile
	if not frappe.db.exists("POS Profile", pos_profile):
		frappe.throw(_("POS Profile '{0}' not found.").format(pos_profile))

	# Check for existing open session
	existing_session = frappe.db.get_value(
		"POS Opening Entry",
		{
			"pos_profile": pos_profile,
			"user": frappe.session.user,
			"docstatus": 0,
			"status": ["in", ["Draft", "Open"]],
		},
		"name",
	)

	if existing_session:
		frappe.throw(
			_("You already have an open session '{0}'. Please close it first.").format(existing_session)
		)

	# Parse cash breakdown if provided
	breakdown_list = []
	if cash_breakdown:
		breakdown_list = frappe.parse_json(cash_breakdown) if isinstance(cash_breakdown, str) else cash_breakdown

	# Get company from POS profile
	company = frappe.db.get_value("POS Profile", pos_profile, "company")
	if not company:
		company = frappe.defaults.get_user_default("Company") or frappe.db.get_single_value(
			"Global Defaults", "default_company"
		)

	# Create POS Opening Entry
	opening_entry = frappe.new_doc("POS Opening Entry")
	opening_entry.pos_profile = pos_profile
	opening_entry.user = frappe.session.user
	opening_entry.company = company
	opening_entry.posting_date = getdate()
	opening_entry.posting_time = now_datetime().strftime("%H:%M:%S")
	opening_entry.grand_opening_amount = flt(opening_balance)
	opening_entry.set_posting_time = 1

	# Add opening balance details
	if breakdown_list:
		for item in breakdown_list:
			opening_entry.append(
				"balance_details",
				{
					"mode_of_payment": item.get("mode_of_payment", "Cash"),
					"opening_amount": flt(item.get("amount", 0)),
				},
			)
	else:
		# Default cash entry
		opening_entry.append(
			"balance_details",
			{
				"mode_of_payment": "Cash",
				"opening_amount": flt(opening_balance),
			},
		)

	if notes:
		opening_entry.remarks = notes

	opening_entry.insert(ignore_permissions=True)

	# Optionally submit if auto_submit is enabled
	# opening_entry.submit()

	return {
		"success": True,
		"session_name": opening_entry.name,
		"status": opening_entry.status or "Draft",
		"opening_balance": opening_entry.grand_opening_amount,
		"posting_date": opening_entry.posting_date,
		"message": _("POS session {0} opened successfully").format(opening_entry.name),
	}


@frappe.whitelist(methods=["POST"])
def close_pos_session(
	session_name: str,
	closing_balance: float,
	cash_breakdown: str | None = None,
	notes: str | None = None,
):
	"""
	Close a POS session (cash register closing with reconciliation).

	Args:
	    session_name: Name of the POS Opening Entry
	    closing_balance: Actual cash counted
	    cash_breakdown: JSON string with cash denomination breakdown
	    notes: Optional closing notes

	Returns:
	    Closing details including variance
	"""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	# Get opening entry
	if not frappe.db.exists("POS Opening Entry", session_name):
		frappe.throw(_("POS Session '{0}' not found.").format(session_name))

	opening_entry = frappe.get_doc("POS Opening Entry", session_name)

	# Check ownership or manager role
	if opening_entry.user != frappe.session.user:
		frappe.only_for(["Sales Manager", "System Manager"])

	# Check if already closed
	if opening_entry.docstatus == 1:
		frappe.throw(_("Session '{0}' is already closed.").format(session_name))

	# Parse cash breakdown if provided
	breakdown_list = []
	if cash_breakdown:
		breakdown_list = frappe.parse_json(cash_breakdown) if isinstance(cash_breakdown, str) else cash_breakdown

	# Calculate expected balance from sales
	expected_balance = flt(opening_entry.grand_opening_amount)

	# Get all POS invoices for this session
	sales_invoices = frappe.get_all(
		"Sales Invoice",
		filters={
			"pos_profile": opening_entry.pos_profile,
			"owner": opening_entry.user,
			"posting_date": [">=", opening_entry.posting_date],
			"docstatus": 1,
			"is_pos": 1,
		},
		fields=["name", "grand_total", "status"],
	)

	# Calculate total sales
	total_sales = sum(flt(si.grand_total) for si in sales_invoices)
	expected_balance += total_sales

	# Calculate variance
	variance = flt(closing_balance) - expected_balance

	# Create POS Closing Entry
	closing_entry = frappe.new_doc("POS Closing Entry")
	closing_entry.pos_opening_entry = session_name
	closing_entry.pos_profile = opening_entry.pos_profile
	closing_entry.user = opening_entry.user
	closing_entry.company = opening_entry.company
	closing_entry.posting_date = getdate()
	closing_entry.posting_time = now_datetime().strftime("%H:%M:%S")

	# Add balance details
	if breakdown_list:
		for item in breakdown_list:
			closing_entry.append(
				"payment_reconciliation",
				{
					"mode_of_payment": item.get("mode_of_payment", "Cash"),
					"opening_amount": flt(item.get("opening_amount", 0)),
					"expected_amount": flt(item.get("expected_amount", 0)),
					"closing_amount": flt(item.get("amount", 0)),
				},
			)
	else:
		# Default cash entry
		closing_entry.append(
			"payment_reconciliation",
			{
				"mode_of_payment": "Cash",
				"opening_amount": flt(opening_entry.grand_opening_amount),
				"expected_amount": flt(expected_balance),
				"closing_amount": flt(closing_balance),
			},
		)

	if notes:
		closing_entry.remarks = notes

	closing_entry.insert(ignore_permissions=True)

	# Submit opening entry first
	if opening_entry.docstatus == 0:
		opening_entry.submit()

	# Submit closing entry
	closing_entry.submit()

	return {
		"success": True,
		"closing_name": closing_entry.name,
		"opening_balance": opening_entry.grand_opening_amount,
		"total_sales": total_sales,
		"expected_balance": expected_balance,
		"closing_balance": closing_balance,
		"variance": variance,
		"variance_status": "shortage" if variance < 0 else ("excess" if variance > 0 else "balanced"),
		"sales_count": len(sales_invoices),
		"message": _("Session closed. Variance: {0}").format(flt(variance)),
	}


@frappe.whitelist()
def get_session_status(pos_profile: str | None = None):
	"""
	Get the current POS session status for the logged-in user.

	Args:
	    pos_profile: Optional POS profile to check

	Returns:
	    Session status details
	"""
	# Get active session for current user
	filters = {"user": frappe.session.user, "docstatus": ["<", 2]}

	if pos_profile:
		filters["pos_profile"] = pos_profile

	active_session = frappe.db.get_value(
		"POS Opening Entry",
		filters,
		["name", "pos_profile", "posting_date", "posting_time", "grand_opening_amount", "docstatus", "status"],
		as_dict=True,
	)

	if not active_session:
		return {
			"has_active_session": False,
			"session": None,
			"message": "No active session found",
		}

	# Calculate session duration
	from datetime import datetime

	opening_time = datetime.combine(active_session.posting_date, active_session.posting_time or datetime.min.time())
	duration = datetime.now() - opening_time

	# Get sales summary for the session
	sales_summary = frappe.db.sql(
		"""
		SELECT COUNT(*) as count, COALESCE(SUM(grand_total), 0) as total
		FROM `tabSales Invoice`
		WHERE pos_profile = %s
		AND owner = %s
		AND posting_date >= %s
		AND docstatus = 1
		AND is_pos = 1
	""",
		(active_session.pos_profile, frappe.session.user, active_session.posting_date),
		as_dict=True,
	)

	summary = sales_summary[0] if sales_summary else {"count": 0, "total": 0}

	return {
		"has_active_session": True,
		"session": {
			"name": active_session.name,
			"pos_profile": active_session.pos_profile,
			"opening_date": str(active_session.posting_date),
			"opening_time": str(active_session.posting_time),
			"opening_balance": flt(active_session.grand_opening_amount),
			"status": active_session.status or "Draft",
			"docstatus": active_session.docstatus,
			"duration_hours": round(duration.total_seconds() / 3600, 2),
			"sales_count": summary.count,
			"sales_total": flt(summary.total),
		},
	}


@frappe.whitelist()
def get_session_sales(session_name: str):
	"""
	Get all sales for a specific session.

	Args:
	    session_name: Name of the POS Opening Entry

	Returns:
	    List of sales invoices
	"""
	opening_entry = frappe.get_doc("POS Opening Entry", session_name)

	# Check permission
	if opening_entry.user != frappe.session.user:
		frappe.only_for(["Sales Manager", "System Manager"])

	sales = frappe.get_all(
		"Sales Invoice",
		filters={
			"pos_profile": opening_entry.pos_profile,
			"owner": opening_entry.user,
			"posting_date": [">=", opening_entry.posting_date],
			"docstatus": 1,
			"is_pos": 1,
		},
		fields=["name", "customer", "posting_date", "grand_total", "status", "currency"],
		order_by="posting_date, creation",
	)

	return {"sales": sales, "count": len(sales)}


@frappe.whitelist()
def list_user_sessions(user: str | None = None, limit: int = 10):
	"""
	List recent POS sessions for a user.

	Args:
	    user: User ID (defaults to current user)
	    limit: Maximum sessions to return

	Returns:
	    List of sessions
	"""
	if not user:
		user = frappe.session.user

	# Check permission - managers can view all, others only their own
	if user != frappe.session.user:
		frappe.only_for(["Sales Manager", "System Manager"])

	sessions = frappe.get_all(
		"POS Opening Entry",
		filters={"user": user},
		fields=[
			"name",
			"pos_profile",
			"posting_date",
			"posting_time",
			"grand_opening_amount",
			"docstatus",
			"status",
		],
		order_by="creation desc",
		limit_page_length=limit,
	)

	return {"sessions": sessions, "count": len(sessions)}
