# Synthetic biostatistics and scientific narrative in R

This toolkit converts computed research statistics into **reusable, auditable Results prose**, never fabricated interpretations. It is a synthetic counterpart to the HSE 712 week-two methods and is not a copy of the actual course records.

## Files

- [`biomedical_narrative.R`](../../06_RESOURCES/R/biomedical_narrative.R) - group summaries, positive-only geometric means, Shapiro-Wilk (optional Anderson-Darling and Lilliefors), central-limit normal approximation, directional tail probability, and tightly conditioned narrative.
- [`synthetic_biostat.R`](../../06_RESOURCES/R/synthetic_biostat.R) - reproducible, fictitious participants with missing values and one zero biomarker.
- [`test_biomedical_narrative.R`](../../06_RESOURCES/tests/test_biomedical_narrative.R) - positive and negative fixtures.
- Existing shared code: [stats_plots.R](../../06_RESOURCES/R/stats_plots.R), [scientific_palette.R](../../06_RESOURCES/R/scientific_palette.R), [teaching_data.R](../../06_RESOURCES/R/teaching_data.R), and [statistical_test_lab.R](../../03_learning/examples/statistical_test_lab.R). Reuse these, do not fork their implementations.

## R Markdown use (one setup, reusable named chunks)

```r
# ================================================================
# 01 | SCIENTIFIC NARRATIVE SETUP
# ================================================================
source("06_RESOURCES/R/biomedical_narrative.R")
source("06_RESOURCES/R/synthetic_biostat.R")
d <- pn_make_synthetic_biostat(n = 120L, seed = 712L)

# ================================================================
# 02 | DESCRIPTIVE REPORTING
# ================================================================
hb <- pn_group_descriptives(d, "hemoglobin_g_dl", "group")
knitr::kable(hb, digits = 3, caption = "Synthetic hemoglobin by group")
cat(paste(pn_narrate_group(hb, "Hemoglobin", "g/dL"), collapse = "\n\n"))

# ================================================================
# 03 | BIOMARKER LOG AND GEOMETRIC MEANS
# ================================================================
gm <- pn_geometric_descriptives(d, "marker_mg_l", "group")
knitr::kable(gm, digits = 3, caption = "Synthetic biomarker geometric means")
cat(paste(pn_narrate_geometric(gm, "Marker", "mg/L"), collapse = "\n\n"))

# ================================================================
# 04 | SAMPLING DISTRIBUTION AND TAIL
# ================================================================
x <- d$hemoglobin_g_dl[d$group == "Reference"]
result <- pn_sampling_mean(x, assumed_mean = 12.5)
cat(pn_narrate_sampling(result, unit = "g/dL"))

# ================================================================
# 05 | NORMALITY ASSUMPTION AUDIT
# ================================================================
diagnostics <- pn_normality_diagnostics(x)
print(diagnostics)\ncat(pn_narrate_normality(diagnostics, group = "Reference"))
```

When knitting, use a results='asis' chunk for Markdown prose if required, or regular output for verbatim narrative. To keep source text personal, code comments can be used as operator notes; the narrative text is derived from numeric objects.

## Method inventory / acceptance gates

| Course method | Existing source | New synthetic exercise | Gate |
| --- | --- | --- | --- |
| Participant IDs, missingness, group counts | `stats_plots.R` / existing lab | Cohort with unique synthetic identifiers and NA | G2 |
| Mean, sample SD, median, Q1/Q3, IQR | `describe_measurements()` | `pn_group_descriptives()` and prose | G2/G7 |
| Histogram, box, violin, normal Q-Q, empirical CDF | Existing `stats_plots.R`, `biostat_panels.R`, `one_call_plots.R` | Reuse plotting tools, no new duplicate plotting engine | G7 |
| Shapiro-Wilk | Base R `stats::shapiro.test` | `pn_normality_diagnostics()` | G5 |
| Anderson-Darling, Lilliefors | `nortest` (optional) | `pn_normality_diagnostics(extra=TRUE)` | G5 |
| Sampling mean normal reference and plug-in SE | Base R `sd`, `sqrt` | `pn_sampling_mean()` | G5 |
| One-sided extreme tail area | Base R `pnorm` | `pn_sampling_mean()` and `pn_narrate_sampling()` | G5/G7 |
| Log biomarker eligibility and geometric mean | Base R `log`, `exp` | `pn_geometric_descriptives()` | G2/G5 |
| Results prose and scientific probability language | Newly centralized narrative layer | `pn_narrate_*()` | G7/G8 |
| Palette / professional figures | `scientific_palette.R` | Use existing Okabe-Ito mapping; no copied palette | G7 |

**Scope and safeguards:** All results here are sample descriptions or explicitly model-conditional normal-tail probabilities. A one-sided tail is not a two-sided p-value; a normality non-rejection does not establish normality; a descriptive group contrast does not establish significance or causation. If real NHANES analyses are intended, use survey weights and design information before claiming population-representative estimates. The synthetic fixture has no clinical significance.

## Validation

```bash
Rscript --vanilla 06_RESOURCES/tests/test_biomedical_narrative.R
```

For optional Anderson-Darling/Lilliefors functions, install `nortest`. Report R and package versions when results are published. Tests assert expected behavior on fictional records; they cannot certify clinical validity, real study assumptions, or scientific conclusions. Refer to [implementation gates](IMPLEMENTATION_GATES.md).
