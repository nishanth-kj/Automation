from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QFrame
from PySide6.QtGui import QFont, QPixmap, QDesktopServices
from PySide6.QtCore import Qt, QUrl
import requests
import io

class NewsDetailPage(QWidget):
    def __init__(self, text_service, image_service, meme_service, show_result, view_web_callback):
        super().__init__()

        self.text_service = text_service
        self.image_service = image_service
        self.meme_service = meme_service
        self.show_result = show_result
        self.view_web_callback = view_web_callback

        from repository.meme_repository import MemeRepository
        self.meme_repo = MemeRepository()

        layout = QVBoxLayout()

        # Header
        header = QHBoxLayout()
        self.back_btn = QPushButton("Back")
        self.source_label = QLabel("Source: Unknown")
        header.addWidget(self.back_btn)
        header.addStretch()
        header.addWidget(self.source_label)
        layout.addLayout(header)

        # Title
        self.title_label = QLabel("Title")
        self.title_label.setWordWrap(True)
        self.title_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.title_label)

        # Image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(200)
        self.image_label.setStyleSheet("background-color: #ddd;")
        layout.addWidget(self.image_label)

        # Content
        self.content_box = QTextEdit()
        self.content_box.setReadOnly(True)
        layout.addWidget(self.content_box)

        # Link
        self.link_btn = QPushButton("Open Original Article")
        layout.addWidget(self.link_btn)

        # Action
        self.generate_btn = QPushButton("Create Meme")
        self.status_label = QLabel("")
        layout.addWidget(self.generate_btn)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        
        self.generate_btn.clicked.connect(self.generate_meme)
        self.link_btn.clicked.connect(self.open_link)

    def open_link(self):
        url = self.news.get("url")
        if url:
            self.view_web_callback(url)


    def load_news(self, news, news_service=None):
        self.news = news
        self.title_label.setText(news.get("title", "Untitled"))
        self.source_label.setText(f"Source: {news.get('source', 'Unknown')}")
        self.content_box.setText("Fetching content...")
        self.image_label.clear()
        self.image_label.setText("Loading image...")
        self.status_label.setText("")
        self.generate_btn.setEnabled(False)

        # Load thumbnail if available immediately
        if news.get("image_url"):
            self._display_image(news["image_url"])

        if news_service and "url" in news:
            data = news_service.fetch_full_content(news["url"])
            content = data.get("content", "")
            full_image = data.get("image_url")
            resolved_url = data.get("url")
            
            if resolved_url:
                self.news["url"] = resolved_url

            if content:
                self.news["content"] = content
                self.content_box.setText(content)
            else:
                self.content_box.setText("Could not fetch full content. You can still try generating a meme from the title.")

            if full_image:
                self.news["image_url"] = full_image
                self._display_image(full_image)
            
            self.generate_btn.setEnabled(True)
        else:
            self.content_box.setText(news.get("content", "No content available."))
            self.generate_btn.setEnabled(True)

    def _display_image(self, url):
        try:
            res = requests.get(url, timeout=5)
            pixmap = QPixmap()
            pixmap.loadFromData(res.content)
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.image_label.setText("No Image Available")
        except:
            self.image_label.setText("Failed to load image")

    def generate_meme(self):
        self.status_label.setText("🤖 AI is thinking... (Generating text and image)")
        self.generate_btn.setEnabled(False)
        
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()

        try:
            title = self.news.get("title", "")
            
            # 1. TEXT (Gemma)
            prompt = f"Create a funny meme caption for this news: {title}. Format: TOP: text BOTTOM: text"
            result = self.text_service.generate(prompt)

            top = ""
            bottom = ""
            for line in result.split("\n"):
                if "TOP:" in line:
                    top = line.replace("TOP:", "").strip()
                elif "BOTTOM:" in line:
                    bottom = line.replace("BOTTOM:", "").strip()

            if not top: top = title
            if not bottom: bottom = "True Story"

            # 2. IMAGE
            img_path = self.image_service.generate(title)

            # 3. MEME
            meme_path = self.meme_service.create_meme(img_path, top, bottom)

            # 4. SAVE TO DB
            self.meme_repo.create(title, top, bottom, meme_path)

            self.status_label.setText("✨ Meme created successfully!")
            self.show_result(meme_path)


        except Exception as e:
            self.status_label.setText(f"❌ Error: {str(e)}")
        
        self.generate_btn.setEnabled(True)