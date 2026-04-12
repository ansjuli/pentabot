# modules/files/gui_list.py
import os  # ⚡ Fix: needed for basename
from PyQt5.QtWidgets import QApplication, QListWidget
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import sys

def show_file_list(category, files):
    # Only show file names, not full paths
    names = [os.path.basename(f) for f in files]

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    window = QListWidget()
    window.setWindowTitle(f"{category.upper()} files")
    window.resize(400, 600)

    # Translucent blue background
    window.setStyleSheet("""
        QListWidget {
            background-color: rgba(0, 120, 215, 180);
            color: white;
            font-size: 14px;
        }
    """)
    window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)

    for name in names:
        window.addItem(name)

    window.show()
    app.exec_()