# Biomedical statistical methods and R deployment: curated 2021–2026 reading

**Paul's Notes · expanded 2026-11-08**<br>
[Data-first learning guide](../../03_learning/biomedical-statistics-decision-guide.md) · [Machine-readable source table](biostatistics_r_literature_2021_2026.csv) · [Existing biomedical evidence matrix](../../02_biomedical_coding/BIOMEDICAL_CODING_LITERATURE_MATRIX.md)

## Scope and method

A **curated narrative reading list**, focused on recent articles that help interpret variable types, choose appropriate statistical methods, implement analysis in R, and deliver reproducible scientific computing. Included below are **nineteen curated publications (2021–2026)** located from publisher/journal records, DOI metadata and article pages as of **2026-11-08**. It is **not** a systematic review, PRISMA search, clinical guideline, validation of paper code, exhaustive comparison of packages, or a claim that all studies are applicable to a particular population. No original patient data or third-party article content is stored here.

Methods are grouped by the teaching decision they inform rather than ranking papers by citation count. A publication supports **why a method matters**; current primary package documentation governs **how to run the installed version**.

## Source-to-learning and implementation matrix

| ID | Publication and year | Type | Practical contribution | Required interpretation / limitation |
| --- | --- | --- | --- | --- |
| BS-001 | [Chicco, Sichenze & Jurman, 2025](https://doi.org/10.1186/s13040-025-00465-6). *A simple guide to the use of Student's t-test, Mann-Whitney U test, Chi-squared test, and Kruskal-Wallis test in biostatistics.* | Statistical tutorial / method | Distinguishes four introductory methods using variable type, independent groups and assumptions; motivates data-first decision aids | Not a comprehensive chart for paired, clustered, count, censoring or high-dimensional endpoints; report effect estimates, not p alone |
| BS-002 | [Muhammad, 2023](https://doi.org/10.1172/JCI171058). *Guidelines for repeated measures statistical analysis approaches with basic science research considerations.* | Viewpoint / methods | Shows why repeated observations on a unit require correlation-aware analyses such as repeated-measures or mixed models | Example analysis is not a universal mixed-model specification; verify clusters, dropout and covariance assumptions |
| BS-003 | [Li et al., 2022](https://doi.org/10.1371/journal.pone.0264246). *An evaluation of RNA-seq differential analysis methods.* | Simulation comparison | Benchmarks multiple RNA-seq differential-expression approaches, including R/Bioconductor tools | Simulated benchmarks cannot establish superiority for every real assay; align raw-count models, design/dispersion and biological replicates |
| BS-004 | [Giorgi, Ceraolo & Mercatelli, 2022](https://doi.org/10.3390/life12050648). *The R Language: An Engine for Bioinformatics and Data Science.* | Narrative review | Introduces R's statistics, bioinformatics package ecosystem and reproducibility roles | Overview and historical descriptions are not runtime/version or numerical validation |
| BS-005 | [Landau, 2021](https://doi.org/10.21105/joss.02959). *The targets R package: a dynamic Make-like function-oriented pipeline toolkit for reproducibility and high-performance computing.* | Research software article | Motivates dependency graphs and reproducible execution with `targets` | A pipeline graph does not prove inputs, methods or clinical interpretation are correct |
| BS-006 | [Schilder, Murphy & Skene, 2024](https://doi.org/10.1038/s41467-023-44484-5). *rworkflows: automating reproducible practices for the R community.* | Research software article | Explains CI, package checks, dependency restoration, docs and deployment automation in R workflows | Successful CI does not prove statistical validity, confidentiality or clinical fitness |
| BS-007 | [Collins et al., 2024](https://doi.org/10.1136/bmj-2023-078378). *TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods.* | Reporting consensus | Transparent reporting for clinical prediction models, regression and ML | A reporting standard is not an external validation certificate or justification for a particular predictor |
| BS-008 | [Hopewell et al., 2025](https://doi.org/10.1136/bmj-2024-081123). *CONSORT 2025 statement: updated guideline for reporting randomised trials.* | Reporting consensus | Updated RCT reporting with design, allocation, outcomes and open-science disclosures | Does not apply to every observational molecular study; trial reporting != causal identification or model validation |

| BS-009 | [West, 2021](https://doi.org/10.1177/0004563221992088). *Best practice in statistics: Use the Welch t-test when testing the difference between two groups.* | Clinical biochemistry practice article | Explains why Welch's unequal-variance t-test is a useful starting point for independent means | Still assumes a meaningful mean estimand and defensible sampling; does not address clustering, heavy tails or causal identification |
| BS-010 | [Wilcox & Rousselet, 2023](https://doi.org/10.1002/cpz1.719). *An Updated Guide to Robust Statistical Methods in Neuroscience.* | Updated methods overview with R code | Explains robust estimators, heteroscedasticity and alternative approaches when conventional comparisons mislead | Robustness does not waive the need for independent units, prespecified estimands or uncertainty review |
| BS-011 | [Midway & White, 2025](https://doi.org/10.1098/rsos.241904). *Testing for normality in regression models: mistakes abound (but may not matter).* | Empirical/simulation methods critique | Differentiates normality assumptions for modeled residuals from indiscriminate tests of raw outcome columns | Simulation results are context-dependent; does **not** justify selecting a new test solely from a Shapiro p-value |

| BS-012 | [Kim, Kim & Kwak (2024)](https://doi.org/10.4097/kja.24016), *Comprehensive guidelines for appropriate statistical analysis methods in research* | Methods guide | Organizes test selection around endpoint, hypothesis, design and assumptions | Does not replace study-specific independence or diagnostics |
| BS-013 | [Pérez-Guerrero et al. (2024)](https://doi.org/10.3390/jcm13144005), *Methodological and Statistical Considerations for Cross-Sectional, Case-Control, and Cohort Studies* | Observational methods review | Clarifies outcome and study-design decisions | Simplified charts omit specialized clustered, causal and rare-event settings |
| BS-014 | [Delporte et al. (2025)](https://doi.org/10.1177/09622802241300823), *Analysing matched continuous longitudinal data: A review* | Systematic methods review | Distinguishes simple paired contrasts from more complex matched longitudinal models | Pairing and correlation structure require design-specific consideration |
| BS-015 | [Wijesuriya et al. (2025)](https://doi.org/10.1002/sim.10274), *Multiple Imputation for Longitudinal Data: A Tutorial* | Tutorial in biostatistics | Addresses longitudinal missingness and correlation-aware imputation | Missing-data mechanism must be justified; not an automatic imputation recipe |
| BS-016 | [Christensen, Ranstam & Overgaard (2023)](https://doi.org/10.2340/17453674.2023.11656), *Guidelines for a structured manuscript: Statistical methods and reporting in biomedical research journals* | Reporting guidance | Requires denominators, method rationale, uncertainty and sensitivity analyses | Reporting alone does not validate a statistical model |
| BS-017 | [Mondal et al. (2026)](https://doi.org/10.7759/cureus.116428), *Effect Estimates, Effect Sizes, Confidence Intervals, and P-values: A Framework for Reporting and Interpreting Biomedical Research* | Educational framework | Reinforces effect magnitude, confidence intervals and p values | A teaching framework cannot replace model-specific theory |
| BS-018 | [Fernandez & Vatcheva (2022)](https://doi.org/10.1186/s12874-022-01685-8), *A comparison of statistical methods for modeling count data with an application to hospital length of stay* | Simulation and applied comparison | Explains Poisson, NB and zero-inflation under dispersion changes | Simulation results are context-specific; no universal count model |
| BS-019 | [Dey et al. (2025)](https://doi.org/10.1186/s12874-024-02454-5), *The proper application of logistic regression model in complex survey data: a systematic review* | Systematic methodological review | Documents common failures to use weights, PSUs and strata | Focuses on particular surveys; follow each survey's design guide |

## Direct translation into the beginner's flowchart

1. **Data type first:** Continuous, count, nominal, ordinal and censored time-to-event require different distributions/estimands. **BS-001** motivates the initial t/rank/chi-square/Kruskal-Wallis split; **BS-009 to BS-011** add practical cautions on Welch tests, robustness and residual diagnostics.
2. **Independence next:** Tumor/normal pairs and repeated visits cannot be treated like unrelated patients. **BS-002** motivates blocking and within-unit covariance.
3. **Genomic measurement scale:** Raw gene-level RNA-seq counts demand assay-aware count models and multiple testing; transformed expression can serve other models, but is not raw read-count input. **BS-003** informs method comparison; check current Bioconductor vignettes.
4. **Computational translation:** Write typed data contracts, checks, versioned analysis and pipeline steps. **BS-004 to BS-006** support the R infrastructure and automation layers.
5. **Publication and use case:** Reporting a prediction model vs randomized intervention requires a matching reporting family. **BS-007 / BS-008** support transparency but cannot prove suitability.

## Upstream software documentation (not research papers)

| Implementation topic | Current authoritative manual | Validation action |
| --- | --- | --- |
| Base R statistics (`t.test`, `chisq.test`, `fisher.test`, `glm`) | [R manual](https://cran.r-project.org/manuals.html) | Run independently checkable fixtures; inspect warnings and missingness |
| Survival models | [`survival` package](https://cran.r-project.org/package=survival) | Check time origin, events, censoring and proportional-hazards diagnostics |
| Mixed models | [`lme4` package](https://cran.r-project.org/package=lme4) | Review random-effect structure, convergence and singular fits |
| RNA-seq differential expression | [Bioconductor `DESeq2`](https://bioconductor.org/packages/DESeq2/) and [`rnaseqGene` workflow](https://bioconductor.org/packages/release/workflows/html/rnaseqGene.html) | Confirm raw counts, sample-to-column alignment, design rank, contrasts and FDR |
| Reproducible workflow | [`targets` manual](https://books.ropensci.org/targets/) | Build pipeline from permitted synthetic inputs and retain execution log |
| Environment freeze | [`renv` manual](https://rstudio.github.io/renv/) | Lock and restore on a clean runner, verify package versions |
| Reporting source | [Quarto documentation](https://quarto.org/docs/) | Verify rendered output from reviewed source files and numeric fixtures |

## Validation ledger and acceptance boundary

| Check | Review status |
| --- | --- |
| Publisher/journal title, year, DOI and linked source | Source pages inspected 2026-10-22 |
| Practical implications | Independent synthesis for educational use; **not** extracted recommendations attributed verbatim to papers |
| Eleven-row machine-readable register | Prepared; repository/CI validation should confirm structure and path integrity |
| Independent rerun of published papers | **Not performed** |
| Clinical study method sign-off, external validation, data admission | **Not performed / not conferred** |

Recent methods also disagree in their emphasis on normality screening: a beginner should evaluate the design, estimand, influence, sample size and model assumptions rather than implementing an automatic Shapiro-result switch. Source position and software behavior should be documented separately.

Only add new references after checking source identity, DOI resolution, year, study type and relevance; add a clear entry about limitations. Keep references in this bounded beginner guide separate from the broad [biomedical coding corpus](../../02_biomedical_coding/README.md). Do not publish participant-linked records or unreviewed small-cell exports.

## Expanded evidence-to-decision crosswalk (2026-11-08)

| Clinical/data situation | Evidence IDs | Design gate before method | Implementation |
| --- | --- | --- | --- |
| Two independent continuous groups | BS-009, BS-011, BS-012 | Confirm independent units, influential values and mean estimand | Generic Welch helper, draft PR #39 |
| Independent continuous groups, 3+ | BS-001, BS-012 | Distinguish omnibus inference from pairwise contrasts; state multiplicity | Welch ANOVA helper, draft PR #39 |
| Paired continuous values | BS-014 | Align by subject and visit; check difference distribution and complete pairs | Paired t helper, draft PR #39 |
| Paired binary outcome | BS-012, BS-014 | Tabulate discordant pairs and assess sparse-data exact options | Documented stats::mcnemar.test |
| Binary/nominal independent groups | BS-001, BS-012, BS-013 | Verify raw counts, denominator, cell frequencies, design | Existing teaching methods; specialist review where needed |
| Count/rate outcomes | BS-018 | Confirm exposure, dispersion and zero-generating mechanisms | Model-specific review |
| Repeated measures and longitudinal missingness | BS-002, BS-014, BS-015 | Check subject IDs, time, covariance and missingness | Specialist model review |
| Complex survey | BS-013, BS-019 | Require weights plus PSU/strata/replicate design | Survey specialist review |
| Interpretation and reporting | BS-016, BS-017 | Estimate, interval, sampling denominator, multiplicity and clinical relevance | Reproducible result table and ggplot2 figure where supported |

These are method-selection references, not evidence that a generic test or model is scientifically valid for a particular study. Package documentation governs current implementation details.
