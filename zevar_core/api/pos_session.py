"""
POS Session API - Opening and closing cash register sessions

Provides endpoints for:
- Opening a new POS session
- Closing an active session with reconciliation
- Getting current session status
"""

import frappe
from frappe import _
from frappe.utils import flt, get_datetime, now_datetime, nowdate, time_diff_in_hours


@frappe.whitelist()
def get_session_status() -> dict:
	"""
	Get the current POS session status for the logged-in user.

	Returns:
		dict: Session status with details if active session exists
	"""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	user = frappe.session.user

	# Find active POS Opening Entry for this user
	active_session = frappe.db.get_value(
		"POS Opening Entry",
		filters={
			"user": user,
			"docstatus": 1,
			"status": "Open",
		},
		fieldname=["name", "pos_profile", "period_start_date", "opening_amount", "company"],
		order_by="creation desc",
	)

	if not active_session:
		return {
			"has_active_session": False,
			"session": None,
		}

	session_name, pos_profile, period_start, opening_amount, company = active_session

	# Calculate session duration
	duration_hours = 0
	if period_start:
		duration_hours = time_diff_in_hours(now_datetime(), get_datetime(period_start))

	# Get sales count and total for this session
	sales_data = frappe.db.sql(
		"""
		SELECT COUNT(*) as count, COALESCE(SUM(grand_total), 0) as total
		FROM `tabSales Invoice`
		WHERE owner = %s
		AND posting_date >= DATE(%s)
		AND docstatus = 1
		AND is_pos = 1
		""",
		(user, period_start.date() if hasattr(period_start, "date") else period_start),
		as_dict=True,
	)

	sales_count = 0
	sales_total = 0
	if sales_data and sales_data[0]:
		sales_count = sales_data[0].get("count", 0) or 0
		sales_total = flt(sales_data[0].get("total", 0))

	# Get opening time
	opening_time = frappe.db.get_value("POS Opening Entry", session_name, "period_start_date")

	# Get warehouse from POS Profile
	warehouse = frappe.db.get_value("POS Profile", pos_profile, "warehouse")

	return {
		"has_active_session": True,
		"session": {
			"name": session_name,
			"pos_profile": pos_profile,
			"company": company,
			"warehouse": warehouse,
			"opening_date": period_start.date()
			if hasattr(period_start, "date")
			else str(period_start).split()[0],
			"opening_time": str(opening_time.time())
			if opening_time and hasattr(opening_time, "time")
			else "",
			"opening_balance": flt(opening_amount),
			"sales_count": sales_count,
			"sales_total": flt(sales_total),
			"duration_hours": round(duration_hours, 2),
		},
	}


@frappe.whitelist(methods=["POST"])
def open_pos_session(
	pos_profile: str,
	opening_balance: float,
	cash_breakdown: str | list | None = None,
	notes: str | None = None,
) -> dict:
	"""
	Open a new POS session (cash register).

	Args:
		pos_profile: Name of the POS Profile
		opening_balance: Opening cash amount
		cash_breakdown: JSON string or list of denomination breakdown
		notes: Optional opening notes

	Returns:
		dict: Success status and session details
	"""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	user = frappe.session.user

	# Validate inputs
	if not pos_profile:
		frappe.throw(_("POS Profile is required."))

	if not frappe.db.exists("POS Profile", pos_profile):
		frappe.throw(_("POS Profile '{0}' not found.").format(pos_profile))

	# Check for existing open session
	existing_session = frappe.db.get_value(
		"POS Opening Entry",
		filters={
			"user": user,
			"docstatus": 1,
			"status": "Open",
		},
	)

	if existing_session:
		frappe.throw(
			_("You already have an open session: {0}. Please close it first.").format(existing_session)
		)

	# Parse cash breakdown if provided
	breakdown_list = []
	if cash_breakdown:
		if isinstance(cash_breakdown, str):
			breakdown_list = frappe.parse_json(cash_breakdown)
		else:
			breakdown_list = cash_breakdown

	# Get POS Profile details
	profile = frappe.get_doc("POS Profile", pos_profile)

	try:
		# Create POS Opening Entry
		opening_entry = frappe.new_doc("POS Opening Entry")
		opening_entry.pos_profile = pos_profile
		opening_entry.user = user
		opening_entry.company = profile.company
		opening_entry.period_start_date = now_datetime()
		opening_entry.opening_amount = flt(opening_balance)

		if notes:
			opening_entry.remarks = notes

		# Add cash breakdown details if provided
		for item in breakdown_list:
			if flt(item.get("amount", 0)) > 0:
				opening_entry.append(
					"balance_details",
					{
						"mode_of_payment": item.get("mode_of_payment", "Cash"),
						"opening_amount": flt(item.get("amount", 0)),
					},
				)

		# If no breakdown provided, add default cash entry
		if not breakdown_list and flt(opening_balance) > 0:
			opening_entry.append(
				"balance_details",
				{
					"mode_of_payment": "Cash",
					"opening_amount": flt(opening_balance),
				},
			)

		opening_entry.insert(ignore_permissions=True)
		opening_entry.submit()

		return {
			"success": True,
			"session_name": opening_entry.name,
			"message": _("POS Session opened successfully"),
			"opening_balance": flt(opening_balance),
		}

	except Exception as e:
		frappe.log_error("POS Session Opening Failed", frappe.get_traceback())
		if isinstance(e, frappe.ValidationError):
			raise
		frappe.throw(_("Failed to open POS session: {0}").format(str(e)))


@frappe.whitelist(methods=["POST"])
def close_pos_session(
	session_name: str,
	closing_balance: float,
	cash_breakdown: str | list | None = None,
	notes: str | None = None,
) -> dict:
	"""
	Close an active POS session with reconciliation.

	Args:
		session_name: Name of the POS Opening Entry
		closing_balance: Actual closing cash amount
		cash_breakdown: JSON string or list of denomination breakdown
		notes: Optional closing notes

	Returns:
		dict: Success status, variance details, and summary
	"""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	user = frappe.session.user

	# Validate session exists and belongs to user
	if not session_name or not frappe.db.exists("POS Opening Entry", session_name):
		frappe.throw(_("POS Session '{0}' not found.").format(session_name or ""))

	session = frappe.get_doc("POS Opening Entry", session_name)

	if session.user != user:
		# Allow managers to close other users' sessions
		if "Sales Manager" not in frappe.get_roles(user) and "System Manager" not in frappe.get_roles(user):
			frappe.throw(_("You can only close your own sessions."))

	if session.docstatus != 1:
		frappe.throw(_("Session must be submitted before closing."))

	if session.status != "Open":
		frappe.throw(_("Session is already closed."))

	# Parse cash breakdown if provided
	breakdown_list = []
	if cash_breakdown:
		if isinstance(cash_breakdown, str):
			breakdown_list = frappe.parse_json(cash_breakdown)
		else:
			breakdown_list = cash_breakdown

	# Calculate expected closing balance
	opening_balance = flt(session.opening_amount)

	# Get total sales for this session
	sales_data = frappe.db.sql(
		"""
		SELECT COALESCE(SIM(grand_total), 0) as total
		FROM `tabSales Invoice`
		WHERE owner = %s
		AND posting_date >= DATE(%s)
		AND docstatus = 1
		AND is_pos = 1
		""",
		(
			user,
			session.period_start_date.date()
			if hasattr(session.period_start_date, "date")
			else session.period_start_date,
		),
		as_dict=True,
	)

	total_sales = flt(sales_data[0].get("total", 0)) if sales_data else 0
	expected_balance = opening_balance + total_sales
	variance = flt(closing_balance) - expected_balance

	try:
		# Create POS Closing Entry
		closing_entry = frappe.new_doc("POS Closing Entry")
		closing_entry.pos_opening_entry = session_name
		closing_entry.pos_profile = session.pos_profile
		closing_entry.user = user
		closing_entry.company = session.company
		closing_entry.period_end_date = now_datetime()
		closing_entry.grand_total = flt(closing_balance)
		closing_entry.net_total = flt(closing_balance)
		closing_entry.closing_amount = flt(closing_balance)
		closing_entry.opening_amount = opening_balance

		if notes:
			closing_entry.remarks = notes

		# Add cash breakdown details
		for item in breakdown_list:
			if flt(item.get("amount", 0)) > 0:
				closing_entry.append(
					"payment_reconciliation",
					{
						"mode_of_payment": item.get("mode_of_payment", "Cash"),
						"opening_amount": flt(item.get("opening_amount", 0)),
						"closing_amount": flt(item.get("amount", 0)),
						"expected_amount": flt(item.get("expected_amount", item.get("amount", 0))),
					},
				)

		# If no breakdown provided, add default cash entry
		if not breakdown_list and flt(closing_balance) > 0:
			closing_entry.append(
				"payment_reconciliation",
				{
					"mode_of_payment": "Cash",
					"opening_amount": opening_balance,
					"closing_amount": flt(closing_balance),
					"expected_amount": expected_balance,
				},
			)

		closing_entry.insert(ignore_permissions=True)
		closing_entry.submit()

		# Update session status
		session.db_set("status", "Closed")

		# Determine variance status
		variance_status = "balanced"
		if variance > 0:
			variance_status = "excess"
		elif variance < 0:
			variance_status = "shortage"

		return {
			"success": True,
			"closing_entry": closing_entry.name,
			"message": _("POS Session closed successfully"),
			"opening_balance": opening_balance,
			"total_sales": total_sales,
			"closing_balance": flt(closing_balance),
			"expected_balance": expected_balance,
			"variance": variance,
			"variance_status": variance_status,
		}

	except Exception as e:
		frappe.log_error("POS Session Closing Failed", frappe.get_traceback())
		if isinstance(e, frappe.ValidationError):
			raise
		frappe.throw(_("Failed to close POS session: {0}").format(str(e)))


@frappe.whitelist()
def get_session_sales(session_name: str) -> dict:
	"""
	Get all sales for a specific POS session.

	Args:
		session_name: Name of the POS Opening Entry

	Returns:
		dict: List of sales invoices for the session
	"""
	frappe.only_for(["Sales User", "Sales Manager", "System Manager"])

	if not session_name or not frappe.db.exists("POS Opening Entry", session_name):
		frappe.throw(_("POS Session '{0}' not found.").format(session_name or ""))

	session = frappe.get_doc("POS Opening Entry", session_name)

	# Get all sales invoices for this session
	sales = frappe.get_all(
		"Sales Invoice",
		filters={
			"owner": session.user,
			"posting_date": [
				">=",
				session.period_start_date.date()
				if hasattr(session.period_start_date, "date")
				else session.period_start_date,
			],
			"docstatus": 1,
			"is_pos": 1,
		},
		fields=[
			"name",
			"customer",
			"posting_date",
			"posting_time",
			"grand_total",
			"status",
			"currency",
		],
		order_by="posting_date, posting_time",
	)

	# Calculate totals
	total = sum(flt(s.get("grand_total", 0)) for s in sales)

	return {
		"session_name": session_name,
		"sales": sales,
		"total_count": len(sales),
		"total_amount": total,
	}
