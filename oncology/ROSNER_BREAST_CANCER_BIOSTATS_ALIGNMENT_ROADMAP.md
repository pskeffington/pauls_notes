# Roadmap — Rosner-aligned breast cancer biostatistics textbook

**Program ID:** BC-ROSNER-ALIGN-2026  
**Scope:** Paul's Notes breast-cancer biostatistics teaching track and statistics-relevant chapters of the 60-chapter Computational Oncology book.  
**Current state:** Planning and crosswalk established; **no newly authored chapter, code test, book sign-off or external expert review is implied by this roadmap**.  
**Primary teaching source:** Bernard Rosner, *Fundamentals of Biostatistics*, **8th edition (2016)**, available as a source reference at https://shahealthcare.org/wp-content/uploads/2022/04/Fundamentals-of-Biostatistics-Bernard-Rosner_compressed.pdf. Retain the supplied 6e table-of-contents as a separate edition record; do not combine section numbers.  
**Copyright boundary:** Cite methods and original source pages; author original demonstrations, derivations and questions. Do not import the book's prose, exercise text, proprietary figures, tables, flowchart, or datasets into the repository.

## North-star outcome

A researcher should be able to start from a breast-cancer question; identify independent patient/specimen and assay units; choose and defend a statistical model; derive its mathematical basis; run reproducible R code on a synthetic fixture; inspect assumptions, effect estimates and uncertainty; interpret a medically meaningful result; and distinguish statistical significance, clinical relevance, bias, prediction, and causation.

**Reference priority:** Rosner for foundational inference and teaching progression; modern primary methods literature and official statistical package documentation for current implementation; clinical oncology reporting standards for endpoint/study context; Paul's Notes G0–G10 gates for code quality. Neither textbook reputation nor a passing R test automatically validates a cancer study.

## Existing materials to reuse, not fork

| Asset | Path | Integration |
| --- | --- | --- |
| 60-chapter oncology architecture | `oncology/ROADMAP.md` / `oncology/book-manifest.json` | Canonical chapter IDs and actual publication statuses |
| 8e method selector | `03_learning/bio_stats/ROSNER_TEST_SELECTION_MATRIX.md` | Entry-by-design, no test selected from outcome alone |
| 27-route and 25-gate matrix | `03_learning/bio_stats/BIOMEDICAL_DECISION_MATRIX_V2.md` | Required study information before inference |
| 26-method breast cancer atlas | `03_learning/bio_stats/BREAST_CANCER_WORKED_TEST_ATLAS.md` | Original oncology interpretation, expand each card to full chapter lab |
| Breast cancer statistical foundations | `03_learning/bio_stats/BREAST_CANCER_STATISTICS_FOUNDATIONS.md` | CLT, Welch, t, ANOVA, Poisson foundations |
| Distributions and power | `03_learning/bio_stats/BREAST_CANCER_DISTRIBUTIONS_AND_POWER.md` | CIs, sampling, exact/approximation methods |
| Cancer study design | `03_learning/bio_stats/CANCER_STUDY_DESIGN.md` | Clinical designs, denominators, power |
| Protocol-to-results case | `03_learning/bio_stats/BREAST_CANCER_PROTOCOL_TO_RESULTS.md` | End-to-end study narrative |
| Complete R Markdown example | `02_biomedical_coding/examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd` | Style, named chunks and knit contract; independently verify |
| Canonical R coding rules | `02_biomedical_coding/BIOMEDICAL_R_CANONICAL_EXAMPLE.md` | AI first-read |
| 8e source companion | `02_biomedical_coding/ROSNER_8E_SOURCE_VERIFIED_IMPLEMENTATION.md` | Source-specific method notes, with stated review coverage |
| 6e separate TOC crosswalk | `02_biomedical_coding/ROSNER_6E_CHAPTER_TO_CODE_BEST_PRACTICES.md` | Historical edition separation |
| Implementation acceptance gates | `02_biomedical_coding/IMPLEMENTATION_GATES.md` | G0–G10 and evidence grading |
| Visualization standards | `06_RESOURCES/R/scientific_palette.R`; `06_RESOURCES/R/stats_plots.R` | Plot overlays, Okabe–Ito mapping, labels |

## Verification acceptance checkpoint
[Live acceptance ledger](../02_biomedical_coding/ROSNER_8E_VERIFICATION_ACCEPTANCE_LEDGER.md) records page-level source verification, fixture repairs, the 17-chunk workbook execution test and GitHub Actions knit requirements. Physical PDF chapter start-page mapping is verified 14/14; R execution and specialist review are **not** yet recorded as passed.

## Complete chapter-method contract and structural gate

[Rosner 8e complete methodology contract](../02_biomedical_coding/ROSNER_8E_COMPLETE_METHODOLOGY_CONTRACT.md) and the [14-chapter machine coverage ledger](../02_biomedical_coding/rosner_8e_complete_chapter_alignment.csv) establish chapter-by-chapter method expectations. Run `python3 scripts/check_rosner_8e_alignment.py` to verify all 14 source chapter IDs, correct edition/page-offset mapping, manifest links, method sections and test file presence. This checks structural coverage **only**; statistical and R/knit gates remain separate. No book-manifest completion statuses have been advanced.

## First alignment implementation checkpoint

[BR-001 first source-to-code audit](../02_biomedical_coding/ROSNER_ALIGNMENT_FIRST_PASS_AUDIT.md) has been authored. It identifies the Rosner 8e type-2 versus Paul's Notes type-7 quantile convention and adds an opt-in helper/test without changing established descriptive results. **No R runtime was available; all execution, knitting and scientific-review gates remain pending.** This is a partial BR-001 checkpoint, not closure of BR-001 or advancement of any CO chapter status.

## Workstreams and gated execution

### Phase P0 — Source and content audit (blocker for attributing author-specific claims)

**Deliverables:** one row per 8e chapter/section, correct printed page and PDF page, source classification, current oncology chapter and matching code/tests; audit which of 60 oncology chapters actually exist. Preserve 6e vs 8e distinction and record areas where the published 8e chapter is not yet reviewed.

**Acceptance:** chapter map has no ambiguous edition references; no new chapter statuses promoted; all links resolve; missing reading, reproducibility and external verification remain explicit. Never infer that a broad crosswalk means a section-by-section textbook review occurred.

### Phase P1 — Mathematical and clinical foundations

**Rosner scope:** chapters 1–6 plus 7's foundations. **Oncology chapters:** CO-04/05/06 then CO-07 through CO-11; clinical examples connect to CO-01/02/03 and CO-15/20.

For each topic produce original derivation (notation and denominator defined), synthetic patient-level case, worked calculation and independent R cross-check:
- probability rules, base-rate effects and Bayes screening;
- normal and discrete random variables, exact binomial vs tail, Poisson counts and exposure;
- mean, sample variance, coefficient of variation applicability, standard error, CLT limitations;
- confidence intervals (mean, proportion, incidence rate), finite-sample assumptions and bootstrap alternatives;
- prevalence vs incidence vs risk vs rate;
- measurement units, stage ordinalness, tumor grade and receptor-test semantics.

**Exit:** at least one hand-computed reference value and one R fixture per concept, all numerically agreeing within prespecified tolerance; graphics explicitly show denominators and missingness.

### Phase P2 — Statistical test choice and inference

**Rosner scope:** chapters 7–10 and 12. **Oncology:** CO-11/12/13 and CO-17/20/22.

Build one reusable method card and one runnable named chunk for each: one-sample t, Welch/pooled t, paired t, sign, Wilcoxon signed-rank/rank-sum, one-way/two-way ANOVA, Kruskal–Wallis, Fisher/chi-square/R×C GOF, one/two proportions, McNemar, kappa, group contrast, and familywise/FDR adjustment. Test sample-size and power under simple and design-adjusted cases.

**Exit:** per method clinical question → independent unit → estimand → mathematical sampling model → diagnostics → R function → computed estimate, CI and test statistic → interpretation → contraindication/counterexample → reviewer checklist. Include a case where superficially similar data require *different* tests (paired specimen vs independent tumor groups).

### Phase P3 — Adjusted oncology analyses and study design

**Rosner scope:** chapters 11 and 13. **Oncology:** CO-14/16/17/18/19 and CO-22/23/27/28.

Produce linear/logistic models; confounding and effect modification; Mantel–Haenszel and standardization; crossover/clustered and repeated outcomes; ICC, random effects and GEE; missing data, measurement error, meta-analysis and equivalence. Separate model-adjusted association from causal identification and never treat odds, risk, rate and hazard ratios as interchangeable.

**Exit:** regression formula and coding, adjusted estimand, factor reference, dependency structure, covariance/SE basis, diagnostics, interval, sensitivity, missing-data handling and a synthetic challenge that makes naive inference wrong.

### Phase P4 — Epidemiology, person-time, survival and prediction

**Rosner scope:** chapters 3, 13 and 14. **Oncology:** CO-15/20/24/25/26 and CO-43–48 as modern extensions.

Build nested synthetic cancer follow-up demonstrations: risk sets, person-time, incidence-rate ratios, Poisson offset and dispersion, KM/log-rank, Cox PH residual diagnostics and sample-size planning. Modern extensions are separately identified: competing risks, time-varying exposures, calibration, decision curves, internal/temporal/external validation, leakage prevention, clinical threshold selection.

**Exit:** define eligibility/time zero, censoring and competing events; prove units/offsets; inspect survival and calibration curves and show a clear counterexample to interpreting HR as risk ratio.

### Phase P5 — Molecular oncology translation

**Textbook relation:** Rosner provides basic distributions, multiple testing and regression, **not a substitute for current RNA-seq/assay methods**. **Oncology:** CO-37–42 plus the ESR1/ERBB2 breast cancer learning case.

Use *entirely synthetic* count matrices with independent biological samples to demonstrate:
- raw counts vs normalized expression and log-transformed scores;
- gene IDs, sample metadata alignment, library sizes and QC;
- assay-aware dispersion/normalization (edgeR/DESeq2/limma when supported);
- prespecified contrasts, batch confounding and technical vs biological replicates;
- thousands of feature tests, BH FDR, volcano/MA, heatmap and gene-set caveats;
- source-linked biological interpretation without suggesting the randomly generated effect is measured breast cancer biology.

**Exit:** tests prove samples did not swap, learned processing did not leak, negative counts/zero libraries are rejected, and multi-gene inference does not substitute unadjusted t-tests for an RNA-seq count model.

### Phase P6 — Peer review, code verification and publication

For each chapter, keep **separate labels**: `outlined`, `drafted`, `source_checked`, `numerically_replayed`, `r_executed`, `knit_reviewed`, `statistically_reviewed`, `clinical_content_reviewed`, `publication_ready`. All begin false until evidence exists.

**Exit:** CI runs for synthetic R fixtures; independent calculations match; one clean knit with every table/figure and computed narrative; specialist checks design and inference; oncology domain reviewer checks endpoints and clinical terminology; editorial check verifies citations/rights/accessibility. Publish only when the relevant chapter gate and manifest status are supported by evidence.

## Method-to-chapter mapping — priority sequence

| Priority | Rosner 8e chapter(s) | Oncology chapters | Method module / target |
| --- | --- | --- | --- |
| 1 | 1–3 | CO-04, CO-07, CO-20 | unit of analysis, probability, screening |
| 2 | 2, 4–6 | CO-08–CO-10, CO-15 | distributions, sampling, estimation |
| 3 | 7–9 | CO-11–CO-13 | hypotheses, two-sample, rank/permutation |
| 4 | 10, 12 | CO-12, CO-13, CO-20, CO-27 | categorical, ANOVA, interactions, ICC |
| 5 | 11 | CO-22 | linear regression, correlation and diagnostics |
| 6 | 13 | CO-14, CO-16–19, CO-23, CO-27 | epidemiologic effects, confounding, logistic/cluster |
| 7 | 14 | CO-15, CO-24–26 | person-time, KM, Cox |
| 8 | 12 (FDR), contemporary omics | CO-37–42 | genes, variance, FDR and appropriate assays |
| 9 | Rosner + modern validation methods | CO-43–48 | prediction, leakage, calibration and generalizability |
| 10 | all above | CO-55–60 | evidence appraisal, manuscript and audit |

The remaining oncology chapters (including AI, Rust/Python, deployment, clinical governance) retain their own independent references; Rosner is **not** declared an authority for unrelated software engineering or modern clinical AI.

## Required chapter artifact contract

A chapter is a package of independently inspectable materials:
1. **Human narrative:** clinical question, learning objectives, prerequisites, original breast cancer example, definitions and intuition.
2. **Mathematical exposition:** sampling model, explicit formula, units, derivation, assumptions and expected edge cases; numerical reference calculation.
3. **Study protocol:** eligibility, design, source, independent unit, treatment/exposure definition, time zero, outcome, estimand, contrast, missingness, selection and multiplicity.
4. **Executable Rmd:** YAML, named section chunks with `##` dividers, synthetic data generator, schema gates, graphics, tables, method diagnostics and data-driven results narrative; no Markdown `**` in R code.
5. **Test suite:** valid fixture, malformed inputs, paired-vs-independent, NA/Inf, non-positive exposure, empty/singleton groups, sparse counts, and numerical tolerance checks.
6. **Review record:** Rosner 8e specific section/page (where verified), contemporary source/official R manual if needed, exact commands and outputs, knit QA, specialist reviewer, source boundary and open issues.

**Templates must not invent results, simulate a patient dataset and label it TCGA, copy textbook content, add silent packages, or change the mainline book manifest without actual chapter implementation and review.**

## Quantitative quality controls and milestone ledger

| Gate | Metric / pass criterion | Initial status |
| --- | --- | --- |
| Q1 — Crosswalk | 14/14 Rosner chapters mapped, edition explicit; 60 CO chapter relationships reviewed | Mapping drafted; review pending |
| Q2 — Concept coverage | 100% of selected core methods have a question, estimand, assumptions and failure case | Not measured |
| Q3 — Computation | 100% of claims with numeric worked examples have deterministic fixture and independent tolerance check | Not measured |
| Q4 — R code | 100% of published code chunks parse/run with required dependencies; invalid data fail appropriately | Not measured |
| Q5 — Reports | 100% publishable Rmd labs knit clean and visibly include evidence, figures, Ns and uncertainty | Not measured |
| Q6 — Literature | Every source-dependent attribution has checked edition, section and evidence record | Partial targeted source checks |
| Q7 — Clinical fidelity | All survival/response/assay terms reviewed by qualified domain reviewer | Not reviewed |
| Q8 — Reproducibility | CI logs and clean-environment replay tied to exact commit | Not measured |
| Q9 — Publication | No chapters labeled final without completed author, statistician and clinical review | Gate defined, not fulfilled |

## First ten bounded Codex work packages

| ID | Dependencies | Work product | Acceptance evidence |
| --- | --- | --- | --- |
| BR-001 | none | Inventory all stats/oncology assets and 60 manifest chapter statuses | machine-readable report and diff |
| BR-002 | BR-001 | 8e source/section-to-CO concept crosswalk, with page/edition evidence | no edition collision or unsupported quote |
| BR-003 | BR-001 | Synthetic breast cancer master data dictionary and independent patient/assay fixtures | schema and edge-case tests |
| BR-004 | BR-002/003 | CO-07 probability/Bayes screening teaching chapter and Rmd | source checks, independent calculation, knit |
| BR-005 | BR-002/003 | CO-08 discrete/binomial/Poisson module | exact-tail, exposure and integer tests |
| BR-006 | BR-002/003 | CO-09 continuous distribution and CLT simulation module | seed, approximations, tolerance, failure case |
| BR-007 | BR-004–006 | CO-10/11 estimation and inference module | mean/proportion/rate CIs, design-based rationale |
| BR-008 | BR-007 | CO-12/13 comparative methods, power and multiplicity | full test selector + validated Rmd |
| BR-009 | BR-008 | Epidemiology/longitudinal/regression and survival bridge (CO-14–28) | model diagnostics, uncertainty, clinical endpoints |
| BR-010 | BR-001–009 | Editorial, independent R knit and chapter review; only then manifest status proposals | per-chapter source+runtime+review evidence |

**Operational instruction:** work one package at a time, make small source-specific changes, run actual tests before recording success, and never mark other chapters complete because a chapter roadmap exists. The owner can authorize parallel *independent* fixture/source work once shared interfaces are frozen.

## AI retrieval instructions

Retrieve in this order for breast-cancer biostatistics:
`AGENTS.md` → `llms.txt` → **this roadmap** → `oncology/book-manifest.json` → `02_biomedical_coding/ROSNER_8E_SOURCE_VERIFIED_IMPLEMENTATION.md` → `03_learning/bio_stats/ROSNER_TEST_SELECTION_MATRIX.md` → `02_biomedical_coding/BIOMEDICAL_R_CANONICAL_EXAMPLE.md` → relevant verified chapter and R code.

**Stable retrieval key:** `pauls-notes.breast-cancer.rosner-methodology-roadmap.v1`.  
**Search aliases:** Rosner aligned breast cancer biostatistics book; breast cancer stats textbook roadmap; Rosner method to oncology chapter crosswalk; Paul's Notes bio-stats author alignment.

## Open risks

- Full per-section review of Rosner 8e is not complete: use evidence flags, not blanket “cover-to-cover aligned” claims.
- Existing 6e contents and 8e full text can collide if page references are copied without edition fields.
- Competing risks, modern assay pipelines, prediction and causal inference require current specialists beyond the textbook.
- The existing full-study Rmd and legacy test atlas need independent execution/knit verification; none is assumed here.
- Independent statistical and oncology content review is not yet recorded.
