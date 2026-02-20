frappe.provide('zevar_core');

const update_icons = () => {
    const overrides = {
        "POS": "/assets/zevar_core/images/pos_logo.svg",
        "Employee Portal": "/assets/zevar_core/images/employee_portal_logo.svg",
        "Zevar POS": "/assets/zevar_core/images/pos_logo.svg",
        "Employee P...": "/assets/zevar_core/images/employee_portal_logo.svg"
    };

    // Strategy 1: Modify in-memory data
    if (frappe.boot && frappe.boot.app_data) {
        frappe.boot.app_data.forEach(app => {
            if (overrides[app.app_title] || overrides[app.app_name]) {
                app.app_logo_url = overrides[app.app_title] || overrides[app.app_name];
            }
        });
    }

    // Strategy 2: DOM Manipulation
    // Target .app-item (Apps Launcher) and .desktop-shortcut (Workspace)
    const targets = ['.app-item', '.desktop-shortcut', '.standard-sidebar-item'];

    targets.forEach(selector => {
        $(selector).each(function () {
            const title = $(this).attr('title') || $(this).find('.app-title, .sidebar-item-label').text();
            if (overrides[title] || (title && overrides[title.trim()])) {
                const img = $(this).find('img, .app-icon img');
                if (img.length) { // Replace existing image
                    img.attr('src', overrides[title] || overrides[title.trim()]);
                } else {
                    // Check if it's an SVG icon/symbol usage and replace it?
                    // Harder, but for now focus on image case
                }
            }
        });
    });
};

$(document).on('app_ready', function () {
    update_icons();

    // Re-run on route change
    frappe.router.on('change', () => {
        setTimeout(update_icons, 500); // Wait for render
        setTimeout(update_icons, 2000); // Retry
    });
});
