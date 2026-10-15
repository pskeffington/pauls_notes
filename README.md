# Paul's Notes

## Biomedical research documentation and resource guide

Authored by Paul Skeffington · Compiled with OpenAI

A working reference for planning biomedical studies, understanding molecular data, writing reproducible analysis code, and communicating results. Start with the research workflow or open a subject guide directly.

## Start here

| Research task | Guide |
| --- | --- |
| Plan a study and organize its analysis | [Research workflow](docs/research-workflow.md) |
| Find documentation, methods and reusable code | [Resource guide](docs/resource-guide.md) |
| Practice the biomedical computing workflow | [Learning sections and runnable case](03_learning/README.md) |
| Learn command-line research computing | [Unix and Bash](01_unix_bash/README.md) |
| Connect biomedical literature to coding practice | [Biomedical coding and literature](02_biomedical_coding/README.md) |
| Read the breast cancer book | [Breast Cancer Research Guide — People, Data, Biology and 60 Genes](06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md) |
| Look up gene functions, assays and evidence | [Genomics and gene atlas](06_RESOURCES/Genomics/README.md) |
| Build plots and summarize data in R | [R tools](06_RESOURCES/R/README.md) |
| Prepare a manuscript and bibliography | [Writing resources](06_RESOURCES/LaTeX/README.md) |

## Working materials

Use the [study protocol](templates/study-protocol.md), [data dictionary](templates/data-dictionary.md), and [analysis record](templates/analysis-record.md) to connect the research question, input definitions, analysis decisions and reported outputs.

The [resource collection](06_RESOURCES/README.md) brings together Bash, R, genomics, visualization, literature and manuscript tools. The literature section includes 71 publications and 36 documentation resources, with implementation checks and method-specific limits.

## Run the checks

From the repository root:

```bash
bash 01_unix_bash/tests/test_summarize_metadata.sh
python3 02_biomedical_coding/tests/test_literature_matrix.py
python3 scripts/check_documentation.py
```

For R prerequisites and individual checks, see [R tools](06_RESOURCES/R/README.md). Repository reuse terms are in [LICENSE](LICENSE).
