import firebase_admin
from firebase_admin import firestore
from datetime import datetime

db = firestore.client()

CHAT_COLLECTION = "chat_history"

def add_message(user_id: str, message: str, is_user: bool):
    doc_ref = db.collection(CHAT_COLLECTION).document()
    doc_ref.set({
        "user_id": user_id,
        "message": message,
        "is_user": is_user,
        "timestamp": datetime.utcnow()
    })

def get_chat_history(user_id: str):
    messages = (
        db.collection(CHAT_COLLECTION)
        .where("user_id", "==", user_id)
        .order_by("timestamp")
        .stream()
    )
    return [{"message": m.get("message"), "is_user": m.get("is_user")} for m in messages] 