/**
 * Session Store
 *
 * Manages user session state, authentication, and warehouse selection.
 */

import { defineStore } from 'pinia'
import { createResource } from 'frappe-ui'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export const useSessionStore = defineStore('session', () => {
  const router = useRouter()

  // State
  const user = ref(null)
  const isLoggedIn = ref(false)
  const currentWarehouse = ref(localStorage.getItem('active_warehouse') || null)

  // Resources
  const userResource = createResource({
    url: 'frappe.auth.get_logged_user',
    auto: true,
    onSuccess(data) {
      // Handle case where server returns just a string (e.g., "Administrator")
      if (typeof data === 'string') {
        user.value = {
          full_name: data,
          email: data
        }
      } else {
        user.value = data
      }
      isLoggedIn.value = true
    },
    onError() {
      user.value = null
      isLoggedIn.value = false

      // Only redirect if not already on login page
      if (window.location.pathname !== '/pos/login') {
        router.push('/login')
      }
    }
  })

  const logoutResource = createResource({
    url: 'logout',
    onSuccess() {
      user.value = null
      isLoggedIn.value = false
      currentWarehouse.value = null
      localStorage.removeItem('active_warehouse')
      window.location.href = '/pos/login'
    }
  })

  // Actions
  function setWarehouse(warehouseID) {
    currentWarehouse.value = warehouseID
    if (warehouseID) {
      localStorage.setItem('active_warehouse', warehouseID)
    } else {
      localStorage.removeItem('active_warehouse')
    }
  }

  return {
    user,
    isLoggedIn,
    currentWarehouse,
    userResource,
    logoutResource,
    setWarehouse
  }
})
