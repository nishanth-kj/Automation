from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(200)

        layout = QVBoxLayout()

        self.home_btn = QPushButton("Home")
        self.meme_btn = QPushButton("Meme Generator")

        layout.addWidget(self.home_btn)
        layout.addWidget(self.meme_btn)
        layout.addStretch()

        self.setLayout(layout)
