from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QFrame
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class NewsDetailPage(QWidget):
    def __init__(self, text_service, image_service, meme_service, show_result):
        super().__init__()

        # services
        self.text_service = text_service
        self.image_service = image_service
        self.meme_service = meme_service
        self.show_result = show_result

        # layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header with back button
        header = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.back_btn.setFixedWidth(80)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #ecf0f1;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #bdc3c7;
            }
        """)
        header.addWidget(self.back_btn)
        header.addStretch()
        layout.addLayout(header)

        # title
        self.title_label = QLabel("Loading...")
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("font-size: 22px; font-weight: bold; color: #2c3e50;")

        # divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #ddd;")

        # content
        self.content_box = QTextEdit()
        self.content_box.setReadOnly(True)
        self.content_box.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: transparent;
                font-size: 15px;
                line-height: 1.6;
                color: #34495e;
            }
        """)

        # button
        self.generate_btn = QPushButton("Generate AI Meme from this News")
        self.generate_btn.setFixedHeight(50)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.generate_btn.setCursor(Qt.PointingHandCursor)
        self.generate_btn.clicked.connect(self.generate_meme)

        # status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #7f8c8d; font-style: italic;")

        # add widgets
        layout.addWidget(self.title_label)
        layout.addWidget(line)
        layout.addWidget(self.content_box, 1)
        layout.addWidget(self.generate_btn)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    # ------------------ Load news ------------------

    def load_news(self, news, news_service=None):
        self.news = news
        self.title_label.setText(news.get("title", "Untitled"))
        self.content_box.setText("Fetching content...")
        self.status_label.setText("")
        self.generate_btn.setEnabled(False)

        # In a real app, this should be in a thread
        if news_service and "url" in news:
            content = news_service.fetch_full_content(news["url"])
            if content:
                self.news["content"] = content
                self.content_box.setText(content)
                self.generate_btn.setEnabled(True)
            else:
                self.content_box.setText("Could not fetch full content. You can still try generating a meme from the title.")
                self.generate_btn.setEnabled(True)
        else:
            self.content_box.setText(news.get("content", "No content available."))
            self.generate_btn.setEnabled(True)

    # ------------------ Generate meme ------------------

    def generate_meme(self):
        self.status_label.setText("🤖 AI is thinking... (Generating text and image)")
        self.generate_btn.setEnabled(False)
        
        # This will block the UI, but let's keep it simple for now
        # Ideally use QThread
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()

        try:
            title = self.news.get("title", "")
            content = self.news.get("content", "")

            # 1. TEXT (Gemma)
            prompt = f"Create a funny meme caption for this news: {title}. Format: TOP: text BOTTOM: text"
            result = self.text_service.generate(prompt)

            # parse result
            top = ""
            bottom = ""

            for line in result.split("\n"):
                if "TOP:" in line:
                    top = line.replace("TOP:", "").strip()
                elif "BOTTOM:" in line:
                    bottom = line.replace("BOTTOM:", "").strip()

            # fallback
            if not top: top = title
            if not bottom: bottom = "True Story"

            # 2. IMAGE
            img_path = self.image_service.generate(title)

            # 3. MEME
            meme_path = self.meme_service.create_meme(img_path, top, bottom)

            self.status_label.setText("✨ Meme created successfully!")
            self.show_result(meme_path)

        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")
        
        self.generate_btn.setEnabled(True)