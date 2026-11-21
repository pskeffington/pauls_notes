# CO-04 — Data Literacy: What Does One Row Represent?

*Computational Oncology: A Clinician–Scientist's Guide · Part I · Draft 0.2*

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

| Relationship | Possible multiplicity | What must remain identifiable |
| --- | --- | --- |
| Participant to visit | One participant may have several recorded visits | Participant key and visit key |
| Participant to specimen | One participant may contribute several specimens | Participant key and specimen key |
| Specimen to assay product | One specimen may produce several measurements or files | Specimen lineage and assay/file identifier |
| Participant to endpoint record | Depends on the endpoint and whether episodes recur | Endpoint definition, episode, origin and event/ascertainment time |

These are role-level relationships, not a universal database schema. A direct specimen-to-visit link must be established from the source; it does not follow merely because both records name the same participant.

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

### 4.1. A concrete dictionary for the six-person teaching extract

The [existing Python lab](../examples/observation_grain.py) provides a deliberately small breast cancer research-data exercise: six invented participants, nine specimens and nine visit records. It is separate from the 80-person response example in the [data-science introduction](../../03_learning/INTRODUCTION_TO_DATA_SCIENCE.md); no treatment outcomes are imported into this exercise. The scientific question here is **baseline assay availability among the six roster members**.

| Table or output | One row represents | Primary key | Relationship to retain |
| --- | --- | --- | --- |
| Participant roster (`PERSON_IDS`) | An eligible invented participant | `person_id` | Defines the six-person denominator |
| Specimen records (`SAMPLES`) | A collection | `specimen_id` | Each `person_id` refers to one roster member |
| Visit records (`VISITS`) | A recorded encounter | `visit_id` | Each `person_id` refers to one roster member |
| Baseline participant table | One roster member and the selected baseline specimen, if present | `person_id` | Zero or one selected specimen per participant |

The field dictionary makes the selection rule and missing states explicit:

| Field | Table / type | Definition and allowed values | Missingness and validation |
| --- | --- | --- | --- |
| `person_id` | Roster and child tables / string | Invented participant identifier, P01–P06 in this fixture; no measurement unit | Nonblank and unique in the roster; nonblank child references must resolve |
| `specimen_id` | Specimens / string | Unique collection identifier, S01–S09 | Nonblank string required; duplicate specimen keys are rejected |
| `visit_id` | Visits / string | Unique recorded-visit identifier, V01–V09 | Nonblank string required in source visits; `None` in linked output means no matching visit row |
| `date` | Specimens / `YYYY-MM-DD` string | Collection date; day precision | Required valid calendar date in this exact format; not a diagnosis or survival origin |
| `date` | Visits / `YYYY-MM-DD` string | Encounter date; day precision | Required valid calendar date in this exact format; `(person_id, date)` must be unique for this exercise's linkage rule |
| `baseline` | Specimens / Boolean | `True` selects the stipulated 2025-01-10 baseline collection; `False` identifies a later collection | No missing flags; multiple qualifying baseline specimens stop selection |
| `assay_available` | Specimens / Boolean | A recorded assay is available (`True`) or unavailable (`False`) | `False` does not identify the reason for unavailability or imply a biological result |
| `baseline_specimen_id` | Participant output / string or `None` | Identifier of the uniquely selected baseline specimen | `None` means no eligible specimen was present |
| `baseline_assay_available` | Participant output / Boolean or `None` | Copies availability from that selected specimen | `None` means no eligible specimen; it remains distinct from recorded `False` |

All dates and flags are authored teaching values. There is no clinical time-to-event endpoint in these records. The fixed baseline date is a selection convention for the exercise, not a proposed clinical schedule. Preserve the two meanings of `date` when exporting or joining tables; a shared column name does not establish a shared event.

The lab applies a strict input contract: every source identifier, including each parent reference, must be a nonblank string. Source dates must use the canonical `YYYY-MM-DD` representation. Compact dates such as `20250110`, week-date forms and invalid dates are rejected before matching. This prevents alternate spellings of the same day from appearing as different join keys or bypassing the participant-date uniqueness check. The lab does not silently repair or normalize source values.

The [GDC Data Dictionary](https://docs.gdc.cancer.gov/Data_Dictionary/) illustrates the broader need to document entities, keys, links, types and permissible values. Use the [data-dictionary template](../../templates/data-dictionary.md) to record those decisions for a real study, including source release, measurement units, temporal reference and derivation. The simplified tables above are original teaching records, not a copy of the GDC schema.

**Section references:** [GDC Data Dictionary](https://docs.gdc.cancer.gov/Data_Dictionary/) · [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/)

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

### 5.1. A person-only join changes the table and the population

Suppose the investigator attempts to attach encounter information to each specimen by matching `person_id` alone. An inner join emits every matching specimen–visit combination and excludes specimens with no matching visit. This is standard [relational join behavior](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN), but it does not implement the intended collection-to-encounter relationship.

The lab's inputs give the following hand calculation. Let $s_i$ and $v_i$ denote specimen and visit counts for participant $i$.

| Participant | Specimens, $s_i$ | Visit records, $v_i$ | Rows after person-only inner join, $s_i v_i$ |
| --- | ---: | ---: | ---: |
| P01 | 2 | 3 | 6 |
| P02 | 2 | 2 | 4 |
| P03 | 1 | 1 | 1 |
| P04 | 2 | 2 | 4 |
| P05 | 1 | 1 | 1 |
| P06 | 1 | 0 | 0 |
| **Total** | **9** | **9** | **16** |

Thus $\sum_i s_i v_i=6+4+1+4+1+0=16$, even though only six participants entered the study. P01's two specimens are each copied three times. P06 disappears because the visit extract contains no row for that participant. The absence of a visit record does not establish that no clinical encounter occurred.

This error changes more than the apparent sample size. In the original roster, five of six participants have an available baseline assay. Among the five people retained by the incorrect inner join, four have one. Reporting $4/5=80\%$ would describe that selected subset; the original question requires $5/6\approx83.3\%$. Neither counting 16 rows nor retaining five distinct IDs repairs the missing participant. If the multiplied rows entered an analysis, participants with more specimen–visit combinations would contribute repeated information unless the analysis explicitly accounted for that structure.

**Section references:** [PostgreSQL: joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN) · [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/)

### 5.2. Repair the join by declaring the retained grain

For this exercise, retain **one row per specimen**. The invented data collection rule states that an eligible visit has the same participant and calendar date as the collection, with at most one visit per participant-date. The implementation checks that rule before performing a specimen-left-join. In actual research, same-day dates alone may be insufficient; use a verified collection/encounter identifier or a separately justified matching rule. An ambiguous match should remain unresolved rather than being settled by file order.

The expected links can be inspected individually:

| Specimen | Participant | Collection date | Matched visit |
| --- | --- | --- | --- |
| S01 | P01 | 2025-01-10 | V01 |
| S02 | P02 | 2025-01-10 | V04 |
| S03 | P03 | 2025-01-10 | V06 |
| S04 | P04 | 2025-01-10 | V07 |
| S05 | P05 | 2025-01-10 | V09 |
| S06 | P06 | 2025-01-10 | No matching visit row |
| S07 | P01 | 2025-03-01 | V02 |
| S08 | P02 | 2025-03-15 | V05 |
| S09 | P04 | 2025-04-01 | V08 |

The repaired table has nine specimen rows, eight matched visits and all six participants. Visit V03, P01 on 2025-06-01, has no same-date specimen and is reported separately as unused. This is not an orphaned participant reference: V03 still belongs to a valid roster member. S06 remains in the specimen table with `visit_id=None`; its recorded assay availability remains `True`.

The participant-level question requires one additional, declared operation. `baseline_person_rows()` selects the unique specimen marked `baseline=True` and attaches it to every roster member. It rejects multiple eligible specimens instead of choosing one arbitrarily. If a participant has no eligible baseline specimen, that participant remains in the output with `None` for the selected specimen and its availability. The original fixture produces six participant rows and five `True` availability values; P05's recorded `False` remains different from an absent baseline specimen.

A left join preserves unmatched left records; it does not by itself prevent multiplication when several right records match. Here, the validated right-hand `(person_id, date)` key makes the specimen-preserving result possible. The two contracts—what is matched and what is retained—must both be stated.

**Section references:** [PostgreSQL: joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN) · [GDC Data Dictionary](https://docs.gdc.cancer.gov/Data_Dictionary/)

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

The proportion of people with a baseline assay in this invented roster is `5 / 6`, approximately `0.833` (83.3%). It is not `8 / 9` or `5 / 9`, because the estimand is person-level availability. Conversely, “what fraction of nine specimen records have an available assay?” gives `8 / 9`, approximately 88.9%, and answers a specimen-level question. Availability alone does not establish assay validity or a clinical result.

For a genuine study, even these simple descriptive proportions require a clear sampling frame and a defensible definition of eligibility; do not generalize them from this artificial exercise.

**Section references:** [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/) · [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/)

### Executable checks and expected linkage output

The default command above retains the original JSON summary. To inspect the join demonstration and run its numerical and invalid-input checks:

```bash
python3 oncology/examples/observation_grain.py --join-demo
python3 oncology/examples/observation_grain.py --check
```

| Output | Expected result |
| --- | --- |
| Incorrect person-only inner join | 16 rows, five distinct people; P06 excluded |
| Baseline assays among people retained by that join | Four of five |
| Repaired specimen-left-join | Nine specimen rows, six distinct people |
| Unmatched specimen / unused visit | S06 / V03, reported separately |
| Participant baseline table | Six rows; five available assays |

The checks verify the original fixture summary, all nine specific visit matches, the hand-counted products, and retention when the visit table is empty. Negative cases reject duplicate specimen IDs, duplicate visit IDs, references to absent participants, ambiguous visit keys and multiple eligible baseline specimens. They also reject blank, null or nonstring identifiers in every source-key role; noncanonical, missing or impossible dates; and a second same-day visit disguised by compact date formatting. A separate check removes one baseline specimen and confirms that the participant remains with an explicit missing-selection state. These bounded checks establish the implemented teaching contracts; study-specific scientific selection rules still require justification.

**Section references:** [GDC Data Dictionary](https://docs.gdc.cancer.gov/Data_Dictionary/) · [PostgreSQL: joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)

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

**Exercise G: Unmatched records.** S06 has no matched visit; P05's selected specimen has `assay_available=False`. Are these the same missing-data state?

*Answer:* no. S06 has a recorded available assay and an unresolved visit link. P05 has a selected specimen with explicitly unavailable assay data. Neither state supplies an unrecorded clinical reason.

**Exercise H: Ambiguous matches.** A second visit for P01 on 2025-01-10 appears with a different visit ID. Why should the repair stop?

*Answer:* the participant-date key is no longer unique. A left join would duplicate S01, and taking the first visit would invent a linkage decision. Obtain a stronger key or an explicit source-supported rule.

**Exercise I: Baseline selection.** S06 is removed from the specimen extract. How many rows should the participant availability table retain?

*Answer:* six, because eligibility is defined by the roster. P06 has no selected baseline specimen and a `None` availability state. Report that state rather than dropping the participant or claiming an observed assay failure.

**Exercise J: Denominator recovery.** Why is `COUNT(DISTINCT person_id)` after the incorrect inner join insufficient to recover the original availability estimate?

*Answer:* it counts only the five retained participants. The lost P06 record must be reconciled against the six-person roster; only then can the original five-of-six availability count be reconstructed.

**Section references:** [Sterne et al., Missing Data (2009)](https://pubmed.ncbi.nlm.nih.gov/19564179/) · [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/) · [GDC Data Dictionary](https://docs.gdc.cancer.gov/Data_Dictionary/) · [PostgreSQL: joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)

## 11. Primary and further reading

- NCI Genomic Data Commons. [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization). Documented case, sample, portion and aliquot relationships.
- NCI GDC. [Biospecimen Data](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/). Hierarchical entities and clinical versus assay file associations.
- NCI GDC. [Data Dictionary](https://docs.gdc.cancer.gov/Data_Dictionary/). Entity schemas, keys, relationships, types and allowed values.
- PostgreSQL Global Development Group. [Table expressions: joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN). Relational inner/outer join semantics; the Python exercise implements its own small teaching example.
- Collins GS et al. *TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods.* BMJ (2024). [DOI:10.1136/bmj-2023-078378](https://doi.org/10.1136/bmj-2023-078378). Reporting guidance, not proof of model validation.
- [Paul's Notes: Data identifiers, keys and reshaping](../../03_learning/keys-and-reshaping.md) and [Missingness and comparisons](../../03_learning/missingness-and-comparisons.md). Complementary independently developed coding lessons.
- [Paul's Notes: Visual ML data-flow](../../04_machine_learning/visual-data-guide.md). Group-aware partitions and leakage considerations.

**Review status:** Draft 0.2 with invented teaching data. The expanded Python join exercise and its positive/negative checks executed locally on November 21, 2026; its original default summary was preserved. The GDC dictionary and PostgreSQL join sources were checked on that date. This bounded execution is separate from clinical expert review, scientific peer review and publication acceptance.

**Next:** [CO-05 — Essential Mathematics I](CO-05-essential-mathematics-i.md), covering algebra, logarithms, rates and units through oncology examples.

**Section references:** [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/) · [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/)

