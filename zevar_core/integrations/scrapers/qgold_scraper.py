import asyncio
import json
import os
import argparse
import requests
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async # Standard import
from urllib.parse import urljoin, urlparse

# --- Configuration ---
BASE_URL = "https://qgold.com"
OUTPUT_DIR = "scraped_data"

MAIN_CATEGORY_MAP = {
    "chains": "https://qgold.com/pl/jewelry-chains",
    "pendants": "https://qgold.com/pl/jewelry-pendants-and-charms",
    "earrings": "https://qgold.com/pl/jewelry-earrings",
    "necklaces": "https://qgold.com/pl/jewelry-necklaces",
    "rings": "https://qgold.com/pl/jewelry-rings",
    "bracelets": "https://qgold.com/pl/jewelry-bracelets",
    "beads": "https://qgold.com/pl/jewelry-bead-jewelry",
    "anklets": "https://qgold.com/pl/jewelry-anklets",
}

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

async def remove_qgold_overlay(page):
    try:
        removed = await page.evaluate("""
            () => {
                const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
                let node;
                let count = 0;
                while(node = walker.nextNode()) {
                    if (node.nodeValue.includes("Browser not Supported")) {
                        const container = node.parentElement;
                        if (container) {
                            container.remove();
                            count++;
                        }
                    }
                }
                return count;
            }
        """)
        if removed > 0: print(f"  ✅ Removed {removed} overlays.")
    except Exception as e: pass

async def get_sub_categories(page, main_url):
    print("  🔍 Scanning for Sub-Categories...")
    sub_links = []
    blacklist = ['edge', 'chrome', 'firefox', 'safari', 'download', 'update']
    try:
        all_links = await page.locator('//a[not(contains(@href, "cart")) and not(contains(@href, "account"))]').all()
        current_path = urlparse(main_url).path
        for link in all_links:
            try:
                href = await link.get_attribute('href')
                text = await link.inner_text().strip().lower()
                if text and href and current_path not in href:
                    if any(bad in text for bad in blacklist): continue
                    if 3 < len(text) < 60: 
                        full_url = urljoin(BASE_URL, href)
                        if not any(l['url'] == full_url for l in sub_links):
                            sub_links.append({"name": text, "url": full_url})
            except: continue
    except Exception as e: pass
    print(f"    ✅ Found {len(sub_links)} sub-categories.")
    return sub_links

async def scrape_products_from_page(page, category_name):
    items = []
    await page.wait_for_timeout(2000)
    potential_items = await page.locator('//*[contains(text(), "$") or contains(text(), "MSRP")]').all()
    for container in potential_items:
        if len(items) >= 1000: break 
        try:
            img = container.locator('.//img').first
            if await img.count() == 0: continue
            src = await img.get_attribute('src')
            if not src: src = await img.get_attribute('data-src')
            if not src: continue
            if any(x in src.lower() for x in ['icon', 'logo', 'sprite', 'banner']): continue
            
            full_text = await container.inner_text()
            lines = [line.strip() for line in full_text.split('\n') if line.strip()]
            name = lines[0] if lines else "Unknown"
            price = "0.00"
            for line in lines:
                if "MSRP" in line or "$" in line:
                    price = line.replace("MSRP", "").replace(":", "").strip()
                    break
            
            img_filename = None
            try:
                if not src.startswith('http'): src = urljoin(BASE_URL, src)
                ext = os.path.splitext(src)[1].split('?')[0] or ".jpg"
                img_filename = f"{OUTPUT_DIR}/{category_name}_{len(items)}{ext}"
                r = requests.get(src, timeout=5)
                if r.status_code == 200:
                    with open(img_filename, 'wb') as f: f.write(r.content)
            except: pass
            items.append({"name": name, "price": price, "image_url": src, "local_image": img_filename})
        except: continue
    return items

async def scrape_main_category(category_key, limit):
    main_url = MAIN_CATEGORY_MAP.get(category_key)
    if not main_url: return
    ensure_dir(OUTPUT_DIR)
    output_file = f"{OUTPUT_DIR}/{category_key}_products.json"
    print(f"🚀 Spidering: {category_key} -> {main_url}")
    
    all_data = []
    browser_args = ['--disable-blink-features=AutomationControlled', '--no-sandbox']
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=browser_args)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1280}, locale='en-US', timezone_id='America/New_York'
        )
        page = await context.new_page()
        
        # FIX: Use standard stealth_async import
        await stealth_async(page)

        try:
            print("  ⏳ Loading Main Category Page...")
            await page.goto(main_url, wait_until="commit", timeout=60000)
            await remove_qgold_overlay(page)

            sub_links = await get_sub_categories(page, main_url)

            if not sub_links:
                print("  ⚠️  No sub-categories found. Scraping main page directly...")
                items = await scrape_products_from_page(page, category_key)
                all_data.extend(items)
            else:
                for link in sub_links:
                    if len(all_data) >= limit: break
                    print(f"  ➡️  Entering Sub-Category: {link['name']}")
                    try:
                        await page.goto(link['url'], wait_until="commit", timeout=60000)
                        await remove_qgold_overlay(page)
                        await page.wait_for_timeout(2000)
                        
                        page_items = await scrape_products_from_page(page, category_name)
                        all_data.extend(page_items[:limit - len(all_data)])
                        print(f"    📦 Scraped {len(page_items)} items. (Total: {len(all_data)})")
                        
                        if len(all_data) >= limit: break
                    except Exception as e:
                        print(f"    ❌ Error scraping sub-category: {e}")
                        continue

        except Exception as e:
            print(f"❌ Critical Error: {e}")
            await page.screenshot(path=f"{OUTPUT_DIR}/error_{category_key}.png")
        finally:
            await browser.close()

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    print(f"✅ Finished '{category_key}'. Total: {len(all_data)} items.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--category', type=str, default='rings', help='Category key')
    parser.add_argument('--limit', type=int, default=100, help='Target limit')
    args = parser.parse_args()

    if args.category == "all":
        for cat in MAIN_CATEGORY_MAP.keys():
            asyncio.run(scrape_main_category(cat, args.limit))
    else:
        asyncio.run(scrape_main_category(args.category, args.limit))