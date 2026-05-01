from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt, Signal

class ToolCard(QFrame):
    clicked = Signal()
    def __init__(self, title, description, color="#3498db"):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedSize(250, 180)
        self.setStyleSheet(f"""
            ToolCard {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 12px;
            }}
            ToolCard:hover {{
                background-color: #f9f9f9;
                border-width: 3px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {color};")
        layout.addWidget(t_lbl, 0, Qt.AlignCenter)
        
        d_lbl = QLabel(description)
        d_lbl.setWordWrap(True)
        d_lbl.setAlignment(Qt.AlignCenter)
        d_lbl.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(d_lbl, 0, Qt.AlignCenter)
        
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked.emit()

class HomePage(QWidget):
    def __init__(self, nav_callback):
        super().__init__()
        self.nav_callback = nav_callback

        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        
        header = QLabel("Welcome to AI News Meme Studio")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(header)
        
        grid = QGridLayout()
        grid.setSpacing(20)
        
        # Define Tools
        tools = [
            ("News Feed", "Browse latest trending stories", "news", "#3498db"),
            ("Meme Gen", "Create viral AI memes", "meme", "#e67e22"),
            ("History", "View your generated memes", "history", "#2ecc71"),
            ("Chat AI", "Talk to Gemma AI directly", "chat", "#9b59b6"),
            ("AI Knowledge", "RAG-powered semantic search", "rag", "#f1c40f"),
            ("Settings", "Configure AI and UI themes", "settings", "#95a5a6"),
        ]
        
        row, col = 0, 0
        for title, desc, key, color in tools:
            card = ToolCard(title, desc, color)
            card.clicked.connect(lambda k=key: self.nav_callback(k))
            grid.addWidget(card, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
                
        layout.addLayout(grid)
        layout.addStretch()
        self.setLayout(layout)