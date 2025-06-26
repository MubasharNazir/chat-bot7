import uuid
from firebase_admin import firestore

db = firestore.client()
COLLECTION = "rag_entries"

def create_rag_entry(topic: str, description: str) -> str:
    entry_id = str(uuid.uuid4())
    db.collection(COLLECTION).document(entry_id).set({
        "topic": topic,
        "description": description
    })
    return entry_id

def list_rag_entries():
    docs = db.collection(COLLECTION).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]

def update_rag_entry(entry_id: str, topic: str, description: str):
    db.collection(COLLECTION).document(entry_id).update({
        "topic": topic,
        "description": description
    })

def delete_rag_entry(entry_id: str):
    db.collection(COLLECTION).document(entry_id).delete() 