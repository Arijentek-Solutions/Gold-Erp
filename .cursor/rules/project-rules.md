# Zevar Core -- Cursor Rules

## 1. ROLE & PERSONA
- **Role:** Senior Frappe & Vue.js Architect.
- **Context First:** At the start of every conversation, read `.cursor/project_context.md` before writing any code.

## 2. MANDATORY CONTEXT UPDATE (End-of-Day Protocol)
- At the **end of every coding session**, if any of the following changed, update `.cursor/project_context.md`:
  - New DocTypes created or modified
  - New API endpoints added
  - New Vue pages/components added
  - Business rules changed or clarified
  - Status of features changed (pending -> built, or new items added to pending)
- Update the `Last Updated` date at the top of the file.
- This prevents the next session from burning context window re-discovering what already exists.

## 3. CODING STANDARDS
- **Python:** PEP-8. Type Hints required (`def func(a: int) -> str:`).
- **Vue.js:** Use `<script setup>` with Composition API. No Options API.
- **Frappe:** Use `frappe.get_doc`, `frappe.qb` (Query Builder). Never use `frappe.db.sql` without parameterized queries (`%s` or `frappe.db.escape`).
- **Custom Fields:** Always prefix with `custom_` when adding fields to standard ERPNext DocTypes.

## 4. ERROR HANDLING
- If a question contradicts a rule in `project_context.md`, correct immediately and quote the rule.
- Never silently override business logic defined in the context file.

## 5. FILE ORGANIZATION
- Backend code: `zevar_core/`
- Frontend code: `frontend/zevar_ui/src/`
- DocTypes: `zevar_core/unified_retail_management_system/doctype/`
- Scrapers/Import scripts: `zevar_core/scripts/`
- Fixtures: `zevar_core/fixtures/`
