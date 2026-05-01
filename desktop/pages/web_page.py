from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

class WebPage(QWidget):
    def __init__(self, back_callback):
        super().__init__()
        self.back_callback = back_callback

        layout = QVBoxLayout()
        
        # Header
        header = QHBoxLayout()
        self.back_btn = QPushButton("← Back to Details")
        self.back_btn.clicked.connect(self.back_callback)
        header.addWidget(self.back_btn)
        header.addStretch()
        layout.addLayout(header)

        # Web View
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        self.setLayout(layout)

    def load_url(self, url):
        self.browser.setUrl(QUrl(url))
