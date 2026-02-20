/**
 * Offline Sync Composable
 *
 * Manages offline data and sync queue
 */
import { ref, computed } from 'vue'
import {
	saveCart,
	loadCart,
	savePendingTransaction,
	getPendingTransactions,
} from '@/utils/offlineDB'

export function useOfflineSync() {
	const isOnline = ref(navigator.onLine)
	const pendingCount = ref(0)
	const syncInProgress = ref(false)

	const handleOnline = () => {
		isOnline.value = true
		syncPendingTransactions()
	}

	const handleOffline = () => {
		isOnline.value = false
	}

	// Monitor online/offline status
	window.addEventListener('online', handleOnline)
	window.addEventListener('offline', handleOffline)

	// Cleanup function — caller should invoke on component unmount
	const cleanup = () => {
		window.removeEventListener('online', handleOnline)
		window.removeEventListener('offline', handleOffline)
	}

	/**
	 * Save cart to IndexedDB
	 */
	const persistCart = async (cartData) => {
		try {
			await saveCart(cartData)
			return true
		} catch (error) {
			console.error('[Offline] Failed to persist cart:', error)
			return false
		}
	}

	/**
	 * Load cart from IndexedDB
	 */
	const restoreCart = async () => {
		try {
			return await loadCart()
		} catch (error) {
			console.error('[Offline] Failed to restore cart:', error)
			return { items: [], customer: null }
		}
	}

	/**
	 * Queue transaction for offline sync
	 */
	const queueTransaction = async (transactionData) => {
		try {
			const id = await savePendingTransaction(transactionData)
			await updatePendingCount()
			return id
		} catch (error) {
			console.error('[Offline] Failed to queue transaction:', error)
			throw error
		}
	}

	/**
	 * Sync pending transactions
	 */
	const syncPendingTransactions = async () => {
		if (syncInProgress.value || !isOnline.value) return

		try {
			syncInProgress.value = true
			const pending = await getPendingTransactions()

			// TODO: Implement actual sync logic
			console.log('[Offline] Syncing', pending.length, 'transactions')

			await updatePendingCount()
		} catch (error) {
			console.error('[Offline] Sync failed:', error)
		} finally {
			syncInProgress.value = false
		}
	}

	/**
	 * Update pending transaction count
	 */
	const updatePendingCount = async () => {
		try {
			const pending = await getPendingTransactions()
			pendingCount.value = pending.length
		} catch (error) {
			console.error('[Offline] Failed to update pending count:', error)
		}
	}

	// Initialize
	updatePendingCount()

	return {
		isOnline: computed(() => isOnline.value),
		pendingCount: computed(() => pendingCount.value),
		syncInProgress: computed(() => syncInProgress.value),
		persistCart,
		restoreCart,
		queueTransaction,
		syncPendingTransactions,
		cleanup,
	}
}
