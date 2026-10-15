# Primary software documentation — current API sources

See the separate [official methods and specifications register](OFFICIAL_METHODS_REGISTER.md) for 36 version-sensitive health-data, research-software, genomics and clinical research standards.

Foundational papers describe methods and historical software. Before implementing an algorithm, use its maintained manual, write down the installed version, and separately validate study assumptions. URLs here are **documentation pointers**, not mirrored external content.

| Technical area | Maintainer documentation | Implementation purpose |
| --- | --- | --- |
| R language and stats | [R manuals](https://cran.r-project.org/manuals.html) | Base types, mathematical notation, model formulae |
| caret | [CRAN caret](https://cran.r-project.org/package=caret) | Resampling and tuning; verify the current package status/API |
| Modern R modeling | [tidymodels](https://www.tidymodels.org/) | Current modeling and recipe/resampling approaches |
| lme4 | [CRAN lme4](https://cran.r-project.org/package=lme4) | Mixed-effects model formulation and diagnostics |
| Bioconductor | [Bioconductor](https://bioconductor.org/) | Matching R/Bioconductor versions and scientific containers |
| DESeq2 | [DESeq2 vignette](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html) | Count assumptions, design and contrasts |
| edgeR | [edgeR](https://bioconductor.org/packages/release/bioc/html/edgeR.html) | Count analysis and library normalization |
| limma | [limma](https://bioconductor.org/packages/release/bioc/html/limma.html) | Linear models, voom and planned contrasts |
| ComplexHeatmap | [ComplexHeatmap guide](https://jokergoo.github.io/ComplexHeatmap-reference/book/) | Heatmaps, scales and layered annotations |
| Python computing | [NumPy](https://numpy.org/doc/stable/), [pandas](https://pandas.pydata.org/docs/), [SciPy](https://docs.scipy.org/doc/scipy/) | Numeric and tabular contracts |
| Scikit-learn | [Pipeline user guide](https://scikit-learn.org/stable/modules/compose.html) | Train-only feature pipelines |
| Scanpy/scVI | [Scanpy docs](https://scanpy.readthedocs.io/), [scvi-tools](https://docs.scvi-tools.org/) | Single-cell data and modeling |
| Snakemake | [Snakemake docs](https://snakemake.readthedocs.io/) | Rules, DAG, software environments |
| Nextflow | [Nextflow docs](https://www.nextflow.io/docs/latest/) | Containerized and distributed workflows |
| Clinical reporting | [EQUATOR Network](https://www.equator-network.org/) and [TRIPOD](https://www.tripod-statement.org/) | Match reporting guideline to study design |
| Research data rights | [NIH Data Management and Sharing](https://sharing.nih.gov/) | Research data access and sharing controls |

The package/manual is authoritative for **present-day syntax**; original papers identify methodological motivation. An API's existence does not establish appropriate assumptions for a particular biomedical study.

[Return to matrix](BIOMEDICAL_CODING_LITERATURE_MATRIX.md).
