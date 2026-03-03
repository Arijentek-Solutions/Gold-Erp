/**
 * Cart Store Unit Tests (Vitest)
 * Tests: State mutations, adding items, updating totals, trade-in credit
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCartStore } from '../../src/stores/cart.js'

// Mock frappe-ui
vi.mock('frappe-ui', () => ({
    createResource: vi.fn(() => ({
        fetch: vi.fn(() => Promise.resolve({ tax_rate: 7.5, currency: 'USD' })),
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

describe('Cart Store', () => {
    beforeEach(() => {
        setActivePinia(createPinia())
        localStorageMock.clear()
    })

    // ==========================================================================
    // STATE INITIALIZATION TESTS
    // ==========================================================================

    describe('State Initialization', () => {
        it('should initialize with empty items array', () => {
            const cart = useCartStore()
            expect(cart.items).toEqual([])
        })

        it('should initialize with null customer', () => {
            const cart = useCartStore()
            expect(cart.customer).toBeNull()
        })

        it('should initialize with zero tax rate', () => {
            const cart = useCartStore()
            expect(cart.taxRate).toBe(0)
        })

        it('should initialize with empty salespersons array', () => {
            const cart = useCartStore()
            expect(cart.salespersons).toEqual([])
        })

        it('should initialize with empty trade-ins array', () => {
            const cart = useCartStore()
            expect(cart.tradeIns).toEqual([])
        })
    })

    // ==========================================================================
    // ADD ITEM TESTS
    // ==========================================================================

    describe('addItem', () => {
        it('should add a new item to the cart', () => {
            const cart = useCartStore()
            const item = {
                item_code: 'ITEM-001',
                item_name: 'Gold Ring',
                final_price: 500,
                image: '/assets/item.jpg',
            }

            cart.addItem(item)

            expect(cart.items).toHaveLength(1)
            expect(cart.items[0].item_code).toBe('ITEM-001')
            expect(cart.items[0].item_name).toBe('Gold Ring')
            expect(cart.items[0].amount).toBe(500)
            expect(cart.items[0].qty).toBe(1)
        })

        it('should increment quantity when adding existing item', () => {
            const cart = useCartStore()
            const item = {
                item_code: 'ITEM-001',
                item_name: 'Gold Ring',
                final_price: 500,
            }

            cart.addItem(item)
            cart.addItem(item)

            expect(cart.items).toHaveLength(1)
            expect(cart.items[0].qty).toBe(2)
        })

        it('should not add item without item_code', () => {
            const cart = useCartStore()
            const item = {
                item_name: 'Invalid Item',
                final_price: 500,
            }

            cart.addItem(item)

            expect(cart.items).toHaveLength(0)
        })

        it('should use price from different price fields', () => {
            const cart = useCartStore()

            // Test with final_price
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 })
            expect(cart.items[0].amount).toBe(100)

            // Test with price (when final_price is not available)
            cart.addItem({ item_code: 'ITEM-002', price: 200 })
            expect(cart.items[1].amount).toBe(200)

            // Test with amount (when final_price and price are not available)
            cart.addItem({ item_code: 'ITEM-003', amount: 300 })
            expect(cart.items[2].amount).toBe(300)
        })

        it('should extract metal and purity from item', () => {
            const cart = useCartStore()
            const item = {
                item_code: 'ITEM-001',
                custom_metal_type: 'Yellow Gold',
                custom_purity: '14K',
                final_price: 500,
            }

            cart.addItem(item)

            expect(cart.items[0].metal).toBe('Yellow Gold')
            expect(cart.items[0].purity).toBe('14K')
        })

        it('should save to localStorage after adding item', () => {
            const cart = useCartStore()
            const item = {
                item_code: 'ITEM-001',
                item_name: 'Gold Ring',
                final_price: 500,
            }

            cart.addItem(item)

            expect(localStorageMock.store['zevar_cart_items']).toBeDefined()
            const stored = JSON.parse(localStorageMock.store['zevar_cart_items'])
            expect(stored).toHaveLength(1)
        })
    })

    // ==========================================================================
    // REMOVE ITEM TESTS
    // ==========================================================================

    describe('removeItem', () => {
        it('should remove item at specified index', () => {
            const cart = useCartStore()
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 })
            cart.addItem({ item_code: 'ITEM-002', final_price: 200 })
            cart.addItem({ item_code: 'ITEM-003', final_price: 300 })

            cart.removeItem(1)

            expect(cart.items).toHaveLength(2)
            expect(cart.items[0].item_code).toBe('ITEM-001')
            expect(cart.items[1].item_code).toBe('ITEM-003')
        })

        it('should update localStorage after removal', () => {
            const cart = useCartStore()
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 })
            cart.addItem({ item_code: 'ITEM-002', final_price: 200 })

            cart.removeItem(0)

            const stored = JSON.parse(localStorageMock.store['zevar_cart_items'])
            expect(stored).toHaveLength(1)
            expect(stored[0].item_code).toBe('ITEM-002')
        })
    })

    // ==========================================================================
    // TOTALS CALCULATION TESTS
    // ==========================================================================

    describe('Computed Totals', () => {
        it('should calculate totalItems correctly', () => {
            const cart = useCartStore()
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 })
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 }) // qty = 2
            cart.addItem({ item_code: 'ITEM-002', final_price: 200 })

            expect(cart.totalItems).toBe(3) // 2 + 1
        })

        it('should calculate subtotal correctly', () => {
            const cart = useCartStore()
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 })
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 }) // qty = 2, total = 200
            cart.addItem({ item_code: 'ITEM-002', final_price: 200 }) // qty = 1, total = 200

            expect(cart.subtotal).toBe(400) // (100 * 2) + (200 * 1)
        })

        it('should calculate tax correctly', () => {
            const cart = useCartStore()
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 })
            cart.taxRate = 7.5

            expect(cart.tax).toBe(7.5) // 100 * 7.5%
        })

        it('should calculate grandTotal correctly', () => {
            const cart = useCartStore()
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 })
            cart.taxRate = 7.5 // tax = 7.5

            expect(cart.grandTotal).toBe(107.5) // 100 + 7.5
        })

        it('should calculate grandTotal with trade-in credit', () => {
            const cart = useCartStore()
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 })
            cart.taxRate = 7.5 // tax = 7.5
            cart.addTradeIn({ tradeInValue: 50 })

            expect(cart.grandTotal).toBe(57.5) // 100 + 7.5 - 50
        })

        it('should not return negative grandTotal', () => {
            const cart = useCartStore()
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 })
            cart.addTradeIn({ tradeInValue: 200 }) // trade-in exceeds total

            expect(cart.grandTotal).toBe(0)
        })
    })

    // ==========================================================================
    // CUSTOMER MANAGEMENT TESTS
    // ==========================================================================

    describe('Customer Management', () => {
        it('should set customer', () => {
            const cart = useCartStore()
            const customer = { name: 'CUST-001', customer_name: 'John Doe' }

            cart.setCustomer(customer)

            expect(cart.customer).toEqual(customer)
        })

        it('should clear customer', () => {
            const cart = useCartStore()
            cart.setCustomer({ name: 'CUST-001', customer_name: 'John Doe' })

            cart.clearCustomer()

            expect(cart.customer).toBeNull()
        })
    })

    // ==========================================================================
    // SALESPERSON MANAGEMENT TESTS
    // ==========================================================================

    describe('Salesperson Management', () => {
        it('should add salesperson with split', () => {
            const cart = useCartStore()

            cart.addSalesperson('EMP-001', 100)

            expect(cart.salespersons).toHaveLength(1)
            expect(cart.salespersons[0].employee).toBe('EMP-001')
            expect(cart.salespersons[0].split).toBe(100)
        })

        it('should not add more than 4 salespersons', () => {
            const cart = useCartStore()

            cart.addSalesperson('EMP-001', 25)
            cart.addSalesperson('EMP-002', 25)
            cart.addSalesperson('EMP-003', 25)
            cart.addSalesperson('EMP-004', 25)
            cart.addSalesperson('EMP-005', 25) // Should not be added

            expect(cart.salespersons).toHaveLength(4)
        })

        it('should remove salesperson at index', () => {
            const cart = useCartStore()
            cart.addSalesperson('EMP-001', 50)
            cart.addSalesperson('EMP-002', 50)

            cart.removeSalesperson(0)

            expect(cart.salespersons).toHaveLength(1)
            expect(cart.salespersons[0].employee).toBe('EMP-002')
        })

        it('should clear all salespersons', () => {
            const cart = useCartStore()
            cart.addSalesperson('EMP-001', 50)
            cart.addSalesperson('EMP-002', 50)

            cart.clearSalespersons()

            expect(cart.salespersons).toHaveLength(0)
        })
    })

    // ==========================================================================
    // TRADE-IN MANAGEMENT TESTS
    // ==========================================================================

    describe('Trade-In Management', () => {
        it('should add trade-in item', () => {
            const cart = useCartStore()

            cart.addTradeIn({
                description: 'Old gold ring',
                tradeInValue: 200,
                newItemValue: 500,
            })

            expect(cart.tradeIns).toHaveLength(1)
            expect(cart.tradeIns[0].description).toBe('Old gold ring')
            expect(cart.tradeIns[0].trade_in_value).toBe(200)
        })

        it('should calculate tradeInCredit correctly', () => {
            const cart = useCartStore()
            cart.addTradeIn({ tradeInValue: 100 })
            cart.addTradeIn({ tradeInValue: 200 })

            expect(cart.tradeInCredit).toBe(300)
        })

        it('should remove trade-in at index', () => {
            const cart = useCartStore()
            cart.addTradeIn({ tradeInValue: 100 })
            cart.addTradeIn({ tradeInValue: 200 })

            cart.removeTradeIn(0)

            expect(cart.tradeIns).toHaveLength(1)
            expect(cart.tradeInCredit).toBe(200)
        })

        it('should clear all trade-ins', () => {
            const cart = useCartStore()
            cart.addTradeIn({ tradeInValue: 100 })
            cart.addTradeIn({ tradeInValue: 200 })

            cart.clearTradeIns()

            expect(cart.tradeIns).toHaveLength(0)
            expect(cart.tradeInCredit).toBe(0)
        })
    })

    // ==========================================================================
    // CLEAR CART TESTS
    // ==========================================================================

    describe('clearCart', () => {
        it('should clear all cart data', () => {
            const cart = useCartStore()
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 })
            cart.setCustomer({ name: 'CUST-001' })
            cart.addSalesperson('EMP-001', 100)
            cart.addTradeIn({ tradeInValue: 50 })

            cart.clearCart()

            expect(cart.items).toHaveLength(0)
            expect(cart.customer).toBeNull()
            expect(cart.salespersons).toHaveLength(0)
            expect(cart.tradeIns).toHaveLength(0)
        })

        it('should clear localStorage', () => {
            const cart = useCartStore()
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 })

            cart.clearCart()

            expect(localStorageMock.store['zevar_cart_items']).toBe('[]')
        })
    })

    // ==========================================================================
    // LOCALSTORAGE PERSISTENCE TESTS
    // ==========================================================================

    describe('LocalStorage Persistence', () => {
        it('should persist items to localStorage', () => {
            const cart = useCartStore()
            cart.addItem({ item_code: 'ITEM-001', final_price: 100 })

            const stored = JSON.parse(localStorageMock.store['zevar_cart_items'])
            expect(stored).toHaveLength(1)
            expect(stored[0].item_code).toBe('ITEM-001')
        })

        it('should load items from localStorage on initialization', () => {
            // Pre-populate localStorage
            localStorageMock.store['zevar_cart_items'] = JSON.stringify([
                { item_code: 'ITEM-001', amount: 100, qty: 1 },
            ])

            const cart = useCartStore()
            expect(cart.items).toHaveLength(1)
            expect(cart.items[0].item_code).toBe('ITEM-001')
        })

        it('should handle corrupted localStorage data', () => {
            localStorageMock.store['zevar_cart_items'] = 'invalid json'

            const cart = useCartStore()
            expect(cart.items).toEqual([])
        })
    })
})
