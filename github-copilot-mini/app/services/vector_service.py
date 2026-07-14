"""
Vector Service (RAG - Retrieval Augmented Generation)
------------------------------------------------------
Idea: Poora codebase LLM ke context window mein nahi bhej sakte (bahut bada hota hai).
Isliye:
1. Codebase ko chunks (functions/files) mein todte hain
2. Har chunk ka "embedding" (vector) banate hain
3. Chroma DB mein store karte hain
4. Jab user query kare, sirf "relevant" chunks retrieve karke LLM ko dete hain

Isse LLM ko codebase ka context milta hai without overloading it.
"""

import chromadb
from app.services.llm_service import get_embedding

# Local persistent vector DB (production mein Pinecone/Weaviate bhi use kar sakte ho)
chroma_client = chromadb.PersistentClient(path="./chroma_store")
collection = chroma_client.get_or_create_collection(name="codebase")


def add_code_chunk(chunk_id: str, code_text: str, metadata: dict = None):
    """
    Ek code chunk (e.g. ek function ya file) ko Vector DB mein store karta hai.
    chunk_id -> unique identifier (e.g. "utils.py::calculate_total")
    """
    embedding = get_embedding(code_text)
    collection.add(
        ids=[chunk_id],
        embeddings=[embedding],
        documents=[code_text],
        metadatas=[metadata or {}],
    )


def search_similar_chunks(query: str, top_k: int = 3) -> list[str]:
    """
    Query se milte-julte code chunks dhoondhta hai (semantic similarity se).
    Ye chunks phir LLM ko "context" ke roop mein diye jaate hain.
    """
    query_embedding = get_embedding(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    documents = results.get("documents", [[]])[0]
    return documents


def build_context_from_query(query: str) -> str:
    """
    Helper: query ke relevant chunks nikalke ek single context string banata hai,
    jo prompt mein daala ja sake.
    """
    chunks = search_similar_chunks(query)
    if not chunks:
        return ""
    return "\n\n---\n\n".join(chunks)
