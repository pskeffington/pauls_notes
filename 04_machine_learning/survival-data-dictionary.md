# G4 data dictionary — invented oncology survival cohort

[Prospective G4 protocol](survival-protocol.md) · [Machine-readable contract](evidence/survival-contract-v1.json) · [Cancer-wide study requirements](../docs/cancer-research-scope.md) · [Generic data dictionary template](../templates/data-dictionary.md)

**Data provider:** Internal synthetic RNG only. **Stage:** frozen design, no rows generated or outcomes inspected by this change. **Research use:** educational and software testing only. No actual patient follow-up, samples, genomic barcodes, clinic dates, diagnoses or recurrence outcomes are admitted.

## Biological/analytic unit and identity

One row = **one independent invented person**, with one baseline and one observed time-to-event interval. No patient-to-specimen join is needed or allowed for this version; the synthetic people have *no connection* to G0–G3 paired specimen identifiers. `person_id` must be `S001...S240`, unique, nonempty, and stable through splits. The key must **not** be changed to GDC barcodes, medical record IDs or private participant identifiers.

Only the **five ordered columns** below can be supplied to the future analysis function:

| Field | Meaning / scope | Type and units | Missing values | Validation / use |
| --- | --- | --- | --- | --- |
| `person_id` | Made-up independent person key | string, `S001..S240` | Never | One row per invented person, unique; joins and folds only |
| `age_years` | Artificial age-like baseline covariate | finite numeric years | Never | `30 ≤ age_years ≤ 75`, generator `Uniform(30,75)`; not personally identifying |
| `marker` | Artificial unnamed assay-like baseline score | finite numeric, unitless | Never | `Normal(0,1)` generated; not a real gene or clinical measurement |
| `time_months` | Observed follow-up from invented baseline to event or censor | finite numeric months | Never | `0 < time_months ≤ 60`; equals `min(latent_event_time, censor_time)` |
| `event` | Whether the fictional event was observed | integer `0` or `1` | Never | `1` = first invented recurrence-like event; `0` = right censoring, **not** proof of being event-free at 24 months |

The generator may use latent event and censoring times **internally** but they must never appear in the modeled columns or support train/held-out feature engineering. The event uses `event_time <= censor_time` as the deterministic tie policy. Dates, treatment arms, cancer stages, diagnostic labels, competing events, left truncation and time-varying predictors are *absent by design*.

## Computation and link relationships

- `person_id -> exactly one baseline record`; no specimens/images/visits, and no sharing IDs with any other experiment.
- Split IDs by **person**, not by follow-up row or time point. Reserve **60** IDs using seed `26102402`. The other **180** form development, with three disjoint **60-person** test folds from seed `26102403`.
- Within each outer fold, training uses **120** people; test uses **60**. The 60 reserved people are not part of the model, censor-weight estimator, training diagnostics or reported assessment.
- **Prediction target:** event-free survival probability `S(24)`; a Cox linear predictor is not that probability. `event` must never be a feature.
- **At-horizon status:** observed event at or before 24 -> survival outcome 0; observed follow-up after 24 -> survival outcome 1; censoring at/before 24 -> status **unknown**, weight zero in IPCW Brier. No recoding of early censoring.
- **Training-only censor support:** `Ghat` is fitted on the outer training fold through reverse KM; require `Ghat(24) >= 0.20` and `Ghat(t-)>0` for events to be scored.

## Expected output record types (future implementation only)

| Output artifact (new external directory, not this repo) | Required fields |
| --- | --- |
| Run manifest | Protocol ID and frozen commit, protocol/contract/source SHA-256, seed, R and survival version, disclaimer, source=synthetic |
| Synthetic input digest | Exact five-field schema, 240 rows, aggregate event/censor count and SHA-256; row contents never attached to public CI |
| Split manifest | All 240 invented IDs, role/fold allocation, 60 reserve, 180 development, outer-train/test disjointness |
| Fold report | Per-fold train/test people/events/horizon counts, Cox estimates, training PH diagnostics, KM and censor-support estimate at 24 |
| Prediction report | Fold, invented person ID, observed follow-up/event, Cox and null event-free probabilities, Cox relative log hazard, IPCW weight/contribution; **not** public artifact |
| Assessment summary | Pooled 180-person Cox and null Brier, signed contrast, descriptive concordance, fixed-bin calibration counts/KM or unavailable reason |
| Failure report | Failed gate name, stage, non-sensitive diagnostic, exact code/protocol hash; no silent seed/horizon change |

Do not include any real participant-level data or model weights in public repository files, Actions artifacts or AI prompts. **The table describes a prospective output contract and does not imply those files currently exist.**

## Fail-closed schema tests

Reject duplicate/invalid identifiers, altered field order, extra clinical identifiers, missing/NaN/infinite covariates, `time_months <= 0`, time beyond 60, event outside `{0,1}`, wrong target semantics, reserved people in training/test, overlapping outer folds, and inconsistent censor-weight time logic. If synthetic generator feasibility fails, record failure without changing seeds to improve apparent performance.

**RESEARCH AND EDUCATION ONLY — NOT FOR CLINICAL USE.** The fictional event is not a cancer diagnosis, actual recurrence, cause of death, or personal prognosis.
