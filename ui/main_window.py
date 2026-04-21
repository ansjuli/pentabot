from PyQt5.QtWidgets import (
    QMainWindow, QWidget,
    QVBoxLayout, QTextEdit, QPushButton, QLabel
)
from PyQt5.QtCore import pyqtSignal


class PentabotUI(QMainWindow):
    # 🔥 Signals for thread-safe updates
    output_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.install_button = None
        self.init_ui()

        # Connect signals
        self.output_signal.connect(self.append_output)
        self.status_signal.connect(self.update_status)

    def init_ui(self):
        self.setWindowTitle("Pentabot")
        self.setGeometry(200, 100, 1000, 650)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout()

        # 🖥️ Output console
        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setStyleSheet("""
            background-color: black;
            color: #00aaff;
            font-family: Consolas;
            font-size: 14px;
        """)

        # 📊 Status
        self.status_label = QLabel("Idle")

        # 🎤 Button (not wired yet)
        self.voice_button = QPushButton("Start Voice Assistant")

        self.layout.addWidget(self.output_console)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.voice_button)

        central_widget.setLayout(self.layout)

    # =========================
    # 🔹 CORE DISPLAY METHODS
    # =========================

    def append_output(self, text):
        self.output_console.append(text)

    def update_status(self, text):
        self.status_label.setText(text)

    def safe_output(self, text):
        self.output_signal.emit(text)

    def safe_status(self, text):
        self.status_signal.emit(text)

    # =========================
    # 🔹 METHODS USED BY main.py
    # =========================

    def show_input(self, text):
        self.safe_output(f"> {text}")

    def show_message(self, text):
        self.safe_output(f"[Pentabot] {text}")

    def show_output(self, text):
        self.safe_output(text)

    # =========================
    # 🔘 INSTALL BUTTON
    # =========================

    def show_install_button(self, tool):
        # Prevent duplicates
        if self.install_button:
            return

        self.install_button = QPushButton(f"Install {tool}")
        self.install_button.clicked.connect(self.install_nmap)

        self.layout.addWidget(self.install_button)

    def install_nmap(self):
        import webbrowser
        webbrowser.open("https://nmap.org/download.html")
        self.safe_output("[Pentabot] Opening Nmap download page...")