import random

import frappe


def run():
    frappe.set_user("Administrator")
    print("💎 Generating Zevar Dummy Data (Using Verified IDs)...")

    # ---------------------------------------------------------
    # 1. SETUP DATA POOLS (Using Exact IDs from your Screenshots)
    # ---------------------------------------------------------

    # Matches your "Zevar Metal" IDs
    metals = ["Gold", "Silver", "Platinum"]

    # Matches your "Zevar Purity" IDs
    purities = ["24K", "22K", "18K", "14K", "10K", "925 Sterling", "999 Fine"]

    items_types = ["Ring", "Chain", "Bracelet", "Earrings", "Necklace"]

    # ---------------------------------------------------------
    # 2. CREATE ITEMS
    # ---------------------------------------------------------
    created_items = []

    # Ensure Item Group exists
    if not frappe.db.exists("Item Group", "Products"):
        frappe.get_doc(
            {
                "doctype": "Item Group",
                "item_group_name": "Products",
                "is_group": 0,
                "parent_item_group": "All Item Groups",
            }
        ).insert(ignore_permissions=True)

    print("   Creating Items...")
    for i in range(50):
        metal = random.choice(metals)  # e.g. "Gold"
        purity = random.choice(purities)  # e.g. "22K"
        item_type = random.choice(items_types)

        # Name: "Gold Ring 22K"
        item_name = f"{metal} {item_type} {purity}"

        # Unique Item Code
        item_code = f"{metal[0]}{item_type[0]}-{purity.replace(' ', '')}-{random.randint(1000, 9999)}"

        if not frappe.db.exists("Item", item_code):
            try:
                doc = frappe.get_doc(
                    {
                        "doctype": "Item",
                        "item_code": item_code,
                        "item_name": item_name,
                        "item_group": "Products",
                        "stock_uom": "Nos",
                        "is_stock_item": 1,
                        "valuation_rate": random.randint(300, 2000),
                        # LINKING: We use the variables directly because they match the IDs now
                        "custom_metal_type": metal,
                        "custom_purity": purity,
                        "custom_gross_weight_g": round(random.uniform(3.0, 20.0), 3),
                        "custom_making_charge_type": "Fixed Amount",
                        "custom_making_charge_value": random.randint(50, 200),
                    }
                )
                doc.insert(ignore_permissions=True)
                created_items.append(item_code)
                print(f"   Created: {item_name}")
            except Exception as e:
                print(f"   ⚠️ Skipping {item_name}: {str(e)}")

    # ---------------------------------------------------------
    # 3. ADD STOCK
    # ---------------------------------------------------------
    print("📦 Adding Stock...")

    # Get a valid Warehouse
    target_warehouse = frappe.db.get_value("Warehouse", {"name": ["like", "%Store 2%"]})
    if not target_warehouse:
        target_warehouse = frappe.db.get_value(
            "Warehouse", {"is_group": 0, "parent_warehouse": ["like", "%Zevar%"]}
        )

    if target_warehouse and created_items:
        se = frappe.new_doc("Stock Entry")
        se.stock_entry_type = "Material Receipt"  # Validated for v15
        se.company = frappe.defaults.get_user_default(
            "Company"
        ) or frappe.db.get_single_value("Global Defaults", "default_company")

        for item in created_items:
            # 80% chance to add stock
            if random.random() > 0.2:
                se.append(
                    "items",
                    {
                        "item_code": item,
                        "t_warehouse": target_warehouse,
                        "qty": random.randint(1, 10),
                        "basic_rate": random.randint(400, 1500),
                    },
                )

        if se.items:
            se.insert(ignore_permissions=True)
            se.submit()
            print(f"✅ Stock successfully added to {target_warehouse}!")

    frappe.db.commit()
