import chromadb
from llm_api_provider import embed_text
import os
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")

os.makedirs(CHROMA_PATH, exist_ok=True)
_chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _chroma_client.get_or_create_collection(name="epc_documents")



def add_chunks(chunks: list[dict]):
    """
    Embeds and stores a list of chunk dicts (from chunk_document())
    into ChromaDB.
    """
    ids = []
    texts = []
    metadatas = []
    embeddings = []

    for chunk in chunks:
        ids.append(chunk["chunk_id"])
        texts.append(chunk["text"])
        embeddings.append(embed_text(chunk["text"]))
        metadatas.append({
            "filename": chunk["filename"],
            "filetype": chunk["filetype"],
            "doc_type": chunk["doc_type"],
            "document_type": chunk["document_type"],
        })

    _collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search(query: str, n_results: int = 5, filter_document_type: str = None):
    """
    Embeds the query and finds the closest matching chunks.
    Optionally filter by document_type, e.g. "Vendor Submittal".
    """
    query_embedding = embed_text(query)

    where_filter = {"document_type": filter_document_type} if filter_document_type else None

    results = _collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where_filter,
    )

    matches = []
    for i in range(len(results["ids"][0])):
        matches.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],  # lower = more similar
        })
    return matches



def list_documents():
    """
    Groups all stored chunks by filename, returning one summary row per
    document instead of raw chunks. Powers GET /documents.
    """
    # Pull every chunk's metadata — cheap since we only need metadata, not embeddings
    all_data = _collection.get(include=["metadatas"])

    grouped = {}
    for metadata in all_data["metadatas"]:
        filename = metadata["filename"]
        if filename not in grouped:
            grouped[filename] = {
                "filename": filename,
                "document_type": metadata["document_type"],
                "filetype": metadata["filetype"],
                "chunk_count": 0,
            }
        grouped[filename]["chunk_count"] += 1

    return list(grouped.values())


def get_stats():
    """
    Aggregate counts for the dashboard's stat cards.
    Deliberately cheap — just summarizes list_documents(), no new queries.
    """
    documents = list_documents()
    total_documents = len(documents)
    total_chunks = sum(doc["chunk_count"] for doc in documents)

    return {
        "total_documents": total_documents,
        "total_chunks": total_chunks,
    }