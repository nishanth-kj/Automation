from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QCheckBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class NewsCard(QFrame):
    def __init__(self, news, view_callback):
        super().__init__()
        self.news = news
        self.view_callback = view_callback
        
        self.setFixedHeight(110)
        self.setObjectName("news_card")
        
        self.setStyleSheet("""
            QFrame#news_card {
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 8px;
                margin-bottom: 5px;
            }
            QFrame#news_card:hover {
                border: 1px solid #3b82f6;
                background-color: #1c1c20;
            }
            QLabel#title {
                font-size: 14px;
                font-weight: 600;
                color: #fff;
            }
            QLabel#source {
                font-size: 11px;
                color: #3b82f6;
                font-weight: 500;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(15)
        
        # Selection
        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox)

        # Thumbnail
        self.img_label = QLabel()
        self.img_label.setFixedSize(100, 70)
        self.img_label.setStyleSheet("background-color: #09090b; border-radius: 4px;")
        self.img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.img_label)

        # Content
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        self.source_label = QLabel(news.get("source", "Unknown"))
        self.source_label.setObjectName("source")
        
        self.title_label = QLabel(news.get("title", "No Title"))
        self.title_label.setObjectName("title")
        self.title_label.setWordWrap(True)
        
        text_layout.addWidget(self.source_label)
        text_layout.addWidget(self.title_label)
        text_layout.addStretch()
        
        layout.addLayout(text_layout, 1)

        # View
        self.view_btn = QPushButton("View")
        self.view_btn.setFixedSize(60, 32)
        self.view_btn.clicked.connect(lambda: self.view_callback(self.news))
        layout.addWidget(self.view_btn)

    def is_selected(self): return self.checkbox.isChecked()
    def set_selected(self, s): self.checkbox.setChecked(s)
