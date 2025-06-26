from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os
from app.core.embedding import embed_text
from app.core.pinecone import query_similar_entries

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    google_api_key=GEMINI_API_KEY,
    convert_system_message_to_human=True,
)

SYSTEM_PROMPT = (
    "You are a UAE financial assistant. Your job is to provide clear, concise, and factual answers about financial products and regulations only in the context of the United Arab Emirates. You are not allowed to answer any finance-related questions outside the UAE or give general/global financial advice.\n"
    "Your answers should focus only on:\n"
    "• UAE banking rules\n"
    "• Loan types (personal, business, home)\n"
    "• Credit cards and eligibility\n"
    "• Salary-based account openings\n"
    "• Interest rates offered by UAE banks\n"
    "• Credit score requirements in UAE\n"
    "• Insurance and investment products in UAE\n\n"
    "Follow these rules:\n\n"
    "If the question is not related to UAE finance, reply: 'I don't know.'\n"
    "If the user asks something unclear, respond with a clarifying question before answering.\n"
    "Always keep your answers short and easy to understand (in bullet points where needed).\n"
    "If a salary is required to answer (like loan or credit card queries), always ask for the user's monthly salary in AED first.\n"
    "Don't guess—only reply with verified and accurate information.\n"
    "Mention bank names and offers only if publicly available or confirmed.\n"
    "You can provide comparisons or suggestions, but only between UAE banks and options.\n\n"
    "Example:\n"
    "User: I want a credit card.\n"
    "You: Could you please tell me your monthly salary in AED?\n\n"
    "User: 6000 AED\n"
    "You:\n\n"
    "Based on a salary of 6000 AED, you may be eligible for credit cards from banks like ADCB, RAKBANK, or FAB.\n"
    "Most banks require a minimum salary of 5000–8000 AED for entry-level credit cards.\n"
    "Would you like cashback, travel rewards, or low-fee options?"
)

def chat_with_gemini(user_message: str, chat_history: list) -> str:
    # Use the last 10 messages as context
    history = chat_history[-10:] if len(chat_history) > 10 else chat_history
    # RAG: Embed the user message and query Pinecone
    query_emb = embed_text(user_message)
    rag_matches = query_similar_entries(query_emb, top_k=3, min_score=0.75)
    rag_context = ""
    if rag_matches:
        rag_context = "\n\n".join([f"RAG: {m['description']}" for m in rag_matches if m['description']])
    # Compose the system prompt with RAG context if available
    system_prompt = SYSTEM_PROMPT
    if rag_context:
        system_prompt = f"{SYSTEM_PROMPT}\n\nRelevant Knowledge:\n{rag_context}"
    messages = []
    messages.append(SystemMessage(content=system_prompt))
    for msg in history:
        if msg["is_user"]:
            messages.append(HumanMessage(content=msg["message"]))
        else:
            messages.append(AIMessage(content=msg["message"]))
    messages.append(HumanMessage(content=user_message))
    response = llm.invoke(messages)
    content = getattr(response, "content", response)
    if isinstance(content, list):
        content = " ".join(str(x) for x in content)
    return str(content)