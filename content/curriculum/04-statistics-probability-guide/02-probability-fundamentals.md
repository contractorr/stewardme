# Probability Fundamentals

## Overview

Probability is the mathematical framework for quantifying uncertainty. It provides the foundation for statistical inference, allowing us to make predictions, assess risks, and draw conclusions from incomplete information. This chapter covers the basic principles of probability theory, conditional probability, independence, and Bayes' theorem.

## Basic Probability Concepts

### Definition of Probability
Probability is a number between 0 and 1 (or 0% to 100%) that represents the likelihood of an event occurring:
- **P(A) = 0**: Event A is impossible
- **P(A) = 1**: Event A is certain
- **0 < P(A) < 1**: Event A may or may not occur

### Three Interpretations of Probability

| Interpretation | Description | Example |
|----------------|-------------|---------|
| **Classical** | Ratio of favorable outcomes to total equally likely outcomes | Probability of rolling a 6 on a fair die = 1/6 |
| **Frequentist** | Long-run relative frequency of an event over many trials | Flip a coin 10,000 times; proportion of heads approaches 0.5 |
| **Subjective** | Degree of belief based on available information | "I'm 70% confident it will rain tomorrow" |

### Sample Space and Events
- **Sample Space (S)**: Set of all possible outcomes
- **Event**: A subset of the sample space
- **Simple Event**: Single outcome
- **Compound Event**: Combination of multiple outcomes

**Example**: Rolling a die
- Sample space: S = {1, 2, 3, 4, 5, 6}
- Event "rolling an even number": A = {2, 4, 6}
- P(A) = 3/6 = 0.5

## Probability Rules

### Rule 1: Complement Rule
The probability that event A does not occur:

**P(A') = 1 - P(A)**

Example: If P(rain) = 0.3, then P(no rain) = 1 - 0.3 = 0.7

### Rule 2: Addition Rule

**For mutually exclusive events** (cannot occur simultaneously):
**P(A or B) = P(A) + P(B)**

**For non-mutually exclusive events**:
**P(A or B) = P(A) + P(B) - P(A and B)**

Example: Drawing a card from a deck
- P(King or Queen) = 4/52 + 4/52 = 8/52 (mutually exclusive)
- P(King or Heart) = 4/52 + 13/52 - 1/52 = 16/52 (King of Hearts counted twice)

### Rule 3: Multiplication Rule

**For independent events** (outcome of one doesn't affect the other):
**P(A and B) = P(A) × P(B)**

**For dependent events**:
**P(A and B) = P(A) × P(B|A)**

Example: Flipping two coins
- P(heads on first AND heads on second) = 0.5 × 0.5 = 0.25

## Conditional Probability

### Definition
Conditional probability is the probability of event A occurring given that event B has already occurred:

**P(A|B) = P(A and B) / P(B)**

where P(B) > 0

### Intuition
Conditional probability updates our beliefs based on new information. We restrict the sample space to only those outcomes where B occurred.

### Example: Medical Testing
- 1% of population has disease
- Test is 99% accurate for those with disease (true positive rate)
- Test is 95% accurate for those without disease (true negative rate)

If someone tests positive, what's the probability they actually have the disease?

Let:
- D = has disease
- + = tests positive

We need P(D|+), not just the test accuracy!

## Independence

### Definition
Two events A and B are independent if:
**P(A|B) = P(A)** or equivalently **P(A and B) = P(A) × P(B)**

The occurrence of B doesn't change the probability of A.

### Examples of Independence
- Flipping two separate coins
- Rolling dice multiple times
- Drawing cards with replacement

### Examples of Dependence
- Drawing cards without replacement
- Weather on consecutive days
- Test results for the same person

### Common Misconception
**Mutually exclusive ≠ Independent**
- Mutually exclusive: If A occurs, B cannot (they are dependent!)
- Independent: Occurrence of A doesn't affect probability of B

## Bayes' Theorem

### The Formula
**P(A|B) = [P(B|A) × P(A)] / P(B)**

Or in expanded form:
**P(A|B) = [P(B|A) × P(A)] / [P(B|A) × P(A) + P(B|A') × P(A')]**

### Components
- **P(A)**: Prior probability (before new evidence)
- **P(B|A)**: Likelihood (probability of evidence given hypothesis)
- **P(A|B)**: Posterior probability (updated belief after evidence)
- **P(B)**: Marginal probability (total probability of evidence)

### Why It Matters
Bayes' theorem allows us to update beliefs based on new evidence. It's fundamental to:
- Medical diagnosis
- Spam filtering
- Machine learning
- Scientific inference
- Legal reasoning

## Real-World Examples

### Example 1: Disease Testing (Bayes' Theorem)

**Setup**:
- Disease prevalence: 1% (prior probability)
- Test sensitivity: 99% (true positive rate)
- Test specificity: 95% (true negative rate)

**Question**: If test is positive, what's probability of having disease?

**Solution**:
- P(D) = 0.01, P(D') = 0.99
- P(+|D) = 0.99
- P(+|D') = 0.05

Using Bayes' theorem:
P(D|+) = [0.99 × 0.01] / [0.99 × 0.01 + 0.05 × 0.99]
P(D|+) = 0.0099 / (0.0099 + 0.0495)
P(D|+) = 0.0099 / 0.0594 ≈ 0.167 or 16.7%

**Interpretation**: Despite a 99% accurate test, only 16.7% of positive results actually have the disease! This is because the disease is rare (1% prevalence).

### Example 2: Birthday Problem

**Question**: How many people need to be in a room for 50% probability that two share a birthday?

**Solution**:
- Calculate probability that all have different birthdays
- P(all different) = 365/365 × 364/365 × 363/365 × ...
- P(at least one match) = 1 - P(all different)

With 23 people: P(match) ≈ 0.507 (50.7%)
With 50 people: P(match) ≈ 0.970 (97%)

**Counterintuitive**: Most people guess much higher than 23!

### Example 3: Monty Hall Problem

**Setup**:
- Three doors: one has car, two have goats
- You pick door #1
- Host (who knows what's behind doors) opens door #3, revealing a goat
- Host offers: "Switch to door #2 or stay with door #1?"

**Question**: Should you switch?

**Solution**:
Initially:
- P(car behind door 1) = 1/3
- P(car behind door 2) = 1/3
- P(car behind door 3) = 1/3

After host opens door 3:
- P(car behind door 1) = 1/3 (your initial choice unchanged)
- P(car behind door 2) = 2/3 (combines probability from doors 2 and 3)

**Answer**: Switch! You double your chances from 1/3 to 2/3.

### Example 4: Weather Forecasting

**Question**: Weather forecast says "70% chance of rain." What does this mean?

**Interpretation**:
- Of all past days with similar conditions, 70% had rain
- If you repeated this day 100 times, expect rain about 70 times
- Your degree of belief in rain should be 0.7

**Decision-making**:
- Bring umbrella if cost of getting wet > 0.3 × cost of carrying umbrella

### Example 5: Spam Filtering

Email contains word "FREE":
- P(spam) = 0.5 (prior: 50% of emails are spam)
- P("FREE"|spam) = 0.8 (80% of spam contains "FREE")
- P("FREE"|not spam) = 0.1 (10% of legitimate emails contain "FREE")

Using Bayes' theorem:
P(spam|"FREE") = [0.8 × 0.5] / [0.8 × 0.5 + 0.1 × 0.5]
P(spam|"FREE") = 0.4 / 0.45 ≈ 0.889 or 88.9%

The word "FREE" increases spam probability from 50% to 89%.

## Counting Principles

### Fundamental Counting Principle
If there are n₁ ways for event 1, n₂ ways for event 2, etc., then total number of ways = n₁ × n₂ × ... × nₖ

Example: License plate with 3 letters and 4 digits = 26³ × 10⁴ = 175,760,000 possibilities

### Permutations
Number of ways to arrange n items in order:
**P(n,r) = n! / (n-r)!**

Example: Arrange 3 books from 5 = 5!/(5-3)! = 60 ways

### Combinations
Number of ways to choose r items from n (order doesn't matter):
**C(n,r) = n! / [r!(n-r)!]**

Example: Choose 3 books from 5 = 5!/(3!×2!) = 10 ways

## Probability Distributions Preview

A probability distribution assigns probabilities to all possible values of a random variable:

- **Discrete**: Probability mass function (PMF)
  - Example: P(X = k) for rolling a die
- **Continuous**: Probability density function (PDF)
  - Example: Height distribution (covered in Chapter 3)

## Key Terms

| Term | Definition |
|------|------------|
| **Event** | A subset of the sample space |
| **Mutually Exclusive** | Two events that cannot occur simultaneously |
| **Independent Events** | Events where occurrence of one doesn't affect the other |
| **Conditional Probability** | P(A\|B), probability of A given B has occurred |
| **Prior Probability** | Initial belief before observing evidence |
| **Posterior Probability** | Updated belief after observing evidence |
| **Likelihood** | P(evidence\|hypothesis), probability of observing data given hypothesis |
| **Complement** | The event that A does not occur, denoted A' or Aᶜ |
| **Sample Space** | Set of all possible outcomes |
| **Random Variable** | Variable whose value depends on a random process |

## Summary

Probability provides the mathematical foundation for reasoning under uncertainty. Basic probability rules - complement, addition, and multiplication - allow us to calculate probabilities of complex events from simpler ones.

Conditional probability updates our beliefs when we gain new information, recognizing that probabilities change based on context. Independence is a special case where events don't influence each other, simplifying calculations.

Bayes' theorem is one of the most powerful tools in statistics, enabling us to update prior beliefs with new evidence to obtain posterior probabilities. It explains counterintuitive results like low positive predictive values in medical testing despite high test accuracy.

Understanding these fundamentals prepares you for probability distributions, statistical inference, and hypothesis testing - building blocks for all of data science and machine learning.
