# Biomedical coding: evidence to implementation

**Paul's Notes · Biomedical research computing**

**Author:** Paul Skeffington · **Prepared with OpenAI**

This section supports [research across cancer types](../docs/cancer-research-scope.md) and connects influential biomedical computing, statistics, genomics, and clinical-AI papers to study-aware coding rules. Each referenced paper is treated as a **source**, not as an automatically validated software implementation.

## Start here

**AI / Codex / R analyst: begin with the [canonical biomedical R Markdown example](BIOMEDICAL_R_CANONICAL_EXAMPLE.md).** It is the retrievable reference for header, named chunks, `##` comments, input validation, descriptives, tests with numerical reasoning, scientific figures and end-to-end knitting. For comprehensive study write-ups and choosing between major analyses, follow the [full synthetic breast cancer R Markdown workbook](examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd). Read [implementation gates](IMPLEMENTATION_GATES.md) and the relevant study dictionary as well.


- **New to Rust?** Start with [Rust from the first variable through object-oriented programming and scientific engineering](../03_learning/rust/README.md), including a tested, dependency-free lab.
- [Rust engineering handbook aligned with the 12-chapter breast cancer book](RUST_CODING_BEST_PRACTICES.md) — 2021–2026 verification and defect studies plus official Rust/Cargo/Clippy guidance, with code checks for the breast-cancer ML runner and a [machine-readable source register](rust_coding_best_practices_sources.csv) and [eight-paper bibliography](rust_coding_references.bib).

- [Biomedical coding literature matrix](BIOMEDICAL_CODING_LITERATURE_MATRIX.md) — 71 primary-source-linked publications organized by methodological area, research contributors, and coding implications.
- [Machine-readable literature register](biomedical_coding_literature_matrix.csv) — stable IDs, article metadata, software, quality checks and failure modes.
- [Evidence-to-code acceptance gates](IMPLEMENTATION_GATES.md) — enforceable study and engineering requirements.
- [Primary implementation manuals](PRIMARY_DOCUMENTATION.md) — up-to-date package documentation for implementation; papers describe methods at publication time.
- [Official biomedical specification and methods register](OFFICIAL_METHODS_REGISTER.md) — 36 authoritative provider references kept separate from peer-reviewed research.
- [Machine-readable official-source register](official_methods_register.csv) — provider URLs, original entry IDs, implementation requirements and version checks.
- [Matrix regression checks](tests/test_literature_matrix.py) — offline source-register structural tests.

## Rosner acceptance evidence
[Verification and acceptance ledger](ROSNER_8E_VERIFICATION_ACCEPTANCE_LEDGER.md) · [complete synthetic R workbook execution test](tests/test_full_study_execution.R) · [CI workflow](../.github/workflows/learning-case-validation.yml). The ledger distinguishes verified source pages and independent numerical/structural checks from pending R execution, knit and specialist review. Never mark those gates completed from a documentation commit.

## Rosner eighth-edition methodology alignment

**For complete Rosner alignment:** read the [fourteen-chapter biomedical coding contract](ROSNER_8E_COMPLETE_METHODOLOGY_CONTRACT.md), the [chapter coverage registry](rosner_8e_complete_chapter_alignment.csv), and the [breast cancer book roadmap](../oncology/ROSNER_BREAST_CANCER_BIOSTATS_ALIGNMENT_ROADMAP.md). Structural validator: `python3 scripts/check_rosner_8e_alignment.py`. These record method and acceptance requirements; they do not certify all source paragraphs, R execution or clinical findings.

## Rosner eighth-edition source-to-code alignment (first pass)

[First-pass audit and follow-up gates](ROSNER_ALIGNMENT_FIRST_PASS_AUDIT.md) · [8e chapter-specific coding companion](ROSNER_8E_SOURCE_VERIFIED_IMPLEMENTATION.md) · [Opt-in Rosner descriptive helper](../06_RESOURCES/R/rosner_descriptive_contract.R) · [Offline R regression test](../06_RESOURCES/tests/test_rosner_descriptive_contract.R). Rosner 8e §2.4 explicitly demonstrates quantile type 2, while pre-existing Paul's Notes reports use type 7. The opt-in helper exposes both conventions; do **not** silently change historic output. R test execution is pending.

## Learn statistics from the measurement type

Use the [data-type-first computational statistical biology guide](../03_learning/biomedical-statistics-decision-guide.md) to choose tests from continuous, count, nominal, ordinal and censored outcomes. Then use the [practice workbook](../03_learning/statistics-practice-workbook.md) and the [synthetic R test lab](../03_learning/examples/statistical_test_lab.R) before approaching cohort-specific analysis. The [recent statistical methods and R workflow register](../06_RESOURCES/Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md) is separate from full study-method validation.

## Explore computing subjects

Start with the [computing subject guides](../03_learning/README.md). They cover R objects, checked joins, reshaping, missingness, paired comparisons, exploratory models, visualization, simulation and a complete local Bash-to-R deployment. The case uses base R; optional examples show dplyr, tidyr and survey interfaces.

Use the [Unix and Bash guide](../01_unix_bash/README.md) for shell foundations, and the [R tools](../06_RESOURCES/R/README.md) for additional plotting helpers. The [machine-learning section](../04_machine_learning/README.md) includes a reader's introduction, basic algorithms, caret, independent Python nested evaluation, direct R survival and limma examples, a [package guide](../04_machine_learning/package-guide.md), and [recent paper-to-code studies](../04_machine_learning/recent-code-studies.md). Full RNA-seq classification, multi-site external assessment and neural deployments remain implementation-planning topics.

## Boundaries

Use only independently authored narrative, source-linked bibliographic metadata, authoritative provider documentation and purpose-built synthetic tests. Do not copy private repository Git history, protected teaching files, sensitive research data, or third-party publications in full. A published software methods paper supports study planning, not automatic clinical suitability.
