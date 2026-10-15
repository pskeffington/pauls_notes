# Biomedical coding: evidence-to-code acceptance gates

**Purpose:** Turn reference literature into measurable code-quality requirements. These are design gates, **not a validation certificate** for any archived script or clinical model.

| Stage | Required artifact | Pass condition | Common failure |
| --- | --- | --- | --- |
| G0 — Bibliography | Publication, DOI/primary page, source type, methodological role | Citation is traceable and distinguishes software from reporting | Fabricated or misclassified method |
| G1 — Data permission | Data agreement, lawful use, access restrictions, retention rule | No unauthorized study records, identifiers or credentials in repo | PHI or restricted-source publication |
| G2 — Schema | Record unit, sample IDs, variable types, missingness, units | Input schema and key uniqueness checked | Silent type, ID, unit mismatch |
| G3 — Study design | Estimand, predictors, outcomes, timing, replicates, clusters | Model matches observational or experimental structure | Pseudoreplication, immortal time |
| G4 — Model selection | Deterministic split plan, seed, tuning/nesting | Every learned transformation is trained only in correct partition | Leakage through imputation and feature selection |
| G5 — Inferential validity | Assumptions, diagnostics, multiplicity, effect/uncertainty reporting | Numeric and statistical guards pass on known fixtures | Anti-conservative discoveries |
| G6 — Omics semantics | Count scale, normalization, annotation, batch and sample design | All assay/sample ID contracts pass, design and contrasts reviewed | Inappropriate count model, confounded batch correction |
| G7 — Manuscript figures | Reproducible plotting code, labels, legends, uncertainty | Output inspected at publication dimensions and reference group mapping checked | Overlapping annotations, misleading scale |
| G8 — Computational replay | Lockfile, environment, metadata log, source checksums | Clean environment regenerates synthetic output | Hidden local dependency |
| G9 — Predictive validity | Independent/outer held-out assessment, calibration, subgroup checks | No tuning leak; discrimination and uncertainty jointly assessed | Inflated AUC or invalid probabilities |
| G10 — Clinical claims | Applicable reporting standard, bias appraisal, intended-use decision | Study design matched to the right guideline and reviewed | Equating checklist completion with patient safety |

## R and biomedical statistics

- Keep factor reference levels, data types and model formulas explicit.
- Separate preprocessing from assessment in `caret` or another modeling framework; confirm current API syntax in official documentation.
- For repeated measures, model clusters rather than assuming independent rows; inspect singular fits and convergence.
- Declare the exact hypothesis family used for FDR adjustment; report effect estimates and confidence/credible intervals when appropriate.

## Gene expression and figures

- Do not feed TPM, log counts or otherwise transformed expression directly into raw-count models intended for counts.
- Require sample/feature identity checks before each matrix or metadata join.
- Assess batch/condition confounding; correction can erase the scientific effect if the design is not identifiable.
- Preserve sample-group order, readable labels, uncertainty, colour scales, and complete legends in heatmaps, violins, volcano/MA and other manuscript figures.

## Biomedical AI, models and RAG

- Choose the independent unit of evaluation: **patient, donor, time, site, sequence family**, or another true independence level.
- Avoid using evaluation data for hyperparameter search, feature selection, normalization or imputation.
- Include calibration and precision-recall where class prevalence and clinical decisions require them.
- Use TRIPOD+AI for applicable prediction model reports and PROBAST+AI for bias/applicability appraisal; use STARD-AI for diagnostic accuracy and CONSORT-AI/SPIRIT-AI for applicable trials/protocols.
- For LLM/RAG experiments, freeze retrieval-corpus versions and model configuration; test citation entailment, nonanswers, subgroup errors and human oversight.
- The foundational RAG literature is not evidence that an LLM is safe for patient care.

## Readiness labels

**Source-linked** means a publication is traceable. **Code tested** means a specified implementation passed a stated fixture. **Scientifically reviewed** requires study-level appraisal. **Manuscript-ready** requires presentation and reporting review. **Clinically deployable** needs independent governance, safety evidence, authorizations and monitoring. Never silently promote one label into the next.


[Return to matrix](BIOMEDICAL_CODING_LITERATURE_MATRIX.md).
