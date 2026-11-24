# Computational Oncology — Independent Open Textbook

**Computational Oncology: A Clinician–Scientist's Guide**

[Paul's Notes](../README.md) · [Task-first navigation](../docs/NAVIGATION.md) · [Chapter roadmap](ROADMAP.md) · [Biostatistics learning](../03_learning/bio_stats/README.md)

A ten-part, 60-chapter independent learning architecture spanning cancer biology, quantitative reasoning, study design, clinical data engineering, genomics, imaging, machine learning, applied AI and reproducible research. Seven manuscript chapters and the introduction are drafted; **none are yet independently peer reviewed or released as final textbook chapters**.

## Start reading

Read the original [Introduction — Why Cancer Research Matters](INTRODUCTION.md), then follow the drafted opening sequence.

For an active breast cancer study, use the [investigator pathway](../docs/NAVIGATION.md#breast-cancer-investigator-pathway). The expanded [clinical-data chapter](chapters/CO-02-clinical-oncology-data.md) covers patient/specimen lineage, receptor and molecular labels, breast-specific endpoints, TCGA/WDBC source selection and analysis denominators. The [applied data-science opening](../03_learning/INTRODUCTION_TO_DATA_SCIENCE.md) supplies a worked introduction to the question-to-result reasoning. Continue with the [data dictionary and join exercise](chapters/CO-04-data-literacy.md) to preserve record units and denominators, then the [probability and Bayes chapter](chapters/CO-07-randomness-and-probability.md) to distinguish conditioning, predictive values and uncertainty.

| Chapter | Clinical and scientific question | Manuscript status |
| --- | --- | --- |
| [CO-01: Cancer Biology](chapters/CO-01-cancer-biology.md) | How does cancer biology become a research variable? | Draft; section-linked evidence |
| [CO-02: Clinical Oncology Data](chapters/CO-02-clinical-oncology-data.md) | How do clinical observations become usable data? | Draft; section-linked evidence |
| [CO-03: Molecular Foundations](chapters/CO-03-molecular-foundations.md) | What do molecular assays actually measure? | Draft; section-linked evidence |
| [CO-04: Data Literacy](chapters/CO-04-data-literacy.md) | What does a row represent and which units are independent? | Draft; section-linked evidence |
| [CO-05: Essential Mathematics I](chapters/CO-05-essential-mathematics-i.md) | Which quantities, denominators, units and logarithms make oncology calculations meaningful? | Draft; section-linked evidence and executable labs |
| [CO-06: Essential Mathematics II](chapters/CO-06-essential-mathematics-ii.md) | How do derivatives, matrices and optimization explain statistical models? | Draft; [historical verification record](evidence/CO-06-VALIDATION-2026-10-27.md) and executable labs |
| [CO-07: Randomness and Probability](chapters/CO-07-randomness-and-probability.md) | How do conditioning, prevalence and test assumptions determine predictive values? | Draft; [Python/R execution and review scope](evidence/CO-07-VALIDATION-2026-11-21.md) |

Continue with the [complete 60-chapter roadmap](ROADMAP.md). Chapters CO-08 through CO-60 remain planned; do not assume that a roadmap title is an authored chapter.

## References and evidence

Every H2/H3 section in the **current introduction and CO-01 through CO-07 drafts** has directly clickable source references. The [linked bibliography](evidence/SOURCES.md) and [curated source registry](evidence/source-registry.json) records titles, URLs, roles and source context. The [section citation crosswalk](evidence/section-citations.json) supports machine retrieval, and the [evidence policy](evidence/README.md) describes the scientific review requirements. A [citation validator](../scripts/validate_oncology_citations.py) checks that every drafted section retains those links.

**Citation coverage is not equivalent to scientific peer review.** Linked sources should be checked against the particular claim and intended research context before a chapter is marked reviewed or released. Original numerical examples use invented teaching data.

## Existing foundation libraries

| Need | Resource |
| --- | --- |
| Biostatistics and selection of methods | [Statistics decision guide](../03_learning/biomedical-statistics-decision-guide.md) |
| Scientific computing with worked examples | [Computing subjects](../03_learning/README.md) |
| Independent oncology mathematics labs | [Python and R examples](examples/README.md) |
| Clinical and molecular case context | [Genomics reference](../06_RESOURCES/Genomics/README.md) |
| Machine learning and validation | [Machine learning guide](../04_machine_learning/README.md) |
| Methods literature and code quality | [Biomedical coding](../02_biomedical_coding/README.md) |
| Machine-readable book state | [Chapter manifest](book-manifest.json) |

## Publication standard

The book advances through **planned → draft → tested → reviewed → released**. Learning outcomes, synthetic laboratory checks, scientific references and editorial/source verification are separate requirements. No part of the manuscript confers medical credentials, validates a clinical model or substitutes for professional care or supervised medical training.

The educational writing, organization and examples are independently developed; third-party research is cited rather than reproduced.
