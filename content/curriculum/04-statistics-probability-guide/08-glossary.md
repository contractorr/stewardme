# Statistics & Probability Glossary

## A

**Adjusted R²**: Modified R² that penalizes for adding variables to regression model. Only increases if new variable improves model enough to justify added complexity.

**Alternative Hypothesis (H₁, Hₐ)**: Statement we seek evidence for in hypothesis testing. Contains inequality (<, >, ≠).

**ANOVA (Analysis of Variance)**: Statistical test comparing means of three or more groups. Uses F-distribution.

## B

**Bayes' Theorem**: Formula for updating probability based on new evidence: P(A|B) = P(B|A)×P(A)/P(B). Foundation of Bayesian inference.

**Bernoulli Distribution**: Distribution of single trial with two outcomes (success/failure). Parameter p = probability of success.

**Bias**: Systematic error causing estimates to differ from true value. Unbiased estimator has expected value equal to parameter.

**Binomial Distribution**: Number of successes in n independent trials with constant success probability p. Mean = np, Variance = np(1-p).

**Bimodal**: Distribution with two peaks (modes). Suggests mixture of two groups.

**Boxplot**: Visual display showing five-number summary (min, Q₁, median, Q₃, max). Useful for comparing groups and identifying outliers.

**Bootstrap**: Resampling method with replacement from observed data to construct confidence intervals without distributional assumptions.

## C

**Categorical Data**: Data representing categories or groups. Can be nominal (no order) or ordinal (natural order).

**Central Limit Theorem (CLT)**: For large samples (n ≥ 30), distribution of sample means approximates normal distribution, regardless of population distribution.

**Chi-Square Distribution**: Distribution of sum of squared standard normal variables. Used for testing variance, goodness-of-fit, and independence.

**Chi-Square Test**: Tests for relationships between categorical variables or goodness-of-fit to expected distribution.

**Coefficient of Variation (CV)**: Relative variability measure: CV = (σ/μ)×100%. Enables comparison across different scales.

**Confidence Interval (CI)**: Range of plausible values for population parameter with associated confidence level (e.g., 95%). Not probability interval for parameter!

**Confidence Level**: Probability that interval construction method captures true parameter. Common: 90%, 95%, 99%.

**Confounding Variable**: Variable related to both predictor and response, potentially creating spurious relationship.

**Continuous Data**: Numerical data taking any value in interval (e.g., height, weight, time).

**Correlation**: Strength and direction of linear relationship between two variables. Measured by Pearson's r (-1 to 1).

**Correlation Coefficient (r)**: Measure of linear association. r = 1 (perfect positive), r = -1 (perfect negative), r = 0 (no linear relationship).

**Critical Value**: Boundary value separating rejection region from non-rejection region in hypothesis test.

**Cumulative Distribution Function (CDF)**: P(X ≤ x), probability random variable is less than or equal to x.

## D

**Degrees of Freedom (df)**: Number of independent values in calculation. For sample variance: n-1. Affects t and chi-square distributions.

**Dependent Variable**: Response variable (y) in regression. What we're trying to predict or explain.

**Descriptive Statistics**: Methods to summarize and describe data (mean, median, SD, graphs). No inference to larger population.

**Discrete Data**: Countable values (integers). Examples: number of children, coin flips, dice rolls.

**Distribution**: Pattern showing which values a variable takes and their frequencies or probabilities.

## E

**Effect Size**: Magnitude of relationship or difference, independent of sample size. Examples: Cohen's d, R².

**Empirical Rule (68-95-99.7 Rule)**: For normal distribution: 68% within 1 SD, 95% within 2 SD, 99.7% within 3 SD of mean.

**Error**: Difference between observed and true value. Random error varies unpredictably; systematic error (bias) is consistent.

**Expected Value (E(X))**: Long-run average value of random variable. Also called mean or expectation.

**Exponential Distribution**: Continuous distribution modeling time until event. Parameter λ (rate). Mean = 1/λ. Memoryless property.

**Extrapolation**: Predicting beyond range of observed data. Dangerous because model may not apply outside observed range.

## F

**F-Distribution**: Ratio of two chi-square distributions. Used in ANOVA and comparing variances. Parameters: two degrees of freedom.

**F-Test**: Test comparing variances of two groups or testing overall significance of regression model.

**False Negative**: Type II error. Failing to reject null hypothesis when it's false.

**False Positive**: Type I error. Rejecting null hypothesis when it's true.

## G

**Geometric Distribution**: Number of trials until first success. Parameter p. Mean = 1/p.

**Goodness-of-Fit Test**: Chi-square test determining if observed data matches expected distribution.

## H

**Histogram**: Bar graph showing frequency distribution of continuous data. X-axis divided into bins, height shows frequency.

**Homoscedasticity**: Equal variance of residuals across all predictor values. Assumption of linear regression.

**Hypothesis Test**: Formal procedure using sample data to evaluate claim about population parameter.

## I

**Independence**: Two events are independent if occurrence of one doesn't affect probability of other. P(A and B) = P(A)×P(B).

**Independent Variable**: Predictor variable (x) in regression. Used to predict response variable.

**Inferential Statistics**: Methods for drawing conclusions about population from sample. Includes hypothesis tests, confidence intervals.

**Intercept**: Value of y when x = 0 in regression equation. Often not meaningful if x = 0 impossible or outside data range.

**Interquartile Range (IQR)**: Q₃ - Q₁. Range of middle 50% of data. Robust to outliers.

## K

**Kurtosis**: Measure of tail heaviness. Leptokurtic (heavy tails), mesokurtic (normal-like), platykurtic (light tails).

## L

**Least Squares**: Method finding regression line minimizing sum of squared residuals.

**Left-Skewed**: Distribution with long left tail. Mean < Median < Mode.

**Level of Significance**: See Significance Level (α).

**Likelihood**: P(data|hypothesis). Probability of observing data given hypothesis is true. Used in Bayes' theorem.

**Linear Regression**: Modeling relationship between response variable and predictor(s) using linear equation.

**Log-Normal Distribution**: If ln(X) is normal, X is log-normal. Positive values only, right-skewed. Common for incomes, prices.

**Logistic Regression**: Regression when response is binary (yes/no). Models probability using logistic function.

## M

**Margin of Error (ME)**: Half-width of confidence interval. In polls: "52% ± 3%" means ME = 3%.

**Mean**: Arithmetic average. Sum divided by count. Affected by outliers.

**Median**: Middle value when data ordered. 50th percentile. Robust to outliers.

**Memoryless Property**: Past doesn't affect future probabilities. Property of exponential and geometric distributions.

**Mode**: Most frequently occurring value. Can have multiple modes (bimodal, multimodal).

**Multicollinearity**: High correlation among predictor variables in multiple regression. Causes unstable coefficient estimates.

**Multiple Regression**: Regression with multiple predictor variables. Controls for confounding, improves predictions.

**Mutually Exclusive**: Two events that cannot occur simultaneously. If A occurs, B cannot. P(A and B) = 0.

## N

**Nominal Data**: Categorical data with no natural order. Examples: colors, gender, country.

**Normal Distribution (Gaussian)**: Symmetric bell-shaped distribution. Parameters: μ (mean), σ (SD). Foundation of many statistical methods.

**Null Hypothesis (H₀)**: Statement of no effect or no difference. Assumed true until evidence suggests otherwise. Contains equality.

**Numerical Data**: Quantitative data. Can be discrete (counts) or continuous (measurements).

## O

**Odds Ratio**: Ratio of odds in one group to odds in another. Used in logistic regression and case-control studies.

**One-Tailed Test**: Alternative hypothesis in one direction only (>, <). More power but less flexible.

**Ordinal Data**: Categorical data with natural order. Examples: education level, satisfaction rating (low/medium/high).

**Outlier**: Data point differing significantly from other observations. Detected using IQR method (1.5×IQR) or z-scores (|z| > 3).

**Overfitting**: Model too complex, fits noise rather than signal. Performs well on training data but poorly on new data.

## P

**p-value**: Probability of observing data at least as extreme as ours, assuming null hypothesis is true. NOT probability H₀ is true!

**Paired t-Test**: Compares means of paired observations (before/after, matched pairs). Tests if mean difference equals zero.

**Parameter**: Numerical characteristic of population. Usually unknown. Examples: μ, σ, p. (Greek letters)

**Pearson's r**: See Correlation Coefficient.

**Percentile**: Value below which given percentage of data falls. 90th percentile means 90% below this value.

**Point Estimate**: Single value estimating population parameter. Example: sample mean x̄ estimates population mean μ.

**Poisson Distribution**: Number of events in fixed interval. Parameter λ (rate). Mean = Variance = λ. For rare events.

**Polynomial Regression**: Regression with squared or cubed terms to model curved relationships.

**Population**: Entire group of individuals or items of interest. Size N. Parameters (μ, σ, p) usually unknown.

**Posterior Probability**: Updated belief after observing evidence. P(hypothesis|data). Output of Bayes' theorem.

**Power**: Probability of correctly rejecting false null hypothesis. Power = 1 - β. Typically aim for ≥ 0.80.

**Prediction Interval**: Range for individual new observation. Wider than confidence interval for mean.

**Prior Probability**: Initial belief before observing evidence. P(hypothesis). Input to Bayes' theorem.

**Probability**: Number between 0 and 1 representing likelihood of event. 0 = impossible, 1 = certain.

**Probability Density Function (PDF)**: Function giving relative likelihood of continuous random variable taking specific value.

**Probability Mass Function (PMF)**: Function giving probability discrete random variable equals specific value.

## Q

**Qualitative Data**: See Categorical Data.

**Quantitative Data**: See Numerical Data.

**Quartile**: Values dividing data into four equal parts. Q₁ (25th percentile), Q₂ (median), Q₃ (75th percentile).

## R

**R² (R-squared)**: Coefficient of determination. Proportion of variance in y explained by x. Range: 0 to 1. For simple regression: R² = r².

**Random Sample**: Sample where every member of population has known (usually equal) probability of selection.

**Random Variable**: Variable whose value determined by random process. Can be discrete or continuous.

**Range**: Difference between maximum and minimum values. Simplest measure of spread.

**Regression**: Method modeling relationship between response and predictor variable(s) for prediction and explanation.

**Regression Line**: Line of best fit: ŷ = b₀ + b₁x. Minimizes sum of squared residuals.

**Residual**: Difference between observed and predicted value: y - ŷ. Used for model diagnostics.

**Residual Plot**: Graph of residuals vs. fitted values. Should show random scatter if model assumptions satisfied.

**Response Variable**: Dependent variable (y) in regression. What we're trying to predict.

**Right-Skewed**: Distribution with long right tail. Mode < Median < Mean. Common: income, prices, lifespan.

**Robust**: Statistic not heavily influenced by outliers. Median and IQR are robust; mean and SD are not.

## S

**Sample**: Subset of population actually observed. Size n. Statistics (x̄, s, p̂) computed from sample data.

**Sample Space**: Set of all possible outcomes of random process.

**Sampling Distribution**: Probability distribution of statistic (like x̄) across all possible samples of size n.

**Sampling Error**: Difference between sample statistic and population parameter due to observing sample rather than entire population.

**Scatterplot**: Graph showing relationship between two quantitative variables. Each point represents one observation.

**Significance Level (α)**: Threshold for rejecting null hypothesis. Probability of Type I error. Common: 0.05, 0.01, 0.10.

**Simple Random Sample (SRS)**: Every member has equal probability of selection. Foundation of statistical inference.

**Simpson's Paradox**: Trend appears in separate groups but reverses when groups combined. Highlights importance of considering confounding.

**Skewness**: Measure of asymmetry. Right-skewed (positive): long right tail. Left-skewed (negative): long left tail.

**Slope**: Change in y per unit change in x in regression. b₁ in equation ŷ = b₀ + b₁x.

**Standard Deviation (SD)**: Square root of variance. Typical distance from mean. Same units as data. Symbol: σ (population), s (sample).

**Standard Error (SE)**: Standard deviation of sampling distribution. Measures uncertainty in estimate. SE(x̄) = σ/√n.

**Standard Normal Distribution**: Normal distribution with μ = 0, σ = 1. Denoted Z ~ N(0,1). Used for z-scores.

**Standardization**: Converting to z-scores: z = (x - μ)/σ. Results in mean 0, SD 1.

**Statistic**: Numerical characteristic of sample. Computed from data. Examples: x̄, s, p̂. (Latin letters)

**Statistical Inference**: See Inferential Statistics.

**Statistical Significance**: Result unlikely to occur by chance alone. Typically p < 0.05. Doesn't guarantee practical importance!

**Stratified Sampling**: Divide population into groups (strata), sample from each. Ensures representation of subgroups.

**Student's t-Distribution**: Similar to normal but heavier tails. Parameter: degrees of freedom. Used when σ unknown.

## T

**t-Test**: Hypothesis test for means when population SD unknown. Uses t-distribution. Common types: one-sample, two-sample, paired.

**Test Statistic**: Standardized value calculated from sample data for hypothesis test. Examples: z, t, χ², F.

**Two-Tailed Test**: Alternative hypothesis in both directions (≠). More conservative than one-tailed.

**Type I Error**: False positive. Rejecting true null hypothesis. Probability = α (significance level).

**Type II Error**: False negative. Failing to reject false null hypothesis. Probability = β. Power = 1 - β.

## U

**Unbiased Estimator**: Estimator whose expected value equals parameter. E(estimator) = parameter. Sample mean is unbiased for population mean.

**Uniform Distribution**: All values in interval equally likely. Parameters: a (min), b (max). Mean = (a+b)/2.

## V

**Variable**: Characteristic that can take different values. Can be categorical or numerical.

**Variance**: Average squared deviation from mean. Measures spread. Units are squared. Var(X) = σ² (population), s² (sample).

**Variance Inflation Factor (VIF)**: Measure of multicollinearity. VIF > 10 problematic.

## Z

**z-Score (Standard Score)**: Number of standard deviations from mean. z = (x - μ)/σ. Enables comparison across scales.

**z-Test**: Hypothesis test for means when population SD known or large sample. Uses normal distribution.

---

## Quick Reference Tables

### Common Distributions

| Distribution | Type | Parameters | Mean | Variance |
|--------------|------|------------|------|----------|
| Bernoulli | Discrete | p | p | p(1-p) |
| Binomial | Discrete | n, p | np | np(1-p) |
| Poisson | Discrete | λ | λ | λ |
| Geometric | Discrete | p | 1/p | (1-p)/p² |
| Uniform | Continuous | a, b | (a+b)/2 | (b-a)²/12 |
| Normal | Continuous | μ, σ | μ | σ² |
| Exponential | Continuous | λ | 1/λ | 1/λ² |

### Critical Values (Two-Tailed)

| Confidence Level | α | z* |
|------------------|---|-----|
| 90% | 0.10 | 1.645 |
| 95% | 0.05 | 1.96 |
| 99% | 0.01 | 2.576 |

### Hypothesis Test Types

| Test | Use When | Test Statistic |
|------|----------|----------------|
| **One-sample z-test** | Testing mean, σ known | z = (x̄ - μ₀)/(σ/√n) |
| **One-sample t-test** | Testing mean, σ unknown | t = (x̄ - μ₀)/(s/√n) |
| **Two-sample t-test** | Comparing two means | t = (x̄₁ - x̄₂)/SE |
| **Paired t-test** | Comparing paired means | t = d̄/(s_d/√n) |
| **z-test for proportion** | Testing proportion | z = (p̂ - p₀)/√[p₀(1-p₀)/n] |
| **Chi-square test** | Categorical relationships | χ² = Σ(O-E)²/E |
| **F-test** | Comparing variances/ANOVA | F = s₁²/s₂² |

### Correlation Strength

| |r| | Interpretation |
|------|----------------|
| 0.0-0.2 | Very weak |
| 0.2-0.4 | Weak |
| 0.4-0.6 | Moderate |
| 0.6-0.8 | Strong |
| 0.8-1.0 | Very strong |

---

## Symbol Reference

### Greek Letters (Population Parameters)
- **μ** (mu): Population mean
- **σ** (sigma): Population standard deviation
- **σ²**: Population variance
- **ρ** (rho): Population correlation
- **α** (alpha): Significance level, Type I error probability
- **β** (beta): Type II error probability; regression coefficient
- **λ** (lambda): Rate parameter (Poisson, Exponential)

### Latin Letters (Sample Statistics)
- **x̄** (x-bar): Sample mean
- **s**: Sample standard deviation
- **s²**: Sample variance
- **r**: Sample correlation
- **p̂** (p-hat): Sample proportion
- **n**: Sample size
- **N**: Population size

### Other Symbols
- **H₀**: Null hypothesis
- **H₁**, **Hₐ**: Alternative hypothesis
- **P(A)**: Probability of event A
- **P(A|B)**: Conditional probability of A given B
- **E(X)**: Expected value of X
- **Var(X)**: Variance of X
- **ŷ** (y-hat): Predicted value of y
- **SE**: Standard error
- **CI**: Confidence interval
- **df**: Degrees of freedom

---

*This glossary provides quick reference for key terms throughout the statistics and probability guide. For detailed explanations and examples, see the relevant chapters.*
