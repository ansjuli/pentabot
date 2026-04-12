from datetime import datetime
from .calendar import EchoCalendar

calendar = EchoCalendar()

def handle_calendar_command(command):
    command = command.lower()
    today = datetime.now().strftime("%Y-%m-%d")

    if "next" in command and "event" in command:
        return calendar.next_event()

    elif "today" in command and "event" in command:
        return calendar.get_events_by_date(today)

    elif "add" in command or "schedule" in command:
        try:
            title = command
            date_str = today
            time_str = "12:00"

            if "on" in command:
                parts = command.split("on")
                title = parts[0].replace("schedule","").replace("add","").strip()
                date_str = parts[1].strip().split()[0]

            if "at" in command:
                parts = command.split("at")
                title = parts[0].replace("schedule","").replace("add","").strip()
                time_part = parts[1].split()[0]
                time_str = "12:00" if "noon" in time_part else time_part

            return calendar.add_event(title, date_str, time_str)
        except:
            return "Sorry, I couldn't understand the event details."

    return None