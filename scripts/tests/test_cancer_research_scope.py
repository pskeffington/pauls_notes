"""Deliberate failures for cancer-wide documentation scope and case boundaries."""
import copy
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "check_cancer_research_scope.py"
spec = importlib.util.spec_from_file_location("cancer_scope", SCRIPT)
scope = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scope)


class CancerResearchScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = scope.read_pages()

    def test_main_scope_is_coherent(self):
        self.assertEqual(scope.validate(self.pages), [])

    def test_tcga_cannot_silently_become_repo_wide_requirement(self):
        pages = copy.deepcopy(self.pages)
        pages["CONTRIBUTING.md"] += "\nTie machine-learning additions to the breast cancer book.\n"
        problems = scope.validate(pages)
        self.assertTrue(any("mandatory dependency" in p for p in problems))

    def test_scope_and_case_are_both_required(self):
        pages = copy.deepcopy(self.pages)
        pages["README.md"] = pages["README.md"].replace("across all cancer types", "only TCGA-BRCA")
        self.assertTrue(any("across all cancer types" in p for p in scope.validate(pages)))
        pages = copy.deepcopy(self.pages)
        pages["docs/cancer-research-scope.md"] = pages["docs/cancer-research-scope.md"].replace(
            "not a blanket claim", "a blanket claim"
        )
        self.assertTrue(any("not a blanket" in p for p in scope.validate(pages)))

    def test_missing_navigation_and_d1_scope_fail(self):
        pages = copy.deepcopy(self.pages)
        pages["04_machine_learning/README.md"] = pages["04_machine_learning/README.md"].replace(
            "../docs/cancer-research-scope.md", "../docs/other-methods.md"
        )
        self.assertTrue(any("missing link" in p for p in scope.validate(pages)))
        pages = copy.deepcopy(self.pages)
        pages["docs/roadmap-gates.md"] = pages["docs/roadmap-gates.md"].replace(
            "current real TCGA-BRCA proposal", "all real cancer projects"
        )
        self.assertTrue(any("Roadmap must distinguish" in p for p in scope.validate(pages)))


if __name__ == "__main__":
    unittest.main()
