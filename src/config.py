import os
from pathlib import Path
from datetime import date

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

# Data Paths
DATA_DIR = BASE_DIR / "data"
POLICY_PATH = DATA_DIR / "policy" / "store_policy.md"
SAMPLE_RECEIPTS_DIR = DATA_DIR / "sample_receipts"
ORDERS_CSV_PATH = DATA_DIR / "orders_db.csv"
ORDERS_DB_PATH = DATA_DIR / "orders.db"
CHROMA_PERSIST_DIR = BASE_DIR / "chroma_db"

# Groq LLM Configuration (EXCLUSIVELY GROQ)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Embedding Settings
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-minilm")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

# Business Logic Configuration
URGENT_DAYS_THRESHOLD = 7
CURRENT_DATE = date.today()

# Category standard windows in days
CATEGORY_WINDOWS = {
    "Consumer Electronics & Gadgets": {"return_days": 30, "warranty_days": 365},
    "Apparel, Clothing & Footwear": {"return_days": 30, "warranty_days": 90},
    "Home & Kitchen Appliances": {"return_days": 45, "warranty_days": 730},
    "Final Sale & Clearance Items": {"return_days": 0, "warranty_days": 0},
    "Personal Care, Health & Perishables": {"return_days": 0, "warranty_days": 0}
}
