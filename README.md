# Habit Streak Tracker

A command-line habit tracker that records daily check-ins and calculates your **current streak** and **longest streak** for each habit. Data is saved to a local JSON file, so your history is kept between runs.

## Features

- Add habits and check in daily, or for a past date with `--date`
- Current streak with a grace period: a streak stays alive until the end of today
- Longest streak across your full history, even after a streak has ended
- JSON persistence with safe handling of a missing data file
- Clear error messages for unknown habits, invalid dates, and future dates
- 11 pytest tests covering streak logic, edge cases, and save/load round trips

## Getting Started

Requires Python 3.8 or newer

```bash
git clone https://github.com/CristianoRonaldo-ui/habit-streak-tracker.git
cd habit-streak-tracker
python3 -m pip install -r requirements.txt
```

## Usage

```bash
python3 src/cli.py add Reading
python3 src/cli.py checkin Reading
python3 src/cli.py checkin Reading --date 2026-09-25
python3 src/cli.py stats Reading
python3 src/cli.py list
```

Run the tests:

```bash
python3 -m pytest -v
``` 
## Example

```
$ python3 src/cli.py stats Reading
Habit: Reading
Total check-ins: 3
Current streak: 3 day(s)
Longest streak: 3 day(s)

$ python3 src/cli.py list
Gym: 0 day streak (best: 0)
Reading: 3 day streak (best: 3)

$ python3 src/cli.py checkin Reading --date 2030-01-01
Error: Cannot check in for a future date
```

## How It Works

**Current streak — O(n).** Start from today (or yesterday, if today has no check-in yet) and walk backwards one day at a time, counting while the day is in the check-in set. Dates are stored in a `set`, so each lookup is O(1) on average

**Longest streak — O(n log n).** Sort the unique dates, then scan adjacent pairs. If two dates are exactly one day apart, the current run grows; otherwise it resets to 1. A running maximum keeps the best run. Sorting dominates the cost.

| Operation | Time | Why |
|---|---|---|
| `current_streak` | O(n) | build a set, then walk backwards |
| `longest_streak` | O(n log n) | sort, then one linear scan |
| `get_habit` | O(1) average | dict lookup by name |

## Project Structure

```
habit-streak-tracker/
├── src/
│   ├── habit.py      # Habit class: one habit and its check-in dates
│   ├── tracker.py    # HabitTracker (composition) + streak algorithms
│   ├── storage.py    # Save/load habits as JSON (dates as ISO strings)
│   └── cli.py        # argparse commands: add, checkin, stats, list
├── tests/
│   ├── test_tracker.py
│   └── test_storage.py
├── pytest.ini
└── requirements.txt
```

## What I Learned

- **Composition in Python**: `HabitTracker` *has* many `Habit` objects, stored in a dict keyed by name for O(1) lookup, instead of scanning an array like the `Book[]` in my Java library-book-tracker.
- **Designing for testability**: passing `today` and `path` as parameters let me test with fixed dates and temporary files, instead of depending on the real clock or my real data.
- **JSON cannot store dates**: I convert `date` objects to ISO strings with `isoformat()` when saving and back with `date.fromisoformat()` when loading. A round-trip test checks that nothing is lost.
- **One error type, one handler**: the tracker, the CLI validation, and `datetime` all raise `ValueError`, so a single `try/except` in `cli.py` turns every failure into a one-line message
- **Module paths**: a `ModuleNotFoundError` taught me that a REPL looks for modules in the current directory, while a script looks in its own directory. `pythonpath = src` in `pytest.ini` fixes this for tests
- **Two Pythons on one machine**: `pytest` ran on Python 3.14 while `python3` was 3.12. Running `python3 -m pytest` keeps code and tests on the same interpreter