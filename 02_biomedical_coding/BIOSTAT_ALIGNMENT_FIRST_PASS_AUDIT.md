# Biomedical coding alignment — first implementation pass

**Program:** BC-BIOSTAT-ALIGN-2026 / BR-001 first pass  
**Date:** 2026-11-15  
**Evidence category:** source-to-code comparison and new opt-in helper; **not** comprehensive method certification or a clinical finding.

## Source material actually checked

- the cited textbook author, *Fundamentals of Biostatistics*, **8th edition** (2016), uploaded full PDF; chapter 1 on planning, sampling, order of measurement and data validation (printed pp. 1–4); chapter 2 on descriptive reporting and quantile definitions (printed pp. 5–23); eighth-edition preface on full-precision intermediate calculations (printed p. xiv).
- Exact authority for quantiles: §2.4, printed p. 18, demonstrates `stats::quantile(..., type=2)`, matching the text's sample percentile definition.
- Existing code inspected on main: `06_RESOURCES/R/stats_plots.R` uses `stats::quantile(...,type=7)`, with count/missingness and sample SD; `02_biomedical_coding/BIOMEDICAL_R_CANONICAL_EXAMPLE.md` and full synthetic Rmd use type-7 quantiles. **Both conventions are valid; results can differ on small samples.**
- The sixth-edition TOC is a **different source**, not to be used to assign eighth-edition section/page numbers.

## Disposition matrix

| ID | Inspection | Finding | First-pass action | Status |
| --- | --- | --- | --- | --- |
| A-01 | Source edition | 6e TOC and 8e full text both exist | Maintain edition-specific sources, paths and stable keys | documented |
| A-02 | Quantile method | Biomedical methods 8e explicitly uses type 2; existing helper type 7 | Add opt-in type-2 helper; preserve established type-7 default | code authored; runtime unverified |
| A-03 | Arithmetic precision | Biomedical methods carries intermediate calculations at full precision | Add display-only rounding rule for all methods and Rmd | documentation rule |
| A-04 | Patient/specimen structure | Ch 1 stresses unique IDs and validation before analysis | Reassert G2 uniqueness, missingness, units and input validation | existing gate; no new tests |
| A-05 | Bias/design | Ch 1 highlights sites, sampling, measurement order and missing readings | Make patient/site/visit and acquisition-order metadata explicit in case labs | queued |
| A-06 | Graphics | Ch 2 calls for self-contained, labeled displays | Retain N, scale, unit and accessible legend checks | existing gate; figure QA pending |
| A-07 | Complete Rmd | Prior 17-chunk synthetic Rmd exists | Audit parse/execution/knit against complete chapter contract | pending: R runtime unavailable in this pass |
| A-08 | Source claims | Full section-specific study review is not complete | Preserve `source_checked` separately from `R_executed` and `statistically_reviewed` | pending |
| A-09 | Synthetic example | ERBB2 score and subtype data invented | Keep every figure/result labeled synthetic | documented; scientific reality not inferred |
| A-10 | Ontology | Existing oncology book has planned CO-07+ chapter records | Do not promote manifest statuses for a style/utility change | retained |

## New executable compatibility module

- `06_RESOURCES/R/biostat_descriptive_contract.R`: `biostat_quantiles()` with `method="biostat8"` (R type 2) or `method="pauls_notes"` (R type 7), explicit NA policy; `biostat_descriptive_contract()` for total N, observed n, missing n/%, mean, sample SD, median, Q1/Q3/IQR and documented units.
- `06_RESOURCES/tests/test_biostat_descriptive_contract.R`: deterministic synthetic checks of different percentile conventions, known exact values, integer observation counts, sample SD, type-7 compatibility, invalid probabilities, NA/NaN/Inf, zero-observation cases and singleton behavior.
- Existing `stats_plots.R`, its calls, and the existing 17-chunk Rmd were **not rewritten** in this pass. No new patient data imported.

~~~r
## Example from repository root; choose quantile method explicitly
source("06_RESOURCES/R/biostat_descriptive_contract.R")
x <- c(1, 2, 5, 9, NA_real_)
biostat_descriptive_contract(x, method="biostat8", unit="fictional score")
biostat_descriptive_contract(x, method="pauls_notes", unit="fictional score")
~~~

**Numerical reference, before execution:** For observed synthetic values (1,2,5,9), Biomedical methods type-2 Q1=1.5, median=3.5, Q3=7; type-7 Q1=1.75, median=3.5, Q3=6. Sample mean=4.25, n=4 of N=5; missing 1 (20%). The tests assert these values and retain unrounded calculations.

## Verification commands and status

~~~bash
Rscript --vanilla 06_RESOURCES/tests/test_biostat_descriptive_contract.R
Rscript --vanilla 06_RESOURCES/tests/test_biomedical_test_selector.R
Rscript --vanilla 06_RESOURCES/tests/test_biostat_method_crosswalk.R
Rscript -e 'rmarkdown::render("02_biomedical_coding/examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd", quiet=TRUE)'
~~~

**Observed environment limitation:** `Rscript` and `R` were not found on the current container's PATH. Therefore these are **prepared commands, not passed tests**. No claim of successful R execution, clean knit, or scientific validation should be inferred. Independent R runtime/knit is the next physical acceptance gate.

## Next minimal passes

1. Run the new tests in a configured R runtime; correct any observed defects before integrating the helper into `stats_plots.R`.
2. Audit the complete Rmd for assumptions/errors and identify analyses inappropriate for observational cancer subtype examples.
3. Add source-linked topic/section registry for 8e, with checked source location, parameterizations and example IDs; do not simply reuse old 6e page references.
4. Build synthetic patient–tumor–specimen–visit fixtures that fail invalid joins, duplication and data leakage.
5. Implement independent numerical replay tests for the core inferential and categorical methods.
6. Report actual source reviews and runtime evidence before changing oncology book manifest states.

**Boundary:** Source alignment confirms code matches a clearly stated convention. It does not establish scientific validity for patient data or justify any particular hypothesis test.
