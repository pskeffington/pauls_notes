# CO-02 — Clinical Oncology Data: From Care to Research Variables

*Computational Oncology: A Clinician–Scientist's Guide · Part I · Draft 0.1*  
[Book home](../README.md) · [Introduction](../INTRODUCTION.md) · [CO-01: Cancer biology](CO-01-cancer-biology.md) · [Roadmap](../ROADMAP.md)

## Why clinical data matter

An oncology record does not begin as a research table. It begins as care delivered over time: symptoms are evaluated, diagnoses are revised, specimens are collected, stage is documented, therapies are prescribed and administered, imaging is interpreted, toxicity is monitored, and outcomes are observed or remain unknown. Transforming that process into analyzable data is an intellectual and clinical task, not merely a programming task.

A single word such as *response* may refer to a radiographic category, a laboratory marker, a pathologic finding, a patient-reported change, or a clinician's judgment. A numerical field such as `stage = 3` may refer to different disease-specific staging systems or editions, while a missing value may mean no test was ordered, the test was not available, or the value was not abstracted. Without definitions, computation can be perfectly reproducible and scientifically misleading.

**Guiding question:** How do we represent a person's cancer care as research data without changing the meaning of what was observed?

## Learning objectives

The reader should be able to:
1. Distinguish patients, diagnoses, tumors/lesions, specimens, encounters, therapies and observations.
2. Explain stage versus grade and why classification-system edition, time and tumor site matter.
3. Differentiate an imaging response category, a clinical event, an adverse event and a patient-reported outcome.
4. Define time origins, events, censoring, competing events and a study's analysis population.
5. Draft a minimal data dictionary with keys, cardinality, units, allowed values, provenance and missingness.
6. Detect duplicate joins, time-order violations, denominator changes and common interpretation errors.
7. Identify when controlled or protected clinical data require separate authorization and cannot enter a public educational repository.

## 1. The clinical timeline precedes the data model

Consider a person diagnosed with lung cancer. A diagnostic biopsy may occur before definitive staging; a molecular result may become available later; a first treatment may start later still. A follow-up scan may be completed at another institution. The record might also contain prior cancers, multiple lesions, additional lines of treatment and incomplete follow-up.

A research question determines which timeline is relevant. For example, measuring overall survival *from diagnosis* is different from measuring survival *from initiation of second-line therapy*. An analysis that labels both as `survival_months` obscures a major scientific difference.

We should document at least five elements for every clinically defined time-to-event endpoint:

- **Population:** whose follow-up contributes to the estimate?
- **Time origin:** the precise date or eligibility event at which the clock begins.
- **Event definition:** what is counted, and how is it adjudicated?
- **Observation process:** how and when outcome status is ascertained.
- **Competing and censoring rules:** what happens for loss to follow-up, administrative closure or another event that changes the possibility of observing the event of interest?

The same person may contribute multiple episodes to an explicitly defined recurrent-event analysis, but the episodes are not automatically independent individuals.

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

## 3. Stage, grade, histology and molecular classification

**Stage** generally characterizes extent of disease; many solid tumors use TNM-related systems, but staging is disease-specific and some cancers use other systems. **Grade** typically characterizes histologic or cellular differentiation or aggressiveness according to a particular grading framework. Neither should be treated as a simple continuous number merely because it is encoded numerically.

A strong staging record preserves `cancer_site`, `stage_system`, `stage_edition`, `stage_group`, `stage_basis` (for example, clinical or pathological when applicable) and `stage_assessed_at`. Stage at initial diagnosis is not synonymous with disease burden measured after recurrence or progression. NCI explains why an original diagnostic stage remains distinct from subsequent changes in disease extent.

An example oncology dataset might contain:
- **Histology:** nominal categorical diagnosis, encoded with a documented vocabulary.
- **Grade:** ordinal or otherwise categorical according to its disease-specific rules.
- **Stage group:** ordered clinical classification but not a measurement with equal numeric distances.
- **ER or HER2 status:** a biomarker finding from a specified assay, site, specimen and date.
- **Treatment:** an exposure history, not a single permanent patient attribute.

Do not calculate a mean of stage categories as though the differences between stage I and II and between III and IV have equal scientific meaning.

## 4. Response and toxicity are different constructs

For selected solid-tumor research settings, RECIST 1.1 provides standardized imaging-response rules. However, not all diseases, therapies or studies use RECIST; immune-based treatments and hematologic diseases may require different prespecified systems. A recorded `partial_response` is meaningful only when the criterion, assessment date, baseline and adjudication approach are known.

**Objective response rate (ORR)** generally requires a protocol-defined numerator and analysis population, often complete plus partial responders under the chosen system; requirements such as confirmation, measurable disease and handling of missing assessment must be written into the protocol. A response proportion is not interchangeable with overall survival or durable benefit.

**Adverse events (AEs)** describe unwanted medical occurrences and are not automatically caused by treatment. The NCI Common Terminology Criteria for Adverse Events (CTCAE) standardizes descriptions and severity grades in oncology research. As of this edition, NCI lists CTCAE **version 6.0**; a study must retain the version actually used, and a conversion between v5.0 and v6.0 is not simply a renaming operation.

Patient-reported outcomes capture another dimension, often including symptoms or functioning. They should not be folded into a clinician-graded toxicity field without a justified measurement mapping.

| Field | Correct research question | Common mistake |
| --- | --- | --- |
| Radiographic category | Was the patient classified as responding under criterion X at time Y? | Treat any reduction in a lesion measurement as a standardized response |
| Adverse-event grade | What severity was recorded using terminology version Z? | Treat grade as proof of treatment causality |
| Patient-reported symptom | What experience did the patient report with instrument Q? | Substitute a clinician's note for an instrument score |
| Vital status | Was death ascertained by the specified cutoff? | Treat absent death documentation as evidence of survival |
| Progression | Did the protocol-defined progression event occur? | Treat every imaging change as objective progression |

## 5. Endpoint semantics and the denominator

Common oncology endpoints include overall survival (OS), progression-free survival (PFS), disease-free survival (DFS), event-free survival (EFS), time to recurrence, treatment response and toxicity incidence. These names are not permission to assume identical definitions across studies. A protocol must say exactly what counts as an event, what time origin applies, and which patients are eligible.

**Overall survival** commonly uses death from any cause as its event, with time measured from a prespecified origin. **Progression-free survival** commonly incorporates progression or death, but exact criteria, ascertainment and sensitivity analyses are protocol-specific. **DFS** and **EFS** can vary substantially by malignancy and intervention.

For right-censored data we may store `time` plus `event` for a given estimand, with `event = 1` for a defined event and `event = 0` for a censored observation. This two-field representation is not sufficient to answer every competing-risk, interval-censoring or multi-state question. If death precludes the recurrence of interest, the treatment of death must be justified rather than silently coded as ordinary noninformative censoring.

**Immortal-time warning:** defining the exposed group using a treatment that could only be received after surviving to a later date, then analyzing survival from an earlier origin as if exposure existed from the start, creates a structural bias. Represent treatment start and eligibility times explicitly.

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

## 7. Worked example: a teaching extract with related records

Imagine an invented cohort with **8 people, 12 specimens and 20 encounters**. The analysis asks: among the eight eligible people, how many have a recorded baseline assay? A specimen table and an encounter table cannot be joined indiscriminately to count people.

A robust sequence is:
1. Verify that each `person_id` appears once in the person table.
2. Verify that each specimen belongs to one valid person and that specimen IDs are unique.
3. Define what counts as a baseline assay, including time relative to the analysis origin.
4. Create a one-row-per-person baseline eligibility indicator by an explicitly justified rule.
5. Join that person-level indicator to the participant roster with an expected row count of eight.
6. Report the number of eligible people with a documented assay, not the number of assay or encounter rows.

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

## 8. Research governance

Patient-linked clinical records may contain direct or indirect identifiers and may be subject to privacy, institutional, contractual and consent restrictions. Publicly available documentation about a data source does not authorize exporting its restricted data. Prefer fabricated teaching fixtures. Any real oncology research dataset requires project-specific review of access rights, acceptable use, retention, disclosure and de-identification before ingestion or publication.

A distinction central to this book: **a model that can read a record is not necessarily permitted to retain, transmit or index it.** The same applies to embedding pipelines, search indexes and machine-generated research summaries.

## 9. Competency exercises and answer checks

1. **Classification:** Explain why grade, stage and tumor size cannot be substituted for one another. *Check:* distinguish histologic features, extent of disease and measured size, plus scheme/version and time.
2. **Cardinality:** Eight patients have 12 specimens and 20 encounters. Identify three legitimate denominators. *Check:* patients = 8, specimens = 12, encounters = 20, each tied to its own question.
3. **Time origin:** Two studies start OS clocks at diagnosis versus treatment initiation. Are their survival times directly interchangeable? *Check:* no; eligibility, time zero and treatment selection differ.
4. **Safety:** Is a grade 3 AE necessarily caused by study therapy? *Check:* no; severity and attribution are distinct.
5. **Protocol design:** A paper reports ORR without specifying response criteria or the denominator. What must be requested? *Check:* response system/version, imaging rules, evaluable population, assessment/confirmation and missingness rules.
6. **Data debugging:** A specimen-level table is joined to an event table by `person_id` and the number of event rows doubles. What should be verified? *Check:* keys, event grain, duplicate matches and intended estimand before deduplication.

## 10. Core sources and further reading

- National Cancer Institute. [Cancer Staging](https://www.cancer.gov/about-cancer/diagnosis-staging/staging) and [Tumor Grade](https://www.cancer.gov/about-cancer/diagnosis-staging/diagnosis/tumor-grade). Distinct constructs and disease-specific context.
- Eisenhauer EA et al. *New response evaluation criteria in solid tumours: revised RECIST guideline (version 1.1).* European Journal of Cancer (2009). [DOI:10.1016/j.ejca.2008.10.026](https://doi.org/10.1016/j.ejca.2008.10.026). Use the original full guideline for exact trial protocol details.
- NCI. [Imaging Response Criteria for Clinical Trials](https://dctd.cancer.gov/research/research-areas/imaging/resources/response-criteria). Summarizes multiple response frameworks and appropriate context.
- NCI. [CTCAE and Adverse Event Reporting](https://dctd.cancer.gov/research/ctep-trials/for-sites/adverse-events). Current resource and version documentation.
- NCI GDC. [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization). Case-to-sample lineage and specimen metadata.
- NCI. [TCGA Data Types Collected](https://www.cancer.gov/ccg/research/genome-sequencing/tcga/using-tcga-data/types). Illustrates clinical, molecular and biospecimen data with access distinctions.

**Review record:** Draft 0.1; original synthesis and invented teaching example. Source links checked during October 2026 authoring; exact practice is disease-, protocol- and edition-specific. No clinical validation or independent expert peer review has been completed.

**Next:** [CO-03 — Molecular Foundations](CO-03-molecular-foundations.md).
