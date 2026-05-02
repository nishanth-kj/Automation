from fastapi import APIRouter
from pydantic import BaseModel
from services.ai_service import AiService
from utils.api_response import ApiResponse

router = APIRouter()
ai_service = AiService()

from models.requests.chat_request import ChatRequest

@router.post("/chat")
async def chat(request: ChatRequest):
    response_text = ai_service.chat(
        model=request.model,
        system_prompt=request.system_prompt,
        input_text=request.input
    )
    
    return ApiResponse.success({
        "model": request.model,
        "response": response_text
    })
