from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from services.meme_service import MemeService
from services.text_service import TextService
from services.image_generate_service import ImageGenerateService
from repository.news_repository import NewsRepository
from utils.api_response import ApiResponse
from utils.exception.api_exception import ApiException
from utils.contants.error_code import ErrorCode
import os

router = APIRouter()
meme_service = MemeService()
text_service = TextService()
image_service = ImageGenerateService()
news_repo = NewsRepository()

class MemeRequest(BaseModel):
    news_id: int
    top_text: Optional[str] = None
    bottom_text: Optional[str] = None

@router.post("/generate")
async def generate_meme(request: MemeRequest):
    news = news_repo.get_by_id(request.news_id)
    if not news:
        raise ApiException(ErrorCode.NOT_FOUND, message=f"News with id {request.news_id} not found")

    top = request.top_text
    bottom = request.bottom_text
    
    if not top or not bottom:
        prompt = f"Write a funny meme caption for this news: {news.title}"
        generated_text = text_service.generate(prompt)
        parts = generated_text.split("\n")
        top = top or parts[0]
        bottom = bottom or (parts[1] if len(parts) > 1 else "")

    image_path = "temp_image.png"
    # Generate image based on news title
    image_service.generate(f"A meme image for: {news.title}", output_path=image_path)

    output_path = f"assets/memes/meme_{request.news_id}.png"
    os.makedirs("assets/memes", exist_ok=True)
    
    final_path = meme_service.create_meme(image_path, top, bottom, output_path=output_path)
    
    return ApiResponse.success({
        "status": "success",
        "meme_url": f"/assets/memes/{os.path.basename(final_path)}",
        "top_text": top,
        "bottom_text": bottom
    })
