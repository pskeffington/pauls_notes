"""Regression tests for index path coverage and orphan candidate auditing."""
import unittest
from audit_machine_index import audit


def record(path, section="intro", inbound=None):
    return {"path": path, "section_id": f"{path}#{section}", "inbound_documents": inbound or []}


class IndexAuditTests(unittest.TestCase):
    def test_complete_coverage_and_orphan_candidates(self):
        rows = [record("README.md"), record("a.md", inbound=["README.md"]), record("b.md")]
        report = audit(rows, {"README.md", "a.md", "b.md"})
        self.assertEqual([], report["errors"])
        self.assertEqual(["b.md"], report["orphan_candidates"])

    def test_missing_document_fails_coverage(self):
        report = audit([record("README.md")], {"README.md", "missing.md"})
        self.assertEqual(["missing.md"], report["missing_documents"])
        self.assertTrue(report["errors"])

    def test_duplicate_section_is_rejected(self):
        report = audit([record("README.md"), record("README.md")], {"README.md"})
        self.assertTrue(any("duplicate section" in e for e in report["errors"]))

    def test_inconsistent_reverse_links_is_rejected(self):
        rows = [record("README.md"), record("a.md", "one", ["README.md"]), record("a.md", "two")]
        report = audit(rows, {"README.md", "a.md"})
        self.assertTrue(any("inconsistent" in e for e in report["errors"]))

    def test_unindexed_incoming_source_is_rejected(self):
        rows = [record("README.md"), record("a.md", inbound=["not-indexed.md"])]
        report = audit(rows, {"README.md", "a.md"})
        self.assertTrue(any("incoming-link source" in e for e in report["errors"]))


if __name__ == "__main__":
    unittest.main()
