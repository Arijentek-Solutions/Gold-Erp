<template>
  <div class="select-none px-2 py-4">
    
    <div class="flex items-center justify-between mb-6 px-1">
        <h3 class="text-[10px] font-bold text-[#555961] uppercase tracking-widest">Filters</h3>
        <button v-if="hasActiveFilters" @click="ui.resetFilters()" class="text-[10px] text-[#D4AF37] hover:text-yellow-300 transition-colors">
            Reset All
        </button>
    </div>

    <div class="mb-6">
        <label class="block text-[10px] font-bold text-gray-500 mb-3 px-1">Metal</label>
        <div class="flex flex-wrap gap-2">
            <button 
                @click="updateMetal('')"
                :class="!currentMetal 
                    ? 'bg-[#D4AF37] text-[#0F1115] font-bold border-[#D4AF37]' 
                    : 'bg-[#1C1F26] text-gray-400 border-white/5 hover:border-gray-600 hover:text-white'"
                class="flex-1 min-w-[45%] px-3 py-2.5 text-[11px] rounded-lg border transition-all text-center shadow-sm"
            >
                All
            </button>
            
            <button 
                v-for="metal in Object.keys(metalPurityMap)" 
                :key="metal"
                @click="updateMetal(metal)"
                :class="currentMetal === metal 
                    ? 'bg-[#D4AF37] text-[#0F1115] font-bold border-[#D4AF37]' 
                    : 'bg-[#1C1F26] text-gray-400 border-white/5 hover:border-gray-600 hover:text-white'"
                class="flex-1 min-w-[45%] px-3 py-2.5 text-[11px] rounded-lg border transition-all text-center shadow-sm"
            >
                {{ metal }}
            </button>
        </div>
    </div>

    <div class="mb-6">
        <label class="block text-[10px] font-bold text-gray-500 mb-3 px-1">Gemstone</label>
        <div class="flex flex-wrap gap-2">
            <button 
                @click="updateGemstone('')"
                :class="!currentGemstone 
                    ? 'bg-[#D4AF37] text-[#0F1115] font-bold border-[#D4AF37]' 
                    : 'bg-[#1C1F26] text-gray-400 border-white/5 hover:border-gray-600 hover:text-white'"
                class="flex-1 min-w-[45%] px-3 py-2.5 text-[11px] rounded-lg border transition-all text-center shadow-sm"
            >
                Any
            </button>
            
            <button 
                v-for="gem in gemstoneOptions" 
                :key="gem"
                @click="updateGemstone(gem)"
                :class="currentGemstone === gem 
                    ? 'bg-[#D4AF37] text-[#0F1115] font-bold border-[#D4AF37]' 
                    : 'bg-[#1C1F26] text-gray-400 border-white/5 hover:border-gray-600 hover:text-white'"
                class="flex-1 min-w-[45%] px-3 py-2.5 text-[11px] rounded-lg border transition-all text-center shadow-sm"
            >
                {{ gem }}
            </button>
        </div>
    </div>

    <div class="mb-6">
        <label class="block text-[10px] font-bold text-gray-500 mb-2 px-1">Purity</label>
        <div class="relative">
            <select 
                :value="ui.activeFilters.custom_purity || ''"
                @change="ui.setFilter('custom_purity', $event.target.value)"
                class="w-full bg-[#1C1F26] text-gray-300 text-xs border border-white/10 rounded-lg p-3 focus:border-[#D4AF37] focus:ring-1 focus:ring-[#D4AF37] outline-none cursor-pointer"
            >
                <option value="">{{ currentMetal ? `Any ${currentMetal} Purity` : 'Any Purity' }}</option>
                <option v-for="p in purityOptions" :key="p" :value="p">{{ p }}</option>
            </select>
        </div>
    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUIStore } from '@/stores/ui'

const ui = useUIStore()

// 1. Data Options
const gemstoneOptions = ['Diamond', 'Ruby', 'Sapphire', 'Emerald', 'Polki', 'Kundan', 'No Stone']

const metalPurityMap = {
    'Yellow Gold': ['24K', '22K', '18K', '14K'],
    'White Gold':  ['18K', '14K'],
    'Rose Gold':   ['18K', '14K'],
    'Platinum':    ['950'],
    'Silver':      ['925 Sterling', '999 Fine']
}

// 2. Helpers
const currentMetal = computed(() => ui.activeFilters.custom_metal_type || '')
const currentGemstone = computed(() => ui.activeFilters.custom_gemstone || '')
const hasActiveFilters = computed(() => Object.keys(ui.activeFilters).length > 0 || ui.searchQuery)

// 3. Smart Purity Logic
const purityOptions = computed(() => {
    if (currentMetal.value && metalPurityMap[currentMetal.value]) {
        return metalPurityMap[currentMetal.value]
    }
    return [...new Set(Object.values(metalPurityMap).flat())]
})

// 4. Actions
function updateMetal(val) {
    // Reset purity if switching metals to avoid invalid combinations
    if (ui.activeFilters.custom_purity) {
        ui.setFilter('custom_purity', '')
    }
    ui.setFilter('custom_metal_type', val)
}

function updateGemstone(val) {
    ui.setFilter('custom_gemstone', val)
}
</script>