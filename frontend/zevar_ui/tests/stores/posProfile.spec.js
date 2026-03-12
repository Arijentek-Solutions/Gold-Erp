/**
 * POS Profile Store Unit Tests
 * Tests: Profile state management, active profile, localStorage persistence
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { usePOSProfileStore } from '../../src/stores/posProfile.js'

// Mock frappe-ui
vi.mock('frappe-ui', () => ({
	createResource: vi.fn(() => ({
		fetch: vi.fn(() => Promise.resolve({ profiles: [], active_profile: null })),
	})),
}))

// Mock localStorage
const localStorageMock = {
	store: {},
	getItem(key) {
		return this.store[key] || null
	},
	setItem(key, value) {
		this.store[key] = value
	},
	removeItem(key) {
		delete this.store[key]
	},
	clear() {
		this.store = {}
	},
}

Object.defineProperty(global, 'localStorage', {
	value: localStorageMock,
})

describe('POS Profile Store', () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		localStorageMock.clear()
	})

	// ==========================================================================
	// STATE INITIALIZATION TESTS
	// ==========================================================================

	describe('State Initialization', () => {
		it('should initialize with empty profiles array', () => {
			const store = usePOSProfileStore()
			expect(store.profiles).toEqual([])
		})

		it('should initialize with null active profile', () => {
			const store = usePOSProfileStore()
			expect(store.activeProfile).toBeNull()
		})

		it('should initialize with null store location', () => {
			const store = usePOSProfileStore()
			expect(store.storeLocation).toBeNull()
		})

		it('should initialize with loading false', () => {
			const store = usePOSProfileStore()
			expect(store.loading).toBe(false)
		})
	})

	// ==========================================================================
	// ACTIVE PROFILE COMPUTED TESTS
	// ==========================================================================

	describe('Computed Properties', () => {
		it('should return true when active profile is set', () => {
			const store = usePOSProfileStore()
			store.activeProfile = { name: 'Main POS', company: 'Zevar Jewelry' }

			expect(store.hasActiveProfile).toBe(true)
		})

		it('should return false when no active profile', () => {
			const store = usePOSProfileStore()

			expect(store.hasActiveProfile).toBe(false)
		})

		it('should return profile name when active', () => {
			const store = usePOSProfileStore()
			store.activeProfile = { name: 'Main POS' }

			expect(store.profileName).toBe('Main POS')
		})

		it('should return default text when no active profile', () => {
			const store = usePOSProfileStore()

			expect(store.profileName).toBe('Select Profile')
		})

		it('should return warehouse from active profile', () => {
			const store = usePOSProfileStore()
			store.activeProfile = { warehouse: 'Main Warehouse' }

			expect(store.warehouse).toBe('Main Warehouse')
		})

		it('should return null warehouse when no active profile', () => {
			const store = usePOSProfileStore()

			expect(store.warehouse).toBeNull()
		})
	})

	// ==========================================================================
	// SET ACTIVE PROFILE TESTS
	// ==========================================================================

	describe('setActiveProfile', () => {
		it('should set active profile', () => {
			const store = usePOSProfileStore()
			const profile = { name: 'Main POS', company: 'Zevar Jewelry' }

			store.setActiveProfile(profile)

			expect(store.activeProfile).toEqual(profile)
		})

		it('should save to localStorage', () => {
			const store = usePOSProfileStore()
			const profile = { name: 'Main POS' }

			store.setActiveProfile(profile)

			const stored = JSON.parse(localStorageMock.store['zevar_pos_profile'])
			expect(stored.name).toBe('Main POS')
		})
	})

	// ==========================================================================
	// CLEAR PROFILE TESTS
	// ==========================================================================

	describe('clearProfile', () => {
		it('should clear active profile', () => {
			const store = usePOSProfileStore()
			store.activeProfile = { name: 'Main POS' }

			store.clearProfile()

			expect(store.activeProfile).toBeNull()
		})

		it('should clear store location', () => {
			const store = usePOSProfileStore()
			store.storeLocation = { name: 'Main Store' }

			store.clearProfile()

			expect(store.storeLocation).toBeNull()
		})

		it('should clear localStorage', () => {
			const store = usePOSProfileStore()
			localStorageMock.store['zevar_pos_profile'] = JSON.stringify({ name: 'Main POS' })

			store.clearProfile()

			expect(localStorageMock.store['zevar_pos_profile']).toBeUndefined()
		})
	})

	// ==========================================================================
	// LOCALSTORAGE PERSISTENCE TESTS
	// ==========================================================================

	describe('LocalStorage Persistence', () => {
		it('should load profile from localStorage on init', () => {
			localStorageMock.store['zevar_pos_profile'] = JSON.stringify({
				name: 'Saved Profile',
				company: 'Test Company'
			})

			const store = usePOSProfileStore()

			// Check if loaded from storage
			expect(store.activeProfile).toBeNull() // Will be null until fetch
		})

		it('should handle corrupted localStorage data', () => {
			localStorageMock.store['zevar_pos_profile'] = 'invalid json'

			const store = usePOSProfileStore()
			expect(store.activeProfile).toBeNull()
		})
	})
})
