from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame
from PySide6.QtCore import Qt, Signal

class ToolCard(QFrame):
    clicked = Signal()
    def __init__(self, title, description):
        super().__init__()
        self.setObjectName("card")
        self.setFixedSize(300, 200)
        
        self.setStyleSheet("""
            QFrame#card {
                background-color: #000;
                border: 1px solid #222;
                border-radius: 0px;
            }
            QFrame#card:hover {
                border: 1px solid #fff;
            }
            QLabel { border: none; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        t_lbl = QLabel(title.upper())
        t_lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: #fff; letter-spacing: 2px;")
        layout.addWidget(t_lbl)
        
        d_lbl = QLabel(description)
        d_lbl.setWordWrap(True)
        d_lbl.setStyleSheet("color: #666; font-size: 12px; margin-top: 10px; font-weight: 400;")
        layout.addWidget(d_lbl)
        
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked.emit()

class HomePage(QWidget):
    def __init__(self, nav_callback):
        super().__init__()
        self.nav_callback = nav_callback

        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(40)
        
        welcome_layout = QVBoxLayout()
        header = QLabel("STUDIO / 01")
        header.setStyleSheet("font-size: 40px; font-weight: 900; color: #fff; letter-spacing: -1px; border: none;")
        welcome_layout.addWidget(header)
        
        sub_header = QLabel("AI POWERED CONTENT ARCHITECTURE.")
        sub_header.setStyleSheet("font-size: 11px; color: #444; border: none; letter-spacing: 3px; font-weight: 700;")
        welcome_layout.addWidget(sub_header)
        layout.addLayout(welcome_layout)
        
        grid = QGridLayout()
        grid.setSpacing(20)
        
        tools = [
            ("News Feed", "Global intelligence ingestion.", "news"),
            ("Meme Gen", "Visual viral synthesis.", "meme"),
            ("History", "Archived production.", "history"),
            ("Chat AI", "Direct neural interaction.", "chat"),
            ("Knowledge", "Semantic memory retrieval.", "rag"),
            ("Settings", "System core configuration.", "settings"),
        ]
        
        row, col = 0, 0
        for title, desc, key in tools:
            card = ToolCard(title, desc)
            card.clicked.connect(lambda k=key: self.nav_callback(k))
            grid.addWidget(card, row, col)
            col += 1
            if col > 2:
                col = 0
                row += 1
                
        layout.addLayout(grid)
        layout.addStretch()