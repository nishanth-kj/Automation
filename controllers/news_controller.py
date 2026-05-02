from fastapi import APIRouter, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from services.news_service import NewsService
from utils.api_response import ApiResponse
from utils.exception.api_exception import ApiException
from utils.contants.error_code import ErrorCode
from utils.websocket_manager import manager

router = APIRouter()
news_service = NewsService()

@router.websocket("/ws/scraper")
async def websocket_scraper(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.post("/list")
async def get_news(page: int = 0, size: int = 20, sort_by: str = "newest", sort_order: str = "desc"):
    # Controller -> Service only
    data = news_service.get_all(page=page, size=size, sort_by=sort_by, sort_order=sort_order)
    return ApiResponse.success(data)

@router.post("/refresh")
async def refresh_news(background_tasks: BackgroundTasks, query: str = "trending", limit: int = 20):
    # Controller -> Service only
    background_tasks.add_task(news_service.run_background_scraper, query, limit)
    return ApiResponse.success({"message": "Scraper started in background"})

@router.post("/detail/{news_id}")
async def get_news_by_id(news_id: int):
    # Controller -> Service only
    news = news_service.get_by_id(news_id)
    if not news:
        raise ApiException(ErrorCode.NOT_FOUND, message=f"News item with id {news_id} not found")
    return ApiResponse.success(news)

@router.delete("/{news_id}")
async def delete_news(news_id: int):
    # Controller -> Service only
    news_service.delete(news_id)
    return ApiResponse.success({"message": "News item deleted"})
