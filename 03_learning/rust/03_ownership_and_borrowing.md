# 3. Ownership and borrowing without jargon

[← Collections](02_collections_and_control.md) · [Course contents](README.md) · [Next: structs and traits](04_structs_traits_and_composition.md)

Rust does not depend on a garbage collector for most memory management. Instead, the compiler enforces ownership and borrowing rules. Learning these rules helps with efficient software and also makes it easier to see **when a function can modify the study data**.

## A variable owns a value

~~~rust
let first = String::from("ESR1");
let second = first;                // ownership moves
println!("{second}");
// println!("{first}");            // WILL NOT compile: first was moved
~~~

A `String` is an owned, growable value. Moving it avoids an implicit deep copy. Numeric types like `i32` and `f64` ordinarily implement `Copy` and behave differently: assigning them copies a small value. To duplicate owned text intentionally, use `clone()` and document why the extra allocation is justified.

## Borrowing with `&`

~~~rust
fn count_chars(label: &str) -> usize {
    label.chars().count()
}
let gene = String::from("CD8A");
let n = count_chars(&gene);         // borrow, do not move
assert_eq!(n, 4);
assert_eq!(gene, "CD8A");           // still owned here
~~~

The `&` creates an **immutable reference**. The function promises it will read without changing the borrowed value. Prefer parameters like `&str` and `&[T]` when they only need to inspect text or a collection.

## Mutation with `&mut`

~~~rust
fn append_label(labels: &mut Vec<String>, label: &str) {
    labels.push(label.to_owned());
}
let mut names = vec!["ESR1".to_owned()];
append_label(&mut names, "CD8A");
assert_eq!(names.len(), 2);
~~~

A `&mut` borrow provides exclusive access for modification during its use. Rust normally prevents simultaneous conflicting mutable/immutable borrows. You do not need to memorize lifetime syntax yet: first understand that a reference cannot outlive the value it points to.

The lab's [`push_unique_label`](lab/src/ownership.rs) extends this example with validation and a `Result`, so duplicate and malformed teaching labels are not silently accepted.

## `String` versus `&str`, `Vec<T>` versus `&[T]`

| Caller owns | A function usually borrows |
| --- | --- |
| `String` | `&str` |
| `Vec<f64>` | `&[f64]` |
| `Specimen` | `&Specimen` |
| `Vec<Specimen>` | `&[Specimen]` |

If a function needs to *retain* a string or create a new value, it may take ownership or call `to_owned`. If it just validates a feature name, borrow it. This choice reduces unnecessary copying in large data pipelines.

## References and lifetimes: first intuition

~~~rust
fn first_name(names: &[String]) -> Option<&str> {
    names.first().map(String::as_str)
}
~~~

The returned `&str` borrows from `names`; Rust can infer the lifetime relationship here. You may need explicit lifetime annotations for more complicated borrowed relationships, but annotations do **not** extend how long data is alive. A function cannot safely return a reference to its own temporary `String`.

## Scientific meaning of these coding rules

Rust ownership prevents many memory-use errors. It does **not** prevent:
- Transposing a gene matrix and mislabeling the rows.
- Putting one person's two specimens into different evaluation folds.
- Fitting medians or feature selection with held-out measurements.
- Accidentally sharing a pseudonymous GDC sample identifier.
- Mistaking an expression association for evidence of gene mechanism.

Those are **design/validation problems** addressed in Lesson 6. Ownership makes code clearer; scientific correctness still requires domain contracts and tests.

## Exercises

Read [`ownership.rs`](lab/src/ownership.rs). Trace which function **owns** a `String`, which one only **borrows** a `&str`, and which one mutates a `Vec<String>`. Predict why `uppercase_owned(original)` prevents using `original` afterward. Then run `cargo +1.90.0 test --locked --manifest-path 03_learning/rust/lab/Cargo.toml ownership`.

**Checkpoint:** You can explain a move, an immutable borrow, a mutable borrow, and the purpose of cloning without claiming ownership proves scientific validity.

[Next: structs and traits →](04_structs_traits_and_composition.md)
