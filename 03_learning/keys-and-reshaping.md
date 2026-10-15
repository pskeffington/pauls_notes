# Keys, joins and reshaping

[Learning sections](README.md) · [Next: missingness](missingness-and-comparisons.md)

## State what uniquely identifies a row

The registry has one row per `person_id`. The visit table needs the compound key `person_id` plus `visit`. A join is a statement about relationships between observations; it should not be selected merely because the resulting table looks convenient.

| Join | Retained keys | Check before interpretation |
| --- | --- | --- |
| Left | All left-side rows | Right-side key uniqueness and missing matches |
| Inner | Keys matched on both sides | Which left-side observations were excluded |
| Full | Keys appearing on either side | Which fields are unavailable after matching |
| Many-to-many | All matching combinations | Whether the resulting observation unit is intended |

For a many-to-one linkage, every left observation may match one right record. Duplicating a registry key can multiply visit rows and exaggerate denominators. A plausible mean does not establish a safe join.

## Preserve order and count

```r
source("03_learning/examples/research_case.R")
case <- make_case()
require_key(case$registry, "person_id")
require_key(case$visits, c("person_id", "visit"))
joined <- attach_registry(case$visits, case$registry[8:1, ])
stopifnot(nrow(joined) == 16L)
stopifnot(identical(joined$person_id, case$visits$person_id))
```

`attach_registry()` first checks keys, then uses `match()` to align registry attributes to visit rows. It rejects unknown people and overlapping non-key column names. It retains all sixteen visit rows; changing the registry's row order has no effect on linkage.

Before using this pattern on study inputs, document identifier namespaces, leading-zero handling, permitted missing keys and expected cardinality. Here all keys are strings and unknown matches are errors. An actual study may permit unmatched records, but that requires an explicit exclusion or missingness policy.

## Wide and long preserve the same observations

```r
wide <- to_wide(case$visits)
stopifnot(nrow(wide) == 8L, sum(is.na(wide)) == 2L)
stopifnot(identical(wide$person_id, sprintf("S%02d", seq_len(8))))
```

There are sixteen person-visits in long form and eight people in wide form. The two unavailable values remain unavailable. A pivot does not create additional people, solve missingness or establish pairing; the key and visit definitions do that.

`to_wide()` requires both visit labels and exactly two visit rows per person. If a study stores absent visits as absent rows, first build its expected visit grid and distinguish an absent record from an observed record with a missing measurement.

## Optional tidyverse implementation

With `dplyr` and `tidyr` installed, the same idea can be expressed through named operations. This optional example is separate from the base-R deployment:

```r
if (requireNamespace("dplyr", quietly = TRUE) && requireNamespace("tidyr", quietly = TRUE) &&
    utils::packageVersion("dplyr") >= "1.1.0") {
  linked <- dplyr::left_join(case$visits, case$registry,
    by = "person_id", relationship = "many-to-one")
  stopifnot(nrow(linked) == 16L)
  pivoted <- tidyr::pivot_wider(linked[c("person_id", "visit", "marker_au")],
    id_cols = "person_id", names_from = "visit", values_from = "marker_au")
  stopifnot(nrow(pivoted) == 8L)
}
```

Check unsupported and unmatched identifiers separately; the relationship argument constrains multiplicity but does not implement every study-specific missing-match rule. Typical pipelines use `filter()` for rows, `mutate()` for derived columns, `group_by()` with `summarise()` for group summaries, and `arrange()` for order. State the observation unit after each operation.

## Transfer exercise

Duplicate one registry row and catch the resulting error. Next, insert an unknown person in one visit. Explain why each case needs a different correction and why deleting arbitrary rows is not a defensible general fix.

References: [Join relationship contracts](https://dplyr.tidyverse.org/reference/mutate-joins.html), [long-form pivots](https://tidyr.tidyverse.org/reference/pivot_longer.html), [wide-form pivots](https://tidyr.tidyverse.org/reference/pivot_wider.html).
