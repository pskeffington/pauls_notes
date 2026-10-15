# Biomedical researcher resource guide

[Paul's Notes](../README.md) · [Research workflow](research-workflow.md)

| Area | Local entry point | Use it for |
| --- | --- | --- |
| Task-based learning | [Learning sections](../03_learning/README.md) | Objects, linkage, repeated measures, models, figures, simulation and execution |
| Shell and filesystem | [Unix and Bash](../01_unix_bash/README.md) | Paths, streams, quoting, exit status and synthetic metadata processing |
| Research software | [Implementation gates](../02_biomedical_coding/IMPLEMENTATION_GATES.md) | Input contracts, dependency records and acceptance checks |
| Biomedical methods | [Publication matrix](../02_biomedical_coding/BIOMEDICAL_CODING_LITERATURE_MATRIX.md) | Papers, coding implications, test expectations and failure modes |
| Software documentation | [Methods register](../02_biomedical_coding/OFFICIAL_METHODS_REGISTER.md) | Provider manuals and specifications with version requirements |
| Breast cancer | [Complete book](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) | People, datasets, measurements, biology, 60 gene profiles and worked examples |
| Gene lookup | [Integrated gene atlas](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-6-the-integrated-60-gene-atlas) | Symbols, biological domains and linked gene cards |
| Gene annotations | [Annotation register](../06_RESOURCES/Genomics/REFERENCES/ANNOTATION_SOURCE_REGISTER.md) | Stable identifiers, annotation sources and review dates |
| Evidence limits | [Gene evidence matrix](../06_RESOURCES/Genomics/REFERENCES/GENE_EVIDENCE_MATRIX.md) | Study design, supported claims and review extent |
| R and visualization | [R tools](../06_RESOURCES/R/README.md) | Summaries, plots, annotations and companion tests |
| Scientific writing | [Manuscript resources](../06_RESOURCES/LaTeX/README.md) | Bibliography structure and manuscript source |

## Choose a source for the question

Use language manuals for syntax, package vignettes for API behavior, primary papers for study methods and findings, annotation records for gene identity, and reporting checklists for disclosure requirements. Record the version and date relevant to the analysis. An abstract-level reading is insufficient to reproduce a paper's full method.

## Record an evidence-to-code decision

For each adopted method, record the citation, source version, study assumption, proposed implementation, expected output, failure case and validation result. Keep candidate methods separate from methods actually executed. The source registers contain bibliographic and structural checks; the execution record belongs to the individual analysis.
