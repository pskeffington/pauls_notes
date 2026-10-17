# Configuration-driven machine-learning research toolkit

Authored by Paul Skeffington · Compiled with OpenAI

This reusable configuration-driven toolkit is intended to support **methods for any cancer type**, subject to a separate protocol for each new cohort, tumor context, modality and endpoint. The current runnable configuration is **synthetic paired-specimen breast cancer teaching data**; the [public cancer research scope](../../docs/cancer-research-scope.md) is wider than that example. The code does **not** download, inspect or fit private Dartmouth data, GDC participants or any other real patients. In the separate Dartmouth.HSE study, R18F/R19 gates still prohibit patient-level training; those private-study limits are not a requirement that unrelated cancer projects use the same dataset or endpoint.

## Cancer-wide privacy and source-specific admission

Read the [cancer-wide model-use/privacy policy](MODEL_USE_POLICY.md) and [generic research model-card template](model_card.template.json). Dataset rights, access and permitted publication differ among providers: **every real cancer dataset requires its own reviewed study contract**. Participant-linked clinical/genomic/imaging records, predictions, model weights and secrets from **any source** must stay outside public Git, unrestricted AI tools and telemetry. The [repository scanner](../../scripts/check_public_data_boundaries.py) covers the public code tree regardless of cancer site and can run as a local staged hook. New public CSV/JSON content requires independent review and registration in [the public-asset ledger](../../scripts/public_data_assets.json); this does not prove the data are anonymous.

### Current TCGA-BRCA/GDC metadata example

For the present breast-cancer source example, **TCGA-BRCA does not imply that every GDC file is open access**. This project-specific checker is one adapter, not the admissibility rule for all oncology research.

The [read-only GDC preflight](gdc_open_access_preflight.py) queries the authoritative official GDC `files` endpoint by **file UUID**, checks `access=open`, project `TCGA-BRCA`, allowed data types and metadata checksums, and records only aggregate metadata outside the repository. It performs **zero downloads and zero fits**. Example (the UUID list must come from the public GDC Data Portal; no patient identifiers):

```bash
python3 04_machine_learning/research_toolkit/gdc_open_access_preflight.py \
  --ids /tmp/gdc-public-file-ids.txt \
  --output /tmp/new-gdc-preflight
```

The synthetic runner remains independent of the GDC metadata checker. It cannot be switched to **any real cancer data source** by changing JSON. Different cancer projects require independently reviewed adapters and study-specific data/use permissions. Dartmouth HSE R18F/R19 restrictions continue to govern **that private study**, not the repository's entire scientific subject matter.

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

For a future independently **authorized cancer study**, separately implement and review a provider-specific input adapter with cohort/sample provenance, data dictionary, source rights, target definition, correct observation unit, frozen feature universe, grouped nested assessment, outcome timing, calibration/uncertainty plan, independent audit and resource policy. If the adapter is for Dartmouth.HSE, its own R18F/R19 science gates are additionally required. **Never** import real participant files into the synthetic runner or loosen the stage allowlist to bypass study-specific admission. Keep data and model artifacts outside this public repository.

Proposed future Rust integration: export a reviewed schema-only plan/metadata and pass fold-local numerical matrices to native Rust training after admission; Rust and Python should share identities, split maps and preprocessing checks but should not silently assume objectives, loss scaling or class encoding agree. The existing G3 fixed-objective Rust comparison remains a distinct synthetic protocol.

## Next validation gates

1. Parameterized input contract and synthetic nested-group smoke — **implemented; local unit checks run**.
2. Independent held-out metric and split-contract audit, source commit pinning and CI replay — **partially implemented, pending review**.
3. Real-data adapter for a separately authorized cancer cohort — **blocked, not implemented**; current TCGA-BRCA/Dartmouth R18F admission remains a specific outstanding case.
4. Multi-class, survival/time-dependent, calibrated and externally replicated workflows — **separate prospective protocols required**.

Change configuration to test **synthetic engineering scenarios**, not scientific admission status, cancer subtype truth, or real-data permissions.