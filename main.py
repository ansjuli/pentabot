from voice.voice_engine import listen
from brain.router import route
from tools.command_executor import execute

def main():
    print("[Pentabot] Starting...")

    while True:
        text = listen()

        if not text:
            continue

        print(f"[Heard]: {text}")

        decision = route(text)
        print(f"[Brain]: {decision}")

        result = execute(decision)
        print(f"[Result]: {result}")


if __name__ == "__main__":
    main()