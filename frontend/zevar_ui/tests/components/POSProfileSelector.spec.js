/**
 * POS Profile Selector Component Unit Tests
 * Tests: Dropdown rendering, profile selection, active profile display
 *
 * Key source details:
 *   - Uses .pos-profile-selector root class
 *   - Uses showDropdown ref (not isOpen)
 *   - Uses emoji 🏪 and ▼ (not SVG icons)
 *   - Loading shows text "Loading profiles..." (not .animate-spin)
 *   - Empty state shows "No profiles available"
 *   - Close via .dropdown-backdrop click (not handleClickOutside)
 *   - selectProfile(profileName) takes a string, calls store.setActiveProfile, no emit
 *   - profile-btn is disabled when loading=true — so we must force showDropdown for loading test
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import POSProfileSelector from '../../src/components/POSProfileSelector.vue'

// Mock frappe-ui
vi.mock('frappe-ui', () => ({
	createResource: vi.fn(() => ({
		fetch: vi.fn(),
		submit: vi.fn(),
	})),
}))

// Helper to create a mock store return value
function createMockStore(overrides = {}) {
	return {
		profiles: [
			{ name: 'Main POS', company: 'Zevar Jewelry', warehouse: 'Main Warehouse' },
			{ name: 'Outlet POS', company: 'Zevar Jewelry', warehouse: 'Outlet Warehouse' },
		],
		activeProfile: { name: 'Main POS', company: 'Zevar Jewelry' },
		profileName: 'Main POS',
		hasActiveProfile: true,
		loading: false,
		error: null,
		setActiveProfile: vi.fn(() => Promise.resolve()),
		loadProfiles: vi.fn(() => Promise.resolve()),
		...overrides,
	}
}

// Mock posProfile store — note: usePosProfileStore (lowercase 'p')
vi.mock('../../src/stores/posProfile.js', () => ({
	usePosProfileStore: vi.fn(),
}))

import { usePosProfileStore } from '../../src/stores/posProfile.js'

describe('POSProfileSelector', () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		vi.clearAllMocks()
		usePosProfileStore.mockReturnValue(createMockStore())
	})

	// ==========================================================================
	// RENDERING TESTS
	// ==========================================================================

	describe('Rendering', () => {
		it('should render profile selector container', () => {
			const wrapper = mount(POSProfileSelector)

			expect(wrapper.find('.pos-profile-selector').exists()).toBe(true)
		})

		it('should display current profile name', () => {
			const wrapper = mount(POSProfileSelector)

			expect(wrapper.text()).toContain('Main POS')
		})

		it('should show profile icon (emoji)', () => {
			const wrapper = mount(POSProfileSelector)

			expect(wrapper.text()).toContain('🏪')
		})

		it('should show dropdown arrow', () => {
			const wrapper = mount(POSProfileSelector)

			expect(wrapper.text()).toContain('▼')
		})

		it('should render profile button', () => {
			const wrapper = mount(POSProfileSelector)

			expect(wrapper.find('.profile-btn').exists()).toBe(true)
		})
	})

	// ==========================================================================
	// DROPDOWN INTERACTION TESTS
	// ==========================================================================

	describe('Dropdown Interaction', () => {
		it('should toggle dropdown on button click', async () => {
			const wrapper = mount(POSProfileSelector)

			// Initially dropdown should be closed
			expect(wrapper.vm.showDropdown).toBe(false)

			// Click button to open
			await wrapper.find('.profile-btn').trigger('click')
			expect(wrapper.vm.showDropdown).toBe(true)
		})

		it('should close dropdown when clicking backdrop', async () => {
			const wrapper = mount(POSProfileSelector)

			// Open the dropdown
			await wrapper.find('.profile-btn').trigger('click')
			expect(wrapper.vm.showDropdown).toBe(true)

			// Click the backdrop to close
			await wrapper.find('.dropdown-backdrop').trigger('click')
			expect(wrapper.vm.showDropdown).toBe(false)
		})

		it('should show dropdown-menu when showDropdown is true', async () => {
			const wrapper = mount(POSProfileSelector)

			expect(wrapper.find('.dropdown-menu').exists()).toBe(false)

			await wrapper.find('.profile-btn').trigger('click')

			expect(wrapper.find('.dropdown-menu').exists()).toBe(true)
		})

		it('should show dropdown-backdrop when showDropdown is true', async () => {
			const wrapper = mount(POSProfileSelector)

			expect(wrapper.find('.dropdown-backdrop').exists()).toBe(false)

			await wrapper.find('.profile-btn').trigger('click')

			expect(wrapper.find('.dropdown-backdrop').exists()).toBe(true)
		})
	})

	// ==========================================================================
	// PROFILE SELECTION TESTS
	// ==========================================================================

	describe('Profile Selection', () => {
		it('should call store.setActiveProfile when profile selected', async () => {
			const mockSetActive = vi.fn(() => Promise.resolve())
			usePosProfileStore.mockReturnValue(
				createMockStore({
					setActiveProfile: mockSetActive,
				})
			)

			const wrapper = mount(POSProfileSelector)

			// Open dropdown
			await wrapper.find('.profile-btn').trigger('click')

			// Click on a profile option
			const options = wrapper.findAll('.profile-option')
			await options[1].trigger('click') // Click "Outlet POS"

			expect(mockSetActive).toHaveBeenCalledWith('Outlet POS')
		})

		it('should close dropdown after selecting a profile', async () => {
			const wrapper = mount(POSProfileSelector)

			// Open dropdown
			await wrapper.find('.profile-btn').trigger('click')
			expect(wrapper.vm.showDropdown).toBe(true)

			// Click on a profile option
			const options = wrapper.findAll('.profile-option')
			await options[0].trigger('click')

			expect(wrapper.vm.showDropdown).toBe(false)
		})

		it('should show check mark on active profile', async () => {
			const wrapper = mount(POSProfileSelector)

			// Open dropdown
			await wrapper.find('.profile-btn').trigger('click')

			// First option (Main POS) is active
			const options = wrapper.findAll('.profile-option')
			expect(options[0].find('.check-mark').exists()).toBe(true)
			expect(options[1].find('.check-mark').exists()).toBe(false)
		})
	})

	// ==========================================================================
	// NO PROFILES STATE TESTS
	// ==========================================================================

	describe('No Profiles State', () => {
		it('should show message when no profiles available', async () => {
			usePosProfileStore.mockReturnValue(
				createMockStore({
					profiles: [],
					activeProfile: null,
					profileName: 'No Profile Selected',
					hasActiveProfile: false,
				})
			)

			const wrapper = mount(POSProfileSelector)

			// Open dropdown
			await wrapper.find('.profile-btn').trigger('click')

			expect(wrapper.text()).toContain('No profiles available')
		})
	})

	// ==========================================================================
	// LOADING STATE TESTS
	// ==========================================================================

	describe('Loading State', () => {
		it('should show loading text when loading', async () => {
			usePosProfileStore.mockReturnValue(
				createMockStore({
					loading: true,
					profiles: [],
					activeProfile: null,
					profileName: 'No Profile Selected',
					hasActiveProfile: false,
				})
			)

			const wrapper = mount(POSProfileSelector)

			// Loading=true disables the button, so we can't click to open.
			// Force showDropdown open instead.
			wrapper.vm.showDropdown = true
			await wrapper.vm.$nextTick()

			expect(wrapper.text()).toContain('Loading profiles...')
		})
	})

	// ==========================================================================
	// ERROR STATE TESTS
	// ==========================================================================

	describe('Error State', () => {
		it('should show error message when error exists', async () => {
			usePosProfileStore.mockReturnValue(
				createMockStore({
					error: 'Failed to load profiles',
					profiles: [],
					activeProfile: null,
					profileName: 'No Profile Selected',
					hasActiveProfile: false,
				})
			)

			const wrapper = mount(POSProfileSelector)

			// Open dropdown
			await wrapper.find('.profile-btn').trigger('click')

			expect(wrapper.text()).toContain('Failed to load profiles')
		})
	})
})
