frappe.query_reports["Finance Account Balances"] = {
	filters: [
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nActive\nSuspended\nClosed\nCollections",
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "has_balance",
			label: __("With Balance Only"),
			fieldtype: "Check",
			default: 1,
		},
	],
};
