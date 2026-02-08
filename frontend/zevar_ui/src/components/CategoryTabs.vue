<template>
  <div class="flex gap-2 overflow-x-auto scrollbar-hide py-1 -mx-4 px-4 sm:mx-0 sm:px-0">
    <button 
      v-for="cat in displayCategories"
      :key="cat.id"
      @click="$emit('select', cat.id)"
      class="flex-shrink-0 px-4 py-2 rounded-full font-medium text-sm transition-all whitespace-nowrap flex items-center gap-2"
      :class="getButtonClass(cat.id)"
    >
      <span class="w-4 h-4 flex items-center justify-center">
        <!-- All -->
        <svg v-if="cat.id === 'all'" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
        </svg>
        <!-- Rings -->
        <svg v-else-if="cat.id === 'rings'" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="13" r="6"/>
          <path d="M12 7V3M10 4l2-1 2 1"/>
        </svg>
        <!-- Chains -->
        <svg v-else-if="cat.id === 'chains'" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
          <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
        </svg>
        <!-- Earrings -->
        <svg v-else-if="cat.id === 'earrings'" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="15" r="4"/>
          <path d="M12 3v8"/>
        </svg>
        <!-- Bracelets -->
        <svg v-else-if="cat.id === 'bracelets'" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <ellipse cx="12" cy="12" rx="9" ry="5"/>
        </svg>
        <!-- Pendants -->
        <svg v-else-if="cat.id === 'pendants'" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2v4M12 6a4 4 0 1 0 0 8 4 4 0 0 0 0-8z"/>
          <path d="M12 14v2l-2 4M12 16l2 4"/>
        </svg>
        <!-- Watches -->
        <svg v-else-if="cat.id === 'watches'" class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="6"/>
          <path d="M12 9v3l2 1"/>
          <path d="M9 2h6M9 22h6"/>
        </svg>
      </span>
      {{ cat.name }}
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  activeCategory: { type: String, default: 'all' },
  categories: { type: Array, default: () => [] }
})

defineEmits(['select'])

const displayCategories = computed(() => {
  if (props.categories?.length > 0) return props.categories
  return [
    { id: 'all', name: 'All' },
    { id: 'rings', name: 'Rings' },
    { id: 'chains', name: 'Chains' },
    { id: 'earrings', name: 'Earrings' },
    { id: 'bracelets', name: 'Bracelets' },
    { id: 'pendants', name: 'Pendants' },
    { id: 'watches', name: 'Watches' }
  ]
})

function getButtonClass(catId) {
  const isActive = props.activeCategory === catId
  const isDark = document.documentElement.classList.contains('dark')
  
  if (isActive) {
    return 'bg-[#C9A962] text-black font-semibold'
  }
  
  return isDark
    ? 'bg-[#1a1a1e] text-gray-300 border border-white/10 hover:border-[#C9A962]/50 hover:text-white'
    : 'bg-white text-gray-600 border border-gray-200 hover:border-[#C9A962] hover:text-gray-900'
}
</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
