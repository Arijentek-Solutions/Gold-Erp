/**
 * Keyboard Shortcuts Composable
 *
 * Provides keyboard shortcuts for POS operations.
 */

import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const shortcuts = ref([])
const showHint = ref(false)
const hintText = ref('')

// Default POS shortcuts
const defaultShortcuts = [
	{ key: 'F1', label: 'Help', action: 'help', global: true },
	{ key: 'F2', label: 'Search Items', action: 'search', global: true },
	{ key: 'F3', label: 'New Sale', action: 'new-sale', global: true },
	{ key: 'F4', label: 'Cart', action: 'cart', global: true },
	{ key: 'F5', label: 'Refresh', action: 'refresh', global: true },
	{ key: 'F6', label: 'Customer', action: 'customer', global: true },
	{ key: 'F7', label: 'Discount', action: 'discount', global: true },
	{ key: 'F8', label: 'Hold', action: 'hold', global: true },
	{ key: 'F9', label: 'Void', action: 'void', global: true },
	{ key: 'F10', label: 'Settings', action: 'settings', global: true },
	{ key: 'Escape', label: 'Close', action: 'close', global: true },
	{ key: 's', label: 'Save', action: 'save', ctrl: true },
	{ key: 'p', label: 'Print', action: 'print', ctrl: true },
	{ key: 'n', label: 'New', action: 'new', ctrl: true },
]

export function useKeyboardShortcuts(customShortcuts = [], options = {}) {
	const router = useRouter()
	const enabled = ref(true)

	// Merge custom shortcuts with defaults
	const allShortcuts = [...defaultShortcuts, ...customShortcuts]

	// Handler map
	const handlers = {
		help: () => showShortcutList(),
		search: () => focusSearch(),
		'new-sale': () => router.push('/'),
		cart: () => toggleCart(),
		refresh: () => window.location.reload(),
		customer: () => focusCustomer(),
		discount: () => applyDiscount(),
		hold: () => holdOrder(),
		void: () => voidOrder(),
		settings: () => openSettings(),
		close: () => closeModal(),
		save: () => saveCurrent(),
		print: () => printCurrent(),
		new: () => createNew(),
	}

	function showShortcutList() {
		showHint.value = true
		hintText.value = 'Keyboard Shortcuts: F1=Help, F2=Search  F3=New Sale  F4=Cart  F5=Refresh'
		setTimeout(() => {
			showHint.value = false
		}, 3000)
	}

	function focusSearch() {
		const searchInput = document.querySelector('input[placeholder*="Search"]')
		if (searchInput) searchInput.focus()
	}

	function toggleCart() {
		// Emit event or call store action
		console.log('Toggle cart')
	}

	function focusCustomer() {
		const customerInput = document.querySelector('[data-customer_selector]')
		if (customerInput) customerInput.focus()
	}

	function applyDiscount() {
		// Open discount modal
		console.log('Apply discount')
	}

	function holdOrder() {
		// Hold current order
		console.log('Hold order')
	}

	function voidOrder() {
		// Void current order
		console.log('Void order')
	}

	function openSettings() {
		// Open settings modal
		console.log('Open settings')
	}

	function closeModal() {
		// Close any open modal
		const modal = document.querySelector('.modal-overlay, .modal-content')
		if (modal) modal.click()
	}

	function saveCurrent() {
		// Save current form
		console.log('Save')
	}

	function printCurrent() {
		// Print current document
		console.log('Print')
	}

	function createNew() {
		// Create new document
		console.log('Create new')
	}

	function handleKeyDown(event) {
		if (!enabled.value) return

		// Check for matching shortcut
		for (const shortcut of allShortcuts) {
			const keyMatch = event.key === shortcut.key
			const ctrlMatch = shortcut.ctrl ? event.ctrlKey || event.metaKey : true

			if (keyMatch && ctrlMatch) {
				event.preventDefault()
				const handler = handlers[shortcut.action]
				if (handler) {
					handler()
					// Show brief hint
					showHint.value = true
					hintText.value = shortcut.label
					setTimeout(() => {
						showHint.value = false
					}, 1000)
					break
				}
			}
		}
	}

	onMounted(() => {
		document.addEventListener('keydown', handleKeyDown)
	})

	onUnmounted(() => {
		document.removeEventListener('keydown', handleKeyDown)
	})

	return {
		shortcuts: allShortcuts,
		showHint,
		hintText,
		enabled,
		showShortcutList,
	}
}

export default useKeyboardShortcuts
