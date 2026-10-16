# Maintaining Paul's Notes

[Home](README.md)

Keep material organized by subject. Tie machine-learning additions to the breast cancer book's people, specimens, measurements, research question, and interpretation. Preserve the distinction between generic teaching fixtures and analyses of real breast cancer data. Introduce the research question, define unfamiliar terms, explain the method's assumptions, and connect the example to an interpretation. Distinguish executed examples, reference patterns, and proposed work. Mark synthetic data and unverified findings clearly.

Use descriptive `snake_case` names for R and Python functions. Validate schemas, identifiers, types, and missingness before analysis. Keep source files free of work on import where practical. Use explicit seeds for stochastic examples, preserve independent units during resampling, and fit preprocessing within the training partition.

Write generated results to a new directory outside the repository. Record software versions, input provenance, partition membership, and the commands needed to reproduce an analysis. Keep participant data and credentials out of source and shared outputs. Inspect embedded values before sharing interactive figures.

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
