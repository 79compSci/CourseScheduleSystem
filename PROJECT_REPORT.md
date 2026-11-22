# Course Schedule System – CSC 223 Project Report

**Student:** [Enter your name]  
**IDE:** PyCharm  
**GitHub repository:** [Add your repository URL]  
**Dataset:** Instructor-provided `courses.csv`

## 1. Project purpose
I developed a read-only, menu-driven Python application that loads course-section records from CSV into a dictionary and supports exact composite-key retrieval, partial-key searches, and instructor-surname searches. The project demonstrates the Map ADT and the difference between hash-based lookup and record filtering.

## 2. Design decisions
`ScheduleItem` is an immutable dataclass holding course identifiers, instructor, meeting information, and enrollment fields. `Schedule` encapsulates the dictionary so the menu does not directly modify its storage. Each normalized tuple `(Subject, Catalog, Section)` maps to one `ScheduleItem`, because these three fields identify a section for this assignment. Normalization strips spaces and uppercases key fields so user input such as `bio` matches `BIO`.

## 3. Loading and validation
The loader uses `csv.DictReader` with `utf-8-sig` to accommodate the supplied file's BOM. It verifies required headers and key fields, requires an instructor, validates numeric enrollment/capacity values, and records malformed line numbers. On duplicate keys, the first valid record is retained and later rows are reported rather than silently overwriting data. The supplied file has 174 rows, 173 unique keys, and one repeated key (`UMS`, `107`, `D01`).

## 4. Search operations
A complete Subject–Catalog–Section tuple uses `dict.get()` for average-case O(1) retrieval. Partial searches scan the dictionary values and match the supplied fields. Instructor search compares the surname before the comma using case-insensitive substring matching. Criteria can be combined; results are sorted for consistent display.

## 5. Testing and debugging
Unit tests cover real CSV counts, normalized exact lookup, missing keys, partial matching, case-insensitive instructor matching, combined criteria, no-match results, missing files, missing headers, malformed rows, and duplicate-key behavior. Run `python -m unittest discover -s tests -v` to reproduce the test results. The program also handles invalid menu selections and clean exits.

## 6. Complexity analysis
For n stored sections, dictionary construction takes average O(n) time and O(n) memory. A complete composite-key lookup takes average O(1) time. Partial or instructor filtering takes O(n) to inspect entries and O(k log k) to sort k matching results. Displaying all sections also requires sorting O(n log n). Worst-case hash-table operations can degrade with severe collisions, but average-case lookup is constant time.

## 7. Reflection
The Map ADT is effective when the user knows all three identifying fields, because the program can retrieve one section without scanning the entire schedule. A dictionary cannot directly answer instructor or incomplete-key queries without additional indexes, so this implementation filters values. Separating parsing, storage, searching, and the menu made the program easier to test and maintain.

## 8. Evidence to attach
Add a screenshot of the running menu, an exact-key result, a combined instructor search, and the terminal unit-test output after running the program locally.