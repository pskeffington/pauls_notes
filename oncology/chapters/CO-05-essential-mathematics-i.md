# CO-05 — Essential Mathematics I: Quantities, Rates, Units and Logarithms

*Computational Oncology: A Clinician–Scientist's Guide · Part I · Draft 0.1*  
[Book home](../README.md) · [Introduction](../INTRODUCTION.md) · [CO-04](CO-04-data-literacy.md) · [Roadmap](../ROADMAP.md) · [Citation policy](../evidence/README.md)

## Why mathematics belongs in oncology research

A clinical question becomes a research question when its quantities and comparisons are defined. The words *response*, *recurrence*, *higher*, and *faster* require a numerator, denominator, time frame, and unit before they can be interpreted. Mathematics lets us expose those choices rather than hide them in software.

For example, “24 new cancer diagnoses” is a **count**, not an incidence rate. A population denominator and observation interval are needed to construct a population rate, and a time-at-risk denominator is needed to construct a person-time rate. Even after those quantities are computed, selection and ascertainment can limit interpretation. [SEER's incidence-rate definitions](https://seer.cancer.gov/statistics/types/incidence.html) and the [CDC's frequency-measure discussion](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section1.html) make these distinctions explicit.

**Guiding question:** What can we calculate, and which conclusions does the calculation *not* authorize?

**Section references:** [SEER: Cancer Incidence Rates](https://seer.cancer.gov/statistics/types/incidence.html) · [CDC: Principles of Epidemiology, Frequency Measures](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section1.html)

## Learning objectives and starting assumptions

After completing the chapter, the learner should be able to:

1. Define a variable, unit, numerator, denominator, observation interval, and eligible population.
2. Rearrange a one-variable equation and check units and plausibility.
3. Distinguish ratios, proportions, percentages, percentage-point differences, risks, and rates.
4. Compute a population-based incidence rate and a person-time event rate without interchanging their denominators.
5. Convert units using dimensional analysis, retaining justified measurement precision.
6. Calculate powers, exponential changes, logarithms and log2 fold changes while checking their domains.
7. Interpret a standardized score without turning it into a clinical diagnostic threshold.
8. Reproduce calculations in **base R** and **Python standard library**, including deliberate invalid-input cases.

**Prerequisites:** CO-01 through CO-04 or equivalent clinical/data literacy. Familiarity with a calculator is enough; programming experience is not required. All numbers below are invented. No dose calculation, treatment choice or individual clinical prediction follows from this chapter.

**Section references:** [NIST: Unit Conversion](https://www.nist.gov/pml/owm/metric-si/unit-conversion) · [CDC: Principles of Epidemiology, Frequency Measures](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section1.html)

## 1. Variables, equations and rearrangement

A **variable** is a symbol whose value may change; a **constant** is fixed within the stated calculation. An equation asserts equality and can often be rearranged without changing its meaning. Start by writing the scientific definition, not by memorizing an isolated formula.

If $E$ denotes a number of events, $P$ denotes an eligible population count, and $K$ is a chosen scale factor, then a simple population rate is:

$$R = \frac{E}{P}\,K,\qquad P>0.$$

To solve for events, multiply both sides by $P/K$:

$$E = \frac{RP}{K}.$$

In an **invented one-year registry**, $P=80{,}000$, $R=30$ new cancers per 100,000 population in that year, and $K=100{,}000$. Therefore $E=30(80{,}000)/100{,}000=\mathbf{24}$ incident cancer records. The reverse check gives $24/80{,}000\times100{,}000=30$.

This algebra does not prove that ascertainment was complete or that the population denominator was appropriate. SEER cautions that incident cancer counts can include multiple primary cancers in one person and generally exclude recurrences.

**Error test:** A zero or negative population denominator invalidates the calculation; a negative event count is nonsensical. Units in $R$ must match the choice of $K$ and population definition.

**Section references:** [SEER: Cancer Incidence Rates](https://seer.cancer.gov/statistics/types/incidence.html) · [NIST: Unit Conversion](https://www.nist.gov/pml/owm/metric-si/unit-conversion)

## 2. Ratios, proportions and percentages

A **ratio** compares two quantities, such as 12 laboratory assays to 8 tissue specimens ($12:8=1.5$ assays per specimen). A **proportion** is a special ratio in which the numerator is a subset of the denominator and lies between 0 and 1. A **percentage** expresses that proportion per hundred.

Suppose 18 of 60 eligible people in invented Group A have a protocol-defined response. The descriptive response proportion is:

$$p_A=\frac{18}{60}=0.30=30\%.$$

The denominator is the number of eligible **people**, not the number of scans or biopsies. If Group B contains 12 responders out of 60 eligible people, then $p_B=12/60=0.20=20\%$. The bare number “18 responders” cannot support a meaningful proportion without knowing who was eligible, how response was defined, and whether response status was ascertained.

The CDC distinguishes ratios and proportions precisely; clinical response definitions should be obtained from the relevant protocol rather than inferred from arithmetic.

**Section references:** [CDC: Principles of Epidemiology, Frequency Measures](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section1.html) · [RECIST 1.1: Revised Response Evaluation Criteria (2009)](https://pubmed.ncbi.nlm.nih.gov/19097774/)

## 3. Absolute and relative comparisons

Different comparison scales answer different questions. For the invented two-group response example:

- **Absolute proportion difference:** $p_A-p_B=0.30-0.20=0.10$, or **10 percentage points**.
- **Relative proportion ratio:** $p_A/p_B=0.30/0.20=1.5$.
- **Relative increase from Group B:** $(p_A-p_B)/p_B =0.5$, or **50%**.

A 10-percentage-point difference is *not* a 10% relative increase. A ratio of 1.5 does *not* mean 1.5 additional people responded. If the reference proportion is zero, the ratio is undefined; the absolute difference may still be defined.

These are **descriptive summaries**: without study design, denominators, uncertainty, and potential bias, they do not demonstrate treatment effectiveness or causal benefit. If an outcome is not a one-time binary event under a specified observation window, a simple response proportion may be an inappropriate estimand.

**Section references:** [CDC: Principles of Epidemiology, Frequency Measures](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section1.html) · [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/)

## 4. Population rates, person-time rates and risk

A **population incidence rate** is commonly reported as new cancers in a defined year divided by an appropriate population size, scaled per 100,000 people. A **person-time rate** has accumulated time at risk in its denominator. A **fixed-horizon risk** is a probability/proportion over a defined interval for a defined eligible cohort; it is not interchangeable with either rate.

**Example A — registry (invented):** 24 new cancers among 80,000 eligible people observed at the population level in one year:

$$R_{\mathrm{pop}}=\frac{24}{80{,}000}\times100{,}000=30\quad\text{new cancers per 100,000 population during that year}.$$

**Example B — cohort follow-up (invented):** 12 first recurrences accrued over 600 *at-risk person-years* in a separate defined cohort:

$$\hat\lambda=\frac{12}{600}=0.02\text{ events/person-year}=20\text{ events/1,000 person-years}.$$

The two numerical examples describe different event types, populations and denominators; they cannot be compared as though they represented the same outcome. The second calculation is an observed event-density estimate, **not a 2% one-year recurrence probability**. The risk-set rules, event eligibility, censoring and competing events matter.

**Age adjustment:** Two populations can have different crude rates partly because their age structures differ. An age-adjusted rate is a weighted summary of age-specific rates using a standard population; it is not the observed crude event fraction. SEER describes the distinction and its role in comparisons.

**Section references:** [SEER: Cancer Incidence Rates](https://seer.cancer.gov/statistics/types/incidence.html) · [CDC: Principles of Epidemiology, Measures of Risk](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section2.html) · [SEER: Defining Cancer Statistics](https://seer.cancer.gov/statistics/types.html)

## 5. Units, conversion and measurement precision

A number without units is frequently unusable in oncology. A lesion dimension of “2.5” cannot be interpreted without knowing whether it is in millimeters or centimeters, how it was measured, and what its uncertainty is. **Dimensional analysis** multiplies by a conversion factor equal to 1 so units cancel:

$$2.5\ \mathrm{cm}\times\frac{10\ \mathrm{mm}}{1\ \mathrm{cm}}=25\ \mathrm{mm}.$$

A fictional analyte concentration of $0.8$ ng/mL converts to $800$ pg/mL, because $1$ ng = $1000$ pg. This converts **reported units**, not assay meaning or clinical reference intervals.

Unit conversion does not create additional measurement precision. Keep full precision internally, use exact factors when available, and round the final reported result to a defensible level. [NIST's unit-conversion guidance](https://www.nist.gov/pml/owm/metric-si/unit-conversion) explicitly recommends checking unit cancellation, plausibility and rounding only at the end.

**Safety boundary:** These are measurement demonstrations, not medication dosing instructions or validated medical device calculations. A real laboratory conversion must verify analyte identity and any method-specific conversion factor.

**Section references:** [NIST: Unit Conversion](https://www.nist.gov/pml/owm/metric-si/unit-conversion) · [NIST: Writing with SI Units](https://www.nist.gov/pml/owm/writing-si-metric-system-units)

## 6. Powers, exponentials and logarithms

A **power** represents repeated multiplication: $2^3=8$. A **logarithm** reverses a power: $\log_2 8=3$, because $2^3=8$. Common bases are 2, 10 and the natural base $e$:

$$\log_b(x)=y\quad\Longleftrightarrow\quad b^y=x,\quad x>0,\ b>0,\ b\ne 1.$$

Useful identities include:

$$\log_b(ab)=\log_b a+\log_b b,\qquad
\log_b(a/b)=\log_b a-\log_b b,\quad a,b>0.$$

The distinction between bases matters. In R, `log(x)` is the natural logarithm, `log2(x)` has base 2, and `log10(x)` has base 10. Python's `math.log` is natural by default; `math.log2` is base 2.

**Domain check:** $\log_2 0$ and $\log_2(-1)$ are not real-valued finite calculations. Never silently substitute an arbitrary pseudocount for zero expression values without explaining how it changes the estimand. The mathematics is general; the choice of biological transformation is method-specific.

**Section references:** [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/) · [Love et al., DESeq2 (2014)](https://doi.org/10.1186/s13059-014-0550-8)

## 7. Log2 fold change for molecular measurements

In a **fictional expression comparison**, suppose valid, comparable normalized group summaries are 80 and 20 arbitrary abundance units. The ratio is $80/20=4$ and:

$$\log_2\left(\frac{80}{20}\right)=\log_2 4=\mathbf{+2}.$$

Reversing the group order gives $\log_2(20/80)=\mathbf{-2}$. The sign reports direction relative to the chosen reference. A log2 change of +1 corresponds to a twofold ratio, and -1 to a half-as-large ratio. Neither is a probability or a significance test.

**Crucial assay caveat:** Raw RNA-seq counts, TPM, FPKM and transformed values are not interchangeable. This arithmetic illustration is **not** a differential-expression analysis. A defensible analysis must document sample independence, normalization, biological replication, dispersion or variance, model specification and multiplicity. The GDC documents RNA-seq outputs, and DESeq2 describes a model-based count-analysis approach. Neither authorizes interpreting this two-number exercise as gene significance.

**Section references:** [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/) · [Love et al., DESeq2 (2014)](https://doi.org/10.1186/s13059-014-0550-8)

## 8. Exponential models: useful mathematics, limited biology

An idealized quantity that doubles at a constant interval $T_d$ follows:

$$N(t)=N_0 2^{t/T_d}=N_0 e^{kt},\quad k=\frac{\ln 2}{T_d}.$$

For **invented abstract units**, set $N_0=100$, $T_d=30$ days and $t=60$ days. Then $N(60)=100\times2^2=\mathbf{400}$ units. The equivalent continuous-rate parameter is $k=\ln(2)/30\approx0.0231$ per day.

This is a mathematical model, **not a clinically defensible tumor-growth forecast**. Real cancers can show heterogeneous dynamics, treatment effects, changing growth patterns and measurement limitations. A doubling interval would need to be inferred from appropriately timed and measured observations and its uncertainty evaluated. Do not derive a patient's prognosis from this fictional curve.

The biological caution follows the changing, heterogeneous nature of cancer and should be revisited in subsequent regression, longitudinal modeling and imaging chapters.

**Section references:** [What Is Cancer?](https://www.cancer.gov/about-cancer/understanding/what-is-cancer) · [Hallmarks of Cancer: New Dimensions (2022)](https://doi.org/10.1158/2159-8290.CD-21-1059)

## 9. Standardized values without diagnostic overreach

A standardized score expresses a value relative to a selected mean and standard deviation:

$$z=\frac{x-\mu}{\sigma},\qquad \sigma>0.$$

For an invented laboratory score with $x=75$, reference mean $\mu=60$ and reference standard deviation $\sigma=10$, the calculated score is $z=1.5$. It is **dimensionless**: measurement units cancel in numerator and denominator.

A $z$ score is not automatically a clinical cutoff or evidence of disease. It depends on the reference population, distribution, measurement method and whether mean/standard deviation summarize the intended target. Scaling an assay can also leak information into a predictive model if its parameters are estimated using held-out specimens instead of the development data.

For expression matrices and multi-feature modeling, see the [existing visual ML guide](../../04_machine_learning/visual-data-guide.md), which emphasizes fitting preparation only inside the appropriate training partition.

**Section references:** [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/) · [Kapoor and Narayanan: Data Leakage (2023)](https://doi.org/10.1016/j.patter.2023.100804)

## 10. Integrated worked case: three incompatible denominators

A fictional oncology research program reports three pieces of information:

| Question | Numerator | Denominator | Correct arithmetic |
| --- | ---: | ---: | --- |
| How many new cancers per 100,000 population in one year? | 24 diagnoses | 80,000 eligible population | 30 per 100,000 population in that year |
| What was the observed first-recurrence rate during follow-up? | 12 events | 600 at-risk person-years | 20 per 1,000 person-years |
| What fraction of people in a separate response cohort met a response definition? | 18 responders | 60 eligible people | 30% |

The calculations are numerically straightforward. Their **scientific interpretations differ**: new cancer incidence, event density during follow-up, and a descriptive proportion of eligible responders are not interchangeable quantities. This is why every analysis record must include the endpoint, unit, numerator, denominator, source, ascertainment period and relevant sampling restrictions.

Before drawing any comparison, the investigator should ask whether the underlying cases, time frames, endpoint definitions and eligible populations align. Even precise arithmetic cannot resolve a biased study design.

**Section references:** [SEER: Cancer Incidence Rates](https://seer.cancer.gov/statistics/types/incidence.html) · [CDC: Principles of Epidemiology, Measures of Risk](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section2.html) · [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/)

## 11. Reproducible exercises in Python and R

Two independent, dependency-light teaching implementations accompany the chapter:

- [Python lab: oncology_math.py](../examples/oncology_math.py), using Python's standard library and explicit invalid-input guards.
- [R lab: oncology_math.R](../examples/oncology_math.R), using base R and independent assertions.
- [Python regression tests](../../scripts/test_oncology_math.py), including expected results and deliberate failure cases.

Run from the repository root:

```bash
python3 oncology/examples/oncology_math.py
python3 -m unittest discover -s scripts -p 'test_oncology_math.py' -v
Rscript --vanilla oncology/examples/oncology_math.R
```

The labs compute exact fixture expectations, print named outputs, verify reverse calculations and reject invalid denominators or nonpositive log arguments. They use **invented counts and concentrations only**; neither script fits a clinical model, accesses research records, or produces a treatment recommendation. Python and R are separate implementations; agreement adds confidence in arithmetic, not biological validation.

**Section references:** [NIST: Unit Conversion](https://www.nist.gov/pml/owm/metric-si/unit-conversion) · [CDC: Principles of Epidemiology, Frequency Measures](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section1.html) · [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/)

## 12. Original mastery exercises

Work each question on paper, state its *unit*, and then reproduce it in either lab.

1. **Algebra.** If the rate is 45 per 100,000 and the population denominator is 40,000 for a defined year, how many events does the formula imply?
2. **Proportion.** A hypothetical response cohort contains 21 responders among 70 eligible patients. Express the result as a fraction, decimal and percent.
3. **Percentage points.** If another cohort has 14 responders among 70, calculate the absolute percentage-point difference and the ratio of response proportions. State one reason not to interpret the difference causally.
4. **Person-time.** Eight first events occur over 320 person-years. Report events per 1,000 person-years and explain why the answer is not necessarily a one-year risk.
5. **Conversion.** Convert an invented measured lesion length of 1.8 cm into mm. Preserve appropriate reporting precision.
6. **Log2.** Group A and Group B have fictional comparable expression summaries of 48 and 12. Compute $\log_2(A/B)$ and the reverse. Why might raw RNA-seq reads require a different procedure?
7. **Exponential.** For an idealized, nonclinical quantity of 50 units doubling every 20 days, what is the value after 60 days?
8. **Standardization.** A result is 120 units, with a chosen reference mean of 100 and SD of 25. Compute $z$. Why is this not sufficient for diagnosis?
9. **Negative cases.** Explain why dividing by zero, a log of zero, and a negative event count must not be treated as ordinary numeric outputs.
10. **Critical reasoning.** A paper compares 30 new diagnoses per 100,000 population with 20 recurrences per 1,000 person-years and concludes recurrence incidence is lower. Identify at least three scientific flaws in the comparison.

**Section references:** [CDC: Principles of Epidemiology, Frequency Measures](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section1.html) · [NIST: Unit Conversion](https://www.nist.gov/pml/owm/metric-si/unit-conversion) · [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/)

## 13. Answer key, interpretation and common failures

1. $E=45\times40{,}000/100{,}000=\mathbf{18}$ implied events; the numerator and denominator must describe the same population and period.
2. $21/70=0.30=\mathbf{30\%}$.
3. $14/70=0.20$, so the difference is **10 percentage points** and $0.30/0.20=\mathbf{1.5}$. Without a valid comparative design, these are descriptive associations.
4. $8/320\times1{,}000=\mathbf{25}$ events per 1,000 person-years; time at risk rather than one-time eligible people is the denominator.
5. $1.8\text{ cm}\times 10=\mathbf{18\text{ mm}}$; do not invent more precise measurement digits.
6. $\log_2(48/12)=\mathbf{+2}$, reverse $\mathbf{-2}$. Raw counts require normalization and a justified inferential model.
7. $50\times2^{60/20}=50\times8=\mathbf{400}$ abstract units; not a tumor prediction.
8. $(120-100)/25=\mathbf{0.8}$; interpretation requires an appropriate reference population and validated clinical purpose.
9. Zero denominators are undefined, $\log(0)$ is outside the finite real-log domain, and negative event counts contradict the study variable's definition.
10. The compared **events** differ (new diagnoses vs recurrences), denominators differ (population vs person-time), and populations, time windows, eligibility and ascertainment may differ. Numerical magnitudes cannot be compared without a shared estimand.

**Frequent errors:** treating percentage points as relative percentages, calling a person-time rate a probability, using an assay fold change as a test statistic, converting units without preserving their meaning, and interpreting an idealized growth model as clinical prediction.

**Section references:** [CDC: Principles of Epidemiology, Frequency Measures](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section1.html) · [CDC: Principles of Epidemiology, Measures of Risk](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section2.html) · [Love et al., DESeq2 (2014)](https://doi.org/10.1186/s13059-014-0550-8)

## 14. Evidence boundaries and progression

**Evidence scope:** The external links in this chapter support definitions and methodological cautions; the numerical examples are independently invented arithmetic fixtures, not findings from a clinical dataset. Section links are part of the book's citation audit but do not constitute independent peer review.

The next chapter, **CO-06: Essential Mathematics II**, should introduce derivatives, gradients, linear algebra, matrix orientation and numerical optimization, then return to regression and gene-expression feature matrices. Readers who cannot yet explain denominators and logarithmic transforms should repeat the practice cases before progressing.

**Further reading:** [SEER incidence-rate definitions](https://seer.cancer.gov/statistics/types/incidence.html), [CDC frequency measures](https://archive.cdc.gov/www_cdc_gov/csels/dsepd/ss1978/lesson3/section1.html), [NIST conversion guidance](https://www.nist.gov/pml/owm/metric-si/unit-conversion), [GDC RNA-seq outputs](https://docs.gdc.cancer.gov/Encyclopedia/pages/RNA-Seq/), and [the complete textbook roadmap](../ROADMAP.md).

**Manuscript status:** Draft 0.1; numerical verification and claim-level scientific review are separate release gates.

**Section references:** [SEER: Cancer Incidence Rates](https://seer.cancer.gov/statistics/types/incidence.html) · [NIST: Unit Conversion](https://www.nist.gov/pml/owm/metric-si/unit-conversion) · [GDC mRNA Analysis Pipeline](https://docs.gdc.cancer.gov/Data/Bioinformatics_Pipelines/Expression_mRNA_Pipeline/)

