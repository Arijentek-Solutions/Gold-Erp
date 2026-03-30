import frappe

def execute():
	"""
	Migrate legacy custom_salesperson_{1..4} fields into the new Salesperson Split child table
	across all Sales Invoices.
	"""
	frappe.reload_doc("accounts", "doctype", "sales_invoice")

	# Fetch all invoices that have at least one of the legacy salesperson fields set
	invoices = frappe.db.sql(
		"""
		SELECT name, custom_salesperson_1, custom_salesperson_2,
			   custom_salesperson_3, custom_salesperson_4
		FROM `tabSales Invoice`
		WHERE custom_salesperson_1 IS NOT NULL AND custom_salesperson_1 != ''
		   OR custom_salesperson_2 IS NOT NULL AND custom_salesperson_2 != ''
		   OR custom_salesperson_3 IS NOT NULL AND custom_salesperson_3 != ''
		   OR custom_salesperson_4 IS NOT NULL AND custom_salesperson_4 != ''
		""",
		as_dict=True,
	)

	count = 0
	for invoice in invoices:
		doc = frappe.get_doc("Sales Invoice", invoice.name)
		
		# Skip if already migrated
		if len(doc.get("custom_salesperson_splits", [])) > 0:
			continue

		# Collect unique salespersons from the legacy fields
		salespersons = []
		for field in ["custom_salesperson_1", "custom_salesperson_2", "custom_salesperson_3", "custom_salesperson_4"]:
			sp = invoice.get(field)
			if sp and sp not in salespersons:
				salespersons.append(sp)

		if not salespersons:
			continue

		# Distribute the allocation percentage equally
		split_percent = 100.0 / len(salespersons)

		for sp in salespersons:
			doc.append(
				"custom_salesperson_splits",
				{
					"salesperson": sp,
					"allocated_percentage": split_percent,
				},
			)

		# Save the splits without triggering full validation/submission logic
		# to ensure historical docstatus remains intact
		doc.flags.ignore_permissions = True
		doc.flags.ignore_validate_update_after_submit = True
		doc.flags.ignore_links = True
		doc.save(ignore_version=True)
		count += 1
		
		# Commit every 500 records
		if count % 500 == 0:
			frappe.db.commit()

	frappe.db.commit()
	frappe.log_error(f"Migrated salespersons for {count} Sales Invoices to the new child table", "Zevar Core Patch")
