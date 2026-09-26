import json
import sqlite3
from typing import Optional
from fastmcp import FastMCP
from src.tools import calculate_return_and_warranty_window, lookup_order_status

# Initialize FastMCP Server for CODEX
mcp = FastMCP("CODEX_Order_Warranty_Server")

@mcp.tool()
def mcp_calculate_return_and_warranty_window(
    item_name: str,
    category: str,
    purchase_date_str: str,
    current_date_str: Optional[str] = None
) -> str:
    """
    Computes days remaining in the return or warranty window from purchase date and policy document.
    Flags anything with fewer than 7 days left as EXPIRING_SOON.
    """
    return calculate_return_and_warranty_window.invoke({
        "item_name": item_name,
        "category": category,
        "purchase_date_str": purchase_date_str,
        "current_date_str": current_date_str
    })

@mcp.tool()
def mcp_lookup_order_status(order_id: str) -> str:
    """
    Queries mock order database by order ID and returns tracking details.
    Handles not-found IDs gracefully without fabricating statuses.
    """
    return lookup_order_status.invoke({"order_id": order_id})

if __name__ == "__main__":
    print("Starting CODEX FastMCP server on stdio...")
    mcp.run()
