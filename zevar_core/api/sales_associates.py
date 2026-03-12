"""
Sales Associates API - Employee management for POS
"""

from typing import Any

import frappe
from frappe import _


@frappe.whitelist()
def get_sales_associates(active_only: bool = True) -> list[dict[str, Any]]:
	"""
	Get list of employees who can be sales associates.

	Args:
		active_only: Only return active employees

	Returns:
		List of employees with id, name, and designation
	"""
	filters = {}
	if active_only:
		filters["status"] = "Active"

	employees = frappe.get_all(
		"Employee",
		filters=filters,
		fields=["name", "employee_name", "designation", "department", "status"],
		order_by="employee_name asc",
	)

	return employees


@frappe.whitelist(methods=["POST"])
def create_sales_associate(
	employee_name: str,
	designation: str = "Sales Associate",
	department: str | None = None,
	email: str | None = None,
	phone: str | None = None,
) -> dict[str, Any]:
	"""
	Create a new employee for sales associate role.

	Args:
		employee_name: Full name of the employee
		designation: Job title
		department: Department name
		email: Employee email
		phone: Phone number

	Returns:
		Created employee details
	"""
	if not frappe.has_permission("Employee", "create"):
		frappe.throw(_("You don't have permission to create Employees"), frappe.PermissionError)

	if not employee_name or not employee_name.strip():
		frappe.throw(_("Employee name is required"))

	# Create employee
	emp = frappe.new_doc("Employee")
	emp.employee_name = employee_name.strip()
	emp.designation = designation
	emp.status = "Active"

	if department:
		emp.department = department
	if email:
		emp.personal_email = email
	if phone:
		emp.cell_number = phone

	emp.insert(ignore_permissions=True)

	return {
		"success": True,
		"name": emp.name,
		"employee_name": emp.employee_name,
		"designation": emp.designation,
		"message": _("Employee {0} created successfully").format(emp.name),
	}
