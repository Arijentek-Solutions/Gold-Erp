"""
Tax API - Store-based tax rate lookups
"""

import frappe


@frappe.whitelist()
def get_tax_details_by_store(store_code: str) -> dict:
	"""Return the tax template and county tax rate for a Store Location."""
	if not frappe.db.exists("Store Location", store_code):
		frappe.throw(f"Store Location {store_code} not found")

	doc = frappe.get_doc("Store Location", store_code)
	return {
		"store_code": doc.store_code,
		"county": doc.county,
		"county_tax_rate": doc.county_tax_rate,
		"tax_template": doc.tax_template,
	}


@frappe.whitelist()
def get_tax_details_by_warehouse(warehouse: str) -> dict:
	"""Resolve Store Location from a warehouse and return its tax details."""
	store = frappe.get_all(
		"Store Location",
		filters={"default_warehouse": warehouse, "is_active": 1},
		fields=["name", "county", "county_tax_rate", "tax_template"],
		limit=1,
	)
	if not store:
		return {}

	s = store[0]
	return {
		"store_code": s.name,
		"county": s.county,
		"county_tax_rate": s.county_tax_rate,
		"tax_template": s.tax_template,
	}
