# 6. From a Rust object to a research-quality pipeline

[← Cargo and testing](05_cargo_testing_and_quality.md) · [Course contents](README.md) · [Next: practice and mastery](07_practice_and_mastery.md) · [Book: research evidence](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-8-from-measurements-to-scientific-evidence)

Everything earlier prepares you to answer the scientific question: **which observation does this row represent, how was it measured, and which information may this fit legitimately see?** The type system helps express that contract, while scientific validation, privacy and provenance enforce it.

## Start with the breast cancer book

| Book chapters | Research meaning | Rust design |
| --- | --- | --- |
| [1–2: people and specimens](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-2-understanding-the-breast-cancer-dataset) | One person may yield several dependent records | Validated `Specimen` objects, person-unique partitions, checked relationships |
| [3: measurements](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-3-how-researchers-measure-genes) | Raw counts, normalized data and logarithms are different | Explicit units/assay version, `Option<f64>` for true missingness, finite checks |
| [4–7: biology and gene atlas](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-6-the-integrated-60-gene-atlas) | ESR1/CD8A and others are annotated genes, not automatic predictive features | `GeneAnnotation` is distinct from measured feature columns |
| [8–9: evidence and figures](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-8-from-measurements-to-scientific-evidence) | Pairing, confounding, comparisons and denominators | Person-level grouping, train-only fit objects and checks |
| [10–12: interpretation and reporting](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-10-what-the-data-cannot-tell-us) | Correlation is not mechanism or clinical utility | Model limitations, no identifier-bearing exports, reproducible audits |

The book's **60 gene cards** are a curated teaching atlas. The existing G3 executable uses **48 anonymous synthetic features** on **60 fictional people**, not expression data from those named genes. This course lab uses still smaller invented values to teach code structure. Neither is a TCGA experiment.

## Step 1: validate identities before statistics

`objects::Specimen::new` rejects empty/control-character names and invalid observed values. `objects::Pair::new` checks the two tissues belong to the same fictional person. Then `engineering::validate_person_split` requires complete pairs in each partition and disjoint person sets:

~~~rust
// From the tested lab API; these are fictional records.
use breast_cancer_rust_lab::objects::{Specimen, Tissue};
use breast_cancer_rust_lab::engineering::validate_person_split;

let training = vec![
    Specimen::new("Demo1", Tissue::Comparator, Some(10.0)).unwrap(),
    Specimen::new("Demo1", Tissue::Tumor, Some(20.0)).unwrap(),
];
let assessment = vec![
    Specimen::new("Demo2", Tissue::Comparator, None).unwrap(),
    Specimen::new("Demo2", Tissue::Tumor, Some(30.0)).unwrap(),
];
assert!(validate_person_split(&training, &assessment).is_ok());
~~~

The `unwrap` calls above are safe **only because these are hardcoded fixed test fixtures**. An input adapter reading actual data would propagate the constructor error and stop. The two specimens per person are not two independent people. Real studies may have unmatched or longitudinal samples; you must create a new sampling protocol, not weaken this exercise's declared synthetic pair contract.

## Step 2: fit only on development/training values

`MedianPreparation::fit` takes the training specimens, extracts valid observed measurements, computes a median and stores it privately. `transform` then fills missing values in assessment specimens with that *stored training median*. It cannot silently recompute from the test group.

~~~rust
use breast_cancer_rust_lab::engineering::MedianPreparation;
let preparation = MedianPreparation::fit(&training).unwrap();
assert_eq!(preparation.median(), 15.0);
assert_eq!(preparation.transform(&assessment).unwrap()[0], 15.0);
~~~

Change an assessment value from 30 to 30,000 and rerun: the **training median must remain 15**. The lab's `assessment_mutation_cannot_change_fitted_median` test enforces this. This is an *educational median-only transformation*, not a complete RNA-seq normalization pipeline or a feature-selected model.

## Step 3: understand where learning begins

A fully specified machine-learning procedure would add **separate, reviewed** modules for features, targets, grouping/split maps, train-only transforms, model fitting, tuning, prediction, held-out metrics and research reporting.

~~~text
Study question + permitted data
       ↓
Validate person / specimen / assay / label / provenance
       ↓
Reserve assessment people before fitting anything
       ↓
For each development training fold:
    fit preprocessing and feature selection only there
    fit model, score on its own inner validation people
       ↓
Choose settings on development data only
       ↓
Evaluate the full chosen procedure on held-out people
       ↓
Record denominators, uncertainty, limits and provenance
       ↓
Independent review before any research-model release
~~~

The [native Rust G3 experiment](../../04_machine_learning/rust-native-training.md) uses a fixed Linfa logistic objective and separate Python numerical reference, not the simple course lab. The [ML guide](../../04_machine_learning/visual-data-guide.md) explains nested tuning and leakage in detail. **Changing a variable is not approval to change a research endpoint, use reserved people for fitting or unlock controlled data.**

## Step 4: avoid common biomedical category errors

- `person_id` is a grouping key, not a model feature. `specimen_id` locates an observation but must not become predictive signal.
- A tissue-category label does **not** automatically represent diagnosis, subtype, survival or treatment response.
- A gene's annotation domain (hormone, immune, stromal) is not its measured expression or proof of causal mechanism.
- Median imputation and z-scoring do **not** substitute for declared sequencing normalization or batch/QC methods.
- A classifier trained on specimen categories cannot diagnose cancer in an unscreened population merely because test accuracy is high.
- A good synthetic result cannot validate clinical deployment, future recurrence or generalization to new hospitals.

## Step 5: data access, privacy and provenance

TCGA-BRCA belongs to the NCI Genomic Data Commons, which distinguishes open- and controlled-access files. **Verify individual GDC file access status and applicable use terms before any planned real-data work.** Public availability does not eliminate privacy, consent or small-group re-identification risks. Do not commit individual clinical records, genomic matrices, identifiers, controlled files, model weights or row-level predictions to public Git. Do not print participant identifiers to CI logs or submit protected inputs to AI tools.

The [private research workflow](../../docs/research-workflow.md#2-specify-input-and-access-contracts) and [Rust engineering handbook](../../02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md) impose stronger research-admission, reproducibility and numerical checks. The separate [TCGA guard and configuration-runner draft PR](https://github.com/pskeffington/pauls_notes/pull/7) is not an automatic authorization for real-data training.

**Mandatory notice:** Research and education only. This lab is not a medical device, a clinical prediction model, a validated classifier or advice about diagnosis, treatment or prognosis.

## Next engineering gate

Once you can pass the lab's tests and explain the biological unit of each row, work through the [full Chapter 11 paired exercise](../../02_biomedical_coding/examples/book_paired_specimens.rs), then study [Rust engineering best practices](../../02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md) and the [native logistic objective](../../04_machine_learning/rust-training-protocol.md). A future real-data adapter requires **a distinct approved protocol** and independent privacy/scientific review.

[Next: practice and mastery →](07_practice_and_mastery.md)
