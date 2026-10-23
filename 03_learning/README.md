# Biomedical computing by subject

Authored by Paul Skeffington · Compiled with OpenAI

[Paul's Notes](../README.md) · [Research workflow](../docs/research-workflow.md)

Choose the subject that matches your research question. Each guide explains a practical task, gives a runnable example, names the expected result, and asks you to change one assumption. Read any subject on its own, use the related-topic links for context, or combine the methods in the complete analysis example.

Use the [current breast-cancer learning roadmap](../docs/learning-roadmap.md) for one complete worked example, or the [cancer-wide research scope](../docs/cancer-research-scope.md) to design a separate study with a different tumor site, modality or outcome.

## Browse subjects

| Research task | Subject guide | Practical result |
| --- | --- | --- |
| Classify biomedical data and choose an introductory statistical method | [Data-type-first biomedical statistics guide](biomedical-statistics-decision-guide.md) | Quantitative vs qualitative, paired and clustered design; visual test-choice flowchart, executable synthetic R example and method caveats |
| Work from a research question to an analysis plan | [Narrative researcher checklist](researcher-analysis-checklist.md) | Twelve reasoning steps, a reusable decision paragraph, and four worked narratives |
| Recognize study types in published research | [Study designs and published examples](study-designs-and-published-examples.md) | Nine source-linked readings: sampling, timing, allocation, actual analysis, and limits on interpretation |
| Practice choosing a valid test, then verify it in R | [Biomedical statistics workbook](statistics-practice-workbook.md) | Eight data-type and twelve method-choice cases, full answer key and independent numerical/negative-case lab checks |
| Learn Git and GitHub command-line basics | [Git/GitHub from zero to push](git-github-from-zero-to-push.md) | Install, authenticate, clone or initialize, branch, commit, push and open a pull request |
| Learn Rust from first principles to object-oriented research code | [Rust foundations and engineering course](rust/README.md) | Variables, collections, ownership, structs, traits, Cargo and a tested synthetic paired-specimen lab |
| Represent a specimen or participant correctly | [Objects, types and meaning](objects-and-meaning.md) | Typed records, aligned matrices and checked functions |
| Combine and reorganize observations | [Keys, joins and reshaping](keys-and-reshaping.md) | Row-preserving linkage and wide/long reconstruction |
| Account for unavailable observations | [Missingness and comparisons](missingness-and-comparisons.md) | Explicit denominators and a six-pair comparison |
| Explain a fitted relationship | [Models and uncertainty](models-and-uncertainty.md) | Baseline model, diagnostic plots and two interval types |
| Make a figure match its measurements | [Figures and feature matrices](figures-and-features.md) | Paired lines, distributions and row-scaled feature displays |
| Investigate assumptions using simulation | [Probability and study design](probability-and-design.md) | Reproducible probability experiments and survey-design distinctions |
| Execute and package a complete analysis | [Run and package](run-and-package.md) | A Bash-to-R deployment with 15 output files |

## Run the combined example

Requirements: Bash and R with its standard packages. The main case uses no downloaded data or additional R packages. Optional examples explicitly name their additional packages.

From the repository root, choose a new directory whose parent already exists:

```bash
bash 03_learning/examples/run_case.sh /tmp/biomedical-learning-run
```

The invented fixture has eight people, sixteen person-visits, fourteen observed measurements, six complete pairs and seven people in the baseline model. The complete-pair mean change is **1.5 invented arbitrary units**. These constants are arithmetic teaching expectations, not research findings.

## Explore the combined example

1. Predict the counts before running the case.
2. Open `observation_counts.csv`, `complete_pairs.csv` and `diagnostics.pdf`.
3. Explain why the model and paired comparison use different sets of people.
4. Add a duplicate registry record in an in-memory copy and confirm that the analysis rejects it.
5. Change an observation to missing, compute the new expected denominator, and compare it with the result.
6. Write an interpretation that names the measurement scale, comparison, observation unit and one limitation.

The fixture, typed CSV import, analysis and export are in [research_case.R](examples/research_case.R). It can be sourced without running the deployment. The [contract tests](tests/test_research_case.R) check known results, malformed inputs, matrix orientation, intervals and output behavior.

## Check the work

Use the [learning checks](mastery-checks.md) for executable competencies, expected results, deliberate failures, and learner explanations. Additional practice tools cover label cleaning, response codes, checked plotting, input batches and reporting minimums.

```bash
python3 scripts/check_documentation.py
Rscript --vanilla 03_learning/tests/test_research_case.R
```

Generated analysis outputs belong in a chosen working directory. Commit reusable source and documentation; do not commit local runs, participant records or credentials. For molecular context, read the [breast cancer book](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md). For predictive modeling, see the [caret deployment and package guide](../04_machine_learning/README.md).

## Principles covered

| Foundation | Where to inspect or practice |
| --- | --- |
| Assignment, sequences, named vectors, vectorization, recycling and coercion | Objects, types and meaning |
| Missing values, nonfinite numbers, safe subsetting, categories and dates | Objects; missingness and comparisons |
| Matrices, lists, dimension labels, CSV and RDS | Objects; figures; deployed case |
| Scalar decisions, checked functions, loops and apply functions | Objects and deployed helper functions |
| Filtering, derived columns, grouped summaries, keys and joins | Keys and reshaping; measurement summaries |
| Wide/long layouts and complete pairs | Keys; missingness and comparisons |
| Random generators, probability functions and sampling assumptions | Probability and study design |
| Rank-based and parametric comparison assumptions | Missingness and comparisons |
| Regression, eligibility, coefficient units and diagnostic checks | Models and uncertainty |
| Mean confidence and individual prediction intervals | Models and deployed interval tables |
| Distribution displays, paired plots and feature scaling | Figures and feature matrices |
| Complex sampling weights, clusters and strata | Probability and optional survey example |
| Files, quoting, text inspection, exit codes and shell-to-R arguments | Run and package; Unix and Bash |
| Output staging, integrity inventories, session records and reruns | Run and package; deployed case |
