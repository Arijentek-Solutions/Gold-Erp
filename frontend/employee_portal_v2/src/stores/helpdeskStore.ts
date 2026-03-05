import { create } from 'zustand'
import type { Ticket, TicketStats } from '@/types'
import { frappeGetCall, frappeCall } from '@/utils/frappe'

interface HelpdeskState {
    tickets: Ticket[]
    stats: TicketStats | null
    issueTypes: string[]
    isLoading: boolean
    error: string | null

    // Actions
    fetchTickets: () => Promise<void>
    fetchTicketStats: () => Promise<void>
    fetchIssueTypes: () => Promise<void>
    createTicket: (subject: string, description: string, issueType?: string, priority?: string) => Promise<void>
}

export const useHelpdeskStore = create<HelpdeskState>((set, get) => ({
    tickets: [],
    stats: null,
    issueTypes: [],
    isLoading: false,
    error: null,

    fetchTickets: async () => {
        set({ isLoading: true, error: null })
        try {
            const data = await frappeGetCall<Ticket[]>('zevar_core.api.helpdesk.get_employee_tickets')
            set({ tickets: data || [], isLoading: false })
        } catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to fetch tickets', isLoading: false })
        }
    },

    fetchTicketStats: async () => {
        try {
            const data = await frappeGetCall<TicketStats>('zevar_core.api.helpdesk.get_ticket_stats')
            set({ stats: data })
        } catch (error) {
            console.error('Failed to fetch ticket stats:', error)
        }
    },

    fetchIssueTypes: async () => {
        try {
            const data = await frappeGetCall<string[]>('zevar_core.api.helpdesk.get_issue_types')
            set({ issueTypes: data || [] })
        } catch (error) {
            console.error('Failed to fetch issue types:', error)
        }
    },

    createTicket: async (subject: string, description: string, issueType = 'Other', priority = 'Medium') => {
        set({ isLoading: true, error: null })
        try {
            await frappeCall('zevar_core.api.helpdesk.create_attendance_issue', {
                subject,
                description,
                issue_type: issueType,
                priority,
            })
            await get().fetchTickets()
            await get().fetchTicketStats()
            set({ isLoading: false })
        } catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to create ticket', isLoading: false })
        }
    },
}))