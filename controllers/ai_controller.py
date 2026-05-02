from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ai_service import AiService
from utils.api_response import ApiResponse
from utils.exception.api_exception import ApiException
from utils.contants.error_code import ErrorCode

router = APIRouter()
# We might want to lazy load this since it's heavy, but for now we'll initialize it
# ai_service = AiService() 

class AiRequest(BaseModel):
    prompt: str

@router.post("/generate")
async def generate_text(request: AiRequest):
    # Initialize service inside if not global to avoid memory overhead if not used
    from services.ai_service import AiService
    ai_service = AiService()
    result = ai_service.generate(request.prompt)
    return ApiResponse.success({"result": result})
