# Biomedical graph methodology alignment

**Status:** Figure-method source review completed for foundational graphic methods, the ROC example, a targeted bootstrap figure and the survival-curve example; **R execution and visual QA pending**. This is an original editorial crosswalk, not a reproduction of textbook art.

**Source:** *Fundamentals of Biostatistics*, eighth edition, chapter 2 §2.8 (printed pp. 27–31; PDF pages 49–53) and chapter 3 §3.9 / Figure 3.7 (ROC, printed p. 63; PDF p. 85); chapter 6 §6.11 (bootstrap histogram, printed p. 201; PDF p. 223); and chapter 14 §14.9 / Figure 14.5 (survival curves, printed p. 812; PDF p. 834). The PDF pages were rendered and inspected directly. Full scholarly citation and edition identifiers are maintained solely in [Methodology source references](../../02_biomedical_coding/METHODOLOGY_SOURCE_REFERENCES.md).

## Observed visual method → Paul’s Notes implementation

| Figure family | Observed source treatment | Independent implementation | Mandatory interpretation |
| --- | --- | --- | --- |
| Categorical bar | §2.8 introduces non-contiguous bars of uniform width for grouped frequencies | `biostat_graph_bar()` / synthetic grade frequency | Bars are integer frequencies; axis starts at zero; observed and missing denominators explicit |
| Stem and leaf | §2.8 displays stems and leaves to expose individual values and grouped shape | `biostat_graph_stem()`, using base R’s own text rendering | Individual values visible to selected precision; scale, unit and missingness stated |
| Box plot | §2.8 / Fig. 2.8 shows lower/upper quartiles, median line and a **distinct mean + marker**; discussed skew and distributional spread | `biostat_graph_box()` with manually computed **R type-2 quartiles**, explicit mean cross, observed 1.5×IQR whiskers and optionally visible raw points | Box edges are quartiles, **not confidence limits**; mean symbol distinct from median; show actual n and missingness per group |
| Bootstrap estimator histogram | §6.11 / Fig. 6.11 uses a histogram of 1000 resampled **means**, distinguishing this from patient-level histograms | `biostat_graph_bootstrap()`: original synthetic estimator bootstrap with interval reference lines | x-axis is a resampled estimator in specified units; state B, interval convention and sampling unit |
| Empirical ROC curve | §3.9 / Fig. 3.7 uses sensitivity vertically versus 1−specificity horizontally, connecting threshold coordinates | `biostat_graph_roc()`, with explicit positive class, threshold coordinates, held-out/synthetic partition label and rank/trapezoid AUC identity | Axes both 0–1, never interchange specificity with false-positive rate; AUC is discrimination rather than calibration or PPV |
| Survival curve | §14.9 / Fig. 14.5 displays group-specific estimated survival probabilities against elapsed time | Existing workbook's `survival::survfit()` plot, with months on x and event-free probability on y; censor marks and diagnostic context | Survival is conditional on time zero/event/censoring; these curves are not risk ratios or competing-risk cumulative incidence |
| Ordinary continuous histogram | Distribution shape through adjacent numeric bins; teaching supplement | Gallery’s direct `ggplot2::geom_histogram()` | Frequency counts, bins and measurement units; not categorical percentages |
| **Discrete theoretical PMF** | Teaching supplement, not a claim of directly recreated textbook artwork | Base-R mass functions `stats::dbinom()` and `stats::dpois()`; use explicit integer-count sticks/bars | x = count, y = **probability mass**; point/range/tail separately defined; shaded interval is summed mass, **not a confidence interval** |

The source’s original plot is not recreated, traced, downloaded, embedded, or supplied as a reusable asset. The new figures use entirely synthetic breast cancer teaching values and the existing Okabe–Ito scientific palette.

## Graph selection and description guidance

Select the graph from the estimand and data-generating structure, not from a convenient plotting function. The [statistical reporting standards, §4B](SCIENTIFIC_STATISTICAL_REPORTING_STANDARDS.md#4b--statistical-graphic-vocabulary-and-results-reporting) define precise axis, mark, figure-caption and results-language contracts for probability-mass functions, categorical bars, continuous histograms, boxplots, Q–Q and residual diagnostics, mean/CI plots, bootstrap distributions, scatterplots, ROC and survival curves.

A figure description must identify **what is visible** (shape, separation, spread, outliers, monotonic relation, central/tail deviations), whereas a separate inference sentence names **the computed estimator/test and its uncertainty**. A smooth density, a Q–Q reference line, a boxplot whisker and a fitted-model confidence band do not mean the same thing.

- **PMF:** say *probability mass assigned to integer event counts*, not observed frequency. For an inclusive event range, the probability is the sum of mass bars; the dashed count marker represents a particular queried value.
- **Histogram:** say *observed frequency within numeric bins* or *estimated density* according to the plotted y-axis. For continuous variables, the probability at any one exact real number under an absolutely continuous model is zero, whereas a positive-width interval can have positive probability.
- **Boxplot:** report the median, IQR, quartile algorithm, whisker rule, and outlier display. The box and whiskers are not standard errors or confidence intervals. If a plus sign encodes a mean, name it.
- **Q–Q diagnostic:** report *alignment with the reference line*, curvature, deviations in tails, and ties. Avoid phrases such as “normality confirmed” or “model assumptions passed.”
- **Residual plot:** report visible structure or spread in residuals by fitted value/group; it does not assess sampling independence merely because it looks patternless.
- **ROC:** report *sensitivity versus false-positive rate across thresholds*, not sensitivity versus specificity; AUC describes rank discrimination, not calibration or overall classification accuracy.

Use no more than two findings-led sentences when summarizing one graph in a short teaching report. Render and inspect the output before writing a claim about observed features.

## Explicit conventions and compatibility

- `stats_plots.R` historically uses **R quantile type 7**. Its existing call signatures, outputs and readers remain unchanged.
- The new `biostat_graph_box()` explicitly computes **type 2** quartiles for the teaching figure. Its caption and `figure_statistics` attribute record the convention, unrounded descriptive statistics, sample size, missingness and whisker endpoints.
- Do not compare Q1/Q3 in a type-7 numeric table to a type-2 box as if numerically identical. The [full synthetic breast cancer workbook](../../02_biomedical_coding/examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd) explicitly labels its original table as type 7 and new box as type 2.
- Mean and median must use distinguishable glyphs; neither may be called a confidence interval. Distinguish values outside 1.5×IQR (open circle) from extreme values outside 3×IQR (star); show both counts in machine-readable figure summaries. A violin plot is an optional distribution-density extension, **not** an element the source’s §2.8 box-plot figure requires.
- Do not swap chart orientation or y-axis definitions between a numeric histogram, group box, or categorical frequency display without remapping every axis label and caption. In a violin/box plot of biomarker by subtype, the measured biomarker and its units remain on the *numeric* axis.
- Always distinguish synthetic observations from real patient data and preserve patient/specimen grain. Use subject-level rather than cell-level resampling when inference concerns patients.

## Repository entrypoints

- [Original plotting implementation](../../06_RESOURCES/R/biostat_graphs.R) — `biostat_graph_bar`, `biostat_graph_stem`, `biostat_graph_box`, `biostat_graph_bootstrap`
- [Deterministic synthetic chart contracts](../../06_RESOURCES/tests/test_biostat_graphs.R) — method details, known type-2 quartiles, mean, group N, missingness, invalid data and percentile limits
- [Standalone reproducible gallery](GRAPH_METHODS_SYNTHETIC_GALLERY.Rmd) — synthetic categorical bar, histogram, box + mean, stem-and-leaf, bootstrap histogram
- [Full synthetic study workbook](../../02_biomedical_coding/examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd) — integrated plot alignment without changing its original statistical estimands
- [Scientific palette](../../06_RESOURCES/R/scientific_palette.R) — Okabe–Ito group colors, journal-style axes and layout

## Acceptance gates

G1. Source provenance is narrow: §2.8 and Fig. 2.8 physically reviewed; §6.11 / Fig. 6.11 inspected; do not claim a book-wide graph audit.

G2. R helper tests run with no errors in an R/ggplot2 environment; independently verify group-wise type-2 quartiles, mean cross, ordinary/extreme outlier symbols, count totals, stem render, bootstrap percentile calculation, ROC endpoints and tied-score AUC.

G3. Knit gallery and full study report to HTML. Ensure categorical bar x-axis is group, y-axis count; numeric histogram x-axis is measurement, y-axis count; group box x-axis group, y-axis measured numeric biomarker; bootstrap histogram x-axis estimator, y-axis replicates; ROC x-axis 1−specificity and y-axis sensitivity; survival x-axis elapsed time and y-axis event-free probability.

G4. Compare HTML visually for caption/readability, overplotting, legends, character glyphs, right margin, title overflow and device rendering. Verify figures actually appear, not merely that the HTML file is nonempty.

G5. Run existing `06_RESOURCES/tests/test_*.R` and book/report CI without changing existing types or scientific outcomes. Do not promote completion statuses before execution and visual review are proven.

**Current outcome:** original R functions, tests, gallery, and full-workbook plotting changes are authored; numerical runtime, knit and visual acceptance **remain pending**.
