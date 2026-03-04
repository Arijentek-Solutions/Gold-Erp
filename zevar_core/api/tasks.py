"""
Tasks API - Gameplan integration and personal todos
"""

import frappe
from frappe import _
from frappe.utils import getdate, today


@frappe.whitelist()
def get_employee_tasks(status: str | None = None, limit: int = 50):
	"""
	Get Gameplan tasks assigned to current user.

	Args:
	    status: Filter by status (optional: 'Backlog', 'Todo', 'In Progress', 'Done', 'Canceled')
	    limit: Maximum number of tasks to return

	Returns:
	    List of tasks with details
	"""
	# Check if Gameplan is installed
	if not frappe.db.exists("DocType", "GP Task"):
		return {"tasks": [], "gameplan_installed": False, "message": "Gameplan not installed"}

	user = frappe.session.user

	filters = {"assigned_to": user}
	if status:
		filters["status"] = status

	tasks = frappe.get_all(
		"GP Task",
		filters=filters,
		fields=[
			"name",
			"title",
			"description",
			"status",
			"priority",
			"due_date",
			"project",
			"team",
			"creation",
			"modified",
		],
		order_by="due_date asc, priority desc, creation desc",
		limit=limit,
	)

	result = []
	for task in tasks:
		project_name = None
		if task.project:
			project_name = frappe.db.get_value("GP Project", task.project, "title")

		result.append(
			{
				"id": task.name,
				"title": task.title,
				"description": task.description,
				"status": task.status,
				"priority": task.priority,
				"due_date": str(task.due_date) if task.due_date else None,
				"is_overdue": getdate(task.due_date) < getdate() if task.due_date else False,
				"project_id": task.project,
				"project_name": project_name,
				"team": task.team,
				"url": f"/g/tasks/{task.name}",
				"created": str(task.creation),
				"modified": str(task.modified),
			}
		)

	return {"tasks": result, "gameplan_installed": True, "total": len(result)}


@frappe.whitelist()
def get_task_stats():
	"""
	Get task statistics for current user.

	Returns:
	    Dict with task counts by status
	"""
	if not frappe.db.exists("DocType", "GP Task"):
		return {"gameplan_installed": False}

	user = frappe.session.user

	stats = frappe.db.sql(
		"""
        SELECT status, COUNT(*) as count
        FROM `tabGP Task`
        WHERE assigned_to = %s
        GROUP BY status
    """,
		(user,),
		as_dict=True,
	)

	# Get overdue count
	overdue = frappe.db.count(
		"GP Task",
		filters={"assigned_to": user, "due_date": ("<", today()), "status": ("not in", ["Done", "Canceled"])},
	)

	result = {"gameplan_installed": True, "by_status": {}, "total": 0, "overdue": overdue}

	for stat in stats:
		result["by_status"][stat.status] = stat.count
		result["total"] += stat.count

	return result


@frappe.whitelist()
def get_personal_todos(status: str = "Open"):
	"""
	Get personal TODO items for current user.

	Args:
	    status: Filter by status ('Open' or 'Closed')

	Returns:
	    List of TODO items
	"""
	todos = frappe.get_all(
		"TODO",
		filters={"allocated_to": frappe.session.user, "status": status},
		fields=["name", "description", "date", "priority", "status", "reference_type", "reference_name"],
		order_by="date asc, priority desc",
		limit=50,
	)

	return [
		{
			"id": todo.name,
			"description": todo.description,
			"date": str(todo.date) if todo.date else None,
			"priority": todo.priority,
			"status": todo.status,
			"reference_type": todo.reference_type,
			"reference_name": todo.reference_name,
		}
		for todo in todos
	]


@frappe.whitelist()
def create_personal_todo(description: str, date: str | None = None, priority: str = "Medium"):
	"""
	Create a personal TODO item.

	Args:
	    description: TODO description (required)
	    date: Due date (optional, defaults to today)
	    priority: Priority ('Low', 'Medium', 'High')

	Returns:
	    Dict with success status and TODO id
	"""
	if not description:
		frappe.throw(_("Description is required"))

	todo = frappe.get_doc(
		{
			"doctype": "TODO",
			"description": description,
			"allocated_to": frappe.session.user,
			"date": date or today(),
			"priority": priority,
			"status": "Open",
		}
	)
	todo.insert()

	return {"success": True, "todo_id": todo.name, "message": _("TODO created successfully")}


@frappe.whitelist()
def update_todo_status(todo_id: str, status: str = "Closed"):
	"""
	Update TODO status.

	Args:
	    todo_id: TODO document name
	    status: New status ('Open' or 'Closed')

	Returns:
	    Dict with success status
	"""
	todo = frappe.get_doc("TODO", todo_id)

	# Verify ownership
	if todo.allocated_to != frappe.session.user:
		frappe.throw(_("You can only modify your own TODOs"))

	todo.status = status
	todo.save()

	return {"success": True, "message": _("TODO updated successfully")}


@frappe.whitelist()
def delete_todo(todo_id: str):
	"""
	Delete a personal TODO item.

	Args:
	    todo_id: TODO document name

	Returns:
	    Dict with success status
	"""
	todo = frappe.get_doc("TODO", todo_id)

	# Verify ownership
	if todo.allocated_to != frappe.session.user:
		frappe.throw(_("You can only delete your own TODOs"))

	todo.delete()

	return {"success": True, "message": _("TODO deleted successfully")}


@frappe.whitelist()
def get_recent_activities(limit: int = 20):
	"""
	Get recent task and TODO activities for current user.

	Args:
	    limit: Maximum number of activities to return

	Returns:
	    List of recent activities
	"""
	activities = []

	# Get recent Gameplan tasks
	if frappe.db.exists("DocType", "GP Task"):
		tasks = frappe.get_all(
			"GP Task",
			filters={"assigned_to": frappe.session.user},
			fields=["name", "title", "status", "modified"],
			order_by="modified desc",
			limit=limit // 2,
		)

		for task in tasks:
			activities.append(
				{
					"type": "task",
					"id": task.name,
					"title": task.title,
					"status": task.status,
					"date": str(task.modified),
					"url": f"/g/tasks/{task.name}",
				}
			)

	# Get recent TODOs
	todos = frappe.get_all(
		"TODO",
		filters={"allocated_to": frappe.session.user},
		fields=["name", "description", "status", "modified"],
		order_by="modified desc",
		limit=limit // 2,
	)

	for todo in todos:
		activities.append(
			{
				"type": "todo",
				"id": todo.name,
				"title": todo.description,
				"status": todo.status,
				"date": str(todo.modified),
				"url": None,
			}
		)

	# Sort by date
	activities.sort(key=lambda x: x["date"], reverse=True)

	return activities[:limit]
