# Statistical Inference

## Overview

Statistical inference is the process of drawing conclusions about a population based on information from a sample. Unlike descriptive statistics which summarize observed data, inferential statistics use probability theory to make predictions, test hypotheses, and estimate population parameters. This chapter covers sampling methods, point and interval estimation, and the theoretical foundations of inference.

## Why Statistical Inference?

### The Fundamental Problem
We want to know about a **population** (all individuals of interest), but we can only observe a **sample** (subset we actually measure).

**Examples**:
- Want: Average income of all US adults (330 million people)
- Have: Survey of 2,000 randomly selected adults
- Question: How close is our sample mean to the true population mean?

### Goals of Inference
1. **Estimation**: Estimate unknown population parameters
2. **Hypothesis Testing**: Evaluate claims about populations
3. **Prediction**: Predict future observations
4. **Quantify Uncertainty**: Provide measures of confidence/error

## Populations vs. Samples

| Aspect | Population | Sample |
|--------|------------|--------|
| **Definition** | All members of group | Subset of population |
| **Size** | N (usually very large) | n (manageable) |
| **Parameters** | μ, σ, p (Greek letters) | x̄, s, p̂ (Latin letters) |
| **Values** | Fixed but unknown | Computed from data |
| **Variability** | None (fixed value) | Varies sample to sample |

**Key Insight**: Sample statistics (x̄, s, p̂) estimate population parameters (μ, σ, p), but include sampling error.

## Sampling Methods

### Random Sampling

**Simple Random Sample (SRS)**:
- Every member has equal probability of selection
- Every subset of size n has equal probability
- Foundation of statistical inference

**Advantages**:
- Unbiased estimates
- Known sampling distributions
- Theoretical foundation solid

**How to Implement**:
- Number all population members
- Use random number generator
- Select corresponding members

### Other Sampling Methods

| Method | Description | When to Use |
|--------|-------------|-------------|
| **Stratified** | Divide population into groups (strata), sample from each | Ensure representation of subgroups |
| **Cluster** | Divide into clusters, randomly select clusters, sample all in selected clusters | Geographically dispersed population |
| **Systematic** | Select every kth member (e.g., every 10th person) | When list is available |
| **Convenience** | Sample whoever is easily accessible | Exploratory research (not for inference!) |

### Sampling Bias

**Types of Bias**:
1. **Selection Bias**: Sample not representative (e.g., surveying only volunteers)
2. **Non-Response Bias**: Those who respond differ from those who don't
3. **Voluntary Response Bias**: Self-selected respondents (often extreme views)
4. **Undercoverage**: Some population groups excluded from sampling frame

**Example**: 1936 Literary Digest poll predicted Landon over Roosevelt by surveying phone owners and magazine subscribers (wealthy, unrepresentative sample).

## Sampling Distributions

### Definition
A sampling distribution is the probability distribution of a statistic (like x̄) across all possible samples of size n.

### Sampling Distribution of the Mean

If we:
1. Take all possible samples of size n from population
2. Calculate x̄ for each sample
3. Plot all the x̄ values

Result is the **sampling distribution of x̄**.

**Properties**:
- **Mean**: E(x̄) = μ (sample mean is unbiased estimator)
- **Standard Deviation**: σx̄ = σ/√n (called **standard error**)
- **Shape**: Approximately normal for large n (Central Limit Theorem)

### Standard Error

**Definition**: Standard deviation of a sampling distribution

**For Sample Mean**: SE(x̄) = σ/√n

**For Sample Proportion**: SE(p̂) = √[p(1-p)/n]

**Key Insight**: Standard error decreases as sample size increases.
- Double sample size → SE reduced by √2 ≈ 1.41
- Quadruple sample size → SE reduced by half

### Central Limit Theorem (CLT)

**Statement**: For sufficiently large n (typically n ≥ 30), the sampling distribution of x̄ is approximately normal with:
- Mean: μ
- Standard deviation: σ/√n

**Regardless of the population's distribution!**

**Implications**:
1. Justifies using normal distribution for inference
2. Works even if population is skewed or non-normal
3. Larger samples → better approximation
4. Enables hypothesis tests and confidence intervals

**Example**:
Population: Uniform distribution [0, 100]
- Single observation: Uniform (flat)
- Mean of 5 observations: Starting to bell-curve
- Mean of 30 observations: Nearly normal

## Point Estimation

### Definition
A **point estimate** is a single value that estimates a population parameter.

### Common Point Estimates

| Parameter | Point Estimate | Symbol |
|-----------|----------------|--------|
| Population mean μ | Sample mean | x̄ |
| Population proportion p | Sample proportion | p̂ |
| Population variance σ² | Sample variance | s² |
| Population SD σ | Sample SD | s |
| Difference in means | Difference in sample means | x̄₁ - x̄₂ |

### Properties of Good Estimators

**1. Unbiased**: E(estimator) = parameter
- On average, equals the true value

**2. Consistent**: Converges to true value as n → ∞

**3. Efficient**: Smallest variance among unbiased estimators

**Example**:
- x̄ is unbiased for μ: E(x̄) = μ
- s² is unbiased for σ²: E(s²) = σ² (that's why we use n-1, not n)

## Interval Estimation (Confidence Intervals)

### Concept
Rather than single estimate, provide a **range** of plausible values with associated **confidence level**.

**Interpretation**: "We are 95% confident the true parameter lies in this interval"

**Formal Meaning**: If we repeated sampling many times and constructed intervals each time, 95% of intervals would contain the true parameter.

### Confidence Interval for Population Mean (σ known)

**Formula**: x̄ ± z* × (σ/√n)

Where:
- x̄ = sample mean
- z* = critical z-value for confidence level
- σ/√n = standard error

**Common Confidence Levels**:
| Confidence Level | z* |
|------------------|-----|
| 90% | 1.645 |
| 95% | 1.96 |
| 99% | 2.576 |

**Example**:
Sample of 64 students: x̄ = 72, σ = 8
95% CI: 72 ± 1.96(8/√64) = 72 ± 1.96 = [70.04, 73.96]

"We are 95% confident the true mean is between 70.04 and 73.96"

### Confidence Interval for Population Mean (σ unknown)

**Formula**: x̄ ± t* × (s/√n)

Where:
- t* = critical t-value with (n-1) degrees of freedom
- s = sample standard deviation

**When to Use**:
- σ unknown (most real situations)
- Use t-distribution instead of normal
- t-distribution has heavier tails (more conservative)
- As n increases, t → z

**Example**:
Sample of 16 students: x̄ = 72, s = 8, df = 15
95% CI with t* = 2.131: 72 ± 2.131(8/√16) = 72 ± 4.26 = [67.74, 76.26]

### Confidence Interval for Population Proportion

**Formula**: p̂ ± z* × √[p̂(1-p̂)/n]

Where p̂ = x/n (sample proportion)

**Requirements**:
- np̂ ≥ 10 and n(1-p̂) ≥ 10 (success-failure condition)

**Example**:
Survey 400 voters: 220 support candidate
p̂ = 220/400 = 0.55
95% CI: 0.55 ± 1.96√[0.55(0.45)/400] = 0.55 ± 0.049 = [0.501, 0.599]

"Between 50.1% and 59.9% of all voters support the candidate (95% confidence)"

### Interpreting Confidence Intervals

**Correct Interpretations**:
- "We are 95% confident the true parameter is in this interval"
- "If we repeated this procedure many times, 95% of intervals would contain the true parameter"

**Incorrect Interpretations**:
- ❌ "There's a 95% probability the true parameter is in this interval" (parameter is fixed, not random)
- ❌ "95% of the data falls in this interval" (it's about the parameter, not data)

### Factors Affecting Interval Width

**Wider Intervals** (more uncertainty):
- Higher confidence level (95% → 99%)
- Larger variability (larger σ or s)
- Smaller sample size

**Narrower Intervals** (more precision):
- Lower confidence level (95% → 90%)
- Smaller variability
- Larger sample size

**Trade-off**: Precision vs. Confidence
- 95% CI: [68, 76] (narrow but less confident)
- 99% CI: [65, 79] (wider but more confident)

## Sample Size Determination

### For Estimating Mean

**Formula**: n = (z*σ / E)²

Where:
- z* = critical value for confidence level
- σ = population standard deviation (estimate if unknown)
- E = desired margin of error

**Example**: Estimate mean height within ±0.5 inches (95% confidence), σ = 3 inches
n = (1.96 × 3 / 0.5)² = (11.76)² ≈ 139 people

### For Estimating Proportion

**Formula**: n = p̂(1-p̂)(z*/E)²

**Conservative Approach**: Use p̂ = 0.5 (maximizes n)
n = 0.25(z*/E)²

**Example**: Estimate proportion within ±3% (95% confidence)
n = 0.25(1.96/0.03)² = 0.25(65.33)² ≈ 1,068 people

**Key Insight**: To halve margin of error, need 4× the sample size.

## Real-World Examples

### Example 1: Political Polling

**Scenario**: Poll 1,200 voters before election

**Data**:
- 588 support Candidate A
- p̂ = 588/1200 = 0.49

**95% Confidence Interval**:
p̂ ± 1.96√[0.49(0.51)/1200]
= 0.49 ± 0.028
= [0.462, 0.518]

**Interpretation**: We're 95% confident between 46.2% and 51.8% of all voters support Candidate A. Since interval includes 0.5, race is too close to call.

### Example 2: Quality Control

**Scenario**: Manufacturer claims average battery life is 500 hours

**Sample**: n = 36 batteries, x̄ = 485 hours, s = 30 hours

**95% Confidence Interval**:
t* = 2.030 (df = 35)
485 ± 2.030(30/√36)
= 485 ± 10.15
= [474.85, 495.15]

**Interpretation**: We're 95% confident true mean is between 475-495 hours. Since 500 is not in this interval, manufacturer's claim is questionable.

### Example 3: Medical Research

**Scenario**: New drug reduces blood pressure?

**Sample**: n = 50 patients, mean reduction = 12 mmHg, s = 8 mmHg

**90% Confidence Interval**:
t* = 1.677 (df = 49)
12 ± 1.677(8/√50)
= 12 ± 1.90
= [10.1, 13.9]

**Interpretation**: 90% confident true mean reduction is between 10.1-13.9 mmHg. Since entire interval is above 0, drug appears effective.

### Example 4: Income Survey

**Scenario**: Estimate average household income in city

**Pilot Study**: 30 households, x̄ = $65,000, s = $18,000

**Question**: How many households needed for ±$2,000 margin of error (95% confidence)?

**Solution**:
n = (1.96 × 18000 / 2000)²
= (17.64)²
≈ 311 households

### Example 5: Customer Satisfaction

**Scenario**: Company surveys customers

**Data**:
- n = 500 customers
- 380 satisfied (p̂ = 0.76)

**95% CI for proportion satisfied**:
0.76 ± 1.96√[0.76(0.24)/500]
= 0.76 ± 0.037
= [0.723, 0.797]

**Interpretation**: Between 72.3% and 79.7% of all customers are satisfied (95% confidence).

## Bootstrap Methods

### Concept
When theoretical distributions are unclear, use **resampling** from observed data.

**Procedure**:
1. Take random sample (with replacement) from original data
2. Calculate statistic (e.g., mean, median)
3. Repeat thousands of times
4. Use distribution of bootstrap statistics to construct CI

**Advantages**:
- Works for complex statistics (median, trimmed mean)
- Doesn't require distributional assumptions
- Computationally intensive but feasible with computers

**Example**: 95% Bootstrap CI = [2.5th percentile, 97.5th percentile] of bootstrap distribution

## Margin of Error

**Definition**: Half the width of confidence interval

**For Mean**: ME = z* × (σ/√n) or t* × (s/√n)

**For Proportion**: ME = z* × √[p̂(1-p̂)/n]

**In Media**: "52% ± 3%" means:
- Point estimate: 52%
- Margin of error: 3%
- Confidence interval: [49%, 55%]
- Usually assumes 95% confidence

## Key Terms

| Term | Definition |
|------|------------|
| **Population** | Entire group of interest |
| **Sample** | Subset of population actually observed |
| **Parameter** | Numerical characteristic of population (unknown) |
| **Statistic** | Numerical characteristic of sample (computed) |
| **Sampling Distribution** | Distribution of statistic across all possible samples |
| **Standard Error** | Standard deviation of sampling distribution |
| **Point Estimate** | Single value estimating parameter |
| **Confidence Interval** | Range of plausible values for parameter |
| **Confidence Level** | Probability method produces interval containing parameter |
| **Margin of Error** | Half-width of confidence interval |
| **Central Limit Theorem** | Sampling distribution of mean becomes normal for large n |
| **Degrees of Freedom** | Number of independent values in calculation |

## Summary

Statistical inference enables us to draw conclusions about populations from samples. The key challenge is quantifying the uncertainty inherent in sampling - our sample statistic varies from sample to sample due to random sampling.

Sampling distributions describe this variability. The Central Limit Theorem guarantees that sample means follow approximately normal distributions for large samples, providing the theoretical foundation for inference.

Point estimates provide single best guesses for parameters, while confidence intervals provide ranges of plausible values with associated confidence levels. A 95% confidence interval means that if we repeated our sampling procedure many times, 95% of resulting intervals would contain the true parameter.

Sample size determination balances desired precision (narrow intervals) with practical constraints (cost, time). Larger samples reduce standard errors and narrow confidence intervals, but with diminishing returns (quadrupling sample size halves margin of error).

These inference tools - point estimates, confidence intervals, and sample size calculations - prepare you for hypothesis testing, where we'll evaluate specific claims about population parameters.
