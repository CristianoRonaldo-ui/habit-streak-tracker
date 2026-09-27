from datetime import date

from storage import load_tracker, save_tracker
from tracker import HabitTracker


def test_save_and_load_round_trip(tmp_path):
    path = tmp_path / "habits.json"
    tracker = HabitTracker()
    reading = tracker.add_habit("Reading")
    reading.check_in(date(2026, 9, 25))
    reading.check_in(date(2026, 9, 26))
    tracker.add_habit("Gym")

    save_tracker(tracker, path)
    loaded = load_tracker(path)

    assert sorted(loaded.habits) == ["Gym", "Reading"]
    assert loaded.get_habit("Reading").checkin_dates == [date(2026, 9, 25), date(2026, 9, 26)]
    assert loaded.get_habit("Gym").checkin_dates == []


def test_load_missing_file_returns_empty_tracker(tmp_path):
    loaded = load_tracker(tmp_path / "does_not_exist.json")
    assert loaded.habits == {} 