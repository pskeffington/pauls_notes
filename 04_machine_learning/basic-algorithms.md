# A reader's guide to basic algorithms

[What is machine learning?](what-is-machine-learning.md) · [Methods and deployments](methods-and-deployments.md) · [Package guide](package-guide.md)

An algorithm is a procedure for fitting or applying a rule. The same research task can often be approached by several algorithms. Start with the measurement scale, target and evaluation design; then choose a procedure whose assumptions and computational cost fit the study.

## Supervised methods

| Method | Plain-language mechanism | Useful question | Important limitation | Executable example here |
| --- | --- | --- | --- | --- |
| Linear regression | Estimates a weighted sum of predictors | What numerical measurement should we predict? | A linear relationship and suitable error analysis need assessment | Related foundational examples in [models](../03_learning/models-and-uncertainty.md) |
| Logistic regression | Maps a weighted predictor score to a binary-event probability | How can measured features estimate a recorded binary outcome? | Predictor/outcome timing and calibration still matter | [Python classification](examples/sklearn_methods.py) |
| Ridge, lasso and elastic net | Penalize coefficient size; lasso/elastic net can shrink some coefficients to zero | How can correlated predictors be constrained? | Penalty selection belongs inside development; selected variables can be unstable | Ridge in [Python](examples/sklearn_methods.py); elastic net in [caret](caret-deployment.md) |
| k-nearest neighbors | Uses nearby training observations under a distance rule | Do similar measured profiles have similar targets? | Scale, distance and high dimensionality strongly affect neighbors | Reference only |
| Decision tree | Repeatedly splits observations using feature thresholds | Can a sequence of rules predict the target? | Deep trees can be unstable and overfit | Trees are components of the forest/boosting examples |
| Random forest | Combines many randomized trees | Can nonlinear combinations improve a baseline? | Many trees do not cure leakage or miscalibration | [Caret](caret-deployment.md) and [Python](examples/sklearn_methods.py) |
| Gradient boosting | Adds learners sequentially to reduce the remaining loss | Can a controlled sequence of small trees capture more structure? | Learning rate, complexity and stopping must stay inside development | [Python histogram boosting](examples/sklearn_methods.py) |
| Support-vector machine | Learns a separating margin, optionally in a kernel-derived feature space | Can a nonlinear boundary separate a defined category? | Scaling and tuning are important; a margin is not a calibrated probability | Reference only |
| Neural network | Learns successive weighted transformations | Can a representation capture structured images, sequences or measurements? | Data demands, tuning and evaluation complexity can be substantial | [Paper mechanisms](recent-code-studies.md); no local neural deployment |

## Exploration and time-to-event methods

**PCA** finds directions capturing variation in the supplied features. It is a projection, not a clustering algorithm or proof that its largest component is biologically meaningful. Scale features deliberately; fit the transform on development data when it feeds an assessed prediction pipeline. The [Python example](examples/sklearn_methods.py) exports a two-dimensional projection.

**K-means** assigns observations to a prespecified number of centers under its distance objective. Results depend on scaling, initialization, the number of groups and the geometry of the data. The example fixes three clusters before assessment. Silhouette describes separation under that geometry; it does not verify a cancer subtype.

**Cox proportional-hazards regression** models relative event hazard over follow-up, allowing right-censored observations. It is a statistical survival method, not a binary classifier. A larger fitted score represents higher relative hazard under the model; it is not automatically a recurrence probability at a chosen horizon. The [direct R example](examples/research_methods.R) checks event coding and exports a proportional-hazards diagnostic.

**Limma moderated linear models** estimate expression associations and stabilize variance estimation across features. This is inferential analysis, rather than an algorithm for demonstrating held-out predictive performance. The same [R example](examples/research_methods.R) estimates a batch-adjusted contrast with multiple-testing adjustment. Selecting genes from this whole-cohort analysis and then testing a classifier on those same people would mix discovery and assessment.

## Read the result in the right language

Classification asks about recorded labels or probabilities. Regression asks about numerical errors in stated units. Survival asks about event timing with censoring. Unsupervised analysis asks about structure under a representation. Differential-expression analysis asks about a specified contrast and its uncertainty. A useful algorithm comparison keeps the question, eligible observations and assessment design fixed.

Primary references: [linear models](https://scikit-learn.org/stable/modules/linear_model.html), [trees and ensembles](https://scikit-learn.org/stable/modules/ensemble.html), [neighbors](https://scikit-learn.org/stable/modules/neighbors.html), [support-vector machines](https://scikit-learn.org/stable/modules/svm.html), [decomposition](https://scikit-learn.org/stable/modules/decomposition.html), [clustering](https://scikit-learn.org/stable/modules/clustering.html), [survival documentation](https://cran.r-project.org/package=survival), and [limma documentation](https://bioconductor.org/packages/limma/).
