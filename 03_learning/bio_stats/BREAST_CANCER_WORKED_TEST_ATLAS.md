# Breast cancer biostatistics: worked interpretation atlas

[Foundations course: CLT, Welch, Student t, ANOVA and Poisson](BREAST_CANCER_STATISTICS_FOUNDATIONS.md) · [Rosner testing matrix](ROSNER_TEST_SELECTION_MATRIX.md) · [Decision-tree evidence](README.md) · [R laboratory](../examples/breast_cancer_test_atlas.R) · [Rosner chapter registry](rosner_method_registry.csv) · [Breast cancer learning materials](../../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md)

**Teaching edition, 2026-11-13.** Each method in the [Rosner-aligned matrix](ROSNER_TEST_SELECTION_MATRIX.md) has a breast-cancer narrative. The R laboratory uses **invented patients and invented measurements**, never downloaded clinical records. Tumor stage, receptor status, log-expression and follow-up durations are synthetic. **Do not interpret any numerical output as a finding about real patients, treatment effectiveness, ESR1, ERBB2, or any cancer subtype.**

The foundational organization follows Bernard Rosner, *Fundamentals of Biostatistics*, 8th ed. (Cengage, 2016), as a **topical crosswalk**, not copied textbook exercises or text. See the existing [published-paper atlas](README.md) for independently linked method papers. Some methods below are **modern extensions**, not represented as textbook claims.

**Numerical verification companion:** [Fully worked calculations, fixed reference results, and publication-style interpretations](BREAST_CANCER_NUMERICAL_VALIDATION.md) · [independent numerical replay checks](../tests/test_breast_cancer_reference_values.R).\n\n## A single clinical research narrative

Imagine a research team studying postoperative breast cancer outcomes. Investigators record one observation per participant at baseline (person ID; treatment group; age; synthetic continuous tumor biomarker; ER/HER2 status; ordered toxicity grade), and may record a matched biomarker after therapy, recurrences during person-time, or time to first recurrence with censoring. Later, they conduct an assay-level analysis across thousands of genes. The core lesson is that **the same clinical theme contains multiple distinct outcomes and sampling models**.

**Required intake:** Specify population and inclusion criteria, independent experimental unit (person, tumor, specimen or cell), baseline / time zero, outcome definition and unit, exposure or comparator, missing observations, censoring, expected parameter, clinical contrast, and prespecified multiplicity plan. Record total N, observed n, missing n, and exclusions for each analysis. A p-value does not replace effect size and confidence interval.

## Reading statistical results correctly

| Output | Read it as | Do not read it as |
| --- | --- | --- |
| Mean difference + 95% CI | Estimated difference in biomarker units and compatible values under stated assumptions | Probability the null is true or clinically important change |
| Risk difference / ratio | Difference / ratio of event probabilities in specified groups and time window | Causal effect without randomization or defensible identification |
| Odds ratio | Ratio of odds (conditional on modeled covariates if adjusted) | Automatically a risk ratio, particularly when outcomes are common |
| Pearson r / Spearman rho | Linear / rank-monotone association | Causation or agreement between instruments |
| Incidence rate ratio | Relative events per unit exposure time | Ratio of cumulative risks without assumptions |
| Hazard ratio | Relative instantaneous event hazards in at-risk sets under a specified model | Relative survival probability or risk ratio |
| Kaplan–Meier S(t) | Estimated probability of remaining event-free through t under censoring assumptions | Competing-risk event probability when other failures occur |
| FDR-adjusted q value | Multiple-testing error control under stated procedure/family | Probability a particular gene is truly associated |

## The tests, in a breast cancer story

Each method below supplies **question → illustrative data → R method → interpretation → gate**. Execute the [companion laboratory](../examples/breast_cancer_test_atlas.R) in R to obtain numerical results from the invented inputs. Where a CI is available, report it before considering the p-value.

### 01. One-sample mean — Rosner Chapter 7

**Question:** Is the mean of an invented postoperative log-expression score different from a prespecified, externally justified reference of 10 units? **Data:** independent patients, one numeric score each (not IDs). **R:** `t.test(marker, mu=10)`. **Interpretation:** the sample mean minus 10 and its 95% CI quantify a *mean difference*, not recurrence risk; state which direction is clinically relevant. **Gate:** reference validity, independence, extreme values, plausible mean-model assumptions. A score cannot be called log2 expression without its assay protocol.

### 02. Welch two-sample means — Chapter 8

**Question:** Does average synthetic Ki-67-like index differ between independent treatment groups? **Data:** one biomarker value per patient, groups A and B. **R:** `t.test(marker ~ group, var.equal=FALSE)`. **Interpretation:** report **A minus B** with interval, according to factor order; specify the direction deliberately. Welch handles unequal *variances*, not clustering or severe bias from measurement selection. **Gate:** independent people, units, distributional influence and predeclared group comparison.

### 03. Paired mean change — Chapter 8

**Question:** Did the same breast cancer patients' biomarker score change after neoadjuvant therapy? **Data:** one pre and one post score for each identified patient. **R:** `t.test(post - pre, mu=0)`. **Interpretation:** the estimate is **mean within-patient change**, not a comparison of independent patient means. Negative post-minus-pre values indicate reductions. **Gate:** ID matching, time spacing, assay comparability, missing post-therapy specimens.

### 04. Paired Wilcoxon signed-rank / sign — Chapter 9

**Question:** Do matched biomarker changes tend to be positive or negative when differences are skewed or ordinally scored? **Data:** nonzero, nonidentical before/after differences. **R:** `wilcox.test(post, pre, paired=TRUE)`; optional `binom.test(sum(delta>0), sum(delta!=0),p=.5)`. **Interpretation:** signed-rank tests symmetry-centered difference structure; a median-shift claim requires assumptions. A sign-test CI concerns the probability of a positive change **among nonzero differences**, not the mean change. **Gate:** zeros, ties and symmetry.

### 05. Independent Wilcoxon rank-sum — Chapter 9

**Question:** Are invented biomarker distributions different between independent ER-positive and ER-negative cohorts? **Data:** single continuous/ordinal result per participant. **R:** `wilcox.test(marker ~ er_group)`. **Interpretation:** evidence of distributional separation, not automatically a difference of medians if shapes differ. **Gate:** independence, overlaps, ties, distribution shape and selection bias.

### 06. Ordinary / Welch one-way ANOVA — Chapter 12

**Question:** Are average biomarker values equal across three synthetic breast cancer molecular-profile groups? **Data:** three independent groups. **R:** `oneway.test(marker ~ profile, var.equal=FALSE)`; `aov(marker ~ profile)` only when its assumptions are justified. **Interpretation:** a significant omnibus result establishes **at least one mean contrast**, not which pairs differ. Report prespecified contrasts and multiplicity-adjusted uncertainty. **Gate:** independent patients, group distributions, unequal variance, unequal n.

### 07. Kruskal–Wallis — Chapter 12

**Question:** Do toxicity grade distributions differ among three treatment groups? **Data:** ordered grades for independent patients. **R:** `kruskal.test(as.numeric(grade) ~ treatment)` for a predeclared ordering, recognizing the test ranks scores rather than assumes equal grade spacing. **Interpretation:** a distribution/rank difference, not automatically unequal median grade. **Gate:** ordinal coding, independence, ties and post-hoc plan.

### 08. Exact binomial — Chapters 4 and 7

**Question:** Among 80 independently eligible women in an invented cohort, 36 have a documented treatment response; is the true proportion greater than a *prespecified* reference 0.35? **R:** `binom.test(36, 80, p=.35, alternative="greater")`; exact upper tail `pbinom(35,80,.35,lower.tail=FALSE)`. **Interpretation:** a one-sided probability under the 0.35 model and an estimate of the response proportion, **not** treatment efficacy without a credible comparator. **Gate:** fixed eligible denominator, common event probability, independence, reference relevance.

### 09. Two independent proportions — Chapter 10

**Question:** Do independent treatment groups have different binary pathological response rates? **Data:** a 2 × 2 table of **counts**, not percentages. **R:** `prop.test(c(14,9),c(20,20),correct=FALSE)`, then planned risk difference with CI; `fisher.test(table)` for exact conditional analysis when justified. **Interpretation:** specify A vs B response **risk difference** and uncertainty, and distinguish it from the odds ratio from Fisher's test. **Gate:** eligibility and n per arm, randomization/selection and contingency assumptions.

### 10. McNemar paired binary — Chapter 10

**Question:** Did receptor-positive status change in the *same people* across baseline and subsequent assay? **Data:** paired 2 × 2 transition counts (negative→positive and positive→negative drive the contrast). **R:** `mcnemar.test(transition_table)`. **Interpretation:** discordance asymmetry, not differences between independent rates. **Gate:** paired IDs, laboratory reproducibility and a sparse-discordance exact alternative.

### 11. Pearson chi-square / Fisher exact R × C — Chapter 10

**Question:** Is synthetic molecular-profile category associated with pathological response category? **Data:** a patient-level table aggregated into profile × response counts. **R:** `chisq.test(tab)`; `fisher.test(tab)` only with an appropriate exact calculation. **Interpretation:** association of categorical distributions; report proportions and effect size rather than only chi-square p. **Gate:** independent units, expected cell counts, category definitions, multiple comparisons.

### 12. Multinomial goodness-of-fit — Chapter 10

**Question:** Does the invented cohort's distribution of three subtype categories differ from a *predefined* 40%/35%/25% benchmark? **Data:** 60, 45, 45 participants. **R:** `chisq.test(c(60,45,45),p=c(.4,.35,.25))`. **Interpretation:** evidence against the specified entire distribution, not identification of which subtype drives deviation without follow-up. **Gate:** benchmark independent of current observations and expected-cell adequacy.

### 13. Pearson / Spearman correlation — Chapter 11

**Question:** Across independent patients, is age associated with baseline marker expression? **Data:** one age and one marker value per person. **R:** `cor.test(age, marker,method="pearson")` or `method="spearman"`. **Interpretation:** Pearson describes linear co-variation; Spearman describes rank-monotone association; neither describes treatment benefit. **Gate:** inspect scatterplot and outliers and specify intended relation.

### 14. Linear regression — Chapter 11

**Question:** How does a continuous marker differ per decade of age after accounting for treatment group? **Data:** patient-level marker, age, group. **R:** `lm(marker ~ I(age/10) + group)`. **Interpretation:** the age coefficient means *marker units per 10-year increment conditional on group*, not a tenfold risk increase. **Gate:** functional form, residuals, confounding, influential points.

### 15. Logistic regression — Chapter 13

**Question:** What is the association between biomarker value and synthetic binary pathological response after adjustment for age? **Data:** independent patients with binary response and predictors. **R:** `glm(response ~ marker + age, family=binomial())`; `exp(coef(fit))` for odds ratios. **Interpretation:** an odds ratio is the factor multiplying the **odds** of response per unit biomarker, holding age fixed. It is not the risk ratio. **Gate:** outcome coding, separation, events, model misspecification, uncertainty.

### 16. Mantel–Haenszel stratification — Chapter 13

**Question:** Is response associated with treatment after stratifying by prespecified stage group? **Data:** two 2 × 2 response tables, one in each stage. **R:** `mantelhaen.test(array_of_tables)`. **Interpretation:** a common stratified odds-ratio estimate when a common-effect interpretation is defensible; inspect stratum differences first. **Gate:** stratification definition, sparse cells, effect heterogeneity, unmeasured confounding.

### 17. Repeated observations / clustered data — modern extension

**Question:** Are serial biomarker measures different by treatment when each woman has three visits? **Data:** long format with `id`, `visit`, `marker`, `treatment`. **R:** `lme4::lmer(marker ~ visit*treatment + (1|id), data=...)` for an appropriate linear mixed model, or suitable GEE. **Interpretation:** fixed coefficients concern conditional mean differences under the specified model; naive row-level t-tests falsely inflate independent n. **Gate:** cluster structure, visit timing, covariance, missing visits and model adequacy.

### 18. Poisson count test — Chapters 4 and 14

**Question:** If a hypothetical recurrence intensity is 40 per 100,000 person-years, and 20,000 person-years are observed, how surprising are **10 or more** recurrences? **R:** `ppois(9,lambda=8,lower.tail=FALSE)`; a one-rate interval/test can use `poisson.test(10,T=20000,r=40/100000)`. **Interpretation:** this is a count-tail probability **under a hypothetical homogeneous Poisson mechanism**, not an estimate of an individual woman's recurrence probability. **Gate:** exposure validity, event counting, dependence, variable hazard.

### 19. Poisson regression with exposure — Chapter 14

**Question:** Does the rate of recurrent emergency visits differ between follow-up groups? **Data:** independent count + person-time per subject. **R:** `glm(visits ~ group + offset(log(person_years)),family=poisson(),data=...)`. **Interpretation:** exponentiated group coefficient is a ratio of **event rates per person-year**, not an absolute difference in numbers of visits. **Gate:** exposure strictly positive, integer events, mean-variance assumptions, correlation and zero-generating process.

### 20. Negative-binomial count regression — modern extension

**Question:** Are breast cancer follow-up visit counts substantially more variable than a Poisson model allows? **R:** after a documented dispersion review, `MASS::glm.nb(visits ~ group + offset(log(person_years)),data=...)`. **Interpretation:** the exponentiated coefficient is still a rate ratio under the specified log-link model; extra dispersion changes variance modeling, not proof of a new biological mechanism. **Gate:** inspect residual dispersion, excess zeros and independence; avoid choosing by p-value alone.

### 21. Kaplan–Meier — Chapter 14

**Question:** What fraction of an invented cohort remains free of recorded recurrence through 12 months? **Data:** time from surgery, first recurrence flag, censoring indicator. **R:** `survival::survfit(Surv(months, recurrence)~1,data=...)`. **Interpretation:** `S(12)` estimates remaining event-free probability if censoring is suitably noninformative. **Gate:** time zero, at-risk sets, administrative and informative censoring.

### 22. Log-rank test — Chapter 14

**Question:** Do recurrence-free survival functions differ between treatment groups? **Data:** censored time-to-event plus group. **R:** `survival::survdiff(Surv(months,recurrence)~group,data=...)`. **Interpretation:** tests an equality-of-survival hypothesis; no hazard ratio or absolute benefit is produced by log-rank alone. **Gate:** time origin, independently censored outcomes and interpretation under crossing hazards.

### 23. Cox proportional-hazards regression — Chapter 14

**Question:** What is the adjusted instantaneous recurrence-hazard association for synthetic biomarker score? **R:** `survival::coxph(Surv(months,recurrence)~marker+group,data=...)`; check `survival::cox.zph(fit)`. **Interpretation:** `exp(beta)` is a **hazard ratio** per unit marker, conditional on modeled terms, if PH and other assumptions are adequate. **Gate:** PH and functional-form diagnostics, competing events, informative censoring, influential patients.

### 24. Competing-risk cumulative incidence — modern extension

**Question:** What is recurrence probability by 12 months if death without prior recurrence prevents later observation of a first recurrence? **Data:** time and first-event code 0=censored, 1=recurrence, 2=death without recurrence. **R:** `cmprsk::cuminc(ftime, fstatus,group)` or an appropriately specified cause-specific model. **Interpretation:** recurrence cumulative incidence is **not** `1-KM` with deaths censored when death is competing. **Gate:** mutually exclusive event coding, estimand (risk versus hazard), censoring.

### 25. Complex survey design — modern extension

**Question:** Estimate population prevalence of breast cancer screening uptake across a weighted national survey. **Data:** survey design variables, not a convenience clinic sample. **R:** `survey::svydesign(ids=~psu,strata=~stratum,weights=~weight,data=...,nest=TRUE)` then `survey::svymean(~screened, design)`. **Interpretation:** weighted population prevalence and design-based SE, **not** the unweighted proportion of rows. **Gate:** supplied survey weights/PSUs/strata, coding, nonresponse and target population.

### 26. High-dimensional gene-expression testing — modern extension

**Question:** Which transcripts are differentially expressed between two prespecified breast cancer groups? **Data:** raw gene × specimen counts, sample metadata, person-level replicates and batch. **R:** assay-aware `DESeq2::DESeq()`, `edgeR` or `limma-voom` with an explicit design and contrast; BH FDR over the tested gene family. **Interpretation:** each gene's estimated log2 fold change has a direction and uncertainty; FDR controls a multiple-testing criterion, **not** the probability each result is true. **Gate:** data type, library-size factors, independent biological replication, quality, multiple testing and leakage.

## Making a Results paragraph

For **each** worked case, write this sequence:

1. **Design and denominators:** “Of N independent participants, n had observed biomarker measurements; m were missing.”
2. **Contrast/estimand:** “The prespecified difference was group B minus group A in measured units.”
3. **Estimate and uncertainty:** “Estimated mean difference was [computed] units (95% CI [computed]).”
4. **Statistical evidence, when appropriate:** “The prespecified [test] yielded p=[computed].”
5. **Clinical interpretation and limits:** “The interval is compatible with [range of effect sizes]; this synthetic demonstration cannot determine treatment effectiveness.”

Never insert invented numerical values from this teaching chapter into a real abstract or manuscript. A small p-value alone does not demonstrate clinically relevant benefit.

## Reproducibility and evidence links

- [R laboratory for these chapters](../examples/breast_cancer_test_atlas.R) is a synthetic-only companion; optional packages are checked before use.
- [Existing paper-linked decision-tree atlas](README.md) provides publication-level context; this chapter is an **original breast cancer teaching overlay**, not a reproduction of those publications.
- [Rosner foundational matrix](ROSNER_TEST_SELECTION_MATRIX.md) lists the chapters and the distinction between textbook coverage and extensions.
- [Research governance gates](../../02_biomedical_coding/IMPLEMENTATION_GATES.md) apply: G2 units/IDs/missingness, G3 design, G5 diagnostics/uncertainty, G7 figures, G8 executable replay.
