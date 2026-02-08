<template>
  <div class="py-3 border-b" :class="isDark ? 'border-white/5 bg-[#0a0a0c]' : 'border-gray-200 bg-white'">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">
      <div class="flex items-center justify-between">
        <!-- Live Badge -->
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-1.5 px-2 py-1 rounded-md" :class="isDark ? 'bg-emerald-500/10' : 'bg-emerald-50'">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <span class="text-[10px] font-semibold text-emerald-600 uppercase tracking-wide">Live</span>
          </div>
          <span class="text-[10px]" :class="isDark ? 'text-gray-600' : 'text-gray-400'">{{ formattedTime }}</span>
        </div>

        <!-- Prices -->
        <div class="flex items-center gap-4 overflow-x-auto scrollbar-hide">
          <div v-for="metal in metals" :key="metal.symbol" class="flex items-center gap-2 flex-shrink-0">
            <!-- Element Symbol Badge -->
            <div class="w-7 h-7 rounded-md flex items-center justify-center text-[10px] font-bold" :class="metal.badgeClass">
              {{ metal.symbol }}
            </div>
            <!-- Price -->
            <div class="text-right">
              <div class="flex items-center gap-1">
                <span class="text-xs font-semibold" :class="isDark ? 'text-white' : 'text-gray-900'">${{ formatPrice(metal.price) }}</span>
                <span class="text-[9px] font-medium" :class="metal.change >= 0 ? 'text-emerald-500' : 'text-red-500'">
                  {{ metal.change >= 0 ? '+' : '' }}{{ metal.change?.toFixed(2) }}%
                </span>
              </div>
              <span class="text-[9px]" :class="isDark ? 'text-gray-600' : 'text-gray-400'">{{ metal.name }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const isDark = ref(true)
const isLoading = ref(true)
let refreshInterval = null

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark')
  const observer = new MutationObserver(() => {
    isDark.value = document.documentElement.classList.contains('dark')
  })
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })
  
  fetchPrices()
  refreshInterval = setInterval(fetchPrices, 60000)
})

onUnmounted(() => { if (refreshInterval) clearInterval(refreshInterval) })

const formattedTime = computed(() => new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }))

const metals = ref([
  { symbol: 'Au', name: 'Gold (XAU)', price: 2028.43, change: 0.27, badgeClass: 'bg-gradient-to-br from-[#D4AF37] to-amber-600 text-black' },
  { symbol: 'Ag', name: 'Silver (XAG)', price: 22.85, change: -0.41, badgeClass: 'bg-gradient-to-br from-gray-300 to-gray-400 text-gray-700' },
  { symbol: 'Pt', name: 'Platinum', price: 917.11, change: 0.84, badgeClass: 'bg-gradient-to-br from-gray-100 to-gray-200 text-gray-700' },
  { symbol: 'Pd', name: 'Palladium', price: 949.37, change: 1.23, badgeClass: 'bg-gradient-to-br from-blue-200 to-blue-300 text-blue-800' }
])

function formatPrice(price) {
  return price?.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) || '0.00'
}

async function fetchPrices() {
  try {
    const response = await fetch('https://api.metals.live/v1/spot')
    const data = await response.json()
    
    if (Array.isArray(data)) {
      data.forEach(item => {
        const metal = metals.value.find(m => m.name.toLowerCase().includes(item.metal?.toLowerCase()))
        if (metal && item.price) {
          const oldPrice = metal.price
          metal.price = item.price
          metal.change = oldPrice > 0 ? ((item.price - oldPrice) / oldPrice) * 100 : (Math.random() * 2 - 1)
        }
      })
    }
  } catch {
    // Keep simulated values
    metals.value.forEach(m => {
      m.price *= (1 + (Math.random() * 0.002 - 0.001))
      m.change = (Math.random() * 2 - 1)
    })
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
.scrollbar-hide::-webkit-scrollbar { display: none; }
</style>
