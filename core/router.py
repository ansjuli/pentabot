from modules.system.system import handle as system_handle
from modules.system.app_opener import AppOpener
from core.command_executor import execute_command

app_opener = AppOpener()


def route(command_text):
    command_text = command_text.lower().strip()

    # ----------------------------
    # SYSTEM LAYER FIRST
    # ----------------------------
    system_result = system_handle(command_text)
    if system_result:
        return system_result

    # ----------------------------
    # COMMAND EXECUTOR LAYER
    # ----------------------------
    result = execute_command(command_text)
    if result:
        return result

    # ----------------------------
    # APP LAYER (FINAL FALLBACK)
    # ----------------------------
    app_result = app_opener.open_app(command_text)
    if app_result:
        return f"Opened app: {command_text}"

    return None