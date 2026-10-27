"""Book registry contract tests, including missing lab and test sources."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "oncology_book_validator",
    Path(__file__).resolve().parent / "validate_oncology_book.py",
)
book = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(book)


def make_fixture(destination: Path) -> Path:
    """Mirror only manifest-referenced files; no personal or external data."""
    root = book.ROOT
    manifest_path = Path("oncology/book-manifest.json")
    data = json.loads((root / manifest_path).read_text(encoding="utf-8"))
    referenced = {str(manifest_path)}
    for key in ("canonical_roadmap", "introduction_path", "navigation_path"):
        referenced.add(data[key])
    for part in data["parts"]:
        for chapter in part["chapters"]:
            for key in ("chapter_path",):
                if chapter.get(key):
                    referenced.add(chapter[key])
            referenced.update(chapter.get("lab_paths", []))
            referenced.update(chapter.get("test_paths", []))
    for path in referenced:
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / path, target)
    return destination / manifest_path


class BookRegistryTests(unittest.TestCase):
    def test_current_manifest_paths(self):
        self.assertEqual(book.validate(), [])

    def test_missing_lab_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = make_fixture(root)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["parts"][0]["chapters"][4]["lab_paths"].append(
                "oncology/examples/not-a-real-example.py"
            )
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            self.assertTrue(any("missing/unsafe lab_paths" in issue for issue in book.validate(root)))

    def test_unsafe_path_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = make_fixture(root)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["parts"][0]["chapters"][4]["test_paths"].append(
                "scripts/../../outside.py"
            )
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            self.assertTrue(any("missing/unsafe test_paths" in issue for issue in book.validate(root)))

    def test_duplicate_chapter_id_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = make_fixture(root)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["parts"][0]["chapters"][1]["id"] = "CO-01"
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            self.assertTrue(any("duplicate chapter identifiers" in issue for issue in book.validate(root)))


if __name__ == "__main__":
    unittest.main()
