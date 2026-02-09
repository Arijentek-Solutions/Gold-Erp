<template>
  <AppLayout>
    <div class="h-full flex flex-col">
      <div class="flex items-center justify-between gap-4 mb-6">
        <h2 class="text-2xl font-serif font-bold text-gray-900 dark:text-white">Repair Terminal</h2>
        <button
          @click="showNewModal = true"
          class="px-4 py-2 bg-[#8B6914] hover:bg-[#6d5210] text-white rounded-lg text-sm font-bold uppercase tracking-wider"
        >
          + New Repair
        </button>
      </div>

      <div class="flex gap-4 mb-4 flex-wrap">
        <select v-model="statusFilter" @change="loadOrders" class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white text-sm">
          <option value="">All Statuses</option>
          <option value="Received">Received</option>
          <option value="In Progress">In Progress</option>
          <option value="Ready for Pickup">Ready for Pickup</option>
          <option value="Delivered">Delivered</option>
        </select>
        <input v-model="searchTerm" @input="debouncedLoad" placeholder="Search by repair #" class="px-3 py-2 border border-gray-200 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-sm w-48" />
      </div>

      <div v-if="stats" class="flex gap-4 mb-6 text-sm">
        <span class="text-gray-500 dark:text-gray-400">Received: <b class="text-gray-900 dark:text-white">{{ stats.Received || 0 }}</b></span>
        <span class="text-gray-500 dark:text-gray-400">In Progress: <b class="text-gray-900 dark:text-white">{{ stats["In Progress"] || 0 }}</b></span>
        <span class="text-gray-500 dark:text-gray-400">Ready: <b class="text-gray-900 dark:text-white">{{ stats["Ready for Pickup"] || 0 }}</b></span>
      </div>

      <div class="flex-1 overflow-y-auto pb-20">
        <div v-if="ordersResource.loading && !orders.length" class="py-20 text-center">
          <div class="animate-spin rounded-full h-8 w-8 border-2 border-[#8B6914] border-t-transparent mx-auto mb-4"></div>
          <span class="text-gray-500 text-sm">Loading repairs...</span>
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
              <span class="font-mono font-bold text-[#8B6914]">{{ order.name }}</span>
              <span class="text-xs px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400">{{ order.status }}</span>
            </div>
            <p class="font-medium text-gray-900 dark:text-white truncate">{{ order.repair_type_name || order.repair_type }}</p>
            <p class="text-sm text-gray-500 truncate">{{ order.customer_name || order.customer }}</p>
            <p class="text-xs text-gray-400 mt-1">Handled by: {{ order.handled_by_name || "-" }}</p>
            <p class="text-xs text-gray-400">Est. ${{ formatNum(order.estimated_cost) }}</p>
          </div>
        </div>
      </div>
    </div>

    <Teleport to="body">
      <div v-if="showNewModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click.self="showNewModal = false">
        <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-xl max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto p-6">
          <h3 class="text-lg font-bold mb-4 text-gray-900 dark:text-white">New Repair Intake</h3>
          <form @submit.prevent="submitNewRepair" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Customer *</label>
              <Autocomplete
                v-model="newForm.customer"
                :options="customerOptions"
                placeholder="Search Customer (Name or Phone)"
                @update:query="onCustomerSearch"
              />
              <p v-if="!newForm.customer" class="text-xs text-red-500 mt-1">Please select a valid customer.</p>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Repair Type *</label>
              <select v-model="newForm.repair_type" required class="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-800">
                <option value="">Select...</option>
                <option v-for="t in repairTypes" :key="t.name" :value="t.name">{{ t.repair_name }} ({{ t.base_price ? "$" + t.base_price : "-" }})</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Item Description</label>
              <textarea v-model="newForm.item_description" class="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-800" rows="2"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Customer Phone</label>
              <input v-model="newForm.customer_phone" class="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-800" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Estimated Cost</label>
              <input v-model.number="newForm.estimated_cost" type="number" step="0.01" class="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-800" />
            </div>
            <div class="flex gap-2 pt-4">
              <button type="submit" class="flex-1 py-2 bg-[#8B6914] text-white rounded-lg font-bold">Create</button>
              <button type="button" @click="showNewModal = false" class="flex-1 py-2 border border-gray-300 dark:border-gray-600 rounded-lg">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <Teleport to="body">
      <div v-if="detailOrder" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click.self="detailOrder = null">
        <div class="bg-white dark:bg-gray-900 rounded-2xl shadow-xl max-w-lg w-full mx-4 max-h-[90vh] overflow-y-auto p-6">
          <div class="flex justify-between items-start mb-4">
            <h3 class="text-lg font-bold text-gray-900 dark:text-white">{{ detailOrder.name }}</h3>
            <button @click="detailOrder = null" class="text-gray-500 hover:text-gray-700">Close</button>
          </div>
          <p><span class="text-gray-500">Customer:</span> {{ detailOrder.customer_name }}</p>
          <p><span class="text-gray-500">Repair:</span> {{ detailOrder.repair_type_name }}</p>
          <p><span class="text-gray-500">Handled by:</span> {{ detailOrder.handled_by_name || "-" }}</p>
          <p><span class="text-gray-500">Status:</span> {{ detailOrder.status }}</p>
          <p><span class="text-gray-500">Total:</span> ${{ formatNum(detailOrder.total_cost) }}</p>
          <div class="mt-4 flex flex-wrap gap-2">
            <button @click="printReceipt(detailOrder.name)" class="px-3 py-1.5 bg-gray-200 dark:bg-gray-700 rounded-lg text-sm font-medium">Print Receipt</button>
            <button @click="openCustomerHistory(detailOrder.customer)" class="px-3 py-1.5 bg-gray-200 dark:bg-gray-700 rounded-lg text-sm font-medium">Repair History</button>
          </div>
          <div v-if="showHistory.length" class="mt-4 border-t pt-4">
            <h4 class="font-bold text-sm mb-2">Customer repair history</h4>
            <ul class="text-sm space-y-1">
              <li v-for="h in showHistory" :key="h.name">{{ h.name }} - {{ h.repair_type_name }} - {{ h.status }} - ${{ formatNum(h.total_cost) }}</li>
            </ul>
          </div>
          <div class="mt-4 pt-4 border-t">
            <label class="block text-sm font-medium mb-1">Update status</label>
            <select v-model="detailStatus" @change="updateStatus(detailOrder.name)" class="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-800">
              <option v-for="s in statusOptions" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
        </div>
      </div>
    </Teleport>
  </AppLayout>
</template>

<script setup>
import AppLayout from "@/components/AppLayout.vue"
import { useSessionStore } from "@/stores/session.js"
import { createResource, call, toast } from "frappe-ui"
import { Autocomplete } from "frappe-ui"
import { ref, watch, onMounted, computed } from "vue"

const session = useSessionStore()
const statusFilter = ref("")
const searchTerm = ref("")
const orders = ref([])
const stats = ref(null)
const showNewModal = ref(false)
const detailOrder = ref(null)
const detailStatus = ref("")
const showHistory = ref([])
const customerQuery = ref("")

const statusOptions = ["Received", "Estimated", "Approved", "In Progress", "Quality Check", "Ready for Pickup", "Delivered", "Cancelled"]

const newForm = ref({
  customer: null,
  repair_type: "",
  item_description: "",
  customer_phone: "",
  estimated_cost: null
})

// Customer Search
const customersResource = createResource({
  url: "frappe.client.get_list",
  makeParams: () => ({
    doctype: "Customer",
    filters: {
      customer_name: ["like", `%${customerQuery.value}%`]
    },
    fields: ["name", "customer_name", "mobile_no"],
    limit_page_length: 10
  }),
  auto: false
})

const customerOptions = computed(() => {
  return (customersResource.data || []).map(c => ({
    label: c.customer_name + (c.mobile_no ? ` (${c.mobile_no})` : ""),
    value: c.name
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

const repairTypes = ref([])
const repairTypesResource = createResource({
  url: "zevar_core.api.get_repair_types",
  onSuccess: (data) => { repairTypes.value = data || [] }
})

const ordersResource = createResource({
  url: "zevar_core.api.get_repair_orders",
  makeParams: () => ({
    status: statusFilter.value || undefined,
    warehouse: session.currentWarehouse || undefined,
    search_term: searchTerm.value || undefined,
    page_length: 50
  }),
  onSuccess: (data) => { orders.value = data || [] }
})

const statsResource = createResource({
  url: "zevar_core.api.get_repair_stats",
  makeParams: () => ({ warehouse: session.currentWarehouse || undefined }),
  onSuccess: (data) => { stats.value = data }
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
  if (n == null) return "0.00"
  return Number(n).toFixed(2)
}

async function submitNewRepair() {
  if (!newForm.value.customer || !newForm.value.repair_type) {
    toast({ title: "Missing Information", message: "Customer and Repair Type are required.", icon: "alert-circle", intent: "error" })
    return
  }
  
  try {
    const customerValue = newForm.value.customer?.value || newForm.value.customer // Handle Autocomplete object or raw value
    await call("zevar_core.api.create_repair_order", {
      customer: customerValue,
      repair_type: newForm.value.repair_type,
      item_description: newForm.value.item_description || undefined,
      customer_phone: newForm.value.customer_phone || undefined,
      estimated_cost: newForm.value.estimated_cost || undefined,
      warehouse: session.currentWarehouse || undefined,
      handled_by: session.user?.email || undefined
    })
    showNewModal.value = false
    newForm.value = { customer: null, repair_type: "", item_description: "", customer_phone: "", estimated_cost: null }
    loadOrders()
    toast({ title: "Success", message: "Repair order created successfully.", icon: "check", intent: "success" })
  } catch (e) {
    console.error(e)
    toast({ title: "Error", message: e.messages?.[0] || e.message || "Failed to create repair order.", icon: "alert-triangle", intent: "error" })
  }
}

async function openDetail(order) {
  const d = await call("zevar_core.api.get_repair_order_details", { name: order.name })
  detailOrder.value = d
  detailStatus.value = d.status
}

async function updateStatus(name) {
  try {
    await call("zevar_core.api.update_repair_status", { name, status: detailStatus.value })
    const d = await call("zevar_core.api.get_repair_order_details", { name })
    detailOrder.value = d
    loadOrders()
    toast({ title: "Updated", message: `Status changed to ${detailStatus.value}`, icon: "check", intent: "success" })
  } catch (e) {
    console.error(e)
    toast({ title: "Error", message: e.messages?.[0] || "Failed to update status", icon: "alert-triangle", intent: "error" })
  }
}

async function printReceipt(name) {
  try {
    const html = await call("zevar_core.api.get_repair_receipt_html", { name })
    const w = window.open("", "_blank")
    w.document.write(html)
    w.document.close()
    w.print()
  } catch (e) {
    console.error(e)
    toast({ title: "Error", message: "Failed to generate receipt", icon: "alert-triangle", intent: "error" })
  }
}

async function openCustomerHistory(customer) {
  try {
    const list = await call("zevar_core.api.get_customer_repair_history", { customer, limit: 10 })
    showHistory.value = list || []
  } catch (e) {
    console.error(e)
    toast({ title: "Error", message: "Failed to load history", icon: "alert-triangle", intent: "error" })
  }
}

watch(() => session.currentWarehouse, () => { loadOrders() }, { immediate: true })

onMounted(() => {
  repairTypesResource.fetch()
})
</script>
