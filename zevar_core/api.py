import json

import frappe


@frappe.whitelist()
def get_pos_items(
    start=0, page_length=20, warehouse=None, search_term=None, filters=None
):
    # 1. Base Filters
    # We use a list of lists for filters
    query_filters = [["disabled", "=", 0], ["has_variants", "=", 0]]

    # 2. Search Term
    if search_term:
        query_filters.append(["item_name", "like", f"%{search_term}%"])

    # 3. Dynamic Filters (FIXED 🛠️)
    if filters:
        # Use Frappe's built-in helper. It handles Strings, Dicts, and None safely.
        filters_dict = frappe.parse_json(filters)

        if isinstance(filters_dict, dict):
            for key, value in filters_dict.items():
                # Only apply if value is "Real" (not empty string, not None)
                if value:
                    print(f"   👉 Applying: {key} = {value}")
                    query_filters.append([key, "=", value])

    # 4. Fetch Items
    # Note: We removed 'custom_metal_type is set' from base filters
    # because it might conflict if we filter for a specific metal.
    items = frappe.get_list(
        "Item",
        filters=query_filters,
        fields=[
            "name",
            "item_name",
            "item_group",
            "image",
            "custom_metal_type",
            "custom_purity",
            "custom_gross_weight_g",
            "custom_net_weight_g",
            "custom_making_charge_type",
            "custom_making_charge_value",
        ],
        order_by="item_group asc, custom_net_weight_g desc",
        start=start,
        page_length=page_length,
    )

    # ... (Keep your existing stock fetching & loop logic below unchanged) ...
    # (If you need the rest of the function again, let me know, but the bottom half is fine)

    # ------------------ COPY FROM HERE FOR THE REST ------------------
    if not items:
        return []

    item_codes = [item.name for item in items]
    stock_map = {}
    if warehouse:
        bin_entries = frappe.db.get_all(
            "Bin",
            filters={"item_code": ["in", item_codes], "warehouse": warehouse},
            fields=["item_code", "actual_qty"],
        )
        stock_map = {b.item_code: b.actual_qty for b in bin_entries}

    pos_items = []
    for item in items:
        qty = stock_map.get(item.name, 0)

        # Safe Price Calculation
        try:
            # We call your existing get_item_price function
            price_data = get_item_price(item.name)
            final_price = price_data.get("final_price", 0.0)
        except Exception:
            final_price = 0.0

        pos_items.append(
            {
                "item_code": item.name,
                "item_name": item.item_name,
                "item_group": item.item_group,
                "image": item.image,
                "stock_qty": qty,
                "price": final_price,
                "metal": item.custom_metal_type,
                "purity": item.custom_purity,
                "gross_weight": item.custom_gross_weight_g,
            }
        )

    return pos_items


@frappe.whitelist()
def get_item_details(item_code):
    item = frappe.get_doc("Item", item_code)
    price_data = get_item_price(item_code)

    gemstones_list = []

    # 🔍 TRICK: Look for the field name found in your screenshot
    table_field = None

    # Check 1: The most likely name (from your screenshot)
    if hasattr(item, "custom_gemstones") and item.custom_gemstones:
        table_field = item.custom_gemstones

    # Check 2: The standard name (fallback)
    elif hasattr(item, "gemstones") and item.gemstones:
        table_field = item.gemstones

    # Process the table if found
    if table_field:
        for gem in table_field:
            gemstones_list.append(
                {
                    "gem_type": gem.gem_type,
                    "carat": gem.carat,
                    "cut": gem.cut,
                    "clarity": gem.clarity,
                    "color": gem.color,
                    "amount": gem.amount,
                }
            )

    return {
        "item_code": item.name,
        "item_name": item.item_name,
        "description": item.description,
        "image": item.image,
        "metal": item.custom_metal_type,
        "purity": item.custom_purity,
        "gross_weight": item.custom_gross_weight_g,
        "net_weight": item.custom_net_weight_g,
        "stone_weight": item.custom_stone_weight_g,
        "gold_rate": price_data.get("gold_rate_used", 0),
        "gold_value": price_data.get("gold_value", 0),
        "making_charges": price_data.get("making_charges", 0),
        "gemstone_value": price_data.get("gemstone_value", 0),
        "final_price": price_data.get("final_price", 0),
        "gemstones": gemstones_list,
    }


@frappe.whitelist(allow_guest=True)
def get_item_price(item_code):
    """
    Calculates live price: (Gold Value) + (Making Charges) + (Gemstone Value).
    Returns breakdown for UI.
    """
    # 1. Fetch Item Details
    item = frappe.get_doc("Item", item_code)
    if not item:
        return {}

    # --- A. METAL VALUE ---
    pricing_metal = item.custom_metal_type
    if pricing_metal in ["Rose Gold", "White Gold", "Gold"]:
        pricing_metal = "Yellow Gold"

    rate_entry = frappe.db.get_value(
        "Gold Rate Log",
        {"metal": pricing_metal, "purity": item.custom_purity},
        "rate_per_gram",
        order_by="creation desc",
    )
    current_gold_rate = float(rate_entry) if rate_entry else 0.0

    net_weight = item.custom_net_weight_g or 0.0
    gold_value = net_weight * current_gold_rate

    # --- B. GEMSTONE VALUE 💎 ---
    stone_value = 0.0
    if hasattr(item, "gemstones") and item.gemstones:
        for stone in item.gemstones:
            stone_value += stone.amount or 0.0

    # --- C. MAKING CHARGES ---
    mc_value = item.custom_making_charge_value or 0.0
    making_charges = 0.0

    if item.custom_making_charge_type == "Fixed Amount":
        making_charges = mc_value
    elif item.custom_making_charge_type == "Percentage":
        making_charges = gold_value * (mc_value / 100)

    # --- D. TOTAL ---
    final_price = gold_value + making_charges + stone_value

    # DEBUG: Print to your terminal to confirm it works
    # print(f"💎 DEBUG: Item: {item_code} | Stone Value: {stone_value}")

    return {
        "item_code": item.name,
        # "item_name": item.item_name,
        "image": item.image,
        "metal": item.custom_metal_type,
        "purity": item.custom_purity,
        "gross_weight": item.custom_gross_weight_g,
        "net_weight": item.custom_net_weight_g,
        "stone_weight": item.custom_stone_weight_g,
        # 2. Pricing Details
        "gold_rate_used": current_gold_rate,
        "gold_value": round(gold_value, 2),
        "making_charges": round(making_charges, 2),
        "gemstone_value": round(stone_value, 2),
        "final_price": round(final_price, 2),
    }
