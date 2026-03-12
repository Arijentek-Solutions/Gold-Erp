/**
 * UI Store
 *
 * Manages UI state including search, filters, and theme preferences.
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
	// ==========================================================================
	// STATE
	// ==========================================================================

	const searchQuery = ref('')
	const activeFilters = ref({})
	const sidebarCollapsed = ref(false)

	// Check localStorage or system preference on load
	const isDark = ref(localStorage.getItem('theme') === 'dark')

	// Apply the class to the <html> tag immediately
	if (isDark.value) {
		document.documentElement.classList.add('dark')
	} else {
		document.documentElement.classList.remove('dark')
	}

	// ==========================================================================
	// ACTIONS
	// ==========================================================================

	function toggleTheme() {
		isDark.value = !isDark.value
		if (isDark.value) {
			document.documentElement.classList.add('dark')
			localStorage.setItem('theme', 'dark')
		} else {
			document.documentElement.classList.remove('dark')
			localStorage.setItem('theme', 'light')
		}
	}

	function setFilter(key, value) {
		if (value === null || value === undefined || value === '') {
			delete activeFilters.value[key]
		} else {
			activeFilters.value[key] = value
		}
	}

	function resetFilters() {
		activeFilters.value = {}
		searchQuery.value = ''
	}

	return {
		searchQuery,
		activeFilters,
		sidebarCollapsed,
		isDark,
		toggleTheme,
		setFilter,
		resetFilters,
	}
})
