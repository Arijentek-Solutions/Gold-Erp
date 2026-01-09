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
    Calculates live price AND returns item details + gemstone breakdown.
    """
    # 1. Fetch Item Details
    item = frappe.get_doc("Item", item_code)
    if not item:
        return {}

    # --- A. METAL VALUE ---
    pricing_metal = item.custom_metal_type
    if pricing_metal in ["Rose Gold", "White Gold"]:
        pricing_metal = "Yellow Gold"  # Use Yellow Gold rate for variants

    rate_entry = frappe.db.get_value(
        "Gold Rate Log",
        {"metal": pricing_metal, "purity": item.custom_purity},
        "rate_per_gram",
        order_by="creation desc",
    )

    current_gold_rate = float(rate_entry) if rate_entry else 0.0
    net_weight = item.custom_net_weight_g or 0.0
    gold_value = net_weight * current_gold_rate

    # --- B. GEMSTONE VALUE & DETAILS ---
    stone_value = 0.0
    gemstones_list = []

    # Identify the correct child table (custom vs standard)
    table_field = None
    if hasattr(item, "custom_gemstones") and item.custom_gemstones:
        table_field = item.custom_gemstones
    elif hasattr(item, "gemstones") and item.gemstones:
        table_field = item.gemstones

    if table_field:
        for gem in table_field:
            # 1. Sum up value for price
            stone_value += gem.amount or 0.0

            # 2. Build list for UI Table
            gemstones_list.append(
                {
                    "gem_type": gem.gem_type,
                    "carat": gem.carat,
                    "count": gem.count or 1,
                    "cut": gem.cut,
                    "clarity": gem.clarity,
                    "color": gem.color,
                    "amount": gem.amount,
                }
            )

    # --- C. MAKING CHARGES ---
    mc_value = item.custom_making_charge_value or 0.0
    making_charges = 0.0

    if item.custom_making_charge_type == "Fixed Amount":
        making_charges = mc_value
    elif item.custom_making_charge_type == "Percentage":
        making_charges = gold_value * (mc_value / 100)

    # --- D. TOTAL ---
    final_price = gold_value + making_charges + stone_value

    return {
        # Basic Info
        "item_code": item.name,
        "item_name": item.item_name,  # Ensure title is returned
        "image": item.image,
        "metal": item.custom_metal_type,
        "purity": item.custom_purity,
        # Weights
        "gross_weight": item.custom_gross_weight_g,
        "net_weight": item.custom_net_weight_g,
        "stone_weight": item.custom_stone_weight_g,
        # Pricing Breakdown
        "gold_rate": current_gold_rate,
        "gold_value": round(gold_value, 2),
        "making_charges": round(making_charges, 2),
        "gemstone_value": round(stone_value, 2),
        "final_price": round(final_price, 2),
        # FIX: Return the list so the Modal Table works
        "gemstones": gemstones_list,
    }


import json

import frappe


@frappe.whitelist()
def get_pos_items(
    start=0, page_length=20, warehouse=None, search_term=None, filters=None
):
    # 1. Base Filters
    query_filters = [["disabled", "=", 0], ["has_variants", "=", 0]]

    # 2. Search Term
    if search_term:
        query_filters.append(["item_name", "like", f"%{search_term}%"])

    # 3. Dynamic Filters (With Gemstone Logic)
    if filters:
        filters_dict = frappe.parse_json(filters)
        if isinstance(filters_dict, dict):

            # --- GEMSTONE LOGIC START ---
            # We pop 'custom_gemstone' so it doesn't get added to the generic loop below
            gem_filter = filters_dict.pop("custom_gemstone", None)

            if gem_filter:
                if gem_filter == "No Stone":
                    # Find items that appear in the gemstone table
                    items_with_stones = frappe.get_all(
                        "Zevar Gemstone Detail", pluck="parent"
                    )
                    if items_with_stones:
                        query_filters.append(["name", "not in", items_with_stones])
                else:
                    # Find items that have this specific stone
                    # We query the Child Table "Zevar Gemstone Detail"
                    matching_items = frappe.get_all(
                        "Zevar Gemstone Detail",
                        filters={"gem_type": gem_filter},
                        pluck="parent",
                    )

                    if not matching_items:
                        # If no items match, force an empty result safely
                        return []

                    query_filters.append(["name", "in", matching_items])
            # --- GEMSTONE LOGIC END ---

            # Apply remaining filters (Metal, Purity, etc.)
            for key, value in filters_dict.items():
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
        order_by="item_group asc, custom_net_weight_g desc",
        start=start,
        page_length=page_length,
    )

    if not items:
        return []

    # 5. Fetch Stock & Calculate Price
    item_codes = [item.name for item in items]

    # ... (Rest of your existing stock/price logic remains exactly the same) ...

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

        # Get Price
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


# ... (Keep get_item_details, get_item_price, etc. exactly as they were) ...


@frappe.whitelist()
def create_pos_invoice(items, payments, customer=None, discount_amount=0):
    """
    Creates a POS Invoice in ERPNext.
    payload example:
    items = [{"item_code": "Y-24K-123", "qty": 1, "rate": 5000}]
    payments = [{"mode": "Cash", "amount": 5000}]
    """
    import json

    # 1. Parse JSON if it comes as a string (common in Frappe API calls)
    if isinstance(items, str):
        items = json.loads(items)
    if isinstance(payments, str):
        payments = json.loads(payments)

    # 2. Basic Validation
    if not items:
        frappe.throw("Cart is empty! Cannot process order.")

    if not payments:
        frappe.throw("No payment received.")

    # 3. Defaults
    if not customer:
        # Fetch the default 'Walk-In' customer from POS Profile (or hardcode for MVP)
        customer = "Walk-In Customer"

    # 4. (For Today) Return a success echo so we know the frontend connected.
    # Next week, we will replace this return with the actual Invoice Creation code.
    return {
        "status": "success",
        "message": "Payload Received",
        "data": {
            "customer": customer,
            "total_items": len(items),
            "total_paid": sum([p.get("amount", 0) for p in payments]),
        },
    }
