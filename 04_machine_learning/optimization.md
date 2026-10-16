# Optimization without weakening evaluation

[Machine learning](README.md) · [Caret deployment](caret-deployment.md) · [Paper-to-code studies](recent-code-studies.md)

Optimize measured bottlenecks after the prediction task and independent unit are fixed. Preserve assessment design while comparing runtime, memory, and output behavior.

| Mechanism | Implementation in the current case | What to measure before changing it |
| --- | --- | --- |
| Explicit small tuning grids | Six elastic-net candidates; four forest candidates | Development score, stability, elapsed time and total fitting budget |
| Identical resampling across engines | Saved `index` and `indexOut` reused | Paired fold comparisons and class balance |
| Avoid redundant standardization | Caret owns scaling; glmnet standardization disabled | Check saved preprocessing and replayed predictions |
| Bound parallelism | Serial caret; one ranger thread; CI limits BLAS/OpenMP threads | Peak memory and time before enabling a parallel backend |
| Reuse fitted transformations | Prediction through the caret object | Equality of saved/reloaded probabilities; no assessment-time refit |
| Save selection artifacts | All tuning results and selected-setting out-of-fold predictions | Distinguish score selection from independent evaluation |
| Publish completed output atomically | Stage files beside destination, rename only after success | Failure leaves no partially published destination |

The workflow records elapsed time rather than asserting that a particular engine is fastest. This case is too small to establish a general performance ranking. Repeated timing under controlled hardware and fresh processes is needed for benchmarking.

## High-dimensional assays

Separate assay QC from supervised selection. Any learned imputation, normalization, PCA, feature ranking or batch correction that can use information across people needs a training-only fit consistent with the prediction goal. Document transformations that instead use an external frozen reference. Test patient/sample alignment before coercing sparse matrices into dense representations; budget memory before expanding gene matrices.

Use regularized linear and simple baseline methods before escalating to expensive embeddings. For single-cell data, avoid interpreting the number of cells as the number of independent donors. For tissue images, split people before generating patches. A representation trained on evaluation samples can change the evaluation setting even when target labels are hidden.

## Next executable gates

- Add nested outer evaluation before using resampling results to compare tuned workflow families.
- Add group/time/site-aware fixtures before admitting repeated visits or multi-site forecasting.
- Add a clean `renv` restore and package-version compatibility checks before promising environment restoration.
- Add uncertainty, subgroup and calibration assessments sized for the study before interpreting probabilities as transportable risks.
- Benchmark any parallel backend with explicit worker seeds, thread limits and peak memory; avoid parallelizing both folds and each learner without a resource budget.

These are pending implementation gates. They are not capabilities of the current synthetic runner.
