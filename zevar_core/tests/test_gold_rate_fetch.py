import json
from unittest.mock import MagicMock, patch

import frappe
from frappe.tests.utils import FrappeTestCase

from zevar_core.constants import TROY_OZ_TO_GRAMS


class TestGoldRateFetch(FrappeTestCase):
	def setUp(self):
		self.ensure_test_metal_and_purity()
		self.cleanup_rate_logs()

	def tearDown(self):
		self.cleanup_rate_logs()

	def ensure_test_metal_and_purity(self):
		metals = ["Yellow Gold", "Silver"]
		for metal in metals:
			if not frappe.db.exists("Zevar Metal", metal):
				frappe.get_doc({"doctype": "Zevar Metal", "__newname": metal}).insert(ignore_permissions=True)

		purities = {
			"24K": 0.999,
			"22K": 0.916,
			"18Kt": 0.750,
			"14Kt": 0.585,
			"10k": 0.417,
			"999 Fine": 0.999,
			"925 Sterling": 0.925,
		}
		for name, content in purities.items():
			if not frappe.db.exists("Zevar Purity", name):
				frappe.get_doc(
					{"doctype": "Zevar Purity", "__newname": name, "fine_metal_content": content}
				).insert(ignore_permissions=True)
		frappe.db.commit()

	def cleanup_rate_logs(self):
		for name in frappe.get_all("Gold Rate Log", filters={"source": "test-mock"}, pluck="name"):
			frappe.delete_doc("Gold Rate Log", name, ignore_permissions=True, force=True)

	@patch("zevar_core.tasks.requests.get")
	def test_fetch_live_metal_rates_with_mock(self, mock_get):
		mock_response = MagicMock()
		mock_response.json.return_value = {"items": [{"xauPrice": 2650.0, "xagPrice": 32.0}]}
		mock_response.raise_for_status = MagicMock()
		mock_get.return_value = mock_response

		from zevar_core.tasks import fetch_live_metal_rates

		fetch_live_metal_rates()

		gold_24k_rate = 2650.0 / TROY_OZ_TO_GRAMS * 0.999
		silver_999_rate = 32.0 / TROY_OZ_TO_GRAMS * 0.999

		gold_entry = frappe.get_all(
			"Gold Rate Log",
			filters={"metal": "Yellow Gold", "purity": "24K"},
			fields=["rate_per_gram"],
			order_by="creation desc",
			limit=1,
		)
		self.assertTrue(len(gold_entry) > 0)
		self.assertAlmostEqual(float(gold_entry[0].rate_per_gram), round(gold_24k_rate, 2), places=1)

		silver_entry = frappe.get_all(
			"Gold Rate Log",
			filters={"metal": "Silver", "purity": "999 Fine"},
			fields=["rate_per_gram"],
			order_by="creation desc",
			limit=1,
		)
		self.assertTrue(len(silver_entry) > 0)
		self.assertAlmostEqual(float(silver_entry[0].rate_per_gram), round(silver_999_rate, 2), places=1)

	@patch("zevar_core.tasks.requests.get")
	def test_fetch_rates_creates_gold_purity_entries(self, mock_get):
		mock_response = MagicMock()
		mock_response.json.return_value = {"items": [{"xauPrice": 2600.0, "xagPrice": 30.0}]}
		mock_response.raise_for_status = MagicMock()
		mock_get.return_value = mock_response

		from zevar_core.tasks import fetch_live_metal_rates

		fetch_live_metal_rates()

		expected_purities = ["24K", "22K", "18Kt", "14Kt", "10k"]
		for purity in expected_purities:
			exists = frappe.db.exists("Gold Rate Log", {"metal": "Yellow Gold", "purity": purity})
			self.assertTrue(exists, f"Gold Rate Log missing for Yellow Gold {purity}")

	@patch("zevar_core.tasks.requests.get")
	def test_fetch_rates_creates_silver_purity_entries(self, mock_get):
		mock_response = MagicMock()
		mock_response.json.return_value = {"items": [{"xauPrice": 2600.0, "xagPrice": 30.0}]}
		mock_response.raise_for_status = MagicMock()
		mock_get.return_value = mock_response

		from zevar_core.tasks import fetch_live_metal_rates

		fetch_live_metal_rates()

		silver_purities = ["999 Fine", "925 Sterling"]
		for purity in silver_purities:
			exists = frappe.db.exists("Gold Rate Log", {"metal": "Silver", "purity": purity})
			self.assertTrue(exists, f"Gold Rate Log missing for Silver {purity}")

	@patch("zevar_core.tasks.requests.get")
	def test_fetch_rates_fallback_on_error(self, mock_get):
		mock_get.side_effect = Exception("Network error")

		from zevar_core.tasks import fetch_live_metal_rates

		fetch_live_metal_rates()

		fallback_gold = 2450.0 / TROY_OZ_TO_GRAMS * 0.999
		gold_entry = frappe.get_all(
			"Gold Rate Log",
			filters={"metal": "Yellow Gold", "purity": "24K"},
			fields=["rate_per_gram"],
			order_by="creation desc",
			limit=1,
		)
		self.assertTrue(len(gold_entry) > 0)
		self.assertAlmostEqual(float(gold_entry[0].rate_per_gram), round(fallback_gold, 2), places=1)

	@patch("zevar_core.tasks.requests.get")
	def test_fetch_rates_updates_existing_entry(self, mock_get):
		from zevar_core.tasks import fetch_live_metal_rates

		mock_response = MagicMock()
		mock_response.raise_for_status = MagicMock()

		mock_response.json.return_value = {"items": [{"xauPrice": 2600.0, "xagPrice": 30.0}]}
		mock_get.return_value = mock_response
		fetch_live_metal_rates()

		first_rate = frappe.get_all(
			"Gold Rate Log",
			filters={"metal": "Yellow Gold", "purity": "24K"},
			fields=["rate_per_gram"],
			order_by="creation desc",
			limit=1,
		)[0].rate_per_gram

		mock_response.json.return_value = {"items": [{"xauPrice": 2700.0, "xagPrice": 31.0}]}
		fetch_live_metal_rates()

		second_rate = frappe.get_all(
			"Gold Rate Log",
			filters={"metal": "Yellow Gold", "purity": "24K"},
			fields=["rate_per_gram"],
			order_by="creation desc",
			limit=1,
		)[0].rate_per_gram

		self.assertNotEqual(float(first_rate), float(second_rate))

	@patch("zevar_core.tasks.requests.get")
	def test_fetch_rates_sets_source_to_goldprice(self, mock_get):
		mock_response = MagicMock()
		mock_response.json.return_value = {"items": [{"xauPrice": 2600.0, "xagPrice": 30.0}]}
		mock_response.raise_for_status = MagicMock()
		mock_get.return_value = mock_response

		from zevar_core.tasks import fetch_live_metal_rates

		fetch_live_metal_rates()

		entry = frappe.get_all(
			"Gold Rate Log",
			filters={"metal": "Yellow Gold", "purity": "24K"},
			fields=["source"],
			order_by="creation desc",
			limit=1,
		)
		self.assertEqual(entry[0].source, "goldprice.org")

	@patch("zevar_core.tasks.requests.get")
	def test_fetch_rates_sends_correct_user_agent(self, mock_get):
		mock_response = MagicMock()
		mock_response.json.return_value = {"items": [{"xauPrice": 2600.0, "xagPrice": 30.0}]}
		mock_response.raise_for_status = MagicMock()
		mock_get.return_value = mock_response

		from zevar_core.tasks import fetch_live_metal_rates

		fetch_live_metal_rates()

		call_args = mock_get.call_args
		self.assertIn("headers", call_args.kwargs or {})
		headers = (call_args.kwargs or {}).get("headers", {})
		self.assertEqual(headers.get("User-Agent"), "Zevar-POS/1.0 (Zevar Jewelers; gold-rate-sync)")

	@patch("zevar_core.tasks.requests.get")
	def test_fetch_rates_purity_calculation_accuracy(self, mock_get):
		mock_response = MagicMock()
		mock_response.json.return_value = {"items": [{"xauPrice": 3103.5, "xagPrice": 31.1035}]}
		mock_response.raise_for_status = MagicMock()
		mock_get.return_value = mock_response

		from zevar_core.tasks import fetch_live_metal_rates

		fetch_live_metal_rates()

		expected_24k = round(3103.5 / TROY_OZ_TO_GRAMS * 0.999, 2)
		expected_22k = round(3103.5 / TROY_OZ_TO_GRAMS * 0.916, 2)
		expected_14k = round(3103.5 / TROY_OZ_TO_GRAMS * 0.585, 2)

		rate_24k = frappe.get_all(
			"Gold Rate Log",
			filters={"metal": "Yellow Gold", "purity": "24K"},
			fields=["rate_per_gram"],
			order_by="creation desc",
			limit=1,
		)[0].rate_per_gram
		self.assertEqual(float(rate_24k), expected_24k)

		rate_22k = frappe.get_all(
			"Gold Rate Log",
			filters={"metal": "Yellow Gold", "purity": "22K"},
			fields=["rate_per_gram"],
			order_by="creation desc",
			limit=1,
		)[0].rate_per_gram
		self.assertEqual(float(rate_22k), expected_22k)

		rate_14k = frappe.get_all(
			"Gold Rate Log",
			filters={"metal": "Yellow Gold", "purity": "14Kt"},
			fields=["rate_per_gram"],
			order_by="creation desc",
			limit=1,
		)[0].rate_per_gram
		self.assertEqual(float(rate_14k), expected_14k)

	def test_troy_oz_to_grams_constant(self):
		self.assertAlmostEqual(TROY_OZ_TO_GRAMS, 31.1035, places=4)

	@patch("zevar_core.tasks.requests.get")
	def test_fetch_live_gold_rate_alias(self, mock_get):
		mock_response = MagicMock()
		mock_response.json.return_value = {"items": [{"xauPrice": 2600.0, "xagPrice": 30.0}]}
		mock_response.raise_for_status = MagicMock()
		mock_get.return_value = mock_response

		from zevar_core.tasks import fetch_live_gold_rate

		fetch_live_gold_rate()

		entry = frappe.get_all(
			"Gold Rate Log",
			filters={"metal": "Yellow Gold", "purity": "24K"},
			pluck="name",
			limit=1,
		)
		self.assertTrue(len(entry) > 0)
