"""Scheduled tasks for Zevar Core"""

import frappe
import requests


def fetch_live_metal_rates():
    """
    Fetches live gold and silver rates from configured API.
    Falls back to goldprice.org if no API configured.
    Called by scheduler every 15 minutes.
    """
    try:
        # Get API config from Gold Settings (if exists)
        api_url = "https://data-asg.goldprice.org/dbXRates/USD"  # Default
        
        if frappe.db.exists("Gold Settings", "Gold Settings"):
            settings = frappe.get_single("Gold Settings")
            if settings.api_endpoint:
                api_url = settings.api_endpoint
        
        # Fetch live rates
        response = requests.get(
            api_url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        # Extract prices (USD per troy ounce)
        gold_price_per_oz = data["items"][0]["xauPrice"]
        silver_price_per_oz = data["items"][0]["xagPrice"]
        
        # Convert to per gram (1 troy oz = 31.1035 grams)
        gold_per_gram = gold_price_per_oz / 31.1035
        silver_per_gram = silver_price_per_oz / 31.1035
        
        # Gold purities
        gold_purities = {
            "24K": 0.999,
            "22K": 0.916,
            "18K": 0.750,
            "14K": 0.585,
            "10K": 0.417,
        }
        
        # Silver purities
        silver_purities = {
            "999 Fine": 0.999,
            "925 Sterling": 0.925,
        }
        
        # Update Gold rates
        for purity, multiplier in gold_purities.items():
            rate = round(gold_per_gram * multiplier, 2)
            _update_rate("Yellow Gold", purity, rate)
        
        # Update Silver rates
        for purity, multiplier in silver_purities.items():
            rate = round(silver_per_gram * multiplier, 2)
            _update_rate("Silver", purity, rate)
        
        frappe.db.commit()
        frappe.logger().info(
            f"Metal rates updated: Gold 24K=${gold_per_gram:.2f}/g, Silver 999=${silver_per_gram:.2f}/g"
        )
        
    except Exception as e:
        frappe.logger().error(f"Metal rate fetch failed: {str(e)}")


def _update_rate(metal, purity, rate):
    """Helper to update or create a rate entry."""
    existing = frappe.db.exists("Gold Rate Log", {
        "metal": metal,
        "purity": purity
    })
    
    if existing:
        frappe.db.set_value("Gold Rate Log", existing, "rate_per_gram", rate)
        frappe.db.set_value("Gold Rate Log", existing, "source", "goldprice.org")
    else:
        frappe.get_doc({
            "doctype": "Gold Rate Log",
            "metal": metal,
            "purity": purity,
            "rate_per_gram": rate,
            "source": "goldprice.org",
        }).insert(ignore_permissions=True)


# Keep the old function name for backward compatibility
def fetch_live_gold_rate():
    """Alias for backward compatibility."""
    fetch_live_metal_rates()