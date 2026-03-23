# Descriptive Statistics

## Overview

Descriptive statistics summarize and describe the main features of a dataset. Rather than making inferences about a larger population, descriptive statistics focus on organizing, displaying, and characterizing the data you have. This chapter covers measures of central tendency, variability, position, and shape that form the foundation of data analysis.

## Measures of Central Tendency

Central tendency describes the "typical" or "central" value in a dataset.

### 1. Mean (Arithmetic Average)

**Formula**: μ = (Σx) / n or x̄ = (Σx) / n

**Properties**:
- Uses all data values
- Affected by outliers
- Sum of deviations from mean equals zero: Σ(x - x̄) = 0

**When to Use**:
- Symmetric distributions without outliers
- Interval or ratio data
- When you need to do further calculations

**Example**:
Test scores: 85, 90, 78, 92, 88
Mean = (85 + 90 + 78 + 92 + 88) / 5 = 86.6

### 2. Median

**Definition**: Middle value when data is ordered

**Calculation**:
- If n is odd: median is the middle value
- If n is even: median is average of two middle values

**Properties**:
- Not affected by outliers (robust)
- Divides data into two equal halves
- Better than mean for skewed distributions

**When to Use**:
- Skewed distributions
- Data with outliers
- Ordinal data
- Income, house prices, and other right-skewed data

**Example**:
Salaries: $40k, $45k, $50k, $52k, $200k
Median = $50k (middle value)
Mean = $77.4k (pulled up by outlier)

### 3. Mode

**Definition**: Most frequently occurring value

**Properties**:
- Can have multiple modes (bimodal, multimodal)
- May not exist (all values unique)
- Only measure that works for nominal data

**When to Use**:
- Categorical data
- Finding most common value
- Understanding multi-peaked distributions

**Example**:
Shoe sizes: 7, 8, 8, 8, 9, 9, 10
Mode = 8 (appears most frequently)

### Comparison of Central Tendency Measures

| Distribution | Best Measure | Relationship |
|--------------|--------------|--------------|
| **Symmetric** | Mean = Median = Mode | All three equal |
| **Right-skewed** | Median | Mean > Median > Mode |
| **Left-skewed** | Median | Mode > Median > Mean |
| **Bimodal** | Mode | Multiple peaks |
| **With outliers** | Median | Robust to extremes |

## Measures of Variability (Dispersion)

Variability measures how spread out data values are.

### 1. Range

**Formula**: Range = Maximum - Minimum

**Properties**:
- Simplest measure
- Uses only two values
- Heavily affected by outliers

**Example**:
Test scores: 65, 70, 75, 80, 95
Range = 95 - 65 = 30

### 2. Interquartile Range (IQR)

**Formula**: IQR = Q₃ - Q₁

**Definition**: Range of the middle 50% of data

**Properties**:
- Robust to outliers
- Uses quartiles (25th and 75th percentiles)
- Used in boxplots

**Example**:
Data: 10, 15, 20, 25, 30, 35, 40, 45, 50
Q₁ = 17.5, Q₃ = 42.5
IQR = 42.5 - 17.5 = 25

### 3. Variance

**Population Variance**: σ² = Σ(x - μ)² / N

**Sample Variance**: s² = Σ(x - x̄)² / (n - 1)

**Properties**:
- Uses all data values
- Squared units (hard to interpret directly)
- Foundation for many statistical methods
- Always non-negative

**Why n-1 for Sample?**:
- Provides unbiased estimate of population variance
- Called "degrees of freedom" adjustment
- Corrects for using sample mean instead of population mean

### 4. Standard Deviation

**Population**: σ = √σ²

**Sample**: s = √s²

**Properties**:
- Same units as original data (interpretable)
- Measures average distance from mean
- Affected by outliers
- Most commonly used variability measure

**Interpretation**:
- Small SD: Data clustered near mean
- Large SD: Data widely spread

**Example**:
Test scores: 85, 90, 78, 92, 88
Mean = 86.6
Variance = [(85-86.6)² + (90-86.6)² + (78-86.6)² + (92-86.6)² + (88-86.6)²] / 4
= [2.56 + 11.56 + 73.96 + 29.16 + 1.96] / 4
= 119.2 / 4 = 29.8
Standard Deviation = √29.8 ≈ 5.46

### 5. Coefficient of Variation (CV)

**Formula**: CV = (σ / μ) × 100%

**Purpose**: Compare variability across datasets with different units or scales

**Example**:
- Heights: Mean = 68 inches, SD = 3 inches → CV = 4.4%
- Weights: Mean = 170 lbs, SD = 20 lbs → CV = 11.8%
- Weights have relatively more variability

## Measures of Position

### Percentiles

**Definition**: Value below which a given percentage of observations fall

**Common Percentiles**:
- 25th percentile (Q₁): First quartile
- 50th percentile (Q₂): Median
- 75th percentile (Q₃): Third quartile

**Example**: 90th percentile SAT score of 1300 means 90% of test-takers scored below 1300.

### Quartiles

| Quartile | Percentile | Meaning |
|----------|------------|---------|
| **Q₁** | 25th | 25% of data below this value |
| **Q₂** | 50th | Median |
| **Q₃** | 75th | 75% of data below this value |

**Five-Number Summary**:
1. Minimum
2. Q₁
3. Median (Q₂)
4. Q₃
5. Maximum

### Z-Scores (Standard Scores)

**Formula**: z = (x - μ) / σ

**Interpretation**:
- z = 0: Value equals the mean
- z = 1: Value is 1 SD above mean
- z = -2: Value is 2 SD below mean

**Properties**:
- Standardized (mean = 0, SD = 1)
- Enables comparison across different scales
- Identifies outliers (|z| > 3 unusual)

**Example**:
Test score = 92, μ = 80, σ = 10
z = (92 - 80) / 10 = 1.2
Score is 1.2 standard deviations above average.

## Measures of Shape

### Skewness

**Definition**: Measure of asymmetry in distribution

**Types**:
- **Right-skewed (positive)**: Long right tail, mean > median
  - Examples: Income, house prices, lifespan
- **Left-skewed (negative)**: Long left tail, mean < median
  - Examples: Age at retirement, test scores with ceiling effect
- **Symmetric**: Mean ≈ median
  - Example: Height, IQ (approximately normal)

### Kurtosis

**Definition**: Measure of "tailedness" of distribution

**Types**:
- **Leptokurtic**: Heavy tails, more outliers (kurtosis > 3)
- **Mesokurtic**: Normal-like tails (kurtosis = 3)
- **Platykurtic**: Light tails, fewer outliers (kurtosis < 3)

## Outlier Detection

### Methods

| Method | Formula | Interpretation |
|--------|---------|----------------|
| **IQR Method** | < Q₁ - 1.5×IQR or > Q₃ + 1.5×IQR | Standard boxplot rule |
| **Z-Score Method** | \|z\| > 3 | More than 3 SD from mean |
| **Modified Z-Score** | Uses median and MAD | Robust to outliers |

**Example**:
Data: 10, 12, 15, 18, 20, 23, 100
Q₁ = 12, Q₃ = 23, IQR = 11
Upper fence = 23 + 1.5(11) = 39.5
100 > 39.5, so 100 is an outlier

## Data Visualization for Descriptive Statistics

### Boxplot (Box-and-Whisker Plot)

**Components**:
- Box: Q₁ to Q₃ (IQR)
- Line in box: Median
- Whiskers: Extend to min/max (within 1.5×IQR)
- Points beyond whiskers: Outliers

**Interpretation**:
- Shows center, spread, skewness, and outliers at a glance
- Ideal for comparing multiple groups

### Histogram

**Purpose**: Show distribution shape and frequency

**Components**:
- X-axis: Bins (intervals of values)
- Y-axis: Frequency or density
- Bars: Height represents count/density in each bin

**Interpretation**:
- Symmetric, skewed, or multimodal?
- Where is the center?
- How spread out?

### Summary Statistics Table

| Statistic | Formula/Description | Interpretation |
|-----------|---------------------|----------------|
| n | Sample size | Number of observations |
| Mean | Σx / n | Average value |
| Median | Middle value | Center (robust) |
| SD | √[Σ(x-x̄)²/(n-1)] | Typical deviation |
| Min | Smallest value | Lower bound |
| Q₁ | 25th percentile | Lower quartile |
| Q₃ | 75th percentile | Upper quartile |
| Max | Largest value | Upper bound |
| Range | Max - Min | Total spread |
| IQR | Q₃ - Q₁ | Middle 50% spread |

## Real-World Examples

### Example 1: Comparing Two Classes

**Class A Test Scores**: 75, 80, 82, 85, 88, 90, 92
**Class B Test Scores**: 60, 70, 85, 85, 85, 100, 100

| Statistic | Class A | Class B |
|-----------|---------|---------|
| Mean | 84.6 | 83.6 |
| Median | 85 | 85 |
| Mode | None | 85, 100 |
| Range | 17 | 40 |
| SD | 5.8 | 14.7 |

**Interpretation**:
- Similar averages but Class B much more variable
- Class A consistent performance
- Class B bimodal (two groups: struggling and excelling)

### Example 2: Income Distribution

**Data**: Annual incomes in thousands
$35, $42, $45, $48, $51, $55, $58, $62, $250

| Statistic | Value |
|-----------|-------|
| Mean | $71.8k |
| Median | $51k |
| Range | $215k |
| IQR | $16k |

**Interpretation**:
- Mean > Median indicates right skew
- $250k outlier pulls mean up
- Median ($51k) better represents "typical" income
- IQR shows middle 50% within $16k range

### Example 3: Quality Control

Manufacturing process produces bolts with target diameter 10mm.
Sample measurements: 9.8, 10.1, 10.0, 9.9, 10.2, 10.1, 10.0

| Statistic | Value |
|-----------|-------|
| Mean | 10.01mm |
| SD | 0.13mm |
| Range | 0.4mm |

**Interpretation**:
- Process well-centered (mean ≈ target)
- Low variability (SD = 0.13mm)
- Quality appears consistent

### Example 4: Website Performance

Page load times (seconds): 1.2, 1.5, 1.8, 2.0, 2.1, 2.3, 8.5

| Statistic | Value |
|-----------|-------|
| Mean | 2.77s |
| Median | 2.0s |
| Without outlier | 1.82s (mean) |

**Interpretation**:
- 8.5s is an outlier (perhaps slow connection)
- Median (2.0s) better represents typical experience
- Report both: "Median load time 2.0s, with some users experiencing up to 8.5s"

### Example 5: Student Heights

Heights of 30 students (inches): 62-74 range

| Statistic | Value |
|-----------|-------|
| Mean | 68.2 |
| Median | 68.0 |
| SD | 3.1 |
| 68% within | 65.1 - 71.3 |
| 95% within | 62.0 - 74.4 |

**Interpretation**:
- Nearly symmetric (mean ≈ median)
- Follows 68-95-99.7 rule (approximately normal)
- Most students within 3 inches of mean

## Grouped Data

When data is presented in frequency tables:

**Mean**: x̄ = Σ(f × midpoint) / Σf

**Variance**: s² = [Σf(x - x̄)²] / (n - 1)

Where f = frequency of each class

**Example**:

| Class | Frequency | Midpoint | f × midpoint |
|-------|-----------|----------|--------------|
| 0-10 | 5 | 5 | 25 |
| 10-20 | 12 | 15 | 180 |
| 20-30 | 8 | 25 | 200 |
| Total | 25 | - | 405 |

Mean = 405 / 25 = 16.2

## Choosing the Right Statistics

| Data Type | Central Tendency | Variability | Position |
|-----------|------------------|-------------|----------|
| **Nominal** | Mode | - | Proportions |
| **Ordinal** | Median, Mode | IQR, Range | Percentiles |
| **Interval/Ratio (Symmetric)** | Mean | SD, Variance | Z-scores |
| **Interval/Ratio (Skewed)** | Median | IQR | Percentiles |
| **With Outliers** | Median | IQR | Percentiles |

## Key Terms

| Term | Definition |
|------|------------|
| **Mean** | Arithmetic average, sum divided by count |
| **Median** | Middle value when data is ordered |
| **Mode** | Most frequently occurring value |
| **Range** | Difference between maximum and minimum |
| **Variance** | Average squared deviation from mean |
| **Standard Deviation** | Square root of variance, typical distance from mean |
| **IQR** | Interquartile range, spread of middle 50% of data |
| **Percentile** | Value below which a percentage of data falls |
| **Quartile** | Divides data into four equal parts |
| **Z-Score** | Number of standard deviations from the mean |
| **Outlier** | Data point that differs significantly from other observations |
| **Skewness** | Measure of asymmetry in distribution |

## Summary

Descriptive statistics provide tools to summarize, describe, and visualize data without making inferences beyond the observed data. Measures of central tendency (mean, median, mode) describe typical values, while measures of variability (range, IQR, standard deviation) describe spread.

Choosing appropriate statistics depends on data type, distribution shape, and presence of outliers. For symmetric data without outliers, use mean and standard deviation. For skewed data or data with outliers, use median and IQR.

Visual tools like boxplots and histograms complement numerical summaries, revealing distribution shape, outliers, and patterns. Together, these descriptive tools provide a comprehensive picture of your data, forming the foundation for further statistical analysis.

Understanding descriptive statistics enables you to communicate findings clearly, identify data quality issues, and make informed decisions about which inferential methods to apply next.
