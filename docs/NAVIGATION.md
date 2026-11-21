# Navigate Paul's Notes

[Repository home](../README.md) · [Learning subjects](../03_learning/README.md) · [Research resources](../06_RESOURCES/README.md) · [Machine index](machine-index.md)

Choose the **question or deliverable first**, then open the canonical home for that work. This page is a short reader-facing router; the underlying machine-readable routing data lives in [navigation-routes.json](navigation-routes.json). Section-level search and citations remain owned by the [machine index](machine-index.md). Avoid maintaining separate, conflicting lists of every research note.

## First destination by task

**For a guided introduction:** [Introduction to Data Science for Cancer Researchers](../03_learning/INTRODUCTION_TO_DATA_SCIENCE.md) lays out the reader sequence from a breast-cancer research question to reproducible communication. It links to existing lessons and marks integration chapters that remain to be written.

| Your objective | Start here | Then do |
| --- | --- | --- |
| Learn data science through a research narrative | [Introduction to Data Science for Cancer Researchers](../03_learning/INTRODUCTION_TO_DATA_SCIENCE.md) | Follow the ordered chapter map; use each linked lesson and its evidence status |
| Frame a cancer research question | [Research scope](cancer-research-scope.md) | [Study workflow and permissions](research-workflow.md) |
| Define a study and estimand | [Research workflow](research-workflow.md) | [Biomedical implementation gates](../02_biomedical_coding/IMPLEMENTATION_GATES.md) |
| Choose breast cancer data and define endpoints | [Clinical data and dataset suitability](../oncology/chapters/CO-02-clinical-oncology-data.md) | [Cancer study design](../03_learning/bio_stats/CANCER_STUDY_DESIGN.md) and [protocol worksheet](../templates/study-protocol.md) |
| Define record units and combine tables | [Data dictionary and join exercise](../oncology/chapters/CO-04-data-literacy.md) | [Dictionary worksheet](../templates/data-dictionary.md) and [executable observation-grain lab](../oncology/examples/observation_grain.py) |
| Interpret probability and diagnostic evidence | [Probability and Bayes](../oncology/chapters/CO-07-randomness-and-probability.md) | [Python and R probability labs](../oncology/examples/README.md) and [categorical reporting](../03_learning/bio_stats/CATEGORICAL_RISK_ROC_REPORTING.md) |
| Choose a defensible statistical test | [Decision matrix](../03_learning/bio_stats/BIOMEDICAL_DECISION_MATRIX_V2.md) | [Statistics learning atlas](../03_learning/bio_stats/README.md) |
| Learn R or research computing | [Learning subjects](../03_learning/README.md) | [Reusable R tools](../06_RESOURCES/R/README.md) |
| Select a figure | [Graph method guide](../03_learning/bio_stats/GRAPH_METHODS_ALIGNMENT.md) | [Synthetic graph gallery](../03_learning/bio_stats/GRAPH_METHODS_SYNTHETIC_GALLERY.Rmd) |
| Write and check biomedical analysis code | [Biomedical coding](../02_biomedical_coding/README.md) | [Canonical R Markdown example](../02_biomedical_coding/BIOMEDICAL_R_CANONICAL_EXAMPLE.md) |
| Report findings in scientific form | [Statistical reporting and notation](../03_learning/bio_stats/SCIENTIFIC_STATISTICAL_REPORTING_STANDARDS.md) | [Categorical, risk and ROC reporting](../03_learning/bio_stats/CATEGORICAL_RISK_ROC_REPORTING.md) and [presentation acceptance](../02_biomedical_coding/RMARKDOWN_PDF_PRESENTATION_ACCEPTANCE.md) |
| Read the developing computational oncology textbook | [Textbook home](../oncology/README.md) | [Chapter roadmap](../oncology/ROADMAP.md) |
| Explore genomics sources | [Genomics resources](../06_RESOURCES/Genomics/README.md) | [Cancer-wide research scope](cancer-research-scope.md) |
| Build and evaluate ML | [Machine learning](../04_machine_learning/README.md) | [Evidence and acceptance limits](roadmap-gates.md) |
| Learn Unix, Git, or Rust | [Unix/Bash](../01_unix_bash/README.md) · [Git tutorial](../03_learning/git-github-from-zero-to-push.md) · [Rust foundations](../03_learning/rust/README.md) | Choose the matching examples and tests |
| Determine what has actually passed | [Biomedical acceptance ledger](../02_biomedical_coding/BIOSTAT_8E_VERIFICATION_ACCEPTANCE_LEDGER.md) | [Dated R validation summary](../03_learning/bio_stats/R_VALIDATION_STATUS.md) |

## Breast cancer investigator pathway

Use this sequence to plan or review an investigation. Each step produces information needed by the next; experienced readers can enter at the unresolved decision.

| Step | Decision and practical output | Canonical reading |
| --- | --- | --- |
| 1. Frame the question | State whether the purpose is description, diagnosis, prognosis, treatment effect or prediction; name the intended population | [Opening worked chapter](../03_learning/INTRODUCTION_TO_DATA_SCIENCE.md#chapter-1--from-a-breast-cancer-question-to-an-interpretable-result) |
| 2. Match the data | Identify disease/assay definitions, person–specimen relationships and measurements actually available; distinguish diagnostic features, molecular data and follow-up | [Clinical data and source selection](../oncology/chapters/CO-02-clinical-oncology-data.md) |
| 3. Specify the study | Define eligibility, time zero, endpoint, estimand, independent unit and missing-outcome strategy in one protocol | [Study-design guide](../03_learning/bio_stats/CANCER_STUDY_DESIGN.md) · [Protocol worksheet](../templates/study-protocol.md) |
| 4. Prepare and analyze | Account for eligible, observed and analyzed participants; check join keys and denominators, then choose the primary method and diagnostic checks | [Worked dictionary and join](../oncology/chapters/CO-04-data-literacy.md) · [Keys and reshaping](../03_learning/keys-and-reshaping.md) · [Method decision matrix](../03_learning/bio_stats/BIOMEDICAL_DECISION_MATRIX_V2.md) |
| 5. Report the evidence | Connect group denominators, effect, uncertainty and clinical interpretation to the original question | [Scientific reporting](../03_learning/bio_stats/SCIENTIFIC_STATISTICAL_REPORTING_STANDARDS.md) · [Figure-method guide](../03_learning/bio_stats/GRAPH_METHODS_ALIGNMENT.md) |
| 6. Make the work reviewable | Preserve input provenance, execution commands, decisions and evidence for each completed check | [Analysis record](../templates/analysis-record.md) · [Verification ledger](../02_biomedical_coding/BIOSTAT_8E_VERIFICATION_ACCEPTANCE_LEDGER.md) |

The [narrative chapter route](../03_learning/INTRODUCTION_TO_DATA_SCIENCE.md) organizes learning; the [60-chapter oncology manifest](../oncology/book-manifest.json) records a separate manuscript's publication state. Use the manifest and each chapter's evidence record for current draft and verification status.

## Reader workflow

For a guided course, follow the chapter order in the [data science introduction](../03_learning/INTRODUCTION_TO_DATA_SCIENCE.md). Its breast-cancer examples build on one research question; specialist notes remain independently navigable.

**Question → method → example → check → interpretation.** Read the chosen guide's data assumptions and independent-unit definition before its example. Use the cited synthetic exercise, run the appropriate tests when available, and distinguish observed outcomes from proposed or merely committed checks. Navigate back to this page when the task changes rather than jumping between unrelated tutorials.

## Agent and machine workflow

**Task → route ID → canonical entrypoint → narrow source section → evidence gate.** Read [AGENTS.md](../AGENTS.md), use the [routing manifest](navigation-routes.json) to choose a home, then retrieve the smallest relevant section from the [machine index](machine-index.md). The `next` edges in the JSON are suggested transitions, not prerequisites. Preserve exact source scope and avoid interpreting the presence of code or CI jobs as evidence that they ran.

## Scientific boundaries

All synthetic biomedical and cancer examples are educational, not patient-derived clinical findings. The current statistical figure gallery and expanded workbook have not received confirmed end-to-end R/HTML acceptance in the cited [ledger](../02_biomedical_coding/BIOSTAT_8E_VERIFICATION_ACCEPTANCE_LEDGER.md). The ontology or route map does not itself certify code, statistical assumptions, publication readiness or any individual manuscript chapter.

## Navigation maintenance

Update the [route manifest](navigation-routes.json) when a canonical home changes, then update this reader page and short entrypoint links. Keep the full topic catalog in [machine-index.md](machine-index.md). Check the three layers with `python3 scripts/check_navigation_routes.py` and its tests; use `python3 scripts/check_documentation.py` for wider Markdown links and anchors. The [maintenance policy](DOCUMENTATION_MAINTENANCE.md) specifies evidence requirements.
