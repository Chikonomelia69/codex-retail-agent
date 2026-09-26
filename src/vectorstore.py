import os
import re
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

from src.config import CHROMA_PERSIST_DIR, EMBEDDING_MODEL, OLLAMA_BASE_URL
from src.splitters import split_receipt_into_item_chunks, split_policy_document

def get_embedding_function():
    """Returns the Ollama embeddings model for vectorization."""
    return OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL
    )

def sanitize_collection_name(name: str) -> str:
    """Sanitize collection name to be compliant with Chroma's naming rules."""
    sanitized = re.sub(r"[^a-zA-Z0-9_\-]", "_", name)
    # Must start and end with alphanumeric character and be 3-63 chars
    if len(sanitized) < 3:
        sanitized = f"col_{sanitized}"
    elif len(sanitized) > 63:
        sanitized = sanitized[:63]
    return sanitized

def create_receipt_vectorstore(
    receipt_data: Dict[str, Any],
    policy_text: str,
    persist_directory: Path = CHROMA_PERSIST_DIR
) -> Chroma:
    """
    Embed and persist the current shopper receipt and store policy
    into a Chroma collection scoped to the receipt/order.
    """

    order_id = receipt_data.get("order_id", "session_default")
    collection_name = sanitize_collection_name(f"receipt_{order_id}")

    embeddings = get_embedding_function()

    # Split documents
    receipt_chunks: List[Document] = split_receipt_into_item_chunks(receipt_data)
    policy_chunks: List[Document] = split_policy_document(policy_text)

    all_chunks = receipt_chunks + policy_chunks

    # Ensure persistence directory exists
    persist_dir_str = str(persist_directory)
    os.makedirs(persist_dir_str, exist_ok=True)

    # Create a fresh vector store for this receipt.
    #
    # IMPORTANT:
    # Do not delete an existing Chroma collection here.
    # Multiple frontend requests can happen while an active CODEX
    # session is using the collection.
    vectorstore = Chroma.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=persist_dir_str
    )

    return vectorstore

def get_receipt_vectorstore(
    order_id: str,
    persist_directory: Path = CHROMA_PERSIST_DIR
) -> Optional[Chroma]:
    """Retrieve existing vector store scoped to a specific order ID."""
    collection_name = sanitize_collection_name(f"receipt_{order_id}")
    embeddings = get_embedding_function()
    
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=str(persist_directory)
    )
