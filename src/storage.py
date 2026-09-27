import json

DEFAULT_PATH = "habits_data.json"


def save_tracker(tracker, path=DEFAULT_PATH):
    """Save all habits and their check-in dates to a JSON file."""
    data = {}
    for name, habit in tracker.habits.items():
        data[name] = [d.isoformat() for d in habit.checkin_dates]

    with open(path, "w") as file:
        json.dump(data, file, indent=2) 
        