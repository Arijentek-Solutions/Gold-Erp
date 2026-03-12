# Zevar POS System - Administrator Guide

**Version:** 1.0.0
**Last Updated:** March 2026

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [User Management](#user-management)
5. [POS Profiles](#pos-profiles)
6. [Store Locations](#store-locations)
7. [Tax Configuration](#tax-configuration)
8. [Gold Rate Management](#gold-rate-management)
9. [Security & Permissions](#security--permissions)
10. [Reports](#reports)
11. [Audit Logs](#audit-logs)
12. [Backup & Maintenance](#backup--maintenance)
13. [API Reference](#api-reference)
14. [Troubleshooting](#troubleshooting)

---

## System Overview

### Architecture

Zevar POS is built on Frappe Framework with the following components:

```
┌─────────────────────────────────────────────────────────────┐
│                    Zevar Core Application                    │
├─────────────────────────────────────────────────────────────┤
│  Frontend (Vue 3)          │  Backend (Python/Frappe)       │
│  ├── POS Terminal          │  ├── API Endpoints             │
│  ├── Employee Portal       │  ├── DocType Controllers       │
│  └── Shared Components     │  └── Scheduled Tasks           │
├─────────────────────────────────────────────────────────────┤
│                    Database (MariaDB)                        │
├─────────────────────────────────────────────────────────────┤
│                    Redis Cache                               │
└─────────────────────────────────────────────────────────────┘
```

### Key Modules

| Module | Purpose |
|--------|---------|
| POS | Point of Sale terminal and checkout |
| Inventory | Item management and stock tracking |
| Customer | Customer accounts and history |
| Employee | Staff management and commissions |
| Finance | Layaway, gift cards, trade-ins |
| Reports | Sales and analytics reports |

---

## Installation

### Prerequisites

- Frappe Framework v14+
- ERPNext v14+
- Python 3.10+
- Node.js 18+
- MariaDB 10.6+

### Install Steps

```bash
# 1. Get the app
bench get-app zevar_core https://github.com/your-repo/zevar_core.git

# 2. Install on site
bench --site your-site install-app zevar_core

# 3. Run migrations
bench --site your-site migrate

# 4. Build assets
bench build --app zevar_core

# 5. Restart services
bench restart
```

### Post-Installation

1. Create default POS Profile
2. Configure store locations
3. Set up user roles
4. Import item catalog
5. Configure gold rate source

---

## Configuration

### Required Settings

Navigate to **Zevar Core > Settings**

| Setting | Description |
|---------|-------------|
| Default Company | Primary company for transactions |
| Default Warehouse | Main inventory location |
| Currency | Store currency (e.g., USD) |
| Price List | Default selling price list |

### Gold Rate Configuration

1. Go to **Zevar Core > Gold Rate Settings**
2. Configure:
   - Gold rate source API
   - Refresh interval (default: 15 minutes)
   - Markup percentage
3. Enable auto-refresh

### Receipt Configuration

1. Go to **Zevar Core > Print Settings**
2. Configure:
   - Receipt width (default: 80mm)
   - Header text/logo
   - Footer text
   - Tax display format

---

## User Management

### Roles

| Role | Permissions |
|------|-------------|
| **Sales User** | Basic POS operations, create invoices |
| **Sales Manager** | All sales operations, void, returns, discounts |
| **System Manager** | Full system access, configuration |
| **POS User** | POS terminal access only |
| **Cashier** | Cash handling, opening/closing register |

### Creating POS Users

1. Go to **User > New**
2. Enter email and name
3. Assign roles:
   - Sales User (basic)
   - Sales Manager (if needs override)
4. Set user defaults:
   - Default POS Profile
   - Default Warehouse
5. **Set Manager PIN** (for managers)

### Manager PIN Setup

For managers who need override capability:

1. Open user record
2. Find **POS Manager PIN** field
3. Enter 4-6 digit PIN
4. Save

---

## POS Profiles

### Creating a Profile

1. Go to **Zevar Core > POS Profile > New**
2. Configure:

| Field | Description |
|-------|-------------|
| Profile Name | Display name |
| Company | Company for transactions |
| Warehouse | Default inventory location |
| Currency | Transaction currency |
| Price List | Selling price list |
| Tax Template | Default tax template |
| Payment Methods | Allowed payment types |

3. Save

### Profile Assignment

Users select their profile when logging into POS. The profile determines:
- Which warehouse items are pulled from
- Which tax rate is applied
- Which payment methods are available

---

## Store Locations

### Store Setup

1. Go to **Zevar Core > Store Location > New**
2. Enter:
   - Store name
   - Address
   - Default warehouse
   - County tax rate
   - Phone number

### Tax by Location

Each store can have different tax rates:
- Set county tax rate
- Link to POS profile
- Tax is automatically applied based on store

---

## Tax Configuration

### Tax Templates

1. Go to **Accounting > Sales Taxes and Charges Template**
2. Create template for each tax rate
3. Link to POS profiles

### Automatic Tax Application

The system applies tax based on:
1. Store location county
2. Customer tax exemption status
3. Item tax category

Tax is calculated on:
- Gold value
- Gemstone value
- Making charges
- Less: Trade-in credit

---

## Gold Rate Management

### Live Rate Sync

Gold rates are fetched automatically every 15 minutes.

**Configuration:**
```python
# In hooks.py
scheduler_events = {
    "all": [
        "zevar_core.tasks.fetch_live_gold_rate"
    ]
}
```

### Manual Rate Entry

1. Go to **Zevar Core > Gold Rate > New**
2. Enter:
   - Metal type (Gold, Silver, Platinum)
   - Purity (24K, 22K, 18K, 14K)
   - Rate per gram
   - Effective date/time

### Rate History

View historical rates:
- Go to **Reports > Gold Rate History**
- Filter by date range
- Export to CSV/Excel

---

## Security & Permissions

### Permission System

The system uses role-based access control (RBAC):

```python
POS_PERMISSIONS = {
    "pos_access": {"roles": ["Sales User", "Sales Manager", "System Manager"]},
    "create_invoice": {"roles": ["Sales User", "Sales Manager", "System Manager"]},
    "apply_discount": {"roles": ["Sales User", "Sales Manager"], "limit": 10},
    "void_invoice": {"roles": ["Sales Manager", "System Manager"]},
    "process_return": {"roles": ["Sales Manager", "System Manager"]},
}
```

### Manager Override

When users exceed permissions:

1. System prompts for manager PIN
2. Manager enters PIN
3. Action is logged
4. Override is granted

### Audit Events

All security events are logged:
- Login attempts (success/failure)
- Manager overrides
- Permission denials
- Discount approvals

---

## Reports

### Available Reports

| Report | Description |
|--------|-------------|
| Sales by Salesperson | Commission tracking |
| Hourly Sales | Traffic analysis |
| Payment Method Summary | Reconciliation |
| Layaway Aging | Overdue payments |
| Trade-In Summary | Trade volume |
| Gold Rate History | Price trends |
| Low Stock Alert | Inventory alerts |

### Accessing Reports

1. Go to **Zevar Core > Reports**
2. Select report
3. Set filters
4. Run report
5. Export (CSV/Excel/PDF)

### Scheduled Reports

Reports can be emailed automatically:

1. Go to **Report > Schedule**
2. Set frequency
3. Add recipients
4. Save

---

## Audit Logs

### Viewing Logs

1. Go to **Zevar Core > Audit Logs**
2. Filter by:
   - Date range
   - User
   - Category
   - Severity
3. View details

### Log Categories

| Category | Events |
|----------|--------|
| Sales | Invoice created, submitted, cancelled |
| Payment | Payment received, refunded |
| Discount | Discounts applied, overrides |
| Session | Register opened, closed, variance |
| Security | Login, permission denied, override |
| Layaway | Created, payment, cancelled |

### Exporting Logs

1. Open audit logs
2. Set date range
3. Click **Export**
4. Choose format (CSV/Excel)

---

## Backup & Maintenance

### Database Backup

**Automatic Backups:**
- Configured in Frappe settings
- Default: daily at 2 AM

**Manual Backup:**
```bash
bench --site your-site backup
```

### Clearing Cache

```bash
bench --site your-site clear-cache
```

### Rebuilding Indexes

```bash
bench --site your-site rebuild-search-index
```

### Log Rotation

System logs are rotated automatically. To manually clear:
```bash
bench --site your-site clear-activity-logs
```

---

## API Reference

### Authentication

All API calls require Frappe session authentication:
- Cookie-based session
- Or API Key/Secret

### Base URL

```
https://your-domain.com/api/method/zevar_core.api.{module}.{function}
```

### Key Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/pos_profile.get_pos_profiles` | GET | Get all profiles |
| `/pos_session.open_pos_session` | POST | Open register |
| `/pos_session.close_pos_session` | POST | Close register |
| `/sales_history.get_sales_history` | GET | Get sales |
| `/quick_layaway.create_quick_layaway` | POST | Create layaway |
| `/returns.create_return_invoice` | POST | Process return |
| `/audit_log.get_audit_logs` | GET | Get logs |

### Full API Documentation

See `openapi.yaml` for complete API specification.

---

## Troubleshooting

### Common Issues

#### Gold Rate Not Updating

1. Check scheduler is running:
   ```bash
   bench scheduler-status
   ```
2. Check API connectivity
3. Review error logs

#### POS Session Errors

1. Check user has correct role
2. Verify POS profile assignment
3. Clear cache

#### Print Format Issues

1. Check print format is set as default
2. Verify CSS for thermal printing
3. Test with browser print preview

#### Permission Denied

1. Verify user roles
2. Check permission hooks
3. Review audit logs for denials

### Debug Mode

Enable debug logging:
```python
# In site_config.json
{
    "developer_mode": 1
}
```

### Log Files

| Log | Location |
|-----|----------|
| Application | `logs/bench-start.log` |
| Scheduler | `logs/bench-schedule.log` |
| Errors | `logs/error.log` |

### Support

- **GitHub Issues:** https://github.com/your-repo/zevar_core/issues
- **Documentation:** `/docs`
- **Email:** support@zevar.com

---

## Upgrade Instructions

### Backup First

```bash
bench --site your-site backup
```

### Update App

```bash
cd apps/zevar_core
git pull origin main
bench --site your-site migrate
bench build --app zevar_core
bench restart
```

### Post-Upgrade

1. Clear cache
2. Test critical workflows
3. Verify reports
4. Check integrations

---

*© 2026 Zevar Core - Jewelry Retail Management System*
