import { create } from 'zustand'
import type { Employee, AttendanceStatus, RosterInfo, LeaveBalance, LeaveApplication } from '@/types'
import { frappeGetCall, frappeCall } from '@/utils/frappe'

interface EmployeeState {
    employee: Employee | null
    attendance: AttendanceStatus | null
    roster: RosterInfo | null
    leaveBalances: LeaveBalance[]
    leaveApplications: LeaveApplication[]
    isLoading: boolean
    error: string | null

    // Actions
    fetchEmployee: () => Promise<void>
    fetchAttendance: () => Promise<void>
    fetchRoster: () => Promise<void>
    fetchLeaveBalances: () => Promise<void>
    fetchLeaveApplications: () => Promise<void>
    clockIn: () => Promise<void>
    clockOut: () => Promise<void>
}

export const useEmployeeStore = create<EmployeeState>((set, get) => ({
    employee: null,
    attendance: null,
    roster: null,
    leaveBalances: [],
    leaveApplications: [],
    isLoading: false,
    error: null,

    fetchEmployee: async () => {
        set({ isLoading: true, error: null })
        try {
            const data = await frappeGetCall<Employee>('zevar_core.api.attendance.get_current_employee')
            set({ employee: data, isLoading: false })
        } catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to fetch employee', isLoading: false })
        }
    },

    fetchAttendance: async () => {
        const { employee } = get()
        if (!employee?.name) return

        try {
            const data = await frappeGetCall<AttendanceStatus>('zevar_core.api.attendance.get_today_checkin_status', {
                employee_id: employee.name
            })
            set({ attendance: data })
        } catch (error) {
            console.error('Failed to fetch attendance:', error)
        }
    },

    fetchRoster: async () => {
        const { employee } = get()
        if (!employee?.name) return

        try {
            const data = await frappeGetCall<RosterInfo>('zevar_core.api.attendance.get_employee_roster', {
                employee_id: employee.name
            })
            set({ roster: data })
        } catch (error) {
            console.error('Failed to fetch roster:', error)
        }
    },

    fetchLeaveBalances: async () => {
        try {
            const data = await frappeGetCall<Record<string, Omit<LeaveBalance, 'leave_type'>>>('hrms.api.get_leave_balance_map')
            const balances = Object.entries(data || {}).map(([key, value]) => ({
                leave_type: key,
                ...value,
            }))
            set({ leaveBalances: balances })
        } catch (error) {
            console.error('Failed to fetch leave balances:', error)
        }
    },

    fetchLeaveApplications: async () => {
        try {
            const data = await frappeGetCall<LeaveApplication[]>('hrms.api.get_leave_applications')
            set({ leaveApplications: data || [] })
        } catch (error) {
            console.error('Failed to fetch leave applications:', error)
        }
    },

    clockIn: async () => {
        try {
            await frappeCall('zevar_core.api.attendance.clock_in')
            await get().fetchAttendance()
        } catch (error) {
            set({ error: error instanceof Error ? error.message : 'Clock in failed' })
        }
    },

    clockOut: async () => {
        try {
            await frappeCall('zevar_core.api.attendance.clock_out')
            await get().fetchAttendance()
        } catch (error) {
            set({ error: error instanceof Error ? error.message : 'Clock out failed' })
        }
    },
}))