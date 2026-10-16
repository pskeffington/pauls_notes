# What is machine learning?

[Machine learning subjects](README.md) · [Basic algorithms](basic-algorithms.md) · [Breast cancer application](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)

Machine learning uses observations to estimate a rule or representation. A researcher supplies the question, measurements, learning procedure and evaluation design. The computer adjusts parameters to reduce a specified error or organize patterns. It does not decide whether the observations represent the population, whether the labels are meaningful, or whether the result helps patients.

In the [breast cancer book](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data), imagine measuring several molecular features in tissue specimens. We might ask the computer to estimate a recorded tissue category from those measurements. We provide examples containing both measurements and known categories, fit a rule on some people, and assess its predictions on different people. The important test is whether the rule works on the observations we intended to predict, rather than whether it can describe the examples it already saw.

Follow the rows and fitting steps in the [visual data guide](visual-data-guide.md), then return here for the vocabulary.

## Learn the vocabulary through that example

| Term | Meaning in the tissue example |
| --- | --- |
| Observation | A specimen measurement linked to a person; several rows may come from the same person |
| Feature or predictor | An input available when prediction would actually occur, such as a defined expression measurement |
| Target or outcome | The recorded quantity/category to estimate; its source and time must be defined |
| Model | The fitted relationship used to generate estimates |
| Parameter | A quantity learned during fitting, such as a regression coefficient |
| Hyperparameter | A setting chosen around fitting, such as tree depth or penalty strength |
| Loss | The numerical error the procedure attempts to reduce |
| Training | Fitting the relationship and any learned transformations |
| Prediction | Applying the already fitted procedure to another observation |
| Generalization | Performance on the new people, sites or time period relevant to the question |

## Different questions create different learning tasks

**Supervised learning** uses known targets. Classification estimates categories or category probabilities; regression estimates a numerical outcome. A missing target is not automatically a negative outcome. Time-to-event data also contain follow-up and censoring, which require methods that retain that information.

**Unsupervised learning** examines measurements without a target. PCA compresses variation into a few directions; clustering groups observations under a chosen similarity rule. These can reveal technical batches or tissue composition as readily as biological structure. A separated cluster is a finding to investigate, not a newly validated disease class.

**Representation learning** learns a useful encoding, sometimes from large collections before a specific downstream task. **Generative models** learn distributions from which they can produce outputs. Pretraining does not remove the need to check data overlap, appropriate inputs, downstream evaluation and model limitations. The current executable examples focus on classical supervised and unsupervised methods; the [recent-paper guide](recent-code-studies.md) introduces foundation-model mechanisms separately.

## Fitting well is different from predicting well

A complicated rule can memorize accidental detail. This is **overfitting**: performance looks strong on the fitting observations but weakens on new ones. A rule that is too restrictive can miss relevant structure, sometimes called underfitting. More model complexity and more rows are not automatic solutions; the amount of independent information, measurement quality and design matter.

Reserve assessment people before learning preprocessing or selecting features. Inside development data, use resampling to compare settings. When the settings themselves are tuned, an outer evaluation loop can assess the tuned procedure. Relatives, repeated visits, specimens and image patches need grouping appropriate to their dependence. Future prediction needs a time-respecting evaluation rather than random mixing of future and past records.

## Ask what a score means

A classifier can rank cases well while giving poorly calibrated probabilities. Accuracy depends on the decision threshold and outcome frequency; a majority-class guess can appear accurate in an imbalanced sample. For numerical predictions, errors need units and a simple baseline. For survival, evaluation must account for censoring. For clusters, a geometric score is not biological confirmation.

A useful report states the target, observation unit, predictor availability, partition design, comparison baseline, metric definition, uncertainty and limitations. An association or feature importance does not establish causation. A model predicting a historical label does not by itself establish clinical benefit.

## Continue the breast cancer narrative

After tracing the [data slices](visual-data-guide.md), ask which expression measurements should remain in the predictor. The [advanced training guide](advanced-breast-cancer-training.md) shows how to rank and select columns inside training, keep paired specimens together, and distinguish a useful predictor from a biological explanation. Its synthetic paired-specimen deployment is separate from the book's gene evidence.

## Put the ideas into practice

Begin with the [algorithm guide](basic-algorithms.md), choose a [research task](methods-and-deployments.md), and run a small synthetic example. Inspect the split record before the performance score. Explain which observations the model could see and which evidence would be needed before applying the workflow to a real study.

Primary references: [scikit-learn supervised learning](https://scikit-learn.org/stable/supervised_learning.html), [unsupervised learning](https://scikit-learn.org/stable/unsupervised_learning.html), [nested evaluation](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html), and [prediction-model reporting](https://www.tripod-statement.org/).
