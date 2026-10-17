# 7. Rust practice and competency gates

[← Research engineering](06_breast_cancer_engineering.md) · [Course contents](README.md) · [Advanced engineering handbook](../../02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md)

Practice in order; each stage assumes the preceding one. Predict the result before running tests. **Every dataset is invented.** Make changes in a local practice copy or a dedicated branch; do not modify the frozen G3 protocol or claim that teaching output is a new cancer finding.

## Verify the unmodified course first

~~~bash
cargo +1.90.0 fmt --manifest-path 03_learning/rust/lab/Cargo.toml -- --check
cargo +1.90.0 clippy --locked --manifest-path 03_learning/rust/lab/Cargo.toml --all-targets -- -D warnings
cargo +1.90.0 test --locked --manifest-path 03_learning/rust/lab/Cargo.toml
cargo +1.90.0 run --locked --manifest-path 03_learning/rust/lab/Cargo.toml
~~~

A clean test is a **code checkpoint**, not evidence of a clinical result. The separate [CI job](../../.github/workflows/rust-foundations-learning.yml) checks the course on the pinned compiler and expected summary.

## Learning gates

| Gate | Challenge | Expected result | Failure worth checking |
| --- | --- | --- | --- |
| F0 | Explain `fn main`, `let`, `mut`, `usize` and `f64` | You can distinguish six people from twelve fictional specimens | Miscounting files/rows as people |
| F1 | Compute `log2_change(20.0, 10.0)` | `Ok(1.0)` | `log2_change(0.0, 10.0)` must be `Err` |
| F2 | Count positive values in `[1.0, 2.0, 0.0, -1.0, 1.0, 0.0]` | Exactly three positives | `NaN` must fail rather than silently count |
| F3 | Borrow a `String` as `&str` and pass a `&mut Vec<String>` | Caller retains owned text and gains one checked label | A duplicate or whitespace label fails |
| F4 | Construct a `Specimen` and `Pair` with methods | Same-person comparator/tumor pair gives `Some(1.0)` log2 ratio | Opposite-person pairing fails |
| F5 | Implement/read a `Describe` trait | A `Specimen` and `GeneAnnotation` use one behavior interface | Gene domain is not a measured feature |
| F6 | Validate a grouped train/test partition | Fictional person IDs are disjoint and each pair is complete | Assessment contains a training person |
| F7 | Fit `MedianPreparation` only on train | Median 15 from invented values 10 and 20 | Test-data mutation changes fitted statistic |
| F8 | Use Cargo tests and code review | Pin toolchain, lockfile, exact source and green CI evidence | Green lint mistaken for scientific validity |
| F9 | Design a future research adapter (paper exercise) | Approved input/target/normalization/grouping/holdout contract | Controlled-access or identifiable records passed to public Git |

## Deliberate failing experiments

These are **questions and test fixtures**, not directions to disable protections.

1. What should happen when the second tissue record has a *different fictional person*? Inspect `Pair::new` and `validate_person_split`. Explain which invariant would fail.
2. What happens when `None` is supplied for both training measurements? `MedianPreparation::fit` must reject an all-missing training set.
3. What happens when you request `samples.get(20)` on a two-item vector? Compare `None` with the panic from direct `samples[20]` indexing; prefer checked access at a file/data boundary.
4. What happens if the same gene symbol appears twice? Compare a benign repeated mention in reading material with an actual duplicate feature column requiring a schema failure.
5. What happens when a held-out measurement changes? Verify that the fitted training median does not change. Then articulate why the same property should apply to fitted scaling, gene selection and calibration.

## Two ways to demonstrate mastery

**Programmer route:** Explain an ownership move, refactor a teaching function to accept `&str` or `&[T]`, show how a checked constructor protects a type, and add a negative unit test for a malformed synthetic input. Run `cargo test` and `cargo clippy`.

**Researcher route:** Draw a record flow from person → specimen → assay → feature matrix → grouping → fitting → held-out prediction → interpretation. Label which operations occur **before** versus **within** training folds. Explain why a trait can share code behavior without proving two data types are scientifically interchangeable.

## When are you ready for the advanced Rust engineering handbook?

You are ready when you can reproduce the expected synthetic output, explain every source module, use `?`/`Result` for input errors, reject person-level leakage and distinguish biological annotation from measured feature importance. Continue to the [source-backed coding guide](../../02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md), [six-pair book Rust exercise](../../02_biomedical_coding/examples/book_paired_specimens.rs) and [native training protocol](../../04_machine_learning/rust-training-protocol.md).

**Use restriction:** No participant data are included. These lessons do not authorize TCGA controlled data, independent diagnosis, prognosis or treatment decisions.

[Return to course contents](README.md)
