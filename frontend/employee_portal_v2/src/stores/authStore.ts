import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '@/types'
import { frappeGetCall } from '@/utils/frappe'

interface AuthState {
    user: User | null
    isLoading: boolean
    isAuthenticated: boolean
    error: string | null

    // Actions
    fetchUser: () => Promise<void>
    logout: () => Promise<void>
    clearError: () => void
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            user: null,
            isLoading: true,
            isAuthenticated: false,
            error: null,

            fetchUser: async () => {
                set({ isLoading: true, error: null })
                try {
                    const userName = await frappeGetCall<string>('frappe.auth.get_logged_user')
                    if (!userName || userName === 'Guest') {
                        set({ user: null, isAuthenticated: false, isLoading: false })
                        return
                    }

                    // Fetch user details
                    const userData = await frappeGetCall<User>('frappe.client.get', {
                        doctype: 'User',
                        name: userName,
                    })

                    set({
                        user: {
                            name: userName,
                            full_name: userData?.full_name || userName,
                            email: userData?.email || userName,
                            user_image: userData?.user_image,
                        },
                        isAuthenticated: true,
                        isLoading: false,
                    })
                } catch (error) {
                    set({
                        user: null,
                        isAuthenticated: false,
                        isLoading: false,
                        error: error instanceof Error ? error.message : 'Failed to fetch user',
                    })
                }
            },

            logout: async () => {
                try {
                    await frappeGetCall('frappe.core.doctype.user.user.logout')
                    set({ user: null, isAuthenticated: false, error: null })
                    window.location.href = '/login'
                } catch (error) {
                    set({ error: error instanceof Error ? error.message : 'Logout failed' })
                }
            },

            clearError: () => set({ error: null }),
        }),
        {
            name: 'auth-storage',
            partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
        }
    )
)