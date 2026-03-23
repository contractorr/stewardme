# Bayesian Reasoning

## Overview

Bayesian reasoning is the formal framework for updating beliefs in light of evidence. It provides a mathematically optimal way to combine prior knowledge with new data, serving as the gold standard for rational belief revision. Named after Thomas Bayes (1701-1761), whose posthumously published theorem laid the foundation, Bayesian methods now permeate statistics, machine learning, scientific inference, and everyday reasoning about uncertainty.

The Bayesian approach answers a fundamental question: Given what I believed before (my prior) and what I just observed (the evidence), what should I believe now (my posterior)? This seemingly simple question has profound implications for how we interpret medical tests, evaluate scientific theories, make predictions, and navigate uncertainty in every domain.

## Probability: Frequentist vs Bayesian Interpretations

Before diving into Bayes' theorem, we must clarify what "probability" means. Two dominant interpretations exist, and the choice has deep philosophical and practical implications.

| Interpretation | Probability Means... | Example: "70% chance of rain tomorrow" | Can Apply To... |
|---------------|---------------------|----------------------------------------|----------------|
| **Frequentist** | Long-run relative frequency in repeated trials | In an infinite sequence of days with identical conditions, 70% would have rain | Repeatable random experiments |
| **Bayesian** | Degree of belief / credence / subjective confidence | I'm 70% confident it will rain tomorrow | Any proposition with uncertainty |

**Frequentist limitations**: Frequentists can only assign probabilities to repeatable random experiments. They can say "a fair coin has 50% probability of heads" (referring to long-run frequency) but cannot say "this particular startup has a 35% chance of succeeding" (it either will or won't — there's no long-run frequency for this unique startup). They cannot assign probabilities to scientific hypotheses ("evolution is true") or one-time historical events ("Napoleon won at Austerlitz").

**Bayesian flexibility**: Bayesians interpret probability as degree of belief given your knowledge. You can assign probabilities to:
- One-time events: "40% chance Trump wins the 2028 election"
- Scientific hypotheses: "85% confident the Higgs boson exists" (pre-discovery)
- Parameters: "The true click-through rate is between 2.1% and 2.3% with 95% probability"
- Past events with uncertainty: "75% probability the Rapa Nui civilization collapsed due to ecological overshoot"

The Bayesian view treats probability as **epistemic** (about knowledge states) rather than **ontological** (about objective frequencies in the world).

**Historical note**: Pierre-Simon Laplace (1749-1827) independently developed Bayesian probability and applied it extensively. His *Théorie Analytique des Probabilités* (1812) treated probability as "the ratio of favorable cases to all possible cases" — a degree of belief view. The frequentist interpretation arose later with Venn, von Mises, and Fisher as a response to perceived subjectivity in Bayesian priors.

## Bayes' Theorem: The Foundation

Bayes' theorem follows directly from the definition of conditional probability:

```
P(A|B) = P(A and B) / P(B)
P(B|A) = P(A and B) / P(A)
```

Solving for P(A and B) and equating:
```
P(A|B) × P(B) = P(A and B) = P(B|A) × P(A)
```

Rearranging for P(A|B):
```
P(A|B) = [P(B|A) × P(A)] / P(B)
```

For hypothesis H and evidence E:

```
P(H|E) = P(E|H) × P(H) / P(E)
```

| Term | Name | Meaning | Example (medical test) |
|------|------|---------|------------------------|
| P(H) | **Prior** | Belief in hypothesis before evidence | 0.001 (disease prevalence) |
| P(E\|H) | **Likelihood** | Probability of evidence given hypothesis is true | 0.99 (sensitivity — true positive rate) |
| P(H\|E) | **Posterior** | Updated belief after seeing evidence | 0.09 (probability of disease given positive test) |
| P(E) | **Marginal likelihood** | Total probability of evidence | 0.01098 (all ways to get positive result) |

The marginal likelihood P(E) decomposes via the **law of total probability**:

```
P(E) = P(E|H) × P(H) + P(E|¬H) × P(¬H)
```

For multiple hypotheses H₁, H₂, ..., Hₙ that partition the space:
```
P(E) = Σᵢ P(E|Hᵢ) × P(Hᵢ)
```

**Intuitive understanding**: The prior P(H) represents your starting belief. The likelihood P(E|H) represents how expected the evidence is if the hypothesis were true. Evidence that's highly expected under H but unexpected under ¬H provides strong support for H. The posterior P(H|E) is your updated belief after incorporating the evidence.

## The Medical Testing Example (Detailed)

A disease affects 1 in 1,000 people in the population (base rate = 0.1%). A diagnostic test is:
- **99% sensitive**: P(positive | disease) = 0.99 (true positive rate)
- **99% specific**: P(negative | no disease) = 0.99, so P(positive | no disease) = 0.01 (false positive rate)

You test positive. What's the probability you have the disease?

**Naive answer**: "The test is 99% accurate, so I'm 99% sure I have the disease."

**Correct Bayesian answer**:

```
P(disease | positive) = P(positive | disease) × P(disease) / P(positive)
```

First, calculate P(positive) using the law of total probability:

```
P(positive) = P(positive | disease) × P(disease) + P(positive | no disease) × P(no disease)
            = 0.99 × 0.001 + 0.01 × 0.999
            = 0.00099 + 0.00999
            = 0.01098
```

Then apply Bayes' theorem:

```
P(disease | positive) = (0.99 × 0.001) / 0.01098
                      = 0.00099 / 0.01098
                      = 0.0901
                      ≈ 9%
```

**Only 9%!** Despite a positive result on a test that's "99% accurate," you still only have about a 1-in-11 chance of having the disease.

### Why is the probability so low?

**Frequency visualization**: Imagine testing 1,000 people:
- 1 person has the disease (0.1% base rate)
  - 0.99 test positive (99% sensitivity)
  - 0.01 test negative (1% false negative)
- 999 people don't have the disease
  - 9.99 test positive (1% false positive rate)
  - 989.01 test negative (99% specificity)

Total positives: 0.99 + 9.99 ≈ 11
True positives: 0.99
Probability of disease given positive: 0.99/11 ≈ 9%

**The lesson**: Low base rates dominate. When the condition is rare (1/1,000), even a test with only 1% false positive rate produces mostly false positives. For every 1 true positive, you get about 10 false positives.

**Real-world consequences**: Widespread screening for rare diseases can cause more harm (false positives leading to unnecessary treatment, anxiety, and medical costs) than benefit. This is why medical guidelines often recommend against screening low-risk populations.

### Base Rate Neglect

The overwhelming majority of people — including doctors — commit **base rate neglect** when interpreting test results. They focus on the test's accuracy (99%) while ignoring the base rate (0.1%).

**Classic study** (Casscells et al., 1978): Harvard Medical School staff (doctors, nurses, students) were given this exact problem. Modal answer: 95%. Only 18% answered correctly (≈9-10%).

**Why does this happen?**
- P(positive | disease) = 99% is salient and recent (just learned it)
- P(disease) = 0.1% feels abstract and is easily ignored
- Causal reasoning: "The test detected something" feels more important than statistical base rates
- Representativeness heuristic: A positive test "represents" having the disease

Base rate neglect appears in:
- **Medicine**: Over-diagnosis of rare conditions from screening
- **Law**: Jury misinterpretation of DNA evidence (prosecutor's fallacy)
- **Security**: False positives from screening for rare threats (TSA, terrorism)
- **Hiring**: Overweighting interview performance, underweighting base rate success of similar candidates

## Likelihood Ratios and Odds Form

Bayes' theorem is often cleaner and more intuitive in **odds form**.

**Odds**: Instead of probability p, express as odds = p/(1-p).
- Probability 0.5 (50%) = odds 1:1 ("even odds")
- Probability 0.75 (75%) = odds 3:1 ("3-to-1 odds in favor")
- Probability 0.1 (10%) = odds 1:9 ("9-to-1 odds against")

**Bayes in odds form**:

```
Posterior odds = Likelihood ratio × Prior odds
```

Where:
```
Likelihood ratio (LR) = P(E|H) / P(E|¬H)
```

**Medical test example revisited**:

Prior odds of disease = 0.001/0.999 ≈ 1:999

Likelihood ratio = P(positive | disease) / P(positive | no disease)
                 = 0.99 / 0.01
                 = 99

Posterior odds = 99 × (1/999) = 99/999 ≈ 1:10

Converting back to probability: 1/(1+10) ≈ 9%

### Advantages of Likelihood Ratios

1. **Multiplicative**: Multiple independent pieces of evidence just multiply their LRs
2. **Intuitive interpretation**:
   - LR > 1: Evidence supports H
   - LR < 1: Evidence opposes H
   - LR = 1: Evidence is irrelevant (equally likely under H and ¬H)
   - LR = 10: Evidence is 10× more likely under H than ¬H ("10 bits" of evidence)
3. **Portable**: The LR is a property of the evidence, independent of priors. Different people with different priors can agree on the LR.

**Strength scales**:
- LR 1-3: Weak evidence
- LR 3-10: Moderate evidence
- LR 10-30: Strong evidence
- LR 30-100: Very strong evidence
- LR > 100: Extremely strong evidence

**Example**: DNA match at 13 loci provides LR ≈ 1 trillion. Even with a very low prior (1 in 10 million), posterior odds become 1 trillion / 10 million = 100,000:1 in favor of a match.

## Bayesian Updating with Multiple Evidence

When evidence pieces E₁, E₂, ..., Eₙ are **conditionally independent** given H (knowing H makes them independent), you can multiply likelihood ratios:

```
Posterior odds = Prior odds × LR₁ × LR₂ × ... × LRₙ
```

**Criminal investigation example**:

Prior: 1 in 10,000 (any random person)

Evidence:
1. Witness identification: LR = 100 (witnesses are often wrong)
2. DNA match: LR = 1,000,000
3. Found with victim's phone: LR = 1,000
4. No alibi: LR = 3

Posterior odds = (1/10,000) × 100 × 1,000,000 × 1,000 × 3
               = 30,000,000,000:1

Converting to probability: ≈ 99.9999999997%

**Critical assumption: Independence**. In reality, evidence is often correlated:
- If the witness saw the suspect because of contaminated evidence, the witness ID and DNA might not be independent
- If police found the phone because they were already focusing on this suspect, the phone and other evidence might be correlated

Naively multiplying LRs when evidence is correlated **double-counts** and inflates confidence. This is a major source of error in legal and intelligence contexts.

## Prior Selection: Where Do Priors Come From?

The Bayesian framework requires specifying a prior P(H) before seeing evidence. Critics argue this introduces subjectivity. How should priors be chosen?

### Types of Priors

| Type | Description | When to Use | Example |
|------|-------------|-------------|---------|
| **Uninformative / Flat** | All values equally probable | When you genuinely know nothing | P(coin bias) = uniform on [0,1] |
| **Weakly informative** | Constrains to reasonable range without strong commitment | When you know the ballpark | P(click rate) = Beta(2, 20) centered at ~10% |
| **Informative** | Based on previous studies or domain knowledge | When substantial prior evidence exists | P(drug effect) based on previous trials |
| **Reference / Objective** | Derived from formal principles (e.g., Jeffreys prior) | Technical analysis wanting "minimal assumptions" | Jeffreys prior for scale parameters |
| **Maximum entropy** | Highest entropy distribution consistent with constraints | When you know certain facts but want minimal other assumptions | Given mean and variance, use Normal |
| **Conjugate** | Prior from a family that produces posterior in the same family | Mathematical convenience | Beta prior with binomial likelihood → Beta posterior |

### Sensitivity to Priors

With **strong evidence** (lots of data), different priors converge to similar posteriors. The data "overwhelms" the prior.

With **weak evidence** (little data), priors dominate the posterior. Different priors can lead to dramatically different conclusions.

**Example**: Coin flipping.

Flat prior: P(θ) = 1 for θ ∈ [0,1] (all bias values equally likely)
Informative prior: P(θ) peaked at 0.5 (expect fairness)

After 3 flips, all heads:
- Flat prior → posterior peaks at θ=1 (100% heads)
- Informative prior → posterior peaks at θ≈0.6 (still thinks coin is mostly fair)

After 1,000 flips, 600 heads:
- Flat prior → posterior peaks at θ=0.6, narrow
- Informative prior → posterior peaks at θ=0.6, narrow
- **Priors converge**: Enough data makes the prior irrelevant

### Objective Bayesianism

Can we avoid subjectivity in prior selection?

**Jeffreys priors**: Choose priors that are invariant under reparameterization. If you analyze θ vs log(θ) or 1/θ, you should get the same answer.

**Maximum entropy priors**: Given constraints (e.g., known mean), choose the distribution with highest entropy (most "spread out" / least informative).

**Problem**: These often produce **improper priors** (don't integrate to 1), which can lead to improper posteriors. They work as limiting cases but require care.

**Pragmatic view** (E.T. Jaynes): Bayesianism is about **updating** consistently. Everyone updates via Bayes' theorem. Different priors just represent different background knowledge. As long as you're honest about your priors and update correctly, the framework is sound. With enough evidence, priors wash out anyway.

## Bayesian vs Frequentist Statistics

The frequentist vs Bayesian debate has raged for a century. Modern statistics increasingly embraces both, using whichever framework suits the problem.

| Feature | Bayesian | Frequentist |
|---------|----------|-------------|
| **Probability interpretation** | Degree of belief / credence | Long-run frequency |
| **Parameters** | Random variables with distributions | Fixed but unknown constants |
| **Output** | Posterior distribution P(θ\|data) | Point estimates + confidence intervals |
| **Prior information** | Formally incorporated via P(θ) | Excluded (or informally used) |
| **Interpretation of intervals** | "95% probability θ is in this interval given the data" | "95% of such intervals contain θ in repeated sampling" |
| **Small samples** | Works well with informative priors | Unreliable; asymptotic theory doesn't apply |
| **Computational cost** | Often high (MCMC, variational inference) | Usually lower (analytical or optimization) |
| **Multiple comparisons** | Less problematic (coherent probability model) | Requires corrections (Bonferroni, etc.) |
| **Stopping rules** | Irrelevant (Likelihood Principle) | Affect validity |

### The Likelihood Principle

Bayesians follow the **Likelihood Principle**: All information the data contains about the parameters is in the likelihood function P(data|θ). How you planned to collect the data (stopping rules, multiple comparisons) is irrelevant.

**Example**: You flip a coin and want to test if it's fair.

Experiment A: Flip 10 times. Get 8 heads.
Experiment B: Flip until 8 heads. Happened to take 10 flips.

Frequentist: Different p-values! Experiment A: p=0.055. Experiment B: p=0.033. The stopping rule matters.
Bayesian: Identical likelihood, identical posterior. The stopping rule is irrelevant.

**Defenders of frequentism** argue this is a feature, not a bug — sequential testing is easier to game, so penalizing it makes sense. **Defenders of Bayesianism** argue stopping rules are about experimenters' intentions, not about what the data say.

### Practical Considerations

**When to use Bayesian**:
- Small samples where priors help stabilize estimates
- Incorporating prior studies or expert knowledge
- Making probability statements about hypotheses ("the effect is positive with 90% probability")
- Hierarchical models with many parameters
- Sequential decision-making (priors updated as data arrive)

**When to use Frequentist**:
- Large samples where priors don't matter much
- When priors are controversial and you want to avoid prior debates
- When computational resources are limited (some Bayesian methods are computationally intensive)
- When regulatory or publication standards require frequentist methods (still common in medicine)

**Pragmatism**: Andrew Gelman's view: "Use Bayesian methods when they help, and don't worry about philosophical justification." Most modern statisticians are "eclectic" — using Bayesian inference, frequentist significance tests, likelihood methods, and cross-validation as appropriate.

## Cromwell's Rule

Named after Oliver Cromwell's 1650 plea to the Church of Scotland: "I beseech you, in the bowels of Christ, think it possible that you may be mistaken."

**Cromwell's Rule**: Never assign probability exactly 0 or 1 to any empirical proposition.

### Why?

Once P(H) = 0 or P(H) = 1, **no amount of evidence can change it**:

```
If P(H) = 0:
P(H|E) = P(E|H) × 0 / P(E) = 0 for any E

If P(H) = 1:
P(H|E) = P(E|H) × 1 / P(E)
       = P(E|H) / [P(E|H) × 1 + P(E|¬H) × 0]
       = P(E|H) / P(E|H)
       = 1 for any E
```

You've **closed your mind** — evidence is now irrelevant.

### What to do instead

Use **extreme but not absolute** probabilities:
- Instead of P(H) = 0, use P(H) = 0.0001 (one in 10,000)
- Instead of P(H) = 1, use P(H) = 0.9999

This leaves open the possibility that overwhelming evidence could change your mind.

**Examples**:
- "The Earth is round": 99.9999% (not 100% — maybe I'm in a simulation designed to deceive me)
- "Homeopathy works beyond placebo": 0.001% (not 0% — maybe physics is radically wrong)
- "Evolution by natural selection occurs": 99.999% (not 100% — extraordinary evidence could overturn it)

Reserve 0 and 1 for:
- **Logical truths**: P(2+2=4) = 1
- **Logical contradictions**: P(a square circle exists) = 0
- **Definitions**: P(all bachelors are unmarried | English definitions) = 1

For empirical claims about the world, always leave room for error.

## Real-World Applications

### Medical Diagnosis

Bayesian reasoning is essential for interpreting diagnostic tests. Pre-test probability (from symptoms, demographics, medical history) + test result (likelihood ratio) = post-test probability.

**Example**: 45-year-old man, chest pain, family history of heart disease.
- Pre-test probability of coronary artery disease: ~30%
- Positive stress test (LR ≈ 3)
- Post-test odds: (0.3/0.7) × 3 ≈ 1.3:1 → probability ≈ 57%

Moderate concern, might do further testing (angiography). If pre-test probability were 5% (young, no risk factors), post-test would be only 14% — probably a false positive.

**Doctors who ignore base rates** order unnecessary tests, over-diagnose, and cause harm.

### Spam Filtering

**Naive Bayes classifier**: The workhorse of early spam filters (still used).

```
P(spam | words) ∝ P(words | spam) × P(spam)
```

Assume (naively) words are independent given spam/not spam:

```
P(words | spam) = ∏ P(wordᵢ | spam)
```

**Example**:
Email contains: "viagra", "free", "click", "now"

P(spam) = 0.5 (half of emails are spam)
P("viagra" | spam) = 0.05, P("viagra" | ham) = 0.0001 → LR = 500
P("free" | spam) = 0.2, P("free" | ham) = 0.05 → LR = 4
P("click" | spam) = 0.15, P("click" | ham) = 0.08 → LR = 1.9
P("now" | spam) = 0.1, P("now" | ham) = 0.06 → LR = 1.7

Combined LR ≈ 500 × 4 × 1.9 × 1.7 ≈ 6,500

Posterior odds ≈ 6,500:1 → almost certainly spam.

Modern filters use more sophisticated methods, but the Bayesian core remains.

### Legal Reasoning: The Prosecutor's Fallacy

**Prosecutor's Fallacy**: Confusing P(evidence | innocent) with P(innocent | evidence).

**Case**: DNA match at a crime scene. The match is "1 in a million."

**Prosecutor argues**: "The probability of this match if the defendant is innocent is 1 in a million. Therefore, the probability the defendant is innocent is 1 in a million."

**This is wrong.** The correct analysis:

P(match | innocent) = 1/1,000,000 (random match)
P(match | guilty) ≈ 1 (assuming no lab error)

But we need P(innocent | match). This requires the **prior** — how likely was the defendant to be guilty before the DNA evidence?

If the defendant was identified *because of the DNA match* (database search), the prior is roughly the population frequency. In a city of 10 million, about 10 people match. The DNA alone provides weak evidence — you need additional evidence to narrow it to this specific person.

If the defendant was identified *independently* (witness, other evidence), the DNA provides strong additional evidence.

**Famous case**: Sally Clark, convicted of murdering her two infants in the UK (1999). Pediatrician Sir Roy Meadow testified: "The probability of two infants dying of SIDS in one family is 1 in 73 million."

**Error 1**: Assumed independence (SIDS deaths in the same family are correlated — genetic, environmental factors).
**Error 2**: Prosecutor's fallacy — even if P(two SIDS | innocent) = 1 in 73 million, we need P(innocent | two deaths), which requires P(two deaths | guilty). How common is double infanticide? If also rare, the DNA doesn't prove much.

Clark served 3 years before the conviction was overturned. Meadow was later struck off the medical register for his testimony.

### Intelligence Analysis

The CIA's **Analysis of Competing Hypotheses (ACH)** method is essentially Bayesian:

1. List all plausible hypotheses
2. For each piece of evidence, evaluate P(E | H₁), P(E | H₂), ..., P(E | Hₙ)
3. Update probabilities for each hypothesis
4. Identify which evidence is most diagnostic (biggest LR differences)
5. Seek evidence that discriminates between leading hypotheses

This counteracts **confirmation bias** (seeking evidence for your favored hypothesis) by forcing you to evaluate evidence against *all* hypotheses.

## Limitations and Challenges

**Prior dependence**: With limited data, conclusions depend heavily on priors. Disagreement about priors can lead to persistent disagreement about posteriors.

**Model uncertainty**: Bayes' theorem updates beliefs *within* a model (e.g., "what's the bias of this coin?"). It doesn't tell you which model is correct (coin with bias? two-headed coin? rigged mechanism?). Bayesian model comparison exists but is complex.

**Computational cost**: Posterior distributions for complex models often lack closed forms. Requires Markov Chain Monte Carlo (MCMC), variational inference, or approximate Bayesian computation — computationally intensive.

**Cognitive difficulty**: Humans are terrible intuitive Bayesians. Base rate neglect, conjunction fallacy, and probability matching all violate Bayesian norms. Teaching and training help but are effortful.

**Independence assumptions**: Naive Bayes assumes conditional independence, which is often violated in practice. Violations can lead to overconfidence.

**Infinite regress**: Where do priors come from? Previous posteriors. Where do *those* priors come from? Eventually you hit bedrock — some priors are foundational (background knowledge, symmetry, maximum entropy). But it's not fully satisfying.

## Key Terms

- **Prior Probability** P(H): Belief in hypothesis before seeing evidence
- **Likelihood** P(E|H): Probability of evidence given hypothesis is true
- **Posterior Probability** P(H|E): Updated belief in hypothesis after seeing evidence
- **Marginal Likelihood** P(E): Total probability of observing the evidence (normalization constant)
- **Base Rate**: Prior probability of a condition in the population
- **Base Rate Neglect**: Ignoring priors when interpreting evidence; focusing only on likelihoods
- **Likelihood Ratio (LR)**: P(E|H) / P(E|¬H); strength of evidence independent of priors
- **Odds**: p/(1-p); alternative to probability; natural for multiplicative updating
- **Cromwell's Rule**: Never assign probability exactly 0 or 1 to empirical claims
- **Conjugate Prior**: Prior from a distribution family that yields a posterior in the same family
- **Posterior Odds**: Prior odds × likelihood ratio
- **Prosecutor's Fallacy**: Confusing P(evidence|innocent) with P(innocent|evidence)
- **Bayesian Updating**: Iteratively applying Bayes' theorem as new evidence arrives
- **Credible Interval**: Bayesian analog of confidence interval — "95% probability parameter is in this range"
- **Improper Prior**: Prior that doesn't integrate to 1; sometimes used as limiting case

## Summary

Bayesian reasoning provides the mathematically rigorous framework for updating beliefs with evidence. Bayes' theorem — P(H|E) = P(E|H) × P(H) / P(E) — combines prior beliefs with likelihood to yield posterior beliefs. The odds form makes sequential updating intuitive: multiply likelihood ratios.

Base rate neglect — ignoring priors when interpreting evidence — is pervasive and dangerous. Medical over-diagnosis, wrongful convictions, and intelligence failures often stem from focusing on P(E|H) while ignoring P(H). The medical testing example demonstrates how low base rates dominate even highly accurate tests.

Likelihood ratios offer intuitive, portable measures of evidential strength. Multiple independent evidence pieces multiply their LRs, making sequential updating straightforward. But independence assumptions must be carefully checked — correlated evidence leads to overconfidence.

Prior selection involves judgment. Uninformative, weakly informative, and strongly informative priors serve different purposes. With abundant data, priors wash out; with sparse data, they dominate. Cromwell's rule warns against certainty: always assign extreme but non-zero probabilities to empirical claims, leaving room to update.

Bayesian and frequentist statistics differ philosophically and practically. Bayesians treat parameters as random variables with distributions and deliver intuitive probability statements about hypotheses. Frequentists treat parameters as fixed and deliver confidence intervals with less intuitive interpretations. Modern practice is eclectic, using whichever framework suits the problem.

Applications span medicine (diagnosis), machine learning (spam filters, recommendation systems), law (evidence evaluation), intelligence (hypothesis testing), and science (model comparison). The core insight transcends domains: combine what you knew before with what you learned now, and update rationally. This is the essence of learning itself.
