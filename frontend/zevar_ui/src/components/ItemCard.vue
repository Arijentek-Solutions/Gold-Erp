<template>
	<div
		class="bg-white dark:bg-[#15171e] rounded-lg border border-gray-200 dark:border-gray-800 shadow-sm hover:shadow-md transition-all cursor-pointer flex flex-col h-full group relative overflow-hidden"
	>
		<div class="aspect-square bg-gray-100 dark:bg-gray-800 relative">
			<img
				v-if="item.image"
				:src="item.image"
				alt="Item"
				class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
				loading="lazy"
			/>
			<div
				v-else
				class="w-full h-full flex items-center justify-center text-gray-300 dark:text-gray-700"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-12 w-12"
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

			<div class="absolute top-2 right-2 flex flex-col gap-1 items-end">
				<span
					v-if="item.stock_qty <= 0"
					class="bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-200 text-[10px] font-bold px-1.5 py-0.5 rounded-full"
				>
					Out of Stock
				</span>
				<span
					v-else-if="item.stock_qty < 5"
					class="bg-orange-100 text-orange-800 dark:bg-orange-900/50 dark:text-orange-200 text-[10px] font-bold px-1.5 py-0.5 rounded-full"
				>
					Only {{ item.stock_qty }} left
				</span>
			</div>
		</div>

		<div class="p-3 flex-1 flex flex-col">
			<div class="flex items-start justify-between mb-1.5">
				<h3
					class="font-medium text-gray-900 dark:text-white line-clamp-2 text-xs leading-snug min-h-[2rem]"
				>
					{{ item.item_name }}
				</h3>
			</div>

			<div class="flex flex-wrap gap-1 mb-2">
				<span
					class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400"
				>
					{{ item.metal || 'Gold' }}
				</span>
				<span
					class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300"
				>
					{{ item.purity || 'Standard' }}
				</span>
			</div>

			<!-- Weight Breakdown -->
			<div
				v-if="item.net_weight > 0 || item.gross_weight > 0"
				class="hidden lg:block text-[9px] text-gray-500 dark:text-gray-400 mb-2 space-y-0.5 bg-gray-50 dark:bg-white/5 p-1.5 rounded"
			>
				<div v-if="item.gross_weight > 0" class="flex justify-between">
					<span>Gross:</span> <span>{{ item.gross_weight }}g</span>
				</div>
				<div
					v-if="item.stone_weight > 0"
					class="flex justify-between text-red-400 dark:text-red-400/80"
				>
					<span>Stone:</span> <span>-{{ item.stone_weight }}g</span>
				</div>
				<div
					v-if="item.net_weight > 0"
					class="flex justify-between font-bold text-gray-700 dark:text-gray-300 border-t border-gray-200 dark:border-white/10 pt-0.5 mt-0.5"
				>
					<span>Net:</span> <span>{{ item.net_weight }}g</span>
				</div>
			</div>

			<div
				class="mt-auto pt-2 border-t border-gray-50 dark:border-gray-800 flex items-center justify-between"
			>
				<div class="flex flex-col">
					<span class="text-[10px] text-gray-500 dark:text-gray-400">Price</span>
					<span class="text-base font-bold text-gray-900 dark:text-white leading-tight">
						{{ formatCurrency(item.price) }}
					</span>
				</div>

				<button
					@click.stop="quickAdd"
					class="bg-gray-900 dark:bg-white text-white dark:text-black p-1.5 rounded-lg hover:bg-gray-700 dark:hover:bg-gray-200 transition-colors shadow-sm active:scale-95"
					title="Add to Cart"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-4 w-4"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 4v16m8-8H4"
						/>
					</svg>
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import { useCartStore } from '@/stores/cart.js'

const props = defineProps({
	item: {
		type: Object,
		required: true,
		default: () => ({}),
	},
})

const cart = useCartStore()

function quickAdd() {
	cart.addItem(props.item)
}

function formatCurrency(value) {
	if (!value) return '$0.00'
	return new Intl.NumberFormat('en-US', {
		style: 'currency',
		currency: 'USD',
	}).format(value)
}
</script>
