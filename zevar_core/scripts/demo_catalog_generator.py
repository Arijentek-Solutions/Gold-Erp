#!/usr/bin/env python3
"""
Generate Demo Jewelry Catalog with Real Product Images
=======================================================
Uses Unsplash free jewelry images for professional white-background photos.

Usage:
    python demo_catalog_generator.py --count 200
"""

import argparse
import json
import random
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "scraped_data"

# Real Unsplash jewelry image IDs (professional white/clean background jewelry photos)
RING_IMAGES = [
	"https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1589674781759-c21c37956a44?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1602751584552-8ba73aad10e1?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1543294001-f7cd5d7fb516?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1611955167811-4711904bb9f8?w=400&h=400&fit=crop",
]

NECKLACE_IMAGES = [
	"https://images.unsplash.com/photo-1599458448510-59aecaea4752?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1603974372039-adc49044b6bd?w=400&h=400&fit=crop",
]

EARRING_IMAGES = [
	"https://images.unsplash.com/photo-1635767798638-3e25273a8236?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1588444837495-c6cfee53f5?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1610694955371-d4a3e0ce4b52?w=400&h=400&fit=crop",
]

BRACELET_IMAGES = [
	"https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1602524816025-faae4dab1002?w=400&h=400&fit=crop",
]

WATCH_IMAGES = [
	"https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1622434641406-a158123450f9?w=400&h=400&fit=crop",
]

PENDANT_IMAGES = [
	"https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop",
	"https://images.unsplash.com/photo-1602524816025-faae4dab1002?w=400&h=400&fit=crop",
]

# Product templates
RING_TEMPLATES = [
	"{metal} {carat}ct Diamond Solitaire Ring",
	"{metal} Diamond Halo Engagement Ring",
	"{metal} {gem} and Diamond Ring",
	"{metal} Eternity Band with {carat}ct TW",
	"{metal} Classic Wedding Band",
	"{metal} Three Stone Diamond Ring",
	"{metal} Vintage Style Ring",
	"{metal} {gem} Birthstone Ring",
	"{metal} Cluster Diamond Ring",
	"{metal} Promise Ring",
]

NECKLACE_TEMPLATES = [
	"{metal} {length} Rope Chain",
	"{metal} {length} Box Chain",
	"{metal} {length} Figaro Chain",
	"{metal} Diamond Pendant {length}",
	"{metal} {gem} Pendant Necklace",
	"{metal} {length} Cuban Link Chain",
	"{metal} Tennis Necklace {carat}ct TW",
	"{metal} Pearl Strand {length}",
	"{metal} Cross Pendant {length}",
]

EARRING_TEMPLATES = [
	"{metal} {carat}ct Diamond Studs",
	"{metal} Hoop Earrings",
	"{metal} {gem} Drop Earrings",
	"{metal} Diamond Huggie Earrings",
	"{metal} Chandelier Earrings",
	"{metal} Pearl Studs",
	"{metal} Diamond Cluster Earrings",
	"{metal} {gem} Birthstone Studs",
]

BRACELET_TEMPLATES = [
	"{metal} Tennis Bracelet {carat}ct",
	"{metal} Cuban Link Bracelet {length}",
	"{metal} Bangle Bracelet",
	"{metal} Charm Bracelet",
	"{metal} Diamond Bangle {carat}ct",
	"{metal} Chain Bracelet {length}",
	"{metal} {gem} Line Bracelet",
]

PENDANT_TEMPLATES = [
	"{metal} Diamond Heart Pendant",
	"{metal} Initial Pendant",
	"{metal} Cross Pendant",
	"{metal} {gem} Pendant",
	"{metal} Locket Pendant",
	"{metal} Evil Eye Pendant",
	"{metal} Key Pendant",
]

WATCH_TEMPLATES = [
	"{brand} {gender} Classic Watch",
	"{brand} {gender} Chronograph",
	"{brand} {gender} Diamond Accent Watch",
	"{brand} {gender} Sport Watch",
	"{brand} {gender} Dress Watch",
]

METALS = [
	"14K Yellow Gold",
	"14K White Gold",
	"14K Rose Gold",
	"10K Yellow Gold",
	"10K White Gold",
	"Sterling Silver",
	"18K Yellow Gold",
	"Platinum",
]
GEMS = ["Ruby", "Sapphire", "Emerald", "Amethyst", "Topaz", "Aquamarine", "Garnet", "Opal"]
CARATS = [0.25, 0.33, 0.50, 0.75, 1.0, 1.25, 1.5, 2.0]
LENGTHS = ['16"', '18"', '20"', '22"', '24"']
BRACELET_LENGTHS = ['7"', '7.5"', '8"']
BRANDS = ["Bulova", "Citizen", "Seiko", "Fossil", "Michael Kors", "Anne Klein", "Timex", "Invicta"]
GENDERS = ["Men's", "Women's", "Unisex"]


def generate_product(category, sku_num):
	"""Generate a single product."""
	product = {
		"sku": f"ZEV-{category[:3].upper()}-{sku_num:04d}",
		"category": category,
		"source": "demo",
		"created_at": datetime.now().isoformat(),
	}

	metal = random.choice(METALS)
	gem = random.choice(GEMS)
	carat = random.choice(CARATS)

	if category == "rings":
		template = random.choice(RING_TEMPLATES)
		product["name"] = template.format(metal=metal, carat=carat, gem=gem)
		product["image_url"] = random.choice(RING_IMAGES)
		base_price = random.uniform(299, 2999)
		if "Diamond" in product["name"]:
			base_price = random.uniform(799, 7999)
		if "Platinum" in metal or "18K" in metal:
			base_price *= 1.5
		product["price"] = round(base_price, 2)

	elif category == "necklaces":
		length = random.choice(LENGTHS)
		template = random.choice(NECKLACE_TEMPLATES)
		product["name"] = template.format(metal=metal, carat=carat, gem=gem, length=length)
		product["image_url"] = random.choice(NECKLACE_IMAGES)
		base_price = random.uniform(199, 1999)
		if "Diamond" in product["name"] or "Tennis" in product["name"]:
			base_price = random.uniform(999, 5999)
		product["price"] = round(base_price, 2)

	elif category == "earrings":
		template = random.choice(EARRING_TEMPLATES)
		product["name"] = template.format(metal=metal, carat=carat, gem=gem)
		product["image_url"] = random.choice(EARRING_IMAGES)
		base_price = random.uniform(99, 999)
		if "Diamond" in product["name"]:
			base_price = random.uniform(399, 3999)
		product["price"] = round(base_price, 2)

	elif category == "bracelets":
		length = random.choice(BRACELET_LENGTHS)
		template = random.choice(BRACELET_TEMPLATES)
		product["name"] = template.format(metal=metal, carat=carat, gem=gem, length=length)
		product["image_url"] = random.choice(BRACELET_IMAGES)
		base_price = random.uniform(199, 1499)
		if "Tennis" in product["name"]:
			base_price = random.uniform(999, 6999)
		product["price"] = round(base_price, 2)

	elif category == "pendants":
		template = random.choice(PENDANT_TEMPLATES)
		product["name"] = template.format(metal=metal, gem=gem)
		product["image_url"] = random.choice(PENDANT_IMAGES)
		base_price = random.uniform(79, 799)
		if "Diamond" in product["name"]:
			base_price = random.uniform(299, 1999)
		product["price"] = round(base_price, 2)

	elif category == "watches":
		brand = random.choice(BRANDS)
		gender = random.choice(GENDERS)
		template = random.choice(WATCH_TEMPLATES)
		product["name"] = template.format(brand=brand, gender=gender)
		product["image_url"] = random.choice(WATCH_IMAGES)
		if brand in ["Michael Kors", "Fossil"]:
			product["price"] = round(random.uniform(95, 295), 2)
		elif brand in ["Seiko", "Citizen", "Bulova"]:
			product["price"] = round(random.uniform(195, 595), 2)
		else:
			product["price"] = round(random.uniform(49, 199), 2)

	return product


def generate_catalog(count_per_category=30):
	"""Generate full product catalog."""
	products = []
	sku_counter = 1

	categories = ["rings", "necklaces", "earrings", "bracelets", "pendants", "watches"]

	for category in categories:
		print(f"Generating {count_per_category} {category}...")
		for _ in range(count_per_category):
			product = generate_product(category, sku_counter)
			products.append(product)
			sku_counter += 1

	return products


def main():
	parser = argparse.ArgumentParser(description="Generate demo jewelry catalog")
	parser.add_argument("--count", "-c", type=int, default=30, help="Products per category (default: 30)")
	parser.add_argument("--output", "-o", type=str, default="demo_catalog.json", help="Output filename")

	args = parser.parse_args()

	OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

	products = generate_catalog(args.count)

	output_file = OUTPUT_DIR / args.output
	with open(output_file, "w", encoding="utf-8") as f:
		json.dump(products, f, indent=2, ensure_ascii=False)

	print(f"\n✅ Generated {len(products)} products")
	print(f"   Saved to: {output_file}")

	# Summary
	print("\n📊 Summary by category:")
	by_cat = {}
	for p in products:
		by_cat[p["category"]] = by_cat.get(p["category"], 0) + 1
	for cat, count in sorted(by_cat.items()):
		print(f"   - {cat}: {count}")

	# Price stats
	prices = [p["price"] for p in products]
	print(f"\n💰 Price range: ${min(prices):,.2f} - ${max(prices):,.2f}")
	print(f"   Average: ${sum(prices) / len(prices):,.2f}")


if __name__ == "__main__":
	main()
