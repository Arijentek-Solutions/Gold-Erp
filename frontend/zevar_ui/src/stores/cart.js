import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
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
  
  // Fix: Calculate simple Subtotal (Price * Qty)
  const subtotal = computed(() => {
    return items.value.reduce((sum, item) => {
        const qty = item.qty || 1
        const price = item.amount || 0 // Use stored price
        return sum + (price * qty)
    }, 0)
  })

  // Dynamic Tax
  const tax = computed(() => subtotal.value * (taxRate.value / 100))
  const grandTotal = computed(() => subtotal.value + tax.value)

  // 3. ACTIONS
  
  // Renamed back to 'addItem' to match ItemCard.vue
  function addItem(item) {
    if (!item.item_code) {
      console.error("Missing item_code", item)
      return
    }

    // Determine Price (Handle different API structures)
    // Priority: final_price (Modal) > price (Grid) > amount (Gemstones)
    const priceToUse = item.final_price || item.price || item.amount || 0

    // Check for duplicates
    const existingItem = items.value.find(i => i.item_code === item.item_code)

    if (existingItem) {
        existingItem.qty++
    } else {
        // Push new item WITH price
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

  // Renamed back to 'removeItem' (Index based) to match CartSidebar.vue
  function removeItem(index) {
    items.value.splice(index, 1)
    saveToStorage()
  }

  function clearCart() {
    if(confirm("Clear cart?")) {
        items.value = []
        saveToStorage()
    }
  }

  function saveToStorage() {
    localStorage.setItem('zevar_cart_items', JSON.stringify(items.value))
  }

  // 4. DAY 2: FETCH SETTINGS
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
    clearCart
  }
})