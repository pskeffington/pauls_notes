# Biomedical research workflow

[Paul's Notes](../README.md) · [Resource guide](resource-guide.md)

## 1. Define the question before choosing software

Write the population or experimental model, exposure or intervention, comparator, outcome, observation unit and time horizon. Distinguish descriptive, causal, prognostic and predictive aims. Define the quantity to estimate and what evidence would change the interpretation. Record the plan in the [study protocol](../templates/study-protocol.md).

## 2. Specify input and access contracts

Record the dataset accession, release, retrieval date, file checksums, permitted use and storage location. Keep credentials, participant keys and restricted records outside this repository. Work with synthetic examples here. Separate participant, specimen, sample, assay and file identifiers; a file count is not a participant count.

Use the [data dictionary](../templates/data-dictionary.md) to specify types, units, permitted categories, missing-value conventions and identifier relationships. Check duplicate keys, join cardinality, unmatched rows and the number of observation units before and after each join. Preserve raw inputs; write transformations to a separate location.

## 3. Capture the environment and processing decisions

Record operating system, language and package versions, configuration, random seeds and the exact command needed to rerun. Pin dependencies for the study rather than relying on a moving software release. Start with [Unix/Bash workflow practice](../01_unix_bash/reproducible-workflow.md) and the [implementation gates](../02_biomedical_coding/IMPLEMENTATION_GATES.md).

## 4. Inspect measurements and study structure

Summarize missingness, impossible values, batch, repeated measurements and selection rules. For expression analysis, establish assay type and measurement scale before selecting a model. Preserve donor and specimen structure; normalization does not remove every source of bias. The [measurement guide](../06_RESOURCES/Genomics/GENE_EXPRESSION_INTERPRETATION.md) and [breast cancer book](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) connect these checks to molecular interpretation.

## 5. Match analysis and validation to the question

For statistical inference, state the contrast, effect scale, uncertainty method, confounders, multiplicity family and sensitivity analyses. For prediction, separate evaluation data at the participant or other appropriate grouping level before fitting preprocessing, imputation, feature selection or tuning. Assess calibration and clinically relevant operating points alongside discrimination; record subgroup uncertainty and limits to transportability.

Select software using the [literature matrix](../02_biomedical_coding/BIOMEDICAL_CODING_LITERATURE_MATRIX.md) and the linked version-specific manuals. Reporting checklists, software tests and evidence appraisal answer different questions; passing one does not establish the others.

## 6. Check code against explicit expectations

Use small synthetic fixtures with known results, malformed-input checks and justified numerical tolerances. Check that outputs preserve identifiers, units and denominators. Record which checks ran, the environment, results and skipped checks in the [analysis record](../templates/analysis-record.md). A successful rerun demonstrates computational behavior under those conditions; it does not establish the scientific conclusion.

## 7. Explain and package the result

Every table and figure should identify the observation unit, sample counts, measurement scale, contrast and uncertainty. Distinguish exploratory findings from prespecified analyses and report exclusions and limitations. Keep the scripts, configuration, dependency records and output inventory together. Share only outputs permitted by the data's access and disclosure rules.

## Documentation to consult

- [Bash language reference](https://www.gnu.org/software/bash/manual/): command expansion, quoting and process status.
- [DESeq2 analysis vignette](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html): count-based RNA analysis, design formulas and contrasts.
- [Methods documentation register](../02_biomedical_coding/OFFICIAL_METHODS_REGISTER.md): further version and applicability checks.
