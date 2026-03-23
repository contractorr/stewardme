# Probability Distributions

## Overview

A probability distribution describes how probabilities are distributed over the possible values of a random variable. Understanding distributions is crucial for modeling real-world phenomena, conducting statistical inference, and interpreting data. This chapter covers the most important discrete and continuous distributions, their properties, and applications.

## What is a Probability Distribution?

A probability distribution specifies:
- All possible values a random variable can take
- The probability (or probability density) associated with each value

### Discrete vs. Continuous Distributions

| Aspect | Discrete | Continuous |
|--------|----------|------------|
| **Values** | Countable (integers) | Uncountable (real numbers) |
| **Function** | Probability Mass Function (PMF) | Probability Density Function (PDF) |
| **Probability** | P(X = x) directly specified | P(X = x) = 0; use intervals P(a < X < b) |
| **Sum/Integral** | ΣP(X = x) = 1 | ∫f(x)dx = 1 |
| **Examples** | Coin flips, dice rolls, counts | Height, weight, time, temperature |

## Key Properties of Distributions

### 1. Expected Value (Mean)
The average value over the long run:
- **Discrete**: E(X) = Σ x·P(X = x)
- **Continuous**: E(X) = ∫ x·f(x)dx

### 2. Variance
Measure of spread around the mean:
- **Var(X) = E[(X - μ)²] = E(X²) - [E(X)]²**

### 3. Standard Deviation
Square root of variance: **σ = √Var(X)**

### 4. Median
Middle value where P(X ≤ median) = 0.5

### 5. Mode
Most likely value (highest probability or density)

## Discrete Distributions

### 1. Bernoulli Distribution

**Definition**: Single trial with two outcomes (success/failure)

**Parameters**: p (probability of success)

**PMF**:
- P(X = 1) = p
- P(X = 0) = 1 - p

**Properties**:
- Mean: E(X) = p
- Variance: Var(X) = p(1 - p)

**Examples**:
- Coin flip (heads/tails)
- Product defective or not
- Patient recovers or doesn't

### 2. Binomial Distribution

**Definition**: Number of successes in n independent Bernoulli trials

**Parameters**: n (number of trials), p (probability of success)

**PMF**: P(X = k) = C(n,k) × p^k × (1-p)^(n-k)

**Properties**:
- Mean: E(X) = np
- Variance: Var(X) = np(1 - p)

**When to Use**:
- Fixed number of independent trials
- Each trial has same probability of success
- Counting number of successes

**Examples**:

| Scenario | n | p | Question |
|----------|---|---|----------|
| Flip coin 10 times | 10 | 0.5 | How many heads? |
| Quality control: test 100 items | 100 | 0.05 | How many defective? |
| Survey 50 voters | 50 | 0.6 | How many support candidate? |

**Calculation Example**:
Flip coin 10 times. Probability of exactly 6 heads?
- P(X = 6) = C(10,6) × 0.5⁶ × 0.5⁴
- = 210 × 0.015625 × 0.0625
- = 0.205 or 20.5%

### 3. Poisson Distribution

**Definition**: Number of events occurring in fixed time/space interval

**Parameter**: λ (average rate, mean number of occurrences)

**PMF**: P(X = k) = (λ^k × e^(-λ)) / k!

**Properties**:
- Mean: E(X) = λ
- Variance: Var(X) = λ
- Standard deviation = √λ

**When to Use**:
- Events occur independently
- Events occur at constant average rate
- Two events cannot occur at exactly the same instant

**Examples**:

| Scenario | λ | Question |
|----------|---|----------|
| Website gets 5 visitors/hour | 5 | P(exactly 3 visitors in next hour)? |
| Phone receives 20 calls/day | 20 | P(more than 25 calls tomorrow)? |
| Bus stop: 3 buses/hour | 3 | P(no buses in next hour)? |
| Typos: 2 per page | 2 | P(0 typos on this page)? |

**Calculation Example**:
Average 4 customers per hour. Probability of exactly 2 customers next hour?
- P(X = 2) = (4² × e^(-4)) / 2!
- = (16 × 0.0183) / 2
- = 0.146 or 14.6%

### 4. Geometric Distribution

**Definition**: Number of trials until first success

**Parameter**: p (probability of success)

**PMF**: P(X = k) = (1-p)^(k-1) × p

**Properties**:
- Mean: E(X) = 1/p
- Variance: Var(X) = (1-p)/p²

**Examples**:
- Roll die until getting a 6
- Keep flipping coin until heads
- Sales calls until first sale

## Continuous Distributions

### 1. Uniform Distribution

**Definition**: All values in an interval equally likely

**Parameters**: a (minimum), b (maximum)

**PDF**: f(x) = 1/(b-a) for a ≤ x ≤ b

**Properties**:
- Mean: E(X) = (a + b)/2
- Variance: Var(X) = (b - a)²/12

**Examples**:
- Random number generator between 0 and 1
- Bus arrives randomly within 20-minute window
- Rounding errors in measurements

### 2. Normal (Gaussian) Distribution

**Definition**: Symmetric, bell-shaped distribution

**Parameters**: μ (mean), σ (standard deviation)

**PDF**: f(x) = (1/σ√(2π)) × e^(-(x-μ)²/(2σ²))

**Properties**:
- Mean = Median = Mode = μ
- Variance = σ²
- Symmetric around mean
- 68-95-99.7 rule (see below)

**Standard Normal Distribution**:
- Special case: μ = 0, σ = 1
- Any normal can be standardized: Z = (X - μ)/σ

**68-95-99.7 Rule (Empirical Rule)**:
- 68% of data within 1 standard deviation of mean (μ ± σ)
- 95% within 2 standard deviations (μ ± 2σ)
- 99.7% within 3 standard deviations (μ ± 3σ)

**Why It Matters**:
- Central Limit Theorem: Averages tend toward normal distribution
- Many natural phenomena approximately normal
- Foundation for many statistical tests

**Examples**:

| Variable | Typical μ | Typical σ |
|----------|-----------|-----------|
| Human height (inches) | 68 | 3 |
| IQ scores | 100 | 15 |
| SAT scores | 1050 | 200 |
| Measurement errors | 0 | varies |

**Calculation Example**:
Heights are normal with μ = 68 inches, σ = 3 inches.
What percentage of people are between 65 and 71 inches?

- 65 inches = μ - σ
- 71 inches = μ + σ
- By 68-95-99.7 rule: approximately 68%

### 3. Exponential Distribution

**Definition**: Time until an event occurs (continuous version of geometric)

**Parameter**: λ (rate parameter, events per unit time)

**PDF**: f(x) = λe^(-λx) for x ≥ 0

**Properties**:
- Mean: E(X) = 1/λ
- Variance: Var(X) = 1/λ²
- Memoryless property: P(X > s+t | X > s) = P(X > t)

**When to Use**:
- Time between Poisson events
- Lifetimes of products
- Wait times with constant hazard rate

**Examples**:

| Scenario | Rate λ | Mean Time 1/λ |
|----------|--------|---------------|
| Customer arrivals: 5/hour | 5 | 12 minutes |
| Light bulb lifetime | 0.001/hour | 1000 hours |
| Time between earthquakes | 0.1/year | 10 years |

**Memoryless Property**:
If light bulb has already lasted 500 hours, probability of lasting another 500 hours is same as when it was new.

### 4. Log-Normal Distribution

**Definition**: If ln(X) is normally distributed, then X is log-normally distributed

**Properties**:
- Positive values only (X > 0)
- Right-skewed (long right tail)
- Mean > Median > Mode

**Examples**:
- Income distributions
- Stock prices
- File sizes on internet
- City populations

### 5. Student's t-Distribution

**Definition**: Similar to normal but with heavier tails

**Parameter**: ν (degrees of freedom)

**Properties**:
- Symmetric around 0
- As ν → ∞, approaches normal distribution
- More probability in tails than normal

**When to Use**:
- Small sample sizes (n < 30)
- Population standard deviation unknown
- Confidence intervals and hypothesis tests

### 6. Chi-Square Distribution

**Definition**: Sum of squared standard normal variables

**Parameter**: k (degrees of freedom)

**Properties**:
- Always positive (X > 0)
- Right-skewed
- Mean = k, Variance = 2k

**When to Use**:
- Testing variance
- Goodness-of-fit tests
- Tests of independence in contingency tables

### 7. F-Distribution

**Definition**: Ratio of two chi-square distributions

**Parameters**: d₁, d₂ (degrees of freedom)

**When to Use**:
- Comparing variances of two groups
- ANOVA (testing equality of multiple means)
- Regression analysis

## Choosing the Right Distribution

### Decision Framework

| Data Type | Characteristics | Likely Distribution |
|-----------|----------------|---------------------|
| **Count** | Number of successes in fixed trials | Binomial |
| **Count** | Number of rare events in interval | Poisson |
| **Count** | Trials until first success | Geometric |
| **Continuous** | Symmetric, bell-shaped | Normal |
| **Continuous** | Time until event | Exponential |
| **Continuous** | Positive, right-skewed | Log-Normal |
| **Continuous** | Uniform probabilities | Uniform |

## Central Limit Theorem (CLT)

**Statement**: For a sufficiently large sample size (typically n ≥ 30), the distribution of sample means approximates a normal distribution, regardless of the population's distribution.

**Formula**: If X₁, X₂, ..., Xₙ are independent with mean μ and variance σ²:

X̄ ~ N(μ, σ²/n) approximately for large n

**Implications**:
- Justifies using normal distribution for inference
- Explains why normal distribution is so common
- Enables hypothesis testing and confidence intervals

**Example**: Roll a die (uniform distribution)
- Single roll: Equal probability 1-6
- Average of 2 rolls: Starting to cluster around 3.5
- Average of 30 rolls: Nearly normal distribution around 3.5

## Real-World Examples

### Example 1: Quality Control (Binomial)

Factory produces microchips with 2% defect rate.
Sample 100 chips.

**Question**: Probability of finding 0, 1, or 2 defects?

**Solution**:
- X ~ Binomial(n=100, p=0.02)
- E(X) = 100 × 0.02 = 2 defects expected
- P(X ≤ 2) = P(X=0) + P(X=1) + P(X=2) = 0.677

About 68% of samples will have 0-2 defects.

### Example 2: Call Center (Poisson)

Call center receives average 15 calls per hour.

**Question**: Probability of receiving 20+ calls in an hour?

**Solution**:
- X ~ Poisson(λ=15)
- P(X ≥ 20) = 1 - P(X ≤ 19) ≈ 0.083

About 8.3% chance of 20+ calls in an hour.

### Example 3: Test Scores (Normal)

SAT scores: μ = 1050, σ = 200

**Question**: What score represents 90th percentile?

**Solution**:
- Find z-score for 90th percentile: z ≈ 1.28
- X = μ + zσ = 1050 + 1.28(200) = 1306

A score of 1306 is at the 90th percentile.

### Example 4: Product Lifetime (Exponential)

Light bulbs last on average 1000 hours.

**Question**: Probability bulb lasts more than 1500 hours?

**Solution**:
- λ = 1/1000 = 0.001 per hour
- P(X > 1500) = e^(-λ×1500) = e^(-1.5) ≈ 0.223

About 22.3% of bulbs last more than 1500 hours.

### Example 5: Income Distribution (Log-Normal)

If log-income is normal with μ = 10.5, σ = 0.5:

**Question**: What's median income?

**Solution**:
- Median of log-normal = e^μ
- Median income = e^10.5 ≈ $36,316

Half the population earns less than $36,316.

## Relationships Between Distributions

```
Bernoulli (p)
    ↓ (n trials)
Binomial (n, p)
    ↓ (n large, p small, np = λ)
Poisson (λ)

Geometric (p) ← discrete time
    ↓ (continuous time)
Exponential (λ)

Normal (μ, σ²)
    ↑ (Central Limit Theorem)
Many distributions

Z² (Z ~ N(0,1))
    ↓
Chi-square (k=1)
    ↓ (sum k independent)
Chi-square (k)
```

## Key Terms

| Term | Definition |
|------|------------|
| **PMF** | Probability Mass Function (for discrete distributions) |
| **PDF** | Probability Density Function (for continuous distributions) |
| **CDF** | Cumulative Distribution Function, P(X ≤ x) |
| **Expected Value** | Long-run average value, E(X) or μ |
| **Variance** | Measure of spread, Var(X) or σ² |
| **Standard Deviation** | Square root of variance, σ |
| **Parameter** | Value that defines a distribution (e.g., p, λ, μ, σ) |
| **Memoryless** | Past doesn't affect future probabilities |
| **Support** | Set of values where probability/density is non-zero |
| **Quantile** | Value below which a percentage of data falls |

## Summary

Probability distributions provide mathematical models for random phenomena. Discrete distributions (Binomial, Poisson, Geometric) model counts and categorical outcomes, while continuous distributions (Normal, Exponential, Log-Normal) model measurements and time.

The Normal distribution holds special importance due to the Central Limit Theorem, which explains why it appears so frequently in nature and justifies many statistical procedures.

Choosing the right distribution depends on the nature of your data - whether it's discrete or continuous, bounded or unbounded, symmetric or skewed. Understanding distributions enables you to model real-world processes, calculate probabilities, and conduct statistical inference.

Each distribution has specific parameters (like λ for Poisson or μ and σ for Normal) that determine its shape and characteristics. Knowing these properties allows you to make predictions and draw conclusions from data.
