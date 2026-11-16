"""Unit tests for stable, task-first documentation routing."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "navigation_routes", ROOT / "scripts/check_navigation_routes.py")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class NavigationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ROOT / module.MANIFEST).read_text(encoding="utf-8"))

    def test_live_repository_entrypoints(self):
        self.assertEqual(module.validate(ROOT), [])

    def test_stable_full_route_set(self):
        self.assertEqual(module.validate_manifest(self.manifest, ROOT), [])
        self.assertEqual(len(self.manifest["routes"]), 13)

    def test_duplicate_route_id_rejected(self):
        broken = copy.deepcopy(self.manifest)
        broken["routes"][1]["id"] = broken["routes"][0]["id"]
        self.assertTrue(any("Duplicate route IDs" in issue
                            for issue in module.validate_manifest(broken, ROOT)))

    def test_unknown_edge_rejected(self):
        broken = copy.deepcopy(self.manifest)
        broken["routes"][0]["next"].append("nonexistent_route")
        self.assertTrue(any("unknown next route" in issue
                            for issue in module.validate_manifest(broken, ROOT)))

    def test_missing_document_rejected(self):
        broken = copy.deepcopy(self.manifest)
        broken["routes"][0]["entry"] = "docs/nonexistent-navigation.md"
        self.assertTrue(any("missing entry" in issue
                            for issue in module.validate_manifest(broken, ROOT)))

    def test_path_escape_rejected(self):
        broken = copy.deepcopy(self.manifest)
        broken["routes"][0]["entry"] = "../external.md"
        self.assertTrue(any("invalid relative entry path" in issue
                            for issue in module.validate_manifest(broken, ROOT)))

    def test_audience_and_empty_boundary_rejected(self):
        broken = copy.deepcopy(self.manifest)
        broken["routes"][0]["audience"] = ["reader", "reader"]
        broken["routes"][0]["boundary"] = " "
        failures = module.validate_manifest(broken, ROOT)
        self.assertTrue(any("invalid audience" in item for item in failures))
        self.assertTrue(any("empty boundary" in item for item in failures))

    def test_missing_reader_guide_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "docs").mkdir()
            (base / module.MANIFEST).write_text(
                json.dumps(self.manifest), encoding="utf-8")
            errors = module.validate(base)
        self.assertTrue(any("Missing reader-facing" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
