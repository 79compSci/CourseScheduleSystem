"""Menu-driven course schedule application."""
import argparse
import csv
from pathlib import Path
from schedule import Schedule

def display(items):
    if not items:
        print("No matching course sections found.")
        return
    for x in items:
        print(f"{x.subject} {x.catalog} {x.section} | {x.component} | {x.instructor} | "
              f"{x.days or 'TBA'} {x.meeting_start}-{x.meeting_end} | "
              f"Room: {x.room or 'TBA'} | Enrollment: {x.enrollment}/{x.capacity}")
    print(f"Found {len(items)} section(s).")

def run(schedule):
    while True:
        print("\nCOURSE SCHEDULE SYSTEM\n1. Display all sections\n2. Exact key lookup"
              "\n3. Partial key search\n4. Instructor surname search"
              "\n5. Combined key and instructor search\n6. Exit")
        try:
            choice = input("Select 1-6: ").strip()
            if choice == "1":
                display(schedule.all_items())
            elif choice == "2":
                item = schedule.get(input("Subject: "), input("Catalog: "), input("Section: "))
                display([item] if item else [])
            elif choice in ("3", "5"):
                print("Leave unused criteria blank.")
                subject = input("Subject: ")
                catalog = input("Catalog: ")
                section = input("Section: ")
                surname = input("Instructor surname: ") if choice == "5" else ""
                display(schedule.search(subject=subject, catalog=catalog, section=section,
                                        instructor_surname=surname))
            elif choice == "4":
                surname = input("Instructor surname: ").strip()
                if surname:
                    display(schedule.search(instructor_surname=surname))
                else:
                    print("Please enter a surname.")
            elif choice == "6":
                print("Goodbye!")
                return
            else:
                print("Invalid selection. Enter a number from 1 to 6.")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

def main():
    parser = argparse.ArgumentParser(description="Course Schedule System")
    parser.add_argument("csv_file", nargs="?", default=str(Path(__file__).with_name("courses.csv")))
    args = parser.parse_args()
    schedule = Schedule()
    try:
        report = schedule.load_csv(args.csv_file)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        print(f"Unable to load schedule: {exc}")
        return
    print(f"Read {report.total_rows} rows; loaded {report.loaded} unique sections.")
    for warning in report.malformed:
        print("Malformed:", warning)
    for warning in report.duplicates:
        print("Duplicate:", warning)
    run(schedule)

if __name__ == "__main__":
    main()
