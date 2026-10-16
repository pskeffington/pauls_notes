# Manuscript and bibliography resources

[Resources](../README.md)

- [Bibliography guide](Bibliography_Guide.md)
- [Manuscript source](Example_APA_7_Manuscript.tex)
- [Manuscript references](Example_References.bib)
- [Reference entry examples](Example_Entry_Types.bib)
- [Build script](compile_manuscript.sh)

The bibliography examples contain fictional practice records. Replace them with accurate research references before use. The manuscript build needs a TeX distribution, Biber and the packages checked by the build script.

```bash
bash 06_RESOURCES/LaTeX/compile_manuscript.sh --output-dir /tmp/pauls-notes-manuscript
```

Choose a new output directory outside the repository, with an existing parent. The builder refuses to reuse a destination and publishes the PDF only after the LaTeX and Biber passes succeed. Temporary build files are cleaned automatically.

The entry catalogue is a bibliography reference, without a separate manuscript build. This template uses APA-style references; adapt the manuscript layout to the target journal or reporting requirements.
