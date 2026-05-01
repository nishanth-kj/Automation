from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QLabel, QHBoxLayout, QComboBox
from PySide6.QtCore import Qt
from ui.components.news_card import NewsCard
from repository.news_repository import NewsRepository

class HomePage(QWidget):
    def __init__(self, news_service, open_news_callback):
        super().__init__()

        self.news_service = news_service
        self.open_news_callback = open_news_callback
        self.news_repo = NewsRepository()
        
        self.offset = 0
        self.limit = 10
        self.sort_by = "newest"

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

    def on_sort_changed(self, text):
        self.sort_by = text.lower()
        self.offset = 0
        self.load_from_db(clear=True)

    def load_from_db(self, clear=True):
        if clear:
            for i in reversed(range(self.news_layout.count())): 
                widget = self.news_layout.itemAt(i).widget()
                if widget: widget.setParent(None)
            self.offset = 0

        news_items = self.news_repo.get_news(limit=self.limit, offset=self.offset, sort_by=self.sort_by)
        for item in news_items:
            # Convert DB object to dict for UI compatibility
            news_dict = {
                "title": item.title,
                "url": item.url,
                "source": item.source,
                "image_url": item.image_url,
                "category": item.category
            }
            card = NewsCard(news_dict, self.open_news_callback)
            self.news_layout.addWidget(card)
        
        self.offset += len(news_items)

    def load_more(self):
        self.load_from_db(clear=False)

    def refresh_from_web(self):
        try:
            self.refresh_btn.setText("Fetching...")
            self.refresh_btn.setEnabled(False)
            from PySide6.QtWidgets import QApplication
            QApplication.processEvents()

            news = self.news_service.fetch("trending", limit=20)
            self.news_repo.save_all(news)
            
            self.refresh_btn.setText("Refresh from Web")
            self.refresh_btn.setEnabled(True)
            self.load_from_db(clear=True)
        except Exception as e:
            self.news_layout.addWidget(QLabel(f"Error: {str(e)}"))
            self.refresh_btn.setEnabled(True)