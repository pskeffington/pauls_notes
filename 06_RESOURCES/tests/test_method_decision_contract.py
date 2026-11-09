#!/usr/bin/env python3
"""Static LIX/decision-tree contract checks; no clinical data or R runtime."""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs/research-method-map.json"
LITERATURE = ROOT / "06_RESOURCES/Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md"
SOURCE_TABLE = ROOT / "06_RESOURCES/Literature/biostatistics_r_literature_2021_2026.csv"
SELECTOR = ROOT / "06_RESOURCES/R/biomedical_test_selector.R"
TREE = ROOT / "06_RESOURCES/BIOMEDICAL_TEST_DECISION_TREE.md"

IMPLEMENTED = {
    "welch-t": ("welch_mean_comparison.R", "welch_mean_comparison"),
    "welch-anova": ("welch_oneway_comparison.R", "welch_oneway_comparison"),
    "paired-t": ("paired_mean_change.R", "paired_mean_change"),
    "wilcox-independent": ("stats_plots.R", "wilcox_independent"),
    "signed-rank": ("stats_plots.R", "wilcox_paired"),
    "descriptive": ("stats_plots.R", "describe_measurements"),
}
ROUTES = {
    "welch-t", "welch-anova", "paired-t", "mcnemar", "signed-rank",
    "wilcox-independent", "kruskal-wallis", "contingency-analysis",
    "binomial-proportion", "survey-design-review", "correlated-outcome-review",
    "count-rate-model-review", "count-exposure-review", "omics-design-review",
    "survival-analysis-review", "time-origin-review", "prediction-validation-review",
    "adjusted-model-review", "association-model-review", "continuous-design-review",
    "group-count-review", "paired-design-review", "descriptive",
    "descriptive-design-review", "descriptive-categorical",
    "ordinal-one-sample-review", "nominal-one-sample-review",
}
PROHIBITED_DOMAIN_TOKENS = [
    "CHIndex", "SDOHIndex", "NHBlack", "NHWhite",
    "week3_toothlossdata", "RACE", "/Volumes/Data",
]


def main() -> None:
    manifest = json.loads(REGISTRY.read_text(encoding="utf-8"))
    ids = {entry["id"] for entry in manifest["methods"]}
    assert ROUTES <= ids, f"Missing registered routes: {ROUTES - ids}"
    assert len(manifest["methods"]) == len(ids), "Duplicate route IDs"
    selector = SELECTOR.read_text(encoding="utf-8")
    tree = TREE.read_text(encoding="utf-8")
    literature = LITERATURE.read_text(encoding="utf-8")
    table = SOURCE_TABLE.read_text(encoding="utf-8")
    assert "flowchart TD" in tree and "weights + PSU + strata" in tree, "Missing design-aware flow"
    assert "Complex survey" in tree and "Paired" in tree and "Independent" in tree
    assert "ggplot2" in tree
    for method_id in ROUTES:
        assert f'"{method_id}"' in selector, f"Unreachable route: {method_id}"
        assert method_id in tree, f"Route absent from guidance: {method_id}"
    for method_id, (filename, function) in IMPLEMENTED.items():
        source_path = ROOT / "06_RESOURCES/R" / filename
        code = source_path.read_text(encoding="utf-8")
        assert re.search(r"\b" + re.escape(function) + r"\s*<-\s*function\s*\(", code), function
        for token in PROHIBITED_DOMAIN_TOKENS:
            assert token not in code, f"Domain leak in {filename}: {token}"
    for number in range(1, 20):
        evidence_id = f"BS-{number:03d}"
        assert evidence_id in literature, f"Missing literature matrix id {evidence_id}"
        assert f'"{evidence_id}"' in table, f"Missing CSV literature ID {evidence_id}"
    assert "2026-11-08" in literature and "2026-11-08" in table
    print("PASS: 27 decision branches, six implemented helpers (including existing), 19 literature IDs, no domain names")


if __name__ == "__main__":
    main()
