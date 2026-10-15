# Official biomedical methods and specifications register

**Paul's Notes · Authoritative source directory**  
**Author:** Paul Skeffington · **Prepared with OpenAI**  
**Curated:** 2026-10-15 · **36 primary software, standards and methodological documentation entries**


This register is **separate from the peer-reviewed paper matrix** because programming manuals, federal methods guidance, interoperability specifications, and reporting standards serve different roles. Use the linked manuals and specifications to check method applicability, input contracts and software behavior.

A source is listed because its identified provider is the appropriate documentation authority, **not because the associated source code has passed modern runtime or study-level tests**. Versioned standards such as FHIR, OMOP, CDISC and vocabulary releases must be checked against their applicable implementation guide. Documentation links can change over time.

## Clinical and public-health data (7)

| ID | Authoritative provider document | Original source ID | Coding application | Required check | Scope limit |
| --- | --- | --- | --- | --- | --- |
| OFF-001 | [CDC NHANES datasets and documentation](https://wwwn.cdc.gov/nchs/nhanes/tutorials/datasets.aspx) · Federal technical guidance | `BIO-01` | Match variables to cycle-specific codebooks, component eligibility, file structure and documented missing-value conventions; verify joins and record counts | Verify data eligibility, identifiers, missingness and the stated source contract | Variable meaning and availability can change by cycle; do not guess from column names |
| OFF-002 | [CDC NHANES sample design](https://wwwn.cdc.gov/nchs/nhanes/tutorials/SampleDesign.aspx) · Federal survey methodology | `BIO-02` | Specify strata, primary sampling units and weights for population inference | Verify data eligibility, identifiers, missingness and the stated source contract | Treating a complex sample as an unweighted simple random sample can distort precision and estimates |
| OFF-003 | [CDC NHANES weighting](https://wwwn.cdc.gov/nchs/nhanes/tutorials/weighting.aspx) · Federal survey methodology | `BIO-03` | Select weights according to the smallest analytic subsample and the relevant collection component; handle combined cycles explicitly | Verify data eligibility, identifiers, missingness and the stated source contract | Interview weights are not interchangeable with exam or laboratory subsample weights |
| OFF-004 | [R survey package documentation](https://cran.r-project.org/package=survey) · Statistical software reference | `BIO-04` | Represent complex designs explicitly, then use survey-aware estimators rather than ordinary unweighted standard errors | Verify data eligibility, identifiers, missingness and the stated source contract | Inspect current version and variance-design assumptions; this does not validate questionnaire coding |
| OFF-005 | [Bioconductor SummarizedExperiment](https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html) · Primary software documentation | `BIO-05` | Keep assays, sample metadata and feature metadata aligned by stable identifiers | Verify data eligibility, identifiers, missingness and the stated source contract | Assay rows are usually features and columns samples; metadata reordering can silently corrupt interpretations |
| OFF-006 | [STROBE statement](https://www.strobe-statement.org/) · Observational-study reporting guideline | `BIO-10` | State study design, participant selection, variables, bias, statistical methods and limitations | Verify data eligibility, identifiers, missingness and the stated source contract | Reporting completeness does not establish causal validity |
| OFF-007 | [RECORD statement (EQUATOR)](https://www.equator-network.org/reporting-guidelines/record/) · Routinely collected health-data reporting guideline | `BIO-11` | Document data provenance, codes/algorithms, linkage, selection and availability | Verify data eligibility, identifiers, missingness and the stated source contract | RECORD is a reporting extension, not a substitute for legal/ethical permissions |

## Research engineering and regulated data (9)

| ID | Authoritative provider document | Original source ID | Coding application | Required check | Scope limit |
| --- | --- | --- | --- | --- | --- |
| OFF-008 | [NIH DMS Plan guidance](https://www.grants.nih.gov/policy-and-compliance/policy-topics/sharing-policies/dms/writing-dms-plan) · Federal policy implementation | `QA-02` | Describe data management, appropriate access and preservation before release | Plan names data categories, constraints, preservation and sharing strategy | Apply the current plan format only when the project is in policy scope |
| OFF-009 | [NCBI GEO high-throughput submissions](https://www.ncbi.nlm.nih.gov/geo/info/seq.html) · Federal repository instructions | `QA-04` | Retain biological sample, protocol and processed-data metadata; use safe, uniquely identified filenames | Unique sample and file inventory, protocol descriptions, identity checks | Requirements apply to GEO sequencing submissions, not every dataset |
| OFF-010 | [CDISC SDTM](https://www.cdisc.org/standards/foundational/sdtm) · Domain exchange standard | `QA-06` | Keep source observations distinct from standardized clinical trial tabulations | Explicit source-to-target mapping and schema version when SDTM applies | Never impose SDTM on unrelated public-health exploratory datasets |
| OFF-011 | [CDISC ADaM](https://www.cdisc.org/standards/foundational/adam) · Analysis data standard | `QA-07` | Document derivations and traceability from source to analysis datasets | Dataset spec distinguishes analysis variables and derivations | Applies to compatible clinical study analysis workflows |
| OFF-012 | [R packages manual](https://cran.r-project.org/doc/manuals/r-release/R-exts.html) · Primary development manual | `QA-08` | Document functions, input contracts and dependencies in reusable R software | Rebuild or check the package in an isolated supported session | Package-check success is not statistical truth |
| OFF-013 | [testthat reference](https://testthat.r-lib.org/) · Testing framework | `QA-09` | Test valid, missing, duplicate, and invalid-input cases; state what is asserted | A failure fixture rejects an invalid join or wrong unit | Assertions reproduce specified contracts only |
| OFF-014 | [renv](https://rstudio.github.io/renv/) · Dependency-management documentation | `QA-10` | Snapshot package versions and document restoration | Clean environment can restore declared package dependencies | Lockfiles do not freeze external APIs, OS or source data |
| OFF-015 | [Bioconductor developer contributions](https://contributions.bioconductor.org/) · Research-software engineering guidance | `QA-11` | Define assay/sample structures and maintain code/documentation quality | Sample IDs align with assay columns and metadata rows | Package-submission guidance is not automatically required for a course script |
| OFF-016 | [FDA Good Machine Learning Practice principles](https://www.fda.gov/medical-devices/artificial-intelligence-enabled-medical-devices/good-machine-learning-practice-medical-device-development-guiding-principles) · Medical-device AI guidance | `QA-16` | Define intended use, representative evaluation and postdeployment considerations | Intended-use statement, leakage checks, evaluation plan | Medical-device context; not blanket approval of student ML |

## R language and AI governance (2)

| ID | Authoritative provider document | Original source ID | Coding application | Required check | Scope limit |
| --- | --- | --- | --- | --- | --- |
| OFF-017 | [R Language Definition](https://cran.r-project.org/doc/manuals/r-release/R-lang.html) · Primary manual | `STD-03` | Type/indexing/NA semantics and evaluation | Test type, schema and implementation-specific assumptions | Does not validate a research design |
| OFF-018 | [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) · Voluntary risk framework | `STD-19` | Document AI risk, testing, monitoring, transparency and governance | Test type, schema and implementation-specific assumptions | Not a substitute for domain-specific clinical validation |

## Interoperability, identifiers and provenance (14)

| ID | Authoritative provider document | Original source ID | Coding application | Required check | Scope limit |
| --- | --- | --- | --- | --- | --- |
| OFF-019 | [UCUM specification](https://ucum.org/ucum) · Units coding standard | `INT-01` | Store an explicit coded unit alongside its quantitative value; validate dimensional compatibility before conversion | Validate mappings and required semantics against the pinned standard version | Machine-readable units require correct source interpretation and UCUM grammar, not string matching |
| OFF-020 | [LOINC overview](https://loinc.org/get-started/what-loinc-is/) · Observation terminology | `INT-02` | Separate laboratory/clinical observation identity from numeric result and unit | Validate mappings and required semantics against the pinned standard version | Selecting a LOINC code requires meaning, specimen, property, time and method context as relevant |
| OFF-021 | [FHIR R4 Observation](https://hl7.org/fhir/R4/observation.html) · Versioned interoperability resource | `INT-03` | Distinguish Observation.code, subject, effective time, status, value and unit in an interface | Validate mappings and required semantics against the pinned standard version | R4 is not interchangeable with later FHIR releases or jurisdiction-specific profiles |
| OFF-022 | [FHIR R4 Patient](https://hl7.org/fhir/R4/patient.html) · Versioned interoperability resource | `INT-04` | Preserve patient identity boundaries and references rather than substituting event IDs | Validate mappings and required semantics against the pinned standard version | Pseudonymized IDs still require privacy evaluation |
| OFF-023 | [FHIR R4 Specimen](https://hl7.org/fhir/R4/specimen.html) · Versioned interoperability resource | `INT-05` | Model specimen identity, collection, subject and sample relationships independently | Validate mappings and required semantics against the pinned standard version | Specimens are not one-to-one with encounters or subjects by default |
| OFF-024 | [OHDSI OMOP data model conventions](https://ohdsi.github.io/CommonDataModel/dataModelConventions.html) · Common data model conventions | `INT-06` | Keep person, visit, measurement, concept IDs and source vocabulary distinct | Validate mappings and required semantics against the pinned standard version | Require the exact deployed CDM version and ETL contract |
| OFF-025 | [OHDSI Athena vocabularies](https://athena.ohdsi.org/) · Vocabulary distribution | `INT-07` | Record the vocabulary and concept release used in each standardization | Validate mappings and required semantics against the pinned standard version | Mapping availability does not prove clinical equivalence or licensing for redistribution |
| OFF-026 | [SNOMED CT overview](https://www.snomed.org/what-is-snomed-ct) · Clinical terminology | `INT-08` | Use clinical concepts with explicit version and terminology scope | Validate mappings and required semantics against the pinned standard version | Licensing and jurisdictional access conditions may apply |
| OFF-027 | [HGNC guidelines](https://www.genenames.org/about/guidelines/) · Gene nomenclature authority | `INT-09` | Preserve approved symbols and stable identifiers; record alias resolution | Validate mappings and required semantics against the pinned standard version | Symbols can change and aliases can be ambiguous |
| OFF-028 | [NCBI Gene](https://www.ncbi.nlm.nih.gov/gene/) · Reference database | `INT-10` | Record taxon, accession or gene ID, and mapping provenance | Validate mappings and required semantics against the pinned standard version | Do not treat displayed symbols as globally unique identifiers |
| OFF-029 | [GA4GH Phenopackets](https://phenopacket-schema.readthedocs.io/en/latest/) · Phenotype data exchange schema | `INT-11` | Represent individual, phenotypic features, disease, biosamples and time context explicitly | Validate mappings and required semantics against the pinned standard version | Use a specified schema version and controlled ontology references |
| OFF-030 | [RO-Crate specification](https://www.researchobject.org/ro-crate/specification) · Research packaging specification | `INT-12` | Attach machine-readable metadata for datasets, files, authors, software and licenses | Validate mappings and required semantics against the pinned standard version | Current release/version must be recorded; metadata cannot grant absent rights |
| OFF-031 | [W3C PROV-O](https://www.w3.org/TR/prov-o/) · Provenance ontology | `INT-13` | Track entities, activities and agents behind transformations and outputs | Validate mappings and required semantics against the pinned standard version | Provenance records explain lineage, not scientific validity |
| OFF-032 | [DataCite Metadata Schema](https://schema.datacite.org/) · Citation and metadata standard | `INT-14` | Record creators, titles, dates, identifiers, versions and related resources | Validate mappings and required semantics against the pinned standard version | A DOI or citation does not authorize data redistribution |

## Machine-learning implementation guidance (4)

| ID | Authoritative provider document | Original source ID | Coding application | Required check | Scope limit |
| --- | --- | --- | --- | --- | --- |
| OFF-033 | [scikit-learn: common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) · Primary software manual | `ML-03` | Avoid inconsistent preprocessing and information leakage | Fit preprocessing *inside* each training fold; never fit a scaler or imputer on holdout data | Fit preprocessing *inside* each training fold; never fit a scaler or imputer on holdout data |
| OFF-034 | [scikit-learn: probability calibration](https://scikit-learn.org/stable/modules/calibration.html) · Primary software manual | `ML-04` | Calibration and discrimination answer distinct questions | Examine reliability curves and Brier score alongside AUROC and recall | Examine reliability curves and Brier score alongside AUROC and recall |
| OFF-035 | [tidymodels: resampling](https://rsample.tidymodels.org/) · Primary software manual | `ML-07` | Separate resampling specifications from fitting recipes | Demonstrate R-compatible resampling without sharing holdout information | Demonstrate R-compatible resampling without sharing holdout information |
| OFF-036 | [tidymodels: recipes](https://recipes.tidymodels.org/) · Primary software manual | `ML-08` | Declare feature preparation as explicit, estimable steps | Verify predictor selection, missingness and fold-specific preprocessing | Verify predictor selection, missingness and fold-specific preprocessing |

## Maintenance

The CSV records documentation URLs, version requirements and method-specific checks.

**Publication gate:** Revisit the authoritative provider URL, pin the relevant standard/software version and complete local unit/schema tests before upgrading any documented reference into a validated implementation. A statistical or clinical inference claim requires a separate study-level assessment.
