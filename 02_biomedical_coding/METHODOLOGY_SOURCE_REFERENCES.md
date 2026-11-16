# Methodology source references

This bibliography records the source editions behind the independently authored biomedical statistics teaching examples. The author's name is used **only for bibliographic attribution**; it is not the title, name, retrieval key, code symbol, project identity, or general style label of any internal framework.

1. Rosner, Bernard. *Fundamentals of Biostatistics*. 8th ed. Cengage Learning, 2016. ISBN 978-1-305-26892-0. [Source PDF](https://shahealthcare.org/wp-content/uploads/2022/04/Fundamentals-of-Biostatistics-Bernard-Rosner_compressed.pdf). Relevant targeted source sections: §2.4 on sample quantiles (R `type=2`), §6.11 on bootstrap estimation, §9.6 on permutation tests, §12 on multisample inference, §13 on epidemiologic methods, and §14 on person-time/survival. Citation scope is **not** a cover-to-cover verification of all derivations.
2. Rosner, Bernard. *Fundamentals of Biostatistics*. 6th ed. Thomson Brooks/Cole, 2006. ISBN 978-0-495-06441-1. The supplied sixth-edition file contains front matter and the table of contents only; chapter body content was not verified.

**Application policy:** Cite the appropriate edition/section when making a source-specific claim, reproducing a distinct quantile convention, or documenting provenance. General biomedical coding guidance should use descriptive concepts, not author-branded naming. Do not reproduce copyrighted prose, exercises, tables, or textbook figures in the repository.

## Figure-specific source audit

The following **method features**, rather than the original copyrighted image assets, were checked by rendering the actual eighth-edition PDF:

- Chapter 2, §2.8, printed p. 27 (PDF page 49): categorical bar-graph construction with separate rectangular bars and frequency heights; stem-and-leaf as a value-preserving alternative to grouped bars.
- Chapter 2, Figures 2.7–2.8, printed pp. 29–30 (PDF pages 51–52): stem-and-leaf display and a box plot showing lower/upper quartiles, a median line and a separately marked sample mean.
- Chapter 2, definitions 2.11–2.12, printed p. 31 (PDF page 53): 1.5×IQR and 3×IQR outlier thresholds, with distinct ordinary and extreme outlying-value indicators. These are exploratory flags, not individual hypothesis tests.
- Chapter 6, §6.11, Figure 6.11, printed p. 200 (PDF page 222): histogram of 1000 bootstrap estimator replicates, not of the original individual observations.

The associated original programming work is indexed in [Graph method alignment](../03_learning/bio_stats/GRAPH_METHODS_ALIGNMENT.md). All figure examples use new, synthetic measurements. No source image is copied, traced, or embedded.
