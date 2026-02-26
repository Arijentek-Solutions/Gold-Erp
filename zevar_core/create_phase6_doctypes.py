import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def create_doctypes():
	module = "Unified Retail Management System"

	print("Creating Trade In Record...")
	if not frappe.db.exists("DocType", "Trade In Record"):
		doc = frappe.get_doc(
			{
				"doctype": "DocType",
				"name": "Trade In Record",
				"module": module,
				"custom": 0,
				"istable": 1,
				"editable_grid": 1,
				"fields": [
					{
						"fieldname": "original_item_code",
						"fieldtype": "Link",
						"options": "Item",
						"label": "Original Item Code",
						"in_list_view": 1,
						"reqd": 1,
					},
					{
						"fieldname": "original_purchase_date",
						"fieldtype": "Date",
						"label": "Original Date of Purchase",
					},
					{
						"fieldname": "trade_in_value",
						"fieldtype": "Currency",
						"label": "Agreed Trade-In Value",
						"in_list_view": 1,
						"reqd": 1,
					},
					{
						"fieldname": "new_item_code",
						"fieldtype": "Link",
						"options": "Item",
						"label": "New Item (Being Purchased)",
						"in_list_view": 1,
						"reqd": 1,
					},
					{
						"fieldname": "new_item_value",
						"fieldtype": "Currency",
						"label": "New Item Value",
						"in_list_view": 1,
						"reqd": 1,
					},
					{
						"fieldname": "manager_override",
						"fieldtype": "Link",
						"options": "User",
						"label": "Manager Override",
					},
					{
						"fieldname": "override_reason",
						"fieldtype": "Text",
						"label": "Override Reason",
						"depends_on": "manager_override",
					},
				],
			}
		)
		doc.insert(ignore_permissions=True)

	print("Adding Trade-Ins Custom Field to Sales Invoice...")
	custom_fields = {
		"Sales Invoice": [
			{
				"fieldname": "custom_trade_ins_section",
				"fieldtype": "Section Break",
				"label": "Trade-In Records",
				"insert_after": "custom_manager_override_user",
			},
			{
				"fieldname": "custom_trade_ins",
				"fieldtype": "Table",
				"options": "Trade In Record",
				"label": "Trade-Ins",
			},
		]
	}
	create_custom_fields(custom_fields)

	frappe.db.commit()  # nosemgrep: frappe-semgrep-rules.rules.frappe-manual-commit
	print("Phase 6 Trade-In Systems Created Successfully!")
