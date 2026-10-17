#!/usr/bin/env python3
"""Offline verification of the staged Rust learning route and nonclinical lab.

This checks repository consistency. Rust compilation/tests occur separately in CI.
"""
from pathlib import Path
import re
import tomllib

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "03_learning/rust"
LAB = COURSE / "lab"
LESSONS = (
    "README.md",
    "01_first_steps.md",
    "02_collections_and_control.md",
    "03_ownership_and_borrowing.md",
    "04_structs_traits_and_composition.md",
    "05_cargo_testing_and_quality.md",
    "06_breast_cancer_engineering.md",
    "07_practice_and_mastery.md",
)
MODULES = ("foundations", "ownership", "objects", "engineering")


def check_course(root=ROOT):
    """Return human-readable error categories, not private input values."""
    course = root / "03_learning/rust"
    lab = course / "lab"
    errors = []
    for file in LESSONS:
        path = course / file
        if not path.is_file():
            errors.append(f"Missing course lesson: {file}")
            continue
        source = path.read_text(encoding="utf-8")
        if not source.startswith("# ") or "invented" not in source.lower() and "synthetic" not in source.lower():
            errors.append(f"Lesson lacks topic or synthetic scope: {file}")
    overview = (course / "README.md")
    if overview.is_file():
        contents = overview.read_text(encoding="utf-8")
        for item in LESSONS[1:]:
            if f"]({item})" not in contents:
                errors.append(f"Missing route navigation: {item}")
        if "Cargo.toml" not in contents:
            errors.append("Missing Cargo quick start")
    manifest = lab / "Cargo.toml"
    toolchain = lab / "rust-toolchain.toml"
    try:
        m = tomllib.loads(manifest.read_text(encoding="utf-8"))
        t = tomllib.loads(toolchain.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return errors + [f"Missing or malformed lab manifest/toolchain: {type(exc).__name__}"]
    package = m.get("package", {})
    if package.get("name") != "breast-cancer-rust-lab" or package.get("edition") != "2021" or package.get("rust-version") != "1.90":
        errors.append("Course package identity, edition or MSRV drifted")
    if m.get("dependencies") != {}:
        errors.append("Foundation lab must remain free of external dependencies")
    if t.get("toolchain", {}).get("channel") != "1.90.0":
        errors.append("Lab Rust toolchain must stay pinned")
    lock = lab / "Cargo.lock"
    if not lock.is_file() or 'name = "breast-cancer-rust-lab"' not in lock.read_text():
        errors.append("Missing or mismatched Cargo.lock")
    lib = lab / "src/lib.rs"
    if not lib.is_file():
        errors.append("Missing lab library")
    else:
        contents = lib.read_text()
        for module in MODULES:
            if f"pub mod {module};" not in contents:
                errors.append(f"Missing public module: {module}")
    for module in MODULES:
        source = lab / f"src/{module}.rs"
        if not source.is_file():
            errors.append(f"Missing source module: {module}")
            continue
        code = source.read_text()
        if "extern crate" in code or "std::net::" in code or "reqwest" in code:
            errors.append(f"Remote/external dependency is not allowed in {module}")
        if "unsafe {" in code or "unsafe fn" in code:
            errors.append(f"Unsafe code forbidden in foundation module {module}")
        if "#[test]" not in code:
            errors.append(f"Module lacks executable unit tests: {module}")
    for name in ("src/main.rs", "tests/research_workflow.rs"):
        file = lab / name
        if not file.is_file() or "#![forbid(unsafe_code)]" not in file.read_text():
            errors.append(f"Missing guarded source: {name}")
    engineering = lab / "src/engineering.rs"
    if engineering.exists():
        code = engineering.read_text()
        for phrase in ("validate_person_split", "assessment_mutation_cannot_change_fitted_median", "All training measurements missing"):
            if phrase not in code:
                errors.append(f"Missing scientific negative control: {phrase}")
    objects = lab / "src/objects.rs"
    if objects.exists():
        code = objects.read_text()
        for phrase in ("pub enum Tissue", "pub struct Specimen", "pub trait Describe", "pub struct Pair", "pub struct GeneAnnotation"):
            if phrase not in code:
                errors.append(f"Missing research/OOP teaching type: {phrase}")
    all_text = "\n".join((course / f).read_text() for f in LESSONS if (course / f).exists())
    for phrase in ("ownership", "borrowing", "trait", "composition", "Cargo.lock", "TCGA", "60", "48", "research"):
        if not re.search(re.escape(phrase), all_text, re.I):
            errors.append(f"Missing foundational/book link concept: {phrase}")
    readme = (root / "README.md").read_text()
    book = (root / "06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md").read_text()
    if "03_learning/rust/README.md" not in readme:
        errors.append("Root README must link beginner Rust route")
    if "03_learning/rust/README.md" not in book:
        errors.append("Breast cancer book must link beginning Rust route")
    return errors


def main():
    errors = check_course()
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(LESSONS)} sequential Rust lessons, four tested modules, no third-party lab dependencies and book navigation")


if __name__ == "__main__":
    main()
