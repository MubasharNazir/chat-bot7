from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.rag import router as rag_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(rag_router)
