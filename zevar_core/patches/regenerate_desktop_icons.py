"""
Regenerate Desktop Icons — works without Redis (bench start stopped).

Run with: bench --site zevar.localhost execute zevar_core.patches.regenerate_desktop_icons.execute
"""

import frappe


def execute():
    """Delete orphaned icons via direct SQL and regenerate from apps + workspaces."""
    from frappe.desk.doctype.desktop_icon.desktop_icon import create_desktop_icons

    print("=== Current Desktop Icons ===")
    icons = frappe.get_all(
        "Desktop Icon",
        fields=["name", "label", "icon_type", "hidden", "standard", "app"],
        limit_page_length=100,
    )
    for i in icons:
        print(f"  {i.label:25s} type={i.icon_type:8s} hidden={i.hidden} std={i.standard} app={i.app}")
    print(f"Total: {len(icons)} icons\n")

    # Delete orphaned non-standard Link icons that have no matching workspace sidebar
    # Use direct SQL to avoid Redis dependency
    print("=== Cleaning up orphaned icons ===")
    for icon in icons:
        if not icon.standard and icon.icon_type == "Link":
            sidebar_exists = frappe.db.exists("Workspace Sidebar", {"title": icon.label})
            if not sidebar_exists:
                print(f"  Deleting orphaned Link icon: {icon.label}")
                frappe.db.delete("Desktop Icon", {"name": icon.name})

    # Also delete user-created App icons with no proper app link
    for icon in icons:
        if not icon.standard and icon.icon_type == "App" and not icon.app:
            print(f"  Deleting orphaned App icon (no app): {icon.label}")
            frappe.db.delete("Desktop Icon", {"name": icon.name})

    frappe.db.commit()

    # Regenerate standard icons
    print("\n=== Regenerating Desktop Icons ===")
    create_desktop_icons()
    frappe.db.commit()

    # Clear the desktop icons cache (direct, no Redis queue needed)
    try:
        frappe.cache.hdel("desktop_icons", frappe.session.user)
        frappe.cache.hdel("bootinfo", frappe.session.user)
    except Exception:
        print("  Cache clear skipped (Redis not available)")

    print("\n=== Updated Desktop Icons ===")
    new_icons = frappe.get_all(
        "Desktop Icon",
        fields=["name", "label", "icon_type", "hidden", "standard", "app"],
        limit_page_length=100,
    )
    for i in new_icons:
        print(f"  {i.label:25s} type={i.icon_type:8s} hidden={i.hidden} std={i.standard} app={i.app}")
    print(f"Total: {len(new_icons)} icons")

    frappe.db.commit()
    print("\nDone! Now run: bench start && refresh browser (Ctrl+Shift+R)")
