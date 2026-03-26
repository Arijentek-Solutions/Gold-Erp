"""
FoxPro to Frappe Data Migration for Zevar Jewelers

Reads Visual FoxPro .DBF files from the legacy POS system and imports
data into zevar_core DocTypes.

Legacy File Mapping (verified against actual DBF schemas):
- inventor.DBF   → Item (120 records)
- CUSTSHOR.dbf   → Customer (114 records)
- EMPLOYEE.DBF   → Employee (2092 records)
- LOCNAME.dbf    → Store Location (37 records)
- supplier.dbf   → Supplier/Vendor (66 records)
- cat.dbf        → Item Group / Category (63 records)
- KARAT.DBF      → Zevar Purity (6 records)
- COLOR.DBF      → Item Attribute: Color (59 records)
- CLARITY.DBF    → Item Attribute: Clarity (25 records)
- GOLD$.dbf      → Gold Rate Log (5 records)
- 1APTERM1.DBF   → Jewelry Appraisal (schema only, 0 records)
- saletype.dbf   → Repair Type (65 records)
- trans.dbf      → Sales Invoice (516 records)
"""

import os
import json
from datetime import datetime, date
from typing import Dict, List, Optional, Any

import frappe
from frappe import _

try:
	from dbfread import DBF

	HAS_DBFREAD = True
except ImportError:
	HAS_DBFREAD = False


# ──────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────


def check_dbfread():
	"""Verify dbfread is installed."""
	if not HAS_DBFREAD:
		frappe.throw(
			_("dbfread library not installed. Run: pip install dbfread"),
			title=_("Missing Dependency"),
		)


def find_dbf(backup_path: str, filename: str) -> Optional[str]:
	"""Find a DBF file (case-insensitive) in the backup directory."""
	if not os.path.isdir(backup_path):
		return None
	for fname in os.listdir(backup_path):
		if fname.upper() == filename.upper():
			return os.path.join(backup_path, fname)
	return None


def read_dbf(file_path: str, encoding: str = "cp1252") -> List[Dict]:
	"""
	Read a DBF file and return list of clean records.

	Lowercases keys, strips whitespace from strings, handles None/empty.
	"""
	check_dbfread()
	table = DBF(file_path, encoding=encoding, ignore_missing_memofile=True)
	records = []
	for record in table:
		clean = {}
		for key, value in record.items():
			if isinstance(value, str):
				value = value.strip()
			elif isinstance(value, bytes):
				try:
					value = value.decode(encoding).strip()
				except Exception:
					value = str(value)
			if value is not None and value != "":
				clean[key.lower()] = value
		records.append(clean)
	return records


def clean_str(value) -> str:
	"""Safely convert to stripped string."""
	if value is None:
		return ""
	return str(value).strip()


def clean_float(value) -> float:
	"""Safely convert to float."""
	if value is None:
		return 0.0
	try:
		return float(value)
	except (ValueError, TypeError):
		return 0.0


def clean_int(value) -> int:
	"""Safely convert to int."""
	if value is None:
		return 0
	try:
		return int(float(value))
	except (ValueError, TypeError):
		return 0


def format_date(value) -> Optional[str]:
	"""Convert a date value to YYYY-MM-DD string."""
	if value is None:
		return None
	if isinstance(value, date):
		return value.strftime("%Y-%m-%d")
	# Try parsing common FoxPro date strings
	val = str(value).strip()
	if not val:
		return None
	for fmt in ("%Y%m%d", "%m/%d/%Y", "%m-%d-%Y", "%Y-%m-%d", "%m%d%y"):
		try:
			return datetime.strptime(val, fmt).strftime("%Y-%m-%d")
		except ValueError:
			continue
	return None


def parse_hire_date(val) -> Optional[str]:
	"""Parse FoxPro date string like '121790' → '1990-12-17'."""
	if val is None:
		return None
	val = str(val).strip()
	if not val or val == "000000":
		return None
	# Format: MMDDYY
	try:
		dt = datetime.strptime(val, "%m%d%y")
		return dt.strftime("%Y-%m-%d")
	except ValueError:
		return format_date(val)


# ──────────────────────────────────────────────────
# Store Location (from LOCNAME.dbf)
# ──────────────────────────────────────────────────


def import_stores(backup_path: str, dry_run: bool = False) -> Dict:
	"""Import store locations from LOCNAME.dbf."""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	dbf_path = find_dbf(backup_path, "LOCNAME.dbf")
	if not dbf_path:
		stats["errors"].append("LOCNAME.dbf not found")
		return stats

	records = read_dbf(dbf_path)
	stats["total"] = len(records)

	for record in records:
		try:
			loc = clean_str(record.get("loc"))
			locname = clean_str(record.get("locname"))
			if not loc or not locname:
				stats["skipped"] += 1
				continue

			store_code = loc.zfill(2)

			if frappe.db.exists("Store Location", store_code):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			doc = frappe.new_doc("Store Location")
			doc.store_code = store_code
			doc.store_name = locname
			doc.is_active = 1
			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Store {record.get('loc', '?')}: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()
	return stats


# ──────────────────────────────────────────────────
# Employee (from EMPLOYEE.DBF)
# ──────────────────────────────────────────────────

POSITION_MAP = {
	"1": "Sales Associate",
	"2": "Manager",
	"3": "Cashier",
	"9": "System",
}


def _ensure_designation(name: str):
	"""Create a Designation record if it doesn't exist."""
	if name and not frappe.db.exists("Designation", name):
		try:
			doc = frappe.new_doc("Designation")
			doc.designation_name = name
			doc.insert(ignore_permissions=True)
		except frappe.DuplicateEntryError:
			pass


def import_employees(backup_path: str, dry_run: bool = False) -> Dict:
	"""Import employees from EMPLOYEE.DBF."""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	dbf_path = find_dbf(backup_path, "EMPLOYEE.DBF")
	if not dbf_path:
		stats["errors"].append("EMPLOYEE.DBF not found")
		return stats

	records = read_dbf(dbf_path)
	stats["total"] = len(records)

	for idx, record in enumerate(records):
		try:
			empid = clean_str(record.get("empid"))
			clerkname = clean_str(record.get("clerkname"))
			if not empid or not clerkname:
				stats["skipped"] += 1
				continue

			# Skip system/gift certificate entries
			position = clean_str(record.get("position"))
			if position == "9":
				stats["skipped"] += 1
				continue

			if frappe.db.exists("Employee", {"employee_number": empid}):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			doc = frappe.new_doc("Employee")
			doc.employee_number = empid
			doc.employee_name = clerkname

			# Split name on first space
			parts = clerkname.split(" ", 1)
			doc.first_name = parts[0]
			if len(parts) > 1:
				doc.last_name = parts[1]

			doc.status = "Active"
			doc.employment_type = "Full-time"

			if position in POSITION_MAP:
				designation = POSITION_MAP[position]
				_ensure_designation(designation)
				doc.designation = designation

			hire_date = parse_hire_date(record.get("datehire"))
			if hire_date:
				doc.date_of_joining = hire_date

			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

			# Batch commit every 100 records
			if (idx + 1) % 100 == 0:
				frappe.db.commit()

		except Exception as e:
			stats["errors"].append(f"Employee {record.get('empid', '?')}: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()
	return stats


# ──────────────────────────────────────────────────
# Customer (from CUSTSHOR.dbf)
# ──────────────────────────────────────────────────


def import_customers(backup_path: str, dry_run: bool = False) -> Dict:
	"""Import customers from CUSTSHOR.dbf."""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	dbf_path = find_dbf(backup_path, "CUSTSHOR.dbf")
	if not dbf_path:
		stats["errors"].append("CUSTSHOR.dbf not found")
		return stats

	records = read_dbf(dbf_path)
	stats["total"] = len(records)

	for record in records:
		try:
			accountno = clean_str(record.get("accountno"))
			first = clean_str(record.get("first"))
			last = clean_str(record.get("last"))
			company = clean_str(record.get("company"))

			if not accountno:
				stats["skipped"] += 1
				continue

			# Build customer name
			if first or last:
				customer_name = f"{first} {last}".strip()
			elif company:
				customer_name = company
			else:
				customer_name = f"Customer {accountno}"

			if frappe.db.exists("Customer", {"customer_name": customer_name}):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			doc = frappe.new_doc("Customer")
			doc.customer_name = customer_name
			doc.customer_type = "Individual"
			doc.customer_group = "Individual"
			doc.territory = "All Territories"

			# Custom fields if they exist
			if frappe.get_meta("Customer").has_field("custom_legacy_account_no"):
				doc.custom_legacy_account_no = accountno
			if frappe.get_meta("Customer").has_field("custom_company"):
				doc.custom_company = company

			doc.insert(ignore_permissions=True, ignore_mandatory=True)

			# Create linked address
			address = clean_str(record.get("address"))
			city = clean_str(record.get("city"))
			state = clean_str(record.get("state"))
			zipcode = clean_str(record.get("zip"))
			phone = clean_str(record.get("phone"))

			if any([address, city, state]):
				addr = frappe.new_doc("Address")
				addr.address_title = customer_name
				addr.address_type = "Billing"
				addr.address_line1 = address
				addr.city = city
				addr.state = state
				addr.pincode = zipcode
				addr.phone = phone
				addr.append("links", {"link_doctype": "Customer", "link_name": doc.name})
				addr.insert(ignore_permissions=True, ignore_mandatory=True)

			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Customer {record.get('accountno', '?')}: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()
	return stats


# ──────────────────────────────────────────────────
# Item (from inventor.DBF)
# ──────────────────────────────────────────────────


def import_inventory(backup_path: str, dry_run: bool = False) -> Dict:
	"""Import inventory items from inventor.DBF."""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	dbf_path = find_dbf(backup_path, "inventor.DBF")
	if not dbf_path:
		stats["errors"].append("inventor.DBF not found")
		return stats

	records = read_dbf(dbf_path)
	stats["total"] = len(records)

	for record in records:
		try:
			barcode = clean_str(record.get("barcode"))
			stockno = clean_str(record.get("stockno"))
			descript = clean_str(record.get("dscript"))

			if not barcode and not stockno:
				stats["skipped"] += 1
				continue

			# Use barcode as item_code
			item_code = barcode or stockno
			item_name = descript or item_code

			if frappe.db.exists("Item", item_code):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			doc = frappe.new_doc("Item")
			doc.item_code = item_code
			doc.item_name = item_name
			doc.description = descript or item_name
			doc.stock_uom = "Nos"
			doc.is_stock_item = 1

			# Map category to item_group
			category = clean_str(record.get("category"))
			if category:
				doc.item_group = _get_or_create_item_group(category)

			# Map manufacturer/brand
			mfrid = clean_str(record.get("mfrid"))
			if mfrid:
				doc.brand = _get_or_create_brand(mfrid)

			# Pricing
			cost = clean_float(record.get("cost"))
			asklow = clean_float(record.get("asklow"))
			askhigh = clean_float(record.get("askhigh"))
			if asklow > 0:
				doc.standard_rate = asklow
			elif askhigh > 0:
				doc.standard_rate = askhigh
			if cost > 0:
				doc.valuation_rate = cost

			# Custom fields (if they exist)
			_set_custom_field(doc, "custom_barcode", barcode)
			_set_custom_field(doc, "custom_stock_no", stockno)
			_set_custom_field(doc, "custom_style", clean_str(record.get("style")))
			_set_custom_field(doc, "custom_tag_type", clean_str(record.get("tagtype")))
			_set_custom_field(doc, "custom_abr", clean_str(record.get("abr")))
			_set_custom_field(doc, "custom_store_code", clean_str(record.get("storecode")))

			# Weight
			goldwght = clean_float(record.get("goldwght"))
			if goldwght > 0:
				_set_custom_field(doc, "custom_gold_weight", goldwght)

			# Dates
			datebuy = format_date(record.get("datebuy"))
			if datebuy:
				_set_custom_field(doc, "custom_date_purchased", datebuy)

			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Item {record.get('barcode', '?')}: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()
	return stats


# ──────────────────────────────────────────────────
# Supplier (from supplier.dbf)
# ──────────────────────────────────────────────────


def import_suppliers(backup_path: str, dry_run: bool = False) -> Dict:
	"""Import suppliers/vendors from supplier.dbf."""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	dbf_path = find_dbf(backup_path, "supplier.dbf")
	if not dbf_path:
		stats["errors"].append("supplier.dbf not found")
		return stats

	records = read_dbf(dbf_path)
	stats["total"] = len(records)

	for record in records:
		try:
			abbrev = clean_str(record.get("abbrev"))
			fullname = clean_str(record.get("fullname"))
			if not abbrev and not fullname:
				stats["skipped"] += 1
				continue

			supplier_name = fullname or abbrev
			if frappe.db.exists("Supplier", {"supplier_name": supplier_name}):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			doc = frappe.new_doc("Supplier")
			doc.supplier_name = supplier_name
			doc.supplier_group = "All Supplier Groups"
			doc.supplier_type = "Company"

			contact = clean_str(record.get("contact"))
			if contact:
				doc.contact_person = contact

			doc.insert(ignore_permissions=True, ignore_mandatory=True)

			# Create address
			address = clean_str(record.get("address"))
			city = clean_str(record.get("city"))
			state = clean_str(record.get("state"))
			phone = clean_str(record.get("phone"))
			email = clean_str(record.get("email"))

			if any([address, city, state]):
				addr = frappe.new_doc("Address")
				addr.address_title = supplier_name
				addr.address_type = "Billing"
				addr.address_line1 = address
				addr.city = city
				addr.state = state
				addr.pincode = clean_str(record.get("zip"))
				addr.phone = phone
				addr.email_id = email
				addr.append("links", {"link_doctype": "Supplier", "link_name": doc.name})
				addr.insert(ignore_permissions=True, ignore_mandatory=True)

			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Supplier {record.get('abbrev', '?')}: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()
	return stats


# ──────────────────────────────────────────────────
# Item Group / Category (from cat.dbf)
# ──────────────────────────────────────────────────


def import_categories(backup_path: str, dry_run: bool = False) -> Dict:
	"""Import categories from cat.dbf as Item Groups."""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	dbf_path = find_dbf(backup_path, "cat.dbf")
	if not dbf_path:
		stats["errors"].append("cat.dbf not found")
		return stats

	records = read_dbf(dbf_path)
	stats["total"] = len(records)

	for record in records:
		try:
			fullname = clean_str(record.get("fullname"))
			if not fullname:
				stats["skipped"] += 1
				continue

			if frappe.db.exists("Item Group", fullname):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			doc = frappe.new_doc("Item Group")
			doc.item_group_name = fullname
			doc.parent_item_group = "All Item Groups"
			doc.is_group = 0
			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Category {record.get('fullname', '?')}: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()
	return stats


# ──────────────────────────────────────────────────
# Zevar Purity (from KARAT.DBF)
# ──────────────────────────────────────────────────


def import_purities(backup_path: str, dry_run: bool = False) -> Dict:
	"""Import karat/purity records from KARAT.DBF into Zevar Purity."""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	dbf_path = find_dbf(backup_path, "KARAT.DBF")
	if not dbf_path:
		stats["errors"].append("KARAT.DBF not found")
		return stats

	records = read_dbf(dbf_path)
	stats["total"] = len(records)

	for record in records:
		try:
			karat = clean_str(record.get("karat"))
			if not karat:
				stats["skipped"] += 1
				continue

			if frappe.db.exists("Zevar Purity", karat):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			doc = frappe.new_doc("Zevar Purity")
			doc.name = karat
			doc.purity_name = karat
			code = clean_float(record.get("code"))
			if code > 0:
				doc.fine_metal_content = code
			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Purity {record.get('karat', '?')}: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()
	return stats


# ──────────────────────────────────────────────────
# Item Attributes: Color & Clarity (from COLOR.DBF / CLARITY.DBF)
# ──────────────────────────────────────────────────


def import_item_attributes(backup_path: str, dry_run: bool = False) -> Dict:
	"""Import Color and Clarity as Item Attributes."""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	for dbf_name, attr_name, field_name in [
		("COLOR.DBF", "Color", "colour"),
		("CLARITY.DBF", "Clarity", "clarity"),
	]:
		dbf_path = find_dbf(backup_path, dbf_name)
		if not dbf_path:
			stats["errors"].append(f"{dbf_name} not found")
			continue

		records = read_dbf(dbf_path)
		stats["total"] += len(records)

		# Ensure attribute exists
		if not dry_run and not frappe.db.exists("Item Attribute", attr_name):
			attr_doc = frappe.new_doc("Item Attribute")
			attr_doc.attribute_name = attr_name
			attr_doc.numeric_values = 0
			attr_doc.insert(ignore_permissions=True)

		# Track existing values for this attribute
		existing_values = set()
		if not dry_run and frappe.db.exists("Item Attribute", attr_name):
			attr_doc = frappe.get_doc("Item Attribute", attr_name)
			for av in attr_doc.item_attribute_values:
				existing_values.add(av.attribute_value)

		abbr_counter = len(existing_values)
		for record in records:
			try:
				value = clean_str(record.get(field_name))
				if not value or value in existing_values:
					stats["skipped"] += 1
					continue

				if dry_run:
					stats["imported"] += 1
					continue

				# Generate unique abbreviation
				abbr_counter += 1
				abbr = f"{attr_name[:2].upper()}{abbr_counter:02d}"

				# Add value to attribute
				attr_doc = frappe.get_doc("Item Attribute", attr_name)
				attr_doc.append(
					"item_attribute_values",
					{
						"attribute_value": value,
						"abbr": abbr,
					},
				)
				attr_doc.save(ignore_permissions=True)
				existing_values.add(value)
				stats["imported"] += 1

			except Exception as e:
				stats["errors"].append(f"{attr_name} {record.get(field_name, '?')}: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()
	return stats


# ──────────────────────────────────────────────────
# Gold Rate Log (from GOLD$.dbf)
# ──────────────────────────────────────────────────


def import_gold_rates(backup_path: str, dry_run: bool = False) -> Dict:
	"""Import gold price records from GOLD$.dbf."""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	dbf_path = find_dbf(backup_path, "GOLD$.dbf")
	if not dbf_path:
		stats["errors"].append("GOLD$.dbf not found")
		return stats

	records = read_dbf(dbf_path)
	stats["total"] = len(records)

	for record in records:
		try:
			cash = clean_float(record.get("cash"))
			if cash <= 0:
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			doc = frappe.new_doc("Gold Rate Log")
			doc.gold_price = cash
			doc.currency = "USD"
			doc.source = "Legacy Import"
			doc.fetch_time = frappe.utils.now_datetime()
			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Gold rate: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()
	return stats


# ──────────────────────────────────────────────────
# Repair Types (from saletype.dbf)
# ──────────────────────────────────────────────────


def import_repair_types(backup_path: str, dry_run: bool = False) -> Dict:
	"""Import repair type records from saletype.dbf into Repair Type."""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	dbf_path = find_dbf(backup_path, "saletype.dbf")
	if not dbf_path:
		stats["errors"].append("saletype.dbf not found")
		return stats

	records = read_dbf(dbf_path)
	stats["total"] = len(records)

	# Map legacy filters/types to valid Repair Type categories
	CATEGORY_MAP = {
		"RING": "Ring",
		"NECKLACE": "Necklace",
		"BRACELET": "Bracelet",
		"EARRING": "Earring",
		"WATCH": "Watch",
		"CHAIN": "Chain",
		"PENDANT": "Pendant",
	}

	for record in records:
		try:
			type_name = clean_str(record.get("type"))
			if not type_name:
				stats["skipped"] += 1
				continue

			if frappe.db.exists("Repair Type", type_name):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			doc = frappe.new_doc("Repair Type")
			doc.repair_name = type_name
			doc.description = clean_str(record.get("codes"))
			doc.is_active = 1

			# Map category from filter or type name
			filter_val = clean_str(record.get("filter")).upper()
			type_upper = type_name.upper()

			category = "Other"
			for keyword, cat in CATEGORY_MAP.items():
				if keyword in filter_val or keyword in type_upper:
					category = cat
					break
			doc.category = category

			base_price = clean_float(record.get("price"))
			if base_price > 0:
				doc.base_price = base_price

			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Repair Type {record.get('type', '?')}: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()
	return stats


# ──────────────────────────────────────────────────
# Sales Invoice (from trans.dbf)
# ──────────────────────────────────────────────────


def import_transactions(backup_path: str, dry_run: bool = False) -> Dict:
	"""Import transaction records from trans.dbf as Sales Invoices."""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	dbf_path = find_dbf(backup_path, "trans.dbf")
	if not dbf_path:
		stats["errors"].append("trans.dbf not found")
		return stats

	records = read_dbf(dbf_path)
	stats["total"] = len(records)

	# Pre-fetch customer name mapping to avoid per-record DB lookups
	customer_cache = {}
	for c in frappe.get_all("Customer", fields=["name", "customer_name"]):
		customer_cache[c.customer_name] = c.name
	default_customer = _get_default_customer()

	# Check if legacy trans field exists
	has_custom_store = frappe.get_meta("Sales Invoice").has_field("custom_store")
	has_legacy_trans = frappe.get_meta("Sales Invoice").has_field("custom_legacy_trans_no")

	for idx, record in enumerate(records):
		try:
			transno = clean_str(record.get("transno"))
			if not transno:
				stats["skipped"] += 1
				continue

			# Skip voided transactions
			if clean_str(record.get("voided")) == "Y":
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			doc = frappe.new_doc("Sales Invoice")
			doc.title = f"Legacy Trans #{transno}"
			doc.posting_date = format_date(record.get("date")) or frappe.utils.today()
			doc.update_stock = 0

			# Map customer from cache
			firstname = clean_str(record.get("firstname"))
			lastname = clean_str(record.get("lastname"))
			if firstname or lastname:
				customer_name = f"{firstname} {lastname}".strip()
				doc.customer = customer_cache.get(customer_name, default_customer)
			else:
				doc.customer = default_customer

			# Map company
			doc.company = frappe.defaults.get_global_default("company")

			# Store mapping
			storecode = clean_str(record.get("storecode"))
			if storecode and has_custom_store:
				sc = storecode.zfill(2)
				if frappe.db.exists("Store Location", sc):
					doc.custom_store = sc

			# Amount
			amount = clean_float(record.get("amount"))
			if amount > 0:
				doc.append(
					"items",
					{
						"item_code": _get_default_item(),
						"item_name": clean_str(record.get("dscript")) or "Legacy Sale",
						"qty": 1,
						"rate": amount,
					},
				)

			# Remark about legacy reference
			if has_legacy_trans:
				doc.custom_legacy_trans_no = transno

			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

			# Batch commit every 50 records
			if (idx + 1) % 50 == 0:
				frappe.db.commit()

		except Exception as e:
			stats["errors"].append(f"Trans {record.get('transno', '?')}: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()
	return stats


# ──────────────────────────────────────────────────
# Jewelry Appraisal (from 1APTERM1.DBF)
# ──────────────────────────────────────────────────


def import_appraisals(backup_path: str, dry_run: bool = False) -> Dict:
	"""Import jewelry appraisals from 1APTERM1.DBF."""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	dbf_path = find_dbf(backup_path, "1APTERM1.DBF")
	if not dbf_path:
		stats["errors"].append("1APTERM1.DBF not found")
		return stats

	records = read_dbf(dbf_path)
	stats["total"] = len(records)

	if not records:
		return stats

	for i, record in enumerate(records):
		try:
			stockno = clean_str(record.get("stockno"))
			firstname = clean_str(record.get("firstname"))
			lastname = clean_str(record.get("lastname"))
			descript = clean_str(record.get("dscript"))

			if not stockno and not descript:
				stats["skipped"] += 1
				continue

			appraisal_name = f"APP-{stockno or i + 1:04d}"

			if frappe.db.exists("Jewelry Appraisal", appraisal_name):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			doc = frappe.new_doc("Jewelry Appraisal")

			# Customer
			if firstname or lastname:
				customer_name = f"{firstname} {lastname}".strip()
				if frappe.db.exists("Customer", {"customer_name": customer_name}):
					doc.customer = frappe.db.get_value("Customer", {"customer_name": customer_name}, "name")

			doc.description = descript
			doc.stock_number = stockno
			doc.metal_type = clean_str(record.get("metal_type"))
			doc.karat = clean_str(record.get("karat_type"))
			doc.estimated_value = clean_float(record.get("estvalue"))
			doc.purchase_price = clean_float(record.get("purchase"))
			doc.total_weight = clean_float(record.get("weight"))
			doc.center_stone_weight = clean_float(record.get("centerwgt"))
			doc.center_stone_cut = clean_str(record.get("centercut"))
			doc.center_stone_type = clean_str(record.get("centertype"))
			doc.center_stone_clarity = clean_str(record.get("centerclar"))
			doc.center_stone_color = clean_str(record.get("centercol"))
			doc.side_stones_weight = clean_float(record.get("side_wgt"))
			doc.side_stones_quantity = clean_int(record.get("side_qty"))

			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Appraisal {i}: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()
	return stats


# ──────────────────────────────────────────────────
# Helper functions for creating/linking records
# ──────────────────────────────────────────────────


def _get_or_create_item_group(category: str) -> str:
	"""Get or create an Item Group by name."""
	if frappe.db.exists("Item Group", category):
		return category
	try:
		doc = frappe.new_doc("Item Group")
		doc.item_group_name = category
		doc.parent_item_group = "All Item Groups"
		doc.is_group = 0
		doc.insert(ignore_permissions=True)
	except frappe.DuplicateEntryError:
		pass
	return category


def _get_or_create_brand(mfrid: str) -> str:
	"""Get or create a Brand by manufacturer ID."""
	if frappe.db.exists("Brand", mfrid):
		return mfrid
	try:
		doc = frappe.new_doc("Brand")
		doc.brand = mfrid
		doc.insert(ignore_permissions=True)
	except frappe.DuplicateEntryError:
		pass
	return mfrid


def _set_custom_field(doc, fieldname: str, value):
	"""Set a custom field on a document if the field exists and value is non-empty."""
	if value and frappe.get_meta(doc.doctype).has_field(fieldname):
		doc.set(fieldname, value)


def _get_default_customer() -> str:
	"""Get or create a default 'Walk-in Customer'."""
	name = "Walk-in Customer"
	if frappe.db.exists("Customer", name):
		return name
	doc = frappe.new_doc("Customer")
	doc.customer_name = name
	doc.customer_type = "Individual"
	doc.customer_group = "Individual"
	doc.territory = "All Territories"
	doc.insert(ignore_permissions=True)
	return name


def _get_default_item() -> str:
	"""Get or create a default item for legacy transaction lines."""
	item_code = "LEGACY-ITEM"
	if frappe.db.exists("Item", item_code):
		return item_code
	doc = frappe.new_doc("Item")
	doc.item_code = item_code
	doc.item_name = "Legacy Sale Item"
	doc.item_group = "All Item Groups"
	doc.stock_uom = "Nos"
	doc.is_stock_item = 0
	doc.insert(ignore_permissions=True)
	return item_code


# ──────────────────────────────────────────────────
# Root node provisioning
# ──────────────────────────────────────────────────

ROOT_NODES = [
	("Item Group", "All Item Groups", True),
	("Territory", "All Territories", True),
	("Customer Group", "All Customer Groups", True),
	("Supplier Group", "All Supplier Groups", True),
	("UOM", "Nos", False),
	("Warehouse", "All Warehouses", True),
]


def ensure_root_nodes():
	"""Create required root/master nodes if they don't exist."""
	for doctype, name, is_group in ROOT_NODES:
		if not frappe.db.exists(doctype, name):
			try:
				doc = frappe.new_doc(doctype)
				if doctype == "Item Group":
					doc.item_group_name = name
				elif doctype == "Territory":
					doc.territory_name = name
				elif doctype == "Customer Group":
					doc.customer_group_name = name
				elif doctype == "Supplier Group":
					doc.supplier_group_name = name
				elif doctype == "UOM":
					doc.uom_name = name
				elif doctype == "Warehouse":
					doc.warehouse_name = name
					doc.company = frappe.defaults.get_global_default("company") or name
				doc.is_group = is_group
				doc.insert(ignore_permissions=True)
			except frappe.DuplicateEntryError:
				pass


# ──────────────────────────────────────────────────
# Main orchestrator
# ──────────────────────────────────────────────────


def import_all(backup_path: str, dry_run: bool = False, skip_transactions: bool = False) -> Dict:
	"""
	Import all legacy data from the backup directory.

	Runs in dependency order:
	1. Stores (master data)
	2. Employees (master data)
	3. Categories / Item Groups (master data)
	4. Purity / Item Attributes (reference data)
	5. Suppliers (master data)
	6. Customers (master data)
	7. Inventory / Items (depends on categories, brands)
	8. Repair Types
	9. Gold Rates
	10. Transactions (depends on customers, items) -- skippable
	11. Appraisals (depends on customers)
	"""
	if not os.path.isdir(backup_path):
		frappe.throw(_("Backup path does not exist: {0}").format(backup_path))

	# Ensure required root nodes exist
	if not dry_run:
		ensure_root_nodes()

	results = {
		"dry_run": dry_run,
		"backup_path": backup_path,
		"stores": import_stores(backup_path, dry_run),
		"employees": import_employees(backup_path, dry_run),
		"categories": import_categories(backup_path, dry_run),
		"item_attributes": import_item_attributes(backup_path, dry_run),
		"purities": import_purities(backup_path, dry_run),
		"suppliers": import_suppliers(backup_path, dry_run),
		"customers": import_customers(backup_path, dry_run),
		"inventory": import_inventory(backup_path, dry_run),
		"repair_types": import_repair_types(backup_path, dry_run),
		"gold_rates": import_gold_rates(backup_path, dry_run),
		"transactions": import_transactions(backup_path, dry_run)
		if not skip_transactions
		else {"total": 0, "imported": 0, "skipped": 0, "errors": ["Skipped (--skip-transactions)"]},
		"appraisals": import_appraisals(backup_path, dry_run),
	}

	# Calculate totals
	results["total_records"] = sum(r.get("total", 0) for r in results.values() if isinstance(r, dict))
	results["total_imported"] = sum(r.get("imported", 0) for r in results.values() if isinstance(r, dict))
	results["total_skipped"] = sum(r.get("skipped", 0) for r in results.values() if isinstance(r, dict))
	results["total_errors"] = sum(len(r.get("errors", [])) for r in results.values() if isinstance(r, dict))

	return results


def get_mapping_info() -> Dict:
	"""Return field mapping information for all migration categories."""
	return {
		"stores": {
			"file": "LOCNAME.dbf",
			"doctype": "Store Location",
			"fields": {"LOC": "store_code", "LOCNAME": "store_name"},
		},
		"employees": {
			"file": "EMPLOYEE.DBF",
			"doctype": "Employee",
			"fields": {
				"EMPID": "employee_number",
				"CLERKNAME": "employee_name",
				"DATEHIRE": "date_of_joining",
				"POSITION": "designation",
			},
		},
		"categories": {
			"file": "cat.dbf",
			"doctype": "Item Group",
			"fields": {"FULLNAME": "item_group_name"},
		},
		"purities": {
			"file": "KARAT.DBF",
			"doctype": "Zevar Purity",
			"fields": {"KARAT": "name", "CODE": "fine_metal_content"},
		},
		"item_attributes": {
			"file": "COLOR.DBF / CLARITY.DBF",
			"doctype": "Item Attribute",
			"fields": {
				"COLOUR (COLOR.DBF)": "attribute_value",
				"CLARITY (CLARITY.DBF)": "attribute_value",
			},
		},
		"suppliers": {
			"file": "supplier.dbf",
			"doctype": "Supplier",
			"fields": {
				"ABBREV": "supplier_name (fallback)",
				"FULLNAME": "supplier_name",
				"PHONE": "phone",
				"EMAIL": "email_id",
			},
		},
		"customers": {
			"file": "CUSTSHOR.dbf",
			"doctype": "Customer",
			"fields": {
				"ACCOUNTNO": "custom_legacy_account_no",
				"FIRST": "first_name",
				"LAST": "last_name",
				"ADDRESS": "address_line1",
				"CITY": "city",
				"STATE": "state",
				"ZIP": "pincode",
				"PHONE": "phone",
			},
		},
		"inventory": {
			"file": "inventor.DBF",
			"doctype": "Item",
			"fields": {
				"BARCODE": "item_code",
				"DESCRIPT": "item_name",
				"CATEGORY": "item_group",
				"MFRID": "brand",
				"COST": "valuation_rate",
				"ASKLOW": "standard_rate",
				"GOLDWGHT": "custom_gold_weight",
			},
		},
		"repair_types": {
			"file": "saletype.dbf",
			"doctype": "Repair Type",
			"fields": {"TYPE": "repair_name", "PRICE": "base_price"},
		},
		"gold_rates": {
			"file": "GOLD$.dbf",
			"doctype": "Gold Rate Log",
			"fields": {"CASH": "gold_price", "MEMOS": "notes"},
		},
		"transactions": {
			"file": "trans.dbf",
			"doctype": "Sales Invoice",
			"fields": {
				"TRANSNO": "custom_legacy_trans_no",
				"DATE": "posting_date",
				"AMOUNT": "amount",
				"ACCOUNTNO": "customer link",
			},
		},
		"appraisals": {
			"file": "1APTERM1.DBF",
			"doctype": "Jewelry Appraisal",
			"fields": {
				"STOCKNO": "stock_number",
				"DESCRIPT": "description",
				"ESTVALUE": "estimated_value",
				"METAL_TYPE": "metal_type",
				"KARAT_TYPE": "karat",
			},
		},
	}
