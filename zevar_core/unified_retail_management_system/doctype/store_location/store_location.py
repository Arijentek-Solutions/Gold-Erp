# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, today


class StoreLocation(Document):
	def validate(self):
		self._validate_store_code()
		self._validate_warehouse()
		self._validate_tax_config()

	def _validate_store_code(self):
		if not self.store_code:
			frappe.throw(frappe._("Store Code is required."))
		if len(self.store_code) > 20:
			frappe.throw(frappe._("Store Code must be at most 20 characters."))
		if not self.store_name:
			frappe.throw(frappe._("Store Name is required."))

	def _validate_warehouse(self):
		if self.default_warehouse:
			if not frappe.db.exists("Warehouse", self.default_warehouse):
				frappe.throw(
					frappe._("Default Warehouse '{0}' not found.").format(self.default_warehouse),
					frappe.ValidationError,
				)

	def _validate_tax_config(self):
		if self.county_tax_rate is not None:
			if flt(self.county_tax_rate) < 0:
				frappe.throw(frappe._("County Tax Rate should be between 0% and 100%."))
			if flt(self.county_tax_rate) > 100:
				frappe.throw(frappe._("County Tax Rate cannot exceed 100%."))
		if self.tax_template:
			if not frappe.db.exists("Sales Taxes and Charges Template", self.tax_template):
				frappe.throw(
					frappe._("Tax Template '{0}' not found.").format(self.tax_template),
					frappe.ValidationError,
				)
