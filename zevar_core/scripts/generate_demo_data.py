#!/usr/bin/env python3
"""
Generate realistic jewelry product data for demo purposes.
"""

import json
import random
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent / "scraped_data"

# Define product templates
RING_STYLES = [
	"Solitaire Diamond Ring",
	"Halo Engagement Ring",
	"Three Stone Ring",
	"Eternity Band",
	"Cluster Ring",
	"Signet Ring",
	"Promise Ring",
	"Stackable Ring Set",
	"Wedding Band",
	"Anniversary Band",
	"Cocktail Ring",
	"Statement Ring",
	"Birthstone Ring",
]

NECKLACE_STYLES = [
	"Rope Chain",
	"Box Chain",
	"Cable Chain",
	"Figaro Chain",
	"Cuban Link Chain",
	"Herringbone Chain",
	"Singapore Chain",
	"Diamond Pendant Necklace",
	"Pearl Strand",
	"Lariat Necklace",
	"Choker",
	"Tennis Necklace",
	"Cross Pendant",
]

EARRING_STYLES = [
	"Diamond Studs",
	"Hoop Earrings",
	"Drop Earrings",
	"Huggie Earrings",
	"Chandelier Earrings",
	"Threader Earrings",
	"Stud Set",
	"Pearl Studs",
	"Dangle Earrings",
	"Crawler Earrings",
]

BRACELET_STYLES = [
	"Tennis Bracelet",
	"Cuban Link Bracelet",
	"Bangle",
	"Charm Bracelet",
	"Cuff Bracelet",
	"Chain Bracelet",
	"ID Bracelet",
	"Beaded Bracelet",
	"Wrap Bracelet",
]

PENDANT_STYLES = [
	"Diamond Cross",
	"Heart Pendant",
	"Initial Pendant",
	"Evil Eye",
	"Locket",
	"Birthstone Pendant",
	"Religious Medal",
	"Compass Pendant",
	"Key Pendant",
	"Circle Pendant",
	"Bar Pendant",
]

WATCH_BRANDS = [
	"Bulova",
	"Citizen",
	"Seiko",
	"Invicta",
	"Anne Klein",
	"Timex",
	"Fossil",
	"Michael Kors",
	"GUESS",
	"Casio",
]

WATCH_STYLES = [
	"Classic Automatic",
	"Chronograph",
	"Dress Watch",
	"Sport Watch",
	"Diver's Watch",
	"Diamond Accent",
	"Eco-Drive",
	"Solar Powered",
]

METALS = [
	"14k Yellow Gold",
	"14k White Gold",
	"14k Rose Gold",
	"10k Yellow Gold",
	"10k White Gold",
	"Sterling Silver",
	"18k Yellow Gold",
	"Platinum",
	"925 Sterling Silver",
]

LENGTHS = ['16"', '18"', '20"', '22"', '24"', '7.5"', '8"']


def generate_products():
	"""Generate comprehensive product list."""
	products = []
	sku_counter = 1

	# Generate Rings (40 products)
	for i in range(40):
		metal = random.choice(METALS)
		style = random.choice(RING_STYLES)
		carat = random.choice(["1/4ct", "1/2ct", "3/4ct", "1ct", "1.5ct", "2ct", ""])

		name = f"{metal} {carat} {style}".replace("  ", " ").strip()
		price = round(random.uniform(89, 4999), 2)

		if "Diamond" in style or "ct" in name:
			price = round(random.uniform(499, 7999), 2)
		if "Platinum" in metal or "18k" in metal:
			price *= 1.5

		products.append(
			{
				"name": name,
				"price": round(price, 2),
				"category": "rings",
				"image_url": f"https://images.unsplash.com/photo-160510080476{3 + i % 10}-247f67b3557e?w=400",
				"product_url": f"https://partner.example.com/rings/{sku_counter}",
				"sku": f"RING-{sku_counter:04d}",
				"source": "demo",
			}
		)
		sku_counter += 1

	# Generate Necklaces (35 products)
	for i in range(35):
		metal = random.choice(METALS)
		style = random.choice(NECKLACE_STYLES)
		length = random.choice(LENGTHS[:5])

		name = f"{metal} {style} {length}"
		price = round(random.uniform(79, 2499), 2)

		if "Diamond" in style or "Tennis" in style:
			price = round(random.uniform(899, 5999), 2)

		products.append(
			{
				"name": name,
				"price": round(price, 2),
				"category": "necklaces",
				"image_url": f"https://images.unsplash.com/photo-159964347851{8 + i % 10}-a784e5dc4c8f?w=400",
				"product_url": f"https://partner.example.com/necklaces/{sku_counter}",
				"sku": f"NECK-{sku_counter:04d}",
				"source": "demo",
			}
		)
		sku_counter += 1

	# Generate Earrings (35 products)
	for i in range(35):
		metal = random.choice(METALS)
		style = random.choice(EARRING_STYLES)
		carat = random.choice(["1/4ct TW", "1/2ct TW", "1ct TW", ""])

		name = f"{metal} {carat} {style}".replace("  ", " ").strip()
		price = round(random.uniform(49, 1999), 2)

		if "Diamond" in style:
			price = round(random.uniform(299, 3999), 2)

		products.append(
			{
				"name": name,
				"price": round(price, 2),
				"category": "earrings",
				"image_url": f"https://images.unsplash.com/photo-158844465073{3 + i % 10}-d0b9e0f2f1f8?w=400",
				"product_url": f"https://partner.example.com/earrings/{sku_counter}",
				"sku": f"EAR-{sku_counter:04d}",
				"source": "demo",
			}
		)
		sku_counter += 1

	# Generate Bracelets (30 products)
	for i in range(30):
		metal = random.choice(METALS)
		style = random.choice(BRACELET_STYLES)
		length = random.choice(LENGTHS[5:])

		name = f"{metal} {style} {length}"
		price = round(random.uniform(69, 2999), 2)

		if "Tennis" in style:
			price = round(random.uniform(999, 6999), 2)

		products.append(
			{
				"name": name,
				"price": round(price, 2),
				"category": "bracelets",
				"image_url": f"https://images.unsplash.com/photo-161159143728{1 + i % 10}-460bfbe1220a?w=400",
				"product_url": f"https://partner.example.com/bracelets/{sku_counter}",
				"sku": f"BRAC-{sku_counter:04d}",
				"source": "demo",
			}
		)
		sku_counter += 1

	# Generate Pendants (30 products)
	for i in range(30):
		metal = random.choice(METALS)
		style = random.choice(PENDANT_STYLES)

		name = f"{metal} {style}"
		price = round(random.uniform(39, 999), 2)

		if "Diamond" in style:
			price = round(random.uniform(199, 1999), 2)

		products.append(
			{
				"name": name,
				"price": round(price, 2),
				"category": "pendants",
				"image_url": f"https://images.unsplash.com/photo-151556214120{7 + i % 10}-7a88fb7ce338?w=400",
				"product_url": f"https://partner.example.com/pendants/{sku_counter}",
				"sku": f"PEND-{sku_counter:04d}",
				"source": "demo",
			}
		)
		sku_counter += 1

	# Generate Watches (30 products)
	for i in range(30):
		brand = random.choice(WATCH_BRANDS)
		style = random.choice(WATCH_STYLES)
		gender = random.choice(["Men's", "Women's", "Unisex"])

		name = f"{brand} {gender} {style}"

		if brand in ["Michael Kors", "Fossil"]:
			price = round(random.uniform(95, 295), 2)
		elif brand in ["Seiko", "Citizen", "Bulova"]:
			price = round(random.uniform(195, 595), 2)
		else:
			price = round(random.uniform(49, 199), 2)

		products.append(
			{
				"name": name,
				"price": round(price, 2),
				"category": "watches",
				"image_url": f"https://images.unsplash.com/photo-152327533568{4 + i % 10}-37898b6baf30?w=400",
				"product_url": f"https://partner.example.com/watches/{sku_counter}",
				"sku": f"WATCH-{sku_counter:04d}",
				"source": "demo",
			}
		)
		sku_counter += 1

	return products


if __name__ == "__main__":
	OUTPUT_DIR.mkdir(exist_ok=True)

	products = generate_products()

	# Save to JSON
	output_file = OUTPUT_DIR / "demo_products.json"
	with open(output_file, "w") as f:  # nosemgrep: frappe-semgrep-rules.rules.security.frappe-security-file-traversal
		json.dump(products, f, indent=2)

	print(f"✅ Generated {len(products)} demo products")
	print(f"   Saved to: {output_file}")

	# Print summary
	by_category = {}
	for p in products:
		cat = p["category"]
		by_category[cat] = by_category.get(cat, 0) + 1

	print("\n📊 Summary by category:")
	for cat, count in sorted(by_category.items()):
		print(f"   - {cat}: {count}")
