<template>
  <div class="flex h-screen w-screen bg-[#F8F9FA] dark:bg-[#050505] font-sans overflow-hidden transition-colors duration-300">
    
    <aside class="w-16 sm:w-20 lg:w-72 bg-[#1a1c23] dark:bg-black border-r border-white/5 flex flex-col shadow-2xl z-30 relative transition-all duration-300">
       
       <div class="h-24 flex items-center justify-center lg:justify-start lg:px-8 border-b border-white/5">
        <div class="flex items-center gap-4 group cursor-default">
          <div class="w-12 h-12 bg-gradient-to-tr from-[#D4AF37] to-[#F2E6A0] rounded-lg flex items-center justify-center text-[#0F1115] font-serif font-black text-2xl shadow-[0_0_15px_rgba(212,175,55,0.3)] transform group-hover:scale-105 transition-transform duration-500">
            Z
          </div>
          <div class="hidden lg:flex flex-col justify-center">
            <h1 class="text-white font-serif font-bold text-2xl leading-none tracking-wide">ZEVAR</h1>
            <div class="flex justify-between w-full mt-1 px-0.5">
                <span class="text-[9px] text-gray-400 uppercase font-medium tracking-[0.38em]">Jewelers</span>
            </div>
          </div>
        </div>
      </div>

      <nav class="p-4 space-y-2 flex-1 overflow-y-auto custom-scrollbar">
        <router-link to="/" 
          class="flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-300 group relative overflow-hidden"
          active-class="bg-white/10 text-white shadow-inner"
          :class="$route.path === '/' ? '' : 'text-gray-400 hover:text-white hover:bg-white/5'"
        >
          <div class="relative z-10 flex items-center gap-4">
             <svg class="w-5 h-5 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
             <span class="hidden lg:block font-medium tracking-wide text-sm">POS Terminal</span>
          </div>
          <div v-if="$route.path === '/'" class="absolute left-0 top-0 h-full w-1 bg-[#D4AF37] shadow-[0_0_10px_#D4AF37]"></div>
        </router-link>

        <router-link to="/transactions" 
          class="flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-300 group relative overflow-hidden"
          active-class="bg-white/10 text-white shadow-inner"
          :class="$route.path === '/transactions' ? '' : 'text-gray-400 hover:text-white hover:bg-white/5'"
        >
           <div class="relative z-10 flex items-center gap-4">
              <svg class="w-5 h-5 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
              <span class="hidden lg:block font-medium tracking-wide text-sm">Sales History</span>
           </div>
           <div v-if="$route.path === '/transactions'" class="absolute left-0 top-0 h-full w-1 bg-[#D4AF37] shadow-[0_0_10px_#D4AF37]"></div>
        </router-link>

        <router-link to="/catalogues" 
          class="flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-300 group relative overflow-hidden"
          active-class="bg-white/10 text-white shadow-inner"
          :class="$route.path === '/catalogues' ? '' : 'text-gray-400 hover:text-white hover:bg-white/5'"
        >
           <div class="relative z-10 flex items-center gap-4">
              <svg class="w-5 h-5 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
              <span class="hidden lg:block font-medium tracking-wide text-sm">Catalogues</span>
           </div>
           <div v-if="$route.path === '/catalogues'" class="absolute left-0 top-0 h-full w-1 bg-[#D4AF37] shadow-[0_0_10px_#D4AF37]"></div>
        </router-link>

        <div v-if="$route.path === '/'" class="mt-6 pt-6 border-t border-white/5 lg:block hidden">
            <FilterSidebar />
        </div>
      </nav>

      <div class="p-4 border-t border-white/5 bg-[#15171e] dark:bg-black flex items-center justify-between gap-2">
        <button @click="session.logoutResource.submit()" class="flex-1 flex items-center gap-3 p-2 rounded-xl hover:bg-white/5 transition-all group overflow-hidden">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-gray-700 to-gray-800 flex flex-shrink-0 items-center justify-center text-xs font-bold text-white border border-white/10 group-hover:border-[#D4AF37] transition-colors">
            {{ session.user?.full_name?.[0] || 'U' }}
          </div>
          <div class="hidden lg:block text-left overflow-hidden min-w-0">
             <p class="text-xs font-bold text-white truncate">{{ session.user?.full_name || 'User' }}</p>
             <p class="text-[9px] text-gray-500 group-hover:text-[#D4AF37] transition-colors uppercase tracking-wider">Logout</p>
          </div>
        </button>

        <button 
            @click="ui.toggleTheme()" 
            class="hidden lg:flex w-8 h-8 items-center justify-center rounded-lg bg-white/5 hover:bg-white/10 text-gray-400 hover:text-[#D4AF37] transition-colors border border-white/5"
            title="Toggle Theme"
        >
            <svg v-if="ui.isDark" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
        </button>
      </div>
    </aside>

    <div class="flex-1 flex flex-col relative min-w-0">
      
      <header class="h-16 sm:h-20 bg-white dark:bg-[#0F1115] border-b border-gray-200 dark:border-gray-800 flex items-center justify-between px-3 sm:px-6 z-20 sticky top-0 shadow-sm transition-colors duration-300">
        
        <div class="flex items-center gap-4 flex-1 max-w-3xl">
            
            <div class="relative group">
                <select v-model="session.currentWarehouse" @change="session.setWarehouse($event.target.value)" 
                    class="h-11 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 pl-4 pr-10 rounded-lg text-sm font-bold text-gray-800 dark:text-gray-200 focus:ring-2 focus:ring-[#D4AF37] focus:border-[#D4AF37] cursor-pointer min-w-[200px] transition-all hover:bg-gray-100 dark:hover:bg-gray-700 shadow-sm outline-none">
                    <option value="null" disabled>Select Store Location</option>
                    <option v-for="wh in warehouses.data" :key="wh.name" :value="wh.name">{{ wh.name }}</option>
                </select>
                </div>

             <div class="relative flex-1">
                 <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                 <input 
                    type="text"
                    v-model="ui.searchQuery"
                    placeholder="Search collection..." 
                    class="h-11 w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-800 dark:text-gray-200 placeholder-gray-400 dark:placeholder-gray-600 focus:ring-2 focus:ring-[#D4AF37] focus:border-transparent text-sm font-medium pl-11 transition-all"
                 >
             </div>
        </div>

        <div class="flex items-center gap-6">
            <div class="hidden lg:flex items-center gap-0 bg-gray-100 dark:bg-black text-gray-900 dark:text-white pl-4 pr-2 py-2 rounded-xl border border-gray-200 dark:border-gray-800 flex-1 max-w-2xl overflow-hidden transition-colors duration-300">
                 <div class="flex items-center gap-2 border-r border-gray-300 dark:border-gray-800 pr-3 mr-3 flex-shrink-0">
                    <span class="relative flex h-2 w-2">
                      <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-500 opacity-75"></span>
                      <span class="relative inline-flex rounded-full h-2 w-2 bg-green-600"></span>
                    </span>
                    <span class="text-[10px] font-bold uppercase tracking-widest text-gray-500 dark:text-gray-400">Live Rates</span>
                 </div>
                 
                 <div class="flex items-center gap-8 overflow-x-auto pr-2 custom-scrollbar-horizontal pb-2 pt-1">
                     <div v-for="[key, rate] in sortedRates" :key="key" class="flex flex-col leading-tight flex-shrink-0 px-3">
                         <span class="text-[11px] text-gray-500 dark:text-gray-400 uppercase font-bold whitespace-nowrap mb-0.5">{{ key.replace(/-/g, ' ') }}</span>
                         <span class="text-lg font-mono font-bold text-[#D4AF37] tracking-wide">${{ rate }}</span>
                     </div>
                 </div>
            </div>

            <button @click="isCartOpen = true" class="relative p-3 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors group">
                 <svg class="w-6 h-6 text-gray-600 dark:text-gray-300 group-hover:text-black dark:group-hover:text-white transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
                 <span v-if="cartStore.totalItems > 0" class="absolute top-1 right-0.5 h-5 w-5 flex items-center justify-center bg-[#D4AF37] text-white text-[10px] font-bold rounded-full shadow-md transform group-hover:scale-110 transition-transform">
                    {{ cartStore.totalItems }}
                 </span>
            </button>
        </div>
      </header>

      <main class="flex-1 overflow-y-auto overflow-x-hidden p-3 sm:p-4 lg:p-6 bg-[#F8F9FA] dark:bg-[#050505] transition-colors duration-300">
        <slot></slot>
      </main>
    </div>

    <CartSidebar :isOpen="isCartOpen" @close="isCartOpen = false" />
  </div>
</template>

<script setup>
/**
 * AppLayout Component
 *
 * Main application layout with sidebar navigation, header, and cart drawer.
 */

import { useSessionStore } from '@/stores/session'
import { useGoldStore } from '@/stores/gold.js'
import { useCartStore } from '@/stores/cart.js'
import { useUIStore } from '@/stores/ui'
import { createResource } from 'frappe-ui'
import { onMounted, ref, computed } from 'vue'
import CartSidebar from '@/components/CartSidebar.vue'
import FilterSidebar from '@/components/FilterSidebar.vue'

const session = useSessionStore()
const goldStore = useGoldStore()
const cartStore = useCartStore()
const ui = useUIStore()

const isCartOpen = ref(false)

const sortedRates = computed(() => {
  if (!goldStore.rates) return []
  const priority = ['Yellow Gold-22K', 'Yellow Gold-24K', 'Yellow Gold-18K', 'Silver-925 Sterling']
  // Filter out Platinum
  return Object.entries(goldStore.rates)
    .filter(([key]) => !key.includes('Platinum'))
    .sort((a, b) => {
    const indexA = priority.indexOf(a[0]); const indexB = priority.indexOf(b[0])
    if (indexA !== -1 && indexB !== -1) return indexA - indexB
    if (indexA !== -1) return -1
    if (indexB !== -1) return 1
    return a[0].localeCompare(b[0])
  })
})

const warehouses = createResource({
  url: 'frappe.client.get_list',
  params: { doctype: 'Warehouse', filters: { is_group: 0, parent_warehouse: ['like', '%Zevar US Stores%'] }, fields: ['name'] },
  auto: true,
})

onMounted(() => {
  goldStore.startPolling()
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: rgba(255, 255, 255, 0.05); }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 10px; }

.custom-scrollbar-horizontal::-webkit-scrollbar { height: 4px; }
.custom-scrollbar-horizontal::-webkit-scrollbar-track { background: transparent; margin: 0 10px; }
.custom-scrollbar-horizontal::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 10px; }
.dark .custom-scrollbar-horizontal::-webkit-scrollbar-thumb { background: #333; }
.custom-scrollbar-horizontal::-webkit-scrollbar-thumb:hover { background: #D4AF37; }
</style>