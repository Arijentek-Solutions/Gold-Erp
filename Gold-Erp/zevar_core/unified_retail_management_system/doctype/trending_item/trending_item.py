# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TrendingItem(Document):
	def before_save(self):
		# Auto-set created_by on first save
		if not self.created_by:
			self.created_by = frappe.session.user

	def validate(self):
		# Validate URL format
		if self.product_url and not self.product_url.startswith(("http://", "https://")):
			frappe.throw(frappe._("Product URL must start with http:// or https://"))

		if self.image_url and not self.image_url.startswith(("http://", "https://")):
			frappe.throw(frappe._("Image URL must start with http:// or https://"))

	@staticmethod
	def get_trending_items(category=None, limit=20):
		"""Get active trending items, optionally filtered by category"""
		filters = {"is_active": 1}
		if category and category != "all":
			filters["category"] = category

		items = frappe.get_all(
			"Trending Item",
			filters=filters,
			fields=[
				"name",
				"item_name",
				"category",
				"partner",
				"price",
				"product_url",
				"image_url",
				"is_hot",
				"view_count",
			],
			order_by="is_hot desc, view_count desc, modified desc",
			limit_page_length=limit,
		)

		return items

	@staticmethod
	def track_click(item_name):
		"""Track when a trending item is clicked"""
		if frappe.db.exists("Trending Item", item_name):
			doc = frappe.get_doc("Trending Item", item_name)
			doc.view_count = (doc.view_count or 0) + 1
			doc.last_clicked = frappe.utils.now()
			doc.save(ignore_permissions=True)
			frappe.db.commit()  # nosemgrep: frappe-semgrep-rules.rules.frappe-manual-commit
			return True
		return False
