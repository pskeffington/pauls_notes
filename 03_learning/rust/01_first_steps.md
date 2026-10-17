# 1. Rust from zero: tools, a program, variables and types

[Course contents](README.md) · [Next: collections and control](02_collections_and_control.md) · [Official Rust Book](https://doc.rust-lang.org/stable/book/)

## What is Rust?

Rust is a compiled programming language. You write source files ending in `.rs`, a **compiler** checks the types and borrowing rules, and a program executable is built. The compiler catches many programming mistakes before execution, but cannot determine whether a tumor label, molecular measurement or statistical claim is scientifically correct.

- `rustc` compiles Rust source.
- `cargo` creates, builds, tests and runs Rust packages.
- `rustup` installs and selects Rust toolchains.
- `Cargo.toml` is the package manifest; `Cargo.lock` records dependency resolution.

The [course lab](lab/Cargo.toml) provides an existing Cargo package. See the [official Cargo new-package guide](https://doc.rust-lang.org/cargo/guide/creating-a-new-project.html) if you want to create your own from scratch (`cargo new my_first_app --bin --edition 2021`). Do not create a second Git repository inside Paul's Notes.

## Your first code: statements and a program entry point

~~~rust
fn main() {
    let person_count: usize = 6;
    let specimen_count = person_count * 2;
    println!("Invented people: {person_count}, specimens: {specimen_count}");
}
~~~

`fn` begins a function; `main` is the program's entry point. Braces mark a block. `let` binds a **variable**, `usize` stores a nonnegative count/index, `println!` is a **macro**, and the semicolon finishes a statement. The compiler infers the type of `specimen_count`. These six people and twelve specimens are fictitious—not independent counts of twelve people.

### Immutable and mutable values

~~~rust
let count = 6;             // cannot change this binding
let mut excluded = 0;      // mutation is explicitly permitted
excluded += 1;
let eligible = count - excluded;  // 5
assert_eq!(eligible, 5);
~~~

Use immutable bindings by default. `mut` changes a binding's mutability; it does not authorize mutation through every reference. The macro `assert_eq!` checks a condition and deliberately panics when it fails—appropriate in tests, not for routine external input failures.

## Small building-block types

| Type | Example | Meaning |
| --- | --- | --- |
| `i32` | `-1` | Signed integer, useful for arithmetic with negative values |
| `usize` | `6` | Nonnegative index/count (machine-sized) |
| `f64` | `20.0` | Floating-point, with rounding and NaN/infinity to consider |
| `bool` | `true` | Logical flag |
| `char` | `'T'` | Unicode scalar value |
| `&str` | `"ESR1"` | Borrowed string slice |
| `String` | `String::from("ESR1")` | Owned, growable UTF-8 text |
| `()` | `()` | The unit value; a function may return it implicitly |

Avoid mixing incompatible measurement scales. A value of `20.0` can be teaching units, counts, TPM or log-scaled expression—Rust sees an `f64` unless your domain types distinguish them.

## Arithmetic and functions

~~~rust
fn log2_change(tumor: f64, comparator: f64) -> Result<f64, &'static str> {
    if !tumor.is_finite() || !comparator.is_finite() || tumor <= 0.0 || comparator <= 0.0 {
        return Err("Both inputs must be positive and finite");
    }
    Ok(tumor.log2() - comparator.log2())
}

fn main() {
    let change = log2_change(20.0, 10.0).expect("fixed synthetic fixture");
    assert!((change - 1.0).abs() < 1e-12);
}
~~~

`->` declares the return type, `Result` expresses *either* a value (`Ok`) *or* a recoverable failure (`Err`), and `return` exits early. The final expression without `;` returns its value. The comparator is validated before dividing or taking logarithms. With invented values 20 and 10, the log2 ratio is +1. In production, handle `Err` rather than assuming input is valid with `expect`.

Read the tested implementation in [`foundations.rs`](lab/src/foundations.rs).

## Conditions, expressions and scope

~~~rust
let log2_change = 1.0_f64;
let label = if log2_change > 0.0 {
    "larger in the invented tumor measurement"
} else {
    "not larger in the invented tumor measurement"
};
assert!(label.starts_with("larger"));
~~~

An `if` expression produces a value. Variables inside braces normally leave scope at the closing brace. Declaring a new binding with the same name is **shadowing**, not mutation. Use descriptive variable names: `tumor_measurement` conveys more than `x`.

## Common errors worth learning

- `let score = 2 / 3;` yields integer `0`; use `2.0 / 3.0` for floating-point division.
- A `String` cannot be passed to every API requiring `&str` without borrowing it; Lesson 3 explains why.
- `f64` can represent `NaN` and infinity; check `is_finite()` at data boundaries.
- Indexing an invalid vector position can panic; `.get(index)` returns `Option`.
- A successful build is not proof of a scientifically valid denominator, normalized expression scale or independent sample.

## Try it and explain it

Run `cargo +1.90.0 test --locked --manifest-path 03_learning/rust/lab/Cargo.toml foundations`. Predict the answers before running: why is `20.0/10.0` different from `20/10` as types? Why is the independent unit six people, not twelve tissue specimens? Change only a local practice copy of the synthetic values and predict the new log2 difference.

**Checkpoint:** You can explain `fn main`, `let`, `mut`, the basic types, `Result` and an `if` expression.

[Next: collections and control →](02_collections_and_control.md)
