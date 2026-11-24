#!/usr/bin/env python3
"""Validate the educational biostatistics decision matrix without external packages."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = Path("03_learning/bio_stats")
MATRIX_COLUMNS = (
    "method_id", "outcome_family", "study_design", "estimand_or_target",
    "required_fields", "gate_keys", "breast_cancer_example", "interpretation",
    "common_pitfall", "reporting_quantity", "route_class",
)
GATE_COLUMNS = ("gate_key", "review_question", "minimum_evidence")
BIOSTAT_COLUMNS = ("method_id", "topic", "biostat_chapters", "coverage")
BIOSTAT_COVERAGE = {"textbook", "extension", "design_gate"}
BIOSTAT_CHAPTERS = {str(chapter) for chapter in range(1, 15)}
ROUTE_CLASSES = {"descriptive", "inferential", "review", "design_gate"}
OUTCOME_FAMILIES = {
    "any", "numeric", "categorical", "omics_counts", "time_to_event", "count",
    "continuous", "binary", "ordinal", "nominal",
}


class MatrixValidationError(ValueError):
    """Matrix registry contract is not satisfied."""


def read_rows(
    path: Path,
    expected_columns: tuple[str, ...],
    *,
    allow_empty: frozenset[str] = frozenset(),
) -> list[dict[str, str]]:
    if not path.is_file():
        raise MatrixValidationError(f"Missing registry file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != expected_columns:
            raise MatrixValidationError(f"Unexpected columns in {path}")
        rows = list(reader)
    if not rows:
        raise MatrixValidationError(f"Empty registry: {path}")
    for i, row in enumerate(rows, start=2):
        if None in row or any(
            value is None or (not value.strip() and column not in allow_empty)
            for column, value in row.items()
        ):
            raise MatrixValidationError(f"Missing/empty values in {path}:{i}")
    return rows


def unique_keys(rows: list[dict[str, str]], key: str, name: str) -> set[str]:
    keys = [row[key] for row in rows]
    if len(keys) != len(set(keys)):
        raise MatrixValidationError(f"Duplicate {name} keys: {key}")
    return set(keys)


def validate_matrix(root: Path = ROOT) -> dict[str, int]:
    base = root / BASE
    matrix = read_rows(base / "biomedical_decision_matrix.csv", MATRIX_COLUMNS)
    dictionary = read_rows(base / "biomedical_gate_dictionary.csv", GATE_COLUMNS)
    biostat = read_rows(
        base / "biostat_method_registry.csv", BIOSTAT_COLUMNS,
        allow_empty=frozenset({"biostat_chapters"}),
    )
    for row in biostat:
        method_id = row["method_id"]
        coverage = row["coverage"]
        if coverage not in BIOSTAT_COVERAGE:
            raise MatrixValidationError(f"{method_id}: unknown biostat coverage")
        chapter_text = row["biostat_chapters"]
        chapters = chapter_text.split(";") if chapter_text else []
        # An extension/design gate can deliberately have no textbook attribution.
        # Present chapter IDs remain exact, unique eighth-edition chapter numbers.
        if not chapters and coverage == "textbook":
            raise MatrixValidationError(
                f"{method_id}: textbook coverage requires chapter attribution"
            )
        if len(chapters) != len(set(chapters)) or any(
            chapter not in BIOSTAT_CHAPTERS for chapter in chapters
        ):
            raise MatrixValidationError(
                f"{method_id}: invalid or repeated biostat chapter IDs"
            )

    ids = unique_keys(matrix, "method_id", "matrix")
    biostat_ids = unique_keys(biostat, "method_id", "Biomedical methods crosswalk")
    known_gates = unique_keys(dictionary, "gate_key", "gate dictionary")
    if ids != biostat_ids:
        raise MatrixValidationError(
            f"Route coverage differs from Biomedical methods crosswalk: "
            f"missing={sorted(biostat_ids - ids)}, extra={sorted(ids - biostat_ids)}"
        )
    if len(ids) != 27:
        raise MatrixValidationError(f"Expected 27 selector routes, found {len(ids)}")

    used_gates: set[str] = set()
    for row in matrix:
        method_id = row["method_id"]
        if row["route_class"] not in ROUTE_CLASSES:
            raise MatrixValidationError(f"{method_id}: unknown route_class")
        if row["outcome_family"] not in OUTCOME_FAMILIES:
            raise MatrixValidationError(f"{method_id}: unknown outcome_family")
        requested_fields = row["required_fields"].split(";")
        gate_keys = row["gate_keys"].split(";")
        if len(requested_fields) != len(set(requested_fields)) or any(
            not x.strip() for x in requested_fields
        ):
            raise MatrixValidationError(f"{method_id}: bad required_fields")
        if len(gate_keys) != len(set(gate_keys)) or len(gate_keys) < 3:
            raise MatrixValidationError(f"{method_id}: invalid or repeated gate keys")
        unknown_gates = set(gate_keys) - known_gates
        if unknown_gates:
            raise MatrixValidationError(
                f"{method_id}: unknown gate keys: {sorted(unknown_gates)}"
            )
        if not {"unit", "scale"}.issubset(gate_keys):
            raise MatrixValidationError(f"{method_id}: missing basic unit/scale gates")
        used_gates.update(gate_keys)

    if used_gates != known_gates:
        raise MatrixValidationError(
            f"Unreferenced gate definitions: {sorted(known_gates - used_gates)}"
        )
    selector_path = root / "06_RESOURCES/R/biomedical_test_selector.R"
    if not selector_path.is_file():
        raise MatrixValidationError("Missing primary R selector")
    selector = selector_path.read_text(encoding="utf-8")
    absent = [method_id for method_id in ids
              if f'"{method_id}"' not in selector]
    if absent:
        raise MatrixValidationError(
            f"Routes not represented as selector string literals: {sorted(absent)}"
        )
    return {"routes": len(ids), "gates": len(known_gates),
            "reviewed_gate_links": sum(len(r["gate_keys"].split(";")) for r in matrix)}


if __name__ == "__main__":
    stats = validate_matrix()
    print(
        "PASS: biostatistics route matrix — "
        f"{stats['routes']} routes, {stats['gates']} defined gates, "
        f"{stats['reviewed_gate_links']} route-gate links; "
        "matches Biomedical methods crosswalk and R selector."
    )
