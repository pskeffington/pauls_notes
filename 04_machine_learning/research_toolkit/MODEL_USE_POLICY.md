# Cancer research data, privacy and model-use policy

Authored by Paul Skeffington · Compiled with OpenAI

**Repository scope:** Paul's Notes supports research across **all cancer types, data providers, tumor sites and study modalities**. This policy applies to its code, AI-assisted research, Rust/Python/R outputs, CI, plots, manuscripts and future cancer modeling workflows. The [current breast cancer/TCGA-BRCA teaching case](../../docs/cancer-research-scope.md) is **one example**, not a limit on oncology research. References to "PPI" in earlier work orders mean PII/PHI or other protected/linkable participant information here.

## Safeguards applicable to every cancer data source

1. **Current public-repository execution is synthetic.** The checked-in models and variable-only runner use locally invented measurements and do not fit on patient-level TCGA-BRCA, any other real cancer cohort or restricted records. No model is authorized for individual diagnosis, screening, prognosis, treatment selection or clinical decision support.
2. **Verify data use at its actual source.** Independently record provider, accession/release, individual file or dataset access classifications, consent/license/reuse conditions, access date, checksum, cohort and security requirements. Public download availability alone does not imply anonymous or unrestricted data.
3. **Protect participant-linked data from every provider.** Do not commit or attach real downloaded clinical records, biospecimens, images, molecular matrices, participant/case/sample keys, row-level predictions, individual output tables, model weights or credentials to public Git, CI artifacts or unrestricted AI prompts. Follow separately approved storage and analysis arrangements for any authorized outside research.
4. **Treat pseudonyms and combinations as linkable.** A sample barcode or registry key may not reveal a name by itself, but linkage to other data, rare variants, clinical characteristics, timestamps and high-dimensional weights can create disclosure risks. Never attempt reidentification. Review small-cell disclosures and model inversion/memorization risk before any public derived-data release.
5. **Require a new protocol for new research.** Record the cancer context, observation unit (person, specimen, slide, scan, tile, cell, visit), assay or imaging scale, endpoint/timing, grouping, train-only transforms, tuning, uncertainty, privacy protections, independent review and approved publication form. New endpoints or sources are **not unlocked** by changing a JSON field or widening a source allowlist.

A successful regex scanner, .gitignore, or open-access flag cannot establish that a dataset or model has zero PII/PHI/reidentification risk. Absence of a known identifier is not evidence of privacy approval.

## TCGA-BRCA: the current GDC-specific worked example

The NCI Genomic Data Commons (GDC) provides TCGA records with distinct **`open` and `controlled`** access classes. See [GDC data access processes](https://gdc.cancer.gov/access-data/data-access-processes-and-tools) and [GDC analysis policies](https://gdc.cancer.gov/analyze-data/data-analysis-policies).

The [read-only GDC preflight](gdc_open_access_preflight.py) accepts only official file UUIDs with metadata explicitly stating `access=open`, case project exactly **`TCGA-BRCA`**, the reviewed file-type allowlist and a valid file size/checksum. It writes **aggregate metadata only**, makes **no file download** and performs **no model fit**. Even a passing record is **not permission to ingest it into the synthetic runner**, publish participant records or override Dartmouth's independent R18F/R19 admission for the related private study.

**This is a deliberately narrow *adapter contract*, not a global rule that oncology research must use TCGA or breast cancer.** Another TCGA project, GDC file type or source requires an independently reviewed adapter and study/access contract. Do not change `PROJECT` to a different project, relabel a different source as TCGA-BRCA, or relax `access=open` to make an unreviewed file pass.

## Non-TCGA studies and research modalities

Future approved cancer studies may use non-GDC sources and may study other cancers, imaging, tissue biology, public-health outcomes or multi-omics measurements. Each provider has its own provenance, terms, access process and citation rules. A GDC/TCGA `access=open` response is **not** an attribute of an unrelated source, and the TCGA-specific checker should **not** be used to approve those inputs. Create and review a provider-specific data adapter and a separate research protocol before any real-data processing. Controlled or ambiguously permitted participant data stay out of this public repo and its CI.

The [cancer-wide scope and independent-study contract](../../docs/cancer-research-scope.md) lists the minimal information required. The current frozen G0–G3/R3 breast-specimen numerical experiments are not evidence of cross-cancer generalization.

## Mandatory nonclinical notice and model card

> **RESEARCH AND EDUCATIONAL USE ONLY. NOT FOR CLINICAL USE.** Models and figures are methodological demonstrations, not validated medical devices, diagnostic tests, cancer-screening systems, clinical decision-support products or individualized prognosis/treatment tools. A good synthetic classification score or a narrow research cohort does not establish clinical benefit, causal effect, prospective performance or transportability to other cancers or populations.

Every public report or model card should identify: tumor/study context, target definition and intended use; **actual provider/source** (not assumed GDC), dataset/version and permitted access; independent person/specimen/image grouping; source/measurement/normalization; folds, training-only features, class mapping and evaluable denominators; held-out vs in-sample status; calibration, uncertainty, biases, missingness, limitations, external validation and source/code hashes. State `clinical_use_authorized=false`, `patient_level_training_authorized=false` and `real_cancer_data_processed=false` for the current synthetic runner. Missing requirements mean **exploratory / not clinically validated**.

## Attribution is source-specific

If an approved result **actually uses TCGA-derived data**, follow [NCI's TCGA citation instructions](https://www.cancer.gov/ccg/research/genome-sequencing/tcga/using-tcga-data/citing) and acknowledge:

> The results published or shown here are in whole or part based upon data generated by the TCGA Research Network: https://www.cancer.gov/tcga.

Also record the particular GDC TCGA files/cohort, release/access date and transformations. The [GDC paper by Heath et al. (2021)](https://doi.org/10.1038/s41588-021-00791-5) may be cited where relevant. **Do not use the TCGA acknowledgment for non-TCGA data or for examples based wholly on invented measurements.** For any other cancer provider, follow that source's specific attribution, consent and publication requirements.

## Public Git enforcement and its limits

- The [tracked/staged public-data scanner](../../scripts/check_public_data_boundaries.py) and [explicit structured-file register](../../scripts/public_data_assets.json) apply **regardless of cancer site or provider**. New public CSV/TSV/JSON artifacts require source/content review and registration, not a silent exception for "open" data. CI should run the scanner on every PR and a mandatory `main` check must be configured by repository administration.
- Local `.gitignore` and [optional Git pre-commit hook](../../.githooks/pre-commit) are defense in depth, not a guarantee against forced additions, identifiers embedded in free text/images or unexamined history. Scan Git history/secrets independently; review CI logs and artifact retention; seek incident response for actual exposures.
- [Issue #8](https://github.com/pskeffington/pauls_notes/issues/8) tracks required branch protections, privacy review and Git history/secret scanning. An apparently green CI job alone does **not** close that governance gate.

Before sharing even an aggregate result derived from real cancer data, obtain source-specific access permission, protocol/scientific acceptance and independent disclosure/privacy review, including appropriate data-use attribution. No current teaching model claims a real-data or clinical release.
