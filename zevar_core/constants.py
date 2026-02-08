"""
Zevar Core Constants
"""

# Pagination
DEFAULT_PAGE_LENGTH = 20
MAX_PAGE_LENGTH = 100

# Item Sources
PARTNER_SOURCES = ['QGold', 'Stuller', 'Demo']

# Metal Types
METAL_TYPES = ['Yellow Gold', 'White Gold', 'Rose Gold', 'Silver', 'Platinum']

# Purity Values
PURITY_VALUES = {
    '24K': 0.999,
    '22K': 0.916,
    '18K': 0.750,
    '14K': 0.585,
    '10K': 0.417,
    '999 Sterling': 0.999,
    '925 Sterling': 0.925
}

# Unit Conversions
TROY_OZ_TO_GRAMS = 31.1035

# Tax Rates
DEFAULT_TAX_RATES = {
    'NY': 8.875,
    'Miami': 7.00,
    'LA': 9.50
}

# Payment Modes
PAYMENT_MODES = ['Cash', 'Credit Card', 'Debit Card', 'Check', 'Wire Transfer', 'Zelle']
