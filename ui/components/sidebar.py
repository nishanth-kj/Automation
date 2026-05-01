from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt

class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(240)
        self.setObjectName("sidebar")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 30, 15, 30)
        layout.setSpacing(10)
        
        logo = QLabel("NEWS MEME")
        logo.setStyleSheet("font-size: 20px; font-weight: 900; color: #3b82f6; margin-bottom: 20px; letter-spacing: 2px;")
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        self.home_btn = QPushButton(" Dashboard")
        self.news_btn = QPushButton(" News Feed")
        self.meme_btn = QPushButton(" Meme Generator")
        self.history_btn = QPushButton(" History")
        self.chat_btn = QPushButton(" Chat AI")
        self.rag_btn = QPushButton(" Knowledge")
        self.settings_btn = QPushButton(" Settings")

        self.all_btns = [
            self.home_btn, self.news_btn, self.meme_btn, 
            self.history_btn, self.chat_btn, self.rag_btn, 
            self.settings_btn
        ]
        
        for btn in self.all_btns:
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            layout.addWidget(btn)

        layout.addStretch()
        
        footer = QLabel("v1.2.0 Stable")
        footer.setStyleSheet("color: #475569; font-size: 10px; font-weight: 600;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        self.setLayout(layout)