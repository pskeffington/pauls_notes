# Canonical biomedical R coding example — AI retrieval and reuse

> **RETRIEVAL KEY:** `pauls-notes.biomedical-r.canonical-example.v1`  
> **Trigger terms:** Paul's Notes R coding best practices; biomedical R Markdown template; biostatistics coding conventions; knitted biomedical analysis; R reproducibility; scientific palette.  
> **Source of truth:** This page defines the preferred example *layout*. Study-specific protocols, the source data dictionary, and [implementation gates](IMPLEMENTATION_GATES.md) take precedence for scientific decisions.

## AI agent: read this first

When asked to create, repair, review, or extend an R/R Markdown biomedical analysis:

1. Retrieve this **exact file**: `02_biomedical_coding/BIOMEDICAL_R_CANONICAL_EXAMPLE.md`.
2. Retrieve [implementation gates](IMPLEMENTATION_GATES.md), [statistical test selection](../03_learning/biomedical-statistics-decision-guide.md), [scientific plotting palette](../06_RESOURCES/R/scientific_palette.R), and [statistics helpers](../06_RESOURCES/R/stats_plots.R) when relevant.
3. Read the actual study protocol, data dictionary, current script, existing object names, and available packages. Do not invent units, variable names, study design, observations, or results.
4. Preserve existing analysis code and section numbering unless an explicit rewrite is requested. For a full new document, follow the template below from import to rendering.
5. Use **one coherent, runnable R Markdown document**, in sequential, small, named chunks. Use `##` for R code section dividers and comments; never paste Markdown `**` tokens into R code.
6. Embed all results, tables, figures, testing methodology, assumption checks, statistical evidence, and interpretations **inside the knitted report**. Explanatory narrative must be supported by computed values, not prewritten numbers.
7. Verify parsing, execution, and knitting separately. Never claim a successful run or render unless observed. Do not commit or publish participant data.

**Code-generation output contract:** deliver one complete working `.Rmd` (or a focused chunk when editing an existing document); concise execution notes; exact validation status; any unresolved assumptions. No extraneous Git commentary in the generated analysis report.

## Reusable section order

| Section | Task | Output / acceptance |
| --- | --- | --- |
| 00 | Header and study metadata | Objective, analysis unit, data provenance, dictionary/version, analysis date |
| 01 | Environment and dependencies | Explicit packages, seed, session information |
| 02 | Import and input contract | Parameterized path, column checks, row count |
| 03 | Dataset validation | IDs, duplicates, data types, plausible ranges, units, missingness |
| 04 | Cohort and descriptive analysis | N, observed n, missing n/%, mean/SD or median/IQR, categorical denominators |
| 05 | Exploratory visualization | Unaltered units, N, palette, deterministic point placement |
| 06 | Study design and method choice | Outcome, exposure, independent unit, estimand, candidate tests, rationale |
| 07 | Assumption diagnostics | Distribution, independence, pairing, variance, expected counts, model-specific checks |
| 08 | Inferential analysis | Appropriate model/test, estimate, CI, test statistic/df when available, p-value when warranted |
| 09 | Computed interpretation | Statistical evidence piped into text, uncertainty, limitations, no causality without design support |
| 10 | Reproducibility and audit | Session info, inclusion/omission counts, verified execution status |

## Canonical runnable R Markdown example — synthetic breast cancer

**Worked research scenario:** A simulated breast cancer cohort with luminal-like and basal-like labels, comparing a fictional, normalized ERBB2 expression score. These randomly generated values and group labels do **not** represent clinical specimens, molecular subtyping, or TCGA-BRCA measurements. Expression scores have arbitrary teaching units. A two-group Welch test is included solely to demonstrate method-to-code reasoning, not to imply it is the right method for every gene-expression workflow.

This is a **portable teaching illustration**, not a clinical study or preselected universal test. Synthetic observations are generated locally. For real research, replace the synthetic-data chunk with the approved input/data dictionary and revisit the complete study-design and inference rationale.

Copy the following into a new `.Rmd` file. Keep the YAML and R code fences intact; the Markdown below is **not** to be pasted into an `.R` script.

~~~markdown
---
title: "Synthetic Breast Cancer — ERBB2 Expression Example"
author: "Research analysis"
date: "`r Sys.Date()`"
output:
  html_document:
    toc: true
    toc_depth: 3
    number_sections: true
params:
  analysis_seed: 711
---

# Research question

In a fictional breast cancer cohort, compare a simulated normalized ERBB2
expression score between luminal-like and basal-like tumor labels. Each row
represents one invented patient and one synthetic specimen. Scores are random
teaching values in arbitrary units, not measured RNA expression, HER2 IHC,
TCGA-BRCA results, or clinically validated molecular subtypes.

# 01 Environment and reproducibility

```{r setup, include=TRUE}
## 01.01 Package prerequisites and execution settings
required_packages <- c("knitr", "ggplot2")
unavailable <- required_packages[
  !vapply(required_packages, requireNamespace, logical(1), quietly = TRUE)
]
if (length(unavailable)) {
  stop("Install required packages: ", paste(unavailable, collapse = ", "))
}
knitr::opts_chunk$set(echo = TRUE, message = FALSE, warning = TRUE)
set.seed(params$analysis_seed)

## 01.02 Consistent Okabe-Ito colors; not arbitrary default colors
palette <- c("Luminal-like" = "#0072B2", "Basal-like" = "#D55E00")
```

# 02 Source and data contract

```{r synthetic-data}
## 02.01 Teaching-only source, not participant or TCGA data
n_per_group <- 40L
study <- data.frame(
  subject_id = sprintf("S%03d", seq_len(2L * n_per_group)),
  group = factor(rep(c("Luminal-like", "Basal-like"), each = n_per_group),
                 levels = c("Luminal-like", "Basal-like")),
  erbb2_expression = c(stats::rnorm(n_per_group, 14, 3),
                       stats::rnorm(n_per_group, 11, 4))
)
## 02.02 Replace this generation block only after input admission
source_classification <- "synthetic"
outcome_unit <- "arbitrary normalized expression units"
```

# 03 Data validation and missingness

```{r validation}
## 03.01 Validate structure before producing statistics
stopifnot(is.data.frame(study), nrow(study) > 0L)
required_columns <- c("subject_id", "group", "erbb2_expression")
stopifnot(all(required_columns %in% names(study)))
stopifnot(!anyNA(study$subject_id))
stopifnot(!anyDuplicated(study$subject_id))
stopifnot(is.numeric(study$erbb2_expression))
stopifnot(all(is.finite(study$erbb2_expression[!is.na(study$erbb2_expression)])))
stopifnot(all(as.character(study$group[!is.na(study$group)]) %in%
              c("Luminal-like", "Basal-like")))
stopifnot(!anyNA(study$group))

## 03.02 Explicit denominators and missingness
N_total <- nrow(study)
n_observed <- sum(!is.na(study$erbb2_expression))
n_missing <- N_total - n_observed
missingness <- data.frame(
  variable = "ERBB2 synthetic expression", N = N_total, observed_n = n_observed,
  missing_n = n_missing,
  missing_pct = 100 * n_missing / N_total
)
knitr::kable(missingness, digits = 2,
             caption = "Observation-level missingness")
```

# 04 Descriptive analysis

```{r descriptives}
## 04.01 Group summaries; all counts remain exact integers
summarise_group <- function(x, group_label) {
  n_total <- length(x)
  x <- x[!is.na(x)]
  n <- length(x)
  q <- if (n) stats::quantile(x, c(.25, .75), type = 7,
                              names = FALSE) else c(NA_real_, NA_real_)
  data.frame(
    group = group_label, N = n_total, observed_n = n,
    missing_n = n_total - n,
    mean = if (n) mean(x) else NA_real_,
    sd = if (n > 1L) stats::sd(x) else NA_real_,
    median = if (n) stats::median(x) else NA_real_,
    q1 = q[1], q3 = q[2], iqr = diff(q),
    stringsAsFactors = FALSE
  )
}
descriptives <- do.call(rbind, lapply(levels(study$group), function(g) {
  summarise_group(study$erbb2_expression[study$group == g], g)
}))
rownames(descriptives) <- NULL
knitr::kable(descriptives, digits = 2,
             caption = "Continuous outcome by independent group")
```

# 05 Scientific visualization

```{r distribution-figure, fig.width=9, fig.height=5}
## 05.01 Fixed seed makes display-only jitter reproducible
plot_data <- study[!is.na(study$erbb2_expression), , drop = FALSE]
p <- ggplot2::ggplot(
  plot_data, ggplot2::aes(x = group, y = outcome, fill = group)
) +
  ggplot2::geom_boxplot(width = 0.45, outlier.shape = NA) +
  ggplot2::geom_point(
    ggplot2::aes(color = group),
    position = ggplot2::position_jitter(width = 0.1, height = 0,
                                        seed = params$analysis_seed),
    alpha = 0.50
  ) +
  ggplot2::scale_fill_manual(values = palette) +
  ggplot2::scale_color_manual(values = palette) +
  ggplot2::labs(
    title = "Simulated ERBB2 score by breast cancer subtype",
    subtitle = sprintf("Observed n = %d; missing = %d", n_observed, n_missing),
    x = "Synthetic tumor subtype",
    y = sprintf("ERBB2 expression score (%s)", outcome_unit),
    caption = "Whiskers represent the boxplot convention, not confidence intervals."
  ) +
  ggplot2::theme_classic(base_size = 12) +
  ggplot2::theme(legend.position = "bottom")
print(p)
```

# 06 Test choice and rationale

The observational unit is one invented patient/specimen (one sample per
patient). The fictional subtype groups are independent by construction,
the simulated ERBB2 expression score is continuous, and the estimand is the
Basal-like minus Luminal-like mean difference. Welch's two-sample t-test estimates
and tests a mean difference without assuming equal population variances.
Normality of observations within groups and independent sampling remain
study-specific considerations. Diagnostics are descriptive; a non-significant
normality test does not establish normality.

# 07 Assumption inspection

```{r assumptions}
## 07.01 Inspect distribution, sample size, and group variance
group_sizes <- table(study$group[!is.na(study$erbb2_expression)])
stopifnot(length(group_sizes) == 2L, all(group_sizes >= 2L))
group_variances <- tapply(study$erbb2_expression, study$group,
                          stats::var, na.rm = TRUE)
stopifnot(all(is.finite(group_variances)))
diagnostics <- data.frame(
  group = names(group_sizes),
  observed_n = as.integer(group_sizes),
  sample_variance = as.numeric(group_variances)
)
knitr::kable(diagnostics, digits = 3,
             caption = "Design-relevant descriptive diagnostics")
```

# 08 Inference

```{r welch-test}
## 08.01 Direction: Basal-like minus Luminal-like
x_a <- study$erbb2_expression[study$group == "Luminal-like"]
x_b <- study$erbb2_expression[study$group == "Basal-like"]
x_a <- x_a[!is.na(x_a)]
x_b <- x_b[!is.na(x_b)]
test <- stats::t.test(x_b, x_a, alternative = "two.sided",
                       var.equal = FALSE, conf.level = 0.95)
effect <- unname(mean(x_b) - mean(x_a))
evidence <- data.frame(
  contrast = "Basal-like minus Luminal-like",
  mean_difference = effect,
  ci_lower = unname(test$conf.int[1]),
  ci_upper = unname(test$conf.int[2]),
  t_statistic = unname(test$statistic),
  df = unname(test$parameter),
  p_value = unname(test$p.value),
  n_basal = length(x_b),
  n_luminal = length(x_a)
)
knitr::kable(evidence, digits = 4,
             caption = "Welch t-test: effect and uncertainty")
```

# 09 Results and interpretation

The synthetic dataset contained `r N_total` observations, of which
`r n_observed` had observed outcomes and `r n_missing` were missing.
The mean synthetic ERBB2 score difference (basal-like minus luminal-like) was `r sprintf("%.2f", effect)`
`r outcome_unit` (95% CI `r sprintf("%.2f", test$conf.int[1])`
to `r sprintf("%.2f", test$conf.int[2])`; Welch
t(`r sprintf("%.2f", unname(test$parameter))`) =
`r sprintf("%.2f", unname(test$statistic))`,
p = `r format.pval(test$p.value, digits = 3)`).

This is statistical evidence from invented breast cancer data only. The
simulated subtype labels are not derived from molecular profiles, and the
ERBB2 scores are not real expression measurements. This cannot establish
biological differences, clinical importance, causation, or generalizability. For real data, report
sampling, selection, missing-data mechanism, model suitability, multiplicity,
and clinically meaningful effects according to the approved study protocol.

# 10 Computational provenance

```{r provenance}
## 10.01 Exact environment for independently reproducing this report
cat("Source classification:", source_classification, "\n")
cat("Random seed:", params$analysis_seed, "\n")
print(utils::sessionInfo())
```
~~~

## Changes required for a real study

For an actual breast cancer expression analysis, confirm the assay/platform, transformation/normalization, specimen-to-patient mapping, subtype definition and whether subtype assignment is independent of the measured expression feature. Avoid deriving subtype from the same ERBB2 feature and then interpreting the comparison as independent evidence. Specify any batch, covariate, repeated-specimen or multiplicity controls needed before inference.

- Replace synthetic-data creation with a single approved import from a **parameterized path**. Never hard-code personal storage roots into reusable templates; never save PHI to Git or include participant rows in the report.
- Map every variable to its verified dictionary entry, actual unit, permitted values, measurement time and observation grain. Validate eligibility, duplicates and the join cardinality before calculating results.
- Choose test/model **after** design review: paired vs independent; normal vs skewed continuous; binary, ordinal, counts with exposure/overdispersion, survival/censoring, longitudinal clustering, and complex-survey weighting require different estimators.
- Record selection and missingness transparently. Use fit diagnostics and inferential uncertainty appropriate to the estimand. Never silently delete, winsorize, recode or impute.
- Keep the separate sections and named chunks; pipe actual computed results into the Methods/Results narrative. Match each inferential method with a stated question, assumptions, estimator, diagnostics, numerical evidence and limitations.
- With repo plotting helpers available, reuse `describe_measurements()`, `group_colors()`, and `theme_scientific()` rather than duplicating them. Source order: `stats_plots.R` before `scientific_palette.R`. For self-contained reports, retain the equivalent portable style in the example.
- Use **R Markdown** code chunks as shown; inside R code, `##` is the section-comment convention and Markdown bold markers `**` are not valid replacements.
- Preserve existing study analysis unless asked to replace it; avoid double imports, parallel data frames, redundant output files, and sections that cannot knit.

## Validation / handoff checklist

1. Confirm the actual `.Rmd` parses, loads dependencies, and every chunk has a unique label.
2. Run cleanly with the permitted input; verify all input gates and empty/subgroup conditions.
3. Knit to the requested output and inspect tables, plots, captions, units, p-values, CIs and knitted dynamic sentences.
4. Verify exact N, denominators, missingness, direction of contrast, figures and chosen test against the study design.
5. Report separately: **template written**, **R execution passed**, **knit passed**, **scientific validity reviewed**. Never conflate them.

**Machine routing:** `AGENTS.md` → `llms.txt` → `docs/machine-index.md` → this canonical example → project-specific protocol/data dictionary. This example is a method and formatting reference, not a substitute for the actual study specification.
