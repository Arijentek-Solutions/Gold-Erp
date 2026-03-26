"""
Helpdesk API - Issue reporting and ticket management
"""

import frappe
from frappe import _
from frappe.utils import now_datetime


@frappe.whitelist()
def create_support_ticket(
	subject: str,
	description: str,
	category: str = "Other",
	sub_category: str | None = None,
	priority: str = "Medium",
	department: str | None = None,
	reference_type: str | None = None,
	reference_name: str | None = None,
):
	"""
	Create a support ticket with enhanced business categories.

	Args:
	    subject: Ticket subject/title (required)
	    description: Detailed description (required)
	    category: Category ('Customer Issue', 'Jewelry Issue', 'Vendor Issue', 'Employee Issue', 'Store Issue', 'Technical', 'Other')
	    sub_category: Sub-category based on category
	    priority: Priority ('Low', 'Medium', 'High', 'Urgent')
	    department: Responsible department
	    reference_type: Type of reference ('Customer', 'Supplier', 'Employee', 'Item')
	    reference_name: Name of the referenced document

	Returns:
	    Dict with success status and ticket ID
	"""
	if not subject:
		frappe.throw(_("Subject is required"))
	if not description:
		frappe.throw(_("Description is required"))

	# Get employee info
	employee = frappe.db.get_value(
		"Employee",
		{"user_id": frappe.session.user},
		["name", "employee_name", "department", "designation", "reports_to"],
		as_dict=True,
	)

	# Find reporting manager user ID
	manager_user_id = None
	if employee and employee.get("reports_to"):
		manager_user_id = frappe.db.get_value("Employee", {"name": employee.reports_to}, "user_id")

	# Determine assigned user based on department
	assigned_to = manager_user_id
	if department:
		# Try to find department manager or user with this department
		dept_user = frappe.db.get_value(
			"Employee",
			{"department": department, "status": "Active"},
			"user_id",
			order_by="creation desc",
		)
		if dept_user:
			assigned_to = dept_user

	# Build full description with employee context
	context_info = f"""**Reported by:** {employee.employee_name if employee else frappe.session.user}
**Employee ID:** {employee.name if employee else 'N/A'}
**Employee Department:** {employee.department if employee else 'N/A'}
**Category:** {category}
**Sub-Category:** {sub_category or 'N/A'}
**Priority:** {priority}
**Responsible Department:** {department or 'N/A'}
**Date/Time:** {now_datetime().strftime('%Y-%m-%d %H:%M:%S')}"""

	# Add reference info if provided
	if reference_type and reference_name:
		context_info += f"\n**Related {reference_type}:** {reference_name}"

	full_description = f"""{context_info}

---

**Issue Description:**

{description}"""

	# Check if Helpdesk is installed
	if frappe.db.exists("DocType", "HD Ticket"):
		ticket_doc = {
			"doctype": "HD Ticket",
			"subject": subject,
			"description": full_description,
			"raised_by": frappe.session.user,
			"priority": priority,
			"ticket_type": category,
			"status": "Open",
			"custom_category": category,
			"custom_sub_category": sub_category,
			"custom_department": department,
		}

		# Add custom reference fields if they exist
		if reference_type and reference_name:
			ticket_doc["custom_reference_type"] = reference_type
			ticket_doc["custom_reference"] = reference_name

		# Assign to responsible person
		if assigned_to:
			ticket_doc["allocated_to"] = assigned_to

		ticket = frappe.get_doc(ticket_doc)
		ticket.insert()

		return {
			"success": True,
			"ticket_id": ticket.name,
			"message": _("Ticket {0} created successfully").format(ticket.name),
			"helpdesk_installed": True,
		}

	# Fallback to Frappe Issue doctype
	if frappe.db.exists("DocType", "Issue"):
		issue_doc = {
			"doctype": "Issue",
			"subject": subject,
			"description": full_description,
			"raised_by": frappe.session.user,
			"priority": priority,
			"issue_type": category,
			"status": "Open",
		}

		issue = frappe.get_doc(issue_doc)
		issue.insert()

		# Assign to responsible person via ToDo
		if assigned_to:
			todo = frappe.get_doc(
				{
					"doctype": "ToDo",
					"reference_type": "Issue",
					"reference_name": issue.name,
					"description": f"[{category}] {subject}",
					"allocated_to": assigned_to,
					"status": "Open",
				}
			)
			todo.insert(ignore_permissions=True)

		return {
			"success": True,
			"ticket_id": issue.name,
			"message": _("Issue {0} created successfully").format(issue.name),
			"helpdesk_installed": False,
		}

	# Last resort: Create a TODO
	allocated_to = (
		assigned_to or frappe.db.get_value("User", {"role": "HR Manager"}, "name") or "Administrator"
	)

	todo = frappe.get_doc(
		{
			"doctype": "ToDo",
			"description": f"[{category}] {subject}\n\n{full_description}",
			"allocated_to": allocated_to,
			"priority": priority,
			"status": "Open",
			"date": frappe.utils.today(),
		}
	)
	todo.insert()

	return {
		"success": True,
		"ticket_id": todo.name,
		"message": _("Your issue has been reported. A TODO has been created."),
		"helpdesk_installed": False,
	}


@frappe.whitelist()
def get_support_categories():
	"""
	Get available support categories with sub-categories.

	Returns:
	    List of category objects with sub-categories
	"""
	return [
		{
			"value": "Customer Issue",
			"label": "Customer Issue",
			"department": "Customer Service",
			"sub_categories": [
				{"value": "Return Request", "label": "Return Request"},
				{"value": "Exchange Request", "label": "Exchange Request"},
				{"value": "Complaint", "label": "Complaint"},
				{"value": "Billing Dispute", "label": "Billing Dispute"},
				{"value": "Layaway Issue", "label": "Layaway Issue"},
				{"value": "Gift Card Issue", "label": "Gift Card Issue"},
			],
		},
		{
			"value": "Jewelry Issue",
			"label": "Jewelry Issue",
			"department": "Quality Control",
			"sub_categories": [
				{"value": "Quality Defect", "label": "Quality Defect"},
				{"value": "Sizing Issue", "label": "Sizing Issue"},
				{"value": "Damage", "label": "Damage"},
				{"value": "Missing Stones", "label": "Missing Stones"},
				{"value": "Hallmark Issue", "label": "Hallmark Issue"},
			],
		},
		{
			"value": "Vendor Issue",
			"label": "Vendor Issue",
			"department": "Procurement",
			"sub_categories": [
				{"value": "Late Delivery", "label": "Late Delivery"},
				{"value": "Quality Problem", "label": "Quality Problem"},
				{"value": "Wrong Item", "label": "Wrong Item"},
				{"value": "Pricing Dispute", "label": "Pricing Dispute"},
			],
		},
		{
			"value": "Employee Issue",
			"label": "Employee Issue",
			"department": "Human Resources",
			"sub_categories": [
				{"value": "Attendance", "label": "Attendance"},
				{"value": "Payroll", "label": "Payroll"},
				{"value": "Leave", "label": "Leave"},
				{"value": "Manager", "label": "Manager"},
			],
		},
		{
			"value": "Store Issue",
			"label": "Store Issue",
			"department": "Operations",
			"sub_categories": [
				{"value": "Equipment", "label": "Equipment"},
				{"value": "Security", "label": "Security"},
				{"value": "Inventory", "label": "Inventory"},
				{"value": "POS System", "label": "POS System"},
			],
		},
		{
			"value": "Technical",
			"label": "Technical / IT",
			"department": "IT Support",
			"sub_categories": [],
		},
		{
			"value": "Other",
			"label": "Other",
			"department": "General",
			"sub_categories": [],
		},
	]


@frappe.whitelist()
def get_responsible_departments():
	"""
	Get list of departments with their managers.

	Returns:
	    List of department objects
	"""
	departments = frappe.get_all(
		"Department",
		filters={"is_group": 0},
		fields=["name", "department_name"],
		order_by="name",
	)

	result = []
	for dept in departments:
		manager = frappe.db.get_value(
			"Employee",
			{"department": dept.name, "designation": "Manager"},
			["user_id", "employee_name"],
			as_dict=True,
		)
		result.append(
			{
				"value": dept.name,
				"label": dept.department_name or dept.name,
				"manager": manager.employee_name if manager else None,
				"manager_email": manager.user_id if manager else None,
			}
		)

	return result


@frappe.whitelist()
def create_attendance_issue(
	subject: str,
	description: str,
	issue_type: str = "Attendance",
	priority: str = "Medium",
):
	"""
	Create a Helpdesk ticket for attendance/manager issues.

	Args:
	    subject: Issue subject/title (required)
	    description: Detailed description (required)
	    issue_type: Type of issue ('Attendance', 'Manager', 'Payroll', 'Other')
	    priority: Priority ('Low', 'Medium', 'High', 'Urgent')

	Returns:
	    Dict with success status and ticket ID
	"""
	if not subject:
		frappe.throw(_("Subject is required"))
	if not description:
		frappe.throw(_("Description is required"))

	# Get employee info
	employee = frappe.db.get_value(
		"Employee",
		{"user_id": frappe.session.user},
		["name", "employee_name", "department", "designation", "reports_to"],
		as_dict=True,
	)

	# Find reporting manager user ID
	manager_user_id = None
	if employee and employee.get("reports_to"):
		manager_user_id = frappe.db.get_value("Employee", {"name": employee.reports_to}, "user_id")

	# Build full description with employee context
	full_description = f"""**Reported by Employee:** {employee.employee_name if employee else frappe.session.user}
**Employee ID:** {employee.name if employee else 'N/A'}
**Department:** {employee.department if employee else 'N/A'}
**Designation:** {employee.designation if employee else 'N/A'}
**Date/Time:** {now_datetime().strftime('%Y-%m-%d %H:%M:%S')}

---

**Issue Description:**

{description}"""

	# Check if Helpdesk is installed
	if frappe.db.exists("DocType", "HD Ticket"):
		ticket_doc = {
			"doctype": "HD Ticket",
			"subject": subject,
			"description": full_description,
			"raised_by": frappe.session.user,
			"priority": priority,
			"ticket_type": issue_type,
			"status": "Open",
		}

		# Assign to reporting manager if found
		if manager_user_id:
			ticket_doc["allocated_to"] = manager_user_id

		ticket = frappe.get_doc(ticket_doc)
		ticket.insert()

		return {
			"success": True,
			"ticket_id": ticket.name,
			"message": _("Ticket {0} created successfully").format(ticket.name),
			"helpdesk_installed": True,
		}

	# Fallback to Frappe Issue doctype
	if frappe.db.exists("DocType", "Issue"):
		issue_doc = {
			"doctype": "Issue",
			"subject": subject,
			"description": full_description,
			"raised_by": frappe.session.user,
			"priority": priority,
			"issue_type": issue_type,
			"status": "Open",
		}

		issue = frappe.get_doc(issue_doc)
		issue.insert()

		# Assign to reporting manager if found (for Frappe Issue, this is usually via ToDo)
		if manager_user_id:
			todo = frappe.get_doc(
				{
					"doctype": "ToDo",
					"reference_type": "Issue",
					"reference_name": issue.name,
					"description": f"New issue assigned: {subject}",
					"allocated_to": manager_user_id,
					"status": "Open",
				}
			)
			todo.insert(ignore_permissions=True)

		return {
			"success": True,
			"ticket_id": issue.name,
			"message": _("Issue {0} created successfully").format(issue.name),
			"helpdesk_installed": False,
		}

	# Last resort: Create a TODO for HR Manager or Reporting Manager
	allocated_to = manager_user_id
	if not allocated_to:
		allocated_to = frappe.db.get_value("User", {"role": "HR Manager"}, "name") or "Administrator"

	todo = frappe.get_doc(
		{
			"doctype": "TODO",
			"description": f"[{issue_type}] {subject}\n\n{full_description}",
			"allocated_to": allocated_to,
			"priority": priority,
			"status": "Open",
			"date": frappe.utils.today(),
		}
	)
	todo.insert()

	return {
		"success": True,
		"ticket_id": todo.name,
		"message": _("Your issue has been reported. A TODO has been created for HR."),
		"helpdesk_installed": False,
	}


@frappe.whitelist()
def get_employee_tickets(status: str | None = None, limit: int = 50):
	"""
	Get tickets created by current user.

	Args:
	    status: Filter by status (optional)
	    limit: Maximum number of tickets to return

	Returns:
	    List of tickets with details
	"""
	tickets = []
	user = frappe.session.user

	# Try Helpdesk first
	if frappe.db.exists("DocType", "HD Ticket"):
		filters = {"raised_by": user}
		if status:
			filters["status"] = status

		hd_tickets = frappe.get_all(
			"HD Ticket",
			filters=filters,
			fields=[
				"name",
				"subject",
				"status",
				"priority",
				"ticket_type",
				"creation",
				"modified",
				"resolution_details",
			],
			order_by="creation desc",
			limit=limit,
		)

		for t in hd_tickets:
			tickets.append(
				{
					"id": t.name,
					"subject": t.subject,
					"status": t.status,
					"priority": t.priority,
					"type": t.ticket_type,
					"created": str(t.creation),
					"modified": str(t.modified),
					"resolution": t.resolution_details,
					"source": "helpdesk",
				}
			)

	# Also check Frappe Issues
	if frappe.db.exists("DocType", "Issue"):
		filters = {"raised_by": user}
		if status:
			filters["status"] = status

		issues = frappe.get_all(
			"Issue",
			filters=filters,
			fields=[
				"name",
				"subject",
				"status",
				"priority",
				"issue_type",
				"creation",
				"modified",
				"resolution_details",
			],
			order_by="creation desc",
			limit=limit,
		)

		for i in issues:
			tickets.append(
				{
					"id": i.name,
					"subject": i.subject,
					"status": i.status,
					"priority": i.priority,
					"type": i.issue_type,
					"created": str(i.creation),
					"modified": str(i.modified),
					"resolution": i.resolution_details,
					"source": "issue",
				}
			)

	# Sort by creation date
	tickets.sort(key=lambda x: x["created"], reverse=True)

	return tickets[:limit]


@frappe.whitelist()
def get_ticket_details(ticket_id: str):
	"""
	Get details of a specific ticket.

	Args:
	    ticket_id: Ticket document name

	Returns:
	    Ticket details dict
	"""
	# Try Helpdesk first
	if frappe.db.exists("DocType", "HD Ticket") and frappe.db.exists("HD Ticket", ticket_id):
		ticket = frappe.get_doc("HD Ticket", ticket_id)

		# Verify ownership
		if ticket.raised_by != frappe.session.user:
			frappe.throw(_("You can only view your own tickets"))

		return {
			"id": ticket.name,
			"subject": ticket.subject,
			"description": ticket.description,
			"status": ticket.status,
			"priority": ticket.priority,
			"type": ticket.ticket_type,
			"created": str(ticket.creation),
			"modified": str(ticket.modified),
			"resolution": ticket.resolution_details,
			"source": "helpdesk",
		}

	# Try Frappe Issue
	if frappe.db.exists("Issue", ticket_id):
		issue = frappe.get_doc("Issue", ticket_id)

		# Verify ownership
		if issue.raised_by != frappe.session.user:
			frappe.throw(_("You can only view your own tickets"))

		return {
			"id": issue.name,
			"subject": issue.subject,
			"description": issue.description,
			"status": issue.status,
			"priority": issue.priority,
			"type": issue.issue_type,
			"created": str(issue.creation),
			"modified": str(issue.modified),
			"resolution": issue.resolution_details,
			"source": "issue",
		}

	frappe.throw(_("Ticket not found"))


@frappe.whitelist()
def add_ticket_reply(ticket_id: str, message: str):
	"""
	Add a reply/comment to a ticket.

	Args:
	    ticket_id: Ticket document name
	    message: Reply message

	Returns:
	    Dict with success status
	"""
	if not message:
		frappe.throw(_("Message is required"))

	# Try Helpdesk first
	if frappe.db.exists("DocType", "HD Ticket") and frappe.db.exists("HD Ticket", ticket_id):
		ticket = frappe.get_doc("HD Ticket", ticket_id)

		# Verify ownership
		if ticket.raised_by != frappe.session.user:
			frappe.throw(_("You can only reply to your own tickets"))

		# Add comment
		comment = frappe.get_doc(
			{
				"doctype": "Comment",
				"comment_type": "Comment",
				"reference_doctype": "HD Ticket",
				"reference_name": ticket_id,
				"content": message,
				"comment_email": frappe.session.user,
			}
		)
		comment.insert()

		return {"success": True, "message": _("Reply added successfully")}

	# Try Frappe Issue
	if frappe.db.exists("Issue", ticket_id):
		issue = frappe.get_doc("Issue", ticket_id)

		# Verify ownership
		if issue.raised_by != frappe.session.user:
			frappe.throw(_("You can only reply to your own tickets"))

		# Add comment
		comment = frappe.get_doc(
			{
				"doctype": "Comment",
				"comment_type": "Comment",
				"reference_doctype": "Issue",
				"reference_name": ticket_id,
				"content": message,
				"comment_email": frappe.session.user,
			}
		)
		comment.insert()

		return {"success": True, "message": _("Reply added successfully")}

	frappe.throw(_("Ticket not found"))


@frappe.whitelist()
def get_issue_types():
	"""
	Get available issue types for ticket creation.

	Returns:
	    List of issue type options
	"""
	return [
		{"value": "Attendance", "label": "Attendance Issue"},
		{"value": "Manager", "label": "Manager/Escalation"},
		{"value": "Payroll", "label": "Payroll/Salary"},
		{"value": "Leave", "label": "Leave Request Issue"},
		{"value": "Other", "label": "Other"},
	]


@frappe.whitelist()
def get_ticket_stats():
	"""
	Get ticket statistics for current user.

	Returns:
	    Dict with ticket counts by status
	"""
	stats = {"total": 0, "open": 0, "closed": 0, "pending": 0}
	user = frappe.session.user

	# Count Helpdesk tickets
	if frappe.db.exists("DocType", "HD Ticket"):
		hd_stats = frappe.db.sql(
			"""
            SELECT status, COUNT(*) as count
            FROM `tabHD Ticket`
            WHERE raised_by = %s
            GROUP BY status
        """,
			(user,),
			as_dict=True,
		)

		for s in hd_stats:
			stats["total"] += s.count
			if s.status in ["Open", "Replied"]:
				stats["open"] += s.count
			elif s.status in ["Resolved", "Closed"]:
				stats["closed"] += s.count
			else:
				stats["pending"] += s.count

	# Count Frappe Issues
	if frappe.db.exists("DocType", "Issue"):
		issue_stats = frappe.db.sql(
			"""
            SELECT status, COUNT(*) as count
            FROM `tabIssue`
            WHERE raised_by = %s
            GROUP BY status
        """,
			(user,),
			as_dict=True,
		)

		for s in issue_stats:
			stats["total"] += s.count
			if s.status in ["Open"]:
				stats["open"] += s.count
			elif s.status in ["Closed", "Resolved"]:
				stats["closed"] += s.count
			else:
				stats["pending"] += s.count

	return stats
