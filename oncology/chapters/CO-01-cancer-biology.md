# CO-01 — Cancer Biology for Quantitative Investigators

*Computational Oncology: A Clinician–Scientist's Guide · Part I · Draft 0.1*  
[Book home](../README.md) · [Introduction](../INTRODUCTION.md) · [Roadmap](../ROADMAP.md) · [Genomics reference](../../06_RESOURCES/Genomics/README.md)

## Why this chapter matters

An oncologist may see a tumor as a diagnosis, a pathologist as a tissue specimen, a molecular biologist as a set of altered pathways, and a data scientist as an array of measurements. All can describe the same disease, but they do not observe the same unit. Computational oncology succeeds when it connects these representations without mistaking a molecular readout for a patient outcome or an association for a treatment effect.

**Guiding question:** How does a biological process become a defensible variable in an oncology study?

**Section references:** [What Is Cancer?](https://www.cancer.gov/about-cancer/understanding/what-is-cancer) · [Hallmarks of Cancer: New Dimensions (2022)](https://doi.org/10.1158/2159-8290.CD-21-1059)

## Learning outcomes

By the end of this chapter, the reader should be able to:
1. Explain why cancer is a diverse class of diseases arising through acquired and inherited influences rather than one homogeneous disorder.
2. Distinguish oncogenic signaling, loss of growth control, genomic instability, tumor microenvironment interactions, invasion and metastasis.
3. Explain the difference among person, tumor, lesion, tissue block, specimen, cell and molecular measurement.
4. Define an outcome, exposure, biomarker, predictor, mediator and potential confounder in a hypothetical oncology study.
5. Identify one source of selection bias, one form of biological heterogeneity, and one potential data-leakage mechanism in a multi-specimen analysis.
6. State what can and cannot be inferred from a molecular measurement without independent clinical evidence.

**Section references:** [What Is Cancer?](https://www.cancer.gov/about-cancer/understanding/what-is-cancer) · [About Biomarkers and Qualification / BEST](https://www.fda.gov/drugs/biomarker-qualification-program/about-biomarkers-and-qualification)

## 1. What cancer represents

Normal cells respond to external and internal signals governing proliferation, differentiation, damage repair and programmed death. Malignancy may emerge when evolving cell populations acquire combinations of changes that permit abnormal growth and survival. These changes may involve DNA sequence alterations, copy-number changes, epigenetic regulation, gene expression and cell–environment interactions. They are neither identical across cancers nor necessarily shared among all cells of a single tumor.

**A tumor is a changing biological population, not a single constant measurement.** A sample may contain malignant cells alongside stromal, immune, vascular and other nonmalignant cells, consistent with the [NCI overview of the tumor microenvironment](https://www.cancer.gov/about-cancer/understanding/what-is-cancer). A genomic profile therefore reflects specimen composition, assay characteristics and analytical choices as well as cancer biology.

Cancer development can be described by multiple interacting processes: growth signaling, evasion of growth suppression and cell death, genomic instability, altered metabolism, immune interactions and tissue invasion. These are explanatory frameworks, not a universal checklist that every tumor must satisfy in the same order (see [Hallmarks of Cancer: New Dimensions](https://doi.org/10.1158/2159-8290.CD-21-1059)). Consult the primary Hallmarks of Cancer literature and up-to-date authoritative disease-specific sources before treating a general mechanism as established for a particular clinical setting.

**Section references:** [Hallmarks of Cancer: New Dimensions (2022)](https://doi.org/10.1158/2159-8290.CD-21-1059) · [What Is Cancer?](https://www.cancer.gov/about-cancer/understanding/what-is-cancer)

## 2. From mechanism to measurement

| Biological concept | Example observation | What the observation does not prove |
| --- | --- | --- |
| Genomic alteration | Variant detected in tumor sequencing | That the variant drives disease or predicts treatment benefit |
| Copy-number change | Increased copies of a genomic region | That the corresponding protein is active in every cell |
| Transcriptional activity | RNA abundance in a bulk specimen | That each cell expresses the transcript equally |
| Protein expression | Immunohistochemical staining | That the clinical outcome is caused by the protein |
| Tumor burden | Imaging-derived lesion dimension | That all sites of disease or microscopic changes are captured |
| Treatment response | Recorded change under a stated response criterion | That a comparison without a control group identifies causal treatment benefit |
| Recurrence | Clinically adjudicated event after a time origin | That follow-up is complete or censoring is ignorable |

Every analysis needs an explicit measurement model: What biological quantity is of interest? How was it sampled? Which instrument and preprocessing steps produced the data? What uncertainty or misclassification remains?

**Section references:** [About Biomarkers and Qualification / BEST](https://www.fda.gov/drugs/biomarker-qualification-program/about-biomarkers-and-qualification) · [Biomarker Testing for Cancer Treatment](https://www.cancer.gov/about-cancer/treatment/types/biomarker-testing-cancer-treatment)

### Key distinction: biomarker roles

A **diagnostic** marker helps classify an existing condition; a **prognostic** marker is associated with outcomes independent of a specific treatment comparison; a **predictive treatment-effect** marker identifies variation in the relative effect of a treatment (see the [FDA–NIH BEST glossary](https://www.ncbi.nlm.nih.gov/books/NBK326791/)). A feature associated with outcomes among treated patients alone is not automatically a predictive treatment-effect marker. That claim generally requires a credible comparison of treatment effects across marker-defined groups.

**Section references:** [About Biomarkers and Qualification / BEST](https://www.fda.gov/drugs/biomarker-qualification-program/about-biomarkers-and-qualification) · [BEST Biomarkers, EndpointS, and other Tools](https://www.ncbi.nlm.nih.gov/books/NBK326791/)

## 3. The hierarchy of observational units

A single person may contribute multiple tumors or lesions, multiple specimens per lesion, and many cells per specimen. Molecular assays add thousands of measurements to each biological unit.

```text
Person
  └─ Tumor / lesion
       └─ Specimen / biopsy
            └─ Cells or assay aliquots
                 └─ Molecular features
```

This is not a guarantee that every study contains all layers. It is a prompt to document which units are observed and which units are independent. If specimens from one person appear in both training and testing, a classifier may memorize individual characteristics instead of learning to generalize to new people. Splitting rows at random does not solve this dependence.

**Example:** Twelve people each provide two tissue specimens. The dataset has 24 specimen rows but only 12 people. If the research claim is about prediction for unseen people, partitioning must occur by person, not specimen. Twenty-four rows are not equivalent to 24 independent participants.

**Section references:** [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization) · [Kapoor and Narayanan: Data Leakage (2023)](https://doi.org/10.1016/j.patter.2023.100804)

## 4. Heterogeneity and sampling

**Between-patient heterogeneity** includes differences in disease biology, age, treatment history and comorbidities. **Within-patient heterogeneity** includes differences between lesions, between tumor regions and across time. A pre-treatment biopsy and a post-treatment specimen are related observations, not independent replicates.

Sampling may be selective: only patients with sufficient tissue, follow-up, treatment access or assay quality enter an analysis. If inclusion depends on factors related to both exposure and outcome, the analyzed population may not represent the clinical population for which the conclusion is intended.

A sound data dictionary specifies participant IDs, lesion IDs, specimen IDs, collection time, assay version, measurement units, missingness codes and endpoint definitions. Identifiers must never be silently reinterpreted as numerical predictors.

**Section references:** [Hallmarks of Cancer: New Dimensions (2022)](https://doi.org/10.1158/2159-8290.CD-21-1059) · [What Is Cancer?](https://www.cancer.gov/about-cancer/understanding/what-is-cancer)

## 5. Worked synthetic scenario: molecular signal and recurrence

Suppose investigators generate **invented teaching data** for 40 people with a solid tumor. Each person has one baseline specimen and some have a second specimen collected later. The synthetic dataset includes a normalized gene-expression measurement, treatment indicator, event time and recurrence indicator.

The clinical research question is whether a baseline molecular measurement is associated with subsequent recurrence risk. Before fitting a Cox model, the analyst must specify:

1. **Time origin:** e.g., the date of a defined baseline assessment, consistently applied.
2. **Population:** who was eligible, and how missing assays and early events are handled.
3. **Endpoint:** precisely what constitutes recurrence, versus death or another event.
4. **Measurement timing:** baseline expression must be measured before the outcome and must not incorporate post-outcome information.
5. **Independence:** one person-level record for a person-level prognosis model, or a documented method for correlated observations.
6. **Interpretation:** an adjusted association is not necessarily a causal effect or a validated treatment-selection rule.

A second specimen obtained after treatment must not be treated as a baseline predictor without explicitly changing the question and handling its timing.

**Section references:** [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/) · [Overall Survival (NCI Dictionary)](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/overall-survival)

### Small quantitative exercise

If 40 people contribute 65 specimens, what is the person count? **40.** What is the specimen count? **65.** Which is the denominator for a claim about the number of distinct participants? **40.** If 9 of the 40 people experience a recorded recurrence during varying follow-up, why is 9/40 not a complete estimate of a fixed-time recurrence risk? Because observation times and censoring may differ, and competing events or eligibility may affect interpretation.

**Section references:** [Overall Survival (NCI Dictionary)](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/overall-survival) · [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/)

## 6. Three questions before computation

1. **What biological process or patient outcome is actually being represented?**
2. **What unit produced each observation, and what dependencies exist between rows?**
3. **What clinical claim would the analysis be unable to support even if the software runs perfectly?**

These questions establish a bridge to [data literacy](../../03_learning/objects-and-meaning.md), [study design](../../docs/research-workflow.md), [statistical method selection](../../03_learning/biomedical-statistics-decision-guide.md), and [leakage-aware model training](../../04_machine_learning/visual-data-guide.md).

**Section references:** [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/) · [About Biomarkers and Qualification / BEST](https://www.fda.gov/drugs/biomarker-qualification-program/about-biomarkers-and-qualification)

## 7. Mastery checks

**Recall.** Explain how a tumor can contain molecularly different cell populations without being a distinct cancer in every cell.

**Interpretation.** A specimen-level model achieves high accuracy when tissue from the same donor is included in development and evaluation. Describe the possible leakage mechanism and redesign the split.

**Design.** Distinguish a prognostic expression association from evidence that a targeted treatment works better for marker-positive people.

**Critical appraisal.** A paper reports increased expression in tumor specimens relative to nearby normal tissue. Identify three limitations before inferring clinical usefulness.

**Section references:** [Kapoor and Narayanan: Data Leakage (2023)](https://doi.org/10.1016/j.patter.2023.100804) · [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/)

### Answer guide (condensed)

- Intratumoral heterogeneity reflects variation among interacting cell populations and changing evolutionary states.
- Split entire people, not their individual specimens, when generalization to new people is the target.
- A treatment-effect biomarker requires evidence about *comparative treatment benefit*, rather than association with outcomes in one treatment group.
- Examine tissue composition, pairing/selection, assay normalization, batch effects, and external clinical validation before extrapolating from expression differences.

**Section references:** [About Biomarkers and Qualification / BEST](https://www.fda.gov/drugs/biomarker-qualification-program/about-biomarkers-and-qualification) · [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/)

## 8. Independent further reading

- Hanahan D, Weinberg RA. *Hallmarks of Cancer.* Cell (2000). DOI: [10.1016/S0092-8674(00)81683-9](https://pubmed.ncbi.nlm.nih.gov/10647931/).
- Hanahan D, Weinberg RA. *Hallmarks of Cancer: The Next Generation.* Cell (2011). DOI: [10.1016/j.cell.2011.02.013](https://pubmed.ncbi.nlm.nih.gov/21376230/).
- Hanahan D. *Hallmarks of Cancer: New Dimensions.* Cancer Discovery (2022). DOI: [10.1158/2159-8290.CD-21-1059](https://doi.org/10.1158/2159-8290.CD-21-1059).
- National Cancer Institute, [What Is Cancer?](https://www.cancer.gov/about-cancer/understanding/what-is-cancer) — introductory authoritative overview; verify current page before citing specific clinical claims.

**Editorial and evidence status:** draft, not independently reviewed. References are suggested original reading; this chapter does not assert independent replication or literature-level validation.

**Section references:** [Hallmarks of Cancer: New Dimensions (2022)](https://doi.org/10.1158/2159-8290.CD-21-1059) · [What Is Cancer?](https://www.cancer.gov/about-cancer/understanding/what-is-cancer)

