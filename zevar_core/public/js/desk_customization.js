frappe.provide("zevar_core");

const update_icons = () => {
	const overrides = {
		POS: "/assets/zevar_core/images/pos_logo.svg",
		"Employee Portal": "/assets/zevar_core/images/employee_portal_logo.svg",
		"Zevar POS": "/assets/zevar_core/images/pos_logo.svg",
		"Zevar Catalogues": "/assets/zevar_core/images/pos_logo.svg",
		"Catalogues": "/assets/zevar_core/images/pos_logo.svg",
	};

	// App name mappings (for frappe.boot.app_data)
	const appNameMap = {
		zevar_pos: "/assets/zevar_core/images/pos_logo.svg",
		zevar_catalogues: "/assets/zevar_core/images/pos_logo.svg",
		zevar_employee_portal: "/assets/zevar_core/images/employee_portal_logo.svg",
	};

	// Strategy 1: Modify in-memory data
	if (frappe.boot && frappe.boot.app_data) {
		frappe.boot.app_data.forEach((app) => {
			// Check title in overrides, then name in overrides, then name in appNameMap
			const iconUrl = overrides[app.app_title] || overrides[app.app_name] || appNameMap[app.app_name];
			if (iconUrl) {
				app.app_logo_url = iconUrl;
			}
		});
	}

	// Strategy 2: DOM Manipulation via MutationObserver or direct query
	const targets = [".app-item", ".desktop-shortcut", ".standard-sidebar-item"];

	targets.forEach((selector) => {
		$(selector).each(function () {
			const rawTitle = $(this).attr("title");
			const fallbackTitle = $(this).find(".app-title, .sidebar-item-label").text();
			const title = rawTitle != null && rawTitle !== "" ? rawTitle : fallbackTitle || "";
			const cleanTitle = title.trim();

			if (cleanTitle) {
				// Check exact match or startsWith for Employee Portal to handle truncation
				let iconUrl = overrides[cleanTitle];
				if (!iconUrl && cleanTitle.startsWith("Employee P")) {
					iconUrl = overrides["Employee Portal"];
				}
				if (!iconUrl && cleanTitle.startsWith("Zevar Cat")) {
					iconUrl = overrides["Zevar Catalogues"];
				}

				if (iconUrl) {
					const img = $(this).find("img, .app-icon img");
					if (img.length) {
						img.attr("src", iconUrl);
					}
				}
			}
		});
	});
};

$(document).on("app_ready", function () {
	update_icons();

	// Use MutationObserver to handle dynamic loading (better than timeouts)
	const observer = new MutationObserver(
		frappe.utils.debounce(() => {
			update_icons();
		}, 200)
	);

	const deskContainer = document.querySelector(".desk-page") || document.body;
	if (deskContainer) {
		observer.observe(deskContainer, {
			childList: true,
			subtree: true,
		});
	}
});
