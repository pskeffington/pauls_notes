# CO-03 — Molecular Foundations: From DNA to Cancer Biomarkers

*Computational Oncology: A Clinician–Scientist's Guide · Part I · Draft 0.1*  
[Book home](../README.md) · [CO-02: Clinical oncology data](CO-02-clinical-oncology-data.md) · [CO-01: Cancer biology](CO-01-cancer-biology.md) · [Genomics companion](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md)

## Why molecular data matter

A clinician may ask whether a tumor contains a therapeutically relevant alteration. A laboratory may report DNA sequence variants, RNA abundance, protein staining or copy-number estimates. A bioinformatician may receive thousands of rows, each indexed by a gene identifier. All three describe different observations. A fundamental task of molecular oncology is learning which biological claims a measurement can reasonably support.

Cancer involves genetic and nongenetic changes operating in a changing cellular environment. A tumor's DNA sequence does not directly tell us the amount of RNA it produces; RNA abundance does not directly determine protein quantity or activity; and a protein's detection does not independently establish response to therapy. Computational analysis must respect these biological layers.

**Guiding question:** What does each molecular assay actually measure, and how does its meaning constrain a cancer research conclusion?

**Section references:** [Biomarker Testing for Cancer Treatment](https://www.cancer.gov/about-cancer/treatment/types/biomarker-testing-cancer-treatment) · [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/)

## Learning objectives

The reader should be able to:
1. Relate DNA, RNA, proteins and signaling networks without assuming a one-to-one correspondence between their measurements.
2. Distinguish somatic variants from inherited variants and describe why both raise distinct interpretive and governance questions.
3. Separate variant calls, copy number, methylation, expression counts and protein assays.
4. Explain how specimen purity, sampling time, batch, measurement depth and normalization affect observed values.
5. Compute a basic log2 ratio and explain why it is not a complete differential-expression analysis.
6. Explain the difference between a biological mechanism, a candidate biomarker and a clinically validated test.
7. Design a minimal metadata contract for an oncology molecular experiment.

**Section references:** [About Biomarkers and Qualification / BEST](https://www.fda.gov/drugs/biomarker-qualification-program/about-biomarkers-and-qualification) · [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/)

## 1. Biological information and its regulation

DNA encodes sequences from which RNAs can be transcribed. Some RNAs are translated into proteins; others have regulatory or structural functions. Protein abundance and activity depend on additional steps, including translation, modification, localization, degradation and interaction with other molecules. Epigenetic and regulatory processes influence which genes are expressed and under what conditions.

The familiar DNA → RNA → protein teaching model is a useful entry point, but it is not a predictive formula that maps one genomic measurement into one clinical outcome. Oncogenic signaling emerges from networks of interacting components. A change in one component may have different consequences in different tissues or molecular backgrounds.

For each biological claim, ask which layer was observed:
- DNA: sequence, structural alteration or copy-number state.
- Chromatin and epigenetic assays: regulatory features under assay-specific definitions.
- RNA: transcripts or gene-level abundance at a given collection time.
- Protein: abundance, localization, staining or post-translational state.
- Cellular or tissue phenotype: proliferation, morphology, invasion or immune context.
- Clinical outcome: survival, recurrence, toxicity, symptom burden or therapeutic response.

A molecular signal becomes clinically useful only when measurement reliability, biological interpretation and appropriate clinical evidence support the proposed use.

**Section references:** [What Is Cancer?](https://www.cancer.gov/about-cancer/understanding/what-is-cancer) · [Hallmarks of Cancer: New Dimensions (2022)](https://doi.org/10.1158/2159-8290.CD-21-1059)

## 2. Somatic change, germline variation and tumor evolution

A **somatic alteration** is acquired in cells during life and may be present in a subset of tumor cells. A **germline variant** is present in the inherited genetic background and may be found throughout the body. Not every somatic change is a driver of malignancy; many changes may be passengers or uncertain in significance. Even a plausible driver alteration does not guarantee a drug will work for a particular person.

A tumor can contain multiple related cellular populations. Evolutionary selection, local microenvironment and therapy can shift their composition over time. A molecular profile from one biopsy therefore represents a particular specimen at a particular time. It may not fully describe every lesion or later state.

Tumor–normal comparisons can help distinguish some acquired alterations, but matched normal material can also create incidental germline findings. The existence of tumor and normal samples does not by itself establish authorization to publish participant-linked variant data. Access control and consent remain dataset-specific.

**Section references:** [What Is Cancer?](https://www.cancer.gov/about-cancer/understanding/what-is-cancer) · [Biomarker Testing for Cancer Treatment](https://www.cancer.gov/about-cancer/treatment/types/biomarker-testing-cancer-treatment)

## 3. Molecular measurements are not interchangeable

| Assay or reported quantity | Example output | Common inference error |
| --- | --- | --- |
| Tumor DNA sequencing | Variant and allele fraction | Treat any detected variant as causal or actionable |
| Copy-number analysis | Estimated gain/loss in a segment | Equate copy gain with protein overexpression in all cells |
| RNA sequencing | Raw gene counts; transformed abundance | Treat raw counts, TPM and log-transformed expression as identical |
| Immunohistochemistry | Protein staining and scoring | Substitute a transcript threshold for a validated protein assay classification |
| In situ hybridization | Signal-based assessment of genomic amplification | Ignore assay-specific scoring rules or specimen context |
| DNA methylation profiling | Probe- or region-level methylation signal | Assume every methylation difference changes transcription |
| Single-cell RNA sequencing | Count matrix indexed by cell | Treat thousands of cells from one patient as independent patients |
| Spatial profiling | Features and positions within a tissue section | Ignore spatial sampling and section-level dependence |

Assay metadata must identify platform, reference/annotation version, protocol, processing release and sample provenance. A file named `expression.csv` is not a sufficiently specified biological measurement.

**Section references:** [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/) · [About Biomarkers and Qualification / BEST](https://www.fda.gov/drugs/biomarker-qualification-program/about-biomarkers-and-qualification)

## 4. A recurring breast cancer example: ESR1 and ERBB2

The gene **ESR1** encodes estrogen receptor alpha; clinical estrogen-receptor status is assessed through specified diagnostic procedures, commonly protein-based immunohistochemical testing. **ERBB2** encodes HER2, a receptor involved in growth signaling. HER2 status is determined using established clinical testing and interpretation frameworks, including protein expression and, when appropriate, gene amplification assessment.

A molecular data table may include `ESR1_expression` and `ERBB2_expression`; the [NCI breast cancer biomarker reference](https://www.cancer.gov/types/breast/diagnosis/breast-cancer-biomarker-tests) explains why clinical receptor status relies on defined diagnostic assays. Those numerical values are not automatically equivalent to clinical `ER_status` or `HER2_status`. Such equivalence requires independently established assay-specific interpretation; thresholds from one platform or study cannot be transferred without validation.

This distinction also matters for treatment-effect prediction. If patients with higher ESR1 RNA levels have better recorded outcomes, the observation alone does not establish that a particular therapy causes the benefit or that an RNA cutoff should guide care. The analysis must account for disease context, treatments, outcome definitions, confounding, and evidence about comparative treatment effects.

The existing [60-gene breast cancer companion](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) offers extended biological reading. The book's executable feature-selection demonstrations use **invented features** and must not be presented as a validated classifier using the companion's 60 named genes.

**Section references:** [Tests for Breast Cancer Biomarkers](https://www.cancer.gov/types/breast/diagnosis/breast-cancer-biomarker-tests) · [Biomarker Testing for Cancer Treatment](https://www.cancer.gov/about-cancer/treatment/types/biomarker-testing-cancer-treatment)

## 5. From sequence reads to a count matrix

A simplified bulk RNA-seq analysis has the following conceptual stages:

1. Obtain samples with documented biological replication and collection metadata.
2. Extract and assess RNA, recording assay quality.
3. Generate reads and perform documented mapping or quantification.
4. Produce counts at an identified gene/transcript annotation level.
5. Inspect sample quality, depth, batch and potential composition differences.
6. Apply a normalization and statistical model appropriate to the analysis objective.
7. Estimate an effect and its uncertainty, accounting for study design and multiple comparisons.
8. Review biological interpretation and evaluate generalization to independent material.

The [NCI GDC mRNA pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/) provides raw gene-level counts as well as transformed representations, including FPKM and TPM. These have different definitions and uses; do not provide TPM as input to a differential-expression method that expects untransformed counts without a methodologically justified alternative.

For illustration, let `K[i,j]` be the nonnegative integer read count for gene *i* in specimen *j*. The specimen is a column in the usual gene-by-sample count matrix. The biological replicate count is determined by independent participants or experimental units, not the number of sequenced reads.

A standard negative-binomial differential-expression framework often expresses count variation through a mean and dispersion, with normalization for sequencing exposure and design-specific predictors. [DESeq2](https://doi.org/10.1186/s13059-014-0550-8) is one well-documented example; its original methods paper should be read together with current versioned package documentation. This chapter does not implement or validate a complete DESeq2 analysis.

**Section references:** [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/) · [Love et al., DESeq2 (2014)](https://doi.org/10.1186/s13059-014-0550-8)

## 6. A mathematical miniature: effect size versus evidence

Suppose the average normalized abundance of an invented gene is 40 units in one group and 80 in another. The descriptive fold ratio is `80 / 40 = 2`; the log2 fold ratio is `log2(2) = 1`. Reversing the comparison gives `log2(40 / 80) = -1`.

That calculation states the **direction and magnitude of the observed ratio**, subject to the measurement definition. It does not calculate a standard error, confidence interval, p-value or posterior probability. It also does not establish that the groups differ biologically rather than through batch, cell composition, selection or sampling variability.

A fully worked differential-expression analysis needs raw or otherwise appropriate inputs, normalization, design matrix, dispersion/variance assumptions, independent biological units, effect estimation, multiple-testing treatment and appropriate diagnostics.

**Section references:** [Love et al., DESeq2 (2014)](https://doi.org/10.1186/s13059-014-0550-8) · [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/)

### Executable base-R thought experiment

```r
# Invented abundance values; not RNA-seq raw counts or a DE test.
control <- c(38, 42, 40, 40)
case <- c(76, 84, 80, 80)

stopifnot(length(control) == 4L, length(case) == 4L)
ratio <- mean(case) / mean(control)
lfc <- log2(ratio)

stopifnot(isTRUE(all.equal(ratio, 2)),
          isTRUE(all.equal(lfc, 1)))

# Descriptive signal does not establish clinical significance.
```

A key learning exercise is explaining why four values from **four independent people** differ scientifically from four aliquots of a **single specimen**, even when the numbers and resulting means are identical.

**Section references:** [Love et al., DESeq2 (2014)](https://doi.org/10.1186/s13059-014-0550-8) · [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/)

## 7. Purity, batch, normalization and missingness

**Tumor purity:** A bulk tissue specimen includes malignant and nonmalignant cells. Changes in measured expression may reflect differing mixtures of cell types rather than altered expression within cancer cells.

**Batch:** Collection dates, reagent lots, sequencing instruments and preparation sites may influence measurements. If all case samples are processed in one batch and controls in another, disease and batch are inseparable in the observed comparison without additional design information.

**Normalization:** A raw count is affected by library size and technical/biological features. Normalization and transformations depend on the intended estimand and assay; no single transformation fixes every source of bias.

**Missingness:** A gene may have few or zero assigned reads because of biological absence, insufficient depth, feature annotation, processing filters or assay problems. A zero is not always a failed test and a missing specimen is not a zero-count sample. Track these states separately.

**Feature identifiers:** Gene symbols may change or alias; stable identifiers and annotation release should be retained. Verify duplicates and mapping losses before merging expression matrices with clinical annotations.

**Section references:** [Biospecimen Data Standardization](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization) · [Love et al., DESeq2 (2014)](https://doi.org/10.1186/s13059-014-0550-8)

## 8. Minimal molecular dataset contract

| Field | Essential meaning |
| --- | --- |
| `person_id`, `specimen_id`, `aliquot_id` | Hierarchical keys, with expected cardinality |
| `collection_time` | When biology was sampled relative to treatment and endpoints |
| `anatomical_source`, `specimen_type` | Tumor/normal designation and acquisition context |
| `platform`, `assay_protocol` | Instrument and processing method |
| `reference_genome`, `annotation_release` | Genome build and feature coordinate system |
| `feature_id` | Versioned gene, transcript, variant or protein identifier |
| `measurement_scale`, `unit` | Raw counts, TPM, normalized intensity, IHC score, etc. |
| `quality_control` | QC results and exclusions without hiding failed samples |
| `batch_id` | Potential source of technical variation |
| `access_class`, `consent_scope` | Conditions for lawful processing and sharing |

The GDC case → sample → portion → analyte → aliquot hierarchy is a useful real-world example of why these identifiers cannot be casually collapsed. See the [GDC biospecimen documentation](https://gdc.cancer.gov/about-data/gdc-data-processing/biospecimen-data-standardization).

**Section references:** [Biospecimen Data (GDC Documentation)](https://docs.gdc.cancer.gov/Encyclopedia/pages/Biospecimen_Data/) · [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/)

## 9. Research exercises with answer guidance

1. **Assay meaning:** Why cannot `ERBB2_expression = 12` directly establish clinical HER2-positive status? *Check:* units, platform, validated clinical assay and scoring framework are unspecified.
2. **Direction:** A synthetic marker has means of 30 and 120 in groups A and B. Compute the B/A log2 ratio. *Check:* `log2(120/30) = 2`, without a claim about uncertainty.
3. **Independence:** There are 1,000 cells from five people. What sample size should not be used for a population-level patient claim? *Check:* 1,000 independent patients; clustering must be addressed.
4. **Confounding:** All tumor specimens are sequenced in batch A and normal specimens in batch B. Name the fundamental identification problem. *Check:* batch and tissue status are completely confounded.
5. **Clinical interpretation:** Explain the difference between a gene associated with survival and a validated treatment-selection biomarker. *Check:* clinical intended use, comparative treatment effect, measurement validity and independent evidence.
6. **Governance:** A controlled-access tumor–normal file is easy to download with credentials. Does that permit publishing it in an open teaching repository? *Check:* no; permissions and access controls must be examined independently.

**Section references:** [About Biomarkers and Qualification / BEST](https://www.fda.gov/drugs/biomarker-qualification-program/about-biomarkers-and-qualification) · [Love et al., DESeq2 (2014)](https://doi.org/10.1186/s13059-014-0550-8)

## 10. Primary and authoritative reading

- National Cancer Institute. [Biomarker Testing for Cancer Treatment](https://www.cancer.gov/about-cancer/treatment/types/biomarker-testing-cancer-treatment). Contrasts tumor testing with inherited-risk testing and explains limitations.
- NCI. [Tests for Breast Cancer Biomarkers](https://www.cancer.gov/types/breast/diagnosis/breast-cancer-biomarker-tests). ER, PR, HER2 and Ki-67 clinical measurement context.
- NCI Genomic Data Commons. [Genomic Data Processing](https://gdc.cancer.gov/about-data/gdc-data-processing/genomic-data-processing) and [mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/). Input counts and transformed expressions.
- Love MI, Huber W, Anders S. *Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2.* Genome Biology 15:550 (2014). [DOI:10.1186/s13059-014-0550-8](https://doi.org/10.1186/s13059-014-0550-8). Foundational differential-expression model and limitations.
- NCI. [TCGA Data Types Collected](https://www.cancer.gov/ccg/research/genome-sequencing/tcga/using-tcga-data/types). Different assay modalities and access distinctions.

**Review record:** Draft 0.1, independently written pedagogical synthesis with fabricated values; not independently scientifically reviewed or validated as clinical guidance. Sources were consulted during October 2026 authoring. Technical package-specific instructions require versioned confirmation when a full analysis is implemented.

**Next:** [CO-04 — Data Literacy and Observational Units](CO-04-data-literacy.md).

**Section references:** [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/) · [Tests for Breast Cancer Biomarkers](https://www.cancer.gov/types/breast/diagnosis/breast-cancer-biomarker-tests)

