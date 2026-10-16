# Objects, types and scientific meaning

[Computing subjects](README.md) · [Related: keys and reshaping](keys-and-reshaping.md)

## Begin with the observation unit

A registry row represents a person. A visit row represents one person's observation at one occasion. A feature matrix contains measurements: rows are demonstration features and columns are people. Converting a table to a matrix does not change what was measured, but it can change storage types and discard the distinction between identifiers and values.

The case uses synthetic people and arbitrary measurement units. A questionnaire answer is a recorded response; it is not a diagnosis or a substitute for an assay.

## Build and inspect the objects

Run examples from the repository root. `source()` loads functions; `make_case()` builds fresh in-memory practice inputs without writing files.

```r
source("03_learning/examples/research_case.R")
case <- make_case()
str(case$registry)
stopifnot(is.factor(case$registry$arm), is.matrix(case$assay))
stopifnot(identical(colnames(case$assay), case$registry$person_id))
stopifnot(inherits(case$visits$collected_on, "Date"))
```

A list can store a mixed-type registry and a numeric matrix together. A data frame keeps a type per column; an atomic matrix uses one storage type throughout. Adding a text identifier column to a numeric matrix can coerce the whole result to character. Keep identifiers as row/column names or in a separate checked table.

## Arithmetic, indexing and coercion

```r
x <- c(first = 2, second = 4, third = NA_real_)
stopifnot(identical(unname(x * 3), c(6, 12, NA_real_)))
keep <- is.finite(x) & x >= 3
stopifnot(identical(names(x)[keep], "second"))
stopifnot(is.character(c(2, "unknown")))
stopifnot(is.na(NA_real_ * 0))
```

Vector arithmetic is elementwise. Recycling can repeat a shorter vector; some incompatible lengths warn while exact multiples can recycle silently. Confirm lengths before comparing measurements. Use `seq_along(x)` for positions, including empty vectors, and `drop = FALSE` when a subset must remain a matrix or data frame.

`NA` marks an unavailable value, `NaN` an undefined numerical result, `Inf` an infinite result, and `NULL` an absent object component. `is.na()` also detects `NaN`; `is.finite()` rejects all three nonfinite numerical states. Do not replace unavailable measurements with zero to make arithmetic convenient.

## Categories and dates

A factor stores category codes plus labels. `as.numeric(factor_object)` returns codes, not measured values. Declare the intended levels and report unsupported inputs before recoding. Parse calendar values with `as.Date()` before subtracting them; a day interval is not a character-string difference.

```r
f <- factor(c("high", "low"), levels = c("low", "high"))
stopifnot(identical(as.integer(f), c(2L, 1L)))
stopifnot(as.numeric(as.Date("2030-01-15") - as.Date("2030-01-01")) == 14)
```

## Functions and repeated work

A function should state its accepted type, units, missing-value policy and return shape. The case's `require_key()` rejects empty, missing or duplicate keys. `lapply()` constructs one result per visit; the feature scaler uses a `for` loop because it records a different status for each feature. A loop is not intrinsically less scientific than an apply function: inspect the contract and result.

```r
positions <- seq_len(3)
squared <- vapply(positions, function(i) i^2, numeric(1))
i <- 1L
while (i <= length(positions)) {
  stopifnot(squared[i] == positions[i]^2)
  i <- i + 1L
}
```

Use `if` for one checked logical decision; use vectorized predicates for row selection. The case's `assert()` rejects missing or nonscalar decisions rather than letting an unavailable comparison choose a branch.

CSV is useful for rectangular interchange but does not preserve every R attribute or object class. `saveRDS()` and `readRDS()` preserve one R object, including its nested structure; read only trusted serialized inputs. Save code rather than relying on a restored interactive workspace.

## Check the foundations

Use [learning checks LC01–LC11](mastery-checks.md#r-operations-and-data-meaning) to predict arithmetic and extraction behavior, test safe vector lengths, compare finite and missing states, clean categories and verify a CSV/RDS round trip. The runnable cases include recovery from deliberately invalid inputs.

## Transfer exercise

Reorder the registry without reordering the matrix. Predict which check should fail. Then explicitly align matrix columns to registry IDs with `match()` and verify the identities again. Explain why equal dimensions alone would not detect the original mismatch.

Reference: [R language and data structures manual](https://cran.r-project.org/doc/manuals/r-release/R-intro.html), especially vectors, missing values, lists, matrices, functions and data frames.
