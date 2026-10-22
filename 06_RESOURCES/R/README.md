# R research tools

[Resources](../README.md) · [Function sheet](EASY_FUNCTION_SHEET.md)

| Task | Source or guide |
| --- | --- |
| **Pick an appropriate statistical test** | [Data-type-first biomedical statistics guide](../../03_learning/biomedical-statistics-decision-guide.md) with a decision flowchart and examples |
| Synthetic biomedical hypothesis-test teaching lab | [Base-R statistical test lab](../../03_learning/examples/statistical_test_lab.R) and [numerical/negative-case tests](../../03_learning/tests/test_statistical_test_lab.R) |
| General summaries and graphs | [Reusable functions](Reusable_Functions.R) |
| Statistical plot helpers | [Statistics and plots](stats_plots.R) |
| Multi-panel summaries | [Biostatistics panels](biostat_panels.R) |
| Gene expression visuals | [Gene visuals](gene_visuals.R) |
| Paired plots, calibration and uncertainty | [Specialist source](specialist_visuals.R) and [guide](../SPECIALIST_VISUALIZATIONS.md) |
| Plot labels and annotations | [Annotation source](plot_annotations.R) and [guide](../PLOT_ANNOTATIONS.md) |
| Compact plotting calls | [One-call source](one_call_plots.R) and [guide](../ONE_CALL_PLOTS.md) |
| Interactive plotting | [Plotly helpers](plotly_visuals.R) |
| Colors and scales | [Scientific palette](scientific_palette.R) |
| Synthetic cohort | [Practice data generator](teaching_data.R) |

Run scripts from the repository root. R and packages used by the selected helper must be installed; consult its `requireNamespace` or package calls. Tests use packages including ggplot2; interactive helpers also require plotly. Record the installed versions in the study's dependency manifest.

```bash
Rscript --vanilla 06_RESOURCES/tests/test_stats_plots.R
Rscript --vanilla 06_RESOURCES/tests/test_specialist_visuals.R
Rscript --vanilla 06_RESOURCES/Genomics/FIGURES/gene_companion_walkthrough.R
```

Additional companion checks are in [tests](../tests/). Functions use descriptive `snake_case` names. Synthetic demonstrations are not estimated clinical findings.

For additional summary, figure and interactive-export checks, see the [learning checks](../../03_learning/mastery-checks.md#reusable-resources-and-the-book). Continuous integration runs every retained R test suite with its dependencies installed.
