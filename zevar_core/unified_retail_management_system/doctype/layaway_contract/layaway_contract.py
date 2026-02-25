# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class LayawayContract(Document):
	def validate(self):
		self._validate_amounts()
		self._validate_deposit_minimum()
		self._validate_duration()

	def _validate_amounts(self):
		if flt(self.total_amount) <= 0:
			frappe.throw("Total amount must be greater than zero.")

		if flt(self.deposit_amount) <= 0:
			frappe.throw("Deposit amount must be greater than zero.")

		if flt(self.balance_amount) < 0:
			frappe.throw("Balance amount cannot be negative.")

	def _validate_deposit_minimum(self):
		"""Deposit must be at least 10% of total amount."""
		minimum = flt(self.total_amount) * 0.10
		if flt(self.deposit_amount) < minimum:
			frappe.throw(
				f"Deposit must be at least 10% of total amount "
				f"(minimum ${minimum:,.2f}, got ${flt(self.deposit_amount):,.2f})."
			)

	def _validate_duration(self):
		if self.maximum_duration_months not in ("6", "9", "12"):
			frappe.throw("Duration must be 6, 9, or 12 months.")
