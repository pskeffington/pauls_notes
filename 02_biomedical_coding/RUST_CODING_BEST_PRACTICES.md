# Rust coding best practices: verified sources and research-workflow checks

Authored by Paul Skeffington · Compiled with OpenAI

[Biomedical coding](README.md) · [Machine-learning methods](../04_machine_learning/README.md) · [Rust ML literature](../04_machine_learning/rust-ml-literature.md) · [Native Rust training](../04_machine_learning/rust-native-training.md) · [Breast cancer book](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) · [Structured source register](rust_coding_best_practices_sources.csv)

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

**RefinedRust: A Type System for High-Assurance Verification of Rust Programs** · Gaeh er; Sammler; Jung; Krebbers; Dreyer · PACMPL PLDI 2024 · 2024 · [primary record](https://doi.org/10.1145/3656422) · `abstract_and_selected_publisher_sections` · RG-09

- **Supported:** Machine-checked refined ownership proofs can cover selected safe and unsafe Rust.
- **Limit:** Prototype and Vec case study do not generalize to all numerical ML pipelines.
- **Project action:** Avoid claiming verified numerical semantics merely from safe Rust compilation.

#### RC-P06

**Beyond Memory Safety: an Empirical Study on Bugs and Fixes of Rust Programs** · Authors as indexed by IEEE · IEEE QRS 2024 · 2024 · [primary record](https://ieeexplore.ieee.org/abstract/document/10684674) · `abstract_metadata` · RG-04

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

**Targeted Fuzzing for Unsafe Rust Code: Leveraging Selective Instrumentation** · Paassen; Giesen; Davi · arXiv 2025 · 2025 · [primary record](https://arxiv.org/abs/2505.02464v1) · `abstract_metadata` · RG-04

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

The [structured source register](rust_coding_best_practices_sources.csv) is validated offline by `scripts/check_rust_coding_corpus.py`, including duplicate DOIs, source classes, dates, card coverage, scientific-claim statuses and the current crate's pinned manifest/toolchain. **Corpus integrity is bibliographic and policy evidence, not proof that each third-party crate is vulnerability-free or each numerical method is correct.**
