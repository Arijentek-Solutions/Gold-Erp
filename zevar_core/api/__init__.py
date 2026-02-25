"""
Zevar Core API Module

Centralized API endpoints for the Zevar POS system.
Organized into logical submodules for maintainability.
"""

# Import all API functions to maintain backward compatibility
from zevar_core.api.catalog import get_catalog_filters, get_item_details, get_pos_items
from zevar_core.api.customer import get_customer_details, search_customers
from zevar_core.api.item_entry import get_next_vendor_sku, quick_add_item
from zevar_core.api.pos import calculate_invoice_totals, create_pos_invoice, get_pos_settings
from zevar_core.api.pricing import get_item_price, refresh_gold_rates
from zevar_core.api.repair import (
	create_repair_order,
	get_customer_repair_history,
	get_repair_order_details,
	get_repair_orders,
	get_repair_receipt_html,
	get_repair_stats,
	get_repair_types,
	update_repair_status,
)
from zevar_core.api.trending import get_trending_items, track_trending_click

__all__ = [
	"calculate_invoice_totals",
	"create_pos_invoice",
	"create_repair_order",
	"get_catalog_filters",
	"get_customer_details",
	"get_customer_repair_history",
	"get_item_details",
	"get_item_price",
	"get_next_vendor_sku",
	"get_pos_items",
	"get_pos_settings",
	"get_repair_order_details",
	"get_repair_orders",
	"get_repair_receipt_html",
	"get_repair_stats",
	"get_repair_types",
	"get_trending_items",
	"quick_add_item",
	"refresh_gold_rates",
	"search_customers",
	"track_trending_click",
	"update_repair_status",
]
