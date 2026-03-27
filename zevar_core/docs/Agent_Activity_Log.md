# Agent Activity Log

[2026-03-27 00:00] **Prompt:** Frappe HR grouping broke, Desk save reverted to old state, and app shortcut creation failed after the folder fixes. **Fix:** Repaired the regression by restoring app-parent Desktop Layout references, removing unsafe app-parent cleanup logic, normalizing custom external app shortcuts without installed app bindings, and updating the Desk merge path so saved visibility/layout state is not overwritten by boot defaults. Added `zevar_core.patches.repair_desktop_layout_and_shortcuts` and wrote `plans/Frappe_Desktop_Contribution_Guide.md` for upstream contribution guidance.

[2026-03-27 00:00] **Prompt:** Fix the messy Desk edit-mode folder flow where context menus stack, "Add To Folder" only offers the wrong folder, and new folders stay as untitled/uneditable. **Fix:** Patched Desk edit-mode state cleanup in `frappe/desk/page/desktop/desktop.js`, reset stale menu/grid objects between rerenders, prompted for real folder names on creation, rebuilt live folder options for "Add To Folder", and registered `zevar_core.patches.cleanup_desktop_folder_state` in `patches.txt` to rename legacy `Untitled` folders and repair saved Desktop Layout references.

[2026-03-19 08:20] **Prompt:** Set up the FoxPro migration locally using the discovered backup path and note how it was done. **Fix:** Finished the local migration wiring for v16 Bench by adding `zevar_core.commands`, promoting `dbfread` into `pyproject.toml`, adding `scripts/setup_migration_local.sh`, auto-resolving backup paths in `migration/commands.py`, and verifying with `zevar-mapping-info` plus a `zevar-import-legacy --dry-run` run against `/workspace/development/Zevar_URMS/Zevar_HIPmall_RD/Zevar_HIPmall_RD`. See `docs/FoxPro_Migration_Local_Setup.md`.

[2026-03-18 12:25] **Prompt:** Fix Desktop Icon creation bugs in Frappe v16.11.0. **Fix:** Fixed 3 bugs: (1) `validate()` had invalid `module_name` ref, (2) `icon.app_name` → `icon.app`, (3) `workspace.js` callback checked non-existent `r.message.status` → `r.message`. Bugs 1-2 applied by user, Bug 3 fixed in `workspace.js`.

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
[2026-03-26 04:45] **Prompt:** Fix live gold rate panel in POS UI. **Fix:** Harmonized purity names ("18Kt" vs "18K") across DB and code, added missing "24K"/"22K" purities, and cleaned corrupted logs.
[2026-03-26 06:01] **Prompt:** Fix Live Gold Rate panel in POS UI showing NULL or blank. **Fix:** Unified naming conventions, implemented API fallback for 403 Forbidden, and added POS permissions for Gold Rate Log.
[2026-03-26 11:10] **Prompt:** Fix all Desktop Icon bugs in Frappe v16 core. **Fix:** 5 bugs fixed across 4 files: DuplicateEntryError guard in add_workspace_to_desktop(), JS callback property mismatch, expanded bg_color palette, optional chaining for missing icon variant, null-safe .startswith() in create_desktop_icons_from_workspace().
[2026-03-27 05:15] **Prompt:** Fix Duplicate Name: Workspace Employee Portal already exists error. **Fix:** Made save_layout() in desktop_layout.py idempotent. It now checks if a Workspace or Desktop Icon already exists before attempting to create it, preventing DuplicateEntryError when processing new_icons from the frontend.
