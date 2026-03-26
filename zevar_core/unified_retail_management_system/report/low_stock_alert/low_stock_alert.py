# Copyright (c) 2025, Zevar Core
# License: GNU General Public License v3.0


import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	"""
	Execute the Low Stock Alert Report.

	Returns items with low stock levels for reordering alerts.
	"""
	columns = [
		{
			"fieldname": "item_code",
			"label": _("Item Code"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 120,
		},
		{
			"fieldname": "item_name",
			"label": _("Item Name"),
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"fieldname": "item_group",
			"label": _("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 120,
		},
		{
			"fieldname": "warehouse",
			"label": _("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 120,
		},
		{
			"fieldname": "actual_qty",
			"label": _("Actual Qty"),
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"fieldname": "reorder_level",
			"label": _("Reorder Level"),
			"fieldtype": "Float",
			"width": 100,
		},
		{
			"fieldname": "shortage_qty",
			"label": _("Shortage"),
			"fieldtype": "Float",
			"width": 80,
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 80,
		},
		{
			"fieldname": "last_updated",
			"label": _("Last Updated"),
			"fieldtype": "Datetime",
			"width": 120,
		},
	]

	data = []
	filters = filters or {}
	warehouse = filters.get("warehouse")

	warehouse_filter = ""
	if warehouse:
		warehouse_filter = "AND b.warehouse = %(warehouse)s"

	# Get items with low stock
	items = frappe.db.sql(  # nosemgrep
		f"""
		SELECT
			i.name as item_code,
			i.item_name,
			i.item_group,
			b.warehouse,
			b.actual_qty,
			b.projected_qty,
			b.reserved_qty,
			(b.actual_qty - COALESCE(b.reserved_qty, 0)) as reorder_level,
			CASE
				WHEN i.item_group IN ('Raw Materials', 'Gold', 'Diamond') THEN 5
				ELSE 10
			END as shortage_qty,
			CASE
				WHEN b.projected_qty IS NOT NULL AND b.actual_qty <= 0 THEN 'Critical'
				WHEN b.actual_qty <= (b.projected_qty * 0.5) THEN 'Low'
				ELSE 'Normal'
			END as status
		FROM `tabItem` i
		LEFT JOIN `tabBin` b ON b.item_code = i.item_code
		WHERE i.is_stock_item = 1
			AND i.disabled = 0
			{warehouse_filter}
		ORDER BY shortage_qty DESC, b.warehouse
		""",
		{"warehouse": warehouse} if warehouse else {},
		as_dict=1,
	)

	for item in items:
		data.append(
			{
				"item_code": item.get("item_code"),
				"item_name": item.get("item_name"),
				"item_group": item.get("item_group"),
				"warehouse": item.get("warehouse"),
				"actual_qty": flt(item.get("actual_qty")),
				"reorder_level": flt(item.get("reorder_level")),
				"shortage_qty": flt(item.get("shortage_qty")),
				"status": item.get("status"),
				"last_updated": frappe.utils.now_datetime(),
			}
		)

	return columns, data


def get_alert_summary(filters=None):
	"""Return summary statistics for the alert."""
	filters = filters or {}
	warehouse = filters.get("warehouse")

	warehouse_filter = ""
	if warehouse:
		warehouse_filter = "AND b.warehouse = %(warehouse)s"

	summary = frappe.db.sql(  # nosemgrep
		f"""
		SELECT
			COUNT(*) as total_items,
			SUM(CASE WHEN shortage_qty > 0 THEN 1 ELSE 0 END) as critical_items,
			SUM(shortage_qty) as total_shortage
		FROM (
			SELECT
				i.name as item_code,
				i.item_name,
				i.item_group,
				b.warehouse,
				b.actual_qty,
				b.projected_qty,
				b.reserved_qty,
				(b.actual_qty - COALESCE(b.reserved_qty, 0)) as reorder_level,
				CASE
					WHEN i.item_group IN ('Raw Materials', 'Gold', 'Diamond') THEN 5
					ELSE 10
				END as shortage_qty,
				CASE
					WHEN b.projected_qty IS NOT NULL AND b.actual_qty <= 0 THEN 1
					WHEN b.actual_qty <= (b.projected_qty * 0.5) THEN 1
					ELSE 0
				END as needs_reorder
			FROM `tabItem` i
			LEFT JOIN `tabBin` b ON b.item_code = i.item_code
			WHERE i.is_stock_item = 1
				AND i.disabled = 0
				{warehouse_filter}
		) items
		""",
		{"warehouse": warehouse} if warehouse else {},
		as_dict=1,
	)

	if summary:
		summary = summary[0]
		return {
			"total_items": summary.get("total_items", 0),
			"critical_items": summary.get("critical_items", 0),
			"total_shortage": summary.get("total_shortage", 0),
			"needs_reorder": summary.get("needs_reorder", 0),
		}

	return {"total_items": 0, "critical_items": 0, "total_shortage": 0, "needs_reorder": 0}
