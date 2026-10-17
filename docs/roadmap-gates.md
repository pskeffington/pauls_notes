# Roadmap milestone gates and evidence

Authored by Paul Skeffington · Compiled with OpenAI

[Learning roadmap](learning-roadmap.md) · [Machine learning](../04_machine_learning/README.md) · [Breast cancer book](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md)

Original work-order date: **2026-10-16**. Status reconciliation: **2026-10-17**. The [machine-readable evidence ledger](milestone-evidence.toml) records scope, PRs, reviewed heads, merge commits, CI run IDs, sources, prerequisites and limitations for every milestone. Its validator is [check_milestone_evidence.py](../scripts/check_milestone_evidence.py). The ledger is a dated snapshot, **not** a substitute for live GitHub checks or human study approval. This ledger separates repository delivery from scientific interpretation and learner mastery. Status values are **Planned / Implemented / Tested / Reviewed / Complete / Blocked**. A commit, passing script or favorable score alone cannot close a gate. All current experimental evidence is synthetic software evidence; CI does not assess a learner's understanding.

G0–G5 here identify **milestones for the currently documented breast-cancer synthetic research sequence**, not the scope of Paul's Notes as a whole. The repository supports [any cancer research area](cancer-research-scope.md), with separate protocols and milestones for new studies. These milestones do not replace the separately scoped G0–G10 requirements in the [biomedical implementation gates](../02_biomedical_coding/IMPLEMENTATION_GATES.md).

The shared narrative is **people → specimens → measurements → data preparation → training → validation → prediction → biological interpretation**. Preserve the 12-chapter, 60-gene book and its source corpus. No restricted data or participant records are admitted by this work order.

| Gate | Milestone | Dependency | Repository status | Learner mastery |
| --- | --- | --- | --- | --- |
| G0 | Close current Phase 4 software baseline | Existing PR #1 | Complete within bounded synthetic software scope | Not assessed |
| G1 | Phase 4B repeated-cohort robustness | G0; protocol freeze before assessment | Complete within declared synthetic scope; full archived assessment and replay reviewed | Not assessed |
| G2 | Phase 4C uncertainty and reliability | G1 saved predictions; new estimand freeze | Complete within frozen-prediction conditional scope | Not assessed |
| G3 | Native Rust training and numerical validation | Own objective and numerical contract; independent of G1/G2 | Complete within fixed-objective synthetic numerical scope; frozen inference remains separately tested | Not assessed |
| G4 | Phase 5 survival learning case | G1 and G2; separate endpoint protocol | Planned | Not assessed |
| G5 | Phase 6 published-result reproduction | Relevant validated method and reproduction contract | Planned | Not assessed |

**Phase 4's defined synthetic scientific-software milestone is complete through G1/G2.** Its uncertainty assessment holds predictions fixed; a full-procedure refitting experiment, external clinical validation and learner mastery are not established. G3 now completes its fixed-objective engineering extension. G4's G1/G2 dependency is now satisfied, but its own endpoint/protocol gates remain open.

## Delivery and admission snapshot (2026-10-17)

These recorded tracks distinguish **current-case scientific experiment milestones (G0–G5)**, **Rust learning/inference delivery (R0–R3), configurable synthetic Python ML (R4)** and **public repository controls plus the proposed TCGA-BRCA data-admission case (D0–D1)**. A new cancer study will need its **own** admission and endpoint contract. A passing branch workflow is not a merged feature; a merged synthetic training tool is not authorization to train on real TCGA patients. *All learner-mastery states remain unassessed.*

| ID | Gate and exit requirement | Delivery status | Evidence / next dependency |
| --- | --- | --- | --- |
| G0 | Four-scenario synthetic model baseline, fixed assessment and replay | **Complete (bounded)** | [G0 evidence](#g0-phase-4-software-baseline) |
| G1 | Prespecified repeated-cohort synthetic robustness and full replay | **Complete (bounded)** | [G1 evidence](#g1-phase-4b-repeated-cohort-robustness) |
| G2 | Person-resampled conditional uncertainty on frozen predictions | **Complete (bounded)** | [G2 evidence](#g2-phase-4c-uncertainty-and-reliability) |
| G3 | Frozen native Rust logistic objective, class mapping and independent numerical checks | **Complete (bounded)** | [G3 evidence](#g3-native-rust-training) |
| G4 | Frozen synthetic event/time/censoring protocol; separate Cox/KM execution and IPCW replay outstanding | **Planned** | [G4 frozen protocol](../04_machine_learning/survival-protocol.md); no endpoint-specific fit |
| G5 | Predeclared target and permitted source, then independent reproducible refitting | **Planned** | [G5 gate](#g5-phase-6-published-result-reproduction) |
| R0 | Rust syntax→ownership→structs/traits→research engineering, locked Cargo lab/tests | **Complete (bounded)** | [R0 evidence](#r0-rust-foundations-and-object-oriented-learning) |
| R1 | Source-graded Rust coding corpus, exact references and offline integrity checks | **Complete (bounded)** | [R1 evidence](#r1-rust-literature-and-coding-quality-corpus) |
| R2 | Twelve-chapter book-aligned Rust handbook and standalone six-pair arithmetic example | **Complete (bounded)** | [R2 evidence](#r2-breast-cancer-book-aligned-rust-engineering) |
| R3 | Audited final-development native-fit frozen Rust inference; independent probability and identity parity | **Complete (bounded)** | [R3 evidence](#r3-audited-native-fit-frozen-rust-inference) |
| R4 | Configurable synthetic oncology ML (Python), person-grouped tuning and full candidate/feature audit | **Complete (bounded)** | [R4 evidence](#r4-configuration-driven-synthetic-oncology-ml) |
| D0 | Public Git safety across cancer providers and TCGA-BRCA-only GDC preflight | **In review — draft PR** | [PR #7](https://github.com/pskeffington/pauls_notes/pull/7); not enforced on `main` yet |
| D1 | Independent approval of the **current real TCGA-BRCA proposal** (not a block on every cancer topic) | **Blocked** | [Data access and methods contract](research-workflow.md#2-specify-input-and-access-contracts) |

**Gate vocabulary.** `Complete (bounded)` means a merged, specific software or documentation result supported by recorded acceptance checks, **not** an unrestricted scientific conclusion. `In review` means working code on a draft PR with branch-specific checks only; a green CI workflow never changes this status by itself. `Planned` requires a new frozen implementation protocol. `Blocked` forbids the data operation until independent access, privacy, study and scientific acceptance. The separate [biomedical implementation requirements](../02_biomedical_coding/IMPLEMENTATION_GATES.md) retain their own G0–G10 names.

### Evidence precedence and what a gate requires

1. **Source identity:** link the exact reviewed PR, head, merged commit (if merged), versioned protocol, and relevant file. A README claim without code/protocol is not an executed result.
2. **Executable verification:** capture exact command/toolchain, named test, CI run on the correct revision, negative controls, outputs and failed attempts. A link to a current green badge is not enough to reproduce old code.
3. **Data provenance and access:** record whether observations are invented, provider-verified and separately approved open-access cancer research inputs, or access-restricted/unclear. Group by the correct person/sample unit and keep raw people/identifiers out of public Git.
4. **Scientific inference:** state the target, cohort, denominator, selection boundary, uncertainty and effect of prior inspections. Synthetic arithmetic or software parity cannot justify a biological, prognostic or clinical assertion.
5. **Independent review and release:** document limitations, approved use, and human signoff where required. **CI does not certify learner mastery, privacy compliance, or clinical deployment.**

The [TOML registry](milestone-evidence.toml) makes those labels testable; it is intentionally not a live status poll. Review exact PR status and required protections again before changing a pending gate to complete.

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
| Status | Complete within the declared fixed-objective synthetic numerical/software scope; [baseline and interpretation](../04_machine_learning/rust-native-training.md) |
| Source | [PR #5](https://github.com/pskeffington/pauls_notes/pull/5); protocol/config frozen at `1b0d8eda2498136d495ad2a97cf24015d6d34fb1`, published-release addendum at `7b512c0fbccae3a54c5d0089527032c5f0358e78`, accepted execution at `aeb0e5271534c224114beb39607eac3eb7375600` |
| Execution | [Commands/environment/complete findings](../04_machine_learning/evidence/rust-training-validation-2026-10-16.json); three person-disjoint outer folds plus final development, four fits each for Linfa, direct Python objective and matched sklearn: 12 attempts, 90 held-out development prediction records, zero acceptance failures, zero reserved predictions |
| Evidence | 9 new Rust training + 6 inference tests, 12 Python native + 4 exporter + 17 documentation/evidence tests pass; analytical/finite-difference, class mapping, leakage, numerical edge and deliberate-failure fixtures; four payload-corruption rejections; complete artifact audit and exact local/CI probability replay; inference CI remains green |
| Scientific review | Sum logistic loss plus alpha/2 coefficient penalty, alpha=1/C=1, unpenalized intercept, category-1 mapping and f64 verified. Native/oracle max probability difference 1.12398e-8; all-engine residuals pass 1e-6. One SciPy non-success message is retained and accepted by the frozen residual rule; Linfa iterations/termination are unavailable |
| Remaining risks | One fixed all-feature objective and synthetic draw; selection/tuning not ported. Published release differs from newer literature-review source, resolved before assessment. Initial invalid CI environment expression was fixed without numerical changes; both local runs retained. A later truncated delivery ZIP was rebuilt from unchanged complete originals and verified after saving; its cause is unestablished. No language-speed/memory, clinical, full-procedure uncertainty or learner-mastery claim; CI archives expire |
| Next dependency | G4's separate survival endpoint, data dictionary and Cox assessment protocol before fitting; G3 adds no survival requirement |

The [native push CI run](https://github.com/pskeffington/pauls_notes/actions/runs/38943944644) archived artifact **12065045242**, SHA-256 `2472d89f0fb817b520d9fe8086440449e5320672276efcd6db672cf14c779aef`, expiring **2027-01-14T17:59:58Z**. The [PR replay](https://github.com/pskeffington/pauls_notes/actions/runs/38943952801) archived artifact **12064600949**, SHA-256 `be5091212bcf0a13c34051133acbc3acce7c5879d5a5675ca769d1262f494ccd`, expiring **2027-01-14T18:00:02Z**. Both downloaded payloads passed separate local audits; all three engines' four-fit probability arrays match the accepted local run exactly. Six execution-head PR workflows passed, including preserved frozen inference. The final PR revision is checked before merge. Full bundles and the initial passing local run are preserved outside Git; replays do not create additional independent synthetic cohorts.

## G4: Phase 5 survival learning case

| Field | Record |
| --- | --- |
| Milestone | G4, separate breast cancer time-to-event case; depends on G1/G2 |
| Objective | Teach prognosis with a declared event, time origin, follow-up, prediction horizon and censoring mechanism |
| Status | **Planned (G4 protocol declared and frozen; no model fitted)** |
| Source | [Frozen G4 protocol](../04_machine_learning/survival-protocol.md), [data dictionary](../04_machine_learning/survival-data-dictionary.md), [versioned contract](../04_machine_learning/evidence/survival-contract-v1.json), [offline guard](../scripts/check_survival_protocol.py). Separate generic R mechanism remains in [methods](../04_machine_learning/methods-and-deployments.md) and is not this experiment |
| Execution | **No G4 records generated or Cox/KM model fitted**; future implementation must replay 240 invented people, 180 development, 60 protected reserve and three person-disjoint outer folds on the frozen R seeds |
| Evidence | Required: negative censoring/event tests; training-only Cox, KM and reverse-KM censoring; held-out 24-month IPCW Brier on 180 development people, descriptive calibration with denominators, absolute probability and score-direction checks, exact source/protocol hashes and independent replay |
| Scientific review | Specimen category is not recurrence. Hazard ratios, survival probabilities and treatment response have different meanings; censoring assumptions and proportional hazards need assessment |
| Remaining risks | Invalid outcome coding, unsupported censoring models, horizon support and misaligned cross-language estimands |
| Next dependency | G1/G2 complete and G4 endpoint/censoring/metric specification **frozen before any fitting**; next reviewed PR must implement, run and audit it. G3 is not required |

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

## R0: Rust foundations and object-oriented learning

| Evidence field | Record |
| --- | --- |
| Status and scope | **Complete within synthetic educational software scope**; learner mastery **not assessed** |
| Delivered | [Seven-stage beginner course](../03_learning/rust/README.md), [pinned Cargo learning lab](../03_learning/rust/lab/Cargo.toml), [source/unit/integration tests](../03_learning/rust/lab/tests/research_workflow.rs) |
| Source | [Merged PR #12](https://github.com/pskeffington/pauls_notes/pull/12); accepted head `8bdd548f4588eda076acee41e22994b5fc6ae99a`, merged as `f02fe1e020e0f44c118b3c554724fe5101e643b9` |
| Execution evidence | [Merged-`main` Rust foundations CI](https://github.com/pskeffington/pauls_notes/actions/runs/39009076932); on PR acceptance: formatting, strict Clippy, 10 unit tests, 1 integration test, release build and known synthetic console output all passed |
| Contract | Starts from `fn main`/types and progresses through collections, ownership, borrowing, structs/methods/traits, Cargo and a person-exclusive training-only median fixture |
| Limit | Only invented sample measurements and documentation; green tests do not demonstrate clinical model validity or learner competency |
| Exit and next stage | Software delivery closed. Each learner must independently explain record/unit meaning and deliberate-failure behavior before advancing to the Rust handbook |

## R1: Rust literature and coding-quality corpus

| Evidence field | Record |
| --- | --- |
| Status and scope | **Complete within bibliographic and code-review guidance scope** |
| Delivered | [34-source coding register](../02_biomedical_coding/rust_coding_best_practices_sources.csv), [eight-publication bibliography](../02_biomedical_coding/rust_coding_references.bib) and [validator](../scripts/check_rust_coding_corpus.py) |
| Source | [Merged PR #10](https://github.com/pskeffington/pauls_notes/pull/10); accepted head `e0eaa27d8489e5a12e3d1cf5c9bc6b3b3a262632`, merged as `86e6d919f7a5c9f2b0b2b8382e1926ab5c0dcb7e` |
| Execution evidence | [Biomedical literature CI](https://github.com/pskeffington/pauls_notes/actions/runs/39006571252), [documentation CI](https://github.com/pskeffington/pauls_notes/actions/runs/39006571239): source classes, citation identities, reviews/limits, preprint versions, Cargo pin and deliberate-invalid tests passed |
| Scientific boundary | Six peer-reviewed papers, two preprints and 26 primary docs/tools are separately classified. **No full-text systematic review, third-party vulnerability proof or patient-outcome reproduction was performed** |
| Exit and next stage | Bibliographic organization closed; attach implementation-specific testing evidence to future Rust code, rather than upgrading the paper-review grade |

## R2: Breast-cancer book-aligned Rust engineering

| Evidence field | Record |
| --- | --- |
| Status and scope | **Complete within invented six-pair educational software scope** |
| Delivered | [Rust engineering handbook](../02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md), [six-pair source/test exercise](../02_biomedical_coding/examples/book_paired_specimens.rs) and links back to all twelve [breast-cancer book chapters](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) |
| Source | [Merged PR #11](https://github.com/pskeffington/pauls_notes/pull/11); accepted head `bfabde1fe22ac3e58aaf07fcf8a6a2c8e12acc1e`, merged as `e68ab849c6bf3ba7182acbdfebabcef88b196c66` |
| Execution evidence | [Merged-`main` Rust book exercise CI](https://github.com/pskeffington/pauls_notes/actions/runs/39007666795): pinned Rust 1.90.0, formatting, tests and known synthetic Chapter 11 ratios/mean/sensitivity output passed |
| Expected arithmetic | Six fictional tumor/comparator contrasts: `1, 2, 0, -1, 1, 0`; mean `0.5`; omit-one-person means `0.2–0.8`. The range is **not** a confidence interval |
| Scientific boundary | Six pairs are not the 60-person/48-anonymous-feature G3 training cohort; the book's 60 named genes were not used as fitted model features |
| Exit and next stage | Handbook/documentation reviewed and tested. Any actual model/backend extension requires its own source, numerical oracle, budget, privacy and PR gate |

## R3: audited native-fit frozen Rust inference

| Field | Verified record |
| --- | --- |
| Status and scope | **Complete within fixed-objective, synthetic numerical software scope**; no human clinical/learner-validation claim |
| Source | [Merged PR #6](https://github.com/pskeffington/pauls_notes/pull/6), accepted head `75409525de2119618b4dfecea7a9aa3e56af947c`, merged `214ee72743601da0f4b4da0add61cbaf04080e1d` |
| Code | [Read-only Rust frozen inference module](../04_machine_learning/rust/src/frozen.rs), [CLI](../04_machine_learning/rust/src/bin/assay-native-predict.rs), [independent verifier](../04_machine_learning/validation/validate_native_frozen_inference.py) and [failure-fixture tests](../04_machine_learning/tests/test_native_frozen_inference.py) |
| Executed acceptance | [Native numerical training CI](https://github.com/pskeffington/pauls_notes/actions/runs/39050714181) and [ML deployment CI](https://github.com/pskeffington/pauls_notes/actions/runs/39050714166) passed on the reviewed head, alongside documentation, robustness, replication and uncertainty |
| Independent numeric evidence | Audited prior G3 synthetic final-development model and complete source/fit provenance; rebuilt Rust CLI **without** training feature; compared **90 development-only probabilities**, observed max absolute Rust/Python difference `2.220e-16` against frozen tolerance `1e-12`; class-1 identity and ordered specimen IDs checked |
| Data and reporting | Fifteen reserved people unscored; no real TCGA records loaded; model, input and output SHA-256 checked; training=false and explicit **NOT FOR CLINICAL USE** warnings in Rust manifest and CLI. Temporary synthetic parity bundle not attached to the CI archive |
| Boundary | Final-development values are **in-sample numerical probes**, not new held-out accuracy, external validation, clinical utility, prevalence inference, subtype performance or survival predictions |
| Next action | Keep the frozen G3 objective/seed unchanged, retain negative tests and require a new study protocol for any model/data expansion |

## R4: configuration-driven synthetic oncology ML

| Evidence field | Reviewed record |
| --- | --- |
| Status | **Complete (bounded)** for a synthetic Python scientific-software experiment; not a real-data adapter, Rust training backend or clinical predictor |
| Merged source | [PR #16](https://github.com/pskeffington/pauls_notes/pull/16) reviewed head `232a2f5ab01dd070034786b18ffc803f8e52f160`, squash commit `714dbfa8d4d166b3df56451289411457afb92051` |
| Executable files | [Synthetic runner](../04_machine_learning/research_toolkit/research_runner.py), [bounded JSON configuration](../04_machine_learning/research_toolkit/synthetic_brca_config.json), [nine unit tests](../04_machine_learning/research_toolkit/test_research_runner.py), [complete guide](../04_machine_learning/research_toolkit/README.md) |
| Accepted CI | [Configurable synthetic ML workflow](https://github.com/pskeffington/pauls_notes/actions/runs/39053492819) passed **nine tests and a command-line smoke run**; seven other PR-head workflows passed, including Rust numerical training, model deployment, robustness, replication, uncertainty, manuscript and documentation |
| Audit records | Source/config SHA-256 and seed; exact person-exclusion split lists and separate nested inner candidates, balanced-accuracy mean/std/rank, selected settings, selected anonymous feature indices/standardized coefficients, outer metrics and five descriptive calibration bins with counts |
| Controls | Only internally generated measurements and labels; no external data path or real-data stage; fold-local imputation/scaling/selection, validated class-1 meaning, no out-of-repository overwrite; **NOT FOR CLINICAL USE** output |
| Evidence limit | Synthetic paired-specimen labels have no real biological or clinical meaning; descriptive bins lack warranted confidence intervals; no independent cancer cohort, patient-level TCGA training or generic Rust variable-only backend has been validated |
| Next work | Keep the synthetic program frozen for audit; propose a separate Rust/other cancer study interface only after source-specific input/target/validation and privacy review |

## D0 and D1: privacy and real-data admission remain open

| Gate | Source and executed branch check | Why it remains open |
| --- | --- | --- |
| D0 — provider-neutral public Git controls and source-specific GDC example | [Draft PR #7](https://github.com/pskeffington/pauls_notes/pull/7), reviewed head `bb18d902f5f69f1e4faf5950f6259b45bb301875`; [public-data safety CI passed](https://github.com/pskeffington/pauls_notes/actions/runs/39052793655) | **Not merged or enforced on `main` yet**; must re-synchronize after R4, configure required safety check and protected-policy review, complete Git history/secret scan, independently inspect privacy limitations and obtain signoff |
| D1 — current proposed real TCGA-BRCA study | No approved patient-level case cohort, model runner or verified study authorization in this public repository | **Blocked.** Requires authoritative file-level GDC open status, use/consent/privacy rights, patient/specimen linkage, endpoint and normalization, grouping, independent science and release authorization; **not** a blanket ban on other cancer research |

**D0 is not enforced on `main` yet.** The presence of a workflow does not make it a required protected-branch check. **Evidence boundary:** PR #7's passing *branch* checks do not establish protected `main` controls; recorded evidence is tied to the named head, not future rebases. [Issue #8](https://github.com/pskeffington/pauls_notes/issues/8) tracks required administration and historic secret review. There is no general patient-data training admission in R4.

## Next phased acceptance sequence

1. **Documentation and learning:** keep R0–R4 as bounded completed deliverables, maintain the 34-source corpus, and require learner explanation rather than a CI badge for mastery.
2. **Privacy first:** reconcile D0/PR #7 against latest `main` and verify its registered assets; obtain appropriate branch protection, secret/history checks and reviewer signoff. Do not infer privacy from a successful heuristic scan alone.
3. **Synthetic parameterized research:** R4 is delivered by PR #16, with grouped nested tuning, full candidate/feature traces and descriptive calibration-count audits. Preserve the synthetic-only contract. A different tumor dataset or native Rust variable-driven learner requires a **new** study and numerical-review gate.
4. **Rust predictor parity:** R3 is closed within the frozen synthetic final-development numerical replay. Maintain the 90-row parity reference, explicit category-1 meaning, stored hashes and nonclinical restrictions; require a separately approved protocol for new methods or real data.
5. **New science:** G4 requires a frozen synthetic time-to-event protocol; G5 requires declared source and reproduction target. The current D1/TCGA-BRCA proposal stays blocked until its separate authorized real-data protocol. These are not automatically completed by R3/R4.

## Completion discipline

Use focused branches and reviewable PRs; preserve concurrent work and history. For every subsequent pass, update the relevant row with actual PR/source commits, exact commands/environment, test and artifact evidence, numerical findings, scientific review, remaining risks and the next executable dependency. Preserve failures and avoid claiming improvement as an acceptance criterion. A learner can demonstrate mastery using the [analysis record](../templates/analysis-record.md); software evidence alone cannot set that status.
