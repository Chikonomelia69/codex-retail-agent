import os
import re
import json
import sqlite3
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from src.config import POLICY_PATH, ORDERS_CSV_PATH, ORDERS_DB_PATH, CURRENT_DATE

def load_policy(policy_path: Optional[Path] = None) -> str:
    """Load store return and warranty policy document."""
    path = policy_path or POLICY_PATH
    if not path.exists():
        raise FileNotFoundError(f"Policy file not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def infer_category(item_name: str, given_cat: Optional[str] = None) -> str:
    """Infers standard CODEX store category based on product title and keywords."""
    if given_cat and given_cat.strip() and given_cat.strip().lower() not in ["general", "unknown", "item", "default", "n/a"]:
        gc = given_cat.lower()
        if any(k in gc for k in ["elect", "gadget", "headphone", "audio", "phone", "cable", "tech", "mouse", "hub", "ssd"]):
            return "Consumer Electronics & Gadgets"
        if any(k in gc for k in ["apparel", "cloth", "footwear", "shoe", "wear", "jacket", "shirt", "coat", "sleeve"]):
            return "Apparel, Clothing & Footwear"
        if any(k in gc for k in ["kitchen", "home", "appliance"]):
            return "Home & Kitchen Appliances"
        if any(k in gc for k in ["final", "clear"]):
            return "Final Sale & Clearance Items"
        return given_cat.strip()

    name_lower = item_name.lower()
    if any(k in name_lower for k in ["clearance", "final sale", "as-is", "non-returnable", "liquidation", "non-refundable"]):
        return "Final Sale & Clearance Items"
    if any(k in name_lower for k in [
        "headphone", "earphone", "sony", "apple", "phone", "laptop", "cable", 
        "charger", "usb", "tv", "monitor", "audio", "speaker", "gadget", 
        "battery", "camera", "tech", "airpod", "tablet", "ipad", "watch", 
        "playstation", "xbox", "nintendo", "cord", "anker", "electronic", 
        "adapter", "mouse", "hub", "ssd", "hard drive", "storage", "drive", 
        "keyboard", "display", "webcam", "ram", "cpu", "gpu"
    ]):
        return "Consumer Electronics & Gadgets"
    if any(k in name_lower for k in ["sleeve", "jacket", "coat", "hoodie", "shirt", "pant", "jean", "sweater", "footwear", "shoe", "boot", "sneaker", "sock", "dress", "apparel", "cloth", "hat", "glove", "rainwear", "patagonia", "fleece", "wool", "denim", "cotton", "tote", "t-shirt"]):
        return "Apparel, Clothing & Footwear"
    if any(k in name_lower for k in ["blender", "mixer", "kettle", "toaster", "microwave", "pan", "pot", "knife", "cookware", "appliance", "bottle", "mug", "dish", "lamp", "vacuum", "filter", "container", "kitchen", "home", "coffeemaker", "coffee"]):
        return "Home & Kitchen Appliances"

    return "Consumer Electronics & Gadgets"

def extract_items_flexible(text: str, order_id: str, purchase_date: Optional[str]) -> List[Dict[str, Any]]:
    """
    Flexible fallback parser for arbitrary shopkeeper receipts, POS tickets, 
    markdown pipe tables, invoices, and tabular item lines.
    """
    items = []
    lines = text.strip().split("\n")
    skip_keywords = [
        "SUBTOTAL", "SALES TAX", "TAX", "TOTAL CHARGE", "TOTAL DUE", "TOTAL", "PAYMENT", 
        "CASHIER", "DATE", "STORE", "CUSTOMER", "ORDER", "RECEIPT", "INVOICE", 
        "BILL", "THANK YOU", "TEL:", "PHONE", "WWW.", "HTTP", "POLICY NOTICE", 
        "RETURN", "EXCHANGE", "WARRANTY", "AUTH CODE", "PAYMENT METHOD", "VISIT US"
    ]
    
    for line in lines:
        raw_l = line.strip().strip("|").strip()
        if not raw_l or raw_l.startswith(("=", "-", "*", "#", "/")):
            continue
        
        # Check if line contains a price ($XX.XX or XX.XX)
        prices = re.findall(r"[\$£€]?\s*(\d+\.\d{2})\b", raw_l)
        if not prices:
            continue
            
        upper_l = raw_l.upper()
        if any(kw in upper_l for kw in skip_keywords):
            continue
            
        # Parse prices (unit price vs total price)
        unit_price = float(prices[0])
        total_price = float(prices[1]) if len(prices) > 1 else unit_price
        
        # Text before the first price is the item description and optional qty
        first_price_str = prices[0]
        p_idx = raw_l.find(first_price_str)
        # Check if there is a currency symbol right before
        if p_idx > 0 and raw_l[p_idx - 1] in ["$", "£", "€"]:
            p_idx -= 1
        pre_text = raw_l[:p_idx].strip()
        
        # Clean leading item numbering like "1. ", "[1] ", "#1 "
        clean_name = re.sub(r"^(?:\d+[\.\)]|\[\d+\]|#\d+)\s*", "", pre_text).strip()
        clean_name = re.sub(r"[\-:\t|]+$", "", clean_name).strip()
        
        # Extract Qty (e.g., trailing digit in table column, or "x2", "Qty: 2")
        qty = 1
        qty_trailing = re.search(r"\b(\d+)\s*$", clean_name)
        qty_prefix = re.search(r"\b(?:x|qty[:\s]*)\s*(\d+)\b", clean_name, re.IGNORECASE)
        
        if qty_prefix:
            qty = int(qty_prefix.group(1))
            clean_name = re.sub(r"\b(?:x|qty[:\s]*)\s*\d+\b", "", clean_name, flags=re.IGNORECASE).strip()
        elif qty_trailing and int(qty_trailing.group(1)) > 0 and int(qty_trailing.group(1)) <= 100:
            qty = int(qty_trailing.group(1))
            clean_name = clean_name[:qty_trailing.start()].strip()
            
        if len(clean_name) < 2:
            continue
            
        category = infer_category(clean_name)
        condition = "Final Sale - Non Refundable" if category == "Final Sale & Clearance Items" else "New"
        
        # If total price wasn't separate, calculate from qty * unit_price
        if len(prices) == 1:
            total_price = round(unit_price * qty, 2)
        elif len(prices) > 1 and qty > 1 and total_price == unit_price:
            total_price = round(unit_price * qty, 2)
        
        items.append({
            "name": clean_name,
            "sku": f"SKU-{abs(hash(clean_name)) % 10000:04d}",
            "category": category,
            "qty": qty,
            "unit_price": unit_price,
            "total_price": total_price,
            "condition": condition,
            "serial_number": None,
            "purchase_date": purchase_date,
            "order_id": order_id,
            "raw_block": raw_l
        })
        
    return items

def extract_receipt_with_llm(raw_text: str) -> Optional[Dict[str, Any]]:
    """Zero-failure LLM extraction fallback for complex, non-standard receipt formats."""
    try:
        from langchain_groq import ChatGroq
        from langchain_core.messages import SystemMessage, HumanMessage
        from src.config import GROQ_API_KEY, GROQ_MODEL
        if not GROQ_API_KEY:
            return None
            
        llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0.0)
        sys_msg = SystemMessage(content="You are an expert commerce receipt parser. Output ONLY a valid JSON object with no markdown fences, no explanations.")
        user_prompt = (
            "Extract the following receipt into JSON format with keys:\n"
            "- store_name (string)\n"
            "- order_id (string)\n"
            "- customer (string)\n"
            "- purchase_date (string in YYYY-MM-DD)\n"
            "- total (float)\n"
            "- items: list of objects with {name, sku, category, qty, unit_price, total_price, condition}\n"
            "Categories must be one of: 'Consumer Electronics & Gadgets', 'Apparel, Clothing & Footwear', 'Home & Kitchen Appliances', 'Final Sale & Clearance Items'.\n\n"
            f"RECEIPT TEXT:\n{raw_text[:4000]}"
        )
        resp = llm.invoke([sys_msg, HumanMessage(content=user_prompt)])
        content = resp.content.strip()
        if content.startswith("```"):
            content = re.sub(r"^```(?:json)?\s*", "", content)
            content = re.sub(r"\s*```$", "", content)
        data = json.loads(content)
        return data
    except Exception:
        return None

def parse_receipt_text(text: str) -> Dict[str, Any]:
    """Parse receipt text into structured metadata and item chunks."""
    # 0. Normalize non-standard Unicode characters (non-breaking hyphens, spaces, curly quotes)
    text = (
        text.replace('\u2011', '-')
            .replace('\u2012', '-')
            .replace('\u2013', '-')
            .replace('\u2014', '-')
            .replace('\u202f', ' ')
            .replace('\xa0', ' ')
            .replace('\u2018', "'")
            .replace('\u2019', "'")
            .replace('\u201c', '"')
            .replace('\u201d', '"')
    )

    receipt_data = {
        "raw_text": text,
        "store_name": "CODEX Retail Store",
        "order_id": "UNKNOWN",
        "customer": "Valued Shopper",
        "purchase_date": None,
        "items": [],
        "subtotal": None,
        "tax": None,
        "total": None
    }

    # 1. Extract Store Name
    store_match = re.search(r"^\s*([A-Z0-9\s#&'-]+(?:STORE|MART|SHOP|SUPERSTORE|OUTLET|RETAIL|INC|LLC)[^\n]*)", text, re.IGNORECASE | re.MULTILINE)
    if store_match:
        receipt_data["store_name"] = store_match.group(1).strip()
    else:
        first_line = text.strip().split("\n")[0].strip() if text.strip() else ""
        if len(first_line) > 2 and len(first_line) < 45 and not first_line.startswith(("=", "-", "#")):
            receipt_data["store_name"] = first_line

    # 2. Extract Order/Receipt ID
    id_match = re.search(r"(?:RECEIPT\s*#?|ORDER\s*#?|INVOICE\s*#?|BILL\s*#?|TXN\s*#?):\s*([A-Za-z0-9\-]+)", text, re.IGNORECASE)
    if id_match:
        receipt_data["order_id"] = id_match.group(1).strip()
    else:
        # Broader fallback
        id_fallback = re.search(r"\b(?:ORD|REC|INV)-(\d{4,8})\b", text, re.IGNORECASE)
        if id_fallback:
            receipt_data["order_id"] = id_fallback.group(0).upper()
        else:
            receipt_data["order_id"] = f"REC-{abs(hash(text[:50])) % 9000 + 1000}"

    # 3. Extract Customer Name
    cust_match = re.search(r"(?:CUSTOMER|SHOPPER|CLIENT|NAME|BILL\s*TO|SOLD\s*TO|CASHIER):\s*([^\r\n|]+)", text, re.IGNORECASE)
    if cust_match:
        receipt_data["customer"] = cust_match.group(1).strip()

    # 4. Extract Purchase Date (ISO, Slash, or Alphanumeric like '22 Sep 2026')
    date_match = re.search(r"(?:DATE\s*OF\s*PURCHASE|PURCHASE\s*DATE|DATE):\s*([A-Za-z0-9\s,\-\/]+?)(?:\s+(?:TIME|\d{1,2}:)|[\r\n]|$)", text, re.IGNORECASE)
    if date_match:
        raw_date = date_match.group(1).strip()
        for fmt in ["%d %b %Y", "%d %B %Y", "%b %d %Y", "%B %d %Y", "%b %d, %Y", "%B %d, %Y", "%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]:
            try:
                receipt_data["purchase_date"] = datetime.strptime(raw_date, fmt).date().isoformat()
                break
            except ValueError:
                pass

    if not receipt_data["purchase_date"]:
        # Fallback date search
        date_iso = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", text)
        if date_iso:
            receipt_data["purchase_date"] = date_iso.group(1)
        else:
            date_slash = re.search(r"\b(\d{1,2}/\d{1,2}/\d{2,4})\b", text)
            if date_slash:
                parts = date_slash.group(1).split("/")
                if len(parts[2]) == 2:
                    parts[2] = "20" + parts[2]
                receipt_data["purchase_date"] = f"{parts[2]}-{int(parts[0]):02d}-{int(parts[1]):02d}"
            else:
                receipt_data["purchase_date"] = CURRENT_DATE.isoformat()

    # 5. Extract Total
    total_match = re.search(r"(?:\*\*)?TOTAL(?:\s*DUE|\s*CHARGED|\s*CHARGE)?(?:\*\*)?:\s*\$?([\d\.]+)", text, re.IGNORECASE)
    if total_match:
        try:
            receipt_data["total"] = float(total_match.group(1))
        except ValueError:
            pass

    # 6. Extract Items: Strategy A (Canonical CODEX block structure)
    item_blocks = re.findall(r"(Item:\s*.+?)(?=(?:\n\s*Item:|\n\s*---+|\n\s*===+|\Z))", text, re.DOTALL | re.IGNORECASE)
    
    for block in item_blocks:
        name_match = re.search(r"Item:\s*(.+)", block, re.IGNORECASE)
        sku_match = re.search(r"SKU:\s*([A-Za-z0-9\-]+)", block, re.IGNORECASE)
        cat_match = re.search(r"Category:\s*(.+)", block, re.IGNORECASE)
        qty_match = re.search(r"Qty:\s*(\d+)", block, re.IGNORECASE)
        price_match = re.search(r"(?:Unit\s*Price|Price):\s*\$?([\d\.]+)", block, re.IGNORECASE)
        total_price_match = re.search(r"Total:\s*\$?([\d\.]+)", block, re.IGNORECASE)
        condition_match = re.search(r"Condition:\s*(.+)", block, re.IGNORECASE)
        sn_match = re.search(r"Serial\s*Number:\s*([A-Za-z0-9\-]+)", block, re.IGNORECASE)

        item_name = name_match.group(1).strip() if name_match else "Unknown Item"
        item_cat = infer_category(item_name, cat_match.group(1).strip() if cat_match else None)

        item_dict = {
            "name": item_name,
            "sku": sku_match.group(1).strip() if sku_match else "SKU-N/A",
            "category": item_cat,
            "qty": int(qty_match.group(1)) if qty_match else 1,
            "unit_price": float(price_match.group(1)) if price_match else 0.0,
            "total_price": float(total_price_match.group(1)) if total_price_match else 0.0,
            "condition": condition_match.group(1).strip() if condition_match else "Standard",
            "serial_number": sn_match.group(1).strip() if sn_match else None,
            "purchase_date": receipt_data["purchase_date"],
            "order_id": receipt_data["order_id"],
            "raw_block": block.strip()
        }
        receipt_data["items"].append(item_dict)

    # 7. Extract Items: Strategy B (Flexible Line-by-Line POS/Shopkeeper/Table Parser)
    if not receipt_data["items"]:
        receipt_data["items"] = extract_items_flexible(
            text=text,
            order_id=receipt_data["order_id"],
            purchase_date=receipt_data["purchase_date"]
        )

    # 8. Extract Items: Strategy C (LLM Fallback for Unstructured Receipts)
    if not receipt_data["items"]:
        llm_data = extract_receipt_with_llm(text)
        if llm_data and isinstance(llm_data, dict):
            if llm_data.get("store_name"):
                receipt_data["store_name"] = llm_data["store_name"]
            if llm_data.get("order_id"):
                receipt_data["order_id"] = llm_data["order_id"]
            if llm_data.get("customer"):
                receipt_data["customer"] = llm_data["customer"]
            if llm_data.get("purchase_date"):
                receipt_data["purchase_date"] = llm_data["purchase_date"]
            if llm_data.get("total"):
                receipt_data["total"] = float(llm_data["total"])
            if llm_data.get("items"):
                for it in llm_data["items"]:
                    receipt_data["items"].append({
                        "name": it.get("name", "Unknown Item"),
                        "sku": it.get("sku", f"SKU-{abs(hash(it.get('name', ''))) % 10000:04d}"),
                        "category": it.get("category", "Consumer Electronics & Gadgets"),
                        "qty": int(it.get("qty", 1)),
                        "unit_price": float(it.get("unit_price", 0.0)),
                        "total_price": float(it.get("total_price", 0.0)),
                        "condition": it.get("condition", "New"),
                        "serial_number": None,
                        "purchase_date": receipt_data["purchase_date"],
                        "order_id": receipt_data["order_id"],
                        "raw_block": str(it)
                    })

    # 9. Compute total if missing
    if receipt_data["total"] is None and receipt_data["items"]:
        receipt_data["total"] = round(sum(it["total_price"] for it in receipt_data["items"]), 2)

    return receipt_data

def load_receipt(receipt_source: Any) -> Dict[str, Any]:
    """Load receipt from a file path or raw text string."""
    if isinstance(receipt_source, (str, Path)) and os.path.exists(str(receipt_source)):
        with open(receipt_source, "r", encoding="utf-8") as f:
            content = f.read()
    elif isinstance(receipt_source, str):
        content = receipt_source
    elif hasattr(receipt_source, "read"):
        content = receipt_source.read()
        if isinstance(content, bytes):
            content = content.decode("utf-8")
    else:
        raise ValueError("Unsupported receipt source format")

    return parse_receipt_text(content)

def init_orders_db() -> sqlite3.Connection:
    """Initialize SQLite mock order database from CSV if not present."""
    conn = sqlite3.connect(str(ORDERS_DB_PATH), check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_name TEXT,
            order_date TEXT,
            status TEXT,
            carrier TEXT,
            tracking_number TEXT,
            estimated_delivery TEXT,
            items_summary TEXT,
            shipping_address TEXT
        )
    """)
    conn.commit()

    # Populate from CSV if empty
    cursor.execute("SELECT COUNT(*) FROM orders")
    count = cursor.fetchone()[0]
    if count == 0 and ORDERS_CSV_PATH.exists():
        df = pd.read_csv(ORDERS_CSV_PATH)
        df.to_sql("orders", conn, if_exists="append", index=False)
        conn.commit()

    return conn
