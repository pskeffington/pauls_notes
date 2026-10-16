# Caret: preprocessing, tuning and saved-model deployment

[Machine learning](README.md) · [Package guide](package-guide.md) · [Optimization](optimization.md)

## Define the prediction problem

The [runnable case](examples/caret_case.R) predicts an invented binary outcome from four numeric predictors. The schema is `person_id`, `outcome`, `marker_a`, `marker_b`, `age_years`, and `noise`. Markers have arbitrary units; age is in years. `outcome` is a factor with levels `c("case", "control")`; **case is the positive event**. Identifiers and outcomes are excluded from the predictor matrix by an explicit allowlist.

The generator creates 160 independent synthetic people and some missing marker values. A stratified split reserves approximately one quarter of each class for the final assessment. Four stratified folds inside development data supply tuning scores. Counts are exported rather than assumed, since class counts determine rounding.

## Keep each operation inside its proper partition

| Operation | Where it learns | What is retained |
| --- | --- | --- |
| Patient assignment | Fixed split plan before fitting | Row indices and person membership |
| Median imputation, centering and scaling | Each resample's training rows through `train(preProcess = ...)` | Final development preprocessing object in the saved caret model |
| Elastic-net tuning | Development folds only | Six explicit `alpha`/`lambda` candidates and selection results |
| Random-forest tuning | Same development folds | Four `mtry`/`min.node.size` candidates, 100 trees, Gini splitting |
| Final fitting | All development rows after tuning | One fitted caret object per family |
| Probability assessment | Reserved test people | Predictions, ROC AUC, average precision, Brier score, sensitivity and specificity |
| Calibration description | Test predictions and outcomes | Fixed-width probability bins, counts, mean prediction and observed event fraction |

Median imputation is an illustrative policy; it does not solve informative missingness. Scaling is retained in both pipelines to make their preprocessing contract explicit. Forests do not generally need scaling. `glmnet` receives `standardize = FALSE` because caret supplies the learned scaling. No supervised feature selection, batch correction or balancing is performed before splitting.

## Execute and inspect

Install dependencies explicitly in a suitable R environment:

```r
install.packages(c("caret", "glmnet", "ranger", "pROC"))
```

The source does not install packages or read data when sourced. Run from the repository root:

```bash
Rscript --vanilla 04_machine_learning/examples/caret_case.R /tmp/biomedical-caret-run
```

| Output | Inspect it for |
| --- | --- |
| `split_membership.csv`, `split_plan.rds` | Development/test membership and local development-fold indices |
| `development_selection.csv` | Best settings for each family and its selection score |
| `elastic_net_tuning.csv`, `random_forest_tuning.csv` | Every candidate and its resampling summaries |
| `*_oof_predictions.csv` | Out-of-fold predictions for the selected settings, indexed within development |
| `test_predictions.csv`, `test_metrics.csv` | Untouched-test predictions and comparison with a prevalence baseline |
| `test_calibration.csv` | Calibration descriptives with bin counts; sparse bins have large uncertainty |
| `model_bundle.rds` | Caret objects, preprocessing, predictor allowlist, training identifiers, plan and seeds |
| `training_timing.csv` | Elapsed fit time and candidate count for each family |
| `package_versions.csv`, `session_info.txt`, `file_inventory.csv` | Executed versions, runtime environment and file-integrity inventory |

Predict through the saved caret object, which applies its learned preprocessing:

```r
bundle <- readRDS("/tmp/biomedical-caret-run/model_bundle.rds")
cohort <- read.csv("/tmp/biomedical-caret-run/synthetic_cohort.csv")
new_predictors <- cohort[bundle$plan$test, bundle$predictors]
probability <- predict(bundle$models$elastic_net,
                       newdata = new_predictors, type = "prob")$case
```

Using `$finalModel` directly bypasses caret preprocessing. The [caret training manual](https://topepo.github.io/caret/model-training-and-tuning.html) and [preprocessing reference](https://search.r-project.org/CRAN/refmans/caret/html/preProcess.html) describe these interfaces. For alternative split structures, consult [caret data splitting](https://topepo.github.io/caret/data-splitting.html).

## Interpret the assessment

ROC direction is fixed so larger case probabilities indicate cases; it is never automatically reversed to improve the score. Average precision groups tied probabilities. Brier score measures squared probability error. The classification threshold is fixed at 0.5 before assessment; it is not a clinical decision threshold.

Tuned cross-validation scores and the selected-setting out-of-fold predictions are **selection evidence**, not unbiased estimates of the entire tuning procedure. Do not choose the winning model family from test performance and then describe that same test as untouched. Use nested evaluation or a new external assessment when comparing and selecting workflows. This example reports both prespecified families without selecting a family from test outcomes.

The current output provides no confidence intervals, recalibration, subgroup validation, decision-curve analysis, or prospective clinical assessment. Its fixed synthetic holdout verifies software behavior, not biomedical usefulness. Package/session records describe the executed environment; create and test a dependency lock before claiming environment restoration.

## Adapt to a study

Define outcome timing and eligibility before changing the predictor schema. Use donor/person/family groups for dependent observations, chronological splits for forecasting, and independent sites when transportability is the question. Keep preprocessing and feature selection inside the corresponding training partition. An omics classifier also needs annotation, assay-scale and batch/design checks; a survival endpoint needs censoring-aware evaluation rather than this binary runner.
