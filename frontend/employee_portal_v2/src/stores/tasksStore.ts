import { create } from 'zustand'
import type { Task, TaskStats, Todo } from '@/types'
import { frappeGetCall, frappeCall } from '@/utils/frappe'

interface TasksState {
    tasks: Task[]
    todos: Todo[]
    stats: TaskStats | null
    gameplanInstalled: boolean
    isLoading: boolean
    error: string | null

    // Actions
    fetchTasks: () => Promise<void>
    fetchTaskStats: () => Promise<void>
    fetchTodos: () => Promise<void>
    createTodo: (description: string, date?: string, priority?: string) => Promise<void>
    updateTodoStatus: (name: string, status: string) => Promise<void>
    deleteTodo: (name: string) => Promise<void>
}

export const useTasksStore = create<TasksState>((set, get) => ({
    tasks: [],
    todos: [],
    stats: null,
    gameplanInstalled: false,
    isLoading: false,
    error: null,

    fetchTasks: async () => {
        set({ isLoading: true, error: null })
        try {
            const data = await frappeGetCall<{ tasks: Task[]; gameplan_installed: boolean }>('zevar_core.api.tasks.get_employee_tasks')
            set({
                tasks: data?.tasks || [],
                gameplanInstalled: data?.gameplan_installed || false,
                isLoading: false
            })
        } catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to fetch tasks', isLoading: false })
        }
    },

    fetchTaskStats: async () => {
        try {
            const data = await frappeGetCall<TaskStats>('zevar_core.api.tasks.get_task_stats')
            set({
                stats: data,
                gameplanInstalled: data?.gameplan_installed || false
            })
        } catch (error) {
            console.error('Failed to fetch task stats:', error)
        }
    },

    fetchTodos: async () => {
        try {
            const data = await frappeGetCall<Todo[]>('zevar_core.api.tasks.get_personal_todos')
            set({ todos: data || [] })
        } catch (error) {
            console.error('Failed to fetch todos:', error)
        }
    },

    createTodo: async (description: string, date?: string, priority = 'Medium') => {
        try {
            await frappeCall('zevar_core.api.tasks.create_personal_todo', { description, date, priority })
            await get().fetchTodos()
        } catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to create todo' })
        }
    },

    updateTodoStatus: async (name: string, status: string) => {
        try {
            await frappeCall('zevar_core.api.tasks.update_todo_status', { name, status })
            await get().fetchTodos()
        } catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to update todo' })
        }
    },

    deleteTodo: async (name: string) => {
        try {
            await frappeCall('zevar_core.api.tasks.delete_todo', { name })
            await get().fetchTodos()
        } catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to delete todo' })
        }
    },
}))