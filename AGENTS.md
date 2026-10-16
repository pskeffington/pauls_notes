# AI research-agent operating rules — Paul's Notes

Applicable to all AI coding agents, scripts and automated pull requests in this repository.

## Authorized data boundary

1. **Default execution:** synthetic teaching data generated locally. Any actual TCGA-BRCA ingestion requires a separately reviewed experiment/data-use contract.
2. **Official provenance:** only GDC files currently verified as `access=open` and project `TCGA-BRCA` by the GDC API are eligible for later approved local research. A project label, filename, mirror or human claim alone is insufficient. The [read-only GDC preflight](04_machine_learning/research_toolkit/gdc_open_access_preflight.py) does not authorize downloads or fitting.
3. **Never** access, request, transfer, stage, commit, attach to chat/AI prompts, or upload controlled-access GDC data, dbGaP tokens, patient names, health-record numbers, dates of birth, contact information or otherwise restricted participant data.
4. Treat GDC case/sample barcodes and rare combinations of clinical/genomic features as linkable, even if GDC lists the source file as open. Never include row-level identifiers or participant predictions in public issues, logs, model cards, figures, artifacts or PRs.
5. Do not attempt participant reidentification, inference of individual identities, or linkage to external identifiable data.

## Before any code/commit/model publication

* Keep every TCGA archive, downloaded clinical/biospecimen/genomic file, locally fitted model/weights and row-level run output outside this repository and outside GitHub Actions artifacts. Never add data with `git add -f`.
* Register each new public CSV/TSV/JSON as a reviewed **synthetic, aggregate, bibliographic or policy artifact** in [public_data_assets.json](scripts/public_data_assets.json). Registration does not replace inspection for hidden identifiers.
* Run `python3 scripts/check_public_data_boundaries.py --staged` before committing and `--tracked` for full-tree checks. Tests: `python3 -m unittest discover -s scripts/tests -p test_public_data_boundaries.py -v`. Do not remove/disable failing guards to admit an input.
* Ensure configuration-driven experimentation cannot enable clinical, patient-level or prohibited workflows by only editing variables. Dartmouth.HSE R18F/R19 approval gates remain independent from GDC file access designation.
* Add [research-only model disclaimer](04_machine_learning/research_toolkit/MODEL_USE_POLICY.md) to output summaries and model cards. No diagnosis, treatment selection, clinical prognosis, decision support or validated medical-device claims.
* Use training-only preprocessing, person-grouped partitions and explicit measurement/label contracts; never call outer held-out fold outcomes into selection/tuning.
* Source artifacts and log messages must never print the exact sensitive value that caused a guard failure. Rejection categories are enough.

## Publication, citation and failure behavior

* Follow [NCI TCGA attribution guidance](https://www.cancer.gov/ccg/research/genome-sequencing/tcga/using-tcga-data/citing) and identify any real TCGA-BRCA source accession/release in approved publications.
* Label purely synthetic findings `SYNTHETIC`; do not suggest they were learned from TCGA cases.
* If official metadata verification, privacy review, classification, release permission, or scientific validation is unclear, **stop that data operation**. Continue with a synthetic fixture or a metadata-only audit, not a default-open fallback.
* Do not assume `.gitignore` or a regex scan proves anonymity, prevents forced pushes or erases Git history. Require PR review and the repository data-safety status check for merge.
