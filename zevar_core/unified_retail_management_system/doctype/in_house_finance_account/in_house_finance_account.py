# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class InHouseFinanceAccount(Document):
	def validate(self):
		self._validate_credit_limit()
		self._validate_interest_rate()
		self._validate_balances()

	def _validate_credit_limit(self):
		if flt(self.credit_limit) <= 0:
			frappe.throw("Credit limit must be greater than zero.")

	def _validate_interest_rate(self):
		rate = flt(self.interest_rate)
		if rate < 0 or rate > 100:
			frappe.throw("Interest rate must be between 0% and 100%.")

	def _validate_balances(self):
		self.available_credit = flt(self.credit_limit) - flt(self.current_balance)

		if flt(self.current_balance) < 0:
			frappe.throw("Current balance cannot be negative.")
