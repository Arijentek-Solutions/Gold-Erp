<template>
  <header class="relative z-50">
    <!-- Top Bar - Gold Price + Utilities -->
    <div class="border-b" :class="isDark ? 'bg-[#0c0c0e] border-white/5' : 'bg-[#faf9f7] border-gray-200'">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 h-10 flex items-center justify-between text-xs">
        <!-- Gold Price (simplified) -->
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-2">
            <span class="w-4 h-4 rounded-full flex items-center justify-center" style="background: linear-gradient(135deg, #C9A962 0%, #8B7355 100%);">
              <span class="text-[8px] text-white font-bold">Au</span>
            </span>
            <span :class="isDark ? 'text-gray-400' : 'text-gray-600'">Gold</span>
            <span class="font-semibold" :class="isDark ? 'text-white' : 'text-gray-900'">${{ goldPrice }}<span class="font-normal text-[10px]">/oz</span></span>
            <span class="text-xs" :class="priceChange >= 0 ? 'text-emerald-500' : 'text-red-500'">
              {{ priceChange >= 0 ? '▲' : '▼' }} {{ Math.abs(priceChange).toFixed(2) }}%
            </span>
          </div>
        </div>
        
        <!-- Right Utils -->
        <div class="flex items-center gap-4" :class="isDark ? 'text-gray-400' : 'text-gray-600'">
          <a href="#" class="hover:text-[#C9A962] transition-colors flex items-center gap-1">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            Find Stores
          </a>
          <span class="w-px h-4" :class="isDark ? 'bg-white/10' : 'bg-gray-300'"></span>
          <button @click="$emit('toggleTheme')" class="hover:text-[#C9A962] transition-colors flex items-center gap-1">
            <svg v-if="isDark" class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="4" fill="currentColor"/>
              <path stroke-linecap="round" stroke-width="1.5" d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2"/>
            </svg>
            <svg v-else class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
            {{ isDark ? 'Light' : 'Dark' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Main Header -->
    <div class="border-b" :class="isDark ? 'bg-[#08080a] border-white/5' : 'bg-white border-gray-200'">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-8">
        <!-- Logo -->
        <div class="flex items-center gap-3 flex-shrink-0">
          <div class="w-9 h-9 rounded-lg flex items-center justify-center" style="background: linear-gradient(135deg, #C9A962 0%, #8B7355 100%);">
            <span class="text-white font-serif font-bold text-lg">Z</span>
          </div>
          <div class="leading-tight">
            <span class="font-serif font-bold text-xl tracking-tight block" :class="isDark ? 'text-white' : 'text-gray-900'">ZEVAR</span>
            <span class="text-[9px] uppercase tracking-widest" :class="isDark ? 'text-gray-500' : 'text-gray-400'">Fine Jewelry</span>
          </div>
        </div>
        
        <!-- Search Bar -->
        <div class="flex-1 max-w-xl hidden md:block">
          <div class="relative">
            <input 
              v-model="searchQuery"
              type="text"
              placeholder="Search rings, necklaces, earrings..."
              class="w-full h-10 pl-10 pr-4 rounded-lg border text-sm transition-all"
              :class="isDark 
                ? 'bg-[#12121a] border-white/10 text-white placeholder-gray-500 focus:border-[#C9A962]/50 focus:ring-1 focus:ring-[#C9A962]/20' 
                : 'bg-gray-50 border-gray-200 text-gray-900 placeholder-gray-400 focus:border-[#C9A962] focus:ring-1 focus:ring-[#C9A962]/20'"
              @keyup.enter="$emit('search', searchQuery)"
            />
            <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" :class="isDark ? 'text-gray-500' : 'text-gray-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
        </div>
        
        <!-- Right Icons -->
        <div class="flex items-center gap-3" :class="isDark ? 'text-gray-400' : 'text-gray-600'">
          <button class="w-9 h-9 rounded-lg flex items-center justify-center transition-colors hover:text-[#C9A962]" :class="isDark ? 'hover:bg-white/5' : 'hover:bg-gray-100'">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
            </svg>
          </button>
          <button class="w-9 h-9 rounded-lg flex items-center justify-center transition-colors hover:text-[#C9A962]" :class="isDark ? 'hover:bg-white/5' : 'hover:bg-gray-100'">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Navigation Bar with Icons -->
    <nav class="border-b" :class="isDark ? 'bg-[#0a0a0c] border-white/5' : 'bg-white border-gray-100'">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="flex items-center justify-between overflow-x-auto scrollbar-hide">
          <!-- Main Categories with Icons -->
          <div class="flex items-center">
            <button 
              v-for="cat in categories" 
              :key="cat.id"
              @click="$emit('selectCategory', cat.id)"
              class="px-4 py-3 text-sm whitespace-nowrap transition-all relative flex items-center gap-2"
              :class="[
                activeCategory === cat.id 
                  ? 'text-[#C9A962] font-medium' 
                  : (isDark ? 'text-gray-400 hover:text-white' : 'text-gray-600 hover:text-gray-900')
              ]"
            >
              <!-- Category Icon -->
              <component :is="cat.iconComponent" class="w-4 h-4" />
              {{ cat.name }}
              <span v-if="activeCategory === cat.id" class="absolute bottom-0 left-4 right-4 h-0.5 bg-[#C9A962]"></span>
            </button>
          </div>
          
          <!-- Special Occasions with Icons -->
          <div class="flex items-center border-l pl-3" :class="isDark ? 'border-white/10' : 'border-gray-200'">
            <button 
              v-for="occasion in specialOccasions" 
              :key="occasion.id"
              @click="$emit('selectOccasion', occasion.id)"
              class="px-3 py-3 text-sm whitespace-nowrap transition-all flex items-center gap-1.5"
              :class="isDark ? 'text-gray-500 hover:text-[#C9A962]' : 'text-gray-500 hover:text-[#C9A962]'"
            >
              <component :is="occasion.iconComponent" class="w-4 h-4" />
              {{ occasion.name }}
            </button>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted, h, markRaw } from 'vue'

const props = defineProps({
  isDark: { type: Boolean, default: true },
  activeCategory: { type: String, default: 'all' }
})

defineEmits(['toggleTheme', 'search', 'selectCategory', 'selectOccasion'])

const searchQuery = ref('')
const goldPrice = ref('2,031.47')
const priceChange = ref(0.52)

// Icon Components for Categories
const AllJewelryIcon = markRaw({ render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24', strokeWidth: '1.5' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', d: 'M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z' })
])})

const RingsIcon = markRaw({ render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24', strokeWidth: '1.5' }, [
  h('circle', { cx: '12', cy: '12', r: '4' }),
  h('path', { strokeLinecap: 'round', d: 'M12 2v2M12 20v2' })
])})

const ChainsIcon = markRaw({ render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24', strokeWidth: '1.5' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', d: 'M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m13.35-.622l1.757-1.757a4.5 4.5 0 00-6.364-6.364l-4.5 4.5a4.5 4.5 0 001.242 7.244' })
])})

const EarringsIcon = markRaw({ render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24', strokeWidth: '1.5' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', d: 'M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456z' })
])})

const BraceletsIcon = markRaw({ render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24', strokeWidth: '1.5' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', d: 'M21 7.5l-2.25-1.313M21 7.5v2.25m0-2.25l-2.25 1.313M3 7.5l2.25-1.313M3 7.5l2.25 1.313M3 7.5v2.25m9 3l2.25-1.313M12 12.75l-2.25-1.313M12 12.75V15m0 6.75l2.25-1.313M12 21.75V19.5m0 2.25l-2.25-1.313m0-16.875L12 2.25l2.25 1.313M21 14.25v2.25l-2.25 1.313m-13.5 0L3 16.5v-2.25' })
])})

const PendantsIcon = markRaw({ render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24', strokeWidth: '1.5' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', d: 'M21 11.25v8.25a1.5 1.5 0 01-1.5 1.5H5.25a1.5 1.5 0 01-1.5-1.5v-8.25M12 4.875A2.625 2.625 0 1012 10.125 2.625 2.625 0 0012 4.875z' })
])})

const WatchesIcon = markRaw({ render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24', strokeWidth: '1.5' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', d: 'M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z' })
])})

const DiamondIcon = markRaw({ render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24', strokeWidth: '1.5' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', d: 'M12 3l8 5-8 13-8-13 8-5z' }),
  h('path', { strokeLinecap: 'round', d: 'M4 8h16' })
])})

// Special Occasion Icons
const BridalIcon = markRaw({ render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24', strokeWidth: '1.5' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', d: 'M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm0 0V3m0 18v-3m-4.5-4.5L4 12m16 0l-3.5 1.5' })
])})

const AnniversaryIcon = markRaw({ render: () => h('svg', { fill: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { d: 'M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z' })
])})

const GiftingIcon = markRaw({ render: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24', strokeWidth: '1.5' }, [
  h('path', { strokeLinecap: 'round', strokeLinejoin: 'round', d: 'M21 11.25v8.25a1.5 1.5 0 01-1.5 1.5H5.25a1.5 1.5 0 01-1.5-1.5v-8.25M12 4.875A2.625 2.625 0 1012 10.125 2.625 2.625 0 0012 4.875zM12 10.125V21m0-10.875H5.625a1.125 1.125 0 010-2.25H12m0 2.25h6.375a1.125 1.125 0 000-2.25H12' })
])})

const categories = [
  { id: 'all', name: 'All Jewelry', iconComponent: AllJewelryIcon },
  { id: 'gold', name: 'Gold', iconComponent: DiamondIcon },
  { id: 'diamond', name: 'Diamond', iconComponent: DiamondIcon },
  { id: 'rings', name: 'Rings', iconComponent: RingsIcon },
  { id: 'earrings', name: 'Earrings', iconComponent: EarringsIcon },
  { id: 'necklaces', name: 'Necklaces', iconComponent: ChainsIcon },
  { id: 'bracelets', name: 'Bracelets', iconComponent: BraceletsIcon },
  { id: 'pendants', name: 'Pendants', iconComponent: PendantsIcon }
]

const specialOccasions = [
  { id: 'bridal', name: 'Bridal', iconComponent: BridalIcon },
  { id: 'anniversary', name: 'Anniversary', iconComponent: AnniversaryIcon },
  { id: 'gifting', name: 'Gifting', iconComponent: GiftingIcon }
]

// Fetch live gold price
onMounted(async () => {
  try {
    const response = await fetch('https://api.metals.live/v1/spot')
    const data = await response.json()
    const gold = data.find(m => m.metal === 'gold')
    if (gold) {
      goldPrice.value = gold.price.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
      priceChange.value = ((gold.price - gold.previous) / gold.previous * 100)
    }
  } catch (e) {
    // Keep default values
  }
})
</script>

<style scoped>
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
.scrollbar-hide::-webkit-scrollbar { display: none; }
</style>
