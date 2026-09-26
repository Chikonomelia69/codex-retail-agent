import json
import sqlite3
from datetime import datetime, date, timedelta
from typing import Dict, Any, Optional, Union
from langchain_core.tools import tool

from src.config import CURRENT_DATE, URGENT_DAYS_THRESHOLD, CATEGORY_WINDOWS, ORDERS_DB_PATH
from src.loaders import init_orders_db

@tool
def calculate_return_and_warranty_window(
    item_name: str,
    category: str,
    purchase_date_str: str,
    current_date_str: Optional[str] = None
) -> str:
    """
    Computes days remaining in the return or warranty window from the purchase date and the policy document.
    Calculation method:
      1. Return Deadline = purchase_date + policy_return_days
      2. Warranty Deadline = purchase_date + policy_warranty_days
      3. Days Remaining = (Deadline - current_date).days
    Flags anything with fewer than 7 days left as EXPIRING_SOON.
    
    Args:
        item_name: The name or description of the purchased product.
        category: The product category (e.g., 'Consumer Electronics & Gadgets', 'Apparel, Clothing & Footwear', 'Home & Kitchen Appliances', 'Final Sale & Clearance Items').
        purchase_date_str: Date of purchase in YYYY-MM-DD format.
        current_date_str: Optional reference date in YYYY-MM-DD format (defaults to system reference date).
    
    Returns:
        JSON string containing exact deadlines, days remaining, and urgency flags.
    """
    try:
        purchase_dt = datetime.strptime(purchase_date_str.strip(), "%Y-%m-%d").date()
    except Exception as e:
        return json.dumps({
            "error": f"Invalid purchase_date format '{purchase_date_str}'. Expected YYYY-MM-DD. Error: {str(e)}"
        })

    if current_date_str:
        try:
            curr_dt = datetime.strptime(current_date_str.strip(), "%Y-%m-%d").date()
        except Exception:
            curr_dt = CURRENT_DATE
    else:
        curr_dt = CURRENT_DATE

    # Determine category policy rules
    cat_lower = category.lower()
    matched_cat = None
    for standard_cat, windows in CATEGORY_WINDOWS.items():
        if standard_cat.lower() in cat_lower or any(word in cat_lower for word in standard_cat.lower().split()):
            matched_cat = standard_cat
            break

    if "electronic" in cat_lower or "headphone" in cat_lower or "cable" in cat_lower or "gadget" in cat_lower:
        policy = CATEGORY_WINDOWS["Consumer Electronics & Gadgets"]
    elif "apparel" in cat_lower or "cloth" in cat_lower or "shoe" in cat_lower or "jacket" in cat_lower or "sweater" in cat_lower:
        policy = CATEGORY_WINDOWS["Apparel, Clothing & Footwear"]
    elif "kitchen" in cat_lower or "home" in cat_lower or "appliance" in cat_lower or "bottle" in cat_lower:
        policy = CATEGORY_WINDOWS["Home & Kitchen Appliances"]
    elif "final" in cat_lower or "clearance" in cat_lower:
        policy = CATEGORY_WINDOWS["Final Sale & Clearance Items"]
    else:
        policy = CATEGORY_WINDOWS.get(matched_cat, {"return_days": 30, "warranty_days": 365})

    return_days = policy["return_days"]
    warranty_days = policy["warranty_days"]

    # 1. Return Window Calculation
    if return_days == 0:
        return_deadline = purchase_dt
        return_days_left = 0
        return_status = "NON_RETURNABLE_FINAL_SALE"
        return_flag = "FINAL_SALE"
    else:
        return_deadline = purchase_dt + timedelta(days=return_days)
        return_days_left = (return_deadline - curr_dt).days
        if return_days_left < 0:
            return_status = "EXPIRED"
            return_flag = "EXPIRED"
        elif return_days_left < URGENT_DAYS_THRESHOLD:
            return_status = "EXPIRING_SOON"
            return_flag = "URGENT_FLAG_TRIGGERED"
        else:
            return_status = "ACTIVE"
            return_flag = "OK"

    # 2. Warranty Calculation
    if warranty_days == 0:
        warranty_deadline = purchase_dt
        warranty_days_left = 0
        warranty_status = "NO_WARRANTY"
        warranty_flag = "NONE"
    else:
        warranty_deadline = purchase_dt + timedelta(days=warranty_days)
        warranty_days_left = (warranty_deadline - curr_dt).days
        if warranty_days_left < 0:
            warranty_status = "EXPIRED"
            warranty_flag = "EXPIRED"
        elif warranty_days_left < URGENT_DAYS_THRESHOLD:
            warranty_status = "EXPIRING_SOON"
            warranty_flag = "URGENT_FLAG_TRIGGERED"
        else:
            warranty_status = "ACTIVE"
            warranty_flag = "OK"

    result = {
        "item_name": item_name,
        "category": category,
        "purchase_date": purchase_dt.isoformat(),
        "current_reference_date": curr_dt.isoformat(),
        "return_policy_days": return_days,
        "return_deadline": return_deadline.isoformat(),
        "return_days_remaining": return_days_left,
        "return_status": return_status,
        "return_urgent_flag": return_flag,
        "warranty_policy_days": warranty_days,
        "warranty_deadline": warranty_deadline.isoformat(),
        "warranty_days_remaining": warranty_days_left,
        "warranty_status": warranty_status,
        "warranty_urgent_flag": warranty_flag,
        "proactive_summary": (
            f"'{item_name}': {return_days_left} days left to return (Deadline: {return_deadline.isoformat()}). "
            f"{'⚠️ EXPIRING SOON! Only ' + str(return_days_left) + ' days remaining!' if return_status == 'EXPIRING_SOON' else ''}"
            f"{'❌ Final Sale / Non-Returnable' if return_status == 'NON_RETURNABLE_FINAL_SALE' else ''}"
            f"{'❌ Return window has passed' if return_status == 'EXPIRED' else ''}"
            f" Warranty: {warranty_status} ({warranty_days_left} days remaining until {warranty_deadline.isoformat()})."
        )
    }
    return json.dumps(result, indent=2)

def compute_all_windows_for_receipt(
    receipt_data: Dict[str, Any],
    current_date_str: Optional[str] = None
) -> Dict[str, Any]:
    """
    Deterministic helper running immediately upon receipt ingestion.
    Calculates return and warranty window for all items on the receipt and flags
    items with fewer than 7 days left.
    """
    purchase_date_str = receipt_data.get("purchase_date")
    items = receipt_data.get("items", [])
    
    results = []
    has_urgent_items = False
    urgent_items = []

    for item in items:
        calc_json_str = calculate_return_and_warranty_window.invoke({
            "item_name": item.get("name", "Unknown Item"),
            "category": item.get("category", "General"),
            "purchase_date_str": purchase_date_str or CURRENT_DATE.isoformat(),
            "current_date_str": current_date_str
        })
        item_calc = json.loads(calc_json_str)
        results.append(item_calc)

        if item_calc.get("return_status") == "EXPIRING_SOON" or item_calc.get("warranty_status") == "EXPIRING_SOON":
            has_urgent_items = True
            urgent_items.append(item_calc)

    return {
        "order_id": receipt_data.get("order_id"),
        "customer": receipt_data.get("customer"),
        "purchase_date": purchase_date_str,
        "total_items": len(items),
        "has_urgent_items": has_urgent_items,
        "urgent_items": urgent_items,
        "items_analysis": results
    }

@tool
def lookup_order_status(order_id: str) -> str:
    """
    Queries the store's mock order database by order ID and returns live shipping
    and delivery details. Handles non-existent order IDs gracefully without fabricating statuses.
    
    Args:
        order_id: The unique Order ID to look up (e.g., 'ORD-1001', 'ORD-1002').
    
    Returns:
        JSON string containing the order record or a graceful not-found notification.
    """
    cleaned_id = order_id.strip().upper()
    conn = init_orders_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT order_id, customer_name, order_date, status, carrier, 
               tracking_number, estimated_delivery, items_summary, shipping_address
        FROM orders
        WHERE UPPER(order_id) = ?
    """, (cleaned_id,))

    row = cursor.fetchone()
    if not row:
        return json.dumps({
            "found": False,
            "order_id": order_id,
            "message": f"Order ID '{order_id}' was NOT found in the database. Please verify the order number with the shopper. No order status was fabricated."
        }, indent=2)

    order_info = {
        "found": True,
        "order_id": row[0],
        "customer_name": row[1],
        "order_date": row[2],
        "status": row[3],
        "carrier": row[4],
        "tracking_number": row[5],
        "estimated_delivery": row[6],
        "items_summary": row[7],
        "shipping_address": row[8]
    }
    return json.dumps(order_info, indent=2)

@tool
def google_web_search(query: str) -> str:
    """
    Searches the live web like Google for product manuals, manufacturer warranty support,
    carrier policies, store locations, or general information not found in the local receipt or store policy.
    
    Args:
        query: The search query or question to search the web for (e.g. 'Sony WH-1000XM5 manufacturer warranty support', 'FedEx delivery rules').
        
    Returns:
        JSON string of live web search results containing Titles, URLs, and Snippets.
    """
    cleaned_query = query.strip().strip("'").strip('"')
    
    # 1. Try DDGS Live Web Search
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            raw_results = list(ddgs.text(cleaned_query, max_results=4))
            if raw_results:
                formatted = []
                for i, r in enumerate(raw_results, 1):
                    formatted.append({
                        "result_number": i,
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", "")
                    })
                return json.dumps({
                    "query": cleaned_query,
                    "engine": "Google/Live Web Search",
                    "total_results": len(formatted),
                    "results": formatted
                }, indent=2)
    except Exception:
        pass

    # 2. Try DuckDuckGo Instant Answer API
    try:
        import urllib.request
        import urllib.parse
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(cleaned_query)}&format=json&no_html=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = []
            if data.get("AbstractText"):
                results.append({
                    "title": data.get("Heading", "Summary"),
                    "url": data.get("AbstractURL", ""),
                    "snippet": data.get("AbstractText", "")
                })
            for item in data.get("RelatedTopics", [])[:3]:
                if isinstance(item, dict) and "Text" in item:
                    results.append({
                        "title": item.get("Text", "")[:60] + "...",
                        "url": item.get("FirstURL", ""),
                        "snippet": item.get("Text", "")
                    })
            if results:
                return json.dumps({
                    "query": cleaned_query,
                    "engine": "Instant Web Search",
                    "results": results
                }, indent=2)
    except Exception:
        pass

    # 3. Wikipedia Knowledge Search Fallback
    try:
        import urllib.request
        import urllib.parse
        import re
        wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(cleaned_query)}&format=json&utf8="
        req = urllib.request.Request(wiki_url, headers={"User-Agent": "CODEXAgent/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("query", {}).get("search", [])
            if items:
                formatted = []
                for i, it in enumerate(items[:3], 1):
                    clean_snip = re.sub(r"<[^>]+>", "", it.get("snippet", ""))
                    formatted.append({
                        "result_number": i,
                        "title": it.get("title"),
                        "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(it.get('title', ''))}",
                        "snippet": clean_snip
                    })
                return json.dumps({
                    "query": cleaned_query,
                    "engine": "Web Knowledge Search",
                    "results": formatted
                }, indent=2)
    except Exception:
        pass

    return json.dumps({
        "query": cleaned_query,
        "message": f"No online search results found for '{cleaned_query}'."
    })

