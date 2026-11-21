# Computational Oncology — Executable Teaching Labs

[Book home](../README.md) · [Chapter map](../ROADMAP.md) · [Source register](../evidence/SOURCES.md)

Every script in this folder operates on invented data only. Running a script is **not a clinical validation**, and these examples must not ingest patient-level or controlled-access records.

| Learning chapter | Language | Executable file | Checks |
| --- | --- | --- | --- |
| [CO-04: Data Literacy](../chapters/CO-04-data-literacy.md) | Python (stdlib) | [observation_grain.py](observation_grain.py) | Distinct people, specimen keys, valid splits, join multiplicity, unmatched records and baseline selection; run `--check` |
| [CO-05: Essential Mathematics I](../chapters/CO-05-essential-mathematics-i.md) | Python (stdlib) | [oncology_math.py](oncology_math.py) | [Numerical and negative-case tests](../../scripts/test_oncology_math.py) |
| [CO-05: Essential Mathematics I](../chapters/CO-05-essential-mathematics-i.md) | Base R | [oncology_math.R](oncology_math.R) | Built-in assertions, including invalid input cases |
| [CO-06: Essential Mathematics II](../chapters/CO-06-essential-mathematics-ii.md) | Python (stdlib) | [oncology_calculus.py](oncology_calculus.py) | [Gradient, regression and negative tests](../../scripts/test_oncology_calculus.py) |
| [CO-06: Essential Mathematics II](../chapters/CO-06-essential-mathematics-ii.md) | Base R | [oncology_calculus.R](oncology_calculus.R) | QR regression and gradient numerical assertions |
| [CO-07: Randomness and Probability](../chapters/CO-07-randomness-and-probability.md) | Python (stdlib) | [oncology_probability.py](oncology_probability.py) | [Eight probability, precision and invalid-input tests](../../scripts/test_oncology_probability.py) |
| [CO-07: Randomness and Probability](../chapters/CO-07-randomness-and-probability.md) | Base R | [oncology_probability.R](oncology_probability.R) | Embedded expected-table, boundary, input and seeded-replay assertions |

From the repository root:

```bash
python3 oncology/examples/observation_grain.py
python3 oncology/examples/observation_grain.py --join-demo
python3 oncology/examples/observation_grain.py --check
python3 oncology/examples/oncology_math.py
python3 -m unittest discover -s scripts -p 'test_oncology_math.py' -v
Rscript --vanilla oncology/examples/oncology_math.R
python3 oncology/examples/oncology_calculus.py
python3 -m unittest discover -s scripts -p 'test_oncology_calculus.py' -v
Rscript --vanilla oncology/examples/oncology_calculus.R
python3 oncology/examples/oncology_probability.py
python3 -m unittest discover -s scripts -p 'test_oncology_probability.py' -v
Rscript --vanilla oncology/examples/oncology_probability.R
```

The CO-05 mathematical examples deliberately use **different** populations and endpoints for cancer incidence, recurrence person-time and treatment response. A shared numeric scale does not make those quantities comparable. All outputs must be interpreted together with the numerator, denominator, time frame, unit and source. Source definitions appear in the [CO-05 section references](../chapters/CO-05-essential-mathematics-i.md) and [evidence register](../evidence/source-registry.json).

**Verification records:** The [CO-06 record](../evidence/CO-06-VALIDATION-2026-10-27.md) preserves its October Python replay and review scope. The [CO-07 record](../evidence/CO-07-VALIDATION-2026-11-21.md) identifies the source blobs and observed Python/base-R CI run from November 21. The [current draft PR](https://github.com/pskeffington/pauls_notes/pull/42) records subsequent integrated runs. Technical execution and independent scientific review are separate evidence categories.

The CO-04 join exercise preserves nine specimen rows and all six roster members under its explicit fixture key; a deliberately incorrect person-only inner join produces 16 rows and loses one person. CO-07 compares exact probability identities and expected tables across implementations; a common seed does not imply identical R/Python simulated cohorts.
