import frappe
from frappe import _


def run():
	company = "Zevar Jewelers"
	parent_account = "Bank Accounts - ZJ"  # Group account

	# 1. Create Bank Account if missing
	bank_account_name = "Chase Bank - ZJ"
	if not frappe.db.exists("Account", bank_account_name):
		print(f"Creating account {bank_account_name}...")
		bank_acc = frappe.new_doc("Account")
		bank_acc.account_name = "Chase Bank"
		bank_acc.parent_account = parent_account
		bank_acc.company = company
		bank_acc.account_type = "Bank"
		bank_acc.is_group = 0
		bank_acc.insert()
		print(f"Account {bank_account_name} created.")
	else:
		print(f"Account {bank_account_name} already exists.")

	# 2. Update Mode of Payment Account
	bank_modes = ["Credit Card", "Debit Card", "Wire Transfer", "Zelle", "Check"]
	for mode in bank_modes:
		if frappe.db.exists("Mode of Payment", mode):
			# Check if entry exists for this company
			mop_acc = frappe.db.get_value(
				"Mode of Payment Account", {"parent": mode, "company": company}, "name"
			)
			if mop_acc:
				frappe.db.set_value("Mode of Payment Account", mop_acc, "default_account", bank_account_name)
				print(f"Updated global Mode of Payment {mode} to use {bank_account_name}")
			else:
				doc = frappe.get_doc("Mode of Payment", mode)
				doc.append("accounts", {"company": company, "default_account": bank_account_name})
				doc.save()
				print(f"Added Mode of Payment {mode} for company {company} with account {bank_account_name}")

	# 3. Update POS Profile
	profile_name = "POS - New York - ZJ"
	if frappe.db.exists("POS Profile", profile_name):
		profile = frappe.get_doc("POS Profile", profile_name)
		for p in profile.payments:
			if p.mode_of_payment in bank_modes:
				p.default_account = bank_account_name
				print(
					f"Updated POS Profile {profile_name} payment mode {p.mode_of_payment} to use {bank_account_name}"
				)
		profile.save()

	frappe.db.commit()  # nosemgrep (manual commit for setup)
	print("Done.")


if __name__ == "__main__":
	run()
