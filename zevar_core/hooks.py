app_name = "zevar_core"
app_title = "Unified Retail Management System"
app_publisher = "Zevar"
app_description = "A centralized solution for POS operations, real-time inventory management, dynamic pricing, and CRM for Zevar Jewelery."
app_email = "akshay@arijentek.com"
app_license = "mit"
app_logo_url = "/assets/zevar_core/images/pos_logo.svg"
splash_image = "/assets/zevar_core/images/pos_logo.svg"

add_to_apps_screen = [
	{
		"name": "zevar_pos",
		"logo": "/assets/zevar_core/images/pos_logo.svg",
		"title": "Zevar POS",
		"route": "/pos",
	},
	{
		"name": "zevar_catalogues",
		"logo": "/assets/zevar_core/images/pos_logo.svg",
		"title": "Zevar Catalogues",
		"route": "/catalogues",
	},
	{
		"name": "zevar_employee_portal",
		"logo": "/assets/zevar_core/images/employee_portal_logo.svg",
		"title": "Employee Portal",
		"route": "/employee-portal",
	}
]

boot_session = "zevar_core.api.desk.boot_session"

app_include_js = ["/assets/zevar_core/js/desk_customization.js"]

# Jinja
jinja = {"methods": ["zevar_core.utils.assets.get_frontend_asset"]}

# Routing
website_route_rules = [
	{"from_route": "/employee-portal/<path:app_path>", "to_route": "employee-portal"},
	{"from_route": "/pos/<path:app_path>", "to_route": "pos"},
	{"from_route": "/catalogues/<path:app_path>", "to_route": "catalogues"},
]

# Fixtures
fixtures = ["Item Attribute", "Custom Field", "Property Setter"]

# Document Events
doc_events = {
	"Item": {"validate": "zevar_core.item_events.calculate_net_weight_g"},
	"Sales Invoice": {
		"validate": [
			"zevar_core.tax_events.apply_store_tax",
			"zevar_core.trade_in_events.validate_trade_in_2x_rule",
		],
		"on_submit": "zevar_core.api.commission.calculate_commissions",
	},
}

# Scheduler events
scheduler_events = {"cron": {"*/15 * * * *": ["zevar_core.tasks.fetch_live_gold_rate"]}}

# Installation hooks
after_install = "zevar_core.install.create_required_modes_of_payment"
