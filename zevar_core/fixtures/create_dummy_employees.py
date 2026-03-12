#!/usr/bin/env python3
"""
Create dummy sales associates for testing.

Run with: bench --site zevar.localhost execute zevar_core.fixtures.create_dummy_employees.create_employees
"""

import frappe
from frappe import _


def create_employees():
	"""Create dummy sales associate employees for testing."""

	dummy_employees = [
		{
			"first_name": "John",
			"last_name": "Smith",
			"gender": "Male",
			"date_of_birth": "1990-05-15",
			"date_of_joining": "2023-01-15",
			"designation": "Sales Associate",
			"department": "Sales",
			"personal_email": "john.smith@zevar.com",
			"cell_number": "555-0101",
		},
		{
			"first_name": "Sarah",
			"last_name": "Johnson",
			"gender": "Female",
			"date_of_birth": "1988-08-22",
			"date_of_joining": "2022-06-01",
			"designation": "Senior Sales Associate",
			"department": "Sales",
			"personal_email": "sarah.johnson@zevar.com",
			"cell_number": "555-0102",
		},
		{
			"first_name": "Michael",
			"last_name": "Brown",
			"gender": "Male",
			"date_of_birth": "1992-03-10",
			"date_of_joining": "2023-03-20",
			"designation": "Sales Associate",
			"department": "Sales",
			"personal_email": "michael.brown@zevar.com",
			"cell_number": "555-0103",
		},
		{
			"first_name": "Emily",
			"last_name": "Davis",
			"gender": "Female",
			"date_of_birth": "1985-11-30",
			"date_of_joining": "2021-09-15",
			"designation": "Sales Manager",
			"department": "Sales",
			"personal_email": "emily.davis@zevar.com",
			"cell_number": "555-0104",
		},
		{
			"first_name": "David",
			"last_name": "Wilson",
			"gender": "Male",
			"date_of_birth": "1994-07-08",
			"date_of_joining": "2024-01-10",
			"designation": "Sales Associate",
			"department": "Sales",
			"personal_email": "david.wilson@zevar.com",
			"cell_number": "555-0105",
		},
	]

	created = []
	skipped = []

	for emp_data in dummy_employees:
		full_name = f"{emp_data['first_name']} {emp_data['last_name']}"

		# Check if employee already exists by name
		existing = frappe.db.exists("Employee", {"first_name": emp_data["first_name"], "last_name": emp_data["last_name"]})
		if existing:
			skipped.append(full_name)
			print(f"Skipped: {full_name} (already exists with ID: {existing})")
			continue

		try:
			emp = frappe.new_doc("Employee")
			emp.first_name = emp_data["first_name"]
			emp.last_name = emp_data["last_name"]
			emp.gender = emp_data["gender"]
			emp.date_of_birth = emp_data["date_of_birth"]
			emp.date_of_joining = emp_data["date_of_joining"]
			emp.designation = emp_data["designation"]
			emp.department = emp_data["department"]
			emp.personal_email = emp_data["personal_email"]
			emp.cell_number = emp_data["cell_number"]
			emp.status = "Active"
			emp.insert(ignore_permissions=True)

			created.append({"name": emp.name, "employee_name": emp.employee_name})
			print(f"Created: {emp.employee_name} (ID: {emp.name})")
		except Exception as e:
			print(f"Error creating {full_name}: {e}")

	frappe.db.commit()

	print(f"\nSummary:")
	print(f"  Created: {len(created)} employees")
	print(f"  Skipped: {len(skipped)} employees")

	return {"created": created, "skipped": skipped}


if __name__ == "__main__":
	create_employees()
