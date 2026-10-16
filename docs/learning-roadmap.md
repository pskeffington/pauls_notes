# Learning roadmap: breast cancer data, models and evidence

Authored by Paul Skeffington · Compiled with OpenAI

[Paul’s Notes](../README.md) · [Computing subjects](../03_learning/README.md) · [Machine learning](../04_machine_learning/README.md) · [Breast cancer book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)

Updated **2026-10-16**, following the [corpus review and validation run](../04_machine_learning/corpus-review.md). This is a progression through research competencies and repository development, organized by subject and evidence of understanding. Move forward when you can explain and demonstrate the completion check; there is no weekly schedule.

The shared narrative is **people → specimens → measurements → data preparation → training → validation → prediction → biological interpretation**. The present executable assay example predicts a recorded specimen category for previously unseen people. Every later method must retain that question or explicitly define a new endpoint. The [milestone gate ledger](roadmap-gates.md) records repository implementation, execution evidence, scientific limits and dependencies separately from learner mastery.

## Starting position

| Available now | What that readiness establishes |
| --- | --- |
| Unix/Bash guides and seven biomedical computing subject guides | Runnable practice in files, records, joins, missingness, models, figures and packaging |
| ML introduction, algorithms, visual data-flow guide and breast cancer narrative | A connected reading route from data meaning to prediction |
| R caret, direct R and Python examples | Independently executable teaching mechanisms with stated input and partition contracts |
| Rust frozen-model prediction | Compiled CLI with preserved preprocessing, typed inputs and cross-language parity; native Rust fitting remains an extension |
| Five-year Rust ML review | [11 publications/manuscripts and six pinned software inspections](../04_machine_learning/rust-ml-literature.md), with explicit project decisions; external studies remain unreplicated |
| Paired-specimen selection with candidate traces | Training-only selection, grouped nested assessment and saved prediction replay on invented data |
| 36-paper register and dated review | Traceable sources and limitations; three records remain abstract-limited |
| Recorded validation | The earlier 14-test run remains archived; the [comparison guide](../04_machine_learning/model-comparison.md) adds a third Python deployment; the [gallery validation](../04_machine_learning/evidence/gallery-validation-2026-10-16.json) records 25 tests across five suites |
| Conditional person-level uncertainty | [Phase 4C](../04_machine_learning/uncertainty-assessment.md) adds paired person resampling, 36 conditional ranges, independent numeric references and exact replay; full-procedure coverage is not established |

These are repository capabilities. Your understanding has not been assessed by CI. The 60-gene book remains a teaching catalog, and the synthetic features are not those genes. The [ML gallery](../04_machine_learning/gallery/README.md) has seven generated figures covering allocation, missingness, tuning, feature variation, errors and calibration, with saved numeric inputs and interpretation prompts. [Phase 4B replication](../04_machine_learning/replication-experiment.md) and [Phase 4C conditional uncertainty](../04_machine_learning/uncertainty-assessment.md) are implemented and replayed; neither establishes clinical or full-training-procedure uncertainty.

## Next phases

| Phase | Learner question | Repository work | Completion evidence | Status |
| --- | --- | --- | --- | --- |
| 1. Data meaning and training boundaries | What exactly does each row and prediction represent? | Use the existing guides and outputs | Annotated data dictionary, hand-traced split and explanation of one deliberate input failure | Ready for practice |
| 2. Fair baseline comparisons | How does the tuned subset procedure compare with a fixed all-feature model? | Inspect the implemented fixed all-feature comparator under the same assessment plan | Matched outer predictions and documented comparison; no gain is required to pass | Implemented; ready for practice |
| 3. Visual interpretation | Can I see where data went and why predictions differ? | Build a reproducible ML plotting gallery | Labeled figures rebuilt from saved outputs, with denominators and interpretation prompts | Implemented; seven figures ready for practice |
| 4. Stability and tuning budgets | Which choices survive changes in development people or search budget? | [Replication](../04_machine_learning/replication-experiment.md) and [conditional person-level uncertainty](../04_machine_learning/uncertainty-assessment.md) | Complete histories, repeated-cohort results, panel/rank/sign summaries, 36 conditional ranges and verified replay | Defined synthetic milestone complete through G1/G2; learner mastery and full-procedure uncertainty remain unestablished |
| 5. New endpoints and R methods | What changes when the question becomes recurrence or treatment response? | Introduce a separate survival learning case and compare R/Python contracts | Correct time/event schema, censoring-aware assessment and a declared Cox baseline | Planned; requires a new endpoint contract |
| 6. Paper-to-code capstone | Can I reproduce a precisely defined research result and explain its limits? | Reproduce a bounded published component, then package a complete teaching analysis | Pinned artifact, explicit result target, reproduction record and independent replay | Planned after the relevant method checks |

## Phase 1: explain the current data before changing the model

Read [objects and meaning](../03_learning/objects-and-meaning.md), [keys and reshaping](../03_learning/keys-and-reshaping.md), [missingness](../03_learning/missingness-and-comparisons.md), [what ML does](../04_machine_learning/what-is-machine-learning.md), and the [visual data-flow guide](../04_machine_learning/visual-data-guide.md). Use the existing [mastery checks](../03_learning/mastery-checks.md) to practice failures as well as successful outputs.

For the paired-specimen example, explain 60 people, 120 specimens and 48 measurements; 45 development and 15 reserved-test people; and why both specimens from a person remain together. Trace one outer fold and its inner folds using the exported row coordinates. Identify where imputation medians, selected columns, scales and coefficients are learned.

**Finish with:** a filled [data dictionary](../templates/data-dictionary.md), an annotated split sketch, and a short explanation of why a duplicate identity or broken pair must fail. Explain why specimen category, future diagnosis and recurrence are different targets. These explanations are learner work; a passing script alone does not complete the phase.

## Phase 2: compare the declared training procedures

The [review](../04_machine_learning/corpus-review.md#executed-project-validation) identifies the immediate gap: the original selection runner had a prevalence baseline but no fixed all-feature comparator. The [comparison case](../04_machine_learning/model-comparison.md) now implements that comparator under its own declared protocol. The contrast includes regularization tuning and does not isolate a feature-selection-only effect. Read the [tuning contract](../04_machine_learning/model-tuning.md#our-concrete-tuning-contract) and [strong-default evidence](../04_machine_learning/recent-tuning-evidence.md#bc-m16) before expanding the search.

Build the comparator with the same imputation/scaling boundary, an independently declared regularization setting, the same person partitions and the same primary probability loss. Keep the tuned selection procedure and fixed comparator distinct. Retain every held-out prediction, candidate trace and fit count. If model-family selection is added, include that choice inside the procedure being assessed.

**Finish with:** a protocol written before the comparison run, paired prediction records, and an explanation of the observed error difference and its limits. A smaller panel or higher score is not a completion requirement. The existing teaching test has already been inspected; disclose that history and use a newly declared assessment plan for a redesigned experiment. An independently planned synthetic run still supplies software evidence, not a clinical validation cohort.

## Phase 3: build the plotting gallery from real run outputs

Use [figures and feature matrices](../03_learning/figures-and-features.md), [models and uncertainty](../03_learning/models-and-uncertainty.md), and the [candidate-trace fields](../04_machine_learning/model-tuning.md#read-every-candidate-not-just-the-winner) as the starting material. The [gallery](../04_machine_learning/gallery/README.md) now implements all the following views from saved run outputs, including [declared conditional calibration ranges](../04_machine_learning/gallery/plotting-contract.md). The inclusion counts describe the existing three outer fits; they do not complete Phase 4's robustness experiment.

| Available display | What the learner should explain |
| --- | --- |
| Person/specimen allocation and missingness | Observation unit, eligibility and why specimen totals differ from person totals |
| Candidate Brier errors by inner fold | Metric direction, the selection rule and why the winning inner score is not an independent test |
| Held-out predictions and probability-error comparison | Which people were excluded from fitting and what the baseline comparison measures |
| Selected features across outer fits | Changing column identity, correlated substitutes and why frequency is not gene-discovery significance |
| Coefficients and held-out permutation diagnostics | Different meanings of importance; row-wise permutation’s paired-data limitation |
| Calibration display with counts and stated uncertainty limits | Probability agreement versus ranking; sparse bins and dependence restrict conclusions |

**Finish with:** regenerable SVG/PDF figures and a gallery index linking the inputs, plotting command, units, denominator and interpretation question. Figures must reflect saved results. Do not choose models or panels from diagnostic assessment plots and then reuse those results as fresh validation.

## Phase 4: study robustness before making search more elaborate

Read the [overtuning evidence](../04_machine_learning/recent-tuning-evidence.md#bc-m18), [panel-stability evidence](../04_machine_learning/recent-selection-validation.md#bc-m21), and [budget accounting](../04_machine_learning/model-tuning.md#count-the-fitting-budget). The [prespecified Phase 4 protocol](../04_machine_learning/robustness-protocol.md) now varies development people, missingness, and correlated measurements without touching reserved-test fitting boundaries. Run the [software gate](../04_machine_learning/robustness-experiment.md) before designing an independent replication.

[PR #1](https://github.com/pskeffington/pauls_notes/pull/1) merged the bounded baseline as `06cdc2c9de2e42de4852ce07dd8d4d52ae26216c`. The [G0 record](roadmap-gates.md#g0-phase-4-software-baseline) retains the 624-fit/360-prediction replay and merge-CI evidence. [Phase 4B's unchanged protocol](../04_machine_learning/replication-protocol.md) fixed three new cohort seeds before its [12-cell assessment](../04_machine_learning/replication-experiment.md). [G2's separately frozen protocol](../04_machine_learning/uncertainty-protocol.md) now adds 36 conditional person-bootstrap ranges on those saved predictions, known numeric fixtures, complete resampling records and exact CI replay. G1/G2 close the defined synthetic Phase 4 milestone; no complete-training-procedure or clinical coverage claim follows.

Record which settings were fixed, which were searched, failed trials, elapsed time, worker limits and complete candidate histories. Describe stability on repeated, overlapping development samples as descriptive evidence. Keep assessment-based importance out of subsequent feature selection unless that adaptation receives its own assessment boundary.

Once the baseline is credible, compare one search extension against the current grid under a declared resource budget. Fixed-budget random search is a candidate first experiment; Bayesian or multi-fidelity search needs a cost or resource justification. Six transparent candidates may remain sufficient for this small teaching space.

The [Rust review's implementation route](../04_machine_learning/rust-ml-literature.md#a-bounded-route-from-reading-to-implementation) adds a separate candidate: a native Linfa logistic baseline. Declare its loss, penalty, intercept, probability direction and convergence behavior before fitting the same grouped training partitions. Retain the current comparators and distinguish a new training procedure from a change of inference runtime. If runtime is studied, first establish equivalent calculations and record hardware, precision, workload, startup and end-to-end measurements. This experiment remains planned and does not complete the broader stability work.

**Finish with:** reproducible [robustness](../04_machine_learning/replication-experiment.md) and [conditional uncertainty](../04_machine_learning/uncertainty-assessment.md) reports that retain unfavorable runs and explain whether the extra search earned its cost. Do not set a minimum AUC or require a preferred optimizer to win. Explain the equal-person contrast estimand and why paired resampling preserves specimens within a person but omits dependence from shared training fits. Fold spread is not a substitute; full-procedure uncertainty requires a new experiment.

## Phase 5: change the endpoint deliberately

Use the book’s [research question](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#chapter-11-working-through-a-research-question), [R survival and expression examples](../04_machine_learning/methods-and-deployments.md#r-survival-and-expression-analysis), and [recent survival evidence](../04_machine_learning/recent-selection-validation.md#bc-m28).

The next distinct case should define a time origin, follow-up time, event indicator, prediction horizon and eligible population. Begin with a declared Cox comparator and assess discrimination and probability prediction separately. Unobserved future outcomes cannot simply be coded as negative. Any censoring model, calibration update or feature selection must have a stated fitting and assessment boundary.

For R expansion, assess an mlr3 survival pipeline against the existing direct-R route before adding another framework. Restore and test the chosen environment first. The current caret example assumes independent people and rejects duplicate person IDs; paired-specimen admission requires a new contract. R/Python comparisons need compatible inputs, endpoints, splits and loss definitions, not merely similarly named models or identical expected scores.

**Finish with:** a separate synthetic survival fixture, an endpoint-specific protocol, a baseline comparison, saved predictions and an explanation of censoring assumptions. Treatment-response work follows its own regimen and prediction-time definitions; neither prognosis nor response under observed care demonstrates which treatment would benefit an individual more.

## Phase 6: reproduce a bounded result and deliver the capstone

Resolve the relevant [review-ledger limitations](../04_machine_learning/evidence/paper-review.csv) before choosing a target. A useful first route is a small, declared component of the pinned 2026 survival benchmark. Its processed-output audit is already done; actual refitting is additional work requiring the paper-era environment, dataset provenance and explicit result-selection rules. Alternatively, select another accessible paper whose exact inputs and execution route can be reviewed.

Write down the target table or metric, dataset subset, source commit, environment, expected tolerance, resource budget and failure policy before execution. Verify access and reuse conditions for the chosen data. Distinguish a reduced-component reproduction from a whole-paper reproduction. Keep the two MASAI reports linked to one trial and check TransNEO overlap when interpreting response studies.

**Finish with:** a complete breast cancer teaching analysis that another learner can run in a clean environment. Include its question, data dictionary, analysis plan, figures, comparison results, limitations, source/version inventory and an independent replay. Update reproduction status only for the exact component whose execution and result contract have been checked. The capstone should explain what it learned from the data and what evidence is still missing.

## Work order and completion record

**Phase 4's defined synthetic scientific-software milestone is complete through G1/G2. Next engineering priority: freeze G3's native Rust logistic objective and numerical comparison contract. Next new-method priority: design G4's separate survival endpoint and protocol; its G1/G2 dependency is satisfied.** See [G0–G5](roadmap-gates.md) for exact status. Phase 1 can be practiced now with existing material. The [Rust inference path](../04_machine_learning/rust-deployment.md) remains separately tested; native Rust fitting does not block survival progression. Learner mastery, full-procedure uncertainty and clinical validity remain unestablished. Adding literature alone does not complete the remaining implementations.

For each phase, record the question, code/document change, executed command, observed result, learner explanation and remaining limitation in the [analysis record](../templates/analysis-record.md). A failed hypothesis or unchanged predictive performance can be a valid learning result. Mark repository delivery and personal understanding separately.

Continue using the [validation command](../04_machine_learning/corpus-review.md#repeat-the-run) for regression checks as executable methods change. It verifies software behavior and recorded outputs; the learner’s reasoning and the scientific claim still need review.
