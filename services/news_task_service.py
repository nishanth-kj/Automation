from PySide6.QtCore import QThread, Signal
from repository.news_repository import NewsRepository
from utils.contants.status import Status
from utils.logger import logger

class NewsRefreshWorker(QThread):
    finished = Signal()
    error = Signal(str)

    def __init__(self, news_service, query="trending", limit=20):
        super().__init__()
        self.news_service = news_service
        self.query = query
        self.limit = limit
        self.news_repo = NewsRepository()

    def run(self):
        try:
            logger.info(f"Starting async news refresh for query: {self.query}")
            
            # 1. Fetch news
            news_items = self.news_service.fetch(self.query, self.limit)
            
            # 2. Save with PENDING status
            news_ids = self.news_repo.save_all(news_items, status=Status.PENDING.code)
            logger.info(f"Saved {len(news_ids)} items with PENDING status")
            
            # 3. Mark as ACTIVE
            self.news_repo.update_status(news_ids, Status.ACTIVE.code)
            logger.info("Updated status to ACTIVE for new items")
            
            self.finished.emit()
        except Exception as e:
            logger.error(f"News refresh failed: {str(e)}")
            self.error.emit(str(e))
