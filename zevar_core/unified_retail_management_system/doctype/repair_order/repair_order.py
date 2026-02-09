# Copyright (c) 2026, Zevar Core and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RepairOrder(Document):
	def validate(self):
		self.set_total_cost()

	def set_total_cost(self):
		parts_total = sum((row.amount or 0.0) for row in (self.parts or []))
		if parts_total:
			self.material_cost = parts_total
		
		# Ensure we treat None as 0.0 for calculations
		labor = self.labor_cost or 0.0
		material = self.material_cost or 0.0
		self.total_cost = labor + material
		
		if not self.received_date and self.is_new():
			from frappe.utils import now
			self.received_date = now()

	def on_update(self):
		# When status is Delivered, create Stock Entry (Material Issue) for parts consumed (once)
		if self.status == "Delivered" and self.parts and not self.get("parts_stock_created"):
			self._create_parts_stock_entry()

	def _create_parts_stock_entry(self):
		"""Create Material Issue stock entry for parts consumed in this repair."""
		if not self.parts:
			return
		company = frappe.defaults.get_user_default("Company") or frappe.db.get_single_value("Global Defaults", "default_company")
		if not company:
			return
		warehouse = self.warehouse
		items = []
		for row in self.parts:
			wh = row.warehouse or warehouse
			if not wh or not row.item_code or (row.qty or 0) <= 0:
				continue
			items.append({
				"item_code": row.item_code,
				"qty": row.qty,
				"warehouse": wh,
			})
		if not items:
			return
		se = frappe.new_doc("Stock Entry")
		se.stock_entry_type = "Material Issue"
		se.company = company
		for it in items:
			se.append("items", {
				"item_code": it["item_code"],
				"qty": it["qty"],
				"s_warehouse": it["warehouse"],
			})
		se.flags.ignore_permissions = True
		se.submit()
		frappe.db.set_value("Repair Order", self.name, "parts_stock_created", 1)
