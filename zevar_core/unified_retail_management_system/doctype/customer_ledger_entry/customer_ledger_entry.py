# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt, today

VALID_ENTRY_TYPES = ("Purchase", "Payment", "Finance Charge", "Adjustment", "Credit")


class CustomerLedgerEntry(Document):
	def validate(self):
		self._validate_entry_type()
		self._validate_amounts()

	def before_insert(self):
		if not self.entry_date:
			self.entry_date = today()

	def _validate_entry_type(self):
		if self.entry_type and self.entry_type not in VALID_ENTRY_TYPES:
			frappe.throw(
				frappe._("Invalid entry type: {0}. Must be one of: {1}").format(
					self.entry_type, ", ".join(VALID_ENTRY_TYPES)
				)
			)
		if self.reference_name and not self.reference_type:
			frappe.throw(frappe._("Reference type is required when reference_name is set."))

	def _validate_amounts(self):
		if flt(self.debit) < 0:
			frappe.throw(frappe._("Debit amount cannot be negative."))
		if flt(self.credit) < 0:
			frappe.throw(frappe._("Credit amount cannot be negative."))
		if flt(self.debit) == 0 and flt(self.credit) == 0:
			frappe.throw(frappe._("Entry must have either a debit or credit amount."))
