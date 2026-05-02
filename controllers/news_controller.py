from fastapi import APIRouter, HTTPException
from typing import Optional
from pydantic import BaseModel
from services.news_service import NewsService
from repository.news_repository import NewsRepository
from utils.contants.status import Status
from utils.api_response import ApiResponse
from utils.exception.api_exception import ApiException
from utils.contants.error_code import ErrorCode

router = APIRouter()
news_service = NewsService()
news_repo = NewsRepository()

@router.get("/")
async def get_news(page: int = 0, size: int = 20, sort_by: str = "newest", sort_order: str = "desc"):
    data = news_repo.get_all(page=page, size=size, sort_by=sort_by, sort_order=sort_order)
    return ApiResponse.success(data)

@router.post("/refresh")
async def refresh_news(query: str = "trending", limit: int = 20):
    items = news_service.fetch(query=query, limit=limit)
    saved_ids = news_repo.save_all(items, status=Status.PENDING.code)
    news_repo.update_status(saved_ids, Status.ACTIVE.code)
    return ApiResponse.success({"message": f"Successfully refreshed {len(saved_ids)} news items.", "ids": saved_ids})

@router.get("/{news_id}")
async def get_news_by_id(news_id: int):
    news = news_repo.get_by_id(news_id)
    if not news:
        raise ApiException(ErrorCode.NOT_FOUND, message=f"News item with id {news_id} not found")
    return ApiResponse.success(news)

@router.delete("/{news_id}")
async def delete_news(news_id: int):
    news_repo.delete(news_id)
    return ApiResponse.success({"message": "News item deleted"})
