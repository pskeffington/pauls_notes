# Methods and deployments beyond caret

[Machine learning subjects](README.md) · [Reader's introduction](what-is-machine-learning.md) · [Algorithm guide](basic-algorithms.md)

The workflows below are independent implementations. The Python and direct R methods do not import or call caret. All inputs are synthetic; choose a new output directory outside the repository.

In the [breast cancer narrative](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data), classification addresses a defined specimen label, numerical regression a continuous measurement, survival an event over follow-up, and expression inference an adjusted assay contrast. These are different questions. The generic fixtures below teach their mechanisms; the [paired-specimen selection example](advanced-breast-cancer-training.md) adds an explicit synthetic tissue-category task.

| Research task | Implementation | Assessment and output |
| --- | --- | --- |
| Binary prediction | Python logistic regression, random forests and histogram boosting | Family-disjoint outer and inner cross-validation; ROC AUC, average precision, Brier score and final holdout |
| Numerical prediction | Python ridge regression and random forests | Same family partitions; nested out-of-fold predictions, RMSE, MAE, R-squared and mean baseline |
| Representation and clustering | Python imputation, scaling, PCA and k-means | Development-fitted transforms; new-person projections, cluster assignments and descriptive silhouette |
| Time-to-event analysis | Direct R `survival::coxph` | Prespecified predictors; held-out concordance with explicit risk direction and training PH diagnostics |
| Expression association | Direct R `limma::lmFit`, `eBayes`, `topTable` | Sample alignment; full-rank batch/group design; log2-expression contrast and BH adjustment |

## Python: pipelines and nested evaluation

Use Python 3.12 and the pinned direct dependencies in [requirements-python.txt](requirements-python.txt):

```bash
python3 -m pip install -r 04_machine_learning/requirements-python.txt
python3 04_machine_learning/examples/sklearn_methods.py /tmp/biomedical-python-methods
```

The fixture has 120 people in 60 invented two-person families, five numeric predictors, and separate binary and numerical targets. Family membership is a grouping variable, not a predictor. A group split reserves families before fitting. Each of three outer development folds contains its own three-fold grouped parameter search. Imputation and scaling are inside `Pipeline` at both levels. Every development person receives one outer-held-out prediction per model family.

`metrics.json` records nested development scores, final test scores, parameter choices, predictions and inner/outer membership in development-local row coordinates. `splits.json` maps these to full-cohort person/family indices. `models.joblib`, `synthetic_cohort.npz` and `versions.json` support local replay. The version record includes Python; `sha256.json` records file checksums for integrity checks. Load only trusted model bundles.

Final test scores are for the prespecified model families; the runner does not select a winning family from them. Nested estimates have sampling uncertainty and correlated family observations; the example supplies no uncertainty intervals or external-site validation. Nested cross-validation assesses hyperparameter search within each family, not a later choice among families made from those scores.

PCA and k-means use development predictors only, without targets. Three clusters and two components are fixed illustration settings. Test silhouette is a descriptive geometry score, not a disease-label validation. The code handles undefined silhouette when the assigned labels cannot support it.

The [project tuning guide](model-tuning.md) records exact candidate values, selection objectives, evidence references and remaining evaluation boundaries for both Python and R workflows.

## Paired specimens and training-only feature selection

The [advanced breast cancer guide](advanced-breast-cancer-training.md#executable-example-selecting-columns-while-holding-people-apart) follows 60 invented people and two specimen categories per person. Its [Python deployment](examples/breast_cancer_feature_selection.py) performs nested, person-grouped selection of assay columns, then exports held-out predictions, the final selected subset, standardized coefficients, outer-fold selection counts and descriptive permutation diagnostics. The guide documents the full-cohort index convention and interpretation limits.

## R: survival and expression analysis

Install `survival` through CRAN and `limma` through the Bioconductor release matching the R environment. Then run:

```bash
Rscript --vanilla 04_machine_learning/examples/research_methods.R /tmp/biomedical-r-methods
```

The survival example uses one row per independent person, positive follow-up in months, and event codes 1 = observed event and 0 = right-censored. Complete numeric predictors are required. The Cox model uses a fixed formula; higher linear predictors mean greater relative hazard, so held-out concordance uses `reverse = TRUE`. `cox.zph` is a training diagnostic, not an automatic acceptance decision. Absolute horizon risk, competing risks, recurrent events and informative censoring require additional work.

The expression fixture has 120 invented features and 24 samples, balanced control/case groups and a crossed batch factor. The declared input scale is `log2_expression`. Raw counts require an appropriate count/voom workflow instead. The code aligns metadata to assay columns, rejects duplicate identities and a confounded design, and estimates the case-minus-control coefficient. BH correction covers the tested feature family. Differential expression does not supply an independent prediction assessment.

## Run the checks

```bash
python3 04_machine_learning/tests/test_sklearn_methods.py
Rscript --vanilla 04_machine_learning/tests/test_research_methods.R
```

Checks include family leakage at both CV levels, held-out mutation, output replay, outcome-independent embeddings, censor/event coding, metadata reorder invariance and nonidentifiable designs. The [expanded CI workflow](../.github/workflows/machine-learning-validation.yml) executes these alongside the caret case.

Primary implementation guidance: [pipelines](https://scikit-learn.org/stable/modules/compose.html), [group cross-validation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html), [nested evaluation](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html), [concordance](https://www.stat.ethz.ch/R-manual/R-devel/library/survival/html/concordance.html), [PH diagnostics](https://www.stat.ethz.ch/R-manual/R-devel/library/survival/html/cox.zph.html), and [limma design matrices](https://bioconductor.org/packages/release/workflows/vignettes/RNAseq123/inst/doc/designmatrices.html).
