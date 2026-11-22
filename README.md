# CSC 223 – Course Schedule System

A read-only, menu-driven Python application using a dictionary (Map ADT) to store course sections from the instructor-provided `courses.csv`.

## Requirements
Python 3.10 or later; no third-party packages.

## Run
From this folder:

```bash
python main.py
```

Or specify a CSV file:

```bash
python main.py path/to/courses.csv
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Menu
1. Display all sections
2. Exact composite-key lookup
3. Filter by Subject, Catalog, and/or Section
4. Instructor-surname search
5. Combine key-field and instructor filters
6. Exit

## Design
- Immutable `ScheduleItem` dataclass represents one course section.
- Dictionary key: `(Subject, Catalog, Section)` after stripping whitespace and uppercasing.
- The first row for a repeated key is kept; subsequent duplicates are reported.
- Malformed rows are reported with their CSV line numbers.
- Extra CSV columns not needed for display/search are ignored.
- Instructor surnames are taken from the part before the first comma.

## Complexity
Average-case exact key lookup: O(1). Full or partial searches: O(n), plus O(k log k) to sort k matches. Loading n rows: average O(n). Storage: O(n).

## Dataset
The supplied file contains 174 data rows, 173 distinct composite keys, and one duplicate key (`UMS`, `107`, `D01`). It contains historical course dates; the application does not claim that these are current course offerings.