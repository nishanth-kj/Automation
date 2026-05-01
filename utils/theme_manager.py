class ThemeManager:
    @staticmethod
    def get_light_theme():
        return """
            QWidget {
                background-color: #f5f5f5;
                color: #333;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #ddd;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #eee;
            }
            QLineEdit, QTextEdit {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
            QScrollArea {
                border: none;
            }
            QLabel#header {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
            }
        """

    @staticmethod
    def get_dark_theme():
        return """
            QWidget {
                background-color: #121212;
                color: #e0e0e0;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton {
                background-color: #2a2a2a;
                border: 1px solid #444;
                color: #fff;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QLineEdit, QTextEdit {
                background-color: #1e1e1e;
                border: 1px solid #333;
                color: #fff;
                border-radius: 4px;
                padding: 5px;
            }
            QScrollArea {
                border: none;
            }
            QLabel#header {
                font-size: 18px;
                font-weight: bold;
                color: #3498db;
            }
        """
