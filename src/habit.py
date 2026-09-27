from datetime import date


class Habit:
    """Represents a single habit and the days it has been checked in"""

    def __init__(self, name):
        self.name = name
        self.checkin_dates = []

    def check_in(self, checkin_date=None):
        """Record a check-in for this habit. Defaults to today."""
        if checkin_date is None:
            checkin_date = date.today()

        if checkin_date not in self.checkin_dates:
            self.checkin_dates.append(checkin_date)
            self.checkin_dates.sort()

    def __str__(self):
        return f"{self.name} ({len(self.checkin_dates)} check-ins)"