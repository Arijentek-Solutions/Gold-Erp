"""
Attendance API - Roster management and Clock In/Out functionality
"""

import frappe
from frappe import _
from frappe.utils import getdate, now_datetime, time_diff_in_hours


@frappe.whitelist()
def get_employee_roster(employee_id: str = None):
	"""
	Get employee's roster/shift configuration.

	Args:
	    employee_id: Employee ID (optional, defaults to current user's employee)

	Returns:
	    Dict with roster configuration including working hours
	"""
	if not employee_id:
		employee_id = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")

	if not employee_id:
		frappe.throw(_("No employee record found for current user"))

	today = getdate()

	# Check for active shift assignment
	shift_assignment = frappe.db.get_value(
		"Shift Assignment",
		{
			"employee": employee_id,
			"docstatus": 1,
			"status": "Active",
			"start_date": ("<=", today),
			"end_date": (">=", today),
		},
		["shift_type", "start_date", "end_date"],
		as_dict=True,
	)

	if shift_assignment and shift_assignment.shift_type:
		shift_type = frappe.get_doc("Shift Type", shift_assignment.shift_type)
		return {
			"has_roster": True,
			"shift_type": shift_type.name,
			"shift_name": shift_type.shift_name,
			"start_time": str(shift_type.start_time) if shift_type.start_time else None,
			"end_time": str(shift_type.end_time) if shift_type.end_time else None,
			"working_hours": shift_type.working_hours or 8,
			"allow_check_out_before_shift_end": shift_type.allow_check_out_before_shift_end,
		}

	# No shift assignment - check employment type for default hours
	employee = frappe.get_doc("Employee", employee_id)
	employment_type = employee.employment_type or "Full-time"

	# Default working hours based on employment type
	default_hours = 8  # Full-time default
	if employment_type and "Part" in employment_type:
		default_hours = 4
	elif employment_type and "Contract" in employment_type:
		default_hours = 8

	return {
		"has_roster": False,
		"employment_type": employment_type,
		"working_hours": default_hours,
		"shift_type": None,
		"shift_name": "Standard Hours",
		"start_time": "09:00:00",
		"end_time": "17:00:00" if default_hours == 8 else "13:00:00",
	}


@frappe.whitelist()
def get_current_employee():
	"""
	Get the current user's employee record.

	Returns:
	    Employee basic info or None
	"""
	employee = frappe.db.get_value(
		"Employee",
		{"user_id": frappe.session.user, "status": "Active"},
		["name", "employee_name", "employment_type", "department", "designation"],
		as_dict=True,
	)

	if not employee:
		return None

	# Get roster info
	roster = get_employee_roster(employee.name)
	employee.roster = roster

	# Get today's check-in status
	today_checkin = get_today_checkin_status(employee.name)
	employee.today_checkin = today_checkin

	return employee


@frappe.whitelist()
def get_today_checkin_status(employee_id: str = None):
	"""
	Get today's check-in status for an employee.

	Args:
	    employee_id: Employee ID (optional, defaults to current user)

	Returns:
	    Dict with check-in status and logs
	"""
	if not employee_id:
		employee_id = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")

	if not employee_id:
		return {"checked_in": False, "logs": []}

	today = getdate()

	# Get today's check-in logs
	logs = frappe.get_all(
		"Employee Checkin",
		filters={"employee": employee_id, "time": [">=", today]},
		fields=["name", "log_type", "time", "latitude", "longitude", "device_id"],
		order_by="time asc",
	)

	# Determine current status
	checked_in = False
	last_log = None
	if logs:
		last_log = logs[-1]
		checked_in = last_log.log_type == "IN"

	# Calculate working hours for today
	total_hours = 0
	check_in_time = None
	for log in logs:
		if log.log_type == "IN":
			check_in_time = log.time
		elif log.log_type == "OUT" and check_in_time:
			total_hours += time_diff_in_hours(log.time, check_in_time)
			check_in_time = None

	# If currently checked in, add ongoing hours
	if checked_in and last_log:
		total_hours += time_diff_in_hours(now_datetime(), last_log.time)

	# Get roster for comparison
	roster = get_employee_roster(employee_id)
	overtime = max(0, total_hours - roster.get("working_hours", 8))

	return {
		"checked_in": checked_in,
		"last_log_type": last_log.log_type if last_log else None,
		"last_log_time": str(last_log.time) if last_log else None,
		"total_hours_today": round(total_hours, 2),
		"overtime_hours": round(overtime, 2),
		"working_hours_target": roster.get("working_hours", 8),
		"logs": [{"log_type": l.log_type, "time": str(l.time)} for l in logs],
	}


@frappe.whitelist()
def clock_in(latitude: float | None = None, longitude: float | None = None, notes: str | None = None):
	"""
	Record employee check-in with location.

	Args:
	    latitude: GPS latitude (optional)
	    longitude: GPS longitude (optional)
	    notes: Additional notes (optional)

	Returns:
	    Dict with success status and check-in details
	"""
	employee_id = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")

	if not employee_id:
		frappe.throw(_("No employee record found for current user"))

	# Check last log status
	last_log = frappe.db.get_value(
		"Employee Checkin",
		{"employee": employee_id},
		["log_type", "time"],
		order_by="time desc",
		as_dict=True,
	)

	if last_log and last_log.log_type == "IN":
		# Check if it's from today
		today = getdate()
		if getdate(last_log.time) == today:
			frappe.throw(_("Already checked in today. Please check out first."))

	# Create check-in record
	checkin = frappe.get_doc(
		{
			"doctype": "Employee Checkin",
			"employee": employee_id,
			"log_type": "IN",
			"time": now_datetime(),
			"device_id": "HRMS Portal",
			"latitude": latitude,
			"longitude": longitude,
			"note": notes,
		}
	)
	checkin.insert()

	# Get updated status
	status = get_today_checkin_status(employee_id)

	return {
		"success": True,
		"checkin_id": checkin.name,
		"time": str(checkin.time),
		"message": _("Checked in successfully at {0}").format(checkin.time.strftime("%H:%M")),
		"status": status,
	}


@frappe.whitelist()
def clock_out(latitude: float | None = None, longitude: float | None = None, notes: str | None = None):
	"""
	Record employee check-out and calculate hours.

	Args:
	    latitude: GPS latitude (optional)
	    longitude: GPS longitude (optional)
	    notes: Additional notes (optional)

	Returns:
	    Dict with success status, check-out details, and hours worked
	"""
	employee_id = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")

	if not employee_id:
		frappe.throw(_("No employee record found for current user"))

	# Check last log status
	last_log = frappe.db.get_value(
		"Employee Checkin",
		{"employee": employee_id},
		["log_type", "time", "name"],
		order_by="time desc",
		as_dict=True,
	)

	if not last_log or last_log.log_type == "OUT":
		frappe.throw(_("No active check-in found. Please check in first."))

	# Create check-out record
	checkout = frappe.get_doc(
		{
			"doctype": "Employee Checkin",
			"employee": employee_id,
			"log_type": "OUT",
			"time": now_datetime(),
			"device_id": "HRMS Portal",
			"latitude": latitude,
			"longitude": longitude,
			"note": notes,
		}
	)
	checkout.insert()

	# Calculate hours for this session
	hours_worked = time_diff_in_hours(checkout.time, last_log.time)

	# Get updated status
	status = get_today_checkin_status(employee_id)

	return {
		"success": True,
		"checkout_id": checkout.name,
		"time": str(checkout.time),
		"hours_this_session": round(hours_worked, 2),
		"message": _("Checked out successfully. Hours this session: {0}").format(round(hours_worked, 2)),
		"status": status,
	}


@frappe.whitelist()
def get_attendance_history(employee_id: str | None = None, days: int = 30):
	"""
	Get attendance history for an employee.

	Args:
	    employee_id: Employee ID (optional, defaults to current user)
	    days: Number of days to look back (default 30)

	Returns:
	    List of attendance records
	"""
	if not employee_id:
		employee_id = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")

	if not employee_id:
		return []

	from frappe.utils import add_days

	start_date = add_days(getdate(), -days)

	logs = frappe.get_all(
		"Employee Checkin",
		filters={"employee": employee_id, "time": [">=", start_date]},
		fields=["name", "log_type", "time", "latitude", "longitude", "device_id", "note"],
		order_by="time desc",
		limit=100,
	)

	return logs
