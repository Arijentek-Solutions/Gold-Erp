"""
Helpdesk API - Issue reporting and ticket management
"""

import frappe
from frappe import _
from frappe.utils import now_datetime


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
		"Employee", {"user_id": frappe.session.user}, ["name", "employee_name", "department", "designation"], as_dict=True
	)

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
		ticket = frappe.get_doc(
			{
				"doctype": "HD Ticket",
				"subject": subject,
				"description": full_description,
				"raised_by": frappe.session.user,
				"priority": priority,
				"ticket_type": issue_type,
				"status": "Open",
			}
		)
		ticket.insert()

		return {
			"success": True,
			"ticket_id": ticket.name,
			"message": _("Ticket {0} created successfully").format(ticket.name),
			"helpdesk_installed": True,
		}

	# Fallback to Frappe Issue doctype
	if frappe.db.exists("DocType", "Issue"):
		issue = frappe.get_doc(
			{
				"doctype": "Issue",
				"subject": subject,
				"description": full_description,
				"raised_by": frappe.session.user,
				"priority": priority,
				"issue_type": issue_type,
				"status": "Open",
			}
		)
		issue.insert()

		return {
			"success": True,
			"ticket_id": issue.name,
			"message": _("Issue {0} created successfully").format(issue.name),
			"helpdesk_installed": False,
		}

	# Last resort: Create a TODO for HR Manager
	todo = frappe.get_doc(
		{
			"doctype": "TODO",
			"description": f"[{issue_type}] {subject}\n\n{full_description}",
			"allocated_to": frappe.db.get_value("User", {"role": "HR Manager"}, "name") or "Administrator",
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
			fields=["name", "subject", "status", "priority", "ticket_type", "creation", "modified", "resolution_details"],
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
			fields=["name", "subject", "status", "priority", "issue_type", "creation", "modified", "resolution_details"],
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
