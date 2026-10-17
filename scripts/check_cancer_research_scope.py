#!/usr/bin/env python3
"""Check that project-wide oncology scope stays distinct from the TCGA worked case.

Documentation consistency only: not data authorization, privacy certification, or
proof of clinical validity. The existing link validator separately checks links.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "README.md",
    "CONTRIBUTING.md",
    "docs/cancer-research-scope.md",
    "docs/research-workflow.md",
    "docs/resource-guide.md",
    "docs/learning-roadmap.md",
    "docs/roadmap-gates.md",
    "04_machine_learning/README.md",
    "06_RESOURCES/Genomics/README.md",
)
MARKER = {
    "README.md": "docs/cancer-research-scope.md",
    "CONTRIBUTING.md": "docs/cancer-research-scope.md",
    "docs/research-workflow.md": "cancer-research-scope.md",
    "docs/resource-guide.md": "cancer-research-scope.md",
    "docs/learning-roadmap.md": "cancer-research-scope.md",
    "docs/roadmap-gates.md": "cancer-research-scope.md",
    "04_machine_learning/README.md": "docs/cancer-research-scope.md",
    "06_RESOURCES/Genomics/README.md": "docs/cancer-research-scope.md",
}


def read_pages(root=ROOT):
    return {p: (root / p).read_text(encoding="utf-8") for p in PAGES}


def validate(pages):
    errors = []
    for name in PAGES:
        if name not in pages:
            errors.append(f"Missing scope-contract page: {name}")
    if errors:
        return errors
    for name, marker in MARKER.items():
        if marker not in pages[name]:
            errors.append(f"{name}: missing link to cancer-wide research scope")
    root = pages["README.md"].lower()
    scope = pages["docs/cancer-research-scope.md"].lower()
    contribution = pages["CONTRIBUTING.md"].lower()
    roadmap = pages["docs/roadmap-gates.md"].lower()
    ml = pages["04_machine_learning/README.md"].lower()
    for term in ("across all cancer types", "tcga-brca", "current worked case", "synthetic"):
        if term not in root:
            errors.append(f"README.md: missing scope/case boundary '{term}'")
    for term in (
        "all cancer types",
        "current worked case",
        "other cancer sources",
        "tcga-brca",
        "study contract",
        "not for clinical use",
        "not a blanket",
    ):
        if term not in scope:
            errors.append(f"Scope guide: missing independent cancer-research boundary '{term}'")
    if "any cancer type" not in contribution:
        errors.append("Contribution guidance must support independently defined cancer studies")
    if "tie machine-learning additions to the breast cancer book" in contribution:
        errors.append("Breast cancer cannot be a mandatory dependency for all cancer studies")
    if "new cancer study" not in roadmap or "current real tcga-brca proposal" not in roadmap:
        errors.append("Roadmap must distinguish active TCGA admission from independent future studies")
    if "methods for any cancer research question" not in ml:
        errors.append("ML homepage must not imply a single cancer model")
    return errors


def main():
    errors = validate(read_pages())
    if errors:
        raise SystemExit("\n".join(errors))
    print("PASS: cancer-wide scope, TCGA-BRCA case boundary and nonclinical limits are consistent across project navigation")


if __name__ == "__main__":
    main()
