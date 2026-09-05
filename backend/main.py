from fastapi import FastAPI 
from fastapi import UploadFile , File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import ask_with_rag 
from compilance import run_compliance_check
from vector_store import add_chunks
from vector_store import search
from vector_store import _collection
from vector_store import list_documents, delete_document
from vector_store import get_stats
from chunker import chunk_document
from exctractors import extract_file
import os 
import shutil
from compilance import save_compliance_results , load_compliance_results


app = FastAPI(title="EPC Intelligence API")


FRONTEND_URL = os.getenv("FRONTEND_URL", "https://ep-cmind-chi.vercel.app/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}


class AskRequest(BaseModel):
    question : str
    document_type : str | None = None

@app.post("/ask")
def ask(req : AskRequest):
    chunks = search(req.question, filter_document_type = req.document_type)
    answer = ask_with_rag(req.question, filter_document_type = req.document_type)

    sources = [
        {
            "filename" : c["metadata"]["filename"],
            "document_type": c["metadata"]["document_type"],
            "text": c["text"],
            "distance": c["distance"],
        }
        for c in chunks
    ]
    return {"answer" : answer , "sources": sources}


@app.get("/documents")
def get_documents():
    return {"documents": list_documents()}


# upload mechanism
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.getenv(
    "UPLOAD_DIR",
    os.path.join(BASE_DIR, "uploaded_docs")
)

os.makedirs(UPLOAD_DIR, exist_ok=True)


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".xls", ".csv", ".txt", ".md"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB limit
@app.post("/upload")
def upload_document(file: UploadFile = File(...)):
    safe_filename = os.path.basename(file.filename)
    file_ext = os.path.splitext(safe_filename)[1].lower()

    if file_ext not in ALLOWED_EXTENSIONS:
        return {"status": "error", "message": f"File type '{file_ext}' not allowed."}

    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        return {"status": "error", "message": "File too large. Max size is 50 MB"}

    save_path = os.path.join(UPLOAD_DIR, safe_filename)

    with open(save_path, "wb") as f:
        f.write(content)
    # Run it through your existing pipeline — identical to what ingest.py does
    try:
        extracted = extract_file(save_path)
    except ValueError as e:
        return {"status": "error", "message": str(e)}

    chunks = chunk_document(extracted)

    if not chunks:
        return {"status": "error", "message": "No content could be extracted from this file."}

    add_chunks(chunks)

    return {
        "filename": file.filename,
        "document_type": chunks[0]["document_type"],
        "chunks_added": len(chunks),
        "status": "success",
    }

@app.delete("/documents/{filename}")
def remove_document(filename: str):
    safe_filename = os.path.basename(filename)

    # Remove from ChromaDB
    delete_document(safe_filename)

    # Remove from disk too
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    return {"status": "success", "message": f"{safe_filename} removed"}

@app.post("/compliance-check")
def compliance_check():
    results = run_compliance_check()
    data = save_compliance_results(results)
    return data  # {"results": [...], "ran_at": "..."}

@app.get("/compliance-check")
def get_last_compliance_check():
    return load_compliance_results()


@app.get("/stats")
def stats():
    doc_data = get_stats()
    compliance_data = load_compliance_results()
    deviations = sum(1 for r in compliance_data["results"] if r.get("status") == "Deviation")
    return {
        "total_documents": doc_data["total_documents"],
        "total_chunks": doc_data["total_chunks"],
        "deviations_found": deviations,
    }
