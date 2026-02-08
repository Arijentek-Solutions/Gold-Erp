<template>
  <div :key="themeKey" class="min-h-screen transition-colors duration-300" :style="{ backgroundColor: isDark ? '#08080a' : '#ffffff' }">
    
    <Header 
      :isDark="isDark" 
      :activeCategory="activeCategory"
      @toggleTheme="toggleTheme"
      @search="performSearch"
      @selectCategory="handleCategorySelect"
      @selectOccasion="handleOccasionSelect"
    />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3">
      <div class="flex items-center gap-3">
        <button 
          @click="showPromoBanner = !showPromoBanner"
          class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium border transition-all"
          :class="showPromoBanner 
            ? 'bg-[#C9A962] text-black border-[#C9A962] hover:bg-[#b89d52]' 
            : (isDark ? 'bg-transparent text-gray-400 border-white/10 hover:border-[#C9A962]/50' : 'bg-transparent text-gray-600 border-gray-200 hover:border-[#C9A962]')"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
          {{ showPromoBanner ? 'Hide Promo Banner' : 'Show Promo Banner' }}
        </button>
        
        <button 
          @click="showPartnerItems = !showPartnerItems"
          class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium border transition-all"
          :class="showPartnerItems 
            ? 'bg-purple-600 text-white border-purple-600 hover:bg-purple-700' 
            : (isDark ? 'bg-transparent text-gray-400 border-white/10 hover:border-purple-500/50' : 'bg-transparent text-gray-600 border-gray-200 hover:border-purple-500')"
        >
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
          </svg>
          {{ showPartnerItems ? 'Hide Partner Catalog' : 'Show Partner Catalog' }}
        </button>
        <span class="text-xs" :class="isDark ? 'text-gray-600' : 'text-gray-400'">Demo toggles for clients</span>
      </div>
    </div>

    <div v-if="showPromoBanner" class="max-w-7xl mx-auto px-4 sm:px-6 pb-6">
      <PromoBanner :isDark="isDark" />
    </div>

    <main class="relative z-10">
      <section class="relative overflow-hidden" style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24">
          <div class="grid md:grid-cols-2 gap-12 items-center">
            <div class="text-left z-10">
              <p class="text-xs font-medium tracking-[0.3em] uppercase mb-4 text-[#C9A962]">Timeless Elegance</p>
              <h1 class="text-4xl sm:text-5xl lg:text-6xl font-serif font-bold mb-6 leading-tight text-white">
                Discover Beauty <span class="block text-[#C9A962] mt-2">Crafted for You</span>
              </h1>
              <p class="text-lg text-gray-300 mb-8 max-w-md leading-relaxed">
                Explore our curated collection of exquisite diamonds, gold jewelry, and timeless pieces.
              </p>
              <div class="flex flex-wrap gap-4">
                <button @click="scrollToSection('trending')" class="px-8 py-4 bg-[#C9A962] text-black font-bold rounded-lg hover:bg-[#b89d52] transition-all shadow-lg hover:shadow-xl transform hover:-translate-y-0.5">Shop Collection</button>
                <button class="px-8 py-4 border-2 border-white/20 text-white font-bold rounded-lg hover:bg-white/10 transition-all">Book Appointment</button>
              </div>
            </div>
            
            <div class="relative">
              <img src="https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=800&q=80" alt="Jewelry Collection" class="rounded-2xl shadow-2xl w-full aspect-[4/5] object-cover" />
              <div class="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent rounded-2xl"></div>
            </div>
          </div> </div> </section>

      <section id="trending" class="py-16" :style="{ backgroundColor: isDark ? '#0a0a0c' : '#faf9f7' }">
        <div class="max-w-7xl mx-auto px-4 sm:px-6">
          <div class="text-center mb-12">
            <p class="text-xs tracking-[0.3em] uppercase mb-2" :class="isDark ? 'text-[#C9A962]' : 'text-[#8B7355]'">Trending Now</p>
            <h2 class="text-3xl sm:text-4xl font-serif font-bold" :class="isDark ? 'text-white' : 'text-gray-900'">Jewelry Inspired by Your Style</h2>
          </div>
          <TrendingSection :category="activeCategory" :categoryLabel="activeCategoryLabel" @resetCategory="activeCategory = 'all'" @viewItem="openProduct" />
        </div>
      </section>

      <section class="py-16" :style="{ backgroundColor: isDark ? '#08080a' : '#ffffff' }">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 space-y-20">
          
          <div v-if="activeCategory === 'all' || activeCategory === 'rings'" class="space-y-8">
            <div class="flex items-center justify-between">
              <h3 class="text-2xl sm:text-3xl font-serif font-bold" :class="isDark ? 'text-white' : 'text-gray-900'">Rings</h3>
              <button @click="handleCategorySelect('rings')" class="text-[#C9A962] hover:underline">View All</button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div class="hidden lg:block relative rounded-2xl overflow-hidden aspect-[3/4]">
                <img src="https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=600&q=80" class="w-full h-full object-cover" />
              </div>
              <JewelryProductCard v-for="item in ringsItems.slice(0, 3)" :key="item.item_code" :product="item" :is-dark="isDark" @view="openProduct" />
            </div>
          </div>

          <div v-if="activeCategory === 'all' || activeCategory === 'earrings'" class="space-y-8">
            <div class="flex items-center justify-between">
              <h3 class="text-2xl sm:text-3xl font-serif font-bold" :class="isDark ? 'text-white' : 'text-gray-900'">Earrings</h3>
              <button @click="handleCategorySelect('earrings')" class="text-[#C9A962] hover:underline">View All</button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <JewelryProductCard v-for="item in earringsItems.slice(0, 3)" :key="item.item_code" :product="item" :is-dark="isDark" @view="openProduct" />
              <div class="hidden lg:block relative rounded-2xl overflow-hidden aspect-[3/4]">
                <img src="https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=600&q=80" class="w-full h-full object-cover" />
              </div>
            </div>
          </div>

          <div v-if="activeCategory === 'all' || activeCategory === 'chains'" class="space-y-8">
            <div class="flex items-center justify-between">
              <h3 class="text-2xl sm:text-3xl font-serif font-bold" :class="isDark ? 'text-white' : 'text-gray-900'">Chains & Necklaces</h3>
              <button @click="handleCategorySelect('chains')" class="text-[#C9A962] hover:underline">View All</button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div class="hidden lg:block relative rounded-2xl overflow-hidden aspect-[3/4]">
                <img src="https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=600&q=80" class="w-full h-full object-cover" />
              </div>
              <JewelryProductCard v-for="item in chainsItems.slice(0, 3)" :key="item.item_code" :product="item" :is-dark="isDark" @view="openProduct" />
            </div>
          </div>
        </div>
      </section>

      <section v-if="showPartnerItems" class="py-16 border-t" :class="isDark ? 'bg-[#0a0a0c] border-white/5' : 'bg-gray-50 border-gray-200'">
        <div class="max-w-7xl mx-auto px-4 sm:px-6">
          <div class="text-center mb-12">
            <h2 class="text-3xl font-serif font-bold text-white">Explore Our Partners</h2>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
            <JewelryProductCard v-for="item in partnerItems.slice(0, 10)" :key="item.item_code" :product="item" :is-dark="isDark" :show-partner-badge="true" @view="openProduct" />
          </div>
        </div>
      </section>

      <footer class="py-12 border-t" :class="isDark ? 'bg-[#0a0a0c] border-white/5' : 'bg-white border-gray-100'">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 text-center">
          <p class="text-xs text-gray-500">© {{ new Date().getFullYear() }} ZEVAR Jewelers. All rights reserved.</p>
        </div>
      </footer>
    </main>

    <ProductModal :show="showProductModal" :item-code="selectedItemCode" @close="showProductModal = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import Header from '@/components/Header.vue'
import TrendingSection from '@/components/TrendingSection.vue'
import PromoBanner from '@/components/PromoBanner.vue'
import JewelryProductCard from '@/components/JewelryProductCard.vue'
import ProductModal from '@/components/ProductModal.vue'
import { createResource } from 'frappe-ui'

// Theme
const isDark = ref(true)
const themeKey = ref(0)
const showPromoBanner = ref(false)
const showPartnerItems = ref(true) // Default ON so client can evaluate
const showProductModal = ref(false)
const selectedItemCode = ref(null)

// Catalog Data
const allItems = ref([])
const loading = ref(false)

// Filters
const activeCategory = ref('all')
const activeCategoryLabel = computed(() => {
  const catMap = {
    'all': 'All Jewelry',
    'rings': 'Rings',
    'chains': 'Chains',
    'earrings': 'Earrings',
    'bracelets': 'Bracelets',
    'pendants': 'Pendants',
    'watches': 'Watches'
  }
  return catMap[activeCategory.value] || 'All Jewelry'
})
const lastSearchQuery = ref('')

// Category-wise items (computed from allItems) - IN-STORE PRIORITY
const ringsItems = computed(() => allItems.value.filter(i => 
  (i.jewelry_type === 'Rings' || i.item_group === 'Rings') && (i.stock_qty > 0 || !i.custom_source || i.custom_source === 'JCSWIN')
))
const earringsItems = computed(() => allItems.value.filter(i => 
  (i.jewelry_type === 'Earrings' || i.item_group === 'Earrings') && (i.stock_qty > 0 || !i.custom_source || i.custom_source === 'JCSWIN')
))
const chainsItems = computed(() => allItems.value.filter(i => 
  (i.jewelry_type === 'Chains' || i.jewelry_type === 'Necklaces' || i.item_group === 'Chains') && (i.stock_qty > 0 || !i.custom_source || i.custom_source === 'JCSWIN')
))
const braceletsItems = computed(() => allItems.value.filter(i => 
  (i.jewelry_type === 'Bracelets' || i.item_group === 'Bracelets') && (i.stock_qty > 0 || !i.custom_source || i.custom_source === 'JCSWIN')
))
const pendantsItems = computed(() => allItems.value.filter(i => 
  (i.jewelry_type === 'Pendants' || i.item_group === 'Pendants') && (i.stock_qty > 0 || !i.custom_source || i.custom_source === 'JCSWIN')
))

// Partner items (custom_source from external partners, not in stock)
const partnerItems = computed(() => 
  allItems.value.filter(i => 
    i.custom_source && ['QGold', 'Stuller', 'Demo'].includes(i.custom_source) && i.stock_qty === 0
  )
)

onMounted(() => {
  const stored = localStorage.getItem('zevar-theme')
  if (stored) {
    isDark.value = stored === 'dark'
  } else {
    isDark.value = true
    localStorage.setItem('zevar-theme', 'dark')
  }
  updateDocumentClass()
  fetchAllItems()
})

// Fetch all items at once (better for category showcase)
const itemsFetcher = createResource({
  url: 'zevar_core.api.get_pos_items',
  makeParams() {
    const filters = {}
    
    if (lastSearchQuery.value) {
      // Apply search filter
    }

    return {
      start: 0,
      page_length: 100, // Fetch more for showcase
      search_term: lastSearchQuery.value,
      filters: JSON.stringify(filters),
      in_stock_only: false, // Show all items including partner catalog
      source_filter: null // No source restriction for main view
    }
  },
  onSuccess(data) {
    allItems.value = data || []
    loading.value = false
  }
})

// Separate fetcher for in-stock only items (for "Available Now" section)
const inStockFetcher = createResource({
  url: 'zevar_core.api.get_pos_items',
  makeParams() {
    return {
      start: 0,
      page_length: 50,
      in_stock_only: true, // Only in-stock items
      source_filter: null
    }
  },
  onSuccess(data) {
    // Update allItems with proper in-stock flag
    if (data) {
      data.forEach(item => {
        item.in_store = true
      })
      allItems.value = [...data, ...allItems.value.filter(i => !data.find(d => d.item_code === i.item_code))]
    }
  }
})

function fetchAllItems() {
  loading.value = true
  itemsFetcher.fetch()
}

function handleCategorySelect(categoryId) {
  activeCategory.value = categoryId
  scrollToSection('collection')
}

function performSearch(query) {
  lastSearchQuery.value = query
  fetchAllItems()
}

function openProduct(item) {
  selectedItemCode.value = item.item_code
  showProductModal.value = true
}

function scrollToSection(id) {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

function toggleTheme() {
  isDark.value = !isDark.value
  localStorage.setItem('zevar-theme', isDark.value ? 'dark' : 'light')
  updateDocumentClass()
  themeKey.value++
}

function updateDocumentClass() {
  document.documentElement.classList.toggle('dark', isDark.value)
  document.body.style.backgroundColor = isDark.value ? '#08080a' : '#ffffff'
}

function handleOccasionSelect(occasionId) {
  // Future: Filter by occasion tags
  console.log('Selected occasion:', occasionId)
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
