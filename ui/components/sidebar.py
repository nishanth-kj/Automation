from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(200)
        self.setStyleSheet("""
            Sidebar {
                background-color: #2c3e50;
                border-right: 1px solid #34495e;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:checked {
                background-color: #3498db;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 20, 0, 0)
        layout.setSpacing(0)

        self.home_btn = QPushButton(" Home")
        self.meme_btn = QPushButton(" Meme Generator")

        self.home_btn.setCheckable(True)
        self.meme_btn.setCheckable(True)

        layout.addWidget(self.home_btn)
        layout.addWidget(self.meme_btn)
        layout.addStretch()

        self.setLayout(layout)