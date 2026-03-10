"""
POS Profile API - Profile management for POS terminals
"""

import frappe
from frappe import _
from frappe.utils import cint


@frappe.whitelist()
def get_pos_profiles():
	"""
	Get all available POS profiles for the current user.

	Returns:
	    List of POS profiles with basic info
	"""
	frappe.has_permission("POS Profile", "read", throw=True)

	profiles = frappe.get_all(
		"POS Profile",
		filters={"disabled": 0},
		fields=["name", "company", "warehouse", "currency", "selling_price_list"],
		order_by="name",
	)

	return {"profiles": profiles, "count": len(profiles)}


@frappe.whitelist()
def get_active_profile(user: str | None = None):
	"""
	Get the active POS profile for a user.

	Args:
	    user: User ID (defaults to current user)

	Returns:
	    Active profile details or None
	"""
	if not user:
		user = frappe.session.user

	# Check for user's active profile preference
	active_profile_name = frappe.db.get_value(
		"User Permission",
		{"user": user, "allow": "POS Profile", "is_default": 1},
		"for_value",
	)

	if not active_profile_name:
		# Fall back to first available profile
		active_profile_name = frappe.db.get_value(
			"POS Profile", {"disabled": 0}, "name", order_by="creation"
		)

	if not active_profile_name:
		return {"active_profile": None, "message": "No POS profiles available"}

	# Get full profile details
	profile = frappe.get_doc("POS Profile", active_profile_name)

	# Get associated store location info if available
	store_location = frappe.db.get_value(
		"Store Location",
		{"pos_profile": active_profile_name, "is_active": 1},
		["name", "store_name", "default_warehouse", "tax_template", "county_tax_rate"],
		as_dict=True,
	)

	return {
		"active_profile": {
			"name": profile.name,
			"company": profile.company,
			"warehouse": profile.warehouse,
			"currency": profile.currency or "USD",
			"selling_price_list": profile.selling_price_list,
			"write_off_account": profile.write_off_account,
			"write_off_cost_center": profile.write_off_cost_center,
		},
		"store_location": store_location,
	}


@frappe.whitelist(methods=["POST"])
def set_active_profile(profile_name: str, user: str | None = None):
	"""
	Set the active POS profile for a user.

	Args:
	    profile_name: Name of the POS profile to activate
	    user: User ID (defaults to current user)

	Returns:
	    Success status
	"""
	frappe.has_permission("POS Profile", "read", throw=True)

	if not user:
		user = frappe.session.user

	# Validate profile exists and is not disabled
	if not frappe.db.exists("POS Profile", profile_name):
		frappe.throw(_("POS Profile '{0}' not found.").format(profile_name))

	if frappe.db.get_value("POS Profile", profile_name, "disabled"):
		frappe.throw(_("POS Profile '{0}' is disabled.").format(profile_name))

	# Remove existing default for this user
	frappe.db.delete("User Permission", {"user": user, "allow": "POS Profile", "is_default": 1})

	# Create new user permission as default
	perm = frappe.new_doc("User Permission")
	perm.user = user
	perm.allow = "POS Profile"
	perm.for_value = profile_name
	perm.is_default = 1
	perm.apply_to_all_roles = 1
	perm.insert(ignore_permissions=True)

	frappe.db.commit()

	return {"success": True, "message": _("Active profile set to {0}").format(profile_name)}


@frappe.whitelist()
def get_profile_payments(profile_name: str):
	"""
	Get payment modes configured for a POS profile.

	Args:
	    profile_name: Name of the POS profile

	Returns:
	    List of payment modes
	"""
	frappe.has_permission("POS Profile", "read", throw=True)

	payments = frappe.get_all(
		"POS Payment Method",
		filters={"parent": profile_name, "parenttype": "POS Profile"},
		fields=["mode_of_payment", "default"],
		order_by="idx",
	)

	return {"payments": payments}


@frappe.whitelist()
def get_profile_items(profile_name: str, search: str | None = None, limit: int = 50):
	"""
	Get items available for a POS profile.

	Args:
	    profile_name: Name of the POS profile
	    search: Optional search term
	    limit: Maximum items to return

	Returns:
	    List of items
	"""
	frappe.has_permission("POS Profile", "read", throw=True)

	# Get profile's warehouse
	warehouse = frappe.db.get_value("POS Profile", profile_name, "warehouse")
	if not warehouse:
		return {"items": [], "message": "No warehouse configured for profile"}

	# Build query
	filters = {"disabled": 0, "is_sales_item": 1}

	if search:
		filters["item_name"] = ["like", f"%{search}%"]

	items = frappe.get_all(
		"Item",
		filters=filters,
		fields=["item_code", "item_name", "stock_uom", "image", "standard_rate"],
		limit_page_length=limit,
	)

	return {"items": items, "warehouse": warehouse}
