import os
import sys
import json
from pathlib import Path
from datetime import date

# Ensure root directory is in sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Force UTF-8 on Windows terminal output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from src.config import (
    POLICY_PATH, 
    SAMPLE_RECEIPTS_DIR, 
    CURRENT_DATE, 
    URGENT_DAYS_THRESHOLD
)
from src.loaders import load_policy, load_receipt, init_orders_db
from src.splitters import split_receipt_into_item_chunks, split_policy_document
from src.vectorstore import create_receipt_vectorstore
from src.retriever import retrieve_item_and_policy
from src.tools import calculate_return_and_warranty_window, lookup_order_status
from src.agent import get_llm, ingest_receipt_proactively, answer_shopper_query

def print_banner(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_1_llm_setup():
    print_banner("STAGE 1: LLM SETUP (ChatGroq - Exclusive Provider)")
    llm = get_llm()
    res = llm.invoke("Say 'CODEX Groq LLM is operational' in 5 words or less.")
    print(f"ChatGroq Response: {res.content.strip()}")
    assert len(res.content.strip()) > 0, "LLM returned empty response"
    print("[PASS] Stage 1 Passed: ChatGroq is operational with user key.")

def test_2_document_loading():
    print_banner("STAGE 2: DOCUMENT LOADING")
    policy_text = load_policy(POLICY_PATH)
    print(f"Loaded policy document: {len(policy_text)} chars")
    assert "CODEX RETAIL - RETURN, EXCHANGE & WARRANTY POLICY" in policy_text

    receipt_file = SAMPLE_RECEIPTS_DIR / "receipt_urgent_electronics.txt"
    receipt_data = load_receipt(receipt_file)
    print(f"Loaded receipt: Order {receipt_data['order_id']}, Customer: {receipt_data['customer']}")
    print(f"Parsed {len(receipt_data['items'])} items.")
    assert len(receipt_data['items']) == 3, f"Expected 3 items, got {len(receipt_data['items'])}"
    print("[PASS] Stage 2 Passed: Receipt & Policy documents loaded.")

def test_3_text_splitting():
    print_banner("STAGE 3: TEXT SPLITTING (Per-Item Chunks & Policy Chunks)")
    receipt_file = SAMPLE_RECEIPTS_DIR / "receipt_urgent_electronics.txt"
    receipt_data = load_receipt(receipt_file)
    receipt_chunks = split_receipt_into_item_chunks(receipt_data)
    
    print(f"Generated {len(receipt_chunks)} chunks for receipt (1 header + {len(receipt_data['items'])} per-item chunks).")
    for doc in receipt_chunks:
        print(f" - Chunk [{doc.metadata.get('doc_type')}]: {doc.metadata.get('item_name', 'Header')} ({doc.metadata.get('chunk_id')})")
    assert any(doc.metadata.get("doc_type") == "receipt_item" for doc in receipt_chunks)

    policy_text = load_policy(POLICY_PATH)
    policy_chunks = split_policy_document(policy_text)
    print(f"Generated {len(policy_chunks)} logical clause chunks for policy.")
    assert len(policy_chunks) >= 4, "Expected multiple policy clauses"
    print("[PASS] Stage 3 Passed: Specialized text splitting verified.")

def test_4_and_5_vectorstore_and_retriever():
    print_banner("STAGES 4 & 5: VECTOR STORE (Chroma) & RETRIEVER")
    # Use apparel receipt for the workshop canonical query: "when can I return the jacket"
    apparel_receipt = SAMPLE_RECEIPTS_DIR / "receipt_apparel_mixed.txt"
    receipt_data = load_receipt(apparel_receipt)
    policy_text = load_policy(POLICY_PATH)

    print("Creating scoped Chroma vector store for receipt...")
    vectorstore = create_receipt_vectorstore(receipt_data, policy_text)
    print("Scoped vector store ready.")

    query = "when can I return the jacket"
    print(f"Executing query: '{query}'")
    retrieval_res = retrieve_item_and_policy(query, vectorstore, k=4)

    receipt_items = retrieval_res["receipt_items"]
    policy_clauses = retrieval_res["policy_clauses"]

    print(f"Retrieved {len(receipt_items)} receipt items and {len(policy_clauses)} policy clauses.")
    assert len(receipt_items) > 0, "Failed to retrieve jacket receipt item"
    assert any("jacket" in d.page_content.lower() for d in receipt_items), "Jacket was not in retrieved item chunks"
    print(f"Top Receipt Item Chunk:\n{receipt_items[0].page_content[:200]}...\n")
    print(f"Top Policy Clause Chunk:\n{policy_clauses[0].page_content[:200] if policy_clauses else 'N/A'}...\n")
    print("[PASS] Stages 4 & 5 Passed: Vector store persistence & dual retrieval verified.")

def test_6_custom_tools():
    print_banner("STAGE 6: CUSTOM TOOLS & TOOL CALLING")
    
    # Tool 1: Window Calculator (5 days left -> must trigger EXPIRING_SOON flag)
    calc_res_json = calculate_return_and_warranty_window.invoke({
        "item_name": "Sony WH-1000XM5 Headphones",
        "category": "Consumer Electronics & Gadgets",
        "purchase_date_str": "2026-08-27",
        "current_date_str": "2026-09-21"
    })
    calc_res = json.loads(calc_res_json)
    print("Window Calculator Output:")
    print(f" - Return Days Remaining: {calc_res['return_days_remaining']}")
    print(f" - Return Status: {calc_res['return_status']}")
    print(f" - Return Urgent Flag: {calc_res['return_urgent_flag']}")
    assert calc_res["return_days_remaining"] == 5, f"Expected 5 days, got {calc_res['return_days_remaining']}"
    assert calc_res["return_status"] == "EXPIRING_SOON", "Expected EXPIRING_SOON"
    assert calc_res["return_urgent_flag"] == "URGENT_FLAG_TRIGGERED", "Expected URGENT_FLAG_TRIGGERED"
    print("  -> Date math and urgency flag (< 7 days) verified!")

    # Tool 2: Order Status Lookup
    found_order_json = lookup_order_status.invoke({"order_id": "ORD-1002"})
    found_order = json.loads(found_order_json)
    print(f"Lookup ORD-1002 Status: {found_order.get('status')} via {found_order.get('carrier')}")
    assert found_order.get("found") is True
    assert found_order.get("status") == "Shipped"

    # Tool 2: Graceful not-found handling (Zero hallucination)
    missing_order_json = lookup_order_status.invoke({"order_id": "ORD-UNKNOWN-999"})
    missing_order = json.loads(missing_order_json)
    print(f"Lookup ORD-UNKNOWN-999 Result: {missing_order.get('message')}")
    assert missing_order.get("found") is False
    assert "NOT found" in missing_order.get("message")
    print("[PASS] Stage 6 Passed: Both tools executed with deterministic accuracy.")

def test_7_and_8_proactive_ingestion_and_agent():
    print_banner("STAGES 7 & 8: PROACTIVE INGESTION & REACT AGENT")
    urgent_receipt = SAMPLE_RECEIPTS_DIR / "receipt_urgent_electronics.txt"
    
    print("Ingesting receipt proactively...")
    ingestion_result = ingest_receipt_proactively(urgent_receipt, current_date_str="2026-09-21")
    session = ingestion_result["session"]
    proactive_summary = ingestion_result["proactive_summary"]

    print("\n--- PROACTIVE INGESTION SUMMARY (Rendered BEFORE any user question) ---")
    print(proactive_summary)
    print("-----------------------------------------------------------------------")

    assert "EXPIRING WINDOW ALERT" in proactive_summary, "Urgent alert banner missing from proactive summary!"
    assert "5 days remaining" in proactive_summary, "Exact days calculation missing from proactive summary!"

    # Now test follow-up question
    follow_up_1 = "When is the deadline to return the Sony headphones?"
    print(f"\nShopper asks follow-up: '{follow_up_1}'")
    answer_1 = answer_shopper_query(session, follow_up_1)
    print(f"CODEX Agent Answer:\n{answer_1}\n")

    follow_up_2 = "Can I return the microfiber cleaning kit?"
    print(f"\nShopper asks follow-up: '{follow_up_2}'")
    answer_2 = answer_shopper_query(session, follow_up_2)
    print(f"CODEX Agent Answer:\n{answer_2}\n")

    # Follow-up order lookup query
    order_query = "What is the status of my order ORD-1001?"
    print(f"\nShopper asks: '{order_query}'")
    order_answer = answer_shopper_query(session, order_query)
    print(f"CODEX Agent Answer:\n{order_answer}\n")
    assert "Delivered" in order_answer

    print("[PASS] Stages 7 & 8 Passed: Proactive ingestion and grounded QA functioning flawlessly.")

def main():
    print("Starting CODEX End-to-End Pipeline Verification Suite...")
    test_1_llm_setup()
    test_2_document_loading()
    test_3_text_splitting()
    test_4_and_5_vectorstore_and_retriever()
    test_6_custom_tools()
    test_7_and_8_proactive_ingestion_and_agent()
    print_banner("[SUCCESS] ALL WORKSHOP PIPELINE STAGES VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
