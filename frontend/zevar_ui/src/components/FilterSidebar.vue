<template>
  <div class="w-64 bg-white border-r border-gray-200 h-full flex flex-col">
    
    <div class="p-4 border-b border-gray-100">
      <h3 class="font-bold text-gray-800">Filters</h3>
    </div>

    <div class="p-4 flex-1 overflow-y-auto space-y-6">
      
      <div class="mb-8">
        <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">
          Metal
        </h3>
        <div class="space-y-2">
          <label class="flex items-center cursor-pointer group hover:bg-gray-50 p-1 rounded transition-colors">
            <input 
              type="radio" 
              v-model="selectedMetal" 
              value="" 
              class="w-4 h-4 text-gray-900 border-gray-300 focus:ring-gray-900"
            >
            <span class="ml-2 text-sm text-gray-700 group-hover:text-gray-900 font-medium">Any Metal</span>
          </label>

          <label 
            v-for="metal in metalOptions" 
            :key="metal" 
            class="flex items-center cursor-pointer group hover:bg-gray-50 p-1 rounded transition-colors"
          >
            <input 
              type="radio" 
              v-model="selectedMetal" 
              :value="metal" 
              class="w-4 h-4 text-gray-900 border-gray-300 focus:ring-gray-900"
            >
            <span class="ml-2 text-sm text-gray-600 group-hover:text-gray-900">{{ metal }}</span>
          </label>
        </div>
      </div>

      <div class="mb-8">
        <h3 class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">
          Purity
        </h3>
        <select 
          v-model="selectedPurity"
          class="w-full bg-white text-gray-700 text-sm rounded-lg border border-gray-300 focus:ring-gray-500 focus:border-gray-500 block p-2.5 shadow-sm"
        >
          <option value="">Any Purity</option>
          <option v-for="p in purityOptions" :key="p" :value="p">
            {{ p }}
          </option>
        </select>
      </div>

    </div>

    <div class="p-4 border-t border-gray-100 bg-gray-50">
      <button 
        @click="resetFilters"
        class="w-full py-2 text-xs font-medium text-red-600 hover:text-red-800 hover:bg-red-50 border border-transparent rounded transition-colors"
      >
        Reset Filters
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { createResource } from 'frappe-ui'

const emit = defineEmits(['update'])

// --- STATE ---
const selectedMetal = ref('')
const selectedPurity = ref('')
const metalOptions = ref([])
const purityOptions = ref([])

// --- API RESOURCES ---

// 1. Fetch Metal Options
const metalResource = createResource({
  url: 'frappe.client.get_list',
  makeParams: () => ({
    doctype: 'Zevar Metal',
    fields: ['name'],
    order_by: 'name asc'
  }),
  onSuccess: (data) => {
    metalOptions.value = data.map(d => d.name)
  }
})

// 2. Fetch Purity Options
const purityResource = createResource({
  url: 'frappe.client.get_list',
  makeParams: () => ({
    doctype: 'Zevar Purity',
    fields: ['name'],
    order_by: 'name asc'
  }),
  onSuccess: (data) => {
    purityOptions.value = data.map(d => d.name)
  }
})

// --- LOGIC ---

// Watch for changes and notify parent immediately
watch([selectedMetal, selectedPurity], () => {
  emit('update', {
    custom_metal_type: selectedMetal.value,
    custom_purity: selectedPurity.value
  })
})

function resetFilters() {
  selectedMetal.value = ''
  selectedPurity.value = ''
}

// Initial Fetch
onMounted(() => {
  metalResource.fetch()
  purityResource.fetch()
})

defineExpose({ resetFilters })
</script>