/**
 * Theme Composable
 * 
 * Shared theme management
 */
import { ref, onMounted } from 'vue'

export function useTheme() {
  const isDark = ref(true)
  const themeKey = ref(0)

  const loadTheme = () => {
    const stored = localStorage.getItem('zevar-theme')
    if (stored) {
      isDark.value = stored === 'dark'
    } else {
      isDark.value = true
      localStorage.setItem('zevar-theme', 'dark')
    }
    updateDocumentClass()
  }

  const toggleTheme = () => {
    isDark.value = !isDark.value
    localStorage.setItem('zevar-theme', isDark.value ? 'dark' : 'light')
    updateDocumentClass()
    themeKey.value++
  }

  const updateDocumentClass = () => {
    document.documentElement.classList.toggle('dark', isDark.value)
    document.body.style.backgroundColor = isDark.value ? '#08080a' : '#ffffff'
  }

  onMounted(() => {
    loadTheme()
  })

  return {
    isDark,
    themeKey,
    toggleTheme,
    loadTheme
  }
}
