"""
Zevar Core API Module

Centralized API endpoints for the Zevar POS system.
Organized into logical submodules for maintainability.
"""

# Import all API functions to maintain backward compatibility
from zevar_core.api.attendance import (
	clock_in,
	clock_out,
	get_attendance_history,
	get_current_employee,
	get_employee_roster,
	get_today_checkin_status,
)
from zevar_core.api.catalog import get_catalog_filters, get_item_details, get_pos_items
from zevar_core.api.customer import get_customer_details, quick_create_customer, search_customers
from zevar_core.api.helpdesk import (
	add_ticket_reply,
	create_attendance_issue,
	get_employee_tickets,
	get_issue_types,
	get_ticket_details,
	get_ticket_stats,
)
from zevar_core.api.item_entry import get_next_vendor_sku, quick_add_item
from zevar_core.api.payroll import get_payroll_summary, get_salary_slip_details, get_salary_slips
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
from zevar_core.api.tasks import (
	create_personal_todo,
	delete_todo,
	get_employee_tasks,
	get_personal_todos,
	get_recent_activities,
	get_task_stats,
	update_todo_status,
)
from zevar_core.api.pos_profile import (
	get_active_profile,
	get_pos_profiles,
	get_profile_items,
	get_profile_payments,
	set_active_profile,
)
from zevar_core.api.pos_session import (
	close_pos_session,
	get_session_sales,
	get_session_status,
	list_user_sessions,
	open_pos_session,
)
from zevar_core.api.quick_layaway import (
	create_quick_layaway,
	get_layaway_preview,
	get_quick_layaway_defaults,
	validate_item_for_layaway,
)
from zevar_core.api.sales_history import (
	get_customer_purchase_history,
	get_sales_history,
	get_sales_summary,
	get_transaction_details,
	get_customer_purchase_history,
	void_transaction,
)
from zevar_core.api.trending import get_trending_items, track_trending_click

__all__ = [
	"add_ticket_reply",
	"calculate_invoice_totals",
	"clock_in",
	"clock_out",
	"close_pos_session",
	"create_attendance_issue",
	"create_personal_todo",
	"create_pos_invoice",
	"create_quick_layaway",
	"create_repair_order",
	"delete_todo",
	"get_active_profile",
	"get_attendance_history",
	"get_catalog_filters",
	"get_current_employee",
	"get_customer_details",
	"get_customer_repair_history",
	"get_employee_roster",
	"get_employee_tasks",
	"get_employee_tickets",
	"get_issue_types",
	"get_item_details",
	"get_item_price",
	"get_layaway_preview",
	"get_next_vendor_sku",
	"get_payroll_summary",
	"get_personal_todos",
	"get_pos_items",
	"get_pos_profiles",
	"get_pos_settings",
	"get_profile_items",
	"get_profile_payments",
	"get_quick_layaway_defaults",
	"get_recent_activities",
	"get_repair_order_details",
	"get_repair_orders",
	"get_repair_receipt_html",
	"get_repair_stats",
	"get_repair_types",
	"get_salary_slip_details",
	"get_salary_slips",
	"get_sales_history",
	"get_sales_summary",
	"get_session_sales",
	"get_session_status",
	"get_task_stats",
	"get_ticket_details",
	"get_ticket_stats",
	"get_today_checkin_status",
	"get_transaction_details",
	"get_trending_items",
	"list_user_sessions",
	"open_pos_session",
	"quick_add_item",
	"quick_create_customer",
	"refresh_gold_rates",
	"search_customers",
	"set_active_profile",
	"track_trending_click",
	"update_repair_status",
	"update_todo_status",
	"validate_item_for_layaway",
	"void_transaction",
]
