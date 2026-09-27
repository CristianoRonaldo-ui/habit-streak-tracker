import json
import os
from datetime import date

from tracker import HabitTracker

DEFAULT_PATH = "habits_data.json"


def save_tracker(tracker, path=DEFAULT_PATH):
    """Save all habits and their check-in dates to a JSON file."""
    data = {}
    for name, habit in tracker.habits.items():
        data[name] = [d.isoformat() for d in habit.checkin_dates]

    with open(path, "w") as file:
        json.dump(data, file, indent=2)


def load_tracker(path=DEFAULT_PATH):
    """Load habits from a JSON file. Returns an empty tracker if the file is missing"""
    tracker = HabitTracker()
    if not os.path.exists(path):
        return tracker

    with open(path, "r") as file:
        data = json.load(file)

    for name, date_strings in data.items():
        habit = tracker.add_habit(name)
        for s in date_strings:
            habit.check_in(date.fromisoformat(s))
    return tracker
