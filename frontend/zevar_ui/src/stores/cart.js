import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export const useCartStore = defineStore('cart', () => {
  
  // 🛡️ SAFE LOAD: Prevent "Zombie" errors if local storage is corrupt
  let storedItems = []
  try {
    const raw = localStorage.getItem('zevar_cart_items')
    storedItems = raw ? JSON.parse(raw) : []
  } catch (e) {
    console.error("Cart corrupted, resetting.", e)
    localStorage.removeItem('zevar_cart_items')
    storedItems = []
  }

  const items = ref(storedItems)

  // 2. Getters
  // Calculate total physical items (sum of quantities), not just rows
  const totalItems = computed(() => {
    return items.value.reduce((total, item) => total + (item.qty || 1), 0)
  })
  
  // Calculate Subtotal (Price * Qty)
  const subtotal = computed(() => {
    return items.value.reduce((sum, item) => {
        const qty = item.qty || 1
        const price = item.amount || 0
        return sum + (price * qty)
    }, 0)
  })

  // Standard 8.875% Tax
  const tax = computed(() => subtotal.value * 0.08875)
  const grandTotal = computed(() => subtotal.value + tax.value)

  // 3. Actions
  function addItem(item) {
    if (!item.item_code) {
      console.error("Cannot add item: Missing item_code", item)
      alert("Error: Item Code is missing!")
      return
    }

    // 💡 SMART PRICE: Check 'final_price' (Modal) OR 'price' (Grid)
    const priceToUse = item.final_price || item.price || 0

    // CHECK DUPLICATES: Search by Item Code
    const existingItem = items.value.find(i => i.item_code === item.item_code)

    if (existingItem) {
        // If exists, just increment quantity
        existingItem.qty++
        console.log(`🛒 Incremented ${item.item_name} Qty to ${existingItem.qty}`)
    } else {
        // If new, push with qty: 1
        console.log("🛒 Adding New Row:", item.item_name)
        items.value.push({
            item_code: item.item_code,
            item_name: item.item_name,
            image: item.image,
            metal: item.metal,
            purity: item.purity,
            amount: priceToUse, 
            weight: item.gross_weight,
            qty: 1 
        })
    }
  }

  function removeItem(index) {
    items.value.splice(index, 1)
  }

  function clearCart() {
    if(confirm("Are you sure you want to clear the entire cart?")) {
        items.value = []
    }
  }

  // 4. Persistence
  watch(items, (newItems) => {
    localStorage.setItem('zevar_cart_items', JSON.stringify(newItems))
  }, { deep: true })

  return {
    items,
    totalItems,
    subtotal,
    tax,
    grandTotal,
    addItem,
    removeItem,
    clearCart
  }
})