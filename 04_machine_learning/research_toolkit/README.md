# Configurable synthetic oncology machine-learning lab

[Machine learning](../README.md) · [Cancer-wide scope](../../docs/cancer-research-scope.md) · [Current breast cancer book](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) · [Research workflow](../../docs/research-workflow.md)

**Purpose:** Change validated numeric experiment variables and rerun a complete **synthetic-only** machine-learning research example. The same educational principles apply across oncology, but this code is **not** a clinical tool or a general real-data ingestion service. Its current fixture illustrates a *fictional paired breast-specimen category*, **not** an analysis of TCGA-BRCA or another cancer dataset.

This teaching lab was extracted from the [draft public-data/privacy PR #7](https://github.com/pskeffington/pauls_notes/pull/7) so **R4 scientific software delivery can be reviewed independently of D0 repository administration**. It contains no GDC API adapter, no patient-data reader and no permission to fit real cancer data. The draft GDC metadata preflight still applies only to the TCGA-BRCA example and remains separate.

## Configure and execute

Edit the [JSON file](synthetic_brca_config.json). There is deliberately **no data path, input-file flag, remote provider or real-data stage**. The permitted keys are:

| JSON field | Meaning and current limits |
| --- | --- |
| `schema_version`, `stage` | Exactly `1` and `synthetic-validation`; other modes rejected |
| `data.people` | Number of **invented independent persons**, 20–1,000 |
| `data.specimens_per_person` | 1–5 simulated observations per person, grouped together in splits |
| `data.features`, `data.informative` | 4–500 anonymous measurements; 2–`features` informative measurements |
| `data.missing_fraction` | Simulated missing measurements, 0–0.4 |
| `design.outer_folds`, `design.inner_folds` | Person-grouped folds, 2–5 each with feasibility constraints |
| `design.feature_counts`, `design.regularization_C` | Candidate feature counts and positive L2 inverse strengths; no more than 30 grid combinations |
| `models`, `seed` | Fixed baseline and logistic model allowlist; nonnegative integer random seed |

Use pinned [Python requirements](../requirements-python.txt). From the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r 04_machine_learning/requirements-python.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 .venv/bin/python \
  04_machine_learning/research_toolkit/research_runner.py \
  --config 04_machine_learning/research_toolkit/synthetic_brca_config.json \
  --output /tmp/new-unique-synthetic-oncology-run
```

The output directory **must not exist** and **must be outside** the source repository. Do not commit any generated run directory or row-level artifacts. For a second experiment, change only the accepted JSON numeric values and choose a **new** output location; record the change as a different synthetic experiment, never as an existing study's frozen validation.

## What the report demonstrates

Each `report.json` contains the seed, configuration/source SHA-256 hashes, runtime metadata, group/row counts and, for each outer fold and candidate learner:

- **Allocation:** unique train-person IDs and test-person IDs; all dependent specimens from a person stay on one side of the outer split. No held-out person may appear in the inner tuning folds.
- **Training-only preparation:** median imputation, scaling, univariate feature selection and logistic fitting inside the scikit-learn pipeline, refitted in each inner cross-validation fold.
- **Inner candidate audit:** every tried feature-count/C pair, inner balanced accuracy mean/std and rank, followed by the chosen settings; selected anonymous feature indices and standardized model coefficients for comparison.
- **Outer assessment:** balanced accuracy, accuracy, log loss, class-1 probabilities and raw **invented** labels, kept separate from inner candidates.
- **Descriptive calibration counts:** five prespecified probability bins containing observation counts, positive-label counts and mean class-1 probability. Empty bins have a null mean; these descriptive bins are **not** calibration confidence intervals or proof of external reliability.

The majority-class predictor is a comparison baseline. The generator returns its own fictional labels together with its feature matrix; they must **not** be randomly reassigned afterward. Every outer fold is a *development experiment*, not an independent hospital/site validation. Class 1 means the generator's invented positive category, **not cancer diagnosis, a molecular subtype, a survival event or a treatment outcome**.

The report contains explicit `clinical_use_authorized=false`, `patient_level_training_authorized=false`, `real_cancer_data_processed=false` and the **NOT FOR CLINICAL USE** disclaimer. There is **no independent clinical validation**, and no evidence is asserted for a different cancer cohort.

## Verify and extend safely

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 -m unittest discover \
  -s 04_machine_learning/research_toolkit -p 'test_research_runner.py' -v
```

The [unit tests](test_research_runner.py) exercise determinism, exact person-group exclusivity, candidate-history counts, feature-selection consistency, calibration denominators, intentional generator signal, forbidden real-data config keys, output containment and no-overwrite behavior. The [automated CI](../../.github/workflows/configurable-ml-toolkit.yml) runs those checks and a command-line smoke execution on every relevant PR.

**To extend this beyond the current invented binary classification task:** write a **separate** study protocol and source-specific adapter with a declared cancer context, biological units, labels/endpoints, time horizon, measurement normalization, privacy/access review, grouping, split map, baseline, tuning budget, uncertainty and software/numerical evidence. Other cancer datasets, including other GDC projects, are **not** admitted by editing this JSON. Real participant-derived data and trained weights belong outside this public repository.

**Mandatory limitation:** RESEARCH AND EDUCATIONAL USE ONLY. NOT FOR CLINICAL USE. These lessons do not authorize screening, diagnosis, individual prognosis, treatment selection, or publication of participant-linked predictions.
