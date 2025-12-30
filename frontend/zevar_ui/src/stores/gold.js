import { defineStore } from 'pinia'
import { createResource } from 'frappe-ui'
import { ref } from 'vue'

export const useGoldStore = defineStore('gold', () => {
  
  // State: Holds rates like { "Gold-22K": 75.00, "Silver-925": 1.20 }
  const rates = ref({})
  const lastUpdated = ref(null)

  // Fetcher: Get the latest rate for EVERY metal type
  const fetchRates = createResource({
    url: 'frappe.client.get_list',
    makeParams() {
      return {
        doctype: 'Gold Rate Log',
        fields: ['metal', 'purity', 'rate_per_gram'],
        order_by: 'timestamp desc',
        limit_page_length: 20 // Get recent logs
      }
    },
    onSuccess(data) {
      // Convert list to a clean map: "Metal-Purity" -> Rate
      // Example: rates.value["Gold-22K"] = 75.00
      const newRates = {}
      data.forEach(log => {
        const key = `${log.metal}-${log.purity}`
        // Only set if we haven't seen this combo yet (since list is sorted by newest)
        if (!newRates[key]) {
          newRates[key] = log.rate_per_gram
        }
      })
      rates.value = newRates
      lastUpdated.value = new Date()
    }
  })

  // Action: Start the "Heartbeat" (Poll every 60 seconds)
  function startPolling() {
    fetchRates.fetch() // Fetch immediately
    setInterval(() => {
      fetchRates.fetch()
    }, 60000) // 60,000ms = 1 minute
  }

  return {
    rates,
    lastUpdated,
    startPolling
  }
})
