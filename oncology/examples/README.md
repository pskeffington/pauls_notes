# Computational Oncology — Executable Teaching Labs

[Book home](../README.md) · [Chapter map](../ROADMAP.md) · [Source register](../evidence/SOURCES.md)

Every script in this folder operates on invented data only. Running a script is **not a clinical validation**, and these examples must not ingest patient-level or controlled-access records.

| Learning chapter | Language | Executable file | Checks |
| --- | --- | --- | --- |
| [CO-04: Data Literacy](../chapters/CO-04-data-literacy.md) | Python (stdlib) | [observation_grain.py](observation_grain.py) | Distinct people, specimen keys, valid splits and denominators |
| [CO-05: Essential Mathematics I](../chapters/CO-05-essential-mathematics-i.md) | Python (stdlib) | [oncology_math.py](oncology_math.py) | [Numerical and negative-case tests](../../scripts/test_oncology_math.py) |
| [CO-05: Essential Mathematics I](../chapters/CO-05-essential-mathematics-i.md) | Base R | [oncology_math.R](oncology_math.R) | Built-in assertions, including invalid input cases |
| [CO-06: Essential Mathematics II](../chapters/CO-06-essential-mathematics-ii.md) | Python (stdlib) | [oncology_calculus.py](oncology_calculus.py) | [Gradient, regression and negative tests](../../scripts/test_oncology_calculus.py) |
| [CO-06: Essential Mathematics II](../chapters/CO-06-essential-mathematics-ii.md) | Base R | [oncology_calculus.R](oncology_calculus.R) | QR regression and gradient numerical assertions |

From the repository root:

```bash
python3 oncology/examples/observation_grain.py
python3 oncology/examples/oncology_math.py
python3 -m unittest discover -s scripts -p 'test_oncology_math.py' -v
Rscript --vanilla oncology/examples/oncology_math.R
python3 oncology/examples/oncology_calculus.py
python3 -m unittest discover -s scripts -p 'test_oncology_calculus.py' -v
Rscript --vanilla oncology/examples/oncology_calculus.R
```

The CO-05 mathematical examples deliberately use **different** populations and endpoints for cancer incidence, recurrence person-time and treatment response. A shared numeric scale does not make those quantities comparable. All outputs must be interpreted together with the numerator, denominator, time frame, unit and source. Source definitions appear in the [CO-05 section references](../chapters/CO-05-essential-mathematics-i.md) and [evidence register](../evidence/source-registry.json).

**Current verification state:** The CO-06 [Python test source and lab](../evidence/CO-06-VALIDATION-2026-10-27.md) were replayed locally with matching Git blob hashes and all 5 test methods passed. R runtime execution and a successful CI run are not independently verified; no technical check alone establishes scientific or clinical review.
