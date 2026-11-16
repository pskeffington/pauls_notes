# R validation status — breast cancer statistical curriculum

**Audit date:** 2026-11-13. **Scope:** `03_learning` statistical foundations, biostatistics chapter crosswalk, study-design calculator and synthetic protocol-to-results case.

## Evidence epochs and acceptance boundaries

This status document records work available **through its dated audits**, not a live query of every GitHub Actions run. Three evidence streams must remain separate: (1) the October 22 paper-linked **19-object teaching atlas** with historical synthetic and published-aggregate calculation replays; (2) the November 14 **27-selector/25-gate** matrix source checks; and (3) the later **17-chunk synthetic breast cancer workbook** and figure gallery, whose committed R tests and HTML rendering require their own verified execution. An earlier R 4.3.3 atlas result cannot be used as proof that later code executed. The [complete acceptance ledger](../../02_biomedical_coding/BIOSTAT_8E_VERIFICATION_ACCEPTANCE_LEDGER.md) holds the new workstream's evidence and pending gates.

## November 14, 2026 — V2 decision matrix validation extension

The [route-by-route V2 matrix](BIOMEDICAL_DECISION_MATRIX_V2.md) and [CSV registry](biomedical_decision_matrix.csv) now cover **27 distinct selector IDs** linked to **25 defined assumption gates** through **156 route-gate relationships**. A cross-file connector-side structural inspection checked for duplicate/missing selector IDs, missing biostatistics chapter crosswalk IDs, unknown gates and empty matrix fields; **no mismatches were observed**. That inspection is not an R test or clinical validation.

**Committed new validation paths:**

```bash
python3 scripts/check_biostatistics_matrix.py
python3 -m unittest discover -s scripts/tests -p 'test_biostatistics_matrix.py' -v
Rscript --vanilla 06_RESOURCES/tests/test_biomedical_matrix_gate_review.R
```

The first checks the CSV schema and cross-reference integrity; the negative fixtures probe missing routes, duplicate IDs, illegal classes, empty interpretations and bad gates. The R suite is designed to replay each selector route and verify that every gate begins `not_checked`, concerns block review and even all-`documented` gates confer only `ready_for_human_review`. **These suites were added to GitHub Actions but no completed execution log was available during this pass.** Never equate a successful matrix lookup or a complete checklist with sound study design, valid assumptions or a real clinical finding.

## Execution environments

- **Local execution in the November 2026 acceptance audit environment:** BLOCKED. That container had neither `R` nor `Rscript`; no run was recorded there. This does **not** negate the earlier dated atlas execution record and cannot be generalized to other machines.
- **GitHub CI:** `.github/workflows/learning-case-validation.yml` has an R runner installation step and now **explicitly invokes** the newly added R suites and renders the synthetic R Markdown study report.
- **CI outcome as of this audit:** NOT VERIFIED. The GitHub connector exposes neither an independently confirmed completed push-triggered run nor its job logs here. A committed workflow is not proof of green CI.

## Tests specified for the runner

```bash
Rscript --vanilla 03_learning/tests/test_breast_cancer_foundations_lab.R
Rscript --vanilla 03_learning/tests/test_breast_cancer_distribution_lab.R
Rscript --vanilla 03_learning/tests/test_breast_cancer_reference_values.R
Rscript --vanilla 03_learning/tests/test_breast_cancer_test_atlas.R
Rscript --vanilla 03_learning/tests/test_biostat_method_cases.R
Rscript --vanilla 03_learning/tests/test_breast_cancer_study_design.R
Rscript --vanilla 03_learning/tests/test_breast_cancer_protocol_replay.R
Rscript --vanilla 03_learning/tests/test_biostat_method_crosswalk.R
```

### R Markdown render

```bash
Rscript --vanilla -e 'rmarkdown::render("03_learning/examples/breast_cancer_protocol_report.Rmd", output_format="html_document", output_dir=tempdir(), quiet=TRUE)'
```

The report requires `rmarkdown`, `knitr` and Pandoc. The workflow installs the relevant R packages; the Ubuntu runner is expected to have Pandoc but this must be observed in the run logs.

## Independent arithmetic spot checks

For hypothetical continuous outcome difference Δ=5, planning SD=12, two-sided α=.05, target power=.80:

- z-sum: `qnorm(.975)+qnorm(.8)` ≈ 2.8016.
- Approximate equal-arm n = `ceiling(2 * z_sum^2 * 12^2 / 5^2)` = **91** analyzable per arm.
- With 10% endpoint unavailability: `ceiling(91/.9)` = **102** planned enrollment per arm. Inflation is only a heuristic.

For hypothetical survival HR=.75, equal allocation and the same α and power:

- Event formula: `(z_sum)^2 / (0.25 * log(.75)^2)` ≈ 379.35.
- `ceiling(...)` = **380 events**, not enrolled people.

These independently checked values are teaching references. None implies real breast cancer effect sizes or sufficient power under composite missingness rules.

## Acceptance and release decision

| Gate | State | Evidence required to pass |
| --- | --- | --- |
| Code committed and indexed | Completed | Paths and workflow exist on main |
| Independent sample-size arithmetic | Completed | Simple exact inputs and independent numerical calculation |
| Parse all new R files in an R runtime | Pending | R parse succeeds under installed R |
| Execute full R unit suite | Pending | Exit status 0 and detailed logs |
| Knit HTML protocol report | Pending | Renderer exits 0; output reviewed |
| Execute newer 17-chunk workbook and graph gallery | Pending | Dedicated R acceptance job exit 0; retained synthetic HTML inspected |
| Visual review of figures/tables | Pending | Open rendered output and inspect titles, denominators, clipping, missingness |
| Clinical validity | Not assessed | Appropriate governed data, real protocol, ethics, statistical review |

**Do not change Pending to Passed until a completed CI run or local R output actually demonstrates success.** If CI fails, record the failing file, R/package version, error, fix commit and rerun result. Do not suppress errors, delete tests or conflate synthetic checks with clinical inference.
