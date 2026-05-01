from PySide6.QtWidgets import QTextEdit
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

class ConsoleWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                border: none;
                border-top: 1px solid #333;
            }
        """)
        self.setPlaceholderText("System logs will appear here...")

    def append_log(self, message):
        self.append(message)
        # Auto scroll to bottom
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
