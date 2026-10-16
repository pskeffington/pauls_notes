# Biomedical machine-learning package guide

[Machine learning](README.md) · [Caret deployment](caret-deployment.md) · [Primary documentation](../02_biomedical_coding/PRIMARY_DOCUMENTATION.md)

Reviewed for this guide: 2026-10-16. Documentation links are entry points; installation versions and scientific suitability must be checked for the actual study. **Executable** means wired into the synthetic runner and CI; **reference** means documentation supplied without a local deployment here.

| Package or stack | Research task and deployment mechanism | Input/assessment contract | Local status |
| --- | --- | --- | --- |
| [caret](https://topepo.github.io/caret/) | Resampling orchestration through `train`, `trainControl`, `predict.train` | Explicit partitions; all learned transforms inside resampling | Executable |
| [glmnet](https://cran.r-project.org/package=glmnet) | Penalized binary regression through caret `method = "glmnet"` | Numeric predictors; tune penalty within development; never infer causality from coefficients | Executable |
| [ranger](https://cran.r-project.org/package=ranger) | Probability forests through caret `method = "ranger"` | Freeze tree/thread budget; evaluate probabilities, not only labels | Executable |
| [pROC](https://cran.r-project.org/package=pROC) | ROC assessment through `roc` and `auc` | Explicit event level and direction; independent observations | Executable |
| [recipes](https://recipes.tidymodels.org/) | Declarative preprocessing prepared on analysis folds | `prep` on training rows; `bake` on assessment rows; retain factor policy | Reference |
| [rsample](https://rsample.tidymodels.org/) | Grouped, stratified and temporal splits | Choose independence unit and time ordering before fitting | Reference |
| [yardstick](https://yardstick.tidymodels.org/) | Probability, classification and survival metrics | Declare event level, censoring semantics and metric estimator | Reference |
| [mlr3](https://mlr3book.mlr-org.com/) | Task/learner/resampling pipelines and nested benchmarking | Match learner properties to task and resampling design | Reference |
| [survival](https://cran.r-project.org/package=survival) | Censoring-aware survival models | Time origin, event coding, censoring and horizon are mandatory | Reference |
| [limma](https://bioconductor.org/packages/limma/) | Expression analysis with planned design and contrasts | Expression scale, design and sample alignment precede fitting | Reference |
| [edgeR](https://bioconductor.org/packages/edgeR/) | Sequencing count models | Retain counts and library structure; do not replace with arbitrary transformed values | Reference for ML; existing plotting resources have separate checks |
| [DESeq2](https://bioconductor.org/packages/DESeq2/) | Count-based differential expression | Biological replicates and identifiable design; inference is not classifier validation | Reference |
| [SummarizedExperiment](https://bioconductor.org/packages/SummarizedExperiment/) | Aligned assay, row and sample metadata containers | Stable identifiers and compatible dimensions | Reference |
| [scikit-learn](https://scikit-learn.org/stable/modules/compose.html) | Python pipelines and model selection | Put preprocessing in `Pipeline`; preserve grouped/temporal assessment | Reference |
| [Scanpy](https://scanpy.readthedocs.io/) | Single-cell preprocessing and exploratory analysis | Assay layer, QC policy and donor provenance remain explicit | Reference |
| [scvi-tools](https://docs.scvi-tools.org/) | Probabilistic single-cell representations | Register correct count layer and batch covariates; assess at donor level | Reference |
| [renv](https://rstudio.github.io/renv/) | R dependency capture and reconstruction | Restore in a clean environment; a lock does not preserve datasets or hardware | Reference |
| [targets](https://docs.ropensci.org/targets/) | Dependency-aware execution and caching | Every dependency/configuration affecting a result belongs in the graph | Reference |

The runner deliberately has a small CPU dependency set. Install GPU frameworks and foundation-model environments separately. A package citation, a valid installation, and a completed benchmark are different forms of evidence.

## Pair a package with a deployment record

For each adopted package, retain its version, upstream documentation, input schema, fitting parameters, seed/thread policy, resampling indices, prediction interface, expected outputs, invalid-input fixture, runtime, and known limitations. Also retain the source release and model-weight identity when reproducing a paper. Record the code license and the weight/data terms separately when they differ.

## Additional engines to evaluate

For support-vector machines and boosting, consult [kernlab](https://cran.r-project.org/package=kernlab), [e1071](https://cran.r-project.org/package=e1071), and [XGBoost](https://xgboost.readthedocs.io/). Before adding an engine, define its tuning space and budget, preprocessing, probability/calibration behavior, serialization contract and a replay test on the same frozen development partitions. These engines are not executed by the current runner.
