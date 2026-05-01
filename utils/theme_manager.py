class ThemeManager:
    @staticmethod
    def get_dark_theme():
        return """
            QMainWindow, QWidget {
                background-color: #0f172a;
                color: #f8fafc;
                font-family: 'Inter', -apple-system, sans-serif;
            }
            
            /* Sidebar Styling */
            Sidebar {
                background-color: #1e293b;
                border-right: 1px solid #334155;
            }
            Sidebar QPushButton {
                text-align: left;
                padding: 14px 20px;
                border: none;
                background: transparent;
                font-size: 14px;
                color: #94a3b8;
                border-radius: 8px;
                margin: 4px 10px;
            }
            Sidebar QPushButton:hover {
                background-color: #334155;
                color: #f8fafc;
            }
            Sidebar QPushButton:checked, Sidebar QPushButton:pressed {
                background-color: #3b82f6;
                color: white;
            }

            /* Buttons */
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:disabled {
                background-color: #334155;
                color: #64748b;
            }

            /* Inputs */
            QLineEdit, QTextEdit, QComboBox {
                background-color: #1e293b;
                border: 1px solid #334155;
                color: #f8fafc;
                border-radius: 6px;
                padding: 8px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #3b82f6;
            }

            /* ScrollBars */
            QScrollBar:vertical {
                border: none;
                background: #0f172a;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #334155;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            
            /* Cards */
            QFrame#card {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 12px;
            }
        """

    @staticmethod
    def get_light_theme():
        return """
            QMainWindow, QWidget {
                background-color: #f8fafc;
                color: #1e293b;
                font-family: 'Inter', -apple-system, sans-serif;
            }
            
            Sidebar {
                background-color: #ffffff;
                border-right: 1px solid #e2e8f0;
            }
            Sidebar QPushButton {
                text-align: left;
                padding: 14px 20px;
                border: none;
                background: transparent;
                font-size: 14px;
                color: #64748b;
                border-radius: 8px;
                margin: 4px 10px;
            }
            Sidebar QPushButton:hover {
                background-color: #f1f5f9;
                color: #1e293b;
            }

            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }

            QLineEdit, QTextEdit, QComboBox {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                color: #1e293b;
                border-radius: 6px;
                padding: 8px;
            }
        """
