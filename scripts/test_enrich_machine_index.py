"""Tests for deterministic topic enrichment and section deltas."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("enrich", Path(__file__).parent / "enrich_machine_index.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def item(path, section, text, digest="abc"):
    return {"path": path, "section_id": path + "#" + section, "heading": section, "text": text, "content_sha256": digest}

class EnrichmentTests(unittest.TestCase):
    def test_crosslinks_bidirectional_and_sorted(self):
        rows = [item("README.md", "Overview", "[Stats](03_learning/biomedical-statistics-decision-guide.md)"),
                item("03_learning/biomedical-statistics-decision-guide.md", "Poisson regression", "counts")]
        enriched = mod.enrich(rows)
        self.assertEqual(enriched[0]["outbound_documents"], ["03_learning/biomedical-statistics-decision-guide.md"])
        self.assertEqual(enriched[1]["inbound_documents"], ["README.md"])
        self.assertIn("biostatistics", enriched[1]["topics"])
        self.assertEqual(enriched, mod.enrich(rows))

    def test_no_external_or_fragment_links(self):
        rows = [item("README.md", "Root", "[X](https://example.org) [Y](#local) [Z](missing.md)")]
        self.assertEqual(mod.enrich(rows)[0]["outbound_documents"], [])

    def test_delta_added_removed_changed(self):
        old = [item("a.md", "a", "", "one"), item("b.md", "b", "", "old"), item("d.md", "d", "", "same")]
        new = [item("b.md", "b", "", "new"), item("c.md", "c", "", "yes"), item("d.md", "d", "", "same")]
        report = mod.delta(old, new)
        self.assertEqual(report["added"], ["c.md#c"])
        self.assertEqual(report["removed"], ["a.md#a"])
        self.assertEqual(report["changed"], ["b.md#b"])
        self.assertEqual(report["unchanged_count"], 1)

if __name__ == "__main__":
    unittest.main()
