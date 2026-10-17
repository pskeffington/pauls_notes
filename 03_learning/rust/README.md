# Learn Rust: from the first variable to research engineering

[Paul's Notes](../../README.md) · [Computing subjects](../README.md) · [Breast cancer research book](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) · [Advanced Rust engineering handbook](../../02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md)

**Start here with no Rust experience.** This is an introductory, sequential course. Learn one building block, run a small test, explain what it does, then advance. The final lessons apply the same programming ideas to *invented* paired breast-cancer research examples. No TCGA data, private patient information, downloaded cohorts, or trained clinical model is used.

Rust is a compiled language with static types, ownership-based memory management, and several programming styles. You can write **object-oriented designs** using `struct`, `enum`, `impl`, traits and composition; Rust **does not have traditional class inheritance**. We begin with variables and functions rather than assuming you already know objects.

## Learning route

| Stage | Lesson | You will be able to… | Working source |
| --- | --- | --- | --- |
| 0 | [First steps: installation, a program and types](01_first_steps.md) | Run `fn main`, create variables, use functions and understand compiler feedback | [`foundations.rs`](lab/src/foundations.rs) |
| 1 | [Collections, conditions and failures](02_collections_and_control.md) | Use arrays, vectors, slices, strings, loops, `match`, `Option` and `Result` | [`foundations.rs`](lab/src/foundations.rs) |
| 2 | [Ownership and borrowing](03_ownership_and_borrowing.md) | Explain moving vs borrowing, `&`, `&mut`, `String` vs `&str`, and when to clone | [`ownership.rs`](lab/src/ownership.rs) |
| 3 | [Object-oriented Rust](04_structs_traits_and_composition.md) | Build structs, methods, encapsulated state, traits, generic behavior and composition | [`objects.rs`](lab/src/objects.rs) |
| 4 | [Cargo, modules, testing and tooling](05_cargo_testing_and_quality.md) | Navigate a crate, run tests, format, lint and capture reproducible builds | [`lab`](lab/Cargo.toml) |
| 5 | [Scientific engineering: paired specimens to training-only preparation](06_breast_cancer_engineering.md) | Validate person-exclusive partitions, missingness and training-only preprocessing | [`engineering.rs`](lab/src/engineering.rs) |
| 6 | [Practice, mastery checks and next engineering gates](07_practice_and_mastery.md) | Solve small tasks, repair deliberate failures and propose a safe research extension | [Integration test](lab/tests/research_workflow.rs) |

## Run the course lab

1. Install Rust through the [official rustup instructions](https://www.rust-lang.org/tools/install); verify `rustup`, `cargo`, and `rustc` are available. On Windows use PowerShell with an appropriate Rust toolchain installed. Do not paste unreviewed installation commands into privileged shells.
2. From the root of Paul's Notes, use the pinned **Rust 1.90.0** toolchain. The lab deliberately uses edition **2021** to match the existing frozen native Rust example; newer books may teach edition 2024.
3. Run:

~~~bash
rustup toolchain install 1.90.0 --profile minimal --component rustfmt,clippy
cargo +1.90.0 run --locked --manifest-path 03_learning/rust/lab/Cargo.toml
cargo +1.90.0 test --locked --manifest-path 03_learning/rust/lab/Cargo.toml
~~~

Expected lines from the synthetic lab:

~~~text
SYNTHETIC Rust lab | example log2 change = 1.000
Training-only median = 15.000; missing assessment imputed = 15.000
Trait summaries = 2
Research and education only; no participant data, trained model, or clinical claim.
~~~

The example is read-only: it constructs fictional observations in memory, prints summary text and stores no participant records. Cargo's compilation output stays under its `target/` folder unless you set `CARGO_TARGET_DIR`; do not commit compiled binaries.

## Two examples, two purposes

The [book's Chapter 11 six-pair Rust exercise](../../02_biomedical_coding/examples/book_paired_specimens.rs) computes invented log2 ratios, a 0.5 mean and 0.2–0.8 leave-one-person-out sensitivity range. This course lab is *smaller*: it demonstrates a **single invented pair, encapsulated types, and training-only median preparation**. Neither is the [60-person, 48-anonymous-feature G3 native logistic experiment](../../04_machine_learning/rust-native-training.md), and none of these software demonstrations trains on the [book's 60 named genes](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-6-the-integrated-60-gene-atlas).

## Why learn in this order?

A `Specimen` object is easier to understand after learning variables and functions. A constructor that borrows `&str` makes sense only after learning `String` and ownership. A trait-based interface becomes useful after you know how to define a struct. Finally, a leakage-proof machine-learning pipeline requires all of those ideas **plus** correct biological units, group assignment, and scientific validation.

**Research and educational use only.** The examples demonstrate programming mechanics, not diagnostic models, treatment selection, prognosis or new breast-cancer findings. Open-access TCGA files still require per-file authorization checks and an independent research protocol before any real-data model work.

[Start Lesson 1 →](01_first_steps.md)
