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
