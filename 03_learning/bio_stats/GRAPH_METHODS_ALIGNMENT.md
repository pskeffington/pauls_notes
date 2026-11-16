# Biomedical graph methodology alignment

**Status:** Figure-method source review completed for the foundational graph chapter and a targeted bootstrap figure; **R execution and visual QA pending**. This is an original editorial crosswalk, not a reproduction of textbook art.

**Source:** *Fundamentals of Biostatistics*, eighth edition, chapter 2 §2.8 (printed pp. 27–31; PDF pages 49–53) and chapter 6 §6.11 (bootstrap histogram, printed p. 200; PDF p. 222). The PDF pages were rendered and inspected directly. Full scholarly citation and edition identifiers are maintained solely in [Methodology source references](../../02_biomedical_coding/METHODOLOGY_SOURCE_REFERENCES.md).

## Observed visual method → Paul’s Notes implementation

| Figure family | Observed source treatment | Independent implementation | Mandatory interpretation |
| --- | --- | --- | --- |
| Categorical bar | §2.8 introduces non-contiguous bars of uniform width for grouped frequencies | `biostat_graph_bar()` / synthetic grade frequency | Bars are integer frequencies; axis starts at zero; observed and missing denominators explicit |
| Stem and leaf | §2.8 displays stems and leaves to expose individual values and grouped shape | `biostat_graph_stem()`, using base R’s own text rendering | Individual values visible to selected precision; scale, unit and missingness stated |
| Box plot | §2.8 / Fig. 2.8 shows lower/upper quartiles, median line and a **distinct mean + marker**; discussed skew and distributional spread | `biostat_graph_box()` with manually computed **R type-2 quartiles**, explicit mean cross, observed 1.5×IQR whiskers and optionally visible raw points | Box edges are quartiles, **not confidence limits**; mean symbol distinct from median; show actual n and missingness per group |
| Bootstrap estimator histogram | §6.11 / Fig. 6.11 uses a histogram of 1000 resampled **means**, distinguishing this from patient-level histograms | `biostat_graph_bootstrap()`: original synthetic estimator bootstrap with interval reference lines | x-axis is a resampled estimator in specified units; state B, interval convention and sampling unit |
| Ordinary continuous histogram | Distribution shape through adjacent numeric bins; teaching supplement | Gallery’s direct `ggplot2::geom_histogram()` | Frequency counts, bins and measurement units; not categorical percentages |

The source’s original plot is not recreated, traced, downloaded, embedded, or supplied as a reusable asset. The new figures use entirely synthetic breast cancer teaching values and the existing Okabe–Ito scientific palette.

## Explicit conventions and compatibility

- `stats_plots.R` historically uses **R quantile type 7**. Its existing call signatures, outputs and readers remain unchanged.
- The new `biostat_graph_box()` explicitly computes **type 2** quartiles for the teaching figure. Its caption and `figure_statistics` attribute record the convention, unrounded descriptive statistics, sample size, missingness and whisker endpoints.
- Do not compare Q1/Q3 in a type-7 numeric table to a type-2 box as if numerically identical. The [full synthetic breast cancer workbook](../../02_biomedical_coding/examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd) explicitly labels its original table as type 7 and new box as type 2.
- Mean and median must use distinguishable glyphs; neither may be called a confidence interval. A violin plot is an optional distribution-density extension, **not** an element the source’s §2.8 box-plot figure requires.
- Do not swap chart orientation or y-axis definitions between a numeric histogram, group box, or categorical frequency display without remapping every axis label and caption. In a violin/box plot of biomarker by subtype, the measured biomarker and its units remain on the *numeric* axis.
- Always distinguish synthetic observations from real patient data and preserve patient/specimen grain. Use subject-level rather than cell-level resampling when inference concerns patients.

## Repository entrypoints

- [Original plotting implementation](../../06_RESOURCES/R/biostat_graphs.R) — `biostat_graph_bar`, `biostat_graph_stem`, `biostat_graph_box`, `biostat_graph_bootstrap`
- [Deterministic synthetic chart contracts](../../06_RESOURCES/tests/test_biostat_graphs.R) — method details, known type-2 quartiles, mean, group N, missingness, invalid data and percentile limits
- [Standalone reproducible gallery](GRAPH_METHODS_SYNTHETIC_GALLERY.Rmd) — synthetic categorical bar, histogram, box + mean, stem-and-leaf, bootstrap histogram
- [Full synthetic study workbook](../../02_biomedical_coding/examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd) — integrated plot alignment without changing its original statistical estimands
- [Scientific palette](../../06_RESOURCES/R/scientific_palette.R) — Okabe–Ito group colors, journal-style axes and layout

## Acceptance gates

G1. Source provenance is narrow: §2.8 and Fig. 2.8 physically reviewed; §6.11/ Fig. 6.11 inspected; do not claim a book-wide graph audit.

G2. R helper tests run with no errors in an R/ggplot2 environment; independently verify group-wise type-2 quartiles and mean cross, count totals, stem render and percentile calculation.

G3. Knit gallery and full study report to HTML. Ensure categorical bar x-axis is group, y-axis count; numeric histogram x-axis is measurement, y-axis count; group box x-axis group, y-axis measured numeric biomarker; bootstrap histogram x-axis estimator, y-axis replicates.

G4. Compare HTML visually for caption/readability, overplotting, legends, character glyphs, right margin, title overflow and device rendering. Verify figures actually appear, not merely that the HTML file is nonempty.

G5. Run existing `06_RESOURCES/tests/test_*.R` and book/report CI without changing existing types or scientific outcomes. Do not promote completion statuses before execution and visual review are proven.

**Current outcome:** original R functions, tests, gallery, and full-workbook plotting changes are authored; numerical runtime, knit and visual acceptance **remain pending**.
