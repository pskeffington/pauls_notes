# End-to-end synthetic breast cancer study: frozen teaching protocol v1.0

[Parent design chapter](CANCER_STUDY_DESIGN.md) · [R cohort and analysis](../examples/breast_cancer_protocol_replay.R) · [R Markdown report](../examples/breast_cancer_protocol_report.Rmd) · [Verification](../tests/test_breast_cancer_protocol_replay.R)

**Status:** Educational, **synthetic-only** and prospectively specified relative to the simulation code. No human subjects, access to individual TCGA records, efficacy claims or prospective clinical enrollment are authorized by this protocol.

## Rationale and question

Among hypothetical adults with a **defined early breast cancer population** starting preoperative treatment, does random assignment to intervention B, compared with reference A, change the probability of **documented pathological complete response (pCR) by the prespecified surgery assessment window**? This is an invented teaching scenario, not a realistic efficacy estimate or validation of a specific drug.

### PICO and design

| Element | Frozen specification |
| --- | --- |
| Population | Synthetic eligible adults with breast cancer; no actual clinical inclusion/exclusion screening |
| Interventions | Arm A reference vs B hypothetical experimental regimen |
| Allocation | 1:1, complete random allocation within one synthetic cohort |
| Unit | One randomized participant, not cells or specimens |
| Primary endpoint | Binary **documented pCR** by assessment window; missing pCR assessment coded as no documented pCR under a *prespecified composite endpoint* |
| Estimand | Treatment-policy-style randomized-arm **difference in documented pCR probability**, B minus A, in all randomized participants |
| Intercurrent events | Assessment unavailable or no documented surgery/pCR by time window counts as failure for this teaching **composite**; this does not infer pathological nonresponse |
| Target effect | Planning p_A=.30 and p_B=.45 for *assessable outcomes*, difference .15 |
| Alpha / power | Two-sided alpha .05; 80% power for standard independent two-proportion approximation |
| Attrition planning | 10% anticipated endpoint unavailability; inflate approximate per-arm analyzable n by 1/(1-.10) |
| Primary analysis | Difference in observed **documented response** proportions B−A and an unpooled Wald 95% CI (educational large-sample approximation); two-sided independent two-proportion test with continuity correction disabled |
| Secondary checks | Fisher exact conditional test and a complete-case analysis explicitly labeled **sensitivity**, not substitute primary |
| Multiplicity | One primary hypothesis; secondary outcomes exploratory, no confirmatory claims |
| Random seed | 7122026; local RNG state preserved |
| Outcome simulation | Hypothetical Bernoulli p=.30/.45 followed by independent 10% unavailable-assessment indicator |
| Interpretation | Estimated documented-response contrast, NOT true biological pCR risk or causally demonstrated cancer treatment efficacy |

**Important planning caveat:** `power.prop.test()` targets **fully observed** pCR values at .30/.45; coding 10% unavailable as failures produces documented-response probabilities around .27/.405. The simple recruitment inflation is **not guaranteed** to recover 80% power for this composite estimand. Before an actual trial, recalculate power under the **composite endpoint** and credible missingness/intercurrent-event mechanisms, considering simulation and specialist review. Do not call the enrollment count clinically adequate.

## Data dictionary

| Column | Type | Allowed values / meaning |
| --- | --- | --- |
| patient_id | character unique key | SYN001...; never a numerical clinical variable |
| arm | factor | A reference, B intervention |
| latent_response | integer | 0/1 **simulation-only** underlying outcome; never treat as observed clinical field |
| assessment_available | integer | 0/1 synthetic assessment status |
| documented_response | integer | 1 only when available and latent_response=1; otherwise 0 under specified endpoint |
| measured_response | integer/NA | Observed response among assessable only; missing where assessment unavailable |
| biomarker | numeric | Synthetic arbitrary score; exploratory only |

The primary endpoint is `documented_response` with no missing values by construction. The assessed-only variable is `measured_response`; **do not convert its missingness away for a different estimand without declaring a rule**. Real protocol collection must record time, causes and deviations rather than assume the synthetic mechanism.

## Analysis, verification and reporting gates

1. Verify one row per person, exactly two arms, 1:1 allocation, unique IDs, 0/1 primary values and consistent missing counts.
2. Report randomized N, per-arm randomized n, per-arm assessed and unassessed counts, documented pCR numerator and denominator.
3. Calculate B−A risk difference; report the 95% CI and two-sided primary p-value, without interpreting p as probability of truth.
4. Display event proportions and uncertainty with denominators, primary contrast direction and a missingness summary. Report Fisher exact as sensitivity and assessed-only analysis as a different estimand.
5. State statistical assumptions, simulation process and why results do not imply biological truth or clinical effect. Run validation tests before claiming R output has been independently reproduced.

**Required review for any real study:** G0 citation validity; G1 permission; G2 unique keys, units and missingness; G3 time zero/estimand and randomization; G5 inference and interval suitability; G7 plot/label review; G8 independent computational replay. Governance and ethics approval remain separate.

## Reproduce

From repository root:

```bash
Rscript --vanilla 03_learning/tests/test_breast_cancer_protocol_replay.R
# Rendering requires rmarkdown + knitr and a working LaTeX installation for PDF.
Rscript -e 'rmarkdown::render("03_learning/examples/breast_cancer_protocol_report.Rmd", output_format="html_document")'
```

The code has to be executed with a real R installation before any numerical result can be marked validated. Source standards: [SPIRIT 2025](https://www.bmj.com/content/389/bmj-2024-081477), [CONSORT 2025](https://www.bmj.com/content/389/bmj-2024-081477), and [ICH E9(R1)](https://www.fda.gov/media/108698/download). Verify current versions for clinical use; protocol statements above are original teaching specifications.
