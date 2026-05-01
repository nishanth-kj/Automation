from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QCheckBox, QFrame
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt

class NewsCard(QFrame):
    def __init__(self, news, view_callback):
        super().__init__()
        self.news = news
        self.view_callback = view_callback
        
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet("""
            NewsCard {
                background-color: #fff;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-bottom: 5px;
            }
            QLabel { color: #333; border: none; }
            QPushButton { 
                background-color: #3498db; 
                color: white; 
                border-radius: 4px;
                font-weight: bold;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Selection Checkbox
        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox)

        # Thumbnail
        self.img_label = QLabel()
        self.img_label.setFixedSize(120, 80)
        self.img_label.setStyleSheet("background-color: #f0f0f0; border-radius: 4px;")
        self.img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.img_label)

        # Text Content
        text_layout = QVBoxLayout()
        self.title_label = QLabel(news.get("title", "No Title"))
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        self.source_label = QLabel(news.get("source", "Unknown Source"))
        self.source_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.source_label)
        text_layout.addStretch()
        
        layout.addLayout(text_layout, 1)

        # Action Buttons
        btn_layout = QVBoxLayout()
        self.view_btn = QPushButton("Read")
        self.view_btn.setFixedSize(70, 30)
        self.view_btn.clicked.connect(lambda: self.view_callback(self.news))
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.view_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)

    def is_selected(self):
        return self.checkbox.isChecked()

    def set_selected(self, selected):
        self.checkbox.setChecked(selected)
