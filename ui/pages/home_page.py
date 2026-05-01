from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QLabel
from PySide6.QtCore import Qt

class HomePage(QWidget):
    def __init__(self, news_service, open_news_callback):
        super().__init__()

        self.news_service = news_service
        self.open_news_callback = open_news_callback
        
        layout = QVBoxLayout()
        
        self.news_layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Latest News"))
        layout.addLayout(self.news_layout)
        layout.addStretch()

        self.setLayout(layout)
        self.refresh_news()

    def refresh_news(self):
        try:
            news = self.news_service.fetch("technology", limit=10)
            for item in news:
                btn = QPushButton(item["title"])
                btn.clicked.connect(lambda _, n=item: self.open_news_callback(n))
                self.news_layout.addWidget(btn)
        except Exception as e:
            self.news_layout.addWidget(QLabel(f"Error: {str(e)}"))
