# 5. Engineering foundations: Cargo, modules, errors and testing

[← Object-oriented Rust](04_structs_traits_and_composition.md) · [Course contents](README.md) · [Next: breast-cancer research engineering](06_breast_cancer_engineering.md) · [Cargo documentation](https://doc.rust-lang.org/cargo/)

Small snippets teach syntax; a **crate** (Rust compilation unit/package code) makes a maintainable program. A **Cargo package** may include a library, binary, tests and examples. This course lab deliberately has **no third-party dependencies** so you can first learn tooling before adopting numerical ML crates.

## The project tree

~~~text
03_learning/rust/lab/
├── Cargo.toml            # package metadata, edition and dependencies
├── Cargo.lock            # resolved dependency versions (committed)
├── rust-toolchain.toml   # local pinned compiler and tools
├── src/
│   ├── lib.rs            # public module declarations
│   ├── main.rs           # executable entry point
│   ├── foundations.rs    # functions and arithmetic
│   ├── ownership.rs      # references and collection mutation
│   ├── objects.rs        # structs, enums, methods and traits
│   └── engineering.rs    # person groups, preparation and validation
└── tests/
    └── research_workflow.rs  # public-interface integration test
~~~

Inside `src/lib.rs`, `pub mod objects;` tells Rust to compile the `objects.rs` module and expose its public items. Inside `main.rs`, `use breast_cancer_rust_lab::objects::Specimen;` accesses the library API. Integration tests import the same public interface used by downstream code.

Our lab pins **Rust 1.90.0, edition 2021** because the repository's frozen native-training crate already uses that baseline. The current Rust Book can use edition 2024; migrating editions is a separate reviewed task, not necessary for learning objects.

## Build, execute, test, format and lint

From the **repository root**:

~~~bash
cargo +1.90.0 run --locked --manifest-path 03_learning/rust/lab/Cargo.toml
cargo +1.90.0 test --locked --manifest-path 03_learning/rust/lab/Cargo.toml
cargo +1.90.0 fmt --manifest-path 03_learning/rust/lab/Cargo.toml -- --check
cargo +1.90.0 clippy --locked --manifest-path 03_learning/rust/lab/Cargo.toml --all-targets -- -D warnings
cargo +1.90.0 build --release --locked --manifest-path 03_learning/rust/lab/Cargo.toml
~~~

- `run` compiles then starts the program.
- `test` runs unit tests, integration tests and supported documentation tests.
- `fmt -- --check` **checks** formatting without rewriting it.
- `clippy ... -D warnings` raises lints to actionable errors for this exercise.
- `build --release` builds the optimized executable; this is not a benchmark.
- `--locked` refuses changes to the lockfile. It does not guarantee bit-identical floating-point results across platforms.

Run one group of tests while studying its lesson: `cargo +1.90.0 test --locked --manifest-path 03_learning/rust/lab/Cargo.toml ownership`. For debugging, run `cargo ... test -- --nocapture` only if you understand what logs might reveal. Do **not** print or commit private identifiers.

## Documentation and error contracts

A public function should answer: *what inputs are accepted, what units do they represent, what errors are possible, and what output does it produce?* In Rust, use `///` comments for API documentation:

~~~rust
/// Return a log2 difference for positive invented comparable measurements.
///
/// # Errors
///
/// Rejects zero, negative or nonfinite inputs.
pub fn log2_change(tumor: f64, comparator: f64) -> Result<f64, &'static str> {
    // This lesson is an API sketch; the compiling implementation is in foundations.rs.
    if !tumor.is_finite() || !comparator.is_finite() || tumor <= 0.0 || comparator <= 0.0 {
        return Err("Invalid measurement");
    }
    Ok(tumor.log2() - comparator.log2())
}
~~~

Error messages should explain **what failed** without printing the sensitive input value. For a public research API, move from the lab's small `&'static str` errors toward **typed error enums** when you have multiple error classes and recovery needs. Do not suppress a failed validation with a default value.

## Tests that teach rather than merely pass

| Level | What it tests | Where |
| --- | --- | --- |
| Unit | Arithmetic and rejected zeros/NaNs | [`foundations.rs`](lab/src/foundations.rs) |
| Unit | Ownership and invalid duplicated labels | [`ownership.rs`](lab/src/ownership.rs) |
| Unit | Checked object construction and polymorphism | [`objects.rs`](lab/src/objects.rs) |
| Unit | Person overlap, duplicate pairs and leakage of held-out data | [`engineering.rs`](lab/src/engineering.rs) |
| Integration | A whole synthetic journey: math → objects → grouped split → train-only median | [`research_workflow.rs`](lab/tests/research_workflow.rs) |
| CI | Pinned fmt, Clippy, tests, run output and release build | [Rust foundations workflow](../../.github/workflows/rust-foundations-learning.yml) |

Test **invalid** inputs on purpose. A successful compile does not test a dataset's linkage, labels, follow-up, batch structure or privacy. Research test oracles should be independently specified instead of calculated with the same potentially wrong logic as the implementation.

## Build provenance and supply-chain boundaries

At an engineering handoff record: Git commit SHA, source/config hashes, Rust version/edition, `Cargo.lock` hash, enabled features, target/CPU, inputs, random seeds, expected output and actual CI status. The lab has no dependencies; the actual [Rust ML crate](../../04_machine_learning/rust/Cargo.toml) uses pinned libraries and a separately frozen numerical protocol. Do not retrofit a dependency, SIMD optimization or training objective into that frozen experiment without a new acceptance gate.

The [source-backed coding handbook](../../02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md) expands this to `serde`, `ndarray`, `linfa`, numerical oracles, RustSec, fuzzing and formal tools. Those are **next steps** after learning Cargo, not prerequisites for printing a first value.

**Checkpoint:** You can explain a Cargo manifest, a library versus a binary, module visibility, a unit versus integration test, the role of a lockfile and why passing Clippy does not prove a scientific result.

[Next: research engineering →](06_breast_cancer_engineering.md)
