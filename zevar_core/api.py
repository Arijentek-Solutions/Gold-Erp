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
    start=0, page_length=20, warehouse=None, search_term=None, filters=None, in_stock_only=False, source_filter=None
):
    """
    Fetches items for the POS catalog with filtering, search, and pagination.

    Args:
        start: Starting index for pagination
        page_length: Number of items to return
        warehouse: Warehouse to check stock levels for
        search_term: Search term to filter item names
        filters: JSON string of additional filters (metal, purity, gemstone, jewelry_type, etc.)
        in_stock_only: If True, only return items with stock_qty > 0
        source_filter: Filter by custom_source (e.g., 'QGold', 'Stuller', 'JCSWIN')

    Returns:
        List of item dictionaries with stock and price information
    """
    # Base Filters
    query_filters = [["disabled", "=", 0], ["has_variants", "=", 0]]

    # Search Term
    if search_term:
        query_filters.append(["item_name", "like", f"%{search_term}%"])

    # Source filter
    if source_filter:
        query_filters.append(["custom_source", "=", source_filter])

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

            # Price range filter
            min_price = filters_dict.pop("min_price", None)
            max_price = filters_dict.pop("max_price", None)
            
            # Apply remaining filters (Metal, Purity, Jewelry Type, Gender, etc.)
            for key, value in filters_dict.items():
                if isinstance(value, list):
                    query_filters.append([key] + value)
                elif value:
                    query_filters.append([key, "=", value])

    # Fetch Items with all jewelry fields
    items = frappe.get_list(
        "Item",
        filters=query_filters,
        fields=[
            "name",
            "item_name",
            "item_group",
            "image",
            "description",
            # Original fields
            "custom_metal_type",
            "custom_purity",
            "custom_gross_weight_g",
            "custom_stone_weight_g",
            "custom_net_weight_g",
            "custom_making_charge_type",
            "custom_making_charge_value",
            # New classification fields
            "custom_product_type",
            "custom_jewelry_type",
            "custom_jewelry_subtype",
            "custom_material_color",
            "custom_finish",
            "custom_plating",
            # Dimensions
            "custom_length_value",
            "custom_length_unit",
            "custom_width_value",
            "custom_width_unit",
            "custom_size",
            # Chain/Clasp
            "custom_chain_type",
            "custom_clasp_type",
            "custom_chain_length",
            "custom_chain_width",
            # Vendor/Sourcing
            "custom_vendor_sku",
            "custom_vendor",
            "custom_country_of_origin",
            "custom_msrp",
            "custom_cost_price",
            "custom_source",
            # Additional
            "custom_gender",
            "custom_sold_by_unit",
            "custom_is_featured",
            "custom_is_trending",
        ],
        order_by="custom_is_featured desc, custom_is_trending desc, item_group asc, custom_net_weight_g desc",
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
            final_price = item.custom_msrp or 0.0

        # Apply price filter if specified
        if min_price and final_price < float(min_price):
            continue
        if max_price and final_price > float(max_price):
            continue
        
        # Apply stock filter if requested
        if in_stock_only and qty <= 0:
            continue

        pos_items.append(
            {
                "item_code": item.name,
                "item_name": item.item_name,
                "item_group": item.item_group,
                "image": item.image,
                "description": item.description,
                "stock_qty": qty,
                "price": final_price,
                "msrp": item.custom_msrp,
                # Metal/Material
                "metal": item.custom_metal_type,
                "purity": item.custom_purity,
                "material_color": item.custom_material_color,
                "finish": item.custom_finish,
                "plating": item.custom_plating,
                # Weights
                "gross_weight": item.custom_gross_weight_g,
                "stone_weight": item.custom_stone_weight_g,
                "net_weight": item.custom_net_weight_g,
                # Classification
                "product_type": item.custom_product_type,
                "jewelry_type": item.custom_jewelry_type,
                "jewelry_subtype": item.custom_jewelry_subtype,
                # Dimensions
                "length": f"{item.custom_length_value} {item.custom_length_unit}" if item.custom_length_value else None,
                "width": f"{item.custom_width_value} {item.custom_width_unit}" if item.custom_width_value else None,
                "size": item.custom_size,
                # Chain/Clasp
                "chain_type": item.custom_chain_type,
                "clasp_type": item.custom_clasp_type,
                # Vendor
                "vendor_sku": item.custom_vendor_sku,
                "vendor": item.custom_vendor,
                "country_of_origin": item.custom_country_of_origin,
                "custom_source": item.custom_source,
                # Flags
                "gender": item.custom_gender,
                "is_featured": item.custom_is_featured,
                "is_trending": item.custom_is_trending,
            }
        )

    return pos_items


@frappe.whitelist(allow_guest=True)
def get_catalog_filters():
    """
    Returns available filter options for the catalog UI.
    Dynamically generates options based on actual data in the system.
    
    Returns:
        Dictionary with filter options for each filterable field
    """
    filters = {}
    
    # Jewelry Types
    jewelry_types = frappe.db.sql_list("""
        SELECT DISTINCT custom_jewelry_type FROM `tabItem` 
        WHERE custom_jewelry_type IS NOT NULL AND custom_jewelry_type != ''
        ORDER BY custom_jewelry_type
    """)
    filters["jewelry_types"] = jewelry_types or ["Rings", "Chains", "Necklaces", "Earrings", "Bracelets", "Pendants", "Watches"]
    
    # Metal Types
    metal_types = frappe.db.sql_list("""
        SELECT DISTINCT custom_metal_type FROM `tabItem` 
        WHERE custom_metal_type IS NOT NULL AND custom_metal_type != ''
        ORDER BY custom_metal_type
    """)
    filters["metal_types"] = metal_types or ["Yellow Gold", "White Gold", "Rose Gold", "Platinum", "Silver"]
    
    # Purities
    purities = frappe.db.sql_list("""
        SELECT DISTINCT custom_purity FROM `tabItem` 
        WHERE custom_purity IS NOT NULL AND custom_purity != ''
        ORDER BY custom_purity
    """)
    filters["purities"] = purities or ["24 Karat", "22 Karat", "18 Karat", "14 Karat", "10 Karat", "925 Sterling"]
    
    # Material Colors
    material_colors = frappe.db.sql_list("""
        SELECT DISTINCT custom_material_color FROM `tabItem` 
        WHERE custom_material_color IS NOT NULL AND custom_material_color != ''
        ORDER BY custom_material_color
    """)
    filters["material_colors"] = material_colors or ["Yellow", "White", "Rose", "Two-Tone"]
    
    # Genders
    genders = frappe.db.sql_list("""
        SELECT DISTINCT custom_gender FROM `tabItem` 
        WHERE custom_gender IS NOT NULL AND custom_gender != ''
        ORDER BY custom_gender
    """)
    filters["genders"] = genders or ["Unisex", "Men's", "Women's"]
    
    # Countries of Origin
    countries = frappe.db.sql_list("""
        SELECT DISTINCT custom_country_of_origin FROM `tabItem` 
        WHERE custom_country_of_origin IS NOT NULL AND custom_country_of_origin != ''
        ORDER BY custom_country_of_origin
    """)
    filters["countries"] = countries
    
    # Finishes
    finishes = frappe.db.sql_list("""
        SELECT DISTINCT custom_finish FROM `tabItem` 
        WHERE custom_finish IS NOT NULL AND custom_finish != ''
        ORDER BY custom_finish
    """)
    filters["finishes"] = finishes or ["Polished", "Brushed", "Matte", "Satin"]
    
    # Chain Types (for chains/necklaces)
    chain_types = frappe.db.sql_list("""
        SELECT DISTINCT custom_chain_type FROM `tabItem` 
        WHERE custom_chain_type IS NOT NULL AND custom_chain_type != ''
        ORDER BY custom_chain_type
    """)
    filters["chain_types"] = chain_types
    
    # Clasp Types
    clasp_types = frappe.db.sql_list("""
        SELECT DISTINCT custom_clasp_type FROM `tabItem` 
        WHERE custom_clasp_type IS NOT NULL AND custom_clasp_type != ''
        ORDER BY custom_clasp_type
    """)
    filters["clasp_types"] = clasp_types
    
    # Item Groups
    item_groups = frappe.get_all(
        "Item Group",
        filters={"parent_item_group": ["in", ["Jewelry", "Watches", "All Item Groups"]]},
        pluck="name",
        order_by="name"
    )
    filters["item_groups"] = item_groups
    
    # Price ranges (predefined)
    filters["price_ranges"] = [
        {"label": "Under $100", "min": 0, "max": 100},
        {"label": "$100 - $500", "min": 100, "max": 500},
        {"label": "$500 - $1,000", "min": 500, "max": 1000},
        {"label": "$1,000 - $5,000", "min": 1000, "max": 5000},
        {"label": "$5,000 - $10,000", "min": 5000, "max": 10000},
        {"label": "Over $10,000", "min": 10000, "max": None},
    ]
    
    # Gemstone Types from the attribute
    try:
        stone_types = frappe.get_all(
            "Item Attribute Value",
            filters={"parent": "Stone Type"},
            pluck="attribute_value"
        )
        filters["gemstone_types"] = ["No Stone"] + stone_types
    except:
        filters["gemstone_types"] = ["No Stone", "Diamond", "Ruby", "Emerald", "Sapphire", "Cubic Zirconia"]
    
    return {
        "status": "success",
        "filters": filters
    }


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
    Unified price calculation for items - used by both POS and Catalog.
    
    US Market Pricing Logic:
    1. If MSRP is set, use it as the final price
    2. Otherwise, calculate from gold value + gemstone value
    3. No making charges for US market
    
    Price auto-updates based on daily gold rate in Gold Rate Log.

    Args:
        item_code: The unique identifier of the item

    Returns:
        Dictionary with complete price breakdown and item details
    """
    item = frappe.get_doc("Item", item_code)
    if not item:
        return {}

    # =========================================================================
    # GOLD VALUE CALCULATION (for informational purposes & fallback pricing)
    # =========================================================================
    pricing_metal = item.custom_metal_type
    if pricing_metal in ["Rose Gold", "White Gold"]:
        pricing_metal = "Yellow Gold"

    # Get latest gold rate from Gold Rate Log
    rate_entry = frappe.db.get_value(
        "Gold Rate Log",
        {"metal": pricing_metal, "purity": item.custom_purity},
        "rate_per_gram",
        order_by="creation desc",
    )

    current_gold_rate = float(rate_entry) if rate_entry else 0.0
    net_weight = item.custom_net_weight_g or 0.0
    gold_value = net_weight * current_gold_rate

    # =========================================================================
    # GEMSTONE VALUE CALCULATION
    # =========================================================================
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

    # =========================================================================
    # FINAL PRICE CALCULATION (US Market - No Making Charges)
    # =========================================================================
    # Priority 1: Use MSRP if available
    # Priority 2: Calculate from gold value + gemstone value
    calculated_price = gold_value + stone_value
    msrp = item.custom_msrp or 0.0
    
    if msrp > 0:
        final_price = msrp
        price_source = "MSRP"
    elif calculated_price > 0:
        final_price = calculated_price
        price_source = "Calculated"
    else:
        # Fallback to standard rate if nothing else
        final_price = item.standard_rate or 0.0
        price_source = "Standard Rate"

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
        "gemstone_value": round(stone_value, 2),
        "calculated_price": round(calculated_price, 2),  # For reference
        "msrp": round(msrp, 2),
        "final_price": round(final_price, 2),
        "price_source": price_source,  # "MSRP", "Calculated", or "Standard Rate"
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
    Fetches POS settings like Tax Rate, Currency, and Payment Options.

    Args:
        warehouse: Optional warehouse to determine tax rate by location

    Returns:
        Dictionary with POS configuration including:
        - tax_rate: Default tax rate for location
        - tax_exempt_available: Whether no-tax option is available
        - payment_modes: Available payment methods
        - payment_split_enabled: Whether split payments are allowed
        - currency, company, allow_discount
    """
    tax_rate = 0.0
    currency = "USD"

    # Location-based tax rates
    if warehouse and "Miami" in warehouse:
        tax_rate = 7.00
    elif warehouse and "Los Angeles" in warehouse:
        tax_rate = 9.50
    else:
        tax_rate = 8.875  # Default (NY)

    # Available payment modes
    payment_modes = [
        {"mode": "Cash", "type": "Cash"},
        {"mode": "Credit Card", "type": "Bank"},
        {"mode": "Debit Card", "type": "Bank"},
        {"mode": "Check", "type": "Bank"},
        {"mode": "Wire Transfer", "type": "Bank"},
        {"mode": "Zelle", "type": "Bank"},
    ]

    return {
        "tax_rate": tax_rate,
        "tax_exempt_available": True,  # Allow no-tax toggle for US market
        "currency": currency,
        "allow_discount": 1,
        "company": frappe.defaults.get_user_default("Company") or "Zevar Jewelers",
        "payment_modes": payment_modes,
        "payment_split_enabled": True,  # Allow splitting payment across multiple modes
        "max_split_payments": 3,  # Maximum number of payment splits
    }


@frappe.whitelist()
def calculate_invoice_totals(items, tax_exempt=False, discount_amount=0, warehouse=None):
    """
    Calculate invoice totals with optional tax exemption.
    
    Args:
        items: List of items [{item_code, qty, rate}]
        tax_exempt: If True, no tax is applied (for resellers, etc.)
        discount_amount: Discount to apply
        warehouse: For location-based tax rate
    
    Returns:
        Dictionary with subtotal, tax, discount, and grand total
    """
    if isinstance(items, str):
        items = json.loads(items)
    
    subtotal = 0.0
    for item in items:
        qty = item.get("qty", 1)
        rate = item.get("rate", 0)
        subtotal += qty * rate
    
    # Apply discount
    subtotal_after_discount = subtotal - float(discount_amount or 0)
    
    # Calculate tax (unless exempt)
    tax_rate = 0.0
    if not tax_exempt:
        settings = get_pos_settings(warehouse)
        tax_rate = settings.get("tax_rate", 0)
    
    tax_amount = subtotal_after_discount * (tax_rate / 100)
    grand_total = subtotal_after_discount + tax_amount
    
    return {
        "subtotal": round(subtotal, 2),
        "discount": round(float(discount_amount or 0), 2),
        "subtotal_after_discount": round(subtotal_after_discount, 2),
        "tax_rate": tax_rate,
        "tax_exempt": tax_exempt,
        "tax_amount": round(tax_amount, 2),
        "grand_total": round(grand_total, 2),
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


# =============================================================================
# TRENDING ITEMS (Catalogue Dashboard)
# =============================================================================


@frappe.whitelist(allow_guest=True)
def get_trending_items(category=None, limit=20):
    """
    Fetches active trending items from the Item Master.
    Uses custom_is_trending flag or falls back to most viewed/recent.
    """
    filters = [["disabled", "=", 0], ["has_variants", "=", 0]]
    
    # 1. Try to find explicit trending items
    filters.append(["custom_is_trending", "=", 1])

    # Category filter
    if category and category.lower() not in ['all', '']:
        # Map frontend category IDs to Item Group or Jewelery Type
        cat_map = {
            'rings': 'Rings',
            'chains': 'Chains', 
            'earrings': 'Earrings',
            'bracelets': 'Bracelets',
            'pendants': 'Pendants',
            'watches': 'Watches'
        }
        mapped_cat = cat_map.get(category.lower())
        if mapped_cat:
            filters.append(["item_group", "=", mapped_cat])

    items = frappe.get_all(
        "Item",
        filters=filters,
        fields=[
            "name", "item_name", "item_group", "image", "description",
            "custom_msrp", "custom_jewelry_type", "custom_metal_type",
            "custom_is_featured", "custom_is_trending"
        ],
        order_by="custom_is_featured desc, creation desc",
        limit_page_length=int(limit)
    )

    # If no explicitly trending items, fallback to recent items
    if not items and (not category or category == 'all'):
        items = frappe.get_all(
            "Item",
            filters=[["disabled", "=", 0], ["has_variants", "=", 0], ["image", "is", "set"]],
            fields=[
                "name", "item_name", "item_group", "image", "description",
                "custom_msrp", "custom_jewelry_type", "custom_metal_type",
                "custom_is_featured", "custom_is_trending"
            ],
            order_by="creation desc",
            limit_page_length=int(limit)
        )

    # Format response
    result = []
    for item in items:
        # Calculate price (simplified for catalog listing, full calc in detail)
        price = item.custom_msrp or 0.0
        
        result.append({
            "id": item.name,
            "name": item.item_name,
            "item_code": item.name,
            "category": item.custom_jewelry_type or item.item_group,
            "categoryId": (item.custom_jewelry_type or "other").lower(),
            "image": item.image,
            "price": f"${price:,.2f}",
            "price_raw": price,
            "metal": item.custom_metal_type,
            "is_hot": item.custom_is_trending or item.custom_is_featured,
            "is_featured": item.custom_is_featured
        })

    return {
        "status": "success",
        "items": result,
        "count": len(result)
    }


@frappe.whitelist(allow_guest=True)
def track_trending_click(item_id):
    """
    Tracks when a trending item is clicked by a user.
    Updates view_count and last_clicked timestamp.
    
    Args:
        item_id: The Trending Item document name
    
    Returns:
        Success status
    """
    if not item_id:
        return {"status": "error", "message": "Item ID required"}
    
    try:
        if frappe.db.exists("Trending Item", item_id):
            frappe.db.set_value(
                "Trending Item", 
                item_id, 
                {
                    "view_count": frappe.db.get_value("Trending Item", item_id, "view_count") + 1,
                    "last_clicked": frappe.utils.now()
                },
                update_modified=False
            )
            frappe.db.commit()
            return {"status": "success"}
        else:
            return {"status": "error", "message": "Item not found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}