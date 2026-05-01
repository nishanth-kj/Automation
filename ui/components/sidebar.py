from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(200)
        self.setStyleSheet("background-color: #222; color: white;")

        layout = QVBoxLayout()
        
        title = QLabel("AI MEME STUDIO")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px; color: #3498db;")
        layout.addWidget(title)

        self.home_btn = QPushButton("Dashboard")
        self.news_btn = QPushButton("News Feed")
        self.meme_btn = QPushButton("Meme Generator")
        self.history_btn = QPushButton("History")
        self.chat_btn = QPushButton("Chat AI")
        self.rag_btn = QPushButton("AI Knowledge")
        self.settings_btn = QPushButton("Settings")

        layout.addWidget(self.home_btn)
        layout.addWidget(self.news_btn)
        layout.addWidget(self.meme_btn)
        layout.addWidget(self.history_btn)
        layout.addWidget(self.chat_btn)
        layout.addWidget(self.rag_btn)
        layout.addWidget(self.settings_btn)

        layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet(self.styleSheet() + """
            QPushButton {
                text-align: left;
                padding: 12px;
                border: none;
                background: transparent;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)