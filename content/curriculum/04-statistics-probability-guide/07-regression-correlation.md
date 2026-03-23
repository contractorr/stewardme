# Regression and Correlation

## Overview

Regression and correlation analyze relationships between variables. Correlation measures the strength and direction of linear relationships, while regression models how one variable predicts another. These tools are fundamental for understanding associations, making predictions, and identifying causal relationships. This chapter covers correlation coefficients, simple and multiple regression, model assessment, and common pitfalls.

## Correlation

### Definition
Correlation measures the strength and direction of the **linear** relationship between two quantitative variables.

### Correlation Coefficient (r)

**Pearson's Correlation Coefficient**: r = Σ[(x - x̄)(y - ȳ)] / √[Σ(x - x̄)² × Σ(y - ȳ)²]

**Properties**:
- Range: -1 ≤ r ≤ 1
- r = 1: Perfect positive linear relationship
- r = -1: Perfect negative linear relationship
- r = 0: No linear relationship
- Sign indicates direction (positive/negative)
- Magnitude indicates strength

### Interpreting Correlation Strength

| |r| Value | Interpretation |
|-----------|----------------|
| 0.00 - 0.19 | Very weak |
| 0.20 - 0.39 | Weak |
| 0.40 - 0.59 | Moderate |
| 0.60 - 0.79 | Strong |
| 0.80 - 1.00 | Very strong |

**Note**: These are guidelines; context matters!

### Visual Examples

**r = 0.9** (strong positive): As x increases, y increases consistently

**r = -0.8** (strong negative): As x increases, y decreases consistently

**r = 0.1** (very weak): Points scattered with little pattern

**r = 0** (no correlation): No linear pattern (may have non-linear relationship!)

### Important Properties

**1. Correlation ≠ Causation**
- Strong correlation doesn't imply one causes the other
- May be confounding variables
- May be reverse causation
- May be spurious (coincidental)

**2. Outliers Affect Correlation**
- Single extreme point can greatly change r
- Always visualize data (scatterplot)

**3. Only Measures Linear Relationships**
- r = 0 doesn't mean no relationship
- May be strong non-linear relationship (parabolic, exponential)

**4. Unitless and Symmetric**
- r(x,y) = r(y,x)
- Doesn't change with scale or units

### Testing Correlation Significance

**Hypotheses**:
- H₀: ρ = 0 (no linear correlation in population)
- H₁: ρ ≠ 0 (linear correlation exists)

**Test Statistic**: t = r√[(n-2)/(1-r²)], df = n-2

**Example**: n = 30, r = 0.45
t = 0.45√[28/0.7975] = 2.67, p < 0.05
Conclusion: Significant positive correlation

## Simple Linear Regression

### Purpose
Model relationship between:
- **Response variable** (y): What we want to predict/explain
- **Predictor variable** (x): What we use to predict

### Regression Equation

**Population**: y = β₀ + β₁x + ε
**Sample**: ŷ = b₀ + b₁x

Where:
- ŷ = predicted value of y
- b₀ = y-intercept (predicted y when x = 0)
- b₁ = slope (change in y per unit change in x)
- ε = error term (residual)

### Least Squares Method

**Goal**: Minimize sum of squared residuals: Σ(y - ŷ)²

**Slope**: b₁ = r × (s_y / s_x)

**Intercept**: b₀ = ȳ - b₁x̄

**Properties**:
- Regression line always passes through (x̄, ȳ)
- Unique best-fit line

### Interpreting Regression Coefficients

**Slope (b₁)**:
- "For each 1-unit increase in x, y changes by b₁ units (on average)"
- Example: b₁ = 2.5 → "Each additional study hour increases test score by 2.5 points"

**Intercept (b₀)**:
- "Predicted y when x = 0"
- Often not meaningful if x = 0 is outside data range or impossible
- Example: b₀ = 40 → "Predicted score with 0 study hours is 40"

### Residuals

**Definition**: residual = observed - predicted = y - ŷ

**Properties**:
- Positive residual: actual value above prediction
- Negative residual: actual value below prediction
- Sum of residuals = 0
- Used for model diagnostics

### Assumptions of Linear Regression

| Assumption | Description | Check Using |
|------------|-------------|-------------|
| **Linearity** | Relationship between x and y is linear | Scatterplot, residual plot |
| **Independence** | Observations are independent | Study design |
| **Normality** | Residuals are normally distributed | Histogram, Q-Q plot of residuals |
| **Equal Variance** | Variance of residuals constant (homoscedasticity) | Residual plot |

**Residual Plot**: Plot residuals vs. fitted values (ŷ)
- Should show random scatter
- No patterns, no funnel shape
- Points roughly centered on zero

## Coefficient of Determination (R²)

### Definition
**R²** = Proportion of variance in y explained by x

**Formula**: R² = 1 - (SS_residual / SS_total)

Or for simple regression: R² = r²

**Range**: 0 ≤ R² ≤ 1

### Interpretation

| R² Value | Interpretation |
|----------|----------------|
| 0.90 | 90% of variance explained, excellent fit |
| 0.70 | 70% explained, good fit |
| 0.50 | 50% explained, moderate fit |
| 0.25 | 25% explained, weak fit |

**Example**: R² = 0.64
- 64% of variation in y explained by x
- 36% due to other factors

**Important**: High R² doesn't guarantee good model!
- Check residual plots
- Consider context
- Avoid overfitting

## Inference in Regression

### Testing Slope Significance

**Hypotheses**:
- H₀: β₁ = 0 (no linear relationship)
- H₁: β₁ ≠ 0 (linear relationship exists)

**Test Statistic**: t = b₁ / SE(b₁), df = n-2

**Interpretation**: Tests whether x is useful predictor of y

### Confidence Interval for Slope

**95% CI**: b₁ ± t* × SE(b₁)

**Interpretation**: Range of plausible values for true slope

**Example**: 95% CI for slope = [1.2, 3.8]
- Each additional x increases y by between 1.2 and 3.8 units (95% confidence)
- Since interval doesn't include 0, relationship is significant

### Prediction Intervals

**Point Prediction**: ŷ = b₀ + b₁x

**Prediction Interval**: ŷ ± t* × SE(prediction)

**Confidence Interval for Mean**: ŷ ± t* × SE(mean)

**Difference**:
- **Confidence interval**: Where average y is for given x
- **Prediction interval**: Where individual new y will be for given x (wider!)

## Real-World Examples

### Example 1: Study Hours vs. Test Scores

**Data**: 20 students

| Statistic | Value |
|-----------|-------|
| r | 0.75 |
| Regression equation | ŷ = 45 + 8x |
| R² | 0.56 |

**Interpretation**:
- Strong positive correlation (r = 0.75)
- Slope = 8: Each study hour increases score by 8 points
- Intercept = 45: Predicted score with 0 hours is 45
- R² = 0.56: Study hours explain 56% of score variance

**Prediction**: Student studies 5 hours
ŷ = 45 + 8(5) = 85 points

### Example 2: Advertising vs. Sales

**Data**: 50 weeks of data

| Variable | Value |
|----------|-------|
| Regression equation | Sales = 2.5 + 3.2(Advertising) |
| R² | 0.71 |
| SE(b₁) | 0.4 |
| t-statistic | 8.0 |
| p-value | <0.001 |

**Interpretation**:
- Each $1,000 in advertising increases sales by $3,200
- 71% of sales variance explained by advertising
- Slope highly significant (p < 0.001)
- Strong positive relationship

**Business Decision**: ROI = 3.2:1, advertising appears worthwhile

### Example 3: Age vs. Memory Score

**Data**: 100 adults aged 20-80

| Statistic | Value |
|-----------|-------|
| r | -0.68 |
| ŷ | 95 - 0.5(age) |
| R² | 0.46 |

**Interpretation**:
- Strong negative correlation
- Each year of age decreases memory score by 0.5 points
- Age explains 46% of memory variance
- Other factors (54%) also important

**Prediction**: 50-year-old
ŷ = 95 - 0.5(50) = 70 points

## Multiple Regression

### Purpose
Model y using **multiple** predictor variables: x₁, x₂, ..., xₖ

**Equation**: ŷ = b₀ + b₁x₁ + b₂x₂ + ... + bₖxₖ

### Advantages
- More realistic models
- Control for confounding variables
- Better predictions
- Understand relative importance of predictors

### Adjusted R²

**Problem**: R² always increases when adding variables (even irrelevant ones)

**Solution**: Adjusted R² = 1 - [(1-R²)(n-1)/(n-k-1)]

Where k = number of predictors

**Interpretation**: Penalizes for adding variables; only increases if new variable improves model

### Interpreting Coefficients

**Slope for x₁**: "Change in y for 1-unit increase in x₁, **holding other variables constant**"

**Example**: Salary = 30,000 + 2,000(Education) + 5,000(Experience)
- b₁ = 2,000: Each additional year of education increases salary by $2,000, holding experience constant
- b₂ = 5,000: Each additional year of experience increases salary by $5,000, holding education constant

### Variable Selection

**Methods**:
1. **Forward Selection**: Start with no variables, add one at a time
2. **Backward Elimination**: Start with all variables, remove one at a time
3. **Stepwise**: Combination of forward and backward

**Criteria**:
- Adjusted R²
- AIC (Akaike Information Criterion)
- BIC (Bayesian Information Criterion)
- Cross-validation error

### Multicollinearity

**Problem**: Predictor variables highly correlated with each other

**Consequences**:
- Unstable coefficient estimates
- Large standard errors
- Coefficients may have wrong signs

**Detection**:
- Correlation matrix of predictors
- Variance Inflation Factor (VIF > 10 problematic)

**Solutions**:
- Remove redundant variables
- Combine correlated variables
- Use dimension reduction (PCA)

## Logistic Regression

### When to Use
Response variable is **binary** (yes/no, success/failure)

**Examples**:
- Predict if customer will buy (yes/no)
- Predict if patient has disease (yes/no)
- Predict if email is spam (yes/no)

### Logistic Regression Equation

**Linear form**: log(p/(1-p)) = β₀ + β₁x₁ + ...

**Probability form**: p = e^(β₀ + β₁x₁) / (1 + e^(β₀ + β₁x₁))

Where p = probability of success

### Interpreting Coefficients

**Odds Ratio**: e^β₁
- OR = 2: Each unit increase in x doubles the odds of success
- OR = 0.5: Each unit increase in x halves the odds of success

**Example**: Predict loan default
log(odds of default) = -3 + 0.05(debt-to-income ratio)
- e^0.05 = 1.05: Each 1% increase in debt-to-income ratio increases default odds by 5%

## Polynomial Regression

### When to Use
Relationship between x and y is **curved**

**Equation**: ŷ = b₀ + b₁x + b₂x² (quadratic)

Or: ŷ = b₀ + b₁x + b₂x² + b₃x³ (cubic)

**Example**: Fertilizer and crop yield
- Low fertilizer: yield increases
- Moderate fertilizer: optimal yield
- High fertilizer: yield decreases (overfeeding)

Quadratic model captures this inverted-U relationship

### Caution
- Easy to overfit (too flexible)
- Extrapolation dangerous (predictions outside data range)
- Consider domain knowledge

## Common Pitfalls and Misconceptions

### 1. Correlation ≠ Causation

**Examples of Spurious Correlations**:
- Ice cream sales and drowning deaths (both caused by summer)
- Number of Nicolas Cage movies and pool drownings
- Shoe size and reading ability in children (both caused by age)

**Bradford Hill Criteria for Causation**:
- Strength of association
- Consistency across studies
- Temporal sequence (cause before effect)
- Dose-response relationship
- Plausibility (mechanism)
- Experimental evidence

### 2. Extrapolation

**Problem**: Making predictions outside range of observed data

**Example**: Regression of height vs. age for children 5-15 years
- Predicting height at age 30? Extrapolation!
- Model doesn't apply outside observed range

### 3. Ecological Fallacy

**Problem**: Inferring individual relationships from group-level data

**Example**: Countries with more chocolate consumption have more Nobel laureates (correlation)
- Does NOT mean eating chocolate makes individuals win Nobel prizes!

### 4. Simpson's Paradox

**Phenomenon**: Trend appears in separate groups but reverses when groups combined

**Example**: Treatment appears worse than control overall, but better in every subgroup

**Lesson**: Always consider confounding variables

### 5. Overfitting

**Problem**: Model fits training data too well, performs poorly on new data

**Signs**:
- Very high R² on training data
- Many predictors relative to sample size
- Poor performance on test data

**Solutions**:
- Cross-validation
- Regularization (LASSO, Ridge)
- Simpler models

### 6. Influential Points

**Problem**: Single observation greatly affects regression line

**Detection**:
- Cook's distance
- Leverage values
- DFBETAS

**Solution**:
- Investigate why point is unusual
- Consider robustness (e.g., robust regression)
- Report with and without influential point

## Model Diagnostics Checklist

### 1. Scatterplot
- Is relationship linear?
- Any outliers?

### 2. Residual Plot (residuals vs. fitted)
- Random scatter? (linearity holds)
- Constant spread? (equal variance holds)
- No patterns?

### 3. Q-Q Plot of Residuals
- Points follow diagonal line? (normality holds)

### 4. Histogram of Residuals
- Approximately normal?

### 5. R² and Adjusted R²
- Adequate fit?
- Adjusted R² penalizes complexity?

### 6. Significance Tests
- Slope significantly different from 0?
- F-test for overall model?

## Key Terms

| Term | Definition |
|------|------------|
| **Correlation** | Strength and direction of linear relationship between variables |
| **Regression** | Method to model relationship and make predictions |
| **Response Variable (y)** | Variable we want to predict/explain (dependent) |
| **Predictor Variable (x)** | Variable used for prediction (independent, explanatory) |
| **Slope** | Change in y per unit change in x |
| **Intercept** | Predicted y when x = 0 |
| **Residual** | Difference between observed and predicted value |
| **R²** | Proportion of variance explained by model |
| **Least Squares** | Method minimizing sum of squared residuals |
| **Extrapolation** | Predicting outside range of observed data |
| **Multicollinearity** | High correlation among predictor variables |
| **Overfitting** | Model too complex, fits noise not just signal |

## Summary

Correlation quantifies linear relationships between variables using Pearson's r, ranging from -1 (perfect negative) to +1 (perfect positive). However, correlation alone doesn't imply causation - confounding variables and reverse causation must be considered.

Simple linear regression models how one variable predicts another using the equation ŷ = b₀ + b₁x. The slope (b₁) represents the change in y per unit change in x, while R² measures the proportion of variance explained. Residual plots help assess whether regression assumptions (linearity, independence, normality, equal variance) are satisfied.

Multiple regression extends these ideas to multiple predictors, allowing us to control for confounding and build more realistic models. Adjusted R² accounts for model complexity, while multicollinearity among predictors can cause problems.

Regression is powerful but requires careful application. Always visualize data, check assumptions, consider the context, and remember that statistical relationships don't automatically imply causal relationships. Avoid extrapolation beyond observed data ranges, and be wary of overfitting complex models to limited data.

These tools - correlation and regression - form the foundation of predictive modeling, enabling evidence-based decision making across science, business, and policy.
