from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.rag_firestore import (
    create_rag_entry, list_rag_entries, update_rag_entry, delete_rag_entry
)
from app.core.pinecone import upsert_embedding, delete_embedding
from app.core.embedding import embed_text

router = APIRouter(prefix="/rag", tags=["rag"])

class RAGEntryRequest(BaseModel):
    topic: str
    description: str

@router.post("/")
def create_rag(request: RAGEntryRequest):
    entry_id = create_rag_entry(request.topic, request.description)
    embedding = embed_text(request.description)
    upsert_embedding(entry_id, embedding)
    return {"id": entry_id, "message": "RAG entry created"}

@router.get("/")
def list_rag():
    return list_rag_entries()

@router.put("/{entry_id}")
def update_rag(entry_id: str, request: RAGEntryRequest):
    update_rag_entry(entry_id, request.topic, request.description)
    embedding = embed_text(request.description)
    upsert_embedding(entry_id, embedding)
    return {"id": entry_id, "message": "RAG entry updated"}

@router.delete("/{entry_id}")
def delete_rag(entry_id: str):
    delete_rag_entry(entry_id)
    delete_embedding(entry_id)
    return {"id": entry_id, "message": "RAG entry deleted"} 