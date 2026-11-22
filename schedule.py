"""Read-only course schedule backed by a dictionary (Map ADT)."""
import csv
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ScheduleItem:
    subject: str
    catalog: str
    section: str
    component: str
    session: str
    instructor: str
    room: str
    days: str
    meeting_start: str
    meeting_end: str
    start_date: str
    end_date: str
    campus: str
    class_number: str
    enrollment: int | None
    capacity: int | None

    @property
    def key(self):
        return self.subject, self.catalog, self.section

@dataclass(frozen=True)
class LoadReport:
    total_rows: int
    loaded: int
    malformed: tuple[str, ...]
    duplicates: tuple[str, ...]

def normalize(value):
    return value.strip().upper()

class Schedule:
    REQUIRED_COLUMNS = ("Subject", "Catalog", "Section", "Instructor")

    def __init__(self):
        self._items = {}

    def __len__(self):
        return len(self._items)

    @staticmethod
    def _optional_int(value, label):
        value = value.strip()
        if not value:
            return None
        number = int(value)
        if number < 0:
            raise ValueError(f"{label} must be nonnegative")
        return number

    @classmethod
    def _parse_row(cls, row):
        def get(column):
            return (row.get(column) or "").strip()
        subject, catalog, section = (normalize(get(x)) for x in ("Subject", "Catalog", "Section"))
        if not all((subject, catalog, section)):
            raise ValueError("missing Subject, Catalog, or Section")
        if not get("Instructor"):
            raise ValueError("missing Instructor")
        return ScheduleItem(
            subject, catalog, section, get("Component"), get("Session"),
            get("Instructor"), get("Room"), get("Days"), get("MtgStart"),
            get("MtgEnd"), get("StartDate"), get("EndDate"), get("Campus"),
            get("ClassNbr"), cls._optional_int(get("TotEnrl"), "TotEnrl"),
            cls._optional_int(get("CapEnrl"), "CapEnrl"))

    def load_csv(self, filename: str | Path):
        with open(filename, newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames is None:
                raise ValueError("CSV has no header")
            missing = set(self.REQUIRED_COLUMNS) - set(reader.fieldnames)
            if missing:
                raise ValueError("CSV missing columns: " + ", ".join(sorted(missing)))
            items, malformed, duplicates = {}, [], []
            count = 0
            for line_number, row in enumerate(reader, 2):
                count += 1
                try:
                    if None in row:
                        raise ValueError("more fields than header")
                    item = self._parse_row(row)
                except (ValueError, TypeError) as exc:
                    malformed.append(f"line {line_number}: {exc}")
                    continue
                if item.key in items:
                    duplicates.append(f"line {line_number}: duplicate key {item.key}")
                    continue
                items[item.key] = item
        self._items = items
        return LoadReport(count, len(items), tuple(malformed), tuple(duplicates))

    def get(self, subject, catalog, section):
        return self._items.get(tuple(normalize(x) for x in (subject, catalog, section)))

    def search(self, *, subject="", catalog="", section="", instructor_surname=""):
        criteria = (normalize(subject), normalize(catalog), normalize(section))
        surname = instructor_surname.strip().casefold()
        results = []
        for item in self._items.values():
            if any(wanted and wanted != actual for wanted, actual in zip(criteria, item.key)):
                continue
            if surname and surname not in item.instructor.split(",", 1)[0].strip().casefold():
                continue
            results.append(item)
        return sorted(results, key=lambda x: x.key)

    def all_items(self):
        return sorted(self._items.values(), key=lambda x: x.key)
