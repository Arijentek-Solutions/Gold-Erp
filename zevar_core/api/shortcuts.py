"""
Zevar Desk Shortcuts API

Provides endpoints for the custom desk page to fetch shortcuts,
quick stats, and recent activity.
"""

import frappe
from frappe import _


@frappe.whitelist()
def get_desk_shortcuts():
	"""
	Get shortcuts visible to current user based on roles.

	Returns:
		list: List of shortcut dictionaries with all display properties
	"""
	# Try to get from cache first
	cache_key = "zevar_desk_shortcuts"
	cached = frappe.cache.get_value(cache_key)
	if cached:
		return filter_by_roles(cached)

	# Fetch from database
	shortcuts = frappe.get_all(
		"Zevar Desk Shortcut",
		filters={"show_on_desk": True},
		fields=[
			"name",
			"shortcut_name",
			"link_type",
			"link_to",
			"icon_name",
			"custom_icon",
			"color",
			"description",
			"sequence",
			"keyboard_shortcut",
			"open_in_new_tab",
		],
		order_by="sequence",
	)

	# Cache for 5 minutes
	frappe.cache.set_value(cache_key, shortcuts, expires_in_sec=300)

	return filter_by_roles(shortcuts)


def filter_by_roles(shortcuts):
	"""Filter shortcuts by user roles"""
	user_roles = set(frappe.get_roles())
	filtered = []

	for shortcut in shortcuts:
		# Get roles for this shortcut
		shortcut_roles = frappe.get_all(
			"Zevar Desk Shortcut Role", filters={"parent": shortcut.name}, pluck="role"
		)

		# If no roles defined, show to everyone
		if not shortcut_roles:
			filtered.append(shortcut)
		# Otherwise, check if user has any of the required roles
		elif user_roles & set(shortcut_roles):
			filtered.append(shortcut)

	return filtered


@frappe.whitelist()
def get_quick_stats():
	"""
	Get dashboard statistics for the desk.

	Returns:
		dict: Statistics including sales, repairs, layaways, etc.
	"""
	stats = {}
	today = frappe.utils.today()

	try:
		# Today's sales total
		todays_sales = frappe.db.sql(
			"""
			SELECT COALESCE(SUM(grand_total), 0)
			FROM `tabSales Invoice`
			WHERE docstatus = 1
			AND posting_date = %s
		""",
			(today,),
		)[0][0]
		stats["todays_sales"] = flt(todays_sales)
	except Exception:
		stats["todays_sales"] = 0

	try:
		# Pending repairs count
		pending_repairs = frappe.db.count("Repair Order", {"status": "In Progress"})
		stats["pending_repairs"] = pending_repairs or 0
	except Exception:
		stats["pending_repairs"] = 0

	try:
		# Active layaways count
		active_layaways = frappe.db.count("Layaway Contract", {"status": "Active"})
		stats["active_layaways"] = active_layaways or 0
	except Exception:
		stats["active_layaways"] = 0

	try:
		# Pending trade-ins count
		pending_trade_ins = frappe.db.count("Trade In Record", {"status": "Pending"})
		stats["pending_trade_ins"] = pending_trade_ins or 0
	except Exception:
		stats["pending_trade_ins"] = 0

	try:
		# Today's customers
		todays_customers = frappe.db.sql(
			"""
			SELECT COUNT(DISTINCT customer)
			FROM `tabSales Invoice`
			WHERE docstatus = 1
			AND posting_date = %s
		""",
			(today,),
		)[0][0]
		stats["todays_customers"] = todays_customers or 0
	except Exception:
		stats["todays_customers"] = 0

	return stats


@frappe.whitelist()
def get_recent_activity(limit=10):
	"""
	Get recent activity feed for the desk.

	Args:
		limit (int): Maximum number of activities to return

	Returns:
		list: List of activity dictionaries with type, message, and time
	"""
	activities = []

	# Recent POS invoices
	try:
		recent_invoices = frappe.get_all(
			"Sales Invoice",
			fields=["name", "customer", "grand_total", "modified", "owner"],
			filters={"docstatus": 1, "is_pos": 1},
			order_by="modified desc",
			limit=5,
		)
		for inv in recent_invoices:
			activities.append(
				{
					"type": "invoice",
					"icon": "shopping-cart",
					"message": _("POS Invoice {0} created - ${1:,.2f}").format(
						inv.name, flt(inv.grand_total)
					),
					"time": inv.modified,
					"link": f"/app/sales-invoice/{inv.name}",
				}
			)
	except Exception:
		pass

	# Recent repairs
	try:
		recent_repairs = frappe.get_all(
			"Repair Order",
			fields=["name", "status", "modified", "customer"],
			order_by="modified desc",
			limit=3,
		)
		for repair in recent_repairs:
			status_icon = "check" if repair.status == "Completed" else "tools"
			activities.append(
				{
					"type": "repair",
					"icon": status_icon,
					"message": _("Repair Order {0} - {1}").format(repair.name, repair.status),
					"time": repair.modified,
					"link": f"/app/repair-order/{repair.name}",
				}
			)
	except Exception:
		pass

	# Recent layaways
	try:
		recent_layaways = frappe.get_all(
			"Layaway Contract",
			fields=["name", "status", "modified", "customer"],
			order_by="modified desc",
			limit=3,
		)
		for layaway in recent_layaways:
			activities.append(
				{
					"type": "layaway",
					"icon": "credit-card",
					"message": _("Layaway Contract {0} - {1}").format(
						layaway.name, layaway.status
					),
					"time": layaway.modified,
					"link": f"/app/layaway-contract/{layaway.name}",
				}
			)
	except Exception:
		pass

	# Sort by time descending
	activities.sort(key=lambda x: x["time"], reverse=True)

	return activities[:limit]


def flt(value, precision=2):
	"""Convert to float with precision"""
	try:
		return round(float(value or 0), precision)
	except (TypeError, ValueError):
		return 0


@frappe.whitelist()
def get_all_icons():
	"""
	Get list of all available icons for the shortcut form.

	Returns:
		list: List of icon names
	"""
	return [
		"shopping-cart",
		"user",
		"credit-card",
		"tools",
		"repeat",
		"gift",
		"gem",
		"percentage",
		"file-text",
		"calendar",
		"settings",
		"home",
		"store",
		"dollar-sign",
		"package",
		"clipboard-list",
		"users",
		"bar-chart-2",
		"bell",
		"heart",
		"star",
		"bookmark",
		"folder",
		"image",
		"edit",
		"trash-2",
		"plus",
		"search",
		"filter",
		"download",
		"upload",
		"printer",
		"mail",
		"phone",
		"map-pin",
		"globe",
		"lock",
		"unlock",
		"eye",
		"eye-off",
		"check",
		"x",
		"alert-circle",
		"info",
		"help-circle",
		"chevron-right",
		"arrow-right",
		"external-link",
	]
