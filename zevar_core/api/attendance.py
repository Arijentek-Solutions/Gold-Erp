"""
Attendance API - Roster management and Clock In/Out functionality
"""

import frappe
from frappe import _
from frappe.utils import getdate, now_datetime, time_diff_in_hours


@frappe.whitelist()
def get_employee_roster(employee_id: str | None = None):
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
def get_today_checkin_status(employee_id: str | None = None, skip_roster: bool = False):
	"""
	Get today's check-in status for an employee.

	Args:
	    employee_id: Employee ID (optional, defaults to current user)
	    skip_roster: Skip roster lookup for faster response

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

	# Get roster for comparison (skip if not needed for speed)
	working_hours_target = 8
	overtime = 0
	if not skip_roster:
		roster = get_employee_roster(employee_id)
		working_hours_target = roster.get("working_hours", 8)
		overtime = max(0, total_hours - working_hours_target)

	return {
		"checked_in": checked_in,
		"last_log_type": last_log.log_type if last_log else None,
		"last_log_time": str(last_log.time) if last_log else None,
		"total_hours_today": round(total_hours, 2),
		"overtime_hours": round(overtime, 2),
		"working_hours_target": working_hours_target,
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
	try:
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

		# Get updated status (skip roster for speed)
		status = get_today_checkin_status(employee_id, skip_roster=True)

		return {
			"success": True,
			"checkin_id": checkin.name,
			"time": str(checkin.time),
			"message": _("Checked in successfully at {0}").format(checkin.time.strftime("%H:%M")),
			"status": status,
		}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error("HRMS Clock-in Failed", frappe.get_traceback())
		frappe.throw(_("Failed to clock in: {0}").format(str(e)))


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

	try:
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

		# Get updated status (skip roster for speed)
		status = get_today_checkin_status(employee_id, skip_roster=True)

		# Auto-generate Attendance record if this is a final clock-out (not a break)
		is_break = notes and "Break" in notes
		if not is_break:
			_process_auto_attendance(employee_id)

		return {
			"success": True,
			"checkout_id": checkout.name,
			"time": str(checkout.time),
			"hours_this_session": round(hours_worked, 2),
			"message": _("Checked out successfully. Hours this session: {0}").format(round(hours_worked, 2)),
			"status": status,
		}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error("HRMS Clock-out Failed", frappe.get_traceback())
		frappe.throw(_("Failed to clock out: {0}").format(str(e)))


def _process_auto_attendance(employee_id):
	"""
	Process today's check-in logs and create/update an Attendance record.

	Calculates total working hours from all IN/OUT pairs, then creates
	a standard Attendance record with status Present or Half Day based
	on the employee's shift configuration.
	"""
	today = getdate()

	# Check if attendance already exists for today
	existing = frappe.db.get_value(
		"Attendance",
		{"employee": employee_id, "attendance_date": today, "docstatus": ("!=", 2)},
		"name",
	)
	if existing:
		return  # Don't duplicate

	# Get all today's logs
	logs = frappe.get_all(
		"Employee Checkin",
		filters={"employee": employee_id, "time": [">=", today]},
		fields=["log_type", "time"],
		order_by="time asc",
	)

	if not logs:
		return

	# Calculate total hours from all IN/OUT pairs
	total_hours = 0
	check_in_time = None
	for log in logs:
		if log.log_type == "IN":
			check_in_time = log.time
		elif log.log_type == "OUT" and check_in_time:
			total_hours += time_diff_in_hours(log.time, check_in_time)
			check_in_time = None

	if total_hours <= 0:
		return

	# Get roster to determine target hours and shift type
	roster = get_employee_roster(employee_id)
	target_hours = roster.get("working_hours", 8)
	shift_type = roster.get("shift_type")

	# Determine attendance status
	if total_hours >= target_hours:
		status = "Present"
	elif total_hours >= target_hours / 2:
		status = "Half Day"
	else:
		status = "Present"  # Still mark present even if short

	try:
		attendance_doc = frappe.get_doc(
			{
				"doctype": "Attendance",
				"employee": employee_id,
				"attendance_date": today,
				"status": status,
				"working_hours": round(total_hours, 2),
			}
		)
		if shift_type:
			attendance_doc.shift = shift_type

		attendance_doc.insert(ignore_permissions=True)
		attendance_doc.submit()
		frappe.db.commit()
	except Exception:
		# Non-critical: log but don't break the clock-out flow
		frappe.log_error("Auto-Attendance Creation Failed", frappe.get_traceback())


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


@frappe.whitelist()
def get_weekly_roster(employee_id: str | None = None, start_date: str | None = None):
	"""
	Get weekly roster/schedule for an employee.

	Args:
	    employee_id: Employee ID (optional, defaults to current user)
	    start_date: Start date for the week (optional, defaults to current week start)

	Returns:
	    Dict with weekly schedule including shifts for each day
	"""
	from frappe.utils import add_days, get_first_day, get_last_day

	if not employee_id:
		employee_id = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")

	if not employee_id:
		frappe.throw(_("No employee record found for current user"))

	today = getdate()

	# Get start of current week (Monday)
	if start_date:
		week_start = getdate(start_date)
	else:
		week_start = today - timedelta(days=today.weekday())

	week_end = add_days(week_start, 6)

	# Get all shift assignments for the employee in this date range
	shift_assignments = frappe.get_all(
		"Shift Assignment",
		filters={
			"employee": employee_id,
			"docstatus": 1,
			"start_date": ["<=", week_end],
		},
		fields=["name", "shift_type", "start_date", "end_date", "status"],
		order_by="start_date asc",
	)

	# Build daily schedule
	schedule = []
	current_date = week_start

	while current_date <= week_end:
		day_schedule = {
			"date": str(current_date),
			"day_name": current_date.strftime("%A"),
			"day_short": current_date.strftime("%a"),
			"day_num": current_date.day,
			"is_today": current_date == today,
			"is_past": current_date < today,
			"shift": None,
			"checkins": [],
			"total_hours": 0,
			"status": "off",
		}

		# Find applicable shift for this day
		for assignment in shift_assignments:
			assign_start = getdate(assignment.start_date)
			assign_end = getdate(assignment.end_date) if assignment.end_date else None

			if assign_start <= current_date and (not assign_end or assign_end >= current_date):
				if assignment.status == "Active":
					# Get shift type details
					shift_type = frappe.get_doc("Shift Type", assignment.shift_type)
					day_schedule["shift"] = {
						"name": shift_type.name,
						"shift_name": shift_type.shift_name,
						"start_time": str(shift_type.start_time) if shift_type.start_time else None,
						"end_time": str(shift_type.end_time) if shift_type.end_time else None,
						"working_hours": shift_type.working_hours or 8,
					}
					day_schedule["status"] = "working"
					break

		# If no shift assignment, check if it's a weekend or use default
		if not day_schedule["shift"]:
			# Check employment type for default hours
			employee = frappe.get_doc("Employee", employee_id)
			employment_type = employee.employment_type or "Full-time"
			default_hours = 8
			if "Part" in employment_type:
				default_hours = 4

			# Default: Mon-Fri are working days
			if current_date.weekday() < 5:  # Monday = 0, Friday = 4
				day_schedule["shift"] = {
					"name": "Standard",
					"shift_name": "Standard Hours",
					"start_time": "09:00:00",
					"end_time": "17:00:00" if default_hours == 8 else "13:00:00",
					"working_hours": default_hours,
				}
				day_schedule["status"] = "working"
			else:
				day_schedule["status"] = "off"

		# Get check-in logs for this day
		checkins = frappe.get_all(
			"Employee Checkin",
			filters={"employee": employee_id, "time": [">=", current_date, "<", add_days(current_date, 1)]},
			fields=["name", "log_type", "time"],
			order_by="time asc",
		)

		if checkins:
			day_schedule["checkins"] = [{"log_type": c.log_type, "time": str(c.time)} for c in checkins]

			# Calculate total hours
			total_hours = 0
			check_in_time = None
			for log in checkins:
				if log.log_type == "IN":
					check_in_time = log.time
				elif log.log_type == "OUT" and check_in_time:
					total_hours += time_diff_in_hours(log.time, check_in_time)
					check_in_time = None

			day_schedule["total_hours"] = round(total_hours, 2)

			# Update status based on hours
			target_hours = day_schedule["shift"]["working_hours"] if day_schedule["shift"] else 8
			if total_hours >= target_hours:
				day_schedule["status"] = "complete"
			elif total_hours > 0:
				day_schedule["status"] = "partial"

		schedule.append(day_schedule)
		current_date = add_days(current_date, 1)

	# Get roster summary
	roster = get_employee_roster(employee_id)

	return {
		"employee_id": employee_id,
		"week_start": str(week_start),
		"week_end": str(week_end),
		"schedule": schedule,
		"roster": roster,
		"summary": {
			"total_working_days": len([d for d in schedule if d["status"] != "off"]),
			"completed_days": len([d for d in schedule if d["status"] == "complete"]),
			"total_hours": sum(d["total_hours"] for d in schedule),
			"target_hours": sum(d["shift"]["working_hours"] for d in schedule if d["shift"]),
		},
	}


from datetime import timedelta
