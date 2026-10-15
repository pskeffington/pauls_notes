# Data dictionary

Dataset accession and release:

Observation unit and primary key:

| Field | Meaning | Type | Units or categories | Missing convention | Validation rule |
| --- | --- | --- | --- | --- | --- |
| `sample_id` | Synthetic sample identifier | string | unique label | prohibited | unique and nonempty |
| `measurement` | Demonstration measurement | numeric | specify assay and scale | specify explicitly | finite when observed |

## Relationships and transformations

- Participant-to-specimen-to-assay linkage and expected cardinality:
- Identifier namespace, annotation version and join key:
- Date/time format and timezone:
- Detection limits, rounding and impossible values:
- Transformation formula, direction and rationale:
- Source fields and output fields:
- Duplicate and unmatched-row handling:
- Access classification and permitted output fields:

Keep actual participant linkage keys in the approved study storage location.

[Workflow](../docs/research-workflow.md) · [Study protocol](study-protocol.md)
