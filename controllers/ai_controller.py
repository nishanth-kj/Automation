from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_service import AiService
from utils.api_response import ApiResponse
from utils.exception.api_exception import ApiException
from utils.contants.error_code import ErrorCode

from typing import Optional

router = APIRouter()
ai_service = AiService()

class AiRequest(BaseModel):
    prompt: str
    system_prompt: Optional[str] = "You are a helpful AI assistant."

@router.post("/generate")
async def generate_text(request: AiRequest):
    result = ai_service.generate(
        system_prompt=request.system_prompt,
        user_input=request.prompt
    )
    return ApiResponse.success({"result": result})
