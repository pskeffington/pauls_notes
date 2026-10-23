# Paul's Notes

**Cancer research · biomedical computing · reproducible machine learning**

Authored by Paul Skeffington · Compiled with OpenAI

An open, methods-focused notebook for **research across all cancer types**, including molecular oncology, pathology/imaging, cancer epidemiology, computational biology and translational research. The **current worked case** uses a breast cancer teaching book and synthetic paired-specimen ML, with **TCGA-BRCA as the current data-source example under consideration**. Neither TCGA nor breast cancer limits this repository's research scope. Start with a research question, then build a documented, reproducibly checked analysis.

**Quick navigation:** [Research scope](docs/cancer-research-scope.md) · [Start here](#start-here) · [Research workflow](#follow-a-research-question) · [Run the current example](#put-the-methods-to-work) · [Browse subjects](#explore-the-collection) · [Progress and limitations](#research-progress-and-boundaries)

## Start here

Choose the route that matches what you need; no weekly sequence is required.

| I want to… | Start with | Then explore |
| --- | --- | --- |
| **Choose a cancer research question** | [Cancer research scope](docs/cancer-research-scope.md) — all cancer types, data modalities and study designs | [Independent study/data-access contract](docs/research-workflow.md) and [protocol template](templates/study-protocol.md) |
| **Understand the current breast cancer example** | [Breast cancer book](06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) — 12 chapters and 60 gene profiles | [Gene lookup](06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#alphabetical-gene-lookup) and [pathways](06_RESOURCES/Genomics/GENE_PATHWAY_OVERVIEW.md) |
| **Learn Rust from zero** | [Rust foundations course](03_learning/rust/README.md) — variables, borrowing, object-oriented patterns, Cargo and tests | [Research-oriented Rust engineering](03_learning/rust/06_breast_cancer_engineering.md) and [source-backed practices](02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md) |
| **Learn Git/GitHub from zero** | [Zero-to-push Git and GitHub tutorial](03_learning/git-github-from-zero-to-push.md) — setup, sign-in, essential commands and safe first push | Branches, pull requests, errors and research repository safety |
| **Learn introductory biomedical statistics** | [Data-type-first statistics guide](03_learning/biomedical-statistics-decision-guide.md) — quantitative vs qualitative, counts, ordinal, survival, an R test-selection flowchart and a [practice workbook](03_learning/statistics-practice-workbook.md) | [Recent biomedical methods and R evidence](06_RESOURCES/Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md) and [R tools](06_RESOURCES/R/README.md) |
| **Understand study types in real papers** | [Study designs and published examples](03_learning/study-designs-and-published-examples.md) — nine readings connecting sampling, timing, assignment and analysis | [Source register](06_RESOURCES/Literature/study_design_paper_examples.csv) and [probability/sampling](03_learning/probability-and-design.md) |
| **Learn research computing** | [Computing by subject](03_learning/README.md) — R, data structure, joins, missingness and statistics | [Worked analysis](03_learning/README.md#run-the-combined-example) |
| **See how ML actually trains** | [Visual ML data-flow guide](04_machine_learning/visual-data-guide.md) — splits, preprocessing and held-out predictions | [ML methods](04_machine_learning/README.md) and [plotting gallery](04_machine_learning/gallery/README.md) |
| **Run and review an experiment** | [Paired-specimen ML walkthrough](04_machine_learning/advanced-breast-cancer-training.md) | [Comparison](04_machine_learning/model-comparison.md), [tuning](04_machine_learning/model-tuning.md) and [validation evidence](04_machine_learning/corpus-review.md) |
| **Design reproducible research** | [Research workflow](docs/research-workflow.md) — scope, inputs, checks and reporting | [Roadmap](docs/learning-roadmap.md) and [gate evidence](docs/roadmap-gates.md) |

## Git and GitHub: from zero to your first push

New to version control? [Follow the complete command-line guide](03_learning/git-github-from-zero-to-push.md) to install Git, sign in to GitHub, clone a repository or create your own, and upload your first changes. The basic cycle is:

```bash
git status
git switch -c docs/my-change   # in an existing repository
# Edit README.md, then review and save the change:
git diff
git add README.md
git commit -m "docs: update README"
git push -u origin docs/my-change
```

Then open a **pull request** on GitHub for review and merging. These commands assume you have already cloned a repository, configured your Git identity and signed in with push access. **Commit saves locally; push uploads; a pull request proposes a merge.** Never commit credentials, patient-linked records or restricted research data. Start with the [beginner guide](03_learning/git-github-from-zero-to-push.md) if any prerequisite is unfamiliar.

## Follow a research question

**Current worked-case question:** Can invented assay measurements distinguish a recorded specimen category for people who were not used to train the model? This illustrates one oncology research workflow, not the only supported question. A different cancer, data modality or endpoint requires a separately defined study and evaluation protocol. This is not a clinical diagnostic or prognosis task.

**People → specimens → measurements → preparation → training → validation → predictions → interpretation**

1. **Know the unit of analysis.** For the current example, read [the breast cancer research narrative](06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) and [data identifiers and joins](03_learning/keys-and-reshaping.md). Specimens from the same person must stay together in evaluation splits.
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

**Variable-only synthetic ML:** The [configurable oncology teaching lab](04_machine_learning/research_toolkit/README.md) lets you change numeric generator, nested person-grouping, feature-selection and regularization settings in JSON and produce a new auditable research-only report. This remains simulated breast-specimen classification, not an adapter for TCGA or any other participant dataset.

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

- **Milestones and evidence:** [Dated status dashboard](docs/roadmap-gates.md#delivery-and-admission-snapshot-2026-10-17) and [machine-readable gate record](docs/milestone-evidence.toml) distinguish delivered software, draft code, data-access blockers, test evidence and scientific limits. Rust foundations, the book-aligned handbook, G3 inference parity (R3) and the Python configurable synthetic runner (R4) are delivered within bounded educational/software scope. Public-data privacy protections (D0) remain in draft review and TCGA-BRCA real-study admission (D1) is blocked.
- **Established in this repository:** synthetic software demonstrations for person-grouped model comparison, tuning, plotting, robustness, repeated-cohort assessment, conditional uncertainty, and a matched-objective Rust training check. See the [roadmap gate ledger](docs/roadmap-gates.md) for what each test established and what it did not.
- **Still separate work:** the new G4 [synthetic 24-month survival protocol](04_machine_learning/survival-protocol.md) and [data dictionary](04_machine_learning/survival-data-dictionary.md) are frozen **without running a G4 survival model**. G5 published-result reproduction requires its own source-specific protocol. Consult the [learning roadmap](docs/learning-roadmap.md) rather than treating a passing test as evidence of clinical validity.
- **Cancer data and privacy:** Source, file-level access, licensing/consent, privacy and publication review are **study-specific for every cancer dataset**. The TCGA-BRCA example uses the GDC's open/controlled distinction; its metadata-only adapter does not authorize that dataset or other providers. Keep participant-linked records, controlled data and credentials out of this public repository. See [cancer research scope](docs/cancer-research-scope.md#dataset-agnostic-privacy-with-source-specific-adapters) and [data/access contract](docs/research-workflow.md#2-specify-input-and-access-contracts).
- **Model use:** current examples are **research and education only**, not validated for any cancer diagnosis, screening, therapy selection, prognosis or clinical decision support. Synthetic classification results are not findings about human tumors.

## Research templates

Use the [study protocol](templates/study-protocol.md) to plan a study, the [data dictionary](templates/data-dictionary.md) to define records and measurements, and the [analysis record](templates/analysis-record.md) to document each execution.

---

[All resources](06_RESOURCES/README.md) · [Contributing and validation](CONTRIBUTING.md) · [License](LICENSE)
