import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  // Existing State
  const searchQuery = ref('')
  const activeFilters = ref({})
  
  // NEW: Dark Mode State
  // Check localStorage or system preference on load
  const isDark = ref(localStorage.getItem('theme') === 'dark')

  // Apply the class to the <html> tag immediately
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }

  // Actions
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

  // Keep existing filter actions...
  function setFilter(key, value) {
    if (!value) {
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
    isDark,     // Export state
    toggleTheme,// Export action
    setFilter,
    resetFilters
  }
})