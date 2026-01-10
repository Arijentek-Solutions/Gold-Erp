<template>
  <Transition name="fade">
    <div v-if="show" class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
      
      <div @click="close" class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity"></div>

      <div class="relative bg-white dark:bg-[#1a1c23] rounded-2xl shadow-2xl w-full overflow-hidden flex flex-col md:flex-row transition-all duration-500 ease-in-out border border-transparent dark:border-white/10"
           :class="step === 'success' ? 'max-w-md' : 'max-w-3xl h-[600px]'">
        
        <template v-if="step === 'review'">
            <div class="w-full md:w-1/2 bg-gray-50 dark:bg-[#15171e] p-6 border-r border-gray-100 dark:border-white/5 flex flex-col">
                <h3 class="text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-4">Items in Bag</h3>
                
                <div class="flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar">
                    <div v-for="item in cart.items" :key="item.item_code" class="flex justify-between items-center bg-white dark:bg-[#0F1115] p-3 rounded-lg border border-gray-100 dark:border-white/5 shadow-sm">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 bg-gray-100 dark:bg-gray-800 rounded-md overflow-hidden flex-shrink-0">
                                <img v-if="item.image" :src="item.image" class="w-full h-full object-cover">
                            </div>
                            <div class="min-w-0">
                                <div class="font-bold text-gray-900 dark:text-white text-sm line-clamp-1">{{ item.item_name }}</div>
                                <div class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ item.item_code }}</div>
                            </div>
                        </div>
                        <div class="text-right flex-shrink-0">
                             <div class="font-mono font-bold text-sm text-gray-900 dark:text-gray-200">{{ formatCurrency(item.amount * item.qty) }}</div>
                             <div class="text-[10px] text-gray-400">Qty: {{ item.qty }}</div>
                        </div>
                    </div>
                </div>

                <div class="mt-4 space-y-2 pt-4 border-t border-gray-200 dark:border-white/10">
                    <div class="flex justify-between text-sm text-gray-500 dark:text-gray-400">
                        <span>Subtotal</span>
                        <span>{{ formatCurrency(cart.subtotal) }}</span>
                    </div>
                    <div class="flex justify-between text-sm text-gray-500 dark:text-gray-400">
                        <span>Tax ({{ cart.taxRate }}%)</span>
                        <span>{{ formatCurrency(cart.tax) }}</span>
                    </div>
                    <div class="flex justify-between text-2xl font-bold text-gray-900 dark:text-white pt-2 border-t border-gray-200 dark:border-white/10 mt-2">
                        <span>Total</span>
                        <span>{{ formatCurrency(cart.grandTotal) }}</span>
                    </div>
                </div>
            </div>

            <div class="w-full md:w-1/2 p-8 flex flex-col bg-white dark:bg-[#1a1c23] relative">
                <button @click="close" class="absolute top-4 right-4 p-2 hover:bg-gray-100 dark:hover:bg-white/10 rounded-full transition">
                    <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>

                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-1">Checkout</h2>
                <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">Select a payment method to complete the order.</p>

                <div class="space-y-3 flex-1">
                    <button 
                        @click="paymentMethod = 'Cash'"
                        class="w-full flex items-center justify-between p-4 border rounded-xl transition-all group relative overflow-hidden"
                        :class="paymentMethod === 'Cash' 
                            ? 'border-gray-900 bg-gray-50 ring-1 ring-gray-900 dark:border-[#D4AF37] dark:bg-[#D4AF37]/10 dark:ring-[#D4AF37]' 
                            : 'border-gray-200 hover:border-gray-900 dark:border-white/10 dark:hover:border-white/30'"
                    >
                        <div class="flex items-center gap-4 z-10">
                            <div class="w-10 h-10 rounded-full bg-green-100 text-green-600 flex items-center justify-center">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                            </div>
                            <div class="text-left">
                                <div class="font-bold text-gray-900 dark:text-white">Cash</div>
                                <div class="text-xs text-gray-500 dark:text-gray-400">Walk-in Customer</div>
                            </div>
                        </div>
                        <div v-if="paymentMethod === 'Cash'" class="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]"></div>
                    </button>

                    <button 
                        @click="paymentMethod = 'Card Terminal'"
                        class="w-full flex items-center justify-between p-4 border rounded-xl transition-all group relative overflow-hidden"
                        :class="paymentMethod === 'Card Terminal' 
                            ? 'border-gray-900 bg-gray-50 ring-1 ring-gray-900 dark:border-[#D4AF37] dark:bg-[#D4AF37]/10 dark:ring-[#D4AF37]' 
                            : 'border-gray-200 hover:border-gray-900 dark:border-white/10 dark:hover:border-white/30'"
                    >
                         <div class="flex items-center gap-4 z-10">
                            <div class="w-10 h-10 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"></path></svg>
                            </div>
                            <div class="text-left">
                                <div class="font-bold text-gray-900 dark:text-white">Card Terminal</div>
                                <div class="text-xs text-gray-500 dark:text-gray-400">Square</div>
                            </div>
                        </div>
                         <div v-if="paymentMethod === 'Card Terminal'" class="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]"></div>
                    </button>
                </div>

                <button 
                    @click="handlePayment"
                    :disabled="!paymentMethod || processing"
                    class="w-full mt-6 py-4 rounded-xl font-bold text-lg shadow-xl transition-all flex items-center justify-center gap-2 transform active:scale-95"
                    :class="!paymentMethod || processing 
                        ? 'bg-gray-100 text-gray-400 cursor-not-allowed dark:bg-white/5 dark:text-gray-600' 
                        : 'bg-gray-900 text-white hover:bg-black dark:bg-[#D4AF37] dark:text-black dark:hover:bg-[#b5952f]'"
                >
                    <span v-if="processing" class="animate-spin rounded-full h-5 w-5 border-2 border-gray-400 border-t-white"></span>
                    <span v-else-if="!paymentMethod">Select Payment Method</span>
                    <span v-else>Confirm {{ formatCurrency(cart.grandTotal) }}</span>
                </button>
            </div>
        </template>

        <template v-else-if="step === 'success'">
            <div class="p-10 flex flex-col items-center justify-center text-center w-full bg-white dark:bg-[#1a1c23]">
                <div class="w-20 h-20 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mb-6 animate-bounce-short">
                    <svg class="w-10 h-10 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path></svg>
                </div>
                <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Payment Successful!</h2>
                <p class="text-gray-500 dark:text-gray-400 mb-8">Invoice has been generated in ERPNext.</p>
                
                <div class="bg-gray-50 dark:bg-[#15171e] rounded-xl p-4 w-full mb-6 border border-gray-100 dark:border-white/5">
                    <div class="flex justify-between text-sm mb-2">
                        <span class="text-gray-500 dark:text-gray-400">Transaction ID</span>
                        <span class="font-mono font-bold text-gray-900 dark:text-white">{{ lastOrderId || 'POS-2025-001' }}</span>
                    </div>
                    <div class="flex justify-between text-sm">
                        <span class="text-gray-500 dark:text-gray-400">Amount Paid</span>
                        <span class="font-mono font-bold text-green-600 dark:text-green-400">{{ formatCurrency(cart.grandTotal) }}</span>
                    </div>
                </div>

                <div class="flex gap-3 w-full">
                    <button @click="close" class="flex-1 py-3 rounded-lg font-bold text-gray-700 bg-gray-100 hover:bg-gray-200 dark:bg-white/5 dark:text-gray-300 dark:hover:bg-white/10 transition">
                        New Order
                    </button>
                    <button class="flex-1 py-3 rounded-lg font-bold text-white bg-gray-900 hover:bg-black dark:bg-[#D4AF37] dark:text-black dark:hover:bg-[#b5952f] transition flex items-center justify-center gap-2">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2-4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
                        Print Receipt
                    </button>
                </div>
            </div>
        </template>

      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useCartStore } from '@/stores/cart.js'

const props = defineProps(['show'])
const emit = defineEmits(['close'])
const cart = useCartStore()

const paymentMethod = ref('') 
const processing = ref(false)
const step = ref('review') // 'review' | 'success'
const lastOrderId = ref(null)

// Reset state when modal opens
watch(() => props.show, (isOpen) => {
    if (isOpen) {
        step.value = 'review'
        paymentMethod.value = ''
        processing.value = false
    }
})

async function handlePayment() {
  if (!paymentMethod.value) return 
  
  processing.value = true
  try {
    const result = await cart.submitOrder(paymentMethod.value)
    // Extract Order ID from response if available
    if(result && result.data && result.data.name) {
        lastOrderId.value = result.data.name
    }
    
    // Switch to Success View
    step.value = 'success'
    
  } catch (e) {
    alert("Order failed: " + e.message)
  } finally {
    processing.value = false
  }
}

function close() {
    emit('close')
    // Reset cart if we finished a sale
    if (step.value === 'success') {
        cart.clearCart()
    }
}

function formatCurrency(val) {
  if (!val) return '$0.00'
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val)
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.animate-bounce-short {
  animation: bounce 0.5s ease-in-out 1;
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: #f9fafb; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 4px; }
/* Dark Mode Scrollbar */
.dark .custom-scrollbar::-webkit-scrollbar-track { background: #15171e; }
.dark .custom-scrollbar::-webkit-scrollbar-thumb { background: #333; }
</style>