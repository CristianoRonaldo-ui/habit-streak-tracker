from habit import Habit


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