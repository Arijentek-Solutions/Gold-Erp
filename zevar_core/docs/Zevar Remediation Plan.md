# Zevar POS v1.0.0 - Remediation Plan

**Created:** March 11, 2026
**Status:** Action Required
**Estimated Total Effort:** ~85 hours

---

## Overview

This plan addresses all issues identified during the comprehensive codebase audit. Items are prioritized by severity and dependency order.

---

## Phase 0: Blockers (Must Complete First - 6 hours)

These items prevent ANY deployment and must be completed before other work.

### 0.1 Create POS Audit Log DocType (1 hour)

**Location:** `unified_retail_management_system/doctype/pos_audit_log/`

**Create files:**
- `pos_audit_log.json` - DocType definition
- `pos_audit_log.py` - Controller (minimal, hooks only)
- `__init__.py`

**Required Fields:**
```json
{
  "fieldname": "user",
  "fieldtype": "Link",
  "label": "User",
  "options": "User",
  "reqd": 1
},
{
  "fieldname": "event_type",
  "fieldtype": "Select",
  "label": "Event Type",
  "options": "invoice_created\ninvoice_submitted\ninvoice_cancelled\ninvoice_voided\ninvoice_returned\npayment_received\npayment_refunded\nsplit_payment_processed\ngift_card_used\ntrade_in_processed\ndiscount_applied\nlarge_discount_applied\ndiscount_override_approved\nsession_opened\nsession_closed\ncash_variance_detected\nlogin_success\nlogin_failed\nmanager_override_requested\nmanager_override_approved\nmanager_override_rejected\npermission_denied\nlayaway_created\nlayaway_payment\nlayaway_cancelled\nlayaway_completed\ncustomer_created\ncustomer_updated\nstock_adjusted\nlow_stock_alert",
  "reqd": 1
},
{
  "fieldname": "category",
  "fieldtype": "Select",
  "label": "Category",
  "options": "Sales\nPayment\nDiscount\nSession\nSecurity\nLayaway\nCustomer\nInventory"
},
{
  "fieldname": "severity",
  "fieldtype": "Select",
  "label": "Severity",
  "options": "Info\nWarning",
  "default": "Info"
},
{
  "fieldname": "details",
  "fieldtype": "Text",
  "label": "Details"
},
{
  "fieldname": "timestamp",
  "fieldtype": "Datetime",
  "label": "Timestamp",
  "reqd": 1
},
{
  "fieldname": "reference_document",
  "fieldtype": "Data",
  "label": "Reference Document"
},
{
  "fieldname": "reference_type",
  "fieldtype": "Data",
  "label": "Reference Type"
},
{
  "fieldname": "ip_address",
  "fieldtype": "Data",
  "label": "IP Address"
},
{
  "fieldname": "user_agent",
  "fieldtype": "Data",
  "label": "User Agent"
}
```

**Verification:**
```bash
bench --site <site> migrate
bench --site <site> console
>>> frappe.get_doc("DocType", "POS Audit Log")
```

---

### 0.2 Create POS Manager Override DocType (1 hour)

**Location:** `unified_retail_management_system/doctype/pos_manager_override/`

**Create files:**
- `pos_manager_override.json` - DocType definition
- `pos_manager_override.py` - Controller
- `__init__.py`

**Required Fields:**
```json
{
  "fieldname": "requested_by",
  "fieldtype": "Link",
  "label": "Requested By",
  "options": "User",
  "reqd": 1
},
{
  "fieldname": "action",
  "fieldtype": "Data",
  "label": "Action",
  "reqd": 1
},
{
  "fieldname": "reason",
  "fieldtype": "Text",
  "label": "Reason",
  "reqd": 1
},
{
  "fieldname": "status",
  "fieldtype": "Select",
  "label": "Status",
  "options": "Pending\nApproved\nRejected",
  "default": "Pending",
  "reqd": 1
},
{
  "fieldname": "request_time",
  "fieldtype": "Datetime",
  "label": "Request Time",
  "reqd": 1
},
{
  "fieldname": "approved_by",
  "fieldtype": "Link",
  "label": "Approved By",
  "options": "User"
},
{
  "fieldname": "approval_time",
  "fieldtype": "Datetime",
  "label": "Approval Time"
},
{
  "fieldname": "reference_document",
  "fieldtype": "Data",
  "label": "Reference Document"
},
{
  "fieldname": "reference_type",
  "fieldtype": "Data",
  "label": "Reference Type"
}
```

---

### 0.3 Fix Plain Text PIN Storage (2 hours)

**Location:** `api/permissions.py`

**Current Code (Vulnerable):**
```python
# Line 224-233
manager = frappe.db.get_value(
    "User",
    {"pos_manager_pin": pin, ...},
    ...
)
```

**Required Changes:**

1. Create custom field for hashed PIN in User DocType (via fixtures or migration)
2. Update `verify_manager_pin()` function:

```python
import bcrypt

@frappe.whitelist()
def verify_manager_pin(pin: str) -> dict | None:
    """Verify manager PIN using bcrypt."""
    if not pin or len(pin) < 4:
        return None

    # Get all managers with PINs set
    managers = frappe.get_all(
        "User",
        filters={
            "enabled": 1,
            "user_type": "System User",
        },
        fields=["name", "full_name", "email", "pos_manager_pin_hash"]
    )

    for manager in managers:
        if manager.pos_manager_pin_hash:
            try:
                if bcrypt.checkpw(pin.encode(), manager.pos_manager_pin_hash.encode()):
                    user_roles = frappe.get_roles(manager.name)
                    if "Sales Manager" in user_roles or "System Manager" in user_roles:
                        return {
                            "user": manager.name,
                            "full_name": manager.full_name,
                            "email": manager.email
                        }
            except:
                continue

    return None
```

3. Create migration script to hash existing PINs
4. Update PIN setting UI to hash before save

---

### 0.4 Fix Test Imports (15 minutes)

**Files to update:**
- `tests/test_pos_apis.py`
- `tests/test_integration.py`

**Changes:**
```python
# BEFORE (broken):
from zevar_core.api.quick_layaway import get_layaway_preview
from zevar_core.api.quick_layaway import create_quick_layaway

# AFTER (fixed):
from zevar_core.api.layaway import get_layaway_preview
from zevar_core.api.layaway import create_quick_layaway
```

**Verification:**
```bash
bench --site <site> run-tests --app zevar_core --doctype "POS Profile"
```

---

### 0.5 Fix File Naming Bug (5 minutes)

**Current:** `report/low_stock_alert/ow_stock_alert.py`
**Should be:** `report/low_stock_alert/low_stock_alert.py`

```bash
cd /workspace/development/frappe-bench/apps/zevar_core/zevar_core/unified_retail_management_system/report/low_stock_alert/
mv ow_stock_alert.py low_stock_alert.py
```

---

## Phase 1: Critical Fixes (4 hours)

### 1.1 Create Report JSON Files (2 hours)

For each of the 7 incomplete reports, create the JSON metadata file.

**Reports needing JSON:**
1. `sales_by_salesperson`
2. `hourly_sales`
3. `payment_method_summary`
4. `layaway_aging`
5. `trade_in_summary`
6. `gold_rate_history`
7. `low_stock_alert`

**Template for each `report_name.json`:**
```json
{
 "add_total_row": 1,
 "columns": [],
 "creation": "2026-03-11",
 "disabled": 0,
 "docstatus": 0,
 "doctype": "Report",
 "idx": 0,
 "is_standard": "No",
 "modified": "2026-03-11",
 "modified_by": "Administrator",
 "module": "Unified Retail Management System",
 "name": "Report Name",
 "owner": "Administrator",
 "ref_doctype": "Sales Invoice",
 "report_name": "Report Name",
 "report_type": "Script Report",
 "roles": [
  {
   "role": "Sales Manager"
  },
  {
   "role": "System Manager"
  }
 ]
}
```

---

### 1.2 Create Report JS Files (2 hours)

**Template for each `report_name.js`:**
```javascript
// Filters for the report
frappe.query_reports["Report Name"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company"),
            "reqd": 1
        }
    ]
};
```

---

## Phase 2: Security Hardening (8 hours)

### 2.1 Add Rate Limiting to Sensitive APIs (4 hours)

**Files to update (17 files):**

Add `@rate_limit(limit=100, seconds=60)` decorator to sensitive endpoints:

| File | Priority Endpoints |
|------|-------------------|
| `commission.py` | `calculate_commission`, `get_commission_summary` |
| `customer.py` | `create_customer`, `update_customer` |
| `export.py` | All endpoints (already manager-only, but add rate limit) |
| `finance.py` | `create_account`, `record_payment` |
| `gift_card.py` | `redeem_gift_card`, `check_balance` |
| `helpdesk.py` | `create_ticket`, `update_ticket` |
| `item_entry.py` | `create_entry` |
| `payroll.py` | All endpoints |
| `repair.py` | `create_order`, `update_status` |
| `tasks.py` | `create_task`, `update_task` |
| `trending.py` | `update_trending` |

**Example:**
```python
from frappe.rate_limiter import rate_limit

@frappe.whitelist()
@rate_limit(limit=100, seconds=60)
def redeem_gift_card(...):
    ...
```

---

### 2.2 Add Role Checks to Unprotected APIs (4 hours)

**Files needing explicit `frappe.only_for()`:**

```python
# Add at the start of sensitive functions:

def calculate_commission(...):
    frappe.only_for(["Sales Manager", "System Manager"])
    ...

def export_sales_data(...):
    frappe.only_for(["Sales Manager", "System Manager"])
    ...
```

---

## Phase 3: Testing (Detailed Plan)

### Testing Strategy Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    TESTING PYRAMID                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                    ┌─────────┐                               │
│                    │   E2E   │  ← Phase 3.4 (Integration)   │
│                    └─────────┘                               │
│               ┌───────────────────┐                          │
│               │  API/Integration  │  ← Phase 3.3            │
│               └───────────────────┘                          │
│          ┌─────────────────────────────┐                     │
│          │       Unit Tests            │  ← Phase 3.1-3.2   │
│          └─────────────────────────────┘                     │
│     ┌───────────────────────────────────────┐                │
│     │         Fix Existing Tests            │  ← Phase 0.4   │
│     └───────────────────────────────────────┘                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### Phase 3.1: Fix and Verify Existing Tests (2 hours)

**Priority: IMMEDIATE (after Phase 0.4)**

#### 3.1.1 Fix Import Errors

**Files:**
- `tests/test_pos_apis.py`
- `tests/test_integration.py`

**Tasks:**
1. Update all `quick_layaway` imports to `layaway`
2. Verify test fixtures reference correct module
3. Run tests to confirm imports work

**Verification Command:**
```bash
bench --site <site> run-tests --app zevar_core --module zevar_core.tests.test_pos_apis
bench --site <site> run-tests --app zevar_core --module zevar_core.tests.test_integration
```

#### 3.1.2 Verify Test Data Setup

Check that test data creation in `setUp()` methods is complete:
- POS Profile test data
- POS Session test data
- Customer test data
- Item test data

---

### Phase 3.2: Unit Tests for Critical Modules (10 hours)

#### 3.2.1 Catalog API Tests (HIGH - 4 hours)

**File:** `tests/test_catalog.py` (NEW)

**Test Cases:**

| Test ID | Test Name | Description | Priority |
|---------|-----------|-------------|----------|
| CAT-001 | `test_get_pos_items_basic` | Basic item retrieval returns paginated list | HIGH |
| CAT-002 | `test_get_pos_items_with_search` | Search filter works correctly | HIGH |
| CAT-003 | `test_get_pos_items_with_category_filter` | Category filtering works | HIGH |
| CAT-004 | `test_get_pos_items_with_price_range` | Price range filter works | MEDIUM |
| CAT-005 | `test_get_pos_items_pagination` | Pagination returns correct page size | HIGH |
| CAT-006 | `test_get_pos_items_empty_result` | Empty results handled gracefully | MEDIUM |
| CAT-007 | `test_search_sanitization` | Malicious input is sanitized | HIGH |
| CAT-008 | `test_rate_limiting` | Rate limiting is enforced | HIGH |

**Example Test:**
```python
import frappe
from frappe.tests.utils import FrappeTestCase

class TestCatalogAPI(FrappeTestCase):
    def setUp(self):
        # Create test items
        self.test_items = []
        for i in range(5):
            item = frappe.get_doc({
                "doctype": "Item",
                "item_code": f"TEST-ITEM-{i}",
                "item_name": f"Test Item {i}",
                "item_group": "Products",
                "stock_uom": "Nos",
                "is_stock_item": 1
            })
            item.insert()
            self.test_items.append(item.name)

    def tearDown(self):
        for item in self.test_items:
            frappe.delete_doc("Item", item, force=1)

    def test_get_pos_items_basic(self):
        """Test basic item retrieval"""
        from zevar_core.api.catalog import get_pos_items

        result = get_pos_items(page=1, page_size=10)

        self.assertIn("items", result)
        self.assertIn("total", result)
        self.assertIsInstance(result["items"], list)

    def test_search_sanitization(self):
        """Test that malicious search input is sanitized"""
        from zevar_core.api.catalog import get_pos_items

        # Should not raise SQL error
        result = get_pos_items(search="'; DROP TABLE tabItem; --")
        self.assertIn("items", result)
```

---

#### 3.2.2 Layaway API Tests (HIGH - 4 hours)

**File:** `tests/test_layaway.py` (NEW)

**Test Cases:**

| Test ID | Test Name | Description | Priority |
|---------|-----------|-------------|----------|
| LAY-001 | `test_get_layaway_preview` | Preview calculation is correct | HIGH |
| LAY-002 | `test_create_layaway_basic` | Basic layaway creation works | HIGH |
| LAY-003 | `test_create_layaway_3_month_term` | 3-month term schedule generated | HIGH |
| LAY-004 | `test_create_layaway_6_month_term` | 6-month term schedule generated | HIGH |
| LAY-005 | `test_create_layaway_invalid_customer` | Invalid customer rejected | HIGH |
| LAY-006 | `test_create_layaway_below_minimum` | Amount below minimum rejected | MEDIUM |
| LAY-007 | `test_layaway_payment_application` | Payment applies correctly | HIGH |
| LAY-008 | `test_layaway_cancellation` | Cancellation works with refund | MEDIUM |
| LAY-009 | `test_layaway_completion` | Completion creates invoice | HIGH |

**Example Test:**
```python
class TestLayawayAPI(FrappeTestCase):
    def setUp(self):
        self.customer = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": "Test Layaway Customer",
            "customer_type": "Individual"
        }).insert()

        self.item = frappe.get_doc({
            "doctype": "Item",
            "item_code": "LAYAWAY-TEST-001",
            "item_name": "Test Jewelry Item",
            "item_group": "Products",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "standard_rate": 1000
        }).insert()

    def test_get_layaway_preview(self):
        """Test layaway payment preview"""
        from zevar_core.api.layaway import get_layaway_preview

        result = get_layaway_preview(
            total_amount=1200,
            term_months=3,
            down_payment=200
        )

        self.assertEqual(result["term_months"], 3)
        self.assertEqual(result["down_payment"], 200)
        self.assertEqual(result["remaining_amount"], 1000)
        self.assertEqual(len(result["payment_schedule"]), 3)

    def test_create_layaway_basic(self):
        """Test basic layaway creation"""
        from zevar_core.api.layaway import create_quick_layaway

        result = create_quick_layaway(
            customer=self.customer.name,
            items=[{"item_code": self.item.name, "qty": 1}],
            term_months=3,
            down_payment=200
        )

        self.assertTrue(result.get("success"))
        self.assertIn("contract_name", result)

        # Verify contract was created
        contract = frappe.get_doc("Layaway Contract", result["contract_name"])
        self.assertEqual(contract.customer, self.customer.name)
        self.assertEqual(contract.status, "Active")
```

---

#### 3.2.3 Commission API Tests (HIGH - 2 hours)

**File:** `tests/test_commission.py` (NEW)

**Test Cases:**

| Test ID | Test Name | Description | Priority |
|---------|-----------|-------------|----------|
| COM-001 | `test_calculate_flat_commission` | Flat rate commission calculation | HIGH |
| COM-002 | `test_calculate_margin_commission` | Margin-based calculation | HIGH |
| COM-003 | `test_calculate_discount_commission` | Discount-based calculation | HIGH |
| COM-004 | `test_split_commission_two_salespersons` | 2-way split works | HIGH |
| COM-005 | `test_split_commission_four_salespersons` | 4-way split works | MEDIUM |
| COM-006 | `test_commission_with_trade_in` | Trade-in affects commission | MEDIUM |
| COM-007 | `test_commission_summary` | Summary calculation correct | HIGH |

---

### Phase 3.3: API Integration Tests (4 hours)

**File:** `tests/test_api_integration.py` (NEW)

**Test Suites:**

#### 3.3.1 POS Session Workflow Tests

| Test ID | Test Name | Description |
|---------|-----------|-------------|
| INT-001 | `test_full_session_workflow` | Open → Sales → Close session |
| INT-002 | `test_session_with_cash_variance` | Variance detection and logging |
| INT-003 | `test_concurrent_sessions_blocked` | Cannot open two sessions same register |

#### 3.3.2 Sales Invoice Workflow Tests

| Test ID | Test Name | Description |
|---------|-----------|-------------|
| INT-010 | `test_complete_sale_cash` | Cash payment flow |
| INT-011 | `test_complete_sale_split_payment` | Split payment (cash + card) |
| INT-012 | `test_sale_with_gift_card` | Gift card as payment |
| INT-013 | `test_sale_with_trade_in` | Trade-in processing |
| INT-014 | `test_sale_with_discount_override` | Manager approval for discount |

#### 3.3.3 Return/Exchange Workflow Tests

| Test ID | Test Name | Description |
|---------|-----------|-------------|
| INT-020 | `test_return_partial` | Partial return of invoice |
| INT-021 | `test_return_full` | Full return with refund |
| INT-022 | `test_exchange_item` | Exchange for different item |
| INT-023 | `test_void_with_approval` | Void requires manager PIN |

#### 3.3.4 Security Workflow Tests

| Test ID | Test Name | Description |
|---------|-----------|-------------|
| INT-030 | `test_audit_log_created` | Events are logged |
| INT-031 | `test_manager_override_flow` | Full override workflow |
| INT-032 | `test_invalid_pin_rejected` | Wrong PIN rejected |
| INT-033 | `test_permission_denied_logged` | Permission failures logged |

---

### Phase 3.4: End-to-End Integration Tests (4 hours)

**File:** `tests/test_e2e.py` (NEW)

**Complete Workflow Tests:**

#### 3.4.1 Happy Path Scenarios

| Test ID | Scenario | Steps |
|---------|----------|-------|
| E2E-001 | Complete Sales Day | Open register → 5 sales → Close register → Verify totals |
| E2E-002 | Layaway Full Cycle | Create → 3 payments → Complete → Invoice generated |
| E2E-003 | Gift Card Flow | Create card → Redeem partial → Check balance → Redeem full |
| E2E-004 | Trade-In Flow | Create trade-in → Apply to sale → Verify 2x rule |

#### 3.4.2 Error Recovery Scenarios

| Test ID | Scenario | Steps |
|---------|----------|-------|
| E2E-010 | Payment Failure Recovery | Attempt payment → Fail → Retry → Success |
| E2E-011 | Session Crash Recovery | Simulate crash → Reopen → Verify state |
| E2E-012 | Concurrent User Conflict | Two users same item → Verify locking |

---

### Phase 3.5: Frontend Component Tests (4 hours)

**Location:** `frontend/zevar_ui/tests/`

#### 3.5.1 Store Tests (Pinia)

| File | Test Cases |
|------|------------|
| `cart.spec.js` | Add/remove items, quantity update, clear cart, totals calculation |
| `session.spec.js` | Login state, user info, logout |
| `posProfile.spec.js` | Profile selection, persistence, switching |

#### 3.5.2 Component Tests (Vue)

| Component | Test Cases |
|-----------|------------|
| `CheckoutModal.spec.js` | Payment method selection, split payment UI, validation |
| `POSProductModal.spec.js` | Product display, add to cart, quantity selection |
| `QuickLayawayModal.spec.js` | Term selection, preview calculation, submission |
| `FilterSidebar.spec.js` | Filter application, clear filters, URL sync |

---

### Phase 3.6: Performance Tests (2 hours)

**File:** `tests/locust/locustfile.py` (EXISTS - verify/update)

**Load Test Scenarios:**

| Scenario | Users | Duration | Target RPS |
|----------|-------|----------|------------|
| Normal Load | 10 | 5 min | 50 RPS |
| Peak Load | 50 | 5 min | 200 RPS |
| Stress Test | 100 | 5 min | 500 RPS |

**Endpoints to Test:**
- `GET /api/method/zevar_core.api.catalog.get_pos_items`
- `POST /api/method/zevar_core.api.pos.create_pos_invoice`
- `GET /api/method/zevar_core.api.sales_history.get_sales_history`

---

### Test Execution Order

```
┌──────────────────────────────────────────────────────────────┐
│                    EXECUTION ORDER                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Phase 0.4: Fix test imports (15 min)                    │
│     ↓                                                        │
│  2. Phase 3.1: Verify existing tests pass (2 hours)         │
│     ↓                                                        │
│  3. Phase 0.1-0.3: Create DocTypes + fix security (4 hours) │
│     ↓                                                        │
│  4. Phase 3.2: Unit tests for catalog, layaway, commission  │
│     (10 hours - can run in parallel)                        │
│     ↓                                                        │
│  5. Phase 3.3: API integration tests (4 hours)              │
│     ↓                                                        │
│  6. Phase 3.4: E2E integration tests (4 hours)              │
│     ↓                                                        │
│  7. Phase 3.5: Frontend component tests (4 hours)           │
│     ↓                                                        │
│  8. Phase 3.6: Performance tests (2 hours)                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

### Test Coverage Goals

| Module | Current | Target |
|--------|---------|--------|
| API Endpoints | ~30% | 80% |
| DocType Controllers | ~20% | 70% |
| Frontend Stores | ~60% | 90% |
| Frontend Components | ~40% | 75% |
| Integration Flows | 0% | 100% (critical paths) |

---

## Phase 4: Code Cleanup (2 hours)

### 4.1 Remove Debug Files

**Files to remove:**
- `api/debug_pos.py`
- `api/get_err.py`
- `api/get_full_err.py`
- `api/desk.py` (evaluate if needed)
- `api/setup_bank.py` (evaluate if needed)

```bash
cd /workspace/development/frappe-bench/apps/zevar_core/zevar_core/api
rm debug_pos.py get_err.py get_full_err.py
```

### 4.2 Add Missing __init__.py Files

Check all report directories have `__init__.py`:
```bash
find /workspace/development/frappe-bench/apps/zevar_core/zevar_core/unified_retail_management_system/report -type d -exec sh -c 'touch "$1/__init__.py"' _ {} \;
```

---

## Phase 5: Documentation Updates (2 hours)

### 5.1 Update API Documentation

Update `openapi.yaml` with:
- New DocType endpoints
- Corrected module names
- Rate limiting information

### 5.2 Update Deployment Checklist

Add P0 items to `Deployment_Checklist.md`:
- [ ] POS Audit Log DocType migrated
- [ ] POS Manager Override DocType migrated
- [ ] PIN hashing migration run
- [ ] All tests passing

---

## Verification Checklist

Before considering the project production-ready:

```markdown
## Pre-Deployment Checklist

### P0 Blockers
- [ ] POS Audit Log DocType created and migrated
- [ ] POS Manager Override DocType created and migrated
- [ ] PIN storage converted to bcrypt
- [ ] Test imports fixed
- [ ] File naming bug fixed

### P1 Critical
- [ ] All 7 report JSON files created
- [ ] All 7 report JS files created
- [ ] Reports visible in Frappe Desk

### P2 Security
- [ ] Rate limiting added to 17 API files
- [ ] Role checks added to 17 API files
- [ ] Security tests passing

### P3 Testing
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Performance tests within thresholds

### P4 Cleanup
- [ ] Debug files removed
- [ ] Documentation updated
- [ ] Deployment checklist complete
```

---

## Timeline Summary

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 0: Blockers | 6 hours | None |
| Phase 1: Critical | 4 hours | Phase 0 |
| Phase 2: Security | 8 hours | Phase 0 |
| Phase 3: Testing | 26 hours | Phase 0, 1 |
| Phase 4: Cleanup | 2 hours | Phase 3 |
| Phase 5: Docs | 2 hours | All phases |
| **TOTAL** | **48 hours** | |

---

*Plan Created: March 11, 2026*
*Last Updated: March 11, 2026*
