"""
Add database indexes for frequently filtered catalog fields.

This patch adds indexes to improve query performance for:
- Item catalog filtering
- Employee check-in queries
- Sales Invoice reporting
"""

import frappe


def execute():
	"""Add indexes for performance optimization."""

	# Item catalog indexes (custom fields frequently filtered)
	item_indexes = [
		("custom_metal_type", "tabItem"),
		("custom_purity", "tabItem"),
		("custom_product_type", "tabItem"),
		("custom_jewelry_type", "tabItem"),
		("custom_is_featured", "tabItem"),
		("custom_is_trending", "tabItem"),
	]

	# Employee Checkin indexes
	checkin_indexes = [
		("employee", "tabEmployee Checkin"),
		("time", "tabEmployee Checkin"),
		("log_type", "tabEmployee Checkin"),
	]

	# Sales Invoice indexes
	invoice_indexes = [
		("customer", "tabSales Invoice"),
		("posting_date", "tabSales Invoice"),
		("is_pos", "tabSales Invoice"),
	]

	# Sales Commission Split indexes
	commission_indexes = [
		("employee", "tabSales Commission Split"),
		("posting_date", "tabSales Commission Split"),
		("sales_invoice", "tabSales Commission Split"),
	]

	all_indexes = item_indexes + checkin_indexes + invoice_indexes + commission_indexes

	for field, table in all_indexes:
		index_name = f"idx_{table.lower()}_{field}"
		try:
			# Check if index already exists
			existing = frappe.db.sql(
				"""
                SELECT INDEX_NAME
                FROM INFORMATION_SCHEMA.STATISTICS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = %s
                AND INDEX_NAME = %s
            """,
				(table, index_name),
			)

			if not existing:
				frappe.db.sql(f"CREATE INDEX `{index_name}` ON `{table}` (`{field}`)") # nosemgrep
				print(f"Created index: {index_name} on {table}.{field}")
			else:
				print(f"Index already exists: {index_name}")
		except Exception as e:
			print(f"Error creating index {index_name}: {e}")

	frappe.db.commit() # nosemgrep
	print("Index creation complete.")
