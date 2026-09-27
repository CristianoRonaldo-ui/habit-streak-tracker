from datetime import date

import pytest

from tracker import HabitTracker, current_streak, longest_streak

DATES = [
    date(2026, 9, 20),
    date(2026, 9, 21),
    date(2026, 9, 24),
    date(2026, 9, 25),
    date(2026, 9, 26),
]


def test_current_streak_counts_back_from_today():
    assert current_streak(DATES, today=date(2026, 9, 26)) == 3


def test_current_streak_survives_until_end_of_today():
    assert current_streak(DATES, today=date(2026, 9, 27)) == 3


def test_current_streak_resets_after_missed_day():
    assert current_streak(DATES, today=date(2026, 9, 28)) == 0


def test_current_streak_empty_list():
    assert current_streak([], today=date(2026, 9, 26)) == 0


def test_longest_streak_finds_past_run():
    dates = [
        date(2026, 9, 10),
        date(2026, 9, 11),
        date(2026, 9, 12),
        date(2026, 9, 13),
        date(2026, 9, 20),
        date(2026, 9, 21),
    ]
    assert longest_streak(dates) == 4


def test_longest_streak_ignores_order_and_duplicates():
    dates = [date(2026, 9, 3), date(2026, 9, 1), date(2026, 9, 2), date(2026, 9, 2)]
    assert longest_streak(dates) == 3


def test_longest_streak_empty_list():
    assert longest_streak([]) == 0


def test_get_stats_summarises_habit():
    tracker = HabitTracker()
    habit = tracker.add_habit("Gym")
    habit.check_in(date(2026, 9, 25))
    habit.check_in(date(2026, 9, 26))
    habit.check_in(date(2026, 9, 26))

    stats = tracker.get_stats("Gym", today=date(2026, 9, 27))

    assert stats == {
        "name": "Gym",
        "total_checkins": 2,
        "current_streak": 2,
        "longest_streak": 2,
    }


def test_get_stats_unknown_habit_raises():
    tracker = HabitTracker()
    with pytest.raises(ValueError):
        tracker.get_stats("Swimming")
