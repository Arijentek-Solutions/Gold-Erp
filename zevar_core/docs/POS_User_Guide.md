# Zevar POS System - User Guide

**Version:** 1.0.0
**Last Updated:** March 2026

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Opening the Register](#opening-the-register)
3. [Processing Sales](#processing-sales)
4. [Payment Processing](#payment-processing)
5. [Trade-In Transactions](#trade-in-transactions)
6. [Layaway Contracts](#layaway-contracts)
7. [Returns & Exchanges](#returns--exchanges)
8. [Closing the Register](#closing-the-register)
9. [Keyboard Shortcuts](#keyboard-shortcuts)
10. [Troubleshooting](#troubleshooting)

---

## Getting Started

### System Login

1. Open your web browser and navigate to the POS URL
2. Enter your username and password
3. Click **Sign In**

### POS Profile Selection

When you first access the POS:

1. Click on the profile selector in the top header
2. Select your assigned POS profile from the dropdown
3. The system will load your store's settings, warehouse, and tax rates

**Note:** Your profile determines which warehouse items are sold from and which tax rate is applied.

---

## Opening the Register

### Starting a New Session

Before processing any sales, you must open the cash register:

1. Click **Open Register** on the main screen
2. Enter your **Opening Balance** (count your starting cash)
3. Optionally, enter a cash breakdown by denomination:
   - $100 bills
   - $50 bills
   - $20 bills
   - $10 bills
   - $5 bills
   - $1 bills
   - Coins
4. Add any opening notes (e.g., "Received float from manager")
5. Click **Start Session**

### What Happens Next

- A POS Opening Entry is created
- Your session becomes active
- You can now process sales

---

## Processing Sales

### Adding Items to Cart

**Method 1: Barcode Scanning**
1. Click on the search bar or press `F3`
2. Scan the item barcode
3. Item is automatically added to cart

**Method 2: Manual Search**
1. Click the search bar or press `F3`
2. Type item name, code, or description
3. Click on the item to add to cart

**Method 3: Catalog Browse**
1. Click **Catalog** in the sidebar
2. Filter by category, metal type, or price range
3. Click item to view details
4. Click **Add to Cart**

### Viewing Item Details

Click on any item in the catalog to see:
- Item name and code
- Metal type and purity
- Gross weight, stone weight, net weight
- Gold rate and gold value
- Gemstone details (if applicable)
- Final price with breakdown

### Modifying Cart

**Change Quantity:**
- Click the +/- buttons next to the item
- Or type the quantity directly

**Remove Item:**
- Click the trash icon next to the item

**Apply Discount:**
1. Click **Add Discount** in the cart
2. Enter discount percentage or amount
3. Discounts over 10% require manager approval

### Assigning Salespersons

1. Click **Salesperson** in the cart
2. Select primary salesperson
3. Optionally add up to 3 additional salespersons
4. Set the commission split percentage for each

---

## Payment Processing

### Single Payment

1. Click **Checkout** when cart is ready
2. Select payment method:
   - Cash
   - Credit Card
   - Debit Card
   - Gift Card
3. Enter the amount
4. Click **Complete Payment**

### Split Payment (Multiple Methods)

1. Click **Checkout**
2. Enter first payment amount and method
3. Click **Add Payment**
4. Enter second payment
5. Repeat until total is covered
6. Click **Complete Payment**

### Gift Card Payment

1. Select **Gift Card** as payment method
2. Enter or scan the gift card number
3. The system will apply the available balance
4. If insufficient, add another payment method for the remainder

### Trade-In Credit

See [Trade-In Transactions](#trade-in-transactions) for using trade-in value as payment.

---

## Trade-In Transactions

### Creating a Trade-In

1. Click **Trade-In** in the sidebar
2. Enter customer information
3. For each item being traded:
   - Select metal type and purity
   - Enter gross weight
   - Enter stone weight (if applicable)
   - System calculates net weight automatically
4. The system applies the **2x Rule**:
   - Trade-in credit = 2x the gold value
   - Can only be applied to new jewelry purchases
5. Click **Add to Cart** to apply credit

### Trade-In 2x Rule

The 2x rule maximizes customer value:
- Gold value is calculated at current rates
- Customer receives 2x the gold value as store credit
- Credit must be used on the same transaction

**Example:**
- Gold value: $200
- Trade-in credit: $400

---

## Layaway Contracts

### Creating a Layaway

1. Add items to cart
2. Select customer
3. Click **Layaway** button
4. Choose payment terms:
   - 3 months (default)
   - 6 months
   - 9 months
   - 12 months
5. Select down payment percentage (10%, 20%, or 30%)
6. Review the payment schedule
7. Process the down payment
8. Click **Create Contract**

### Payment Schedule

The system calculates:
- Down payment amount
- Balance due
- Monthly payment amount
- Due dates for each installment

### Customer Receives

- Printed layaway contract
- Payment schedule
- Account login to view status

---

## Returns & Exchanges

### Processing a Return

1. Click **Returns** in the sidebar
2. Enter the original invoice number
3. System displays returnable items
4. Select items to return and quantities
5. Choose return type:
   - **Refund** - Cash/card refund
   - **Store Credit** - Credit to customer account
   - **Exchange** - Swap for different item
6. Enter reason for return
7. Process the return

### Voiding an Invoice

Voiding completely cancels a transaction:

1. Find the invoice in Sales History
2. Click **Void**
3. Enter reason
4. Manager must enter PIN for approval
5. Invoice is cancelled

**Note:** Only invoices with no returns can be voided.

---

## Closing the Register

### End of Day Reconciliation

1. Click **Close Register**
2. Count all cash in drawer
3. Enter amounts by denomination
4. System shows:
   - Opening balance
   - Total sales
   - Expected balance
   - Actual balance (your count)
   - Variance (if any)
5. Add notes for any discrepancies
6. Click **Close Session**

### Variance Handling

- **Positive Variance:** Drawer has more cash than expected
- **Negative Variance:** Drawer has less cash than expected

All variances are logged and reported to management.

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `F1` | Help |
| `F2` | New Sale |
| `F3` | Search Items |
| `F4` | Add Customer |
| `F5` | Refresh Catalog |
| `F6` | Trade-In |
| `F7` | Layaway |
| `F8` | Returns |
| `F9` | Sales History |
| `F10` | Open/Close Register |
| `Ctrl+S` | Save Draft |
| `Ctrl+P` | Print Receipt |
| `Esc` | Cancel/Close Modal |

---

## Troubleshooting

### Item Not Found

1. Check spelling in search
2. Try scanning the barcode
3. Verify item is in your warehouse
4. Contact manager to add item

### Payment Declined

1. Verify card details
2. Try another payment method
3. Process as split payment
4. Contact manager for override

### Discount Requires Approval

Discounts over 10% need manager PIN:
1. Request manager to terminal
2. Manager enters PIN
3. Discount is applied

### Printer Not Working

1. Check printer is powered on
2. Verify paper is loaded
3. Check network connection
4. Try reprinting from Sales History

### Session Errors

If you see "No active session":
1. You may have been logged out
2. Log back in
3. Open a new register session

---

## Getting Help

- **In-App:** Press `F1` for contextual help
- **Manager:** Contact your store manager
- **Support:** support@zevar.com

---

## Tips for Success

1. **Always open your register** before processing sales
2. **Count cash carefully** at opening and closing
3. **Verify customer information** before layaways
4. **Get manager approval** for exceptions
5. **Document discrepancies** with notes
6. **Use keyboard shortcuts** to work faster

---

*© 2026 Zevar Core - Jewelry Retail Management System*
