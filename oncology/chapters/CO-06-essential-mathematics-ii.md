# CO-06 — Essential Mathematics II: Calculus, Matrices and Optimization

*Computational Oncology: A Clinician–Scientist's Guide · Part I · Draft 0.1*  
[Book home](../README.md) · [Introduction](../INTRODUCTION.md) · [CO-05 mathematics I](CO-05-essential-mathematics-i.md) · [Roadmap](../ROADMAP.md) · [Evidence policy](../evidence/README.md)

## Why mathematics II is needed for cancer research

In cancer research, methods often begin with a table of people, specimens and measured features, but their calculations are expressed with derivatives and matrices. A biostatistical regression describes how a modeled outcome changes with a predictor. A molecular analysis uses matrices to align thousands of measured features with specimens. A trained model adjusts parameters by changing a numerical loss. A longitudinal summary may approximate an integral over observed time.

These tools are valuable only when their clinical meanings are already defined. A fitted coefficient is not a treatment effect by default; a rapid change in an invented mathematical curve is not evidence of tumor growth; and the columns of a gene-expression matrix are not independent patients merely because they are distinct specimens. The [NIST explanation of least squares](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm) and [Bioconductor's assay data structure](https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html) offer two distinct examples.

**Guiding question:** How do changes, directions, matrices and optimization turn measured oncology data into models—and where can mathematical correctness mislead clinical interpretation?

**Section references:** [NIST: Linear Least Squares Regression](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm) · [Bioconductor: SummarizedExperiment Assay Structure](https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html)

## Learning outcomes and prerequisites

A successful learner can (1) distinguish an average change from a derivative; (2) calculate basic derivatives, including the chain rule; (3) explain what a gradient means and check it numerically; (4) calculate dot products and validate matrix dimensions; (5) construct a correctly oriented design matrix; (6) fit and interpret a minimal least-squares model; (7) recognize rank deficiency; (8) explain gradient descent and parameter sensitivity; (9) approximate a time-integral using a trapezoidal rule; (10) replicate synthetic answers in independently written Python and R implementations; and (11) state why these computations **cannot by themselves justify clinical decisions**.

Read [CO-05](CO-05-essential-mathematics-i.md) first for rates, ratios, logarithms and units. This chapter assumes no prior calculus. The worked outcomes are fictional, arbitrary-unit teaching measurements, not patient observations.

**Section references:** [Calculus I: Derivatives as Rates of Change](https://openstax.org/books/calculus-volume-1/pages/3-4-derivatives-as-rates-of-change) · [R Base: Matrix Multiplication](https://stat.ethz.ch/R-manual/R-devel/library/base/html/matmult.html)

## 1. Functions and average rates of change

A **function** maps an input to an output. Let $m(t)$ describe a synthetic marker index measured in arbitrary units after $t$ weeks. Suppose the toy model is $m(t)=1+2t$. The average change from week 0 to week 2 is:

$$\frac{m(2)-m(0)}{2-0}=\frac{5-1}{2}=\mathbf{2}\ \text{index units/week}.$$

This tells us how a *constructed* value changes across an interval. If actual data were observed only at those two time points, we could compute an average slope but could not establish the true shape of the trajectory between visits. The recording instrument, visit schedule, informative missingness and patient or specimen identity would have to be documented.

The derivative generalizes that idea to a change at an individual input value; the [open calculus treatment of rates of change](https://openstax.org/books/calculus-volume-1/pages/3-4-derivatives-as-rates-of-change) gives the mathematical formulation. A clinical time trend requires longitudinal research design, not only algebra.

**Section references:** [Calculus I: Derivatives as Rates of Change](https://openstax.org/books/calculus-volume-1/pages/3-4-derivatives-as-rates-of-change) · [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/)

## 2. Derivatives, limits and meaningful units

For a differentiable function $f(t)$, its derivative at $t$ is defined by the limit:

$$f'(t)=\lim_{h\to0}\frac{f(t+h)-f(t)}{h}.$$

If $f(t)=t^2$, expanding $(t+h)^2-t^2$ gives $2th+h^2$, so the difference quotient is $2t+h$ and the limit is $f'(t)=2t$. At $t=3$ the derivative equals **6** in output units per unit of $t$. For a smooth, noisy set of clinical observations, this symbolic result does not automatically describe the patient's true instantaneous rate.

The *units* of a derivative come from output units divided by input units. For a dimensionless normalized signal as a function of weeks, the derivative has units of “normalized signal units per week”; a time derivative is not a probability. A finite-difference approximation,

$$f'(t)\approx \frac{f(t+h)-f(t-h)}{2h},$$

depends on a suitable step $h$, numerical precision and assumptions of smoothness. The companion Python lab checks the derivative of $t^2$ against this approximation. This is a mathematical check, not an assay validation.

**Section references:** [Calculus I: Derivatives as Rates of Change](https://openstax.org/books/calculus-volume-1/pages/3-4-derivatives-as-rates-of-change) · [NIST: Unit Conversion](https://www.nist.gov/pml/owm/metric-si/unit-conversion)

## 3. Exponential functions and the chain rule

A common abstract growth model is $f(t)=N_0e^{kt}$. Differentiation gives:

$$\frac{df}{dt}=kN_0e^{kt}=kf(t).$$

The parameter $k$ has reciprocal-time units; the model's fractional rate of change is constant by definition. It is **not** an appropriate universal model for untreated or treated cancer. Real tumors vary by subtype, microenvironment, therapy, sampling and observation schedule. CO-05 introduced the doubling expression as a numerical exercise; CO-06 explains its derivative.

The **chain rule** states that if $y=g(u)$ and $u=h(x)$, then $dy/dx=(dg/du)(du/dx)$. In modeling, composition appears when a linear predictor is passed through a nonlinear link.

For example, the toy logistic function $p(z)=1/(1+e^{-z})$ has derivative $p'(z)=p(z)(1-p(z))$. If $z=\beta_0+\beta_1x$, then $dp/dx=\beta_1p(1-p)$. At $z=0$, $p=0.5$ and $dp/dz=0.25$. The numerical result says something about the model's curve; it does not assert that any measured biomarker causes a change in cancer risk.

**Section references:** [Calculus I: Derivatives as Rates of Change](https://openstax.org/books/calculus-volume-1/pages/3-4-derivatives-as-rates-of-change) · [NIST: Linear Least Squares Regression](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm)

## 4. Partial derivatives and gradients

A model may depend on more than one parameter. For $f(a,b)=a^2+3b^2$, the **partial derivative** with respect to $a$ is $2a$ while holding $b$ fixed; the derivative with respect to $b$ is $6b$ holding $a$ fixed. The **gradient** combines them:

$$\nabla f(a,b)=\begin{bmatrix}2a\\6b\end{bmatrix}.$$

At $(a,b)=(1,2)$ the gradient is $(2,12)$. It describes the local direction of steepest increase under the usual Euclidean geometry, while its negative points toward local decrease. In two or more dimensions the size and interpretation of a gradient also depend on parameter scale and units, which is why normalization matters in numerical optimization.

An optimizer uses this mathematical signal to change coefficients. The [gradient and directional derivative reference](https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient) explains the vector relationship. There is no implication that decreasing an algorithm's loss improves patients' outcomes.

**Section references:** [Calculus III: Directional Derivatives and the Gradient](https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient) · [NIST: Linear Least Squares Regression](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm)

## 5. Vectors, dot products and their biological meaning

A **vector** is an ordered collection of components. Suppose a specimen's two synthetic feature values are $\mathbf{x}=(2,3)$ and a model uses weights $\mathbf{w}=(0.5,-1)$. Their dot product is:

$$\mathbf{x}\cdot\mathbf{w}=2(0.5)+3(-1)=\mathbf{-2}.$$

This calculation can be part of a linear score, but its interpretation requires the fitted model, feature definitions, units and calibration. A separate pure arithmetic fixture $\,(1,2,3)\cdot(4,5,6)=\mathbf{32}\,$ checks the formula.

A dot product requires **matching component lengths**. If gene coordinates or column orders are wrong, even equal-length vectors can be biologically misaligned. A result that is numerically legal is not necessarily scientifically meaningful; stable feature identifiers and unambiguous ordering are essential.

**Section references:** [R Base: Matrix Multiplication](https://stat.ethz.ch/R-manual/R-devel/library/base/html/matmult.html) · [Bioconductor: SummarizedExperiment Assay Structure](https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html)

## 6. Two matrix orientations: assays and clinical models

A matrix is a rectangular array. In many genomics workflows, an assay matrix uses **rows for genes/features and columns for specimens**, as described in the [Bioconductor SummarizedExperiment vignette](https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html). Consider this invented matrix:

$$A=\begin{bmatrix}10&20\\30&40\\50&60\end{bmatrix}.$$

It has **3 feature rows and 2 specimen columns**. The columns do **not** automatically represent two independent patients; specimen-to-person metadata must be checked.

In a conventional linear regression, the design matrix $X$ instead uses **rows for observational units and columns for predictors** (including an intercept if fitted). Our separate four-person teaching example is:

$$X=\begin{bmatrix}1&0\\1&1\\1&2\\1&3\end{bmatrix},\quad
\boldsymbol\beta=\begin{bmatrix}\beta_0\\\beta_1\end{bmatrix},\quad
\hat{\mathbf y}=X\boldsymbol\beta.$$

This $X$ has dimension $4\times2$; $\boldsymbol\beta$ is $2\times1$, so the predicted outcome is $4\times1$. Matrix multiplication fails if inner dimensions disagree. Never silently transpose a matrix solely to satisfy software; justify orientation by its scientific units.

**Section references:** [Bioconductor: SummarizedExperiment Assay Structure](https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html) · [R Base: Matrix Multiplication](https://stat.ethz.ch/R-manual/R-devel/library/base/html/matmult.html)

## 7. Matrix multiplication, rank and identifiability

Matrix multiplication combines rows and columns through dot products. With our four-row design, the cross-product matrices are:

$$X^{T}X=\begin{bmatrix}4&6\\6&14\end{bmatrix},\qquad
X^{T}\mathbf y=\begin{bmatrix}11\\22\end{bmatrix}.$$

The algebraic least-squares solution to the **full-rank** normal equations is $(X^{T}X)\hat{\boldsymbol\beta}=X^{T}\mathbf y$. But a design in which every predictor value is the same cannot separately identify an intercept and that predictor's coefficient; the two columns lack independent information. That is **rank deficiency**.

In production research software, do not routinely compute $(X^{T}X)^{-1}X^{T}\mathbf y$ directly: forming the cross-product can worsen numerical conditioning. QR or singular-value methods are generally preferable for least squares, and rank/conditioning should be inspected. The [R QR-decomposition documentation](https://stat.ethz.ch/R-manual/R-devel/library/base/html/qr.html) explains these operations; the Python lab deliberately uses a tiny centered two-parameter identity for teaching only.

**Section references:** [NIST: Linear Least Squares Regression](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm) · [R Base: QR Decomposition and qr.solve](https://stat.ethz.ch/R-manual/R-devel/library/base/html/qr.html)

## 8. Derive and fit a miniature least-squares model

Our fully invented teaching cohort contains four **independent conceptual units**, each with a dimensionless marker $x$ and a continuous outcome index $y$:

| Unit | $x$ | $y$ |
| --- | ---: | ---: |
| A | 0 | 1 |
| B | 1 | 2 |
| C | 2 | 4 |
| D | 3 | 4 |

A straight-line model predicts $\hat y_i=\beta_0+\beta_1x_i$. The ordinary least-squares criterion is the sum of squared residuals:

$$\operatorname{SSE}(\beta_0,\beta_1)=\sum_{i=1}^{4}(y_i-\beta_0-\beta_1x_i)^2.$$

Here $\bar x=1.5$, $\bar y=2.75$, $\sum(x_i-\bar x)^2=5$, and $\sum(x_i-\bar x)(y_i-\bar y)=5.5$. Thus $\hat\beta_1=5.5/5=\mathbf{1.1}$ and $\hat\beta_0=2.75-1.1(1.5)=\mathbf{1.1}$.

Predictions are $(1.1,2.2,3.3,4.4)$; residuals $y_i-\hat y_i$ are $(-0.1,-0.2,0.7,-0.4)$; therefore $\operatorname{SSE}=\mathbf{0.7}$.

This demonstrates regression arithmetic, **not** valid inference, causality or generalization. Four synthetic observations do not justify clinical interpretation, and the term “independent” is a design assumption, not something we learn from the algebra.

**Section references:** [NIST: Linear Least Squares Regression](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm) · [STROBE Observational Study Reporting](https://www.equator-network.org/reporting-guidelines/strobe/)

## 9. Loss functions, gradients and gradient descent

To simplify optimization derivatives, define the half-mean-squared-error objective:

$$J(\boldsymbol\beta)=\frac{1}{2n}\sum_{i=1}^{n}(\beta_0+\beta_1x_i-y_i)^2.$$

Its gradient is:

$$\frac{\partial J}{\partial\beta_0}=\frac{1}{n}\sum_i(\hat y_i-y_i),\qquad
\frac{\partial J}{\partial\beta_1}=\frac{1}{n}\sum_i x_i(\hat y_i-y_i).$$

At $\boldsymbol\beta=(0,0)$, our fixture's gradient is **$(-2.75,-5.5)$**. A gradient-descent step with $\eta=0.1$ uses $\boldsymbol\beta_{\mathrm{new}}=\boldsymbol\beta-\eta\nabla J$; the first step is $(0.275,0.55)$. Repeating well-behaved steps approaches the least-squares coefficients $(1.1,1.1)$, with final $J=0.7/(2\cdot4)=\mathbf{0.0875}$.

The Python and R labs compare independently implemented gradient descent with closed-form or QR-based fitting. This is **a controlled toy convex problem**. In high-dimensional modeling, convergence, learning rate, numerical stability, initialization and validation require additional review.

**Section references:** [Calculus III: Directional Derivatives and the Gradient](https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient) · [NIST: Linear Least Squares Regression](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm)

## 10. The logistic curve and its derivative

A logistic link maps a real-valued score to $(0,1)$:

$$p(z)=\frac{1}{1+e^{-z}},\qquad \frac{dp}{dz}=p(z)\{1-p(z)\}.$$

At $z=0$, $p(0)=0.5$ and the derivative is $\mathbf{0.25}$. Large positive scores approach 1; large negative scores approach 0. Stable evaluation avoids direct exponentiation of a huge positive number where possible.

In actual cancer prediction, a modeled probability requires a defined **outcome**, population, prediction time, model coefficients and calibration testing. A logistic formula by itself is not a verified cancer risk calculator. The [TRIPOD+AI statement](https://pubmed.ncbi.nlm.nih.gov/38626948/) helps distinguish model reporting from validation and deployment.

**Section references:** [Calculus I: Derivatives as Rates of Change](https://openstax.org/books/calculus-volume-1/pages/3-4-derivatives-as-rates-of-change) · [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/)

## 11. Integration and trapezoidal approximation

An integral can summarize a quantity accumulated over an interval. When we observe a small number of measurements at times $t_0<t_1<\dots<t_k$, we may approximate the area under an interpolated curve using trapezoids:

$$\operatorname{AUC}_{\mathrm{trap}}=\sum_{j=0}^{k-1}(t_{j+1}-t_j)\frac{m_j+m_{j+1}}{2}.$$

For an **invented continuous index** with times $(0,1,2)$ weeks and values $(1,3,3)$ arbitrary units, the two trapezoids contribute $(1+3)/2=2$ and $(3+3)/2=3$, giving an approximate area of **5 index-unit weeks**.

This is not an event probability, cancer survival estimate, drug exposure calculation or causal dose-response estimate. Accuracy depends on the sampling times, units, measurement noise, trajectory between visits and observation process. See the [numerical integration reference](https://openstax.org/books/calculus-volume-2/pages/3-6-numerical-integration).

**Section references:** [Calculus II: Numerical Integration](https://openstax.org/books/calculus-volume-2/pages/3-6-numerical-integration) · [NIST: Unit Conversion](https://www.nist.gov/pml/owm/metric-si/unit-conversion)

## 12. Numerical verification and common pitfalls

Analytic and numerical solutions should agree within a justified tolerance, not by demanding exact equality of floating-point arithmetic. The book's Python test evaluates a centered finite difference of $t^2$ at $t=3$, compares the analytic loss gradient with a finite-difference gradient at multiple coefficient vectors, and verifies that gradient descent approaches the closed-form fit.

**Negative-case checks** reject constant predictor columns, unequal vector lengths, invalid matrix dimensions, nonincreasing time points, missing/nonfinite observations, an invalid optimizer step and malformed coefficients. The R implementation independently uses **QR-based fitting** and verifies the same reference values.

In a real research pipeline, passing those checks would be necessary but insufficient. Beyond numerical tests, investigators must audit access permissions, data provenance, preprocessing fit boundaries, held-out partitions and the scientific suitability of the objective.

**Section references:** [R Base: QR Decomposition and qr.solve](https://stat.ethz.ch/R-manual/R-devel/library/base/html/qr.html) · [Kapoor and Narayanan: Data Leakage (2023)](https://doi.org/10.1016/j.patter.2023.100804)

## 13. Reproducible laboratory walkthrough

The chapter has two separate implementations and a Python regression suite:

- [Python calculus and regression lab](../examples/oncology_calculus.py) — standard library, explicit input guards, synthetic numerical outputs.
- [R calculus and regression lab](../examples/oncology_calculus.R) — base R, independent QR fit, gradient/optimization replay and deliberate failure checks.
- [Python regression tests](../../scripts/test_oncology_calculus.py) — exact fixtures, finite-difference and gradient convergence checks, malformed-input cases.

Run from the repository root:

```bash
python3 oncology/examples/oncology_calculus.py
python3 -m unittest discover -s scripts -p 'test_oncology_calculus.py' -v
Rscript --vanilla oncology/examples/oncology_calculus.R
```

Core expected outcomes: ordinary least-squares intercept and slope of $1.1$, half-MSE $0.0875$, initial gradient $(-2.75,-5.5)$, sigmoid $p(0)=0.5$, derivative $0.25$ and trapezoidal area $5$ in arbitrary index-unit weeks. The study is fabricated and cannot demonstrate statistical significance or clinical usefulness.

**Section references:** [R Base: QR Decomposition and qr.solve](https://stat.ethz.ch/R-manual/R-devel/library/base/html/qr.html) · [NIST: Linear Least Squares Regression](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm)

## 14. Original practice problems

**A. Average versus instantaneous change.** An invented marker curve is $f(t)=2t^2+1$. Compute its average change from $t=1$ to $t=3$ and its derivative at $t=2$. Explain why an actual patient's observations at only two visits would not identify the derivative.

**B. Units.** A fictional biomarker index changes by 9 arbitrary units over 3 weeks. What units does its average slope have?

**C. Matrix dimensions.** For 100 genes measured on 12 specimens, state a conventional expression matrix's shape. Why can the biological sample size be smaller than 12?

**D. Dot products.** Calculate $(1,2,3)\cdot(4,5,6)$. What error results from silently reordering gene features?

**E. Ordinary least squares.** For the chapter's four-point case, calculate fitted values, residuals and the SSE without software.

**F. Optimization.** Derive the two components of the gradient of $J(\boldsymbol\beta)$ and state the first update with learning rate 0.1 from zero parameters.

**G. Rank.** Explain why an intercept plus a constant predictor cannot identify both coefficients.

**H. Numerical integration.** Compute the trapezoidal area for values $(1,3,3)$ at weeks $(0,1,2)$, giving correct combined units.

**I. Logistic derivative.** Compute $p(0)$ and $p'(0)$ for the sigmoid. What additional evidence is required before it becomes a clinically usable prediction?

**J. Scientific criticism.** A fitted gene signature has excellent training loss but mixes specimens from the same people across training and test. Identify the mathematical and scientific claims that remain unsupported.

**Section references:** [Calculus III: Directional Derivatives and the Gradient](https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient) · [Bioconductor: SummarizedExperiment Assay Structure](https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html) · [TRIPOD+AI Reporting Statement (2024)](https://pubmed.ncbi.nlm.nih.gov/38626948/)

## 15. Worked answers with interpretation

**A:** $f(1)=3$, $f(3)=19$, average change $(19-3)/(3-1)=8$ units per time; $f'(t)=4t$, so $f'(2)=8$. Agreement here arises from the chosen quadratic interval symmetry, not from observing a continuous clinical curve.

**B:** $9/3=3$ arbitrary index units per week; units must be declared.

**C:** 100 feature rows × 12 specimen columns; repeated specimens or specimens from the same patient are not necessarily independent patients.

**D:** $4+10+18=32$; mismatched feature order can produce a numerically valid but biologically invalid score.

**E:** Fitted $(1.1,2.2,3.3,4.4)$; observed-minus-fitted $(-0.1,-0.2,0.7,-0.4)$; SSE $0.01+0.04+0.49+0.16=0.7$.

**F:** $\nabla J(0,0)=(-2.75,-5.5)$; first update $(0.275,0.55)$.

**G:** A constant predictor column duplicates the intercept up to scale, so the design is rank deficient; multiple parameter pairs produce the same predictions.

**H:** Areas $2+3=5$ *index-unit weeks*, not a clinical event rate.

**I:** $p(0)=0.5$, $p'(0)=0.25$; clinical use additionally requires measurement validity, defined outcome, appropriate training, calibration, external evaluation and governance.

**J:** Low training loss verifies neither independence nor generalization; grouping by person and testing on truly held-out persons is essential if new-patient prediction is the intended use.

Independent numerical checks can establish these fabricated arithmetic results. They do not establish that an analysis answers a clinical question.

**Section references:** [NIST: Linear Least Squares Regression](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm) · [Kapoor and Narayanan: Data Leakage (2023)](https://doi.org/10.1016/j.patter.2023.100804)

## 16. Mastery gate and the road to probability

Before advancing, the reader should be able to reproduce the derivations, explain the direction and units of each quantity, recognize a rank-deficient or dimensionally invalid design, demonstrate that an analytic gradient matches a finite-difference approximation, and distinguish training optimization from clinical validation.

The next learning part begins with **CO-07: Randomness and Probability**. The transition is essential: a deterministic regression fit can calculate coefficients without telling us whether those estimates are stable across hypothetical repeated samples or support an inferential claim. Sampling, uncertainty and probability will supply the next layer.

**Source and editorial boundary:** This is independently written textbook prose. Linked open educational and official technical sources support background methods; the synthetic mathematical exercises and code are independent implementations. Source-link coverage is not peer review, and no protected research or patient data belong in this chapter.

[Return to the book](../README.md) · [Inspect cited source register](../evidence/SOURCES.md) · [Continue via roadmap](../ROADMAP.md)

**Section references:** [Calculus I: Derivatives as Rates of Change](https://openstax.org/books/calculus-volume-1/pages/3-4-derivatives-as-rates-of-change) · [NIST: Linear Least Squares Regression](https://www.itl.nist.gov/div898/handbook/pmd/section1/pmd141.htm)

