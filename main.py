from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import news_controller, meme_controller, rag_controller, ai_controller, chat_controller
from utils.exception.api_exception import ApiException
from utils.api_response import ApiResponse
from utils.contants.error_code import ErrorCode
from fastapi import Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import List

from utils.websocket_manager import manager
from repository.database.init_db import init_db

app = FastAPI(
    title="AI News Meme Studio API",
    description="Backend API for managing news, generating memes, and RAG operations.",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    try:
        init_db()
    except Exception as e:
        print(f"Error initializing database: {e}")

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(news_controller.router, prefix="/api/news", tags=["News"])
app.include_router(meme_controller.router, prefix="/api/meme", tags=["Meme"])
app.include_router(rag_controller.router, prefix="/api/rag", tags=["RAG"])
app.include_router(ai_controller.router, prefix="/api/ai", tags=["AI"])
app.include_router(chat_controller.router, prefix="/api/v1", tags=["Chat"])

@app.exception_handler(ApiException)
async def api_exception_handler(request: Request, exc: ApiException):
    return JSONResponse(
        status_code=400,
        content=ApiResponse.fail(
            error_code=exc.error_code,
            message=exc.message,
            field=exc.fields
        ).model_dump()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ApiResponse.fail(
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=str(exc)
        ).model_dump()
    )


@app.websocket("/ws/scraper")
async def websocket_scraper(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "Welcome to AI News Meme Studio API", "status": "online"}
