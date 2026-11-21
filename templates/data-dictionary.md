# Data dictionary

Use one versioned dictionary for the source tables and derived analysis tables. Keep field names unique within each table and preserve the link from every derived value to its source. The [data-literacy chapter](../oncology/chapters/CO-04-data-literacy.md#41-a-concrete-dictionary-for-the-six-person-teaching-extract) contains a completed synthetic example.

## 1. Dataset identity and provenance

- Study/protocol identifier and scientific question:
- Dataset provider, accession and release/version:
- Source dictionary or schema URL and version:
- Extraction date, source filenames/manifest and checksums:
- Dictionary version, revision date and responsible reviewer:
- Source classification: synthetic, published aggregate or separately authorized research data:
- Access classification, permitted uses and permitted output fields:

The [GDC Data Dictionary](https://docs.gdc.cancer.gov/Data_Dictionary/) is an example of documenting entities, links, properties and constraints. Retain the actual provider's terms and schema for the selected study rather than assuming GDC conventions apply to every dataset.

## 2. Table identity and observation grain

Complete one row per table. A table's physical row count and its number of independent participants are separate quantities.

| Table | Meaning of one row | Primary key / uniqueness | Parent table and foreign key | Eligible universe and row-count expectation |
| --- | --- | --- | --- | --- |
| [source or derived table] | [participant, specimen, visit, assay, episode, etc.] | [single or composite key; missingness rule] | [parent and linkage field, or not applicable] | [roster/source population; expected cardinality] |

- Identifier namespace and rules preserving leading zeros, case and source identifiers:
- Independent sampling/randomization unit and repeated-observation grouping keys:
- Multiple specimens, visits or episodes: selection/aggregation rule and scientific rationale:
- Source rows retained, excluded and unresolved, with reasons and counts:

Declare each key's data type and reject missing or blank required identifiers before matching. A missing parent identifier must not become a valid link merely because another table also contains a missing key.

## 3. Field definitions

Use `[table].[field]` to distinguish identically named fields from different entities. Replace the placeholder row with one row per field; do not infer meaning from storage type alone.

| Table and field | Meaning and analytic role | Data type and units/scale | Allowed values or coding | Missing states and their meanings | Validation rule |
| --- | --- | --- | --- | --- | --- |
| [table.field] | [definition; identifier, exposure, outcome, covariate, etc.] | [string/integer/number/date; unit, scale and precision] | [range, categories and reference level] | [unknown, not collected, not applicable, failed, withheld, etc., only where supported] | [requiredness, uniqueness, finite/range check or cross-field consistency] |

Record assay/platform, detection limits and rounding where they affect interpretation. Keep absent observations distinct from measured zero, recorded absence and an event that makes a measurement undefined. Missing-data mechanism assumptions belong in the study's analysis plan; a missing-value code does not establish MCAR, MAR or MNAR.

## 4. Time, derivation and source traceability

Link this table to the field definitions above. Preserve raw source fields when deriving analytical versions.

| Table and field | Source field(s) and release | Measurement / availability time | Derivation or mapping | Verification and denominator effect |
| --- | --- | --- | --- | --- |
| [table.field] | [table, field, assay or source identifier] | [time origin, window, date precision, timezone if applicable] | [formula, units, contrast direction, category mapping or selection] | [cross-check; exclusions and missing values introduced] |

- Eligibility, baseline, treatment-start and endpoint time origins:
- Measurement-collection time versus the time its result became available:
- Endpoint component events, event indicators, censoring and last adequate ascertainment:
- Transformation constants, normalization/reference basis and annotation versions:
- Values outside the measurement range, detection limit or permitted chronology:
- Conflicting source values: reconciliation rule, retained alternatives and resolution record:

Specify a canonical representation for each date or timestamp used in matching. Validate that representation, or document an explicit normalization step that preserves the raw source value. Mixed date formats must not create different keys for the same instant or calendar day. The chapter's teaching lab requires `YYYY-MM-DD`; actual studies must also declare any required time precision and timezone.

## 5. Join and selection contract

Specify the desired output grain before linking tables. Include every join used to construct the analysis table.

| Left table and key | Right table and key | Expected match multiplicity | Output grain / retained universe | Duplicate and unmatched-row rule |
| --- | --- | --- | --- | --- |
| [table, key] | [table, key] | [one-to-one, many-to-one, etc.; justification] | [one row per defined unit; left/right/full/inner selection] | [reject, investigate, aggregate or prespecified selection; report unmatched records on both sides] |

Validate the key's uniqueness at the level required by the intended match. A left join retains unmatched left records, but can still multiply them if several right records match. Date proximity or a shared participant ID alone does not establish a specimen–encounter relationship. Record the supporting identifier or matching rule and retain unresolved links explicitly; see the [official relational join definitions](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN).

For each join, record input row and distinct-entity counts, output counts, duplicate matches, unmatched left records and unused right records. Reconcile each analysis population to the eligibility roster. If a selection rule changes the question or denominator, revise the study specification before interpreting results.

## 6. Dictionary acceptance and revision

- Required keys resolve; expected cardinalities and explicit unmatched states are checked:
- Units, ranges, reference groups and time definitions agree with the protocol:
- Derived values can be traced to source fields and a versioned transformation:
- Eligible, observed, missing and analyzed counts reconcile for each endpoint:
- Source review, executed checks and scientific review are recorded separately:
- Revision history: changed definitions, reason, affected outputs and reviewer:

Keep actual participant linkage keys in the approved study storage location.

[Workflow](../docs/research-workflow.md) · [Study protocol](study-protocol.md) · [Analysis record](analysis-record.md)
