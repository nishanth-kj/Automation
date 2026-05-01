from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QSplitter
from PySide6.QtCore import Qt

from ui.components.sidebar import Sidebar
from ui.pages.home_page import HomePage
from ui.pages.news_detail_page import NewsDetailPage
from ui.pages.meme_page import MemePage
from ui.pages.history_page import HistoryPage
from ui.pages.web_page import WebPage
from ui.components.console_widget import ConsoleWidget, QtLogHandler

from services.news_service import NewsService
from services.text_service import TextService
from services.image_generate_service import ImageGenerateService
from services.meme_service import MemeService
from services.websocket_service import WebSocketService
from utils.logger import logger
import logging


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI News Meme Generator")
        self.resize(1200, 850)

        # Main Layout
        main_vbox = QVBoxLayout(self)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.setSpacing(0)

        # Splitter for Content vs Console
        self.vertical_splitter = QSplitter(Qt.Vertical)

        # Horizontal layout for Sidebar + Stack
        content_widget = QWidget()
        content_hbox = QHBoxLayout(content_widget)
        content_hbox.setContentsMargins(0, 0, 0, 0)
        content_hbox.setSpacing(0)

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
            self.show_meme_result,
            self.open_internal_web
        )
        self.meme_page = MemePage()
        self.history_page = HistoryPage()
        self.web_page = WebPage(self.show_news_detail)

        # Add pages to stack
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.news_page)
        self.stack.addWidget(self.meme_page)
        self.stack.addWidget(self.history_page)
        self.stack.addWidget(self.web_page)

        content_hbox.addWidget(self.sidebar)
        content_hbox.addWidget(self.stack, 1)

        # Console
        self.console = ConsoleWidget()
        
        # Connect Logger to Console
        self.qt_log_handler = QtLogHandler()
        self.qt_log_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%H:%M:%S'))
        self.qt_log_handler.signal.new_log.connect(self.console.append_log)
        logger.addHandler(self.qt_log_handler)

        # Add to splitter
        self.vertical_splitter.addWidget(content_widget)
        self.vertical_splitter.addWidget(self.console)
        self.vertical_splitter.setStretchFactor(0, 4)
        self.vertical_splitter.setStretchFactor(1, 1)

        main_vbox.addWidget(self.vertical_splitter)

        # Sidebar actions
        self.sidebar.home_btn.clicked.connect(self.show_home)
        self.sidebar.meme_btn.clicked.connect(self.show_meme)
        self.sidebar.history_btn.clicked.connect(self.show_history)
        
        # Back button in News Page
        self.news_page.back_btn.clicked.connect(self.show_home)

        # Default page
        self.show_home()

    # ------------------ Navigation ------------------

    def show_home(self):
        self.stack.setCurrentWidget(self.home_page)

    def show_meme(self):
        self.stack.setCurrentWidget(self.meme_page)

    def show_history(self):
        self.history_page.load_history()
        self.stack.setCurrentWidget(self.history_page)

    def show_news_detail(self):
        self.stack.setCurrentWidget(self.news_page)

    def open_news(self, news):
        self.news_page.load_news(news, self.news_service)
        self.stack.setCurrentWidget(self.news_page)

    def open_internal_web(self, url):
        self.web_page.load_url(url)
        self.stack.setCurrentWidget(self.web_page)

    def show_meme_result(self, meme_path):
        self.show_meme()
        self.meme_page.show_result(meme_path)