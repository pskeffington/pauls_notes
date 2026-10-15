# Models and uncertainty

[Learning sections](README.md) · [Next: figures](figures-and-features.md)

## A formula specifies required fields

The deployed exploratory model uses baseline marker measurements and age. Its formula is `marker_au ~ age_years`, so eligibility requires finite values for those two fields at baseline. Seven people meet that condition. The model does not use the repeated followup values as additional independent people.

```r
source("03_learning/examples/research_case.R")
result <- analyse_case(make_case())
stopifnot(nobs(result$model) == 7L)
stopifnot("S02" %in% result$model_data$person_id)
coef(result$model)
confint(result$model)
```

The age coefficient has units of invented marker units per year. It describes the fitted conditional linear association in these chosen values. The intercept is the line's expected marker value at age zero, which is outside this fixture's age range and has no useful biomedical interpretation here.

The code uses `na.action = na.fail` after declaring eligibility, so an unexpected later omission is a failure rather than a silent reduction in the analytic sample.

## Mean confidence and individual prediction

A confidence interval for the mean response describes uncertainty in the fitted mean under the model. A prediction interval for a new individual response adds individual-level variation under that model and is wider at the same predictor value when residual variation is positive.

```r
mean_width <- result$confidence$upr - result$confidence$lwr
individual_width <- result$prediction$upr - result$prediction$lwr
stopifnot(all(individual_width > mean_width))
```

Neither interval describes causal certainty. In this case the inputs were deliberately chosen, so the intervals demonstrate software and model mechanics; they do not imply random-sample evidence about people.

## Inspect assumptions and alternatives

The exported PDF includes the raw age–marker relationship, residuals against fitted values, and a normal-quantile plot. Curvature, unequal spread and influential observations can undermine a simple model. Small samples limit diagnostic sensitivity. A visually tidy residual plot does not establish independence or absence of confounding.

Keep selection rules, effect scale and candidate predictors fixed by the question. Repeated measurements need a design that accounts for dependence; survey data need the sampling design; nonlinear outcomes may require different distributions or links. Model-based adjustments do not repair an unmeasured confounder automatically.

## Prediction is a separate evaluation task

This demonstration does not train or evaluate a predictive system. For such a system, split data by the appropriate independent unit before learning preprocessing, imputation, feature selection or tuning. Repeated measurements from one person should not cross training and evaluation boundaries. Assess calibration and discrimination on appropriate held-out data; apparent training fit is insufficient.

## Transfer exercise

Remove an unrelated questionnaire field and confirm that the model count stays seven. Then set one observed baseline marker to missing and confirm that the model count changes. Explain why those operations have different implications for eligibility.

References: [Linear model fitting](https://search.r-project.org/R/refmans/stats/html/lm.html), [linear model predictions](https://search.r-project.org/R/refmans/stats/html/predict.lm.html), [model diagnostics](https://search.r-project.org/R/refmans/stats/html/plot.lm.html).
