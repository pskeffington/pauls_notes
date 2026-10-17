# Maintaining Paul's Notes

[Home](README.md)

Keep material organized by subject across **any cancer type**. Start each new oncology example with its own cancer context, biological question, observation unit, data source, endpoint, access status, methods and interpretation. **The existing breast cancer book and TCGA-BRCA plan are current worked cases, not requirements for every new method or tumor type.** Link additions to the book when they actually extend that case; for another cancer or modality, link a separately reviewed study protocol and evidence corpus. Preserve the distinction between generic synthetic teaching fixtures and analyses of real participant data. Distinguish executed examples, reference patterns, and proposed work. Mark synthetic data and unverified claims clearly. See the [repository-wide scope and case-specific rules](docs/cancer-research-scope.md).

Use descriptive `snake_case` names for R and Python functions. Validate schemas, identifiers, types, and missingness before analysis. Keep source files free of work on import where practical. Use explicit seeds for stochastic examples, preserve independent units during resampling, and fit preprocessing within the training partition.

If new to Rust, work through the [seven-stage foundations-to-engineering route](03_learning/rust/README.md) and pass its pinned Cargo tests before adding new modules. Its example has no patient data and does not change G3's frozen training protocol.

For G4 time-to-event work, keep the [frozen synthetic survival protocol](04_machine_learning/survival-protocol.md) and its [data dictionary](04_machine_learning/survival-data-dictionary.md) immutable during the first execution; any new endpoint, seed, censor model, horizon or time origin is a **new exploratory protocol version**, not a silent fix to obtain favorable output. G4 survival is not the prior specimen-label task and no real cancer participant data are admitted.

For a new synthetic ML teaching experiment, reuse the [parameterized oncology lab](04_machine_learning/research_toolkit/README.md) with only its reviewed JSON numeric settings. Verify grouping, inner candidates, selected features and report denominators; avoid linking actual patient records or suggesting clinical validity. New cancer cohorts, sites, imaging and endpoints require a distinct study protocol and source-specific data review.

For a roadmap milestone update, edit the [human gate ledger](docs/roadmap-gates.md) **and** [machine evidence snapshot](docs/milestone-evidence.toml) together; preserve the exact PR/head/merge SHA, CI run, evidence files, scientific boundary and next unfulfilled prerequisite. Run `python3 scripts/check_milestone_evidence.py` and `python3 -m unittest discover -s scripts/tests -p test_milestone_evidence.py -v`. Do not mark a draft feature complete or claim learner mastery/clinical validation because CI passed.

For Rust code, use the [book-aligned engineering handbook and review checklist](02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md): preserve the frozen native-training contract, pinned toolchain/dependencies, safe-Rust boundary and independent numerical validation. New Rust feature claims require their own execution and review evidence.

Apply access and privacy restrictions **regardless of cancer site or provider**; neither a GDC open flag nor a public download automatically approves participant-level publication or fitting. New data-source adapters require their own provider-specific access review; do not broaden the TCGA-BRCA preflight by removing its project checks. Write generated results to a new directory outside the repository. Record software versions, input provenance, partition membership, and the commands needed to reproduce an analysis. Keep participant data and credentials out of source and shared outputs. Inspect embedded values before sharing interactive figures.

Run commands below from the repository root. Python checks use the standard library except for the machine learning suite, which requires the pinned packages in [its requirements file](04_machine_learning/requirements-python.txt). R dependencies and example execution commands are documented in the [learning guide](03_learning/README.md) and [machine learning guide](04_machine_learning/README.md).

| Area | Check |
| --- | --- |
| Navigation and referenced scripts | `python3 scripts/check_documentation.py` |
| Python and Bash syntax | `python3 scripts/check_repository.py` |
| Navigation regression tests | `python3 scripts/tests/test_documentation.py` |
| Book structure and examples | `python3 scripts/check_book_learning.py` and `python3 03_learning/tests/test_book_learning.py` |
| Breast cancer ML evidence integrity | `python3 scripts/check_ml_evidence.py` and `python3 scripts/tests/test_ml_evidence.py` |
| Literature register integrity | `python3 02_biomedical_coding/tests/test_literature_matrix.py` |
| Shell examples | `bash 01_unix_bash/tests/test_summarize_metadata.sh` and `bash 06_RESOURCES/tests/test_bash_helpers.sh` |
| Manuscript builder contract | `bash 06_RESOURCES/tests/test_manuscript_builder.sh` |
| Python machine learning | `python3 04_machine_learning/tests/test_sklearn_methods.py` and `python3 04_machine_learning/tests/test_breast_cancer_feature_selection.py` |
| R resources | `for test_file in 06_RESOURCES/tests/test_*.R; do Rscript --vanilla "$test_file" || exit; done` |

The manuscript contract test uses stub tools to check arguments, failed builds, and output protection. A real PDF build needs the TeX distribution and Biber listed in the [manuscript guide](06_RESOURCES/LaTeX/README.md); inspect its rendered pages separately.

Review the relevant [GitHub Actions workflows](.github/workflows) before publishing a change. A passing suite checks the documented software behavior and selected scientific safeguards; interpretation, citation accuracy, visual quality, and suitability for a specific study still require review. Add regression tests when fixing a substantive behavior defect. Update links and examples alongside renamed source files.
