from fastapi import APIRouter
from services.ai_service import AiService
from utils.api_response import ApiResponse

router = APIRouter()
ai_service = AiService()

@router.post("/models")
async def list_models():
    models = ai_service.list_models()
    return ApiResponse.success({"models": models})
