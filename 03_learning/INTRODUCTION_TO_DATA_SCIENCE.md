# Introduction to Data Science for Cancer Researchers

Authored by Paul Skeffington · Compiled with OpenAI

[Paul's Notes](../README.md) · [Learning subjects](README.md) · [Reader navigation](../docs/NAVIGATION.md) · [Research workflow](../docs/research-workflow.md)

## Purpose and reader

This evolving applied book introduces data science as a way to answer research questions with data. It is written for researchers who want to move from a scientific question to a defensible, reproducible analysis. Breast cancer examples provide the recurring setting because the repository already contains lessons, statistical exercises, synthetic studies, and machine-learning examples in that domain. The concepts are meant to transfer to other cancer types and research settings when the study design and data are specified for that setting.

The book follows one connected research story: a researcher asks a breast-cancer question, defines what evidence would answer it, determines what each record represents, prepares and explores data, chooses an analysis, checks what the result can support, and communicates the work. The examples distinguish published evidence from invented teaching data. Synthetic examples demonstrate methods and software behavior; they are never presented as patient findings, TCGA results, or clinical evidence.

This is a chapter route through material that is currently distributed across Paul's Notes. A link in the chapter map means there is relevant material to study; it does not mean a complete, integrated chapter or all its exercises have been written or accepted. Chapters marked **bridge to write** identify where the book still needs original connecting prose or exercises.

## How the chapters work together

Data science is iterative. A research question and study design shape what data must be collected and what one row means. The researcher imports and checks those records, tidies and transforms them, then uses visualization and modeling to understand them. Those two activities inform each other: a model can prompt a new plot, and a plot can reveal a data problem or a question the model missed. Results then return to the scientific question for interpretation and communication. Reproducible workflow and ethical stewardship support every stage.

The path moves from research purpose to data representation, exploration, inference, prediction, and communication. Readers can pause at a chapter to use a guide independently, but the sequence below supplies the missing through-line and shows why each technique appears when it does.

## Reader outcomes

By the end of the full sequence, a researcher should be able to:

- translate a research problem into a question, target population, observation unit, outcome, and analysis plan;
- inspect, document, join, reshape, and summarize research records without losing their meaning;
- choose visual and statistical methods that match the data, sampling design, and question;
- distinguish description, statistical inference, explanation, and prediction;
- develop and evaluate a predictive model without leaking information across evaluation boundaries;
- explain uncertainty, assumptions, missingness, limitations, and data provenance;
- produce a reproducible analysis record that another researcher can inspect and rerun.

## Chapter sequence

| Part | Chapter | Researcher's question | Existing material to read and use | Integration status |
| --- | --- | --- | --- | --- |
| I. Begin with the research problem | 1. What does data science contribute to cancer research? | What can data answer, and what must come from study design or domain knowledge? | [Cancer-wide research scope](../docs/cancer-research-scope.md); [breast cancer research narrative](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) | **Bridge to write:** connect the research question, evidence, and data-science cycle in one opening chapter. |
| I. Begin with the research problem | 2. Design the study before analyzing the data | Who or what is studied, what is measured, and what comparison answers the question? | [Study designs and published examples](study-designs-and-published-examples.md); [researcher analysis checklist](researcher-analysis-checklist.md); [cancer study design](bio_stats/CANCER_STUDY_DESIGN.md); [protocol template](../templates/study-protocol.md) | **Mapped:** strong design material exists; breast-cancer narrative transitions need integration. |
| II. Make records usable | 3. Build a reliable research workspace | How do files, commands, scripts, and version control make an analysis repeatable? | [Unix and Bash](../01_unix_bash/README.md); [Git and GitHub from zero](git-github-from-zero-to-push.md); [run and package](run-and-package.md) | **Mapped:** tutorials exist; a researcher-focused chapter bridge is needed. |
| II. Make records usable | 4. Give every row and variable a meaning | Is a row a person, tumor, specimen, visit, image, or measurement? | [Objects, types, and meaning](objects-and-meaning.md); [data dictionary template](../templates/data-dictionary.md) | **Mapped:** core lesson exists; add a breast-cancer data dictionary walkthrough. |
| II. Make records usable | 5. Join, reshape, and check the data | How can records be combined while preserving the study's units and denominators? | [Keys and reshaping](keys-and-reshaping.md); [missingness and comparisons](missingness-and-comparisons.md) | **Mapped:** lessons exist; connect them to the running research question and data-quality decisions. |
| III. Understand the data | 6. Summarize distributions and patterns | What do the measurements look like before a formal model is chosen? | [Breast-cancer distributions and power](bio_stats/BREAST_CANCER_DISTRIBUTIONS_AND_POWER.md); [statistics foundations](bio_stats/BREAST_CANCER_STATISTICS_FOUNDATIONS.md) | **Mapped:** substantial exercises exist; orient them as exploratory work before inference. |
| III. Understand the data | 7. Visualize evidence and inspect assumptions | Which display reveals variation, pairing, missingness, or a model problem? | [Figures and feature matrices](figures-and-features.md); [graph-method alignment](bio_stats/GRAPH_METHODS_ALIGNMENT.md); [visualization resources](../06_RESOURCES/README.md) | **Mapped:** plotting guides exist; add a continuous visual thread through the breast-cancer example. |
| IV. Explain and estimate | 8. Reason from samples to populations | How do sampling, probability, and uncertainty limit what the observed data say? | [Probability and study design](probability-and-design.md); [distribution and power module](bio_stats/BREAST_CANCER_DISTRIBUTIONS_AND_POWER.md) | **Mapped:** core calculations exist; build a chapter transition from design to uncertainty. |
| IV. Explain and estimate | 9. Choose and interpret a statistical analysis | Which method answers this question under this design, and what does its estimate mean? | [Data-type-first statistics guide](biomedical-statistics-decision-guide.md); [biomedical decision matrix](bio_stats/BIOMEDICAL_DECISION_MATRIX_V2.md); [worked test atlas](bio_stats/BREAST_CANCER_WORKED_TEST_ATLAS.md) | **Mapped:** extensive material exists; sequence from simple summaries to comparisons and model-based inference. |
| IV. Explain and estimate | 10. Model relationships and quantify uncertainty | How do we describe associations without overstating them? | [Models and uncertainty](models-and-uncertainty.md); [study design and analysis checklist](researcher-analysis-checklist.md) | **Bridge to write:** unite assumptions, diagnostics, effect estimates, intervals, and interpretation in the running example. |
| V. Predict carefully | 11. Learn from data with machine learning | Can a model predict an outcome for people not used to develop it, and how well do we know? | [What is machine learning?](../04_machine_learning/what-is-machine-learning.md); [visual data flow](../04_machine_learning/visual-data-guide.md); [model comparison](../04_machine_learning/model-comparison.md); [tuning](../04_machine_learning/model-tuning.md) | **Mapped:** detailed synthetic workflows exist; tie them to the earlier research-design chapters and contrast prediction with inference. |
| VI. Deliver research others can inspect | 12. Communicate, reproduce, and critique the analysis | What should another researcher need to understand, verify, and reuse the work? | [Research workflow](../docs/research-workflow.md); [analysis record template](../templates/analysis-record.md); [run and package](run-and-package.md); [mastery checks](mastery-checks.md) | **Bridge to write:** bring provenance, limitations, figures, reporting, and reproducibility together as the book's close. |
| VI. Deliver research others can inspect | Capstone. From a breast-cancer question to a reproducible result | Can the complete chain be followed without changing the question midway? | [Complete synthetic breast-cancer study](../02_biomedical_coding/examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd); [learning roadmap](../docs/learning-roadmap.md); [analysis record](../templates/analysis-record.md) | **In progress:** materials exist; their full chapter sequence and end-to-end acceptance remain separate work. |

## The recurring research example

Each chapter revisits the same broad setting: a researcher wants to understand a clearly defined breast-cancer outcome using measurements collected under a stated design. The exact question, target population, outcome, observation unit, and data source must be declared before analysis. Those details cannot be borrowed from another chapter or silently changed to make an example fit a method.

At every stage, ask:

1. **Question:** Is the goal description, estimation, explanation, or prediction?
2. **Design:** What is the target population, sampling unit, observation unit, outcome, and time frame?
3. **Data:** What does each record mean, how are records linked, and why are values missing?
4. **Method:** Which calculation or model addresses the question under the design's assumptions?
5. **Evidence:** What was actually executed, checked, and independently reviewed?
6. **Interpretation:** Which conclusions are supported, and which remain outside the evidence?

The repository's synthetic breast-cancer examples are useful for learning these steps because their data provenance and expected behavior can be controlled. They do not estimate real-world cancer risk, treatment response, prognosis, or clinical utility. Published studies may be used as evidence examples only with their population, design, analysis, and limitations kept visible.

## Suggested study rhythm

For each chapter, read the research question first, then inspect the relevant data structure and assumptions before running code. Predict a result or failure condition, execute the documented example when its requirements are available, compare the observed output with the expected behavior, and write a brief interpretation in plain language. Change one assumption at a time. Record data provenance, software, methods, outputs, and limitations in the [analysis record](../templates/analysis-record.md).

A listed example is not automatically verified. Use the repository's current [acceptance ledger](../02_biomedical_coding/BIOSTAT_8E_VERIFICATION_ACCEPTANCE_LEDGER.md) and each guide's stated evidence to distinguish a planned check, a source-level check, an executed test, and scientific or clinical review.

## How to continue

- Follow this sequence from [Paul's Notes](../README.md) for a guided introduction.
- Use [learning subjects](README.md) to jump directly to a method or runnable exercise.
- Use the [breast-cancer learning roadmap](../docs/learning-roadmap.md) for the current advanced synthetic research/ML capstone sequence.
- Use the [computational oncology textbook](../oncology/README.md) for a separate, developing cancer biology and computational oncology manuscript.
- Use [research scope and workflow](../docs/cancer-research-scope.md) when designing work beyond the current breast-cancer teaching examples.
