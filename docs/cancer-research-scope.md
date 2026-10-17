# Cancer research scope and current worked examples

[Paul's Notes](../README.md) · [Research workflow](research-workflow.md) · [ML methods](../04_machine_learning/README.md) · [Milestone evidence](roadmap-gates.md)

**Repository mission:** Paul's Notes supports **research methods, scientific computing, reproducible software and evidence review across all cancer types**, not only breast cancer and not only The Cancer Genome Atlas (TCGA). The same study-design and quality principles apply across cancer sites, histologies, stages, model systems and data modalities. This repository is a *methods and learning resource*, not a single-dataset training warehouse or a validated clinical system.

## What is in scope

| Research domain | Examples of supported questions | What a new study must define |
| --- | --- | --- |
| Molecular oncology | Genomics, transcriptomics, epigenetics, proteomics, tumor microenvironment and multi-omics integration | Biological units, assay technologies, preprocessing and feature provenance |
| Pathology and imaging | Whole-slide histopathology, radiology, microscopy and spatial measurements | Patients → specimens → slides/scans → tiles or regions, labeling and leakage boundaries |
| Clinical and translational research | Subtypes, response, recurrence, survival, prognostic modeling and therapeutic hypotheses | Target, time origin, follow-up, interventions, confounding, censoring and endpoints |
| Cancer epidemiology and public health | Screening, incidence, disparities, population outcomes and registry analysis | Population, sampling frame, ascertainment, denominators, access and uncertainty |
| Computational methods | R/Python/Rust pipelines, reproducible figures, model comparison, tuning, simulation and verification | Appropriate dataset contract, held-out design, independent checking and reporting |

These are **permitted subject areas**, not claims that a dataset, trained model or clinical use is already approved or implemented. A new cancer topic should get its own question, source register, study protocol and acceptance evidence; it does **not** have to be forced into the existing breast-cancer classification question.

## The current concrete worked case

The [12-chapter breast cancer book](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) and its 60-gene *teaching atlas* provide the current narrative for interpreting people, paired tissue specimens, measurements and model validation. The present executable classification examples use **invented/synthetic paired specimens and anonymous features**, not measured expression for all 60 atlas genes and not a new TCGA-BRCA patient-level model. The frozen [G0–G3 experiments and R3 parity extension](roadmap-gates.md) validate **specific synthetic numerical/software contracts**, not cancer detection or transfer to other tumors.

**TCGA-BRCA** is the present publicly documented *data-source example* under consideration. It is **not** a repository-wide data-source requirement, a default scientific endpoint or permission for other GDC projects. The proposed [GDC preflight in draft PR #7](https://github.com/pskeffington/pauls_notes/pull/7) intentionally hard-codes `TCGA-BRCA` for **that example only**. The project-specific D1 admission gate blocks *that proposed real-data study*; it is not a blanket claim that no future cancer research of any kind could be approved.

## Reusable study contract for a new cancer project

For **every new study**, independently record:

1. **Question and cancer context:** site/histology/model, population, study design, exposure or contrast, target and clinical/public-health interpretation.
2. **Source and access:** provider/repository, dataset accession and version, file-by-file or provider-specific access classification, consent/license/use terms, storage restrictions and permission to publish derived outputs. Open availability does not guarantee anonymity or unrestricted reuse.
3. **Observation and linkage:** patient/person, specimen, tumor site, cell, image, tile, assay, visit and repeated-measurement relationships, as applicable. Define the independent resampling unit rather than assuming every row or tile is an independent person.
4. **Measurement and endpoint:** modality, units, normalization, batch/QC, missingness, target ascertainment, follow-up/time origin or labels and outcome availability.
5. **Method and evaluation:** training-only feature engineering, grouped or site-aware splits, locked assessment boundaries, baselines, tuning, calibration, uncertainty, failure fixtures and independent numerical/biological reviews.
6. **Provenance and release:** source/config/package versions, hashes, resource budget, reported denominators, external-validation status, privacy review, data/model-sharing policy, disclaimer and bounded claims.

Use the [study-protocol template](../templates/study-protocol.md), [data dictionary](../templates/data-dictionary.md), [execution record](../templates/analysis-record.md) and [methodological admission checklist](research-workflow.md). An oncology method can be reused across studies only after confirming the new study's record, endpoint and access contracts.

## Dataset-agnostic privacy with source-specific adapters

**Public repository default:** Only reviewed documentation, bibliographic metadata, safe configuration, aggregate outputs that have passed disclosure review, and synthetic fixtures belong in public Git. Never commit protected/controlled data, identifiable or linkable participant records, downloaded clinical/genomic/imaging datasets, patient-linked predictions, private model weights, credentials or external research exports. Do not send them to public AI prompts or CI logs. Source data and run artifacts belong outside Git under separately reviewed access controls.

- **GDC / TCGA-BRCA:** The current case-specific open-access metadata checker can verify the official `access=open` flag and the *current example project's* UUIDs/data-type requirements. It **does not** download files, perform modeling, admit another TCGA tumor project or serve as a universal data-source validator.
- **Other cancer sources:** Use a **separate, provider-specific access/provenance review** and study authorization, even when described as public. Never relabel a source as `TCGA-BRCA` to bypass the current checker or weaken the file/project allowlist to make another dataset pass.
- **Controlled, ambiguous or reidentifiable records:** They are not admitted into this public repository's workflows. An externally permitted study needs its own appropriate private infrastructure, data-governance process and independent review; it is **not** unlocked by editing a JSON config, adding a dataset name or passing CI.
- **Generality:** The proposed [public Git safety checks (PR #7)](https://github.com/pskeffington/pauls_notes/pull/7) should apply **regardless of cancer site or source**. Registration and heuristic scans reduce exposure risk but cannot prove PII/PHI absence or erase history. [Administrative enforcement issue #8](https://github.com/pskeffington/pauls_notes/issues/8) remains open.

For any example model or plot, use: **RESEARCH AND EDUCATIONAL USE ONLY — NOT FOR CLINICAL USE.** No current example is validated for diagnosis, screening, treatment selection, individual prognosis or clinical decision support. Cite TCGA when TCGA data actually support a report; cite each *other* source under its own provider requirements rather than attaching TCGA acknowledgments to unrelated studies.

## Gate interpretation

| Item | Repository-wide or case-specific? |
| --- | --- |
| Open subject matter: research on all cancer types | **Repository-wide** |
| Reproducibility, grouped evaluation, model-use limits, public-Git data safeguards | **Repository-wide defaults** |
| Breast cancer book, synthetic paired-specimen classification and G0–G3/R3 | **Current worked case** |
| GDC metadata preflight hard-coded to `TCGA-BRCA` | **Current source adapter only** |
| D1 real `TCGA-BRCA` scientific/data admission | **Blocked for that proposed case**, not for unrelated hypothetical authorized studies |
| New cancer cohort, endpoint, institution, imaging/omics modality or data source | **New independent protocol, provenance/access and evaluation gates required** |

This is a scope statement, not a claim that the repository already contains executed models for every cancer type.
