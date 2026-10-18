# Volcano plots in R: a synthetic teaching example

[Paul's Notes](../README.md) · [Research resources](README.md) · [Reading plots](READING_PLOTS.md) · [Gene visualization functions](R/gene_visuals.R)

A volcano plot puts a **gene-level effect size** on the horizontal axis and **statistical evidence** on the vertical axis. This walkthrough generates artificial values only: **no TCGA data, patient specimens, measured expression, or fitted differential-expression model** are used. It teaches construction, thresholds, labeling, and export—not biological inference.

## Read the figure

| Element | Meaning |
| --- | --- |
| One point | One invented feature |
| X axis | Simulated log2 fold change; negative and positive are illustrative directions |
| Y axis | `-log10` of a simulated BH-adjusted p-value |
| Vertical dashed lines | Example effect thresholds at -1 and +1 |
| Horizontal dashed line | Example adjusted-p cutoff of 0.05 |
| Blue, red, gray | Below -1, above +1, or neither, *when the adjusted-p cutoff is also met* |

## Run a reproducible example

Install `ggplot2` once with `install.packages("ggplot2")`. Run the following in an R script or an R Markdown chunk. No additional package is required.

```r
library(ggplot2)

set.seed(711)
n_features <- 500L

demo <- data.frame(
  feature = sprintf("Feature_%03d", seq_len(n_features)),
  log2FC = rnorm(n_features, mean = 0, sd = 1.4),
  p_value = runif(n_features)
)

# Artificial p-values are deliberately smaller for selected display features.
highlight <- c(12L, 75L, 144L, 280L, 421L)
demo$log2FC[highlight] <- c(-3.0, -2.1, 2.6, 3.2, -2.7)
demo$p_value[highlight] <- c(1e-8, 3e-6, 2e-7, 1e-9, 8e-7)

demo$padj <- p.adjust(demo$p_value, method = "BH")
demo$score <- -log10(pmax(demo$padj, .Machine$double.xmin))
demo$status <- ifelse(
  demo$padj < 0.05 & demo$log2FC <= -1, "Lower",
  ifelse(demo$padj < 0.05 & demo$log2FC >= 1, "Higher", "Other")
)

palette <- c(Lower = "#2166AC", Other = "#A0A0A0", Higher = "#B2182B")

p <- ggplot(demo, aes(x = log2FC, y = score)) +
  geom_point(aes(color = status), alpha = 0.75, size = 1.7) +
  geom_vline(xintercept = c(-1, 1), color = "grey40",
             linewidth = 0.45, linetype = "dashed") +
  geom_hline(yintercept = -log10(0.05), color = "grey40",
             linewidth = 0.45, linetype = "dashed") +
  geom_text(
    data = demo[highlight, , drop = FALSE],
    aes(label = feature),
    color = "grey15", size = 3, vjust = -0.8,
    check_overlap = TRUE
  ) +
  scale_color_manual(values = palette,
                     breaks = c("Lower", "Other", "Higher"),
                     labels = c("Lower", "Other", "Higher"),
                     name = "Illustrative cutoff") +
  labs(
    title = "Synthetic volcano-style plot",
    subtitle = sprintf("%s simulated features | Not biological data", n_features),
    x = "Simulated log2 fold change",
    y = "-log10(BH-adjusted simulated p-value)",
    caption = paste0(
      "Dashed lines: |log2 fold change| = 1 and BH-adjusted p = 0.05.\n",
      "Instructional visualization only; p-values are invented.\n",
      "No count model, experimental design, or biological inference."
    )
  ) +
  theme_minimal(base_size = 11) +
  theme(
    plot.title = element_text(face = "bold"),
    legend.position = "bottom",
    panel.grid.minor = element_blank(),
    plot.caption = element_text(color = "grey30", size = 8,
                                lineheight = 1.25, margin = margin(t = 10)),
    plot.margin = margin(12, 14, 14, 14)
  )

print(p)

dir.create("figures", showWarnings = FALSE)
ggsave("figures/synthetic_volcano.pdf", p,
       width = 8, height = 5.5, units = "in", bg = "white")
ggsave("figures/synthetic_volcano.png", p,
       width = 8, height = 5.5, units = "in", dpi = 300, bg = "white")
```

Both plots use the same data and styling; the PDF is vector-based and the PNG is 300 DPI. The `\n` characters explicitly break the caption into three lines.

## Check the output

```r
stopifnot(
  nrow(demo) == 500L,
  !anyNA(demo$padj),
  all(demo$padj >= 0 & demo$padj <= 1),
  all(is.finite(demo$score)),
  all(demo$status %in% c("Lower", "Other", "Higher")),
  file.exists("figures/synthetic_volcano.pdf"),
  file.exists("figures/synthetic_volcano.png")
)
table(demo$status)
```

The seeded example is reproducible across repeated runs with the same R random-number generation settings. Thresholds are selectable design choices; they should be declared before applying them to scientific findings.

## Moving from a demonstration to research

For real bulk RNA-seq data, start with raw integer gene counts, confirmed sample IDs, independent biological replicates, and a justified study design. Fit a count-aware model such as **DESeq2** or **edgeR**, incorporating pairing and batch structure when supported and identifiable. Pass the resulting model-derived log2 fold changes and adjusted p-values to the plot; **do not substitute random p-values, Welch tests on transformed counts, or a CPM ratio as though they were differential-expression results**.

The existing [`plot_gene_volcano()` function](R/gene_visuals.R) accepts model-derived result columns and can be reused once the inferential gate is complete. For interpretation standards, consult [Reading plots](READING_PLOTS.md) and [Biostatistical R visualization evidence](Literature/BIOSTAT_R_VISUALIZATION_EVIDENCE_MATRIX.md).

**Method references:** [Love, Huber & Anders (2014), DESeq2](https://doi.org/10.1186/s13059-014-0550-8) · [Robinson, McCarthy & Smyth (2010), edgeR](https://doi.org/10.1093/bioinformatics/btp616) · [Benjamini & Hochberg (1995), FDR](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x).
