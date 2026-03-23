# Causal Inference

## Overview

"Correlation does not imply causation" is the most repeated phrase in statistics. But how *do* we establish causation? This chapter covers the frameworks — counterfactual, structural, and experimental — for moving from association to causation. Understanding causal inference is essential for evaluating medical treatments, policy interventions, business decisions, and scientific claims.

Correlation is everywhere. Ice cream sales and drowning deaths correlate. Education and income correlate. Exercise and health correlate. But which are causal? Ice cream doesn't cause drowning (summer causes both). Education plausibly causes higher income. Exercise plausibly causes better health. Distinguishing causation from mere association requires rigorous methods.

## Correlation vs Causation

Observed associations between X and Y can arise from five distinct causal structures:

**1. X causes Y**: Smoking causes cancer. The correlation reflects direct causation.

**2. Y causes X** (reverse causation): High grades cause studying? No — studying causes high grades. Easy to confuse direction.

**3. Z causes both X and Y** (confounding): Ice cream sales and drowning deaths both correlate because summer (Z) causes both. The correlation is spurious — no direct causal relationship.

**4. Coincidence** (spurious correlation): Number of pirates has declined while global temperature has risen. Purely coincidental. With enough variables, random correlations emerge.

**5. Selection/collider bias**: Conditioning on a common effect creates spurious association even when X and Y are independent. Beauty and talent among Hollywood actors are negatively correlated not because beauty reduces talent, but because both increase probability of becoming an actor. Conditioning on "is an actor" (collider) creates the negative association.

### Real-World Examples

| Observed Correlation | Plausible Explanation | Causal? |
|---------------------|----------------------|---------|
| Coffee → cancer | Early studies found correlation | No. Confounded by smoking (smokers drink more coffee). When controlled for smoking, correlation vanishes. |
| Height → income | Taller people earn more | Partly causal. Height signals health, confidence, status. But also confounded by nutrition (childhood nutrition affects both height and cognitive development). |
| Marriage → happiness | Married people happier | Reverse causation + selection. Happy people more likely to marry *and* marriage may cause happiness. |
| Video games → violence | Correlation exists | No consistent causal evidence. Confounded by aggression (aggressive people seek violent games). Experimental studies show no effect. |
| Education → income | More education, higher income | Largely causal. Randomized encouragement designs show significant effects. But also selection (ability predicts both education and income). |

## Counterfactual Theory

David Lewis (1973) and the **potential outcomes framework** (Rubin, 1974) define causation counterfactually:

"X caused Y" means: **if X had not occurred, Y would not have occurred**.

More precisely, for individual i:

- Y₁ᵢ = outcome if i receives treatment
- Y₀ᵢ = outcome if i doesn't receive treatment
- Individual causal effect = Y₁ᵢ - Y₀ᵢ

**Example**: You took aspirin and your headache went away.
- Y₁ = no headache (what happened)
- Y₀ = ? (what would have happened without aspirin — the **counterfactual**)

Did aspirin cause relief? Only if Y₀ = headache (i.e., without aspirin, headache would have persisted).

### The Fundamental Problem of Causal Inference

**We can never observe both Y₁ᵢ and Y₀ᵢ for the same individual at the same time.** You either took aspirin or you didn't. The counterfactual is inherently unobservable. This is the **fundamental problem of causal inference** (Holland, 1986).

### The Solution: Average Treatment Effects

Since individual causal effects are unobservable, we estimate **average causal effects** across a population:

```
ATE = E[Y₁ - Y₀] = E[Y₁] - E[Y₀]
```

**Average Treatment Effect (ATE)**: The expected difference in outcomes if everyone received treatment vs if no one did.

If treatment and control groups are comparable (identical in expectation), the difference in average outcomes estimates the ATE:

```
ATE ≈ Ȳ₁ - Ȳ₀
```

Where Ȳ₁ = average outcome in treated group, Ȳ₀ = average outcome in control group.

**Critical assumption**: Groups must be **comparable**. If treatment and control groups differ systematically (e.g., sicker people get treatment), Ȳ₁ - Ȳ₀ mixes causal effect with selection bias.

### Types of Treatment Effects

| Effect | Definition | When It Matters |
|--------|------------|----------------|
| **ATE** | E[Y₁ - Y₀] for entire population | Universal policy (everyone gets treatment) |
| **ATT** | E[Y₁ - Y₀ \| treated] for those who received treatment | Evaluating actual intervention (those who opted in) |
| **ATU** | E[Y₁ - Y₀ \| untreated] for those who didn't receive treatment | Extending treatment to new group |
| **LATE** | Local ATE for compliers (those affected by instrument) | Instrumental variable estimation |

ATE = ATT only if treatment effect is constant or treatment is randomly assigned. When effects are heterogeneous, ATE ≠ ATT ≠ ATU.

## Structural Causal Models (Pearl)

Judea Pearl's framework (2000) revolutionized causal inference by formalizing causal reasoning with **Directed Acyclic Graphs (DAGs)** and the **do-calculus**.

### DAG Elements

- **Nodes**: Variables (X, Y, Z, etc.)
- **Arrows**: Direct causal effects (X → Y means "X causes Y")
- **No cycles**: Effects don't loop back (acyclic). X → Y → Z → X is forbidden.

**Example DAG**:
```
Education → Income
    ↑           ↑
    Ability ----+
```

Ability causes both education and income. There's also a direct path Education → Income.

### Key Structures

#### Chain (Mediation)
```
X → M → Y
```

X affects Y **through** mediator M. Smoking (X) → Tar deposits (M) → Cancer (Y).

**Conditioning on M blocks the path**. If we control for M (compare people with same tar deposits), X and Y become independent. The entire effect goes through M.

#### Fork (Confounding)
```
X ← Z → Y
```

Z causes both X and Y, creating a spurious association. Summer (Z) → Ice cream (X) and Summer (Z) → Drowning (Y).

**Conditioning on Z blocks the spurious path**. Control for Z (compare same-season), and X and Y become independent. The association was entirely due to Z.

#### Collider (Selection Bias)
```
X → Z ← Y
```

X and Y independently cause Z. X and Y are NOT associated... **unless you condition on Z**.

**Conditioning on a collider *creates* spurious association.** Classic mistake: stratifying by a consequence introduces bias.

**Example**: Beauty (X) and Talent (Y) independently affect being a Hollywood actor (Z). Among actors (conditioning on Z), beauty and talent appear negatively correlated because either suffices. Beautiful actors don't need as much talent; talented actors don't need as much beauty. But beauty and talent are uncorrelated in the general population.

**Another example**: Disease (X) and toxic exposure (Y) both cause hospitalization (Z). Among hospitalized patients (conditioning on Z), disease and exposure appear negatively correlated (if you're hospitalized for disease, you probably weren't exposed to toxin, and vice versa). This is **Berkson's paradox**.

### The do-Calculus

Pearl's intervention operator **do(X = x)** represents physically **setting** X to value x (as in an experiment), distinct from merely **observing** X = x (as in observational data).

```
P(Y | do(X = x)) ≠ P(Y | X = x)  in general
```

**Example**: Barometer (X) and Storm (Y).

- Observing the barometer reads low (X = low) predicts a storm: P(storm | X = low) is high.
- **Forcing** the barometer to read low by tampering with it doesn't cause a storm: P(storm | do(X = low)) = P(storm).

Observing vs intervening differ because observation carries information about causes of X, while intervention breaks those causal links.

### The Backdoor Criterion

To estimate P(Y | do(X)), we need to **block all backdoor paths** from X to Y (paths with an arrow into X) while leaving front-door paths (paths out of X) open.

A set of variables Z satisfies the **backdoor criterion** if:
1. No node in Z is a descendant of X
2. Z blocks every path from X to Y that contains an arrow into X

**If the backdoor criterion is satisfied**, we can identify the causal effect:

```
P(Y | do(X)) = Σ P(Y | X, Z) P(Z)
```

This is **adjustment** — control for Z (confounders), and the conditional association becomes the causal effect.

**Example**:
```
Z → X → Y
```

Z confounds X → Y. Backdoor path: X ← Z → Y. Controlling for Z blocks the backdoor path, identifying the causal effect of X on Y.

## Randomized Controlled Trials (RCTs)

The gold standard for causal inference. **Random assignment** ensures treatment and control groups are comparable on all variables — observed and unobserved.

### Why Randomization Works

By randomly assigning treatment:
- Every confounder is equally likely in treatment and control groups (in expectation)
- Groups differ only in treatment received
- Difference in outcomes = causal effect of treatment

Randomization **breaks the link** between treatment and confounders. In observational data, people selecting treatment may differ systematically. Randomization eliminates selection bias.

### Components of a Good RCT

| Component | Purpose | Example |
|-----------|---------|---------|
| **Randomization** | Eliminates confounding | Coin flip determines group |
| **Control group** | Provides counterfactual | Placebo pill or standard treatment |
| **Blinding (single)** | Prevents placebo effect | Patients don't know their group |
| **Double-blinding** | Prevents observer bias | Doctors don't know patients' groups |
| **Large sample** | Reduces chance imbalance | n ≥ hundreds or thousands |
| **Pre-registration** | Prevents p-hacking | Protocol registered before data collection |
| **Intention-to-treat** | Preserves randomization | Analyze as assigned, not as treated |

### Limitations of RCTs

**Ethical concerns**: Can't randomly assign smoking, child abuse, or harmful treatments. Many causal questions are off-limits to experimentation.

**External validity**: Participants volunteer (selection). Lab ≠ real world. Effects in trial participants may not generalize to target population.

**Cost**: RCTs are expensive (money, time, logistics).

**Compliance**: Assigned treatment ≠ received treatment. Some assigned treatment don't take it; some assigned control find treatment elsewhere. Intention-to-treat analysis preserves randomization but dilutes effect estimate.

**Heterogeneity**: Average effect may mask variation. Treatment might help some, harm others. RCTs estimate ATE, not individual effects.

**Famous RCT example**: Oregon Health Insurance Experiment (2008). Oregon expanded Medicaid via lottery. Random assignment (lottery) → causal identification. Result: Medicaid increased healthcare use, financial security, and self-reported health, but had no statistically significant effect on measured physical health outcomes (blood pressure, cholesterol, etc.) over two years. This was surprising and controversial.

## Natural Experiments and Quasi-Experiments

When RCTs are impossible, researchers exploit "natural" sources of random or as-if-random variation.

### Instrumental Variables (IV)

An **instrument** Z satisfies:
1. **Relevance**: Z affects treatment X (cor(Z, X) ≠ 0)
2. **Exclusion restriction**: Z affects outcome Y **only through** X (no direct path Z → Y)
3. **Exogeneity**: Z is uncorrelated with unobserved confounders of X → Y

**Classic example**: Returns to education (does education cause higher income, or does ability cause both?).

- **Instrument**: Distance to nearest college
- **Relevance**: Distance affects college attendance (people closer more likely to attend)
- **Exclusion**: Distance doesn't directly affect income (only through education)
- **Exogeneity**: Distance is quasi-random (determined by geography, not ability)

**Logic**: Compare people who live near vs far from college. They differ in education (relevance) but not in ability (exogeneity). Difference in income reflects causal effect of education.

**Limitation**: Exclusion restriction is untestable. If distance correlates with urban/rural, which affects income directly, the instrument is invalid.

**Vietnam draft lottery**: Birth date determines draft risk → military service → later earnings. Lottery ensures exogeneity (birth date is random). Angrist (1990) used this IV to estimate effect of military service on earnings (negative for Vietnam veterans).

**Formula**:
```
IV estimand = Cov(Y, Z) / Cov(X, Z)
```

This identifies the **Local Average Treatment Effect (LATE)** for **compliers** — those whose treatment was affected by the instrument.

### Regression Discontinuity (RD)

Treatment is assigned based on a cutoff in a continuous variable. Compare individuals just above and just below the cutoff — they're nearly identical except for treatment.

**Example**: Scholarship eligibility with test score ≥ 50.

- Students scoring 49: No scholarship
- Students scoring 51: Scholarship
- These students are virtually identical (differ by 2 points due to noise)
- Difference in outcomes at cutoff ≈ causal effect of scholarship

**Sharp RD**: Treatment probability jumps from 0 to 1 at cutoff.
**Fuzzy RD**: Treatment probability jumps but not discontinuously (e.g., 20% → 80%). Use IV-like methods.

**Famous example**: Thistlethwaite & Campbell (1960) — effect of merit awards on ambition. Students scoring just above threshold got awards. Comparing just-above to just-below identifies causal effect.

**Limitation**: Only identifies local effect at the cutoff. May not generalize to those far from cutoff.

### Difference-in-Differences (DiD)

Compare **change** in outcomes before/after treatment between treated and control groups.

```
DiD = (Treated_after - Treated_before) - (Control_after - Control_before)
```

**Key assumption**: **Parallel trends** — without treatment, both groups would have changed similarly over time.

**Example**: Card & Krueger (1994) minimum wage study.

- **Treatment**: New Jersey raised minimum wage (1992)
- **Control**: Pennsylvania (neighboring state, didn't raise wage)
- **Outcome**: Fast-food employment

| | Before | After | Change |
|--|--------|-------|--------|
| **NJ** | 20.4 | 21.0 | +0.6 |
| **PA** | 23.3 | 21.2 | -2.1 |
| **DiD** | | | +0.6 - (-2.1) = **+2.7** |

Minimum wage increase in NJ was associated with *increased* employment relative to PA (contrary to standard economic theory). Controversial and debated.

**Limitation**: Parallel trends assumption is untestable (we can't observe the counterfactual trend). Can check pre-treatment trends, but this doesn't guarantee parallel post-treatment trends.

## Confounders, Mediators, Moderators, and Colliders

| Type | Structure | Definition | Action |
|------|-----------|------------|--------|
| **Confounder** | C → X, C → Y | Causes both treatment and outcome | **Control for it** (blocks spurious path) |
| **Mediator** | X → M → Y | Mechanism through which X affects Y | **Don't control** (blocks the causal path you want to estimate) |
| **Moderator** | Effect of X on Y differs by level of M | Third variable that changes the strength/direction of X → Y | **Interaction analysis** (estimate effects separately by M) |
| **Collider** | X → C ← Y | Caused by both X and Y | **Don't control** (creates spurious association) |

**Critical insight**: "Control for everything" is **wrong**. You must know the causal structure.

### Detailed Examples

**Confounder**: Estimating effect of exercise (X) on heart disease (Y).
- Age (C) causes both less exercise and more heart disease
- If you don't control for age, you overestimate harm of inactivity
- Control for age to isolate effect of exercise

**Mediator**: Estimating effect of education (X) on income (Y).
- Occupation (M) is on the causal path: Education → Occupation → Income
- If you control for occupation, you block the mechanism
- Don't control if you want the total effect
- Do control if you want the direct effect (not through occupation)

**Moderator**: Effect of tutoring (X) on test scores (Y) differs by prior ability (M).
- High-ability students benefit more from tutoring than low-ability
- M doesn't cause X or Y, but changes the X → Y relationship
- Estimate separate effects for high-ability vs low-ability (interaction)

**Collider**: Estimating correlation between beauty (X) and talent (Y) among actors (C).
- Beauty and talent independently cause being an actor
- Don't condition on "is an actor" — it creates spurious negative correlation
- In general population, beauty and talent are uncorrelated

## Simpson's Paradox

An association that appears in every subgroup can **reverse** when subgroups are combined (or vice versa).

**Classic example**: UC Berkeley admission rates (1973)

| | Men | Women |
|--|-----|-------|
| **Overall** | 44% admitted | 35% admitted |

Looks like gender bias favoring men.

**But breaking down by department**:

| Department | Men Admitted | Women Admitted |
|-----------|--------------|----------------|
| A | 62% | 82% |
| B | 63% | 68% |
| C | 37% | 34% |
| D | 33% | 35% |
| E | 28% | 24% |
| F | 6% | 7% |

In 4 of 6 departments, women had higher admission rates! How?

**Explanation**: Women applied to more competitive departments (A, B had high admission rates; women applied to C-F with low rates). Men applied to easier departments. The aggregate reversal is Simpson's paradox.

**General structure**: Treatment A better than B in every subgroup, but B better overall. This happens when:
1. Subgroups have different base rates
2. Treatment assignment correlates with subgroup

### Medical Example

| | Treatment A | Treatment B |
|--|-------------|-------------|
| **Mild cases** | 85% recover (100/117) | 80% recover (192/240) |
| **Severe cases** | 50% recover (30/60) | 40% recover (8/20) |
| **Overall** | 76% (130/177) | **77% (200/260)** |

Treatment A is better in both subgroups but worse overall. Why? Treatment A was disproportionately given to severe cases (who have worse outcomes regardless). Treatment B was given mostly to mild cases.

**Resolution**: Which comparison is causal?

- If treatment assignment was random within severity groups, compare within groups (A is better).
- If severity is a **mediator** (treatment → severity → outcome), compare overall (B is better).
- If severity is a **confounder** (severity → treatment and severity → outcome), control for severity (A is better).

The correct answer depends on the **causal structure**, not just the data.

## Hill's Criteria for Causation (1965)

Austin Bradford Hill proposed nine criteria for inferring causation from observational associations. Not all are necessary, and none are sufficient, but they provide heuristics.

| Criterion | Description | Example (Smoking → Cancer) |
|-----------|-------------|---------------------------|
| **Strength** | Strong association more likely causal | Relative risk ~10-20x for heavy smokers |
| **Consistency** | Replicated across studies, populations, methods | Hundreds of studies, many countries |
| **Specificity** | Specific cause → specific effect | Lung cancer, not all cancers |
| **Temporality** | Cause precedes effect | Smoking before cancer diagnosis |
| **Dose-response** | More exposure → more effect | More cigarettes → higher risk |
| **Plausibility** | Plausible mechanism | Tar, carcinogens in smoke |
| **Coherence** | Consistent with known facts | Lung cancer rose with cigarette popularity |
| **Experiment** | Randomized trial evidence | Animal experiments show causation |
| **Analogy** | Similar causes have similar effects | Other inhaled carcinogens cause cancer |

**Temporality** is the only essential criterion (cause must precede effect). The others strengthen the case.

**Limitation**: These are heuristics, not formal tests. Strong correlation can exist without causation (confounding). Weak correlation can exist with causation (small effects, high noise).

## Key Terms

- **Counterfactual**: What would have happened if treatment hadn't occurred; unobservable
- **Average Treatment Effect (ATE)**: E[Y₁ - Y₀] — average causal effect in population
- **Fundamental Problem**: Can't observe both Y₁ and Y₀ for the same unit
- **Confounding**: Third variable causing both treatment and outcome, creating spurious association
- **DAG**: Directed Acyclic Graph — visual causal model with nodes (variables) and arrows (effects)
- **Collider**: Variable caused by two others; conditioning on it creates bias
- **do-Operator**: Pearl's intervention operator; do(X) ≠ observing X
- **Backdoor Criterion**: Conditions for identifying causal effects from observational data
- **Instrumental Variable**: Affects treatment but not outcome except through treatment
- **Regression Discontinuity**: Exploits treatment cutoff; compares just above/below threshold
- **Difference-in-Differences**: Compares changes over time between treatment and control groups
- **Simpson's Paradox**: Association reverses when data aggregated/disaggregated
- **Mediator**: Variable on causal path between treatment and outcome
- **Moderator**: Variable that changes the strength/direction of causal effect
- **Parallel Trends**: DiD assumption that treatment and control would change similarly without treatment
- **Intention-to-Treat**: Analyzing subjects as assigned, not as actually treated
- **External Validity**: Whether findings generalize beyond study context
- **SUTVA**: Stable Unit Treatment Value Assumption — your treatment doesn't affect my outcome

## Summary

Causal inference is the science of distinguishing causation from correlation. The counterfactual framework defines causation (what would have happened otherwise) but faces the fundamental problem: counterfactuals are unobservable. The solution is estimating average causal effects by comparing groups.

Randomized controlled trials are the gold standard — random assignment eliminates confounding. But RCTs are often impossible (ethics, cost, feasibility). Quasi-experimental methods exploit natural experiments: instrumental variables (natural randomization of treatment), regression discontinuity (treatment cutoffs create local randomization), and difference-in-differences (compare changes over time).

Structural causal models (DAGs) formalize causal reasoning. Three key structures: chains (mediation), forks (confounding), and colliders (selection bias). The do-calculus distinguishes observing from intervening. The backdoor criterion specifies when adjustment (controlling for confounders) identifies causal effects.

Critical insight: You can't blindly "control for everything." Controlling for mediators blocks the causal mechanism. Controlling for colliders introduces bias. Causal reasoning requires theory and domain knowledge, not just statistics.

Simpson's paradox shows associations can reverse with aggregation. Resolution requires knowing the causal structure — whether a variable is a confounder, mediator, or collider determines whether to control for it.

Hill's criteria (strength, consistency, temporality, dose-response, plausibility, etc.) provide heuristics for inferring causation from association. Temporality is essential; others strengthen the case.

The practical lesson: Causation is hard. Correlation is easy to find but often misleading. RCTs provide the strongest evidence when feasible. When not, quasi-experimental designs (IV, RD, DiD) combined with careful causal reasoning (DAGs, domain knowledge) allow credible causal inference from observational data. Always ask: What's the counterfactual? What's the causal structure? What assumptions are required? Are they plausible?
