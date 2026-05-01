from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QSplitter, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve

from ui.components.sidebar import Sidebar
from ui.pages.home_page import HomePage
from ui.pages.news_page import NewsPage
from ui.pages.news_detail_page import NewsDetailPage
from ui.pages.meme_page import MemePage
from ui.pages.history_page import HistoryPage
from ui.pages.web_page import WebPage
from ui.pages.settings_page import SettingsPage
from ui.pages.chat_page import ChatPage
from ui.pages.rag_page import RagPage
from ui.components.console_widget import ConsoleWidget, QtLogHandler

from services.news_service import NewsService
from services.text_service import TextService
from services.image_generate_service import ImageGenerateService
from services.meme_service import MemeService
from services.websocket_service import WebSocketService
from repository.setting_repository import SettingRepository
from utils.theme_manager import ThemeManager
from utils.logger import logger
import logging


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI News Meme Studio")
        self.resize(1300, 900)
        self.setting_repo = SettingRepository()

        # Layout
        main_vbox = QVBoxLayout(self)
        main_vbox.setContentsMargins(0, 0, 0, 0)
        main_vbox.setSpacing(0)

        self.vertical_splitter = QSplitter(Qt.Vertical)

        content_widget = QWidget()
        content_hbox = QHBoxLayout(content_widget)
        content_hbox.setContentsMargins(0, 0, 0, 0)
        content_hbox.setSpacing(0)

        self.sidebar = Sidebar()
        self.stack = QStackedWidget()
        
        self.opacity_effect = QGraphicsOpacityEffect(self.stack)
        self.stack.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(350)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)

        # Services
        self.news_service = NewsService()
        self.text_service = TextService()
        self.image_service = ImageGenerateService()
        self.meme_service = MemeService()
        self.ws_service = WebSocketService()
        self.ws_service.start()

        # Pages
        self.dashboard = HomePage(self.navigate_by_key)
        self.news_page = NewsPage(self.news_service, self.open_news_detail, self.ws_service)
        self.news_detail = NewsDetailPage(
            self.text_service,
            self.image_service,
            self.meme_service,
            self.show_meme_result,
            self.open_internal_web
        )
        self.meme_page = MemePage()
        self.history_page = HistoryPage()
        self.web_page = WebPage(self.show_news_detail)
        self.settings_page = SettingsPage()
        self.chat_page = ChatPage()
        self.rag_page = RagPage()

        # Add pages
        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(self.news_page)
        self.stack.addWidget(self.news_detail)
        self.stack.addWidget(self.meme_page)
        self.stack.addWidget(self.history_page)
        self.stack.addWidget(self.web_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.chat_page)
        self.stack.addWidget(self.rag_page)

        content_hbox.addWidget(self.sidebar)
        content_hbox.addWidget(self.stack, 1)

        self.console = ConsoleWidget()
        self.console.close_requested.connect(self.hide_console)
        self.setup_logging()

        self.vertical_splitter.addWidget(content_widget)
        self.vertical_splitter.addWidget(self.console)
        self.vertical_splitter.setStretchFactor(0, 5)
        self.vertical_splitter.setStretchFactor(1, 1)

        main_vbox.addWidget(self.vertical_splitter)

        # Sidebar Actions
        self.sidebar.home_btn.clicked.connect(self.show_home)
        self.sidebar.news_btn.clicked.connect(self.show_news)
        self.sidebar.meme_btn.clicked.connect(self.show_meme)
        self.sidebar.history_btn.clicked.connect(self.show_history)
        self.sidebar.chat_btn.clicked.connect(self.show_chat)
        self.sidebar.rag_btn.clicked.connect(self.show_rag)
        self.sidebar.settings_btn.clicked.connect(self.show_settings)
        
        self.news_detail.back_btn.clicked.connect(self.show_news)

        self.apply_settings()
        self.show_home()

    def setup_logging(self):
        self.qt_log_handler = QtLogHandler()
        formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%H:%M:%S')
        self.qt_log_handler.setFormatter(formatter)
        self.qt_log_handler.signal.new_log.connect(self.console.append_log)
        logger.addHandler(self.qt_log_handler)

    def apply_settings(self):
        theme = self.setting_repo.get("theme", "dark")
        self.setStyleSheet(ThemeManager.get_dark_theme() if theme == "dark" else ThemeManager.get_light_theme())
        show_logs = self.setting_repo.get("show_logs", "true") == "true"
        self.console.setVisible(show_logs)

    def hide_console(self):
        self.console.hide()
        self.setting_repo.set("show_logs", "false")

    def switch_page(self, widget):
        self.animation.stop()
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.stack.setCurrentWidget(widget)
        self.animation.start()

    def navigate_by_key(self, key):
        mapping = {
            "news": self.news_page, "meme": self.meme_page, "history": self.history_page,
            "chat": self.chat_page, "rag": self.rag_page, "settings": self.settings_page
        }
        if key in mapping: self.switch_page(mapping[key])

    def show_home(self): self.switch_page(self.dashboard)
    def show_news(self): self.switch_page(self.news_page)
    def show_meme(self): self.switch_page(self.meme_page)
    def show_history(self):
        self.history_page.load_history()
        self.switch_page(self.history_page)
    def show_chat(self): self.switch_page(self.chat_page)
    def show_rag(self): self.switch_page(self.rag_page)
    def show_settings(self): self.switch_page(self.settings_page)
    def show_news_detail(self): self.switch_page(self.news_detail)

    def open_news_detail(self, news):
        self.news_detail.load_news(news, self.news_service)
        self.show_news_detail()

    def open_internal_web(self, url):
        self.web_page.load_url(url)
        self.switch_page(self.web_page)

    def show_meme_result(self, meme_path):
        self.show_meme()
        self.meme_page.show_result(meme_path)