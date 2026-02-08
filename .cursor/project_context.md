# Project Context: Zevar Gold ERP

> **Last Updated:** 2026-02-08
> **App Name:** `zevar_core` (Unified Retail Management System)
> **Publisher:** Arijentek Solutions (`akshay@arijentek.com`)

---

## 1. Project Goal

Build a **Custom POS & ERP solution** for **Zevar Jewelers** (US-based, multi-store jewelry retailer) on **Frappe Framework v16 + Vue.js 3**.

**Objectives:**
- Replace the legacy **JCS (Jewelry Computer System / JCSWIN)** with ERPNext.
- Custom **Vue.js POS** (not ERPNext's built-in POS) with jewelry-specific workflows: weight-based pricing, gemstone details, live gold rates, tax-exempt toggle.
- **Catalogue Dashboard** (public-facing) for browsing trending/featured items.
- Multi-store inventory management with warehouse-level stock tracking.
- Future: Layaway/installment schemes, vendor consignment, WhatsApp/SMS notifications.

---

## 2. Domain Rules (Business Logic)

### 2.1 Gold Rate & Pricing

| Rule | Detail |
|---|---|
| **Rate Source** | Live API fetch from `goldprice.org` (default), configurable in `Gold Settings`. |
| **Fetch Frequency** | Every **15 minutes** via Frappe scheduler (`*/15 * * * *`). |
| **Unit Conversion** | API returns USD/troy oz. Converted: `price_per_gram = price_per_oz / 31.1035`. |
| **Purity Multipliers** | 24K = 0.999, 22K = 0.916, 18K = 0.750, 14K = 0.585, 10K = 0.417. Silver: 999 = 0.999, 925 = 0.925. |
| **Rose/White Gold** | Priced using **Yellow Gold** rate (same base metal). |
| **Manager Override** | Planned: prompt manager when rate shifts significantly ("Update Inventory Prices? Y/N"). Not yet implemented. |

### 2.2 Item Price Calculation (US Market)

```
Priority 1: MSRP (if set) -> final_price = MSRP
Priority 2: Calculated    -> final_price = gold_value + gemstone_value
Priority 3: Fallback      -> final_price = standard_rate
```

- **Gold Value** = `net_weight_g * rate_per_gram` (from `Gold Rate Log` matching metal + purity).
- **Gemstone Value** = SUM of `amount` from `Zevar Gemstone Detail` child table.
- **Making Charges** = **NOT used for US market** (fields exist but are hidden). Types: "Fixed Amount" or "Percentage of Gold Value".
- **Net Weight** = `gross_weight_g - stone_weight_g` (auto-calculated on Item save via `item_events.py`).

### 2.3 Taxation

| Rule | Detail |
|---|---|
| **Default Rate** | Location-based: NY = 8.875%, Miami = 7.00%, LA = 9.50%. |
| **Tax Exempt Toggle** | Available in POS. `exempt_from_sales_tax` custom field on Customer, Sales Invoice, Sales Order, and Quotation. |
| **Reseller Exemption** | Customers can be flagged tax-exempt at the Customer level. |

### 2.4 Inventory & SKU

- **Unified Product ID** (ERPNext Item Code) + **Vendor SKU** (`custom_vendor_sku`) per vendor.
- **Data Source** tracking: `custom_source` field (options: JCSWIN, Demo, Manual, QGold, Stuller).
- **Thermal Tag Printing** (planned): Purity, Weight, Diamond CTW, Barcode.

### 2.5 Layaway / Installment Schemes (PLANNED -- NOT YET BUILT)

| Rule | Detail |
|---|---|
| **Price Lock** | Price locked at Day 1. Gold rate changes do NOT affect layaway price. |
| **Duration** | Typically 6 months. |
| **Notifications** | WhatsApp/SMS reminders for monthly payments. |
| **DocType Needed** | `Customer Scheme` or `Layaway Plan` -- not yet created. |

### 2.6 POS Payment

- **Modes:** Cash, Credit Card, Debit Card, Check, Wire Transfer, Zelle.
- **Split Payments:** Enabled. Max 3 splits per transaction.
- **Discount:** Allowed (flat amount).
- **Invoice:** Currently returns payload acknowledgement (stub); full `POS Invoice` creation pending.

---

## 3. Technical Schema

### 3.1 Custom DocTypes (module: `Unified Retail Management System`)

| DocType | Type | Purpose | Key Fields |
|---|---|---|---|
| **Gold Settings** | Single | API config for live rate fetcher | `api_endpoint`, `api_key`, `auto_update`, `update_frequency`, `base_currency` |
| **Gold Rate Log** | Regular | Stores rate per metal+purity combo | `metal` (-> Zevar Metal), `purity` (-> Zevar Purity), `rate_per_gram`, `source`, `timestamp` |
| **Zevar Metal** | Regular (lookup) | Metal master list | Name-only (e.g., Yellow Gold, Silver, Platinum, Rose Gold, White Gold) |
| **Zevar Purity** | Regular (lookup) | Purity master list | `fine_metal_content` (Float). Names: 24K, 22K, 18K, 14K, 10K, 925 Sterling, etc. |
| **Zevar Gemstone Detail** | Child Table | Gemstone rows on Item | `gem_type`, `carat` (3dp), `count`, `cut`, `color`, `clarity`, `rate`, `amount` (read-only) |
| **Trending Item** | Regular | Curated trending products for catalogue | `item_name`, `category`, `partner`, `price`, `is_active`, `is_hot`, `product_url`, `image_url`, `view_count`, `last_clicked` |

### 3.2 Custom Fields on ERPNext `Item`

**Section: Jewelry Details**
- `custom_metal_type` (Link -> Zevar Metal)
- `custom_purity` (Link -> Zevar Purity)
- `custom_gross_weight_g` (Float, 3dp)
- `custom_stone_weight_g` (Float, 3dp, default 0)
- `custom_net_weight_g` (Float, 3dp -- auto-calculated)

**Section: Gemstone Details**
- `gemstones` / `custom_gemstones` (Table -> Zevar Gemstone Detail)

**Section: Product Classification**
- `custom_product_type` (Select: Jewelry / Watch / Accessory)
- `custom_jewelry_type` (Select: Rings / Chains / Necklaces / Earrings / Bracelets / Pendants / Watches / Other)
- `custom_jewelry_subtype` (Data -- e.g., Cuban, Tennis, Solitaire)

**Section: Dimensions**
- `custom_length_value` (Float), `custom_length_unit` (Select: in/mm/cm)
- `custom_width_value` (Float), `custom_width_unit` (Select: in/mm)
- `custom_thickness_value` (Float)
- `custom_size` (Data -- ring size, bracelet length, etc.)

**Section: Vendor & Sourcing**
- `custom_vendor_sku` (Data)
- `custom_vendor` (Link -> Supplier)
- `custom_country_of_origin` (Data)
- `custom_msrp` (Currency -- primary pricing field for US market)
- `custom_cost_price` (Currency)
- `custom_source` (Select: JCSWIN / Demo / Manual / QGold / Stuller)

**Section: Additional Details**
- `custom_gender` (Select: Unisex / Men's / Women's)
- `custom_sold_by_unit` (Select: Each / Pair / Set, default Each)
- `custom_is_featured` (Check)
- `custom_is_trending` (Check)

### 3.3 Custom Fields on ERPNext `Customer`
- `custom_spouse_name`, `custom_anniversary`, `custom_ring_size`, `custom_preferred_metal`, `custom_preferred_purity`, `exempt_from_sales_tax`.

### 3.4 Custom Fields on Transactions
- `exempt_from_sales_tax` (Check) on: **Quotation**, **Sales Order**, **Sales Invoice**, **Customer**.

### 3.5 Item Attributes (Fixtures)
- Metal Type, Purity, Stone Type, Size, Colour.

---

## 4. Data Migration (Legacy JCS -> ERPNext)

- **Source System:** JCSWIN (legacy Jewelry Computer System).
- **Strategy:** 1. Clean vendor IDs. 2. Map JCS "Cases" -> Warehouses. 3. Import via scripts.
- **Source Tracking:** `custom_source = "JCSWIN"`.
- **External Scraping:** QGold, Blue Nile catalogs scraped to JSON.

---

## 5. Current Status (as of 2026-02-08)

### BUILT (Working)

| Component | Status |
|---|---|
| **Gold Rate Fetcher** | Live. Runs every 15 min. Fetches gold + silver, writes to `Gold Rate Log`. |
| **Pricing API** | Done. `get_item_price()` -- MSRP-first, then calculated, then fallback. |
| **POS Items API** | Done. `get_pos_items()` -- filtering, search, pagination. Supports `warehouse` and `custom_vendor` filtering. |
| **Catalog Filters API** | Done. `get_catalog_filters()` -- dynamic filter options. |
| **Vue.js POS Frontend** | In progress. Pages: Home, POS, Catalogue, Login. |
| **Frontend Features** | **Cart Sync** (Cross-tab), **Catalog Source Toggle** (Store vs Partner), **Weight Breakdown** (Gross/Stone/Net). |
| **Pinia Stores** | `cart.js` (with sync), `gold.js`, `session.js`, `ui.js`. |
| **Trending Item DocType** | Done. Standalone trending curation. |

### PENDING / NOT YET BUILT

| Component | Priority | Notes |
|---|---|---|
| **POS Invoice Creation** | HIGH | `create_pos_invoice()` is a stub. Needs real `POS Invoice` doc creation. |
| **Layaway / Scheme System** | HIGH | No DocType yet. Needs `Layaway Plan` with price-lock. |
| **Offline POS** | HIGH | Needs Service Worker + IndexedDB caching to match ERPNext offline capability. |
| **Vendor Consignment** | MEDIUM | Tracking items owned by vendor. |
| **Thermal Tag Printing** | MEDIUM | Planned. |
| **Barcode Scanner** | MEDIUM | WebUSB or Frappe Hardware Bridge. |

---

## 6. Tech Stack
- **Backend:** Frappe Framework v16 (Python 3.11+)
- **Frontend:** Vue.js 3 (Composition API) + Pinia + TailwindCSS
- **Database:** MariaDB
- **Build:** Vite

## 7. Key File Map
- `zevar_core/api.py`: All whitelisted API endpoints.
- `zevar_core/item_events.py`: Net weight auto-calc.
- `frontend/zevar_ui/src/stores/cart.js`: Cart state + persistence.
- `frontend/zevar_ui/src/pages/CatalogueDashboard.vue`: Public catalog + Source toggle.
