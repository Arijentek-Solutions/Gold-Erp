"""
POS API - Invoice creation and settings
"""
import frappe
from zevar_core.constants import DEFAULT_TAX_RATES, PAYMENT_MODES


@frappe.whitelist()
def create_pos_invoice(items: str, payments: str, customer: str = None, discount_amount: float = 0):
    """
    Create POS Invoice.
    
    Args:
        items: JSON string of items [{item_code, qty, rate}]
        payments: JSON string of payments [{mode, amount}]
        customer: Customer name (default: Walk-In Customer)
        discount_amount: Discount amount
    
    Returns:
        Invoice details
    """
    items_list = frappe.parse_json(items) if isinstance(items, str) else items
    payments_list = frappe.parse_json(payments) if isinstance(payments, str) else payments
    
    if not customer:
        customer = "Walk-In Customer"
    
    # TODO: Implement actual POS Invoice creation
    # This is currently a stub
    
    return {
        "success": True,
        "message": "Invoice queued for creation",
        "items": items_list,
        "payments": payments_list,
        "customer": customer,
        "discount_amount": discount_amount
    }


@frappe.whitelist()
def get_pos_settings(warehouse: str = None):
    """
    Fetch POS settings including tax rates and payment modes.
    
    Args:
        warehouse: Warehouse name to determine tax rate by location
    
    Returns:
        POS settings dictionary
    """
    # Determine tax rate based on warehouse location
    tax_rate = 0.0
    if warehouse:
        # Simple location detection (enhance with actual warehouse location field)
        warehouse_lower = warehouse.lower()
        for location, rate in DEFAULT_TAX_RATES.items():
            if location.lower() in warehouse_lower:
                tax_rate = rate
                break
    
    # Default company
    company = frappe.defaults.get_user_default("Company") or frappe.db.get_single_value("Global Defaults", "default_company")
    
    return {
        "tax_rate": tax_rate,
        "currency": "USD",
        "company": company,
        "payment_modes": PAYMENT_MODES
    }


@frappe.whitelist()
def calculate_invoice_totals(items: str, tax_exempt: bool = False, discount_amount: float = 0, warehouse: str = None):
    """
    Calculate invoice totals.
    
    Args:
        items: JSON string of items [{item_code, qty, rate}]
        tax_exempt: Whether customer is tax exempt
        discount_amount: Discount amount to apply
        warehouse: Warehouse for tax rate determination
    
    Returns:
        Totals dictionary
    """
    items_list = frappe.parse_json(items) if isinstance(items, str) else items
    
    # Calculate subtotal
    subtotal = sum(float(item.get("rate", 0)) * int(item.get("qty", 1)) for item in items_list)
    
    # Apply discount
    discount = float(discount_amount)
    subtotal_after_discount = subtotal - discount
    
    # Calculate tax
    tax = 0.0
    if not tax_exempt:
        settings = get_pos_settings(warehouse)
        tax_rate = settings.get("tax_rate", 0)
        tax = (subtotal_after_discount * tax_rate) / 100
    
    # Grand total
    grand_total = subtotal_after_discount + tax
    
    return {
        "subtotal": subtotal,
        "discount": discount,
        "subtotal_after_discount": subtotal_after_discount,
        "tax": tax,
        "grand_total": grand_total
    }
