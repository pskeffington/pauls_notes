# Biomedical methods 8e breast cancer biostatistics — verification and acceptance ledger

**Date:** 2026-11-15  
**Workstream:** BC-BIOSTAT-ALIGN-2026; continuation of BR-001/BR-010 acceptance engineering  
**Source:** the cited textbook author, *Fundamentals of Biostatistics*, 8th ed. (2016), user-supplied 962-page PDF. The 6e contents reference remains separate.

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
