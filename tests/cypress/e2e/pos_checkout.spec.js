/**
 * POS Checkout E2E Tests (Cypress)
 * Test Plan: Section 1.5 - Invoice Creation
 * 
 * Step-by-Step Test Plan:
 * 1. Add items to cart
 * 2. Select or create a customer
 * 3. Click "Checkout" button
 * 4. Verify checkout modal opens
 * 5. Select payment mode(s)
 * 6. Enter payment amount(s)
 * 7. Verify validation: payments must cover total
 * 8. Add multiple payment modes (split tender)
 * 9. Click "Complete Sale"
 * 10. Verify success message with invoice ID
 * 11. Verify cart is cleared after successful sale
 * 12. Check Frappe Desk for created Sales Invoice
 */

describe('POS Checkout - Invoice Creation', () => {
    beforeEach(() => {
        // Login before each test
        cy.login('Administrator', 'admin')
        cy.visit('/pos')
    })

    // ==========================================================================
    // TEST 1: BASIC CHECKOUT FLOW
    // ==========================================================================

    it('should complete a basic checkout with single item and cash payment', () => {
        // Step 1: Add items to cart
        cy.get('[data-testid="item-card"]').first().click()
        cy.get('[data-testid="add-to-cart-btn"]').click()

        // Verify item is in cart
        cy.get('[data-testid="cart-item-count"]').should('contain', '1')

        // Step 2: Select or create a customer
        cy.get('[data-testid="customer-selector"]').click()
        cy.get('[data-testid="customer-search"]').type('Walk-In')
        cy.get('[data-testid="customer-option"]').first().click()

        // Step 3: Click "Checkout" button
        cy.get('[data-testid="checkout-btn"]').click()

        // Step 4: Verify checkout modal opens
        cy.get('[data-testid="checkout-modal"]').should('be.visible')

        // Step 5: Select payment mode
        cy.get('[data-testid="payment-mode-select"]').select('Cash')

        // Step 6: Enter payment amount
        cy.get('[data-testid="payment-amount-input"]').should('have.value', '')

        // Step 9: Click "Complete Sale"
        cy.get('[data-testid="complete-sale-btn"]').click()

        // Step 10: Verify success message with invoice ID
        cy.get('[data-testid="success-message"]').should('be.visible')
        cy.get('[data-testid="invoice-id"]').should('contain', 'SI-')

        // Step 11: Verify cart is cleared after successful sale
        cy.get('[data-testid="cart-item-count"]').should('contain', '0')
    })

    // ==========================================================================
    // TEST 2: MULTIPLE ITEMS CHECKOUT
    // ==========================================================================

    it('should complete checkout with multiple items', () => {
        // Add first item
        cy.get('[data-testid="item-card"]').eq(0).click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        // Add second item
        cy.get('[data-testid="item-card"]').eq(1).click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        // Verify both items in cart
        cy.get('[data-testid="cart-item-count"]').should('contain', '2')

        // Select customer
        cy.get('[data-testid="customer-selector"]').click()
        cy.get('[data-testid="customer-search"]').type('Walk-In')
        cy.get('[data-testid="customer-option"]').first().click()

        // Checkout
        cy.get('[data-testid="checkout-btn"]').click()
        cy.get('[data-testid="checkout-modal"]').should('be.visible')

        // Select cash payment
        cy.get('[data-testid="payment-mode-select"]').select('Cash')
        cy.get('[data-testid="complete-sale-btn"]').click()

        // Verify success
        cy.get('[data-testid="success-message"]').should('be.visible')
    })

    // ==========================================================================
    // TEST 3: SPLIT TENDER (MULTIPLE PAYMENT MODES)
    // ==========================================================================

    it('should complete checkout with split tender (multiple payment modes)', () => {
        // Add item
        cy.get('[data-testid="item-card"]').first().click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        // Select customer
        cy.get('[data-testid="customer-selector"]').click()
        cy.get('[data-testid="customer-search"]').type('Walk-In')
        cy.get('[data-testid="customer-option"]').first().click()

        // Checkout
        cy.get('[data-testid="checkout-btn"]').click()
        cy.get('[data-testid="checkout-modal"]').should('be.visible')

        // Step 8: Add multiple payment modes (split tender)
        // First payment - Cash
        cy.get('[data-testid="payment-mode-select"]').select('Cash')
        cy.get('[data-testid="payment-amount-input"]').clear().type('100')

        // Add second payment mode
        cy.get('[data-testid="add-payment-btn"]').click()
        cy.get('[data-testid="payment-mode-select"]').eq(1).select('Credit Card')
        cy.get('[data-testid="payment-amount-input"]').eq(1).clear().type('200')

        // Complete sale
        cy.get('[data-testid="complete-sale-btn"]').click()

        // Verify success
        cy.get('[data-testid="success-message"]').should('be.visible')
    })

    // ==========================================================================
    // TEST 4: PAYMENT VALIDATION
    // ==========================================================================

    it('should validate that payments cover total amount', () => {
        // Add item
        cy.get('[data-testid="item-card"]').first().click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        // Select customer
        cy.get('[data-testid="customer-selector"]').click()
        cy.get('[data-testid="customer-search"]').type('Walk-In')
        cy.get('[data-testid="customer-option"]').first().click()

        // Checkout
        cy.get('[data-testid="checkout-btn"]').click()
        cy.get('[data-testid="checkout-modal"]').should('be.visible')

        // Get the total amount
        cy.get('[data-testid="grand-total"]').invoke('text').then((totalText) => {
            const total = parseFloat(totalText.replace(/[^0-9.]/g, ''))

            // Enter insufficient payment amount
            cy.get('[data-testid="payment-mode-select"]').select('Cash')
            cy.get('[data-testid="payment-amount-input"]').clear().type('10') // Less than total

            // Step 7: Verify validation: payments must cover total
            cy.get('[data-testid="complete-sale-btn"]').should('be.disabled')
            cy.get('[data-testid="payment-error"]').should('be.visible')
        })
    })

    // ==========================================================================
    // TEST 5: CUSTOMER SELECTION REQUIRED
    // ==========================================================================

    it('should require customer selection before checkout', () => {
        // Add item
        cy.get('[data-testid="item-card"]').first().click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        // Try to checkout without selecting customer
        cy.get('[data-testid="checkout-btn"]').click()

        // Should show customer selection prompt
        cy.get('[data-testid="customer-required-message"]').should('be.visible')
    })

    // ==========================================================================
    // TEST 6: TAX EXEMPT OPTION
    // ==========================================================================

    it('should allow tax exempt checkout', () => {
        // Add item
        cy.get('[data-testid="item-card"]').first().click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        // Select customer
        cy.get('[data-testid="customer-selector"]').click()
        cy.get('[data-testid="customer-search"]').type('Walk-In')
        cy.get('[data-testid="customer-option"]').first().click()

        // Checkout
        cy.get('[data-testid="checkout-btn"]').click()
        cy.get('[data-testid="checkout-modal"]').should('be.visible')

        // Get initial tax amount
        cy.get('[data-testid="tax-amount"]').invoke('text').as('initialTax')

        // Toggle tax exempt
        cy.get('[data-testid="tax-exempt-checkbox"]').check()

        // Verify tax is now zero
        cy.get('[data-testid="tax-amount"]').should('contain', '$0.00')

        // Complete sale
        cy.get('[data-testid="payment-mode-select"]').select('Cash')
        cy.get('[data-testid="complete-sale-btn"]').click()

        // Verify success
        cy.get('[data-testid="success-message"]').should('be.visible')
    })

    // ==========================================================================
    // TEST 7: DISCOUNT APPLICATION
    // ==========================================================================

    it('should apply discount and recalculate totals', () => {
        // Add item
        cy.get('[data-testid="item-card"]').first().click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        // Select customer
        cy.get('[data-testid="customer-selector"]').click()
        cy.get('[data-testid="customer-search"]').type('Walk-In')
        cy.get('[data-testid="customer-option"]').first().click()

        // Checkout
        cy.get('[data-testid="checkout-btn"]').click()
        cy.get('[data-testid="checkout-modal"]').should('be.visible')

        // Get initial grand total
        let initialTotal
        cy.get('[data-testid="grand-total"]').invoke('text').then((text) => {
            initialTotal = parseFloat(text.replace(/[^0-9.]/g, ''))
        })

        // Apply discount
        cy.get('[data-testid="discount-input"]').clear().type('50')

        // Verify grand total decreased
        cy.get('[data-testid="grand-total"]').invoke('text').then((text) => {
            const newTotal = parseFloat(text.replace(/[^0-9.]/g, ''))
            expect(newTotal).to.be.lessThan(initialTotal)
        })

        // Complete sale
        cy.get('[data-testid="payment-mode-select"]').select('Cash')
        cy.get('[data-testid="complete-sale-btn"]').click()

        // Verify success
        cy.get('[data-testid="success-message"]').should('be.visible')
    })

    // ==========================================================================
    // TEST 8: SALESPERSON ASSIGNMENT
    // ==========================================================================

    it('should assign salespersons with split percentages', () => {
        // Add item
        cy.get('[data-testid="item-card"]').first().click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        // Add salesperson
        cy.get('[data-testid="add-salesperson-btn"]').click()
        cy.get('[data-testid="salesperson-search"]').type('John')
        cy.get('[data-testid="salesperson-option"]').first().click()
        cy.get('[data-testid="salesperson-split"]').clear().type('100')

        // Select customer
        cy.get('[data-testid="customer-selector"]').click()
        cy.get('[data-testid="customer-search"]').type('Walk-In')
        cy.get('[data-testid="customer-option"]').first().click()

        // Checkout
        cy.get('[data-testid="checkout-btn"]').click()
        cy.get('[data-testid="checkout-modal"]').should('be.visible')

        // Complete sale
        cy.get('[data-testid="payment-mode-select"]').select('Cash')
        cy.get('[data-testid="complete-sale-btn"]').click()

        // Verify success
        cy.get('[data-testid="success-message"]').should('be.visible')
    })

    // ==========================================================================
    // TEST 9: SALESPERSON SPLIT VALIDATION
    // ==========================================================================

    it('should validate salesperson splits total 100%', () => {
        // Add item
        cy.get('[data-testid="item-card"]').first().click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        // Add first salesperson with 50%
        cy.get('[data-testid="add-salesperson-btn"]').click()
        cy.get('[data-testid="salesperson-search"]').type('John')
        cy.get('[data-testid="salesperson-option"]').first().click()
        cy.get('[data-testid="salesperson-split"]').clear().type('50')

        // Add second salesperson with 30% (total 80%, should fail)
        cy.get('[data-testid="add-salesperson-btn"]').click()
        cy.get('[data-testid="salesperson-search"]').eq(1).type('Jane')
        cy.get('[data-testid="salesperson-option"]').eq(1).click()
        cy.get('[data-testid="salesperson-split"]').eq(1).clear().type('30')

        // Select customer
        cy.get('[data-testid="customer-selector"]').click()
        cy.get('[data-testid="customer-search"]').type('Walk-In')
        cy.get('[data-testid="customer-option"]').first().click()

        // Checkout
        cy.get('[data-testid="checkout-btn"]').click()

        // Verify error message
        cy.get('[data-testid="salesperson-split-error"]').should('be.visible')
        cy.get('[data-testid="salesperson-split-error"]').should('contain', '100%')
    })

    // ==========================================================================
    // TEST 10: TRADE-IN PROCESSING
    // ==========================================================================

    it('should process trade-in and reduce grand total', () => {
        // Add item
        cy.get('[data-testid="item-card"]').first().click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        // Get initial grand total
        let initialTotal
        cy.get('[data-testid="grand-total"]').invoke('text').then((text) => {
            initialTotal = parseFloat(text.replace(/[^0-9.]/g, ''))
        })

        // Add trade-in
        cy.get('[data-testid="add-tradein-btn"]').click()
        cy.get('[data-testid="tradein-description"]').type('Old gold ring')
        cy.get('[data-testid="tradein-value"]').clear().type('100')

        // Verify grand total reduced
        cy.get('[data-testid="grand-total"]').invoke('text').then((text) => {
            const newTotal = parseFloat(text.replace(/[^0-9.]/g, ''))
            expect(newTotal).to.be.lessThan(initialTotal)
        })

        // Select customer
        cy.get('[data-testid="customer-selector"]').click()
        cy.get('[data-testid="customer-search"]').type('Walk-In')
        cy.get('[data-testid="customer-option"]').first().click()

        // Checkout
        cy.get('[data-testid="checkout-btn"]').click()
        cy.get('[data-testid="checkout-modal"]').should('be.visible')

        // Complete sale
        cy.get('[data-testid="payment-mode-select"]').select('Cash')
        cy.get('[data-testid="complete-sale-btn"]').click()

        // Verify success
        cy.get('[data-testid="success-message"]').should('be.visible')
    })

    // ==========================================================================
    // TEST 11: VERIFY SALES INVOICE IN DESK
    // ==========================================================================

    it('should create Sales Invoice in Frappe Desk', () => {
        // Add item and complete sale
        cy.get('[data-testid="item-card"]').first().click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        cy.get('[data-testid="customer-selector"]').click()
        cy.get('[data-testid="customer-search"]').type('Walk-In')
        cy.get('[data-testid="customer-option"]').first().click()

        cy.get('[data-testid="checkout-btn"]').click()
        cy.get('[data-testid="payment-mode-select"]').select('Cash')
        cy.get('[data-testid="complete-sale-btn"]').click()

        // Get invoice ID
        cy.get('[data-testid="invoice-id"]').invoke('text').then((invoiceId) => {
            // Step 12: Check Frappe Desk for created Sales Invoice
            cy.visit('/app/sales-invoice/' + invoiceId)
            cy.get('[data-fieldname="is_pos"]').should('have.attr', 'data-value', '1')
            cy.get('[data-fieldname="update_stock"]').should('have.attr', 'data-value', '1')
        })
    })

    // ==========================================================================
    // TEST 12: CART PERSISTENCE
    // ==========================================================================

    it('should persist cart across page refresh', () => {
        // Add item
        cy.get('[data-testid="item-card"]').first().click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        // Verify item in cart
        cy.get('[data-testid="cart-item-count"]').should('contain', '1')

        // Refresh page
        cy.reload()

        // Verify cart persists
        cy.get('[data-testid="cart-item-count"]').should('contain', '1')
    })

    // ==========================================================================
    // TEST 13: CANCEL CHECKOUT
    // ==========================================================================

    it('should allow cancelling checkout and return to cart', () => {
        // Add item
        cy.get('[data-testid="item-card"]').first().click()
        cy.get('[data-testid="add-to-cart-btn"]').click()
        cy.get('[data-testid="close-modal-btn"]').click()

        // Select customer
        cy.get('[data-testid="customer-selector"]').click()
        cy.get('[data-testid="customer-search"]').type('Walk-In')
        cy.get('[data-testid="customer-option"]').first().click()

        // Open checkout
        cy.get('[data-testid="checkout-btn"]').click()
        cy.get('[data-testid="checkout-modal"]').should('be.visible')

        // Cancel checkout
        cy.get('[data-testid="cancel-checkout-btn"]').click()

        // Verify modal is closed and cart still has items
        cy.get('[data-testid="checkout-modal"]').should('not.exist')
        cy.get('[data-testid="cart-item-count"]').should('contain', '1')
    })

    // ==========================================================================
    // TEST 14: EMPTY CART CHECKOUT
    // ==========================================================================

    it('should disable checkout when cart is empty', () => {
        // Verify checkout button is disabled with empty cart
        cy.get('[data-testid="checkout-btn"]').should('be.disabled')
    })

    // ==========================================================================
    // TEST 15: WAREHOUSE SELECTION
    // ==========================================================================

    it('should require warehouse selection before checkout', () => {
        // Clear warehouse if selected
        cy.get('body').then(($body) => {
            if ($body.find('[data-testid="clear-warehouse-btn"]').length > 0) {
                cy.get('[data-testid="clear-warehouse-btn"]').click()
            }
        })

        // Try to add item - should show warehouse prompt
        cy.get('[data-testid="warehouse-prompt"]').should('be.visible')
    })
})

// ==========================================================================
// CUSTOM COMMANDS
// ==========================================================================

Cypress.Commands.add('login', (username, password) => {
    cy.request({
        method: 'POST',
        url: '/api/method/login',
        body: {
            usr: username,
            pwd: password,
        },
    })
})
