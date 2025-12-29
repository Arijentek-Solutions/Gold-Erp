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
      // 👇 NEW LOGIC: Check if data is just a text string
      if (typeof data === 'string') {
        // Wrap it into an object so the UI can read '.full_name'
        user.value = {
          full_name: data,
          email: data
        }
      } else {
        // If it's already an object, use it as is
        user.value = data
      }
      
      isLoggedIn.value = true
    },
    onError(err) {
      console.error("User fetch error:", err);
      user.value = null
      isLoggedIn.value = false
      router.push('/login')
    }
  })

  const logoutResource = createResource({
    url: 'logout',
    onSuccess() {
      user.value = null
      isLoggedIn.value = false
      currentWarehouse.value = null
      localStorage.removeItem('active_warehouse')
      window.location.reload()
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

  function login(userData) {
    user.value = userData
    isLoggedIn.value = true
  }

  return {
    user,
    isLoggedIn,
    currentWarehouse,
    userResource,
    logoutResource,
    setWarehouse,
    login
  }
})

