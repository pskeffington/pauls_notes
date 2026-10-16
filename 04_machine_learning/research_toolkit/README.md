# Configuration-driven machine-learning research toolkit

Authored by Paul Skeffington · Compiled with OpenAI

This public teaching toolkit is designed to support **approved future Dartmouth HSE research methods** through a reusable variable/configuration contract. It does **not** use, copy, inspect, import or train on private Dartmouth datasets; it does not grant patient-level research admission. The private Dartmouth R19 policy explicitly limits training to internally generated synthetic observations and keeps R18F patient-level prediction blocked. The private study's preselected 60 genes cannot be reused as unbiased in-fold feature selection; the public pedagogical 60-gene book is a different catalog.

## TCGA open-access privacy and model-use policy

Read the [mandatory model-use/privacy notice](MODEL_USE_POLICY.md) and [machine-readable model-card template](model_card.template.json). **TCGA-BRCA does not imply every GDC file is open access.** Publicly released clinical and biospecimen files must be verified individually. Data archives, participant-linked predictions, model weights, and secrets are never committed here. Do not share sample-level GDC records with external AI tools or telemetry. The [repository scanner](../../scripts/check_public_data_boundaries.py) runs on all GitHub pull requests and can be enabled locally as a staged Git hook. Any new public CSV or JSON must be explicitly reviewed and added to the [registered public assets](../../scripts/public_data_assets.json) first.

The [read-only GDC preflight](gdc_open_access_preflight.py) queries the authoritative official GDC `files` endpoint by **file UUID**, checks `access=open`, project `TCGA-BRCA`, allowed data types and metadata checksums, and records only aggregate metadata outside the repository. It performs **zero downloads and zero fits**. Example (the UUID list must come from the public GDC Data Portal; no patient identifiers):

```bash
python3 04_machine_learning/research_toolkit/gdc_open_access_preflight.py \
  --ids /tmp/gdc-public-file-ids.txt \
  --output /tmp/new-gdc-preflight
```

The synthetic runner remains independent of those public GDC metadata checks. It cannot be switched to patient-level training by changing JSON; the private Dartmouth HSE R18F/R19 admission requirements remain in force.

## Variable-only execution

Edit `synthetic_brca_config.json`, changing the people/specimens count, feature dimensions, missing fraction, outer/inner folds, feature counts, L2 strengths and seed. Run from the repository root:

```bash
python3 04_machine_learning/research_toolkit/research_runner.py \
  --config 04_machine_learning/research_toolkit/synthetic_brca_config.json \
  --output /tmp/new-synthetic-brca-run
python3 -m unittest discover -s 04_machine_learning/research_toolkit -p 'test_*.py' -v
```

The output directory must not already exist **and must be outside the public source repository**. Every report contains an explicit `model_use` restriction block (research-only, no clinical use, no patient-level training) so the warning follows the output. Each report contains row-level held-out predictions and identities, selected inner search settings, per-fold group counts, balanced accuracy, accuracy and log loss; numerical evidence is descriptive synthetic software evidence. The exact config/source SHA-256 and runtime details are recorded. **Changing the JSON cannot enable research/patient training:** the only admissible stage is `synthetic-validation`, the only input is internally invented data, and arbitrary file paths or model names are rejected. Missing values are inserted by the synthetic generator; imputation, scaling and univariate feature selection are all inside the training pipeline and are re-fitted inside each inner fold. StratifiedGroupKFold prevents the same person from appearing in two folds.

The labels are invented binary specimen categories, **not** survival, subtype accuracy or patient outcomes. Generated data is deliberately simple; its held-out performance has no biological meaning. `majority` is an untouched baseline. `logistic` compares a bounded C×k grid using inner balanced accuracy. Outer folds are used only for evaluation; no reported outer score is used to select inner hyperparameters.

## Research integration design and admission boundary

For a future **private** research adapter, separately implement and review a new admissible stage with explicit cohort/sample provenance, data dictionary, target definition, correct observation unit, frozen feature universe, grouped nested split, outcome timing, calibration/uncertainty plan, audit/replay and resource policy. This extension must go through Dartmouth's own R18F/R19 scientific gate; do **not** import a patient file into the synthetic runner or change the stage allowlist to bypass that gate. Keep private data and model artifacts outside the public repository.

Proposed future Rust integration: export a reviewed schema-only plan/metadata and pass fold-local numerical matrices to native Rust training after admission; Rust and Python should share identities, split maps and preprocessing checks but should not silently assume objectives, loss scaling or class encoding agree. The existing G3 fixed-objective Rust comparison remains a distinct synthetic protocol.

## Next validation gates

1. Parameterized input contract and synthetic nested-group smoke — **implemented; local unit checks run**.
2. Independent held-out metric and split-contract audit, source commit pinning and CI replay — **partially implemented, pending review**.
3. Approved private adapter for R18F patient-level prediction — **blocked, not implemented**.
4. Multi-class, survival/time-dependent, calibrated and externally replicated workflows — **separate prospective protocols required**.

Change configuration, not scientific admission status, to test engineering scenarios.