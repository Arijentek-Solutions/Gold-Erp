import frappe
from frappe import _

def run():
    profile_name = "POS - New York - ZJ"
    if not frappe.db.exists("POS Profile", profile_name):
        print(f"Profile {profile_name} not found")
        return
    
    profile = frappe.get_doc("POS Profile", profile_name)
    print(f"Profile: {profile.name}")
    for p in profile.payments:
        print(f"Mode: {p.mode_of_payment}, Account: {p.default_account}")
    
    company = frappe.get_doc("Company", profile.company)
    print(f"Company: {company.name}")
    print(f"Default Cash Account: {company.default_cash_account}")
    print(f"Default Bank Account: {company.default_bank_account}")
    print(f"Default Income Account: {company.default_income_account}")
