# Biomedical machine-learning package guide

[Machine learning](README.md) · [Methods and deployments](methods-and-deployments.md) · [Primary documentation](../02_biomedical_coding/PRIMARY_DOCUMENTATION.md)

Reviewed for this guide: 2026-10-16. Documentation links are entry points; installation versions and scientific suitability must be checked for the actual study. **Executable** means wired into the synthetic runner and CI; **reference** means documentation supplied without a local deployment here.

Choose packages along the [breast cancer book's workflow](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data): align assay/specimen identities, define a tissue or follow-up target, train on development people, and interpret held-out results. The [advanced training guide](advanced-breast-cancer-training.md) links feature selection and importance to this sequence. Package capability alone is not evidence that a breast cancer model has been validated.

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
| [survival](https://cran.r-project.org/package=survival) | Direct Cox model, PH diagnostics and held-out concordance | Time origin, event coding and censoring are mandatory; relative score is not horizon risk | [Executable R methods](methods-and-deployments.md#r-survival-and-expression-analysis) |
| [limma](https://bioconductor.org/packages/limma/) | Direct batch-adjusted expression contrast with variance moderation | Log2-expression scale, sample alignment and identifiable design; inference rather than classifier validation | [Executable R methods](methods-and-deployments.md#r-survival-and-expression-analysis) |
| [edgeR](https://bioconductor.org/packages/edgeR/) | Sequencing count models | Retain counts and library structure; do not replace with arbitrary transformed values | Reference for ML; existing plotting resources have separate checks |
| [DESeq2](https://bioconductor.org/packages/DESeq2/) | Count-based differential expression | Biological replicates and identifiable design; inference is not classifier validation | Reference |
| [SummarizedExperiment](https://bioconductor.org/packages/SummarizedExperiment/) | Aligned assay, row and sample metadata containers | Stable identifiers and compatible dimensions | Reference |
| [scikit-learn](https://scikit-learn.org/stable/modules/compose.html) | Classification, regression, PCA, k-means and nested assay-column selection pipelines | Family-disjoint nested CV and training-only transforms; temporal assessment needs a different design | [Executable Python methods](methods-and-deployments.md#python-pipelines-and-nested-evaluation) |
| [NumPy](https://numpy.org/doc/stable/) | Numeric arrays, synthetic generation and NPZ inputs | Aligned observation axis; finite-target and shape checks | Executable Python methods |
| [SciPy](https://docs.scipy.org/doc/scipy/) | Numerical dependency supporting the Python estimators | Record installed version and compatible binary environment | Executed dependency; no standalone SciPy method here |
| [joblib](https://joblib.readthedocs.io/) | Save and reload fitted Python pipelines | Trusted artifacts and compatible runtime; verify replayed predictions | Executable Python methods |
| [Rust inference dependencies](rust/Cargo.toml) | Serde/serde_json parse versioned models, csv parses assay tables, sha2 records artifact identities | Frozen development-fitted transforms and coefficients; ordered features and class-1 probability parity | [Executable Rust prediction](rust-deployment.md) |
| [Linfa](https://docs.rs/linfa-logistic/0.8.1/linfa_logistic/) / [SmartCore](https://docs.rs/smartcore/0.6.15/smartcore/) | Native Rust classical-model training routes | Rebuild grouping, preprocessing, probability and tuning contracts for the chosen learner | Reference; fitting not deployed here |
| [Burn](https://burn.dev/) / [Candle](https://github.com/huggingface/candle) | Rust neural/tensor model training or execution | Pin model/backend, weight provenance, precision and grouped assessment | Reference |
| [ort](https://docs.rs/ort/latest/ort/) | Rust binding for compatible ONNX Runtime graphs | Full-transform conversion, operator support and probability parity need checks | Reference |
| [Scanpy](https://scanpy.readthedocs.io/) | Single-cell preprocessing and exploratory analysis | Assay layer, QC policy and donor provenance remain explicit | Reference |
| [scvi-tools](https://docs.scvi-tools.org/) | Probabilistic single-cell representations | Register correct count layer and batch covariates; assess at donor level | Reference |
| [renv](https://rstudio.github.io/renv/) | R dependency capture and reconstruction | Restore in a clean environment; a lock does not preserve datasets or hardware | Reference |
| [targets](https://docs.ropensci.org/targets/) | Dependency-aware execution and caching | Every dependency/configuration affecting a result belongs in the graph | Reference |

The [Rust ML literature review](rust-ml-literature.md) appraises 11 publications/manuscripts and inspects six upstream source files at immutable commits. It explains why probability interfaces, loss definitions, validation boundaries and native runtime versions matter for these package choices. Those inspections do not change the reference packages into executed deployments.

The runnable workflows use CPU dependencies. The Python direct dependencies have a [version specification](requirements-python.txt); R runs record their session environment. Install GPU frameworks and foundation-model environments separately. A package citation, a valid installation, and a completed benchmark are different forms of evidence.

## Pair a package with a deployment record

For each adopted package, retain its version, upstream documentation, input schema, fitting parameters, seed/thread policy, resampling indices, prediction interface, expected outputs, invalid-input fixture, runtime, and known limitations. Also retain the source release and model-weight identity when reproducing a paper. Record the code license and the weight/data terms separately when they differ.

## Additional engines to evaluate

For support-vector machines and boosting, consult [kernlab](https://cran.r-project.org/package=kernlab), [e1071](https://cran.r-project.org/package=e1071), and [XGBoost](https://xgboost.readthedocs.io/). Before adding an engine, define its tuning space and budget, preprocessing, probability/calibration behavior, serialization contract and a replay test on the same frozen development partitions. These engines are not executed by the current runner.
