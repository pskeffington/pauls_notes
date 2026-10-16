# Paired-specimen comparison protocol, version 1

Declared before the comparison runner's first execution on 2026-10-16.

**Question:** How do two declared training procedures compare on invented paired specimens from people excluded from fitting? This is a software teaching experiment using arbitrary assay features, not a study of named genes or participants.

| Design choice | Declared value |
| --- | --- |
| Generator | Existing 60-person, two-specimen, 48-feature fixture; cohort seed 26101602 |
| Development/test allocation | GroupShuffleSplit, test fraction 0.25, split seed 26101603 |
| Outer assessment | Three person-grouped folds on development, shared by both procedures |
| Selected procedure | Training-only median imputation, F-score selection, scaling, logistic model; k in 5/10/20 and C in 0.1/1.0; three grouped inner folds, negative Brier scoring |
| Fixed comparator | Training-only median imputation, scaling, logistic model with all 48 features; C = 1.0 and max_iter = 1000; no hyperparameter search |
| Context baseline | Outer-training prevalence for each outer fold; full-development prevalence for the reserved test |
| Primary comparison | Mean binary Brier error; selected minus all-feature error, negative favors the selected procedure |
| Additional descriptive measures | AUROC and average precision for each procedure, plus person-averaged paired error differences |
| Fitting budget | Selected procedure: 76 pipeline fits; fixed comparator: 3 outer fits + 1 development fit; 80 pipeline fits total; prevalence is computed arithmetically |
| Final assessment | Refit each declared procedure on development, then assess both on the same 15 reserved people; neither is selected as a winner for deployment |
| Failure policy | Fit errors stop the run; reject broken person partitions and completely missing training columns; no favorable replacement scores |
| Interpretation | Compare complete procedures, including different tuning budgets; do not attribute differences solely to feature selection |

Both specimens of a person stay together. Test measurements and outcomes do not enter training, tuning or panel review. The generator and model-fitting seeds are recorded; no seed, C, subset size or procedure is changed after inspecting the comparison results. The fresh synthetic draw follows the same engineered generator used in earlier examples, so it does not provide independent evidence of clinical transportability.

No minimum performance, preferred direction of difference, confidence interval, significance test, calibrated-probability claim or clinical utility claim is required. Equal specimen counts make the specimen-weighted and person-weighted mean errors equal in this fixture; that equality need not hold with unequal numbers of specimens.

Any later parameter, endpoint, population or assessment change must be recorded as a new protocol version or an amendment. Existing results remain teaching outputs whose assessment has already been inspected.
