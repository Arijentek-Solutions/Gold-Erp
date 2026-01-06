<template>
  <div>
    <div 
      v-if="isOpen" 
      @click="close"
      class="fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-40 transition-opacity"
    ></div>

    <div 
      class="fixed top-0 right-0 h-full w-full sm:w-[400px] bg-white shadow-2xl z-50 transform transition-transform duration-300 ease-in-out flex flex-col"
      :class="isOpen ? 'translate-x-0' : 'translate-x-full'"
    >
      
      <div class="p-4 border-b border-gray-100 flex items-center justify-between bg-gray-50">
        <h2 class="text-lg font-bold text-gray-800 flex items-center gap-2">
          <span>🛒</span> Shopping Bag
          <span class="text-xs font-normal text-gray-500">({{ cart.totalItems }} items)</span>
        </h2>
        
        <div class="flex items-center gap-2">
            <button 
                v-if="cart.items.length > 0"
                @click="cart.clearCart()"
                class="text-xs font-bold text-red-500 hover:text-red-700 hover:bg-red-50 px-2 py-1 rounded transition-colors"
            >
                Clear
            </button>

            <button @click="close" class="p-2 hover:bg-gray-200 rounded-full transition-colors">
            <svg class="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
            </button>
        </div>
      </div>

      <div v-if="cart.items.length === 0" class="flex-1 flex flex-col items-center justify-center text-gray-400">
        <svg class="w-16 h-16 mb-4 text-gray-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
        </svg>
        <p>Your bag is empty.</p>
        <button @click="close" class="mt-4 text-sm text-blue-600 font-medium hover:underline">Start Browsing</button>
      </div>

      <div v-else class="flex-1 overflow-y-auto p-4 space-y-4">
        <div 
          v-for="(item, index) in cart.items" 
          :key="index"
          class="flex gap-4 border-b border-gray-100 pb-4 last:border-0"
        >
          <div class="w-16 h-16 bg-gray-100 rounded-lg flex-shrink-0 overflow-hidden border border-gray-200 relative">
            <img v-if="item.image" :src="item.image" loading="lazy" class="w-full h-full object-cover">
            <div v-else class="w-full h-full flex items-center justify-center text-xs text-gray-400">No Img</div>
            
            <div v-if="item.qty > 1" class="absolute bottom-0 right-0 bg-black text-white text-[10px] font-bold px-1.5 py-0.5 rounded-tl-md">
                x{{ item.qty }}
            </div>
          </div>

          <div class="flex-1 min-w-0">
            <h3 class="text-sm font-bold text-gray-900 truncate">{{ item.item_name }}</h3>
            <p class="text-xs text-gray-500 truncate">{{ item.item_code }}</p>
            
            <div class="flex items-center gap-2 mt-1">
              <span class="text-[10px] uppercase font-bold bg-yellow-100 text-yellow-800 px-1.5 py-0.5 rounded">{{ item.metal }}</span>
              <span class="text-[10px] uppercase font-bold bg-gray-100 text-gray-800 px-1.5 py-0.5 rounded">{{ item.purity }}</span>
            </div>
            
            <div class="mt-2 flex items-center justify-between">
              <div class="flex flex-col">
                  <span class="text-xs text-gray-400">{{ formatCurrency(item.amount) }} ea</span>
                  <span class="font-mono text-sm font-bold text-gray-900">
                    {{ formatCurrency(item.amount * item.qty) }}
                  </span>
              </div>

              <button 
                @click="cart.removeItem(index)"
                class="text-red-400 hover:text-red-600 p-1 hover:bg-red-50 rounded transition-colors"
                title="Remove Item"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="cart.items.length > 0" class="p-6 bg-gray-50 border-t border-gray-200">
        <div class="space-y-2 mb-4 text-sm">
          <div class="flex justify-between text-gray-600">
            <span>Subtotal</span>
            <span>{{ formatCurrency(cart.subtotal) }}</span>
          </div>
          <div class="flex justify-between text-gray-600">
            <span>Tax (Est. 8.875%)</span>
            <span>{{ formatCurrency(cart.tax) }}</span>
          </div>
          <div class="flex justify-between text-lg font-bold text-gray-900 pt-2 border-t border-gray-200">
            <span>Total</span>
            <span>{{ formatCurrency(cart.grandTotal) }}</span>
          </div>
        </div>
        
        <button class="w-full bg-gray-900 text-white py-3 rounded-lg font-bold shadow-lg hover:bg-gray-800 active:scale-95 transition-all">
          Checkout
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cart.js'

// We receive 'isOpen' from the parent (AppLayout/AppHeader)
const props = defineProps(['isOpen'])
const emit = defineEmits(['close'])

const cart = useCartStore()

function close() {
  emit('close')
}

function formatCurrency(val) {
  if (!val) return '$0.00'
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val)
}
</script>