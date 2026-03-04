# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_months, flt


class LayawayContract(Document):
	def validate(self):
		self._set_target_completion_date()
		self._validate_amounts()
		self._validate_deposit_minimum()
		self._validate_duration()

	def _set_target_completion_date(self):
		"""Auto-calculate target completion from contract_date + duration."""
		if self.contract_date and self.maximum_duration_months:
			self.target_completion_date = add_months(self.contract_date, int(self.maximum_duration_months))

	def _validate_amounts(self):
		if flt(self.total_amount) <= 0:
			frappe.throw(frappe._("Total amount must be greater than zero."))

		if flt(self.deposit_amount) <= 0:
			frappe.throw(frappe._("Deposit amount must be greater than zero."))

		if flt(self.balance_amount) < 0:
			frappe.throw(frappe._("Balance amount cannot be negative."))

	def _validate_deposit_minimum(self):
		"""Deposit must be at least 10% of total amount."""
		minimum = flt(self.total_amount) * 0.10
		if flt(self.deposit_amount) < minimum:
			frappe.throw(
				frappe._(
					"Deposit must be at least 10% of total amount (minimum ${0:,.2f}, got ${1:,.2f})."
				).format(minimum, flt(self.deposit_amount))
			)

	def _validate_duration(self):
		if self.maximum_duration_months not in ("3", "6", "9", "12"):
			frappe.throw(frappe._("Duration must be 3, 6, 9, or 12 months."))
