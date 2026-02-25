# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt

VALID_CALC_TYPES = ("Flat Rate", "By Discount Range", "By Profit Margin", "By Sale Amount")


class CommissionRule(Document):
	def validate(self):
		self._validate_calculation_type()
		self._validate_flat_rate()
		self._validate_single_default()

	def _validate_calculation_type(self):
		if self.calculation_type not in VALID_CALC_TYPES:
			frappe.throw(f"Invalid calculation type. Must be one of: {', '.join(VALID_CALC_TYPES)}")

	def _validate_flat_rate(self):
		if self.calculation_type == "Flat Rate":
			rate = flt(self.flat_rate)
			if rate <= 0 or rate > 100:
				frappe.throw("Flat rate must be between 0% and 100%.")

	def _validate_single_default(self):
		if self.is_default:
			existing = frappe.get_all(
				"Commission Rule",
				filters={"is_default": 1, "name": ["!=", self.name]},
				limit=1,
			)
			if existing:
				frappe.throw(
					f"'{existing[0].name}' is already the default rule. "
					"Only one default commission rule is allowed."
				)
