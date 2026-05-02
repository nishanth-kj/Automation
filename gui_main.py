import sys
import os
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QLockFile, QDir
from ui.main_window import MainWindow
from repository.database.init_db import init_db

def main():
    # Ensure database is initialized before starting
    try:
        init_db()
    except Exception as e:
        print(f"Error initializing database: {e}")

    app = QApplication(sys.argv)
    
    # Use a lock file in the temporary directory to prevent multiple instances
    lock_path = os.path.join(QDir.tempPath(), "ai_news_meme_studio.lock")
    lock_file = QLockFile(lock_path)
    
    if not lock_file.tryLock(100):
        # Could not lock, another instance is probably running
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Another instance of AI News Meme Studio is already running.")
        msg.setWindowTitle("Already Running")
        msg.exec()
        sys.exit(1)

    window = MainWindow()
    window.show()
    
    # Keep the lock_file object alive as long as the app is running
    sys.exit(app.exec())

if __name__ == "__main__":
    main()