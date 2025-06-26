from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.auth import get_current_user
from app.core.firestore import add_message, get_chat_history
from app.core.gemini import chat_with_gemini

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat(request: ChatRequest, user: dict = Depends(get_current_user)):
    user_id = user["uid"]
    # Store user message
    add_message(user_id, request.message, is_user=True)
    # Get chat history
    history = get_chat_history(user_id)
    # Get Gemini response
    response = chat_with_gemini(request.message, history)
    # Store model response
    add_message(user_id, response, is_user=False)
    return {"response": response} 