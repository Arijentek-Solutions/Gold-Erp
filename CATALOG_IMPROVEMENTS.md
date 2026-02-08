# Catalog & POS - Implementation Summary

## ✅ COMPLETED (2026-02-08)

### 1. Price Display Logic ✓
- **API**: `stone_weight` field added to `get_pos_items()` response (line 181 in api.py)
- **Frontend**: ProductModal already displays:
  - Gross Weight
  - Stone Weight (in red)
  - Net Weight = Gross - Stone (calculated, in gold color)
- **Status**: Working correctly

### 2. Cart Sync Across Pages ✓
- **Architecture**: Both POS and Catalog use the same Pinia `useCartStore()`
- **Reactivity**: Pinia reactivity ensures cart updates reflect immediately
- **Cross-tab Sync**: localStorage events + custom 'cart-updated' event
- **Status**: Working - no refresh needed

## 🎯 CURRENT TASK: Catalog Page Redesign

### Problem
Current catalog shows "Partner Catalog" (external items) mixed with store inventory. Client wants:
1. **Primary Focus**: In-stock items from their own warehouse
2. **Secondary Section**: Partner catalog for special orders

### Solution Architecture

**Catalog Page Structure**:
```
1. Hero Section (stays as-is)
2. "Available In-Store" Section
   - Filter: stock_qty > 0 OR custom_source = 'JCSWIN'/'Manual'
   - Shows: Rings, Earrings, Chains, Bracelets, Pendants (in stock)
3. "Order from Partners" Section (collapsible/toggleable)
   - Filter: custom_source IN ('QGold', 'Stuller', 'Demo')
   - Badge: "Ships from Partner"
```

**API Enhancement Needed**:
- Add `in_stock_only` parameter to `get_pos_items()`
- Add `source_filter` parameter to filter by data source

## 📋 NEXT: Offline POS

### ERPNext Offline Capabilities (v16)
- Service Worker for asset caching
- IndexedDB for local data storage
- Sync queue for pending transactions
- Built-in offline mode hooks in Frappe

### Implementation Plan
1. Create service worker for Vue app
2. Use Frappe's offline mode APIs
3. Queue POS transactions when offline
4. Auto-sync when connection restored
