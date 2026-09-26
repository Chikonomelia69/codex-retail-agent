from typing import List, Dict, Any, Optional
from langchain_chroma import Chroma
from langchain_core.documents import Document

def retrieve_item_and_policy(
    query: str,
    vectorstore: Chroma,
    k: int = 4,
    k_items: Optional[int] = None,
    k_policy: Optional[int] = None
) -> Dict[str, Any]:
    """
    Dual-aspect retriever: Ensures queries retrieve BOTH the matching
    receipt item (from the shopper's uploaded receipt) and the corresponding
    store policy clause (from CODEX policy).
    """
    num_items = k_items if k_items is not None else max(1, k // 2)
    num_policy = k_policy if k_policy is not None else max(1, k // 2)

    receipt_items: List[Document] = []
    policy_clauses: List[Document] = []

    # 1. Retrieve scoped receipt items matching the query
    try:
        receipt_items = vectorstore.similarity_search(
            query, 
            k=num_items, 
            filter={"doc_type": "receipt_item"}
        )
    except Exception:
        pass

    # 2. Retrieve store policy clauses matching the query
    try:
        policy_clauses = vectorstore.similarity_search(
            query, 
            k=num_policy, 
            filter={"doc_type": "policy_clause"}
        )
    except Exception:
        pass

    # Fallback to similarity_search_with_score or collection lookup if filtered search returned nothing
    if not receipt_items:
        try:
            docs_with_scores = vectorstore.similarity_search_with_score(
                query, 
                k=num_items, 
                filter={"doc_type": "receipt_item"}
            )
            receipt_items = [d for d, _ in docs_with_scores]
        except Exception:
            pass

    if not receipt_items:
        try:
            col_res = vectorstore._collection.get(where={"doc_type": "receipt_item"})
            if col_res and col_res.get("documents"):
                for d_text, d_meta in zip(col_res["documents"][:num_items], col_res["metadatas"][:num_items]):
                    receipt_items.append(Document(page_content=d_text, metadata=d_meta))
        except Exception:
            pass

    if not policy_clauses:
        try:
            docs_with_scores = vectorstore.similarity_search_with_score(
                query, 
                k=num_policy, 
                filter={"doc_type": "policy_clause"}
            )
            policy_clauses = [d for d, _ in docs_with_scores]
        except Exception:
            pass

    all_docs = receipt_items + policy_clauses

    formatted_context = ""
    if receipt_items:
        formatted_context += "=== PURCHASED ITEMS MATCHING QUERY ===\n"
        for item_doc in receipt_items:
            formatted_context += f"{item_doc.page_content}\n\n"

    if policy_clauses:
        formatted_context += "=== RELEVANT CODEX STORE POLICIES ===\n"
        for pol_doc in policy_clauses:
            formatted_context += f"{pol_doc.page_content}\n\n"

    return {
        "raw_docs": all_docs,
        "receipt_items": receipt_items,
        "policy_clauses": policy_clauses,
        "formatted_context": formatted_context.strip()
    }
