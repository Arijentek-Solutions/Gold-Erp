/**
 * Cart Store
 *
 * Manages shopping cart state, item operations, tax calculation, and order submission.
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'

export const useCartStore = defineStore('cart', () => {
	// ==========================================================================
	// STATE
	// ==========================================================================

	let storedItems = []
	try {
		const raw = localStorage.getItem('zevar_cart_items')
		storedItems = raw ? JSON.parse(raw) : []
	} catch (e) {
		localStorage.removeItem('zevar_cart_items')
		storedItems = []
	}

	// Customer linked to this sale
	const customer = ref(null)
	const items = ref(storedItems)
	const taxRate = ref(0)
	const currency = ref('USD')

	// Salespersons attached to the current sale (up to 4)
	const salespersons = ref([])

	// Trade-in items attached to the current sale
	const tradeIns = ref([])

	// Sync state across tabs/windows
	window.addEventListener('storage', (event) => {
		if (event.key === 'zevar_cart_items') {
			try {
				const newVal = event.newValue ? JSON.parse(event.newValue) : []
				items.value = newVal
			} catch (e) {
				items.value = []
			}
		}
	})

	// ==========================================================================
	// GETTERS
	// ==========================================================================

	const totalItems = computed(() => {
		return items.value.reduce((total, item) => total + (item.qty || 1), 0)
	})

	const subtotal = computed(() => {
		return items.value.reduce((sum, item) => {
			const qty = item.qty || 1
			const price = item.amount || 0
			return sum + price * qty
		}, 0)
	})

	const tax = computed(() => subtotal.value * (taxRate.value / 100))

	const tradeInCredit = computed(() => {
		return tradeIns.value.reduce((sum, ti) => sum + (ti.trade_in_value || 0), 0)
	})

	const grandTotal = computed(() => {
		const total = subtotal.value + tax.value - tradeInCredit.value
		return Math.max(0, total)
	})

	// ==========================================================================
	// ACTIONS
	// ==========================================================================

	function addItem(item) {
		if (!item.item_code) {
			return
		}

		const priceToUse = item.final_price || item.price || item.amount || 0
		const existingItem = items.value.find((i) => i.item_code === item.item_code)

		if (existingItem) {
			existingItem.qty++
		} else {
			items.value.push({
				item_code: item.item_code,
				item_name: item.item_name,
				image: item.image,
				metal: item.metal || item.custom_metal_type,
				purity: item.purity || item.custom_purity,
				amount: priceToUse,
				weight: item.gross_weight || item.custom_gross_weight_g,
				qty: 1,
			})
		}
		saveToStorage()
	}

	function removeItem(index) {
		items.value.splice(index, 1)
		saveToStorage()
	}

	function setCustomer(customerData) {
		customer.value = customerData
	}

	function clearCustomer() {
		customer.value = null
	}

	// Salesperson management
	function addSalesperson(employee, split) {
		if (salespersons.value.length >= 4) return
		salespersons.value.push({ employee, split: split })
	}

	function removeSalesperson(index) {
		salespersons.value.splice(index, 1)
	}

	function clearSalespersons() {
		salespersons.value = []
	}

	// Trade-in management
	function addTradeIn({ description, tradeInValue, newItemValue }) {
		tradeIns.value.push({
			description: description || '',
			trade_in_value: tradeInValue || 0,
			new_item_value: newItemValue || 0,
			manager_override: '',
			override_reason: '',
		})
	}

	function removeTradeIn(index) {
		tradeIns.value.splice(index, 1)
	}

	function clearTradeIns() {
		tradeIns.value = []
	}

	function clearCart() {
		items.value = []
		customer.value = null
		salespersons.value = []
		tradeIns.value = []
		saveToStorage()
	}

	function saveToStorage() {
		localStorage.setItem('zevar_cart_items', JSON.stringify(items.value))
	}

	// ==========================================================================
	// RESOURCES
	// ==========================================================================

	const fetchSettings = createResource({
		url: 'zevar_core.api.get_pos_settings',
		onSuccess(data) {
			if (data) {
				taxRate.value = data.tax_rate || 0
				currency.value = data.currency || 'USD'
			}
		},
	})

	function loadTaxForWarehouse(warehouse) {
		if (warehouse) {
			fetchSettings.fetch({ warehouse })
		}
	}

	// ==========================================================================
	// ORDER SUBMISSION
	// ==========================================================================

	/**
	 * Submit a POS invoice to the backend.
	 *
	 * @param {Array<{mode: string, amount: number}>} payments - Payment modes with amounts.
	 * @param {object} options - Additional options.
	 * @param {boolean} [options.taxExempt=false] - Whether to exempt tax.
	 * @param {string} [options.warehouse] - Warehouse for stock deduction.
	 * @returns {Promise<object>} The API response.
	 */
	async function submitOrder(payments, { taxExempt = false, warehouse } = {}) {
		const itemsPayload = items.value.map((i) => ({
			item_code: i.item_code,
			qty: i.qty || 1,
			rate: i.amount || 0,
		}))

		const paymentsPayload = payments.map((p) => ({
			mode_of_payment: p.mode,
			amount: p.amount,
		}))

		const customerName = customer.value?.name || 'Walk-In Customer'

		const params = {
			items: JSON.stringify(itemsPayload),
			payments: JSON.stringify(paymentsPayload),
			customer: customerName,
			warehouse: warehouse || '',
			tax_exempt: taxExempt,
		}

		// Attach salespersons if any are assigned
		if (salespersons.value.length > 0) {
			params.salespersons = JSON.stringify(
				salespersons.value.map((sp) => ({
					employee: sp.employee,
					split: sp.split,
				}))
			)
		}

		// Attach trade-ins if any are present
		if (tradeIns.value.length > 0) {
			params.trade_ins = JSON.stringify(
				tradeIns.value.map((ti) => ({
					trade_in_value: ti.trade_in_value,
					new_item_value: ti.new_item_value,
					manager_override: ti.manager_override,
					override_reason: ti.override_reason,
				}))
			)
		}

		const r = await createResource({
			url: 'zevar_core.api.create_pos_invoice',
			method: 'POST',
			params,
		}).fetch()

		return r
	}

	/**
	 * Create a layaway contract from the current cart items.
	 *
	 * @param {number} depositAmount - Initial deposit.
	 * @param {number} durationMonths - Contract duration (6, 9, or 12).
	 * @returns {Promise<object>} The API response with layaway_id.
	 */
	async function submitLayaway(depositAmount, durationMonths, { warehouse } = {}) {
		const itemsPayload = items.value.map((i) => ({
			item_code: i.item_code,
			qty: i.qty || 1,
			rate: i.amount || 0,
		}))

		const customerName = customer.value?.name || 'Walk-In Customer'

		const r = await createResource({
			url: 'zevar_core.api.layaway.create_layaway',
			method: 'POST',
			params: {
				customer: customerName,
				items: JSON.stringify(itemsPayload),
				deposit_amount: depositAmount,
				duration_months: durationMonths,
				warehouse: warehouse || '',
			},
		}).fetch()

		return r
	}

	return {
		items,
		taxRate,
		currency,
		totalItems,
		subtotal,
		tax,
		tradeInCredit,
		grandTotal,
		fetchSettings,
		loadTaxForWarehouse,
		addItem,
		removeItem,
		clearCart,
		submitOrder,
		submitLayaway,
		customer,
		setCustomer,
		clearCustomer,
		salespersons,
		addSalesperson,
		removeSalesperson,
		clearSalespersons,
		tradeIns,
		addTradeIn,
		removeTradeIn,
		clearTradeIns,
	}
})
