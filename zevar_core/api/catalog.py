"""
Catalog API - Item retrieval and filtering
"""
import frappe
from zevar_core.constants import DEFAULT_PAGE_LENGTH, PARTNER_SOURCES


@frappe.whitelist()
def get_pos_items(start=0, page_length=DEFAULT_PAGE_LENGTH, warehouse=None, 
                  search_term=None, filters=None, in_stock_only=False, out_of_stock_only=False, source_filter=None):
    """
    Fetch items for POS catalog with filtering, search, and pagination.
    
    Args:
        start: Starting index for pagination
        page_length: Number of items to return
        warehouse: Warehouse to check stock levels
        search_term: Search term to filter item names
        filters: JSON string of additional filters
        in_stock_only: Only return items with stock_qty > 0
        out_of_stock_only: Only return items with stock_qty <= 0
        source_filter: Filter by custom_source
    
    Returns:
        List of item dictionaries with stock and price information
    """
    from zevar_core.api.pricing import get_item_price
    
    # Convert string booleans from frontend
    in_stock_only = in_stock_only in (True, 'true', '1', 1)
    out_of_stock_only = out_of_stock_only in (True, 'true', '1', 1)
    
    # Build filters
    query_filters = [["disabled", "=", 0], ["has_variants", "=", 0]]
    
    if search_term:
        query_filters.append(["item_name", "like", f"%{search_term}%"])
    
    if source_filter:
        query_filters.append(["custom_source", "=", source_filter])
    
    # Parse additional filters
    min_price = None
    max_price = None
    
    if filters:
        filters_dict = frappe.parse_json(filters)
        if isinstance(filters_dict, dict):
            # Handle gemstone filter
            gem_filter = filters_dict.pop("custom_gemstone", None)
            if gem_filter:
                if gem_filter == "No Stone":
                    items_with_stones = frappe.get_all("Zevar Gemstone Detail", pluck="parent")
                    if items_with_stones:
                        query_filters.append(["name", "not in", items_with_stones])
                else:
                    matching_items = frappe.get_all(
                        "Zevar Gemstone Detail",
                        filters={"gem_type": gem_filter},
                        pluck="parent"
                    )
                    if not matching_items:
                        return []
                    query_filters.append(["name", "in", matching_items])
            
            # Price range
            min_price = filters_dict.pop("min_price", None)
            max_price = filters_dict.pop("max_price", None)
            
            # Apply remaining filters
            for key, value in filters_dict.items():
                if value:
                    if isinstance(value, list) and len(value) == 2 and value[0] == 'like':
                        # Handle 'like' operator: ["like", "%Gold%"]
                        query_filters.append([key, "like", value[1]])
                    elif isinstance(value, list):
                        # Handle array of values: ["14K", "18K"] -> IN filter
                        query_filters.append([key, "in", value])
                    else:
                        query_filters.append([key, "=", value])
    
    # When stock or price filters are active, overfetch to compensate for post-query filtering
    has_post_filters = in_stock_only or out_of_stock_only or min_price or max_price
    fetch_length = int(page_length) * 5 if has_post_filters else int(page_length)
    
    # Fetch items
    items = frappe.get_list(
        "Item",
        filters=query_filters,
        fields=_get_item_fields(),
        order_by="custom_is_featured desc, custom_is_trending desc, item_group asc",
        start=int(start),
        page_length=fetch_length
    )
    
    if not items:
        return []
    
    # Fetch stock (aggregate across all warehouses if none specified)
    item_codes = [item.name for item in items]
    stock_map = {}
    
    if warehouse:
        bin_entries = frappe.db.get_all(
            "Bin",
            filters={"item_code": ["in", item_codes], "warehouse": warehouse},
            fields=["item_code", "actual_qty"]
        )
        stock_map = {b.item_code: b.actual_qty for b in bin_entries}
    else:
        # Sum stock across all warehouses
        bin_entries = frappe.db.sql("""
            SELECT item_code, SUM(actual_qty) as total_qty
            FROM `tabBin`
            WHERE item_code IN %s AND actual_qty > 0
            GROUP BY item_code
        """, (item_codes,), as_dict=True) if item_codes else []
        stock_map = {b.item_code: b.total_qty for b in bin_entries}
    
    # Build response
    pos_items = []
    for item in items:
        qty = stock_map.get(item.name, 0)
        
        # Get price
        try:
            price_data = get_item_price(item.name)
            final_price = price_data.get("final_price", 0.0)
        except Exception:
            final_price = item.custom_msrp or 0.0
        
        # Apply price filter
        if min_price and final_price < float(min_price):
            continue
        if max_price and final_price > float(max_price):
            continue
        
        # Apply stock filters
        if in_stock_only and qty <= 0:
            continue
        if out_of_stock_only and qty > 0:
            continue
        
        
        pos_items.append(_build_item_dict(item, qty, final_price))
    
    # Sort: In-stock items first, then out-of-stock
    pos_items.sort(key=lambda x: (x['stock_qty'] <= 0, -x['stock_qty']))
    
    return pos_items


@frappe.whitelist(allow_guest=True)
def get_catalog_filters():
    """Return available filter options for catalog UI."""
    filters = {}
    
    # Jewelry Types
    jewelry_types = frappe.db.sql_list("""
        SELECT DISTINCT custom_jewelry_type FROM `tabItem` 
        WHERE custom_jewelry_type IS NOT NULL AND custom_jewelry_type != ''
        ORDER BY custom_jewelry_type
    """)
    filters["jewelry_types"] = jewelry_types or ["Rings", "Chains", "Necklaces"]
    
    # Metals
    metals = frappe.db.sql_list("""
        SELECT DISTINCT custom_metal_type FROM `tabItem` 
        WHERE custom_metal_type IS NOT NULL
        ORDER BY custom_metal_type
    """)
    filters["metals"] = metals or ["Yellow Gold", "White Gold"]
    
    # Purities
    purities = frappe.db.sql_list("""
        SELECT DISTINCT custom_purity FROM `tabItem` 
        WHERE custom_purity IS NOT NULL
        ORDER BY custom_purity
    """)
    filters["purities"] = purities or ["14K", "18K"]
    
    # Gemstones
    gemstones = frappe.db.sql_list("""
        SELECT DISTINCT gem_type FROM `tabZevar Gemstone Detail`
        ORDER BY gem_type
    """)
    gemstones.insert(0, "No Stone")
    filters["gemstones"] = gemstones
    
    # Gender
    filters["genders"] = ["Unisex", "Men's", "Women's"]
    
    # Price range
    price_range = frappe.db.sql("""
        SELECT MIN(custom_msrp) as min_price, MAX(custom_msrp) as max_price
        FROM `tabItem`
        WHERE custom_msrp > 0
    """, as_dict=True)
    
    if price_range:
        filters["price_range"] = {
            "min": price_range[0].min_price or 0,
            "max": price_range[0].max_price or 10000
        }
    
    return filters


@frappe.whitelist()
def get_item_details(item_code):
    """Fetch full item details including gemstones and all product attributes."""
    from zevar_core.api.pricing import get_item_price
    
    item = frappe.get_doc("Item", item_code)
    
    # Get gemstones
    gemstones = []
    if hasattr(item, 'gemstones'):
        for gem in item.gemstones:
            gemstones.append({
                "gem_type": gem.gem_type,
                "carat": gem.carat,
                "count": gem.count,
                "cut": gem.cut,
                "color": gem.color,
                "clarity": gem.clarity,
                "rate": gem.rate,
                "amount": gem.amount
            })
    
    # Get price
    try:
        price_data = get_item_price(item_code)
        price = price_data.get("final_price", item.custom_msrp or 0)
    except Exception:
        price = item.custom_msrp or 0
    
    return {
        "item_code": item.name,
        "item_name": item.item_name,
        "description": item.description,
        "image": item.image,
        "metal": item.custom_metal_type,
        "purity": item.custom_purity,
        "gross_weight": item.custom_gross_weight_g,
        "stone_weight": item.custom_stone_weight_g,
        "net_weight": item.custom_net_weight_g,
        "product_type": item.custom_product_type,
        "jewelry_type": item.custom_jewelry_type,
        "jewelry_subtype": item.custom_jewelry_subtype,
        "material_color": item.custom_material_color,
        "finish": item.custom_finish,
        "plating": item.custom_plating,
        "length": f"{item.custom_length_value} {item.custom_length_unit}" if item.custom_length_value else None,
        "width": f"{item.custom_width_value} {item.custom_width_unit}" if item.custom_width_value else None,
        "size": item.custom_size,
        "chain_type": item.custom_chain_type,
        "clasp_type": item.custom_clasp_type,
        "gender": item.custom_gender,
        "completeness": "Complete (all stones included)" if item.custom_product_type else None,
        "country_of_origin": item.custom_country_of_origin,
        "gemstones": gemstones,
        "custom_source": item.custom_source,
        "price": price,
        "msrp": item.custom_msrp
    }


def _get_item_fields():
    """Return list of fields to fetch for items."""
    return [
        "name", "item_name", "item_group", "image", "description",
        "custom_metal_type", "custom_purity",
        "custom_gross_weight_g", "custom_stone_weight_g", "custom_net_weight_g",
        "custom_product_type", "custom_jewelry_type", "custom_jewelry_subtype",
        "custom_material_color", "custom_finish", "custom_plating",
        "custom_length_value", "custom_length_unit",
        "custom_width_value", "custom_width_unit", "custom_size",
        "custom_chain_type", "custom_clasp_type",
        "custom_vendor_sku", "custom_vendor", "custom_country_of_origin",
        "custom_msrp", "custom_cost_price", "custom_source",
        "custom_gender", "custom_is_featured", "custom_is_trending"
    ]


def _build_item_dict(item, qty, final_price):
    """Build item dictionary for API response."""
    return {
        "item_code": item.name,
        "item_name": item.item_name,
        "item_group": item.item_group,
        "image": item.image,
        "description": item.description,
        "stock_qty": qty,
        "price": final_price,
        "msrp": item.custom_msrp,
        "metal": item.custom_metal_type,
        "purity": item.custom_purity,
        "material_color": item.custom_material_color,
        "finish": item.custom_finish,
        "plating": item.custom_plating,
        "gross_weight": item.custom_gross_weight_g,
        "stone_weight": item.custom_stone_weight_g,
        "net_weight": item.custom_net_weight_g,
        "product_type": item.custom_product_type,
        "jewelry_type": item.custom_jewelry_type,
        "jewelry_subtype": item.custom_jewelry_subtype,
        "length": f"{item.custom_length_value} {item.custom_length_unit}" if item.custom_length_value else None,
        "width": f"{item.custom_width_value} {item.custom_width_unit}" if item.custom_width_value else None,
        "size": item.custom_size,
        "chain_type": item.custom_chain_type,
        "clasp_type": item.custom_clasp_type,
        "vendor_sku": item.custom_vendor_sku,
        "vendor": item.custom_vendor,
        "country_of_origin": item.custom_country_of_origin,
        "custom_source": item.custom_source,
        "gender": item.custom_gender,
        "is_featured": item.custom_is_featured,
        "is_trending": item.custom_is_trending
    }
