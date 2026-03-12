# Zevar POS v1.0.0 - Release Notes

**Release Date:** March 2026
**Version:** 1.0.0
**Status:** Production Ready

---

## Overview

Zevar POS v1.0.0 is the first production release of the Zevar jewelry retail management system. This release provides a complete point-of-sale solution designed specifically for jewelry retailers.

---

## Major Features

### POS Terminal

- **Modern Vue 3 Interface** - Fast, responsive touch-friendly UI
- **Real-time Gold Pricing** - Automatic 15-minute gold rate refresh
- **Smart Product Search** - Search by name, code, or barcode
- **Dynamic Pricing** - Price calculated from gold value + gemstones + making charges
- **Split Payment Support** - Multiple payment methods per transaction
- **Multi-Salesperson Commissions** - Up to 4 salespersons per sale with split tracking

### Register Management

- **Session Opening** - Cash count with denomination breakdown
- **Session Closing** - Automatic reconciliation with variance detection
- **Cash Tracking** - All cash movements logged and audited

### Special Transactions

- **Quick Layaway** - One-click layaway creation with 3/6/9/12 month terms
- **Trade-In Processing** - 2x rule automatically applied
- **Gift Card Integration** - Issue, redeem, and track gift cards
- **Repair Orders** - Create and track jewelry repairs

### Returns & Voids

- **Full Return Processing** - Refund, store credit, or exchange
- **Partial Returns** - Return individual items from invoice
- **Manager Void Approval** - PIN-based authorization for voids

### Security & Compliance

- **Role-Based Access Control** - Fine-grained permissions
- **Manager Override System** - PIN-based approval for exceptions
- **Comprehensive Audit Logging** - All transactions logged
- **Discount Limits** - Automatic approval workflow

### Employee Portal

- **Clock In/Out** - GPS-enabled attendance tracking
- **Leave Management** - Request and track time off
- **Payroll Access** - View salary slips and history
- **Task Management** - Personal and assigned tasks

### Reporting

- **Sales by Salesperson** - Commission tracking
- **Hourly Sales Analysis** - Traffic pattern insights
- **Payment Method Summary** - Reconciliation support
- **Layaway Aging Report** - Overdue payment tracking
- **Trade-In Summary** - Volume and compliance tracking
- **Gold Rate History** - Price trend analysis
- **Low Stock Alert** - Inventory reorder notifications

### Print Formats

- **Thermal Receipt (80mm)** - Optimized for POS printers
- **Jewelry Tags** - Product labels with barcodes
- **Layaway Contracts** - Customer agreement documents

---

## API Endpoints

### POS Profile
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/pos_profile.get_pos_profiles` | GET | Get all profiles |
| `/pos_profile.get_active_profile` | GET | Get active profile |
| `/pos_profile.set_active_profile` | POST | Set active profile |

### POS Session
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/pos_session.open_pos_session` | POST | Open register |
| `/pos_session.close_pos_session` | POST | Close register |
| `/pos_session.get_session_status` | GET | Get session status |

### Sales History
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sales_history.get_sales_history` | GET | Get sales list |
| `/sales_history.get_sales_summary` | GET | Get summary stats |
| `/sales_history.get_transaction_details` | GET | Get invoice details |

### Quick Layaway
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/quick_layaway.get_layaway_preview` | POST | Preview payment schedule |
| `/quick_layaway.create_quick_layaway` | POST | Create layaway contract |

### Permissions
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/permissions.check_permission` | GET | Check user permission |
| `/permissions.get_user_permissions` | GET | Get all user permissions |

### Audit Log
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/audit_log.get_audit_logs` | GET | Get audit logs |
| `/audit_log.get_audit_summary` | GET | Get summary stats |

### Returns
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/returns.get_returnable_items` | GET | Get items eligible for return |
| `/returns.create_return_invoice` | POST | Process return |

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| F1 | Help |
| F2 | New Sale |
| F3 | Search Items |
| F4 | Add Customer |
| F5 | Refresh Catalog |
| F6 | Trade-In |
| F7 | Layaway |
| F8 | Returns |
| F9 | Sales History |
| F10 | Open/Close Register |
| Ctrl+S | Save Draft |
| Ctrl+P | Print Receipt |
| Esc | Cancel/Close |

---

## Technical Details

### System Requirements

| Component | Requirement |
|-----------|-------------|
| Frappe Framework | v14+ |
| ERPNext | v14+ |
| Python | 3.10+ |
| Node.js | 18+ |
| MariaDB | 10.6+ |
| Redis | 6.0+ |

### New DocTypes

- POS Profile
- POS Opening Entry
- POS Closing Entry
- POS Audit Log
- POS Manager Override
- Layaway Contract
- Layaway Payment
- Trade In Voucher
- Gift Card
- Gift Card Transaction

### Hooks Added

| Hook | Handler |
|------|---------|
| Item.validate | calculate_net_weight_g |
| Sales Invoice.validate | apply_store_tax |
| Sales Invoice.validate | validate_trade_in_2x_rule |
| Sales Invoice.on_submit | calculate_commissions |

### Scheduled Tasks

| Task | Schedule |
|------|----------|
| fetch_live_gold_rate | Every 15 minutes |
| send_layaway_reminders | Daily at 9 AM |
| generate_low_stock_alert | Daily at 8 AM |

---

## Bug Fixes

N/A - Initial release

---

## Known Issues

1. **RFID Integration** - Not implemented in v1.0.0 (planned for v1.1)
2. **Mobile App** - PWA not available (planned for v1.2)
3. **2FA** - Two-factor authentication not implemented (planned for v1.1)

---

## Upgrade Notes

This is the initial release. No upgrade path required.

---

## Documentation

- [User Guide](./POS_User_Guide.md)
- [Admin Guide](./POS_Admin_Guide.md)
- [Deployment Checklist](./Deployment_Checklist.md)
- [API Reference](./openapi.yaml)

---

## Contributors

- Zevar Core Team
- Frappe Framework Contributors
- ERPNext Contributors

---

## License

GNU General Public License v3.0

---

## Support

- **Email:** support@zevar.com
- **GitHub:** https://github.com/your-repo/zevar_core/issues
- **Documentation:** https://docs.zevar.com

---

*Thank you for using Zevar POS!*
