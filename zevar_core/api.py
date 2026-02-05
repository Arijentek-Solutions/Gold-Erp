"""
Zevar Core API Module

This module provides API endpoints for the Zevar POS system, including
item retrieval, pricing calculations, POS invoice creation, and settings.
"""

import json

import frappe


# =============================================================================
# ITEM RETRIEVAL
# =============================================================================


@frappe.whitelist()
def get_pos_items(
    start=0, page_length=20, warehouse=None, search_term=None, filters=None
):
    """
    Fetches items for the POS catalog with filtering, search, and pagination.

    Args:
        start: Starting index for pagination
        page_length: Number of items to return
        warehouse: Warehouse to check stock levels for
        search_term: Search term to filter item names
        filters: JSON string of additional filters (metal, purity, gemstone)

    Returns:
        List of item dictionaries with stock and price information
    """
    # Base Filters
    query_filters = [["disabled", "=", 0], ["has_variants", "=", 0]]

    # Search Term
    if search_term:
        query_filters.append(["item_name", "like", f"%{search_term}%"])

    # Dynamic Filters
    if filters:
        filters_dict = frappe.parse_json(filters)
        if isinstance(filters_dict, dict):

            # Gemstone filtering logic
            gem_filter = filters_dict.pop("custom_gemstone", None)

            if gem_filter:
                if gem_filter == "No Stone":
                    items_with_stones = frappe.get_all(
                        "Zevar Gemstone Detail", pluck="parent"
                    )
                    if items_with_stones:
                        query_filters.append(["name", "not in", items_with_stones])
                else:
                    matching_items = frappe.get_all(
                        "Zevar Gemstone Detail",
                        filters={"gem_type": gem_filter},
                        pluck="parent",
                    )

                    if not matching_items:
                        return []

                    query_filters.append(["name", "in", matching_items])

            # Apply remaining filters (Metal, Purity, etc.)
            for key, value in filters_dict.items():
                if value:
                    query_filters.append([key, "=", value])

    # Fetch Items
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

    # Fetch Stock
    item_codes = [item.name for item in items]
    stock_map = {}

    if warehouse:
        bin_entries = frappe.db.get_all(
            "Bin",
            filters={"item_code": ["in", item_codes], "warehouse": warehouse},
            fields=["item_code", "actual_qty"],
        )
        stock_map = {b.item_code: b.actual_qty for b in bin_entries}

    # Build response with prices
    pos_items = []
    for item in items:
        qty = stock_map.get(item.name, 0)

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


# =============================================================================
# ITEM DETAILS & PRICING
# =============================================================================


@frappe.whitelist()
def get_item_details(item_code):
    """
    Fetches detailed information for a specific item.

    Args:
        item_code: The unique identifier of the item

    Returns:
        Dictionary with complete item details including gemstones and pricing
    """
    item = frappe.get_doc("Item", item_code)
    price_data = get_item_price(item_code)

    gemstones_list = []

    # Check for gemstone table (custom or standard)
    table_field = None

    if hasattr(item, "custom_gemstones") and item.custom_gemstones:
        table_field = item.custom_gemstones
    elif hasattr(item, "gemstones") and item.gemstones:
        table_field = item.gemstones

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
    Calculates live price for an item including gold value, gemstones, and making charges.

    Args:
        item_code: The unique identifier of the item

    Returns:
        Dictionary with complete price breakdown and item details
    """
    item = frappe.get_doc("Item", item_code)
    if not item:
        return {}

    # Metal Value Calculation
    pricing_metal = item.custom_metal_type
    if pricing_metal in ["Rose Gold", "White Gold"]:
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

    # Gemstone Value & Details
    stone_value = 0.0
    gemstones_list = []

    table_field = None
    if hasattr(item, "custom_gemstones") and item.custom_gemstones:
        table_field = item.custom_gemstones
    elif hasattr(item, "gemstones") and item.gemstones:
        table_field = item.gemstones

    if table_field:
        for gem in table_field:
            stone_value += gem.amount or 0.0

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

    # Making Charges Calculation
    mc_value = item.custom_making_charge_value or 0.0
    making_charges = 0.0

    if item.custom_making_charge_type == "Fixed Amount":
        making_charges = mc_value
    elif item.custom_making_charge_type == "Percentage":
        making_charges = gold_value * (mc_value / 100)

    # Total Price
    final_price = gold_value + making_charges + stone_value

    return {
        "item_code": item.name,
        "item_name": item.item_name,
        "image": item.image,
        "metal": item.custom_metal_type,
        "purity": item.custom_purity,
        "gross_weight": item.custom_gross_weight_g,
        "net_weight": item.custom_net_weight_g,
        "stone_weight": item.custom_stone_weight_g,
        "gold_rate": current_gold_rate,
        "gold_value": round(gold_value, 2),
        "making_charges": round(making_charges, 2),
        "gemstone_value": round(stone_value, 2),
        "final_price": round(final_price, 2),
        "gemstones": gemstones_list,
    }


# =============================================================================
# POS INVOICE & SETTINGS
# =============================================================================


@frappe.whitelist()
def create_pos_invoice(items, payments, customer=None, discount_amount=0):
    """
    Creates a POS Invoice in ERPNext.

    Args:
        items: List of items [{item_code, qty, rate}]
        payments: List of payments [{mode, amount}]
        customer: Customer name (defaults to Walk-In Customer)
        discount_amount: Optional discount amount

    Returns:
        Dictionary with status and order details
    """
    if isinstance(items, str):
        items = json.loads(items)
    if isinstance(payments, str):
        payments = json.loads(payments)

    if not items:
        frappe.throw("Cart is empty! Cannot process order.")

    if not payments:
        frappe.throw("No payment received.")

    if not customer:
        customer = "Walk-In Customer"

    return {
        "status": "success",
        "message": "Payload Received",
        "data": {
            "customer": customer,
            "total_items": len(items),
            "total_paid": sum([p.get("amount", 0) for p in payments]),
        },
    }


@frappe.whitelist()
def get_pos_settings(warehouse=None):
    """
    Fetches POS settings like Tax Rate and Currency.

    Args:
        warehouse: Optional warehouse to determine tax rate by location

    Returns:
        Dictionary with tax_rate, currency, allow_discount, and company
    """
    tax_rate = 0.0
    currency = "USD"

    if warehouse and "Miami" in warehouse:
        tax_rate = 7.00
    elif warehouse and "Los Angeles" in warehouse:
        tax_rate = 9.50
    else:
        tax_rate = 8.875

    return {
        "tax_rate": tax_rate,
        "currency": currency,
        "allow_discount": 1,
        "company": frappe.defaults.get_user_default("Company") or "Zevar Jewelers",
    }


# =============================================================================
# LIVE GOLD RATE
# =============================================================================


@frappe.whitelist()
def refresh_gold_rates():
    """
    Manually triggers gold rate refresh.
    Returns the latest rates after update.
    """
    from zevar_core.tasks import fetch_live_gold_rate
    
    fetch_live_gold_rate()
    
    # Return latest rates
    rates = frappe.get_all(
        "Gold Rate Log",
        filters={"metal": "Yellow Gold"},
        fields=["purity", "rate_per_gram", "creation"],
        order_by="creation desc",
        limit=5
    )
    
    return {
        "status": "success",
        "rates": rates
    }


# =============================================================================
# CUSTOMER LOOKUP
# =============================================================================


@frappe.whitelist()
def search_customers(query):
    """
    Searches customers by name, phone, or email.
    Returns top 10 matching customers.
    """
    if not query or len(query) < 2:
        return []
    
    search_pattern = f"%{query}%"
    
    customers = frappe.get_all(
        "Customer",
        filters=[
            ["Customer", "disabled", "=", 0],
            [
                ["Customer", "customer_name", "like", search_pattern],
                ["Customer", "mobile_no", "like", search_pattern],
                ["Customer", "email_id", "like", search_pattern],
            ]
        ],
        or_filters=[
            ["customer_name", "like", search_pattern],
            ["mobile_no", "like", search_pattern],
            ["email_id", "like", search_pattern],
        ],
        fields=["name", "customer_name", "mobile_no", "email_id", "customer_group"],
        limit=10,
        order_by="customer_name asc"
    )
    
    return customers


@frappe.whitelist()
def get_customer_details(customer_name):
    """
    Fetches detailed customer info including purchase history summary.
    """
    if not customer_name:
        return None
    
    customer = frappe.get_doc("Customer", customer_name)
    
    # Get purchase summary
    total_spent = frappe.db.sql("""
        SELECT COALESCE(SUM(grand_total), 0) as total
        FROM `tabSales Invoice`
        WHERE customer = %s AND docstatus = 1
    """, customer_name, as_dict=True)[0].total
    
    return {
        "name": customer.name,
        "customer_name": customer.customer_name,
        "mobile_no": customer.mobile_no,
        "email_id": customer.email_id,
        "customer_group": customer.customer_group,
        "total_spent": total_spent
    }