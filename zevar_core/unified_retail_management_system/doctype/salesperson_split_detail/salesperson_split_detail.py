# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SalespersonSplitDetail(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	employee: str  # Link[Employee]
	split_percent: float  # Percent

	# end: auto-generated types

	pass
