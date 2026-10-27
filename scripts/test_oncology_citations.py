"""Regression tests for oncology manuscript citation coverage."""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("citations", Path(__file__).parent / "validate_oncology_citations.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

class CitationCoverageTests(unittest.TestCase):
    def test_repository_section_coverage(self):
        self.assertEqual(module.validate(), [])

    def test_fenced_headings_not_counted(self):
        text = "## Valid\nText\n```markdown\n## Not a heading\n```\n### Real\nBody\n"
        self.assertEqual([x for x, _ in module.section_chunks(text)], ["Valid", "Real"])

    def test_missing_inline_link_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for relative in (module.SOURCES, module.COVERAGE, module.MANIFEST):
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(module.ROOT / relative, destination)
            payload = json.loads((root / module.COVERAGE).read_text(encoding="utf-8"))
            for doc in payload["documents"]:
                destination = root / doc["path"]
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(module.ROOT / doc["path"], destination)
            first = root / payload["documents"][0]["path"]
            original = first.read_text(encoding="utf-8")
            first.write_text(original.replace("**Section references:**", "**Sources omitted:**", 1), encoding="utf-8")
            self.assertTrue(any("expected one section reference" in x for x in module.validate(root)))

    def test_unmapped_new_section_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for relative in (module.SOURCES, module.COVERAGE, module.MANIFEST):
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(module.ROOT / relative, destination)
            payload = json.loads((root / module.COVERAGE).read_text(encoding="utf-8"))
            for doc in payload["documents"]:
                destination = root / doc["path"]
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(module.ROOT / doc["path"], destination)
            first = root / payload["documents"][0]["path"]
            first.write_text(first.read_text(encoding="utf-8") + "\n## Uncited new topic\nClaims\n", encoding="utf-8")
            self.assertTrue(any("unmapped headings" in x for x in module.validate(root)))

if __name__ == "__main__":
    unittest.main()
