# eighth-edition methods breast cancer biostatistics — verification and acceptance ledger

**Date:** 2026-11-15  
**Workstream:** BC-BIOSTAT-ALIGN-2026; continuation of BR-001/BR-010 acceptance engineering  
**Source:** *Fundamentals of Biostatistics*, 8th ed. (2016), user-supplied 962-page PDF. The 6e contents reference remains separate.

## Acceptance results observed in this pass

| Gate | Test / evidence | Result | Limitation |
| --- | --- | --- | --- |
| V-01 structure | `biostat_8e_complete_chapter_alignment.csv` rows and 14 IDs | 14 records mapped to valid book chapter IDs and correct edition/page offset (in-session crosswalk validation) | Checks mapping, not every textbook derivation |
| V-01b book page integrity | PyMuPDF inspected the actual PDF start page for R8-CH01 through R8-CH14 | **14/14** printed start-page numbers verified at PDF page = printed page + 22 | Opening-page integrity only, not a full section-by-section audit |
| V-02 Rmd fencing | Open/close fences and labels in `SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd` | 17 named unique R chunks; 17 code-fence closures; 12 inline R expressions checked structurally | R parser not available in current environment |
| V-03 quantiles | Review of `test_biostat_descriptive_contract.R` | Repaired singleton quantile expectation: default Q1/Q2/Q3 returns 3 values | Actual `Rscript` execution pending |
| V-03b independent numerical replay | Python/NumPy on synthetic vector (1,2,5,9); source PDF p. 40 | Type-2 Q1/median/Q3 = 1.5/3.5/7; type-7 = 1.75/3.5/6; sample SD = 3.593976442141304 | Independent arithmetic/reference verification, **not R execution** |
| V-04 complete method execution | `02_biomedical_coding/tests/test_full_study_execution.R` | Acceptance runner authored and structurally checked; purls/parses all R code, executes all chunks and checks synthetic cohort/model invariants | Not executed locally; R absent |
| V-05 optional branches | survival Cox and `nlme` mixed model | Acceptance runner now **requires** their objects; CI explicitly installs `survival` and `nlme` | CI success unconfirmed |
| V-06 full HTML artifact | `.github/workflows/learning-case-validation.yml` | CI knit step and nonempty HTML check configured | CI result not observed |
| V-07 portability | run environment | Local execution container has no `R` or `Rscript`, and cannot reach GitHub via Git CLI | GitHub connector used for authorized source inspection and commits |
| V-08 code provenance | notebook/cluster/clinical claims | Study uses invented data, no person-level clinical records; existing oncology book manifest left unchanged | Not a clinical validation |
| V-09 CI run | GitHub combined status for final workflow change | No combined status entries returned | Does **not** mean CI passed or failed |

**Physical source check:** The uploaded eighth-edition PDF was opened locally and confirmed to have **962 pages**; page 4 identifies the eighth edition, PDF page 27 begins Chapter 2 and PDF page 40 includes Biomedical methods's type-2 quantile example. These page checks supplement the registry source provenance without demonstrating full chapter-level derivation review.

## Confirmed changes

1. `06_RESOURCES/tests/test_biostat_descriptive_contract.R`: singleton quartile assertion now expects three values and no longer compares a three-vector against scalar `1`.
2. `02_biomedical_coding/tests/test_full_study_execution.R`: end-to-end test reads the actual workbook, requires 17 labeled chunks, extracts and parses R code with `knitr::purl`, sources it in a synthetic-only environment, then checks cohort counts, missingness, unique patients, Welch interval, within-patient pairing, held-out metrics, bootstrap, survival Cox and mixed-model results.
3. `.github/workflows/learning-case-validation.yml`: includes the entire `02_biomedical_coding/**` subtree, checks chapter mapping, runs the end-to-end test, installs `r-cran-nlme`, knits HTML into runner temporary storage and verifies that the output is nonempty. Job timeout was increased to 35 minutes for the existing substantial R/Bioconductor dependency suite.
4. The earlier `scripts/check_biostat_8e_alignment.py` checks chapter and manifest paths; its result is a **structural** gate only.

## Required live commands

Run at repository root in a clean R-enabled machine:

```bash
python3 scripts/check_biostat_8e_alignment.py
Rscript --vanilla 06_RESOURCES/tests/test_biostat_descriptive_contract.R
Rscript --vanilla 02_biomedical_coding/tests/test_full_study_execution.R
Rscript --vanilla 03_learning/tests/test_biostat_method_crosswalk.R
Rscript --vanilla 03_learning/tests/test_breast_cancer_test_atlas.R
Rscript --vanilla -e 'rmarkdown::render("02_biomedical_coding/examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd", output_format="html_document", quiet=TRUE)'
```

For acceptance, record exit codes, R and package versions, CI job URL/commit SHA, generated HTML size, and visible table/figure checks. If any test fails, mark it failed and repair the actual defect; do not promote the surrounding chapter based on other passing tests. The Rmd report must be visually reviewed, not merely written.

## Remaining scientifically meaningful checks

- **Methods:** independently verify exact-tail probability calculations, 95% CIs, paired and independent assumptions, effect/ratio labeling and multiplicity families.
- **Clinical context:** verify oncology endpoint and receptor definitions, specimen–patient relationships, eligibility, time zero, censoring and outcome provenance. Synthetic biomarker/subtype associations are pedagogical only.
- **Source fidelity:** complete page/section-specific checks of author claims and equations across all 14 chapters. The existing chapter-complete **topic** map cannot substitute for that.
- **Model adequacy:** check logistic separation, Poisson dispersion, Cox proportional-hazards diagnostics, repeated-measure covariance assumptions, classification calibration and external validity.
- **Governance:** G0–G10 and independent statistical/domain reviews remain required before any manuscript-ready or clinically applicable designation.

**Readiness:** `source-and-code-structure-reviewed`; `r-execution-pending`; `knit-pending`; `independent-statistical-review-pending`; `publication-ready=false`.


## Acceptance continuation — parsing and paired-analysis repair (2026-11-15)

**Confirmed defect R-011 — hyphenated visit name parsed as subtraction.** The full-study workbook previously used `wide$score.Follow-up` in the difference, paired t-test and signed-rank test. Because hyphen is an operator in R, this does not refer to the `score.Follow-up` column and would fail evaluation. Replaced all three with `wide[["score.Follow-up"]]`; also bracket-addressed `score.Baseline` and asserted the expected reshape schema. This is a **code-level repair**, not a claimed passed knit.

**Regression hardening:** `02_biomedical_coding/tests/test_full_study_execution.R` now verifies both paired visit column names, 240 numeric finite per-patient differences, and equality to follow-up minus baseline. `scripts/check_biostat_8e_alignment.py` checks 17 unique workbook chunks, matching closing fences, absence of the invalid token, and exact column-key references.

**Verification performed:** Refetched both committed GitHub files after the edits. Confirmed three unsafe references became zero, the paired block uses exact bracket column access, and the workbook still contains 17 labeled chunks and 17 matching closing fences.

**CI observation:** GitHub commit status API returned no status entries; commit-associated workflow query returned no PR-triggered runs. These API responses do not establish that the main-branch Actions workflow ran successfully. Full R execution, render inspection, and independent statistical/clinical signoff remain pending. Do not mark workbook acceptance passed until actual run logs and generated output are inspected.

## Acceptance continuation — neutral-method migration verification (2026-11-15)

**Confirmed defect V-012: escaped Python regex tokens.** The structural validator's initial code used double-escaped raw regex groups and did not recognize real R Markdown chunks. It was repaired to use Python raw patterns `r"^```\\{r\\s+([^,}\\s]+)"` and `r"^```\\s*$"`; chunk matching and fence matching are now correctly specified.

**New regression coverage:** `scripts/tests/test_biostat_8e_alignment.py` adds five tests: real workbook chunk structure; invalid hyphenated paired column; duplicate chunk labels; unbalanced fences; missing exact paired column. The CI learning-case workflow invokes the new Python tests and also retains the full R study execution and knit gates.

**Method-label compatibility:** The descriptive estimator now labels conventions by actual calculation, `Quantile type 2` and `Quantile type 7`, and the method selector prints `Biostatistics chapter map (8e)`. The selector's associated R test expects the same text. These are presentation changes; formulas and the 27 existing routing IDs have not been altered.

**Observed in-session source verification:** Re-fetched the committed workbook, validator, new regression test, R selector and matching test, and CI workflow. Found 17 distinct chunk labels, 17 closing code fences, five new test cases, the corrected regex source and consistent labels. **These are structural/source checks only**, not execution of Python tests or R.

**CI evidence:** GitHub combined-status response exposed zero status entries; the commit-associated workflow lookup (which filters to PR-triggered runs) exposed zero runs. Neither is evidence of successful or failed main-branch Actions execution. R execution, knitted HTML visual review, independent statistical review and publication readiness remain **pending**.

**Source policy:** Educational assets use methodology-first names; bibliography-only author attribution is checked by `scripts/check_methodology_attribution.py`. Maintain scholarly source credits in `METHODOLOGY_SOURCE_REFERENCES.md` when specific claims need them, without branding the internal analysis, function names or examples.


## Acceptance continuation — CI preflight and independent inference checks (2026-11-15)

**Verified source change P-01:** `.github/workflows/learning-case-validation.yml` now has a separate `methodology-preflight` job on Ubuntu with no R installation requirement. The preflight invokes `scripts/check_biostat_8e_alignment.py`, five workbook markup regression tests, and `scripts/check_methodology_attribution.py`. Both push and pull-request path filters now include `AGENTS.md`, `llms.txt`, `docs/machine-index.md`, the bibliography and the attribution checker itself. The existing full R execution and knit job is retained.

**Verified source change P-02:** The unclosed-fence test now removes a closing code fence without changing the count of the 17 R chunk labels; it therefore tests the **fence-balance** error path, rather than passing only because an 18th chunk was added.

**Verified source change P-03:** `02_biomedical_coding/tests/test_full_study_execution.R` now calculates the Welch Satterthwaite degrees of freedom, t statistic and 95% CI independently from unrounded group vectors. It separately calculates the paired mean and t-based 95% CI from within-patient differences. Each is compared to the corresponding `stats::t.test()` output with a numerical tolerance of 1e-10. Confidence-interval attributes are intentionally dropped for the numeric comparison, not for original analysis.

**In-session checks performed:** GitHub source was refetched after commit, and the following properties were checked: all four new CI trigger classes present under both push and pull request; preflight job and attribution check present; five Python regression test definitions; a specific missing-fence assertion; independent Welch and paired CI calculations present; and zero discrepancies in these source-level checks.

**Execution boundary:** `Rscript` and `R` were not present in the available execution container. Git clone from GitHub failed due to DNS/network restrictions, so the complete repository and Python tests could not be run locally. CI run success is **not** established from source inspection. Treat Python/R tests as configured but unexecuted until actual CI logs or a clean local replay are inspected. Bibliography-only scholarly attribution policy remains unchanged. No book chapter or publication status was promoted.


## Acceptance continuation — estimand consistency and model contracts (2026-11-15)

**Confirmed semantic mismatch corrected.** The workbook previously described a “grade–subtype association” but its implementation is a comparison of continuous synthetic ERBB2 scores across tumor grades. It now labels the actual grade-specific score estimand. The classifier example is correctly described as held-out *prediction* discrimination, not demonstrated diagnostic screening performance.

**Repeated-measures design corrected.** The original teaching fixture generated independently drawn baseline and follow-up values despite fitting a patient random-intercept model. The revised fixture draws a patient baseline and then generates follow-up from baseline plus a stochastic within-person change; patient IDs and two-visit ordering remain unchanged. A regression assertion requires a positive within-person visit correlation greater than 0.5 in this seeded synthetic fixture. This fixes pedagogical coherence, not clinical realism.

**Additional full-study inference gates authored:**
- Exact per-analysis observation count: synthetic baseline 240, linear regression 234, logistic regression 238, Poisson regression 240, accounting for deliberately injected missing values.
- Wald logistic odds-ratio intervals recomputed from coefficients, covariance diagonal and standard-normal critical value; labels distinguish odds ratios from risk ratios.
- Poisson incidence-rate ratios and confidence limits recomputed independently from model coefficients/standard errors; tests require `log(exposure_years)` as an offset, rather than an estimated slope.
- The previous independently calculated Welch and paired t confidence intervals remain in place.

**Source recheck:** GitHub returned the updated R Markdown workbook and R acceptance script; source inspection found 17 named R chunks, 17 closing fences, revised estimand labels, correlated synthetic visit generation, all model-specific assertions, and retained full-study execution and knit CI steps. Repository code search found only the dedicated methodology bibliography containing the named textbook author.

**Execution status:** Source/structure confirmed; `Rscript` is not installed in the available container. GitHub commit statuses contained no entries and the PR-filtered workflow lookup returned no runs for the tested commit, so neither test execution nor successful CI was demonstrated. **Do not mark numerical runtime, knitted report, statistical review, or publication acceptance complete.** No patient data were used and oncology manuscript statuses remain untouched.
