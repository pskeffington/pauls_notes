# Machine learning for biomedical research

Authored by Paul Skeffington · Compiled with OpenAI

[Paul's Notes](../README.md) · [Computing subjects](../03_learning/README.md) · [Research workflow](../docs/research-workflow.md)

Follow the [breast cancer book's research question](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) from people and specimens to measurements, predictions, and interpretation. The guides below explain reusable methods through that narrative. Existing general-purpose R/Python fixtures teach individual mechanisms; the paired-specimen feature-selection example explicitly connects them to a synthetic tissue-category task.

| Subject | Resource | Practical purpose |
| --- | --- | --- |
| Understanding the subject | [What is machine learning?](what-is-machine-learning.md) | Features, targets, learning, assessment and interpretation in plain language |
| Seeing the data flow | [Visual data guide](visual-data-guide.md) | Follow rows through splitting, training, validation, preprocessing and nested evaluation |
| Choosing a method | [Basic algorithm guide](basic-algorithms.md) | Regression, classification, trees, kernels, clustering, PCA and survival |
| Independent frameworks and research methods | [Methods and deployments](methods-and-deployments.md) | Python nested workflows, direct R survival analysis and limma expression contrasts |
| Resampling, preprocessing and tuning | [Caret deployment](caret-deployment.md) | Fit elastic-net and random-forest classifiers with a protected test partition |
| Advanced training and informative variables | [Breast cancer training and feature selection](advanced-breast-cancer-training.md) | Select assay columns inside nested person-grouped folds; inspect coefficients, selection frequency and held-out importance |
| Fair model comparison | [Matched assay procedures](model-comparison.md) | Fixed all-feature baseline and tuned subset procedure assessed on the same excluded people |
| Reading ML figures | [Plotting gallery](gallery/README.md) | Rebuild seven figures from saved splits, candidates, feature summaries and predictions |
| Robustness and tuning budgets | [Phase 4 synthetic stress experiment](robustness-experiment.md) | Prespecified changes in allocation, missingness and correlation; equal-fit grid/random search, complete candidate histories and guarded validation |
| Repeated-cohort replication | [Phase 4B runner and report](replication-experiment.md) · [Frozen protocol](replication-protocol.md) | Three declared new synthetic cohorts, 1,872-fit ceiling, explicit stability denominators and durable failed-run records |
| Person-aware uncertainty | [Phase 4C calculation](uncertainty-assessment.md) · [Frozen protocol](uncertainty-protocol.md) | Whole-person paired resampling of saved predictions; conditional ranges distinguished from full-procedure uncertainty |
| Rust model deployment | [Frozen assay inference in Rust](rust-deployment.md) | Compile a prediction CLI and check both fitted procedures against Python |
| Native Rust training | [Linfa baseline and numerical validation](rust-native-training.md) · [Frozen objective](rust-training-protocol.md) | Training-only preparation, person-disjoint folds, matched objective, explicit convergence checks and preserved failures |
| Rust ML research | [Five-year literature review](rust-ml-literature.md) | Appraise 11 publications/manuscripts and six pinned software sources; connect deployment, native training and single-cell methods to the book |
| Package selection | [Biomedical package guide](package-guide.md) | Match software to tabular, survival, expression and single-cell tasks |
| Breast cancer evidence | [Study evidence and implementation](breast-cancer-evidence.md) | Screening trials, future risk, prognosis, response prediction, author-code mechanisms and review limits |
| Methods from recent research | [Paper-to-code studies](recent-code-studies.md) | Connect 2025–2026 papers and a leakage reference to implementation decisions |
| Corpus review and validation | [Dated appraisal and executed run](corpus-review.md) | Review all 36 records, inspect access limits and reproduce synthetic verification |
| Recent tuning research | [2021–2025 evidence corpus](recent-tuning-evidence.md) | Nine new primary methods papers tied to assay prediction, budgets, defaults and overtuning |
| Selection and validation research | [2021–2026 evidence corpus](recent-selection-validation.md) | Gene-panel stability, validation precision, leakage, tabular models and survival comparisons |
| Model tuning evidence and practice | [Project tuning guide](model-tuning.md) | Actual search grids, metrics, candidate traces, fit budgets, selection bias and advanced search references |
| Computational efficiency | [Optimization and evaluation](optimization.md) | Measure runtime and reduce redundant fitting without changing the evaluation question |
| Scientific software requirements | [Implementation gates](../02_biomedical_coding/IMPLEMENTATION_GATES.md) | Input contracts, study design, permissions and release evidence |

The [learning roadmap](../docs/learning-roadmap.md) includes the fixed all-feature comparison, seven-figure gallery, bounded robustness baseline, repeated-cohort assessment and conditional whole-person uncertainty. G1/G2 close the defined synthetic Phase 4 milestone. The [gate ledger](../docs/roadmap-gates.md) keeps full-procedure uncertainty and clinical claims separate. The [native Rust baseline](rust-native-training.md) now checks a separately frozen objective and numerical contract. The survival case is next, beginning with its own endpoint protocol.

## Run the caret example

Requirements: R and the `caret`, `glmnet`, `ranger` and `pROC` packages. From the repository root:

```bash
Rscript --vanilla 04_machine_learning/examples/caret_case.R /tmp/biomedical-caret-run
```

Choose a new output directory outside the repository whose parent exists. The command creates synthetic data, saves patient assignments and fold membership, tunes two model families, evaluates their probabilities alongside a development-prevalence baseline, and saves models, metrics and execution records. It refuses to overwrite an existing directory.

The example has one row per independent person. Repeated visits, related participants, multiple specimens per donor, survival outcomes, and external-site validation require different split and model contracts. The runner rejects duplicate person identifiers.

## Follow the paired-specimen example

The [advanced guide](advanced-breast-cancer-training.md) adds a synthetic assay-column selection deployment: 60 people, two specimen categories per person, 48 arbitrary features, nested tuning of subset size and regularization, and a protected final test. It connects each decision to Chapter 11 of the book. It does not fit the 60-gene catalog or analyze participant records.

```bash
python3 04_machine_learning/examples/breast_cancer_feature_selection.py /tmp/breast-cancer-feature-selection
python3 04_machine_learning/tests/test_breast_cancer_feature_selection.py
```

Use the pinned Python dependencies and a new output directory outside the repository with an existing parent.

## Run the Rust prediction deployment

The [Rust guide](rust-deployment.md) adds a compiled prediction CLI for the same two fitted assay procedures, with saved preprocessing parameters and cross-language parity checks. Start with its committed synthetic example; prediction requires no Python runtime after compilation. The [native training extension](rust-native-training.md) is opt-in and separately validated; the frozen inference baseline retains its own CI path.

## Check the implementation

```bash
Rscript --vanilla 04_machine_learning/tests/test_caret_case.R
python3 scripts/check_documentation.py
```

Checks challenge partition overlap, invalid inputs, fold coverage, metric direction, tied probabilities, holdout leakage, saved predictions, and export integrity. They do not require a minimum synthetic AUC. [Continuous integration](../.github/workflows/machine-learning-validation.yml) installs dependencies and executes the documented command.

The [independent deployments](methods-and-deployments.md) add classification, numerical prediction, PCA/clustering, survival analysis and expression contrasts without a caret dependency. Read the [breast cancer application narrative](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) to connect these questions to people, specimens, genes and follow-up. Other packages and paper repositories have their review status stated separately. No study datasets, model weights or publication PDFs are redistributed here.
