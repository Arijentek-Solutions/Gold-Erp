import json

import frappe


@frappe.whitelist()
def get_pos_items(
    start=0, page_length=20, warehouse=None, search_term=None, filters=None
):
    """
    Returns a paginated list of items with warehouse-specific stock.
    Supports complex filtering (Metal, Purity, Item Group).
    """

    # 1. Base Filters
    query_filters = [
        ["custom_metal_type", "is", "set"],
        ["disabled", "=", 0],
        ["has_variants", "=", 0],
    ]

    # 2. Apply Search Term
    if search_term:
        query_filters.append(["item_name", "like", f"%{search_term}%"])

    # 3. Apply Advanced Filters
    if filters:
        if isinstance(filters, str):
            try:
                filters = json.loads(filters)
            except json.JSONDecodeError:
                filters = {}

        if isinstance(filters, dict):
            for key, value in filters.items():
                if value:
                    query_filters.append([key, "=", value])

    # 4. Fetch Items
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
        start=start,
        page_length=page_length,
    )

    if not items:
        return []

    # 5. Batch Fetch Stock
    item_codes = [item.name for item in items]
    stock_map = {}

    if warehouse:
        bin_entries = frappe.db.get_all(
            "Bin",
            filters={"item_code": ["in", item_codes], "warehouse": warehouse},
            fields=["item_code", "actual_qty"],
        )
        stock_map = {b.item_code: b.actual_qty for b in bin_entries}

    # 6. Assemble Data
    pos_items = []
    for item in items:
        qty = stock_map.get(item.name, 0)

        # Calculate Price (Using the helper below)
        try:
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
    """
    Fetches detailed info for a single item, including a fresh price check.
    """
    if not item_code:
        return {}

    # 1. Fetch Basic Info
    item = frappe.get_doc("Item", item_code)

    # 2. Re-calculate Price
    price_data = get_item_price(item_code)

    return {
        "item_code": item.name,
        "item_name": item.item_name,
        "description": item.description,
        "image": item.image,
        "metal": item.custom_metal_type,
        "purity": item.custom_purity,
        # Weights
        "gross_weight": item.custom_gross_weight_g,
        "net_weight": item.custom_net_weight_g,
        "stone_weight": item.custom_stone_weight_g,
        # Pricing Breakdown
        "gold_rate": price_data.get("gold_rate_used", 0),
        "gold_value": price_data.get("gold_value", 0),
        "making_charges": price_data.get("making_charges", 0),
        "final_price": price_data.get("final_price", 0),
    }


@frappe.whitelist()
def get_item_price(item_code):
    """
    Calculates live price: (Gold Value) + (Making Charges) + (Gemstone Value).
    """
    if not item_code:
        return {}

    try:
        # Fetch the Item document
        item = frappe.get_doc("Item", item_code)
    except frappe.DoesNotExistError:
        return {"error": "Item not found"}

    # --- 1. METAL VALUE ---
    gross = item.custom_gross_weight_g or 0.0
    stone = item.custom_stone_weight_g or 0.0
    net_weight = item.custom_net_weight_g or (gross - stone)

    # Normalize Metal Type
    pricing_metal = item.custom_metal_type
    if pricing_metal in ["Rose Gold", "White Gold", "Gold"]:
        pricing_metal = "Yellow Gold"

    # Fetch Gold Rate
    rate_entry = frappe.db.get_value(
        "Gold Rate Log",
        {"metal": pricing_metal, "purity": item.custom_purity},
        "rate_per_gram",
        order_by="creation desc",
    )
    current_gold_rate = float(rate_entry) if rate_entry else 0.0
    gold_value = net_weight * current_gold_rate

    # --- 2. MAKING CHARGES ---
    mc_value = item.custom_making_charge_value or 0.0
    making_charges = 0.0

    if item.custom_making_charge_type == "Fixed Amount":
        making_charges = mc_value
    elif item.custom_making_charge_type == "Percentage":
        making_charges = gold_value * (mc_value / 100.0)

    # --- 3. GEMSTONE VALUE (Diamond Engine) 💎 ---
    gemstone_value = 0.0

    # We access 'custom_gemstones' because you added it via Customize Form
    if hasattr(item, "custom_gemstones") and item.custom_gemstones:
        for gem in item.custom_gemstones:
            # Formula: Carat * Rate
            # We use (gem.carat or 0) to prevent errors if field is empty
            qty = gem.carat or 0.0
            rate = gem.rate or 0.0
            gemstone_value += qty * rate

    # --- TOTAL ---
    final_price = gold_value + making_charges + gemstone_value

    return {
        "gold_rate_used": current_gold_rate,
        "gold_value": round(gold_value, 2),
        "making_charges": round(making_charges, 2),
        "gemstone_value": round(gemstone_value, 2),
        "final_price": round(final_price, 2),
    }
