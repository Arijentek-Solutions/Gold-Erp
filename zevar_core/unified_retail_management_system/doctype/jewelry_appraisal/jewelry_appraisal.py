# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class JewelryAppraisal(Document):
	def validate(self):
		self._validate_appraised_value()
		self._validate_weight()
		self._validate_replacement_values()

	def _validate_appraised_value(self):
		if flt(self.appraised_value) <= 0:
			frappe.throw(frappe._("Appraised value must be greater than zero."))

	def _validate_weight(self):
		if self.total_weight_grams and flt(self.total_weight_grams) <= 0:
			frappe.throw(frappe._("Total weight must be greater than zero."))

	def _validate_replacement_values(self):
		"""Replacement and insurance values should not be less than appraised value."""
		appraised = flt(self.appraised_value)
		if self.replacement_value and flt(self.replacement_value) < appraised:
			frappe.throw(frappe._("Replacement value should not be less than appraised value."))
		if self.insurance_value and flt(self.insurance_value) < appraised:
			frappe.throw(frappe._("Insurance value should not be less than appraised value."))
