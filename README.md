# Paul's Notes

**Biomedical research · scientific computing · reproducible machine learning**

Authored by Paul Skeffington · Compiled with OpenAI

A practical research notebook for moving from a biological question to a documented, tested analysis. The breast cancer examples connect **people, specimens, molecular measurements, model development, validation, and interpretation**. Read a guide, run a synthetic example, or inspect the evidence behind a method.

**Quick navigation:** [Start here](#start-here) · [Research workflow](#follow-a-research-question) · [Run an example](#put-the-methods-to-work) · [Browse subjects](#explore-the-collection) · [Progress and limitations](#research-progress-and-boundaries)

## Start here

Choose the route that matches what you need; no weekly sequence is required.

| I want to… | Start with | Then explore |
| --- | --- | --- |
| **Understand the biology** | [Breast cancer book](06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) — 12 chapters and 60 gene profiles | [Gene lookup](06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#alphabetical-gene-lookup) and [pathways](06_RESOURCES/Genomics/GENE_PATHWAY_OVERVIEW.md) |
| **Learn research computing** | [Computing by subject](03_learning/README.md) — R, data structure, joins, missingness and statistics | [Worked analysis](03_learning/README.md#run-the-combined-example) |
| **See how ML actually trains** | [Visual ML data-flow guide](04_machine_learning/visual-data-guide.md) — splits, preprocessing and held-out predictions | [ML methods](04_machine_learning/README.md) and [plotting gallery](04_machine_learning/gallery/README.md) |
| **Run and review an experiment** | [Paired-specimen ML walkthrough](04_machine_learning/advanced-breast-cancer-training.md) | [Comparison](04_machine_learning/model-comparison.md), [tuning](04_machine_learning/model-tuning.md) and [validation evidence](04_machine_learning/corpus-review.md) |
| **Design reproducible research** | [Research workflow](docs/research-workflow.md) — scope, inputs, checks and reporting | [Roadmap](docs/learning-roadmap.md) and [gate evidence](docs/roadmap-gates.md) |

## Follow a research question

The recurring teaching question is: **Can assay measurements distinguish a recorded specimen category for people who were not used to train the model?** It is not a clinical diagnostic or prognosis task.

**People → specimens → measurements → preparation → training → validation → predictions → interpretation**

1. **Know the unit of analysis.** Read [the breast cancer research narrative](06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) and [data identifiers and joins](03_learning/keys-and-reshaping.md). Specimens from the same person must stay together in evaluation splits.
2. **Prepare measurements without leakage.** Use the [visual data-flow guide](04_machine_learning/visual-data-guide.md) to understand training-only imputation, scaling and feature selection.
3. **Compare methods fairly.** Follow the [paired assay comparison](04_machine_learning/model-comparison.md) and [model-tuning guide](04_machine_learning/model-tuning.md) before interpreting scores.
4. **Explain and reproduce the result.** Inspect the [seven-figure gallery](04_machine_learning/gallery/README.md), [evidence review](04_machine_learning/corpus-review.md) and [analysis record template](templates/analysis-record.md).

## Put the methods to work

Run the existing **synthetic paired-specimen example** from the repository root. Use Python and the [pinned modeling requirements](04_machine_learning/requirements-python.txt):

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r 04_machine_learning/requirements-python.txt
.venv/bin/python 04_machine_learning/examples/breast_cancer_feature_selection.py /tmp/pauls-notes-assay-example
```

This creates a new directory with a fitted pipeline, held-out assessment, feature-review table, environment versions and SHA-256 manifest. **The output path must be new and outside the repository**; choose another path if it already exists. The 60 people and 48 anonymous features in this example are invented teaching data, **not TCGA patient records or the book's 60 named genes**.

Prefer a lighter introduction? Start with the [computing walkthrough](03_learning/README.md#run-the-combined-example). Want an additional programming language? See [Rust inference](04_machine_learning/rust-deployment.md), [native Rust training](04_machine_learning/rust-native-training.md) and the [R/Python methods guide](04_machine_learning/methods-and-deployments.md). Each guide states what has actually been executed.

## Explore the collection

| Area | Go to | What you'll find |
| --- | --- | --- |
| Biology and genomics | [Genomics resources](06_RESOURCES/Genomics/README.md) | The book, gene biology, annotations and pathway context |
| Computing foundations | [Unix and Bash](01_unix_bash/README.md) · [Computing subjects](03_learning/README.md) | Shell scripts, data types, reshaping, missingness and statistics |
| Machine learning | [ML home](04_machine_learning/README.md) | Algorithms, feature selection, comparisons, validation, Python, R and Rust |
| Visualization | [R plotting tools](06_RESOURCES/R/README.md) · [ML figure gallery](04_machine_learning/gallery/README.md) | Reusable plots, annotation and interpretation |
| Research evidence | [Biomedical coding](02_biomedical_coding/README.md) · [Rust engineering handbook](02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md) · [Literature resources](06_RESOURCES/Literature/README.md) | Source matrices, programming and verification rules, methods and quality checks |
| Writing and reproducibility | [LaTeX and bibliography](06_RESOURCES/LaTeX/README.md) · [Research workflow](docs/research-workflow.md) | Manuscripts, citations, provenance and execution records |

For a task-by-task index, use the [research resource guide](docs/resource-guide.md) or [complete resource directory](06_RESOURCES/README.md).

## Research progress and boundaries

- **Established in this repository:** synthetic software demonstrations for person-grouped model comparison, tuning, plotting, robustness, repeated-cohort assessment, conditional uncertainty, and a matched-objective Rust training check. See the [roadmap gate ledger](docs/roadmap-gates.md) for what each test established and what it did not.
- **Still separate work:** a new survival endpoint and published-result reproduction require their own protocols. Consult the [learning roadmap](docs/learning-roadmap.md) rather than treating a passing test as evidence of clinical validity.
- **TCGA-BRCA and privacy:** TCGA contains both open- and controlled-access files. Verify GDC access classification and permitted use **for each file** before any future real-data analysis. Keep credentials, direct identifiers and participant-level data out of this public repository. See [input/access requirements](docs/research-workflow.md#2-specify-input-and-access-contracts).
- **Model use:** examples are **research and education only**. They are not validated for cancer diagnosis, treatment choice or individualized prognosis. Synthetic predictive scores are not breast cancer findings.

## Research templates

Use the [study protocol](templates/study-protocol.md) to plan a study, the [data dictionary](templates/data-dictionary.md) to define records and measurements, and the [analysis record](templates/analysis-record.md) to document each execution.

---

[All resources](06_RESOURCES/README.md) · [Contributing and validation](CONTRIBUTING.md) · [License](LICENSE)
