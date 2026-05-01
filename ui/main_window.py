from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from ui.components.sidebar import Sidebar
from ui.pages.home_page import HomePage
from ui.pages.news_detail_page import NewsDetailPage
from ui.pages.meme_page import MemePage

from services.news_service import NewsService
from services.text_service import TextService
from services.image_generate_service import ImageGenerateService
from services.meme_service import MemeService


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI News Meme Studio")
        self.resize(1100, 750)
        
        # Apply global styling
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #ffffff;
                color: #2c3e50;
            }
            QStackedWidget {
                background-color: #f9f9f9;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()

        # Stack
        self.stack = QStackedWidget()

        # Services
        self.news_service = NewsService()
        self.text_service = TextService()
        self.image_service = ImageGenerateService()
        self.meme_service = MemeService()

        # Pages
        self.home_page = HomePage(self.news_service, self.open_news)
        self.news_page = NewsDetailPage(
            self.text_service,
            self.image_service,
            self.meme_service,
            self.show_meme_result
        )
        self.meme_page = MemePage()

        # Add pages
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.news_page)
        self.stack.addWidget(self.meme_page)

        # Sidebar actions
        self.sidebar.home_btn.clicked.connect(self.show_home)
        self.sidebar.meme_btn.clicked.connect(self.show_meme)
        
        # Back button in News Page
        self.news_page.back_btn.clicked.connect(self.show_home)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, 1)

        self.setLayout(layout)

        # default page
        self.show_home()

    # ------------------ Navigation ------------------

    def show_home(self):
        self.sidebar.home_btn.setChecked(True)
        self.sidebar.meme_btn.setChecked(False)
        self.stack.setCurrentWidget(self.home_page)

    def show_meme(self):
        self.sidebar.home_btn.setChecked(False)
        self.sidebar.meme_btn.setChecked(True)
        self.stack.setCurrentWidget(self.meme_page)

    def open_news(self, news):
        self.news_page.load_news(news, self.news_service)
        self.stack.setCurrentWidget(self.news_page)

    def show_meme_result(self, meme_path):
        self.sidebar.meme_btn.setChecked(True)
        self.sidebar.home_btn.setChecked(False)
        self.meme_page.show_result(meme_path)
        self.stack.setCurrentWidget(self.meme_page)