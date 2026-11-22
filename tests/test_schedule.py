"""Unit tests for dictionary-based Course Schedule System."""
import tempfile
import unittest
from pathlib import Path
from schedule import Schedule

class ScheduleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schedule = Schedule()
        cls.report = cls.schedule.load_csv(Path(__file__).resolve().parents[1] / "courses.csv")

    def test_real_csv_counts(self):
        self.assertEqual(self.report.total_rows, 174)
        self.assertEqual(self.report.loaded, 173)
        self.assertEqual(len(self.report.duplicates), 1)

    def test_exact_lookup_case_and_whitespace(self):
        item = self.schedule.get(" bio ", "141", "d01")
        self.assertIsNotNone(item)
        self.assertEqual(item.instructor, "Abrahams,Shaheem")

    def test_unknown_exact_key(self):
        self.assertIsNone(self.schedule.get("ZZZ", "999", "X99"))

    def test_partial_filter(self):
        self.assertTrue(all(x.subject == "BIO" for x in self.schedule.search(subject="bio")))

    def test_instructor_case_insensitive(self):
        matches = self.schedule.search(instructor_surname="ABRAHAMS")
        self.assertGreater(len(matches), 0)
        self.assertTrue(all("abrahams" in x.instructor.casefold() for x in matches))

    def test_combined_filter(self):
        matches = self.schedule.search(subject="BIO", catalog="142", instructor_surname="Abrahams")
        self.assertGreater(len(matches), 0)
        self.assertTrue(all(x.subject == "BIO" and x.catalog == "142" for x in matches))

    def test_no_results(self):
        self.assertEqual(self.schedule.search(subject="ZZZ"), [])

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            Schedule().load_csv("missing_courses_99999.csv")

    def test_missing_required_header(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.csv"
            path.write_text("Subject,Catalog\nBIO,141\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "missing columns"):
                Schedule().load_csv(path)

    def test_malformed_and_duplicate(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "sample.csv"
            path.write_text('Subject,Catalog,Section,Instructor,TotEnrl,CapEnrl\n'
                            'BIO,141,D01,"Smith,Jane",10,20\n'
                            'bio,141,d01,"Smith,Jane",11,20\n'
                            'BIO,142,D01,"Smith,Jane",bad,20\n'
                            ',142,D02,"Smith,Jane",2,20\n', encoding="utf-8")
            s = Schedule()
            report = s.load_csv(path)
            self.assertEqual((report.total_rows, report.loaded), (4, 1))
            self.assertEqual(len(report.duplicates), 1)
            self.assertEqual(len(report.malformed), 2)
            self.assertEqual(s.get("BIO", "141", "D01").enrollment, 10)

if __name__ == "__main__":
    unittest.main()
