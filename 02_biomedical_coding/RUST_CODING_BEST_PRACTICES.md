# Rust engineering handbook: best practices for breast cancer research

Authored by Paul Skeffington · Compiled with OpenAI

[Biomedical coding](README.md) · [Machine-learning methods](../04_machine_learning/README.md) · [Rust ML literature](../04_machine_learning/rust-ml-literature.md) · [Native Rust training](../04_machine_learning/rust-native-training.md) · [Breast cancer book](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) · [Structured source register](rust_coding_best_practices_sources.csv) · [Publication bibliography](rust_coding_references.bib)

**Read first:** [Book chapter crosswalk](#1-chapter-by-chapter-crosswalk-what-rust-must-preserve) · [Run the six-pair Rust exercise](#2-example-first-workflow-reproduce-the-books-six-pairs) · [Types and input contracts](#3-types-should-rule-out-scientific-category-errors-rg-01--rg-02) · [ML leakage prevention](#5-separate-partitioning-preprocessing-fitting-and-evaluation-rg-01--rg-05) · [Pull-request checklist](#9-small-actionable-pull-request-review-checklist) · [Source appraisals](#source-by-source-coding-decisions)

**Evidence checked on 2026-10-17.** This targeted coding-focused corpus contains **34 distinct sources: 6 peer-reviewed papers, 2 preprints, 17 primary Rust documentation pages, and 9 tool/framework references**. It complements—not replaces—the separate [Rust machine-learning review](../04_machine_learning/rust-ml-literature.md) of native training, deployment, bindings, and single-cell methods.

## Scope and evidence grades

Question: **Which Rust coding practices and source-backed verification techniques make the project's breast-cancer ML teaching pipeline safe to modify, numerically auditable, secure, and reproducible?** The recent research search window is **2021-10-17 through 2026-10-17**; living language/tool documentation is recorded separately and **is not counted as research literature**. Papers are assessed from DOI/publisher/venue metadata and accessible selected abstracts; **this pass did not reproduce any paper experiment, run its verification artifact, or conduct a systematic full-text review**. The register states each item's actual reading depth. A source page or citation alone is not an audited library implementation.

The corpus was collected by targeted searches for Rust ownership, API guidelines, unsafe-code defect studies, fuzzing, formal verification, Cargo reproducibility, dependency auditing, scientific numerics, and crate-specific behavior. Inclusion requires a primary publisher/research venue or maintainer documentation and a concrete application/failure case for this repository. Excluded: uncited blog rules as proof, tool popularity lists, speculative Rust-vs-Python speed claims, and sources that do not affect code or scientific interpretation. The eight recent research records are not a statistical sample of Rust software defects.

**Priority:** trustworthy data contracts and numerical outputs before optimization. Safe Rust eliminates important classes of memory errors but does not validate an endpoint, correct group assignments, convergence, calibration, or clinical utility. In particular, the published `linfa-logistic 0.8.1` class-label mapping requires explicit canonicalization in this project's [G3 source review](../04_machine_learning/rust-training-source-addendum.md).

## Coding gates for this repository

| Gate | Coding standard | Applied requirement | Current scope |
| --- | --- | --- | --- |
| RG-01 | Define observational units | Distinguish person, specimen, assay feature, training partition and outcome; ensure that two specimens from one person stay within the same split | Rust G3 synthetic paired-assay checks exist |
| RG-02 | Stable typed interfaces | Use clear structs, `Result`, well-scoped APIs, documented errors and newtypes where mixing units would be dangerous | Existing `Input`, `Plan`, `Preparation`; ergonomic newtypes proposed |
| RG-03 | Fail-closed data and files | Deny unknown schema keys; validate counts/types/order/finite values; create new external output and protect against overwrites | Existing strict serde schemas and output checks |
| RG-04 | Layered tests | Unit, malformed-input, adversarial, property, integration and cross-runtime tests; keep a separate independent oracle | Rust unit tests and Python replay exist; fuzzing proposed |
| RG-05 | Numerical correctness | Freeze objective/penalty/label direction, training-only preprocessing, tolerances and termination residual; test extreme logits | Matched Rust/Python G3 numerical experiment completed on synthetic data |
| RG-06 | Reproducible build | Pin toolchain, Cargo dependencies and lockfile; record compiler, CPU, flags, seeds, source hashes and execution identity | Frozen G3 build/evidence controls exist |
| RG-07 | Dependency and unsafe-code review | First-party `#![forbid(unsafe_code)]`; inspect transitive dependencies, RustSec advisories, audit source/licensing | First-party unsafe forbidden; extra supply-chain tools not executed in this pass |
| RG-08 | Measured performance | Profile before optimizing; keep feature sets, inputs, objective, precision and hardware matched | Resource observations exist; no speed superiority claim |
| RG-09 | Optional high assurance | Evaluate bounded proofs/Miri/Kani or refinement systems only for concrete critical invariants | Research candidates only; no verification result asserted |
| RG-10 | Research data/privacy/clinical boundary | TCGA open-access metadata is not blanket permission; no controlled data, direct identifiers, or participant-level outputs in public Git | Existing synthetic baseline; separate [private Dartmouth research gates](../docs/research-workflow.md#2-specify-input-and-access-contracts) remain |

### Working Rust quality commands

These match the project's **pinned Rust 1.90.0 / edition 2021** baseline; do **not** silently migrate editions, optimizer dependencies, or the frozen G3 experiment while editing the coding guide.

```bash
cargo +1.90.0 fmt --manifest-path 04_machine_learning/rust/Cargo.toml -- --check
cargo +1.90.0 clippy --locked --manifest-path 04_machine_learning/rust/Cargo.toml --all-features --all-targets -- -D warnings
cargo +1.90.0 test --locked --manifest-path 04_machine_learning/rust/Cargo.toml --all-features
cargo +1.90.0 build --release --locked --manifest-path 04_machine_learning/rust/Cargo.toml --all-features
python3 04_machine_learning/tests/test_breast_cancer_rust_training.py
python3 scripts/check_rust_coding_corpus.py
python3 scripts/tests/test_rust_coding_corpus.py
```

The native training experiment additionally requires the independent [frozen protocol, Python oracle and artifact audit](../04_machine_learning/rust-training-protocol.md); running these quality commands alone is not G3 scientific acceptance. Optional `cargo fuzz`, `cargo deny`, `cargo vet`, Kani and Miri require **separately controlled tool installation, versions, target selection and dedicated CI evidence**, and **were not run** as part of this literature pass.

### Breast-cancer ML crosswalk

| Research problem | Rust programming hazard | Mandatory review/test |
| --- | --- | --- |
| Paired patient and tumor/normal samples | Indexing by specimen instead of person; leaking paired rows across train/test | Group exclusivity and exact partition coverage; test swapped and duplicate IDs |
| Synthetic selected-panel classifier | Computing medians/means or gene-selection scores before inner split | Fit all preparation/selection on training rows in *each* fold; mutate assessment values and check unchanged fit |
| Logistic class output | Positive class can depend on library-internal encoding | Save explicit category-1 mapping and compare each probability against independent calculation |
| Hyperparameter tuning | Comparing unmatched objectives or treating selected inner scores as independent test accuracy | Freeze regularization, intercept, metric direction, search space and held-out evaluation before execution |
| Expression-matrix import | Silent feature reordering, unit confusion (counts/TPM/log transform) or overflow | Record assay scale, annotation version, exact feature names/order, shape and finite checks |
| Scientific visualizations | Raw prediction exports can reveal linkable records; rounded labels can hide calibration errors | Release only reviewed aggregate figures; retain unrounded local values for independent audit |
| Public TCGA-BRCA files | Mistaking public project membership for unrestricted file access | Check authoritative GDC per-file `access=open`; keep patient-linked data and trained models outside public Git |
| Rust performance comparison | Using differing optimizer criteria, target CPU flags or thread counts | Match inputs and mathematical objective; report precision, compiler, machine, repetitions and actual numerical differences |

**Privacy and model-use disclaimer:** All current executable assay data referenced by this guide are **synthetic teaching data**. No biological or clinical accuracy is established by these sources or Rust's language guarantees. Any future use of GDC open data requires separately approved inputs and scientific methods. Models are **research/education only**, never for diagnosis, treatment decisions or individualized prognosis; do not attempt patient reidentification.


## Practical Rust handbook: from the book to defensible code

This is the **operational engineering guide** for the [breast cancer book](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md), not a claim that a literature paper validates a cancer model. The source cards below remain the research trace. Follow the implementation order here: **observation meaning → type/schema → partition → transformation → fit → evaluation → interpretation → safe release**. Use the book's own terminology and do not silently broaden a specimen-category classifier into screening, survival, a subtype assay or therapeutic prediction.

### 1. Chapter-by-chapter crosswalk: what Rust must preserve

| Book chapter | Scientific meaning | Rust responsibility | Failure to test |
| --- | --- | --- | --- |
| [1 — People](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-1-the-people-behind-the-numbers) | Human participants, not rows or file counts | A stable `PersonId` / case mapping never used as a predictor | Double-counting specimens as independent people |
| [2 — Dataset](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-2-understanding-the-breast-cancer-dataset) | Person → case → tissue → sample → assay file | Different identifier types; unique mapping and duplicate checks | Joining expression columns to the wrong specimen |
| [3 — Measurement](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-3-how-researchers-measure-genes) | Counts, normalized measurements and log units differ | Declare `MeasurementScale`, gene ID/version and missingness semantics | Treating TPM/log TPM as raw RNA-seq counts |
| [4 — Subtypes](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-4-why-tumors-behave-differently) | Expression category and clinical receptor findings are different labels | Typed `TargetDefinition` plus independent label provenance | Training/evaluating on circular expression-derived subtypes |
| [5 — Gene biology](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-5-the-biology-behind-the-60-genes) · [6 — Gene atlas](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-6-the-integrated-60-gene-atlas) · [7 — Pathways](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-7-from-genes-to-biological-pathways) | Curated functions and pathway membership, not trained signatures | Immutable feature identities and an external source/annotation register | Mistaking a category network for molecular binding |
| [8 — Evidence and pairing](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-8-from-measurements-to-scientific-evidence) | One person may contribute two dependent specimens | Group-exclusive train/assessment and complete pair checks | Cross-person leakage, mistaken sample-size denominators |
| [9 — Figures](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-9-reading-the-scientific-figures) | Charts must disclose units, populations and denominators | Export aggregate plot data with versioned calculation provenance | A calibration plot with unreported sparse bins |
| [10 — Limits](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-10-what-the-data-cannot-tell-us) | Associations are not mechanistic or clinical evidence | Explicit model-card restrictions and research-purpose type | A performance number promoted into a clinical claim |
| [11 — Research question](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-11-working-through-a-research-question) | Six-pair arithmetic and synthetic tissue classification are separate exercises | Test the literal arithmetic and the independent ML objective separately | Replacing a six-pair sensitivity analysis with a confidence interval |
| [12 — Reporting](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-12-research-practice-references-and-next-steps) | Findings need an auditable design and limitations | Preserve source/config/lock hashes, versions, errors and run status | Publishing unrepeatable or privacy-sensitive outputs |

**Two distinct teaching datasets must stay distinct.** The book's Chapter 11 arithmetic uses **six invented pairs with a single comparable measurement**. The compiled [standalone Rust exercise](examples/book_paired_specimens.rs) reproduces it. The existing [G3 Rust native-training study](../04_machine_learning/rust-training-protocol.md) uses **60 invented people, two specimens per person and 48 anonymous continuous features**; it is a logistic software comparison with its own frozen loss. **Neither uses the book's 60 named genes as fitted predictors**, and neither establishes a TCGA-derived result.

### 2. Example-first workflow: reproduce the book's six pairs

**SYNTHETIC TEACHING EXERCISE — NO PARTICIPANT DATA.** The executable file [`examples/book_paired_specimens.rs`](examples/book_paired_specimens.rs) uses only the Rust standard library, no external dataset, no package installation and no access token. Compile it with the pinned **Rust 1.90.0** toolchain. Commands are run from repository root and write binaries only to `/tmp`, outside Git:

~~~bash
rustup toolchain install 1.90.0 --profile minimal --component rustfmt
rustfmt +1.90.0 --check --edition 2021 02_biomedical_coding/examples/book_paired_specimens.rs
rustc +1.90.0 --edition=2021 --test 02_biomedical_coding/examples/book_paired_specimens.rs -o /tmp/book-paired-tests
/tmp/book-paired-tests
rustc +1.90.0 --edition=2021 02_biomedical_coding/examples/book_paired_specimens.rs -o /tmp/book-paired-demo
/tmp/book-paired-demo
~~~

The six invented log2(tumor/comparator) contrasts are **+1, +2, 0, −1, +1, 0**. The aggregate mean is **0.5 log2 units** and the one-person-omitted means range from **0.2 to 0.8**. These are exact educational expectations, not confidence limits. The file checks complete pairs, duplicate tissues, nonpositive/nonfinite measurements, extreme numerical ratios, person overlap, and exhaustive partitions. The unit of statistical independence is **six invented people**, not twelve independent specimens.

**Why this code pattern?** `Tissue` is an enum instead of a Boolean; `Measurement` and `CompletePair` capture the identity and value contract; `BTreeMap` makes grouping and deterministic order explicit; `Result` propagates malformed inputs rather than silently dropping a specimen; `f64::is_finite` rejects NaN and infinity. Logarithms are subtracted after checking positive inputs, avoiding intermediate ratio overflow. `leave_one_out_range` removes one **whole person** at a time, consistent with Chapter 8.

The example intentionally does **not** normalize actual RNA-seq counts, estimate a population effect, fit a model, claim group differences, read TCGA cases, or implement survival analysis. Changing the arithmetic input to a real molecular table is a **new study**, not merely a different constant.

### 3. Types should rule out scientific category errors (RG-01 / RG-02)

Prefer small, validated domain types over loosely related integers and strings. `PersonId`, `SpecimenId`, `AssayId`, `GeneId`, `ObservationUnit` and `TargetDefinition` are **conceptual design types** for a future adapter; not all are implemented in the current crate. In a new module, give validated types private fields and checked constructors:

~~~rust
#[derive(Clone, Debug, Eq, PartialEq, Hash)]
pub struct PersonId(String);

impl TryFrom<String> for PersonId {
    type Error = &'static str;

    fn try_from(raw: String) -> Result<Self, Self::Error> {
        if raw.is_empty() || raw.trim() != raw || raw.chars().any(char::is_control) {
            return Err("Invalid participant identifier");
        }
        Ok(Self(raw))
    }
}
~~~

This *illustrates* Rust's newtype pattern; it is not a commitment to store real TCGA barcodes or print them in logs. Keep personal/linkable IDs in an authorized local data adapter only. Use `enum` for a closed class/measurement scale, `struct` for named fields, `Option<f64>` for truly missing numeric inputs (not zero), `Result<T,E>` for invalid input, and iterators/slices when copies are unnecessary. Reserve `unwrap`/`expect` for fixtures or previously proved invariants rather than boundary-facing production code. See [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/checklist.html) ([RC-D03](#rc-d03)) and [error handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html) ([RC-D01](#rc-d01)).

Use ownership deliberately: immutable borrows `&[T]` for read-only feature and split data; owned `Vec<T>` when the procedure must retain or transform it; avoid unnecessary cloning inside folds. Preserve deterministic iteration order when serializing evidence. Do not replace a checked type or explicit error with a panic merely because Rust would prevent a dangling reference.

### 4. Parse → validate → admit; never deserialize directly into trust (RG-03 / RG-10)

**Four different gates must all pass:**

1. **Storage/access:** A file's membership in TCGA-BRCA is not proof that it is GDC open access. Confirm authoritative per-file `access=open` and the approved project, then review local handling, small groups and restrictions. This guide does not authorize any real-data training.
2. **Schema:** Whitelist required fields and reject unknown or omitted keys (`#[serde(deny_unknown_fields)]`). Verify version, protocol, class definitions and feature ordering.
3. **Biological record:** Check person-to-specimen/sample relations, complete or declared missing pairs, duplicate keys, tissue label direction, batch/time meaning and assay units. A matrix's shape is not its meaning.
4. **Algorithm:** Check nonempty training sets, per-feature finite observed values, no duplicate indices or group overlap, and no assessment-only knowledge embedded in fitted preprocessing.

In the existing [Rust `Input::validate`](../04_machine_learning/rust/src/training.rs), the schema has `person_id`, `specimen_id`, `cohort_row`, `label` and `values: Vec<Option<f64>>`. The fixture requires exactly two tissue-category labels per fictional person; a real cohort could legitimately have a different sampling design, so **a new protocol** must define the permissible counts rather than bypassing the check. Preserve feature names *and* order when transposing an expression matrix; an assay feature reorder can yield plausible-looking but wrong predictions.

**Never** log or commit direct identifiers, participant barcodes, raw downloaded files, controlled-access GDC data, fitted real-person models or row-level predictions into this public corpus. General `serde` syntax is not a privacy filter. The separate [TCGA/privacy toolkit proposal (draft PR #7)](https://github.com/pskeffington/pauls_notes/pull/7) includes more safeguards but is **not a merged permission change**. See the [research access contract](../docs/research-workflow.md#2-specify-input-and-access-contracts).

### 5. Separate partitioning, preprocessing, fitting and evaluation (RG-01 / RG-05)

The [actual native-training implementation](../04_machine_learning/rust/src/training.rs) separates `Input::validate`, `Preparation::fit`, `Preparation::transform`, `objective_gradient`, and `fit`. The design is more important than the choice of crate:

- **Split by people**, not by rows, tissue specimens, sequencing libraries or individual cells. Development, inner assessment, outer assessment and final reserved people are separate obligations. Keep any related donor/family/site hierarchy consistent with the study question.
- **Fit transformations on current training people only.** Median imputation, scaling, supervised gene ranking/selection, calibration and dimensionality reduction all become part of the fitted procedure. Inner validation never learns medians or selected features from its held-out people.
- **Respect the label's origin.** Synthetic tissue category 0/1 is not a clinically verified receptor, PAM50, recurrence, survival or treatment-response endpoint. An expression-derived subtype is especially vulnerable to circular assessment if the predictors overlap the labeling algorithm.
- **Freeze the search** before evaluating it. Inner scores choose parameters; outer-held-out predictions assess the entire search; a reserved final cohort must not be used to debug or select settings.
- **Do not fit models using the book's genes because they look biologically persuasive.** The curated 60-gene atlas is a learning map. ESR1, ERBB2 and MKI67 lead to hormone/growth/proliferation biology, while CD8A and COL1A1 invite immune/stromal-composition questions. They are **not measured feature rankings in the current synthetic model**.

Test that changing a held-out row cannot alter the fitted training medians, scaling, coefficients or feature selection. The existing G3 suite includes `assessment_mutation_cannot_change_training`. A high AUC does not detect this class of leakage, and duplicate biological units may produce persuasive but invalid precision.

### 6. Treat floating-point results as part of the scientific contract (RG-05)

A Rust program that compiles can still return a biologically meaningless or numerically invalid estimate. In the [frozen G3 study](../04_machine_learning/rust-training-protocol.md), the objective is a **specific regularized logistic loss** using canonical **category-1** labels, penalty `0.5 * sum(w_j²)` and an unpenalized intercept; the exact loss normalization, optimizer and termination checks matter. The code uses:

- `f64` values with explicit finite checks before and after preprocessing, loss evaluation and prediction; positive scales and nonempty training columns.
- `f64::total_cmp` **only after nonfinite observations are screened** when sorting training values for medians. `total_cmp` defines an order even for NaNs; this does *not* make NaNs acceptable measurements.
- Stable sigmoid and softplus calculations rather than unchecked `exp(z) / (1 + exp(z))` on extreme logits.
- A separately calculated loss/gradient; the frozen G3 accepts the fit only when the gradient infinity norm is at most `1e-6`. It also compares canonical Rust probabilities with the library's encoded class probabilities to absolute difference at most `1e-12`.
- Independent Python comparisons, fixed cohort/split seeds, exact input and source provenance, and explicit optimizer failures.

The thresholds above are **specific to frozen G3**: do not relax them after viewing failing results or copy them into a new model as universal standards. For a new model, declare a new numeric tolerance and comparator *before* inspecting assessment outcomes. Never silently reinterpret coefficients with the opposite positive class. Favor checked matrix shapes and failure on an all-missing training column, nonfinite gradient, exhausted iteration budget, or invalid model weights. See [`f64` documentation](https://doc.rust-lang.org/std/primitive.f64.html) ([RC-D10](#rc-d10)) and [pinned Linfa docs](https://docs.rs/linfa-logistic/0.8.1/linfa_logistic/) ([RC-T07](#rc-t07)).

### 7. Test a scientific contract, not just the implementation (RG-04 / RG-09)

| Test layer | Expected signal | Deliberate negative control | Repository action |
| --- | --- | --- | --- |
| Tiny arithmetic oracle | Six invented pairs produce 0.5, leave-one-out 0.2–0.8 | Missing/duplicate pair, zero or infinite measurement | [Rust book example](examples/book_paired_specimens.rs) |
| Schema/property | Unique IDs, finite values and exact feature order | Swap feature columns, duplicate row, add unknown JSON field | [Rust `Model` tests](../04_machine_learning/rust/src/lib.rs) |
| Statistical design | Train and assessment people disjoint | Reassign one person across sides; mutate held-out values | [Native Rust training tests](../04_machine_learning/rust/src/training.rs) |
| Numerical algorithm | Known gradients, sign mapping, stable probabilities | Reversed label, saturated logit, no convergence | [G3 validation](../04_machine_learning/rust-native-training.md) |
| Cross-runtime parity | Rowwise predicted probabilities match declared tolerance | Change normalization, class polarity or a coefficient | [Rust/Python validation](../04_machine_learning/validation/validate_rust_inference.py) |
| Malicious data | No unsafe export, panic or unbounded allocation on untrusted bytes | Oversized CSV/JSON, malformed UTF-8, unknown keys and duplicate IDs | **Fuzzing/resource quotas proposed, not yet audited** |
| Independent study | New-site, new-person performance and biological relevance | Reusing discovery subjects in assessment | **Not established for any clinical TCGA endpoint** |

[Recent empirical studies](#rc-p01) motivate adversarial cases; [RULF](#rc-p02) motivates API-aware fuzzing. Tools such as [cargo-fuzz](#rc-t04), [Kani](#rc-p07), [Verus](#rc-p04) and [RefinedRust](#rc-p05) can complement testing for bounded properties. **They are optional research candidates here, not installed/executed security proofs**. Model-checker completeness is limited by its harness, assumptions, bounds and unsupported features.

### 8. Structure the crate for review and reproducible execution (RG-02 / RG-06 / RG-07)

Keep **library code** small and testable, and **CLI code** limited to argument handling, validated input reading, output management and a recorded exit status. Keep training and inference artifacts distinct; a previously fitted model should not carry training labels or silently refit. A practical module boundary for future code is:

~~~text
domain/       person, specimen, assay and target types (validated)
ingest/       local authorized file admission; mapping and schema
splits/       deterministic person-level memberships
prepare/      fit/transform with training-only parameters
models/       declared objective and class mappings
evaluate/     held-out metrics, error and uncertainty records
artifacts/    non-overwriting external outputs, hash/provenance
cli/          flags, errors and exit status; no scientific decisions
~~~

**This is a proposed module organization, not the present crate tree.** The existing crate deliberately keeps its frozen synthetic objective in `src/training.rs` and frozen inference in `src/lib.rs`; adding modules is a separate change requiring parity checks.

| Guard | Required practice | What it does **not** prove |
| --- | --- | --- |
| Pinned toolchain | Rust `1.90.0`, edition `2021`, `rustfmt`, Clippy; review any migration | Identical machine code or independent experiment |
| Dependency resolution | Commit `Cargo.lock` and use `cargo --locked` | No vulnerable transitive crate |
| Unsafe scope | `#![forbid(unsafe_code)]` in first-party modules; inspect dependencies/FFI separately | All dependencies are written in safe Rust |
| IO discipline | Validate first; write to a new output directory outside Git; `OpenOptions::create_new(true)` | Atomic whole-run transaction or privacy deidentification |
| Provenance | Input/config/lock/source hashes, features, seeds, versions, CPU/flags and class mapping | Scientific validity of the chosen endpoint |
| Supply-chain review | Pilot RustSec, cargo-deny and cargo-vet under pinned policy and documented reviewers | An absence of undiscovered vulnerabilities |
| Performance | Profile separate read/prepare/fit/score phases; controlled warmup and repetitions | Faster Rust necessarily improves clinical utility |

Rust's API guidelines [recommend meaningful errors and validation](https://rust-lang.github.io/api-guidelines/dependability.html); the [Cargo Book](https://doc.rust-lang.org/cargo/commands/cargo-test.html) explains `--locked`. The [Rustonomicon](https://doc.rust-lang.org/nomicon/working-with-unsafe.html) documents the additional invariant burden of unsafe code; the source-catalog [Rudra study](#rc-p01) motivates scrutiny of ecosystem memory-safety bugs, even with safe application code. Do not add a third-party dependency solely to replace a three-line checked standard-library operation.

### 9. Small, actionable pull-request review checklist

Use this table when an AI or contributor modifies the Rust section. **Failing a required check blocks promotion**; a new scientific target requires a new frozen protocol rather than a relaxed check.

| Review question | Acceptance evidence |
| --- | --- |
| What is being estimated, on which people and specimens? | Question, target, unit/denominator and data provenance documented |
| Do the types carry the distinctions we need? | Schema/type definitions, unit handling and explicit category-1 identity |
| Could any held-out data reach fitted preparation? | Train/assessment IDs and mutation/leakage tests |
| Is the algorithm mathematically the same as the reference? | Objective/penalty/intercept definition and independent numerical oracle |
| Are exceptional values and unexpected input rejected? | Negative tests for NaN, infinity, missing/duplicate IDs, shape and unknown fields |
| Does execution replay exactly the intended build? | Toolchain, Cargo.lock, enabled features, source/config hashes, seed and command |
| Are dependencies, unsafe blocks and output permissions reviewed? | Advisory/license review status, refusal to overwrite and no protected data in Git |
| Does the claim match the evidence? | Synthetic/real-data distinction, uncertainty/limitations and no clinical promotion |
| Did the checks actually run? | Commit-specific green CI, attached sanitized logs and a separate reviewed decision |

### 10. AI-assisted variable-only research workflow

An AI may edit **allowed synthetic variables** (people, paired specimens, feature count, missingness, seed, fold count, search candidates) in a separate configuration-driven runner, then execute and evaluate its **explicitly synthetic** protocol. The [configuration-driven toolkit draft](https://github.com/pskeffington/pauls_notes/pull/7) is tracked separately from the stable, frozen G3 crate. A config change must **never** change: observational unit, positive-class meaning, privileged file access, assessment reservations, numerical reference or consent without a new approved protocol. Record which settings were changed and which experiments were rerun.

A real TCGA-BRCA adapter will require **new** patient/specimen data-use and scientific-admission checks, verified per-file GDC `open` status, no public PII/PHI or controlled assets, donor-grouped evaluation, source-dependent normalization, audited labels and approved outputs. This guide and Rust type safety alone cannot authorize that transition. All code, figures and models here are **research and educational only; not for diagnosis, clinical screening, treatment selection or patient-level prognosis**.

### 11. Worked exercises from the book

1. **Beginner (Chapter 11):** Run the six-pair example unchanged; explain why the mean is 0.5, why six rather than twelve is the independent-unit count, and why 0.2–0.8 is *not* a confidence interval. Change one fictional tumor value only on a new exercise branch and update its expected test; do not change a frozen G3 input.
2. **Intermediate (Chapters 2, 3 and 8):** Add a *synthetic* mismatch fixture to `complete_pairs` (missing sample, duplicate tumor, reversed unit) and show it fails closed. Explain why a raw count matrix cannot be substituted into the simple ratio example or logistic preprocessing.
3. **Advanced (Chapters 6, 10 and 11):** Trace one anonymous G3 feature through the saved feature order, median, scale, class-1 logit and Python parity. Separately consult ESR1, CD8A and COL1A1 gene cards to propose biological *questions* about hormone, immune and stromal contributions; **never present the anonymous feature as one of these genes**.
4. **Research-engineering (Chapters 8 and 12):** Write a new protocol for a future approved person-grouped experiment with missingness/selection inside each inner fold, a held-out evaluation, clean source hashes, uncertainty plan and model card. Keep the original book figures and synthetic baselines unchanged.

### 12. Implementation status and next code gates

- **In main:** frozen synthetic Rust inference, separate native Linfa training baseline, numerical checks, literature/citation corpus and now a **standalone book arithmetic + grouping reference with source tests**. No first-party unsafe code is introduced.
- **Not established by this guide:** fuzzing coverage, property-testing coverage beyond the documented fixtures, formal verification, systematic supply-chain audit, multiclass/subtype and survival training, protected TCGA input, private Dartmouth approval, generalizable disease prediction or clinical utility.
- **Next engineering gate:** independent code review of any future numeric parser/adaptor; bounded input sizes, checked file staging, leakage negative controls, source/lock/license review and end-to-end parity on a prespecified **synthetic** fixture *before* any new study-specific data permission.


## Literature appraisal: recent research (8 records)

| Record | Source | What it contributes | Review limitation |
| --- | --- | --- | --- |
| [RC-P01](#rc-p01) | [Rudra: Finding Memory Safety Bugs in Rust at the Ecosystem Scale](https://dl.acm.org/doi/10.1145/3477132.3483570) (2021; paper) | Unsafe dependencies can undermine guarantees of safe calling code. | Ecosystem bug-finding is not proof that this project has a memory defect. |
| [RC-P02](#rc-p02) | [RULF: Rust Library Fuzzing via API Dependency Graph Traversal](https://conf.researchr.org/details/ase-2021/ase-2021-papers/6/RULF-Rust-Library-Fuzzing-via-API-Dependency-Graph-Traversal) (2021; paper) | API sequence generation can increase Rust library fuzz coverage. | Published library workloads do not establish correctness of our CSV/JSON parser. |
| [RC-P03](#rc-p03) | [Flux: Liquid Types for Rust](https://doi.org/10.1145/3591283) (2023; paper) | Refinement types support stronger invariants in selected Rust programs. | Prototype formal technique not a default general-purpose production lint. |
| [RC-P04](#rc-p04) | [Verus: Verifying Rust Programs using Linear Ghost Types](https://2023.splashcon.org/details/splash-2023-oopsla/11/Verus-Verifying-Rust-Programs-using-Linear-Ghost-Types) (2023; paper) | SMT-backed proof specifications can establish properties beyond borrowing checks. | Formal proof demonstrations do not verify Linfa optimization or current native training. |
| [RC-P05](#rc-p05) | [RefinedRust: A Type System for High-Assurance Verification of Rust Programs](https://doi.org/10.1145/3656422) (2024; paper) | Machine-checked refined ownership proofs can cover selected safe and unsafe Rust. | Prototype and Vec case study do not generalize to all numerical ML pipelines. |
| [RC-P06](#rc-p06) | [Beyond Memory Safety: an Empirical Study on Bugs and Fixes of Rust Programs](https://ieeexplore.ieee.org/abstract/document/10684674) (2024; paper) | Study characterizes non-memory defects and failures including panics in Rust projects. | Observational code sample is not a measured defect rate for this repository. |
| [RC-P07](#rc-p07) | [Kani: A Model Checker for Rust](https://arxiv.org/abs/2607.01504v1) (2026; preprint) | Kani combines bounded checking and proof contracts for safety and correctness properties. | Preprint methods and case studies require review before adoption; not automatically peer reviewed. |
| [RC-P08](#rc-p08) | [Targeted Fuzzing for Unsafe Rust Code: Leveraging Selective Instrumentation](https://arxiv.org/abs/2505.02464v1) (2025; preprint) | Selective instrumentation targets unsafe code in reported fuzzing research. | Preprint does not establish benefit for our safe first-party logistic pipeline. |

## Source-by-source coding decisions

Every note records **what the source supports**, **what it cannot support**, and the **next code or validation check**. Papers, preprints and maintainer documentation are kept in separate families to avoid inflating a research-paper count.

### Peer-reviewed research

#### RC-P01

**Rudra: Finding Memory Safety Bugs in Rust at the Ecosystem Scale** · Bae; Kim; Askar; Lim; Kim · SOSP 2021 · 2021 · [primary record](https://dl.acm.org/doi/10.1145/3477132.3483570) · `abstract_metadata` · RG-07

- **Supported:** Unsafe dependencies can undermine guarantees of safe calling code.
- **Limit:** Ecosystem bug-finding is not proof that this project has a memory defect.
- **Project action:** Keep unsafe forbidden in first-party modules; review transitive crates and security advisories.

#### RC-P02

**RULF: Rust Library Fuzzing via API Dependency Graph Traversal** · Jiang; Xu; Zhou · ASE 2021 · 2021 · [primary record](https://conf.researchr.org/details/ase-2021/ase-2021-papers/6/RULF-Rust-Library-Fuzzing-via-API-Dependency-Graph-Traversal) · `abstract_metadata` · RG-04

- **Supported:** API sequence generation can increase Rust library fuzz coverage.
- **Limit:** Published library workloads do not establish correctness of our CSV/JSON parser.
- **Project action:** Add bounded fuzz targets for model-deserialization; adversarial specimen CSV; and CLI options.

#### RC-P03

**Flux: Liquid Types for Rust** · Lehmann; Geller; Vazou; Jhala · PACMPL PLDI 2023 · 2023 · [primary record](https://doi.org/10.1145/3591283) · `abstract_metadata` · RG-09

- **Supported:** Refinement types support stronger invariants in selected Rust programs.
- **Limit:** Prototype formal technique not a default general-purpose production lint.
- **Project action:** Use explicit finite-value and shape invariants first; study Flux for high-risk kernels only.

#### RC-P04

**Verus: Verifying Rust Programs using Linear Ghost Types** · Lattuada et al. · PACMPL OOPSLA 2023 · 2023 · [primary record](https://2023.splashcon.org/details/splash-2023-oopsla/11/Verus-Verifying-Rust-Programs-using-Linear-Ghost-Types) · `abstract_metadata` · RG-09

- **Supported:** SMT-backed proof specifications can establish properties beyond borrowing checks.
- **Limit:** Formal proof demonstrations do not verify Linfa optimization or current native training.
- **Project action:** Consider proofs for small serialization and index invariants only after conventional tests.

#### RC-P05

**RefinedRust: A Type System for High-Assurance Verification of Rust Programs** · Gäher; Sammler; Jung; Krebbers; Dreyer · PACMPL PLDI 2024 · 2024 · [primary record](https://doi.org/10.1145/3656422) · `abstract_and_selected_publisher_sections` · RG-09

- **Supported:** Machine-checked refined ownership proofs can cover selected safe and unsafe Rust.
- **Limit:** Prototype and Vec case study do not generalize to all numerical ML pipelines.
- **Project action:** Avoid claiming verified numerical semantics merely from safe Rust compilation.

#### RC-P06

**Beyond Memory Safety: an Empirical Study on Bugs and Fixes of Rust Programs** · Zhang; Feng; Zhang; Dai; Xu · IEEE QRS 2024 · 2024 · [primary record](https://ieeexplore.ieee.org/abstract/document/10684674) · `abstract_metadata` · RG-04

- **Supported:** Study characterizes non-memory defects and failures including panics in Rust projects.
- **Limit:** Observational code sample is not a measured defect rate for this repository.
- **Project action:** Add negative schema; panic; boundary; and computational regression checks.

### Research preprints

#### RC-P07

**Kani: A Model Checker for Rust** · Delmas et al. · arXiv 2026 · 2026 · [primary record](https://arxiv.org/abs/2607.01504v1) · `abstract_metadata` · RG-09

- **Supported:** Kani combines bounded checking and proof contracts for safety and correctness properties.
- **Limit:** Preprint methods and case studies require review before adoption; not automatically peer reviewed.
- **Project action:** Evaluate Kani for bounded parser and array-index properties after a prospective methods gate.

#### RC-P08

**Targeted Fuzzing for Unsafe Rust Code: Leveraging Selective Instrumentation** · Paaßen; Giesen; Davi · arXiv 2025 · 2025 · [primary record](https://arxiv.org/abs/2505.02464v1) · `abstract_metadata` · RG-04

- **Supported:** Selective instrumentation targets unsafe code in reported fuzzing research.
- **Limit:** Preprint does not establish benefit for our safe first-party logistic pipeline.
- **Project action:** Prioritize exposure surfaces and dependency review rather than fabricating performance gains.

### Rust language and official documentation

#### RC-D01

**The Rust Programming Language: error handling** · Rust Project · Rust Book · living · [primary record](https://doc.rust-lang.org/book/ch09-00-error-handling.html) · `primary_sections` · RG-02

- **Supported:** Recoverable errors are expressed with Result rather than hidden fallback paths.
- **Limit:** Error handling constructs do not determine scientific failure policy.
- **Project action:** Use Result at IO/schema/model boundaries; record failure and retain partial artifacts.

#### RC-D02

**The Rust Programming Language: automated tests** · Rust Project · Rust Book · living · [primary record](https://doc.rust-lang.org/book/ch11-00-testing.html) · `primary_sections` · RG-04

- **Supported:** Unit and integration tests complement the type system.
- **Limit:** Tests detect examples of defects but cannot prove total functional correctness.
- **Project action:** Test missing columns; group leakage; class mapping; probability precision; and overwrite refusal.

#### RC-D03

**Rust API Guidelines checklist** · Rust library team contributors · Rust API Guidelines · living · [primary record](https://rust-lang.github.io/api-guidelines/checklist.html) · `primary_sections` · RG-02

- **Supported:** Naming traits error types and API invariants should follow ecosystem conventions.
- **Limit:** Recommendations are discretionary and not a formal standard or clinical validation.
- **Project action:** Review public types and schema boundaries; avoid anonymous Boolean mode arguments.

#### RC-D04

**rustdoc: How to write documentation** · Rust Project · rustdoc book · living · [primary record](https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html) · `primary_sections` · RG-02

- **Supported:** Document public APIs with examples and failure behavior.
- **Limit:** Documentation is not an executed correctness proof.
- **Project action:** Document data units; class encoding; missingness; numerical errors; and examples.

#### RC-D05

**Clippy: continuous integration** · Rust Project · Clippy documentation · living · [primary record](https://doc.rust-lang.org/clippy/continuous_integration/index.html) · `primary_sections` · RG-04

- **Supported:** Use matching toolchain Clippy and treat warnings as actionable CI evidence.
- **Limit:** Static lints do not detect label leakage or invalid biological outcomes.
- **Project action:** Keep pinned rustfmt and clippy strict alongside independent numerical tests.

#### RC-D06

**Cargo.toml versus Cargo.lock** · Rust Project · Cargo Book · living · [primary record](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html) · `primary_sections` · RG-06

- **Supported:** Cargo.lock captures resolved dependency versions and supports repeatable builds.
- **Limit:** Pinned dependencies do not guarantee bit-identical results on different machines.
- **Project action:** Commit Cargo.lock; use --locked and save toolchain target profile and lock hash.

#### RC-D07

**Cargo metadata command** · Rust Project · Cargo Book · living · [primary record](https://doc.rust-lang.org/cargo/commands/cargo-metadata.html) · `primary_sections` · RG-06

- **Supported:** cargo metadata provides machine-readable workspace and dependency resolution.
- **Limit:** Metadata output is sensitive to enabled features and target selection.
- **Project action:** Record dependency graph and features for reproducible cross-runtime comparisons.

#### RC-D08

**Cargo profiles** · Rust Project · Cargo Book · living · [primary record](https://doc.rust-lang.org/cargo/reference/profiles.html) · `primary_sections` · RG-05

- **Supported:** Optimization debug assertions and overflow checks depend on build profile.
- **Limit:** Release defaults differ from development checks; optimization may change numerical behavior.
- **Project action:** Test debug and release fixtures; record flags and avoid undeclared fast math.

#### RC-D09

**Rustonomicon: Working with unsafe** · Rust Project · Rustonomicon · living · [primary record](https://doc.rust-lang.org/nomicon/working-with-unsafe.html) · `primary_sections` · RG-07

- **Supported:** Unsafe modules demand explicit invariants and encapsulation.
- **Limit:** Unsafe documentation is background not authorization to add unsafe blocks.
- **Project action:** Preserve forbid(unsafe_code); review all imported FFI and unsafe dependency surfaces.

#### RC-D10

**Rust f64 primitive documentation** · Rust Project · Rust standard library · living · [primary record](https://doc.rust-lang.org/std/primitive.f64.html) · `primary_sections` · RG-05

- **Supported:** f64 supports finite checks and explicit total ordering including NaNs.
- **Limit:** IEEE representations alone cannot guarantee numerical reproducibility across optimizers.
- **Project action:** Reject NaN/inf; use stable logit calculations; test extreme values and tolerances.

#### RC-D11

**Serde container attributes** · Serde maintainers · Serde documentation · living · [primary record](https://serde.rs/container-attrs.html) · `primary_sections` · RG-03

- **Supported:** deny_unknown_fields rejects unexpected keys in declared input structs.
- **Limit:** A strict object schema can still contain unsafe or unauthorized field contents.
- **Project action:** Validate provenance access classes identities and dimensions after deserialization.

#### RC-D12

**OpenOptions create_new atomic creation** · Rust Project · Rust standard library · living · [primary record](https://doc.rust-lang.org/std/fs/struct.OpenOptions.html#method.create_new) · `primary_sections` · RG-03

- **Supported:** create_new atomically rejects existing output files including symlinks.
- **Limit:** Atomic single-file creation does not guarantee whole-directory archival integrity.
- **Project action:** Use new outside-repo output directories and per-file exclusive writes.

#### RC-D13

**Cargo test command** · Rust Project · Cargo Book · living · [primary record](https://doc.rust-lang.org/cargo/commands/cargo-test.html) · `primary_sections` · RG-04

- **Supported:** Cargo executes unit integration and documentation tests.
- **Limit:** Passing cargo test is not independent biomedical model validation.
- **Project action:** Run --locked and all relevant features and targets in CI.

#### RC-D14

**Rust 2024 edition migration guide** · Rust Project · Edition Guide · living · [primary record](https://doc.rust-lang.org/edition-guide/rust-2024/index.html) · `primary_sections` · RG-06

- **Supported:** Edition migrations require explicit compatibility review.
- **Limit:** Current assay crate intentionally targets edition 2021 and Rust 1.90.
- **Project action:** Do not silently change edition or MSRV within the frozen G3 protocol.

#### RC-D15

**Rust Performance Book: Benchmarking** · Nicholas Nethercote and contributors · Rust Performance Book · living · [primary record](https://nnethercote.github.io/perf-book/benchmarking.html) · `primary_sections` · RG-08

- **Supported:** Representative workloads and repeated measurements support responsible optimization.
- **Limit:** Microbenchmarks cannot demonstrate clinical utility or cross-language superiority.
- **Project action:** Only measure Rust/Python time after matched objectives and prediction parity.

#### RC-D16

**Rust Performance Book: Profiling** · Nicholas Nethercote and contributors · Rust Performance Book · living · [primary record](https://nnethercote.github.io/perf-book/profiling.html) · `primary_sections` · RG-08

- **Supported:** Profile CPU hot spots and memory before optimization.
- **Limit:** Profiling by itself does not prove a model algorithm was correctly ported.
- **Project action:** Separate IO preparation training inference and RSS measurements.

#### RC-D17

**Unsafe Code Guidelines reference status** · Rust Unsafe Code Guidelines contributors · Historical UCG reference · living · [primary record](https://rust-lang.github.io/unsafe-code-guidelines/introduction.html) · `primary_sections` · RG-07

- **Supported:** The document identifies much of the unsafe guidance as abandoned/incomplete.
- **Limit:** Do not treat incomplete historical recommendations as normative guarantees.
- **Project action:** Prefer stable Rust docs; avoid new unsafe code in the research core.

### Tool and framework documentation

#### RC-T01

**RustSec Advisory Database** · RustSec maintainers · RustSec · living · [primary record](https://github.com/rustsec/advisory-db) · `primary_sections` · RG-07

- **Supported:** Security advisories can be checked against dependencies in Cargo.lock.
- **Limit:** No advisory match does not establish dependency absence of vulnerabilities.
- **Project action:** Use scheduled advisory review and record exact dependency revisions.

#### RC-T02

**cargo-deny dependency linting** · Embark Studios · cargo-deny · living · [primary record](https://github.com/EmbarkStudios/cargo-deny) · `primary_sections` · RG-07

- **Supported:** Check advisories licenses sources and duplicate/banned dependencies.
- **Limit:** License allowlist needs legal/policy approval; no tool alone establishes compliance.
- **Project action:** Pilot advisory and source checks on the Rust crate before requiring merges.

#### RC-T03

**cargo-vet supply-chain audits** · Mozilla contributors · cargo-vet · living · [primary record](https://mozilla.github.io/cargo-vet/) · `primary_sections` · RG-07

- **Supported:** Document independent audit coverage for third-party crates.
- **Limit:** Audit provenance depends on trust in imported reviews and scope.
- **Project action:** Use an approved audit policy for FFI and security-critical dependencies.

#### RC-T04

**Rust Fuzz Book cargo-fuzz** · Rust fuzzing contributors · Rust Fuzz Book · living · [primary record](https://rust-fuzz.github.io/book/cargo-fuzz.html) · `primary_sections` · RG-04

- **Supported:** libFuzzer can exercise adversarial byte sequences at parser boundaries.
- **Limit:** Fuzzing is probabilistic; zero crashes is not total correctness proof.
- **Project action:** Fuzz CSV headers malformed UTF-8 JSON shape and oversized allocations offline.

#### RC-T05

**Miri Rust MIR interpreter** · Rust Project · Miri repository · living · [primary record](https://github.com/rust-lang/miri) · `primary_sections` · RG-09

- **Supported:** Miri can help detect undefined behavior in supported executions.
- **Limit:** Miri does not explore every program path and needs a compatible toolchain.
- **Project action:** Reserve as optional verification for low-level dependency/FFI wrappers.

#### RC-T06

**ndarray 0.16.1 crate documentation** · ndarray contributors · docs.rs pinned crate · living · [primary record](https://docs.rs/ndarray/0.16.1/ndarray/) · `primary_sections` · RG-05

- **Supported:** ndarray encodes shapes dimensions and views for numerical matrices.
- **Limit:** Shape-valid arrays can still contain scientifically wrong labels or units.
- **Project action:** Validate nrows ncols row order missingness and finiteness before fitting.

#### RC-T07

**linfa-logistic 0.8.1 crate documentation** · Linfa contributors · docs.rs pinned crate · living · [primary record](https://docs.rs/linfa-logistic/0.8.1/linfa_logistic/) · `primary_sections` · RG-05

- **Supported:** Pinned logistic API offers binary fitting and probability prediction.
- **Limit:** An optimizer return is not evidence of convergence or sklearn objective equivalence.
- **Project action:** Recompute objective and gradient independently and canonicalize class identity.

#### RC-T08

**Criterion benchmarking library** · Criterion maintainers · docs.rs · living · [primary record](https://docs.rs/criterion/latest/criterion/) · `primary_sections` · RG-08

- **Supported:** Statistical repeated benchmarks help quantify performance variation.
- **Limit:** Microbenchmark confidence is not uncertainty about breast cancer model performance.
- **Project action:** Use separate controlled performance study if numerical agreement succeeds.

#### RC-T09

**Pragmatic Rust Guidelines checklist** · Microsoft Rust contributors · Microsoft Rust Guidelines · living · [primary record](https://microsoft.github.io/rust-guidelines/guidelines/checklist/) · `primary_sections` · RG-02

- **Supported:** Additional engineering recommendations cover linting and API maintainability.
- **Limit:** Organization-specific guidance is supplementary to upstream Rust documentation.
- **Project action:** Use as optional code-review checklist; do not auto-enforce conflicting preferences.


## Adoption order and validation checklist

1. **Baseline inspection:** keep the G3 Rust 1.90.0 target, Cargo.lock, library/class mapping and `#![forbid(unsafe_code)]` untouched. Preserve frozen training protocol bytes.
2. **Input and algorithm:** validate identities, partitions, field ordering, finite values and missingness; reject unrecognized data schemas and incoherent matrices before fitting.
3. **Tests and oracle:** run rustfmt/Clippy/unit tests, negative/failure fixtures, Python comparison and artifact replay; add property tests for conservation of group membership and invariance of training under assessment mutation.
4. **Supply chain:** evaluate RustSec/cargo-deny/cargo-vet under a separately pinned tool contract. Advisory checks and any license decisions need review; adding the documentation is **not** a completed audit.
5. **Numerical experiment:** retain the exact held-out rows, class mapping, precision and training residual and record errors instead of raising or relaxing tolerances post hoc.
6. **Reproducibility:** record toolchain target, machine environment, exact data/schema lineage, source hashes, selected settings, resources, outputs and failure logs outside public Git.
7. **Research release:** review public GDC file access individually, consent/reuse requirements, quasi-identifiers, model artifacts and small groups before publishing; no clinical-use claims.

The [structured source register](rust_coding_best_practices_sources.csv) and [eight-paper BibTeX bibliography](rust_coding_references.bib) are validated offline by `scripts/check_rust_coding_corpus.py`, including duplicate DOIs, source classes, dates, card coverage, scientific-claim statuses and the current crate's pinned manifest/toolchain. **Corpus integrity is bibliographic and policy evidence, not proof that each third-party crate is vulnerability-free or each numerical method is correct.**
