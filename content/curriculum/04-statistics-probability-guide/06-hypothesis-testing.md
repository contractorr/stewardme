# Hypothesis Testing

## Overview

Hypothesis testing is a formal procedure for using sample data to evaluate claims about population parameters. Rather than estimating a parameter (confidence intervals), we test whether evidence supports or contradicts a specific claim. This chapter covers the logic of hypothesis testing, test procedures, p-values, error types, and power.

## The Logic of Hypothesis Testing

### Basic Concept
**Question**: Does our sample provide sufficient evidence to reject a claim about the population?

**Approach**: Assume the claim is true, then determine how unusual our sample data would be under that assumption.

**Decision**: If data is too unusual (unlikely) under the claim, reject the claim.

### Legal Analogy
- **Null hypothesis**: Defendant is innocent (status quo)
- **Alternative hypothesis**: Defendant is guilty (what we suspect)
- **Evidence**: Sample data
- **Verdict**: Reject or fail to reject innocence based on evidence
- **Standard**: "Beyond reasonable doubt" (similar to significance level)

## Hypotheses

### Null Hypothesis (H₀)
- Statement of "no effect" or "no difference"
- Status quo or claim being tested
- Always contains equality (=, ≤, ≥)
- What we assume true until proven otherwise

**Examples**:
- H₀: μ = 100 (mean equals specific value)
- H₀: μ₁ = μ₂ (two means are equal)
- H₀: p = 0.5 (proportion equals 0.5)

### Alternative Hypothesis (H₁ or Hₐ)
- What we suspect might be true
- Claim we're trying to find evidence for
- Contains inequality (<, >, ≠)
- Research hypothesis

**Examples**:
- H₁: μ ≠ 100 (mean differs from 100)
- H₁: μ > 100 (mean is greater than 100)
- H₁: μ < 100 (mean is less than 100)

### Types of Tests

| Type | Alternative Hypothesis | When to Use |
|------|----------------------|-------------|
| **Two-tailed** | H₁: μ ≠ μ₀ | Interested in any difference |
| **Right-tailed** | H₁: μ > μ₀ | Testing if greater than |
| **Left-tailed** | H₁: μ < μ₀ | Testing if less than |

## The Hypothesis Testing Process

### Step 1: State Hypotheses
Define H₀ and H₁ clearly

### Step 2: Choose Significance Level (α)
- Commonly α = 0.05
- Probability of Type I error
- Threshold for "unusual"

### Step 3: Calculate Test Statistic
Transform sample data into standardized value:

**z-test (σ known)**: z = (x̄ - μ₀) / (σ/√n)

**t-test (σ unknown)**: t = (x̄ - μ₀) / (s/√n)

**z-test for proportion**: z = (p̂ - p₀) / √[p₀(1-p₀)/n]

### Step 4: Find p-value
Probability of obtaining test statistic at least as extreme as observed, assuming H₀ is true

### Step 5: Make Decision
- If p-value ≤ α: Reject H₀ (statistically significant)
- If p-value > α: Fail to reject H₀ (not statistically significant)

### Step 6: Interpret in Context
State conclusion in terms of original problem

## P-Values

### Definition
**p-value** = Probability of observing data at least as extreme as what we got, if H₀ were true

### Interpretation

| p-value | Interpretation |
|---------|----------------|
| < 0.01 | Very strong evidence against H₀ |
| 0.01 - 0.05 | Strong evidence against H₀ |
| 0.05 - 0.10 | Moderate evidence against H₀ |
| > 0.10 | Little to no evidence against H₀ |

**Key Points**:
- Smaller p-value = stronger evidence against H₀
- p-value is NOT probability that H₀ is true
- p-value is NOT probability of Type I error (that's α)
- p-value depends on sample data

### Calculating p-values

**Two-tailed test**: p-value = 2 × P(Z > |z|)
**Right-tailed test**: p-value = P(Z > z)
**Left-tailed test**: p-value = P(Z < z)

**Example**: Two-tailed test, z = 2.3
p-value = 2 × P(Z > 2.3) = 2 × 0.0107 = 0.0214

## Significance Level (α)

### Definition
**Significance level** = Maximum acceptable probability of Type I error

### Common Values
- α = 0.05 (most common)
- α = 0.01 (more conservative)
- α = 0.10 (more lenient)

### Relationship to p-value
**Decision Rule**:
- p-value ≤ α → Reject H₀
- p-value > α → Fail to reject H₀

### Critical Values
Values that divide rejection region from non-rejection region

| Test Type | α = 0.05 | α = 0.01 |
|-----------|----------|----------|
| **Two-tailed (z)** | ±1.96 | ±2.576 |
| **Right-tailed (z)** | 1.645 | 2.326 |
| **Left-tailed (z)** | -1.645 | -2.326 |

## Types of Errors

### Type I Error (False Positive)
- **Definition**: Reject H₀ when H₀ is actually true
- **Probability**: α (significance level)
- **Example**: Conclude drug is effective when it isn't
- **Consequence**: False alarm, wasted resources

### Type II Error (False Negative)
- **Definition**: Fail to reject H₀ when H₀ is actually false
- **Probability**: β (beta)
- **Example**: Conclude drug isn't effective when it is
- **Consequence**: Missed opportunity, overlooking real effect

### Error Trade-offs

|  | H₀ True | H₀ False |
|--|---------|----------|
| **Reject H₀** | Type I Error (α) | Correct Decision (Power = 1-β) |
| **Fail to Reject H₀** | Correct Decision (1-α) | Type II Error (β) |

**Key Insight**: Decreasing α (more conservative) increases β (miss real effects)

### Choosing Error Priorities

| Context | Priority | Approach |
|---------|----------|----------|
| **Drug Approval** | Minimize Type I (don't approve ineffective drug) | Small α (0.01) |
| **Disease Screening** | Minimize Type II (don't miss disease) | Larger α (0.10) |
| **Quality Control** | Balance both | Standard α (0.05) |

## Power

### Definition
**Power** = Probability of correctly rejecting H₀ when it's false = 1 - β

### Interpretation
- Power = 0.80 means 80% chance of detecting real effect if it exists
- Higher power is better
- Typically aim for power ≥ 0.80

### Factors Affecting Power

| Factor | Effect on Power |
|--------|----------------|
| **Larger sample size** | Increases power |
| **Larger effect size** | Increases power |
| **Larger α** | Increases power |
| **Smaller variability** | Increases power |

**Trade-off**: Want high power but must balance with Type I error rate

## Common Hypothesis Tests

### 1. One-Sample z-Test for Mean

**When**: Testing population mean, σ known, large sample

**Hypotheses**: H₀: μ = μ₀

**Test Statistic**: z = (x̄ - μ₀) / (σ/√n)

**Assumptions**:
- Random sample
- Population normal or n ≥ 30
- σ known

### 2. One-Sample t-Test for Mean

**When**: Testing population mean, σ unknown

**Hypotheses**: H₀: μ = μ₀

**Test Statistic**: t = (x̄ - μ₀) / (s/√n), df = n-1

**Assumptions**:
- Random sample
- Population approximately normal (especially for small n)
- σ unknown (estimate with s)

### 3. One-Sample z-Test for Proportion

**When**: Testing population proportion

**Hypotheses**: H₀: p = p₀

**Test Statistic**: z = (p̂ - p₀) / √[p₀(1-p₀)/n]

**Assumptions**:
- Random sample
- np₀ ≥ 10 and n(1-p₀) ≥ 10

### 4. Two-Sample t-Test

**When**: Comparing two population means

**Hypotheses**: H₀: μ₁ = μ₂ (or μ₁ - μ₂ = 0)

**Test Statistic**: t = (x̄₁ - x̄₂) / SE, where SE depends on variance assumption

**Assumptions**:
- Independent random samples
- Both populations approximately normal
- Equal or unequal variances (affects SE calculation)

### 5. Paired t-Test

**When**: Comparing means of paired observations

**Hypotheses**: H₀: μ_d = 0 (mean difference = 0)

**Test Statistic**: t = d̄ / (s_d/√n), where d̄ = mean of differences

**Use Cases**:
- Before/after measurements
- Matched pairs
- Repeated measures on same subjects

### 6. Chi-Square Goodness-of-Fit Test

**When**: Testing if categorical data fits expected distribution

**Hypotheses**: H₀: Data follows specified distribution

**Test Statistic**: χ² = Σ[(Observed - Expected)² / Expected]

**Use Cases**:
- Are die rolls fair?
- Do outcomes match theoretical probabilities?

### 7. Chi-Square Test of Independence

**When**: Testing relationship between two categorical variables

**Hypotheses**: H₀: Variables are independent

**Test Statistic**: χ² = Σ[(O - E)² / E] for all cells

**Use Cases**:
- Is gender related to voting preference?
- Is treatment related to outcome?

## Real-World Examples

### Example 1: Drug Effectiveness

**Claim**: New pain reliever works in less than 30 minutes (μ < 30)

**Sample**: n = 40, x̄ = 27.5 minutes, s = 8 minutes

**Hypotheses**:
- H₀: μ = 30 (drug doesn't work faster)
- H₁: μ < 30 (drug works faster) [left-tailed]

**Test Statistic**:
t = (27.5 - 30) / (8/√40) = -2.5 / 1.265 = -1.976
df = 39

**p-value**: P(t < -1.976) ≈ 0.028

**Decision** (α = 0.05): p < 0.05, reject H₀

**Conclusion**: Strong evidence drug works in less than 30 minutes.

### Example 2: Coin Fairness

**Claim**: Coin is fair (p = 0.5)

**Sample**: Flip 100 times, 62 heads (p̂ = 0.62)

**Hypotheses**:
- H₀: p = 0.5 (coin is fair)
- H₁: p ≠ 0.5 (coin is not fair) [two-tailed]

**Test Statistic**:
z = (0.62 - 0.5) / √[0.5(0.5)/100] = 0.12 / 0.05 = 2.4

**p-value**: 2 × P(Z > 2.4) = 2 × 0.0082 = 0.0164

**Decision** (α = 0.05): p < 0.05, reject H₀

**Conclusion**: Evidence suggests coin is not fair.

### Example 3: Weight Loss Program

**Claim**: Program results in weight loss

**Sample**: 25 people, mean loss = 8 lbs, s = 12 lbs

**Hypotheses**:
- H₀: μ = 0 (no weight loss)
- H₁: μ > 0 (weight loss occurs) [right-tailed]

**Test Statistic**:
t = (8 - 0) / (12/√25) = 8 / 2.4 = 3.33
df = 24

**p-value**: P(t > 3.33) ≈ 0.001

**Decision** (α = 0.05): p < 0.05, reject H₀

**Conclusion**: Very strong evidence program causes weight loss.

### Example 4: Before/After Training (Paired)

**Claim**: Training improves test scores

**Sample**: 20 employees tested before and after

| Person | Before | After | Difference |
|--------|--------|-------|------------|
| Mean | 72 | 78 | 6 |
| SD | - | - | 8 |

**Hypotheses**:
- H₀: μ_d = 0 (no improvement)
- H₁: μ_d > 0 (improvement)

**Test Statistic**:
t = 6 / (8/√20) = 6 / 1.789 = 3.35
df = 19

**p-value**: P(t > 3.35) ≈ 0.002

**Decision**: Reject H₀

**Conclusion**: Training significantly improves scores.

### Example 5: Gender and Product Preference

**Claim**: Product preference independent of gender

**Data**:
|  | Prefer A | Prefer B | Total |
|--|----------|----------|-------|
| **Male** | 30 | 20 | 50 |
| **Female** | 15 | 35 | 50 |
| **Total** | 45 | 55 | 100 |

**Hypotheses**:
- H₀: Preference and gender are independent
- H₁: Preference and gender are related

**Expected Frequencies** (if independent):
Male-A: 50×45/100 = 22.5

**Test Statistic**:
χ² = (30-22.5)²/22.5 + ... = 11.11
df = (2-1)(2-1) = 1

**p-value**: P(χ² > 11.11) < 0.001

**Decision**: Reject H₀

**Conclusion**: Strong relationship between gender and preference.

## Effect Size

### Beyond Statistical Significance

**Problem**: With large samples, tiny differences become "statistically significant"

**Solution**: Report effect size - practical significance

### Common Effect Size Measures

| Measure | Formula | Interpretation |
|---------|---------|----------------|
| **Cohen's d** | d = (x̄₁ - x̄₂) / s_pooled | Standardized mean difference |
| **r² (R-squared)** | Proportion of variance explained | 0 to 1 |
| **Odds Ratio** | (odds in group 1) / (odds in group 2) | For categorical outcomes |

**Cohen's d Guidelines**:
- d = 0.2: Small effect
- d = 0.5: Medium effect
- d = 0.8: Large effect

**Example**:
- Group 1: x̄ = 100, Group 2: x̄ = 95, s = 10
- Cohen's d = (100 - 95) / 10 = 0.5 (medium effect)

## Statistical Significance vs. Practical Significance

| Statistical Significance | Practical Significance |
|-------------------------|------------------------|
| Determined by p-value | Determined by effect size and context |
| Affected by sample size | Independent of sample size |
| "Is there an effect?" | "Does the effect matter?" |
| Objective | Subjective/contextual |

**Example**:
Drug lowers blood pressure by 1 mmHg (p < 0.001)
- Statistically significant? Yes
- Practically significant? Probably not (too small to matter clinically)

## Common Mistakes and Misconceptions

### 1. Accepting H₀
❌ "Fail to reject H₀" does NOT mean "accept H₀" or "prove H₀ true"
✅ Lack of evidence against H₀ ≠ evidence for H₀

### 2. p-value = P(H₀ true)
❌ p-value is NOT probability that H₀ is true
✅ p-value is probability of data (or more extreme) given H₀ is true

### 3. Multiple Testing
❌ Conducting many tests increases false positives
✅ Use corrections (Bonferroni) or adjust α

### 4. Cherry-Picking
❌ Testing many hypotheses, reporting only significant ones
✅ Pre-specify hypotheses, report all tests

### 5. p-hacking
❌ Trying different analyses until finding p < 0.05
✅ Pre-register analysis plan

## Key Terms

| Term | Definition |
|------|------------|
| **Null Hypothesis (H₀)** | Statement of no effect or no difference, assumed true |
| **Alternative Hypothesis (H₁)** | Statement we're seeking evidence for |
| **p-value** | Probability of observing data as extreme as ours, given H₀ is true |
| **Significance Level (α)** | Threshold for rejecting H₀, probability of Type I error |
| **Type I Error** | Rejecting H₀ when it's true (false positive) |
| **Type II Error** | Failing to reject H₀ when it's false (false negative) |
| **Power** | Probability of correctly rejecting false H₀, equals 1-β |
| **Test Statistic** | Standardized value calculated from sample data |
| **Critical Value** | Boundary value for rejection region |
| **Effect Size** | Magnitude of difference or relationship |
| **One-tailed Test** | Alternative hypothesis in one direction only |
| **Two-tailed Test** | Alternative hypothesis in either direction |

## Summary

Hypothesis testing provides a formal framework for evaluating claims about populations using sample data. We start by assuming the null hypothesis (status quo) is true, then determine whether our data is too unusual under that assumption.

The p-value quantifies this unusualness - how likely we'd observe data at least as extreme as ours if H₀ were true. Small p-values (below α) provide evidence against H₀, leading us to reject it in favor of the alternative hypothesis.

Two types of errors are possible: Type I (false positive, rejecting true H₀) with probability α, and Type II (false negative, missing real effect) with probability β. Power (1-β) represents our ability to detect real effects.

Statistical significance (p < α) doesn't guarantee practical importance. Always consider effect size and context. Large samples can make trivial differences "significant," while important effects in small samples may not reach significance.

The hypothesis testing framework - with its formal hypotheses, test statistics, p-values, and error types - provides a rigorous approach to evidence-based decision making, balancing the risks of false positives and false negatives according to the consequences in specific contexts.
