"""Checks for the curated research-method registry."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("method_validator", Path(__file__).parent / "validate_research_methods.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class RegistryTests(unittest.TestCase):
    def test_real_registry(self):
        self.assertEqual(module.validate(Path(__file__).resolve().parents[1]), [])

    def test_rejects_duplicate_ids_and_missing_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "docs/research-method-map.json").write_text(json.dumps({"schema_version": "1.0", "methods": [
                {"id": "demo", "guide": "missing.md", "evidence_ids": ["BS-999"]},
                {"id": "demo", "guide": "../outside.md", "evidence_ids": []}
            ]}))
            issues = module.validate(root)
            self.assertTrue(any("duplicate method id" in issue for issue in issues))
            self.assertTrue(any("unknown evidence id" in issue for issue in issues))
            self.assertTrue(any("missing or unsafe guide" in issue for issue in issues))

if __name__ == "__main__":
    unittest.main()
