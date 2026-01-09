<script setup>
import AppLayout from '@/components/AppLayout.vue'
import ItemCard from '@/components/ItemCard.vue'
import ProductModal from '@/components/ProductModal.vue'
import { useSessionStore } from '@/stores/session.js'
import { useUIStore } from '@/stores/ui.js' // Import UI Store
import { createResource } from 'frappe-ui'
import { watch, ref } from 'vue'

const session = useSessionStore()
const ui = useUIStore() // Use the store

// Modal State
const showModal = ref(false)
const selectedItemCode = ref(null)

// Data State
const catalog = ref([]) 
const start = ref(0)
const PAGE_LENGTH = 20
const hasMore = ref(true)

// 1. Fetch Items
const items = createResource({
  url: 'zevar_core.api.get_pos_items', 
  makeParams() {
    return {
      warehouse: session.currentWarehouse,
      page_length: PAGE_LENGTH,
      start: start.value,
      // FIX: Read directly from the UI Store, not local vars
      search_term: ui.searchQuery,
      filters: JSON.stringify(ui.activeFilters)
    }
  },
  onSuccess(data) {
    if (data.length < PAGE_LENGTH) {
      hasMore.value = false
    }
    if (start.value === 0) {
      catalog.value = data
    } else {
      catalog.value.push(...data)
    }
  }
})

// 2. Actions
function loadMore() {
  if (!hasMore.value || items.loading) return
  start.value += PAGE_LENGTH
  items.fetch()
}

// FIX: We don't need handleFilterUpdate anymore because the Store handles it!

function openItemDetails(itemCode) {
  selectedItemCode.value = itemCode
  showModal.value = true
}

// Watchers
let searchTimeout = null

// FIX: Watch the UI STORE for changes (Search or Filters)
watch(() => [ui.searchQuery, ui.activeFilters], () => {
    if (searchTimeout) clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
        start.value = 0
        hasMore.value = true
        items.fetch()
    }, 400) // Debounce search
}, { deep: true })

// Watch: Warehouse changes
watch(
  () => session.currentWarehouse, 
  (newVal) => {
    if (newVal) {
      // items.fetch() will be triggered by the watcher above if needed, 
      // or we call it directly here if store is static.
      start.value = 0
      items.fetch()
    } else {
      catalog.value = []
    }
  },
  { immediate: true }
)
</script>

<template>
  <AppLayout>
    <div v-if="!session.currentWarehouse" class="h-full flex flex-col items-center justify-center text-center opacity-50">
       <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mb-4">
          <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
       </div>
       <h3 class="text-lg font-bold text-gray-900 dark:text-white">Select Store Location</h3>
       <p class="text-sm text-gray-500">Choose a location from the top menu to view inventory.</p>
    </div>

    <div v-else class="h-full flex flex-col">
      
        <div class="flex items-center gap-4 mb-6">
            <h2 class="text-2xl font-serif font-bold text-gray-900 dark:text-white transition-colors">Collection</h2>
            
            <span class="text-xs font-bold uppercase tracking-widest text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 px-3 py-1 rounded-full shadow-sm border border-gray-100 dark:border-gray-700 transition-colors">
                {{ catalog.length }} Items Found
            </span>
        </div>

        <div class="flex-1 overflow-y-auto pb-20 pr-2 custom-scrollbar">
            
            <div v-if="items.loading && start === 0" class="py-20 text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-2 border-gray-900 dark:border-white border-t-transparent mx-auto mb-4"></div>
                <span class="text-gray-400 text-sm font-medium">Curating Collection...</span>
            </div>

            <div v-else-if="catalog.length === 0" class="py-20 text-center bg-white dark:bg-gray-900 rounded-2xl border border-dashed border-gray-200 dark:border-gray-700">
                <p class="text-gray-500">No pieces found matching your criteria.</p>
            </div>

            <div v-else class="smart-grid">
                <div 
                v-for="item in catalog" 
                :key="item.item_code"
                @click="openItemDetails(item.item_code)"
                class="group"
                >
                <ItemCard :item="item" />
                </div>
            </div>

            <div v-if="hasMore && catalog.length > 0" class="flex justify-center pt-12 pb-12">
                <button 
                    @click="loadMore" 
                    :disabled="items.loading"
                    class="px-8 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white rounded-full shadow-sm hover:shadow-md hover:border-gray-900 dark:hover:border-white transition-all text-sm font-bold uppercase tracking-wider disabled:opacity-50"
                >
                    {{ items.loading ? 'Loading...' : 'Load More' }}
                </button>
            </div>
        </div>
    </div>

    <ProductModal 
      :show="showModal" 
      :itemCode="selectedItemCode" 
      @close="showModal = false" 
    />
  </AppLayout>
</template>

<style scoped>
/* MAGIC CSS: This creates the smart zoom effect. 
   It ensures cards are at least 240px wide but fills the space automatically. 
   No media queries needed. */
.smart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
}
</style>