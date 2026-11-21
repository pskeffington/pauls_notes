# CO-02 — Clinical Oncology Data: From Care to Research Variables

*Computational Oncology: A Clinician–Scientist's Guide · Part I · Draft 0.2*
[Book home](../README.md) · [Introduction](../INTRODUCTION.md) · [CO-01: Cancer biology](CO-01-cancer-biology.md) · [Roadmap](../ROADMAP.md)

## Why clinical data matter

An oncology record does not begin as a research table. It begins as care delivered over time: symptoms are evaluated, diagnoses are revised, specimens are collected, stage is documented, therapies are prescribed and administered, imaging is interpreted, toxicity is monitored, and outcomes are observed or remain unknown. Transforming that process into analyzable data is an intellectual and clinical task, not merely a programming task.

A single word such as *response* may refer to a radiographic category, a laboratory marker, a pathologic finding, a patient-reported change, or a clinician's judgment. A numerical field such as `stage = 3` may refer to different disease-specific staging systems or editions, while a missing value may mean no test was ordered, the test was not available, or the value was not abstracted. Without definitions, computation can be perfectly reproducible and scientifically misleading.

**Guiding question:** How do we represent a person's cancer care as research data without changing the meaning of what was observed?

**Section references:** [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/) · [Cancer Staging](https://www.cancer.gov/about-cancer/diagnosis-staging/staging)

## Learning objectives

The reader should be able to:
1. Distinguish patients, diagnoses, tumors/lesions, specimens, encounters, therapies and observations.
2. Explain stage versus grade and why classification-system edition, time and tumor site matter.
3. Differentiate an imaging response category, a clinical event, an adverse event and a patient-reported outcome.
4. Define time origins, events, censoring, competing events and a study's analysis population.
5. Draft a minimal data dictionary with keys, cardinality, units, allowed values, provenance and missingness.
6. Detect duplicate joins, time-order violations, denominator changes and common interpretation errors.
7. Identify when controlled or protected clinical data require separate authorization and cannot enter a public educational repository.

**Section references:** [Cancer Staging](https://www.cancer.gov/about-cancer/diagnosis-staging/staging) · [CTCAE and Adverse Event Reporting](https://dctd.cancer.gov/research/ctep-trials/for-sites/adverse-events)

## 1. The clinical timeline precedes the data model

Consider a person diagnosed with breast cancer. A diagnostic biopsy may occur before definitive staging; a molecular result may become available later; a first treatment may start later still. A follow-up scan may be completed at another institution. The record might also contain prior cancers, multiple lesions, additional lines of treatment and incomplete follow-up.

A research question determines which timeline is relevant. For example, measuring overall survival *from diagnosis* is different from measuring survival *from initiation of second-line therapy*. An analysis that labels both as `survival_months` obscures a major scientific difference.

Every clinically defined time-to-event endpoint requires at least five documented elements:

- **Population:** whose follow-up contributes to the estimate?
- **Time origin:** the precise date or eligibility event at which the clock begins.
- **Event definition:** what is counted, and how is it adjudicated?
- **Observation process:** how and when outcome status is ascertained.
- **Competing and censoring rules:** what happens for loss to follow-up, administrative closure or another event that changes the possibility of observing the event of interest?

The same person may contribute multiple episodes to an explicitly defined recurrent-event analysis, but the episodes are not automatically independent individuals.

**Section references:** [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/) · [Overall Survival (NCI Dictionary)](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/overall-survival)

## 2. Separate the clinical entities

| Entity | Example primary key | Typical relationship | Research meaning |
| --- | --- | --- | --- |
| Person | `person_id` | One person → multiple diagnoses or encounters | Participant-level denominator and clustering unit |
| Diagnosis | `diagnosis_id` | Diagnosis linked to a person | Disease site, histology, diagnosis date, initial stage |
| Tumor / lesion | `lesion_id` | Multiple lesions can belong to one diagnosis | Target lesion, site and longitudinal measurement |
| Specimen | `specimen_id` | Multiple collections per lesion or person | Collection site/time, tissue source, assay eligibility |
| Encounter | `encounter_id` | Multiple visits per person | Care context and observation timing |
| Regimen / treatment | `treatment_id` | Multiple regimens, cycles and administrations | Exposure definition and time-varying history |
| Assessment | `assessment_id` | Repeated scans, tests and evaluations | Measurements and prespecified response categorization |
| Adverse event | `adverse_event_id` | Multiple events with onset, severity and attribution | Safety outcome, distinct from efficacy |
| Follow-up endpoint | `endpoint_id` | Defined analysis record per relevant episode | Time origin, event, last known ascertainment |

This is an illustrative normalized schema, not a claim that all electronic health records or cancer registries have precisely these tables. A well-designed research extract can have fewer tables, provided its variable meanings and multiplicities remain explicit.

**Cardinality matters.** Joining six people to three treatment administrations each produces up to 18 administration rows. Counting those rows as 18 participants is incorrect. If an outcome is person-level, choose the analysis grain deliberately before joining.

**Section references:** [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization) · [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/)

### 2.1. Preserve the patient-to-assay hierarchy

In TCGA, participant, sample, portion, analyte and aliquot identifiers describe different levels of specimen processing. A file is a digital product associated with that lineage. The [GDC barcode documentation](https://docs.gdc.cancer.gov/Encyclopedia/pages/TCGA_Barcode/) explains the hierarchy and identifies UUIDs as primary identifiers; a human-readable barcode remains useful for interpretation. Preserve both identifiers where supplied, with the source relationships. A shortened barcode is not a substitute for verifying the submitted lineage.

Before creating an analysis table, state its intended grain: one row per participant, specimen, lesion or observation. Record the number of distinct identifiers at each retained level. For a participant-level analysis, prespecify how multiple eligible specimens are handled; options might include a defined baseline specimen or an explicitly paired analysis. The choice follows the biological question and collection history. Selecting the first available filename does not define a biological sampling rule.

Consider an invented study with six participants, two tissue specimens per participant and two assay files per specimen. It contains 24 files, 12 specimens and six participants. A paired tumor–normal contrast has at most six participant pairs, provided the specimen identities and pairing are verified. The file count supplies neither 24 independent participants nor 24 independent treatment assignments. If the target is prediction in new participants, the related records must remain together across training and evaluation sets.

**Section references:** [TCGA Barcode](https://docs.gdc.cancer.gov/Encyclopedia/pages/TCGA_Barcode/) · [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization) · [Kapoor and Narayanan: Data Leakage (2023)](https://doi.org/10.1016/j.patter.2023.100804)

## 3. Stage, grade, histology and molecular classification

**Stage** generally characterizes extent of disease; many solid tumors use TNM-related systems, but staging is disease-specific and some cancers use other systems ([NCI cancer staging](https://www.cancer.gov/about-cancer/diagnosis-staging/staging)). **Grade** typically characterizes histologic or cellular differentiation or aggressiveness according to a particular grading framework. Neither should be treated as a simple continuous number merely because it is encoded numerically.

A strong staging record preserves `cancer_site`, `stage_system`, `stage_edition`, `stage_group`, `stage_basis` (for example, clinical or pathological when applicable) and `stage_assessed_at`. Stage at initial diagnosis is not synonymous with disease burden measured after recurrence or progression. NCI explains why an original diagnostic stage remains distinct from subsequent changes in disease extent.

An example oncology dataset might contain:
- **Histology:** nominal categorical diagnosis, encoded with a documented vocabulary.
- **Grade:** ordinal or otherwise categorical according to its disease-specific rules.
- **Stage group:** ordered clinical classification but not a measurement with equal numeric distances.
- **ER or HER2 status:** a biomarker finding from a specified assay, site, specimen and date.
- **Treatment:** an exposure history, not a single permanent patient attribute.

Do not calculate a mean of stage categories as though the differences between stage I and II and between III and IV have equal scientific meaning.

**Section references:** [Cancer Staging](https://www.cancer.gov/about-cancer/diagnosis-staging/staging) · [Tumor Grade](https://www.cancer.gov/about-cancer/diagnosis-staging/diagnosis/tumor-grade)

### 3.1. Keep breast cancer receptor findings and molecular subtypes distinct

A breast cancer study may contain pathology-based receptor results, expression-based molecular assignments and quantitative molecular measurements. These are separate variables. The [original TCGA breast cancer analysis](https://doi.org/10.1038/nature11412) demonstrated that clinical HER2 positivity and the HER2-enriched expression subtype do not identify identical groups. Consequently, a label such as `subtype` needs a definition, assay or classifier, specimen and assessment time.

| Research variable | Information to retain | Interpretation boundary |
| --- | --- | --- |
| ER and progesterone receptor by immunohistochemistry (IHC) | Percentage of stained tumor nuclei, staining intensity when available, interpretation, controls, specimen and guideline version | A receptor result is not an RNA-expression value |
| HER2 by IHC and in situ hybridization (ISH) | IHC score, ISH result when performed, final interpretation, assay and specimen | Preserve an equivocal or unresolved result; do not silently recode it as negative |
| Intrinsic expression subtype | Classifier name/version, input platform, preprocessing, source label and specimen | A HER2-enriched assignment is not a replacement for clinical HER2 testing |
| Individual gene measurement | Gene identifier, assay, units, normalization and sample identity | An ESR1 or ERBB2 expression threshold requires its own justification |

Under the [2020 ASCO/CAP ER/PgR guideline](https://ascopubs.org/doi/10.1200/JCO.19.02309), 1%–100% nuclear staining is interpreted as positive; invasive cancers with 1%–10% ER staining have the specific ER Low Positive reporting category. That category should not be automatically applied to PgR. A research dictionary should preserve the percentage and reported interpretation so that any later grouping remains reproducible.

Interpretation must also retain its date and purpose. The [2023 ASCO/CAP HER2 update](https://www.cap.org/cap-guidelines/her2-testing-in-breast-cancer-2023-guideline-update/) affirmed the existing testing algorithm and did not introduce a HER2-low interpretive category. Separately, a [January 2025 FDA approval](https://www.fda.gov/drugs/cancer-approvals/fda-approves-fam-trastuzumab-deruxtecan-nxki-unresectable-or-metastatic-hr-positive-her2-low-or-her2) used HER2-low and HER2-ultralow eligibility definitions in a specified advanced-disease setting. These distinct uses make a single undated `HER2_positive` flag inadequate for reproducing all research groupings; retain the underlying test results and the exact grouping rule.

**Section references:** [Estrogen and Progesterone Receptor Testing in Breast Cancer: ASCO/CAP Guideline Update (2020)](https://ascopubs.org/doi/10.1200/JCO.19.02309) · [HER2 Testing in Breast Cancer: ASCO/CAP Guideline Update (2023)](https://www.cap.org/cap-guidelines/her2-testing-in-breast-cancer-2023-guideline-update/) · [FDA approval: HR-positive, HER2-low or HER2-ultralow breast cancer (January 2025)](https://www.fda.gov/drugs/cancer-approvals/fda-approves-fam-trastuzumab-deruxtecan-nxki-unresectable-or-metastatic-hr-positive-her2-low-or-her2) · [Comprehensive molecular portraits of human breast tumours (2012)](https://doi.org/10.1038/nature11412)

## 4. Response and toxicity are different constructs

For selected solid-tumor research settings, RECIST 1.1 provides standardized imaging-response rules ([original RECIST 1.1 guideline](https://pubmed.ncbi.nlm.nih.gov/19097774/)). However, not all diseases, therapies or studies use RECIST; immune-based treatments and hematologic diseases may require different prespecified systems. A recorded `partial_response` is meaningful only when the criterion, assessment date, baseline and adjudication approach are known.

**Objective response rate (ORR)** generally requires a protocol-defined numerator and analysis population, often complete plus partial responders under the chosen system; requirements such as confirmation, measurable disease and handling of missing assessment must be written into the protocol. A response proportion is not interchangeable with overall survival or durable benefit.

**Adverse events (AEs)** describe unwanted medical occurrences and are not automatically caused by treatment. The NCI Common Terminology Criteria for Adverse Events (CTCAE) standardizes descriptions and severity grades in oncology research. As of this edition, NCI lists CTCAE **version 6.0** in its [current adverse-event guidance](https://dctd.cancer.gov/research/ctep-trials/for-sites/adverse-events); a study must retain the version actually used, and a conversion between v5.0 and v6.0 is not simply a renaming operation.

Patient-reported outcomes capture another dimension, often including symptoms or functioning. They should not be folded into a clinician-graded toxicity field without a justified measurement mapping.

| Field | Correct research question | Common mistake |
| --- | --- | --- |
| Radiographic category | Was the patient classified as responding under criterion X at time Y? | Treat any reduction in a lesion measurement as a standardized response |
| Adverse-event grade | What severity was recorded using terminology version Z? | Treat grade as proof of treatment causality |
| Patient-reported symptom | What experience did the patient report with instrument Q? | Substitute a clinician's note for an instrument score |
| Vital status | Was death ascertained by the specified cutoff? | Treat absent death documentation as evidence of survival |
| Progression | Did the protocol-defined progression event occur? | Treat every imaging change as objective progression |

**Section references:** [RECIST 1.1: Revised Response Evaluation Criteria (2009)](https://pubmed.ncbi.nlm.nih.gov/19097774/) · [CTCAE and Adverse Event Reporting](https://dctd.cancer.gov/research/ctep-trials/for-sites/adverse-events)

## 5. Endpoint semantics and the denominator

Common oncology endpoints include overall survival (OS), progression-free survival (PFS), disease-free survival (DFS), event-free survival (EFS), time to recurrence, treatment response and toxicity incidence. These names are not permission to assume identical definitions across studies. A protocol must say exactly what counts as an event, what time origin applies, and which patients are eligible.

**Overall survival** commonly uses death from any cause as its event, with time measured from a prespecified origin ([NCI overall-survival definition](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/overall-survival)). **Progression-free survival** commonly incorporates progression or death, but exact criteria, ascertainment and sensitivity analyses are protocol-specific. **DFS** and **EFS** can vary substantially by malignancy and intervention.

For right-censored data we may store `time` plus `event` for a given estimand, with `event = 1` for a defined event and `event = 0` for a censored observation. This two-field representation is not sufficient to answer every competing-risk, interval-censoring or multi-state question. If death precludes the recurrence of interest, the treatment of death must be justified rather than silently coded as ordinary noninformative censoring.

**Immortal-time warning:** defining the exposed group using a treatment that could only be received after surviving to a later date, then analyzing survival from an earlier origin as if exposure existed from the start, creates a structural bias. Represent treatment start and eligibility times explicitly.

**Section references:** [Overall Survival (NCI Dictionary)](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/overall-survival) · [Immortal time bias in observational studies of drug effects (2007)](https://pubmed.ncbi.nlm.nih.gov/17252614/)

### 5.1. Define breast cancer endpoints before selecting a model

Breast cancer endpoint standards distinguish the treatment setting, starting point and qualifying events. [STEEP 2.0](https://pmc.ncbi.nlm.nih.gov/articles/PMC10166345/) addresses adjuvant trials; [NeoSTEEP](https://pmc.ncbi.nlm.nih.gov/articles/PMC10522109/) addresses neoadjuvant trials. Use the chosen standard and protocol together when constructing the outcome variable.

| Endpoint | Definition to preserve | Required study information |
| --- | --- | --- |
| Pathologic complete response (pCR) | NeoSTEEP prefers `ypT0/Tis ypN0`: no residual invasive cancer in the resected breast or sampled regional nodes; residual in situ disease in the breast is allowed | Surgery/pathology assessment, breast and nodal findings, analysis population and rules for missing surgery or assessment |
| Residual cancer burden (RCB) | Retain the continuous score and, when used, its defined class; NeoSTEEP recommends its collection as a secondary endpoint when feasible | Calculation method, pathology inputs, specimen and assessment timing |
| Invasive disease-free survival (IDFS) | STEEP includes invasive breast recurrence, contralateral invasive breast cancer, second nonbreast invasive primary cancer and death from any cause | Prespecified origin, event components, first qualifying event and ascertainment/censoring rules |
| Invasive breast cancer-free survival (IBCFS) | STEEP 2.0 excludes second nonbreast invasive primary cancers from the IDFS event set | Exact event-component mapping; retain the IBCFS name |
| Event-free survival (EFS) in a neoadjuvant trial | Define events from random assignment, including relevant presurgery progression and deaths | Randomization date and events before as well as after surgery |

For pCR, a breast-only response field cannot establish the combined breast-and-node endpoint. A stricter definition excluding residual in situ disease must be named and prespecified. NeoSTEEP also classifies absent surgery or inadequate final pathology as non-pCR for its trial endpoint; this prespecified classification does not establish an unobserved biological response. For time-to-event outcomes, starting follow-up at surgery would omit the earlier risk period that a randomization-based EFS estimand is intended to capture. These distinctions change the analysis dataset before any regression function is selected.

Write the endpoint specification as a short operational paragraph: eligible population; time origin or assessment window; positive event definition; source and adjudication; censoring or competing-event rules; and missing-outcome strategy. Then connect it to the [cancer study-design chapter](../../03_learning/bio_stats/CANCER_STUDY_DESIGN.md) and [statistical reporting standards](../../03_learning/bio_stats/SCIENTIFIC_STATISTICAL_REPORTING_STANDARDS.md). A familiar acronym alone is insufficient documentation.

**Section references:** [Updated Standardized Definitions for Efficacy End Points: STEEP Version 2.0 (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10166345/) · [Standardized Definitions for Efficacy End Points in Neoadjuvant Breast Cancer Clinical Trials: NeoSTEEP (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10522109/) · [Pathological Complete Response in Neoadjuvant Treatment of High-Risk Early-Stage Breast Cancer (2020)](https://www.fda.gov/media/83507/download) · [ICH E9(R1): Estimands and Sensitivity Analysis, Final FDA Guidance (May 2021)](https://www.fda.gov/media/148473/download)

## 6. A minimum clinical oncology research dictionary

The following is a fictional teaching schema, not a universal EHR export standard:

| Variable | Type / unit | Definition and validation |
| --- | --- | --- |
| `person_id` | character ID | Unique per invented person; never convert to a continuous predictor |
| `diagnosis_id` | character ID | Unique diagnosis; must link to a valid person |
| `diagnosis_date` | ISO date | Document time zone/date conventions and precision |
| `diagnosis_site` | categorical | Versioned anatomical vocabulary and values |
| `stage_group` | categorical | Versioned staging system and assessment basis required |
| `specimen_id` | character ID | One specimen per specimen row; link to person/lesion |
| `specimen_date` | ISO date | May precede finalized diagnosis documentation |
| `baseline_assessment_date` | ISO date | Defines analysis eligibility where appropriate |
| `treatment_start_date` | ISO date or missing | Start of a specified regimen, not a lifetime ever/never flag |
| `event_date` | ISO date or missing | Valid only together with endpoint definition |
| `last_contact_date` | ISO date | Final ascertainment; not assumed to be event-free without review |
| `endpoint_type` | categorical | For example, OS; do not mix endpoint types in one unlabelled model |

Missingness codes should distinguish truly unknown, not applicable, not collected, pending and intentionally withheld where source information supports those distinctions. Do not invent reasons for absent measurements.

Each research release must include provenance: source system, extraction date, codebook version, transformation history, access classification and eligibility rules.

**Section references:** [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/) · [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/)

### 6.1. Match the breast cancer dataset to the scientific question

Dataset selection follows the required measurements and outcomes. The table distinguishes the data products that are often described collectively as “the breast cancer data.” It is a source-to-question assessment; no participant records have been downloaded or admitted by this chapter.

| Data product | What it supplies | Appropriate starting use and missing requirements |
| --- | --- | --- |
| GDC clinical and biospecimen exports | Clinical annotations and specimen relationships for the selected cases | Inventory variables, assess missingness and define cohort membership; these exports alone are not gene-expression measurements |
| GDC file manifest | Identifiers of selected downloadable files | Reproduce file selection and retrieval; a manifest is not the contents of those files |
| TCGA-BRCA assay files with linked metadata | Measurements of the selected molecular modality | Molecular analysis after verifying file type, workflow, identifiers and sample selection; clinical JSON does not supply the corresponding RNA-seq matrix |
| TCGA Pan-Cancer Clinical Data Resource (TCGA-CDR) | Publication-specific, curated clinical endpoints, including OS, PFI, DFI and DSS | Endpoint-based molecular research after checking derivation, eligibility, follow-up and version |
| Wisconsin Diagnostic Breast Cancer (WDBC) | 569 diagnostic instances with 30 features derived from breast-mass fine-needle aspirate images and a benign/malignant target | Diagnostic-feature description and classification; the documented schema lacks treatment histories and time-to-event follow-up |

The first three distinctions follow the [GDC repository documentation](https://docs.gdc.cancer.gov/Data_Portal/Users_Guide/Repository/) and [mRNA pipeline specification](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/). For RNA-seq work, record the chosen count or normalized-expression field, annotation and workflow; the availability of an expression file does not make its columns interchangeable. The same candidate cohort can yield different usable sample counts for different assays.

[Liu et al. (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6066282/) recommended PFI and DFI for the evaluated BRCA cohort and advised caution with OS and DSS because of follow-up limitations. That historical recommendation does not certify a newly extracted subset. Their PFI includes specified new tumor events or death with tumor; it must not be renamed trial PFS. Their DFI construction requires evidence that initial treatment rendered the patient disease-free. Record the curated release and derivation instead of inferring either endpoint from a generic vital-status field.

The [UCI WDBC record](https://archive.ics.uci.edu/dataset/17/breast-cancer-wisconsin-data-set) documents diagnostic morphometric features, not sequencing data. A Kaplan–Meier analysis, treatment-response comparison or ESR1 expression study therefore requires another source with those variables. WDBC is also distinct from the [Wisconsin prognostic dataset](https://www.archive.ics.uci.edu/dataset/16/breast%2Bcancer%2Bwisconsin%2Bprognostic); identify the exact dataset and DOI. For either WDBC or TCGA, inspect the actual schema, source terms and eligibility before selecting a statistical test. Use the repository's [research workflow](../../docs/research-workflow.md) for the separate data-access and provenance review.

**Section references:** [GDC Repository and Download Products](https://docs.gdc.cancer.gov/Data_Portal/Users_Guide/Repository/) · [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/) · [An Integrated TCGA Pan-Cancer Clinical Data Resource to Drive High-Quality Survival Outcome Analytics (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6066282/) · [Breast Cancer Wisconsin (Diagnostic), DOI:10.24432/C5DW2B](https://archive.ics.uci.edu/dataset/17/breast-cancer-wisconsin-data-set) · [Breast Cancer Wisconsin (Prognostic), DOI:10.24432/C5GK50](https://www.archive.ics.uci.edu/dataset/16/breast%2Bcancer%2Bwisconsin%2Bprognostic)

## 7. Worked example: a teaching extract with related records

Imagine an invented cohort with **8 people, 12 specimens and 20 encounters**. The analysis asks: among the eight eligible people, how many have a recorded baseline assay? A specimen table and an encounter table cannot be joined indiscriminately to count people.

A robust sequence is:
1. Verify that each `person_id` appears once in the person table.
2. Verify that each specimen belongs to one valid person and that specimen IDs are unique.
3. Define what counts as a baseline assay, including time relative to the analysis origin.
4. Create a one-row-per-person baseline eligibility indicator by an explicitly justified rule.
5. Join that person-level indicator to the participant roster with an expected row count of eight.
6. Report the number of eligible people with a documented assay, not the number of assay or encounter rows.

**Section references:** [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization) · [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/)

### Compact R demonstration

The following base-R example is synthetic and does not contact any external service:

```r
people <- data.frame(person_id = sprintf("P%02d", 1:8))
samples <- data.frame(
  specimen_id = sprintf("S%02d", 1:12),
  person_id = c(sprintf("P%02d", 1:8), sprintf("P%02d", 1:4)),
  baseline = c(rep(TRUE, 8), rep(FALSE, 4))
)
stopifnot(!anyDuplicated(people$person_id),
          !anyDuplicated(samples$specimen_id),
          all(samples$person_id %in% people$person_id))
has_baseline <- unique(samples$person_id[samples$baseline])
people$baseline_assay <- people$person_id %in% has_baseline
stopifnot(nrow(people) == 8L, sum(people$baseline_assay) == 8L)

# Deliberate error: joining all specimens increases the row count.
joined <- merge(people, samples, by = "person_id")
stopifnot(nrow(joined) == 12L, length(unique(joined$person_id)) == 8L)
```

This example checks **join cardinality**, not a cancer treatment outcome. An assay being present does not imply clinical validity, and a passing `stopifnot` is a code assertion rather than scientific proof.

**Section references:** [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/) · [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/)

### 7.1. Worked planning example: account for every analysis denominator

Suppose an invented breast cancer study has 12 eligible participants. Ten have a recorded baseline assay; eight have sufficient follow-up information for a separately specified endpoint; seven have both. These values are a constructed set example, not measurements from WDBC or TCGA.

Let $A$ denote participants with an eligible assay and $F$ those with the required follow-up. Then

$$
|A|=10,\qquad |F|=8,\qquad |A\cap F|=7,\qquad
|A\cup F|=10+8-7=11.
$$

The assay-only group contains three participants, the follow-up-only group contains one, and one has neither. The joint-analysis denominator is therefore seven; replacing it with 10 or 12 would misstate who contributes to that particular analysis. Seven complete records also do not establish that complete-case analysis answers the intended population question; the missing-data assessment remains part of the design.

The resulting cohort record should show the 12-person eligibility roster, the 10-person assay subset, the eight-person endpoint subset and their seven-person intersection. Exclusions need stated reasons, and each table or figure needs its applicable denominator. If the question changes to baseline assay availability, all 12 eligible people again form the relevant denominator.

This example demonstrates the bookkeeping needed before a molecular–outcome analysis. It does not supply enough information to fit a survival model: the endpoint definition, event indicators, elapsed times and assumptions must still be specified. The [missing-data chapter](../../03_learning/missingness-and-comparisons.md) develops the observation process, while the [analysis record](../../templates/analysis-record.md) preserves the decisions made for a particular study.

**Section references:** [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/) · [Sterne et al., Missing Data (2009)](https://pubmed.ncbi.nlm.nih.gov/19564179/)

## 8. Research governance

Patient-linked clinical records may contain direct or indirect identifiers and may be subject to privacy, institutional, contractual and consent restrictions. Publicly available documentation about a data source does not authorize exporting its restricted data. Prefer fabricated teaching fixtures. Any real oncology research dataset requires project-specific review of access rights, acceptable use, retention, disclosure and de-identification before ingestion or publication.

A distinction central to this book: **a model that can read a record is not necessarily permitted to retain, transmit or index it.** The same applies to embedding pipelines, search indexes and machine-generated research summaries.

**Section references:** [HIPAA and Research](https://www.hhs.gov/hipaa/for-professionals/special-topics/research/index.html) · [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization)

## 9. Competency exercises and answer checks

1. **Classification:** Explain why grade, stage and tumor size cannot be substituted for one another. *Check:* distinguish histologic features, extent of disease and measured size, plus scheme/version and time.
2. **Cardinality:** Eight patients have 12 specimens and 20 encounters. Identify three legitimate denominators. *Check:* patients = 8, specimens = 12, encounters = 20, each tied to its own question.
3. **Time origin:** Two studies start OS clocks at diagnosis versus treatment initiation. Are their survival times directly interchangeable? *Check:* no; eligibility, time zero and treatment selection differ.
4. **Safety:** Is a grade 3 AE necessarily caused by study therapy? *Check:* no; severity and attribution are distinct.
5. **Protocol design:** A paper reports ORR without specifying response criteria or the denominator. What must be requested? *Check:* response system/version, imaging rules, evaluable population, assessment/confirmation and missingness rules.
6. **Data debugging:** A specimen-level table is joined to an event table by `person_id` and the number of event rows doubles. What should be verified? *Check:* keys, event grain, duplicate matches and intended estimand before deduplication.
7. **Dataset suitability:** Can the documented WDBC table estimate five-year recurrence? *Check:* no event times or recurrence follow-up are supplied; diagnostic status is a different outcome.
8. **Endpoint definition:** A post-treatment breast specimen has no invasive tumor but a sampled regional node contains invasive disease. Does it satisfy NeoSTEEP's preferred pCR definition? *Check:* no; both the breast and sampled nodes must meet the definition.
9. **Label provenance:** Is a HER2-enriched expression assignment sufficient to replace an absent clinical HER2 result? *Check:* no; preserve the classifier result and missing clinical assay separately.
10. **Analysis population:** Reconstruct the four mutually exclusive groups in the 12-person planning example. *Check:* seven with both requirements, three with assay only, one with follow-up only and one with neither; their sum is 12.

**Section references:** [RECIST 1.1: Revised Response Evaluation Criteria (2009)](https://pubmed.ncbi.nlm.nih.gov/19097774/) · [Cancer Staging](https://www.cancer.gov/about-cancer/diagnosis-staging/staging) · [Breast Cancer Wisconsin (Diagnostic), DOI:10.24432/C5DW2B](https://archive.ics.uci.edu/dataset/17/breast-cancer-wisconsin-data-set) · [Standardized Definitions for Efficacy End Points in Neoadjuvant Breast Cancer Clinical Trials: NeoSTEEP (2023)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10522109/) · [Comprehensive molecular portraits of human breast tumours (2012)](https://doi.org/10.1038/nature11412)

## 10. Core sources and further reading

- National Cancer Institute. [Cancer Staging](https://www.cancer.gov/about-cancer/diagnosis-staging/staging) and [Tumor Grade](https://www.cancer.gov/about-cancer/diagnosis-staging/diagnosis/tumor-grade). Distinct constructs and disease-specific context.
- Eisenhauer EA et al. *New response evaluation criteria in solid tumours: revised RECIST guideline (version 1.1).* European Journal of Cancer (2009). [DOI:10.1016/j.ejca.2008.10.026](https://doi.org/10.1016/j.ejca.2008.10.026). Use the original full guideline for exact trial protocol details.
- NCI. [Imaging Response Criteria for Clinical Trials](https://dctd.cancer.gov/research/research-areas/imaging/resources/response-criteria). Summarizes multiple response frameworks and appropriate context.
- NCI. [CTCAE and Adverse Event Reporting](https://dctd.cancer.gov/research/ctep-trials/for-sites/adverse-events). Current resource and version documentation.
- NCI GDC. [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization). Case-to-sample lineage and specimen metadata.
- NCI. [TCGA Data Types Collected](https://www.cancer.gov/ccg/research/genome-sequencing/tcga/using-tcga-data/types). Illustrates clinical, molecular and biospecimen data with access distinctions.

**Review record:** Draft 0.2; original synthesis and invented teaching examples. The breast cancer endpoint, receptor and data-product sources added in this revision were checked on November 21, 2026. The cohort-set arithmetic is explicit; no new participant-data analysis or clinical validation is claimed. Earlier material retains its October 2026 source-review scope. Independent clinical expert review remains pending.

**Next:** [CO-03 — Molecular Foundations](CO-03-molecular-foundations.md).

**Section references:** [CTCAE and Adverse Event Reporting](https://dctd.cancer.gov/research/ctep-trials/for-sites/adverse-events) · [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization)

