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

## Chapter 1 — From a breast cancer question to an interpretable result

**Opening bridge: authored draft.** This chapter introduces the reasoning that connects the later methods. Its numerical example is an original, deliberately small teaching construction; every participant, treatment label and outcome count is invented.

An investigator may receive a pathology table, a folder of expression files and a clinical follow-up extract on the same day. Each can be valuable, but none determines the scientific question by itself. A molecular measurement describes an assay performed on material collected at a particular time. A diagnosis describes a clinical classification. A treatment comparison describes an intervention and a population. The first analytical task is to establish how those observations bear on the question.

Breast cancer supplies a useful recurring setting because the investigator must connect biological measurements, specimen provenance, disease characterization, treatment timing and outcomes. The opening goal is modest and concrete: produce a research statement in which the population, measurement, comparison and meaning of the answer remain consistent from the first data table to the final paragraph.

### 1.1 Similar variables can answer different questions

Consider a tumor measurement called *marker score*. Its presence in a dataset does not establish what it is useful for. The intended question determines which observations and comparisons are required.

| Research purpose | Example question | Evidence that must be present |
| --- | --- | --- |
| Description | How are recorded marker scores distributed among eligible baseline specimens? | A defined sampling frame, assay units, specimen timing and observed/missing counts |
| Diagnosis | Does a baseline score distinguish a specified pathological diagnosis? | The intended diagnostic population, a documented reference diagnosis and a defined test procedure |
| Prognosis | Does a baseline score help estimate recurrence by a specified follow-up time? | A defined starting population, baseline measurement, event definition and follow-up information |
| Treatment effect | Does assignment to A rather than B change a specified response probability? | An interpretable treatment comparison, endpoint ascertainment and an analysis aligned with the assignment and follow-up design |
| Treatment-effect modification | Does the effect of A versus B differ by baseline marker status? | Treatment comparisons within marker-defined groups and an explicit interaction contrast |

The FDA–NIH BEST resource distinguishes [diagnostic biomarkers](https://www.ncbi.nlm.nih.gov/books/NBK402285/?report=reader) from [prognostic and predictive biomarkers](https://www.ncbi.nlm.nih.gov/books/NBK402284/?report=reader). In its terminology, a predictive biomarker concerns differential effects of an intervention. In machine learning, *prediction* may instead mean estimating any recorded outcome. The intended meaning therefore belongs in the research question.

A marker associated with response among people receiving A does not, by that observation alone, identify who benefits more from A than from B. That second question requires information about the treatment contrast. Likewise, distinguishing recorded benign and malignant diagnoses does not evaluate future recurrence. These distinctions determine the next data request, rather than merely changing the label attached to a model.

### 1.2 Define the target before choosing the estimator

A useful opening statement specifies whose outcome is of interest, what is measured, when it is measured, and which contrast will be estimated. The **target population** is the group to which the scientific question refers. The **analysis population** consists of records contributing to a particular calculation. Eligibility, missingness and exclusions explain why those populations may differ.

The **independent unit** is the entity whose dependence structure the analysis must respect. In an individually randomized study, assignment occurs at the participant level. Several specimens, images or assay wells from one participant do not create additional randomized participants. The [clinical data chapter](../oncology/chapters/CO-02-clinical-oncology-data.md) develops the associated person, specimen and assessment relationships.

The **estimand** is the quantity the study aims to estimate; an **estimator** is the procedure used to estimate it. For a trial, [ICH E9(R1), final guidance](https://www.fda.gov/media/148473/download) connects the population, treatment conditions, endpoint, handling of intercurrent events and population summary. Treatment discontinuation is an intercurrent event whose handling can change the question. A missing pathology report is a missing-data problem; it does not automatically define a clinical failure.

This distinction is practical. Writing “compare treatments with logistic regression” names a possible model, but leaves the intended effect unresolved. Writing “estimate the difference in response probability under assignment to A versus B in the eligible trial population” identifies an effect scale; the endpoint and intercurrent-event rules must then complete the definition. Chapter 2 and the [study-design guide](bio_stats/CANCER_STUDY_DESIGN.md) provide that fuller specification.

### 1.3 A synthetic study connects the records to the question

Consider a fictional, individually randomized breast cancer teaching study. Its simplified extract has 80 eligible participants assigned equally to hypothetical treatments A and B. The purpose is to understand a binary response comparison, not to recommend either treatment or a clinical schedule.

| Element | Definition in this teaching construction |
| --- | --- |
| Population | Adults with newly diagnosed, nonmetastatic invasive breast cancer meeting a declared study eligibility definition |
| Assignment and analysis unit | One participant; 40 assigned to A and 40 to B |
| Starting point | Randomization before study treatment; baseline assay measurements precede randomization |
| Response assessment | Pathology at the protocol-planned surgery; the timing and assessment rules belong in the study dictionary |
| Pathology definition | pCR defined as $ypT0/Tis\;ypN0$, using the breast and sampled regional-node assessment |
| Simplifying conditions | All 80 have surgery and an interpretable response assessment; no treatment switch, death, progression preventing surgery or omitted surgery is stipulated |
| Primary descriptive contrast | Response proportion under A minus response proportion under B |
| Research specimen records | Two research specimen collections per participant, giving 160 specimen rows linked to 80 participant IDs |

The pathology definition is one of the [FDA definitions for this trial setting](https://www.fda.gov/media/83507/download) and the preferred definition in [NeoSTEEP](https://pubmed.ncbi.nlm.nih.gov/37433103/): residual invasive disease is assessed in the resected breast and sampled regional lymph nodes; residual in situ disease in the breast is allowed by this definition. The specimen-row count is solely an invented research-table structure, not a specification of the pathology sampling required for pCR assessment.

This miniature case deliberately excludes intercurrent events so the first calculation can be checked directly. A complete trial protocol must specify their handling before those events occur. The specimen table can describe multiple collections while the response table still contains one adjudicated response per participant.

Suppose the invented response counts are:

| Assigned group | pCR | No pCR | Participants with known response | Missing response |
| --- | ---: | ---: | ---: | ---: |
| A | 18 | 22 | 40 | 0 |
| B | 12 | 28 | 40 | 0 |

Let $x_g$ denote the number with pCR and $n_g$ the number with known response in group $g$. The observed proportion is $\widehat p_g=x_g/n_g$. For this complete-outcome construction,

$$
\widehat p_A=\frac{18}{40}=0.45,\qquad
\widehat p_B=\frac{12}{40}=0.30,\qquad
\widehat\Delta=\widehat p_A-\widehat p_B=0.15.
$$

The descriptive statement is: **The invented response proportions were 45% (18/40) under A and 30% (12/40) under B; the observed difference was 15 percentage points.** “Percentage points” states an absolute difference. The contrast has not become a 15% relative increase simply because its numerical value is 0.15.

This calculation supplies the point estimate. An inferential analysis must additionally choose and report an interval method, account for the actual design and missingness, and explain the uncertainty. The [categorical and risk reporting chapter](bio_stats/CATEGORICAL_RISK_ROC_REPORTING.md) supplies that next step. No significance claim follows from the arithmetic presented here.

### 1.4 A changed denominator changes the answer

Now consider an information-limited version of the same teaching extract. Keep 18 known responses in A and 12 in B, but make four A outcomes and two B outcomes unavailable. There are then 36 known outcomes in A and 38 in B. An available-case calculation gives

$$
\frac{18}{36}=0.50,\qquad
\frac{12}{38}\approx0.3158,\qquad
0.50-\frac{12}{38}\approx0.1842.
$$

The resulting 18.42-percentage-point difference describes the participants with available outcomes. It cannot be silently substituted for the full randomized-population contrast. Keeping denominators at 40 while using the same positive counts instead treats every unavailable outcome as nonresponse. That is an additional assumption or a distinct, explicitly defined documented-response endpoint.

A direct arithmetic check makes the information gap visible. If none or all of the missing A outcomes were responses, A's full-group proportion could range from $18/40$ to $22/40$. B's corresponding range is $12/40$ to $14/40$. The possible full-group differences consistent with these incomplete counts are bounded by

$$
\frac{18}{40}-\frac{14}{40}=0.10
\quad\text{and}\quad
\frac{22}{40}-\frac{12}{40}=0.25.
$$

These are **bounds from possible assignments of missing binary outcomes**, not a 95% confidence interval. They describe what the incomplete table permits before sampling uncertainty is assessed. The exercise shows why an investigator must report missing counts and reasons alongside response counts; a model cannot supply the absent clinical facts merely by accepting an input table.

### 1.5 Preserve the question while preparing and modeling data

The participant roster, specimen table and response table serve different purposes. The roster defines assignment and eligibility. The specimen table records collection and assay provenance. The response table records the endpoint. Their joins must preserve those meanings. Counting 160 specimen rows as 160 independent participants would change the sample size without changing the number of people randomized.

The same logic governs predictor timing. A model intended for use at baseline may use measurements available at that point. A surgical pathology result collected later cannot be inserted as a baseline predictor simply because it appears in the same final export. The researcher should record both when a measurement was obtained and when its result became available for the proposed use.

The [keys and reshaping lesson](keys-and-reshaping.md) explains how to check record relationships. The [machine-learning data-flow guide](../04_machine_learning/visual-data-guide.md) extends the principle to development and evaluation: related specimens stay with their participant, and learned preprocessing remains inside the training procedure. These are consequences of the intended research use, not cosmetic software choices.

Model selection follows the clarified task. A description of a marker distribution requires appropriate summaries. An unadjusted binary response contrast requires counts and an effect estimate on the chosen scale. A baseline prediction task requires an evaluation design and performance assessment for future participants. The [method decision matrix](bio_stats/BIOMEDICAL_DECISION_MATRIX_V2.md) helps select among these paths once the study information is known.

### 1.6 Assemble a result that another investigator can inspect

The investigator's deliverable is a connected argument. The Methods explain where the observations came from and how they became the analysis population. The Results give denominators, estimates and uncertainty. The Discussion explains what the estimated quantity means for the original question and identifies the assumptions that materially limit that interpretation.

For the synthetic example, a reviewer should be able to trace 80 participant IDs through assignment, specimen linkage, response ascertainment and the final counts. If an exclusion changes 40 assigned participants into 36 analyzed participants, that transition must be visible. If a comparison changes from an absolute difference to an odds ratio, the resulting interpretation must change with it.

Use the [scientific reporting standards](bio_stats/SCIENTIFIC_STATISTICAL_REPORTING_STANDARDS.md) for the formal reporting sequence and notation. Use the [analysis record](../templates/analysis-record.md) to retain input provenance, transformations, software versions and execution evidence. The first chapter's arithmetic is intentionally small enough to check without a statistical package; later executable examples add uncertainty estimation and diagnostic evidence.

### 1.7 Exercises and answer reasoning

1. **Identify the question.** A score separates recorded malignant and benign samples. Which additional observations are needed to study five-year recurrence?

   **Reasoning:** a defined baseline population, time origin, recurrence ascertainment, follow-up and censoring information are needed. A diagnostic label alone supplies neither event time nor follow-up.

2. **Recover the unit.** The teaching extract contains 160 specimen rows from 80 randomized participants. What is the randomized sample size?

   **Reasoning:** 80 participants. The additional collections describe within-person observations; they do not add independently assigned individuals.

3. **Interpret the contrast.** Explain $18/40-12/40=0.15$ in one sentence.

   **Reasoning:** the observed response proportion under A exceeded that under B by 15 percentage points in the complete synthetic extract. A precision or significance statement requires further analysis.

4. **Audit missingness.** Four outcomes in A and two in B become unavailable. Why do $18/36-12/38$ and $18/40-12/40$ answer different immediate questions?

   **Reasoning:** the first describes available outcomes; the second counts missing outcomes as failures when interpreted as a full-group response proportion. The intended estimand and missing-data assumptions must justify the chosen procedure.

5. **Interpret the bounds.** Does the interval from 0.10 to 0.25 quantify sampling uncertainty?

   **Reasoning:** no. It enumerates the extremal full-group differences compatible with the supplied missing binary outcomes. Sampling uncertainty remains a separate question.

6. **Distinguish response from differential benefit.** A marker is associated with response among participants assigned A. What is missing from a claim that it identifies greater benefit from A than B?

   **Reasoning:** the corresponding treatment comparison by marker status is missing. An explicit interaction estimand is needed to assess how that comparison changes across marker groups.

Proceed to Chapter 2 by completing the [study-design worksheet](bio_stats/CANCER_STUDY_DESIGN.md#10-researcher-study-design-worksheet). Its purpose is to resolve eligibility, endpoint timing, intercurrent events, missingness and the primary contrast before a statistical method is selected.

## Chapter sequence

| Part | Chapter | Researcher's question | Existing material to read and use | Integration status |
| --- | --- | --- | --- | --- |
| I. Begin with the research problem | 1. What does data science contribute to cancer research? | What can data answer, and what must come from study design or domain knowledge? | [Opening research narrative](#chapter-1--from-a-breast-cancer-question-to-an-interpretable-result); [cancer-wide research scope](../docs/cancer-research-scope.md); [breast cancer research narrative](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) | **Opening bridge drafted:** question, estimand, synthetic response arithmetic, missingness and reasoned exercises; independent scientific review remains pending. |
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
