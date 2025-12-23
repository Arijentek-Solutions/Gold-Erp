import frappe


def calculate_net_weight_g(doc, method):
    """
    Run on Item Save.
    Calculates Net Weight = Gross Weight - Stone Weight.
    """
    # 1. Use the correct field names with _g
    gross = doc.custom_gross_weight_g or 0.0
    stone = doc.custom_stone_weight_g or 0.0

    # 2. Calculate
    doc.custom_net_weight_g = gross - stone
