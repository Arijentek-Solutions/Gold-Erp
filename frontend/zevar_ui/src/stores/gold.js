/**
 * Gold Store
 *
 * Manages live gold rate polling and caching for different metal/purity combinations.
 */

import { defineStore } from 'pinia'
import { createResource } from 'frappe-ui'
import { ref } from 'vue'

export const useGoldStore = defineStore('gold', () => {
	// ==========================================================================
	// STATE
	// ==========================================================================

	// Holds rates like { "Gold-22K": 75.00, "Silver-925": 1.20 }
	const rates = ref({})
	const lastUpdated = ref(null)

	// ==========================================================================
	// RESOURCES
	// ==========================================================================

	const fetchRates = createResource({
		url: 'frappe.client.get_list',
		makeParams() {
			return {
				doctype: 'Gold Rate Log',
				fields: ['metal', 'purity', 'rate_per_gram'],
				order_by: 'timestamp desc',
				limit_page_length: 20,
			}
		},
		onSuccess(data) {
			// Convert list to a clean map: "Metal-Purity" -> Rate
			const newRates = {}
			data.forEach((log) => {
				const key = `${log.metal}-${log.purity}`
				// Only set if we haven't seen this combo yet (since list is sorted by newest)
				if (!newRates[key]) {
					newRates[key] = log.rate_per_gram
				}
			})
			rates.value = newRates
			lastUpdated.value = new Date()
		},
	})

	// ==========================================================================
	// ACTIONS
	// ==========================================================================

	function startPolling() {
		fetchRates.fetch()
		setInterval(() => {
			fetchRates.fetch()
		}, 60000)
	}

	return {
		rates,
		lastUpdated,
		startPolling,
	}
})
