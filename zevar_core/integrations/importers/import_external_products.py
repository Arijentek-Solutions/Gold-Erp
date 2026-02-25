#!/usr/bin/env python3
"""
Import External Product Data to ERPNext
========================================
This script imports product data from JSON/CSV files that you can populate
by manually scraping or copying product info from QGold, Stuller, etc.

Usage:
    python import_external_products.py scraped_data/my_products.json
    python import_external_products.py scraped_data/my_products.csv

Expected JSON format:
[
    {
        "name": "14k Yellow Gold Diamond Ring",
        "price": 1299.00,
        "category": "rings",
        "image_url": "https://images.qgold.com/...",
        "sku": "ABC123"
    },
    ...
]

Expected CSV format:
name,price,category,image_url,sku
14k Yellow Gold Diamond Ring,1299.00,rings,https://...,ABC123
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

# Add frappe path
sys.path.insert(0, "/workspace/development/frappe-bench/apps/frappe")
sys.path.insert(0, "/workspace/development/frappe-bench/sites")

# For running from command line
OUTPUT_DIR = Path(__file__).parent / "scraped_data"


def load_products_json(filepath):
	"""Load products from JSON file."""
	with open(filepath) as f:  # nosemgrep: frappe-semgrep-rules.rules.security.frappe-security-file-traversal
		return json.load(f)


def load_products_csv(filepath):
	"""Load products from CSV file."""
	products = []
	with open(filepath) as f:  # nosemgrep: frappe-semgrep-rules.rules.security.frappe-security-file-traversal
		reader = csv.DictReader(f)
		for row in reader:
			product = {
				"name": row.get("name", "").strip(),
				"price": float(row.get("price", 0) or 0),
				"category": row.get("category", "").strip().lower(),
				"image_url": row.get("image_url", "").strip(),
				"sku": row.get("sku", "").strip(),
				"source": row.get("source", "external").strip(),
			}
			if product["name"]:
				products.append(product)
	return products


def validate_products(products):
	"""Validate product data."""
	valid = []
	errors = []

	for i, p in enumerate(products):
		if not p.get("name"):
			errors.append(f"Product {i}: Missing name")
			continue
		if not p.get("price") or p["price"] <= 0:
			errors.append(f"Product {i} ({p.get('name', 'unknown')}): Invalid price")
			continue
		if not p.get("category"):
			# Default to 'other' if no category
			p["category"] = "other"

		valid.append(p)

	return valid, errors


def print_summary(products):
	"""Print product summary."""
	print("\n📊 Product Summary:")
	print(f"   Total products: {len(products)}")

	by_category = {}
	for p in products:
		cat = p.get("category", "unknown")
		by_category[cat] = by_category.get(cat, 0) + 1

	print("\n   By category:")
	for cat, count in sorted(by_category.items()):
		print(f"     - {cat}: {count}")

	# Price stats
	prices = [p["price"] for p in products if p.get("price")]
	if prices:
		print(f"\n   Price range: ${min(prices):,.2f} - ${max(prices):,.2f}")
		print(f"   Average price: ${sum(prices) / len(prices):,.2f}")


def main():
	parser = argparse.ArgumentParser(description="Import external product data")
	parser.add_argument("file", help="Path to JSON or CSV file with product data")
	parser.add_argument("--validate-only", "-v", action="store_true", help="Only validate, don't import")
	parser.add_argument("--output", "-o", help="Output validated JSON file")

	args = parser.parse_args()
	filepath = Path(args.file)

	if not filepath.exists():
		print(f"❌ File not found: {filepath}")
		sys.exit(1)

	# Load based on extension
	print(f"📂 Loading products from: {filepath}")

	if filepath.suffix.lower() == ".json":
		products = load_products_json(filepath)
	elif filepath.suffix.lower() == ".csv":
		products = load_products_csv(filepath)
	else:
		print(f"❌ Unsupported file format: {filepath.suffix}")
		print("   Supported formats: .json, .csv")
		sys.exit(1)

	print(f"   Loaded {len(products)} products")

	# Validate
	valid_products, errors = validate_products(products)

	if errors:
		print(f"\n⚠️  Validation errors ({len(errors)}):")
		for err in errors[:10]:  # Show first 10
			print(f"   - {err}")
		if len(errors) > 10:
			print(f"   ... and {len(errors) - 10} more")

	print_summary(valid_products)

	# Save validated products
	if args.output:
		output_path = Path(args.output)
	else:
		output_path = OUTPUT_DIR / "validated_products.json"

	with open(output_path, "w") as f:  # nosemgrep: frappe-semgrep-rules.rules.security.frappe-security-file-traversal
		json.dump(valid_products, f, indent=2)
	print(f"\n✅ Saved validated products to: {output_path}")

	if args.validate_only:
		print("\n📝 Validation complete. Use import_to_erpnext.py to import.")
	else:
		print("\n📝 Ready for import. Run:")
		print(f"   python import_to_erpnext.py {output_path}")


if __name__ == "__main__":
	main()
