from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(200)

        layout = QVBoxLayout()

        self.home_btn = QPushButton("Home")
        self.meme_btn = QPushButton("Meme Generator")
        self.history_btn = QPushButton("History")
        self.chat_btn = QPushButton("Chat AI")
        self.rag_btn = QPushButton("AI Knowledge")
        self.settings_btn = QPushButton("Settings")

        layout.addWidget(self.home_btn)
        layout.addWidget(self.meme_btn)
        layout.addWidget(self.history_btn)
        layout.addWidget(self.chat_btn)
        layout.addWidget(self.rag_btn)
        layout.addWidget(self.settings_btn)




        layout.addStretch()

        self.setLayout(layout)
