import { beforeEach, describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useUIStore } from '../../src/stores/ui.js'

describe('UI Store', () => {
	beforeEach(() => {
		setActivePinia(createPinia())
		document.documentElement.classList.remove('dark')
	})

	it('defaults the catalog to in-stock items only', () => {
		const store = useUIStore()

		expect(store.activeFilters).toEqual({ in_stock_only: true })
	})

	it('removes false filter values instead of storing them', () => {
		const store = useUIStore()

		store.setFilter('out_of_stock_only', true)
		store.setFilter('out_of_stock_only', false)

		expect(store.activeFilters.out_of_stock_only).toBeUndefined()
	})

	it('restores default filters and clears search on reset', () => {
		const store = useUIStore()

		store.searchQuery = 'ring'
		store.setFilter('in_stock_only', false)
		store.setFilter('custom_metal_type', 'Yellow Gold')

		store.resetFilters()

		expect(store.searchQuery).toBe('')
		expect(store.activeFilters).toEqual({ in_stock_only: true })
	})
})
