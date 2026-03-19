"""
FoxPro to Frappe Data Migration

Parses Visual FoxPro DBF files and imports data into Zevar DocTypes.

Legacy File Mapping:
- 1APTERM1.DBF → Jewelry Appraisal
- Inventry.bup → Item (inventory)
- Employee.bup → Employee
- Guest.bup → Customer
- showinfo.DBF → Store Location
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

import frappe
from frappe import _

try:
	from dbfread import DBF
	HAS_DBFREAD = True
except ImportError:
	HAS_DBFREAD = False


# Field Mappings: Legacy Field → Zevar Field
APPRAISAL_MAPPING = {
	"TRANSID": "name",
	"LASTNAME": "customer_last_name",
	"FIRSTNAME": "customer_first_name",
	"ACCOUNTNO": "customer_account",
	"DESCRIPT": "description",
	"DESC1": "description_line_1",
	"DESC2": "description_line_2",
	"STOCKNO": "stock_number",
	"ABR": "abbreviation",
	"ESTVALUE": "estimated_value",
	"PURCHASE": "purchase_price",
	"METAL_TYPE": "metal_type",
	"KARAT_TYPE": "karat",
	"STONES": "stones_description",
	"WEIGHT": "total_weight",
	"CENTERWGT": "center_stone_weight",
	"CENTERCUT": "center_stone_cut",
	"CENTERTYPE": "center_stone_type",
	"CENTERCLAR": "center_stone_clarity",
	"CENTERCOL": "center_stone_color",
	"SIDE_WGT": "side_stones_weight",
	"SIDE_QTY": "side_stones_quantity",
	"SIDE_OPT": "side_stones_options",
}

INVENTORY_MAPPING = {
	"STOCKNO": "item_code",
	"DESCRIPT": "item_name",
	"DESC1": "description",
	"METAL": "custom_metal_type",
	"KARAT": "custom_karat",
	"WEIGHT": "custom_weight",
	"PRICE": "standard_rate",
	"COST": "valuation_rate",
	"QTY": "stock_qty",
}

EMPLOYEE_MAPPING = {
	"EMPID": "employee_number",
	"NAME": "employee_name",
	"FNAME": "first_name",
	"LNAME": "last_name",
	"ADDR1": "permanent_address",
	"CITY": "city",
	"STATE": "state",
	"ZIP": "pincode",
	"PHONE": "cell_number",
	"HIREDATE": "date_of_joining",
}

CUSTOMER_MAPPING = {
	"ACCOUNTNO": "name",
	"NAME": "customer_name",
	"ADDR1": "address_line1",
	"ADDR2": "address_line2",
	"CITY": "city",
	"STATE": "state",
	"ZIP": "pincode",
	"PHONE": "phone",
	"EMAIL": "email_id",
}

STORE_MAPPING = {
	"STORECODE": "store_code",
	"STORENAME": "store_name",
	"ADDR1": "address_line1",
	"CITY": "city",
	"STATE": "state",
	"ZIP": "pincode",
	"PHONE": "phone",
}


def check_dbfread():
	"""Check if dbfread is available."""
	if not HAS_DBFREAD:
		frappe.throw(
			_("dbfread library not installed. Run: pip install dbfread"),
			title=_("Missing Dependency")
		)


def read_dbf(file_path: str, encoding: str = "cp1252") -> List[Dict]:
	"""
	Read a DBF file and return list of records.

	Args:
		file_path: Path to .DBF file
		encoding: Character encoding (default: Windows-1252)

	Returns:
		List of dictionaries with field names as keys
	"""
	check_dbfread()

	if not os.path.exists(file_path):
		frappe.throw(_("File not found: {0}").format(file_path))

	try:
		table = DBF(file_path, encoding=encoding, ignore_missing_memofile=True)
		records = []
		for record in table:
			# Convert bytes to strings and handle None values
			clean_record = {}
			for key, value in record.items():
				if isinstance(value, bytes):
					try:
						value = value.decode(encoding).strip()
					except:
						value = str(value)
				if value is not None and value != "":
					clean_record[key.lower()] = value
			records.append(clean_record)
		return records
	except Exception as e:
		frappe.log_error(f"Failed to read DBF {file_path}: {e}", "Migration Error")
		raise


def read_bup_file(file_path: str, encoding: str = "cp1252") -> List[Dict]:
	"""
	Read a .bup file (backup) - these are often DBF files with different extension.

	Args:
		file_path: Path to .bup file
		encoding: Character encoding

	Returns:
		List of dictionaries
	"""
	# .bup files are typically DBF files with a different extension
	# Try reading as DBF first
	try:
		return read_dbf(file_path, encoding)
	except:
		pass

	# Fallback: try reading as text/CSV
	records = []
	try:
		with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
			lines = f.readlines()
			# Parse based on format - this may need adjustment based on actual format
			for line in lines:
				if line.strip():
					records.append({"raw": line.strip()})
	except Exception as e:
		frappe.log_error(f"Failed to read BUP {file_path}: {e}", "Migration Error")

	return records


def map_record(record: Dict, mapping: Dict) -> Dict:
	"""
	Map legacy record fields to Zevar fields.

	Args:
		record: Legacy record dictionary (lowercase keys)
		mapping: Field mapping dict (uppercase legacy → lowercase zevar)

	Returns:
		Dictionary with Zevar field names
	"""
	mapped = {}
	for legacy_field, zevar_field in mapping.items():
		value = record.get(legacy_field.lower())
		if value is not None:
			# Handle date fields
			if isinstance(value, str) and "date" in zevar_field.lower():
				try:
					value = parse_legacy_date(value)
				except:
					pass
			# Handle numeric fields
			if zevar_field in ["estimated_value", "purchase_price", "standard_rate",
							   "valuation_rate", "total_weight", "center_stone_weight"]:
				try:
					value = float(value) if value else 0
				except:
					value = 0
			mapped[zevar_field] = value
	return mapped


def parse_legacy_date(value: str) -> Optional[str]:
	"""Parse legacy date format to YYYY-MM-DD."""
	if not value:
		return None

	# Common FoxPro date formats
	formats = ["%Y%m%d", "%m/%d/%Y", "%m-%d-%Y", "%Y-%m-%d"]

	for fmt in formats:
		try:
			dt = datetime.strptime(str(value).strip(), fmt)
			return dt.strftime("%Y-%m-%d")
		except ValueError:
			continue

	return None


def import_appraisals(backup_path: str, dry_run: bool = False) -> Dict:
	"""
	Import jewelry appraisals from 1APTERM1.DBF.

	Args:
		backup_path: Path to backup directory
		dry_run: If True, don't create records, just return stats

	Returns:
		Dictionary with import statistics
	"""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	# Find appraisal file
	appraisal_file = None
	for fname in os.listdir(backup_path):
		if fname.upper().startswith("1APTERM") and fname.upper().endswith(".DBF"):
			appraisal_file = os.path.join(backup_path, fname)
			break

	if not appraisal_file:
		stats["errors"].append("Appraisal file (1APTERM1.DBF) not found")
		return stats

	records = read_dbf(appraisal_file)
	stats["total"] = len(records)

	for record in records:
		try:
			mapped = map_record(record, APPRAISAL_MAPPING)

			if not mapped.get("name") and not mapped.get("stock_number"):
				stats["skipped"] += 1
				continue

			# Generate name if not present
			if not mapped.get("name"):
				mapped["name"] = f"APP-{mapped.get('stock_number', stats['imported'])}"

			# Check if exists
			if frappe.db.exists("Jewelry Appraisal", mapped["name"]):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			# Create appraisal
			doc = frappe.new_doc("Jewelry Appraisal")
			doc.update(mapped)
			doc.docstatus = 0
			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Error importing record: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()

	return stats


def import_inventory(backup_path: str, dry_run: bool = False) -> Dict:
	"""
	Import inventory items from Inventry.bup.

	Args:
		backup_path: Path to backup directory
		dry_run: If True, don't create records

	Returns:
		Dictionary with import statistics
	"""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	# Find inventory file
	inventory_file = None
	for fname in os.listdir(backup_path):
		if fname.upper().startswith("INVENT") and (
			fname.upper().endswith(".BUP") or fname.upper().endswith(".DBF")
		):
			inventory_file = os.path.join(backup_path, fname)
			break

	if not inventory_file:
		stats["errors"].append("Inventory file (Inventry.bup) not found")
		return stats

	# Try reading as DBF first
	try:
		records = read_dbf(inventory_file)
	except:
		records = read_bup_file(inventory_file)

	stats["total"] = len(records)

	for record in records:
		try:
			mapped = map_record(record, INVENTORY_MAPPING)

			if not mapped.get("item_code"):
				stats["skipped"] += 1
				continue

			# Check if exists
			if frappe.db.exists("Item", mapped["item_code"]):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			# Create item
			doc = frappe.new_doc("Item")
			doc.item_code = mapped.get("item_code")
			doc.item_name = mapped.get("item_name", doc.item_code)
			doc.description = mapped.get("description", doc.item_name)
			doc.item_group = "Products"  # Default group
			doc.stock_uom = "Nos"
			doc.is_stock_item = 1
			doc.docstatus = 0

			# Set custom fields
			for field in ["custom_metal_type", "custom_karat", "custom_weight"]:
				if mapped.get(field):
					setattr(doc, field, mapped[field])

			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Error importing item: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()

	return stats


def import_employees(backup_path: str, dry_run: bool = False) -> Dict:
	"""
	Import employees from Employee.bup.

	Args:
		backup_path: Path to backup directory
		dry_run: If True, don't create records

	Returns:
		Dictionary with import statistics
	"""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	# Find employee file
	employee_file = None
	for fname in os.listdir(backup_path):
		if fname.upper().startswith("EMPLOY") and (
			fname.upper().endswith(".BUP") or fname.upper().endswith(".DBF")
		):
			employee_file = os.path.join(backup_path, fname)
			break

	if not employee_file:
		stats["errors"].append("Employee file (Employee.bup) not found")
		return stats

	try:
		records = read_dbf(employee_file)
	except:
		records = read_bup_file(employee_file)

	stats["total"] = len(records)

	for record in records:
		try:
			mapped = map_record(record, EMPLOYEE_MAPPING)

			if not mapped.get("employee_name") and not mapped.get("employee_number"):
				stats["skipped"] += 1
				continue

			# Generate employee number if not present
			if not mapped.get("employee_number"):
				mapped["employee_number"] = f"EMP-{stats['imported'] + 1:04d}"

			# Check if exists
			if frappe.db.exists("Employee", {"employee_number": mapped["employee_number"]}):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			# Create employee
			doc = frappe.new_doc("Employee")
			doc.update(mapped)
			doc.status = "Active"
			doc.employment_type = "Full-time"
			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Error importing employee: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()

	return stats


def import_customers(backup_path: str, dry_run: bool = False) -> Dict:
	"""
	Import customers from Guest.bup.

	Args:
		backup_path: Path to backup directory
		dry_run: If True, don't create records

	Returns:
		Dictionary with import statistics
	"""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	# Find customer file
	customer_file = None
	for fname in os.listdir(backup_path):
		if fname.upper().startswith("GUEST") and (
			fname.upper().endswith(".BUP") or fname.upper().endswith(".DBF")
		):
			customer_file = os.path.join(backup_path, fname)
			break

	if not customer_file:
		stats["errors"].append("Customer file (Guest.bup) not found")
		return stats

	try:
		records = read_dbf(customer_file)
	except:
		records = read_bup_file(customer_file)

	stats["total"] = len(records)

	for record in records:
		try:
			mapped = map_record(record, CUSTOMER_MAPPING)

			if not mapped.get("customer_name"):
				stats["skipped"] += 1
				continue

			# Generate customer ID if not present
			customer_id = mapped.get("name") or f"CUST-{stats['imported'] + 1:04d}"

			# Check if exists
			if frappe.db.exists("Customer", customer_id):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			# Create customer
			doc = frappe.new_doc("Customer")
			doc.name = customer_id
			doc.customer_name = mapped.get("customer_name")
			doc.customer_type = "Individual"
			doc.customer_group = "Individual"
			doc.territory = "United States"

			# Create address
			if any(mapped.get(f) for f in ["address_line1", "city", "state"]):
				addr = frappe.new_doc("Address")
				addr.address_title = doc.customer_name
				addr.address_type = "Billing"
				for field in ["address_line1", "address_line2", "city", "state", "pincode", "phone", "email_id"]:
					if mapped.get(field):
						setattr(addr, field, mapped[field])
				addr.append("links", {"link_doctype": "Customer", "link_name": customer_id})
				addr.insert(ignore_permissions=True, ignore_mandatory=True)

			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Error importing customer: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()

	return stats


def import_stores(backup_path: str, dry_run: bool = False) -> Dict:
	"""
	Import store locations from showinfo.DBF.

	Args:
		backup_path: Path to backup directory
		dry_run: If True, don't create records

	Returns:
		Dictionary with import statistics
	"""
	stats = {"total": 0, "imported": 0, "skipped": 0, "errors": []}

	# Find store file
	store_file = None
	for fname in os.listdir(backup_path):
		if fname.upper().startswith("SHOW") and fname.upper().endswith(".DBF"):
			store_file = os.path.join(backup_path, fname)
			break

	if not store_file:
		stats["errors"].append("Store file (showinfo.DBF) not found")
		return stats

	records = read_dbf(store_file)
	stats["total"] = len(records)

	# Group by store code
	stores_seen = set()

	for record in records:
		try:
			mapped = map_record(record, STORE_MAPPING)

			if not mapped.get("store_code"):
				stats["skipped"] += 1
				continue

			# Skip duplicates
			if mapped["store_code"] in stores_seen:
				stats["skipped"] += 1
				continue
			stores_seen.add(mapped["store_code"])

			# Check if exists
			if frappe.db.exists("Store Location", {"store_code": mapped["store_code"]}):
				stats["skipped"] += 1
				continue

			if dry_run:
				stats["imported"] += 1
				continue

			# Create store
			doc = frappe.new_doc("Store Location")
			doc.store_code = mapped["store_code"]
			doc.store_name = mapped.get("store_name", mapped["store_code"])
			for field in ["address_line1", "city", "state", "pincode", "phone"]:
				if mapped.get(field):
					setattr(doc, field, mapped[field])
			doc.is_active = 1
			doc.insert(ignore_permissions=True, ignore_mandatory=True)
			stats["imported"] += 1

		except Exception as e:
			stats["errors"].append(f"Error importing store: {str(e)[:100]}")

	if not dry_run:
		frappe.db.commit()

	return stats


def import_all(backup_path: str, dry_run: bool = False) -> Dict:
	"""
	Import all legacy data from backup directory.

	Args:
		backup_path: Path to backup directory
		dry_run: If True, don't create records

	Returns:
		Dictionary with all import statistics
	"""
	if not os.path.isdir(backup_path):
		frappe.throw(_("Backup path does not exist: {0}").format(backup_path))

	results = {
		"dry_run": dry_run,
		"backup_path": backup_path,
		"stores": import_stores(backup_path, dry_run),
		"employees": import_employees(backup_path, dry_run),
		"customers": import_customers(backup_path, dry_run),
		"inventory": import_inventory(backup_path, dry_run),
		"appraisals": import_appraisals(backup_path, dry_run),
	}

	# Calculate totals
	results["total_records"] = sum(
		r.get("total", 0) for r in results.values() if isinstance(r, dict)
	)
	results["total_imported"] = sum(
		r.get("imported", 0) for r in results.values() if isinstance(r, dict)
	)
	results["total_skipped"] = sum(
		r.get("skipped", 0) for r in results.values() if isinstance(r, dict)
	)
	results["total_errors"] = sum(
		len(r.get("errors", [])) for r in results.values() if isinstance(r, dict)
	)

	return results


def get_mapping_info() -> Dict:
	"""
	Get information about field mappings.

	Returns:
		Dictionary with mapping information for each DocType
	"""
	return {
		"appraisals": {
			"file": "1APTERM1.DBF",
			"doctype": "Jewelry Appraisal",
			"field_count": len(APPRAISAL_MAPPING),
			"fields": APPRAISAL_MAPPING,
		},
		"inventory": {
			"file": "Inventry.bup",
			"doctype": "Item",
			"field_count": len(INVENTORY_MAPPING),
			"fields": INVENTORY_MAPPING,
		},
		"employees": {
			"file": "Employee.bup",
			"doctype": "Employee",
			"field_count": len(EMPLOYEE_MAPPING),
			"fields": EMPLOYEE_MAPPING,
		},
		"customers": {
			"file": "Guest.bup",
			"doctype": "Customer",
			"field_count": len(CUSTOMER_MAPPING),
			"fields": CUSTOMER_MAPPING,
		},
		"stores": {
			"file": "showinfo.DBF",
			"doctype": "Store Location",
			"field_count": len(STORE_MAPPING),
			"fields": STORE_MAPPING,
		},
	}
