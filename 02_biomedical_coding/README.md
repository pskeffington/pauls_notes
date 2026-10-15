# Biomedical coding: evidence to implementation

**Paul's Notes · Independent technical research**

**Author:** Paul Skeffington · **Prepared with OpenAI**

This section connects influential biomedical computing, statistics, genomics, and clinical-AI papers to study-aware coding rules. Each referenced paper is treated as a **source**, not as an automatically validated software implementation.

## Start here

- [Biomedical coding literature matrix](BIOMEDICAL_CODING_LITERATURE_MATRIX.md) — 71 primary-source-linked publications organized by methodological area, research contributors, and coding implications.
- [Machine-readable literature register](biomedical_coding_literature_matrix.csv) — stable IDs, article metadata, software, quality checks and failure modes.
- [Evidence-to-code acceptance gates](IMPLEMENTATION_GATES.md) — enforceable study and engineering requirements.
- [Primary implementation manuals](PRIMARY_DOCUMENTATION.md) — up-to-date package documentation for implementation; papers describe methods at publication time.
- [Official biomedical specification and methods register](OFFICIAL_METHODS_REGISTER.md) — 36 authoritative provider references kept separate from peer-reviewed research.
- [Machine-readable official-source register](official_methods_register.csv) — provider URLs, original entry IDs, implementation requirements and version checks.
- [Source reconciliation ledger](LEGACY_SOURCE_RECONCILIATION.md) — the 30 newly selected research papers and their pinned legacy source IDs; duplicate papers excluded.
- [Matrix regression checks](tests/test_literature_matrix.py) — offline source-register structural tests.

## Learning and deployment sequence

1. [Unix and Bash](../01_unix_bash/README.md) — established runnable foundation.
2. R programming, tidy data, biostatistics, resampling and `caret` — **planned**.
3. Bioconductor, differential expression, feature-level uncertainty, and genomic plots — **planned**.
4. Python biomedical ML, patient-aware validation, calibrated prediction and explainability — **planned**.
5. Computational workflows, clinical data interoperability, and clinical AI reporting — **planned**.

See the [curated preserved resources](../06_RESOURCES/README.md) for original implementation references retained as source files. The resource archive is not a certification that its scripts were re-executed or that software dependencies remain current.

## Boundaries

Use only independently authored narrative, source-linked bibliographic metadata, authoritative provider documentation and purpose-built synthetic tests. Do not copy private repository Git history, protected teaching files, sensitive research data, or third-party publications in full. A published software methods paper supports study planning, not automatic clinical suitability.
