import re
from typing import List, Dict, Any
from langchain_core.documents import Document

def split_receipt_into_item_chunks(receipt_data: Dict[str, Any]) -> List[Document]:
    """
    Splits receipt into distinct item records (one item per chunk)
    rather than fixed character splitting.
    """
    documents = []
    order_id = receipt_data.get("order_id", "UNKNOWN")
    purchase_date = receipt_data.get("purchase_date", "UNKNOWN")
    customer = receipt_data.get("customer", "Customer")
    store_name = receipt_data.get("store_name", "CODEX Store")

    items = receipt_data.get("items", [])
    for idx, item in enumerate(items, start=1):
        content = (
            f"RECEIPT ITEM #{idx} [Order: {order_id}]\n"
            f"Product Name: {item.get('name')}\n"
            f"SKU: {item.get('sku')}\n"
            f"Category: {item.get('category')}\n"
            f"Quantity: {item.get('qty')}\n"
            f"Unit Price: ${item.get('unit_price'):.2f}\n"
            f"Total Price: ${item.get('total_price'):.2f}\n"
            f"Condition: {item.get('condition')}\n"
            f"Serial Number: {item.get('serial_number') or 'None'}\n"
            f"Purchase Date: {purchase_date}\n"
            f"Customer: {customer}\n"
            f"Store: {store_name}"
        )
        metadata = {
            "doc_type": "receipt_item",
            "order_id": order_id,
            "item_name": item.get("name"),
            "sku": item.get("sku"),
            "category": item.get("category"),
            "purchase_date": purchase_date,
            "unit_price": item.get("unit_price"),
            "chunk_id": f"{order_id}_item_{idx}"
        }
        documents.append(Document(page_content=content, metadata=metadata))

    # Also include one receipt header summary document
    header_content = (
        f"RECEIPT SUMMARY HEADER\n"
        f"Store: {store_name}\n"
        f"Order / Receipt ID: {order_id}\n"
        f"Customer: {customer}\n"
        f"Purchase Date: {purchase_date}\n"
        f"Item Count: {len(items)}\n"
        f"Total Amount Charged: ${receipt_data.get('total') or 0.0:.2f}"
    )
    documents.append(Document(
        page_content=header_content,
        metadata={
            "doc_type": "receipt_header",
            "order_id": order_id,
            "purchase_date": purchase_date,
            "chunk_id": f"{order_id}_header"
        }
    ))

    return documents

def split_policy_document(policy_text: str) -> List[Document]:
    """
    Chunks policy document by logical sections and category clauses.
    """
    documents = []
    # Split on markdown H2 (##) or H3 (###) headers
    sections = re.split(r"(?=\n##\s+)", policy_text)

    for sec_idx, section in enumerate(sections, start=1):
        clean_section = section.strip()
        if not clean_section:
            continue

        # Extract title from first line
        first_line = clean_section.split("\n")[0].replace("#", "").strip()

        # If section contains sub-clauses (###), split further for precision
        subsections = re.split(r"(?=\n###\s+)", clean_section)
        if len(subsections) > 1:
            for sub_idx, sub in enumerate(subsections, start=1):
                clean_sub = sub.strip()
                if not clean_sub:
                    continue
                sub_title = clean_sub.split("\n")[0].replace("#", "").strip()
                metadata = {
                    "doc_type": "policy_clause",
                    "section_title": f"{first_line} -> {sub_title}",
                    "chunk_id": f"policy_{sec_idx}_{sub_idx}"
                }
                documents.append(Document(page_content=clean_sub, metadata=metadata))
        else:
            metadata = {
                "doc_type": "policy_clause",
                "section_title": first_line,
                "chunk_id": f"policy_{sec_idx}"
            }
            documents.append(Document(page_content=clean_section, metadata=metadata))

    return documents
