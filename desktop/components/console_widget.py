from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel
from PySide6.QtCore import QObject, Signal, Qt
import logging

class LogSignal(QObject):
    new_log = Signal(str)

class QtLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.signal = LogSignal()

    def emit(self, record):
        msg = self.format(record)
        self.signal.new_log.emit(msg)

class ConsoleWidget(QWidget):
    close_requested = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        header = QWidget()
        header.setFixedHeight(30)
        header.setStyleSheet("background-color: #333; color: #ccc;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 0, 5, 0)
        
        title = QLabel("SYSTEM LOGS")
        title.setStyleSheet("font-size: 10px; font-weight: bold; color: #aaa;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Clear Button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setFixedSize(50, 20)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #444;
                border: none;
                color: #ccc;
                font-size: 10px;
                border-radius: 2px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_logs)
        header_layout.addWidget(self.clear_btn)

        # Close Button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setStyleSheet("border: none; font-size: 18px; color: #999; margin-left: 5px;")
        self.close_btn.clicked.connect(self.close_requested.emit)
        header_layout.addWidget(self.close_btn)
        
        layout.addWidget(header)

        # Log Area
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                border: none;
            }
        """)
        layout.addWidget(self.text_edit)

    def append_log(self, message):
        self.text_edit.append(message)
        self.text_edit.verticalScrollBar().setValue(self.text_edit.verticalScrollBar().maximum())

    def clear_logs(self):
        self.text_edit.clear()
