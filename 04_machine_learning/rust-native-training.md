# Rust Native Training Baseline and Numerical Validation

Authored by Paul Skeffington · Compiled with OpenAI

[ML subjects](README.md) · [Frozen protocol](rust-training-protocol.md) · [Release-source addendum](rust-training-source-addendum.md) · [Contract](evidence/rust-training-contract-v1.json) · [Compact verification record](evidence/rust-training-validation-2026-10-16.json) · [G3 ledger](../docs/roadmap-gates.md#g3-native-rust-training) · [Preserved inference](rust-deployment.md)

**G3 adds a working native Linfa logistic fit and numerical comparison on synthetic data.** It follows people → specimens → measurements → preparation → training → validation → prediction → interpretation. The task remains recorded specimen category, not recurrence, future diagnosis or treatment benefit. The 48 anonymous features are not the book's 60 named genes.

## What was frozen and fitted

[PR #5](https://github.com/pskeffington/pauls_notes/pull/5) preserves the protocol/config freeze at **`1b0d8eda2498136d495ad2a97cf24015d6d34fb1`** and pre-assessment source addendum at **`7b512c0fbccae3a54c5d0089527032c5f0358e78`**. The published crate differs from the newer source inspected during the literature review. The addendum identifies the actual 0.8.1 release and its exact installed-source hash; no seeds, thresholds, objective or fitting budget changed. The experiment used execution commit **`aeb0e5271534c224114beb39607eac3eb7375600`**.

One fresh synthetic draw uses cohort seed **26102201** and split seed **26102202**. All **60 people / 120 specimens** have complete paired category identities. Only **45 people / 90 specimens** enter the compact development input. The **15 reserved people / 30 specimens** are listed in membership records but never supplied to a training or prediction engine.

Three GroupKFold splits each train on **30 people / 60 specimens** and assess **15 people / 30 specimens**. Each engine produces all **90 held-out development probabilities**, once per specimen. A fourth model uses all 45 development people; its 90 development predictions are labeled **training-set numerical probes**, excluded from reported held-out metrics. Linfa, SciPy trust-exact and sklearn lbfgs each perform four fits: **12 optimization attempts**, plus a training-prevalence comparator without an optimizer. No feature selection, hyperparameter search or inner tuning occurs. The earlier grid/random/selected procedures remain separately available.

Rust learns median imputation, imputed means and population scales within each training slice. Python learns them separately with SimpleImputer/StandardScaler, assigning scale 1 only to exactly constant columns. All fitted preprocessing quantities agree exactly in the recorded local assessment. The CLI validates aligned identities, complete pairs, exhaustive indices and person exclusion before fitting; numerical failures retain attempt evidence.

## The matched objective

For standardized X, category y∈{0,1}, z=Xw+b, all three engines minimize the same **sum** logistic loss plus **½‖w‖²**, with an **unpenalized intercept**, no weights, f64 and zero initialization. Linfa alpha=1 corresponds to sklearn **C=1**, not C=n or C=1/n. The direct Python oracle implements stable loss, analytical gradient and full Hessian, checked against known values and finite differences.

The published Linfa release determines its positive class using counts and encounter order. The wrapper reads the fitted label mapping and saves parameters/probabilities in category-1 coordinates; all four recorded fits originally map positive to category 0 and are canonicalized. Small fixtures also test reversed encounter order and unequal class counts. This prevents a plausible-looking probability complement from silently reversing the biological label.

Linfa's public fitted API exposes neither iteration count nor termination reason. The record keeps both unavailable and recalculates objective/gradient. **Returning a model is insufficient**: all engines must pass the frozen **gradient infinity norm ≤1e-6**, probability error ≤1e-5 and objective error ≤1e-8. Native L-BFGS has max_iterations=5,000 and gradient_tolerance=1e-8; the direct oracle uses gtol=1e-10/maxiter=1,000, sklearn tol=1e-10/max_iter=5,000. The probability tolerance is an engineering allowance for different iterative optimizers; frozen-model inference retains its stricter 1e-12 contract.

## Observed numerical findings

The following table preserves every native fit. Differences are absolute against the direct Python oracle on that model's declared prediction rows.

| Fit | Training people | Assessed people | Max Rust probability difference | Objective difference | Rust gradient infinity norm |
| --- | --- | --- | --- | --- | --- |
| outer_0 | 30 | 15 | 7.53088e-9 | 2.66454e-15 | 3.42059e-8 |
| outer_1 | 30 | 15 | 2.32782e-9 | 1.77636e-15 | 7.25787e-9 |
| outer_2 | 30 | 15 | 2.76226e-9 | 1.77636e-15 | 5.12388e-9 |
| final_development, training probes | 45 | 0 | 1.12398e-8 | 0 | 8.85228e-8 |

Across the four fits, sklearn's maximum probability difference is **3.49366e-7**, objective difference **1.12088e-12** and gradient infinity norm **8.11193e-7**. All acceptance checks pass. Native canonical coefficients differ from the oracle by at most **1.98421e-8**, after matching preparation, loss, intercept and class direction; the full vectors are preserved outside Git.

**One oracle solver status is non-success.** SciPy's final-development fit reports “A bad approximation caused failure to predict improvement.” after seven iterations, with gradient infinity norm **3.94281e-10**. The three outer oracle fits report success after seven iterations each. The final fit passes the explicitly frozen residual criterion despite missing its stricter requested gtol, and its message is retained. Thus **zero acceptance-gate failures** is not a claim that every optimizer returned a success flag. Sklearn takes 27, 28, 29 and 29 iterations, without ConvergenceWarning. Linfa iterations/termination remain unobserved.

The following metrics use only the 90 outer-held-out specimens from 45 people. Equal paired specimen counts make pooled Brier and equal-person mean Brier coincide, apart from floating-point summation. These descriptive scores are not acceptance thresholds.

| Procedure | Person-mean Brier | ROC-AUC | Average precision |
| --- | --- | --- | --- |
| Native Linfa | 0.101648369895 | 0.931851851852 | 0.925106670008 |
| Direct Python objective | 0.101648370002 | 0.931851851852 | 0.925106670008 |
| Matched sklearn | 0.101648374202 | 0.931851851852 | 0.925106670008 |
| Training prevalence | 0.250000000000 | 0.500000000000 | 0.500000000000 |

Near-identical scores are expected when fitting the same objective. This is no new model-selection result, clinical validation, calibration study, uncertainty interval or evidence of a superior language. The final-development probes supply no additional assessment people.

## Run and audit it

Use the repository's pinned Python requirements and Rust 1.90.0. Run from a clean committed checkout, outside source output directories, with an existing parent:

```bash
CARGO_TARGET_DIR=/tmp/assay-native-build cargo +1.90.0 fmt --manifest-path 04_machine_learning/rust/Cargo.toml -- --check
CARGO_TARGET_DIR=/tmp/assay-native-build cargo +1.90.0 clippy --locked --manifest-path 04_machine_learning/rust/Cargo.toml --all-features --all-targets -- -D warnings
CARGO_TARGET_DIR=/tmp/assay-native-build cargo +1.90.0 test --locked --manifest-path 04_machine_learning/rust/Cargo.toml --all-features
CARGO_TARGET_DIR=/tmp/assay-native-build cargo +1.90.0 build --release --locked --manifest-path 04_machine_learning/rust/Cargo.toml --all-features
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 ASSAY_TRAIN_BINARY=/tmp/assay-native-build/release/assay-train python3 04_machine_learning/tests/test_breast_cancer_rust_training.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/examples/breast_cancer_rust_training.py /tmp/assay-native-comparison --binary /tmp/assay-native-build/release/assay-train
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/examples/breast_cancer_rust_training.py /tmp/assay-native-comparison --audit-only
```

The feature is opt-in: ordinary Cargo builds/tests still provide the existing inference path. The native CLI consumes `development.json` and a new output-directory path. The Python runner creates its declared input, invokes Rust, fits both Python witnesses, audits the payload and records predictions. It requires unchanged freeze/addendum bytes, committed computational sources, reviewed published-crate bytes and pinned dependencies. It saves models, mapping, fitted preparation, objective/gradient, diagnostics, membership, attempts, source/binary/input hashes, subprocess output, resource fields and SHA-256 inventory. Failures preserve partial output; existing output is protected.

The separate audit process verifies membership against regenerated synthetic input, all training-only quantities, every saved probability and identity, recomputed objectives/gradients, fit-budget reconciliation, source commit/bytes and artifact hashes, without refitting optimizers. Four explicit corruption probes rejected altered bytes, an altered objective even with a regenerated inventory, altered prediction identity and altered source provenance. Small test suites contain **9 new Rust training tests + 6 preserved inference tests**, **12 Python numerical/CLI tests**, and **17 documentation/evidence tests**. Tests cover analytical/finite-difference derivatives, stable extreme logits, constant/missing columns, class direction, regularized separation/collinearity, held-out-value invariance, exhausted budgets, malformed inputs and overwrite protection.

The first local run at `df8e625…` passed and is preserved. GitHub rejected the initial workflow before executing jobs because `runner.temp` is invalid in a job-level environment expression. A workflow-only correction at `aeb0e52…` used a valid fixed Cargo output path. The recorded second local run has **exactly identical numerical results**; numerical code, protocol and criteria were unchanged. These are two executions of one synthetic draw, not additional cohorts. CI executions likewise replay that same draw.

The recorded local runtime is **0.219341 seconds** (300-second ceiling), Rust subprocess wall time **0.016301 seconds**, on Linux x86_64 / **Intel Xeon Platinum 8573C**, Rust **1.90.0**, release opt-level 3, default CPU flags, f64, linfa/linfa-logistic **0.8.1**, ndarray **0.16.1**, argmin **0.11.0**, one worker, OMP/OPENBLAS=1. Python **3.12.14**, numpy **2.3.5**, scipy **1.17.0**, scikit-learn **1.8.0**, joblib **1.5.3**, matplotlib **3.10.8** are pinned. Full OS/compiler/target/lock/source/binary identities and process CPU/high-water RSS are in the evidence. CPU fields include orchestration; child RSS may include inherited process memory. These are not isolated memory or controlled speed benchmarks. No speed or memory advantage is claimed.

## CI replay and artifact review

The [push replay](https://github.com/pskeffington/pauls_notes/actions/runs/38943944644) and [PR replay](https://github.com/pskeffington/pauls_notes/actions/runs/38943952801) both compiled, linted, tested, executed and audited the comparison. Their downloaded ZIP digests and internal inventories were verified locally. **All three engines' saved probabilities agree exactly** with the accepted local run across all four fits, within the frozen cross-environment tolerance of 1e-10. The local and two CI comparisons reuse one synthetic draw; they are software replays, not three independent cohorts. Two local and two recorded CI executions account for 48 optimization attempts, with later CI refreshes likewise replaying the same contract.

| Replay | Artifact ID | ZIP SHA-256 | Expiry |
| --- | --- | --- | --- |
| Push at `aeb0e52…` | 12065045242 | `2472d89f0fb817b520d9fe8086440449e5320672276efcd6db672cf14c779aef` | 2027-01-14T17:59:58Z |
| PR test merge `23a517f…` | 12064600949 | `be5091212bcf0a13c34051133acbc3acce7c5879d5a5675ca769d1262f494ccd` | 2027-01-14T18:00:02Z |

The PR test-merge tree equals the reviewed execution-head tree `b57eea40fd04d3af30aa3ee4de43ee951d1e4862`. To audit that downloaded PR artifact elsewhere, fetch its recorded test-merge commit while available; the push artifact uses the durable branch commit. Both saved computational source maps also match the accepted local source. CI runtimes were 0.074520 and 0.078458 seconds on AMD EPYC 9V45; these observations are not language-speed estimates. The full downloaded evidence preserves the exact compiler, CPU, build, diagnostics and resource fields. Archive expiry remains a limitation of the GitHub copy.

All six execution-head PR workflows passed: native training, preserved ML deployment (including fresh inference export/replay), documentation, robustness, repeated-cohort replication and conditional uncertainty. The final evidence/navigation revision is checked again before merge. The [compact record](evidence/rust-training-validation-2026-10-16.json) identifies commands, source hashes, complete per-fit numerical findings, corruption probes, resource observations and artifact digests. The existing frozen inference also passed locally with maximum probability differences 2.77556e-16 for the selected model and 3.33067e-16 for all features, and its four Python exporter tests passed.

## Review limits and next step

This validates one fixed regularized objective on a small synthetic paired-specimen contract. It does not port feature selection, grouped tuning, arbitrary preprocessing, multinomial models, weights, GPU computation or neural training. The exact installed crate is identified separately from a newer development revision. The comparison's explicit residual gate substitutes for unavailable native termination diagnostics; it does not recover those diagnostics.

The book, 12 chapters, 60-gene catalog and source corpus are preserved. G3 is an engineering extension to the completed scoped G1/G2 milestone. **Next executable method: G4's separate synthetic survival endpoint/data dictionary and frozen Cox assessment protocol**, followed by the R baseline and censoring-aware validation. Full-procedure uncertainty, clinical validity and learner mastery remain unestablished.
