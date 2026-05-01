class ThemeManager:
    @staticmethod
    def get_dark_theme():
        return """
            QMainWindow, QWidget {
                background-color: #000000;
                color: #ffffff;
                font-family: 'Inter', -apple-system, sans-serif;
            }
            
            Sidebar {
                background-color: #000000;
                border-right: 1px solid #222;
            }
            Sidebar QPushButton {
                text-align: left;
                padding: 14px 20px;
                border: none;
                background: transparent;
                font-size: 13px;
                color: #888;
                border-radius: 0px;
                margin: 0;
            }
            Sidebar QPushButton:hover {
                background-color: #111;
                color: #fff;
            }
            Sidebar QPushButton:checked {
                background-color: #111;
                color: #fff;
                border-left: 2px solid #fff;
            }

            QPushButton {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #ffffff;
                padding: 10px 20px;
                border-radius: 0px;
                font-weight: 700;
                text-transform: uppercase;
                font-size: 11px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #000000;
                color: #ffffff;
            }
            QPushButton:disabled {
                background-color: #111;
                color: #444;
                border: 1px solid #222;
            }

            QLineEdit, QTextEdit, QComboBox {
                background-color: #000000;
                border: 1px solid #333;
                color: #ffffff;
                border-radius: 0px;
                padding: 10px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #fff;
            }

            QScrollBar:vertical {
                border: none;
                background: #000;
                width: 8px;
            }
            QScrollBar::handle:vertical {
                background: #333;
                border-radius: 0px;
            }
            
            QFrame#card {
                background-color: #000;
                border: 1px solid #222;
                border-radius: 0px;
            }
            QFrame#news_card {
                background-color: #000;
                border-bottom: 1px solid #111;
                border-radius: 0px;
            }
        """

    @staticmethod
    def get_light_theme():
        return """
            QMainWindow, QWidget {
                background-color: #ffffff;
                color: #000000;
                font-family: 'Inter', -apple-system, sans-serif;
            }
            
            Sidebar {
                background-color: #f9f9f9;
                border-right: 1px solid #eee;
            }
            Sidebar QPushButton {
                text-align: left;
                padding: 14px 20px;
                border: none;
                background: transparent;
                font-size: 13px;
                color: #666;
            }
            Sidebar QPushButton:hover {
                background-color: #eee;
                color: #000;
            }
            Sidebar QPushButton:checked {
                background-color: #eee;
                color: #000;
                border-left: 2px solid #000;
            }

            QPushButton {
                background-color: #000000;
                color: #ffffff;
                border: 1px solid #000;
                padding: 10px 20px;
                border-radius: 0px;
                font-weight: 700;
                text-transform: uppercase;
                font-size: 11px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #ffffff;
                color: #000000;
            }

            QLineEdit, QTextEdit, QComboBox {
                background-color: #ffffff;
                border: 1px solid #eee;
                color: #000000;
                border-radius: 0px;
                padding: 10px;
            }
        """
