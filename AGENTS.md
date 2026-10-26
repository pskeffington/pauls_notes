# AI research-agent operating rules — Paul's Notes

Applicable to all AI coding agents, scripts and automated pull requests in this public repository.

**Research scope:** Paul's Notes supports [methods for any cancer type](docs/cancer-research-scope.md), including molecular, pathology/imaging, translational and population-health studies. **Breast cancer/TCGA-BRCA is the active worked example, not an exclusive permitted topic or dataset.** Separate scientific and data-admission reviews are required for a new cancer study.

## Authorized data boundary — all sources

1. **Default executable data: synthetic teaching data generated locally.** No patient-level cancer cohort, from TCGA, another registry, an institution or a different public resource, becomes an approved input because it is online or a JSON variable was changed.
2. **Verify the actual provider.** For each proposed real-data study, record source/release/file access, use restrictions, consent/license, intended cohort, allowed outputs and a separately reviewed study protocol. The [GDC metadata preflight](04_machine_learning/research_toolkit/gdc_open_access_preflight.py) is **specific to the current TCGA-BRCA case** and only checks official GDC file metadata with `access=open`. It makes no download and never authorizes fitting; do not apply it to other projects or weaken its `PROJECT` filter.
3. **Never** stage, commit, share in CI/artifacts or send to external AI prompts protected, controlled, identifiable or linkable participant data, credentials, raw genomic/clinical/imaging datasets, case/sample/visit identifiers, individual predictions or model weights derived from real participants. If a separate institution permits private processing, conduct it in independent approved infrastructure, **not this public repository**.
4. Treat all providers' pseudonymous specimen/registry labels, clinical/genomic combinations and rare features as potentially linkable. Do not reidentify participants or link to outside identifiable sources.
5. Keep every downloaded research file, trained real-data model and participant-level run artifact out of public Git and GitHub Actions artifacts. A project label such as `TCGA-BRCA` or `open` is not a privacy certificate.

## Before code/commit/model publication

- Register each new public CSV/TSV/JSON as independently reviewed synthetic, aggregate, bibliography or policy content in [the asset register](scripts/public_data_assets.json); inclusion on an allowlist alone is not deidentification.
- Run `python3 scripts/check_public_data_boundaries.py --staged` before committing and `--tracked` for full-tree checks; run the deliberate-failure tests in `scripts/tests/test_public_data_boundaries.py`. Do not circumvent a failure by relabeling the source or removing protections.
- The [general cancer research contract](docs/cancer-research-scope.md) and [model-use policy](04_machine_learning/research_toolkit/MODEL_USE_POLICY.md) apply to **all cancer data**. A new source needs its own provider-specific adapter/protocol; the current `synthetic-validation` runner accepts only invented data and cannot unlock patient-level training.
- Preserve correct observational units: person, specimen, slide/scan/patch, cell, visit and assay are not interchangeable. Group appropriately; learn imputation, scaling, feature selection and hyperparameters only inside training folds; protect reserved outcomes and report uncertainty honestly.
- Do not print exact sensitive data or filenames in error logs; fail with categories/hashes where possible. Never claim a heuristic scan proves all PII/PHI absent.
- Label all example outputs **RESEARCH AND EDUCATIONAL USE ONLY; NOT FOR CLINICAL USE**. Current code is not approved for diagnosis, screening, prognosis, treatment selection, patient-level predictions or clinical decision support.

## Research-specific rules and evidence

- The frozen G0–G3/R3 breast-specimen experiments and the 12-chapter 60-gene book remain one **worked case**. Changing cancer type, source, endpoint, imaging modality or label requires an independently declared study contract and evaluation; no cross-cancer performance claim follows from synthetic tests.
- The private Dartmouth.HSE R18F/R19 admission gates continue to apply **to that separate private study** and are not automatically the research protocol for unrelated cancer work. Neither GDC file availability nor public teaching code overrides them.
- Cite **the actual provider** for every executed study. Use [NCI's TCGA attribution](https://www.cancer.gov/ccg/research/genome-sequencing/tcga/using-tcga-data/citing) only for results based on TCGA; never claim invented or non-TCGA data are TCGA-derived.
- If provider metadata, data rights, privacy approval, scientific validation or release permission are ambiguous, stop that data operation and continue with synthetic fixtures or metadata-only investigation.
- `.gitignore`, a regex scanner and an `open` classification are not historical or privacy guarantees. The public data-safety status must be enforced under repository rules, with review of protected policy files, Git history/secrets and CI retention ([governance issue #8](https://github.com/pskeffington/pauls_notes/issues/8)).
