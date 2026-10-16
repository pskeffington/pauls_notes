# Machine learning for biomedical research

Authored by Paul Skeffington · Compiled with OpenAI

[Paul's Notes](../README.md) · [Computing subjects](../03_learning/README.md) · [Research workflow](../docs/research-workflow.md)

Build a prediction workflow around the observation unit, input measurements, and evaluation design. Choose a subject or run the synthetic deployment.

| Subject | Resource | Practical purpose |
| --- | --- | --- |
| Understanding the subject | [What is machine learning?](what-is-machine-learning.md) | Features, targets, learning, assessment and interpretation in plain language |
| Seeing the data flow | [Visual data guide](visual-data-guide.md) | Follow rows through splitting, training, validation, preprocessing and nested evaluation |
| Choosing a method | [Basic algorithm guide](basic-algorithms.md) | Regression, classification, trees, kernels, clustering, PCA and survival |
| Independent frameworks and research methods | [Methods and deployments](methods-and-deployments.md) | Python nested workflows, direct R survival analysis and limma expression contrasts |
| Resampling, preprocessing and tuning | [Caret deployment](caret-deployment.md) | Fit elastic-net and random-forest classifiers with a protected test partition |
| Package selection | [Biomedical package guide](package-guide.md) | Match software to tabular, survival, expression and single-cell tasks |
| Methods from recent research | [Paper-to-code studies](recent-code-studies.md) | Connect 2025–2026 papers and a leakage reference to implementation decisions |
| Computational efficiency | [Optimization and evaluation](optimization.md) | Measure runtime and reduce redundant fitting without changing the evaluation question |
| Scientific software requirements | [Implementation gates](../02_biomedical_coding/IMPLEMENTATION_GATES.md) | Input contracts, study design, permissions and release evidence |

## Run the caret example

Requirements: R and the `caret`, `glmnet`, `ranger` and `pROC` packages. From the repository root:

```bash
Rscript --vanilla 04_machine_learning/examples/caret_case.R /tmp/biomedical-caret-run
```

Choose a new output directory outside the repository whose parent exists. The command creates synthetic data, saves patient assignments and fold membership, tunes two model families, evaluates their probabilities alongside a development-prevalence baseline, and saves models, metrics and execution records. It refuses to overwrite an existing directory.

The example has one row per independent person. Repeated visits, related participants, multiple specimens per donor, survival outcomes, and external-site validation require different split and model contracts. The runner rejects duplicate person identifiers.

## Check the implementation

```bash
Rscript --vanilla 04_machine_learning/tests/test_caret_case.R
python3 scripts/check_documentation.py
```

Checks challenge partition overlap, invalid inputs, fold coverage, metric direction, tied probabilities, holdout leakage, saved predictions, and export integrity. They do not require a minimum synthetic AUC. [Continuous integration](../.github/workflows/machine-learning-validation.yml) installs dependencies and executes the documented command.

The [independent deployments](methods-and-deployments.md) add classification, numerical prediction, PCA/clustering, survival analysis and expression contrasts without a caret dependency. Read the [breast cancer application narrative](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) to connect these questions to people, specimens, genes and follow-up. Other packages and paper repositories have their review status stated separately. No study datasets, model weights or publication PDFs are redistributed here.
