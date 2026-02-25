#!/usr/bin/env python3
"""
Blue Nile Jewelry Scraper
=========================
Scrapes jewelry products from Blue Nile's public catalog.
Blue Nile has clean product pages with good images on white backgrounds.

Usage:
    python bluenile_scraper.py --category rings --limit 50
    python bluenile_scraper.py --all --limit 100
"""

import argparse
import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

try:
	from playwright.async_api import async_playwright
except ImportError:
	print("Please install playwright: pip install playwright && playwright install chromium")
	exit(1)

# Configuration
BASE_URL = "https://www.bluenile.com"
OUTPUT_DIR = Path(__file__).parent / "scraped_data"

# Blue Nile categories with their URLs
CATEGORIES = {
	"rings": "/engagement-rings/recently-purchased-engagement-rings",
	"wedding-bands": "/wedding-rings/womens-wedding-rings",
	"earrings": "/jewelry/earrings",
	"necklaces": "/jewelry/necklaces",
	"bracelets": "/jewelry/bracelets",
	"pendants": "/jewelry/pendants",
}


def ensure_dir(directory):
	"""Create directory if it doesn't exist."""
	Path(directory).mkdir(parents=True, exist_ok=True)


def download_image(url, filepath):
	"""Download image to local file."""
	try:
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
		r = requests.get(url, headers=headers, timeout=10)
		if r.status_code == 200:
			with open(filepath, "wb") as f:
				f.write(r.content)
			return True
	except Exception as e:
		print(f"    Failed to download image: {e}")
	return False


async def scrape_category(category: str, limit: int = 50, download_images: bool = True):
	"""Scrape products from a Blue Nile category."""

	if category not in CATEGORIES:
		print(f"Unknown category: {category}")
		print(f"Available: {', '.join(CATEGORIES.keys())}")
		return []

	url = BASE_URL + CATEGORIES[category]
	products = []

	async with async_playwright() as p:
		browser = await p.chromium.launch(headless=True)
		context = await browser.new_context(
			user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
			viewport={"width": 1920, "height": 1080},
			locale="en-US",
		)
		page = await context.new_page()

		print(f"🔍 Scraping {category} from {url}...")

		try:
			await page.goto(url, wait_until="domcontentloaded", timeout=60000)
			await page.wait_for_timeout(5000)

			# Try to accept cookies if present
			try:
				cookie_btn = page.locator('button:has-text("Accept")')
				if await cookie_btn.count() > 0:
					await cookie_btn.first.click()
					await page.wait_for_timeout(1000)
			except Exception:
				pass

			# Scroll to load more products
			for _ in range(3):
				await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
				await page.wait_for_timeout(2000)

			# Find product cards
			product_selectors = [
				'[data-testid="product-card"]',
				".product-card",
				'[class*="ProductCard"]',
				'[class*="product-tile"]',
				'article[class*="product"]',
				".gallery-item",
				'li[class*="product"]',
			]

			product_elements = []
			for selector in product_selectors:
				try:
					elements = await page.locator(selector).all()
					if elements and len(elements) > 0:
						product_elements = elements
						print(f"  Found {len(elements)} products with selector: {selector}")
						break
				except Exception:
					continue

			# If no product cards found, try extracting from page content
			if not product_elements:
				print("  Trying alternative extraction method...")

				# Look for any elements with price and image
				cards = await page.locator('a[href*="jewelry"], a[href*="ring"], a[href*="earring"]').all()
				print(f"  Found {len(cards)} potential product links")
				product_elements = cards[:limit]

			# Save debug info
			await page.screenshot(path=str(OUTPUT_DIR / f"debug_{category}.png"), full_page=True)
			content = await page.content()
			with open(OUTPUT_DIR / f"debug_{category}.html", "w") as f:
				f.write(content)
			print("  Debug files saved to scraped_data/")

			# Extract product data
			for i, element in enumerate(product_elements[:limit]):
				try:
					product = {"category": category, "source": "bluenile"}

					# Get link
					href = await element.get_attribute("href")
					if href:
						product["url"] = urljoin(BASE_URL, href)

					# Get text content
					text = await element.inner_text()
					lines = [l.strip() for l in text.split("\n") if l.strip()]

					# Extract name (usually first non-price line)
					for line in lines:
						if not line.startswith("$") and len(line) > 5:
							product["name"] = line
							break

					# Extract price
					for line in lines:
						if "$" in line:
							price_match = re.search(r"\$([\d,]+)", line)
							if price_match:
								product["price"] = float(price_match.group(1).replace(",", ""))
								break

					# Get image
					try:
						img = element.locator("img").first
						if await img.count() > 0:
							src = await img.get_attribute("src") or await img.get_attribute("data-src")
							if src:
								product["image_url"] = urljoin(BASE_URL, src)
					except Exception:
						pass

					# Generate SKU
					product["sku"] = f"BN-{category.upper()[:3]}-{i + 1:04d}"

					if product.get("name") and product.get("price"):
						products.append(product)
						print(f"  ✓ {i + 1}. {product['name'][:40]}... ${product['price']}")

						# Download image
						if download_images and product.get("image_url"):
							img_dir = OUTPUT_DIR / "images" / category
							ensure_dir(img_dir)
							ext = os.path.splitext(product["image_url"])[1].split("?")[0] or ".jpg"
							img_path = img_dir / f"{product['sku']}{ext}"
							if download_image(product["image_url"], str(img_path)):
								product["local_image"] = str(img_path)

				except Exception as e:
					print(f"  ✗ Error extracting product {i}: {e}")
					continue

		except Exception as e:
			print(f"Error loading page: {e}")
			await page.screenshot(path=str(OUTPUT_DIR / f"error_{category}.png"))

		await browser.close()

	return products


async def scrape_all_categories(limit_per_category: int = 20):
	"""Scrape products from all categories."""
	all_products = []

	for category in CATEGORIES:
		print(f"\n{'=' * 50}")
		print(f"Category: {category.upper()}")
		print("=" * 50)

		products = await scrape_category(category, limit_per_category)
		all_products.extend(products)

		await asyncio.sleep(2)  # Be nice to server

	return all_products


def save_products(products, filename=None):
	"""Save products to JSON file."""
	ensure_dir(OUTPUT_DIR)

	if not filename:
		filename = f"bluenile_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

	filepath = OUTPUT_DIR / filename
	with open(filepath, "w", encoding="utf-8") as f:
		json.dump(products, f, indent=2, ensure_ascii=False)

	print(f"\n✅ Saved {len(products)} products to {filepath}")
	return filepath


async def main():
	parser = argparse.ArgumentParser(description="Scrape Blue Nile jewelry products")
	parser.add_argument("--category", "-c", choices=list(CATEGORIES.keys()), help="Category to scrape")
	parser.add_argument("--all", "-a", action="store_true", help="Scrape all categories")
	parser.add_argument("--limit", "-l", type=int, default=20, help="Max products per category (default: 20)")
	parser.add_argument("--no-images", action="store_true", help="Don't download product images")

	args = parser.parse_args()

	if not args.category and not args.all:
		parser.print_help()
		print("\n⚠️  Please specify --category or --all")
		return

	ensure_dir(OUTPUT_DIR)

	if args.all:
		products = await scrape_all_categories(args.limit)
	else:
		products = await scrape_category(args.category, args.limit, not args.no_images)

	if products:
		save_products(products)

		# Print summary
		print("\n📊 Summary:")
		print(f"   Total products: {len(products)}")

		by_category = {}
		for p in products:
			cat = p.get("category", "unknown")
			by_category[cat] = by_category.get(cat, 0) + 1

		for cat, count in sorted(by_category.items()):
			print(f"   - {cat}: {count}")
	else:
		print("\n⚠️  No products scraped. Check the debug files in scraped_data/")


if __name__ == "__main__":
	asyncio.run(main())
