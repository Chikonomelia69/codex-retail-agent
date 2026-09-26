# Contributing to CODEX

Thank you for your interest in contributing to **CODEX: Order & Warranty Agent**! We welcome bug reports, feature suggestions, documentation enhancements, and pull requests.

---

## 🛠️ Development Setup

### 1. Fork & Clone
```bash
git clone https://github.com/your-username/coreX.git
cd coreX
```

### 2. Set Up Virtual Environment
```bash
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
cp .env.example .env
```
Edit `.env` to supply your Groq API key:
```env
GROQ_API_KEY=gsk_...
GROQ_MODEL=openai/gpt-oss-120b
```

### 5. Start Ollama (for Embeddings)
Ensure Ollama is installed and running with `all-minilm`:
```bash
ollama serve
ollama pull all-minilm
```

---

## 🧪 Testing Your Changes

Before submitting any code, verify that all 8 workshop pipeline stages pass without error:

```bash
python test_pipeline.py
```

All 8 stages must output `[PASS]` and conclude with:
`[SUCCESS] ALL WORKSHOP PIPELINE STAGES VERIFIED SUCCESSFULLY!`

### Manual UI Verification
1. **Launch Streamlit 3D Twin Cockpit (Port 8501):**
   ```bash
   streamlit run app.py
   ```
2. Test receipt uploads, sample quick-loader buttons, 5.6 Tera ChartGPT analytics, 3D/4D visual studio, and Google AI Overview queries.

---

## 🔀 Pull Request Process

1. **Create a branch** for your work:
   ```bash
   git checkout -b feature/amazing-new-feature
   ```
2. **Make your changes** following PEP 8 coding standards for Python and semantic formatting for HTML/JS.
3. **Never commit secrets**: Verify that `.env` is never added to git commits.
4. **Commit with descriptive messages**:
   ```bash
   git commit -m "feat(agent): add support for multi-currency return calculations"
   ```
5. **Push and open a Pull Request** against `main`. Provide a clear summary of what was added or fixed and attach verification test logs.

---

## 📜 Code of Conduct
Please be respectful, collaborative, and considerate in all interactions within this project.
