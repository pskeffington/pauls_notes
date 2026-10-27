# Source Library — Computational Oncology

[Book home](../README.md) · [Evidence policy](README.md) · [Machine-readable registry](source-registry.json) · [Section citation map](section-citations.json)

This bibliography groups external scientific and technical references used in the current introduction and CO-01 through CO-06. **A citation establishes traceability, not independent scientific review of each claim.** Original explanations and synthetic exercises are authored separately from source materials.

## Foundational oncology and epidemiology

| Reference ID | Direct linked source | Relevance |
| --- | --- | --- |
| `NCI-CANCER` | [What Is Cancer?](https://www.cancer.gov/about-cancer/understanding/what-is-cancer) | Cancer mechanisms, variation and basic tumor biology |
| `NCI-TRIALS` | [Clinical Trials Programs and Initiatives](https://www.cancer.gov/research/infrastructure/clinical-trials) | Research purpose, intervention evaluation and translation |
| `NCI-STATS` | [Cancer Statistics](https://www.cancer.gov/about-cancer/understanding/statistics) | Incidence, mortality, population denominators and limitations |
| `SEER-INCIDENCE` | [SEER: Cancer Incidence Rates](https://seer.cancer.gov/statistics/types/incidence.html) | Distinguishes new cancer counts, population-based incidence rates, age adjustment and population definitions |
| `SEER-STAT-TYPES` | [SEER: Defining Cancer Statistics](https://seer.cancer.gov/statistics/types.html) | Incidence, mortality, prevalence, survival and lifetime-risk measures are distinct |
| `CDC-RATE` | [CDC: Principles of Epidemiology, Frequency Measures](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section1.html) | Ratio versus proportion and rate; event numerator and population denominator |
| `CDC-PERSONTIME` | [CDC: Principles of Epidemiology, Measures of Risk](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section2.html) | Incidence proportion versus person-time incidence rate and denominator requirements |

## Clinical definitions and endpoints

| Reference ID | Direct linked source | Relevance |
| --- | --- | --- |
| `NCI-STAGE` | [Cancer Staging](https://www.cancer.gov/about-cancer/diagnosis-staging/staging) | Stage, TNM systems and extent of disease |
| `NCI-GRADE` | [Tumor Grade](https://www.cancer.gov/about-cancer/diagnosis-staging/diagnosis/tumor-grade) | Grade versus stage and histological classification |
| `NCI-BIOMARKER` | [Biomarker Testing for Cancer Treatment](https://www.cancer.gov/about-cancer/treatment/types/biomarker-testing-cancer-treatment) | Molecular tumor testing, use cases and limitations |
| `NCI-BREAST` | [Tests for Breast Cancer Biomarkers](https://www.cancer.gov/types/breast/diagnosis/breast-cancer-biomarker-tests) | ER, PR, HER2 assays and clinical biomarker context |
| `NCI-CTCAE` | [CTCAE and Adverse Event Reporting](https://dctd.cancer.gov/research/ctep-trials/for-sites/adverse-events) | Adverse event grading, attribution and CTCAE release |
| `NCI-OS` | [Overall Survival (NCI Dictionary)](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/overall-survival) | Time origin and overall survival endpoint |

## Biomarker terminology

| Reference ID | Direct linked source | Relevance |
| --- | --- | --- |
| `FDA-BEST` | [About Biomarkers and Qualification / BEST](https://www.fda.gov/drugs/biomarker-qualification-program/about-biomarkers-and-qualification) | Biomarker definition, predictive versus prognostic roles |
| `FDA-BEST-BOOK` | [BEST Biomarkers, EndpointS, and other Tools](https://www.ncbi.nlm.nih.gov/books/NBK326791/) | Biomarker classification and measurement context |

## Data, measurement and scientific computing

| Reference ID | Direct linked source | Relevance |
| --- | --- | --- |
| `GDC-BIO` | [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization) | Case, sample, analyte, aliquot relationships and provenance |
| `GDC-ENTITY` | [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/) | Biospecimen hierarchy and assay data associations |
| `GDC-RNA` | [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/) | RNA read counts, transforms, sequence processing |
| `NIST-CONVERSION` | [NIST: Unit Conversion](https://www.nist.gov/pml/owm/metric-si/unit-conversion) | Unit conversions, conversion factors, dimensional checks, significant digits and final rounding |
| `NIST-SI` | [NIST: Writing with SI Units](https://www.nist.gov/pml/owm/writing-si-metric-system-units) | Proper SI unit notation, precision and communication conventions |
| `NIST-OLS` | [NIST: Linear Least Squares Regression](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm) | Linear-in-parameters regression formulation and least-squares fitting |
| `BIOC-SE` | [Bioconductor: SummarizedExperiment Assay Structure](https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html) | Features as rows, samples as columns, coordinated sample and feature metadata |
| `R-MATMULT` | [R Base: Matrix Multiplication](https://stat.ethz.ch/R-manual/R-devel/library/base/html/matmult.html) | Conformable numeric matrices, dot products and matrix multiplication in R |
| `R-QR` | [R Base: QR Decomposition and qr.solve](https://stat.ethz.ch/R-manual/R-devel/library/base/html/qr.html) | QR regression fitting, rank/linear dependence and numerical stability |

## Independent calculus and applied mathematics

| Reference ID | Direct linked source | Relevance |
| --- | --- | --- |
| `MATH-DERIV` | [Calculus I: Derivatives as Rates of Change](https://openstax.org/books/calculus-volume-1/pages/3-4-derivatives-as-rates-of-change) | Difference quotients, analytic derivatives and time-rate interpretation |
| `MATH-GRAD` | [Calculus III: Directional Derivatives and the Gradient](https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient) | Partial derivatives, gradients and multivariate directions of change |
| `MATH-QUAD` | [Calculus II: Numerical Integration](https://openstax.org/books/calculus-volume-2/pages/3-6-numerical-integration) | Trapezoidal approximation and the distinction between an integral and discrete observations |

## Cancer biology reviews

| Reference ID | Direct linked source | Relevance |
| --- | --- | --- |
| `HALLMARKS` | [Hallmarks of Cancer: New Dimensions (2022)](https://doi.org/10.1158/2159-8290.CD-21-1059) | Hallmark framework, microenvironment and tumor evolution |

## Statistical and machine-learning methods

| Reference ID | Direct linked source | Relevance |
| --- | --- | --- |
| `DESEQ2` | [Love et al., DESeq2 (2014)](https://doi.org/10.1186/s13059-014-0550-8) | RNA-seq count models, dispersion, log-fold changes |
| `LEAKAGE` | [Kapoor and Narayanan: Data Leakage (2023)](https://doi.org/10.1016/j.patter.2023.100804) | Data leakage, independence and validation failures |
| `MISSING` | [Sterne et al., Missing Data (2009)](https://pubmed.ncbi.nlm.nih.gov/19564179/) | Missingness assumptions and clinical multiple imputation pitfalls |

## Methodological guidance

| Reference ID | Direct linked source | Relevance |
| --- | --- | --- |
| `RECIST` | [RECIST 1.1: Revised Response Evaluation Criteria (2009)](https://pubmed.ncbi.nlm.nih.gov/19097774/) | Solid tumor imaging response assessment |

## Research reporting

| Reference ID | Direct linked source | Relevance |
| --- | --- | --- |
| `TRIPOD-AI` | [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/) | Prediction-model reporting and transparency |
| `STROBE` | [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/) | Observational study design, transparent reporting |

## Research privacy and authorization

| Reference ID | Direct linked source | Relevance |
| --- | --- | --- |
| `HHS-RESEARCH` | [HIPAA and Research](https://www.hhs.gov/hipaa/for-professionals/special-topics/research/index.html) | Research disclosures, privacy conditions and authorizations |

## Scholarly publication

| Reference ID | Direct linked source | Relevance |
| --- | --- | --- |
| `ICMJE` | [ICMJE Recommendations (2026)](https://icmje.org/recommendations/) | Medical research writing, reporting and source responsibility |

## Verification and release boundary

The listed URLs have been inspected for subject suitability in the October 2026 manuscript work, but availability, source version, clinical interpretation, publication rights and suitability for any specific claim require independent review before chapter release. The course examples are fabricated and no protected or patient-level records are stored here.
