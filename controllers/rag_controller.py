from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rag_service import RagService
from typing import List, Dict, Any
from utils.api_response import ApiResponse
from utils.exception.api_exception import ApiException
from utils.contants.error_code import ErrorCode

router = APIRouter()
rag_service = RagService()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

@router.post("/search")
async def search_news(request: SearchRequest):
    results = rag_service.search(request.query, top_k=request.top_k)
    data = [
        {
            "score": float(res[0]),
            "news_id": res[1]["news_id"],
            "title": res[1]["title"],
            "source": res[1]["source"]
        }
        for res in results
    ]
    return ApiResponse.success(data)

@router.post("/index/build")
async def build_index():
    count = rag_service.build_index()
    return ApiResponse.success({"message": f"Successfully indexed {count} news items."})
