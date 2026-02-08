"""
Zevar Core API Module

Centralized API endpoints for the Zevar POS system.
Organized into logical submodules for maintainability.
"""

# Import all API functions to maintain backward compatibility
from zevar_core.api.catalog import (
    get_pos_items,
    get_catalog_filters,
    get_item_details
)

from zevar_core.api.pricing import (
    get_item_price,
    refresh_gold_rates
)

from zevar_core.api.pos import (
    create_pos_invoice,
    get_pos_settings,
    calculate_invoice_totals
)

from zevar_core.api.customer import (
    search_customers,
    get_customer_details
)

from zevar_core.api.trending import (
    get_trending_items,
    track_trending_click
)

__all__ = [
    # Catalog
    'get_pos_items',
    'get_catalog_filters',
    'get_item_details',
    # Pricing
    'get_item_price',
    'refresh_gold_rates',
    # POS
    'create_pos_invoice',
    'get_pos_settings',
    'calculate_invoice_totals',
    # Customer
    'search_customers',
    'get_customer_details',
    # Trending
    'get_trending_items',
    'track_trending_click',
]
