# Statistical method intake and reusable-code policy

**Scope:** All new statistical tests and inference routines added to Paul's Notes, including methods first used in coursework, demonstrations or research.

## Method admission and deduplication

1. Search `06_RESOURCES/R/`, `03_learning/examples/`, existing tests and method guides before introducing another method. Distinguish tutorial usage from a reusable method with a documented data/argument contract.
2. If the method exists as a reusable tested helper, reuse or improve that helper rather than cloning the implementation.
3. If absent as a reusable helper, introduce a neutral function in `06_RESOURCES/R/` with corresponding synthetic-only tests in `06_RESOURCES/tests/`; document it and link it from `06_RESOURCES/R/README.md`.
4. For each new method family, update the [literature registry](Literature/biostatistics_r_literature_2021_2026.csv), [source-to-method matrix](Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md), [design-first flowchart](BIOMEDICAL_TEST_DECISION_TREE.md), and [method registry](../docs/research-method-map.json) using verified primary references and explicit methodological limits.
5. Add synthetic tests for method routing, evidence paths, invalid designs and consistency between table/figure result objects; register the tests in CI.
6. Use a feature branch and pull request, retaining the existing implementation unchanged unless a defect or clear extension justifies modifying it.

## Input and naming contract

- No study-specific column names, race labels, disease names, institution names, CSV paths, identifiers or real participant records in the shared method implementation.
- Prefer `data`, `outcome`, `group`, `subject_id`, `reference_level`, `comparison_level`, `time`, `event`, `exposure`, `alpha`, `confidence_level`, and context-specific variants; use `snake_case` for functions and variables.
- Pass column names as explicit string parameters; never assume fixed dataset schemas or silently coerce substantive variables.
- Preserve method-specific definitions of contrasts, risk ratios, weights, denominators and units. Name the estimand and reference class explicitly.
- Source a module to define functions only. Do not execute user analysis, import datasets, write artifacts or install packages on load.

## Scientific acceptance gates

- G1: Confirm lawful and authorized use of any inputs; tests should use exclusively invented or appropriately licensed public fixtures.
- G2: Validate schema, types, missingness, unique IDs where applicable, finite values, factor levels and plausible input domain.
- G3: State independence/paired/clustered/survey design requirements, true experimental unit, timing and estimand.
- G5: Document assumptions, test choice, reference direction, uncertainty calculation, p-values, confidence intervals and multiplicity; include edge-case rejection paths.
- G7: Produce graphical results in **ggplot2** from the **same computed result object** used in tables. Use Okabe-Ito colors, exact n/denominators, labeled units and CI explanations. Never display Python approximations as outputs of R code.
- G8: Add deterministic tests and reproducible demonstrations, compatible with `Rscript --vanilla` and CI. Record package requirements and report the distinction between code-executed and reasoning-reviewed work.

## Release checklist

1. Verify numerical calculations against base R reference functions or independently derived fixture expectations.
2. Test swapped contrast/reference labels, shuffled rows, missingness, invalid categories, invalid units and small-sample limits as relevant.
3. Ensure synthetic fixture values and expected outcomes are clearly identified as nonclinical.
4. If a visualization is included, validate the ggplot build and output framing, axes, annotations and CI semantics.
5. Add usage documentation, method-selection rationale and authoritative sources; update the resource index.
6. Open a PR; disclose missing runtime/tooling if local R execution was impossible, and rely on CI before merge.

**Rule:** An instructional script illustrating a test is not automatically a reusable function. Add the smallest generic and validated implementation that is missing; do not bulk-copy coursework outputs into the repository.
