# R research tools

[Resources](../README.md) · [Function sheet](EASY_FUNCTION_SHEET.md)

| Task | Source or guide |
| --- | --- |
| General summaries and graphs | [Reusable functions](Reusable_Functions.R) |
| Statistical plot helpers | [Statistics and plots](hse_stats_plots.R) |
| Multi-panel summaries | [Biostatistics panels](hse_biostat_panels.R) |
| Gene expression visuals | [Gene visuals](hse_gene_visuals.R) |
| Paired plots, calibration and uncertainty | [Specialist source](hse_specialist_visuals.R) and [guide](../SPECIALIST_VISUALIZATIONS.md) |
| Plot labels and annotations | [Annotation source](hse_plot_annotations.R) and [guide](../PLOT_ANNOTATIONS.md) |
| Compact plotting calls | [One-call source](hse_one_call_plots.R) and [guide](../ONE_CALL_PLOTS.md) |
| Interactive plotting | [Plotly helpers](hse_plotly_visuals.R) |
| Colors and scales | [Scientific palette](hse_scientific_palette.R) |
| Synthetic cohort | [Practice data generator](hse_teaching_data.R) |

Run scripts from the repository root. R and packages used by the selected helper must be installed; consult its `requireNamespace` or package calls. Tests use packages including ggplot2; interactive helpers also require plotly. Record the installed versions in the study's dependency manifest.

```bash
Rscript --vanilla 06_RESOURCES/tests/test_hse_stats_plots.R
Rscript --vanilla 06_RESOURCES/tests/test_hse_specialist_visuals.R
Rscript --vanilla 06_RESOURCES/Genomics/FIGURES/gene_companion_walkthrough.R
```

Additional companion checks are in [tests](../tests/). The `hse_` function prefix is retained for compatibility with existing callers. Synthetic demonstrations are not estimated clinical findings.
