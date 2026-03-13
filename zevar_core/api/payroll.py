"""
Payroll API - Salary slips and payroll information
"""

import frappe
from frappe import _


@frappe.whitelist()
def get_salary_slips(year: int | None = None, limit: int = 12):
	"""
	Get salary slips for current employee.

	Args:
	    year: Filter by year (optional, defaults to current year)
	    limit: Maximum number of slips to return

	Returns:
	    List of salary slips with details
	"""
	employee = _get_current_employee_id()
	if not employee:
		return []

	from frappe.utils import getdate

	year = year or getdate().year

	salary_slips = frappe.get_all(
		"Salary Slip",
		filters={"employee": employee, "docstatus": 1, "start_date": (">=", f"{year}-01-01")},
		fields=[
			"name",
			"start_date",
			"end_date",
			"posting_date",
			"gross_pay",
			"net_pay",
			"total_deduction",
			"currency",
		],
		order_by="start_date desc",
		limit=limit,
	)

	if not salary_slips:
		return []

	# Batch fetch all earnings and deductions to avoid N+1 queries
	slip_names = [s.name for s in salary_slips]
	all_details = frappe.get_all(
		"Salary Detail",
		filters={"parent": ["in", slip_names], "parentfield": ["in", ["earnings", "deductions"]]},
		fields=["parent", "parentfield", "salary_component", "amount", "abbr", "idx"],
		order_by="parent, idx",
	)

	# Build lookup maps for earnings and deductions
	earnings_map = {}
	deductions_map = {}
	for detail in all_details:
		if detail.parentfield == "earnings":
			if detail.parent not in earnings_map:
				earnings_map[detail.parent] = []
			earnings_map[detail.parent].append(detail)
		elif detail.parentfield == "deductions":
			if detail.parent not in deductions_map:
				deductions_map[detail.parent] = []
			deductions_map[detail.parent].append(detail)

	result = []
	for slip in salary_slips:
		earnings = earnings_map.get(slip.name, [])
		deductions = deductions_map.get(slip.name, [])

		result.append(
			{
				"id": slip.name,
				"start_date": str(slip.start_date),
				"end_date": str(slip.end_date),
				"posting_date": str(slip.posting_date),
				"gross_pay": slip.gross_pay,
				"net_pay": slip.net_pay,
				"total_deduction": slip.total_deduction,
				"currency": slip.currency,
				"earnings": [
					{"component": e.salary_component, "amount": e.amount, "abbr": e.abbr} for e in earnings
				],
				"deductions": [
					{"component": d.salary_component, "amount": d.amount, "abbr": d.abbr} for d in deductions
				],
				"url": f"/app/salary-slip/{slip.name}",
			}
		)

	return result


@frappe.whitelist()
def get_salary_slip_details(slip_name: str):
	"""
	Get detailed salary slip information.

	Args:
	    slip_name: Salary Slip document name

	Returns:
	    Detailed salary slip with all components
	"""
	employee = _get_current_employee_id()
	if not employee:
		frappe.throw(_("Employee not found"))

	slip = frappe.get_doc("Salary Slip", slip_name)

	# Verify ownership
	if slip.employee != employee:
		frappe.throw(_("You can only view your own salary slips"))

	return {
		"id": slip.name,
		"employee": slip.employee,
		"employee_name": slip.employee_name,
		"start_date": str(slip.start_date),
		"end_date": str(slip.end_date),
		"posting_date": str(slip.posting_date),
		"gross_pay": slip.gross_pay,
		"net_pay": slip.net_pay,
		"total_deduction": slip.total_deduction,
		"total_earnings": slip.gross_pay,
		"currency": slip.currency,
		"earnings": [
			{"component": e.salary_component, "amount": e.amount, "abbr": e.abbr, "formula": e.formula}
			for e in slip.earnings
		],
		"deductions": [
			{"component": d.salary_component, "amount": d.amount, "abbr": d.abbr, "formula": d.formula}
			for d in slip.deductions
		],
		"leave_details": get_leave_details(slip),
		"url": f"/app/salary-slip/{slip.name}",
	}


@frappe.whitelist()
def get_payroll_summary(year: int | None = None):
	"""
	Get payroll summary for current employee.

	Args:
	    year: Filter by year (optional, defaults to current year)

	Returns:
	    Dict with YTD totals and monthly breakdown
	"""
	employee = _get_current_employee_id()
	if not employee:
		return {"total_earnings": 0, "total_deductions": 0, "total_net_pay": 0, "slips": []}

	from frappe.utils import getdate

	year = year or getdate().year

	salary_slips = frappe.get_all(
		"Salary Slip",
		filters={"employee": employee, "docstatus": 1, "start_date": (">=", f"{year}-01-01")},
		fields=["name", "start_date", "end_date", "gross_pay", "net_pay", "total_deduction"],
		order_by="start_date asc",
	)

	summary = {
		"year": year,
		"total_earnings": 0,
		"total_deductions": 0,
		"total_net_pay": 0,
		"slips": [],
		"slip_count": len(salary_slips),
	}

	for slip in salary_slips:
		summary["total_earnings"] += slip.gross_pay or 0
		summary["total_deductions"] += slip.total_deduction or 0
		summary["total_net_pay"] += slip.net_pay or 0

		summary["slips"].append(
			{
				"id": slip.name,
				"start_date": str(slip.start_date),
				"end_date": str(slip.end_date),
				"gross_pay": slip.gross_pay,
				"deductions": slip.total_deduction,
				"net_pay": slip.net_pay,
			}
		)

	return summary


def _get_current_employee_id():
	"""Get the employee ID for the current logged-in user (internal helper)."""
	return frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")


def get_leave_details(slip):
	"""Extract leave details from salary slip if available."""
	leave_details = []
	if hasattr(slip, "leave_details") and slip.leave_details:
		for leave in slip.leave_details:
			leave_details.append(
				{
					"leave_type": leave.leave_type,
					"leaves_allocated": leave.leaves_allocated,
					"leaves_taken": leave.leaves_taken,
					"leaves_remaining": leave.leaves_remaining,
				}
			)
	return leave_details
