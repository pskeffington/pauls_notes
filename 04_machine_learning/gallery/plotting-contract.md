# Figure inputs and uncertainty contract

[Gallery](README.md) · [Training protocol](../comparison-protocol.md)

Declared on 2026-10-16 before executing the additional gallery displays. This supplement changes presentation only: the version 1 cohort, split, training procedures, six candidates and 80-fit budget remain fixed.

## Saved inputs and observation units

The renderer reads `report.json`, `predictions.csv` and `display-inputs.json`. The last file exports raw missingness masks, specimen identities and feature summaries from the existing run. It contains no fitted model objects. The renderer neither fits nor predicts. The snapshot manifest covers these inputs, exported figure calculations and SVGs.

Show every person and every arbitrary feature in identity order. A person contributes two specimens, one in each recorded category. Allocation cells represent people; missingness cells represent specimen/feature measurements before imputation. Missingness in assessment specimens is descriptive and never updates training medians. Eligibility is fixed by the synthetic input contract; no additional exclusions are made by these figures.

Show all six candidates and all three inner-fold Brier errors separately for each outer search and the final development search. Mark the saved selected candidate. Fold spread is descriptive, not an interval. Show feature inclusion across the three overlapping outer fits and the final development fit; only the first three contribute to the outer selection count. This is observed selection variation, not a repeated-sampling stability study.

Display final development standardized coefficients for both procedures alongside the selected procedure's mean outer-held-out permutation Brier increase. These have different units. Unselected coefficients are absent, not estimated zero. All 48 features remain visible. Permutation uses the existing five row-wise shuffles per feature per outer assessment, which break person pairing; its importance is a limited diagnostic, not grouped inference or a mechanism of gene action.

## Calibration calculation

Use five fixed probability bins: `[0, .2)`, `[.2, .4)`, `[.4, .6)`, `[.6, .8)`, `[.8, 1]`. Internal endpoints go into the bin on their right. For each procedure and partition, plot the mean saved prediction against the fraction of specimens labeled 1. Show specimen counts and distinct-person counts for every bin, including empty bins. Person counts across bins can exceed the partition total because a person's specimens may occupy different bins. The specimen-weighted target remains the recorded category in this deliberately balanced paired fixture; it is not population cancer prevalence.

For a descriptive uncertainty diagnostic, draw 2,000 bootstrap samples of the partition's people with replacement, carrying both specimens and their fixed probabilities together. Use NumPy's default generator with seed `26101604`, restarted for each procedure/partition, so procedures use matching person draws. Retain the fixed bin boundaries and calculate observed fractions again; use the 2.5th and 97.5th percentiles (`method='linear'`) of nonempty replicates. Save the number of valid replicates for every bin.

Display a vertical interval only when the original bin has at least 10 distinct people, both labels occur, at least 95% of replicates are nonempty, and the percentile limits differ. Otherwise save null limits and a reason (`empty`, `sparse`, `one_label`, `too_many_empty_replicates`, or `degenerate`). Ten people is a teaching display safeguard, not an evidence-based adequacy threshold or coverage guarantee. Missing intervals never mean certainty. Do not change bins, safeguards or seeds after viewing results to obtain a preferred picture.

These are pointwise **conditional person-bootstrap ranges**, assuming exchangeable independent people with the paired structure retained. Predictions and fitted models are held fixed. Especially for pooled outer predictions, people share fitted models, so these ranges omit training/fold dependence and must not be interpreted as confidence intervals for the whole training procedure. They are not simultaneous bands, external-validation precision, or clinical uncertainty. A separately planned refitting/resampling design and substantially more assessment people would be needed to address those questions. No recalibration model or new selection is fitted here.

## Method references

The [scikit-learn 1.8 calibration documentation](https://scikit-learn.org/1.8/modules/generated/sklearn.calibration.calibration_curve.html) defines binned mean probability and observed positive fractions and explains the data demand of extra bins. Our explicit endpoint convention and retained empty bins make the calculation independently auditable.

[Field and Welsh (2007), *Bootstrapping clustered data*](https://doi.org/10.1111/j.1467-9868.2007.00593.x) examines how bootstrap validity depends on the model and clustering structure. It supports taking dependence seriously; it does not validate this small fixture, the chosen display threshold or conditional ranges as full pipeline inference. This foundational reference supplements the project's recent evidence corpus rather than extending its five-year publication register.
