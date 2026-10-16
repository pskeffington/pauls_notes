# Machine learning plotting gallery

[Breast cancer narrative](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) · [Comparison guide](../model-comparison.md) · [Data-flow diagrams](../visual-data-guide.md) · [Broader visualization resources](../../06_RESOURCES/SPECIALIST_VISUALIZATIONS.md)

These first two figures follow the book’s question from invented paired specimens to assessed predictions. They are generated from the [saved specimen probabilities](example/predictions.csv) and [comparison report](example/report.json), not drawn from performance targets. The fixed version 1 example uses 60 people, two specimens each, and 48 arbitrary continuous assay features. No named-gene or clinical result is depicted.

The selected procedure tunes subset size and C. The comparator keeps all features with C fixed at 1.0. Their comparison includes that difference in tuning, so it does not isolate the effect of feature selection. The [protocol](../comparison-protocol.md), [runtime versions](example/versions.json), report source hashes and [snapshot manifest](example/manifest.json) identify this example.

## Compare probability error

![Synthetic Brier errors for selected, fixed all-feature and prevalence procedures, separately for outer-held-out development and reserved-test people](example/brier-comparison.svg)

**Read the axes:** Bar height is mean squared probability error, where zero is perfect and lower is better. Each set uses the same excluded people across procedures. The left group contains 45 development people whose predictions came from outer fits excluding them; the right contains 15 people reserved from the initial split. The training-prevalence value is estimated without those assessment outcomes.

**Interpret:** The selected/tuned procedure has lower mean error in this draw. That is a descriptive comparison of two declared procedures on engineered data. The two groups answer different assessment questions; their bars are not independent replications. There are no uncertainty intervals or clinical efficacy estimates.

**Try:** Recompute each bar from `selected_squared_error`, `all_feature_squared_error` and `prevalence_squared_error`, filtering by `partition`. Explain why a high AUROC could coexist with poor probability error.

## Inspect differences within people

![Each dot shows the average selected-minus-all-feature squared-error difference over a person's two synthetic specimens, with separate development and final-test panels](example/person-errors.svg)

**Read the axes:** One dot is one person, averaging that person’s two specimen errors. Below zero favors selected plus tuned C; above zero favors the fixed all-feature procedure. Position on the horizontal axis is an invented identity, not severity, time or rank. Both panels use the same bounded error-difference scale.

**Interpret:** An average advantage can coexist with worse predictions for some people. These dots are descriptive paired differences. They are not fold standard errors, causal effects, independent effect estimates, or confidence intervals. Equal specimen counts make the person-weighted and specimen-weighted mean differences equal only in this fixture.

**Try:** Find an above-zero and a below-zero point, recover their specimen probabilities, and explain each difference. Do not use those people to select a new panel and then reuse the same assessment as fresh validation.

## Rebuild and export

Run the [comparison deployment](../model-comparison.md#run-and-inspect) to generate a complete bundle, including figures in SVG, PDF and PNG. To redraw figures without training or loading a model:

```bash
python3 04_machine_learning/examples/plot_comparison.py 04_machine_learning/gallery/example /tmp/breast-cancer-figures
```

Choose a new directory outside the repository with an existing parent. The plotting function validates the saved numeric inputs and uses the noninteractive Matplotlib backend. SVG/PDF preserve vector content; PNG is useful for previews. Text, denominators, loss direction and observation units should stay with exported figures.

## What comes next

| Display | Status |
| --- | --- |
| Matched procedure Brier errors | Available above |
| Person-level paired error differences | Available above |
| Person/specimen allocation and missingness | Planned |
| Inner candidate scores and selected settings | Planned |
| Feature-selection stability and coefficient/importance contrasts | Planned |
| Calibration with counts and justified uncertainty treatment | Planned |

The [learning roadmap](../../docs/learning-roadmap.md) distinguishes the initial comparison gallery from those later displays. The [existing R figure guide](../../03_learning/figures-and-features.md) covers additional plotting mechanics while those ML-specific views are developed.
