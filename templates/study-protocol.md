# Study protocol

Use the [cancer study-design chapter](../03_learning/bio_stats/CANCER_STUDY_DESIGN.md) for estimands, endpoints, sample size and event planning; use the [clinical-data chapter](../oncology/chapters/CO-02-clinical-oncology-data.md) for disease, assay and endpoint definitions. The [synthetic R design calculator](../03_learning/examples/breast_cancer_study_design.R) illustrates planning calculations.

Complete this record before inspecting outcome comparisons. A field without a justified answer remains an unresolved design decision. For a randomized trial, also use the complete [SPIRIT 2025 checklist](https://www.bmj.com/content/389/bmj-2024-081477); this local worksheet is a preparation aid, not that checklist or an approved clinical protocol.

## 1. Scientific question and intended claim

- Working title:
- Research question and objective:
- Descriptive, causal, prognostic or predictive aim:
- Population or experimental model and setting:
- Disease definition, histology, stage system/edition and relevant assay criteria:
- Intended use of the result and population to which it should apply:

## 2. Observation unit, data source and cohort

- Observation unit and repeated-measure structure:
- Independent sampling/randomization unit and grouping key:
- Person → diagnosis → specimen → assay/file identifiers and join cardinality:
- Data source, accession, release and permitted use:
- Source dictionary, extraction date, file manifest/checksums and transformation version:
- Inclusion, exclusion and duplicate-resolution rules:
- Specimen selection rule, collection time and handling of multiple eligible samples:
- Participant flow: source population, eligible, excluded with reasons, included, observed and analyzed counts:
- Analysis-specific intersections: participants with each required assay, covariate and endpoint:

## 3. Time, treatment and endpoint specification

Record these fields for every primary and secondary endpoint. Preserve original event components and dates even when the final analysis uses a single event indicator.

| Field | Study-specific specification |
| --- | --- |
| Exposure or intervention and comparator | Assignment or measurement rule; reference group; treatment start/stop dates |
| Eligibility and time zero | Eligibility date; allocation/exposure assessment; follow-up origin; any delayed entry |
| Baseline measurements | Permitted collection window relative to time zero and treatment |
| Endpoint | Exact definition, component events, scale and units; criterion/version; primary or secondary role |
| Assessment | Scheduled window, ascertainment source, blinded/adjudicated assessment and confirmation rules |
| Event record | Event type/date; date precision; handling of simultaneous or contradictory records |
| Follow-up record | Last known alive date; last adequate endpoint-free assessment; administrative cutoff |
| Censoring and competing events | Endpoint-specific rule and rationale for each event; competing-death handling |
| Denominator | Eligible analysis population; evaluability requirements; repeated observations |

## 4. Estimand and unavailable outcomes

- Target quantity, effect scale, contrast direction and time horizon:
- Population and treatment conditions to which that quantity applies:
- Each intercurrent event and its strategy: treatment policy, composite, hypothetical, while on treatment or principal stratum, where applicable:
- Missing-data strategy: distinguish absent measurements from intercurrent events; record reasons, timing and by-group counts:
- Assumptions supporting the estimator and sensitivity analyses targeting the same estimand:
- Supplementary analyses that change the endpoint or analyzed population, labeled accordingly:

Use [ICH E9(R1), final FDA guidance (May 2021), §A.3–A.5](https://www.fda.gov/media/148473/download) to distinguish the estimand, estimator and missing-data assumptions. A missing pathology result is not evidence of pathological nonresponse. Any documented-response composite must be named and justified explicitly.

## 5. Sample size and primary analysis

- Sample-size rationale and feasibility:
- Assumed effect, control distribution/variance, source and clinically meaningful threshold:
- Alpha, sidedness, target power/precision, allocation, accrual and follow-up:
- Required analyzable participants, pairs or events; enrollment inflation and its assumptions:
- Planning formula/software/version; sensitivity scenarios for weaker effects and greater missingness:
- Confounders, batch and anticipated bias:
- Primary analysis, model assumptions and diagnostics:
- Multiplicity family and adjustment:

## 6. Prediction and validation, when applicable

- Training, tuning and evaluation split, if applicable:
- Patient/site/time grouping; preprocessing and feature selection within training folds:
- Information available at prediction time; outcome-leakage exclusions:
- Prespecified discrimination, calibration, threshold and clinical-use evaluation targets:
- Independent validation population and uncertainty method:

## 7. Reporting, reproducibility and review

- Sensitivity analyses and subgroup limitations:
- Dependencies and reproducibility commands:
- Output and disclosure checks:
- Tables/figures and corresponding [scientific reporting standards](../03_learning/bio_stats/SCIENTIFIC_STATISTICAL_REPORTING_STANDARDS.md):
- Source, numeric, code execution, render and scientific-review evidence, recorded separately:
- Ethics/access review, prospective registration where applicable, and responsible reviewers:

## 8. Version and deviations

- Date, version and deviations from this plan:
- Decisions frozen before outcome access; deviations with date, reason and effect on interpretation:
- Outstanding design questions and owner for each resolution:

[Workflow](../docs/research-workflow.md) · [Data dictionary](data-dictionary.md) · [Analysis record](analysis-record.md)
