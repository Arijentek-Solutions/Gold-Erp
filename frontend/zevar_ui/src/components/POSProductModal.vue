<template>
	<Transition name="fade">
		<div v-if="show" class="fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6">
			<div
				@click="close"
				class="absolute inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity"
			></div>

			<div
				class="relative bg-white dark:bg-[#1a1c23] rounded-xl shadow-2xl w-full max-w-4xl overflow-hidden flex flex-col md:flex-row max-h-[90vh] border border-transparent dark:border-white/10 transition-all"
			>
				<button
					@click="close"
					class="absolute top-4 right-4 z-10 p-2 bg-white/80 dark:bg-black/50 backdrop-blur rounded-full hover:bg-gray-100 dark:hover:bg-white/20 transition-colors group"
				>
					<svg
						class="h-6 w-6 text-gray-600 dark:text-white group-hover:scale-110 transition-transform"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M6 18L18 6M6 6l12 12"
						/>
					</svg>
				</button>

				<div
					class="w-full md:w-1/2 bg-gray-50 dark:bg-[#0F1115] flex items-center justify-center p-8 border-r border-gray-100 dark:border-white/5 relative"
				>
					<img
						v-if="details.image"
						:src="details.image"
						class="max-h-[60vh] object-contain drop-shadow-xl transform hover:scale-105 transition-transform duration-500"
					/>
					<div v-else class="text-gray-300 dark:text-gray-700">
						<svg
							class="h-32 w-32"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="1"
								d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
							/>
						</svg>
					</div>
				</div>

				<div class="w-full md:w-1/2 p-8 overflow-y-auto bg-white dark:bg-[#1a1c23]">
					<div v-if="loading" class="h-full flex items-center justify-center">
						<div
							class="animate-spin rounded-full h-8 w-8 border-2 border-gray-900 dark:border-[#D4AF37] border-t-transparent"
						></div>
					</div>

					<div v-else>
						<div class="mb-6">
							<h2
								class="text-2xl font-serif font-bold text-gray-900 dark:text-white leading-tight"
							>
								{{ details.item_name }}
							</h2>
							<p
								class="text-sm text-gray-500 dark:text-gray-400 mt-1 font-mono tracking-wide"
							>
								{{ details.item_code }}
							</p>
						</div>

						<div class="flex gap-2 mb-8">
							<span
								v-if="details.metal"
								class="px-3 py-1 bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-500 rounded text-xs font-bold uppercase tracking-wider border border-yellow-200 dark:border-yellow-700/50"
							>
								{{ details.metal }}
							</span>
							<span
								v-if="details.purity"
								class="px-3 py-1 bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300 rounded text-xs font-bold uppercase tracking-wider border border-gray-200 dark:border-gray-700"
							>
								{{ details.purity }}
							</span>
						</div>

						<div
							class="bg-gray-50 dark:bg-[#15171e] rounded-xl p-5 mb-6 text-sm border border-gray-100 dark:border-white/5"
						>
							<div
								class="flex justify-between mb-2 text-gray-600 dark:text-gray-400"
							>
								<span>Gross Weight</span>
								<span class="font-medium text-gray-900 dark:text-gray-200"
									>{{ formatWeight(details.gross_weight) }} g</span
								>
							</div>
							<div
								class="flex justify-between mb-2 text-red-400 dark:text-red-400/80"
							>
								<span>- Stone Weight</span>
								<span>{{ formatWeight(details.stone_weight) }} g</span>
							</div>
							<div
								class="flex justify-between pt-3 border-t border-gray-200 dark:border-white/10 mt-1"
							>
								<span class="font-bold text-gray-700 dark:text-white"
									>Net Weight</span
								>
								<span class="font-bold text-gray-900 dark:text-[#D4AF37] text-base"
									>{{ formatWeight(calculatedNetWeight) }} g</span
								>
							</div>
						</div>

						<div v-if="details.gemstones && details.gemstones.length > 0" class="mb-6">
							<h4
								class="text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-3"
							>
								Gemstone Details
							</h4>
							<div
								class="bg-white dark:bg-[#0F1115] rounded-lg border border-gray-100 dark:border-white/10 overflow-hidden"
							>
								<table class="w-full text-sm text-left">
									<thead class="bg-gray-50 dark:bg-white/5">
										<tr
											class="text-xs text-gray-500 dark:text-gray-400 uppercase"
										>
											<th class="px-4 py-2 font-medium">Stone</th>
											<th class="px-4 py-2 font-medium text-right">Carat</th>
										</tr>
									</thead>
									<tbody class="divide-y divide-gray-100 dark:divide-white/5">
										<tr v-for="(gem, i) in details.gemstones" :key="i">
											<td class="px-4 py-2.5">
												<div
													class="font-medium text-gray-900 dark:text-gray-200"
												>
													{{ gem.gem_type }}
												</div>
												<div
													class="text-[10px] text-gray-500 dark:text-gray-500"
												>
													{{ gem.cut }} • {{ gem.color }} •
													{{ gem.clarity }}
												</div>
											</td>
											<td
												class="px-4 py-2.5 text-right font-mono text-gray-700 dark:text-gray-300"
											>
												{{ gem.carat }}
											</td>
										</tr>
									</tbody>
								</table>
							</div>
						</div>

						<div class="space-y-3 mb-8 pt-2">
							<template v-if="details.net_weight > 0 && details.gold_rate > 0">
								<div class="flex justify-between text-sm">
									<span class="text-gray-500 dark:text-gray-400"
										>Gold Rate (Live)</span
									>
									<span class="text-gray-900 dark:text-gray-300 font-medium"
										>{{ formatCurrency(details.gold_rate) }} /g</span
									>
								</div>
								<div class="flex justify-between text-sm">
									<span class="text-gray-500 dark:text-gray-400"
										>Gold Value</span
									>
									<span class="text-gray-900 dark:text-gray-300 font-medium">{{
										formatCurrency(details.gold_value)
									}}</span>
								</div>
							</template>
							<div
								v-if="details.gemstone_value > 0"
								class="flex justify-between text-sm"
							>
								<span class="text-purple-600 dark:text-purple-400 font-medium"
									>Gemstone Value</span
								>
								<span class="text-purple-700 dark:text-purple-300 font-bold">{{
									formatCurrency(details.gemstone_value)
								}}</span>
							</div>

							<div
								class="flex justify-between items-end pt-4 border-t border-gray-100 dark:border-white/10 mt-2"
							>
								<div>
									<span class="text-lg font-bold text-gray-900 dark:text-white"
										>Total Price</span
									>
									<span
										v-if="details.price_source"
										class="ml-2 text-xs text-gray-400"
										>({{ details.price_source }})</span
									>
								</div>
								<span
									class="text-3xl font-serif font-bold text-gray-900 dark:text-white tracking-tight"
									>{{ formatCurrency(details.final_price) }}</span
								>
							</div>
						</div>

						<button
							@click="addToCart"
							class="w-full bg-gray-900 text-white dark:bg-[#D4AF37] dark:text-black py-4 rounded-xl font-bold text-lg hover:bg-gray-800 dark:hover:bg-[#b5952f] transition-all shadow-lg hover:shadow-xl transform active:scale-95 flex items-center justify-center gap-2"
						>
							<svg
								class="w-5 h-5"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
								></path>
							</svg>
							Add to Cart
						</button>
					</div>
				</div>
			</div>
		</div>
	</Transition>
</template>

<script setup>
import { createResource } from 'frappe-ui'
import { watch, ref, computed } from 'vue'
import { useCartStore } from '@/stores/cart.js'

const props = defineProps(['show', 'itemCode'])
const emit = defineEmits(['close'])
const cart = useCartStore()

const details = ref({})
const loading = ref(false)

const calculatedNetWeight = computed(() => {
	if (details.value.net_weight) return details.value.net_weight
	const gross = details.value.gross_weight || 0
	const stone = details.value.stone_weight || 0
	return Math.max(0, gross - stone)
})

const itemFetcher = createResource({
	url: 'zevar_core.api.pricing.get_item_price',
	makeParams() {
		return { item_code: props.itemCode }
	},
	onSuccess(data) {
		details.value = { ...data, item_code: props.itemCode }
		loading.value = false
	},
	onError(error) {
		console.error('Failed to load item:', error)
		loading.value = false
	},
})

watch(
	() => props.show,
	(isOpen) => {
		if (isOpen && props.itemCode) {
			loading.value = true
			details.value = {}
			itemFetcher.fetch()
		}
	}
)

function addToCart() {
	if (!details.value.item_code) return
	cart.addItem(details.value)
	emit('close')
}

function close() {
	emit('close')
}

function formatCurrency(val) {
	if (!val) return '$0.00'
	return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(val)
}

function formatWeight(val) {
	if (!val && val !== 0) return '0.000'
	return parseFloat(val).toFixed(3)
}
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
