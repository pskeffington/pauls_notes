# CO-07 — Randomness and Probability: From Events to Screening Results

*Computational Oncology: A Clinician–Scientist's Guide · Part II · Draft 0.1*

[Book home](../README.md) · [CO-06: Essential mathematics II](CO-06-essential-mathematics-ii.md) · [Roadmap](../ROADMAP.md) · [Python laboratory](../examples/oncology_probability.py) · [R laboratory](../examples/oncology_probability.R) · [Citation policy](../evidence/README.md)

## Why probability belongs in a breast cancer investigation

A research question often contains a conditional statement before it contains a statistical model: response *among* people with a marker, a positive result *among* people with a target condition, or the target condition *among* people with a positive result. These statements have different denominators. Probability notation makes those differences explicit.

The [NCI screening overview](https://www.cancer.gov/about-cancer/screening/hp-screening-overview-pdq) distinguishes sensitivity, specificity and predictive values by their conditioning groups. A test's ability to produce a positive result when the target condition is present does not by itself supply the probability of the condition after a positive result. The latter calculation also depends on how common the condition is in the population being considered.

This chapter develops that reasoning from a constructed breast cancer research roster and a separate hypothetical screening model. The roster counts, model parameters and expected screening counts are invented teaching inputs. They are not clinical accuracy estimates, observed study participants or breast cancer prevalence measurements.

**Guiding question:** Which event is being calculated, what information is given, and which population or model supplies the denominator?

**Section references:** [OpenStax: Probability Theory and Bayes' Theorem](https://openstax.org/books/principles-data-science/pages/3-4-probability-theory) · [NCI PDQ: Cancer Screening Overview for Health Professionals](https://www.cancer.gov/about-cancer/screening/hp-screening-overview-pdq)

## Learning objectives and prerequisites

After completing the chapter, the reader should be able to:

1. Define a random experiment, sample space, event, intersection, union and complement.
2. Calculate conditional probabilities while preserving the direction of conditioning.
3. Distinguish mutually exclusive events from independent events.
4. Derive the total-probability rule and Bayes' theorem from disjoint groups and a common joint probability.
5. Translate prevalence, sensitivity and specificity into a four-cell table of expected counts.
6. Explain why changing a prevalence assumption can change predictive values while the assumed test characteristics remain fixed.
7. Separate an exact model calculation, a simulated realization and an estimate from observed data.
8. Use the existing R and Python laboratory to check arithmetic, reproducibility and undefined conditioning cases.

**Prerequisites:** fractions, proportions and algebra from [CO-05](CO-05-essential-mathematics-i.md); the distinction between a mathematical model and its numerical implementation developed in [CO-06](CO-06-essential-mathematics-ii.md). The chapter introduces its probability notation before using it.

**Section references:** [OpenStax: Introductory Statistics Probability Terminology](https://openstax.org/books/introductory-statistics-2e/pages/3-key-terms) · [OpenStax: Probability Theory and Bayes' Theorem](https://openstax.org/books/principles-data-science/pages/3-4-probability-theory)

## 1. Define the experiment before the probability

A **random experiment** specifies what is selected or generated. Its **sample space**, denoted by $\Omega$, contains the possible outcomes. An **event** is a set of those outcomes. The probability $\Pr(A)$ assigns a number between 0 and 1 to an event $A$ under the stated experiment.

For the first example, construct a roster of 80 fictional participants in a breast cancer research exercise. Every record has a baseline marker label and a binary response-event label at the same hypothetical assessment point. Define the experiment as selecting **one of these 80 records with equal probability**. Each labeled record therefore has probability $1/80$ of selection.

Let $M$ mean that the selected record is marker-positive, and let $E$ mean that its response event is present. Their complements, $M^c$ and $E^c$, mean marker-negative and response-event absent. The superscript $c$ denotes the complement; it is not a power.

| Constructed marker category | Event present, $E$ | Event absent, $E^c$ | Row total |
| --- | ---: | ---: | ---: |
| Marker-positive, $M$ | 8 | 12 | 20 |
| Marker-negative, $M^c$ | 8 | 52 | 60 |
| Column total | 16 | 64 | 80 |

All four cells and their margins are stipulated. Consequently,

$$
\Pr(M)=\frac{20}{80}=0.25,\qquad
\Pr(E)=\frac{16}{80}=0.20,\qquad
\Pr(M\cap E)=\frac{8}{80}=0.10.
$$

The intersection symbol $\cap$ means that both conditions hold for the same selected record. These are exact probabilities for uniform selection from this constructed roster. If an analogous table were obtained from a sample of actual participants, its proportions would instead be estimates of quantities in a separately defined target population; sampling design and uncertainty would then matter.

**Section references:** [OpenStax: Introductory Statistics Probability Terminology](https://openstax.org/books/introductory-statistics-2e/pages/3-key-terms)

## 2. Combine events without counting the intersection twice

The union $M\cup E$ includes records that are marker-positive, event-positive, or both. Adding the two marginal counts counts the eight records in their intersection twice. Subtracting the intersection once gives the addition rule:

$$
\Pr(M\cup E)
=\Pr(M)+\Pr(E)-\Pr(M\cap E)
=0.25+0.20-0.10
=0.35.
$$

The same calculation on the table is $(20+16-8)/80=28/80$. The 28 qualifying records comprise eight in both categories, 12 with the marker alone and eight with the event alone.

The complement of the union contains records with neither condition:

$$
\Pr\{(M\cup E)^c\}=1-\Pr(M\cup E)=0.65=\frac{52}{80}.
$$

This check connects an equation to an identifiable table cell. It also prevents a common language error: “either” must be defined. Inclusive “or” uses the union; “one or the other, but not both” excludes the intersection and would give $(12+8)/80=0.25$ in this example.

The intersection cannot be chosen independently of the margins. For any two events $A$ and $B$,

$$
\max\{0,\Pr(A)+\Pr(B)-1\}
\leq \Pr(A\cap B)
\leq \min\{\Pr(A),\Pr(B)\}.
$$

The upper bound follows because the intersection is contained in each event. The lower bound follows because the union cannot exceed probability 1. The existing laboratory checks these compatibility constraints before returning a union.

**Section references:** [OpenStax: Two Basic Rules of Probability](https://openstax.org/books/introductory-statistics/pages/3-3-two-basic-rules-of-probability)

## 3. Conditional probability changes the denominator

The notation $\Pr(E\mid M)$ means the probability of $E$ **given** $M$. Restricting attention to the marker-positive records changes the eligible set from 80 records to 20. The eight records in the intersection remain the numerator:

$$
\Pr(E\mid M)
=\frac{\Pr(E\cap M)}{\Pr(M)}
=\frac{8/80}{20/80}
=\frac{8}{20}
=0.40.
$$

Reversing the conditioning asks a different question:

$$
\Pr(M\mid E)
=\frac{\Pr(M\cap E)}{\Pr(E)}
=\frac{8/80}{16/80}
=\frac{8}{16}
=0.50.
$$

Thus, 40% of the constructed marker-positive records have the event, whereas 50% of the constructed event-positive records have the marker. The shared numerator does not make the probabilities interchangeable. Conditioning also does not establish temporal or causal direction; it specifies the information restricting the calculation.

For an event $B$ with positive probability, the definition is

$$
\Pr(A\mid B)=\frac{\Pr(A\cap B)}{\Pr(B)},\qquad \Pr(B)>0.
$$

In these finite examples, a conditioning event with probability zero supplies no eligible outcomes. Dividing by zero is undefined. The correct response is to identify that missing denominator, rather than report a conditional probability of zero. In the existing laboratory, `conditional(0.1, 0.25)` returns 0.4; a call with a zero second argument is rejected.

**Section references:** [OpenStax: Probability Theory and Bayes' Theorem](https://openstax.org/books/principles-data-science/pages/3-4-probability-theory) · [OpenStax: Two Basic Rules of Probability](https://openstax.org/books/introductory-statistics/pages/3-3-two-basic-rules-of-probability)

## 4. Independence differs from mutual exclusion

Two events $A$ and $B$ are independent when

$$
\Pr(A\cap B)=\Pr(A)\Pr(B).
$$

When the relevant conditioning probability is positive, this also means that conditioning on one event leaves the probability of the other unchanged. In the constructed roster,

$$
\Pr(M)\Pr(E)=0.25(0.20)=0.05
\neq0.10=\Pr(M\cap E).
$$

The two labels are therefore dependent under this finite selection experiment. Equivalently, $\Pr(E\mid M)=0.40$ differs from the marginal probability $\Pr(E)=0.20$. This is a property of the stipulated table; it is not an inferential test of a biological association.

Mutually exclusive events have no shared outcomes: $A\cap B=\varnothing$. Their intersection probability is zero. Marker-positive and marker-negative labels are mutually exclusive in this two-category construction. They are not independent: selecting a marker-positive record excludes marker-negative status for that same selection.

If mutually exclusive events both have positive probability, they cannot be independent because their positive marginal-product probability cannot equal their zero intersection probability. A zero-probability event is the boundary exception. This statement concerns events within one experiment; it must also be distinguished from the separate study-design assumption that different participants contribute independent observations.

**Section references:** [OpenStax: Two Basic Rules of Probability](https://openstax.org/books/introductory-statistics/pages/3-3-two-basic-rules-of-probability) · [OpenStax: Introductory Statistics Probability Terminology](https://openstax.org/books/introductory-statistics-2e/pages/3-key-terms)

## 5. Derive total probability and Bayes' theorem

The marker-positive and marker-negative groups partition the roster: they do not overlap and together include every record. The response event can therefore be separated into two disjoint pieces:

$$
E=(E\cap M)\cup(E\cap M^c).
$$

Adding their probabilities and using the definition of conditional probability gives the total-probability rule:

$$
\Pr(E)
=\Pr(E\mid M)\Pr(M)
+\Pr(E\mid M^c)\Pr(M^c).
$$

The example reconstructs the marginal event probability from the two groups:

$$
\Pr(E)
=\frac{8}{20}\frac{20}{80}
+\frac{8}{60}\frac{60}{80}
=\frac{8}{80}+\frac{8}{80}
=0.20.
$$

This is a weighted average of conditional probabilities. The group weights, 0.25 and 0.75, reflect their different sizes; an unweighted average of $8/20$ and $8/60$ would answer a different question.

The joint probability can also be written in either direction:

$$
\Pr(M\cap E)
=\Pr(E\mid M)\Pr(M)
=\Pr(M\mid E)\Pr(E).
$$

Dividing by $\Pr(E)>0$ yields Bayes' theorem:

$$
\Pr(M\mid E)
=\frac{\Pr(E\mid M)\Pr(M)}{\Pr(E)}.
$$

Substituting total probability into the denominator gives

$$
\Pr(M\mid E)
=
\frac{\Pr(E\mid M)\Pr(M)}
{\Pr(E\mid M)\Pr(M)+\Pr(E\mid M^c)\Pr(M^c)}
=\frac{0.40(0.25)}{0.20}=0.50.
$$

All conditioning groups used here have positive probability. The derivation explains how to reverse a conditional statement while retaining the group weights; it does not permit simply exchanging the expressions on either side of the conditioning bar.

**Section references:** [OpenStax: Probability Theory and Bayes' Theorem](https://openstax.org/books/principles-data-science/pages/3-4-probability-theory) · [OpenStax: Two Basic Rules of Probability](https://openstax.org/books/introductory-statistics/pages/3-3-two-basic-rules-of-probability)

## 6. Define a separate screening probability model

The next experiment concerns a hypothetical population at a defined screening occasion. Let $D$ denote the presence of a specified target condition and $D^c$ its absence. Let $T^+$ and $T^-$ denote positive and negative results under a fixed test procedure and threshold. This two-result model excludes indeterminate or missing results.

Define the following parameters using the [NCI screening terminology](https://www.cancer.gov/about-cancer/screening/hp-screening-overview-pdq):

| Quantity | Probability definition | Conditioning group |
| --- | --- | --- |
| Prevalence, $\pi$ | $\Pr(D)$ | Hypothetical target population at the screening occasion |
| Sensitivity, $\mathrm{Se}$ | $\Pr(T^+\mid D)$ | People with the target condition |
| Specificity, $\mathrm{Sp}$ | $\Pr(T^-\mid D^c)$ | People without the target condition |
| Positive predictive value, $\mathrm{PPV}$ | $\Pr(D\mid T^+)$ | Positive results |
| Negative predictive value, $\mathrm{NPV}$ | $\Pr(D^c\mid T^-)$ | Negative results |

Under this model, the false-positive probability conditional on absence of the condition is $1-\mathrm{Sp}$. The probability of being both condition-negative and test-positive is a different quantity:

$$
\Pr(D^c\cap T^+)=(1-\pi)(1-\mathrm{Sp}).
$$

Combining the two routes to a positive result gives

$$
\Pr(T^+)=\pi\mathrm{Se}+(1-\pi)(1-\mathrm{Sp}),
$$

and Bayes' theorem gives

$$
\mathrm{PPV}
=\frac{\pi\mathrm{Se}}
{\pi\mathrm{Se}+(1-\pi)(1-\mathrm{Sp})}.
$$

Similarly,

$$
\mathrm{NPV}
=\frac{(1-\pi)\mathrm{Sp}}
{(1-\pi)\mathrm{Sp}+\pi(1-\mathrm{Se})}.
$$

Each expression requires a positive denominator. These formulas map stated population and test assumptions to conditional probabilities; they do not estimate those assumptions from a dataset.

**Section references:** [NCI PDQ: Cancer Screening Overview for Health Professionals](https://www.cancer.gov/about-cancer/screening/hp-screening-overview-pdq) · [OpenStax: Probability Theory and Bayes' Theorem](https://openstax.org/books/principles-data-science/pages/3-4-probability-theory)

## 7. Calculate expected counts for 10,000 hypothetical people

Fix the teaching assumptions at $\pi=0.01$, $\mathrm{Se}=0.90$ and $\mathrm{Sp}=0.95$. These are assumed constants. For a hypothetical population size $n=10{,}000$, multiplying each joint probability by $n$ yields its expected cell count.

| Expected result | Target condition present, $D$ | Target condition absent, $D^c$ | Expected row total |
| --- | ---: | ---: | ---: |
| Positive, $T^+$ | True positive: 90 | False positive: 495 | 585 |
| Negative, $T^-$ | False negative: 10 | True negative: 9,405 | 9,415 |
| Expected column total | 100 | 9,900 | 10,000 |

The four calculations are

$$
\begin{aligned}
\mathbb{E}[N_{\mathrm{TP}}]&=10{,}000(0.01)(0.90)=90,\\
\mathbb{E}[N_{\mathrm{FN}}]&=10{,}000(0.01)(0.10)=10,\\
\mathbb{E}[N_{\mathrm{FP}}]&=10{,}000(0.99)(0.05)=495,\\
\mathbb{E}[N_{\mathrm{TN}}]&=10{,}000(0.99)(0.95)=9{,}405.
\end{aligned}
$$

Here $N_{\mathrm{TP}}$ is the random true-positive count in a generated cohort; $\mathbb{E}$ denotes its expectation under the model. Expectations can be fractional for other choices of $n$ and parameters. Integer values in this table do not turn them into observed counts.

The positive-result denominator contains both true and false positives:

$$
\mathrm{PPV}
=\frac{90}{90+495}
=\frac{2}{13}
\approx0.1538
=15.38\%.
$$

The corresponding negative predictive value is

$$
\mathrm{NPV}
=\frac{9{,}405}{9{,}405+10}
=\frac{1{,}881}{1{,}883}
\approx0.9989
=99.89\%.
$$

Under these stipulated assumptions, 15.38% is the model probability of the target condition given a positive result. Sensitivity remains 90%; the 15.38% calculation uses a different conditioning group. The model's positive-result probability is $585/10{,}000=0.0585$, or 5.85%.

The ratio of these expected cell counts reproduces the model PPV because the common factor $n$ cancels. It is not a statement that every simulated cohort has 585 positives, nor that the expectation of a finite-sample estimated ratio must equal the ratio of expected counts.

**Section references:** [NCI PDQ: Cancer Screening Overview for Health Professionals](https://www.cancer.gov/about-cancer/screening/hp-screening-overview-pdq) · [OpenStax: Probability Theory and Bayes' Theorem](https://openstax.org/books/principles-data-science/pages/3-4-probability-theory)

## 8. Change prevalence while holding the test assumptions fixed

For a second hypothetical scenario, change only prevalence to $\pi=0.05$. Keep sensitivity at 0.90 and specificity at 0.95. In 10,000 expected records, the condition-positive and condition-negative totals become 500 and 9,500.

| Model quantity | Prevalence 0.01 | Prevalence 0.05 |
| --- | ---: | ---: |
| Expected true positives | 90 | 450 |
| Expected false positives | 495 | 475 |
| Expected false negatives | 10 | 50 |
| Expected true negatives | 9,405 | 9,025 |
| Expected positive results | 585 | 925 |
| PPV | $90/585\approx15.38\%$ | $450/925\approx48.65\%$ |
| NPV | $9{,}405/9{,}415\approx99.89\%$ | $9{,}025/9{,}075\approx99.45\%$ |

The second scenario has more condition-positive people contributing true positives and fewer condition-negative people contributing false positives. Bayes' theorem therefore produces

$$
\mathrm{PPV}
=\frac{0.05(0.90)}{0.05(0.90)+0.95(0.05)}
=\frac{450}{925}
=\frac{18}{37}
\approx0.486486.
$$

The PPV changes because the population weight changes; the assumed sensitivity and specificity do not improve. This is a controlled mathematical comparison with fixed test properties, not evidence that those properties remain constant when a real test moves between populations.

The count table also makes the scale explicit. Changing $n$ alone scales the expected counts while leaving these model predictive values unchanged. Changing prevalence changes the relative contributions to the positive-result group.

**Section references:** [NCI PDQ: Cancer Screening Overview for Health Professionals](https://www.cancer.gov/about-cancer/screening/hp-screening-overview-pdq) · [OpenStax: Probability Theory and Bayes' Theorem](https://openstax.org/books/principles-data-science/pages/3-4-probability-theory)

## 9. Separate expectation, simulation and sampling uncertainty

The existing laboratory implements three distinct operations:

| Operation | Inputs and output | Meaning |
| --- | --- | --- |
| Exact model calculation | Fixed $\pi$, sensitivity and specificity produce joint probabilities, PPV and NPV | An algebraic consequence of the assumptions |
| Expected-count calculation | Model probabilities multiplied by a stated population size | Expected cell counts; not a generated dataset |
| Simulation | Pseudorandom draws produce integer cells for one fictional cohort | One realization from the assumed probability model |

In the simulation, each hypothetical person first receives a condition indicator with probability $\pi$. A second draw produces a positive test with probability $\mathrm{Se}$ when the condition is present and $1-\mathrm{Sp}$ otherwise. The code treats people as independent under this generator. All four simulated cell counts sum to $n$; their individual values need not equal the expectations.

For example, $\mathbb{E}[N_{\mathrm{TP}}]=n\pi\mathrm{Se}$ can be derived by adding the true-positive probabilities over the $n$ people. This expectation does not itself require between-person independence; the independent-cohort generator makes an additional assumption about the joint distribution and resulting variability.

The [Python random documentation](https://docs.python.org/3.12/library/random.html) and [R random-number documentation](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Random.html) describe seed and generator behavior. A recorded seed supports replay within the specified implementation and environment. It does not imply matching R and Python draws. The existing Python lab draws condition and test values consecutively for each person; the R lab draws the condition vector and then the test vector. Their generator initialization and draw order differ even when both receive seed 711.

More simulated replications can reduce Monte Carlo uncertainty when approximating properties of the fixed model. They do not provide additional clinical participants or establish the accuracy of the input prevalence and test parameters. In an actual study, those parameters would be estimated; their uncertainty would need a justified analysis. A confidence interval cannot be manufactured by treating an expected-count table as observed patient data.

**Section references:** [Python 3.12: random module and reproducibility](https://docs.python.org/3.12/library/random.html) · [R Base: Random Number Generation](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Random.html)

## 10. Run the existing laboratory and inspect its checks

Use the existing [Python probability laboratory](../examples/oncology_probability.py), [base-R probability laboratory](../examples/oncology_probability.R) and [Python test suite](../../scripts/test_oncology_probability.py). No external dataset or additional scientific package is required by these files. Run the commands from the repository root:

```bash
python3 oncology/examples/oncology_probability.py
python3 -m unittest discover -s scripts -p 'test_oncology_probability.py' -v
Rscript --vanilla oncology/examples/oncology_probability.R
```

The last command requires an installed R runtime. Each program prints its own fixture output; the R script also runs its embedded checks when executed directly. A command listed here is a reproducibility instruction, not a record that it has been executed for the current revision.

| Mathematical task | Existing function | Check against this chapter |
| --- | --- | --- |
| Conditional probability | `conditional` in both languages | `conditional(0.1, 0.25)` gives 0.4; reversing the conditioning denominator to 0.2 gives 0.5 |
| Union | Python `union`; R `union_probability` | Marginals 0.20 and 0.25 with intersection 0.10 give 0.35 |
| Predictive values | `screening_probabilities` | PPV is $90/585$ at prevalence 0.01 and $450/925$ at prevalence 0.05 |
| Expected cells | `expected_screening_counts` | At $n=10{,}000$ and prevalence 0.01: TP 90, FP 495, FN 10, TN 9,405 |
| Four-cell reconstruction | `probabilities_from_table` | Reconstruct sensitivity 0.90 and specificity 0.95 from the integer teaching table |
| One simulated cohort | `simulate_screening` | Four nonnegative integer cells sum to $n$; replay is within implementation |

The four-cell reconstruction accepts integer counts. It cannot be used to reclassify arbitrary fractional expected counts as observed records. The supplied integer teaching table is a convenient identity check only.

The expected-count helper preserves fractional and very small positive values. Floating-point output may differ slightly from an exact decimal representation; round values for display, while retaining the unrounded calculations for subsequent checks.

Inspect a failure case as carefully as a successful calculation. An intersection larger than either marginal is incompatible with a probability table. A zero conditioning denominator is undefined. If the model produces no positive results, PPV is undefined; the combined predictive-value helper rejects that request rather than substituting zero. This is an undefined conditional quantity within a boundary model, not a claim that every boundary prevalence is invalid.

Record the code revision, runtime versions, commands and observed outputs using the [analysis record](../../templates/analysis-record.md). Keep numerical replay, R execution, document rendering and independent scientific review as separate evidence.

**Section references:** [Python 3.12: random module and reproducibility](https://docs.python.org/3.12/library/random.html) · [R Base: Random Number Generation](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Random.html) · [OpenStax: Two Basic Rules of Probability](https://openstax.org/books/introductory-statistics/pages/3-3-two-basic-rules-of-probability)

## 11. Assumptions and scope of interpretation

The calculations require clearly defined target-condition and test-result categories, a specified population and screening occasion, and valid conditioning denominators. The illustrative screening model additionally assumes fixed prevalence and test characteristics, a fixed threshold, complete classification and no indeterminate results. The simulation adds independent people and a stated pseudorandom generator.

Actual research must determine how the reference condition was ascertained, how participants were selected, whether verification was complete, and whether test performance applies to the intended population. The [FDA diagnostic-test reporting guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/statistical-guidance-reporting-results-studies-evaluating-diagnostic-tests-guidance-industry-and-fda) and [STARD 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4623764/) address these requirements. A change in population can involve more than a change in prevalence. Repeated screens, related specimens and several tests per person require their own dependence model; multiplication of marginal probabilities is justified only when the needed independence assumption is appropriate.

The [NCI screening overview](https://www.cancer.gov/about-cancer/screening/hp-screening-overview-pdq) also separates test performance from benefits and harms of screening. A positive result can require further assessment. High sensitivity, specificity or predictive value alone does not establish a screening program's effect on mortality or its balance of benefits and harms.

For the investigator, the practical boundary is precise: these calculations explain the consequences of a probability model. Applying them to empirical breast cancer research requires source-specific estimates, study design and uncertainty analysis. The [diagnostic reporting guide](../../03_learning/bio_stats/CATEGORICAL_RISK_ROC_REPORTING.md) develops that reporting task.

**Section references:** [NCI PDQ: Cancer Screening Overview for Health Professionals](https://www.cancer.gov/about-cancer/screening/hp-screening-overview-pdq) · [OpenStax: Two Basic Rules of Probability](https://openstax.org/books/introductory-statistics/pages/3-3-two-basic-rules-of-probability) · [FDA: Statistical Guidance on Reporting Results from Studies Evaluating Diagnostic Tests (2007)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/statistical-guidance-reporting-results-studies-evaluating-diagnostic-tests-guidance-industry-and-fda) · [STARD 2015: Diagnostic Accuracy Reporting](https://pmc.ncbi.nlm.nih.gov/articles/PMC4623764/)

## 12. Original practice problems

Use the constructed 80-record roster or the stated screening assumptions; no external patient records are needed.

1. **Reconstruct the roster.** Only $n=80$, 20 marker-positive records, 16 event-positive records and an overlap of eight are supplied. Recover the four cells. Compute the probabilities of either condition, neither condition, and exactly one condition.
2. **Read the direction.** Calculate $\Pr(E\mid M)$, $\Pr(M\mid E)$ and $\Pr(E\mid M^c)$. Write a denominator-specific sentence for each.
3. **Evaluate independence.** Compare the roster's intersection probability with the product of its marginal probabilities. Explain whether the result is a test of association in a clinical population.
4. **Recover a marginal probability.** Use total probability to reconstruct $\Pr(E)$ from the marker-positive and marker-negative groups. Explain why an unweighted average is inappropriate.
5. **Rebuild the screening table.** Under prevalence 0.01, sensitivity 0.90 and specificity 0.95, calculate all four expected cells for 10,000 people. Compute PPV, NPV and the probability of a positive result.
6. **Change the population assumption.** Repeat the predictive-value calculation at prevalence 0.05. Identify which expected cells increase, which decrease, and which test parameters remain fixed.
7. **Identify an undefined quantity.** Suppose the target condition has probability zero and a hypothetical test is always negative. What is $\Pr(D\mid T^+)$? Explain the expected software response.
8. **Interpret reproducibility.** Two runs of the same implementation use seed 711 and identical settings. A separate R implementation also uses seed 711. Which agreement should be checked within an implementation, and which agreement should be checked between languages?
9. **Separate counts from expectations.** With the first screening model but $n=1{,}000$, the expected false-positive count is 49.5. Explain why this is valid and why a generated cohort cannot contain 49.5 false-positive people.

**Section references:** [OpenStax: Probability Theory and Bayes' Theorem](https://openstax.org/books/principles-data-science/pages/3-4-probability-theory) · [Python 3.12: random module and reproducibility](https://docs.python.org/3.12/library/random.html) · [R Base: Random Number Generation](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Random.html)

## 13. Worked answers with reasoning

1. **Cells and event combinations.** The cells are 8 in both categories, $20-8=12$ in the marker-only category, $16-8=8$ in the event-only category, and $80-8-12-8=52$ in neither. Therefore the union is $28/80=0.35$, neither is $52/80=0.65$, and exactly one is $20/80=0.25$. Inclusion of the intersection distinguishes the union from “exactly one.”
2. **Conditional direction.** The probabilities are $8/20=0.40$, $8/16=0.50$, and $8/60=2/15\approx0.133333$. The denominators respectively select marker-positive records, event-positive records and marker-negative records. Their numerical differences follow from these different eligible groups.
3. **Independence.** The intersection is $8/80=0.10$, whereas the marginal product is $(20/80)(16/80)=0.05$. Independence does not hold for the constructed selection experiment. This exact comparison uses stipulated counts; it contains no sampling-based hypothesis test or inference about real tumors.
4. **Total probability.** The weighted calculation is $(8/20)(20/80)+(8/60)(60/80)=0.20$. The two marker groups contain different fractions of the roster. Giving them equal weight would define a different selection scheme.
5. **First screening scenario.** The expected cells are TP 90, FP 495, FN 10 and TN 9,405. PPV is $90/585\approx15.38\%$; NPV is $9{,}405/9{,}415\approx99.89\%$; the positive-result probability is $585/10{,}000=5.85\%$. Each denominator corresponds to the quantity named.
6. **Higher prevalence scenario.** The expected cells are TP 450, FP 475, FN 50 and TN 9,025. PPV is $450/925\approx48.65\%$ and NPV is $9{,}025/9{,}075\approx99.45\%$. True-positive and false-negative counts increase because the expected condition-positive group grows. False-positive and true-negative counts decrease because the expected condition-negative group shrinks. Sensitivity and specificity remain 0.90 and 0.95 by construction.
7. **Impossible conditioning event.** $\Pr(T^+)=0$, so the requested ratio is $0/0$ and is undefined. Returning zero would confuse an absent conditioning group with an observed positive-result group containing no condition-positive people. A clear error or explicitly undefined result is required; the existing helper raises an error.
8. **Reproducibility.** The same implementation, source, runtime settings and seed should reproduce its own simulated counts. Between languages, compare the deterministic probability identities and expected counts numerically. Matching the seed alone does not establish matching random streams or draw order.
9. **Fractional expectation.** The calculation is $1{,}000(0.99)(0.05)=49.5$. Expectation summarizes a random count under the model; any single generated count must be an integer. It is unnecessary to round the expectation to pretend it is an observed number of people.

**Section references:** [OpenStax: Two Basic Rules of Probability](https://openstax.org/books/introductory-statistics/pages/3-3-two-basic-rules-of-probability) · [OpenStax: Probability Theory and Bayes' Theorem](https://openstax.org/books/principles-data-science/pages/3-4-probability-theory) · [Python 3.12: random module and reproducibility](https://docs.python.org/3.12/library/random.html) · [R Base: Random Number Generation](https://stat.ethz.ch/R-manual/R-devel/library/base/html/Random.html)

## 14. Mastery check and the transition to discrete outcomes

Before proceeding, the reader should be able to construct the four-cell roster, name the event and conditioning group before calculating, derive PPV from the two routes to a positive result, and explain why an expected count differs from a simulated count. The laboratory should be inspected for both correct outputs and meaningful rejection of invalid or undefined requests.

The next step is to describe the distribution of a count across repeated experiments. Instead of calculating the expected number of responses alone, an investigator may ask for the probability of observing at least a specified count under a stated model. That transition leads to the planned [CO-08 discrete-outcomes chapter](../ROADMAP.md); the existing [distribution and power guide](../../03_learning/bio_stats/BREAST_CANCER_DISTRIBUTIONS_AND_POWER.md) provides the current working material.

The scientific reporting distinction carries forward: a model-conditional event probability, an observed sample proportion, a confidence interval and a hypothesis-test probability are different objects. The [reporting and notation standard](../../03_learning/bio_stats/SCIENTIFIC_STATISTICAL_REPORTING_STANDARDS.md) supplies the common language used throughout the later chapters.

**Section references:** [OpenStax: Introductory Statistics Probability Terminology](https://openstax.org/books/introductory-statistics-2e/pages/3-key-terms) · [OpenStax: Probability Theory and Bayes' Theorem](https://openstax.org/books/principles-data-science/pages/3-4-probability-theory)
