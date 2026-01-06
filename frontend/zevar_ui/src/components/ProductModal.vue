<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
    
    <div @click="close" class="absolute inset-0 bg-gray-900/50 backdrop-blur-sm transition-opacity"></div>

    <div class="relative bg-white rounded-xl shadow-2xl w-full max-w-4xl overflow-hidden flex flex-col md:flex-row max-h-[90vh]">
      
      <button @click="close" class="absolute top-4 right-4 z-10 p-2 bg-white/80 rounded-full hover:bg-gray-100 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <div class="w-full md:w-1/2 bg-gray-50 flex items-center justify-center p-8 border-r border-gray-100">
        <img 
          v-if="details.image" 
          :src="details.image" 
          class="max-h-[60vh] object-contain drop-shadow-lg transform hover:scale-105 transition-transform duration-500" 
        />
        <div v-else class="text-gray-300">
           <svg class="h-32 w-32" fill="none" viewBox="0 0 24 24" stroke="currentColor">
             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
           </svg>
        </div>
      </div>

      <div class="w-full md:w-1/2 p-8 overflow-y-auto">
        
        <div v-if="loading" class="h-full flex items-center justify-center">
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
        </div>

        <div v-else>
          <div class="mb-6">
            <h2 class="text-2xl font-bold text-gray-900">{{ details.item_name }}</h2>
            <p class="text-sm text-gray-500 mt-1">{{ details.item_code }}</p>
          </div>

          <div class="flex gap-2 mb-8">
            <span class="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs font-bold uppercase">{{ details.metal }}</span>
            <span class="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-xs font-bold uppercase">{{ details.purity }}</span>
          </div>

          <div class="bg-gray-50 rounded-lg p-4 mb-6 text-sm border border-gray-100">
            <div class="flex justify-between mb-2">
              <span class="text-gray-500">Gross Weight</span>
              <span class="font-medium">{{ details.gross_weight }} g</span>
            </div>
            <div class="flex justify-between mb-2 text-red-400">
              <span class="">- Stone Weight</span>
              <span class="">{{ details.stone_weight }} g</span>
            </div>
            <div class="flex justify-between pt-2 border-t border-gray-200">
              <span class="font-bold text-gray-700">Net Weight</span>
              <span class="font-bold text-gray-900">{{ details.net_weight }} g</span>
            </div>
          </div>

          <div v-if="details.gemstones && details.gemstones.length > 0" class="mb-6 bg-gray-50 rounded-lg border border-gray-100 p-3">
            <h4 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Zevar Gemstone Detail</h4>
            <table class="w-full text-sm text-left">
              <thead>
                <tr class="text-xs text-gray-500 uppercase border-b border-gray-200">
                  <th class="pb-1">Stone</th>
                  <th class="pb-1 text-right">Carat</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(gem, i) in details.gemstones" :key="i" class="border-b last:border-0 border-gray-100">
                  <td class="py-2 font-medium text-gray-800">
                    {{ gem.gem_type }}
                    <span class="block text-[10px] text-gray-500 font-normal">
                       {{ gem.cut }} • {{ gem.color }} • {{ gem.clarity }}
                    </span>
                  </td>
                  <td class="py-2 text-right font-mono">{{ gem.carat }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="space-y-3 mb-8">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Gold Rate (Live)</span>
              <span>{{ formatCurrency(details.gold_rate) }} /g</span>
            </div>
            
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Gold Value</span>
              <span>{{ formatCurrency(details.gold_value) }}</span>
            </div>

            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Making Charges</span>
              <span>{{ formatCurrency(details.making_charges) }}</span>
            </div>

            <div v-if="details.gemstone_value > 0" class="flex justify-between text-sm">
              <span class="text-purple-600 font-medium">💎 Gemstone Value</span>
              <span class="text-purple-700 font-bold">{{ formatCurrency(details.gemstone_value) }}</span>
            </div>

            <div class="flex justify-between items-end pt-4 border-t border-gray-100">
              <span class="text-lg font-bold text-gray-900">Total</span>
              <span class="text-3xl font-bold text-gray-900">{{ formatCurrency(details.final_price) }}</span>
            </div>
          </div>

          <button 
          @click="addToCart"
          class="w-full bg-gray-900 text-white py-4 rounded-xl font-bold text-lg hover:bg-gray-800 transition-all shadow-lg hover:shadow-xl transform active:scale-95">
            Add to Cart
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { createResource } from 'frappe-ui'
import { watch, ref } from 'vue'
import { useCartStore } from '@/stores/cart.js'

const props = defineProps(['show', 'itemCode'])
const emit = defineEmits(['close'])
const cart = useCartStore()

const details = ref({})
const loading = ref(false)

// Fetcher
const itemFetcher = createResource({
  url: 'zevar_core.api.get_item_price',
  makeParams() {
    return { item_code: props.itemCode }
  },
  onSuccess(data) {
    // 1. Merge API data with Item Code
    details.value = { ...data, item_code: props.itemCode }
    
    // 2. STOP LOADING (This was the missing line!) 🛑
    loading.value = false 
    
    console.log("✅ Data Loaded:", details.value)
  }
})

// Watcher
watch(() => props.show, (isOpen) => {
  if (isOpen && props.itemCode) {
    loading.value = true
    details.value = {} // Clear old data
    itemFetcher.fetch()
  }
})

function addToCart() {
  if (!details.value.item_code) return
  
  // Add to Store
  cart.addItem(details.value)
  
  // Alert and Close
  alert("Added to Cart!")
  emit('close')
}

function close() {
  emit('close')
}

function formatCurrency(val) {
  if (!val) return '$0.00'
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val)
}
</script>