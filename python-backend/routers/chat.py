
from fastapi import APIRouter
from models.chat_request import ChatRequest
from models.chat_response import ChatResponse
from core.handlers.chat_handler import handle_chat_request

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    return await handle_chat_request(req)