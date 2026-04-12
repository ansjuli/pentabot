# modules/control.py
from core.router import route

def handle(command_text):
    response = route(command_text)
    return response  # Always a string