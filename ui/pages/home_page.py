from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QLabel, QHBoxLayout, QComboBox
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebSockets import QWebSocket
from ui.components.news_card import NewsCard
from repository.news_repository import NewsRepository
from repository.setting_repository import SettingRepository
from services.news_task_service import NewsRefreshWorker
from utils.logger import logger
from utils.time_utils import TimeUtils
import json

class HomePage(QWidget):
    def __init__(self, news_service, open_news_callback, ws_service):
        super().__init__()

        self.news_service = news_service
        self.open_news_callback = open_news_callback
        self.ws_service = ws_service
        self.news_repo = NewsRepository()
        self.setting_repo = SettingRepository()
        
        self.current_page = 0
        self.limit = 10
        self.sort_by = "newest"
        self.cards = []

        # WebSocket Client
        self.client = QWebSocket()
        self.client.textMessageReceived.connect(self.on_ws_message)
        self.client.open(QUrl("ws://localhost:8765"))

        main_layout = QVBoxLayout()
        
        # Header 1: Status and Last Fetched
        header1 = QHBoxLayout()
        self.last_fetched_label = QLabel("Last Fetched: Never")
        header1.addWidget(self.last_fetched_label)
        header1.addStretch()
        main_layout.addLayout(header1)

        # Header 2: Toolbar
        toolbar = QHBoxLayout()
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.toggle_select_all)
        
        self.ai_select_btn = QPushButton("AI Select Best")
        self.ai_select_btn.clicked.connect(self.ai_select_best)
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected)
        
        toolbar.addWidget(self.select_all_btn)
        toolbar.addWidget(self.ai_select_btn)
        toolbar.addWidget(self.delete_btn)

        toolbar.addStretch()
        
        self.sort_box = QComboBox()
        self.sort_box.addItems(["Newest", "Source"])
        self.sort_box.currentTextChanged.connect(self.on_sort_changed)
        toolbar.addWidget(QLabel("Sort:"))
        toolbar.addWidget(self.sort_box)
        
        main_layout.addLayout(toolbar)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.news_layout = QVBoxLayout(self.scroll_content)
        self.news_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll)

        # Footer
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
        self.load_from_db()

    def toggle_select_all(self):
        if not self.cards: return
        # If all selected, deselect. Else select all.
        all_sel = all(c.is_selected() for c in self.cards)
        for c in self.cards:
            c.set_selected(not all_sel)

    def ai_select_best(self):
        selected_news = [c.news for c in self.cards if c.is_selected()]
        if not selected_news:
            logger.warning("No news selected for AI analysis")
            return
            
        logger.info(f"UI: Asking AI to select best news from {len(selected_news)} items")
        self.ai_select_btn.setEnabled(False)
        self.ai_select_btn.setText("AI Thinking...")
        
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()

        try:
            titles = [n["title"] for n in selected_news]
            prompt_tpl = self.setting_repo.get("selection_prompt", "From the following news titles, select the 3 most viral/funny ones. Return only the titles separated by |.")
            full_prompt = f"{prompt_tpl}\n\n" + "\n".join(titles)
            
            # Use MainWindow's text service via some bridge or import
            # For now, I'll assume we can use news_service's internal text generator if it exists or just use a new one.
            from services.text_service import TextService
            ts = TextService()
            result = ts.generate(full_prompt)
            best_titles = [t.strip() for t in result.split("|")]
            
            # Select them in UI
            for c in self.cards:
                if c.news["title"] in best_titles:
                    c.set_selected(True)
                else:
                    c.set_selected(False)
            
            logger.info("AI selection complete")
        except Exception as e:
            logger.error(f"AI selection failed: {e}")
            
        self.ai_select_btn.setEnabled(True)
        self.ai_select_btn.setText("AI Select Best")

    def delete_selected(self):
        selected_ids = [c.news["news_id"] for c in self.cards if c.is_selected()]
        if not selected_ids: return
        
        logger.info(f"UI: Soft-deleting {len(selected_ids)} news items")
        for news_id in selected_ids:
            self.news_repo.delete(news_id)
        
        self.load_from_db(clear=True)


    def on_ws_message(self, message):
        try:
            data = json.loads(message)
            if data.get("action") == "new_news":
                self.load_from_db(clear=True)
                self.refresh_btn.setText("Refresh from Web")
                self.refresh_btn.setEnabled(True)
        except Exception as e:
            logger.error(f"WS error: {e}")

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
            self.cards = []

        page_obj = self.news_repo.get_all(page=self.current_page, size=self.limit, sort_by=self.sort_by)
        
        for item in page_obj.content:
            news_dict = {
                "news_id": item.news_id,
                "title": item.title,
                "url": item.url,
                "source": item.source,
                "image_url": item.image_url,
                "category": item.category,
                "created_at": item.created_at
            }
            card = NewsCard(news_dict, self.open_news_callback)
            self.news_layout.addWidget(card)
            self.cards.append(card)
        
        # Update last fetched label
        if page_obj.content:
            latest = page_obj.content[0].created_at
            dt = TimeUtils.from_epoch(latest)
            self.last_fetched_label.setText(f"Last Fetched: {dt.strftime('%H:%M:%S')}")

        self.load_more_btn.setEnabled(not page_obj.last)
        if page_obj.last: self.load_more_btn.setText("No more news")
        else: self.load_more_btn.setText("Load More")

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
        logger.error(f"Refresh failed: {error_msg}")
        self.refresh_btn.setText("Refresh from Web")
        self.refresh_btn.setEnabled(True)