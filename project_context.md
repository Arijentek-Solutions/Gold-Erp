# Project Context: Zevar Gold ERP

## 1. High-Level Objective
Build a Custom POS & ERP solution for **Zevar Jewelers** using **Frappe Framework (v16)** and **Vue.js**. 
**Goal:** Replace legacy JCS system, enable multi-store management, and implement specific jewelry business logic (Layaways, Gold Rates, Vendor Consignment).

## 2. Domain & Business Logic (Critical)
- **Gold Rate Logic:**
  - Rates fluctuate daily, but client changes *Sales Price* only if fluctuation is major (e.g., >$500/oz shift).
  - **Feature:** "Live Rate Fetcher" must prompt the Manager: *"Gold rate changed by X%. Update Inventory Prices? (Y/N)"*.
  - **Unit:** 1 Tula = 10 grams. Ounces used for raw purchase, Grams for retail.
- **Taxation:**
  - **Logic:** Tax is based on Store Location (County/State).
  - **Illinois:** ~10.5%.
  - **Requirement:** Dropdown in POS to select/override Tax Rate (0% for specific "Cash/No-Bill" transactions - strictly internal).
- **Inventory & SKU:**
  - **Conflict:** Same ring can come from Vendor A ($500) and Vendor B ($450).
  - **Solution:** Unified Product ID (Internal) + Vendor-Specific Batch/Serial.
  - **Tags:** Must print thermal tags with: Purity (14K), Weight, Diamond Carat (CTW), and Barcode.
- **Layaway (Leasing):**
  - Customer pays in installments (e.g., 6 months).
  - **Rule:** Price is locked at Day 1. Even if Gold Rate rises, customer pays the original agreed price.
  - **Notifications:** WhatsApp/SMS reminders for monthly payments.

## 3. Tech Stack & Standards
- **Backend:** Frappe Framework (Python). Use `frappe.get_doc` and `frappe.qb` (Query Builder) over raw SQL.
- **Frontend:** Vue.js 3 (Composition API). State management via Pinia.
- **Database:** MariaDB.
- **Hardware:** Integration required for Thermal Printers & Barcode Scanners (WebUSB or Frappe Hardware Bridge).

## 4. Data Migration (Legacy JCS)
- **Source:** Excel exports from JCS / Access Database.
- **Challenge:** Data is messy. Images are missing.
- **Strategy:** 1. Script to clean Vendor IDs.
  2. Map "Cases" (Showcase 1, 2) to Frappe "Warehouses".