"""
Patch to Fix Desktop Icon Creation Bug in Frappe v16.11.0

This patch applies runtime monkey patches to fix two bugs in
frappe/desk/doctype/desktop_icon/desktop_icon.py:

Bug 1 (Line 45-46): References non-existent 'module_name' field
    Original: self.label = self.module_name
    Fix: Skip this assignment as module_name field doesn't exist in v16

Bug 2 (Line 252): Sets non-existent 'app_name' field
    Original: icon.app_name = app_name
    Fix: Use 'app' field instead

This is a runtime patch - it does NOT modify core Frappe files.
Remove this patch after Frappe officially fixes the bug upstream.
"""

import frappe


def execute():
	"""
	Apply runtime monkey patches to fix desktop icon creation bugs.
	Only patches if the bug is detected (idempotent).
	"""
	_patch_validate_method()
	_patch_create_desktop_icons_from_workspace()
	print("Desktop icon creation bugs patched successfully!")


def _patch_validate_method():
	"""
	Patch DesktopIcon.validate() to avoid module_name AttributeError.

	Original buggy code:
	    def validate(self):
	        if not self.label:
	            self.label = self.module_name  # BUG: module_name doesn't exist

	Patched code:
	    def validate(self):
	        pass  # Skip the buggy assignment
	"""
	import inspect

	from frappe.desk.doctype.desktop_icon.desktop_icon import DesktopIcon

	# Get current source code of validate method
	try:
		source = inspect.getsource(DesktopIcon.validate)
	except (TypeError, OSError):
		# Method might already be patched or unavailable
		print("  validate(): Already patched or unavailable, skipping")
		return

	# Check if bug exists (look for module_name reference)
	if "self.module_name" not in source:
		print("  validate(): Bug not found (already fixed), skipping")
		return

	# Apply monkey patch
	def patched_validate(self):
		# Original intent: set label from module_name if not set
		# But module_name field doesn't exist in v16, so we skip
		pass

	DesktopIcon.validate = patched_validate
	print("  validate(): Patched to skip module_name reference")


def _patch_create_desktop_icons_from_workspace():
	"""
	Patch create_desktop_icons_from_workspace() to use 'app' instead of 'app_name'.

	Original buggy code:
	    icon.app_name = app_name  # BUG: app_name field doesn't exist

	Patched code:
	    icon.app = app_name  # Use correct field name
	"""
	import inspect

	import frappe.desk.doctype.desktop_icon.desktop_icon as desktop_icon_module

	# Get current source code
	try:
		source = inspect.getsource(desktop_icon_module.create_desktop_icons_from_workspace)
	except (TypeError, OSError):
		print("  create_desktop_icons_from_workspace(): Already patched or unavailable, skipping")
		return

	# Check if bug exists (look for app_name assignment)
	if "icon.app_name = app_name" not in source:
		print("  create_desktop_icons_from_workspace(): Bug not found (already fixed), skipping")
		return

	# Define patched function with same logic but fixed field name
	def patched_create_desktop_icons_from_workspace():
		workspaces = frappe.get_all(
			"Workspace",
			filters={"public": 1, "name": ["!=", "Welcome Workspace"]},
			fields=["name", "icon", "app", "module"],
		)

		for w in workspaces:
			icon = frappe.new_doc("Desktop Icon")
			icon.link_type = "Workspace Sidebar"
			icon.label = w.name
			icon.icon_type = "Link"
			icon.link_to = w.name
			icon.icon = w.icon
			if w.module:
				app_name = w.app or frappe.db.get_value("Module Def", w.module, "app_name")
				if app_name in frappe.get_installed_apps():
					# BUG FIX: Use 'app' field instead of non-existent 'app_name'
					icon.app = app_name
					app_title = frappe.get_hooks("app_title", app_name=app_name)[0]
					app_icon = frappe.db.exists("Desktop Icon", {"label": app_title, "icon_type": "App"})
					if app_icon:
						icon.parent_icon = app_icon

					# Portal App With Desk Workspace
					if frappe.db.get_value("Desktop Icon", app_icon, "link") and not frappe.db.get_value(
						"Desktop Icon", app_icon, "link"
					).startswith("/app"):
						icon.hidden = 1
						icon.parent_icon = None

					# If Desk App has one workspace with the same name
					if icon.label == app_title and (
						app_icon and frappe.db.get_value("Desktop Icon", app_icon, "link").startswith("/app")
					):
						icon.hidden = 1
						icon.parent_icon = None

					try:
						if not frappe.db.exists(
							"Desktop Icon", [{"label": icon.label, "icon_type": icon.icon_type}]
						):
							icon.insert(ignore_if_duplicate=True)
					except Exception as e:
						frappe.error_log(title="Creation of Desktop Icon Failed", message=e)

	# Apply monkey patch
	desktop_icon_module.create_desktop_icons_from_workspace = patched_create_desktop_icons_from_workspace
	print("  create_desktop_icons_from_workspace(): Patched to use 'app' instead of 'app_name'")
