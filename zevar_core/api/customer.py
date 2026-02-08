"""
Customer API - Customer search and details
"""
import frappe


@frappe.whitelist()
def search_customers(query: str):
    """
    Search customers by name, phone, or email.
    
    Args:
        query: Search query string
    
    Returns:
        List of matching customers
    """
    if not query or len(query) < 2:
        return []
    
    query_lower = f"%{query.lower()}%"
    
    customers = frappe.db.sql("""
        SELECT 
            name as customer_name,
            customer_name as display_name,
            mobile_no,
            email_id,
            customer_group,
            territory
        FROM `tabCustomer`
        WHERE (
            LOWER(name) LIKE %(query)s
            OR LOWER(customer_name) LIKE %(query)s
            OR LOWER(mobile_no) LIKE %(query)s
            OR LOWER(email_id) LIKE %(query)s
        )
        AND disabled = 0
        ORDER BY customer_name
        LIMIT 20
    """, {"query": query_lower}, as_dict=True)
    
    return customers


@frappe.whitelist()
def get_customer_details(customer_name: str):
    """
    Fetch full customer details including preferences.
    
    Args:
        customer_name: Customer ID
    
    Returns:
        Customer details dictionary
    """
    customer = frappe.get_doc("Customer", customer_name)
    
    # Get recent purchase history
    recent_orders = frappe.get_all(
        "Sales Invoice",
        filters={"customer": customer_name, "docstatus": 1},
        fields=["name", "posting_date", "grand_total"],
        order_by="posting_date desc",
        limit=5
    )
    
    return {
        "customer_name": customer.name,
        "display_name": customer.customer_name,
        "mobile_no": customer.mobile_no,
        "email_id": customer.email_id,
        "customer_group": customer.customer_group,
        "territory": customer.territory,
        # Custom fields
        "spouse_name": customer.custom_spouse_name,
        "anniversary": customer.custom_anniversary,
        "ring_size": customer.custom_ring_size,
        "preferred_metal": customer.custom_preferred_metal,
        "preferred_purity": customer.custom_preferred_purity,
        "tax_exempt": customer.exempt_from_sales_tax,
        # Purchase history
        "recent_orders": recent_orders,
        "total_spent": sum(order.grand_total for order in recent_orders)
    }
