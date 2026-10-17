"""Fail-closed checks for Rust beginner curriculum contracts."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "check_rust_foundations_course.py"
spec = importlib.util.spec_from_file_location("rust_course", SOURCE)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

class RustFoundationsCourseTests(unittest.TestCase):
    def test_course_contract_current_repository(self):
        self.assertEqual(checker.check_course(), [])

    def test_missing_lessons_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            problems = checker.check_course(root)
            self.assertTrue(any("Missing course lesson" in message for message in problems))
            self.assertTrue(any("manifest/toolchain" in message for message in problems))

    def test_module_and_privacy_checks_exist(self):
        source = (checker.ROOT / "03_learning/rust/lab/src/engineering.rs").read_text()
        self.assertIn("assessment_mutation_cannot_change_fitted_median", source)
        self.assertIn("Person leakage between training and assessment", source)
        self.assertIn("All training measurements missing", source)
        original = (checker.ROOT / "03_learning/rust/lab/Cargo.toml").read_text()
        self.assertIn("[dependencies]", original)
        self.assertNotIn("reqwest", original)

if __name__ == "__main__":
    unittest.main()
