"""
Zevar Core Constants
"""

# Pagination
DEFAULT_PAGE_LENGTH = 20
MAX_PAGE_LENGTH = 100

# Item Sources
PARTNER_SOURCES = ["QGold", "Stuller", "Demo"]

# Metal Types
METAL_TYPES = ["Yellow Gold", "White Gold", "Rose Gold", "Silver", "Platinum"]

# Purity Values
PURITY_VALUES = {
	"24K": 0.999,
	"22K": 0.916,
	"18Kt": 0.750,
	"14Kt": 0.585,
	"10k": 0.417,
	"999 Sterling": 0.999,
	"925 Sterling": 0.925,
}

# Unit Conversions
TROY_OZ_TO_GRAMS = 31.1035

# Tax Rates (keys match warehouse name substrings, case-insensitive)
DEFAULT_TAX_RATES = {
	"new york": 8.875,
	"miami": 7.00,
	"los angeles": 9.50,
	"houston": 8.25,
	"chicago": 10.25,
}

# Payment Modes
PAYMENT_MODES = [
	"Cash",
	"Credit Card",
	"Debit Card",
	"Check",
	"Wire Transfer",
	"Zelle",
	"Gift Card",
	"Trade-In",
]
