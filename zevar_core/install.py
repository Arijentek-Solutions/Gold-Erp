"""
Zevar Core Installation Utilities

Functions to set up required data on app installation.
"""

import json
import os

import frappe
from frappe import _
from frappe.modules.import_file import import_file_by_path


def create_required_modes_of_payment():
	"""
	Create all Mode of Payment records required by the POS system.

	The frontend checkout supports these payment methods. Each must exist
	as a Frappe 'Mode of Payment' record for Sales Invoice validation to pass.
	"""
	if not frappe.db.exists("DocType", "Mode of Payment"):
		frappe.logger().warning(
			"Skipping Mode of Payment bootstrap: DocType 'Mode of Payment' does not exist yet."
		)
		return

	modes = [
		{"mode_of_payment": "Cash", "type": "Cash"},
		{"mode_of_payment": "Credit Card", "type": "Bank"},
		{"mode_of_payment": "Debit Card", "type": "Bank"},
		{"mode_of_payment": "Check", "type": "Bank"},
		{"mode_of_payment": "Wire Transfer", "type": "Bank"},
		{"mode_of_payment": "Zelle", "type": "General"},
		{"mode_of_payment": "Gift Card", "type": "General"},
		{"mode_of_payment": "Trade-In", "type": "General"},
	]

	for mode in modes:
		if not frappe.db.exists("Mode of Payment", mode["mode_of_payment"]):
			doc = frappe.new_doc("Mode of Payment")
			doc.mode_of_payment = mode["mode_of_payment"]
			doc.type = mode["type"]
			doc.enabled = 1
			doc.save(ignore_permissions=True)

	frappe.db.commit()  # nosemgrep (manual commit during install)


def import_desktop_icons():
	"""
	Import desktop icons from JSON files in the desktop_icon directory.

	Desktop icons are stored as JSON files but are not automatically imported
	during app installation. This function imports them to make shortcuts
	like Layaway List and Inventory appear on the desk.
	"""
	app_path = frappe.get_app_path("zevar_core")
	icons_dir = os.path.join(app_path, "zevar_core", "desktop_icon")

	if not os.path.exists(icons_dir):
		return

	for fname in os.listdir(icons_dir):
		if fname.endswith(".json"):
			file_path = os.path.join(icons_dir, fname)
			try:
				with open(file_path) as f:
					icon_data = json.load(f)

				# Must have doctype key to be valid
				if not icon_data.get("doctype"):
					frappe.log_error(
						f"Desktop icon {fname} missing 'doctype' key",
						"Desktop Icon Import",
					)
					continue

				icon_name = icon_data.get("name")
				if icon_name and not frappe.db.exists("Desktop Icon", icon_name):
					import_file_by_path(file_path)
					frappe.db.commit()  # nosemgrep
			except Exception as e:
				frappe.log_error(f"Failed to import desktop icon {fname}: {e}", "Desktop Icon Import")

	# Clear cache to ensure icons appear immediately
	frappe.cache.delete_key("desktop_icons")
	frappe.cache.delete_key("bootinfo")


def import_workspaces():
	"""
	Import workspace JSON files.

	Workspaces are stored as JSON files and need to be imported
	to appear in the workspace sidebar.
	"""
	import json

	app_path = frappe.get_app_path("zevar_core")
	workspaces_dir = os.path.join(app_path, "zevar_core", "workspace")

	if not os.path.exists(workspaces_dir):
		return

	for workspace_name in os.listdir(workspaces_dir):
		workspace_path = os.path.join(workspaces_dir, workspace_name)
		if os.path.isdir(workspace_path):
			json_file = os.path.join(workspace_path, f"{workspace_name}.json")
			if os.path.exists(json_file):
				try:
					# Read the JSON to get the actual workspace name (not directory name)
					with open(json_file) as f:
						workspace_data = json.load(f)
					actual_name = workspace_data.get("name") or workspace_data.get("label") or workspace_name

					if not frappe.db.exists("Workspace", actual_name):
						import_file_by_path(json_file)
						frappe.db.commit()  # nosemgrep
				except Exception as e:
					frappe.log_error(
						f"Failed to import workspace {workspace_name}: {e}",
						"Workspace Import",
					)


def create_default_desk_shortcuts():
	"""
	Create default desk shortcuts for Zevar Core features.

	These shortcuts appear on the custom Zevar desk page and can be
	managed via the Zevar Desk Shortcut DocType.
	"""
	# Check if DocType exists (may not exist before migration)
	if not frappe.db.exists("DocType", "Zevar Desk Shortcut"):
		print("Zevar Desk Shortcut DocType not found. Run migrate first.")
		return

	shortcuts = [
		{
			"shortcut_name": "POS Terminal",
			"link_type": "URL",
			"link_to": "/pos",
			"icon_name": "shopping-cart",
			"color": "#2563eb",
			"description": "Point of Sale terminal for processing transactions",
			"sequence": 10,
			"keyboard_shortcut": "alt+p",
			"show_on_desk": True,
			"roles": [{"role": "Sales User"}, {"role": "POS Manager"}, {"role": "Store Manager"}],
		},
		{
			"shortcut_name": "Employee Portal",
			"link_type": "URL",
			"link_to": "/employee-portal",
			"icon_name": "user",
			"color": "#6b7280",
			"description": "Employee self-service portal",
			"sequence": 20,
			"keyboard_shortcut": "alt+e",
			"show_on_desk": True,
			"roles": [{"role": "Employee"}, {"role": "HR Manager"}],
		},
		{
			"shortcut_name": "Layaway Contracts",
			"link_type": "DocType",
			"link_to": "Layaway Contract",
			"icon_name": "credit-card",
			"color": "#8b5cf6",
			"description": "Manage customer layaway contracts",
			"sequence": 30,
			"keyboard_shortcut": "alt+l",
			"show_on_desk": True,
			"roles": [{"role": "Sales User"}, {"role": "Store Manager"}],
		},
		{
			"shortcut_name": "Repair Orders",
			"link_type": "DocType",
			"link_to": "Repair Order",
			"icon_name": "tools",
			"color": "#f59e0b",
			"description": "Jewelry repair tracking and management",
			"sequence": 40,
			"keyboard_shortcut": "alt+r",
			"show_on_desk": True,
			"roles": [{"role": "Sales User"}, {"role": "Technician"}, {"role": "Store Manager"}],
		},
		{
			"shortcut_name": "Trade-Ins",
			"link_type": "DocType",
			"link_to": "Trade In Record",
			"icon_name": "repeat",
			"color": "#14b8a6",
			"description": "Customer trade-in transactions",
			"sequence": 50,
			"keyboard_shortcut": "alt+t",
			"show_on_desk": True,
			"roles": [{"role": "Sales User"}, {"role": "Store Manager"}],
		},
		{
			"shortcut_name": "Gift Cards",
			"link_type": "DocType",
			"link_to": "Gift Card",
			"icon_name": "gift",
			"color": "#ec4899",
			"description": "Gift card management and redemption",
			"sequence": 60,
			"keyboard_shortcut": "alt+g",
			"show_on_desk": True,
			"roles": [{"role": "Sales User"}, {"role": "Store Manager"}],
		},
		{
			"shortcut_name": "Jewelry Appraisal",
			"link_type": "DocType",
			"link_to": "Jewelry Appraisal",
			"icon_name": "gem",
			"color": "#d97706",
			"description": "Professional jewelry appraisals",
			"sequence": 70,
			"keyboard_shortcut": "alt+a",
			"show_on_desk": True,
			"roles": [{"role": "Appraiser"}, {"role": "Store Manager"}],
		},
		{
			"shortcut_name": "Commission Tracking",
			"link_type": "DocType",
			"link_to": "Sales Commission Split",
			"icon_name": "percentage",
			"color": "#10b981",
			"description": "Sales commission splits and tracking",
			"sequence": 80,
			"keyboard_shortcut": "alt+c",
			"show_on_desk": True,
			"roles": [{"role": "Store Manager"}, {"role": "System Manager"}],
		},
		{
			"shortcut_name": "Gold Rate Log",
			"link_type": "DocType",
			"link_to": "Gold Rate Log",
			"icon_name": "dollar-sign",
			"color": "#fbbf24",
			"description": "Live gold price tracking",
			"sequence": 90,
			"show_on_desk": True,
			"roles": [{"role": "Sales User"}, {"role": "Store Manager"}],
		},
		{
			"shortcut_name": "Customer Ledger",
			"link_type": "DocType",
			"link_to": "Customer Ledger Entry",
			"icon_name": "file-text",
			"color": "#6366f1",
			"description": "Customer transaction history",
			"sequence": 100,
			"show_on_desk": True,
			"roles": [{"role": "Store Manager"}, {"role": "Accounts Manager"}],
		},
		{
			"shortcut_name": "Store Locations",
			"link_type": "DocType",
			"link_to": "Store Location",
			"icon_name": "map-pin",
			"color": "#0ea5e9",
			"description": "Multi-store location management",
			"sequence": 110,
			"show_on_desk": True,
			"roles": [{"role": "Store Manager"}, {"role": "System Manager"}],
		},
		{
			"shortcut_name": "Inventory",
			"link_type": "DocType",
			"link_to": "Item",
			"icon_name": "package",
			"color": "#8b5cf6",
			"description": "Jewelry inventory management",
			"sequence": 120,
			"show_on_desk": True,
			"roles": [{"role": "Stock Manager"}, {"role": "Store Manager"}],
		},
	]

	for shortcut_data in shortcuts:
		shortcut_name = shortcut_data.get("shortcut_name")

		# Check if shortcut already exists
		if frappe.db.exists("Zevar Desk Shortcut", shortcut_name):
			continue

		try:
			doc = frappe.new_doc("Zevar Desk Shortcut")

			# Set basic fields
			doc.shortcut_name = shortcut_data.get("shortcut_name")
			doc.link_type = shortcut_data.get("link_type")
			doc.link_to = shortcut_data.get("link_to")
			doc.icon_name = shortcut_data.get("icon_name", "star")
			doc.color = shortcut_data.get("color", "#2563eb")
			doc.description = shortcut_data.get("description", "")
			doc.sequence = shortcut_data.get("sequence", 100)
			doc.keyboard_shortcut = shortcut_data.get("keyboard_shortcut", "")
			doc.show_on_desk = shortcut_data.get("show_on_desk", True)

			# Add roles
			roles = shortcut_data.get("roles", [])
			for role_data in roles:
				doc.append("roles", role_data)

			doc.insert(ignore_permissions=True)

		except Exception as e:
			frappe.log_error(
				f"Failed to create desk shortcut '{shortcut_name}': {e}",
				"Desk Shortcut Creation",
			)

	# Clear cache to ensure shortcuts appear
	frappe.cache.delete_key("zevar_desk_shortcuts")
	frappe.db.commit()  # nosemgrep
