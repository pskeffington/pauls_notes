"""Regressions for bounded biomedical documentation entrypoint hygiene."""
import importlib.util
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "notes_docs_hygiene", ROOT / "scripts/check_notes_docs_hygiene.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class NotesDocHygieneTests(unittest.TestCase):
    def test_current_core_pages(self):
        self.assertEqual(module.validate(), [])

    def test_literal_escaped_newline(self):
        issues = module.inspect_page("03_learning/README.md",
                                     "Line one\\nLine two")
        self.assertTrue(any("backslash-n" in x for x in issues))

    def test_intentional_inline_code_escape_allowed(self):
        issues = module.inspect_page("03_learning/README.md",
                                     "The literal `\\n` is a code token.")
        self.assertFalse(any("backslash-n" in x for x in issues))

    def test_fenced_example_escape_allowed(self):
        text = "Intro\n```python\nexample = \"\\\\n\"\n```\nClosing."
        issues = module.inspect_page("03_learning/README.md", text)
        self.assertFalse(any("backslash-n" in x for x in issues))

    def test_unfenced_narrative_escape_still_rejected(self):
        issues = module.inspect_page("03_learning/README.md",
                                     "One paragraph\\nAnother paragraph")
        self.assertTrue(any("backslash-n" in x for x in issues))

    def test_legacy_placeholder_rejected(self):
        issues = module.inspect_page("03_learning/README.md",
                                     "Biomedical methods chapter outline")
        self.assertTrue(any("placeholder" in x for x in issues))

    def test_canonical_route_target_must_exist(self):
        routes = module.REQUIRED_ROUTES["README.md"]
        with TemporaryDirectory() as empty, patch.object(module, "ROOT", Path(empty)):
            issues = module.inspect_page("README.md", "\n".join(routes))
        self.assertTrue(any("route target missing" in x for x in issues))
    def test_canonical_routes_required(self):
        issues = module.inspect_page("README.md", "# Notes")
        self.assertTrue(any("canonical route" in x for x in issues))


if __name__ == "__main__":
    unittest.main()
