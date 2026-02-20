
import frappe
from typing import Dict, Any, Optional

def boot_session(bootinfo: Dict[str, Any]) -> None:
    """
    Override the app logo for POS and Employee Portal in the desk.
    This runs on every session boot.
    """
    app_data = bootinfo.get("app_data", [])
    if not app_data:
        return

    # Use frappe.logger().debug() if you need to log during development
    # frappe.logger().debug(f"zevar_core boot_session executing. Apps found: {[a.get('app_title') for a in app_data]}")

    for app in app_data:
        # Check against title or name
        title = app.get("app_title", "")
        name = app.get("app_name", "")

        # Override POS logo
        if title in ["POS", "Zevar POS"] or name in ["POS", "zevar_pos"]:
            app["app_logo_url"] = "/assets/zevar_core/images/pos_logo.svg"

        # Override Employee Portal logo
        if title == "Employee Portal" or name == "employee_portal" or title.startswith("Employee P"):
             app["app_logo_url"] = "/assets/zevar_core/images/employee_portal_logo.svg"
