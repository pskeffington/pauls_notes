# Practice workbook: recognize biomedical data and choose a statistical test

**Paul's Notes · Foundational computational statistical biology · 2026-10-22**  
[Data-first guide and flowchart](biomedical-statistics-decision-guide.md) · [Synthetic R lab](examples/statistical_test_lab.R) · [Mastery checks](mastery-checks.md) · [Recent methods literature](../06_RESOURCES/Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md)

## Instructions

This is a **teaching exercise**, not a clinical research protocol. For every question, decide in this order: **outcome data type → predictor/group type → independent unit → independent or paired/repeated → proposed estimate and statistical method → assumptions and interpretation**. No participant datasets are provided or used.

You can write your answers before opening the key. A method name without the observation unit and intended estimate is **incomplete**.

## Part A. Classify the measurement

| Item | Recorded variable | Is it continuous, discrete count, nominal, ordinal, time-to-event or an identifier? |
| --- | --- | --- |
| A1 | Plasma glucose measured in mg/dL | ? |
| A2 | Number of hospital admissions during 1 year | ? |
| A3 | Cancer stage I, II, III or IV | ? |
| A4 | BRCA specimen barcode "ABC-019" | ? |
| A5 | Tumor subtype A, B, C or D (unordered) | ? |
| A6 | Follow-up time in months **and** relapse indicator (yes/no) | ? |
| A7 | Raw sequencing read counts for each gene | ? |
| A8 | A continuous log2-normalized gene expression measurement | ? |

## Part B. Choose a starting method and defend it

| Item | Biomedical question | Design clue |
| --- | --- | --- |
| B1 | Do mean creatinine concentrations differ between two treatment arms? | One person in one arm; continuous result |
| B2 | Does blood pressure change from admission to discharge? | Same person measured twice; continuous |
| B3 | Do mean marker levels differ across four independent diagnostic categories? | Continuous outcome, 4 independent groups |
| B4 | Is binary infection status associated with two exposure groups? | Independent people, modest/sparse 2-by-2 table |
| B5 | Does yes/no screening status change after counseling? | Same people, before and after |
| B6 | Is ordinal toxicity grade associated with treatment group? | Ordered categories, independent arms |
| B7 | Does the **rate** of infections differ by treatment group? | Event counts and unequal person-time |
| B8 | Is time to relapse different by therapy? | Event times include right-censored follow-up |
| B9 | Is age associated with continuous gene-expression level? | Independent people, quantitative variables |
| B10 | Which genes have differential counts between tumor and normal? | Thousands of raw RNA-seq genes; matched specimens per person |
| B11 | Are repeated cell measurements higher in exposed animals? | Many cells per animal, animal is experimental unit |
| B12 | Do weighted population survey outcomes differ by region? | Stratified multistage survey with weights and clusters |

For each item, also state **one common incorrect test** (for example, a row-independent t-test on repeated cells, or a chi-square on a paired binary table) and why it fails.

## Part C. Calculate on invented data in R

All values are invented. The lab runs with **base R** and creates no reports or patient records.

```r
source("03_learning/examples/statistical_test_lab.R")
d <- make_statistical_test_lab()
a <- analyse_statistical_test_lab(d)

# 16 unique people, two independent groups of 8
stopifnot(nrow(d) == 16L, !anyDuplicated(d$person_id))
stopifnot(all(table(d$group) == 8L))

# Arithmetic checks: effect direction matters.
reference_mean <- mean(d$marker_au[d$group == "Reference"])
comparison_mean <- mean(d$marker_au[d$group == "Comparison"])
difference <- comparison_mean - reference_mean
paired_change <- mean(d$after_au - d$before_au)
stopifnot(isTRUE(all.equal(difference, 3.875)),
          isTRUE(all.equal(paired_change, 27 / 16)))

# Numerical checks are not scientific validation.
stopifnot(a$welch$p.value >= 0, a$welch$p.value <= 1,
          a$fisher$p.value >= 0, a$fisher$p.value <= 1)
```

**Write out the answer to these four interpretation prompts:** What is the outcome data type for `marker_au`? Is `diagnosis` categorical even though logistic regression accepts a 0/1 coding? Why are `before_au` and `after_au` paired? Does the difference `+3.875` mean that an intervention is effective? Explain why or why not.

For a stand-alone terminal run and checks:

```bash
Rscript --vanilla 03_learning/examples/statistical_test_lab.R
Rscript --vanilla 03_learning/tests/test_statistical_test_lab.R
```

## Part D. Answer key and boundary conditions

### Data type answers

| Item | Correct classification | Reason |
| --- | --- | --- |
| A1 | Continuous quantitative | Concentration has meaningful magnitude and units |
| A2 | Discrete count | Nonnegative integer number of events; exposure length matters |
| A3 | Ordinal qualitative | Ordered stages, unequal and unverified distances between levels |
| A4 | Identifier | A code is not a measured quantity |
| A5 | Nominal qualitative | Distinct groups, no meaningful mathematical ordering |
| A6 | Censored time-to-event composite | Time and event indicator must stay together |
| A7 | Discrete count, high-dimensional assay | Raw gene read counts; depth/library normalization and count-aware inference |
| A8 | Continuous transformed assay | Assay scale differs from raw counts and requires appropriate methods |

### Test-selection answers

| Item | Starting method | Design check and common trap |
| --- | --- | --- |
| B1 | Welch independent t-test for the mean difference; regression if adjusted | Check person-level independence, outliers and units; equal-variance Student t is not compulsory |
| B2 | Paired t-test on within-person differences or suitable paired robust/rank method | Never use independent two-sample test on same people |
| B3 | ANOVA / Welch ANOVA for means; prespecified multiple comparisons | A single uncorrected series of t-tests inflates false positives |
| B4 | Fisher exact test when appropriate for a small/sparse 2x2 table; chi-square if approximation is suitable | Show cell counts and effect estimate/CI; do not infer causation |
| B5 | McNemar approach for paired binary outcomes | Dependence invalidates independent chi-square standard errors |
| B6 | Proportional-odds / ordinal model if assumptions fit, or justified rank comparison | Treating I/II/III/IV as equally spaced continuous values changes meaning |
| B7 | Poisson rate regression with log(person-time) offset; check dispersion or use alternative count model | Comparing raw counts ignores unequal follow-up exposure |
| B8 | Kaplan–Meier/log-rank for unadjusted descriptive comparison; Cox or another survival model if justified | Ordinary t-tests of observed follow-up time ignore censoring |
| B9 | Scatterplot; Pearson/Spearman association or regression as justified | Rank correlations and linear slope measure different constructs; neither establishes causation |
| B10 | Gene-level DESeq2/edgeR model from **raw** counts with patient blocking, QC and FDR | Thousands of unadjusted paired t-tests on raw counts are inappropriate |
| B11 | Person/animal-aware summary, mixed model or other valid hierarchical analysis | Cells from the same animal are not independent animals |
| B12 | `survey`-design-aware estimation and regression/tests | Unweighted row-level procedures can misstate population and uncertainty |

**Interpretation reminder:** The lab's mean difference of **3.875** invented arbitrary units and paired change of **1.6875** invented arbitrary units are calculations on a deterministic fixture. There is no clinical treatment, effect-size threshold, randomization claim, external validity or eligible real-data admission.

## Part E. Mastery gate

- [ ] Correctly classify all eight measurement types without using storage classes as shortcuts.
- [ ] Distinguish group/predictor roles from the outcome variable in all 12 vignettes.
- [ ] Identify the actual independent unit and whether data are paired, nested, clustered or censored.
- [ ] Explain the selected test's estimand, two assumptions and one plausible alternative.
- [ ] Produce the two synthetic mean arithmetic checks before reading R's p-values.
- [ ] Explain why a p-value is not the probability of the null hypothesis.
- [ ] State a confidence interval interpretation and contrast direction correctly.
- [ ] Run the lab contract test, review failure cases and record an R session/version.

When ready, continue with [missingness and comparisons](missingness-and-comparisons.md), [models and uncertainty](models-and-uncertainty.md), [probability and study design](probability-and-design.md), and the [advanced oncology ML guide](../04_machine_learning/README.md).

**Scope:** No clinical use, no copied third-party patient data and no claim that successful software tests validate published numerical findings. Use a prespecified research design, reviewed data contract and trained analyst for real decisions.
