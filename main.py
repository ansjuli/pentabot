import sys
import threading
from PyQt5.QtWidgets import QApplication

from brain.router import route
from tools.command_executor import execute
from voice.voice_engine import listen
from voice.tts import speak
from ui.main_window import PentabotUI


class Pentabot:
    def __init__(self):
        self.ui = PentabotUI()
        self.ui.show()

        # 🔥 Voice control state
        self.voice_active = False

        # Connect UI button
        self.ui.voice_button.clicked.connect(self.toggle_voice)

    # =========================
    # 🎤 VOICE CONTROL
    # =========================
    def toggle_voice(self):
        self.voice_active = not self.voice_active

        if self.voice_active:
            self.ui.safe_status("Listening...")
            self.ui.voice_button.setText("Stop Voice Assistant")

            # Start thread ONLY when activated
            threading.Thread(target=self.voice_loop, daemon=True).start()

        else:
            self.ui.safe_status("Idle")
            self.ui.voice_button.setText("Start Voice Assistant")

    # =========================
    # 🔁 VOICE LOOP (controlled)
    # =========================
    def voice_loop(self):
        while self.voice_active:

            text = listen()
            if not text:
                continue

            self.ui.show_input(text)
            self.ui.safe_status("Processing...")

            decision = route(text)
            result = execute(decision)

            self.handle_result(result)

            if self.voice_active:
                self.ui.safe_status("Listening...")

    # =========================
    # 🧠 RESULT HANDLER (clean separation)
    # =========================
    def handle_result(self, result):
        status = result.get("status")
        message = result.get("message")
        tool = result.get("tool")

        # ❌ Missing dependency
        if status == "missing":
            self.ui.show_message(message)
            self.ui.show_install_button(tool)
            speak(f"{tool} is not installed")

        # 🟡 Action (install)
        elif status == "action":
            self.ui.show_message(message)
            speak(message)

        # 🟢 Ready (execute tool)
        elif status == "ready":

            if tool == "nmap":
                self.ui.safe_status("Scanning...")
                speak("Scanning network")

                from tools.nmap_tool import run_nmap_scan
                output = run_nmap_scan()

                self.ui.show_output(output)

        # 🔵 Done
        elif status == "done":
            self.ui.show_output(message)

        # ⚠️ Unknown
        else:
            self.ui.show_message(message)
            speak("Command not recognized")


# =========================
# 🚀 ENTRY POINT
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    bot = Pentabot()

    sys.exit(app.exec_())