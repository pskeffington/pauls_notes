# Find the right research resource

[Paul's Notes](../README.md) · [Research workflow](research-workflow.md) · [Learning roadmap](learning-roadmap.md)

Use this index to navigate methods for **research across cancer types**. The TCGA-BRCA/breast cancer material is today's worked case, not a source or endpoint requirement for unrelated research. If you're new, start with [project scope](cancer-research-scope.md) and the [starting routes](../README.md#start-here).

## Learn the concepts

| Your question | Start here | Continue with |
| --- | --- | --- |
| How do I start a new cancer type or data source? | [Cancer research scope](cancer-research-scope.md) | [Independent study protocol](../templates/study-protocol.md), [data/access workflow](research-workflow.md) and [data dictionary](../templates/data-dictionary.md) |
| How do tumor and normal specimens relate to people and genes? | [Breast cancer book](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) | [Gene atlas](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-6-the-integrated-60-gene-atlas) and [pathways](../06_RESOURCES/Genomics/GENE_PATHWAY_OVERVIEW.md) |
| How do I learn Rust from zero and build research objects? | [Rust foundations course](../03_learning/rust/README.md) | [Object-oriented Rust](../03_learning/rust/04_structs_traits_and_composition.md) then [research engineering](../03_learning/rust/06_breast_cancer_engineering.md) |
| How do I work with tables, joins and missing data? | [Computing by subject](../03_learning/README.md) | [Keys and reshaping](../03_learning/keys-and-reshaping.md) and [missingness](../03_learning/missingness-and-comparisons.md) |
| How does a model train and why do data splits matter? | [ML data-flow guide](../04_machine_learning/visual-data-guide.md) | [ML home](../04_machine_learning/README.md) and [nested comparison](../04_machine_learning/model-comparison.md) |
| How do I script a reproducible run? | [Unix and Bash](../01_unix_bash/README.md) | [Research workflow](research-workflow.md) |

## Build or inspect an analysis

| Your task | Go to | Deliverable |
| --- | --- | --- |
| Plan the question and define the records | [Research workflow](research-workflow.md) | An explicit [study protocol](../templates/study-protocol.md) and [data dictionary](../templates/data-dictionary.md) |
| Train and compare models on synthetic assay data | [Paired-specimen example](../04_machine_learning/advanced-breast-cancer-training.md) | Held-out predictions, selected features and a reproducible run |
| Select hyperparameters and check leakage | [Tuning guide](../04_machine_learning/model-tuning.md) | Grouped partitions, training-only preparation and candid candidate-score history |
| Create figures and explain them | [ML plotting gallery](../04_machine_learning/gallery/README.md) · [R tools](../06_RESOURCES/R/README.md) | Labeled, reproducible figures with an interpretation |
| Work across R, Python and Rust | [Methods and deployments](../04_machine_learning/methods-and-deployments.md) · [Rust deployment](../04_machine_learning/rust-deployment.md) | Bounded and documented computing examples |
| Write a manuscript and manage citations | [LaTeX resources](../06_RESOURCES/LaTeX/README.md) | Manuscript source and bibliography |

## Check evidence and quality

| Need | Reference |
| --- | --- |
| Find primary studies and coding implications | [Biomedical coding literature matrix](../02_biomedical_coding/BIOMEDICAL_CODING_LITERATURE_MATRIX.md) |
| Inspect package/API guidance and source versions | [Official methods register](../02_biomedical_coding/OFFICIAL_METHODS_REGISTER.md) |
| Write and audit Rust research code | [Rust engineering handbook](../02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md) and [Rust ML application review](../04_machine_learning/rust-ml-literature.md) |
| Check gene identity and supporting annotation | [Gene annotation register](../06_RESOURCES/Genomics/REFERENCES/ANNOTATION_SOURCE_REGISTER.md) · [Evidence matrix](../06_RESOURCES/Genomics/REFERENCES/GENE_EVIDENCE_MATRIX.md) |
| Compare executed work with planned milestones | [Dated gate dashboard](roadmap-gates.md#delivery-and-admission-snapshot-2026-10-17), [machine-readable evidence record](milestone-evidence.toml) and [ML corpus validation](../04_machine_learning/corpus-review.md) |
| Record results and limitations | [Analysis record template](../templates/analysis-record.md) · [Implementation gates](../02_biomedical_coding/IMPLEMENTATION_GATES.md) |

## Choose a source for the question

Use language manuals for syntax, package vignettes for API behavior, primary papers for study methods and findings, annotation records for gene identity, and reporting checklists for disclosure requirements. Record the version and date relevant to the analysis. An abstract-level reading is insufficient to reproduce a paper's full method.

## Record an evidence-to-code decision

For each adopted method, record its citation, source version, study assumption, proposed implementation, expected output, failure case and validation result. Keep candidate methods separate from methods actually executed. Source registers document bibliographic and structural checks; the execution record belongs to the individual analysis.

**Data and model boundary:** No participant-level cancer datasets from TCGA **or any other source** are bundled here. Future real-data studies require **provider-specific** access, privacy and scientific admission. Existing executable examples are synthetic and not validated clinical tools. [Start at the research data-access contract](research-workflow.md#2-specify-input-and-access-contracts) before building a new adapter.
