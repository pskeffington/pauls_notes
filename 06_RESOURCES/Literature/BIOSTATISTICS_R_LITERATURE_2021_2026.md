# Biomedical statistical methods and R deployment: curated 2021–2026 reading

**Paul's Notes · reviewed 2026-10-22**  
[Data-first learning guide](../../03_learning/biomedical-statistics-decision-guide.md) · [Machine-readable source table](biostatistics_r_literature_2021_2026.csv) · [Existing biomedical evidence matrix](../../02_biomedical_coding/BIOMEDICAL_CODING_LITERATURE_MATRIX.md)

## Scope and method

A **curated narrative reading list**, focused on recent articles that help interpret variable types, choose appropriate statistical methods, implement analysis in R, and deliver reproducible scientific computing. Included below are **eight primary publications (2021–2025)** located from publisher/journal records, DOI metadata and article pages as of **2026-10-22**. It is **not** a systematic review, PRISMA search, clinical guideline, validation of paper code, exhaustive comparison of packages, or a claim that all studies are applicable to a particular population. No original patient data or third-party article content is stored here.

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

## Direct translation into the beginner's flowchart

1. **Data type first:** Continuous, count, nominal, ordinal and censored time-to-event require different distributions/estimands. **BS-001** motivates the initial t/rank/chi-square/Kruskal-Wallis split.
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
| Eight-row machine-readable register | Prepared; repository/CI validation should confirm structure and path integrity |
| Independent rerun of published papers | **Not performed** |
| Clinical study method sign-off, external validation, data admission | **Not performed / not conferred** |

Only add new references after checking source identity, DOI resolution, year, study type and relevance; add a clear entry about limitations. Keep references in this bounded beginner guide separate from the broad [biomedical coding corpus](../../02_biomedical_coding/README.md). Do not publish participant-linked records or unreviewed small-cell exports.
