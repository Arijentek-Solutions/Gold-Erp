/**
 * POS Profile Store Unit Tests
 * Tests: Profile state management, active profile, localStorage persistence
 *
 * Key source details:
 *   - Export: usePosProfileStore (lowercase 'p' in Pos)
 *   - profileName default: 'No Profile Selected'
 *   - localStorage key: 'pos_profile'
 *   - No storeLocation property
 *   - setActiveProfile(profileName) takes a string, calls API resource
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { usePosProfileStore } from '../../src/stores/posProfile.js'

// Mock frappe-ui
vi.mock('frappe-ui', () => ({
	createResource: vi.fn(() => ({
		fetch: vi.fn(() => Promise.resolve({ profiles: [], active_profile: null })),
		submit: vi.fn(() => Promise.resolve({ success: true })),
	})),
}))

describe('POS Profile Store', () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		localStorage.clear()
	})

	// ==========================================================================
	// STATE INITIALIZATION TESTS
	// ==========================================================================

	describe('State Initialization', () => {
		it('should initialize with empty profiles array', () => {
			const store = usePosProfileStore()
			expect(store.profiles).toEqual([])
		})

		it('should initialize with null active profile', () => {
			const store = usePosProfileStore()
			expect(store.activeProfile).toBeNull()
		})

		it('should initialize with loading false', () => {
			const store = usePosProfileStore()
			expect(store.loading).toBe(false)
		})

		it('should initialize with null error', () => {
			const store = usePosProfileStore()
			expect(store.error).toBeNull()
		})
	})

	// ==========================================================================
	// COMPUTED PROPERTIES TESTS
	// ==========================================================================

	describe('Computed Properties', () => {
		it('should return true when active profile is set', () => {
			const store = usePosProfileStore()
			store.activeProfile = { name: 'Main POS', company: 'Zevar Jewelry' }

			expect(store.hasActiveProfile).toBe(true)
		})

		it('should return false when no active profile', () => {
			const store = usePosProfileStore()

			expect(store.hasActiveProfile).toBe(false)
		})

		it('should return profile name when active', () => {
			const store = usePosProfileStore()
			store.activeProfile = { name: 'Main POS' }

			expect(store.profileName).toBe('Main POS')
		})

		it('should return "No Profile Selected" when no active profile', () => {
			const store = usePosProfileStore()

			expect(store.profileName).toBe('No Profile Selected')
		})

		it('should return warehouse from active profile', () => {
			const store = usePosProfileStore()
			store.activeProfile = { warehouse: 'Main Warehouse' }

			expect(store.warehouse).toBe('Main Warehouse')
		})

		it('should return null warehouse when no active profile', () => {
			const store = usePosProfileStore()

			expect(store.warehouse).toBeNull()
		})

		it('should return company from active profile', () => {
			const store = usePosProfileStore()
			store.activeProfile = { company: 'Zevar Jewelry' }

			expect(store.company).toBe('Zevar Jewelry')
		})

		it('should return null company when no active profile', () => {
			const store = usePosProfileStore()

			expect(store.company).toBeNull()
		})
	})

	// ==========================================================================
	// CLEAR PROFILE TESTS
	// ==========================================================================

	describe('clearProfile', () => {
		it('should clear active profile', () => {
			const store = usePosProfileStore()
			store.activeProfile = { name: 'Main POS' }

			store.clearProfile()

			expect(store.activeProfile).toBeNull()
		})

		it('should clear localStorage', () => {
			const store = usePosProfileStore()
			localStorage.setItem('pos_profile', JSON.stringify({ name: 'Main POS' }))

			store.clearProfile()

			expect(localStorage.getItem('pos_profile')).toBeNull()
		})
	})

	// ==========================================================================
	// LOCALSTORAGE PERSISTENCE TESTS
	// ==========================================================================

	describe('LocalStorage Persistence', () => {
		it('should load profile from localStorage on init', () => {
			localStorage.setItem('pos_profile', JSON.stringify({
				name: 'Saved Profile',
				company: 'Test Company',
			}))

			// Create a fresh pinia + store — initFromStorage runs in the store constructor
			setActivePinia(createPinia())
			const store = usePosProfileStore()

			expect(store.activeProfile).toEqual({
				name: 'Saved Profile',
				company: 'Test Company',
			})
		})

		it('should handle corrupted localStorage data gracefully', () => {
			localStorage.setItem('pos_profile', 'invalid json')

			setActivePinia(createPinia())
			const store = usePosProfileStore()

			expect(store.activeProfile).toBeNull()
		})

		it('should not set activeProfile when localStorage is empty', () => {
			const store = usePosProfileStore()

			expect(store.activeProfile).toBeNull()
		})
	})

	// ==========================================================================
	// RESOURCE EXISTENCE TESTS
	// ==========================================================================

	describe('Resources', () => {
		it('should expose profilesResource', () => {
			const store = usePosProfileStore()
			expect(store.profilesResource).toBeDefined()
			expect(typeof store.profilesResource.fetch).toBe('function')
		})

		it('should expose activeProfileResource', () => {
			const store = usePosProfileStore()
			expect(store.activeProfileResource).toBeDefined()
			expect(typeof store.activeProfileResource.fetch).toBe('function')
		})

		it('should expose setActiveProfileResource', () => {
			const store = usePosProfileStore()
			expect(store.setActiveProfileResource).toBeDefined()
			expect(typeof store.setActiveProfileResource.submit).toBe('function')
		})
	})
})
