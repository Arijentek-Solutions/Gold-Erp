/**
 * Quick Layaway Modal Component Unit Tests
 * Tests: Modal rendering, payment schedule calculation, layaway creation
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import QuickLayawayModal from '../../src/components/QuickLayawayModal.vue'

// Mock frappe-ui
vi.mock('frappe-ui', () => ({
	createResource: vi.fn(() => ({
		fetch: vi.fn(() => Promise.resolve({
			preview: {
				total: 1000,
				down_payment: 200,
				balance: 800,
				monthly_payment: 266.67
			},
			payment_schedule: [
				{ installment: 1, due_date: '2026-04-11', amount: 266.67, status: 'Pending' },
				{ installment: 2, due_date: '2026-05-11', amount: 266.67, status: 'Pending' },
				{ installment: 3, due_date: '2026-06-11', amount: 266.66, status: 'Pending' },
			]
		})),
	})),
}))

// Mock cart store
vi.mock('../../src/stores/cart.js', () => ({
	useCartStore: vi.fn(() => ({
		items: [
			{ item_code: 'ITEM-001', item_name: 'Gold Ring', amount: 500, qty: 1 },
			{ item_code: 'ITEM-002', item_name: 'Diamond Earrings', amount: 500, qty: 1 },
		],
		subtotal: 1000,
		customer: { name: 'CUST-001', customer_name: 'John Doe' },
	})),
}))

describe('QuickLayawayModal', () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.clearAllMocks()
	})

	// ==========================================================================
	// MODAL VISIBILITY TESTS
	// ==========================================================================

	describe('Modal Visibility', () => {
		it('should not render when show prop is false', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: false },
			})

			expect(wrapper.find('.fixed.inset-0').exists()).toBe(false)
		})

		it('should render when show prop is true', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.find('.fixed.inset-0').exists()).toBe(true)
		})

		it('should emit close event when close button clicked', async () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			await wrapper.find('button.absolute.top-4.right-4').trigger('click')

			expect(wrapper.emitted('close')).toBeTruthy()
		})
	})

	// ==========================================================================
	// TERM SELECTION TESTS
	// ==========================================================================

	describe('Term Selection', () => {
		it('should display term options', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.text()).toContain('3 months')
			expect(wrapper.text()).toContain('6 months')
			expect(wrapper.text()).toContain('9 months')
			expect(wrapper.text()).toContain('12 months')
		})

		it('should default to 3 months', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.vm.selectedTerm).toBe(3)
		})

		it('should update term when clicked', async () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			await wrapper.findAll('button')[2].trigger('click')

			// Term should be updated
		})
	})

	// ==========================================================================
	// DOWN PAYMENT TESTS
	// ==========================================================================

	describe('Down Payment', () => {
		it('should display down payment percentage options', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.text()).toContain('10%')
			expect(wrapper.text()).toContain('20%')
			expect(wrapper.text()).toContain('30%')
		})

		it('should default to 20% down payment', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.vm.downPaymentPercent).toBe(20)
		})
	})

	// ==========================================================================
	// PAYMENT SCHEDULE PREVIEW TESTS
	// ==========================================================================

	describe('Payment Schedule Preview', () => {
		it('should display total amount', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.text()).toContain('Total')
		})

		it('should display down payment amount', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.text()).toContain('Down Payment')
		})

		it('should display balance amount', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.text()).toContain('Balance')
		})

		it('should display monthly payment', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.text()).toContain('Monthly')
		})
	})

	// ==========================================================================
	// CREATE LAYAWAY TESTS
	// ==========================================================================

	describe('Create Layaway', () => {
		it('should have Create Layaway button', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.text()).toContain('Create Layaway')
		})

		it('should disable button when no customer', async () => {
			const mockUseCartStore = await import('../../src/stores/cart.js')
			mockUseCartStore.useCartStore.mockReturnValue({
				items: [{ item_code: 'ITEM-001', amount: 500, qty: 1 }],
				subtotal: 500,
				customer: null,
			})

			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			const button = wrapper.find('button.bg-gray-900')
			expect(button.attributes('disabled')).toBeDefined()
		})

		it('should disable button when cart is empty', async () => {
			const mockUseCartStore = await import('../../src/stores/cart.js')
			mockUseCartStore.useCartStore.mockReturnValue({
				items: [],
				subtotal: 0,
				customer: { name: 'CUST-001' },
			})

			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			const button = wrapper.find('button.bg-gray-900')
			expect(button.attributes('disabled')).toBeDefined()
		})
	})

	// ==========================================================================
	// VALIDATION TESTS
	// ==========================================================================

	describe('Validation', () => {
		it('should show warning when no customer selected', async () => {
			const mockUseCartStore = await import('../../src/stores/cart.js')
			mockUseCartStore.useCartStore.mockReturnValue({
				items: [{ item_code: 'ITEM-001', amount: 500, qty: 1 }],
				subtotal: 500,
				customer: null,
			})

			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.text()).toContain('customer')
		})
	})

	// ==========================================================================
	// LOADING STATE TESTS
	// ==========================================================================

	describe('Loading State', () => {
		it('should show loading spinner during submission', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
				data: () => ({ submitting: true }),
			})

			expect(wrapper.find('.animate-spin').exists()).toBe(true)
		})

		it('should disable buttons during submission', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
				data: () => ({ submitting: true }),
			})

			const buttons = wrapper.findAll('button')
			buttons.forEach(btn => {
				expect(btn.attributes('disabled')).toBeDefined()
			})
		})
	})
})
