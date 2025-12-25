import frappe


@frappe.whitelist()
def get_item_price(item_code):
    """
    Calculates the live price of an item based on Gold Rate.
    Formula: (Net Weight * Current Gold Rate) + Making Charges
    """
    # 1. Fetch the Item
    if not item_code:
        return 0.0

    item = frappe.get_doc("Item", item_code)

    # Validation: Is this actually jewelry?
    if not item.custom_metal_type or not item.custom_purity:
        frappe.throw(f"Item {item_code} is missing Metal Type or Purity details.")

    # 2. Fetch the Latest Gold Rate
    # We look for the most recent log for this specific Metal & Purity
    rate_entry = frappe.db.get_value(
        "Gold Rate Log",
        {"metal": item.custom_metal_type, "purity": item.custom_purity},
        "rate_per_gram",
        order_by="timestamp desc",
    )

    if not rate_entry:
        frappe.throw(
            f"No Gold Rate found for {item.custom_metal_type} - {item.custom_purity}. Please add a rate in Gold Rate Log."
        )

    current_gold_rate = float(rate_entry)

    # 3. Calculate Gold Value
    # Note: Using the _g field names you confirmed
    net_weight = item.custom_net_weight_g or 0.0
    gold_value = net_weight * current_gold_rate

    # 4. Calculate Making Charges
    making_charges = 0.0
    mc_value = item.custom_making_charge_value or 0.0

    if item.custom_making_charge_type == "Fixed Amount":
        making_charges = mc_value
    elif item.custom_making_charge_type == "Percentage of Gold Value":
        making_charges = gold_value * (mc_value / 100)

    # 5. Final Price
    final_price = gold_value + making_charges

    return {
        "item": item_code,
        "gold_rate_used": current_gold_rate,
        "net_weight": net_weight,
        "gold_value": gold_value,
        "making_charges": making_charges,
        "final_price": final_price,
    }

@frappe.whitelist()
def get_pos_items(item_group=None):
    """
    Returns a list of items optimized for the POS Grid.
    Includes: Basic Info, Stock Levels, and Live Price.
    """
    # 1. Base Filters: Only show items that are 'Jewelry' (have a metal type)
    filters = {
        "custom_metal_type": ["is", "set"],
        "disabled": 0
    }
    if item_group:
        filters["item_group"] = item_group

    # 2. Fetch Basic Data
    items = frappe.get_list("Item",
        filters=filters,
        fields=["name", "item_name", "item_group", "image", "custom_metal_type", "custom_purity", "custom_gross_weight_g"]
    )

    pos_items = []
    
    # 3. Enhance with Live Price & Stock
    # Note: For MVP we loop. For production with 10k items, we will optimize this later.
    for item in items:
        # Get Stock Quantity
        bin_qty = frappe.db.get_value("Bin", {"item_code": item.name}, "actual_qty") or 0
        
        # Get Live Price (Re-using your logic from Day 3!)
        # We wrap in try/except so one bad item doesn't crash the whole POS
        try:
            price_data = get_item_price(item.name)
            final_price = price_data.get("final_price")
        except Exception:
            final_price = 0.0

        pos_items.append({
            "item_code": item.name,
            "item_name": item.item_name,
            "item_group": item.item_group,
            "image": item.image,
            "stock_qty": bin_qty,
            "currency": "USD", # Or fetch from settings
            "price": final_price,
            "metal": item.custom_metal_type,
            "purity": item.custom_purity
        })

    return pos_items

@frappe.whitelist()
def create_pos_invoice(customer, items, payments):
    """
    Receives the cart from Frontend and creates the transaction.
    """
    import json
    
    # 1. Parse Data (Frontend sends JSON strings usually)
    if isinstance(items, str):
        items = json.loads(items)
    if isinstance(payments, str):
        payments = json.loads(payments)

    # 2. Basic Validation
    if not customer:
        frappe.throw("Customer is required")
    if not items:
        frappe.throw("Cart is empty")

    # 3. TODO: Next Sprint - Create Sales Invoice logic here.
    # For now, we just return success to unblock the frontend dev.
    
    return {
        "status": "success",
        "message": "Order Received (Backend Logic Pending)",
        "invoice_name": "TBD-12345"
    }

