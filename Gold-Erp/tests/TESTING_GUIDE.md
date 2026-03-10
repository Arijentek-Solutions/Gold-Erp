# ZEVAR POS Module - Testing Guide

This guide explains how to run all automated tests for the POS Module.

## Prerequisites

Ensure you have the following installed:
- Frappe Bench (`bench`)
- Node.js 18+
- Python 3.10+
- Docker (for containerized testing)

---

## 1. Backend Unit Tests (Frappe unittest)

### Location
```
frappe-bench/apps/zevar_core/zevar_core/tests/test_pos_invoice.py
```

### Run All POS Tests
```bash
# From frappe-bench directory
bench run-tests --app zevar_core --doctype TestPOSInvoiceCreation
```

### Run Specific Test Class
```bash
# Test POS Invoice Creation
bench run-tests --app zevar_core --test test_pos_invoice.TestPOSInvoiceCreation

# Test Tax Calculation
bench run-tests --app zevar_core --test test_pos_invoice.TestTaxCalculation

# Test Trade-In Deduction
bench run-tests --app zevar_core --test test_pos_invoice.TestTradeInDeduction
```

### Run Specific Test Method
```bash
bench run-tests --app zevar_core --test test_pos_invoice.TestPOSInvoiceCreation.test_create_pos_invoice_basic
```

### Run with Coverage
```bash
bench run-tests --app zevar_core --coverage
```

### Using Docker (Containerized)
```bash
# Enter the container
docker compose exec backend bash

# Run tests inside container
bench run-tests --app zevar_core --test test_pos_invoice
```

---

## 2. Frontend Unit Tests (Vitest)

### Location
```
frappe-bench/apps/zevar_core/frontend/zevar_ui/tests/
├── stores/cart.spec.js
├── components/POSProductModal.spec.js
└── setup.js
```

### Install Dependencies
```bash
cd frappe-bench/apps/zevar_core/frontend/zevar_ui
npm install
```

### Run All Tests
```bash
npm run test
```

### Run Tests with Watch Mode
```bash
npm run test:watch
```

### Run Tests with UI
```bash
npm run test:ui
```

### Run Tests with Coverage
```bash
npm run test:coverage
```

### Run Specific Test File
```bash
npx vitest run tests/stores/cart.spec.js
npx vitest run tests/components/POSProductModal.spec.js
```

### Run Tests Matching Pattern
```bash
npx vitest run -t "addItem"
npx vitest run -t "Modal Visibility"
```

### Package.json Scripts (add these)
```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage"
  }
}
```

---

## 3. E2E Tests (Cypress)

### Location
```
frappe-bench/apps/zevar_core/tests/cypress/e2e/pos_checkout.spec.js
```

### Install Cypress
```bash
cd frappe-bench/apps/zevar_core
npm install cypress --save-dev
```

### Configure Cypress
Create `cypress.config.js`:
```javascript
module.exports = {
  e2e: {
    baseUrl: 'http://localhost:8000',
    specPattern: 'tests/cypress/e2e/**/*.spec.js',
    supportFile: false,
    video: false,
    screenshotOnRunFailure: true,
  },
}
```

### Run Cypress Tests (Headless)
```bash
npx cypress run --spec "tests/cypress/e2e/pos_checkout.spec.js"
```

### Run Cypress Tests (Interactive)
```bash
npx cypress open
```

### Run Specific Test
```bash
npx cypress run --spec "tests/cypress/e2e/pos_checkout.spec.js" --grep "should complete a basic checkout"
```

### Run with Environment Variables
```bash
CYPRESS_baseUrl=http://localhost:8000 npx cypress run
```

### Docker Setup for Cypress
```bash
docker run -it -v $PWD:/e2e -w /e2e cypress/included:latest --browser chrome
```

---

## 4. Stress Tests (Locust)

### Location
```
frappe-bench/apps/zevar_core/tests/locust/locustfile.py
```

### Install Locust
```bash
pip install locust
```

### Run Locust (Web UI)
```bash
cd frappe-bench/apps/zevar_core/tests/locust
locust -f locustfile.py --host http://localhost:8000
```
Then open http://localhost:8089 in your browser.

### Run Locust (Headless - 50 Concurrent Users)
```bash
locust -f locustfile.py \
  --headless \
  --users 50 \
  --spawn-rate 5 \
  --run-time 5m \
  --host http://localhost:8000
```

### Run with CSV Report
```bash
locust -f locustfile.py \
  --headless \
  --users 50 \
  --spawn-rate 5 \
  --run-time 5m \
  --host http://localhost:8000 \
  --csv results \
  --html report.html
```

### Run Distributed (Master)
```bash
locust -f locustfile.py --master --users 50 --host http://localhost:8000
```

### Run Distributed (Worker)
```bash
locust -f locustfile.py --worker --master-host=<master-ip>
```

### Test Scenarios

| Scenario | Users | Spawn Rate | Duration |
|----------|-------|------------|----------|
| Light Load | 10 | 2/s | 3m |
| Normal Load | 50 | 5/s | 5m |
| Stress Test | 100 | 10/s | 10m |
| Spike Test | 200 | 20/s | 3m |

---

## 5. Run All Tests (Complete Suite)

### Create Test Runner Script
```bash
#!/bin/bash
# run_all_tests.sh

echo "=========================================="
echo "ZEVAR POS Module - Complete Test Suite"
echo "=========================================="

# 1. Backend Unit Tests
echo "\n[1/4] Running Backend Unit Tests..."
bench run-tests --app zevar_core --test test_pos_invoice

# 2. Frontend Unit Tests
echo "\n[2/4] Running Frontend Unit Tests..."
cd frappe-bench/apps/zevar_core/frontend/zevar_ui
npm run test

# 3. E2E Tests
echo "\n[3/4] Running E2E Tests..."
cd ../../..
npx cypress run --spec "tests/cypress/e2e/pos_checkout.spec.js"

# 4. Stress Tests (5 minute run)
echo "\n[4/4] Running Stress Tests..."
cd tests/locust
locust -f locustfile.py --headless --users 50 --spawn-rate 5 --run-time 5m --host http://localhost:8000

echo "\n=========================================="
echo "All tests completed!"
echo "=========================================="
```

### Make Executable
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

---

## 6. CI/CD Integration

### GitHub Actions Example
```yaml
name: POS Module Tests

on:
  push:
    paths:
      - 'apps/zevar_core/**'

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Backend Tests
        run: bench run-tests --app zevar_core --test test_pos_invoice

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: Run Vitest
        run: |
          cd apps/zevar_core/frontend/zevar_ui
          npm ci
          npm run test

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Cypress
        uses: cypress-io/github-action@v5
        with:
          spec: tests/cypress/e2e/pos_checkout.spec.js

  load-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Locust
        run: pip install locust
      - name: Run Load Tests
        run: |
          cd tests/locust
          locust -f locustfile.py --headless --users 50 --spawn-rate 5 --run-time 2m --host ${{ secrets.FRAPPE_HOST }}
```

---

## 7. Test Reports

### Backend Coverage Report
```bash
bench run-tests --app zevar_core --coverage
# Report generated in: coverage/index.html
```

### Frontend Coverage Report
```bash
npm run test:coverage
# Report generated in: coverage/index.html
```

### Cypress Report
```bash
npx cypress run --reporter json --reporter-options output=cypress-report.json
```

### Locust Report
```bash
locust -f locustfile.py --html report.html
```

---

## Quick Reference

| Test Type | Command | Location |
|-----------|---------|----------|
| Backend | `bench run-tests --app zevar_core --test test_pos_invoice` | `zevar_core/tests/` |
| Frontend | `npm run test` | `frontend/zevar_ui/tests/` |
| E2E | `npx cypress run` | `tests/cypress/` |
| Load | `locust -f locustfile.py` | `tests/locust/` |
