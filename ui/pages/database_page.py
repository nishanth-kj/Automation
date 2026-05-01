from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QPushButton, QTextEdit, QLabel, QSplitter
from PySide6.QtCore import Qt
from sqlalchemy import text
from repository.database.db import engine
from utils.logger import logger

class DatabasePage(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Database Explorer"))
        
        # Splitter
        splitter = QSplitter(Qt.Vertical)
        
        # Upper Section: Table Viewer
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        
        controls = QHBoxLayout()
        self.table_selector = QComboBox()
        self.refresh_tables()
        controls.addWidget(QLabel("Table:"))
        controls.addWidget(self.table_selector)
        
        self.view_btn = QPushButton("View Data")
        self.view_btn.clicked.connect(self.load_table_data)
        controls.addWidget(self.view_btn)
        controls.addStretch()
        
        top_layout.addLayout(controls)
        
        self.data_table = QTableWidget()
        top_layout.addWidget(self.data_table)
        
        # Lower Section: Raw Query
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.addWidget(QLabel("Run Raw SQL Query:"))
        
        self.query_edit = QTextEdit()
        self.query_edit.setPlaceholderText("SELECT * FROM news LIMIT 10")
        bottom_layout.addWidget(self.query_edit)
        
        self.run_btn = QPushButton("Execute SQL")
        self.run_btn.setStyleSheet("background-color: #e67e22;")
        self.run_btn.clicked.connect(self.run_custom_query)
        bottom_layout.addWidget(self.run_btn)
        
        splitter.addWidget(top_widget)
        splitter.addWidget(bottom_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        
        layout.addWidget(splitter)

    def refresh_tables(self):
        try:
            with engine.connect() as conn:
                result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                tables = [row[0] for row in result]
                self.table_selector.clear()
                self.table_selector.addItems(tables)
        except Exception as e:
            logger.error(f"Failed to fetch tables: {e}")

    def load_table_data(self):
        table_name = self.table_selector.currentText()
        if not table_name: return
        self.execute_and_display(f"SELECT * FROM {table_name} LIMIT 100")

    def run_custom_query(self):
        query = self.query_edit.toPlainText().strip()
        if not query: return
        self.execute_and_display(query)

    def execute_and_display(self, query):
        try:
            with engine.connect() as conn:
                result = conn.execute(text(query))
                
                # Setup headers
                columns = result.keys()
                self.data_table.setColumnCount(len(columns))
                self.data_table.setHorizontalHeaderLabels(columns)
                
                # Load data
                rows = result.fetchall()
                self.data_table.setRowCount(len(rows))
                for r_idx, row in enumerate(rows):
                    for c_idx, val in enumerate(row):
                        self.data_table.setItem(r_idx, c_idx, QTableWidgetItem(str(val)))
                
                logger.info(f"DB Explorer: Executed query successfully. Rows: {len(rows)}")
        except Exception as e:
            logger.error(f"SQL Error: {e}")
            self.query_edit.append(f"\n-- ERROR: {str(e)}")
