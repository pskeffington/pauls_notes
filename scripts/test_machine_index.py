"""Regression tests for the machine-readable Markdown index."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("machine_index", Path(__file__).resolve().parent / "build_machine_index.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

class MachineIndexTests(unittest.TestCase):
    def test_fenced_headings_are_not_sections(self):
        text = "# Real\nText\n\x60\x60\x60markdown\n# Fake\n\x60\x60\x60\n## Next\nBody\n"
        rows = list(module.sections(text))
        self.assertEqual([row[0] for row in rows], ["real", "next"])
        self.assertIn("# Fake", rows[0][4])

    def test_duplicate_heading_anchors(self):
        rows = list(module.sections("# A\n# A\n# A\n"))
        self.assertEqual([row[0] for row in rows], ["a", "a-1", "a-2"])

    def test_preamble_and_unicode(self):
        rows = list(module.sections("Opening\n\n## Clinical Δ\nnotes\n"))
        self.assertEqual(rows[0][0], "introduction")
        self.assertEqual(rows[1][0], "clinical-δ")

    def test_index_determinism_and_broken_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Intro\n[missing](gone.md)\n", encoding="utf-8")
            first, issues = module.index(root)
            second, _ = module.index(root)
            self.assertEqual(first, second)
            self.assertEqual(len(first), 1)
            self.assertEqual(len(issues), 1)
            self.assertEqual(first[0]["role"], "instruction")
            self.assertEqual(len(first[0]["content_sha256"]), 64)

if __name__ == "__main__":
    unittest.main()
