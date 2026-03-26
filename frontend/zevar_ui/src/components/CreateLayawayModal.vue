<template>
	<Transition name="fade">
		<div v-if="show" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
			<div class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm" @click="close"></div>

			<div class="relative bg-white dark:bg-[#1a1c23] rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden border border-transparent dark:border-white/10">
				<!-- Header -->
				<div class="flex items-center justify-between p-6 border-b border-gray-100 dark:border-white/5">
					<div>
						<h2 class="text-lg font-bold text-gray-900 dark:text-white">Create Layaway Contract</h2>
						<p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">Step {{ currentStep }} of {{ totalSteps }}</p>
					</div>
					<button @click="close" class="p-2 hover:bg-gray-100 dark:hover:bg-white/10 rounded-full transition">
						<svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
						</svg>
					</button>
				</div>

				<!-- Progress Bar -->
				<div class="px-6 py-3 bg-gray-50 dark:bg-gray-900/50">
					<div class="flex items-center gap-2">
						<template v-for="step in totalSteps" :key="step">
							<div
								class="flex-1 h-1.5 rounded-full transition-colors"
								:class="step <= currentStep ? 'bg-[#D4AF37]' : 'bg-gray-200 dark:bg-gray-700'"
							></div>
						</template>
					</div>
					<div class="flex justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
						<span>Customer</span>
						<span>Items</span>
						<span>Terms</span>
						<span>Preview</span>
						<span>Payment</span>
						<span>Confirm</span>
					</div>
				</div>

				<!-- Content -->
				<div class="p-6 overflow-y-auto" style="max-height: calc(90vh - 200px)">
					<!-- Step 1: Customer Selection -->
					<div v-if="currentStep === 1">
						<h3 class="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">Select Customer</h3>
						<div class="relative mb-4">
							<input
								v-model="customerSearch"
								type="text"
								placeholder="Search customer by name or phone..."
								@input="searchCustomers"
								class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-sm text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-[#D4AF37] focus:border-transparent placeholder-gray-400"
							/>
							<svg class="w-5 h-5 text-gray-400 absolute right-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
							</svg>
						</div>

						<!-- Customer Results -->
						<div v-if="customerResults.length > 0" class="space-y-2 mb-4">
							<button
								v-for="customer in customerResults"
								:key="customer.name"
								type="button"
								@click="selectCustomer(customer)"
								class="w-full p-3 rounded-lg border text-left transition"
								:class="form.customer === customer.name ? 'border-[#D4AF37] bg-[#D4AF37]/5' : 'border-gray-200 dark:border-gray-700 hover:border-[#D4AF37]/50'"
							>
								<p class="font-medium text-gray-900 dark:text-white">{{ customer.customer_name }}</p>
								<p class="text-sm text-gray-500">{{ customer.mobile_no || customer.email_id || 'No contact' }}</p>
							</button>
						</div>

						<!-- Selected Customer -->
						<div v-if="selectedCustomer" class="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800/30 rounded-lg">
							<p class="text-sm font-medium text-green-800 dark:text-green-300">Selected Customer:</p>
							<p class="text-lg font-bold text-green-900 dark:text-green-200">{{ selectedCustomer.customer_name }}</p>
							<p class="text-sm text-green-600 dark:text-green-400">{{ selectedCustomer.mobile_no || 'No phone' }}</p>
						</div>
					</div>

					<!-- Step 2: Add Items -->
					<div v-if="currentStep === 2">
						<h3 class="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">Add Items to Layaway</h3>

						<div class="relative mb-4">
							<input
								v-model="itemSearch"
								type="text"
								placeholder="Search items by code or name..."
								@input="searchItems"
								class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-sm text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-[#D4AF37] focus:border-transparent placeholder-gray-400"
							/>
						</div>

						<!-- Item Results -->
						<div v-if="itemResults.length > 0" class="grid grid-cols-2 gap-2 mb-4 max-h-40 overflow-y-auto">
							<button
								v-for="item in itemResults"
								:key="item.item_code"
								type="button"
								@click="addItem(item)"
								class="p-2 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-[#D4AF37]/50 text-left transition"
							>
								<p class="text-xs font-medium text-gray-900 dark:text-white truncate">{{ item.item_name }}</p>
								<p class="text-xs text-[#D4AF37] font-bold">${{ formatPrice(item.price) }}</p>
							</button>
						</div>

						<!-- Selected Items -->
						<div v-if="selectedItems.length > 0" class="space-y-2">
							<p class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Selected Items</p>
							<div
								v-for="(item, index) in selectedItems"
								:key="item.item_code"
								class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900 rounded-lg"
							>
								<div>
									<p class="text-sm font-medium text-gray-900 dark:text-white">{{ item.item_name }}</p>
									<p class="text-xs text-gray-500">{{ item.item_code }}</p>
								</div>
								<div class="flex items-center gap-3">
									<span class="text-sm font-bold text-[#D4AF37]">${{ formatPrice(item.price) }}</span>
									<button @click="removeItem(index)" class="text-red-500 hover:text-red-600">
										<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
										</svg>
									</button>
								</div>
							</div>
							<div class="pt-2 border-t border-gray-200 dark:border-gray-700">
								<p class="text-right font-bold text-gray-900 dark:text-white">
									Total: <span class="text-[#D4AF37]">${{ formatPrice(totalAmount) }}</span>
								</p>
							</div>
						</div>
					</div>

					<!-- Step 3: Set Terms -->
					<div v-if="currentStep === 3">
						<h3 class="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">Set Layaway Terms</h3>

						<div class="space-y-4">
							<!-- Deposit Amount -->
							<div>
								<label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1.5">
									Initial Deposit (Minimum 10%)
								</label>
								<div class="relative">
									<span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">$</span>
									<input
										v-model.number="form.deposit"
										type="number"
										:min="minDeposit"
										:max="totalAmount"
										class="w-full pl-8 pr-4 py-2.5 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg text-sm text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-[#D4AF37] focus:border-transparent"
									/>
								</div>
								<p class="text-xs text-gray-500 mt-1">Minimum deposit: ${{ formatPrice(minDeposit) }}</p>
							</div>

							<!-- Duration -->
							<div>
								<label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1.5">
									Payment Duration
								</label>
								<div class="grid grid-cols-4 gap-2">
									<button
										v-for="duration in durations"
										:key="duration.value"
										type="button"
										@click="form.duration = duration.value"
										class="px-3 py-2.5 rounded-lg text-sm font-bold border transition"
										:class="form.duration === duration.value ? 'border-[#D4AF37] bg-[#D4AF37]/10 text-[#D4AF37]' : 'border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:border-gray-300'"
									>
										{{ duration.label }}
									</button>
								</div>
							</div>

							<!-- Monthly Payment Preview -->
							<div v-if="form.deposit && form.duration" class="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg">
								<p class="text-sm text-gray-500 dark:text-gray-400">Monthly Payment</p>
								<p class="text-2xl font-bold text-[#D4AF37]">${{ formatPrice(monthlyPayment) }}/mo</p>
								<p class="text-xs text-gray-500 mt-1">
									Remaining balance: ${{ formatPrice(balanceAmount) }} over {{ form.duration }} months
								</p>
							</div>
						</div>
					</div>

					<!-- Step 4: Preview Payment Schedule -->
					<div v-if="currentStep === 4">
						<h3 class="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">Payment Schedule Preview</h3>

						<div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-4">
							<div class="flex justify-between mb-2">
								<span class="text-gray-500 dark:text-gray-400">Total Amount</span>
								<span class="font-bold text-gray-900 dark:text-white">${{ formatPrice(totalAmount) }}</span>
							</div>
							<div class="flex justify-between mb-2">
								<span class="text-gray-500 dark:text-gray-400">Initial Deposit</span>
								<span class="font-bold text-green-600">${{ formatPrice(form.deposit) }}</span>
							</div>
							<div class="flex justify-between pt-2 border-t border-gray-200 dark:border-gray-700">
								<span class="text-gray-500 dark:text-gray-400">Remaining Balance</span>
								<span class="font-bold text-[#D4AF37]">${{ formatPrice(balanceAmount) }}</span>
							</div>
						</div>

						<div class="space-y-2">
							<p class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Payment Schedule</p>
							<div
								v-for="(payment, index) in paymentSchedule"
								:key="index"
								class="flex items-center justify-between p-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg"
							>
								<div>
									<p class="text-sm font-medium text-gray-900 dark:text-white">{{ payment.label }}</p>
									<p class="text-xs text-gray-500">{{ payment.date }}</p>
								</div>
								<span class="font-bold text-gray-900 dark:text-white">${{ formatPrice(payment.amount) }}</span>
							</div>
						</div>
					</div>

					<!-- Step 5: Process Initial Payment -->
					<div v-if="currentStep === 5">
						<h3 class="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">Process Initial Payment</h3>

						<div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-4">
							<p class="text-sm text-gray-500 dark:text-gray-400">Deposit Amount Due</p>
							<p class="text-3xl font-bold text-[#D4AF37]">${{ formatPrice(form.deposit) }}</p>
						</div>

						<div>
							<label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1.5">
								Payment Method
							</label>
							<div class="grid grid-cols-3 gap-2">
								<button
									v-for="method in paymentMethods"
									:key="method.value"
									type="button"
									@click="form.paymentMethod = method.value"
									class="px-3 py-3 rounded-lg text-sm font-bold border transition flex flex-col items-center gap-1"
									:class="form.paymentMethod === method.value ? 'border-[#D4AF37] bg-[#D4AF37]/10 text-[#D4AF37]' : 'border-gray-200 dark:border-gray-700 text-gray-600 dark:text-gray-400 hover:border-gray-300'"
								>
									<span>{{ method.icon }}</span>
									<span>{{ method.label }}</span>
								</button>
							</div>
						</div>

						<div class="mt-4 p-3 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800/30 rounded-lg">
							<p class="text-xs text-yellow-700 dark:text-yellow-400">
								<strong>Note:</strong> You can skip payment now and collect deposit later. The layaway will be created with "Pending" status.
							</p>
						</div>
					</div>

					<!-- Step 6: Confirm -->
					<div v-if="currentStep === 6">
						<h3 class="text-sm font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">Confirm & Create</h3>

						<div class="space-y-4">
							<!-- Summary -->
							<div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
								<h4 class="font-bold text-gray-900 dark:text-white mb-3">Contract Summary</h4>
								<div class="space-y-2 text-sm">
									<div class="flex justify-between">
										<span class="text-gray-500 dark:text-gray-400">Customer</span>
										<span class="font-medium text-gray-900 dark:text-white">{{ selectedCustomer?.customer_name }}</span>
									</div>
									<div class="flex justify-between">
										<span class="text-gray-500 dark:text-gray-400">Items</span>
										<span class="font-medium text-gray-900 dark:text-white">{{ selectedItems.length }} items</span>
									</div>
									<div class="flex justify-between">
										<span class="text-gray-500 dark:text-gray-400">Total Amount</span>
										<span class="font-medium text-[#D4AF37]">${{ formatPrice(totalAmount) }}</span>
									</div>
									<div class="flex justify-between">
										<span class="text-gray-500 dark:text-gray-400">Deposit</span>
										<span class="font-medium text-green-600">${{ formatPrice(form.deposit) }}</span>
									</div>
									<div class="flex justify-between">
										<span class="text-gray-500 dark:text-gray-400">Duration</span>
										<span class="font-medium text-gray-900 dark:text-white">{{ form.duration }} months</span>
									</div>
									<div class="flex justify-between">
										<span class="text-gray-500 dark:text-gray-400">Monthly Payment</span>
										<span class="font-medium text-gray-900 dark:text-white">${{ formatPrice(monthlyPayment) }}</span>
									</div>
								</div>
							</div>

							<!-- Terms Agreement -->
							<label class="flex items-start gap-3 cursor-pointer">
								<input
									v-model="form.agreedToTerms"
									type="checkbox"
									class="mt-1 w-4 h-4 text-[#D4AF37] border-gray-300 rounded focus:ring-[#D4AF37]"
								/>
								<span class="text-sm text-gray-600 dark:text-gray-400">
									I confirm that the customer has agreed to the layaway terms including the payment schedule and cancellation policy.
								</span>
							</label>
						</div>
					</div>
				</div>

				<!-- Footer -->
				<div class="flex items-center justify-between p-6 border-t border-gray-100 dark:border-white/5 bg-gray-50 dark:bg-gray-900/30">
					<button
						v-if="currentStep > 1"
						@click="prevStep"
						class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition"
					>
						← Back
					</button>
					<div v-else></div>

					<div class="flex gap-3">
						<button
							@click="close"
							class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition"
						>
							Cancel
						</button>
						<button
							v-if="currentStep < totalSteps"
							@click="nextStep"
							:disabled="!canProceed"
							class="px-6 py-2 bg-[#D4AF37] text-black rounded-lg text-sm font-bold hover:bg-[#c9a432] disabled:opacity-50 disabled:cursor-not-allowed transition"
						>
							Next →
						</button>
						<button
							v-else
							@click="createLayaway"
							:disabled="submitting || !form.agreedToTerms"
							class="px-6 py-2 bg-[#D4AF37] text-black rounded-lg text-sm font-bold hover:bg-[#c9a432] disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center gap-2"
						>
							<svg v-if="submitting" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
							</svg>
							{{ submitting ? 'Creating...' : 'Create Layaway' }}
						</button>
					</div>
				</div>
			</div>
		</div>
	</Transition>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { createResource } from 'frappe-ui'

const props = defineProps({
	show: { type: Boolean, default: false },
})

const emit = defineEmits(['close', 'created'])

// State
const currentStep = ref(1)
const totalSteps = 6
const submitting = ref(false)
const customerSearch = ref('')
const itemSearch = ref('')
const customerResults = ref([])
const itemResults = ref([])
const selectedCustomer = ref(null)
const selectedItems = ref([])

const durations = [
	{ value: 3, label: '3 Months' },
	{ value: 6, label: '6 Months' },
	{ value: 9, label: '9 Months' },
	{ value: 12, label: '12 Months' },
]

const paymentMethods = [
	{ value: 'Cash', label: 'Cash', icon: '💵' },
	{ value: 'Card', label: 'Card', icon: '💳' },
	{ value: 'Skip', label: 'Pay Later', icon: '⏳' },
]

const form = ref({
	customer: '',
	deposit: 0,
	duration: 3,
	paymentMethod: 'Cash',
	agreedToTerms: false,
})

// Computed
const totalAmount = computed(() => {
	return selectedItems.value.reduce((sum, item) => sum + (item.price || 0), 0)
})

const minDeposit = computed(() => {
	return Math.ceil(totalAmount.value * 0.1) // 10% minimum
})

const balanceAmount = computed(() => {
	return Math.max(0, totalAmount.value - (form.value.deposit || 0))
})

const monthlyPayment = computed(() => {
	if (!form.value.duration || form.value.duration === 0) return 0
	return Math.ceil(balanceAmount.value / form.value.duration)
})

const paymentSchedule = computed(() => {
	const schedule = []
	const today = new Date()

	// Deposit
	schedule.push({
		label: 'Initial Deposit',
		date: 'Today',
		amount: form.value.deposit,
	})

	// Monthly payments
	for (let i = 1; i <= form.value.duration; i++) {
		const dueDate = new Date(today)
		dueDate.setMonth(dueDate.getMonth() + i)
		schedule.push({
			label: `Payment ${i} of ${form.value.duration}`,
			date: dueDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
			amount: i === form.value.duration ? balanceAmount.value - (monthlyPayment.value * (form.value.duration - 1)) : monthlyPayment.value,
		})
	}

	return schedule
})

const canProceed = computed(() => {
	switch (currentStep.value) {
		case 1:
			return !!selectedCustomer.value
		case 2:
			return selectedItems.value.length > 0
		case 3:
			return form.value.deposit >= minDeposit.value && form.value.duration > 0
		case 4:
			return true
		case 5:
			return !!form.value.paymentMethod
		default:
			return true
	}
})

// Resources
const searchCustomersResource = createResource({
	url: 'frappe.client.get_list',
	auto: false,
})

const searchItemsResource = createResource({
	url: 'zevar_core.api.get_pos_items',
	auto: false,
})

const createLayawayResource = createResource({
	url: 'zevar_core.api.layaway.create_layaway',
	auto: false,
})

// Methods
function formatPrice(price) {
	if (price == null) return '0.00'
	return Number(price).toFixed(2)
}

async function searchCustomers() {
	if (!customerSearch.value || customerSearch.value.length < 2) {
		customerResults.value = []
		return
	}

	try {
		const result = await searchCustomersResource.submit({
			doctype: 'Customer',
			fields: ['name', 'customer_name', 'mobile_no', 'email_id'],
			filters: {
				customer_name: ['like', `%${customerSearch.value}%`],
			},
			limit_page_length: 10,
		})
		customerResults.value = result || []
	} catch (error) {
		console.error('Customer search failed:', error)
	}
}

function selectCustomer(customer) {
	selectedCustomer.value = customer
	form.value.customer = customer.name
}

async function searchItems() {
	if (!itemSearch.value || itemSearch.value.length < 2) {
		itemResults.value = []
		return
	}

	try {
		const result = await searchItemsResource.submit({
			search: itemSearch.value,
			page_length: 20,
		})
		itemResults.value = (result || []).map(item => ({
			item_code: item.item_code,
			item_name: item.item_name,
			price: item.price || item.standard_rate || 0,
		}))
	} catch (error) {
		console.error('Item search failed:', error)
	}
}

function addItem(item) {
	// Check if already added
	if (selectedItems.value.find(i => i.item_code === item.item_code)) {
		return
	}
	selectedItems.value.push(item)

	// Auto-set deposit to 10% of total
	form.value.deposit = Math.ceil(totalAmount.value * 0.1)
}

function removeItem(index) {
	selectedItems.value.splice(index, 1)
	// Recalculate deposit
	form.value.deposit = Math.ceil(totalAmount.value * 0.1)
}

function nextStep() {
	if (canProceed.value && currentStep.value < totalSteps) {
		currentStep.value++
	}
}

function prevStep() {
	if (currentStep.value > 1) {
		currentStep.value--
	}
}

async function createLayaway() {
	submitting.value = true

	try {
		const result = await createLayawayResource.submit({
			customer: form.value.customer,
			items: selectedItems.value.map(item => ({
				item_code: item.item_code,
				item_name: item.item_name,
				amount: item.price,
			})),
			total_amount: totalAmount.value,
			deposit_amount: form.value.deposit,
			duration_months: form.value.duration,
			payment_method: form.value.paymentMethod,
		})

		if (result?.success || result?.layaway_id) {
			emit('created', result)
			close()
		}
	} catch (error) {
		console.error('Failed to create layaway:', error)
		alert('Failed to create layaway: ' + (error.message || 'Unknown error'))
	} finally {
		submitting.value = false
	}
}

function close() {
	// Reset state
	currentStep.value = 1
	customerSearch.value = ''
	itemSearch.value = ''
	selectedCustomer.value = null
	selectedItems.value = []
	form.value = {
		customer: '',
		deposit: 0,
		duration: 3,
		paymentMethod: 'Cash',
		agreedToTerms: false,
	}
	emit('close')
}

// Watchers
watch(
	() => props.show,
	(isOpen) => {
		if (isOpen) {
			// Reset on open
			currentStep.value = 1
		}
	}
)
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}
</style>
