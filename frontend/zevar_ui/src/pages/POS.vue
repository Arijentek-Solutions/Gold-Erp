<script setup>
import AppLayout from '@/components/AppLayout.vue'
import ItemCard from '@/components/ItemCard.vue'
import { useSessionStore } from '@/stores/session.js'
import { createResource } from 'frappe-ui'
import { watch, ref, computed } from 'vue'

const session = useSessionStore()

// State for Pagination & Search
const catalog = ref([]) // Our main bucket of items
const start = ref(0)    // How many items we have loaded so far
const searchQuery = ref('')
const PAGE_LENGTH = 20  // Load 20 at a time (snappy)
const hasMore = ref(true) // Do we have more items to load?

// 1. The Resource (Fetcher)
const items = createResource({
  url: 'zevar_core.api.get_pos_items', 
  makeParams() {
    return {
      warehouse: session.currentWarehouse,
      page_length: PAGE_LENGTH,
      start: start.value,
      search_term: searchQuery.value
    }
  },
  onSuccess(data) {
    // If we got fewer items than requested, we reached the end
    if (data.length < PAGE_LENGTH) {
      hasMore.value = false
    }

    // If it's a fresh search (start=0), replace the catalog
    if (start.value === 0) {
      catalog.value = data
    } 
    // Otherwise, append to existing list
    else {
      catalog.value.push(...data)
    }
  }
})

// 2. Actions
function loadMore() {
  if (!hasMore.value) return
  start.value += PAGE_LENGTH
  items.fetch()
}

function triggerSearch() {
  // Reset everything for a new search
  start.value = 0
  hasMore.value = true
  items.fetch()
}

// Watcher: If store changes, reset and fetch
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
    <div class="max-w-6xl mx-auto">
      
      <div v-if="!session.currentWarehouse" class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6 rounded-r">
        <div class="flex">
          <div class="ml-3">
            <p class="text-sm text-yellow-700">
              ⚠️ Please select a <strong>Store Location</strong> from the top bar to start selling.
            </p>
          </div>
        </div>
      </div>

      <div v-else>
        
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <h2 class="text-2xl font-bold text-gray-800">Catalog</h2>
          
          <div class="relative">
            <input 
              v-model="searchQuery"
              @keydown.enter="triggerSearch()"
              type="text" 
              placeholder="Search (e.g. Ring, 22K)..." 
              class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg w-full md:w-64 focus:ring-gray-900 focus:border-gray-900 transition-colors"
            >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 absolute left-3 top-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <ItemCard 
            v-for="item in catalog" 
            :key="item.item_code" 
            :item="item" 
          />
        </div>

        <div v-if="catalog.length === 0 && !items.loading" class="text-center py-20 bg-gray-50 rounded-lg mt-6">
           <p class="text-gray-500">No items found.</p>
           <button @click="searchQuery = ''; triggerSearch()" class="text-blue-600 text-sm mt-2 hover:underline">
             Clear Search
           </button>
        </div>

        <div class="mt-8 flex justify-center pb-10">
          
          <div v-if="items.loading" class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
          
          <button 
            v-else-if="hasMore && catalog.length > 0" 
            @click="loadMore()"
            class="bg-gray-100 text-gray-700 px-6 py-2 rounded-full font-medium hover:bg-gray-200 transition-colors"
          >
            Load More items...
          </button>
          
          <p v-else-if="catalog.length > 0" class="text-sm text-gray-400">
            You've reached the end of the list.
          </p>

        </div>
      </div>

    </div>
  </AppLayout>
</template>