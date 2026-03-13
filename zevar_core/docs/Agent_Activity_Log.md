# Agent Activity Log

This document tracks the tasks performed by the AI agent on the Zevar Unified Retail Management System project.

### Task 1: Project Onboarding
* **Prompt:** `cd frappe-bench/apps/zevar_core, understand the project and report when you are ready to work.`
* **Solution:** Analyzed the `zevar_core` app structure, configuration (`pyproject.toml`, `hooks.py`), and project status (`Zevar_Project_Completion_Report.md`). Identified P0 blockers (missing DocTypes, plain text PIN storage, broken test imports, file naming bug) and P1 report config tasks.

### Task 2: Stable Version Migration
* **Prompt:** `update v16 latest and all to stable no develop version is needed`
* **Solution:** Migrated all Frappe bench applications away from development branches to stable releases:
  * `frappe`, `erpnext`, `hrms` → `version-16`
  * `crm`, `helpdesk`, `gameplan` → `main`
  * `insights` → `version-3`
  * *(telephony remained on `develop` as no stable tags existed)*
  * Executed hard resets, database migrations, rebuilt frontend assets (`bench build`), and restarted the bench.

### Task 3: Backend Security Audit & Feature Hardening
* **Prompt:** `Role: Principal Backend Security Architect & Frappe/Python Expert... Task: Conduct a rigorous security audit, feature hardening, and best-practice refactoring on all custom Frappe backend code...`
* **Solution:** 
  * **API Security:** Removed `allow_guest=True` from POS catalog endpoints (`get_pos_items`, `get_catalog_filters`, `get_item_details`) in `api/catalog.py` to enforce authentication.
  * **SQL Injection Prevention:** Audited `frappe.db.sql()` calls across modules, verifying strict adherence to parameterized query structures.
  * **Transactional Resilience:** Injected `frappe.db.rollback()` within `try...except` blocks across core transactional APIs (`pos.py`, `layaway.py`, `attendance.py`, `returns.py`) to prevent partial data writes/corrupted ledgers on failure. Standardized error handling using `frappe.throw()`.
\n[2026-03-12 00:20] **Prompt:** Add setting to auto-update docs with date/time, crisp and short. **Fix:** Saved global memory instruction to enforce this format for all future interactions.
[2026-03-12 07:45] **Prompt:** Apply premium fonts globally, fix theme visibility, add sidebar collapse toggles, and refine attendance buttons. **Fix:** Standardized fonts (Inter/Cinzel) globally, moved sidebar collapse to header, renamed buttons to "Clock In/Out", and added "Break" button.
[2026-03-12 07:51] **Prompt:** Fix dark mode button toggle text/symbol. **Fix:** Made the theme toggle dynamic: shows "Light Mode" + Sun when in dark mode, and "Dark Mode" + Moon when in light mode.
- [2026-03-12 10:18] **Prompt:** Fix real-time auto-calculation and decimal precision in POS Checkout Modal (Split Tender) and Sales Associate Commission Split. **Fix:** Implemented auto-balancing `.toFixed(2)` logic for payment splits and salesperson splits in CheckoutModal.vue and cart.js, and updated Remaining label to display Change Due when overpaid.
- [2026-03-12 10:45] **Prompt:** Unify UI across POS/Employee Portal, fix Light/Dark mode contrast, implement Time Tracking & Auto-Attendance. **Fix:** Fixed clock face visibility in light mode (removed destructive display:none), restructured header [Hamburger→Logo], wired Break buttons to Frappe Employee Checkin API (IN/OUT), added _process_auto_attendance to generate Attendance records on clock-out, added dark: prefixes to Expense/Tasks/Portal headers.
- [2026-03-12 11:30] **Prompt:** Apply consistent UI (Expense Standard), fix sidebar placement, improve POS collapse view, and implement premium calendars. **Fix:** Created global premium UI classes (.premium-card, .premium-title, .premium-subtitle), moved sidebars to leftmost corner, fixed POS collapsed branding/toggle, and created/integrated StandardCalendar.vue across all portal views.
[2026-03-12 11:30] **Prompt:** Refining POS & Portal UI to Expense Standard. **Fix:** Replaced glass-card with premium-card, updated typography, restructured sidebar headers, and consolidated clock-in buttons across all apps.
[2026-03-12 11:55] **Prompt:** Fixed giant UI break and sidebar logo visibility. **Fix:** Restored missing Tailwind directives in index.css, hid logos in collapsed sidebars, and de-consolidated attendance buttons into separate persistent 'Clock In', 'Clock Out', and 'Break' controls.
[2026-03-13 09:43] **Prompt:** Fix product modal click, dark mode quick-add button, modal border-radius, sidebar collapse. **Fix:** Added @click + emit('open-details') on ItemCard, fixed dark:bg-primary → dark:bg-[#D4AF37], changed premium-card border-radius from 2rem to 0.75rem, replaced Material Symbols icon with inline SVGs, changed nav labels from hidden lg:block to v-show collapsed-aware.
