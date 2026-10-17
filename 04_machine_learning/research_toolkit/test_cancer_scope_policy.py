"""Guard the distinction between oncology-wide methods and case-specific GDC access.

This is a static documentation/contract check, not privacy certification.
"""
import copy
import json
from pathlib import Path
import re
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read_contracts():
    return {
        "card": json.loads((HERE / "model_card.template.json").read_text(encoding="utf-8")),
        "policy": (HERE / "MODEL_USE_POLICY.md").read_text(encoding="utf-8"),
        "agents": (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        "readme": (HERE / "README.md").read_text(encoding="utf-8"),
        "gdc": (HERE / "gdc_open_access_preflight.py").read_text(encoding="utf-8"),
        "scope": (ROOT / "docs/cancer-research-scope.md").read_text(encoding="utf-8"),
    }


def inspect(contract):
    issues = []
    card = contract["card"]
    if ("any cancer type" not in card.get("cancer_research_scope", "").lower()
        or card.get("data_provider") != "internally_generated_synthetic_only"
        or "TCGA-BRCA" not in card.get("current_gdc_adapter_scope", "")
        or card.get("actual_real_cancer_data_processed") is not False):
        issues.append("Model card conflates overall oncology scope and synthetic worked case")
    for restricted in ("clinical_use_authorized", "patient_level_training_currently_admitted",
                       "controlled_access_permitted", "direct_identifiers_permitted"):
        if card.get(restricted) is not False:
            issues.append(f"Model card incorrectly permits {restricted}")
    if "all cancer types" not in contract["policy"].lower() or "non-tcga" not in contract["policy"].lower():
        issues.append("Model policy is not cancer-wide and source-specific")
    if "any cancer type" not in contract["agents"].lower() or "all sources" not in contract["agents"].lower():
        issues.append("AI agent policy accidentally restricts oncology scope")
    if "methods for any cancer type" not in contract["readme"].lower():
        issues.append("Toolkit README lacks generic oncology research mission")
    if "across all cancer types" not in contract["scope"].lower():
        issues.append("Repository scope guide no longer includes all cancer types")
    if not re.search(r'^PROJECT = "TCGA-BRCA"$', contract["gdc"], re.M):
        issues.append("GDC preflight must preserve current case-specific project admission")
    if 'if hit.get("access") != "open":' not in contract["gdc"]:
        issues.append("GDC preflight must continue to reject unknown/controlled access")
    return issues


class CancerScopePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = read_contracts()

    def test_cancer_scope_not_restricted_to_current_tcga_example(self):
        self.assertEqual(inspect(self.original), [])

    def test_tcga_gdc_project_stays_specific(self):
        item = copy.deepcopy(self.original)
        item["gdc"] = item["gdc"].replace('PROJECT = "TCGA-BRCA"', 'PROJECT = "TCGA-COAD"')
        self.assertTrue(any("case-specific" in x for x in inspect(item)))

    def test_model_card_cannot_claim_real_patient_execution_or_clinical_use(self):
        item = copy.deepcopy(self.original)
        item["card"]["actual_real_cancer_data_processed"] = True
        item["card"]["clinical_use_authorized"] = True
        problems = inspect(item)
        self.assertTrue(any("synthetic worked case" in x for x in problems))
        self.assertTrue(any("clinical_use_authorized" in x for x in problems))

    def test_scope_and_source_access_must_not_be_weakened(self):
        item = copy.deepcopy(self.original)
        item["agents"] = item["agents"].replace("any cancer type", "only TCGA")
        item["gdc"] = item["gdc"].replace('if hit.get("access") != "open":',
                                         'if hit.get("access") == "controlled":')
        problems = inspect(item)
        self.assertTrue(any("AI agent policy" in x for x in problems))
        self.assertTrue(any("unknown/controlled" in x for x in problems))


if __name__ == "__main__":
    unittest.main()
