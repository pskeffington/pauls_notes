"""Positive and negative tests for tracked editor/build debris detection."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_repository_artifacts import find_tracked_debris


class RepositoryArtifactTests(unittest.TestCase):
    def test_reject_nested_runtime_and_editor_artifacts(self):
        bad = [
            ".DS_Store", "Thumbs.db", ".Rhistory", "Rplots.pdf",
            "03_learning/rust/lab/target/debug/example",
            "04_machine_learning/__pycache__/model.cpython-312.pyc",
            "scripts/.pytest_cache/v/cache/lastfailed",
            "src/.mypy_cache/state", "src/.ruff_cache/data",
            "src/.venv/bin/python", "pkg/node_modules/dependency/main.js",
            "site/.idea/workspace.xml", "cache/result.pyc",
            "notes/draft.md~", "notes/.#draft.md",
            "src\\target\\debug\\demo", "src/package.swp",
        ]
        self.assertEqual(find_tracked_debris(bad), sorted(bad))

    def test_keep_documented_research_sources_and_curated_examples(self):
        expected_clean = [
            "04_machine_learning/gallery/example/report.json",
            "06_RESOURCES/Genomics/FIGURES/gene_companion_walkthrough.R",
            "06_RESOURCES/tests/test_stats_plots.R",
            "03_learning/rust/lab/Cargo.lock",
            ".github/workflows/documentation-validation.yml",
            "docs/targeting-study.md",
            "04_machine_learning/evidence/gallery-validation-2026-10-16.json",
            "README.md", ".gitignore", ".editorconfig",
        ]
        self.assertEqual(find_tracked_debris(expected_clean), [])

    def test_duplicates_are_reported_once_and_sorted(self):
        self.assertEqual(find_tracked_debris(
            ["z/.DS_Store", "a/.venv/lib/site.py", "z/.DS_Store"]),
            ["a/.venv/lib/site.py", "z/.DS_Store"])

    def test_invalid_path_segments_rejected(self):
        self.assertEqual(find_tracked_debris(
            ["../outside.txt", "a/../b.txt", ""]),
            ["", "../outside.txt", "a/../b.txt"])


if __name__ == "__main__":
    unittest.main()
