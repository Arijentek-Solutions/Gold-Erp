/**
 * Vitest Test Setup
 * Global setup for all tests
 */

import { vi } from 'vitest'

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
    writable: true,
    value: vi.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: vi.fn(),
        removeListener: vi.fn(),
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
    })),
})

// Mock ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn(),
}))

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
    observe: vi.fn(),
    unobserve: vi.fn(),
    disconnect: vi.fn(),
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
    get length() {
        return Object.keys(this.store).length
    },
    key(index) {
        return Object.keys(this.store)[index] || null
    },
}

Object.defineProperty(global, 'localStorage', {
    value: localStorageMock,
})

// Reset localStorage before each test
beforeEach(() => {
    localStorageMock.clear()
})
