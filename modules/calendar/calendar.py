import os
import json
from datetime import datetime

EVENTS_FILE = os.path.join(os.path.dirname(__file__), "events.json")

class EchoCalendar:
    def __init__(self):
        self.events = self.load_events()
        self.clear_past_events()

    def load_events(self):
        if os.path.exists(EVENTS_FILE):
            try:
                with open(EVENTS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_events(self):
        self.clear_past_events()
        with open(EVENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=4)

    def clear_past_events(self):
        now = datetime.now()
        self.events = [
            e for e in self.events
            if datetime.strptime(f"{e['date']} {e['time']}", "%Y-%m-%d %H:%M") >= now
        ]

    def add_event(self, title, date_str, time_str):
        self.events.append({"title": title, "date": date_str, "time": time_str})
        self.save_events()
        return f"Event '{title}' scheduled for {date_str} at {time_str}."

    def get_events_by_date(self, date_str):
        events_today = [e for e in self.events if e["date"] == date_str]
        if events_today:
            return "\n".join([f"{e['time']} - {e['title']}" for e in events_today])
        return "No events for today."

    def next_event(self):
        now = datetime.now()
        future = [
            e for e in self.events
            if datetime.strptime(f"{e['date']} {e['time']}", "%Y-%m-%d %H:%M") > now
        ]
        if not future:
            return "No upcoming events."
        next_e = min(future, key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M"))
        return f"Next event: {next_e['title']} on {next_e['date']} at {next_e['time']}"