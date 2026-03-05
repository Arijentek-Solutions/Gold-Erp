"""
Unit Tests for POS Invoice Creation
Tests: create_pos_invoice, tax calculation, trade-in deduction logic
"""

import json

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import flt


class TestPOSInvoiceCreation(FrappeTestCase):
	"""Test suite for POS invoice creation functionality."""

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.create_test_data()

	@classmethod
	def create_test_data(cls):
		"""Create test customer, warehouse, items, and POS profile."""
		# Create test company if not exists
		cls.company = frappe.defaults.get_user_default("Company") or frappe.db.get_single_value(
			"Global Defaults", "default_company"
		)

		# Create test customer
		if not frappe.db.exists("Customer", "Test POS Customer"):
			cls.test_customer = frappe.get_doc(
				{
					"doctype": "Customer",
					"customer_name": "Test POS Customer",
					"customer_type": "Individual",
					"customer_group": "Individual",
					"territory": "All Territories",
				}
			).insert(ignore_permissions=True)
		else:
			cls.test_customer = "Test POS Customer"

		# Create test warehouse
		if not frappe.db.exists("Warehouse", "Test POS Warehouse - _TC"):
			cls.test_warehouse = frappe.get_doc(
				{
					"doctype": "Warehouse",
					"warehouse_name": "Test POS Warehouse",
					"company": cls.company,
				}
			).insert(ignore_permissions=True)
		else:
			cls.test_warehouse = "Test POS Warehouse - _TC"

		# Create test item group
		if not frappe.db.exists("Item Group", "Test POS Items"):
			frappe.get_doc(
				{
					"doctype": "Item Group",
					"item_group_name": "Test POS Items",
					"parent_item_group": "All Item Groups",
				}
			).insert(ignore_permissions=True)

		# Create test items
		cls.test_items = []
		for i in range(1, 4):
			item_code = f"TEST-POS-ITEM-{i:03d}"
			if not frappe.db.exists("Item", item_code):
				item = frappe.get_doc(
					{
						"doctype": "Item",
						"item_code": item_code,
						"item_name": f"Test POS Item {i}",
						"item_group": "Test POS Items",
						"stock_uom": "Nos",
						"is_stock_item": 1,
						"is_sales_item": 1,
						"standard_rate": 100.0 * i,
					}
				).insert(ignore_permissions=True)
				cls.test_items.append(item.name)
			else:
				cls.test_items.append(item_code)

		frappe.db.commit()

	def setUp(self):
		"""Set up for each test."""
		frappe.set_user("Administrator")

	def tearDown(self):
		"""Clean up after each test."""
		frappe.db.rollback()

	# ==========================================================================
	# CREATE POS INVOICE TESTS
	# ==========================================================================

	def test_create_pos_invoice_basic(self):
		"""Test basic POS invoice creation with single item and payment."""
		from zevar_core.api.pos import create_pos_invoice

		items = json.dumps(
			[
				{
					"item_code": self.test_items[0],
					"qty": 1,
					"rate": 100.0,
				}
			]
		)

		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": 100.0,
				}
			]
		)

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
		)

		self.assertTrue(result.get("success"))
		self.assertIsNotNone(result.get("invoice_name"))
		self.assertEqual(result.get("status"), "Overdue")

		# Verify invoice was created
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))
		self.assertEqual(si.is_pos, 1)
		self.assertEqual(si.update_stock, 1)
		self.assertEqual(len(si.items), 1)

	def test_create_pos_invoice_multiple_items(self):
		"""Test POS invoice creation with multiple items."""
		from zevar_core.api.pos import create_pos_invoice

		items = json.dumps(
			[
				{"item_code": self.test_items[0], "qty": 2, "rate": 100.0},
				{"item_code": self.test_items[1], "qty": 1, "rate": 200.0},
			]
		)

		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": 400.0,
				}
			]
		)

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
		)

		self.assertTrue(result.get("success"))
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))
		self.assertEqual(len(si.items), 2)

	def test_create_pos_invoice_split_tender(self):
		"""Test POS invoice with multiple payment modes (split tender)."""
		from zevar_core.api.pos import create_pos_invoice

		items = json.dumps(
			[
				{
					"item_code": self.test_items[0],
					"qty": 1,
					"rate": 500.0,
				}
			]
		)

		payments = json.dumps(
			[
				{"mode_of_payment": "Cash", "amount": 200.0},
				{"mode_of_payment": "Credit Card", "amount": 300.0},
			]
		)

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
		)

		self.assertTrue(result.get("success"))
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))
		self.assertEqual(len(si.payments), 2)

	def test_create_pos_invoice_no_items_throws_error(self):
		"""Test that creating invoice without items throws error."""
		from zevar_core.api.pos import create_pos_invoice

		with self.assertRaises(frappe.exceptions.ValidationError):
			create_pos_invoice(
				items="[]",
				payments=json.dumps([{"mode_of_payment": "Cash", "amount": 100.0}]),
				customer=self.test_customer.name
				if hasattr(self.test_customer, "name")
				else self.test_customer,
			)

	def test_create_pos_invoice_no_payments_throws_error(self):
		"""Test that creating invoice without payments throws error."""
		from zevar_core.api.pos import create_pos_invoice

		with self.assertRaises(frappe.exceptions.ValidationError):
			create_pos_invoice(
				items=json.dumps([{"item_code": self.test_items[0], "qty": 1, "rate": 100.0}]),
				payments="[]",
				customer=self.test_customer.name
				if hasattr(self.test_customer, "name")
				else self.test_customer,
			)

	def test_create_pos_invoice_invalid_qty_throws_error(self):
		"""Test that zero or negative quantity throws error."""
		from zevar_core.api.pos import create_pos_invoice

		with self.assertRaises(frappe.exceptions.ValidationError):
			create_pos_invoice(
				items=json.dumps([{"item_code": self.test_items[0], "qty": 0, "rate": 100.0}]),
				payments=json.dumps([{"mode_of_payment": "Cash", "amount": 100.0}]),
				customer=self.test_customer.name
				if hasattr(self.test_customer, "name")
				else self.test_customer,
			)

	def test_create_pos_invoice_invalid_rate_throws_error(self):
		"""Test that zero or negative rate throws error."""
		from zevar_core.api.pos import create_pos_invoice

		with self.assertRaises(frappe.exceptions.ValidationError):
			create_pos_invoice(
				items=json.dumps([{"item_code": self.test_items[0], "qty": 1, "rate": 0}]),
				payments=json.dumps([{"mode_of_payment": "Cash", "amount": 100.0}]),
				customer=self.test_customer.name
				if hasattr(self.test_customer, "name")
				else self.test_customer,
			)

	def test_create_pos_invoice_with_salespersons(self):
		"""Test POS invoice with salesperson assignments."""
		from zevar_core.api.pos import create_pos_invoice

		# Create test employee
		if not frappe.db.exists("Employee", "TEST-EMP-001"):
			emp = frappe.get_doc(
				{
					"doctype": "Employee",
					"first_name": "Test",
					"last_name": "Salesperson",
					"naming_series": "EMP-",
				}
			).insert(ignore_permissions=True)
			emp_id = emp.name
		else:
			emp_id = "TEST-EMP-001"

		items = json.dumps([{"item_code": self.test_items[0], "qty": 1, "rate": 100.0}])
		payments = json.dumps([{"mode_of_payment": "Cash", "amount": 100.0}])
		salespersons = json.dumps([{"employee": emp_id, "split": 100}])

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
			salespersons=salespersons,
		)

		self.assertTrue(result.get("success"))
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))
		self.assertEqual(si.custom_salesperson_1, emp_id)
		self.assertEqual(flt(si.custom_salesperson_1_split), 100.0)

	def test_create_pos_invoice_salesperson_split_validation(self):
		"""Test that salesperson splits must total 100%."""
		from zevar_core.api.pos import create_pos_invoice

		# Create test employees
		employees = []
		for i in range(2):
			emp_id = f"TEST-EMP-{i:03d}"
			if not frappe.db.exists("Employee", emp_id):
				emp = frappe.get_doc(
					{
						"doctype": "Employee",
						"first_name": f"Test {i}",
						"last_name": "Salesperson",
						"naming_series": "EMP-",
					}
				).insert(ignore_permissions=True)
				employees.append(emp.name)
			else:
				employees.append(emp_id)

		items = json.dumps([{"item_code": self.test_items[0], "qty": 1, "rate": 100.0}])
		payments = json.dumps([{"mode_of_payment": "Cash", "amount": 100.0}])
		# Splits total 80%, should fail
		salespersons = json.dumps(
			[
				{"employee": employees[0], "split": 50},
				{"employee": employees[1], "split": 30},
			]
		)

		with self.assertRaises(frappe.exceptions.ValidationError):
			create_pos_invoice(
				items=items,
				payments=payments,
				customer=self.test_customer.name
				if hasattr(self.test_customer, "name")
				else self.test_customer,
				warehouse=self.test_warehouse.name
				if hasattr(self.test_warehouse, "name")
				else self.test_warehouse,
				salespersons=salespersons,
			)


class TestTaxCalculation(FrappeTestCase):
	"""Test suite for POS tax calculation functionality."""

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.company = frappe.defaults.get_user_default("Company") or frappe.db.get_single_value(
			"Global Defaults", "default_company"
		)

	def setUp(self):
		frappe.set_user("Administrator")

	def tearDown(self):
		frappe.db.rollback()

	def test_calculate_invoice_totals_basic(self):
		"""Test basic invoice totals calculation without tax."""
		from zevar_core.api.pos import calculate_invoice_totals

		items = json.dumps(
			[
				{"item_code": "ITEM-001", "qty": 2, "rate": 100.0},
				{"item_code": "ITEM-002", "qty": 1, "rate": 50.0},
			]
		)

		result = calculate_invoice_totals(items=items, tax_exempt=True)

		self.assertEqual(result["subtotal"], 250.0)
		self.assertEqual(result["discount"], 0.0)
		self.assertEqual(result["subtotal_after_discount"], 250.0)
		self.assertEqual(result["tax"], 0.0)
		self.assertEqual(result["grand_total"], 250.0)

	def test_calculate_invoice_totals_with_discount(self):
		"""Test invoice totals calculation with discount."""
		from zevar_core.api.pos import calculate_invoice_totals

		items = json.dumps([{"item_code": "ITEM-001", "qty": 1, "rate": 200.0}])

		result = calculate_invoice_totals(
			items=items,
			tax_exempt=True,
			discount_amount=50.0,
		)

		self.assertEqual(result["subtotal"], 200.0)
		self.assertEqual(result["discount"], 50.0)
		self.assertEqual(result["subtotal_after_discount"], 150.0)
		self.assertEqual(result["grand_total"], 150.0)

	def test_calculate_invoice_totals_with_tax(self):
		"""Test invoice totals calculation with tax based on warehouse."""
		from zevar_core.api.pos import calculate_invoice_totals

		items = json.dumps([{"item_code": "ITEM-001", "qty": 1, "rate": 100.0}])

		# Test with warehouse that has tax rate
		result = calculate_invoice_totals(
			items=items,
			tax_exempt=False,
			discount_amount=0,
			warehouse="California Store",
		)

		self.assertEqual(result["subtotal"], 100.0)
		# Tax rate should be determined by warehouse location
		self.assertGreaterEqual(result["tax"], 0.0)
		self.assertEqual(result["grand_total"], result["subtotal_after_discount"] + result["tax"])

	def test_calculate_invoice_totals_tax_exempt(self):
		"""Test that tax exempt flag sets tax to zero."""
		from zevar_core.api.pos import calculate_invoice_totals

		items = json.dumps([{"item_code": "ITEM-001", "qty": 1, "rate": 100.0}])

		result = calculate_invoice_totals(
			items=items,
			tax_exempt=True,
			discount_amount=0,
			warehouse="California Store",
		)

		self.assertEqual(result["tax"], 0.0)

	def test_calculate_invoice_totals_discount_exceeds_subtotal(self):
		"""Test that grand total is not negative when discount exceeds subtotal."""
		from zevar_core.api.pos import calculate_invoice_totals

		items = json.dumps([{"item_code": "ITEM-001", "qty": 1, "rate": 100.0}])

		result = calculate_invoice_totals(
			items=items,
			tax_exempt=True,
			discount_amount=150.0,
		)

		self.assertEqual(result["subtotal"], 100.0)
		self.assertEqual(result["discount"], 150.0)
		self.assertEqual(result["subtotal_after_discount"], 0.0)
		self.assertEqual(result["grand_total"], 0.0)

	def test_get_pos_settings_returns_tax_rate(self):
		"""Test that get_pos_settings returns tax rate based on warehouse."""
		from zevar_core.api.pos import get_pos_settings

		result = get_pos_settings()

		self.assertIn("tax_rate", result)
		self.assertIn("currency", result)
		self.assertIn("company", result)
		self.assertIn("payment_modes", result)
		self.assertIsInstance(result["tax_rate"], (int, float))

	def test_get_pos_settings_with_warehouse(self):
		"""Test that get_pos_settings determines tax from warehouse name."""
		from zevar_core.api.pos import get_pos_settings

		# Test with California warehouse
		result = get_pos_settings(warehouse="California Store Warehouse")
		self.assertGreaterEqual(result["tax_rate"], 0.0)


class TestTradeInDeduction(FrappeTestCase):
	"""Test suite for trade-in deduction logic."""

	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.create_test_data()

	@classmethod
	def create_test_data(cls):
		"""Create test data for trade-in tests."""
		cls.company = frappe.defaults.get_user_default("Company") or frappe.db.get_single_value(
			"Global Defaults", "default_company"
		)

		# Create test customer
		if not frappe.db.exists("Customer", "Test Trade-In Customer"):
			cls.test_customer = frappe.get_doc(
				{
					"doctype": "Customer",
					"customer_name": "Test Trade-In Customer",
					"customer_type": "Individual",
					"customer_group": "Individual",
					"territory": "All Territories",
				}
			).insert(ignore_permissions=True)
		else:
			cls.test_customer = "Test Trade-In Customer"

		# Create test warehouse
		if not frappe.db.exists("Warehouse", "Test Trade-In Warehouse - _TC"):
			cls.test_warehouse = frappe.get_doc(
				{
					"doctype": "Warehouse",
					"warehouse_name": "Test Trade-In Warehouse",
					"company": cls.company,
				}
			).insert(ignore_permissions=True)
		else:
			cls.test_warehouse = "Test Trade-In Warehouse - _TC"

		# Create test item
		if not frappe.db.exists("Item", "TEST-TRADEIN-ITEM"):
			cls.test_item = frappe.get_doc(
				{
					"doctype": "Item",
					"item_code": "TEST-TRADEIN-ITEM",
					"item_name": "Test Trade-In Item",
					"item_group": "All Item Groups",
					"stock_uom": "Nos",
					"is_stock_item": 1,
					"is_sales_item": 1,
					"standard_rate": 500.0,
				}
			).insert(ignore_permissions=True)
		else:
			cls.test_item = "TEST-TRADEIN-ITEM"

		frappe.db.commit()

	def setUp(self):
		frappe.set_user("Administrator")

	def tearDown(self):
		frappe.db.rollback()

	def test_create_pos_invoice_with_trade_in(self):
		"""Test POS invoice creation with trade-in items."""
		from zevar_core.api.pos import create_pos_invoice

		items = json.dumps(
			[
				{
					"item_code": self.test_item.name if hasattr(self.test_item, "name") else self.test_item,
					"qty": 1,
					"rate": 500.0,
				}
			]
		)

		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": 300.0,  # Reduced by trade-in value
				}
			]
		)

		trade_ins = json.dumps(
			[
				{
					"trade_in_value": 200.0,
					"new_item_value": 500.0,
					"manager_override": "",
					"override_reason": "",
				}
			]
		)

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
			trade_ins=trade_ins,
		)

		self.assertTrue(result.get("success"))
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))
		self.assertEqual(len(si.custom_trade_ins), 1)
		self.assertEqual(flt(si.custom_trade_ins[0].trade_in_value), 200.0)

	def test_create_pos_invoice_multiple_trade_ins(self):
		"""Test POS invoice with multiple trade-in items."""
		from zevar_core.api.pos import create_pos_invoice

		items = json.dumps(
			[
				{
					"item_code": self.test_item.name if hasattr(self.test_item, "name") else self.test_item,
					"qty": 1,
					"rate": 1000.0,
				}
			]
		)

		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": 500.0,
				}
			]
		)

		trade_ins = json.dumps(
			[
				{
					"trade_in_value": 300.0,
					"new_item_value": 500.0,
					"manager_override": "",
					"override_reason": "",
				},
				{
					"trade_in_value": 200.0,
					"new_item_value": 500.0,
					"manager_override": "",
					"override_reason": "",
				},
			]
		)

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
			trade_ins=trade_ins,
		)

		self.assertTrue(result.get("success"))
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))
		self.assertEqual(len(si.custom_trade_ins), 2)

	def test_create_pos_invoice_trade_in_with_manager_override(self):
		"""Test POS invoice with trade-in requiring manager override."""
		from zevar_core.api.pos import create_pos_invoice

		items = json.dumps(
			[
				{
					"item_code": self.test_item.name if hasattr(self.test_item, "name") else self.test_item,
					"qty": 1,
					"rate": 500.0,
				}
			]
		)

		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": 200.0,
				}
			]
		)

		trade_ins = json.dumps(
			[
				{
					"trade_in_value": 300.0,
					"new_item_value": 500.0,
					"manager_override": "Manager Name",
					"override_reason": "Customer loyalty discount",
				}
			]
		)

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
			trade_ins=trade_ins,
		)

		self.assertTrue(result.get("success"))
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))
		self.assertEqual(si.custom_trade_ins[0].manager_override, "Manager Name")
		self.assertEqual(si.custom_trade_ins[0].override_reason, "Customer loyalty discount")

	def test_trade_in_value_zero(self):
		"""Test POS invoice with zero trade-in value."""
		from zevar_core.api.pos import create_pos_invoice

		items = json.dumps(
			[
				{
					"item_code": self.test_item.name if hasattr(self.test_item, "name") else self.test_item,
					"qty": 1,
					"rate": 500.0,
				}
			]
		)

		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": 500.0,
				}
			]
		)

		trade_ins = json.dumps(
			[
				{
					"trade_in_value": 0.0,
					"new_item_value": 500.0,
					"manager_override": "",
					"override_reason": "",
				}
			]
		)

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
			trade_ins=trade_ins,
		)

		self.assertTrue(result.get("success"))
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))
		self.assertEqual(flt(si.custom_trade_ins[0].trade_in_value), 0.0)

	def test_trade_in_creates_payment_entry(self):
		"""Test that trade-in creates a payment entry with mode 'Trade-In'."""
		from zevar_core.api.pos import create_pos_invoice

		items = json.dumps(
			[
				{
					"item_code": self.test_item.name if hasattr(self.test_item, "name") else self.test_item,
					"qty": 1,
					"rate": 500.0,
				}
			]
		)

		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": 300.0,
				}
			]
		)

		trade_ins = json.dumps(
			[
				{
					"trade_in_value": 200.0,
					"new_item_value": 500.0,
					"manager_override": "",
					"override_reason": "",
				}
			]
		)

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
			trade_ins=trade_ins,
		)

		self.assertTrue(result.get("success"))
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))

		# Verify trade-in payment entry exists
		trade_in_payment = [p for p in si.payments if p.mode_of_payment == "Trade-In"]
		self.assertEqual(len(trade_in_payment), 1, "Trade-In payment entry should exist")
		self.assertEqual(flt(trade_in_payment[0].amount), 200.0)

		# Verify total paid_amount covers grand_total
		total_paid = sum(flt(p.amount) for p in si.payments)
		self.assertGreaterEqual(
			total_paid, flt(si.grand_total) - 0.01, "Total payments should cover grand total"
		)

	def test_multiple_trade_ins_summed_in_payment_entry(self):
		"""Test that multiple trade-ins are summed into single payment entry."""
		from zevar_core.api.pos import create_pos_invoice

		items = json.dumps(
			[
				{
					"item_code": self.test_item.name if hasattr(self.test_item, "name") else self.test_item,
					"qty": 1,
					"rate": 1000.0,
				}
			]
		)

		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": 500.0,
				}
			]
		)

		trade_ins = json.dumps(
			[
				{
					"trade_in_value": 300.0,
					"new_item_value": 500.0,
					"manager_override": "",
					"override_reason": "",
				},
				{
					"trade_in_value": 200.0,
					"new_item_value": 500.0,
					"manager_override": "",
					"override_reason": "",
				},
			]
		)

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
			trade_ins=trade_ins,
		)

		self.assertTrue(result.get("success"))
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))

		# Verify single trade-in payment entry with summed amount
		trade_in_payment = [p for p in si.payments if p.mode_of_payment == "Trade-In"]
		self.assertEqual(len(trade_in_payment), 1)
		self.assertEqual(flt(trade_in_payment[0].amount), 500.0)  # 300 + 200

	def test_trade_in_covers_full_amount(self):
		"""Test trade-in that covers full invoice amount with no additional payment."""
		from zevar_core.api.pos import create_pos_invoice

		items = json.dumps(
			[
				{
					"item_code": self.test_item.name if hasattr(self.test_item, "name") else self.test_item,
					"qty": 1,
					"rate": 500.0,
				}
			]
		)

		# No additional payment needed - trade-in covers full amount
		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": 0.0,
				}
			]
		)

		trade_ins = json.dumps(
			[
				{
					"trade_in_value": 500.0,
					"new_item_value": 1000.0,
					"manager_override": "",
					"override_reason": "",
				}
			]
		)

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
			trade_ins=trade_ins,
			tax_exempt=True,
		)

		self.assertTrue(result.get("success"))
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))

		# Verify trade-in payment covers full amount
		trade_in_payment = [p for p in si.payments if p.mode_of_payment == "Trade-In"]
		self.assertEqual(flt(trade_in_payment[0].amount), 500.0)

		# Verify invoice is fully paid
		total_paid = sum(flt(p.amount) for p in si.payments)
		self.assertGreaterEqual(total_paid, flt(si.grand_total) - 0.01)

	def test_trade_in_with_split_tender(self):
		"""Test trade-in combined with other payment modes (split tender)."""
		from zevar_core.api.pos import create_pos_invoice

		items = json.dumps(
			[
				{
					"item_code": self.test_item.name if hasattr(self.test_item, "name") else self.test_item,
					"qty": 1,
					"rate": 1000.0,
				}
			]
		)

		payments = json.dumps(
			[
				{"mode_of_payment": "Cash", "amount": 300.0},
				{"mode_of_payment": "Credit Card", "amount": 200.0},
			]
		)

		trade_ins = json.dumps(
			[
				{
					"trade_in_value": 500.0,
					"new_item_value": 1000.0,
					"manager_override": "",
					"override_reason": "",
				}
			]
		)

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
			trade_ins=trade_ins,
			tax_exempt=True,
		)

		self.assertTrue(result.get("success"))
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))

		# Verify all payment modes exist
		payment_modes = {p.mode_of_payment for p in si.payments}
		self.assertIn("Trade-In", payment_modes)
		self.assertIn("Cash", payment_modes)
		self.assertIn("Credit Card", payment_modes)

		# Verify total paid covers grand total
		total_paid = sum(flt(p.amount) for p in si.payments)
		self.assertGreaterEqual(total_paid, flt(si.grand_total) - 0.01)

	def test_zero_trade_in_no_payment_entry(self):
		"""Test that zero trade-in value does not create a payment entry."""
		from zevar_core.api.pos import create_pos_invoice

		items = json.dumps(
			[
				{
					"item_code": self.test_item.name if hasattr(self.test_item, "name") else self.test_item,
					"qty": 1,
					"rate": 500.0,
				}
			]
		)

		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": 500.0,
				}
			]
		)

		trade_ins = json.dumps(
			[
				{
					"trade_in_value": 0.0,
					"new_item_value": 500.0,
					"manager_override": "",
					"override_reason": "",
				}
			]
		)

		result = create_pos_invoice(
			items=items,
			payments=payments,
			customer=self.test_customer.name if hasattr(self.test_customer, "name") else self.test_customer,
			warehouse=self.test_warehouse.name
			if hasattr(self.test_warehouse, "name")
			else self.test_warehouse,
			trade_ins=trade_ins,
			tax_exempt=True,
		)

		self.assertTrue(result.get("success"))
		si = frappe.get_doc("Sales Invoice", result.get("invoice_name"))

		# Verify no Trade-In payment entry for zero value
		trade_in_payment = [p for p in si.payments if p.mode_of_payment == "Trade-In"]
		self.assertEqual(len(trade_in_payment), 0, "Zero trade-in should not create payment entry")
