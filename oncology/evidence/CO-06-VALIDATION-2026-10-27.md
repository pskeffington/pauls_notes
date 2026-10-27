# CO-06 verification record — 2026-10-27

**Component:** [CO-06 — Essential Mathematics II](../chapters/CO-06-essential-mathematics-ii.md)  
**Nature of record:** Technical / mathematical audit of a synthetic teaching example, **not** clinical research validation, peer review or proof of publication readiness.

## Repository evidence checked

- The [Python laboratory](../examples/oncology_calculus.py) was reconstructed in an isolated local environment and its `git hash-object` blob ID matched the fetched GitHub blob: `b2a5c7d2c3cc0377a5843abfbd2e42f6b22fd831`.
- The [Python regression test module](../../scripts/test_oncology_calculus.py) was independently reconstructed and its Git blob ID matched the fetched GitHub blob: `f64b0fb41125f55e0963037a185ece1d9f83c213`.
- This identity check ensures the locally executed source and tests had the same bytes as the two GitHub files at inspection, rather than testing only a paraphrase of their algorithms.
- Python interpreter used for the independent local run: **Python 3.13.5**.

## Executed verification

```bash
python3 -m py_compile oncology/examples/oncology_calculus.py
python3 oncology/examples/oncology_calculus.py
python3 -m unittest discover -s scripts -p 'test_oncology_calculus.py' -v
```

**Result:** Python compilation completed successfully. The synthetic fixture printed expected quantities. All **5 test methods passed**, including positive numerical reference values, analytic-to-numeric gradient agreement, gradient descent versus closed-form coefficients, dimension/finite-value checks, and deliberately invalid inputs.

## Numerically replayed benchmark

| Quantity | Expected | Verified |
| --- | ---: | --- |
| Average change over stated interval | 2 | 2 |
| Analytic derivative of `t^2` at `t=3` | 6 | 6 |
| Three-component dot product | 32 | 32 |
| OLS intercept (invented data) | 1.1 | 1.1 |
| OLS slope (invented data) | 1.1 | 1.1 |
| Half-mean-squared error | 0.0875 | 0.0875 |
| Initial intercept/slope gradient | (-2.75, -5.5) | matched |
| Gradient descent (2000 steps, rate 0.1) | approximately (1.1, 1.1) | matched |
| Logistic value at zero | 0.5 | 0.5 |
| Logistic derivative at zero | 0.25 | 0.25 |
| Invented trapezoidal area | 5 index-unit weeks | 5 |

These are arithmetic teaching fixtures, not estimates from cancer patients.

## Repository navigation and evidence integrity

A read-back of the live repository's JSON manifests, evidence registers and seven manuscript documents established at this pass:
- 60 sequential chapter identifiers, six chapters marked `draft`;
- seven citation-mapped manuscript documents (introduction plus CO-01 through CO-06);
- 93 H2/H3 source-linked sections, 194 section/source assignments;
- 36 source entries in the linked bibliography;
- no missing source IDs, unmapped headings, or missing draft-to-citation records detected by the independent structural check;
- CO-06 Python and R test steps present in the versioned GitHub Actions YAML.

**Interpretation:** Structural checks verify navigability and source link accounting only. They cannot establish that every clinical claim is faithfully supported by each cited work; a qualified reviewer must still complete that assessment.

## Remaining gates

1. **R runtime:** `Rscript` was not available in the independent local execution environment. The committed base-R laboratory includes assertions and negative-case tests, and is configured in CI, but **its live execution is not confirmed here**.
2. **GitHub Actions:** No successful workflow run was independently verified through the available status interfaces. Pending checks must not be represented as passing.
3. **Scholarly review:** Claims, source versions, pedagogical effectiveness, accessibility, and clinical interpretation still require separate independent review.
4. **Broader validation:** This small regression fixture does not test a real oncology cohort, causal identification, external prediction performance, patient benefit, or clinical applicability.

**Chapter release status remains `draft`.** Technical success cannot automatically promote a manuscript to `reviewed` or `released`.
