export interface User {
    name: string
    full_name: string
    email: string
    user_image?: string
}

export interface Employee {
    name: string
    employee_name: string
    designation?: string
    department?: string
    branch?: string
    reports_to?: string
    date_of_joining?: string
    employee_image?: string
}

export interface AttendanceStatus {
    checked_in: boolean
    check_in_time?: string
    check_out_time?: string
    total_hours_today: number
    overtime_hours: number
    shift?: string
}

export interface RosterInfo {
    shift?: string
    working_hours: number
    week_off?: string
}

export interface LeaveBalance {
    leave_type: string
    total_leaves: number
    used_leaves: number
    balance: number
}

export interface LeaveApplication {
    name: string
    leave_type: string
    from_date: string
    to_date: string
    total_leave_days: number
    status: 'Open' | 'Pending' | 'Approved' | 'Rejected' | 'Cancelled'
    posting_date: string
    reason?: string
}

export interface Task {
    id: string
    title: string
    description?: string
    status: 'Backlog' | 'Todo' | 'In Progress' | 'Done' | 'Canceled'
    priority: 'Low' | 'Medium' | 'High' | 'Urgent'
    due_date?: string
    is_overdue: boolean
    project_id?: string
    project_name?: string
    team?: string
    url: string
    created: string
    modified: string
}

export interface TaskStats {
    total: number
    overdue: number
    by_status: Record<string, number>
    gameplan_installed: boolean
}

export interface Todo {
    name: string
    description: string
    status: 'Open' | 'Closed'
    priority: 'Low' | 'Medium' | 'High'
    date?: string
}

export interface Ticket {
    name: string
    subject: string
    description?: string
    status: 'Open' | 'Replied' | 'Resolved' | 'Closed'
    priority: 'Low' | 'Medium' | 'High' | 'Urgent'
    ticket_type: string
    creation: string
    modified: string
}

export interface TicketStats {
    total: number
    open: number
    closed: number
    pending: number
}

export interface PayrollInfo {
    month: string
    gross_pay: number
    net_pay: number
    total_deduction: number
    total_working_days: number
    leave_without_pay: number
    payment_date?: string
}

export interface ExpenseClaim {
    name: string
    expense_type: string
    total_claimed_amount: number
    status: 'Draft' | 'Submitted' | 'Cancelled' | 'Paid'
    posting_date: string
}

export interface DashboardWidget {
    id: string
    type: 'clock' | 'attendance' | 'leaves' | 'tasks' | 'tickets' | 'payroll' | 'announcements' | 'quick-links'
    title: string
    colSpan: 1 | 2 | 3 | 4
    rowSpan: 1 | 2
    visible: boolean
    order: number
}

export interface NavItem {
    to: string
    icon: string
    label: string
    badge?: number
}