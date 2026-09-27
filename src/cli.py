import argparse

from storage import load_tracker, save_tracker


def cmd_add(tracker, args):
    tracker.add_habit(args.name)
    save_tracker(tracker)
    print(f"Added habit '{args.name}'.")


def main():
    parser = argparse.ArgumentParser(description="Track daily habits and streaks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new habit")
    add_parser.add_argument("name", help="Name of the habit")

    args = parser.parse_args()
    tracker = load_tracker()

    try:
        if args.command == "add":
            cmd_add(tracker, args)
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main() 