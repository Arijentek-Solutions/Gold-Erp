# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class WarrantySku(Document):
	def validate(self):
		self._validate_price()
		self._validate_duration()

	def _validate_price(self):
		if flt(self.price) <= 0:
			frappe.throw("Warranty price must be greater than zero.")

	def _validate_duration(self):
		if self.duration_months not in ("6", "12", "24", "36"):
			frappe.throw("Duration must be 6, 12, 24, or 36 months.")
