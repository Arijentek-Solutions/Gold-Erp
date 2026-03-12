frappe.query_reports["Gold Rate History"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_days(frappe.datetime.get_today(), -7),
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
			reqd: 1,
		},
		{
			fieldname: "metal_type",
			label: __("Metal Type"),
			fieldtype: "Link",
			options: "Zevar Metal",
		},
		{
			fieldname: "purity",
			label: __("Purity"),
			fieldtype: "Link",
			options: "Zevar Purity",
		},
	],
};
