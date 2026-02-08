#!/usr/bin/env python3
"""
Item Master Import Script for Zevar Jewelers
=============================================
Imports items from JCSWIN legacy data and demo catalog into ERPNext Item master.

Usage (from bench):
    bench --site zevar.localhost execute zevar_core.scripts.import_items_to_erpnext.import_items
    
    # Dry run (no database changes):
    bench --site zevar.localhost execute zevar_core.scripts.import_items_to_erpnext.import_items --kwargs '{"dry_run": true}'
"""

import json
import random
from pathlib import Path
from datetime import datetime

# Unsplash image URLs for different categories
CATEGORY_IMAGES = {
    "rings": [
        "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1589674781759-c21c37956a44?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop",
    ],
    "chains": [
        "https://images.unsplash.com/photo-1599458448510-59aecaea4752?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&h=400&fit=crop",
    ],
    "necklaces": [
        "https://images.unsplash.com/photo-1599458448510-59aecaea4752?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1603974372039-adc49044b6bd?w=400&h=400&fit=crop",
    ],
    "earrings": [
        "https://images.unsplash.com/photo-1635767798638-3e25273a8236?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1610694955371-d4a3e0ce4b52?w=400&h=400&fit=crop",
    ],
    "bracelets": [
        "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1573408301185-9146fe634ad0?w=400&h=400&fit=crop",
    ],
    "pendants": [
        "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=400&fit=crop",
    ],
    "watches": [
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=400&fit=crop",
        "https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e?w=400&h=400&fit=crop",
    ],
}

# Category mapping from JCSWIN to our standard (jewelry_type, product_type)
JCSWIN_CATEGORY_MAP = {
    "ASHFORD WATCHES": ("Watches", "Watch"),
    "CITIZEN WATCH CO.": ("Watches", "Watch"),
    "BULOVA WATCHES": ("Watches", "Watch"),
    "SAIB DIAMONDS INC": ("Rings", "Jewelry"),
    "GBC INC (DIA & COLOR FINISHED GOODS": ("Rings", "Jewelry"),
    "QUALITY GOLD": ("Chains", "Jewelry"),
    "ROYAL CHAIN GROUP": ("Chains", "Jewelry"),
    "JEWELRY DEPOT, INC": ("Necklaces", "Jewelry"),
    "JEWELRY OUTLET LLC": ("Pendants", "Jewelry"),
}

# Jewelry type options
JEWELRY_SUBTYPES = {
    "Rings": ["Solitaire", "Halo", "Three Stone", "Eternity", "Fashion", "Wedding Band", "Engagement"],
    "Chains": ["Rope", "Box", "Figaro", "Cuban", "Paperclip", "Singapore", "Wheat"],
    "Necklaces": ["Pendant", "Tennis", "Choker", "Lariat", "Station"],
    "Earrings": ["Studs", "Hoops", "Drops", "Huggie", "Chandelier", "Climber"],
    "Bracelets": ["Tennis", "Bangle", "Chain", "Cuff", "Charm"],
    "Pendants": ["Heart", "Cross", "Initial", "Birthstone", "Religious"],
    "Watches": ["Dress", "Sport", "Chronograph", "Classic", "Diamond Accent"],
}

METAL_COLORS = ["Yellow", "White", "Rose", "Two-Tone"]
FINISHES = ["Polished", "Brushed", "Matte", "Satin"]
CLASP_TYPES = ["Lobster", "Spring Ring", "Toggle", "Box Clasp", "Hook"]
CHAIN_TYPES = ["Rope", "Box", "Figaro", "Cuban", "Paperclip", "Singapore"]
COUNTRIES = ["ITALY", "USA", "INDIA", "CHINA", "THAILAND"]


def get_random_image(jewelry_type):
    """Get a random image URL for the given jewelry type."""
    category_key = jewelry_type.lower()
    if category_key in CATEGORY_IMAGES:
        return random.choice(CATEGORY_IMAGES[category_key])
    return random.choice(CATEGORY_IMAGES.get("rings", []))


def create_item_groups(dry_run=False):
    """Create the jewelry Item Group hierarchy."""
    import frappe
    
    groups = [
        {"name": "Jewelry", "parent": "All Item Groups"},
        {"name": "Rings", "parent": "Jewelry"},
        {"name": "Engagement Rings", "parent": "Rings"},
        {"name": "Wedding Bands", "parent": "Rings"},
        {"name": "Fashion Rings", "parent": "Rings"},
        {"name": "Necklaces & Chains", "parent": "Jewelry"},
        {"name": "Chains", "parent": "Necklaces & Chains"},
        {"name": "Pendants", "parent": "Necklaces & Chains"},
        {"name": "Necklaces", "parent": "Necklaces & Chains"},
        {"name": "Earrings", "parent": "Jewelry"},
        {"name": "Studs", "parent": "Earrings"},
        {"name": "Hoops", "parent": "Earrings"},
        {"name": "Drops", "parent": "Earrings"},
        {"name": "Bracelets", "parent": "Jewelry"},
        {"name": "Tennis Bracelets", "parent": "Bracelets"},
        {"name": "Chain Bracelets", "parent": "Bracelets"},
        {"name": "Bangles", "parent": "Bracelets"},
        {"name": "Watches", "parent": "All Item Groups"},
        {"name": "Men's Watches", "parent": "Watches"},
        {"name": "Women's Watches", "parent": "Watches"},
    ]
    
    created = 0
    for g in groups:
        if not frappe.db.exists("Item Group", g["name"]):
            if dry_run:
                print(f"[DRY RUN] Would create Item Group: {g['name']} under {g['parent']}")
            else:
                doc = frappe.get_doc({
                    "doctype": "Item Group",
                    "item_group_name": g["name"],
                    "parent_item_group": g["parent"],
                    "is_group": 1 if g["name"] in ["Jewelry", "Watches", "Necklaces & Chains", "Rings", "Earrings", "Bracelets"] else 0
                })
                doc.insert(ignore_permissions=True)
                created += 1
                print(f"Created Item Group: {g['name']}")
    
    if not dry_run:
        frappe.db.commit()
    
    return created


def load_demo_catalog():
    """Load the demo catalog JSON."""
    demo_path = Path(__file__).parent / "scraped_data" / "demo_catalog.json"
    if demo_path.exists():
        with open(demo_path, 'r') as f:
            return json.load(f)
    return []


def load_jcswin_data():
    """Load data from JCSWIN DBF file."""
    try:
        from dbfread import DBF
        dbf_path = "/workspace/development/Zevar_URMS/JCSWIN 1(1)/JCSWIN/inventor.DBF"
        db = DBF(dbf_path, encoding='latin-1')
        
        items = []
        for record in db:
            # Only import items with sufficient data
            if record.get('STOCKNO') and record.get('DESCRIPT'):
                items.append(dict(record))
        
        return items
    except Exception as e:
        print(f"Error loading JCSWIN data: {e}")
        return []


def map_jcswin_item(record):
    """Map a JCSWIN record to Item fields."""
    category = record.get('CATEGORY', '').strip()
    jewelry_type, product_type = JCSWIN_CATEGORY_MAP.get(category, ("Other", "Jewelry"))
    
    # Parse gold type for purity - use exact names from Zevar Purity doctype
    gold_type = record.get('GOLDTYPE', '').strip()
    purity = None
    metal_type = None
    if '14K' in gold_type or '14k' in gold_type:
        purity = "14K"
    elif '18K' in gold_type or '18k' in gold_type:
        purity = "18K"
    elif '10K' in gold_type or '10k' in gold_type:
        purity = "10K"
    elif '22K' in gold_type or '22k' in gold_type:
        purity = "22K"
    elif '24K' in gold_type or '24k' in gold_type:
        purity = "24K"
    
    if 'GOLD' in category.upper() or gold_type:
        metal_type = "Yellow Gold"
    elif 'SIL' in category.upper() or 'STERLING' in category.upper():
        metal_type = "Silver"
    
    # Get prices
    msrp = record.get('ASKHIGH') or record.get('ASKLOW') or 0
    cost = record.get('COST') or 0
    
    return {
        "item_code": f"JCS-{record.get('STOCKNO', '').strip()}",
        "item_name": record.get('DESCRIPT', '').strip()[:140],
        "item_group": jewelry_type if jewelry_type != "Other" else "Products",
        "stock_uom": "Nos",
        "is_stock_item": 1,
        "include_item_in_manufacturing": 0,
        "custom_product_type": product_type,
        "custom_jewelry_type": jewelry_type,
        "custom_jewelry_subtype": random.choice(JEWELRY_SUBTYPES.get(jewelry_type, [""])),
        "custom_metal_type": metal_type,
        "custom_purity": purity,
        "custom_material_color": random.choice(METAL_COLORS) if metal_type else None,
        "custom_finish": random.choice(FINISHES),
        "custom_vendor_sku": record.get('STYLE', '').strip(),
        "custom_country_of_origin": random.choice(COUNTRIES),
        "custom_msrp": msrp,
        "custom_cost_price": cost,
        "custom_source": "JCSWIN",
        "custom_gender": random.choice(["Unisex", "Men's", "Women's"]),
        "custom_gross_weight_g": record.get('GOLDWGHT') or record.get('WEIGHT'),
        "image": get_random_image(jewelry_type),
        "description": f"{record.get('DESC2', '')} {record.get('DESC3', '')}".strip() or None,
    }


def map_demo_item(record):
    """Map a demo catalog record to Item fields."""
    category = record.get('category', 'rings').title()
    if category == "Necklaces":
        category = "Chains"  # Map to our standard
    
    # Parse metal from name
    name = record.get('name', '')
    metal_type = None
    purity = None
    if 'Yellow Gold' in name:
        metal_type = "Yellow Gold"
    elif 'White Gold' in name:
        metal_type = "White Gold"
    elif 'Rose Gold' in name:
        metal_type = "Rose Gold"
    elif 'Platinum' in name:
        metal_type = "Platinum"
    elif 'Sterling' in name:
        metal_type = "Silver"
    
    # Use exact names from Zevar Purity doctype
    if '14K' in name:
        purity = "14K"
    elif '18K' in name:
        purity = "18K"
    elif '10K' in name:
        purity = "10K"
    elif '22K' in name:
        purity = "22K"
    elif '24K' in name:
        purity = "24K"
    elif 'Sterling' in name:
        purity = "925 Sterling"
    
    price = record.get('price', 0)
    
    return {
        "item_code": record.get('sku', f"ZEV-{random.randint(10000, 99999)}"),
        "item_name": name[:140],
        "item_group": category if category in ["Rings", "Chains", "Earrings", "Bracelets", "Pendants", "Watches"] else "Products",
        "stock_uom": "Nos",
        "is_stock_item": 1,
        "include_item_in_manufacturing": 0,
        "custom_product_type": "Watch" if category == "Watches" else "Jewelry",
        "custom_jewelry_type": category,
        "custom_jewelry_subtype": random.choice(JEWELRY_SUBTYPES.get(category, [""])),
        "custom_metal_type": metal_type,
        "custom_purity": purity,
        "custom_material_color": random.choice(METAL_COLORS) if metal_type and "Gold" in metal_type else None,
        "custom_finish": random.choice(FINISHES),
        "custom_country_of_origin": random.choice(COUNTRIES),
        "custom_msrp": price,
        "custom_cost_price": round(price * 0.4, 2),  # Assume 40% cost
        "custom_source": "Demo",
        "custom_gender": random.choice(["Unisex", "Men's", "Women's"]),
        "custom_length_value": round(random.uniform(6, 24), 1) if category in ["Chains", "Necklaces", "Bracelets"] else None,
        "custom_length_unit": "in" if category in ["Chains", "Necklaces", "Bracelets"] else None,
        "custom_width_value": round(random.uniform(1, 5), 1) if category == "Chains" else None,
        "custom_width_unit": "mm" if category == "Chains" else None,
        "custom_chain_type": random.choice(CHAIN_TYPES) if category in ["Chains", "Necklaces"] else None,
        "custom_clasp_type": random.choice(CLASP_TYPES) if category in ["Chains", "Necklaces", "Bracelets"] else None,
        "image": record.get('image_url'),
    }


def import_items(dry_run=False, limit=None, source="all"):
    """
    Import items into ERPNext Item master.
    
    Args:
        dry_run: If True, don't make database changes
        limit: Max items to import (None for all)
        source: "jcswin", "demo", or "all"
    """
    import frappe
    
    print("=" * 60)
    print("Zevar Item Master Import")
    print("=" * 60)
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"Source: {source}")
    print(f"Limit: {limit or 'No limit'}")
    print()
    
    # Create Item Groups first
    print("Step 1: Creating Item Groups...")
    groups_created = create_item_groups(dry_run)
    print(f"  Created {groups_created} new Item Groups")
    print()
    
    items_to_import = []
    
    # Load demo catalog
    if source in ["all", "demo"]:
        print("Step 2a: Loading Demo Catalog...")
        demo_items = load_demo_catalog()
        print(f"  Found {len(demo_items)} demo items")
        for item in demo_items:
            items_to_import.append(map_demo_item(item))
    
    # Load JCSWIN data
    if source in ["all", "jcswin"]:
        print("Step 2b: Loading JCSWIN Data...")
        jcswin_items = load_jcswin_data()
        print(f"  Found {len(jcswin_items)} JCSWIN items")
        
        # Filter to items with COMPLETE data:
        # - Must have price data (COST or ASKHIGH > 0)
        # - Must have a description (DESCRIPT not empty)
        # - Must have a stock number (STOCKNO not empty)
        quality_items = [
            r for r in jcswin_items 
            if ((r.get('COST') or 0) > 0 or (r.get('ASKHIGH') or 0) > 0)
            and r.get('DESCRIPT', '').strip()
            and r.get('STOCKNO', '').strip()
        ]
        print(f"  {len(quality_items)} items with complete data (price + description)")
        
        # Import ALL quality items (no limit)
        for item in quality_items:
            items_to_import.append(map_jcswin_item(item))
    
    if limit:
        items_to_import = items_to_import[:limit]
    
    print()
    print(f"Step 3: Importing {len(items_to_import)} items...")
    
    imported = 0
    skipped = 0
    errors = 0
    
    for item_data in items_to_import:
        item_code = item_data.get("item_code")
        
        # Check if already exists
        if frappe.db.exists("Item", item_code):
            skipped += 1
            continue
        
        if dry_run:
            print(f"  [DRY RUN] Would create: {item_code} - {item_data.get('item_name', '')[:50]}")
            imported += 1
            continue
        
        try:
            # Clean None values
            clean_data = {k: v for k, v in item_data.items() if v is not None}
            clean_data["doctype"] = "Item"
            
            doc = frappe.get_doc(clean_data)
            doc.insert(ignore_permissions=True)
            imported += 1
            
            if imported % 50 == 0:
                print(f"  Imported {imported} items...")
                frappe.db.commit()
                
        except Exception as e:
            errors += 1
            if errors <= 5:
                print(f"  Error with {item_code}: {str(e)[:100]}")
    
    if not dry_run:
        frappe.db.commit()
    
    print()
    print("=" * 60)
    print("Import Complete!")
    print(f"  Imported: {imported}")
    print(f"  Skipped (existing): {skipped}")
    print(f"  Errors: {errors}")
    print("=" * 60)
    
    return {"imported": imported, "skipped": skipped, "errors": errors}


if __name__ == "__main__":
    # For standalone testing
    print("Run this script via bench:")
    print("  bench --site zevar.localhost execute zevar_core.scripts.import_items_to_erpnext.import_items")


def test_single_item():
    """Test creating a single item to debug issues."""
    import frappe
    
    test_data = {
        "doctype": "Item",
        "item_code": "TEST-IMPORT-001",
        "item_name": "Test 14K Yellow Gold Ring",
        "item_group": "Rings",
        "stock_uom": "Nos",
        "is_stock_item": 1,
        "include_item_in_manufacturing": 0,
        "custom_product_type": "Jewelry",
        "custom_jewelry_type": "Rings",
        "custom_jewelry_subtype": "Fashion",
        "custom_metal_type": "Yellow Gold",
        "custom_purity": "14K",
        "custom_material_color": "Yellow",
        "custom_finish": "Polished",
        "custom_country_of_origin": "USA",
        "custom_msrp": 500.0,
        "custom_cost_price": 200.0,
        "custom_source": "Demo",
        "custom_gender": "Unisex",
        "image": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=400&h=400&fit=crop",
    }
    
    # Delete existing if any
    if frappe.db.exists("Item", test_data["item_code"]):
        frappe.delete_doc("Item", test_data["item_code"], force=True)
        frappe.db.commit()
        print(f"Deleted existing: {test_data['item_code']}")
    
    try:
        doc = frappe.get_doc(test_data)
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"SUCCESS - Created: {doc.name}")
        return {"status": "success", "item_code": doc.name}
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"ERROR: {e}")
        return {"status": "error", "error": str(e)}
