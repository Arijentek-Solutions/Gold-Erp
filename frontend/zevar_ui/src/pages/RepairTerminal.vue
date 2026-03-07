<template>
    <AppLayout>
        <div class="h-full flex flex-col min-h-0">
            <div class="flex items-center justify-between gap-4 mb-6 flex-shrink-0">
                <h2 class="text-2xl font-serif font-bold text-gray-900 dark:text-white">
                    Repair Terminal
                </h2>
                <button
                    @click="showNewModal = true"
                    class="px-4 py-2 bg-[#8B6914] text-white rounded-lg text-sm font-bold uppercase tracking-wider"
                >
                    + New Repair
                </button>
            </div>

            <div class="flex gap-4 mb-4 flex-wrap">
                <select
                    v-model="statusFilter"
                    @change="loadOrders"
                    class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm"
                >
                    <option value="">All Statuses</option>
                    <option v-for="s in statusOptions" :key="s" :value="s">{{ s }}</option>
                </select>
                <input
                    v-model="searchTerm"
                    @input="debouncedLoad"
                    placeholder="Search by repair #"
                    class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-sm w-48"
                />
            </div>

            <div v-if="stats" class="flex gap-4 mb-6 text-sm">
                <span class="text-gray-500 dark:text-gray-400">
                    Received:
                    <b class="text-gray-900 dark:text-white">{{ stats.Received || 0 }}</b>
                </span>
                <span class="text-gray-500 dark:text-gray-400">
                    In Progress:
                    <b class="text-gray-900 dark:text-white">{{ stats['In Progress'] || 0 }}</b>
                </span>
                <span class="text-gray-500 dark:text-gray-400">
                    Ready:
                    <b class="text-gray-900 dark:text-white">{{ stats['Ready for Pickup'] || 0 }}</b>
                </span>
            </div>

            <div class="flex-1 overflow-y-auto pb-20">
                <div v-if="ordersResource.loading && !orders.length" class="py-20 text-center bg-white dark:bg-gray-900 rounded-2xl border border-dashed border-gray-200 dark:border-gray-700">
                    <p class="text-gray-500">Loading...</p>
                </div>
                <div v-else-if="!orders.length" class="py-20 text-center bg-white dark:bg-gray-900 rounded-2xl border border-dashed border-gray-200 dark:border-gray-700">
                    <p class="text-gray-500">No repair orders found.</p>
                </div>

                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div
                        v-for="order in orders"
                        :key="order.name"
                        @click="openDetail(order)"
                        class="p-4 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 hover:border-[#8B6914] cursor-pointer transition-colors"
                    >
                        <div class="flex justify-between items-start mb-2">
                            <span class="font-mono font-bold text-[#8B6914]">{{
                                order.name
                            }}</span>
                        </div>
                        <p class="font-medium text-gray-900 dark:text-white truncate">
                            {{ order.repair_type_name || order.repair_type }}
                        </p>
                        <p class="text-sm text-gray-500 truncate">
                            {{ order.customer_name || order.customer }}
                        </p>
                        <p class="text-xs text-gray-400 mt-1">
                            Handled by: {{ order.handled_by_name || '-' }}
                        </p>
                        <p class="text-xs text-gray-400">
                            Est. ${{ formatNum(order.estimated_cost) }}
                        </p>
                    </div>
                </div>
            </div>

            <!-- Detail Modal -->
            <Teleport to="body">
                <div
                    v-if="detailOrder"
                    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
                    @click.self="detailOrder = null"
                >
                    <div
                        class="bg-white dark:bg-gray-900 rounded-2xl shadow-xl max-w-lg w-full mx-4 max-h-[90vh] overflow-y-auto p-6"
                    >
                        <div class="flex justify-between items-start mb-4">
                            <h3 class="text-lg font-bold text-gray-900 dark:text-white">
                                {{ detailOrder.name }}
                            </h3>
                            <button
                                @click="detailOrder = null"
                                class="text-gray-500 hover:text-gray-700"
                            >
                                Close
                            </button>
                        </div>
                        <p>
                            <span class="text-gray-500">Customer:</span>
                            {{ detailOrder.customer_name }}
                        </p>
                        <p>
                            <span class="text-gray-500">Repair:</span>
                            {{ detailOrder.repair_type_name }}
                        </p>
                        <p>
                            <span class="text-gray-500">Handled by:</span>
                            {{ detailOrder.handled_by_name || '-' }}
                        </p>
                        <p><span class="text-gray-500">Status:</span> {{ detailOrder.status }}</p>
                        <p>
                            <span class="text-gray-500">Total:</span> ${{
                                formatNum(detailOrder.total_cost)
                            }}
                        </p>
                        <div class="mt-4 flex flex-wrap gap-2">
                            <button
                                @click="printReceipt(detailOrder.name)"
                                class="px-3 py-1.5 bg-gray-200 dark:bg-gray-700 rounded-lg text-sm font-medium"
                            >
                                Print Receipt
                            </button>
                            <button
                                @click="openCustomerHistory(detailOrder.customer)"
                                class="px-3 py-1.5 bg-gray-200 dark:bg-gray-700 rounded-lg text-sm font-medium"
                            >
                                Repair History
                            </button>
                        </div>
                        <div v-if="showHistory.length" class="mt-4 border-t pt-4">
                            <h4 class="font-bold text-sm mb-2">Customer repair history</h4>
                            <ul class="text-sm space-y-1">
                                <li v-for="h in showHistory" :key="h.name">
                                    {{ h.name }} - {{ h.repair_type_name }} - {{ h.status }} - ${{
                                        formatNum(h.total_cost)
                                    }}
                                </li>
                            </ul>
                        </div>
                        <div class="mt-4 pt-4 border-t">
                            <label class="block text-sm font-medium mb-1">Update status</label>
                            <select
                                v-model="detailStatus"
                                @change="updateStatus(detailOrder.name)"
                                class="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-800"
                            >
                                <option v-for="s in statusOptions" :key="s" :value="s">{{ s }}</option>
                            </select>
                        </div>
                    </div>
                </div>
            </Teleport>
        </div>
    </AppLayout>
</template>

<script setup>
import AppLayout from '@/components/AppLayout.vue'
import { useSessionStore } from '@/stores/session.js'
import { createResource, call, toast } from 'frappe-ui'
import { Autocomplete } from 'frappe-ui'
import { ref, watch, onMounted, computed } from 'vue'

const session = useSessionStore()
const statusFilter = ref('')
const searchTerm = ref('')
const orders = ref([])
const stats = ref(null)
const showNewModal = ref(false)
const detailOrder = ref(null)
const detailStatus = ref('')
const showHistory = ref([])

const customerQuery = ref('')

const statusOptions = [
    'Received',
    'Estimated',
    'Approved',
    'In Progress',
    'Quality Check',
    'Ready for Pickup',
    'Delivered',
    'Cancelled',
]

const newForm = ref({
    customer: null,
    repair_type: '',
    item_description: '',
    customer_phone: '',
    estimated_cost: null,
})

const repairTypes = ref([])
const repairTypesResource = createResource({
    url: 'zevar_core.api.get_repair_types',
    onSuccess: (data) => {
        repairTypes.value = data || []
    },
})

const customersResource = createResource({
    url: 'frappe.client.get_list',
    makeParams: () => ({
        doctype: 'Customer',
        filters: {
            customer_name: ['like', `%${customerQuery.value}%`],
        },
        fields: ['name', 'customer_name', 'mobile_no'],
        limit_page_length: 10,
    }),
    auto: false
})

const customerOptions = computed(() => {
    return (customersResource.data || []).map((c) => ({
        label: c.customer_name + (c.mobile_no ? ` (${c.mobile_no})` : ''),
        value: c.name,
    }))
})

let customerSearchTimer
function onCustomerSearch(q) {
    customerQuery.value = q
    clearTimeout(customerSearchTimer)
    customerSearchTimer = setTimeout(() => {
        customersResource.fetch()
    }, 300)
}

const ordersResource = createResource({
    url: 'zevar_core.api.get_repair_orders',
    makeParams: () => ({
        status: statusFilter.value || undefined,
        warehouse: session.currentWarehouse || undefined,
        search_term: searchTerm.value || undefined,
        page_length: 50,
    }),
    onSuccess: (data) => {
        orders.value = data || []
    },
})

const statsResource = createResource({
    url: 'zevar_core.api.get_repair_stats',
    makeParams: () => ({ warehouse: session.currentWarehouse || undefined }),
    onSuccess: (data) => {
        stats.value = data
    },
})

function loadOrders() {
    ordersResource.fetch()
    statsResource.fetch()
}

let debounceTimer
function debouncedLoad() {
    clearTimeout(debounceTimer)
    debounceTimer = setTimeout(loadOrders, 300)
}

function formatNum(n) {
    if (n == null) return '0.00'
    return Number(n).toFixed(2)
}
async function submitNewRepair() {
    if (!newForm.value.customer || !newForm.value.repair_type) {
        toast({
            title: 'Missing Information',
            message: 'Customer and Repair Type are required.',
            icon: 'alert-circle',
            intent: 'error',
        })
        return
    }

    try {
        const customerValue = newForm.value.customer?.value || newForm.value.customer // Handle Autocomplete object or raw value
        await call('zevar_core.api.create_repair_order', {
            customer: customerValue,
            repair_type: newForm.value.repair_type,
            item_description: newForm.value.item_description || undefined,
            customer_phone: newForm.value.customer_phone || undefined,
            estimated_cost: newForm.value.estimated_cost || undefined,
            warehouse: session.currentWarehouse || undefined,
            handled_by: session.user?.email || undefined,
        })
        showNewModal.value = false
        newForm.value = {
            customer: null,
            repair_type: '',
            item_description: '',
            customer_phone: '',
            estimated_cost: null,
        }
        loadOrders()
        toast({
            title: 'Success',
            message: 'Repair order created successfully.',
            icon: 'check',
            intent: 'success',
        })
    } catch (e) {
        console.error(e)
        toast({
            title: 'Error',
            message: e.messages?.[0] || e.message || 'Failed to create repair order.',
            icon: 'alert-triangle',
            intent: 'error',
        })
    }
}

async function openDetail(order) {
    const d = await call('zevar_core.api.get_repair_order_details', { name: order.name })
    detailOrder.value = d
    detailStatus.value = d.status
}

async function updateStatus(name, status) {
    try {
        await call('zevar_core.api.update_repair_status', { name, status: detailStatus.value })
        loadOrders()
        toast({
            title: 'Updated',
            message: `Status changed to ${detailStatus.value}`,
            icon: 'check',
            intent: 'success',
        })
    } catch (e) {
        console.error(e)
        toast({
            title: 'Error',
            message: e.messages?.[0] || e.message || 'Failed to update status',
            icon: 'alert-triangle',
            intent: 'error',
        })
    }
}

async function printReceipt(name) {
    try {
        const html = await call('zevar_core.api.get_repair_receipt_html', { name })
        const w = window.open('', '_blank')
        w.document.write(html)
        w.document.close()
        w.print()
    } catch (e) {
        console.error(e)
        toast({
            title: 'Error',
            message: 'Failed to generate receipt',
            icon: 'alert-triangle',
            intent: 'error',
        })
    }
}

async function openCustomerHistory(customer) {
    try {
        const list = await call('zevar_core.api.get_customer_repair_history', {
            customer,
            limit: 10,
        })
        showHistory.value = list || []
    } catch (e) {
        console.error(e)
        toast({
            title: 'Error',
            message: 'Failed to load history',
            icon: 'alert-triangle',
            intent: 'error',
        })
    }
}

onMounted(() => {
    loadOrders()
    repairTypesResource.fetch()
})
</script>
