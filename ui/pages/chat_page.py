from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
from services.text_service import TextService

class ChatPage(QWidget):
    def __init__(self):
        super().__init__()
        self.text_service = TextService()
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Chat with Gemma AI"))
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask Gemma anything...")
        self.input_field.returnPressed.connect(self.send_message)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        layout.addLayout(input_layout)
        
        self.setLayout(layout)

    def send_message(self):
        msg = self.input_field.text().strip()
        if not msg: return
        
        self.chat_display.append(f"<b>You:</b> {msg}")
        self.input_field.clear()
        
        # Async-ish call (for UI responsiveness)
        from PySide6.QtWidgets import QApplication
        QApplication.processEvents()
        
        try:
            response = self.text_service.generate(msg)
            self.chat_display.append(f"<b>Gemma:</b> {response}")
        except Exception as e:
            self.chat_display.append(f"<b>Error:</b> {str(e)}")
        
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())
