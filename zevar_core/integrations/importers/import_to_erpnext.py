#!/usr/bin/env python3
"""
Zevar ERPNext Item Importer
===========================
Imports scraped product data into ERPNext Item master.

Usage:
    bench execute zevar_core.scripts.import_to_erpnext.import_products --kwargs '{"file": "scraped_data/qgold_products.json"}'

Or run directly:
    python import_to_erpnext.py scraped_data/qgold_products.json
"""

import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests


def download_image(url: str, save_dir: Path, filename: str = None) -> str:
	"""Download image and return local path."""
	try:
		if not filename:
			filename = Path(urlparse(url).path).name or "product.jpg"

		save_path = save_dir / filename
		if save_path.exists():
			return str(save_path)

		response = requests.get(url, timeout=30)
		if response.status_code == 200:
			save_path.write_bytes(response.content)
			return str(save_path)
	except Exception as e:
		print(f"  ⚠️ Failed to download image: {e}")
	return None


def import_products(file: str = None, dry_run: bool = False):
	"""
	Import products from JSON file to ERPNext Items.

	Args:
	    file: Path to JSON file with scraped products
	    dry_run: If True, don't actually create Items (just validate)
	"""
	import frappe

	if not file:
		print("Please provide a JSON file path")
		return

	filepath = Path(file)
	if not filepath.exists():
		print(f"File not found: {filepath}")
		return

	with open(filepath, "r") as f:
		products = json.load(f)

	print(f"📦 Importing {len(products)} products from {filepath}")

	# Setup
	images_dir = Path(frappe.get_site_path("public", "files", "products"))
	images_dir.mkdir(parents=True, exist_ok=True)

	# Category to Item Group mapping
	CATEGORY_MAP = {
		"rings": "Rings",
		"necklaces": "Necklaces",
		"earrings": "Earrings",
		"bracelets": "Bracelets",
		"pendants": "Pendants",
		"watches": "Watches",
		"charms": "Charms",
	}

	# Ensure Item Groups exist
	for group_name in CATEGORY_MAP.values():
		if not frappe.db.exists("Item Group", group_name):
			if dry_run:
				print(f"  Would create Item Group: {group_name}")
			else:
				frappe.get_doc(
					{
						"doctype": "Item Group",
						"item_group_name": group_name,
						"parent_item_group": "All Item Groups",
						"is_group": 0,
					}
				).insert(ignore_permissions=True)
				print(f"  ✓ Created Item Group: {group_name}")

	# Import products
	created = 0
	skipped = 0
	errors = 0

	for i, product in enumerate(products, 1):
		try:
			# Generate item code from source + sku or name
			sku = product.get("sku", "")
			source = product.get("source", "ext").upper()[:3]
			name = product.get("name", "Product")[:50]

			if sku:
				item_code = f"{source}-{sku}"
			else:
				# Generate from name
				clean_name = "".join(c for c in name if c.isalnum() or c == " ")
				item_code = f"{source}-{clean_name[:20].strip().replace(' ', '-').upper()}"

			# Check if already exists
			if frappe.db.exists("Item", item_code):
				print(f"  ⏭️ {i}. Skipped (exists): {item_code}")
				skipped += 1
				continue

			# Get category
			category = product.get("category", "other").lower()
			item_group = CATEGORY_MAP.get(category, "All Item Groups")

			# Download image
			image_path = None
			if product.get("image_url") and not dry_run:
				image_file = f"{item_code.lower()}.jpg"
				local_path = download_image(product["image_url"], images_dir, image_file)
				if local_path:
					image_path = f"/files/products/{image_file}"

			# Prepare Item doc
			item_doc = {
				"doctype": "Item",
				"item_code": item_code,
				"item_name": name,
				"item_group": item_group,
				"stock_uom": "Nos",
				"is_stock_item": 1,
				"include_item_in_manufacturing": 0,
				"standard_rate": product.get("price", 0),
				"description": f"<p>{name}</p><p>Source: {product.get('source', 'Unknown')}</p>",
				"image": image_path,
			}

			# Custom fields for tracking source
			item_doc["custom_source_url"] = product.get("product_url", "")
			item_doc["custom_source_partner"] = product.get("source", "")

			if dry_run:
				print(f"  📝 {i}. Would create: {item_code} - {name[:30]}... ${product.get('price', 0)}")
			else:
				doc = frappe.get_doc(item_doc)
				doc.insert(ignore_permissions=True)
				print(f"  ✓ {i}. Created: {item_code}")

			created += 1

		except Exception as e:
			print(f"  ✗ {i}. Error: {product.get('name', 'Unknown')[:30]} - {e}")
			errors += 1

	if not dry_run:
		frappe.db.commit()

	# Summary
	print(f"\n{'='*50}")
	print(f"📊 Import Summary")
	print(f"{'='*50}")
	print(f"  Created: {created}")
	print(f"  Skipped: {skipped}")
	print(f"  Errors:  {errors}")
	print(f"  Total:   {len(products)}")

	if dry_run:
		print("\n⚠️  This was a DRY RUN - no items were actually created")
		print("   Run without --dry-run to create items")


# For standalone execution
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Usage: python import_to_erpnext.py <json_file> [--dry-run]")
		sys.exit(1)

	file_path = sys.argv[1]
	dry = "--dry-run" in sys.argv

	# When running outside frappe context
	print("⚠️  For ERPNext import, run via bench:")
	print(
		f'   bench execute zevar_core.scripts.import_to_erpnext.import_products --kwargs \'{{"file": "{file_path}", "dry_run": {str(dry).lower()}}}\''
	)
