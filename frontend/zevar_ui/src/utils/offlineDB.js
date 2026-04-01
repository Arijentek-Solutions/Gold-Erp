/**
 * IndexedDB Utility for Offline POS
 */

const DB_NAME = 'zevar-pos-db'
const DB_VERSION = 1

const STORES = {
	CART: 'cart',
	PENDING_TRANSACTIONS: 'pending_transactions',
	CACHED_ITEMS: 'cached_items',
}

let dbInstance = null

export async function initDB() {
	if (dbInstance) return dbInstance

	return new Promise((resolve, reject) => {
		const request = indexedDB.open(DB_NAME, DB_VERSION)
		request.onerror = () => reject(request.error)
		request.onsuccess = () => {
			dbInstance = request.result
			resolve(dbInstance)
		}
		request.onupgradeneeded = (event) => {
			const db = event.target.result
			if (!db.objectStoreNames.contains(STORES.CART)) {
				db.createObjectStore(STORES.CART, { keyPath: 'id' })
			}
			if (!db.objectStoreNames.contains(STORES.PENDING_TRANSACTIONS)) {
				const txStore = db.createObjectStore(STORES.PENDING_TRANSACTIONS, {
					keyPath: 'id',
					autoIncrement: true,
				})
				txStore.createIndex('timestamp', 'timestamp', { unique: false })
				txStore.createIndex('synced', 'synced', { unique: false })
			}
			if (!db.objectStoreNames.contains(STORES.CACHED_ITEMS)) {
				const itemsStore = db.createObjectStore(STORES.CACHED_ITEMS, {
					keyPath: 'item_code',
				})
				itemsStore.createIndex('timestamp', 'timestamp', { unique: false })
			}
		}
	})
}

export async function saveCart(cartData) {
	const db = await initDB()
	return new Promise((resolve, reject) => {
		const transaction = db.transaction([STORES.CART], 'readwrite')
		const store = transaction.objectStore(STORES.CART)
		const request = store.put({
			id: 'current',
			items: cartData.items,
			customer: cartData.customer,
			timestamp: Date.now(),
		})
		request.onsuccess = () => resolve()
		request.onerror = () => reject(request.error)
	})
}

export async function loadCart() {
	const db = await initDB()
	return new Promise((resolve, reject) => {
		const transaction = db.transaction([STORES.CART], 'readonly')
		const store = transaction.objectStore(STORES.CART)
		const request = store.get('current')
		request.onsuccess = () => {
			const data = request.result
			resolve(
				data
					? { items: data.items || [], customer: data.customer || null }
					: { items: [], customer: null }
			)
		}
		request.onerror = () => reject(request.error)
	})
}

export async function savePendingTransaction(transactionData) {
	const db = await initDB()
	return new Promise((resolve, reject) => {
		const transaction = db.transaction([STORES.PENDING_TRANSACTIONS], 'readwrite')
		const store = transaction.objectStore(STORES.PENDING_TRANSACTIONS)
		const request = store.add({ ...transactionData, timestamp: Date.now(), synced: false })
		request.onsuccess = () => resolve(request.result)
		request.onerror = () => reject(request.error)
	})
}

export async function getPendingTransactions() {
	const db = await initDB()
	return new Promise((resolve, reject) => {
		const transaction = db.transaction([STORES.PENDING_TRANSACTIONS], 'readonly')
		const store = transaction.objectStore(STORES.PENDING_TRANSACTIONS)
		const request = store.getAll()
		request.onsuccess = () => resolve(request.result || [])
		request.onerror = () => reject(request.error)
	})
}

export async function removePendingTransaction(id) {
	const db = await initDB()
	return new Promise((resolve, reject) => {
		const transaction = db.transaction([STORES.PENDING_TRANSACTIONS], 'readwrite')
		const store = transaction.objectStore(STORES.PENDING_TRANSACTIONS)
		const request = store.delete(id)
		request.onsuccess = () => resolve()
		request.onerror = () => reject(request.error)
	})
}

export async function markTransactionSynced(id) {
	const db = await initDB()
	return new Promise((resolve, reject) => {
		const transaction = db.transaction([STORES.PENDING_TRANSACTIONS], 'readwrite')
		const store = transaction.objectStore(STORES.PENDING_TRANSACTIONS)
		const getReq = store.get(id)
		getReq.onsuccess = () => {
			const data = getReq.result
			if (data) {
				data.synced = true
				data.syncedAt = Date.now()
				const putReq = store.put(data)
				putReq.onsuccess = () => resolve()
				putReq.onerror = () => reject(putReq.error)
			} else {
				resolve()
			}
		}
		getReq.onerror = () => reject(getReq.error)
	})
}

export async function cacheItems(items) {
	const db = await initDB()
	return new Promise((resolve, reject) => {
		const transaction = db.transaction([STORES.CACHED_ITEMS], 'readwrite')
		const store = transaction.objectStore(STORES.CACHED_ITEMS)
		transaction.oncomplete = () => resolve()
		transaction.onerror = () => reject(transaction.error)
		for (const item of items) {
			store.put({ ...item, timestamp: Date.now() })
		}
	})
}

export async function getCachedItems() {
	const db = await initDB()
	return new Promise((resolve, reject) => {
		const transaction = db.transaction([STORES.CACHED_ITEMS], 'readonly')
		const store = transaction.objectStore(STORES.CACHED_ITEMS)
		const request = store.getAll()
		request.onsuccess = () => resolve(request.result || [])
		request.onerror = () => reject(request.error)
	})
}

export async function clearPendingTransactions() {
	const db = await initDB()
	return new Promise((resolve, reject) => {
		const transaction = db.transaction([STORES.PENDING_TRANSACTIONS], 'readwrite')
		const store = transaction.objectStore(STORES.PENDING_TRANSACTIONS)
		const request = store.clear()
		request.onsuccess = () => resolve()
		request.onerror = () => reject(request.error)
	})
}
