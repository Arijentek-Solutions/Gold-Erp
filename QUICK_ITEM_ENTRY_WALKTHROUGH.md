# Quick Item Entry Walkthrough for Zevar ERP
**For Client Demo & Training**

---

## Overview: Old Way vs. New Way

### Legacy JCS System (Old Way - 5+ Steps)
1. Create new item record
2. Navigate to vendor section  
3. Add vendor details
4. Go to jewelry details section
5. Enter metal, purity, weight
6. Navigate to stock section
7. Create stock entry
8. **Total Time: 3-5 minutes per item**

### Zevar ERP (New Way - Single API Call)
- **One step creates everything**
- **Auto-generated vendor SKU**
- **Total Time: 30 seconds per item**

---

## 1. Finding Vendors in ERPNext v15

### Method 1: Search Bar
1. Click the search bar (top right, or press Ctrl+K / Cmd+K)
2. Type "Supplier"
3. Click "Supplier List"

### Method 2: Buying Module
1. Click on "Buying" module (left sidebar)
2. Under "Masters" section
3. Click "Supplier"

### Method 3: Direct URL
Navigate to: `http://localhost:8080/app/supplier`

### Current Demo Vendors
- **QGold** - Premium gold supplier
- **Stuller** - Major jewelry supplier  
- **Blue Nile** - Diamond supplier
- **Zevar In-House** - Store-made items

---

## 2. Adding a New Vendor

### Step-by-Step

1. **Open Supplier List**
   - Navigate to: Buying → Supplier
   - Click "+ Add Supplier" (blue button top right)

2. **Fill Required Fields**
   - **Supplier Name**: e.g., "Brilliant Gems"
   - **Supplier Group**: Select "All Supplier Groups" 
   - **Supplier Type**: Choose "Company"

3. **Optional Fields (Recommended)**
   - **Tax ID**: For tax-exempt purchases
   - **Primary Contact**: Phone/Email
   - **Address**: Business address
   - **Payment Terms**: Net 30, COD, etc.

4. **Save**
   - Click "Save" button
   - Vendor is now ready to use

---

## 3. Adding Items - Via ERPNext UI (Manual)

### Traditional Method (for single items)

1. **Navigate to Item**
   - Stock → Item → + Add Item

2. **Basic Details**
   - Item Code: Leave blank (auto-generated)
   - Item Name: "14K Yellow Gold Solitaire Ring"
   - Item Group: "Rings"
   - Stock UOM: "Nos"

3. **Jewelry Details** (scroll down)
   - Metal Type: "Yellow Gold"
   - Purity: "14K"
   - Gross Weight: 5.20 g
   - Stone Weight: 0.50 g  
   - Net Weight: Auto-calculated (4.70 g)

4. **Classification**
   - Product Type: "Jewelry"
   - Jewelry Type: "Rings"
   - Gender: "Women's"

5. **Vendor & Pricing**
   - Vendor: Select "QGold"
   - Vendor SKU: Leave blank (auto-generated)
   - MSRP: $2,495.00
   - Cost Price: $1,800.00
   - Country: "USA"

6. **Save Item**

7. **Add Stock** (separate step)
   - Stock → Stock Entry → + Add
   - Entry Type: "Material Receipt"
   - Target Warehouse: "Store 1 - New York - ZJ"
   - Add item, enter quantity
   - Submit

**Total Time: 3-5 minutes**

---

## 4. Adding Items - Via API (Recommended)

### Using Frappe Console

```bash
# Open terminal
cd /workspace/development/frappe-bench
bench --site zevar.localhost console
```

```python
# Import the quick add function
from zevar_core.api.item_entry import quick_add_item

# Add a new ring from QGold
result = quick_add_item(
    item_name="14K Yellow Gold Diamond Solitaire Ring",
    vendor="QGold",
    metal_type="Yellow Gold",
    purity="14K",
    jewelry_type="Rings",
    gross_weight=5.20,
    stone_weight=0.50,
    msrp=2495.00,
    cost_price=1800.00,
    gender="Women's",
    country_of_origin="USA",
    warehouse="Store 1 - New York - ZJ",
    qty=1,
    description="Classic solitaire engagement ring"
)

print(result)
# Output:
# {
#   'success': True,
#   'item_code': 'ZEV-RNG-0001',
#   'vendor_sku': 'QGO-RNG-00001',
#   'message': 'Item ZEV-RNG-0001 created successfully'
# }
```

**Total Time: 30 seconds**

---

## 5. Auto Vendor SKU Logic

### Format
`{VENDOR_PREFIX}-{TYPE_CODE}-{SEQUENCE}`

### Examples

| Vendor | Type | 1st Item | 2nd Item | 10th Item |
|--------|------|----------|----------|-----------|
| QGold | Rings | QGO-RNG-00001 | QGO-RNG-00002 | QGO-RNG-00010 |
| Stuller | Chains | STU-CHN-00001 | STU-CHN-00002 | STU-CHN-00010 |
| Blue Nile | Earrings | BLU-EAR-00001 | BLU-EAR-00002 | BLU-EAR-00010 |
| (No Vendor) | Bracelets | ZEV-BRA-00001 | ZEV-BRA-00002 | ZEV-BRA-00010 |

### Type Codes
- Rings = RNG
- Chains = CHN
- Necklaces = NKL
- Earrings = EAR
- Bracelets = BRA
- Pendants = PND
- Watches = WTC
- Other = OTH

### Preview Next SKU

```python
from zevar_core.api.item_entry import get_next_vendor_sku

# Check what SKU will be assigned next
next_sku = get_next_vendor_sku("QGold", "Rings")
print(next_sku)  # QGO-RNG-00015
```

---

## 6. Bulk Import (100+ Items)

### CSV Import Example

**CSV Format** (qgold_catalog.csv):
```csv
item_name,metal_type,purity,jewelry_type,gross_weight,stone_weight,msrp,cost_price,description
"14K Gold Diamond Ring",Yellow Gold,14K,Rings,5.2,0.5,2495,1800,"Solitaire ring"
"18K Gold Tennis Bracelet",White Gold,18K,Bracelets,15.5,2.1,4999,3500,"Classic tennis"
```

**Import Script**:
```python
import frappe
import csv
from zevar_core.api.item_entry import quick_add_item

with open('/path/to/qgold_catalog.csv', 'r') as f:
    reader = csv.DictReader(f)
    success = 0
    
    for row in reader:
        try:
            result = quick_add_item(
                item_name=row['item_name'],
                vendor="QGold",
                metal_type=row['metal_type'],
                purity=row['purity'],
                jewelry_type=row['jewelry_type'],
                gross_weight=float(row['gross_weight']),
                stone_weight=float(row['stone_weight']),
                msrp=float(row['msrp']),
                cost_price=float(row['cost_price']),
                warehouse="Store 1 - New York - ZJ",
                qty=1,
                description=row['description']
            )
            if result['success']:
                success += 1
                print(f"✓ {result['item_code']}: {result['vendor_sku']}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    frappe.db.commit()
    print(f"\nImported {success} items successfully!")
```

**Result: 100 items in under 2 minutes** (vs 5+ hours manually)

---

## 7. Client Demo Script (5-10 min)

### Demo Flow

**Part 1: Show the Problem (1 min)**
> "In the old JCS system, adding one item required 5-7 screens and took 3-5 minutes. For a 50-item shipment, that's 2-3 hours of tedious data entry."

**Part 2: Show Vendor Management (2 min)**
1. Navigate to Supplier list (`/app/supplier`)
2. Open "QGold" vendor
3. Show clean interface
4. Point out: "Once vendor is added, you never add it again"

**Part 3: Live Item Creation (2 min)**
1. Open Frappe console
2. Copy-paste the `quick_add_item` example
3. Hit Enter - show it completes in seconds
4. Navigate to the new item in UI
5. Show all fields populated, stock created

**Part 4: Show Auto SKU Magic (1 min)**
1. Run `get_next_vendor_sku("QGold", "Rings")`
2. Add another ring
3. Show SKU auto-incremented: `QGO-RNG-00002`

**Part 5: Bulk Import Preview (2 min)**
> "For vendor catalogs with 100+ items, we import from their CSV. No manual entry at all."

---

## 8. Troubleshooting

### Issue: "Warehouse not found"
**Error**: `Warehouse 'Store 1' does not exist`

**Solution**: Use the full warehouse name with company suffix
```python
Correct: "Store 1 - New York - ZJ"
Wrong: "Store 1" or "New York"
```

To see all warehouses:
```python
import frappe
wh = frappe.get_all('Warehouse', filters={'is_group': 0}, pluck='name')
print(wh)
```

### Issue: "Vendor not found"
**Solution**: Check exact vendor name (case-sensitive)
```python
vendors = frappe.get_all('Supplier', pluck='name')
print(vendors)
```

### Issue: Stock entry failed but item created
**Solution**: Item is saved successfully, just add stock manually later via Stock Entry

---

## 9. API Parameters Reference

### Required Parameters
- `item_name`: Display name (string)

### Common Parameters
- `vendor`: Supplier name (string, optional)
- `vendor_sku`: Custom SKU (optional, auto-generated if blank)
- `metal_type`: Yellow Gold, White Gold, Rose Gold, Silver, Platinum
- `purity`: 10K, 14K, 18K, 22K, 24K, 925 Sterling, 950
- `jewelry_type`: Rings, Chains, Earrings, Bracelets, Pendants, Watches, Other
- `gross_weight`: Total weight in grams (float)
- `stone_weight`: Stone weight in grams (float)
- `msrp`: Retail price USD (float)
- `cost_price`: Wholesale cost USD (float)
- `warehouse`: Target warehouse for stock (string)
- `qty`: Initial quantity (int, default 1)

### Optional Parameters
- `gender`: Unisex (default), Men's, Women's
- `country_of_origin`: Default "USA"
- `image`: URL or file path
- `description`: Item description

---

## 10. Best Practices

### Data Entry
1. **Verify vendor exists first** - Search supplier list
2. **Use consistent naming** - "Yellow Gold" not "yellow gold"
3. **Weight in grams** - Industry standard, most precise
4. **Always enter both MSRP and Cost** - For margin tracking
5. **Add descriptions** - Helps sales team

### Quality Control
Run weekly to find data issues:
```python
# Items missing weights
items = frappe.get_all('Item', 
    filters={'custom_gross_weight_g': 0, 'disabled': 0},
    limit=100,
    pluck='name'
)
print(f"Items needing weight data: {len(items)}")

# Items without vendor
no_vendor = frappe.get_all('Item',
    filters={'custom_vendor': ['is', 'not set'], 'disabled': 0},
    limit=100,
    pluck='name'
)
print(f"Items without vendor: {len(no_vendor)}")
```

---

## 11. Training Checklist

- [ ] Can access Supplier list in ERPNext
- [ ] Can create a new vendor
- [ ] Can manually create an item via UI
- [ ] Can run `quick_add_item` via console
- [ ] Understands auto vendor SKU logic
- [ ] Can preview next SKU
- [ ] Can import from CSV
- [ ] Knows how to troubleshoot common errors
- [ ] Can verify items in POS/Catalog

---

## Contact

**Technical Support**: Arijentek Solutions  
**Email**: akshay@arijentek.com  
**System**: Zevar ERP v16 (Frappe Framework)

**Document Version**: 1.0  
**Last Updated**: February 8, 2026
