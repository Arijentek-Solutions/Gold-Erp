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
      <div v-else class="w-full h-full flex items-center justify-center text-gray-300 dark:text-gray-700">
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

      <div class="absolute top-2 right-2">
        <span
          v-if="item.stock_qty <= 0"
          class="bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-200 text-xs font-bold px-2 py-1 rounded-full"
        >
          Out of Stock
        </span>
        <span
          v-else-if="item.stock_qty < 5"
          class="bg-orange-100 text-orange-800 dark:bg-orange-900/50 dark:text-orange-200 text-xs font-bold px-2 py-1 rounded-full"
        >
          Only {{ item.stock_qty }} left
        </span>
      </div>
    </div>

    <div class="p-4 flex-1 flex flex-col">
      <div class="flex items-start justify-between mb-2">
        <h3
          class="font-medium text-gray-900 dark:text-white line-clamp-2 text-sm leading-snug min-h-[2.5rem]"
        >
          {{ item.item_name }}
        </h3>
      </div>

      <div class="flex flex-wrap gap-1 mb-3">
        <span
          class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400"
        >
          {{ item.metal || 'Gold' }}
        </span>
        <span
          class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300"
        >
          {{ item.purity || 'Standard' }}
        </span>
      </div>

      <div class="mt-auto pt-3 border-t border-gray-50 dark:border-gray-800 flex items-center justify-between">
        <div class="flex flex-col">
          <span class="text-xs text-gray-500 dark:text-gray-400">Price</span>
          <span class="text-lg font-bold text-gray-900 dark:text-white">
            {{ formatCurrency(item.price) }}
          </span>
        </div>

        <button
          @click.stop="quickAdd"
          class="bg-gray-900 dark:bg-white text-white dark:text-black p-2 rounded-lg hover:bg-gray-700 dark:hover:bg-gray-200 transition-colors shadow-md active:scale-95"
          title="Add to Cart"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
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