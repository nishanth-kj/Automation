from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QFrame
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt


class NewsDetailPage(QWidget):
    def __init__(self, text_service, image_service, meme_service, show_result):
        super().__init__()

        self.text_service = text_service
        self.image_service = image_service
        self.meme_service = meme_service
        self.show_result = show_result

        layout = QVBoxLayout()

        self.back_btn = QPushButton("Back")
        self.title_label = QLabel("Title")
        self.content_box = QTextEdit()
        self.content_box.setReadOnly(True)
        self.generate_btn = QPushButton("Create Meme")
        self.status_label = QLabel("")

        layout.addWidget(self.back_btn)
        layout.addWidget(self.title_label)
        layout.addWidget(self.content_box)
        layout.addWidget(self.generate_btn)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.generate_btn.clicked.connect(self.generate_meme)


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