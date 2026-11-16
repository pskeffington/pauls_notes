# Navigate Paul's Notes

[Repository home](../README.md) · [Learning subjects](../03_learning/README.md) · [Research resources](../06_RESOURCES/README.md) · [Machine index](machine-index.md)

Choose the **question or deliverable first**, then open the canonical home for that work. This page is a short reader-facing router; the underlying machine-readable routing data lives in [navigation-routes.json](navigation-routes.json). Section-level search and citations remain owned by the [machine index](machine-index.md). Avoid maintaining separate, conflicting lists of every research note.

## First destination by task

| Your objective | Start here | Then do |
| --- | --- | --- |
| Frame a cancer research question | [Research scope](cancer-research-scope.md) | [Study workflow and permissions](research-workflow.md) |
| Define a study and estimand | [Research workflow](research-workflow.md) | [Biomedical implementation gates](../02_biomedical_coding/IMPLEMENTATION_GATES.md) |
| Choose a defensible statistical test | [Decision matrix](../03_learning/bio_stats/BIOMEDICAL_DECISION_MATRIX_V2.md) | [Statistics learning atlas](../03_learning/bio_stats/README.md) |
| Learn R or research computing | [Learning subjects](../03_learning/README.md) | [Reusable R tools](../06_RESOURCES/R/README.md) |
| Select a figure | [Graph method guide](../03_learning/bio_stats/GRAPH_METHODS_ALIGNMENT.md) | [Synthetic graph gallery](../03_learning/bio_stats/GRAPH_METHODS_SYNTHETIC_GALLERY.Rmd) |
| Write and check biomedical analysis code | [Biomedical coding](../02_biomedical_coding/README.md) | [Canonical R Markdown example](../02_biomedical_coding/BIOMEDICAL_R_CANONICAL_EXAMPLE.md) |
| Read the developing computational oncology textbook | [Textbook home](../oncology/README.md) | [Chapter roadmap](../oncology/ROADMAP.md) |
| Explore genomics sources | [Genomics resources](../06_RESOURCES/Genomics/README.md) | [Cancer-wide research scope](cancer-research-scope.md) |
| Build and evaluate ML | [Machine learning](../04_machine_learning/README.md) | [Evidence and acceptance limits](roadmap-gates.md) |
| Learn Unix, Git, or Rust | [Unix/Bash](../01_unix_bash/README.md) · [Git tutorial](../03_learning/git-github-from-zero-to-push.md) · [Rust foundations](../03_learning/rust/README.md) | Choose the matching examples and tests |
| Determine what has actually passed | [Biomedical acceptance ledger](../02_biomedical_coding/BIOSTAT_8E_VERIFICATION_ACCEPTANCE_LEDGER.md) | [Dated R validation summary](../03_learning/bio_stats/R_VALIDATION_STATUS.md) |

## Reader workflow

**Question → method → example → check → interpretation.** Read the chosen guide's data assumptions and independent-unit definition before its example. Use the cited synthetic exercise, run the appropriate tests when available, and distinguish observed outcomes from proposed or merely committed checks. Navigate back to this page when the task changes rather than jumping between unrelated tutorials.

## Agent and machine workflow

**Task → route ID → canonical entrypoint → narrow source section → evidence gate.** Read [AGENTS.md](../AGENTS.md), use the [routing manifest](navigation-routes.json) to choose a home, then retrieve the smallest relevant section from the [machine index](machine-index.md). The `next` edges in the JSON are suggested transitions, not prerequisites. Preserve exact source scope and avoid interpreting the presence of code or CI jobs as evidence that they ran.

## Scientific boundaries

All synthetic biomedical and cancer examples are educational, not patient-derived clinical findings. The current statistical figure gallery and expanded workbook have not received confirmed end-to-end R/HTML acceptance in the cited [ledger](../02_biomedical_coding/BIOSTAT_8E_VERIFICATION_ACCEPTANCE_LEDGER.md). The ontology or route map does not itself certify code, statistical assumptions, publication readiness or any individual manuscript chapter.

## Navigation maintenance

Update the [route manifest](navigation-routes.json) when a canonical home changes, then update this reader page and short entrypoint links. Keep the full topic catalog in [machine-index.md](machine-index.md). Check the three layers with `python3 scripts/check_navigation_routes.py` and its tests; use `python3 scripts/check_documentation.py` for wider Markdown links and anchors. The [maintenance policy](DOCUMENTATION_MAINTENANCE.md) specifies evidence requirements.
