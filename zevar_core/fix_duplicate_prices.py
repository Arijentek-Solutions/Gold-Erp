#!/usr/bin/env python3
"""Fix duplicate item prices in ERPNext test data"""

import frappe

def fix_duplicate_prices():
    """Remove duplicate item prices that cause test failures"""

    # Find all item prices for test items
    prices = frappe.db.sql("""
        SELECT name, item_code, price_list, creation
        FROM `tabItem Price`
        WHERE item_code IN ('_Test Item', '_Test Item Home Desktop 100')
        ORDER BY item_code, price_list, creation
    """, as_dict=True)

    print(f"Found {len(prices)} item prices to check")

    # Keep only the first one for each item_code + price_list combination
    seen = set()
    deleted_count = 0

    for price in prices:
        key = (price.item_code, price.price_list)
        if key in seen:
            print(f"Deleting duplicate: {price.name} ({price.item_code} / {price.price_list})")
            frappe.delete_doc("Item Price", price.name, ignore_permissions=True)
            deleted_count += 1
        else:
            seen.add(key)

    frappe.db.commit()
    print(f"Cleanup complete! Deleted {deleted_count} duplicate prices")

def execute():
    """Patch entry point"""
    fix_duplicate_prices()
