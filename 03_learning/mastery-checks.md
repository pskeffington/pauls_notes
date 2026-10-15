# Learning checks and completion evidence

[Learning sections](README.md)

Use the checks to test a skill on new inputs. A passing program checks computational behavior; explain the observation unit, units, assumptions and limitation yourself before marking a learning task complete.

## Execute the checks

The main analysis needs base R. The extended R checks additionally require `dplyr` 1.1 or later, `tidyr`, `ggplot2` and `survey`. These packages are installed in the continuous-integration job. Run from the repository root:

```bash
Rscript --vanilla 03_learning/tests/test_research_case.R
Rscript --vanilla 03_learning/tests/test_mastery.R
Rscript --vanilla 03_learning/tests/check_learning_pages.R
bash 03_learning/tests/test_shell_practice.sh
Rscript --vanilla 03_learning/tests/test_resource_contracts.R
```

The shell suite runs its R bridge checks when Rscript is available. Continuous integration requires R and executes both. Tests create and clean their own temporary directories; no study inputs are needed.

## R operations and data meaning

The `LC` labels identify executable groups in [test_mastery.R](tests/test_mastery.R).

| Check | Demonstrate | Expected evidence |
| --- | --- | --- |
| LC01 | Predict arithmetic precedence, integer division and remainder | Distinct grouped and ungrouped results |
| LC02 | Distinguish intended scalar adjustment from mismatched vectors | Wrong-length offsets fail |
| LC03 | Separate unavailable, undefined and infinite values | Finite count and unknown-preserving derived flags |
| LC04 | Extract vectors, list elements and dimension-preserving subsets | Container and shape checks pass |
| LC05 | Clean labels, retain factor levels and subtract dates | Unsupported category fails; ten elapsed days |
| LC06 | Explain row/column summaries and matrix multiplication | Known row means and unchanged identity product |
| LC07 | Trace decisions, loops, lapply and typed vapply | Repeated results agree; nonscalar and missing decisions fail |
| LC08 | Round-trip CSV and RDS | String IDs remain intact; RDS retains factor metadata |
| LC09 | Separate people, visits and analysis samples | Counts of 8, 16, 14, 6 and 7 for the defined units |
| LC10 | Normalize categories before grouped counts | Two alpha and one beta label |
| LC11 | Keep reported yes/no, refusal, uncertainty and missing distinct | Four labeled states plus missing; unsupported code fails |

## Transform, compare and model

| Check | Demonstrate | Expected evidence |
| --- | --- | --- |
| LC12 | Predict left, inner, full, one-to-many and many-to-one joins | Known counts and unmatched IDs; duplicate relationship fails |
| LC13 | Reverse a wide/long pivot | Same keys, values and missingness after ordering |
| LC14 | Select, filter, mutate, arrange, group and summarize | Six selected people; person counts differ from visit counts |
| LC15 | Use complete pairs for within-person differences | Six pairs; mean change 1.5 invented units |
| LC16 | Execute rank and t procedures on a chosen difference vector | Known rank sum; t statistic matches its formula |
| LC17 | Reproduce normal, uniform and Bernoulli draws | Same seed repeats results; support constraints hold |
| LC18 | Inspect Anscombe's four contrasting datasets | Similar slopes coexist with different point arrangements |
| LC19 | Restrict eligibility to the model's required fields | Seven baseline observations; unrelated missing response retained |
| LC20 | Separate mean confidence from individual prediction | Individual intervals wider under this model |
| LC21 | Inspect diagnostic inputs | Seven residuals and fitted values |
| LC22 | Use a checked plotting function | Eligible/excluded counts; invalid types and unit labels fail |
| LC23 | Export labeled distribution and association displays | Nonempty PDF; histogram, density, ECDF, box and violin displays |
| LC24 | Scale features while preserving missingness | Constant display policy and insufficient-data status are explicit |
| LC25 | Distinguish weighted arithmetic from survey variance estimation | Design-aware estimate and finite standard error |

The [analysis-contract suite](tests/test_research_case.R) adds command-line execution, input-key failures, matrix-order failures, output-file inventory, checksum verification and refusal to overwrite an existing run. The [R page checker](tests/check_learning_pages.R) executes the displayed examples in their local order.

## Shell and batch operations

The [shell practice suite](tests/test_shell_practice.sh) exercises these tasks. The [R bridge suite](tests/test_signal_bridge.R) checks the numeric and batch results.

| Task | Expected evidence |
| --- | --- |
| Locate a disposable workspace; copy, rename and quote paths with spaces | Copied bytes agree; the original input is unchanged |
| Inspect a header, final row and physical line count | Seven physical lines represent six records plus a header |
| Extract, sort and count categories | Three records in each of two panels |
| Explain executable permissions and Bash function arguments | A copied script runs directly after setting its executable bit; a bad function argument returns status 2 |
| Handle grep and pipeline statuses | Match, no-match and execution failure are distinguished |
| Filter the constrained TSV with awk | Header and selected IDs retained, including an unavailable value |
| Select a category with no records | Header-only result, rather than an invented observation |
| Reject malformed fields, duplicate IDs and unsupported categories | Nonzero status and no partially published file |
| Reject existing outputs and input/output aliases | Valid earlier output and source input remain unchanged |
| Parse quoted CSV correctly | A comma inside a quoted label remains inside one field |
| Discover two named batch inputs and check identities | Each has three records; duplicate physical paths fail |
| Apply a minimum observed-count rule | Alpha has 3 records but 2 measurements; minimum 3 withholds its mean |
| Explain a descriptive mean and its denominator | With minimum 2, alpha's mean is 5; beta's mean is 10 from 3 measurements |
| Handle missing measurements and invalid CLI arguments | All-missing means remain unavailable; noninteger minimum fails |
| Verify a completed run and clean generated temporary files | Output inventory and checksums agree; study inputs are untouched |

The minimum-count rule is a teaching example. It is not a disclosure-control guarantee or a clinical reporting standard. The numeric TSV contract excludes quoted fields and embedded separators; general CSV needs a structured parser.

## Explain and repair

These are learner checks, not claims that an automated test can assess understanding.

- [ ] Explain the difference between a participant, a specimen, a feature and an assay measurement. Use [observation units](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-2-understanding-the-breast-cancer-dataset) and [molecular measurements](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-3-how-researchers-measure-genes) to justify two concrete data-contract choices.
- [ ] Start a new R session, locate the working directory, inspect `sessionInfo()` and `packageVersion()`, and use `help()` for a selected function. Explain how a saved script differs from console history and an object workspace.
- [ ] State the denominator, contrast direction and measurement units for every table and figure. Explain why reshaping does not create new people and why complete-case selection can introduce bias.
- [ ] Explain paired versus independent comparisons, rank-test assumptions, ties and zeros, and why a p-value from chosen values is not population evidence.
- [ ] Read the exported residual and normal-quantile plots. Explain what they can reveal and what they cannot establish about confounding, independence or causality.
- [ ] Explain how a row z-score discards absolute magnitude, how unavailable values differ from zero, and how assay rows and sample metadata would map into a feature/sample-aware container such as `SummarizedExperiment`.
- [ ] Relate two method references to an analysis decision and two book passages to a biological interpretation. Record one alternative explanation and one additional measurement that would address it.
- [ ] Introduce a duplicate key or invalid plotting column, predict the failure, repair the input, and rerun the workflow in a fresh directory. Explain the corrected result without reading a prepared answer.

## Documentation for the decisions

[R language semantics](https://cran.r-project.org/doc/manuals/r-release/R-lang.html), [R data import and export](https://cran.r-project.org/doc/manuals/r-release/R-data.html), [join contracts](https://dplyr.tidyverse.org/reference/mutate-joins.html), [tidy pivots](https://tidyr.tidyverse.org/articles/pivot.html), [rank comparisons](https://search.r-project.org/R/refmans/stats/html/wilcox.test.html), [Anscombe's data](https://search.r-project.org/R/refmans/datasets/html/anscombe.html), [assay and sample containers](https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html), and [Bash behavior](https://www.gnu.org/software/bash/manual/).

## Reusable resources and the book

The [resource contract suite](tests/test_resource_contracts.R) verifies summary counts, quartiles, IQR, missingness percentages, single-observation uncertainty, empty inputs, narrative summaries, the book's paired arithmetic and all 24 heatmap table values against the figure source.

Continuous integration also executes all seven retained [R resource suites](../06_RESOURCES/tests/). Their dependencies include ggplot2, plotly, htmlwidgets, pROC, survival and edgeR. These checks exercise the actual retained helper functions, including statistical dispatch, keyed feature metadata, color scales, annotations, paired plots, calibration, uncertainty and interactive exports. They do not convert a software test into a validated scientific finding.
