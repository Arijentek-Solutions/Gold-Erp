"""
Trending Items API - Trending and featured items
"""
import frappe


@frappe.whitelist(allow_guest=True)
def get_trending_items(category: str = None, limit: int = 20):
    """
    Fetch trending items for catalog display.
    
    Args:
        category: Filter by jewelry category
        limit: Maximum number of items to return
    
    Returns:
        List of trending items
    """
    filters = {"is_active": 1}
    
    if category and category != "all":
        filters["category"] = category
    
    # Try to get from Trending Item DocType
    trending = frappe.get_all(
        "Trending Item",
        filters=filters,
        fields=[
            "name", "item_name", "category", "partner",
            "price", "is_hot", "product_url", "image_url",
            "view_count", "last_clicked"
        ],
        order_by="is_hot desc, view_count desc, last_clicked desc",
        limit=limit
    )
    
    # If no trending items, fallback to recent/featured items
    if not trending:
        trending = _get_fallback_items(category, limit)
    
    return trending


@frappe.whitelist(allow_guest=True)
def track_trending_click(item_id: str):
    """
    Track click on trending item.
    
    Args:
        item_id: Trending Item ID
    
    Returns:
        Success status
    """
    try:
        doc = frappe.get_doc("Trending Item", item_id)
        doc.view_count = (doc.view_count or 0) + 1
        doc.last_clicked = frappe.utils.now()
        doc.save(ignore_permissions=True)
        frappe.db.commit()
        
        return {"success": True, "view_count": doc.view_count}
    except Exception as e:
        frappe.log_error(f"Failed to track trending click: {str(e)}")
        return {"success": False, "error": str(e)}


def _get_fallback_items(category: str = None, limit: int = 20):
    """Get fallback items when no trending items exist."""
    filters = {"disabled": 0, "has_variants": 0}
    
    if category and category != "all":
        filters["custom_jewelry_type"] = category
    
    items = frappe.get_all(
        "Item",
        filters=filters,
        fields=[
            "name as item_name",
            "item_name",
            "custom_jewelry_type as category",
            "custom_msrp as price",
            "image as image_url",
            "custom_is_featured as is_hot"
        ],
        order_by="custom_is_featured desc, modified desc",
        limit=limit
    )
    
    return items
