import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'

export const useCartStore = defineStore('cart', () => {
  
  // 1. STATE
  let storedItems = []
  try {
    const raw = localStorage.getItem('zevar_cart_items')
    storedItems = raw ? JSON.parse(raw) : []
  } catch (e) {
    localStorage.removeItem('zevar_cart_items')
    storedItems = []
  }

  const items = ref(storedItems)
  const taxRate = ref(0) 
  const currency = ref('USD')

  // 2. GETTERS
  const totalItems = computed(() => {
    return items.value.reduce((total, item) => total + (item.qty || 1), 0)
  })
  
  const subtotal = computed(() => {
    return items.value.reduce((sum, item) => {
        const qty = item.qty || 1
        const price = item.amount || 0 
        return sum + (price * qty)
    }, 0)
  })

  // Dynamic Tax
  const tax = computed(() => subtotal.value * (taxRate.value / 100))
  const grandTotal = computed(() => subtotal.value + tax.value)

  // 3. ACTIONS
  
  function addItem(item) {
    if (!item.item_code) {
      console.error("Missing item_code", item)
      return
    }

    const priceToUse = item.final_price || item.price || item.amount || 0

    // Check for duplicates
    const existingItem = items.value.find(i => i.item_code === item.item_code)

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
            qty: 1 
        })
    }
    saveToStorage()
  }

  function removeItem(index) {
    items.value.splice(index, 1)
    saveToStorage()
  }

  // FIX: Removed 'confirm()' so "New Order" wipes cart silently
  function clearCart() {
    items.value = []
    saveToStorage()
  }

  function saveToStorage() {
    localStorage.setItem('zevar_cart_items', JSON.stringify(items.value))
  }

  // --- FETCH SETTINGS ---
  const fetchSettings = createResource({
    url: 'zevar_core.api.get_pos_settings',
    auto: true,
    onSuccess(data) {
        if (data) {
            taxRate.value = data.tax_rate || 0
            currency.value = data.currency || 'USD'
            console.log(`⚙️ Settings: Tax ${taxRate.value}%`)
        }
    }
  })

  // --- SUBMIT ORDER ---
  async function submitOrder(paymentMode) {
    // 1. Prepare Items
    const itemsPayload = items.value.map(i => ({
        item_code: i.item_code,
        qty: i.qty || 1,
        rate: i.amount || 0
    }))

    // 2. Prepare Payment
    const paymentsPayload = [{
        mode: paymentMode, 
        amount: grandTotal.value
    }]

    console.log("🚀 Sending Order...", { items: itemsPayload, payment: paymentsPayload })

    // 3. Call Python API (Short Path)
    try {
        const r = await createResource({
            url: 'zevar_core.api.create_pos_invoice',
            method: 'POST',
            params: {
                items: JSON.stringify(itemsPayload),
                payments: JSON.stringify(paymentsPayload),
                customer: "Walk-In Customer" 
            }
        }).fetch()

        console.log("✅ Order Success:", r)
        // FIX: Removed alert() so flow is uninterrupted
        return r

    } catch (e) {
        console.error("❌ Order Failed:", e)
        throw e
    }
  }

  return {
    items,
    taxRate,
    currency,
    totalItems,
    subtotal,
    tax,
    grandTotal,
    fetchSettings,
    addItem,    
    removeItem, 
    clearCart,
    submitOrder 
  }
})