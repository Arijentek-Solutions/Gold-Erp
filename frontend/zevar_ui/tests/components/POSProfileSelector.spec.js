/**
 * POS Profile Selector Component Unit Tests
 * Tests: Dropdown rendering, profile selection, active profile display
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import POSProfileSelector from '../../src/components/POSProfileSelector.vue'

// Mock frappe-ui
vi.mock('frappe-ui', () => ({
	createResource: vi.fn(() => ({
		fetch: vi.fn(),
	})),
}))

// Mock posProfile store
vi.mock('../../src/stores/posProfile.js', () => ({
	usePOSProfileStore: vi.fn(() => ({
		profiles: [
			{ name: 'Main POS', company: 'Zevar Jewelry', warehouse: 'Main Warehouse' },
			{ name: 'Outlet POS', company: 'Zevar Jewelry', warehouse: 'Outlet Warehouse' },
		],
		activeProfile: { name: 'Main POS', company: 'Zevar Jewelry' },
		profileName: 'Main POS',
		hasActiveProfile: true,
		setActiveProfile: vi.fn(),
		fetchProfiles: vi.fn(),
	})),
}))

describe('POSProfileSelector', () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.clearAllMocks()
	})

	// ==========================================================================
	// RENDERING TESTS
	// ==========================================================================

	describe('Rendering', () => {
		it('should render profile selector container', () => {
			const wrapper = mount(POSProfileSelector)

			expect(wrapper.find('.profile-selector').exists()).toBe(true)
		})

		it('should display current profile name', () => {
			const wrapper = mount(POSProfileSelector)

			expect(wrapper.text()).toContain('Main POS')
		})

		it('should show dropdown icon', () => {
			const wrapper = mount(POSProfileSelector)

			expect(wrapper.find('svg').exists()).toBe(true)
		})

		it('should show active indicator when profile is set', () => {
			const wrapper = mount(POSProfileSelector)

			// Active profile should show green indicator
			const indicator = wrapper.find('.bg-green-500')
			expect(indicator.exists()).toBe(true)
		})
	})

	// ==========================================================================
	// DROPDOWN INTERACTION TESTS
	// ==========================================================================

	describe('Dropdown Interaction', () => {
		it('should toggle dropdown on click', async () => {
			const wrapper = mount(POSProfileSelector)

			// Initially dropdown should be closed
			expect(wrapper.vm.isOpen).toBe(false)

			// Click to open
			await wrapper.find('.profile-selector').trigger('click')
			expect(wrapper.vm.isOpen).toBe(true)
		})

		it('should close dropdown when clicking outside', async () => {
			const wrapper = mount(POSProfileSelector)
			wrapper.vm.isOpen = true

			// Trigger click outside
			await wrapper.vm.handleClickOutside({ target: document.body })

			expect(wrapper.vm.isOpen).toBe(false)
		})
	})

	// ==========================================================================
	// PROFILE SELECTION TESTS
	// ==========================================================================

	describe('Profile Selection', () => {
		it('should emit change event when profile selected', async () => {
			const mockSetActive = vi.fn()
			const mockUsePOSProfileStore = await import('../../src/stores/posProfile.js')
			mockUsePOSProfileStore.usePOSProfileStore.mockReturnValue({
				profiles: [
					{ name: 'Main POS', company: 'Zevar Jewelry' },
					{ name: 'Outlet POS', company: 'Zevar Jewelry' },
				],
				activeProfile: { name: 'Main POS' },
				profileName: 'Main POS',
				hasActiveProfile: true,
				setActiveProfile: mockSetActive,
				fetchProfiles: vi.fn(),
			})

			const wrapper = mount(POSProfileSelector)

			// Select a profile
			await wrapper.vm.selectProfile({ name: 'Outlet POS' })

			expect(wrapper.emitted('change')).toBeTruthy()
		})
	})

	// ==========================================================================
	// NO PROFILES STATE TESTS
	// ==========================================================================

	describe('No Profiles State', () => {
		it('should show message when no profiles available', async () => {
			const mockUsePOSProfileStore = await import('../../src/stores/posProfile.js')
			mockUsePOSProfileStore.usePOSProfileStore.mockReturnValue({
				profiles: [],
				activeProfile: null,
				profileName: 'Select Profile',
				hasActiveProfile: false,
				setActiveProfile: vi.fn(),
				fetchProfiles: vi.fn(),
			})

			const wrapper = mount(POSProfileSelector)
			wrapper.vm.isOpen = true
			await wrapper.vm.$nextTick()

			expect(wrapper.text()).toContain('No profiles')
		})
	})

	// ==========================================================================
	// LOADING STATE TESTS
	// ==========================================================================

	describe('Loading State', () => {
		it('should show loading spinner when loading', async () => {
			const mockUsePOSProfileStore = await import('../../src/stores/posProfile.js')
			mockUsePOSProfileStore.usePOSProfileStore.mockReturnValue({
				profiles: [],
				activeProfile: null,
				profileName: 'Select Profile',
				hasActiveProfile: false,
				loading: true,
				setActiveProfile: vi.fn(),
				fetchProfiles: vi.fn(),
			})

			const wrapper = mount(POSProfileSelector)

			expect(wrapper.find('.animate-spin').exists()).toBe(true)
		})
	})
})
