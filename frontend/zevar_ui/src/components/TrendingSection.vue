<template>
  <section class="px-4 sm:px-6 py-3 overflow-x-hidden">
    <!-- Header - Compact -->
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-lg flex items-center justify-center" style="background: linear-gradient(135deg, #C9A962 0%, #8B7355 100%);">
          <svg class="w-3.5 h-3.5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h2 class="text-sm font-semibold flex items-center gap-1.5" :class="isDark ? 'text-white' : 'text-gray-900'">
          Trending
          <span class="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span>
        </h2>
      </div>
      
      <button @click="refreshTrending" class="w-6 h-6 rounded flex items-center justify-center transition-all hover:scale-105" :class="[isDark ? 'hover:bg-white/5' : 'hover:bg-gray-100', isRefreshing ? 'animate-spin' : '']">
        <svg class="w-3.5 h-3.5" :class="isDark ? 'text-gray-500' : 'text-gray-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
        </svg>
      </button>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="flex justify-center py-6">
      <div class="w-5 h-5 border-2 border-[#C9A962] border-t-transparent rounded-full animate-spin"></div>
    </div>

    <!-- Empty -->
    <div v-else-if="displayItems.length === 0" class="text-center py-6 rounded-lg border" :class="isDark ? 'bg-[#12121a] border-white/5' : 'bg-gray-50 border-gray-200'">
      <p class="text-xs" :class="isDark ? 'text-gray-500' : 'text-gray-500'">No trending items</p>
    </div>

    <!-- Carousel -->
    <div v-else class="relative -mx-4 sm:-mx-6">
      <!-- Left Arrow -->
      <button 
        @click="scrollLeft" 
        class="absolute left-2 sm:left-3 top-1/2 -translate-y-1/2 z-20 w-8 h-8 rounded-full flex items-center justify-center transition-all hover:scale-110"
        :class="isDark ? 'bg-black/80 text-white border border-white/20' : 'bg-white text-gray-700 border border-gray-200 shadow-md'"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </button>
      
      <!-- Right Arrow -->
      <button 
        @click="scrollRight" 
        class="absolute right-2 sm:right-3 top-1/2 -translate-y-1/2 z-20 w-8 h-8 rounded-full flex items-center justify-center transition-all hover:scale-110"
        :class="isDark ? 'bg-black/80 text-white border border-white/20' : 'bg-white text-gray-700 border border-gray-200 shadow-md'"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
      </button>

      <!-- Scrollable Items -->
      <div 
        ref="carouselRef" 
        class="flex gap-3 px-12 sm:px-14 py-1 pb-3 overflow-x-scroll scrollbar-gold"
        style="scroll-behavior: smooth; -webkit-overflow-scrolling: touch;"
      >
        <div 
          v-for="(item, index) in displayItems" 
          :key="item.id"
          @click="$emit('viewItem', item)"
          class="flex-none w-36 group cursor-pointer"
        >
          <div 
            class="rounded-lg overflow-hidden border transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md"
            :class="isDark 
              ? 'bg-[#111113] border-white/5 hover:border-[#C9A962]/30' 
              : 'bg-white border-gray-100 hover:border-[#C9A962]/50'"
          >
            <!-- Image -->
            <div class="relative aspect-square overflow-hidden" :class="isDark ? 'bg-[#0a0a0c]' : 'bg-gray-50'">
              <!-- Rank -->
              <div class="absolute top-1 left-1 z-10 w-4 h-4 rounded flex items-center justify-center text-[9px] font-bold" :class="isDark ? 'bg-black/60 text-[#C9A962]' : 'bg-white/80 text-[#8B7355]'">
                {{ index + 1 }}
              </div>
              <!-- HOT -->
              <div v-if="item.is_hot" class="absolute top-1.5 right-1.5 z-10 px-1.5 py-0.5 rounded-md text-[8px] font-bold text-white shadow-sm" style="background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);">🔥 HOT</div>
              
              <img v-if="item.image" :src="item.image" :alt="item.name" class="w-full h-full object-cover group-hover:scale-103 transition-transform duration-300" loading="lazy" @error="e => e.target.style.display='none'"/>
              <div v-else class="w-full h-full flex items-center justify-center">
                <svg class="w-6 h-6" :class="isDark ? 'text-gray-800' : 'text-gray-200'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
              </div>
            </div>
            
            <!-- Content -->
            <div class="p-2">
              <p class="text-[8px] font-medium text-[#C9A962]">{{ item.category }}</p>
              <h3 class="font-medium text-[11px] truncate" :class="isDark ? 'text-white' : 'text-gray-900'">{{ item.name }}</h3>
              <p class="text-xs font-semibold mt-0.5" :class="isDark ? 'text-white' : 'text-gray-900'">{{ item.price }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  category: { type: String, default: 'all' },
  categoryLabel: { type: String, default: 'All' }
})

defineEmits(['resetCategory'])

const carouselRef = ref(null)
const isRefreshing = ref(false)
const isLoading = ref(true)
const isUsingBackend = ref(false)
const backendItems = ref([])
const isDark = ref(true)
let refreshInterval = null

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark')
  const observer = new MutationObserver(() => {
    isDark.value = document.documentElement.classList.contains('dark')
  })
  observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] })
  
  fetchTrendingItems()
  refreshInterval = setInterval(fetchTrendingItems, 3600000)
})

onUnmounted(() => { if (refreshInterval) clearInterval(refreshInterval) })

const formattedTime = computed(() => new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }))

// No sample items - using backend data only
const sampleItems = []

const displayItems = computed(() => {
  const items = backendItems.value
  if (props.category && props.category !== 'all') return items.filter(item => item.categoryId === props.category)
  return items
})

async function fetchTrendingItems() {
  isLoading.value = true
  try {
    const response = await fetch('/api/method/zevar_core.api.get_trending_items', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': window.csrf_token || '' },
      body: JSON.stringify({ category: props.category, limit: 20 })
    })
    const data = await response.json()
    if (data.message?.status === 'success' && data.message.items?.length > 0) {
      backendItems.value = data.message.items
      isUsingBackend.value = true
    } else {
      isUsingBackend.value = false
    }
  } catch { isUsingBackend.value = false }
  finally { isLoading.value = false }
}

async function trackClick(itemId) {
  if (!isUsingBackend.value) return
  try {
    await fetch('/api/method/zevar_core.api.track_trending_click', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': window.csrf_token || '' },
      body: JSON.stringify({ item_id: itemId })
    })
  } catch {}
}

function scrollLeft() { carouselRef.value?.scrollBy({ left: -260, behavior: 'smooth' }) }
function scrollRight() { carouselRef.value?.scrollBy({ left: 260, behavior: 'smooth' }) }

function refreshTrending() {
  isRefreshing.value = true
  fetchTrendingItems().finally(() => setTimeout(() => isRefreshing.value = false, 500))
}

watch(() => props.category, fetchTrendingItems)
</script>

<style scoped>
/* Visible gold scrollbar */
.scrollbar-gold {
  scrollbar-width: thin;
  scrollbar-color: #C9A962 rgba(201,169,98,0.15);
}
.scrollbar-gold::-webkit-scrollbar {
  height: 6px;
}
.scrollbar-gold::-webkit-scrollbar-track {
  background: rgba(201,169,98,0.1);
  border-radius: 3px;
  margin: 0 48px;
}
.scrollbar-gold::-webkit-scrollbar-thumb {
  background: linear-gradient(90deg, #C9A962, #8B7355);
  border-radius: 3px;
}
.scrollbar-gold::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(90deg, #b89d52, #7a6448);
}
</style>
