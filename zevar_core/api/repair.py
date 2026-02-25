"""
Repair API - Repair orders, types, and customer repair history
"""

from typing import Any, Optional, Union

import frappe
from frappe import _
from frappe.utils import escape_html


@frappe.whitelist()
def get_repair_types(active_only: bool = True) -> list[dict[str, Any]]:
	if not frappe.has_permission("Repair Type", "read"):
		frappe.throw(_("Insufficient permissions to access Repair Types"), frappe.PermissionError)

	filters = {"is_active": 1} if active_only else {}
	return frappe.get_all(
		"Repair Type",
		filters=filters,
		fields=["name", "repair_name", "category", "base_price", "estimated_days", "description"],
		order_by="category asc, repair_name asc",
	)


@frappe.whitelist()
def get_repair_orders(
	status: str | None = None,
	warehouse: str | None = None,
	search_term: str | None = None,
	start: int = 0,
	page_length: int = 20,
	customer: str | None = None,
	handled_by: str | None = None,
) -> list[dict[str, Any]]:
	if not frappe.has_permission("Repair Order", "read"):
		frappe.throw(_("Insufficient permissions to access Repair Orders"), frappe.PermissionError)

	filters = []
	if status:
		filters.append(["status", "=", status])
	if warehouse:
		filters.append(["warehouse", "=", warehouse])
	if customer:
		filters.append(["customer", "=", customer])
	if handled_by:
		filters.append(["handled_by", "=", handled_by])
	if search_term:
		filters.append(["name", "like", f"%{search_term}%"])

	orders = frappe.get_list(
		"Repair Order",
		filters=filters or None,
		fields=[
			"name",
			"status",
			"priority",
			"customer",
			"customer_phone",
			"handled_by",
			"repair_type",
			"item_description",
			"estimated_cost",
			"total_cost",
			"payment_status",
			"received_date",
			"promised_date",
			"completed_date",
			"delivered_date",
			"assigned_to",
			"warehouse",
		],
		order_by="modified desc",
		start=int(start),
		page_length=int(page_length),
	)

	# Enrichment
	for o in orders:
		if o.get("customer"):
			o["customer_name"] = frappe.db.get_value("Customer", o["customer"], "customer_name")
		if o.get("repair_type"):
			o["repair_type_name"] = frappe.db.get_value("Repair Type", o["repair_type"], "repair_name")
		if o.get("handled_by"):
			o["handled_by_name"] = frappe.db.get_value("User", o["handled_by"], "full_name")

	return orders


@frappe.whitelist()
def get_repair_stats(warehouse: str | None = None) -> dict[str, int]:
	if not frappe.has_permission("Repair Order", "read"):
		frappe.throw(_("Insufficient permissions to access Repair Stats"), frappe.PermissionError)

	filters = {}
	if warehouse:
		filters["warehouse"] = warehouse

	statuses = [
		"Received",
		"Estimated",
		"Approved",
		"In Progress",
		"Quality Check",
		"Ready for Pickup",
		"Delivered",
		"Cancelled",
	]
	counts = {}
	for s in statuses:
		counts[s] = frappe.db.count("Repair Order", filters={**filters, "status": s})
	counts["total"] = frappe.db.count("Repair Order", filters=filters)
	return counts


@frappe.whitelist()
def create_repair_order(
	customer: str,
	repair_type: str,
	item_description: str | None = None,
	customer_phone: str | None = None,
	handled_by: str | None = None,
	warehouse: str | None = None,
	customer_notes: str | None = None,
	estimated_cost: float | None = None,
	priority: str = "Medium",
	**kwargs: Any,
) -> dict[str, Any]:
	if not frappe.has_permission("Repair Order", "create"):
		frappe.throw(_("Insufficient permissions to create Repair Order"), frappe.PermissionError)

	doc = frappe.new_doc("Repair Order")
	doc.customer = customer
	doc.repair_type = repair_type
	doc.status = "Received"
	doc.item_description = item_description
	doc.customer_phone = customer_phone
	doc.handled_by = handled_by or frappe.session.user
	doc.warehouse = warehouse
	doc.customer_notes = customer_notes
	doc.estimated_cost = estimated_cost
	doc.priority = priority

	for key, value in kwargs.items():
		if hasattr(doc, key):
			setattr(doc, key, value)

	doc.insert()
	return {"name": doc.name, "status": doc.status}


@frappe.whitelist()
def update_repair_status(name: str, status: str, work_notes: str | None = None) -> dict[str, str]:
	if not frappe.has_permission("Repair Order", "write", doc=name):
		frappe.throw(_("Insufficient permissions to update Repair Order"), frappe.PermissionError)

	doc = frappe.get_doc("Repair Order", name)
	doc.status = status

	if work_notes is not None:
		doc.work_notes = (doc.work_notes or "") + "\n" + work_notes if doc.work_notes else work_notes

	if status == "Delivered":
		from frappe.utils import now

		doc.delivered_date = now()

	if (
		status in ("In Progress", "Quality Check", "Ready for Pickup")
		and not doc.completed_date
		and status == "Ready for Pickup"
	):
		from frappe.utils import now

		doc.completed_date = now()

	doc.save()
	return {"name": doc.name, "status": doc.status}


@frappe.whitelist()
def get_repair_order_details(name: str) -> dict[str, Any]:
	if not frappe.has_permission("Repair Order", "read", doc=name):
		frappe.throw(_("Insufficient permissions to view Repair Order"), frappe.PermissionError)

	doc = frappe.get_doc("Repair Order", name)
	doc_dict = doc.as_dict()

	if doc_dict.get("customer"):
		doc_dict["customer_name"] = frappe.db.get_value("Customer", doc_dict["customer"], "customer_name")
	if doc_dict.get("repair_type"):
		doc_dict["repair_type_name"] = frappe.db.get_value(
			"Repair Type", doc_dict["repair_type"], "repair_name"
		)
	if doc_dict.get("handled_by"):
		doc_dict["handled_by_name"] = frappe.db.get_value("User", doc_dict["handled_by"], "full_name")

	return doc_dict


@frappe.whitelist()
def get_customer_repair_history(customer: str, limit: int = 20) -> list[dict[str, Any]]:
	if not frappe.has_permission("Repair Order", "read"):
		frappe.throw(_("Insufficient permissions to access Repair History"), frappe.PermissionError)

	orders = frappe.get_all(
		"Repair Order",
		filters={"customer": customer},
		fields=[
			"name",
			"status",
			"repair_type",
			"item_description",
			"total_cost",
			"received_date",
			"delivered_date",
		],
		order_by="received_date desc",
		limit=int(limit),
	)
	for o in orders:
		if o.get("repair_type"):
			o["repair_type_name"] = frappe.db.get_value("Repair Type", o["repair_type"], "repair_name")
	return orders


@frappe.whitelist()
def get_repair_receipt_html(name: str) -> str:
	"""Return HTML for repair claim ticket / receipt (for print)."""
	if not frappe.has_permission("Repair Order", "read", doc=name):
		frappe.throw(_("Insufficient permissions to view receipt"), frappe.PermissionError)

	doc = frappe.get_doc("Repair Order", name)
	d = doc.as_dict()
	d["customer_name"] = (
		frappe.db.get_value("Customer", doc.customer, "customer_name") if doc.customer else ""
	)
	d["repair_type_name"] = (
		frappe.db.get_value("Repair Type", doc.repair_type, "repair_name") if doc.repair_type else ""
	)
	d["handled_by_name"] = frappe.db.get_value("User", doc.handled_by, "full_name") if doc.handled_by else ""

	# Escape all user-provided fields to prevent XSS
	safe = {k: escape_html(str(v)) if v else "" for k, v in d.items()}

	html = f"""
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Repair Receipt - {safe.get("name")}</title>
<style>
body {{ font-family: sans-serif; max-width: 400px; margin: 20px auto; padding: 16px; }}
h1 {{ font-size: 18px; border-bottom: 2px solid #333; padding-bottom: 8px; }}
table {{ width: 100%; border-collapse: collapse; }}
td {{ padding: 4px 0; }}
.label {{ font-weight: bold; color: #555; }}
</style></head><body>
<h1>ZEVAR JEWELERS - REPAIR CLAIM TICKET</h1>
<p><span class="label">Repair #:</span> {safe.get("name")}</p>
<p><span class="label">Date:</span> {safe.get("received_date")}</p>
<p><span class="label">Customer:</span> {safe.get("customer_name")}</p>
<p><span class="label">Phone:</span> {safe.get("customer_phone") or "-"}</p>
<p><span class="label">Repair Type:</span> {safe.get("repair_type_name")}</p>
<p><span class="label">Item:</span> {safe.get("item_description") or "-"}</p>
<p><span class="label">Estimated Cost:</span> ${float(d.get("estimated_cost") or 0):.2f}</p>
<p><span class="label">Handled By:</span> {safe.get("handled_by_name") or "-"}</p>
<p style="margin-top: 24px; font-size: 12px; color: #666;">Keep this ticket to pick up your item.</p>
</body></html>
"""
	return html
