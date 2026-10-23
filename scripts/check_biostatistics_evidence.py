#!/usr/bin/env python3
"""Require paper and executable coverage for every object in the biostatistics chart."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "03_learning/bio_stats"

# The method names in compound boxes remain covered even when one runnable
# alternative is inadvertently removed while its other alternatives still work.
REQUIRED_OUTPUTS = {
    "T": {"welch", "rank_sum"},
    "P": {"paired_t", "signed_rank", "sign"},
    "AN": {"anova", "welch_anova", "kruskal_wallis"},
    "CR": {"pearson", "spearman", "linear"},
    "R": {"poisson", "negative_binomial"},
    "BIN": {"binomial"},
    "CH": {"chi_square", "fisher", "logistic", "multinomial"},
    "MC": {"published.mcnemar", "published.mcnemar_cc",
           "published.mcnemar_exact", "published.mcnemar_mid_p"},
    "O": {"ordinal_rank", "ordinal", "ordinal_po_check"},
    "MX": {"mixed", "mixed_lrt", "gee", "survey"},
    "S": {"kaplan_meier", "log_rank", "cox", "cox_ph_check", "cumulative_incidence"},
    "H": {"deseq2", "edger", "voom_limma", "intensity_limma"},
    "Z": {"Z"},
}
DESIGN_NODES = {"A", "B", "C", "D", "E", "N"}


def validate_evidence(register, guide, atlas, source):
    """Pure validation enables negative coverage checks without editing the repo."""
    errors = []
    decision_section = guide.split("## 2.", 1)[-1].split("## 3.", 1)[0]
    charts = re.findall(r"```mermaid\n(.*?)```", decision_section, re.S)
    if not charts:
        return ["Missing decision chart"]
    graph = "\n".join(charts)
    sections = {
        re.sub(r"[^a-z0-9 -]", "", line.lstrip("# ").lower()).replace(" ", "-")
        for line in atlas.splitlines() if re.match(r"^#{1,6} ", line)
    }
    declarations = re.findall(r'\b([A-Z]+)(?:\[|\{)"([^"\n]+)"', graph)
    declared = dict(declarations)
    for name, label in declarations:
        if declared[name] != label:
            errors.append(f"{name}: conflicting labels across decision panels")
    nodes = register.get("nodes", [])
    node_ids = [node["node"] for node in nodes]
    if len(node_ids) != len(set(node_ids)):
        errors.append("Duplicate evidence object")
    if set(node_ids) != set(declared):
        errors.append(f"Chart/evidence mismatch: chart={sorted(declared)}, map={sorted(node_ids)}")
    if set(node_ids) != DESIGN_NODES | set(REQUIRED_OUTPUTS):
        errors.append("Named chart procedures or design objects lost coverage")
    papers = register.get("papers", [])
    paper_ids = [paper["id"] for paper in papers]
    if len(paper_ids) != len(set(paper_ids)):
        errors.append("Duplicate paper ID")
    for paper in papers:
        for field in ("id", "authors", "year", "title", "identifier", "url", "locator", "checked"):
            if not paper.get(field):
                errors.append(f"Paper {paper.get('id')}: missing {field}")
        if not re.match(r"https://(?:doi[.]org/10[.]|pubmed[.]ncbi[.]nlm[.]nih[.]gov/)", paper.get("url", "")):
            errors.append(f"Paper {paper.get('id')}: no DOI or PubMed URL")
    for node in nodes:
        name = node["node"]
        ids = node.get("paper_ids", [])
        if not ids or not set(ids) <= set(paper_ids):
            errors.append(f"{name}: missing or unknown paper")
        if name in declared and not any(i in declared[name] for i in ids):
            errors.append(f"{name}: chart label has no mapped paper ID")
        if node.get("section", "") not in sections:
            errors.append(f"{name}: missing atlas section")
        outputs = set(node.get("outputs", []))
        if name in DESIGN_NODES:
            if node.get("execution") != "design_gate" or not re.search(rf"\b{name}\s*=", source):
                errors.append(f"{name}: no executable design gate")
        elif not REQUIRED_OUTPUTS.get(name, set()) <= outputs:
            errors.append(f"{name}: missing a named method or diagnostic")
        for output in outputs:
            key = output.rsplit(".", 1)[-1]
            if not re.search(rf"\b{re.escape(key)}\s*=", source):
                errors.append(f"{name}: no implementation output {output}")
    if "Disagreement retained" not in atlas or ".003976752" not in atlas or ".398" not in atlas:
        errors.append("Published rank-sum discrepancy must remain visible")
    return errors


def main():
    register = json.loads((ATLAS / "decision-tree-evidence.json").read_text())
    guide = (ATLAS / register["chart"]).read_text()
    source = (ATLAS / register["source"]).read_text()
    atlas = (ATLAS / "README.md").read_text()
    errors = validate_evidence(register, guide, atlas, source)
    if errors:
        raise SystemExit("\n".join(errors))
    count = sum(len(node["outputs"]) for node in register["nodes"])
    print(f"PASS: {len(register['nodes'])} chart objects, {len(register['papers'])} real papers, "
          f"{count} method/diagnostic outputs; explicit reproduction boundaries")


if __name__ == "__main__":
    main()
