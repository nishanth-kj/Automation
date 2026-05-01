from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from services.text_service import TextService
from services.meme_service import MemeService
from services.image_generate_service import ImageGenerateService

class MemePage(QWidget):
    def __init__(self):
        super().__init__()

        self.text_service = TextService()
        self.meme_service = MemeService()
        self.image_service = ImageGenerateService()

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("AI Custom Meme Generator")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Describe the meme you want (e.g., 'doge at a computer')")
        self.input.setFixedHeight(45)
        self.input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)

        self.button = QPushButton("Generate Meme")
        self.button.setFixedHeight(50)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.button.clicked.connect(self.run)

        # Result display
        self.result_container = QFrame()
        self.result_container.setStyleSheet("background-color: #f1f2f6; border-radius: 12px;")
        result_layout = QVBoxLayout(self.result_container)
        
        self.image_label = QLabel("Your meme will appear here")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        self.image_label.setMinimumHeight(300)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        result_layout.addWidget(self.image_label)
        result_layout.addWidget(self.status_label)

        layout.addWidget(self.input)
        layout.addWidget(self.button)
        layout.addWidget(self.result_container, 1)

        self.setLayout(layout)

    def run(self):
        topic = self.input.text().strip()

        if not topic:
            self.status_label.setText("⚠️ Please enter a topic")
            return

        self.status_label.setText("🎨 AI is creating your meme...")
        self.button.setEnabled(False)
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()

        try:
            # 1. Generate text
            prompt = f"Create a funny meme caption for: {topic}. Format: TOP: text BOTTOM: text"
            result = self.text_service.generate(prompt)
            
            top = ""
            bottom = ""
            for line in result.split("\n"):
                if "TOP:" in line: top = line.replace("TOP:", "").strip()
                elif "BOTTOM:" in line: bottom = line.replace("BOTTOM:", "").strip()
            
            if not top: top = topic
            if not bottom: bottom = "Logic"

            # 2. Generate image
            img_path = self.image_service.generate(topic)

            # 3. Create meme
            meme_path = self.meme_service.create_meme(img_path, top, bottom)

            self.show_result(meme_path)
            self.status_label.setText("✅ Meme generated!")

        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")
        
        self.button.setEnabled(True)

    def show_result(self, meme_path):
        pixmap = QPixmap(meme_path)
        # scale pixmap to fit label while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(
            self.image_label.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setStyleSheet("border: none;")