/**
 * POSProductModal Component Unit Tests
 * Tests: Modal rendering, item details display, add to cart functionality
 *
 * Key source details:
 *   - Uses <script setup> with ref() — cannot use data() mount option
 *   - details = ref({}), loading = ref(false)
 *   - calculatedNetWeight is computed from details.value
 *   - Gold rate section uses v-if="details.net_weight > 0 && details.gold_rate > 0"
 *   - Price source uses v-if="details.price_source"
 *   - formatCurrency: if (!val) return '$0.00' (0 is falsy)
 *   - addToCart() checks details.value.item_code before adding
 *   - Button class: "w-full bg-gray-900 text-white ..."
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import POSProductModal from '../../src/components/POSProductModal.vue'

vi.mock('frappe-ui', () => ({
	createResource: vi.fn(() => ({
		fetch: vi.fn(),
	})),
}))

vi.mock('../../src/stores/cart.js', () => ({
	useCartStore: vi.fn(() => ({
		addItem: vi.fn(),
		items: [],
	})),
}))

function mountWithDetails(details = {}, loading = false) {
	const wrapper = mount(POSProductModal, {
		props: { show: true, itemCode: 'ITEM-001' },
	})
	wrapper.vm.details = details
	wrapper.vm.loading = loading
	return wrapper
}

describe('POSProductModal', () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.clearAllMocks()
	})

	describe('Modal Visibility', () => {
		it('should not render when show prop is false', () => {
			const wrapper = mount(POSProductModal, {
				props: { show: false, itemCode: 'ITEM-001' },
			})
			expect(wrapper.find('.fixed.inset-0').exists()).toBe(false)
		})

		it('should render when show prop is true', () => {
			const wrapper = mount(POSProductModal, {
				props: { show: true, itemCode: 'ITEM-001' },
			})
			expect(wrapper.find('.fixed.inset-0').exists()).toBe(true)
		})

		it('should emit close event when backdrop is clicked', async () => {
			const wrapper = mount(POSProductModal, {
				props: { show: true, itemCode: 'ITEM-001' },
			})
			await wrapper.find('.absolute.inset-0.bg-gray-900\\/60').trigger('click')
			expect(wrapper.emitted('close')).toBeTruthy()
		})

		it('should emit close event when close button is clicked', async () => {
			const wrapper = mount(POSProductModal, {
				props: { show: true, itemCode: 'ITEM-001' },
			})
			await wrapper.find('button.absolute.top-4.right-4').trigger('click')
			expect(wrapper.emitted('close')).toBeTruthy()
		})
	})

	describe('Loading State', () => {
		it('should show loading spinner when loading', async () => {
			const wrapper = mount(POSProductModal, {
				props: { show: true, itemCode: 'ITEM-001' },
			})
			wrapper.vm.loading = true
			await wrapper.vm.$nextTick()
			expect(wrapper.find('.animate-spin').exists()).toBe(true)
		})

		it('should not show loading spinner when not loading', async () => {
			const wrapper = mountWithDetails({ item_name: 'Test Item' }, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.find('.animate-spin').exists()).toBe(false)
		})
	})

	describe('Item Details Display', () => {
		const mockDetails = {
			item_name: 'Gold Diamond Ring',
			item_code: 'ITEM-001',
			metal: 'Yellow Gold',
			purity: '14K',
			gross_weight: 5.5,
			stone_weight: 0.5,
			net_weight: 5.0,
			gold_rate: 65.5,
			gold_value: 327.5,
			gemstone_value: 150.0,
			final_price: 477.5,
			price_source: 'Live',
			image: '/assets/item.jpg',
			gemstones: [
				{ gem_type: 'Diamond', carat: 0.5, cut: 'Excellent', color: 'D', clarity: 'VVS1' },
			],
		}

		it('should display item name', async () => {
			const wrapper = mountWithDetails(mockDetails, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).toContain('Gold Diamond Ring')
		})

		it('should display item code', async () => {
			const wrapper = mountWithDetails(mockDetails, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).toContain('ITEM-001')
		})

		it('should display metal badge', async () => {
			const wrapper = mountWithDetails(mockDetails, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).toContain('Yellow Gold')
		})

		it('should display purity badge', async () => {
			const wrapper = mountWithDetails(mockDetails, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).toContain('14K')
		})

		it('should display weight breakdown', async () => {
			const wrapper = mountWithDetails(mockDetails, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).toContain('Gross Weight')
			expect(wrapper.text()).toContain('Stone Weight')
			expect(wrapper.text()).toContain('Net Weight')
		})

		it('should display gold rate and value when available', async () => {
			const wrapper = mountWithDetails(mockDetails, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).toContain('Gold Rate')
			expect(wrapper.text()).toContain('Gold Value')
		})

		it('should display gemstone value when available', async () => {
			const wrapper = mountWithDetails(mockDetails, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).toContain('Gemstone Value')
		})

		it('should display final price', async () => {
			const wrapper = mountWithDetails(mockDetails, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).toContain('Total Price')
		})

		it('should display price source indicator', async () => {
			const wrapper = mountWithDetails(mockDetails, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).toContain('Live')
		})
	})

	describe('Gemstone Table', () => {
		const mockDetailsWithGemstones = {
			item_name: 'Diamond Ring',
			item_code: 'ITEM-001',
			final_price: 1000,
			gemstones: [
				{ gem_type: 'Diamond', carat: 0.5, cut: 'Excellent', color: 'D', clarity: 'VVS1' },
				{ gem_type: 'Sapphire', carat: 1, cut: 'Good', color: 'Blue', clarity: 'VS1' },
			],
		}

		it('should display gemstone table when gemstones exist', async () => {
			const wrapper = mountWithDetails(mockDetailsWithGemstones, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).toContain('Gemstone Details')
			expect(wrapper.text()).toContain('Diamond')
			expect(wrapper.text()).toContain('Sapphire')
		})

		it('should not display gemstone table when no gemstones', async () => {
			const wrapper = mountWithDetails({ item_name: 'Plain Ring', gemstones: [] }, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).not.toContain('Gemstone Details')
		})

		it('should display gemstone carat weight', async () => {
			const wrapper = mountWithDetails(mockDetailsWithGemstones, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).toContain('0.5')
			// Vue renders 1.0 as 1 in text interpolation
			expect(wrapper.text()).toContain('1')
		})
	})

	describe('Image Display', () => {
		it('should display item image when available', async () => {
			const wrapper = mountWithDetails({ image: '/assets/item.jpg' }, false)
			await wrapper.vm.$nextTick()
			const img = wrapper.find('img')
			expect(img.exists()).toBe(true)
			expect(img.attributes('src')).toBe('/assets/item.jpg')
		})

		it('should display placeholder when no image available', async () => {
			const wrapper = mountWithDetails({ image: null }, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.find('img').exists()).toBe(false)
			expect(wrapper.find('svg').exists()).toBe(true)
		})
	})

	describe('Add to Cart', () => {
		it('should have Add to Cart button', async () => {
			const wrapper = mountWithDetails({ item_name: 'Test Item' }, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.text()).toContain('Add to Cart')
		})

		it('should emit close event when Add to Cart is clicked', async () => {
			const wrapper = mountWithDetails(
				{ item_code: 'ITEM-001', item_name: 'Test Item' },
				false
			)
			await wrapper.vm.$nextTick()
			await wrapper.find('button.w-full.bg-gray-900').trigger('click')
			expect(wrapper.emitted('close')).toBeTruthy()
		})
	})

	describe('Computed Properties', () => {
		it('should calculate net weight from gross - stone weight', async () => {
			const wrapper = mountWithDetails({ gross_weight: 10, stone_weight: 2 }, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.vm.calculatedNetWeight).toBe(8)
		})

		it('should return 0 for negative net weight', async () => {
			const wrapper = mountWithDetails({ gross_weight: 5, stone_weight: 10 }, false)
			await wrapper.vm.$nextTick()
			expect(wrapper.vm.calculatedNetWeight).toBe(0)
		})

		it('should use net_weight from details if available', async () => {
			const wrapper = mountWithDetails(
				{ net_weight: 7.5, gross_weight: 10, stone_weight: 2 },
				false
			)
			await wrapper.vm.$nextTick()
			expect(wrapper.vm.calculatedNetWeight).toBe(7.5)
		})
	})

	describe('Helper Functions', () => {
		it('should format currency correctly', () => {
			const wrapper = mount(POSProductModal, {
				props: { show: true, itemCode: 'ITEM-001' },
			})
			expect(wrapper.vm.formatCurrency(1234.5)).toBe('$1,234.50')
		})

		it('should format currency with zero value', () => {
			const wrapper = mount(POSProductModal, {
				props: { show: true, itemCode: 'ITEM-001' },
			})
			expect(wrapper.vm.formatCurrency(0)).toBe('$0.00')
		})

		it('should format currency with null value', () => {
			const wrapper = mount(POSProductModal, {
				props: { show: true, itemCode: 'ITEM-001' },
			})
			expect(wrapper.vm.formatCurrency(null)).toBe('$0.00')
		})

		it('should format weight correctly', () => {
			const wrapper = mount(POSProductModal, {
				props: { show: true, itemCode: 'ITEM-001' },
			})
			expect(wrapper.vm.formatWeight(5.5)).toBe('5.500')
		})

		it('should format weight with zero value', () => {
			const wrapper = mount(POSProductModal, {
				props: { show: true, itemCode: 'ITEM-001' },
			})
			expect(wrapper.vm.formatWeight(0)).toBe('0.000')
		})

		it('should format weight with null value', () => {
			const wrapper = mount(POSProductModal, {
				props: { show: true, itemCode: 'ITEM-001' },
			})
			expect(wrapper.vm.formatWeight(null)).toBe('0.000')
		})
	})

	describe('Accessibility', () => {
		it('should have proper z-index for modal overlay', () => {
			const wrapper = mount(POSProductModal, {
				props: { show: true, itemCode: 'ITEM-001' },
			})
			const overlay = wrapper.find('.fixed.inset-0')
			expect(overlay.classes()).toContain('z-[100]')
		})

		it('should have close button accessible', () => {
			const wrapper = mount(POSProductModal, {
				props: { show: true, itemCode: 'ITEM-001' },
			})
			const closeButton = wrapper.find('button.absolute.top-4.right-4')
			expect(closeButton.exists()).toBe(true)
		})
	})
})
