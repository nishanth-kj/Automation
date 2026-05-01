from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QLabel
from PySide6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self, news_service, open_news_callback):
        super().__init__()

        self.news_service = news_service
        self.open_news_callback = open_news_callback
        
        main_layout = QVBoxLayout()
        
        title = QLabel("Top Technology News")
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px; color: #2c3e50;")
        main_layout.addWidget(title)

        # Scroll area for news
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        container = QWidget()
        self.news_layout = QVBoxLayout(container)
        self.news_layout.setAlignment(Qt.AlignTop)
        
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)
        
        self.refresh_news()

    def refresh_news(self):
        # Clear layout
        for i in reversed(range(self.news_layout.count())): 
            self.news_layout.itemAt(i).widget().setParent(None)

        try:
            news = self.news_service.fetch("technology", limit=10)
            for item in news:
                btn = QPushButton(item["title"])
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        padding: 15px;
                        text-align: left;
                        font-size: 14px;
                        margin-bottom: 5px;
                    }
                    QPushButton:hover {
                        background-color: #f8f9fa;
                        border-color: #3498db;
                    }
                """)
                btn.setCursor(Qt.PointingHandCursor)
                btn.clicked.connect(lambda _, n=item: self.open_news_callback(n))
                self.news_layout.addWidget(btn)
        except Exception as e:
            self.news_layout.addWidget(QLabel(f"Error fetching news: {str(e)}"))