# Biomedical and biostatistical visualization in R — evidence-to-code matrix

**Author:** Paul Skeffington · **Prepared with OpenAI**  
**Reviewed:** 11 October 2026 · **Status:** curated methodological bibliography and implementation plan

[Resource index](../README.md) · [Literature index](README.md) · [Visualization gallery](../SPECIALIST_VISUALIZATIONS.md) · [Reusable R modules](../R/README.md) · [Scientific palette](../R/scientific_palette.R)

This original guide maps peer-reviewed biostatistics, data-visualization methods, reporting guidance and software references to reproducible R plots. It is a *targeted literature matrix*, not an exhaustive or systematic review. Papers about visual perception, software, statistical models, and study/reporting guidelines provide different types of evidence; no single paper certifies that a plot is clinically valid. Runtime tests, patient privacy review and scientific admission are separate release gates.

## Decide what to show before choosing a plotting function

| Research question | Preferred visualization | Existing R implementation / next implementation | Interpretive safeguard |
| --- | --- | --- | --- |
| What is the distribution of a biomarker? | Raw dots with box/violin; histogram or ECDF | [one-call plots](../ONE_CALL_PLOTS.md), [gallery](../SPECIALIST_VISUALIZATIONS.md) | Show n, units and missingness; never treat box whiskers as CIs |
| How does a patient's value change over time? | Matched trajectory, hybrid paired line | plot_trajectory in [biostat_panels.R](../R/biostat_panels.R) | Confirm unique ID × visit; specify complete-pair denominator |
| What are the estimated group effects? | Effect-size / coefficient forest with intervals | ggplot2::geom_pointrange; only verified model output | State reference group, estimator, uncertainty type and multiplicity |
| How do measurements relate? | Scatter, fitted model and diagnostics | [one-call plots](../ONE_CALL_PLOTS.md) | State units; no causal claim from association |
| What patterns occur in gene expression? | Annotated heatmap, PCA, MA | [gene_visuals.R](../R/gene_visuals.R) | Freeze matrix identifiers; describe normalized expression versus row z-score |
| Do statistical tests support a contrast? | Volcano or uncertainty interval | Gene plotting only after inferential gate | Do not derive FDR/CI from descriptive effect sizes |
| How well does a diagnostic classifier discriminate? | ROC plus PR when cases are rare | [biostat panels](../R/README.md); pROC / yardstick | Use out-of-sample labels and scores; record event prevalence |
| Are predicted clinical risks calibrated? | Observed versus predicted risk / calibration curve | Planned validation plot: ggplot2::geom_point + geom_line + geom_abline | Require held-out predictions, events, horizon and smoothing details |
| Does a single-cell embedding show separation? | UMAP/t-SNE with batch and sample facets | Planned: Seurat::DimPlot; documented seed/settings | Neighbor and cluster appearance is exploratory, not a formal test |
| Do imaging measurements differ? | Independent-specimen summaries with cell-level detail | Planned: ggplot2::geom_point + geom_boxplot + facet_wrap | Cells and image fields within a specimen are not independent participants |
| Are there public-health spatial differences? | Standardized rate choropleth with suppression | Planned: ggplot2::geom_sf + sequential fill | Map denominators, uncertainty and privacy protections, not raw counts as risks |

## Scholarly matrix

*Each linked DOI is a primary publication record. R functions are proposed mappings, not commands supplied by the authors unless the paper concerns the named package.*

| ID | Source | Research or guidance contribution | Plotting use |
| --- | --- | --- | --- |
| L01 | [Cleveland & McGill, 1984](https://doi.org/10.1080/01621459.1984.10478080) | Experimental research on visual estimation | Position encodings; point/forest plots |
| L02 | [Wickham, 2010](https://doi.org/10.1198/jcgs.2009.07098) | Layered grammar of graphics | ggplot2 composition |
| L03 | [Wickham et al., 2019](https://doi.org/10.21105/joss.01686) | Tidyverse software ecosystem | Data preprocessing |
| L04 | [Weissgerber et al., 2015](https://doi.org/10.1371/journal.pbio.1002128) | Critique of summary-only bar plots | Raw observations |
| L05 | [Weissgerber et al., 2019](https://doi.org/10.1161/CIRCULATIONAHA.118.037777) | Transparent biological data displays | Small samples and pairing |
| L06 | [Allen et al., 2019 / revised version](https://doi.org/10.12688/wellcomeopenres.15191.2) | Raincloud displays | Density + raw points |
| L07 | [Ho et al., 2019](https://doi.org/10.1038/s41592-019-0470-3) | Estimation graphics | Effect magnitude and CIs |
| L08 | [Patil, 2021](https://doi.org/10.21105/joss.03167) | Statistical graphic annotations in R | ggstatsplot |
| L09 | [Kay, 2024](https://doi.org/10.1109/TVCG.2023.3327195) | Distribution/uncertainty graphics | ggdist intervals |
| L10 | [Zeileis et al., 2020](https://doi.org/10.18637/jss.v096.i01) | Perceptually designed palettes | colorspace |
| L11 | [Crameri et al., 2020](https://doi.org/10.1038/s41467-020-19160-7) | Misleading color scales | Sequential and diverging colors |
| L12 | [Jambor, 2025](https://doi.org/10.1038/s41556-025-01684-z) | Scientific figure checklist | Labels, clarity, readability |
| L13 | [Torres et al., 2025](https://doi.org/10.1371/journal.pone.0336917) | Biomedical figure-scoring proposal | Experimental design review, not a universal standard |
| L14 | [Jambor & Bornhäuser, 2024](https://doi.org/10.1371/journal.pcbi.1011789) | Graphical abstracts | Concept visuals |
| L15 | [Sjoberg et al., 2021](https://doi.org/10.32614/RJ-2021-053) | Reproducible tables | gtsummary |
| L16 | [Gu et al., 2016](https://doi.org/10.1093/bioinformatics/btw313) | Multidimensional genomic heatmaps | ComplexHeatmap |
| L17 | [Gu, 2022](https://doi.org/10.1002/imt2.43) | Complex heatmap tutorial | Multi-omic annotations |
| L18 | [Love et al., 2014](https://doi.org/10.1186/s13059-014-0550-8) | DESeq2 model | MA/volcano with verified results |
| L19 | [Ritchie et al., 2015](https://doi.org/10.1093/nar/gkv007) | limma inference | Contrasts and multiplicity |
| L20 | [Robin et al., 2011](https://doi.org/10.1186/1471-2105-12-77) | ROC package | pROC |
| L21 | [Sachs, 2017](https://doi.org/10.18637/jss.v079.c02) | ROC plot construction | plotROC |
| L22 | [Saito & Rehmsmeier, 2015](https://doi.org/10.1371/journal.pone.0118432) | Precision–recall in imbalanced settings | yardstick PR |
| L23 | [Collins et al., 2024](https://doi.org/10.1136/bmj-2023-078378) | TRIPOD+AI reporting | Prediction assessment |
| L24 | [Bland & Altman, 1986](https://doi.org/10.1016/S0140-6736(86)90837-8) | Clinical method agreement | Difference versus mean |
| L25 | [Ben-Shachar et al., 2020](https://doi.org/10.21105/joss.02815) | Effect size software | effectsize estimates |
| L26 | [Freeman et al., 2026](https://doi.org/10.1128/mbio.00572-26) | Audit of 8,834 biology figures across 2,930 studies | Replace mean-only bars when appropriate |
| L27 | [Schriger, 2018](https://doi.org/10.1016/j.annemergmed.2017.05.033) | Paired-clinical-data graph tutorial | Hybrid matched lines |
| L28 | [Xia et al., 2024](https://doi.org/10.1038/s41467-024-45891-y) | Diagnostic assessment of potentially misleading single-cell embeddings | UMAP/t-SNE caution |
| L29 | [Senft et al., 2023](https://doi.org/10.1371/journal.pbio.3002167) | Quantitative microscopy workflow | Image-derived measurements |
| L30 | [Van Calster et al., 2019](https://doi.org/10.1186/s12916-019-1466-7) | Clinical prediction calibration | Reliability displays |

## Five additional plotting blueprints (Pass 2)

| ID | Inputs required | Output and labels | Stop condition |
| --- | --- | --- | --- |
| P19 Calibration | Held-out true outcomes, predicted risk, event horizon, evaluation partition | Observed-versus-predicted, identity line, events/n, smoothing/bin method | Training predictions presented as external validation |
| P20 Single-cell embedding | Normalized cell data or validated embeddings; sample/batch labels; seed/settings | UMAP/t-SNE axes, points, batch facets, preprocessing note | Inferring biological truth from proximity alone |
| P21 Quantitative microscopy | Specimen, field/cell nesting, numeric measurement and units | Points nested by specimen, specimen-level summaries, n at each level | Pseudoreplication; unlabeled image acquisition method |
| P22 Paired comparison | One non-missing matched subject × visit observation; explicit time order | Patient lines, complete-pair n, between-group facet | Duplicate or mismatched subject/visit keys |
| P23 High-volume raw-data display | Raw measurement, group, denominator, inclusion/subsample seed | Faceted raw/sample overlay and distribution; disclosed n | Downsampling that hides extreme values |

## Scientific figure admission and release contract

Apply the full [figure workflow](../SPECIALIST_VISUALIZATIONS.md) and [annotation requirements](../PLOT_ANNOTATIONS.md). In addition to the established checks for units, missingness, inferential authority, palette semantics, privacy, reproducibility and export QA, Pass 2 adds:

- **Q17 Independent unit:** Count participants, specimens, fields, and cells separately. Do not silently analyze dependent observations as independent.
- **Q18 Embedding reliability:** Preserve seed, preprocessing, model settings, and sensitivity analyses where applicable.
- **Q19 Prediction calibration:** Prove evaluation partition, event horizon and outcomes before release.
- **Q20 Sampling transparency:** Record filters, original N, displayed N, sample selection and deterministic random seed.

No graph should acquire a p-value, false-discovery rate or confidence interval merely because its plotting API supports the annotation. If only descriptive effects are authorized, use descriptive plots and explain the unavailable inferential quantities.

## Code and release roadmap

**Gate V1 — literature:** DOI and study-type checks for all thirty records; distinguish independent evidence from implementation choices. The five new records L26–L30 were publisher/PubMed checked on 11 October 2026. The earlier 25 are inherited from the first curated matrix.

**Gate V2 — R dependency and data schema:** Build an explicit source/role contract for every new plot. Reuse current modules where supported; use existing Okabe–Ito, viridis, and zero-centered diverging scales only when appropriate to variable semantics.

**Gate V3 — numerical tests:** Check pair keys, denominators, intervals, estimated effects, normalization direction, embedded labels, color semantics, missingness and invalid-input rejection. Synthetic inputs only in public tests.

**Gate V4 — figure QA:** Run the gallery and R numerical validators, then export high-resolution PNG and vector PDF. Inspect the actual figures at publication size. Output file existence alone is not visual QA.

**Gate V5 — release:** Link reviewed plots from this guide, [the gallery](../SPECIALIST_VISUALIZATIONS.md) and [the resource index](../README.md). No exposure of private data or clinical conclusions without source-specific authorization.

Run existing review checks from the repository root:

~~~bash
python3 06_RESOURCES/Presentation/check_navigation.py
python3 06_RESOURCES/Presentation/build_reading_editions.py --check
python3 scripts/validate_visualization_gallery.py --output-dir /tmp/pauls-gallery-check
~~~

The gallery validator requires Rscript and relevant R packages; an environment without them cannot certify V3 or V4.

## Implementation notes and authoritative package references

- [ggplot2 graphics and exports](https://ggplot2.tidyverse.org/reference/ggsave.html)
- [colorspace](https://colorspace.r-forge.r-project.org/)
- [ComplexHeatmap](https://bioconductor.org/packages/ComplexHeatmap/)
- [Seurat DimPlot](https://satijalab.org/seurat/reference/dimplot)
- [ggsurvfit](https://www.danieldsjoberg.com/ggsurvfit/)
- [TRIPOD+AI](https://doi.org/10.1136/bmj-2023-078378)

**Boundary:** This bibliography does not release a new inferred clinical finding, new validated analysis, or R implementation. It supplies the traceable evidence and acceptance criteria for those next implementation gates.
