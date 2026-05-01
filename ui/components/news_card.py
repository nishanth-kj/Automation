from PySide6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QCheckBox
from PySide6.QtCore import Qt

class NewsCard(QFrame):
    def __init__(self, news, view_callback):
        super().__init__()
        self.news = news
        self.view_callback = view_callback
        
        self.setObjectName("news_card")
        self.setFixedHeight(100)
        
        self.setStyleSheet("""
            QFrame#news_card {
                background-color: #000;
                border-bottom: 1px solid #111;
                border-radius: 0px;
                margin: 0px;
            }
            QFrame#news_card:hover {
                background-color: #050505;
                border-bottom: 1px solid #333;
            }
            QLabel#title {
                font-size: 14px;
                font-weight: 600;
                color: #fff;
                border: none;
            }
            QLabel#source {
                font-size: 9px;
                font-weight: 800;
                color: #444;
                border: none;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(20)
        
        # Selection
        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox)

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

        # Action
        self.view_btn = QPushButton("OPEN")
        self.view_btn.setFixedSize(70, 30)
        self.view_btn.setStyleSheet("""
            QPushButton {
                background-color: #fff;
                color: #000;
                font-size: 9px;
                font-weight: 900;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: #000;
                color: #fff;
                border: 1px solid #fff;
            }
        """)
        self.view_btn.clicked.connect(lambda: self.view_callback(self.news))
        layout.addWidget(self.view_btn)

    def is_selected(self): return self.checkbox.isChecked()
    def set_selected(self, s): self.checkbox.setChecked(s)
