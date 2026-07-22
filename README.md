# EPCmind - AI-Powered EPC Project Intelligence

An intelligent document processing platform that extracts and analyzes EPC (Engineering, Procurement, and Construction) project documents using Google Gemini AI.

## 🎯 What is EPCmind?

EPCmind automates the analysis of construction project documents (PDFs, Word docs, Excel sheets, etc.) by:
- Extracting text from multiple document formats
- Processing documents intelligently with AI
- Providing insights for EPC project management
- Supporting data centre construction projects

## 📂 Project Structure

```
EPCmind/
├── backend/
│   ├── exctractor.py           # Document extraction engine
│   ├── docRead.py              # Batch document processor
│   ├── llm_api_provider.py     # Google Gemini AI integration
│   ├── chunker.py              # Document chunking (coming soon)
│   └── Sample_docs/            # Sample documents
├── frontend/
│   └── frontend.txt            # Frontend (coming soon)
├── .gitignore
└── README.md
```

## 🔧 Backend Modules

### 1. **exctractor.py** - Document Extraction Engine

Extracts text from multiple document formats:

**Supported Formats:**
- 📄 **PDF** - Page-by-page extraction
- 📝 **DOCX (Word)** - Paragraphs and tables
- 📊 **Excel (XLSX, XLS)** - Row-by-row data
- 📋 **CSV** - Tabular data
- 📃 **TXT/MD** - Plain text

**Main Function:**
```python
extract_file(path)
```

**Returns:**
```python
{
    "filename": "document.pdf",
    "filetype": ".pdf",
    "doc_type": "unstructured",  # or "structured"
    "text": "extracted text content..."
}
```

**Functions:**
- `extract_docx(path)` - Extract from Word documents
- `extract_pdf(path)` - Extract from PDF files
- `extract_txt(path)` - Read text files
- `extract_excel(path)` - Parse Excel/CSV files
- `iter_block_items(parent)` - Iterate document blocks

---

### 2. **llm_api_provider.py** - AI Integration

Centralized Google Gemini API integration for AI-powered analysis.

**Configuration:**
- Model: `gemini-2.5-flash` (default) or `gemini-2.5-pro`
- API Key: From `.env` file

**Main Function:**
```python
ask_ai(prompt: str) -> str
```

**Usage:**
```python
from llm_api_provider import ask_ai

response = ask_ai("Your analysis prompt here")
print(response)
```

---

### 3. **docRead.py** - Batch Document Processor

Processes all documents in the `Sample_docs` folder and displays extracted text preview.

**Usage:**
```bash
python docRead.py
```

**Output:**
```
=== document.pdf (unstructured) ===
extracted text preview...

=== spreadsheet.xlsx (structured) ===
row 1 data...
```

---

### 4. **chunker.py** - Document Chunking (Coming Soon)

Will implement semantic chunking for RAG (Retrieval-Augmented Generation) pipeline.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Google Gemini API key

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/shubhamsaini-commits/EPCmind.git
cd EPCmind
```

2. **Create virtual environment:**
```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install python-docx pypdf pandas google-genai python-dotenv
```

4. **Set up API key:**
Create a `.env` file in the `backend/` folder:
```
API_KEY=your_google_gemini_api_key_here
```

### Run the Project

**Process sample documents:**
```bash
cd backend
python docRead.py
```

---

## 💡 Usage Examples

### Example 1: Extract a Single Document
```python
from exctractor import extract_file

# Extract any supported document
result = extract_file("path/to/file.pdf")

print(result['filename'])     # "file.pdf"
print(result['doc_type'])     # "unstructured"
print(result['text'][:500])   # First 500 characters
```

### Example 2: Analyze with AI
```python
from llm_api_provider import ask_ai

prompt = "Analyze this EPC document for compliance issues: {text}"
analysis = ask_ai(prompt)
print(analysis)
```

### Example 3: Complete Pipeline
```python
from exctractor import extract_file
from llm_api_provider import ask_ai

# Step 1: Extract document
doc = extract_file("specification.pdf")

# Step 2: Prepare analysis prompt
analysis_prompt = f"""
Review this document:
{doc['text']}

Provide:
1. Main topics
2. Key requirements
3. Risk areas
"""

# Step 3: Get AI insights
insights = ask_ai(analysis_prompt)
print(insights)
```

---

## 📦 Dependencies

```
python-docx>=0.8.11     # DOCX files
pypdf>=4.0.0            # PDF extraction
pandas>=1.5.0           # Excel/CSV files
google-genai>=0.3.0     # Google Gemini API
python-dotenv>=1.0.0    # Environment variables
```

**Install all at once:**
```bash
pip install -r requirements.txt
```

---

## 🔐 Security Notes

⚠️ **Important:**
- Never commit your `.env` file (already in `.gitignore`)
- Keep your API key secret
- Don't share your `.env` file
- Rotate API keys regularly

---

## 📝 How It Works

```
Input Document (PDF, DOCX, Excel, etc.)
         ↓
    exctractor.py
         ↓
  Normalized Text + Metadata
         ↓
   llm_api_provider.py
         ↓
   Google Gemini AI Analysis
         ↓
    Intelligent Insights
```

---

## 🎯 Future Features

- [ ] Document chunking for RAG
- [ ] Specification compliance checking
- [ ] Schedule risk prediction
- [ ] Procurement validation
- [ ] Quality assurance automation
- [ ] Frontend UI
- [ ] REST API endpoints
- [ ] Database integration
- [ ] User authentication

---

## 📄 Supported File Types

| Format | Type | Status |
|--------|------|--------|
| `.pdf` | Unstructured | ✅ Working |
| `.docx` | Unstructured | ✅ Working |
| `.txt` | Unstructured | ✅ Working |
| `.md` | Unstructured | ✅ Working |
| `.xlsx` | Structured | ✅ Working |
| `.xls` | Structured | ✅ Working |
| `.csv` | Structured | ✅ Working |

---






