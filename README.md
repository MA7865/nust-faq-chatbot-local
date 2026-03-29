# NUST FAQ Chatbot — Local Chatbot Competition 2026

A fully **offline** admissions assistant for NUST, built for the Local Chatbot Competition 2026 under the direction of **Dr. Sohail Iqbal**.

Answers student questions about admissions, MBBS, fees, scholarships, and university policies — with zero internet dependency.

---

## How it works

```
User query
    ↓
Spell correction  (SymSpell — custom NUST dictionary)
    ↓
Semantic search   (Sentence Transformers + FAISS)
    ↓
LLM answer        (Qwen 1.5B — quantized GGUF, CPU only)
    ↓
Browser UI
```

---

## Project structure

```
nust-faq-chatbot-local/
├── app.py                  ← Start here
├── chat.html               ← Browser UI
├── requirements.txt
├── setup.bat               ← Windows one-click setup
├── data/
│   ├── faqs.json           ← 73 official NUST FAQs
│   └── smalltalk.json      ← Greeting / meta responses
├── models/
│   └── qwen.gguf           ← Quantized LLM (download from releases)
├── src/
│   ├── chatbot.py          ← RAG pipeline + LLM call
│   ├── embed_and_search.py ← FAISS index + semantic search
│   └── spell_corrector.py  ← SymSpell spell correction
```

---

## Running the chatbot

### Prerequisites
- Download the Qwen model from [GitHub Releases](https://github.com/MA7865/nust-faq-chatbot-local/releases) and place it in `models/qwen.gguf`.
- create a models folder in nust-faq-chatbot-local folder and move the qwen.gguf file in it
### Option A — One-Click Setup (Windows)

```powershell
# Run the setup script (creates venv and installs dependencies)
setup.bat

# Activate virtual environment
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / Mac

# Start the server (browser opens automatically)
python app.py
```

### Option B — Manual Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / Mac

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

Once running, open **http://localhost:5000** in your browser.  
Press `Ctrl+C` to stop the server.

---

## Hardware requirements

| Spec | Minimum |
|------|---------|
| RAM | 4 GB (8 GB recommended) |
| CPU | Any modern CPU (i5 13th Gen or below is fine) |
| GPU | Not required |
| OS  | Windows 10/11 |
| Python | 3.10 or higher |

---

## Constraints met

- ✅ 100% offline — no internet, no API calls, no remote fallback
- ✅ Runs on CPU only, no GPU required
- ✅ Works within 8 GB RAM
- ✅ Single command to launch
- ✅ Ships fully through this repository

---

## Model Download
The Qwen model is too large for direct Git storage. Download it from [GitHub Releases](https://github.com/MA7865/nust-faq-chatbot-local/releases) and place it in `models/qwen.gguf`.

```bash
git lfs install
git lfs pull
```

---

## Known limitations

- Answers are strictly based on the 73 official NUST FAQs — the bot will say so if a question is out of scope.
- First startup takes ~5–10 seconds while the model and FAISS index load.
- Response time is ~2–6 seconds on an i5 CPU (no GPU).

---

## 🚀 Technical Workflow & Stack

**Workflow:**
1. **User Query** (via browser or CLI)
2. **Spell Correction**: All queries are corrected using SymSpell with a custom NUST dictionary, handling typos and student slang.
3. **Normalization**: Queries are lowercased, punctuation removed, and split for multi-part questions.
4. **Semantic Search**: Sentence Transformers (MiniLM) embed the query, and FAISS finds the most relevant NUST FAQ(s) using vector similarity.
5. **LLM Answer**: Qwen-1.5B (quantized, CPU-only) generates a concise answer, strictly using only the retrieved FAQ context.
6. **Smalltalk**: Friendly responses for greetings, thanks, and meta-questions.
7. **Web UI**: Flask serves a modern, responsive chat interface.

**Stack:**
- **Python 3.10+**
- **Flask** (API + static web server)
- **llama-cpp-python** (Qwen LLM, local inference)
- **sentence-transformers** (MiniLM for embeddings)
- **faiss-cpu** (vector search)
- **symspellpy** (spell correction)
- **HTML/CSS/JS** (chat.html for UI)
- **Git LFS** (for model file)
- **No internet required** (fully offline, all data and models local)

---

## ⚙️ Engineering Choices & Tradeoffs

- **Offline-First**: No API calls, no cloud dependencies. All data, models, and logic run locally for privacy, speed, and reliability.
- **Strict RAG Pipeline**: The LLM is forced to answer only from the FAQ context, preventing hallucinations and ensuring trustworthiness.
- **Custom Spell Correction**: SymSpell is seeded with NUST-specific terms, so even misspelled queries about "mbbs", "nshs", or "mdcat" are understood.
- **Semantic Search**: FAISS + MiniLM enables robust matching for natural language queries, not just keyword search.
- **Multi-Question Handling**: Queries with "and", ",", or "?" are split and answered separately, then combined for the user.
- **Smalltalk Layer**: Friendly, pre-defined responses for greetings and meta-questions, making the bot approachable.
- **Web UI**: Modern, responsive, and easy to use for students on any device.
- **Model Size**: Qwen-1.5B is small enough to run on 4–8GB RAM, but large enough for high-quality answers. (Tradeoff: not as powerful as cloud LLMs, but 100% private and free.)

---

## 🛡️ Why Students Can Trust This Chatbot

- **Official Data Only**: All answers are strictly based on the 73 official NUST FAQs, with no hallucinated or made-up information.
- **No Hallucinations**: The LLM is forced to answer only from the provided context. If the answer isn't in the FAQs, the bot says so.
- **Transparent**: Links to official NUST pages are provided where appropriate.
- **Privacy**: No data ever leaves your computer. No tracking, no analytics, no cloud.
- **Open Source**: All code, data, and models are available for inspection and improvement.
- **Battle-Tested**: Handles typos, slang, and multi-part questions. Friendly for both casual and formal queries.

---

## 📚 Example Test FAQs (for Demo/Validation)

Try these queries to check the bot's features:

### 1. **Spell Correction**
- `what is the fee strcutre for mbbs?`
- `can i aply for bshnd with pre medical?`
- `is there any scholaship avaiable?`

### 2. **Multi-Question Handling**
- `where is nshs and what is the fee for mbbs?`
- `is there any quota and what is the age limit?`
- `can i migrate to nust, what is the process?`

### 3. **Smalltalk & Meta**
- `hi there!`
- `what can you do?`
- `thanks!`

### 4. **Strict FAQ Scope**
- `what are the scholarships in usa?`
- `tell me about harvard university`  

### 5. **Typos & Slang**
- `wht r the test venews?`
- `admissin critria for gap yr canddates?`

### 6. **Links & Official Info**
- `what is the fee structure?`
- `what are the salient features of UG Admissions at NUST?`

### 7. **Edge Cases**
- `is there any negative marking in the entry test?`
- `who is exempted from payment of net application processing fees?`

---

*See the full FAQ list in `data/faqs.json` for more.*

---

*Local Chatbot Competition 2026 · NUST Islamabad*
