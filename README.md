# EPCmind

**AI-powered Industrial Knowledge Intelligence** — a RAG-based assistant that ingests EPC (Engineering, Procurement, Construction) project documents and lets you query them in natural language, with source citations, confidence scoring, and automated compliance checking.
---

## 🎯 What it does

Industrial and EPC projects generate huge volumes of scattered documents — specifications, vendor submittals, procurement schedules, RFIs, inspection reports. Engineers routinely lose hours hunting for a single answer buried across formats. EPCmind fixes this by turning your document set into a queryable knowledge base:

- **Ask anything** about your uploaded documents in plain English and get a grounded answer with citations
- **Compliance Check** automatically compares your latest Specification against the latest Vendor Submittal and flags deviations
- **Multi-format ingestion** — PDF, DOCX, XLSX, XLS, CSV, TXT, MD

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **RAG-powered Q&A** | Ask natural-language questions across all your ingested documents |
| 📎 **Source citations** | Every answer links back to the exact document and chunk it came from |
| 🟢 **Confidence badges** | High / Medium / Low confidence tags based on retrieval similarity |
| 🚫 **Honest "no match" handling** | If the documents don't contain the answer, the UI says so clearly instead of showing misleading sources |
| ✅ **Automated compliance check** | Compares the latest Spec vs. Vendor Submittal and flags Match / Deviation / Cannot Verify per requirement |
| 🔐 **Per-user data isolation** | Each browser session has its own private document set — no cross-user data leakage |
| 💬 **Persistent chat history** | Conversations survive page reloads (stored locally in-browser) |
| 📊 **Live stats dashboard** | Total documents, chunks indexed, and deviations found at a glance |
| 🎨 **Markdown-formatted responses** | AI answers render with proper formatting — bold, lists, headings |
| 🧩 **Smart upload feedback** | Step-by-step processing indicator (extracting → chunking → embedding → indexing) |

---

## 🏗️ Architecture

```
                     ┌─────────────────────┐
   Upload Document → │  FastAPI Backend     │
   (PDF/DOCX/XLSX)    │  ─────────────────   │
                     │  1. Extract text     │
                     │  2. Chunk + classify │
                     │  3. Embed (Gemini)   │
                     │  4. Store in ChromaDB│──── session-tagged
                     └──────────┬───────────┘     (per-user isolation)
                                │
   Ask Question →   ┌──────────▼───────────┐
                     │  Vector Search        │
                     │  (session-filtered)   │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼───────────┐
                     │  Gemini 2.5 Flash     │
                     │  (grounded answer +   │
                     │   source citations)   │
                     └──────────┬───────────┘
                                │
                     ┌──────────▼───────────┐
                     │  React Dashboard      │
                     │  (chat UI, confidence,│
                     │   compliance report)  │
                     └───────────────────────┘
```

---

## 🛠️ Tech Stack

**Backend**
- Python, FastAPI
- ChromaDB (vector store)
- Google Gemini 2.5 Flash (embeddings + generation)
- PyMuPDF / python-docx / openpyxl (document extraction)

**Frontend**
- React + Vite
- Tailwind CSS
- GSAP (animations)
- react-markdown

**Deployment**
- Docker
- Google Cloud Run

---

## 🔐 Security & Data Handling

- Uploaded filenames are sanitized to prevent path-traversal
- File type is validated against an allowlist before saving
- Uploads are capped at 20 MB
- CORS is restricted to known frontend origins
- Each browser session gets an isolated view of documents via a secure, HttpOnly session cookie — no login required, no cross-user data leakage
- Security headers (CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy) are set on all responses

> **Known limitation:** Session isolation is cookie-based rather than account-based — clearing browser data resets a user's document history. This is an intentional trade-off for a frictionless, no-signup demo experience.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- A Google AI Studio API key (Gemini)

### Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt

# Create a .env file with:
# GEMINI_API_KEY=your_key_here

uvicorn main:app --reload
```
Backend runs at `http://localhost:8000`

### Frontend setup

```bash
cd Dashboard
npm install
npm run dev
```
Frontend runs at `http://localhost:5173`

---

## 📖 Usage

1. Open the app and upload your project documents (specs, submittals, schedules, RFIs)
2. Go to **Ask Documents** and ask a question — e.g. *"What is the battery autonomy requirement?"*
3. Go to **Compliance Check** to auto-compare your latest Specification against your latest Vendor Submittal
4. Check the **Dashboard** for a live count of indexed documents and flagged deviations

---

## 📌 Roadmap / Future Scope

- Account-based authentication for persistent, cross-device sessions
- Knowledge graph visualization of entities across documents
- Server-side chat history storage
- Multi-project / multi-tenant support
