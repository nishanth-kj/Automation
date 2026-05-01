from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QCheckBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class NewsCard(QWidget):
    def __init__(self, news, view_callback):
        super().__init__()
        self.news = news
        self.view_callback = view_callback

        layout = QHBoxLayout()
        
        # Selection Checkbox
        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox)

        # Image/Thumbnail (Small)
        self.img_label = QLabel()
        self.img_label.setFixedSize(80, 60)
        self.img_label.setStyleSheet("background-color: #eee; border: 1px solid #ccc;")
        self.img_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.img_label)

        # Text Content
        text_layout = QVBoxLayout()
        self.title_label = QLabel(news.get("title", "No Title"))
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("font-weight: bold;")
        
        self.source_label = QLabel(news.get("source", "Unknown Source"))
        self.source_label.setStyleSheet("color: #666; font-size: 10px;")
        
        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.source_label)
        
        layout.addLayout(text_layout, 1)

        # View Button
        self.view_btn = QPushButton("View")
        self.view_btn.setFixedWidth(60)
        self.view_btn.clicked.connect(lambda: self.view_callback(self.news))
        layout.addWidget(self.view_btn)

        self.setLayout(layout)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #eee;
            }
        """)

    def is_selected(self):
        return self.checkbox.isChecked()

    def set_selected(self, selected):
        self.checkbox.setChecked(selected)
