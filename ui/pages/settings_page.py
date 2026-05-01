from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QComboBox, QCheckBox, QTabWidget, QPushButton
from repository.setting_repository import SettingRepository
from ui.pages.database_page import DatabasePage

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.repo = SettingRepository()
        
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Settings & Data Management"))
        
        self.tabs = QTabWidget()
        
        # Tab 1: General Settings
        self.general_tab = QWidget()
        self.setup_general_tab()
        
        # Tab 2: Database Explorer
        self.db_tab = DatabasePage()
        
        self.tabs.addTab(self.general_tab, "General")
        self.tabs.addTab(self.db_tab, "Database Explorer")
        
        layout.addWidget(self.tabs)

    def setup_general_tab(self):
        layout = QVBoxLayout(self.general_tab)
        
        # Theme Setting
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("UI Theme:"))
        self.theme_box = QComboBox()
        self.theme_box.addItems(["Dark", "Light"])
        current_theme = self.repo.get("theme", "dark").capitalize()
        self.theme_box.setCurrentText(current_theme)
        theme_layout.addWidget(self.theme_box)
        layout.addLayout(theme_layout)

        # Log Toggle
        self.log_toggle = QCheckBox("Show System Logs Console")
        current_logs = self.repo.get("show_logs", "true") == "true"
        self.log_toggle.setChecked(current_logs)
        layout.addWidget(self.log_toggle)

        # Meme Prompt
        layout.addWidget(QLabel("Meme Generation Prompt:"))
        self.prompt_edit = QTextEdit()
        current_prompt = self.repo.get("meme_prompt", "Create a funny meme caption for this news: {title}. Format: TOP: text BOTTOM: text")
        self.prompt_edit.setText(current_prompt)
        layout.addWidget(self.prompt_edit)

        # AI Selection Prompt
        layout.addWidget(QLabel("AI News Selection Prompt:"))
        self.selection_prompt = QTextEdit()
        current_sel = self.repo.get("selection_prompt", "From the following news titles, select the 3 most viral/funny ones. Return only the titles separated by |.")
        self.selection_prompt.setText(current_sel)
        layout.addWidget(self.selection_prompt)

        self.save_btn = QPushButton("Save & Apply Settings")
        self.save_btn.clicked.connect(self.save)
        layout.addWidget(self.save_btn)
        
        self.status = QLabel("")
        layout.addWidget(self.status)
        layout.addStretch()

    def save(self):
        self.repo.set("theme", self.theme_box.currentText().lower())
        self.repo.set("show_logs", "true" if self.log_toggle.isChecked() else "false")
        self.repo.set("meme_prompt", self.prompt_edit.toPlainText())
        self.repo.set("selection_prompt", self.selection_prompt.toPlainText())
        self.status.setText("✅ Settings saved!")
        
        # Trigger updates in MainWindow
        from ui.main_window import MainWindow
        from PySide6.QtWidgets import QApplication
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.apply_settings()
