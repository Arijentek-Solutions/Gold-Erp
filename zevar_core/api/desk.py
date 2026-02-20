
import frappe

def boot_session(bootinfo):
    """
    Override the app logo for POS and Employee Portal in the desk.
    This runs on every session boot.
    """
    if not bootinfo or not bootinfo.get("app_data"):
        return

    print(f"DEBUG: zevar_core boot_session executing. Apps found: {[a.get('app_title') for a in bootinfo.app_data]}")

    for app in bootinfo.app_data:
        # Check against title or name
        title = app.get("app_title", "")
        name = app.get("app_name", "")
        
        # Override POS logo
        if title == "POS" or name == "POS" or title == "Zevar POS" or name == "zevar_pos":
            app["app_logo_url"] = "/assets/zevar_core/images/pos_logo.svg"
            
        # Override Employee Portal logo
        # Matching "Employee Portal" or "Employee" if exclusive
        if title == "Employee Portal" or name == "employee_portal" or title == "Employee P...":
             app["app_logo_url"] = "/assets/zevar_core/images/employee_portal_logo.svg"
