# 2. Collections, control flow, and missing values

[← First steps](01_first_steps.md) · [Course contents](README.md) · [Next: ownership and borrowing](03_ownership_and_borrowing.md)

A biomedical analysis usually handles more than one number. Before modeling, learn how Rust stores groups of values and how a function responds to missing or invalid input. The numbers below are **invented Chapter 11 teaching measurements**, not sequence counts.

## Arrays, tuples, vectors and slices

~~~rust
let fixed: [f64; 3] = [10.0, 20.0, 30.0];       // three values, fixed length
let pair: (f64, f64) = (10.0, 20.0);             // two differently named positions
let mut measurements: Vec<f64> = vec![10.0, 20.0];
measurements.push(30.0);                        // growable
let view: &[f64] = &measurements;                // read-only borrowed slice
assert_eq!(fixed.len(), 3);
assert_eq!(pair.1, 20.0);
assert_eq!(view.len(), 3);
assert_eq!(view.get(100), None);                 // no panic
~~~

Use tuples for a few related values, arrays for a known fixed length, vectors for a changing count, and slices to accept a view of data without copying it. As you move into research, give the *people*, *specimens*, and *measurements* **named types**, not anonymous tuple positions.

## A string is not simply a vector of characters

`String` owns UTF-8 bytes. `&str` borrows a range of text. `.len()` reports **bytes**, whereas `.chars().count()` counts Unicode scalar values. Do not index a Rust string with an integer. Clinical labels should not be parsed by assuming all characters are ASCII; the later **synthetic gene-symbol fixture** intentionally has an ASCII-only rule.

~~~rust
let label = String::from("ESR1");
let borrowed: &str = &label;
assert_eq!(borrowed.chars().count(), 4);
~~~

## Loops, iterators and `match`

~~~rust
let changes = [1.0_f64, 2.0, 0.0, -1.0, 1.0, 0.0];
let mut positive = 0;
for change in changes {
    if change > 0.0 {
        positive += 1;
    }
}
assert_eq!(positive, 3);

let interpretation = match positive {
    0 => "none positive",
    1 => "one positive",
    _ => "several positive",
};
assert_eq!(interpretation, "several positive");
~~~

A `for` loop visits every item; `if` selects actions; `match` handles an enum or patterns exhaustively. Later, an iterator may express the same operation as `changes.iter().filter(|&&x| x > 0.0).count()`. Use the clearest approach, not the shortest.

## `Option` and `Result` are not interchangeable

- `Option<T>` is `Some(value)` or `None`. An unavailable measurement can legitimately be missing.
- `Result<T,E>` is `Ok(value)` or `Err(problem)`. A malformed specimen identifier, nonfinite value or invalid partition should be rejected.
- `None` does not mean zero. `NaN` is a floating-point value, **not** an idiomatic marker for missingness when `Option<f64>` is available.

~~~rust
fn read_value(value: Option<f64>) -> Result<Option<f64>, &'static str> {
    match value {
        Some(v) if !v.is_finite() || v <= 0.0 => Err("Invalid measurement"),
        other => Ok(other),
    }
}
assert_eq!(read_value(None), Ok(None));
assert_eq!(read_value(Some(10.0)), Ok(Some(10.0)));
assert!(read_value(Some(f64::NAN)).is_err());
~~~

The `?` operator propagates an error to the caller. Avoid `.unwrap()` on uncertain external records; in tests it is sometimes useful to fail fast. You will learn how a validated `Specimen` struct stores `Option<f64>` in Lesson 4.

## Sets, maps and duplicates

For grouped samples, a `BTreeMap` maps a key to a value; a `BTreeSet` tracks unique keys in a defined order. `HashMap`/`HashSet` are also useful but do not provide a guaranteed iteration order. The [research engineering lab](lab/src/engineering.rs) uses trees to verify that each **fictional person** has one comparator and one tumor specimen before splitting.

## Practice

Read [`foundations.rs`](lab/src/foundations.rs) and predict the test for `positive_count`. Change a local practice vector to include `f64::INFINITY`: should the function silently skip it, treat it as missing, or report `Err`? The lab intentionally reports an error because nonfinite values violate this arithmetic contract.

**Checkpoint:** You can choose between `Vec` and `&[T]`, use `for`/`if`/`match`, and explain missingness (`None`) versus bad data (`Err`).

[Next: ownership and borrowing →](03_ownership_and_borrowing.md)
