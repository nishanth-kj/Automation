from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QProgressBar
from services.rag_service import RagService
from services.text_service import TextService
from PySide6.QtCore import QThread, Signal

class IndexWorker(QThread):
    finished = Signal(int)
    error = Signal(str)

    def __init__(self, rag_service):
        super().__init__()
        self.rag_service = rag_service

    def run(self):
        try:
            count = self.rag_service.build_index()
            self.finished.emit(count)
        except Exception as e:
            self.error.emit(str(e))

class RagPage(QWidget):
    def __init__(self):
        super().__init__()
        self.rag_service = RagService()
        self.text_service = TextService()
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("RAG Knowledge Base (AI Memory)"))
        
        # Index Section
        self.status_lbl = QLabel("Index status: Unknown")
        layout.addWidget(self.status_lbl)
        
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        layout.addWidget(self.progress)
        
        self.build_btn = QPushButton("Rebuild AI Index from News Database")
        self.build_btn.clicked.connect(self.start_indexing)
        layout.addWidget(self.build_btn)

        # Search Section
        layout.addSpacing(20)
        layout.addWidget(QLabel("Semantic AI Search (Talk to your News):"))
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter a topic or question...")
        self.query_input.returnPressed.connect(self.run_search)
        layout.addWidget(self.query_input)
        
        self.search_btn = QPushButton("Query RAG AI")
        self.search_btn.clicked.connect(self.run_search)
        layout.addWidget(self.search_btn)
        
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        layout.addWidget(self.result_display)

        self.setLayout(layout)

    def start_indexing(self):
        self.build_btn.setEnabled(False)
        self.progress.show()
        self.status_lbl.setText("🔄 AI is indexing your news database...")
        
        self.worker = IndexWorker(self.rag_service)
        self.worker.finished.connect(self.on_index_finished)
        self.worker.error.connect(self.on_index_error)
        self.worker.start()

    def on_index_finished(self, count):
        self.build_btn.setEnabled(True)
        self.progress.hide()
        self.status_lbl.setText(f"✅ AI Index Ready! ({count} articles indexed)")

    def on_index_error(self, err):
        self.build_btn.setEnabled(True)
        self.progress.hide()
        self.status_lbl.setText(f"❌ Error during indexing: {err}")

    def run_search(self):
        query = self.query_input.text().strip()
        if not query: return
        
        self.result_display.setText("🔎 Searching AI knowledge base...")
        results = self.rag_service.search(query)
        
        if not results:
            self.result_display.setText("No relevant news found in index.")
            return
            
        # Build Context for Gemma
        context_parts = []
        for sim, meta in results:
            context_parts.append(f"- {meta['title']} (Source: {meta['source']})")
        
        context_str = "\n".join(context_parts)
        
        # Ask Gemma to summarize based on RAG
        prompt = f"Based on the following news found in my database, answer this: {query}\n\nRelevant News:\n{context_str}\n\nAI Response:"
        
        try:
            response = self.text_service.generate(prompt)
            final_text = f"<b>Context from Database:</b>\n{context_str}\n\n<b>AI Summary:</b>\n{response}"
            self.result_display.setHtml(final_text)
        except Exception as e:
            self.result_display.setText(f"Error generating AI summary: {e}")
