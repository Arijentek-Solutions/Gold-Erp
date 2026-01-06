<template>
    <div class="flex h-screen w-screen bg-gray-50">
        <aside class="w-64 bg-white border-r border-gray-200 flex flex-col transition-all duration-300">
            <div class="h-16 flex items-center justify-center border-b border-gray-100">
                <div class="flex items-center gap-2">
                    <div class="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center text-white font-bold">
                        Z
                    </div>
                    <h1 class="text-xl font-bold text-gray-800 tracking-tight">Zevar POS</h1>
                </div>
            </div>

            <nav class="p-4 space-y-2 flex-1">
                <router-link to="/"
                    class="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-colors"
                    active-class="bg-gray-900 text-white font-medium">
                    <span>💍</span> POS
                </router-link>

                <router-link to="/transactions"
                    class="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-colors"
                    active-class="bg-gray-900 text-white font-medium">
                    <span>📜</span> History
                </router-link>
            </nav>

            <div class="p-4 border-t border-gray-100">
                <button @click="session.logoutResource.submit()"
                    class="w-full flex items-center gap-2 text-red-500 hover:bg-red-50 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
                    🚪 Logout
                </button>
            </div>
        </aside>

        <div class="flex-1 flex flex-col overflow-hidden">
            <header
                class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 shadow-sm z-10">
                
                <div class="flex items-center gap-4">
                    <label class="text-sm text-gray-500 font-medium">Store Location:</label>
                    <select v-model="session.currentWarehouse" @change="session.setWarehouse($event.target.value)"
                        class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-gray-500 focus:border-gray-500 block w-64 p-2.5">
                        <option :value="null" disabled>Select a Store...</option>
                        <option v-for="wh in warehouses.data" :key="wh.name" :value="wh.name">
                            {{ wh.name }}
                        </option>
                    </select>
                </div>

                <div class="hidden lg:flex items-center gap-4 bg-gray-50 px-4 py-1.5 rounded-full border border-gray-200 mx-4 overflow-x-auto max-w-2xl no-scrollbar">
                    <div class="flex items-center gap-2 flex-shrink-0">
                        <span class="relative flex h-2 w-2">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                        </span>
                        <span class="text-xs font-bold text-gray-500 uppercase tracking-wide whitespace-nowrap">Live Rates</span>
                    </div>

                    <div v-for="(rate, key) in goldStore.rates" :key="key"
                        class="flex flex-col leading-none border-l border-gray-300 pl-4 min-w-[80px]">
                        <span class="text-[10px] text-gray-400 font-semibold uppercase truncate">
                            {{ key.replace('-', ' ') }}
                        </span>
                        <span class="text-sm font-bold text-gray-800">
                            ${{ rate }}
                        </span>
                    </div>
                </div>

                <div class="flex items-center gap-3">
                    
                    <button 
                        @click="isCartOpen = true"
                        class="relative p-2 text-gray-600 hover:text-gray-900 transition-colors mr-2"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                        </svg>
                        
                        <span 
                            v-if="cartStore.totalItems > 0" 
                            class="absolute top-0 right-0 inline-flex items-center justify-center px-1.5 py-0.5 text-xs font-bold leading-none text-white transform translate-x-1/4 -translate-y-1/4 bg-red-600 rounded-full"
                        >
                            {{ cartStore.totalItems }}
                        </span>
                    </button>

                    <div class="text-right hidden md:block">
                        <p class="text-sm font-medium text-gray-900">
                            {{ session.user?.full_name || 'Loading...' }}
                        </p>
                        <p class="text-xs text-gray-500">Sales Associate</p>
                    </div>
                    <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 font-bold border-2 border-white shadow-sm">
                        {{ session.user?.full_name?.[0] || 'U' }}
                    </div>
                </div>
            </header>

            <main class="flex-1 overflow-auto p-6 relative">
                <slot></slot>
            </main>
        </div>

        <CartSidebar :isOpen="isCartOpen" @close="isCartOpen = false" />
    </div>
</template>

<script setup>
import { useSessionStore } from '@/stores/session'
import { useGoldStore } from '@/stores/gold.js'
import { useCartStore } from '@/stores/cart.js' // 👈 Import Cart Store
import { createResource } from 'frappe-ui'
import { onMounted, ref } from 'vue'
import CartSidebar from '@/components/CartSidebar.vue'

const session = useSessionStore()
const goldStore = useGoldStore()
const cartStore = useCartStore() // 👈 Initialize Cart Store
const isCartOpen = ref(false)

// Fetch Warehouses
const warehouses = createResource({
    url: 'frappe.client.get_list',
    params: {
        doctype: 'Warehouse',
        filters: {
            is_group: 0,
            parent_warehouse: ['like', '%Zevar US Stores%'],
        },
        fields: ['name'],
    },
    auto: true,
})

onMounted(() => {
    goldStore.startPolling()
})
</script>