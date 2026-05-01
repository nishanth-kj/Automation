from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTextEdit, QComboBox, QHBoxLayout
from repository.setting_repository import SettingRepository

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.repo = SettingRepository()
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Application Settings"))

        # Theme Setting
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("UI Theme:"))
        self.theme_box = QComboBox()
        self.theme_box.addItems(["Dark", "Light"])
        current_theme = self.repo.get("theme", "dark").capitalize()
        self.theme_box.setCurrentText(current_theme)
        theme_layout.addWidget(self.theme_box)
        layout.addLayout(theme_layout)

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
        self.setLayout(layout)

    def save(self):
        self.repo.set("theme", self.theme_box.currentText().lower())
        self.repo.set("meme_prompt", self.prompt_edit.toPlainText())
        self.repo.set("selection_prompt", self.selection_prompt.toPlainText())
        self.status.setText("✅ Settings saved! Restart or re-open to see full effects.")
        
        # Trigger theme apply in MainWindow if possible
        from ui.main_window import MainWindow
        from PySide6.QtWidgets import QApplication
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.apply_theme()
