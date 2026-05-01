from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QColor

class ToolCard(QFrame):
    clicked = Signal()
    def __init__(self, title, description, icon_text):
        super().__init__()
        self.setFixedSize(260, 160)
        self.setObjectName("tool_card")
        
        # Soft Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet("""
            QFrame#tool_card {
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 12px;
            }
            QFrame#tool_card:hover {
                background-color: #1c1c20;
                border: 1px solid #3f3f46;
            }
            QLabel { border: none; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        icon_lbl = QLabel(icon_text)
        icon_lbl.setStyleSheet("font-size: 24px; margin-bottom: 5px;")
        layout.addWidget(icon_lbl)
        
        t_lbl = QLabel(title)
        t_lbl.setStyleSheet("font-size: 16px; font-weight: 700; color: #fff;")
        layout.addWidget(t_lbl)
        
        d_lbl = QLabel(description)
        d_lbl.setWordWrap(True)
        d_lbl.setStyleSheet("color: #71717a; font-size: 12px; margin-top: 4px;")
        layout.addWidget(d_lbl)
        
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked.emit()

class HomePage(QWidget):
    def __init__(self, nav_callback):
        super().__init__()
        self.nav_callback = nav_callback

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        header_section = QVBoxLayout()
        title = QLabel("Welcome to the Studio")
        title.setStyleSheet("font-size: 28px; font-weight: 800; color: #fff;")
        header_section.addWidget(title)
        
        subtitle = QLabel("Select a workspace to start generating content.")
        subtitle.setStyleSheet("font-size: 14px; color: #71717a;")
        header_section.addWidget(subtitle)
        layout.addLayout(header_section)
        
        layout.addSpacing(20)
        
        grid = QGridLayout()
        grid.setSpacing(20)
        
        tools = [
            ("News Feed", "Explore trending global news.", "news", "🌐"),
            ("Meme Gen", "Create viral AI memes.", "meme", "🎭"),
            ("History", "Your past generations.", "history", "📂"),
            ("Chat AI", "Talk with Gemma AI.", "chat", "💬"),
            ("Knowledge", "RAG Knowledge Base.", "rag", "🧠"),
            ("Settings", "System configuration.", "settings", "⚙️"),
        ]
        
        row, col = 0, 0
        for title, desc, key, icon in tools:
            card = ToolCard(title, desc, icon)
            card.clicked.connect(lambda k=key: self.nav_callback(k))
            grid.addWidget(card, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
                
        layout.addLayout(grid)
        layout.addStretch()