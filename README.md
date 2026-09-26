<div align="center">

# ⚡ CODEX: Autonomous Retail & Warranty Agent
### *Track 5: E-Commerce / Retail Agentic RAG System*

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-1.4+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-gpt--oss--120b-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![FastMCP](https://img.shields.io/badge/FastMCP-4.0+-00DC82?style=for-the-badge)](https://modelcontextprotocol.io)
[![Three.js](https://img.shields.io/badge/Three.js-WebGL%203D-000000?style=for-the-badge&logo=three.js&logoColor=white)](https://threejs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <b>An autonomous retail intelligence system that ingests shopper receipts, parses line items, scopes a Chroma vector database, deterministically computes return and warranty horizons, and proactively flags expiring windows before any question is asked.</b>
</p>

[Quick Start](#-quick-start) • [Architecture](#-architecture--data-flow) • [Key Features](#-key-features) • [Samples](#-sample-evaluation-receipts) • [API Reference](#-rest-api-reference) • [Verification](#-verification-matrix)

---
</div>

## 🌟 Key Features

- **🚨 Proactive Ingestion & Urgency Alerting**: Automatically scans receipts upon upload and triggers bold alerts for any return or warranty window expiring in `< 7 days` *before* the shopper types a single prompt.
- **⏱️ Deterministic Return & Warranty Math**: Replaces LLM date hallucinations with verified Python arithmetic: `Days Remaining = (Purchase Date + Policy Days) - Current Date`.
- **🌐 Google AI Overview Powered by Gemini**: Delivers instant, bold **Direct Answers**, verified citation cards (Store Policy, Receipt Items, Carrier DB), and interactive **"People Also Ask"** chips.
- **📊 5.6 Tera ChartGPT Visual Analytics**: Interactive 5.6 Tera visual intelligence engine rendering dynamic bar, line, and area charts for 7-day revenue velocity, return urgency radars, and warranty coverage horizons.
- **🎬 3D Cinematic Ambient Background**: GPU-accelerated Three.js celestial neural lattice, rotating iridescent gyroscopes, wireframe crystals, autonomous camera glide, and deep space volumetric fog.
- **🌀 Spatial 3D Digital Twin & 4D Continuum**: Real-time 3D parcel inspection with rotating holographic warranty shields, real-time laser scan beams, and 4D Tesseract spacetime curvature.
- **🚚 Zero-Hallucination Order Tracking**: Direct SQLite integration querying carrier tracking numbers (`FX-9823411029`, `1Z9999999999999999`) with strict graceful fallbacks for missing orders.
- **⚡ FastMCP Standard Server**: Exposes core tools over standard Model Context Protocol (MCP) on a dedicated port for agent interoperability.

---

## 🏗️ Architecture & Data Flow

```
                     ┌──────────────────────────┐
                     │ Shopper Receipt Document │
                     │   (TXT, MD, CSV, POS)    │
                     └────────────┬─────────────┘
                                  │
                                  ▼
                     ┌──────────────────────────┐
                     │ Multi-Format Parser      │
                     │ (Unicode/Markdown/Regex) │
                     └────────────┬─────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
┌───────────────────────────┐                 ┌──────────────────────────┐
│   Per-Item Text Splitter  │                 │  Store Policy Splitter   │
│ (One chunk per line item) │                 │  (Categorized clauses)   │
└─────────────┬─────────────┘                 └────────────┬─────────────┘
              │                                            │
              └─────────────────────┬──────────────────────┘
                                    ▼
                     ┌──────────────────────────┐
                     │ Chroma Vector Store      │
                     │ (Scoped: receipt_{order})│
                     └──────────────┬───────────┘
                                    │
         ┌──────────────────────────┴──────────────────────────┐
         ▼                                                     ▼
┌─────────────────────────────────┐           ┌─────────────────────────────────┐
│ Deterministic Math Tool         │           │ Multi-Aspect Retriever          │
│ (purchase + policy - current)   │           │ (Item Chunks + Policy Clauses)  │
└────────────────┬────────────────┘           └────────────────┬────────────────┘
                 ▼                                             ▼
┌─────────────────────────────────┐           ┌─────────────────────────────────┐
│ Proactive Urgency Alert Banner  │           │ ReAct Autonomous Agent          │
│ (Triggered if < 7 days left)    │           │ (Groq openai/gpt-oss-120b)      │
└────────────────┬────────────────┘           └────────────────┬────────────────┘
                 │                                             │
                 └──────────────────────┬──────────────────────┘
                                        ▼
         ┌─────────────────────────────────────────────────────────────┐
         │                    DEPLOYMENT APPLICATION                   │
         │  Streamlit 3D Digital Twin Cockpit (Port 8501)              │
         └─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python**: Version `3.10`, `3.11`, or `3.12` installed.
- **Groq API Key**: Free API key from [Groq Console](https://console.groq.com/keys).
- **Ollama** (Local Embeddings):
  ```bash
  # Install Ollama from https://ollama.ai, then:
  ollama serve
  ollama pull all-minilm
  ```

### 2. Clone & Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/your-username/coreX.git
cd coreX

# Create and activate virtual environment
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy the example environment template
cp .env.example .env
```
Open `.env` and insert your Groq API key:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
STREAMLIT_PORT=8501
```

---

## 💻 Running the Applications

### 1. Streamlit 3D Digital Twin Cockpit (Port 8501)
```bash
streamlit run app.py
```
Open your browser at **`http://localhost:8501`**.
- Features 3D Spatial Digital Twin, 4D spacetime continuum, 5.6 Tera ChartGPT analytics, Google AI Overview search cockpit, and live receipt inspection.

### 2. FastMCP Standard Protocol Server
```bash
python src/mcp_server.py
```
- Starts the FastMCP server exposing `calculate_return_and_warranty_window` and `lookup_order_status` over standard MCP protocol.

---

## 🧪 Automated Pipeline Verification

Verify all 8 workshop stages end-to-end with the built-in test suite:

```bash
python test_pipeline.py
```

### Verification Matrix & Workshop Results:

| Stage | Requirement | Implementation | Status |
|---|---|---|:---:|
| **1. LLM Setup** | High-speed LLM connection | `ChatGroq(model="openai/gpt-oss-120b")` | ✅ **PASS** |
| **2. Document Loading** | Shopper receipt + store policy | Custom structured loaders in `src/loaders.py` | ✅ **PASS** |
| **3. Text Splitting** | One item per chunk + policy clauses | `src/splitters.py` chunking by product & section | ✅ **PASS** |
| **4. Vector Store** | Scoped Chroma DB persistence | Collection scoped to `receipt_{order_id}` | ✅ **PASS** |
| **5. Retriever** | Multi-aspect retrieval | Dual lookup for item records + matching policy | ✅ **PASS** |
| **6. Custom Tools** | Window calculator & order status lookup | `@tool` decorated with deterministic Python math | ✅ **PASS** |
| **7. Proactive Ingestion** | Pre-prompt urgency summary | Triggers on ingestion; flags windows `< 7 days` | ✅ **PASS** |
| **8. ReAct Agent** | Grounded QA & order lookup | Zero-hallucination agent with Google AI Overview | ✅ **PASS** |
| **Bonus Scope** | FastMCP Protocol Server | FastMCP standard server in `src/mcp_server.py` | ✅ **PASS** |

---

## 📂 Sample Evaluation Receipts

The repository includes 5 ready-to-test evaluation receipts located in [`data/sample_receipts/`](data/sample_receipts/):

1. **🚨 Sample 1 (`receipt_urgent_electronics.txt`)**:
   - Order `REC-2026-8891` (Sony Headphones & Anker Cable).
   - Purchased 2026-08-27 → Only **5 days left** to return!
   - Triggers the immediate red urgency banner.
2. **🧥 Sample 2 (`receipt_apparel_mixed.txt`)**:
   - Order `REC-2026-4421` (Patagonia Rain Jacket, Trail Running Shoes, Merino Socks).
   - 30-day apparel return window with active coverage.
3. **⏳ Sample 3 (`receipt_expiring_apparel.txt`)**:
   - Order `REC-2026-1102` (Wool Winter Coat).
   - Only **3 days left** to return! High priority alert.
4. **🧾 Sample 4 (`sample_shopkeeper_bill.txt`)**:
   - Shopkeeper mixed invoice (Tabish) with mixed tax lines and itemized billing.
5. **📑 Sample 5 (`corex_sample_receipt.txt`)**:
   - ABC Mart POS markdown table format invoice testing table parsing.

---

## 📁 Repository Structure

```
coreX/
├── .github/
│   ├── workflows/
│   │   └── ci.yml               # GitHub Actions CI pipeline
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md        # Issue template for bugs
│       └── feature_request.md   # Issue template for feature proposals
├── data/
│   ├── orders.db                # SQLite database for order status lookups
│   ├── orders_db.csv            # Source order records seed dataset
│   ├── policy/
│   │   └── store_policy.md      # CODEX retail return & warranty policies
│   └── sample_receipts/         # 5 pre-built evaluation sample receipts
├── src/
│   ├── agent.py                 # ReAct agent, Google AI Overview & ChartGPT brain
│   ├── components_3d.py         # Three.js 3D WebGL Digital Twin & Cinematic Background
│   ├── config.py                # Environment configuration & business logic thresholds
│   ├── loaders.py               # Robust receipt and policy loaders with LLM fallback
│   ├── mcp_server.py            # FastMCP server exposing tools over MCP protocol
│   ├── retriever.py             # Dual-aspect retriever for items + policy clauses
│   ├── splitters.py             # Custom per-item and policy section splitters
│   ├── tools.py                 # Deterministic window calculator & SQLite lookup tools
│   └── vectorstore.py           # Chroma vector store scoped to receipt order ID
├── app.py                       # Streamlit 3D Digital Twin Cockpit (Port 8501)
├── test_pipeline.py             # End-to-end workshop pipeline verification suite
├── requirements.txt             # Project dependencies
├── .env.example                 # Template for environment variables
├── .gitignore                   # Git exclusion rules (secrets, cache, DBs)
├── CONTRIBUTING.md               # Contribution guidelines
├── LICENSE                      # MIT License
└── README.md                    # Project documentation
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <b>Built with precision for Track 5: E-commerce / Retail Agentic RAG</b><br>
  <sub>Powered by Groq • LangChain • Ollama • Three.js • Streamlit</sub>
</div>
