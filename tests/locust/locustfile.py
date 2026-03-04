"""
Locust Load Test for POS Module
Simulates 50 concurrent cashiers performing POS operations

Tests:
- get_pos_items: Catalog browsing with pagination
- create_pos_invoice: Invoice creation with items and payments
"""

import json
import random
import string

from typing import ClassVar

from locust import HttpUser, between, events, task
from locust.runners import MasterRunner, WorkerRunner


class POSCashierUser(HttpUser):
	"""
	Simulates a POS cashier performing typical operations:
	1. Browse catalog (get_pos_items)
	2. Create invoices (create_pos_invoice)
	"""

	# Wait time between tasks (1-3 seconds to simulate realistic user behavior)
	wait_time = between(1, 3)

	# Class variables for shared data
	item_codes: ClassVar[list] = []
	warehouse = "Stores - _TC"
	customer = "Walk-In Customer"

	def on_start(self):
		"""Initialize user session with login and fetch initial data."""
		self.login()
		self.fetch_csrf_token()
		self.load_item_codes()

	def login(self):
		"""Login to Frappe and establish session."""
		response = self.client.post(
			"/api/method/login",
			data={
				"usr": "Administrator",
				"pwd": "admin",
			},
			name="login",
		)
		if response.status_code != 200:
			print(f"Login failed: {response.text}")

	def fetch_csrf_token(self):
		"""Fetch CSRF token for subsequent POST requests."""
		response = self.client.get(
			"/api/method/frappe.sessions.get",
			name="get_csrf",
		)
		if response.status_code == 200:
			try:
				data = response.json()
				self.csrf_token = data.get("message", {}).get("csrf_token", "")
			except Exception:
				self.csrf_token = ""

	def load_item_codes(self):
		"""Pre-load item codes for testing."""
		if POSCashierUser.item_codes:
			return

		response = self.client.get(
			"/api/method/zevar_core.api.catalog.get_pos_items",
			params={
				"start": 0,
				"page_length": 50,
				"warehouse": POSCashierUser.warehouse,
			},
			name="load_items",
		)

		if response.status_code == 200:
			try:
				data = response.json()
				items = data.get("message", [])
				POSCashierUser.item_codes = [item.get("item_code") for item in items if item.get("item_code")]
			except Exception:
				# Use fallback item codes if API fails
				POSCashierUser.item_codes = [f"ITEM-{i:04d}" for i in range(1, 51)]

	# ==========================================================================
	# TASK 1: GET POS ITEMS (Catalog Browsing)
	# ==========================================================================

	@task(5)  # Higher weight - browsing is more frequent
	def get_pos_items_basic(self):
		"""Test basic catalog item retrieval with pagination."""
		self.client.get(
			"/api/method/zevar_core.api.catalog.get_pos_items",
			params={
				"start": 0,
				"page_length": 20,
				"warehouse": POSCashierUser.warehouse,
			},
			name="get_pos_items_basic",
		)

	@task(3)
	def get_pos_items_with_search(self):
		"""Test catalog search functionality."""
		search_terms = ["ring", "gold", "diamond", "necklace", "bracelet"]
		search_term = random.choice(search_terms)

		self.client.get(
			"/api/method/zevar_core.api.catalog.get_pos_items",
			params={
				"start": 0,
				"page_length": 20,
				"warehouse": POSCashierUser.warehouse,
				"search_term": search_term,
			},
			name="get_pos_items_search",
		)

	@task(2)
	def get_pos_items_with_filters(self):
		"""Test catalog filtering."""
		filters = json.dumps(
			{
				"custom_metal_type": random.choice(["Yellow Gold", "White Gold", "Rose Gold"]),
			}
		)

		self.client.get(
			"/api/method/zevar_core.api.catalog.get_pos_items",
			params={
				"start": 0,
				"page_length": 20,
				"warehouse": POSCashierUser.warehouse,
				"filters": filters,
			},
			name="get_pos_items_filtered",
		)

	@task(2)
	def get_pos_items_pagination(self):
		"""Test catalog pagination (load more)."""
		start = random.choice([0, 20, 40, 60, 80])

		self.client.get(
			"/api/method/zevar_core.api.catalog.get_pos_items",
			params={
				"start": start,
				"page_length": 20,
				"warehouse": POSCashierUser.warehouse,
			},
			name="get_pos_items_pagination",
		)

	@task(1)
	def get_pos_items_stock_filter(self):
		"""Test in-stock only filter."""
		self.client.get(
			"/api/method/zevar_core.api.catalog.get_pos_items",
			params={
				"start": 0,
				"page_length": 20,
				"warehouse": POSCashierUser.warehouse,
				"in_stock_only": "true",
			},
			name="get_pos_items_in_stock",
		)

	# ==========================================================================
	# TASK 2: CREATE POS INVOICE
	# ==========================================================================

	@task(2)  # Lower weight - invoice creation is less frequent
	def create_pos_invoice_single_item(self):
		"""Test creating invoice with single item."""
		if not POSCashierUser.item_codes:
			return

		item_code = random.choice(POSCashierUser.item_codes)
		rate = round(random.uniform(100, 1000), 2)

		items = json.dumps(
			[
				{
					"item_code": item_code,
					"qty": 1,
					"rate": rate,
				}
			]
		)

		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": rate,
				}
			]
		)

		self.client.post(
			"/api/method/zevar_core.api.pos.create_pos_invoice",
			data={
				"items": items,
				"payments": payments,
				"customer": POSCashierUser.customer,
				"warehouse": POSCashierUser.warehouse,
				"tax_exempt": "false",
			},
			headers={
				"Content-Type": "application/x-www-form-urlencoded",
				"X-Frappe-CSRF-Token": self.csrf_token,
			},
			name="create_pos_invoice_single",
		)

	@task(1)
	def create_pos_invoice_multiple_items(self):
		"""Test creating invoice with multiple items."""
		if len(POSCashierUser.item_codes) < 3:
			return

		# Select 2-4 random items
		num_items = random.randint(2, 4)
		selected_items = random.sample(POSCashierUser.item_codes, num_items)

		items_list = []
		total = 0
		for item_code in selected_items:
			rate = round(random.uniform(100, 500), 2)
			qty = random.randint(1, 2)
			items_list.append(
				{
					"item_code": item_code,
					"qty": qty,
					"rate": rate,
				}
			)
			total += rate * qty

		items = json.dumps(items_list)
		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": round(total, 2),
				}
			]
		)

		self.client.post(
			"/api/method/zevar_core.api.pos.create_pos_invoice",
			data={
				"items": items,
				"payments": payments,
				"customer": POSCashierUser.customer,
				"warehouse": POSCashierUser.warehouse,
				"tax_exempt": "false",
			},
			headers={
				"Content-Type": "application/x-www-form-urlencoded",
				"X-Frappe-CSRF-Token": self.csrf_token,
			},
			name="create_pos_invoice_multiple",
		)

	@task(1)
	def create_pos_invoice_split_tender(self):
		"""Test creating invoice with split payment."""
		if not POSCashierUser.item_codes:
			return

		item_code = random.choice(POSCashierUser.item_codes)
		rate = round(random.uniform(200, 800), 2)

		items = json.dumps(
			[
				{
					"item_code": item_code,
					"qty": 1,
					"rate": rate,
				}
			]
		)

		# Split payment between cash and card
		cash_amount = round(rate * 0.6, 2)
		card_amount = round(rate - cash_amount, 2)

		payments = json.dumps(
			[
				{"mode_of_payment": "Cash", "amount": cash_amount},
				{"mode_of_payment": "Credit Card", "amount": card_amount},
			]
		)

		self.client.post(
			"/api/method/zevar_core.api.pos.create_pos_invoice",
			data={
				"items": items,
				"payments": payments,
				"customer": POSCashierUser.customer,
				"warehouse": POSCashierUser.warehouse,
				"tax_exempt": "false",
			},
			headers={
				"Content-Type": "application/x-www-form-urlencoded",
				"X-Frappe-CSRF-Token": self.csrf_token,
			},
			name="create_pos_invoice_split",
		)

	@task(1)
	def create_pos_invoice_with_discount(self):
		"""Test creating invoice with discount."""
		if not POSCashierUser.item_codes:
			return

		item_code = random.choice(POSCashierUser.item_codes)
		rate = round(random.uniform(200, 600), 2)
		discount = round(random.uniform(10, 50), 2)

		items = json.dumps(
			[
				{
					"item_code": item_code,
					"qty": 1,
					"rate": rate,
				}
			]
		)

		payments = json.dumps(
			[
				{
					"mode_of_payment": "Cash",
					"amount": round(rate - discount, 2),
				}
			]
		)

		self.client.post(
			"/api/method/zevar_core.api.pos.create_pos_invoice",
			data={
				"items": items,
				"payments": payments,
				"customer": POSCashierUser.customer,
				"warehouse": POSCashierUser.warehouse,
				"discount_amount": discount,
				"tax_exempt": "false",
			},
			headers={
				"Content-Type": "application/x-www-form-urlencoded",
				"X-Frappe-CSRF-Token": self.csrf_token,
			},
			name="create_pos_invoice_discount",
		)

	# ==========================================================================
	# TASK 3: GET POS SETTINGS
	# ==========================================================================

	@task(3)
	def get_pos_settings(self):
		"""Test fetching POS settings including tax rate."""
		self.client.get(
			"/api/method/zevar_core.api.pos.get_pos_settings",
			params={
				"warehouse": POSCashierUser.warehouse,
			},
			name="get_pos_settings",
		)

	# ==========================================================================
	# TASK 4: CALCULATE INVOICE TOTALS
	# ==========================================================================

	@task(2)
	def calculate_invoice_totals(self):
		"""Test invoice totals calculation."""
		if not POSCashierUser.item_codes:
			return

		item_code = random.choice(POSCashierUser.item_codes)
		rate = round(random.uniform(100, 500), 2)

		items = json.dumps(
			[
				{
					"item_code": item_code,
					"qty": random.randint(1, 3),
					"rate": rate,
				}
			]
		)

		self.client.get(
			"/api/method/zevar_core.api.pos.calculate_invoice_totals",
			params={
				"items": items,
				"tax_exempt": "false",
				"discount_amount": 0,
				"warehouse": POSCashierUser.warehouse,
			},
			name="calculate_totals",
		)


# ==========================================================================
# EVENT HANDLERS
# ==========================================================================


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
	"""Called when test starts."""
	print("\n" + "=" * 60)
	print("POS Module Load Test Starting")
	print("=" * 60)
	print("Target: 50 concurrent cashiers")
	print("Operations: get_pos_items, create_pos_invoice")
	print("=" * 60 + "\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
	"""Called when test stops."""
	print("\n" + "=" * 60)
	print("POS Module Load Test Completed")
	print("=" * 60 + "\n")


# ==========================================================================
# CONFIGURATION FOR DIFFERENT TEST SCENARIOS
# ==========================================================================


class HighVolumeCashierUser(POSCashierUser):
	"""High-volume user for stress testing - faster operations."""

	wait_time = between(0.5, 1.5)


class BrowsingOnlyUser(HttpUser):
	"""User that only browses catalog - no purchases."""

	wait_time = between(2, 5)

	def on_start(self):
		self.login()

	def login(self):
		self.client.post(
			"/api/method/login",
			data={"usr": "Administrator", "pwd": "admin"},
			name="login",
		)

	@task
	def browse_catalog(self):
		start = random.choice([0, 20, 40])
		self.client.get(
			"/api/method/zevar_core.api.catalog.get_pos_items",
			params={
				"start": start,
				"page_length": 20,
			},
			name="browse_catalog",
		)


# ==========================================================================
# RUN COMMANDS
# ==========================================================================

# Run with 50 concurrent users:
# locust -f locustfile.py --users 50 --spawn-rate 5 --host http://localhost:8000
#
# Run with web UI:
# locust -f locustfile.py --host http://localhost:8000
#
# Run distributed (master):
# locust -f locustfile.py --master --users 50 --host http://localhost:8000
#
# Run distributed (worker):
# locust -f locustfile.py --worker --master-host=<master-ip>
