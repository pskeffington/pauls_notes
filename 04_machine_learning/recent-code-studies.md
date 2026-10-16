# Recent papers: mechanisms to inspect and adapt

[Machine learning](README.md) · [Package guide](package-guide.md) · [Foundational literature matrix](../02_biomedical_coding/BIOMEDICAL_CODING_LITERATURE_MATRIX.md)

Source check: 2026-10-16. Four 2025–2026 studies and one 2024 leakage reference extend the foundational matrix. This is a selective implementation reading list. The notes below distinguish publication evidence, repository documentation, and our own proposed acceptance checks. None of these full studies has been reproduced here. No paper text, third-party source tree, study data or model weights is copied into the repository.

| ID | Academic paper | Author code or archived implementation | Review extent |
| --- | --- | --- | --- |
| ML-2025-01 | Hollmann et al. (2025), [Accurate predictions on small data with a tabular foundation model](https://doi.org/10.1038/s41586-024-08328-6) | [Paper-associated archive](https://doi.org/10.5281/zenodo.13981285); [maintained TabPFN repository](https://github.com/PriorLabs/TabPFN) | Publication summary/code link and current repository documentation; no execution |
| ML-2025-02 | Kedzierska, Crawford, Amini and Lu (2025), [Zero-shot evaluation reveals limitations of single-cell foundation models](https://doi.org/10.1186/s13059-025-03574-x) | [Evaluation repository](https://github.com/microsoft/zero-shot-scfoundation); [archive](https://doi.org/10.5281/zenodo.15123462) | Methods, code-availability section and repository documentation; no execution |
| ML-2025-03 | Kalfon et al. (2025), [scPRINT: pre-training on 50 million cells allows robust gene network predictions](https://doi.org/10.1038/s41467-025-58699-1) | [scPRINT repository](https://github.com/cantinilab/scPRINT); [versioned release archive](https://doi.org/10.5281/zenodo.15490696) | Publication summary and repository usage/input documentation; no execution |
| ML-2026-01 | Wang, Danek, Yang, Chen and Sun (2026), [Making large language models reliable data science programming copilots for biomedical research](https://doi.org/10.1038/s41551-025-01587-2) | [Original benchmark landing repository](https://github.com/RyanWangZf/BioDSBench); [maintained successor](https://github.com/RyanWangZf/BioDSA) | Publication abstract/code linkage and current repository organization; no execution |
| ML-2024-01 | Rosenblatt et al. (2024), [Data leakage inflates prediction performance in connectome-based machine learning models](https://doi.org/10.1038/s41467-024-46150-w) | [Leakage analysis repository](https://github.com/mattrosenblatt7/leakage_neuroimaging) | Publication methods summary, repository documentation and selected `run_leakage.py` blocks; no execution |

## Tabular prediction and frozen releases

**Observed mechanism:** TabPFN exposes a familiar fit/predict interface, while the paper also supplies a code archive. A current default checkpoint is not necessarily the model evaluated in the 2025 paper.

**Adaptation:** Benchmark a frozen model/checkpoint against regularized regression and forests using the same assessment people. Record checkpoint identity, installed version, preprocessing, memory and inference time. Check code, weights and data terms separately.

**Acceptance task:** Replay probabilities from the specified release and prove that the assessment cohort was excluded from task fitting and any task-dependent selection. The local caret workflow supplies comparator mechanics; it does not run TabPFN.

## Single-cell representations and simple baselines

**Observed mechanism:** The zero-shot evaluation compares Geneformer/scGPT representations with highly variable gene and scVI baselines. Its repository separates evaluation notebooks and environment setup, including `notebooks`, `envs`, and `sc_foundation_evals`.

**Adaptation:** Preserve model-specific gene preprocessing, donor provenance, and explicit baseline implementations. Evaluate biological structure and batch behavior separately. Treat pretrained-data overlap as part of the evaluation setting.

**Acceptance task:** Save aligned cell/gene identifiers and a donor-level split record; compare embeddings under a frozen metric configuration. More cells do not automatically supply more independent biological replicates.

## Gene-network inference and explicit input contracts

**Observed mechanism:** scPRINT documentation describes raw-count inputs, organism/gene identity requirements, task-specific inference commands, checkpoints and optional acceleration. Its documented assessment notebooks include `notebooks/assessments/bench_omni.ipynb` and `bench_denoising.ipynb`.

**Adaptation:** Separate data loading, checkpoint loading and task evaluation. Estimate memory for embedding and projection stages. Select an archived compatible environment before enabling optional GPU kernels.

**Acceptance task:** Reject incompatible assay layers and unresolved identifiers before inference; retain the checkpoint hash and compare a small task fixture with a reference output. Predicted network edges are hypotheses requiring biological evaluation.

## Biomedical coding agents and execution evidence

**Observed mechanism:** The 2026 study describes biomedical analysis coding tasks. The original landing repository redirects to a successor that now separates agents, benchmarks, runners and tests; current main has evolved beyond the paper release.

**Adaptation:** Keep task inputs, expected scientific meaning and execution checks separate from generated code. Freeze the paper-associated benchmark version when evaluating a paper claim.

**Acceptance task:** A plausible plot or successful process is insufficient: check row identities, units, exclusions and numerical expectations on deliberately broken fixtures. This repository adopts that testing principle, not the external agent platform.

## Leakage as a deliberate negative control

**Observed mechanism:** The neuroimaging study contrasts pipelines that differ in feature, covariate and subject leakage. Its code separates `run_leakage.py`, sample-size analysis and plotting. The repository describes academic/noncommercial use constraints; inspect the applicable terms before reuse.

In the inspected [analysis script](https://github.com/mattrosenblatt7/leakage_neuroimaging/blob/main/run_leakage.py), family identifiers determine outer membership, covariate coefficients learned on training data are applied to test data, and `GridSearchCV` tunes ridge/SVR candidates. When adapting this pattern, place learned transformations inside every relevant inner training fold too.

**Adaptation:** Challenge a pipeline by altering assessment predictors while keeping training rows fixed. Fitted preprocessing and tuning must remain unchanged.

**Acceptance task:** The [caret tests](tests/test_caret_case.R) implement that holdout-mutation challenge and reject overlapping partitions. They reproduce neither the original datasets nor the study's numerical effects.

## Promote a reading entry to a deployment

Record the release/commit, software environment, data access, checkpoint identity, input contract, exact command, expected artifacts, independent-unit split, baseline, runtime and failed-case tests. Mark a study reproduced only after those artifacts have been executed and reviewed. Summarized mechanisms and suggested optimizations remain proposals until measured locally.
