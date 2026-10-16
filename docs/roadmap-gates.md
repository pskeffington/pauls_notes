# Roadmap milestone gates and evidence

Authored by Paul Skeffington · Compiled with OpenAI

[Learning roadmap](learning-roadmap.md) · [Machine learning](../04_machine_learning/README.md) · [Breast cancer book](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md)

Work-order date: **2026-10-16**. This ledger separates repository delivery from scientific interpretation and learner mastery. Status values are **Planned / Implemented / Tested / Reviewed / Complete / Blocked**. A commit, passing script or favorable score alone cannot close a gate. All current experimental evidence is synthetic software evidence; CI does not assess a learner's understanding.

G0–G5 here identify **roadmap milestones**. They do not replace the separately scoped G0–G10 requirements in the [biomedical implementation gates](../02_biomedical_coding/IMPLEMENTATION_GATES.md).

The shared narrative is **people → specimens → measurements → data preparation → training → validation → prediction → biological interpretation**. Preserve the 12-chapter, 60-gene book and its source corpus. No restricted data or participant records are admitted by this work order.

| Gate | Milestone | Dependency | Repository status | Learner mastery |
| --- | --- | --- | --- | --- |
| G0 | Close current Phase 4 software baseline | Existing PR #1 | Complete within bounded synthetic software scope | Not assessed |
| G1 | Phase 4B repeated-cohort robustness | G0; protocol freeze before assessment | Complete within declared synthetic scope; full archived assessment and replay reviewed | Not assessed |
| G2 | Phase 4C uncertainty and reliability | G1 saved predictions; new estimand freeze | Complete within frozen-prediction conditional scope | Not assessed |
| G3 | Native Rust training and numerical validation | Own objective and numerical contract; independent of G1/G2 | Planned; frozen-model inference already exists separately | Not assessed |
| G4 | Phase 5 survival learning case | G1 and G2; separate endpoint protocol | Planned | Not assessed |
| G5 | Phase 6 published-result reproduction | Relevant validated method and reproduction contract | Planned | Not assessed |

**Phase 4's defined synthetic scientific-software milestone is complete through G1/G2.** Its uncertainty assessment holds predictions fixed; a full-procedure refitting experiment, external clinical validation and learner mastery are not established. G3 remains an engineering extension. G4's G1/G2 dependency is now satisfied, but its own endpoint/protocol gates remain open.

## G0: Phase 4 software baseline

| Field | Record |
| --- | --- |
| Milestone | G0, close current Phase 4 delivery; no new scientific endpoint |
| Objective | Verify that the four-scenario paired-assay experiment respects split, tuning, fit-budget and artifact contracts |
| Status | Complete within bounded synthetic software scope: reviewed, merged, locally replayed and all four triggered merge-commit workflows passed |
| Source | [PR #1](https://github.com/pskeffington/pauls_notes/pull/1), reviewed head `51a10cb49a3f85bb79230a791028d0fc046d1273`; merged to `main` as `06cdc2c9de2e42de4852ce07dd8d4d52ae26216c` |
| Execution | Commands and exact local environment below; GitHub executes the workflow's own environment at the merge SHA |
| Evidence | [Compact verification record](../04_machine_learning/evidence/phase4-baseline-validation-2026-10-16.json), seven robustness tests, complete 624-fit replay, 360 development prediction rows, full membership/history/hash audit; navigation and corpus checks pass |
| Scientific review | Original protocol discloses inspected development runs; paired specimen category only; 15 reserved people per scenario remain unscored; overlapping scenarios are not independent studies |
| Remaining risks | The original baseline discards staged artifacts on failure; G1's separate runner now preserves them. G1/G2 provide broader synthetic replication and conditional uncertainty, without full-procedure or clinical coverage. CI archives expire; identities/digests do not guarantee permanent availability |
| Next dependency | Preserve this baseline while proceeding through G3's objective contract and G4's separate endpoint design |

The PR changed only eight intended files: the robustness workflow, runner, tests, protocol and guide, the root/ML indexes and learning roadmap. No book or source-corpus file changed. Merge and reviewed-head trees both equal `7cfe06bee50cc19c9b1e82a69b81511cb276645d`; local code replay therefore applies to the identical merged source tree. Review included split exclusion, training-only transformations, six-candidate histories and the chosen-setting rule, comparator accounting, recorded inner failure tests, output protection and source/output digests. Review here is a recorded code/evidence review, not a claim of an independent clinical or human PR approval.

### Execution and checks

From the repository root, with Python **3.12.14**, numpy **2.3.5**, scipy **1.17.0**, scikit-learn **1.8.0**, joblib **1.5.3** and matplotlib **3.10.8**:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/tests/test_breast_cancer_robustness.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/examples/breast_cancer_robustness.py /workspace/scratch/2f9cb88229e2/g0-robustness-replay
python3 scripts/check_documentation.py
python3 scripts/check_repository.py
python3 scripts/tests/test_documentation.py
python3 scripts/check_ml_evidence.py
python3 scripts/tests/test_ml_evidence.py
python3 scripts/tests/test_rust_ml_evidence.py
```

All commands exited 0. The local replay path records this execution only; replay elsewhere requires a new, unused directory outside the repository. Local automated tests: **7 robustness + 2 documentation + 9 ML evidence + 6 Rust evidence = 24 tests**. Navigation also verified 80 Markdown pages, local anchors, 12 chapters and 60 gene profiles; syntax checking parsed 35 Python/Bash sources. The independent post-run audit recalculated partitions and eligible rows for all four scenarios, checked six complete candidate histories in each of eight searches per scenario, checked per-search 19-fit counts and zero failed fits, and verified source/output hashes. R and Rust executable checks are evidenced by GitHub CI, not claimed as locally rerun.

### Observed software findings

| Scenario | Grid Brier | Random Brier | All-feature Brier | Prevalence Brier | Random minus grid |
| --- | --- | --- | --- | --- | --- |
| Reference | 0.110535 | 0.124426 | 0.119549 | 0.250000 | +0.013892 |
| Extra missingness | 0.128732 | 0.156721 | 0.170740 | 0.250000 | +0.027989 |
| Correlated measurement | 0.112495 | 0.116706 | 0.126423 | 0.250000 | +0.004211 |
| Reallocated people | 0.151007 | 0.156206 | 0.174699 | 0.250000 | +0.005199 |

Each row has **45 development people, 90 specimens, 45 positive and 45 negative specimen labels, 156 fits and zero failed trials**. The 360 prediction records contain four probabilities each. Lower Brier is better. Random search was worse than the original grid in all four inspected cells, a retained unfavorable result. The missingness probe worsened all fitted procedures' Brier error in this draw. These are descriptive outcomes from one engineered cohort; reallocation changes assessed people, and no inference about clinical performance or universal search superiority follows.

### CI and archive record

All four PR workflows passed at the reviewed head: [documentation](https://github.com/pskeffington/pauls_notes/actions/runs/38920448744), [robustness](https://github.com/pskeffington/pauls_notes/actions/runs/38920448763), [Unix/Bash](https://github.com/pskeffington/pauls_notes/actions/runs/38920448656), and [ML deployment](https://github.com/pskeffington/pauls_notes/actions/runs/38920448592). The last workflow includes R methods, Python replay/gallery validation and frozen-model Rust compilation/parity.

All four merge-commit runs passed: [documentation](https://github.com/pskeffington/pauls_notes/actions/runs/38922611741), [robustness](https://github.com/pskeffington/pauls_notes/actions/runs/38922611591), [Unix/Bash](https://github.com/pskeffington/pauls_notes/actions/runs/38922611708), and [ML deployment](https://github.com/pskeffington/pauls_notes/actions/runs/38922612242). Their observed conclusions are recorded in the compact verification JSON. The corpus-specific and learning-case workflows have path filters and were not triggered by PR #1; local corpus checks still ran. No branch-protection setting was changed or bypassed; only triggered workflow results are asserted here.

The merge robustness run preserved artifact **12054712479**, `phase4-robustness`, SHA-256 archive digest `f4fe45f31cc32e6830b3f1aee55706c41de87f2755ffe4bc7c0446278262ae46`, expiring **2026-10-30T15:17:08Z**. The local replay's separate manifest digest is `50cb73eb4cdf1220981501ea24ef9cd187ef5454908d43d2a149d0406ac72574`. Timing/version fields can change artifact bytes between otherwise equivalent runs. Local output digests are retained in the verification JSON; do not expect the CI ZIP digest to equal a local manifest digest.

## G1: Phase 4B repeated-cohort robustness

| Field | Record |
| --- | --- |
| Milestone | G1, independent synthetic draws and stability; depends on G0 |
| Objective | Measure robustness of the four fixed procedures across three declared new generator draws and four scenarios each |
| Status | Complete within the declared internal synthetic scope: implementation, tests, full assessment, archived replay and scientific-scope review; delivery in [PR #3](https://github.com/pskeffington/pauls_notes/pull/3) |
| Source | [PR #2](https://github.com/pskeffington/pauls_notes/pull/2) froze the unchanged protocol/config at `65a0b8776a876c0a845e6f9f57c067adb30f713e`; implementation/recorded execution at `3cef4b52b1124e988eedd0c7811cc7fa9de4d3dd` in PR #3 |
| Execution | [Exact commands and environment](../04_machine_learning/evidence/replication-validation-2026-10-16.json): one worker, 12 cells, 1,872 fits, 1,080 development prediction rows, zero failed fits; 12.004 seconds locally against a 2,700-second ceiling |
| Evidence | [Full report and interpretation](../04_machine_learning/replication-experiment.md); 10 new + 7 baseline + 17 documentation/evidence tests pass; legacy parity/invariance; complete partitions, candidate/fitting histories, ranks/signs/frequencies, retained failures, output/input hashes and downloaded CI replay |
| Scientific review | Random search improves Brier in 4 cells and worsens it in 8. New seeded draws from the same generator are internal synthetic replication. Scenarios overlap; ranking scores retain within-person dependence. No performance threshold, biological discovery or interval claim was used |
| Remaining risks | An initial local report/manifest discrepancy remains unexplained; that bundle was rejected and preserved, then unchanged-source local and CI replays passed. All three executions and their 5,616 attempts are disclosed. CI archives expire; complete downloadable evidence is also preserved. G2 now supplies conditional ranges; full-procedure uncertainty is still unestimated |
| Next dependency | G2 is complete within its declared conditional scope; proceed to G3/G4 with their own frozen protocols |

The [accepted full CI run](https://github.com/pskeffington/pauls_notes/actions/runs/38936820625) archived `phase4b-full`, artifact **12062065184**, with verified SHA-256 `e13edef4d52ea60439f0e5704b7add03f843050645a90777c7e47a88875c766a`, expiring **2027-01-14T17:04:09Z**. The downloaded bundle passed a separate local audit and differed from the accepted local probabilities by at most `8.731904088676856e-14`. The report preserves all 12 results and separates outer/all-fit/final-panel denominators; source protocol bytes were not amended after outcomes.

## G2: Phase 4C uncertainty and reliability

| Field | Record |
| --- | --- |
| Milestone | G2, person-aware uncertainty; depends on G1 |
| Objective | Quantify paired error-contrast uncertainty without treating a person's specimens as independent observations |
| Status | Complete within prespecified fixed-prediction conditional scope; [assessment and interpretation](../04_machine_learning/uncertainty-assessment.md) |
| Source | [PR #4](https://github.com/pskeffington/pauls_notes/pull/4); unchanged [protocol](../04_machine_learning/uncertainty-protocol.md), [contract](../04_machine_learning/evidence/uncertainty-contract-v1.json) and compact G1 input frozen at `d440b82b9af696f3717e302b6e276cb10ad39255`; implementation/assessment at `da9ecc5d8263466a3c803e31275b516899fa58b3` |
| Execution | [Exact commands/environment](../04_machine_learning/evidence/uncertainty-validation-2026-10-16.json); 45 people/90 specimens per cell, 10,000 draws per cell, root seed 26102101 with cohort/scenario streams, linear 0.025/0.975 endpoints; 12 cells, 36 ranges, 120,000 person-index resamples, 360,000 means and zero new model fits |
| Evidence | 13 uncertainty + 17 documentation/evidence tests pass; exact numeric enumeration and SciPy paired reference; malformed cluster/value/identity rejection; complete saved arrays and hashes; local/CI second-process audits and exact cross-environment array/endpoint agreement |
| Scientific review | Eight of twelve random-versus-grid ranges include zero, without equivalence/winner claims. Resampling is paired at person level and conditional on frozen predictions. Shared-training dependence, complete-procedure uncertainty and independent variance components are not estimated; no assessment-based redesign occurs |
| Remaining risks | Nominal pointwise ranges have no demonstrated clinical/population or simultaneous coverage. G1 outcomes were known before this descriptive follow-up. Full-procedure uncertainty needs a separate refitting/resampling experiment. CI archive expiry is explicit; complete downloadable evidence and a compact offline input snapshot are preserved |
| Next dependency | G1/G2 close defined synthetic Phase 4. Next engineering milestone: G3 objective/numerical contract. G4 may proceed with its own survival endpoint protocol; G3 does not block it |

The [G2 CI replay](https://github.com/pskeffington/pauls_notes/actions/runs/38939809441) archived artifact **12062851000**, SHA-256 `d89db0fe2cdd282dd56dee11273785febf5b00480461452da13e54517a40d1a5`, expiring **2027-01-14T17:27:21Z**. Downloaded bytes and all internal outputs were verified; local and CI person/loss/draw/replicate arrays, endpoints and reliability descriptions agree exactly. The report includes common-person reallocation counts of **32, 34 and 34** and preserves candidate/stability evidence without an unsupported variance decomposition.

## G3: native Rust training

| Field | Record |
| --- | --- |
| Milestone | G3, native logistic fitting; engineering extension independent of Phase 5 progression |
| Objective | Verify a native Rust training procedure's objective, preprocessing, probability convention and numerical behavior |
| Status | Planned; existing Rust inference remains a separate tested capability |
| Source | Existing [Rust review](../04_machine_learning/rust-ml-literature.md) and [inference baseline](../04_machine_learning/rust-deployment.md); no native-training implementation PR yet |
| Execution | Not executed; first freeze loss normalization, penalty, intercept treatment, class direction, stopping criteria and matched Python calculation; investigate pinned Linfa |
| Evidence | Required: person-disjoint partitions, training-only preprocessing, convergence/numerical failure fixtures, justified probability tolerances and preserved inference CI |
| Scientific review | Similar library names or regularization parameters do not establish equivalent objectives; coefficients are comparable only after conventions match |
| Remaining risks | Library/version compatibility, optimization failure, objective scaling, hardware/precision/compilation effects; no measured Rust speed advantage exists |
| Next dependency | Own reviewed objective and numerical contract; does not block G4 once G1/G2 pass |

## G4: Phase 5 survival learning case

| Field | Record |
| --- | --- |
| Milestone | G4, separate breast cancer time-to-event case; depends on G1/G2 |
| Objective | Teach prognosis with a declared event, time origin, follow-up, prediction horizon and censoring mechanism |
| Status | Planned |
| Source | Existing direct-R survival mechanism in [methods](../04_machine_learning/methods-and-deployments.md); no endpoint-specific learning-case implementation PR yet |
| Execution | Not executed; new synthetic person-level data dictionary/protocol, then R survival Cox baseline; Python follows compatible quantities and assumptions |
| Evidence | Required: invalid/contradictory outcome tests, person-separated partitions, saved predictions/environment, censoring-aware discrimination and time-dependent calibration assessment |
| Scientific review | Specimen category is not recurrence. Hazard ratios, survival probabilities and treatment response have different meanings; censoring assumptions and proportional hazards need assessment |
| Remaining risks | Invalid outcome coding, unsupported censoring models, horizon support and misaligned cross-language estimands |
| Next dependency | G1/G2 complete; new endpoint protocol frozen before fitting; G3 not required |

## G5: Phase 6 published-result reproduction

| Field | Record |
| --- | --- |
| Milestone | G5, bounded research capstone; depends on the relevant validated method |
| Objective | Reproduce one precisely declared published result or component and connect it to the book's learning narrative |
| Status | Planned |
| Source | [Corpus review](../04_machine_learning/corpus-review.md) and pinned survival-benchmark processed-output audit; no refitting reproduction PR yet |
| Execution | Not executed; freeze publication/version, source SHA, target/table, permitted dataset, environment lock, expected output/tolerance, budget and failure policy |
| Evidence | Required: source/input provenance, use rights, clean-environment execution, numeric target comparison, deviations, figures, complete artifact manifest and independent replay |
| Scientific review | Published-count arithmetic and processed-output integrity audits already exist; they do not constitute model refitting or complete paper reproduction |
| Remaining risks | Data access/licensing, original environment restoration, resource costs and target comparability; an accessible processed table does not grant rights to its underlying study data |
| Next dependency | Verify the selected component's methodological prerequisites and artifact permissions before execution; state partial/full reproduction scope accurately |

## Completion discipline

Use focused branches and reviewable PRs; preserve concurrent work and history. For every subsequent pass, update the relevant row with actual PR/source commits, exact commands/environment, test and artifact evidence, numerical findings, scientific review, remaining risks and the next executable dependency. Preserve failures and avoid claiming improvement as an acceptance criterion. A learner can demonstrate mastery using the [analysis record](../templates/analysis-record.md); software evidence alone cannot set that status.
