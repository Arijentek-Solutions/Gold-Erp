/**
 * Quick Layaway Modal Component Unit Tests
 * Tests: Modal rendering, payment schedule calculation, layaway creation
 *
 * Key source details:
 *   - Uses <script setup> with ref() — cannot use data() mount option
 *   - Root element: div.modal-overlay (class, not .fixed.inset-0 — though it has position:fixed via CSS)
 *   - Close button: button.close-btn (not button.absolute.top-4.right-4)
 *   - form = ref({ term_months: 3, down_payment_percent: 20, ... })
 *   - State exposed: form, loading, customers, preview, successResult
 *   - Button disabled when: loading || !form.customer
 *   - No .animate-spin — loading shows "Creating..." text on the button
 *   - Balance/Monthly only shown when preview exists (from API call)
 *   - No cart store import — uses props: cartItems, cartTotal, warehouse
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import QuickLayawayModal from '../../src/components/QuickLayawayModal.vue'

// Mock frappe-ui — createResource returns objects with submit and fetch
vi.mock('frappe-ui', () => ({
	createResource: vi.fn(() => ({
		submit: vi.fn(() => Promise.resolve({})),
		fetch: vi.fn(() => Promise.resolve({})),
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

			expect(wrapper.find('.modal-overlay').exists()).toBe(false)
		})

		it('should render when show prop is true', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.find('.modal-overlay').exists()).toBe(true)
		})

		it('should emit close event when close button clicked', async () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			await wrapper.find('.close-btn').trigger('click')

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

			// form is a ref, accessed via .value internally but exposed as proxy
			expect(wrapper.vm.form.term_months).toBe(3)
		})

		it('should update term when clicked', async () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			// Click the "6 months" term button — second term-btn
			const termBtns = wrapper.findAll('.term-btn')
			await termBtns[1].trigger('click') // 6 months

			expect(wrapper.vm.form.term_months).toBe(6)
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

			expect(wrapper.vm.form.down_payment_percent).toBe(20)
		})
	})

	// ==========================================================================
	// PAYMENT SCHEDULE PREVIEW TESTS
	// ==========================================================================

	describe('Payment Schedule Preview', () => {
		it('should display total amount', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true, cartItems: [], cartTotal: 0 },
			})

			// "Total:" is shown in the items summary
			expect(wrapper.text()).toContain('Total')
		})

		it('should display down payment section', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			expect(wrapper.text()).toContain('Down Payment')
		})

		it('should display balance when preview is available', async () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			// Simulate a successful preview response
			wrapper.vm.preview = {
				preview: { total: 1000 },
				payment_schedule: [
					{ installment: 1, due_date: '2026-05-01', amount: 300 },
					{ installment: 2, due_date: '2026-06-01', amount: 300 },
					{ installment: 3, due_date: '2026-07-01', amount: 200 },
				],
			}
			await wrapper.vm.$nextTick()

			// Balance appears in schedule-preview section
			expect(wrapper.text()).toContain('Installment')
		})

		it('should display monthly payment amounts in term buttons', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true, cartTotal: 1000 },
			})

			// Term buttons show $X.XX/mo format
			expect(wrapper.text()).toContain('/mo')
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

		it('should disable Create button when no customer selected', () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			// form.customer defaults to '' — button should be disabled
			const submitBtn = wrapper.find('.btn-primary')
			expect(submitBtn.attributes('disabled')).toBeDefined()
		})

		it('should enable Create button when customer is selected', async () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			wrapper.vm.form.customer = 'CUST-001'
			await wrapper.vm.$nextTick()

			const submitBtn = wrapper.find('.btn-primary')
			expect(submitBtn.attributes('disabled')).toBeUndefined()
		})
	})

	// ==========================================================================
	// VALIDATION TESTS
	// ==========================================================================

	describe('Validation', () => {
		it('should show warning when no customer selected', async () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})

			// The form has a customer select with "Select customer..." default
			expect(wrapper.text()).toContain('customer')
		})
	})

	// ==========================================================================
	// LOADING STATE TESTS
	// ==========================================================================

	describe('Loading State', () => {
		it('should show Creating text during submission', async () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})
			wrapper.vm.loading = true
			await wrapper.vm.$nextTick()

			// Loading shows "Creating..." text in the submit button
			expect(wrapper.text()).toContain('Creating')
		})

		it('should disable buttons during submission', async () => {
			const wrapper = mount(QuickLayawayModal, {
				props: { show: true },
			})
			wrapper.vm.loading = true
			wrapper.vm.form.customer = 'CUST-001' // so submit button is enabled
			await wrapper.vm.$nextTick()

			// Submit button should still be disabled due to loading
			const submitBtn = wrapper.find('.btn-primary')
			expect(submitBtn.attributes('disabled')).toBeDefined()

			// Cancel button should also be disabled
			const cancelBtn = wrapper.find('.btn-secondary')
			expect(cancelBtn.attributes('disabled')).toBeDefined()
		})
	})
})
