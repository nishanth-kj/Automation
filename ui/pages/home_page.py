from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QLabel, QHBoxLayout, QComboBox
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebSockets import QWebSocket
from ui.components.news_card import NewsCard
from repository.news_repository import NewsRepository
from services.news_task_service import NewsRefreshWorker
from utils.logger import logger
import json

class HomePage(QWidget):
    def __init__(self, news_service, open_news_callback, ws_service):
        super().__init__()

        self.news_service = news_service
        self.open_news_callback = open_news_callback
        self.ws_service = ws_service
        self.news_repo = NewsRepository()
        
        self.current_page = 0
        self.limit = 10
        self.sort_by = "newest"

        # WebSocket Client
        self.client = QWebSocket()
        self.client.textMessageReceived.connect(self.on_ws_message)
        self.client.open(QUrl("ws://localhost:8765"))

        main_layout = QVBoxLayout()
        
        # Header with Sort
        header = QHBoxLayout()
        header.addWidget(QLabel("Trending News"))
        header.addStretch()
        
        self.sort_box = QComboBox()
        self.sort_box.addItems(["Newest", "Source"])
        self.sort_box.currentTextChanged.connect(self.on_sort_changed)
        header.addWidget(QLabel("Sort by:"))
        header.addWidget(self.sort_box)
        
        main_layout.addLayout(header)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.news_layout = QVBoxLayout(self.scroll_content)
        self.news_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)

        # Footer with Load More
        footer = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh from Web")
        self.refresh_btn.clicked.connect(self.refresh_from_web)
        
        self.load_more_btn = QPushButton("Load More")
        self.load_more_btn.clicked.connect(self.load_more)
        
        footer.addWidget(self.refresh_btn)
        footer.addStretch()
        footer.addWidget(self.load_more_btn)
        main_layout.addLayout(footer)

        self.setLayout(main_layout)
        
        # Initial load from DB
        self.load_from_db()

    def on_ws_message(self, message):
        try:
            data = json.loads(message)
            if data.get("action") == "new_news":
                logger.info("UI: WebSocket notification received - refreshing feed")
                self.load_from_db(clear=True)
                self.refresh_btn.setText("Refresh from Web")
                self.refresh_btn.setEnabled(True)
        except Exception as e:
            logger.error(f"UI: WS message error: {e}")

    def on_sort_changed(self, text):
        self.sort_by = text.lower()
        self.current_page = 0
        self.load_from_db(clear=True)

    def load_from_db(self, clear=True):
        if clear:
            for i in reversed(range(self.news_layout.count())): 
                widget = self.news_layout.itemAt(i).widget()
                if widget: widget.setParent(None)
            self.current_page = 0

        # Use new pagination format
        page_obj = self.news_repo.get_all(
            page=self.current_page, 
            size=self.limit, 
            sort_by=self.sort_by
        )

        
        for item in page_obj.content:
            news_dict = {
                "title": item.title,
                "url": item.url,
                "source": item.source,
                "image_url": item.image_url,
                "category": item.category
            }
            card = NewsCard(news_dict, self.open_news_callback)
            self.news_layout.addWidget(card)
        
        # Update Load More button based on 'last' property
        self.load_more_btn.setEnabled(not page_obj.last)
        if page_obj.last:
            self.load_more_btn.setText("No more news")
        else:
            self.load_more_btn.setText("Load More")

    def load_more(self):
        self.current_page += 1
        self.load_from_db(clear=False)

    def refresh_from_web(self):
        self.refresh_btn.setText("Refreshing...")
        self.refresh_btn.setEnabled(False)
        
        self.worker = NewsRefreshWorker(self.news_service)
        self.worker.finished.connect(self.on_refresh_finished)
        self.worker.error.connect(self.on_refresh_error)
        self.worker.start()

    def on_refresh_finished(self):
        self.ws_service.broadcast({"action": "new_news"})

    def on_refresh_error(self, error_msg):
        logger.error(f"UI: Refresh failed: {error_msg}")
        self.refresh_btn.setText("Refresh from Web")
        self.refresh_btn.setEnabled(True)