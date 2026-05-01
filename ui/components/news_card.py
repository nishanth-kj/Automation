from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QCheckBox, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtCore import Qt

class NewsCard(QFrame):
    def __init__(self, news, view_callback):
        super().__init__()
        self.news = news
        self.view_callback = view_callback
        
        self.setObjectName("news_card")
        self.setFixedHeight(120)
        
        # Modern Card Style
        self.setStyleSheet("""
            QFrame#news_card {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
                margin: 5px 10px;
            }
            QFrame#news_card:hover {
                background-color: #334155;
                border: 1px solid #3b82f6;
            }
            QLabel#title {
                font-size: 15px;
                font-weight: 700;
                color: #f8fafc;
                border: none;
            }
            QLabel#source {
                font-size: 11px;
                font-weight: 500;
                color: #3b82f6;
                border: none;
                text-transform: uppercase;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Selection
        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox)

        # Thumbnail with rounded corners
        self.img_label = QLabel()
        self.img_label.setFixedSize(120, 90)
        self.img_label.setStyleSheet("background-color: #0f172a; border-radius: 8px;")
        self.img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.img_label)

        # Content
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        self.source_label = QLabel(news.get("source", "Unknown").upper())
        self.source_label.setObjectName("source")
        
        self.title_label = QLabel(news.get("title", "No Title"))
        self.title_label.setObjectName("title")
        self.title_label.setWordWrap(True)
        
        text_layout.addWidget(self.source_label)
        text_layout.addWidget(self.title_label)
        text_layout.addStretch()
        
        layout.addLayout(text_layout, 1)

        # Action
        self.view_btn = QPushButton("Open")
        self.view_btn.setFixedSize(80, 36)
        self.view_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                font-weight: 700;
                border-radius: 18px;
            }
            QPushButton:hover {
                background-color: #60a5fa;
            }
        """)
        self.view_btn.clicked.connect(lambda: self.view_callback(self.news))
        layout.addWidget(self.view_btn)

    def is_selected(self): return self.checkbox.isChecked()
    def set_selected(self, s): self.checkbox.setChecked(s)
