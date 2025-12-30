<template>
  <div class="w-64 bg-white border-r border-gray-200 h-full flex flex-col">
    <div class="p-4 border-b border-gray-100">
      <h3 class="font-bold text-gray-800">Filters</h3>
    </div>

    <div class="p-4 flex-1 overflow-y-auto space-y-6">
      
      <div>
        <label class="text-xs font-bold text-gray-400 uppercase tracking-wider">Metal</label>
        <div class="mt-2 space-y-2">
          <label v-for="metal in metals" :key="metal" class="flex items-center gap-2 cursor-pointer">
            <input 
              type="radio" 
              name="metal" 
              :value="metal" 
              v-model="filters.custom_metal_type"
              class="text-gray-900 focus:ring-gray-900 border-gray-300"
            >
            <span class="text-sm text-gray-700">{{ metal }}</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="radio" name="metal" :value="''" v-model="filters.custom_metal_type" class="text-gray-900 border-gray-300">
            <span class="text-sm text-gray-400 italic">Any Metal</span>
          </label>
        </div>
      </div>

      <div>
        <label class="text-xs font-bold text-gray-400 uppercase tracking-wider">Purity</label>
        <div class="mt-2 space-y-2">
          <select v-model="filters.custom_purity" class="w-full text-sm border-gray-200 rounded-md">
            <option value="">Any Purity</option>
            <option v-for="p in purities" :key="p" :value="p">{{ p }}</option>
          </select>
        </div>
      </div>

    </div>

    <div class="p-4 border-t border-gray-100 bg-gray-50">
      <button 
        @click="resetFilters"
        class="w-full py-2 text-xs font-medium text-gray-500 hover:text-gray-800 border border-transparent hover:border-gray-300 rounded"
      >
        Reset Filters
      </button>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from 'vue'

const emit = defineEmits(['update'])

// We use the EXACT IDs from your backend verification
const metals = ["Gold", "Silver", "Platinum"]
const purities = ["24K", "22K", "18K", "14K", "10K", "925 Sterling", "999 Fine"]

const filters = reactive({
  custom_metal_type: '',
  custom_purity: ''
})

// Whenever filters change, tell the parent (POS.vue)
watch(filters, (newVal) => {
  emit('update', newVal)
})

function resetFilters() {
  filters.custom_metal_type = ''
  filters.custom_purity = ''
}
</script>