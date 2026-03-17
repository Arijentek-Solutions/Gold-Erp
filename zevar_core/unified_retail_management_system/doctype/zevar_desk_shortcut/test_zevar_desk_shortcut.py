# Copyright (c) 2026, Zevar and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestZevarDeskShortcut(FrappeTestCase):
	"""Test Zevar Desk Shortcut DocType"""

	def setUp(self):
		"""Set up test data"""
		self.test_shortcut_name = "Test Shortcut"

	def tearDown(self):
		"""Clean up test data"""
		if frappe.db.exists("Zevar Desk Shortcut", self.test_shortcut_name):
			frappe.delete_doc("Zevar Desk Shortcut", self.test_shortcut_name)

	def test_create_shortcut(self):
		"""Test creating a basic shortcut"""
		shortcut = frappe.get_doc(
			{
				"doctype": "Zevar Desk Shortcut",
				"shortcut_name": self.test_shortcut_name,
				"link_type": "URL",
				"link_to": "/test",
				"icon_name": "star",
				"color": "#2563eb",
				"show_on_desk": 1,
			}
		)
		shortcut.insert()
		self.assertTrue(frappe.db.exists("Zevar Desk Shortcut", self.test_shortcut_name))

	def test_keyboard_shortcut_validation(self):
		"""Test keyboard shortcut format validation"""
		# Valid shortcuts
		valid_shortcuts = ["alt+p", "ctrl+shift+p", "shift+f1", "alt+1"]
		for ks in valid_shortcuts:
			shortcut = frappe.get_doc(
				{
					"doctype": "Zevar Desk Shortcut",
					"shortcut_name": f"Test {ks}",
					"link_type": "URL",
					"link_to": "/test",
					"keyboard_shortcut": ks,
				}
			)
			shortcut.insert()
			shortcut.delete()

		# Invalid shortcuts
		invalid_shortcuts = ["p", "invalid+p"]
		for ks in invalid_shortcuts:
			with self.assertRaises(frappe.ValidationError):
				shortcut = frappe.get_doc(
					{
						"doctype": "Zevar Desk Shortcut",
						"shortcut_name": f"Test Invalid {ks}",
						"link_type": "URL",
						"link_to": "/test",
						"keyboard_shortcut": ks,
					}
				)
				shortcut.insert()

	def test_doctype_validation(self):
		"""Test DocType link validation"""
		with self.assertRaises(frappe.ValidationError):
			shortcut = frappe.get_doc(
				{
					"doctype": "Zevar Desk Shortcut",
					"shortcut_name": "Invalid DocType",
					"link_type": "DocType",
					"link_to": "Non Existent DocType",
				}
			)
			shortcut.insert()
