# CO-07 verification record — 2026-11-21

**Component:** [CO-07 — Randomness and Probability](../chapters/CO-07-randomness-and-probability.md).

**Scope:** Original teaching prose, probability identities, expected counts, synthetic simulation and input validation. The manuscript remains a draft; this record establishes bounded technical and editorial evidence.

## Source and example boundaries

The chapter uses a constructed 80-record marker/response table and a separate hypothetical screening model. Neither is an empirical cancer dataset. The screening assumptions are prevalence 0.01 or 0.05, sensitivity 0.90 and specificity 0.95; the 10,000-person tables contain mathematical expectations.

The existing OpenStax probability sources, NCI screening overview, Python random documentation and R random-number documentation were inspected for the chapter's definitions and implementation statements. FDA's final 2007 diagnostic-test guidance and the primary STARD 2015 article support the discussion of reference standards, participant selection and applicability. Titles, URLs and claim scope are retained in the [source registry](source-registry.json), and all 16 H2 sections are mapped in the [section citation record](section-citations.json).

An independent AI reviewer checked the manuscript's conditioning directions, event algebra, Bayes derivation, expected versus simulated counts, assumptions and nine exercise answers against independent rational arithmetic. FDA/STARD links and a display-rounding explanation were added in response. External statistical and clinical expert review remains pending.

## Independent numerical reference

Python's standard-library `Fraction` arithmetic reconstructed the tables without using the floating-point results as reference values. The existing regression suite also carries these exact fractions.

| Quantity | Independent reference |
| --- | --- |
| Event given marker in the constructed roster | $8/20=2/5=0.40$ |
| Marker given event | $8/16=1/2=0.50$ |
| Marker or event | $(20+16-8)/80=7/20=0.35$ |
| Expected cells at prevalence 0.01: TP, FP, FN, TN | 90; 495; 10; 9,405 |
| PPV / NPV at prevalence 0.01 | $2/13$ / $1881/1883$ |
| Expected cells at prevalence 0.05: TP, FP, FN, TN | 450; 475; 50; 9,025 |
| PPV / NPV at prevalence 0.05 | $18/37$ / $361/363$ |

The Python seed-711 realization contains TP 90, FP 487, FN 14 and TN 9,409. Those generated counts illustrate one draw; they are distinct from the expected-count references. R and Python share deterministic probability identities but do not promise identical random streams.

## Executed code and source identity

The following source versions passed in [machine-index CI run 44898310988](https://github.com/pskeffington/pauls_notes/actions/runs/44898310988), job `136828611540`, on commit `6316e6002063e6196e30f5c07fca0fef939c3ac6`. A corresponding [push run](https://github.com/pskeffington/pauls_notes/actions/runs/44898307307) also passed.

| File | Git blob SHA at the executed revision |
| --- | --- |
| [Python probability lab](../examples/oncology_probability.py) | `311796ec2dfa6d88112ddd0af2037b26662be7ae` |
| [Base-R probability lab](../examples/oncology_probability.R) | `23874e040c9313a70c5defda04097a432a0a1617` |
| [Python probability tests](../../scripts/test_oncology_probability.py) | `637ff05f116006f553186788a992c719f1eb3833` |

```bash
python3 oncology/examples/oncology_probability.py
python3 -m unittest discover -s scripts -p 'test_oncology_probability.py' -v
Rscript --vanilla oncology/examples/oncology_probability.R
```

**Observed:** all eight Python test methods passed; the base-R script completed its arithmetic and negative-input checks and printed `CO-07 R fixtures and negative-input checks passed`. CI reported Python **3.12.3** and R **4.3.3**. Local Python **3.12.14** also passed the eight tests. R was unavailable locally; its execution evidence is the observed CI result.

The acceptance checks cover both expected-count tables, conditioning direction, valid boundary probabilities, invalid intersections, undefined denominators and seeded replay. Corrections made in this pass reject nonscalar/logical R table cells before coercion, prevent integer-storage overflow in valid count sums, reject nonfinite denominator sums, allow machine-scale roundoff at a valid union boundary, preserve very small positive expected counts, and reject unrepresentable R seeds before integer conversion. The seed-711 generator and principal teaching assumptions are unchanged.

## Status and remaining acceptance

| Evidence category | Status and limit |
| --- | --- |
| Original manuscript | Substantive draft present with worked explanations and nine reasoned exercises |
| Source inspection | Claim-scoped sources inspected; section mappings recorded |
| Independent arithmetic | Exact rational reference values agree with implementation results |
| Python and base-R execution | Passed for the source blobs and CI runs identified above |
| Independent editorial/method review | AI review completed; findings resolved |
| Chapter export and visual acceptance | No complete chapter export or page-by-page visual acceptance recorded |
| Expert scientific review | Independent statistical and clinical specialist review pending |
| Publication | Chapter remains `draft`; not `reviewed` or `released` |

The [existing draft PR](https://github.com/pskeffington/pauls_notes/pull/42) records CI results for the later integrated manuscript head. A change to one of the code blobs above requires a fresh execution record; earlier success does not transfer automatically to changed code.
