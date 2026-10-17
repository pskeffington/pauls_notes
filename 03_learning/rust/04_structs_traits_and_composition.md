# 4. Object-oriented Rust: structs, methods, traits and composition

[← Ownership](03_ownership_and_borrowing.md) · [Course contents](README.md) · [Next: Cargo, testing and tooling](05_cargo_testing_and_quality.md) · [Rust Book: OOP characteristics](https://doc.rust-lang.org/stable/book/ch18-01-what-is-oo.html)

Rust supports **objects that combine data and behavior, information hiding, and polymorphism**. It does *not* support conventional class inheritance. Instead, Rust developers often use **structs** for data, **methods** for behavior, **enums** for defined alternatives, **traits** for shared capabilities, and **composition** for combining components.

## 1. A struct names the data

A research row with two unnamed values is easy to misinterpret. Use a struct to name the fields:

~~~rust
#[derive(Debug)]
struct TeachingMeasurement {
    specimen_label: String,
    value: f64,
}

let sample = TeachingMeasurement {
    specimen_label: String::from("DemoTumor"),
    value: 20.0,
};
assert_eq!(sample.value, 20.0);
~~~

`#[derive(Debug)]` asks the compiler to implement debug printing. Other common derives include `Clone`, `Copy`, `PartialEq`, `Eq` and `Hash` where appropriate. Not all types can safely or meaningfully derive all traits; `f64` does **not** implement `Eq` because NaN breaks normal equality assumptions.

## 2. An `impl` adds constructor and methods

~~~rust
struct PositiveMeasurement {
    value: f64,       // private outside its module
}

impl PositiveMeasurement {
    fn new(value: f64) -> Result<Self, &'static str> {
        if !value.is_finite() || value <= 0.0 {
            return Err("Expected positive, finite teaching units");
        }
        Ok(Self { value })
    }

    fn value(&self) -> f64 {
        self.value
    }
}
~~~

`Self` means the current type. `new` is an **associated function** (like a constructor convention), not a special Rust keyword. `&self` borrows the object to read it; `&mut self` would allow modifying it; `self` consumes it. Private fields plus a checked `new` function provide **encapsulation**: callers cannot create invalid instances by directly supplying unvalidated fields from another module.

This is a *code-level* invariant; it does not establish that the laboratory scale or tissue label is correct.

## 3. Enums make categories explicit

~~~rust
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Tissue {
    Comparator,
    Tumor,
}
~~~

Use `Tissue::Tumor` instead of guessing whether `0` or `1` means tumor. `Option<f64>` and `Result<T,E>` are also enums. `match` makes handling alternatives explicit. An enum of two teaching tissues does not automatically describe all clinical biospecimen categories; a real protocol must define its own allowed labels.

## 4. Composition instead of subclass inheritance

The working lab combines two `Specimen` objects into a `Pair`:

~~~rust
pub struct Pair {
    comparator: Specimen,
    tumor: Specimen,
}

impl Pair {
    pub fn new(comparator: Specimen, tumor: Specimen) -> Result<Self, &'static str> {
        // A checked constructor ensures the same person and opposite tissue types.
        // See the complete, compiling source in lab/src/objects.rs.
        todo!()
    }
}
~~~

**The constructor above is a design sketch only; it will panic if called.** Use the [fully implemented source](lab/src/objects.rs) to learn and run tests. The crucial design idea is *has-a*: a pair **has two specimens**; it is not a special subclass of `Specimen`.

Composition is particularly valuable for the breast-cancer book, where a person may contribute multiple specimens, one specimen may yield multiple assay files, and assays measure features. Those are **relationships among different entities**, not inherited class hierarchies.

## 5. Traits supply common behavior

Two otherwise different types can implement the same interface:

~~~rust
trait Describe {
    fn summary(&self) -> String;
}
~~~

The [lab](lab/src/objects.rs) implements `Describe` on both a `Specimen` and a `GeneAnnotation`. A `Specimen` is a fictional observation; `GeneAnnotation` is a biological reference record such as ESR1's hormone-related context, **not a fitted expression measurement**. Their summaries deliberately do not expose a person identifier.

**Two forms of polymorphism:**
- `fn describe_one<T: Describe>(item: &T)` is generic **static dispatch**; a type is known when compiled.
- `fn describe_many(items: &[&dyn Describe])` accepts **trait objects** with runtime dispatch, allowing unlike types in one slice.

A trait is not a superclass. Shared behavior does not imply shared fields or biological equivalence.

## 6. Generics, method calls, and visibility

- `impl Trait` accepts some concrete type meeting an interface; `dyn Trait` uses a trait object.
- `pub` exports an item from its module; fields remain private unless marked public.
- `use` imports named items; `mod` declares a module; `crate::` names the current crate root.
- Borrow with `&self` rather than cloning an entire dataset just to read a measurement.
- A trait default method is behavior reuse, not inheritance of stored state.

The lab's [`objects.rs`](lab/src/objects.rs) provides the **complete source**, including tests for the constructors, missing values, mixed-type trait summaries, duplicate/invalid identity and a positive log2 ratio.

## Exercise: which is an object and which is a record?

Read [Chapter 2 of the book](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-2-understanding-the-breast-cancer-dataset) and sketch these types: `Person`, `Specimen`, `Assay`, `GeneAnnotation`. Which relationships are composition or linked references? Which could reasonably share a `Describe` trait? Which identifiers **must not** become model features? Then run:

~~~bash
cargo +1.90.0 test --locked --manifest-path 03_learning/rust/lab/Cargo.toml objects
~~~

**Checkpoint:** You can explain `struct`, `impl`, private fields, checked constructors, `enum`, a trait, composition and the difference between static and runtime dispatch. You can state clearly why **Rust does not use Java-style class inheritance**.

[Next: Cargo and testing →](05_cargo_testing_and_quality.md)
