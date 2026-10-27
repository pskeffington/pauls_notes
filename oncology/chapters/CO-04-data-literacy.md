# CO-04 — Data Literacy: What Does One Row Represent?

*Computational Oncology: A Clinician–Scientist's Guide · Part I · Draft 0.1*  
[Book home](../README.md) · [CO-03: Molecular foundations](CO-03-molecular-foundations.md) · [CO-02: Clinical oncology data](CO-02-clinical-oncology-data.md) · [Independent Python lab](../examples/observation_grain.py)

## Why data literacy is a scientific skill

A cancer research dataset may look like a rectangular table, but its rows usually conceal a network of relationships: one person has multiple visits; one lesion produces multiple specimens; one specimen produces multiple molecular measurements; one trial records longitudinal outcomes and treatment changes. The apparent simplicity of a spreadsheet makes mistakes especially easy. A difference in the meaning of one row can change the denominator, inflate precision, create leakage or transform a biologically plausible hypothesis into an invalid conclusion.

Data literacy begins before statistics. It asks: *Who or what was observed? Why was it recorded? What does the number mean? Which comparisons are scientifically defensible?*

**Guiding question:** How can a researcher turn complex oncology records into correct, auditable units of analysis?

**Section references:** [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization) · [Kapoor and Narayanan: Data Leakage (2023)](https://doi.org/10.1016/j.patter.2023.100804)

## Learning objectives

Upon completing this chapter, the reader should be able to:
1. Identify the unit of observation, unit of independence, unit of assignment and unit of inference.
2. Construct a variable dictionary covering scale, units, level, missingness and provenance.
3. Distinguish continuous, ordinal, nominal, discrete-count and time-to-event outcomes.
4. Detect when joins multiply rows or break one-to-one constraints.
5. Define a study denominator and trace all inclusion and exclusion decisions.
6. Explain why participant-based data partitions are essential when predicting outcomes for new people.
7. Recognize common temporal leakage and selection mechanisms.
8. Run and interpret a minimal, dependency-free synthetic data-integrity lab.

**Section references:** [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/) · [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/)

## 1. Four units that must not be conflated

**Unit of observation:** The entity represented by a recorded row, such as a specimen, encounter or person-month.

**Unit of independence:** The level at which observations can reasonably be treated as statistically independent under the scientific model. Two specimens from one participant usually share important dependencies.

**Unit of assignment:** In an experiment, the level assigned to treatment, such as an individual patient, ward or hospital. In an observational study, exposure may be assigned by clinical practice rather than randomization.

**Unit of inference:** The population entity to which the result is intended to generalize, such as newly diagnosed patients or future biopsies.

These can differ. A randomized trial might assign hospitals, record patients and analyze repeated clinical visits. Treating every visit as an independently randomized unit would be incorrect.

A useful schematic:

```text
Study population (eligible people)
    |
    +-- Person A -- Visit 1 -- Specimen A1 -- Features
    |            \-- Visit 2 -- Specimen A2 -- Features
    |
    +-- Person B -- Visit 1 -- Specimen B1 -- Features
                 \-- Follow-up event and time
```

The lines express **relationships**, not a claim that every oncology system has the same database structure.

**Section references:** [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/) · [Kapoor and Narayanan: Data Leakage (2023)](https://doi.org/10.1016/j.patter.2023.100804)

## 2. How counts change with the question

Consider six independent people who contribute nine tissue specimens. Let `N_people = 6` and `N_specimens = 9`. If the question is the proportion of *patients* with a baseline assay result, the eligible patient count is the natural denominator. If the question is the fraction of *specimens* with sufficient sequencing quality, the specimen count may be appropriate.

An estimate based on nine rows can be valid for a specimen-level estimand while invalid for an independent-person estimand. Replication in the laboratory, multiple cells, multiple lesions and repeated visits can supply information without creating additional independent patients.

**Statistical consequence:** If correlated observations are analyzed as independent, reported uncertainty may be understated. The appropriate remedy depends on design: participant-level aggregation, clustered estimation, hierarchical models, repeated-measures methods or an explicitly justified sampling/weighting strategy. Blindly deleting duplicates is not a general solution.

**Section references:** [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization) · [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/)

## 3. Measurement scales and variable roles

| Type | Oncology example | Common mistake |
| --- | --- | --- |
| Continuous quantitative | Tumor diameter (mm), biomarker concentration, age (years) | Omit units or treat severely rounded values as exact |
| Discrete count | Number of admissions or observed mutation calls | Treat counts as continuous without modeling exposure and dispersion |
| Binary nominal | Event occurred: yes/no | Treat coded `0/1` as meaning an interval-scale clinical measure |
| Multicategory nominal | Anatomical site or tumor subtype | Impose an unjustified order |
| Ordinal | Toxicity grade or a staged severity category | Assume intervals between categories are equal |
| Time to event | Days from defined origin with event indicator | Discard censoring or confound time origins |
| Identifier | Patient or specimen code | Model ID numbers as quantitative biology |
| Date/time | Specimen collection, diagnosis, treatment initiation | Confuse event time, record entry time and extraction time |

A variable is not defined solely by its storage type. For example, `stage = 2` might be stored as an integer while representing a tumor-specific clinical classification. A missing symptom score is not necessarily a score of zero. Molecular raw read counts and normalized gene-expression values belong to different measurement scales.

A column can also change **role** across research questions. ER status might be an outcome in one validation study, an explanatory covariate in a prognosis model and a treatment-effect modifier in a randomized trial. A statistical method must be chosen for the intended question, not simply from the column name.

**Section references:** [Cancer Staging](https://www.cancer.gov/about-cancer/diagnosis-staging/staging) · [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/)

## 4. What a data dictionary must record

Every analysis-ready variable should have, at minimum:
- Stable variable name and descriptive label.
- Entity and granularity: person, lesion, specimen, visit, assay or event.
- Data type, allowed values, units and precision.
- Measurement protocol and date/time reference.
- Source table, system and provenance/processing version.
- Explicit codes for unknown, not applicable, excluded and missing where supported.
- Rule for derived variables, including inclusion/exclusion and denominator.
- Intended analytic role and any known limitations.

For example, the derived flag `baseline_assay_available` cannot simply mean “this person has any assay row.” It must specify the qualifying specimen type and time window. A result measured after treatment or after the outcome is not necessarily an eligible baseline predictor.

**Section references:** [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization) · [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/)

## 5. Keys, joins and record multiplicity

A **primary key** uniquely identifies rows within a table; the [GDC biospecimen data model](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/) illustrates how related case and specimen entities retain distinct identities. A **foreign key** links a child record to its parent. A join combines records based on these keys. When one parent has multiple children on each of two tables, a direct join may create a many-to-many multiplication.

Example:

- Person P01 has two specimens and three encounters.
- Joining specimen and encounter tables on person alone may create six records for P01.
- Those six records do not represent six independent patients or six actual linked specimen–encounter pairs.

**Join checklist:**
1. State the expected output grain before joining.
2. Check uniqueness of each supposed primary key.
3. Check that every foreign key belongs to a valid parent.
4. Test how many rows each parent contributes before and after the join.
5. Use an explicit time/window key when observations must be linked by visit or acquisition episode.
6. Report unmatched records rather than silently dropping them.
7. Recalculate expected denominators and trace changes.

In SQL, `COUNT(*)` answers how many rows remain; `COUNT(DISTINCT person_id)` answers how many distinct people are represented. Neither alone proves the join is correct.

**Section references:** [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/) · [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/)

## 6. Missingness is information about observation

Three common conceptual missing-data categories are:
- **MCAR:** the probability of missingness does not depend on observed or unobserved data under the defined model.
- **MAR:** missingness may depend on recorded variables but not on the unobserved value after conditioning on those variables.
- **MNAR:** missingness can still depend on unobserved values even after considering recorded variables.

These are modeling assumptions, not labels one can usually establish from a simple missingness table (see [Sterne et al. on clinical missing-data methods](https://pubmed.ncbi.nlm.nih.gov/19564179/)). Cancer cohorts often have informative measurement patterns: more ill patients may undergo more testing, and follow-up may differ across institutions. Complete-case analysis can change the study population and introduce bias.

Always distinguish a missing biomarker measurement, a failed assay, a clinically not-indicated test and a missing follow-up endpoint. A row with no event documentation is not automatically event-free. Record observation windows and why each record entered or left the analysis.

**Section references:** [Sterne et al., Missing Data (2009)](https://pubmed.ncbi.nlm.nih.gov/19564179/) · [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/)

## 7. Time, eligibility and information leakage

In oncology research, whether data occur **before** or **after** a specified origin can determine if they are appropriate predictors.

Suppose the research aim is to predict recurrence from measurements available at diagnosis. A genomic profile obtained after recurrence is not a valid baseline feature. Neither is a survival time, future treatment decision or post-progression assessment that would not have been known at prediction time.

A related problem occurs when splitting high-dimensional datasets into training and testing subsets. If multiple specimens from one patient cross the split boundary, apparent generalization may be contaminated by within-person similarities, consistent with the broader [scientific data-leakage literature](https://doi.org/10.1016/j.patter.2023.100804). Train/test separation should follow the intended generalization unit and pre-specified study design.

**Contrast:** A model intended to predict future *specimens from already-known people* may legitimately have a different design than one intended to generalize to entirely new patients. The validation scheme must match the claim.

**Section references:** [Kapoor and Narayanan: Data Leakage (2023)](https://doi.org/10.1016/j.patter.2023.100804) · [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/)

## 8. Worked lab: six invented people, nine specimens

The companion [Python fixture](../examples/observation_grain.py) uses six **invented** people and nine specimens, with multiple specimens for three people. Five of six have an available synthetic baseline assay. Four people belong to the development set and two are held out; every specimen inherits its owner's partition.

Run it with standard Python, no packages or downloads required:

```bash
python3 oncology/examples/observation_grain.py
```

Expected core counts:

| Metric | Expected |
| --- | ---: |
| Distinct people | 6 |
| Specimen records | 9 |
| People with qualifying baseline assay | 5 |
| Held-out people | 2 |
| People in both partitions | 0 |

The script validates specimen ID uniqueness, valid parent references, dates, boolean flags and partition names, and emits a transparent JSON summary. These are **engineering assertions** on a synthetic fixture, not a statistical result or clinical validation.

**Section references:** [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization) · [Kapoor and Narayanan: Data Leakage (2023)](https://doi.org/10.1016/j.patter.2023.100804)

### Hand calculation

The proportion of people with a baseline assay in this invented roster is `5 / 6`, approximately `0.833` (83.3%). It is not `8 / 9` or `5 / 9`, because the estimand is person-level availability. Conversely, the question “what fraction of nine specimen records have a successful assay?” requires specimen-level counting.

For a genuine study, even these simple descriptive proportions require a clear sampling frame and a defensible definition of eligibility; do not generalize them from this artificial exercise.

**Section references:** [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/) · [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/)

## 9. Worked design challenge: choosing the split

A researcher fits a model to classify tumors and proposes a random 80/20 split by specimen ID. The dataset contains repeated specimens from patients across multiple dates.

Before accepting this plan, require the investigator to state:
1. Whether the intended use is prediction for **new patients** or for additional specimens from **known patients**.
2. Whether both records from the same patient can appear across the split.
3. Which preprocessing steps (imputation, feature selection, scaling) are fitted only on training data.
4. Whether any feature was obtained after the prediction time.
5. Whether data come from several sites, and how site shifts will be evaluated.
6. Which held-out performance and uncertainty measures address the clinical estimand.

For new-patient prediction, a person-disjoint outer assessment is the baseline requirement; external-site or temporal testing may be necessary for stronger claims. A held-out test set does not alone prove transportability or clinical usefulness.

**Section references:** [Kapoor and Narayanan: Data Leakage (2023)](https://doi.org/10.1016/j.patter.2023.100804) · [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/)

## 10. Mastery exercises and answer guide

**Exercise A: Grain.** A study has 30 patients, 45 biopsies and 900 cellular measurements. State the three observation counts and select a valid independence unit for patient-level prediction.  
*Answer:* 30 people, 45 specimens, 900 measured cells; generalization to new people must account for dependence within people.

**Exercise B: Join.** Four patients each contribute two tissue rows and three encounter rows. What is the possible number of rows after a naive person-only join?  
*Answer:* `4 × 2 × 3 = 24`, though there are four people; a legitimate matched event join requires further keys or declared rules.

**Exercise C: Missingness.** Gene expression is missing more often after severe treatment toxicity. Why might complete-case analysis mislead?  
*Answer:* measurement inclusion is potentially linked to severity, changing the analyzed cohort and perhaps biasing outcome associations.

**Exercise D: Temporal leakage.** A baseline prognosis model includes a drug administered six months after diagnosis. What is wrong?  
*Answer:* future treatment information is not available at baseline and can induce misleading prediction or bias unless the question and design are reframed.

**Exercise E: Measurement.** Why should cancer stage stored as 1–4 not be treated automatically as a continuous exposure?  
*Answer:* the values encode disease-specific ordinal categories with nonuniform or unspecified distances.

**Exercise F: Defensibility.** Design one audit that would prevent specimen duplication from inflating participant counts.  
*Answer:* validate unique participant keys, specimen foreign keys, expected cardinality and distinct-person denominators before and after linkage.

**Section references:** [Sterne et al., Missing Data (2009)](https://pubmed.ncbi.nlm.nih.gov/19564179/) · [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/)

## 11. Primary and further reading

- NCI Genomic Data Commons. [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization). Documented case, sample, portion and aliquot relationships.
- NCI GDC. [Biospecimen Data](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/). Hierarchical entities and clinical versus assay file associations.
- Collins GS et al. *TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods.* BMJ (2024). [DOI:10.1136/bmj-2023-078378](https://doi.org/10.1136/bmj-2023-078378). Reporting guidance, not proof of model validation.
- [Paul's Notes: Data identifiers, keys and reshaping](../../03_learning/keys-and-reshaping.md) and [Missingness and comparisons](../../03_learning/missingness-and-comparisons.md). Complementary independently developed coding lessons.
- [Paul's Notes: Visual ML data-flow](../../04_machine_learning/visual-data-guide.md). Group-aware partitions and leakage considerations.

**Review status:** Draft 0.1 with invented teaching data, not scientific peer review or clinical certification. Demonstrations explain integrity concepts and do not license the use of participant data.

**Next:** [CO-05 — Essential Mathematics I](../ROADMAP.md), covering algebra, logarithms, rates and units through oncology examples.

**Section references:** [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/) · [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/)

