"""
Zevar Core Installation Utilities

Functions to set up required data on app installation.
"""

import frappe
from frappe import _


def create_required_modes_of_payment():
	"""
	Create all Mode of Payment records required by the POS system.

	The frontend checkout supports these payment methods. Each must exist
	as a Frappe 'Mode of Payment' record for Sales Invoice validation to pass.
	"""
	modes = [
		{"mode_of_payment": "Cash", "type": "Cash"},
		{"mode_of_payment": "Credit Card", "type": "Bank"},
		{"mode_of_payment": "Debit Card", "type": "Bank"},
		{"mode_of_payment": "Check", "type": "Bank"},
		{"mode_of_payment": "Wire Transfer", "type": "Bank"},
		{"mode_of_payment": "Zelle", "type": "General"},
		{"mode_of_payment": "Gift Card", "type": "General"},
		{"mode_of_payment": "Trade-In", "type": "General"},
	]

	for mode in modes:
		if not frappe.db.exists("Mode of Payment", mode["mode_of_payment"]):
			doc = frappe.new_doc("Mode of Payment")
			doc.mode_of_payment = mode["mode_of_payment"]
			doc.type = mode["type"]
			doc.enabled = 1
			doc.save(ignore_permissions=True)

	frappe.db.commit() # nosemgrep (manual commit during install)
