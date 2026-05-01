from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt
import requests

class NewsCard(QFrame):
    def __init__(self, news_item, callback):
        super().__init__()
        self.news = news_item
        self.callback = callback

        self.setFrameShape(QFrame.StyledPanel)
        self.setLineWidth(1)
        self.setMinimumHeight(150)
        
        layout = QVBoxLayout()
        
        # Source & Time
        header = QHBoxLayout()
        source_lbl = QLabel(news_item.get("source", "Unknown"))
        source_lbl.setStyleSheet("color: #666; font-size: 10px; font-weight: bold;")
        header.addWidget(source_lbl)
        header.addStretch()
        layout.addLayout(header)

        # Title
        title_lbl = QLabel(news_item.get("title", "No Title"))
        title_lbl.setWordWrap(True)
        title_lbl.setFont(QFont("Arial", 11, QFont.Bold))
        layout.addWidget(title_lbl)

        # Description (if available)
        # content_lbl = QLabel(news_item.get("content", "")[:100] + "...")
        # layout.addWidget(content_lbl)

        # Footer with button
        footer = QHBoxLayout()
        view_btn = QPushButton("View Details")
        view_btn.clicked.connect(lambda: self.callback(self.news))
        footer.addStretch()
        footer.addWidget(view_btn)
        layout.addLayout(footer)

        self.setLayout(layout)
