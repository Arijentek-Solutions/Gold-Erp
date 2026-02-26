# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt


class SkuVendorCode(Document):
	def validate(self):
		self._validate_vendor_sku()
		self._validate_vendor_cost()
		self._validate_unique_mapping()

	def _validate_vendor_sku(self):
		if not self.vendor_sku or not self.vendor_sku.strip():
			frappe.throw(frappe._("Vendor SKU Code is required."))

	def _validate_vendor_cost(self):
		if self.vendor_cost and flt(self.vendor_cost) < 0:
			frappe.throw(frappe._("Vendor cost cannot be negative."))

	def _validate_unique_mapping(self):
		"""Ensure no duplicate item + supplier + vendor_sku combination."""
		existing = frappe.get_all(
			"SKU Vendor Code",
			filters={
				"item_code": self.item_code,
				"supplier": self.supplier,
				"vendor_sku": self.vendor_sku,
				"name": ["!=", self.name],
			},
			limit=1,
		)
		if existing:
			frappe.throw(
				frappe._(
					"A mapping for Item '{0}' + Supplier '{1}' + Vendor SKU '{2}' already exists."
				).format(self.item_code, self.supplier, self.vendor_sku)
			)
