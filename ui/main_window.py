from PySide6.QtWidgets import QWidget, QHBoxLayout, QStackedWidget, QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from ui.components.sidebar import Sidebar
from ui.pages.home_page import HomePage
from ui.pages.news_detail_page import NewsDetailPage
from ui.pages.meme_page import MemePage
from ui.pages.history_page import HistoryPage

from services.news_service import NewsService
from services.text_service import TextService
from services.image_generate_service import ImageGenerateService
from services.meme_service import MemeService
from services.websocket_service import WebSocketService


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI News Meme Generator")
        self.resize(1100, 750)

        layout = QHBoxLayout()

        # Sidebar
        self.sidebar = Sidebar()

        # Stack
        self.stack = QStackedWidget()

        # Services
        self.news_service = NewsService()
        self.text_service = TextService()
        self.image_service = ImageGenerateService()
        self.meme_service = MemeService()
        self.ws_service = WebSocketService()
        self.ws_service.start()

        # Pages
        self.home_page = HomePage(self.news_service, self.open_news, self.ws_service)
        self.news_page = NewsDetailPage(
            self.text_service,
            self.image_service,
            self.meme_service,
            self.show_meme_result
        )
        self.meme_page = MemePage()
        self.history_page = HistoryPage()

        # Add pages
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.news_page)
        self.stack.addWidget(self.meme_page)
        self.stack.addWidget(self.history_page)

        # Sidebar actions
        self.sidebar.home_btn.clicked.connect(self.show_home)
        self.sidebar.meme_btn.clicked.connect(self.show_meme)
        self.sidebar.history_btn.clicked.connect(self.show_history)
        
        # Back button in News Page
        self.news_page.back_btn.clicked.connect(self.show_home)

        layout.addWidget(self.sidebar)
        layout.addWidget(self.stack, 1)

        self.setLayout(layout)

        # default page
        self.show_home()

    # ------------------ Navigation ------------------

    def show_home(self):
        self.sidebar.home_btn.setDown(True)
        self.sidebar.meme_btn.setDown(False)
        self.sidebar.history_btn.setDown(False)
        self.stack.setCurrentWidget(self.home_page)

    def show_meme(self):
        self.sidebar.home_btn.setDown(False)
        self.sidebar.meme_btn.setDown(True)
        self.sidebar.history_btn.setDown(False)
        self.stack.setCurrentWidget(self.meme_page)

    def show_history(self):
        self.sidebar.home_btn.setDown(False)
        self.sidebar.meme_btn.setDown(False)
        self.sidebar.history_btn.setDown(True)
        self.history_page.load_history()
        self.stack.setCurrentWidget(self.history_page)

    def open_news(self, news):
        self.news_page.load_news(news, self.news_service)
        self.stack.setCurrentWidget(self.news_page)

    def show_meme_result(self, meme_path):
        self.show_meme()
        self.meme_page.show_result(meme_path)