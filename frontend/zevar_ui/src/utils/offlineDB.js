/**
 * IndexedDB Utility for Offline POS
 */

const DB_NAME = 'zevar-pos-db'
const DB_VERSION = 1

const STORES = {
  CART: 'cart',
  PENDING_TRANSACTIONS: 'pending_transactions',
  CACHED_ITEMS: 'cached_items'
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
          autoIncrement: true 
        })
        txStore.createIndex('timestamp', 'timestamp', { unique: false })
        txStore.createIndex('synced', 'synced', { unique: false })
      }
      if (!db.objectStoreNames.contains(STORES.CACHED_ITEMS)) {
        const itemsStore = db.createObjectStore(STORES.CACHED_ITEMS, { 
          keyPath: 'item_code' 
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
      timestamp: Date.now()
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
      resolve(data ? { items: data.items || [], customer: data.customer || null } : { items: [], customer: null })
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
