from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QColor, QLinearGradient, QPalette, QBrush

class ToolCard(QFrame):
    clicked = Signal()
    def __init__(self, title, description, color_start, color_end):
        super().__init__()
        self.setObjectName("card")
        self.setFixedSize(280, 200)
        
        # Apply shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet(f"""
            QFrame#card {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {color_start}, stop:1 {color_end});
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
            }}
            QFrame#card:hover {{
                border: 2px solid white;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignCenter)
        
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-size: 20px; font-weight: 800; color: white; border: none;")
        layout.addWidget(t_lbl, 0, Qt.AlignCenter)
        
        d_lbl = QLabel(description)
        d_lbl.setWordWrap(True)
        d_lbl.setAlignment(Qt.AlignCenter)
        d_lbl.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 13px; border: none; font-weight: 500;")
        layout.addWidget(d_lbl, 0, Qt.AlignCenter)
        
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked.emit()

class HomePage(QWidget):
    def __init__(self, nav_callback):
        super().__init__()
        self.nav_callback = nav_callback

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        welcome_layout = QVBoxLayout()
        header = QLabel("AI News Meme Studio")
        header.setStyleSheet("font-size: 32px; font-weight: 900; color: #3b82f6; border: none;")
        welcome_layout.addWidget(header)
        
        sub_header = QLabel("Select a tool to get started with your content creation.")
        sub_header.setStyleSheet("font-size: 16px; color: #64748b; border: none;")
        welcome_layout.addWidget(sub_header)
        layout.addLayout(welcome_layout)
        
        grid = QGridLayout()
        grid.setSpacing(25)
        
        # Tools with Gradient pairs
        tools = [
            ("News Feed", "Explore trending global news", "news", "#3b82f6", "#1d4ed8"),
            ("Meme Gen", "Generate viral AI memes", "meme", "#f97316", "#c2410c"),
            ("History", "Your past masterpieces", "history", "#10b981", "#047857"),
            ("Chat AI", "Interact with Gemma", "chat", "#8b5cf6", "#6d28d9"),
            ("Knowledge", "RAG Semantic Search", "rag", "#f59e0b", "#d97706"),
            ("Settings", "System configuration", "settings", "#64748b", "#334155"),
        ]
        
        row, col = 0, 0
        for title, desc, key, c1, c2 in tools:
            card = ToolCard(title, desc, c1, c2)
            card.clicked.connect(lambda k=key: self.nav_callback(k))
            grid.addWidget(card, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
                
        layout.addLayout(grid)
        layout.addStretch()