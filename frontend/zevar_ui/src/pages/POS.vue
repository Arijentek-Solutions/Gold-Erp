<script setup>
import AppLayout from '@/components/AppLayout.vue'
import ItemCard from '@/components/ItemCard.vue'
import FilterSidebar from '@/components/FilterSidebar.vue'
import ProductModal from '@/components/ProductModal.vue'
import { useSessionStore } from '@/stores/session.js'
import { createResource } from 'frappe-ui'
import { watch, ref } from 'vue'

const session = useSessionStore()
const activeFilters = ref({})

// Modal State
const showModal = ref(false)
const selectedItemCode = ref(null)

// Data State
const catalog = ref([]) 
const start = ref(0)
const searchQuery = ref('')
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
      search_term: searchQuery.value,
      filters: JSON.stringify(activeFilters.value)
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

function triggerSearch() {
  start.value = 0
  hasMore.value = true
  items.fetch()
}

function handleFilterUpdate(newFilters) {
  activeFilters.value = { ...newFilters }
  triggerSearch()
}

// ✅ Open Modal Function
function openItemDetails(itemCode) {
  selectedItemCode.value = itemCode
  showModal.value = true
}

// Watcher: Reset if warehouse changes
watch(
  () => session.currentWarehouse, 
  (newVal) => {
    if (newVal) {
      triggerSearch()
    } else {
      catalog.value = []
    }
  },
  { immediate: true }
)
</script>

<template>
  <AppLayout>
    
    <div v-if="!session.currentWarehouse" class="max-w-4xl mx-auto mt-10">
      <div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded-r">
        <p class="text-sm text-yellow-700">⚠️ Please select a <strong>Store Location</strong> to start.</p>
      </div>
    </div>

    <div v-else class="flex h-[calc(100vh-64px)] -m-6"> 
      
      <div class="hidden md:block w-64 flex-shrink-0">
        <FilterSidebar @update="handleFilterUpdate" />
      </div>

      <div class="flex-1 flex flex-col min-w-0 bg-gray-50">
        
        <div class="p-4 bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm flex items-center gap-4">
          <div class="relative flex-1 max-w-lg">
            <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">🔍</span>
            <input 
              v-model="searchQuery" 
              @input="triggerSearch"
              type="text" 
              placeholder="Search items..." 
              class="w-full py-2 pl-10 pr-4 text-sm text-gray-700 bg-gray-100 border-transparent rounded-lg focus:bg-white focus:border-gray-500"
            >
          </div>
          <div class="text-sm text-gray-500">
            Showing {{ catalog.length }} items
          </div>
        </div>

        <div class="flex-1 overflow-y-auto p-6">
          
          <div v-if="items.loading && start === 0" class="py-20 text-center">
            <span class="text-gray-400 animate-pulse">Loading Catalog...</span>
          </div>

          <div v-else-if="catalog.length === 0" class="py-20 text-center bg-white rounded-lg border border-dashed border-gray-300">
            <p class="text-gray-500">No items found.</p>
          </div>

          <div v-else>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              <div 
                v-for="item in catalog" 
                :key="item.item_code"
                @click="openItemDetails(item.item_code)"
                class="cursor-pointer transition-transform hover:scale-105"
              >
                <ItemCard :item="item" />
              </div>
            </div>

            <div class="mt-8 text-center pb-10">
              <button 
                v-if="hasMore" 
                @click="loadMore" 
                :disabled="items.loading"
                class="px-6 py-2 bg-white border border-gray-300 rounded-full shadow-sm hover:bg-gray-50 disabled:opacity-50 text-sm font-medium"
              >
                {{ items.loading ? 'Loading...' : 'Load More' }}
              </button>
              <p v-else class="text-xs text-gray-400 mt-4">End of catalog.</p>
            </div>
          </div>

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