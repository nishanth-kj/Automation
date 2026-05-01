from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QScrollArea, QLabel, QHBoxLayout, QGridLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from repository.meme_repository import MemeRepository
from utils.logger import logger

class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.meme_repo = MemeRepository()
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Meme History"))
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.grid = QGridLayout(self.scroll_content)
        self.scroll.setWidget(self.scroll_content)
        
        layout.addWidget(self.scroll)
        
        self.refresh_btn = QPushButton("Refresh History")
        self.refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(self.refresh_btn)
        
        self.setLayout(layout)
        self.load_history()

    def load_history(self):
        # Clear grid
        for i in reversed(range(self.grid.count())): 
            widget = self.grid.itemAt(i).widget()
            if widget: widget.setParent(None)
            
        page_obj = self.meme_repo.get_all(size=50)
        memes = page_obj.content
        
        row = 0
        col = 0
        for meme in memes:
            container = QFrame()
            container.setFrameShape(QFrame.StyledPanel)
            vbox = QVBoxLayout(container)
            
            img_lbl = QLabel()
            pixmap = QPixmap(meme.image_path)
            if not pixmap.isNull():
                img_lbl.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                img_lbl.setText("No Image")
            
            vbox.addWidget(img_lbl)
            vbox.addWidget(QLabel(meme.headline[:30] + "..."))
            
            self.grid.addWidget(container, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

from PySide6.QtWidgets import QFrame
