import argparse
import argparse
from datetime import date

from storage import load_tracker, save_tracker


def cmd_add(tracker, args):
    tracker.add_habit(args.name)
    save_tracker(tracker)
    print(f"Added habit '{args.name}'.")


def cmd_checkin(tracker, args):
    habit = tracker.get_habit(args.name)
    if args.date:
        checkin_date = date.fromisoformat(args.date)
    else:
        checkin_date = date.today()

    if checkin_date > date.today():
        raise ValueError("Cannot check in for a future date.")

    habit.check_in(checkin_date)
    save_tracker(tracker)
    print(f"Checked in '{args.name}' on {checkin_date.isoformat()}.")


def cmd_stats(tracker, args):
    stats = tracker.get_stats(args.name)
    print(f"Habit: {stats['name']}")
    print(f"Total check-ins: {stats['total_checkins']}")
    print(f"Current streak: {stats['current_streak']} day(s)")
    print(f"Longest streak: {stats['longest_streak']} day(s)")


def cmd_list(tracker, args):
    if not tracker.habits:
        print("No habits yet. Add one with: add <name>")
        return

    for name in sorted(tracker.habits):
        stats = tracker.get_stats(name)
        print(
            f"{name}: {stats['current_streak']} day streak (best: {stats['longest_streak']})"
        )


def main():
    parser = argparse.ArgumentParser(description="Track daily habits and streaks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new habit")
    add_parser.add_argument("name", help="Name of the habit")
    checkin_parser = subparsers.add_parser("checkin", help="Check in a habit")
    checkin_parser.add_argument("name", help="Name of the habit")
    checkin_parser.add_argument(
        "--date", help="Date to check in (YYYY-MM-DD), defaults to today"
    )

    stats_parser = subparsers.add_parser("stats", help="Show streak stats for a habit")
    stats_parser.add_argument("name", help="Name of the habit")

    subparsers.add_parser("list", help="List all habits with their current streaks")

    args = parser.parse_args()
    tracker = load_tracker()

    try:
        if args.command == "add":
            cmd_add(tracker, args)
        elif args.command == "checkin":
            cmd_checkin(tracker, args)
        elif args.command == "stats":
            cmd_stats(tracker, args)
        elif args.command == "list":
            cmd_list(tracker, args)
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
