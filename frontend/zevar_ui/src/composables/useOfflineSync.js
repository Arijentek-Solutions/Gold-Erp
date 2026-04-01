/**
 * Offline Sync Composable
 *
 * Manages offline data and sync queue with actual server reconciliation.
 */
import { ref, computed } from 'vue'
import {
	saveCart,
	loadCart,
	savePendingTransaction,
	getPendingTransactions,
	removePendingTransaction,
	markTransactionSynced,
	clearPendingTransactions,
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

	window.addEventListener('online', handleOnline)
	window.addEventListener('offline', handleOffline)

	const cleanup = () => {
		window.removeEventListener('online', handleOnline)
		window.removeEventListener('offline', handleOffline)
	}

	const persistCart = async (cartData) => {
		try {
			await saveCart(cartData)
			return true
		} catch (error) {
			return false
		}
	}

	const restoreCart = async () => {
		try {
			return await loadCart()
		} catch (error) {
			return { items: [], customer: null }
		}
	}

	const queueTransaction = async (transactionData) => {
		const id = await savePendingTransaction(transactionData)
		await updatePendingCount()
		return id
	}

	const syncPendingTransactions = async () => {
		if (syncInProgress.value || !isOnline.value) return

		try {
			syncInProgress.value = true
			const pending = await getPendingTransactions()

			for (const tx of pending) {
				if (tx.synced) continue
				try {
					const method = tx.method || 'zevar_core.api.pos.create_pos_invoice'
					const args = tx.args || tx
					await frappe.call(method, args)
					await markTransactionSynced(tx.id)
				} catch (error) {
					frappe.log_error(
						`[Offline Sync] Failed to sync transaction ${tx.id}: ${error.message}`
					)
				}
			}

			await updatePendingCount()
		} catch (error) {
			frappe.log_error(`[Offline Sync] Sync batch failed: ${error.message}`)
		} finally {
			syncInProgress.value = false
		}
	}

	const updatePendingCount = async () => {
		try {
			const pending = await getPendingTransactions()
			pendingCount.value = pending.filter((t) => !t.synced).length
		} catch (error) {
			pendingCount.value = 0
		}
	}

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
