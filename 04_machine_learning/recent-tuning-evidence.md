# Recent tuning evidence for the breast cancer workflow

[Project tuning guide](model-tuning.md) · [Breast cancer evidence](breast-cancer-evidence.md) · [Structured register](evidence/breast-cancer-studies.csv) · [Book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)

Reviewed through **2026-10-16**. This selective update covers **2021–2025 publication years**, roughly the last five years, with nine new primary methodological papers. Together with the existing [Bischl et al., 2023 review](breast-cancer-evidence.md#bc-m10), it provides ten recent tuning sources. Foundational references remain in the main evidence guide. This is a targeted reading corpus, not an exhaustive or systematic review; it does not assert that no relevant 2026 work exists.

The organizing question is the book's own: **can assay measurements distinguish the recorded specimen category for people excluded from training?** Our current example uses invented paired specimens, not participant records or the book's named genes. General tabular benchmarks can suggest a search mechanism or an evaluation question; they cannot establish its performance on breast cancer assays, pathology, future risk or treatment response.

Continue with the [2021–2026 selection and validation evidence](recent-selection-validation.md) for nine additional papers on gene panels, validation precision, leakage and model-family comparisons. Together the two reading sets contain nineteen recent sources, including the existing Bischl review.

## Read by the decision you need to make

| Project decision | Recent evidence | What to carry into our work |
| --- | --- | --- |
| Make comparisons replayable | [HPOBench](#bc-m11), [TabRepo](#bc-m17) | Preserve data/split identity, environment, predictions and trial history |
| Spend a limited training budget | [DEHB](#bc-m12), [PriorBand](#bc-m15) | Define the training resource and test whether cheap trials preserve useful rankings |
| Search a complex model space | [SMAC3](#bc-m14), [Bischl review](breast-cancer-evidence.md#bc-m10) | Declare conditional settings, objective and budget before searching |
| Balance prediction and assay burden | [YAHPO Gym](#bc-m13) | Separate prediction error, runtime and panel burden; assess the selected tradeoff |
| Require a credible starting point | [Better by default](#bc-m16) | Compare tuning against a fixed, independently chosen baseline |
| Decide whether additional search helped | [Overtuning](#bc-m18), [TabArena](#bc-m19) | Assess the entire selection procedure beyond the validation scores that selected it |

Publication year identifies the paper, not the current software release. The [corpus review](corpus-review.md) now records selected full-text review for these papers, plus a pinned SMAC3 example inspection. Individual review scopes and remaining reproduction limits are in the [paper ledger](evidence/paper-review.csv). No external optimizer benchmark was executed. Review of an implementation is distinct from installing it or reproducing its publication.

## BC-M11

**HPOBench: reproducible multi-fidelity benchmarks — Eggensperger et al., 2021.** [Primary source](https://arxiv.org/abs/2109.06716v3)

**Reported evidence:** The authors package heterogeneous optimization problems behind a shared interface and isolated containers, including tabular and surrogate variants. The source identifies the NeurIPS 2021 publication; this card uses author manuscript version 3, revised in 2022.

**Review extent:** Selected full-text methods/results and limitations; not an exhaustive supplementary-material audit. See the [dated paper-review ledger](evidence/paper-review.csv) for the source, sections, findings and remaining limits. No study training was reproduced.

**Breast cancer application:** Our comparison unit must be an entire assay pipeline on a fixed set of development people. Save input identity, person partitions, dependency versions and candidate traces together. The runner already exports these ingredients; a container would be an additional packaging choice, not proof that missing-value handling or person separation is correct. Reusing a benchmark interface does not make unrelated cancer cohorts interchangeable.

**Artifact pointer:** [Author software](https://github.com/automl/HPOBench); not installed or source-reviewed.

## BC-M12

**DEHB: differential evolution with Hyperband — Awad et al., 2021.** [Primary source](https://www.ijcai.org/proceedings/2021/296)

**Reported evidence:** DEHB combines population-based configuration search with Hyperband resource allocation. Its empirical optimizer comparisons concern benchmark tasks, rather than breast cancer assays.

**Review extent:** Selected full-text methods/results and limitations; not an exhaustive supplementary-material audit. See the [dated paper-review ledger](evidence/paper-review.csv) for the source, sections, findings and remaining limits. No study training was reproduced.

**Breast cancer application:** For a future expensive pathology learner, define a resource such as training epochs before considering early elimination. For our small logistic grid, selecting fewer arbitrary specimen rows would alter paired structure and class composition; it is not an acceptable shortcut. Check cheap-versus-full-budget rankings within development and include interrupted trials in the budget. DEHB is a reference extension, not an executed optimizer here.

**Artifact pointer:** [Author software](https://github.com/automl/DEHB); not installed or source-reviewed.

## BC-M13

**YAHPO Gym: multiple objectives and resource levels — Pfisterer et al., 2022.** [Primary source](https://proceedings.mlr.press/v188/pfisterer22a.html)

**Reported evidence:** The paper supplies surrogate-based optimization problems with multiple objectives and fidelities. Its comparison also shows that tabular and surrogate benchmark representations can produce different optimizer rankings.

**Review extent:** Selected full-text methods/results and limitations; not an exhaustive supplementary-material audit. See the [dated paper-review ledger](evidence/paper-review.csv) for the source, sections, findings and remaining limits. No study training was reproduced.

**Breast cancer application:** Panel size, assay cost, runtime and prediction error are different quantities. Our current k values count arbitrary columns; they do not measure the cost of a real assay panel. A proposed smaller breast cancer panel needs a declared cost model and a selection rule applied within development. If examining a Pareto frontier, choose and assess the final tradeoff without consulting final-test people. A simulated benchmark ranking cannot settle that choice.

**Artifact pointer:** [Author software](https://github.com/slds-lmu/yahpo_gym); not installed or source-reviewed.

## BC-M14

**SMAC3: model-based configuration search — Lindauer et al., 2022.** [Primary source](https://www.jmlr.org/papers/v23/21-0888.html)

**Reported evidence:** SMAC3 presents Bayesian optimization software with interfaces for hyperparameter optimization, algorithm configuration and related optimization settings.

**Review extent:** Selected full-text methods/results and limitations; not an exhaustive supplementary-material audit. See the [dated paper-review ledger](evidence/paper-review.csv) for the source, sections, findings and remaining limits. No study training was reproduced.

**Breast cancer application:** A future comparison across logistic, forest and boosting families needs conditional settings: a tree-depth option does not belong to logistic regression. Record each family’s space, preprocessing and budget, and keep family selection inside the assessed procedure. Use the same person boundaries and primary objective across candidates. Our six-point k/C grid remains the implemented procedure; naming SMAC3 does not establish a working deployment.

**Artifact inspection:** [Pinned quadratic example](https://github.com/automl/SMAC3/blob/841488796a82944b7c753c62eec3dfb74f72585e/examples/1_basics/1_quadratic_function.py) read; current API rather than the frozen paper release. Not installed or executed.

## BC-M15

**PriorBand: expert knowledge with cheap evaluations — Mallik et al., 2023.** [Primary source](https://papers.nips.cc/paper_files/paper/2023/hash/1704fe7aaff33a54802b83a016050ab8-Abstract-Conference.html)

**Reported evidence:** PriorBand combines expert-supplied configuration priors with multi-fidelity optimization. The abstract reports gains from informative priors and benchmark robustness when supplied priors are poor.

**Review extent:** Selected full-text methods/results and limitations; not an exhaustive supplementary-material audit. See the [dated paper-review ledger](evidence/paper-review.csv) for the source, sections, findings and remaining limits. No study training was reproduced.

**Breast cancer application:** Expert knowledge could motivate plausible regularization ranges or architecture settings, but it must be available before inspecting the reserved test. Gene biology does not itself identify an optimal C or learning rate. Compare a prespecified prior-guided search with an equally budgeted search without that prior on development people. Avoid promoting weak candidates solely because a prior favors them; inspect full-budget assessment. This remains a proposed comparison.

**Artifact pointer:** [Author software](https://github.com/automl/mf-prior-exp); not installed or source-reviewed.

## BC-M16

**Better by default: strong baselines before large searches — Holzmüller et al., 2024.** [Primary source](https://proceedings.neurips.cc/paper_files/paper/2024/hash/2ee1c87245956e3eaa71aaba5f5753eb-Abstract-Conference.html)

**Reported evidence:** The work derives defaults using meta-training datasets and assesses them on separate meta-test datasets, including RealMLP and tree models. The selected methods describe repeated random train/validation/test splits and classification error or one-versus-rest AUROC, and normalized regression RMSE. Numeric missingness is excluded from the benchmark data, including removal of affected rows.

**Review extent:** Selected full-text methods/results and limitations; not an exhaustive supplementary-material audit. See the [dated paper-review ledger](evidence/paper-review.csv) for the source, sections, findings and remaining limits. No study training was reproduced.

**Breast cancer application:** Prespecify a fixed baseline before asking whether our feature/regularization search earns its 76 fits. Do not transfer the benchmark’s random-row split or missing-value exclusions into paired assays: our example needs person grouping and training-only imputation, and selects by Brier error. General benchmark defaults are candidates for evaluation, not clinically established assay settings. The current runner has a prevalence baseline; an all-feature model with fixed C is a future comparator, not an existing result.

**Artifact pointer:** [Author software](https://github.com/dholzmueller/pytabkit); not installed or source-reviewed.

## BC-M17

**TabRepo: preserve predictions to examine model choices — Salinas and Erickson, 2024.** [Primary source](https://proceedings.mlr.press/v256/salinas24a.html)

**Reported evidence:** TabRepo collects model predictions and evaluation metrics, enabling retrospective comparisons of optimization and ensemble choices without refitting every stored model.

**Review extent:** Selected full-text methods/results and limitations; not an exhaustive supplementary-material audit. See the [dated paper-review ledger](evidence/paper-review.csv) for the source, sections, findings and remaining limits. No study training was reproduced.

**Breast cancer application:** Retain outer-held-out specimen predictions alongside person IDs, fold labels, targets and the training protocol. These records make disagreements and subgroup errors inspectable. Selecting ensemble weights from those same predictions is another training step and needs its own assessment boundary; a cached prediction file does not make repeated adaptive comparisons independent. The present runner exports outer predictions but does not execute an ensemble. Pin a release before following the evolving software pointer.

**Artifact pointer:** [Author software](https://github.com/autogluon/tabrepo); not installed or source-reviewed.

## BC-M18

**Overtuning: searching can overfit the selection criterion — Schneider et al., 2025.** [Primary source](https://proceedings.mlr.press/v293/schneider25a.html)

**Reported evidence:** The authors reanalyze optimization benchmark data and distinguish improved validation scores from improved generalization. They report overtuning that is often mild but can be severe, with particular concern for small datasets.

**Review extent:** Selected full-text methods/results and limitations; not an exhaustive supplementary-material audit. See the [dated paper-review ledger](evidence/paper-review.csv) for the source, sections, findings and remaining limits. No study training was reproduced.

**Breast cancer application:** Our 45 development people, rather than the number of specimen rows or search trials, constrain the evidence. Do not enlarge k/C ranges just because the best inner Brier score continues falling. Compare fixed budgets as complete development procedures, retain every candidate’s score, and use people excluded from each search to assess them. The paper’s reported benchmark frequency is not an estimated overtuning rate for breast cancer patients. The protected final test cannot be recycled to select a budget.

## BC-M19

**TabArena: assess budgets, validation and ensembles together — Erickson et al., 2025.** [Primary source](https://proceedings.neurips.cc/paper_files/paper/2025/hash/1697e3fb412da11dc9488249f9e7bbc9-Abstract-Datasets_and_Benchmarks_Track.html)

**Reported evidence:** TabArena introduces a living tabular benchmark examining methods under standardized evaluation. Its abstract highlights the effects of training budgets, ensembling and validation overfitting on conclusions about model families.

**Review extent:** Selected full-text methods/results and limitations; not an exhaustive supplementary-material audit. See the [dated paper-review ledger](evidence/paper-review.csv) for the source, sections, findings and remaining limits. No study training was reproduced.

**Breast cancer application:** An assay-model comparison must state whether it compares equal numbers of candidates, equal fitting time or another resource; these answer different questions. Include preprocessing and ensemble selection in the procedure being assessed. A large-budget neural model should not be described as inherently superior to our small logistic search from unrelated benchmark results. Record hardware, workers, elapsed time and failures in any future budget comparison; the current runner reports fit counts, not a measured cross-family timing experiment.

**Artifact pointer:** [Author software](https://github.com/autogluon/tabarena); not installed or source-reviewed.

## Turn the reading into a study-specific comparison

For the next assay-method experiment, write the comparison before looking at performance:

1. State the prediction target and the unit held out: previously unseen people, with both specimens kept together.
2. Declare the fixed comparator, selected features, primary loss, search space, fit/time budget and refit rule. Count model-family, panel-size and ensemble choices as selection.
3. Keep imputation, selection and scaling inside every training partition. Use inner folds for choices and outer excluded people for assessment of each complete procedure.
4. Save trial parameters, resource levels, failures, elapsed time and held-out predictions. Keep endpoint, cohort and assay definitions attached to every result.
5. Choose the final procedure using development evidence, then freeze it for the reserved test. A later redesign needs an evaluation plan that acknowledges the information already used.

These steps are our proposed application of the reading. This update adds evidence and interpretation; it does not implement adaptive search, empirical timing comparisons, stronger baselines or clinical validation. The executable starting point remains the [paired-specimen runner](examples/breast_cancer_feature_selection.py), its [candidate-trace contract](model-tuning.md#read-every-candidate-not-just-the-winner), and the [advanced training guide](advanced-breast-cancer-training.md).

## How this corpus was assembled

The update used targeted searches and primary proceedings, journal and author-manuscript pages for hyperparameter optimization, multi-fidelity search, reproducible benchmarks, defaults, overtuning and tabular model evaluation. Selection favored a distinct mechanism or evaluation issue that could be connected to our assay workflow. Searches were checked through 2026-10-16; this is not a registered search protocol, complete database export or quality-ranked evidence synthesis.

The ten recent sources are methodological publications, including one existing review. They are not ten independent patient cohorts. TabRepo and TabArena have overlapping authors and software lineage; other sources share benchmark ecosystems. Publication counts must not be read as independent replications. Before adopting a method, review the full relevant methods, pin its code/data release, assess compatibility with the study design, and reproduce its behavior under our own split and feature contract.

[Return to Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)
