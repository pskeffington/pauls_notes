# Biomedical coding: evidence to implementation

**Paul's Notes · Biomedical research computing**

**Author:** Paul Skeffington · **Prepared with OpenAI**

This section connects influential biomedical computing, statistics, genomics, and clinical-AI papers to study-aware coding rules. Each referenced paper is treated as a **source**, not as an automatically validated software implementation.

## Start here

- [Biomedical coding literature matrix](BIOMEDICAL_CODING_LITERATURE_MATRIX.md) — 71 primary-source-linked publications organized by methodological area, research contributors, and coding implications.
- [Machine-readable literature register](biomedical_coding_literature_matrix.csv) — stable IDs, article metadata, software, quality checks and failure modes.
- [Evidence-to-code acceptance gates](IMPLEMENTATION_GATES.md) — enforceable study and engineering requirements.
- [Primary implementation manuals](PRIMARY_DOCUMENTATION.md) — up-to-date package documentation for implementation; papers describe methods at publication time.
- [Official biomedical specification and methods register](OFFICIAL_METHODS_REGISTER.md) — 36 authoritative provider references kept separate from peer-reviewed research.
- [Machine-readable official-source register](official_methods_register.csv) — provider URLs, original entry IDs, implementation requirements and version checks.
- [Matrix regression checks](tests/test_literature_matrix.py) — offline source-register structural tests.

## Explore computing subjects

Start with the [computing subject guides](../03_learning/README.md). They cover R objects, checked joins, reshaping, missingness, paired comparisons, exploratory models, visualization, simulation and a complete local Bash-to-R deployment. The case uses base R; optional examples show dplyr, tidyr and survey interfaces.

Use the [Unix and Bash guide](../01_unix_bash/README.md) for shell foundations, and the [R tools](../06_RESOURCES/R/README.md) for additional plotting helpers. Advanced resampling with caret, full RNA-seq workflows and predictive-model deployments remain reference topics without a complete executable example here; the literature matrix supplies planning references for those areas.

## Boundaries

Use only independently authored narrative, source-linked bibliographic metadata, authoritative provider documentation and purpose-built synthetic tests. Do not copy private repository Git history, protected teaching files, sensitive research data, or third-party publications in full. A published software methods paper supports study planning, not automatic clinical suitability.
