from datetime import date, timedelta
from habit import Habit


def current_streak(checkin_dates, today=None):
    """Count consecutive check-in days ending today (or yesterday)."""
    if today is None:
        today = date.today()

    dates = set(checkin_dates)

    if today in dates:
        day = today
    elif today - timedelta(days=1) in dates:
        day = today - timedelta(days=1)
    else:
        return 0

    streak = 0
    while day in dates:
        streak += 1
        day -= timedelta(days=1)
    return streak


def longest_streak(checkin_dates):
    """Return the length of the longest run of consecutive check-in days."""
    if not checkin_dates:
        return 0

    dates = sorted(set(checkin_dates))

    longest = 1
    run = 1
    for i in range(1, len(dates)):
        if dates[i] - dates[i - 1] == timedelta(days=1):
            run += 1
        else:
            run = 1
        longest = max(longest, run)
    return longest


class HabitTracker:
    """Manages a collection of habits (a tracker HAS many habits)."""

    def __init__(self):
        self.habits = {}

    def add_habit(self, name):
        """Create a new habit. Raises ValueError if it already exists."""
        if name in self.habits:
            raise ValueError(f"Habit '{name}' already exists.")
        habit = Habit(name)
        self.habits[name] = habit
        return habit

    def get_habit(self, name):
        """Return the habit with this name. Raises ValueError if not found."""
        if name not in self.habits:
            raise ValueError(f"Habit '{name}' not found.")
        return self.habits[name]
