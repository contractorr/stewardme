# Game Theory & Strategic Reasoning

## Overview

Game theory is the mathematical study of strategic interaction — situations where your best action depends on what others do. It provides tools for analyzing conflict, cooperation, bargaining, and mechanism design across economics, politics, biology, and everyday life.

Unlike decision theory (choosing against nature), game theory involves strategic interdependence. Your optimal choice depends on others' choices, which depend on their predictions of your choice, which depend on your predictions of their predictions... Game theory formalizes this recursive reasoning.

Applications range from nuclear deterrence to auction design, from evolution to business strategy, from voting to negotiation. Understanding game theory reveals strategic structures underlying seemingly disparate situations.

## Normal Form Games

A game in **normal (strategic) form** specifies:
1. **Players**: Who makes decisions (2+ players)
2. **Strategies**: Actions available to each player
3. **Payoffs**: Outcome for each combination of strategies

### Example: Prisoner's Dilemma

| | B: Cooperate | B: Defect |
|--|-------------|-----------|
| **A: Cooperate** | 3, 3 | 0, 5 |
| **A: Defect** | 5, 0 | 1, 1 |

First number = A's payoff, second = B's payoff.

### Dominant Strategies

A strategy is **strictly dominant** if it's the best response regardless of what others do.

In Prisoner's Dilemma:
- If B cooperates, A gets 3 (cooperate) or 5 (defect) → defect better
- If B defects, A gets 0 (cooperate) or 1 (defect) → defect better
- **Defect dominates cooperate** for both players

When both use dominant strategies: (Defect, Defect) with payoff (1,1). Yet both would prefer (Cooperate, Cooperate) with payoff (3,3). This tension — individual rationality leads to collective irrationality — defines the dilemma.

### Nash Equilibrium

**Definition**: A set of strategies where no player can improve by unilaterally changing strategy. Formally: For each player i, strategy s*ᵢ is a **best response** to all other players' strategies s*₋ᵢ.

**Nash's Theorem** (1950): Every finite game has at least one Nash equilibrium (possibly in mixed strategies).

**Key properties**:
- Nash equilibria aren't necessarily good outcomes (Prisoner's Dilemma)
- Nash equilibria aren't necessarily unique (Battle of the Sexes has two)
- Nash equilibria aren't necessarily stable in all senses (Chicken)
- Nash equilibrium is about mutual best responses, not optimality

### Finding Nash Equilibria

**Best response method**:
1. For each player, identify best response to each opponent strategy
2. Find strategy combinations where each player is playing a best response

**Example**: Battle of the Sexes

| | B: Opera | B: Football |
|--|---------|-------------|
| **A: Opera** | 3, 2 | 0, 0 |
| **A: Football** | 0, 0 | 2, 3 |

A's best responses: Opera if B plays Opera; Football if B plays Football
B's best responses: Opera if A plays Opera; Football if A plays Football

**Nash equilibria**: (Opera, Opera) with payoff (3,2) and (Football, Football) with payoff (2,3).

Both are equilibria, but they differ in distribution. Coordination is valuable, but on whose terms?

## Classic Games and Strategic Structures

### Prisoner's Dilemma (Social Dilemma)

**Structure**: Dominant strategy → suboptimal outcome.

**Real-world examples**:
- **Arms races**: Each country prefers to arm (dominates) but both disarming would be better
- **Climate agreements**: Each country prefers to pollute (free-ride) but collective action needed
- **Doping in sports**: Each athlete has incentive to dope, but clean sport better for all
- **Price wars**: Each firm wants to undercut, but high prices better for both
- **Overfishing**: Each fisher wants to catch more, but restraint preserves the resource

**Resolution mechanisms**:
- Repetition (folk theorem — see below)
- Enforceable contracts (external enforcement)
- Reputation (in repeated or networked settings)
- Social norms and punishment
- Changing payoffs (altruism, reciprocity, fairness preferences)

### Stag Hunt (Coordination Game)

| | B: Stag | B: Hare |
|--|---------|---------|
| **A: Stag** | 5, 5 | 0, 3 |
| **A: Hare** | 3, 0 | 3, 3 |

**Two Nash equilibria**:
1. (Stag, Stag) — payoff-dominant equilibrium (5,5)
2. (Hare, Hare) — risk-dominant equilibrium (3,3)

Hunting stag requires cooperation (both must hunt stag to succeed). Hunting hare is safe (succeeds alone, payoff 3).

**Dilemma**: (Stag, Stag) is better, but risky. If the other hunts hare, you get 0 hunting stag but 3 hunting hare. Trust and coordination matter.

**Real examples**:
- **Technology standards**: VHS vs Betamax, Blu-ray vs HD-DVD. Better technology may lose if coordination fails.
- **Bank runs**: Everyone prefers the bank to remain stable, but if others withdraw, you should too (hare = withdraw).
- **Investment coordination**: Projects succeed only if enough investors commit.

**Resolution**: Communication, leadership, focal points, conventions.

### Battle of the Sexes (Distributional Conflict)

| | B: Opera | B: Football |
|--|---------|-------------|
| **A: Opera** | 3, 2 | 0, 0 |
| **A: Football** | 0, 0 | 2, 3 |

**Two pure Nash equilibria** with different distributional preferences. Both prefer being together over being apart, but A prefers opera and B prefers football.

**Problem**: Coordination + distribution. How do we coordinate on one equilibrium? Who gets their preferred outcome?

**Real examples**:
- **Household decisions**: Where to live, where to vacation, whose career to prioritize
- **Business partnerships**: Which project to pursue, how to split equity
- **Political coalitions**: Which policy to support (all prefer coalition over opposition, but differ on policy)

**Resolutions**: Alternation, side payments, randomization, social conventions (e.g., gender norms historically favored one party).

### Chicken (Anti-Coordination Game)

| | B: Swerve | B: Straight |
|--|----------|------------|
| **A: Swerve** | 3, 3 | 2, 4 |
| **A: Straight** | 4, 2 | 0, 0 |

**Two pure Nash equilibria**:
1. (Swerve, Straight) — A yields, B wins (2,4)
2. (Straight, Swerve) — A wins, B yields (4,2)

Both going straight = mutual disaster (0,0). Both swerving = okay but not great (3,3). The best is being the one who doesn't swerve (4) while the other swerves (2).

**Strategic insight**: Commitment is valuable. If you can credibly commit to "straight" (e.g., visibly throw away your steering wheel), the opponent must swerve. **Brinkmanship** — making your threat credible even if costly.

**Real examples**:
- **Nuclear deterrence**: "Mutually Assured Destruction" — credible threat of retaliation deters first strike
- **Budget negotiations**: Threatening government shutdown
- **Lane merging**: Who yields?
- **Legal disputes**: Threatening to go to trial (costly for both)

**Thomas Schelling's insight**: Sometimes **limiting your own options** gives you strategic advantage. Burning bridges, making binding commitments, appearing irrational — all can force opponents to accommodate.

### Matching Pennies (Zero-Sum)

| | B: Heads | B: Tails |
|--|---------|---------|
| **A: Heads** | 1, -1 | -1, 1 |
| **A: Tails** | -1, 1 | 1, -1 |

A wins if pennies match; B wins if they differ.

**No pure strategy Nash equilibrium**. Whatever A does, B wants to do the opposite. Whatever B does, A wants to match.

**Mixed strategy equilibrium**: Both randomize 50-50. In equilibrium, each earns expected payoff of 0.

## Mixed Strategies

When no pure strategy Nash equilibrium exists (or when randomization is optimal), players **mix** — choose strategies probabilistically.

### Definition

A **mixed strategy** assigns probabilities to pure strategies. Player i chooses pure strategy sᵢⱼ with probability pᵢⱼ, where Σⱼ pᵢⱼ = 1.

### Mixed Strategy Nash Equilibrium

Each player mixes such that the opponent is indifferent among their pure strategies (each pure strategy has the same expected payoff).

**Example**: Matching Pennies

If A plays Heads with probability p and Tails with probability 1-p:
- B's expected payoff from Heads: p(-1) + (1-p)(1) = 1 - 2p
- B's expected payoff from Tails: p(1) + (1-p)(-1) = 2p - 1

For B to mix, these must be equal: 1 - 2p = 2p - 1 → p = 0.5

Similarly, B must play 50-50 to make A indifferent. **Mixed equilibrium**: Both play 50-50.

### Real-World Mixing

**Penalty kicks** (soccer): Palacios-Huerta (2003) analyzed 1,417 penalty kicks. Kickers and goalkeepers mix roughly 60% left, 40% right (actual percentages vary by foot preference). Empirical frequencies match Nash predictions remarkably well.

**Military tactics**: Attack points, patrol routes, bombing times — unpredictability is strategic. Predictable strategies are exploitable.

**Inspection games**: Tax audits, customs inspections, quality control — randomization prevents gaming the system.

**Tennis serves**: Randomizing between serves makes opponent uncertain.

**Poker**: Bluffing frequencies follow game-theoretic predictions among experts.

## Sequential Games and Backward Induction

In **sequential games**, players move in turns. Represented by **game trees** (extensive form).

### Backward Induction

Solve from the end:
1. Identify final decision nodes — determine optimal choice
2. Work backward — what would the second-to-last player do, knowing the final player's choice?
3. Continue backward to the beginning

**Example**: Entry Deterrence

```
Firm A (Entrant)
    |
    +-- Enter
    |    |
    |    Firm B (Incumbent)
    |        |
    |        +-- Fight (-1, -1)
    |        +-- Accommodate (2, 2)
    |
    +-- Stay Out (0, 5)
```

**Backward induction**:
1. If A enters, B chooses between Fight (-1) and Accommodate (2). B chooses Accommodate.
2. Knowing this, A chooses between Enter (payoff 2) and Stay Out (payoff 0). A chooses Enter.
3. **Outcome**: (Enter, Accommodate) with payoff (2, 2)

B's threat to "Fight" is **not credible** — when the moment comes, fighting hurts B more than accommodating. A knows this and enters.

### Subgame Perfect Equilibrium

**Definition**: A Nash equilibrium that is also a Nash equilibrium in every **subgame** (every decision subtree).

This eliminates "incredible threats" — threats that wouldn't actually be carried out if put to the test.

In Entry Deterrence:
- (Stay Out, Fight) is a Nash equilibrium in the whole game (if A believes B will fight, A stays out)
- But it's not subgame perfect — in the subgame starting after A enters, Fight is not a best response

**Subgame perfect equilibrium**: (Enter, Accommodate).

### Commitment Value

Sometimes **limiting your own options is valuable**. If B could credibly commit to fighting (e.g., by installing automatic defenses that fight regardless of B's later preference), A would stay out.

**Schelling's insight**: Strategic moves (commitments, threats, promises) change the game tree. Commitment devices make otherwise incredible threats credible.

**Examples**:
- **Burning bridges** (Cortés scuttling ships): Makes retreat impossible → soldiers fight harder → opponent more likely to surrender
- **Contractual penalties**: "If I don't deliver, I owe $1 million" makes your commitment credible
- **Delegation**: Hiring an agent with different preferences ("Don't negotiate, only fight") commits you

## Repeated Games and the Folk Theorem

When players interact repeatedly, cooperation can emerge even without external enforcement.

### Finitely vs Infinitely Repeated

**Finitely repeated**: Backward induction unravels cooperation. In the last round, players defect (no future). Knowing this, they defect in second-to-last round. Unraveling continues to the first round.

**Infinitely repeated** (or uncertain ending): No definite last round, so backward induction doesn't apply. Folk theorem applies.

### The Folk Theorem

In infinitely repeated games (or games with uncertain ending), virtually **any feasible, individually rational outcome** can be sustained as an equilibrium through **trigger strategies**, provided players are sufficiently patient (discount factor δ close enough to 1).

**Trigger strategies**:

**Grim trigger**: Cooperate until opponent defects, then defect forever.
- Punishment is severe (permanent)
- Not forgiving
- Clear signal

**Tit-for-tat**: Mirror opponent's last move.
- Start with cooperation
- Retaliate immediately if defected against
- Forgive immediately if cooperation resumes
- Simple, forgiving, retaliatory

**Win-stay, lose-shift**: If last payoff was good, repeat strategy; if bad, switch.

### Conditions for Cooperation

1. **Repeated interaction**: One-shot → defect. Repeated → cooperation possible.
2. **Shadow of the future**: High probability of future interaction (δ close to 1). If δ too low, immediate gain from defection outweighs future loss.
3. **Observation**: Can detect defection. If actions are unobservable, can't punish.
4. **Patience**: Value future sufficiently. Impatient players (low δ) defect even in repeated games.

**Example**: Prisoner's Dilemma with Grim Trigger

Cooperate each round: payoff 3 per round → total 3 + 3δ + 3δ² + ... = 3/(1-δ)

Defect once, then punished forever: payoff 5 (defection) + 1δ + 1δ² + ... = 5 + δ/(1-δ)

Cooperation sustained if 3/(1-δ) ≥ 5 + δ/(1-δ) → 3 ≥ 5(1-δ) + δ → 3 ≥ 5 - 4δ → δ ≥ 1/2

If players value the future at least half as much as the present (δ ≥ 0.5), cooperation can be sustained.

### Real-World Repeated Interactions

- **International relations**: Countries cooperate on trade, environment, security because they interact repeatedly
- **Business relationships**: Suppliers and buyers maintain quality/payment because of repeat business
- **Organized crime**: "Honor among thieves" — defection punished by exclusion from future cooperation
- **Online markets**: eBay, Amazon — reputation systems enable cooperation despite anonymity

## Incomplete Information and Bayesian Games

Players are uncertain about others' **types** (preferences, information, capabilities).

### Bayesian Games

Each player has:
- A **type** tᵢ (private information)
- **Beliefs** about others' types: probability distribution P(t₋ᵢ | tᵢ)
- **Strategies** that depend on type: sᵢ(tᵢ)

**Bayesian Nash Equilibrium**: Each player's strategy is a best response given their beliefs about others' types.

### Signaling Games

An **informed player** (sender) sends a **signal**; an **uninformed player** (receiver) observes the signal, updates beliefs (Bayes' theorem), and acts.

#### Spence's Job Market Signaling (1973)

**Setup**:
- Workers have ability (high or low — private information)
- Workers can get education (costly signal)
- Employers observe education, infer ability, offer wage

**Key insight**: Education may not increase productivity, but it **separates types** if:
- High-ability workers find education less costly (smarter → learn faster)
- Low-ability workers find education prohibitively costly

**Separating equilibrium**:
- High-ability workers get education (signal)
- Low-ability workers don't
- Employers infer: Educated → high ability → high wage. Uneducated → low ability → low wage.

Education is valuable to workers **as a signal**, even if it teaches nothing useful. This explains why degrees from prestigious schools command wage premiums even when curriculum is similar.

**Pooling equilibrium**: Both types get education (or neither do). Signal reveals nothing. Less efficient.

**Applications**:
- **Warranties**: High-quality producers offer warranties (signal confidence). Low-quality can't afford to (too many claims).
- **Dividends**: Profitable firms pay dividends (costly signal of confidence). Unprofitable firms can't afford to.
- **Advertising**: Expensive ads signal quality (only quality products can afford to advertise extensively).

### Screening

The **uninformed party** designs a **menu of options** to induce **self-selection**.

**Example**: Insurance companies offer:
- High deductible / low premium (attracts low-risk types)
- Low deductible / high premium (attracts high-risk types)

Each type chooses the contract designed for them, **revealing** their type through choice.

**Other examples**:
- **Quantity discounts**: Heavy users select bulk; light users select small quantities
- **Pricing tiers** (software, airlines): High-value users select premium; low-value select basic
- **Coupons**: Price-sensitive consumers clip coupons; time-rich, price-sensitive self-select

## Evolutionary Game Theory

Instead of rational agents, consider **populations** where strategies **replicate based on fitness** (payoff).

### Evolutionarily Stable Strategy (ESS)

A strategy is an **ESS** if:
1. When adopted by the whole population, it can't be invaded by any mutant strategy
2. More robust than Nash equilibrium — requires stability against evolutionary drift

**Formally**: Strategy s* is an ESS if for any mutant strategy s ≠ s*:
- Either π(s*, s*) > π(s, s*)
- Or π(s*, s*) = π(s, s*) and π(s*, s) > π(s, s)

### Hawk-Dove Game

| | Dove | Hawk |
|--|------|------|
| **Dove** | V/2, V/2 | 0, V |
| **Hawk** | V, 0 | (V-C)/2, (V-C)/2 |

V = value of resource, C = cost of fight (assume C > V → fighting is costly)

**Pure ESS?** No pure strategy is stable.
- All-Dove population: Invaded by Hawk (gets V vs V/2)
- All-Hawk population: Invaded by Dove if C > V (gets 0 vs (V-C)/2 < 0)

**Mixed ESS**: Population with proportion p of Hawks, 1-p of Doves, where p = V/C.

**Example**: If V = 2 (food worth 2 units) and C = 10 (fight costs 10 units), ESS has 20% Hawks, 80% Doves.

**Insight**: Explains why animal aggression is limited rather than total. Costly conflict selects for restraint. "Bourgeois strategy" (owner = Hawk, intruder = Dove) is also ESS in many contexts.

### Replicator Dynamics

Strategy frequency changes proportional to relative fitness:

```
dpᵢ/dt = pᵢ [π(sᵢ, p) - π̄(p)]
```

Where π(sᵢ, p) = payoff of strategy i in population p, π̄(p) = average population payoff.

Strategies with above-average payoff grow; below-average shrink. ESS are stable fixed points.

**Applications**:
- **Biology**: Evolution of cooperation, altruism, mating strategies
- **Economics**: Market dynamics, technology adoption
- **Culture**: Social norms, institutions

## Bargaining Theory

### Nash Bargaining Solution (1950)

Two players negotiate to split a surplus. If they agree, both gain; if they disagree, both get **disagreement payoff** (d₁, d₂).

The **Nash solution** maximizes the product of gains:

```
max (u₁ - d₁)(u₂ - d₂)
```

**Properties**:
- Pareto efficient (can't make one better off without hurting the other)
- Symmetric (if players are symmetric, they get equal splits)
- Independent of irrelevant alternatives
- Invariant to affine transformations of utility

**Implication**: Bargaining power depends on your **outside option** (disagreement payoff). Better BATNA (Best Alternative To Negotiated Agreement) = better bargaining position.

**Example**: Firm-union wage negotiation.
- Firm's disagreement payoff: Hire replacement workers, earn profit π₀
- Union's disagreement payoff: Strike fund, w₀
- Nash solution: Split the surplus (π - π₀ - w) in proportion to how much each values it

### Rubinstein Bargaining (1982)

**Sequential offers**: Players alternate making offers. After each rejection, there's a delay (time discounting).

**Subgame perfect equilibrium**: First proposer offers a split that makes the second player indifferent between accepting now and rejecting to make a counter-offer next period (which would be accepted).

**Result**: First-mover advantage. With discount factor δ, first proposer gets (1 + δ)/(1 + δ + δ²) ≈ 2/3 for δ → 1.

**Insight**: Patience is power. More patient player captures more surplus. Delay is costly, so agreements happen immediately in equilibrium.

### Ultimatum Game (Experimental)

**Setup**: Proposer offers a split of $10. Responder accepts (both get split) or rejects (both get $0).

**Rational prediction**: Proposer offers $0.01, Responder accepts (something > nothing).

**Actual behavior** (hundreds of experiments, many countries):
- Modal offer: $4-$5 (40-50%)
- Offers below $2 (20%) are frequently rejected
- Offers below $1 (10%) are rejected >50% of the time

**Interpretation**: Fairness norms override pure rationality. People punish unfair offers even at personal cost. "Inequity aversion" — disutility from unequal splits.

## Common Knowledge

Something is **common knowledge** if:
- Everyone knows it
- Everyone knows that everyone knows it
- Everyone knows that everyone knows that everyone knows it
- ... ad infinitum

**Notation**: E(X) = everyone knows X. Common knowledge = E(E(...E(X)...)).

### Why It Matters

**Coordinated attack problem**: Two generals on opposite hills must attack simultaneously to win. Each sends a messenger (who might be captured). Even with acknowledged receipt, neither can be *certain* the other knows they know. Common knowledge is impossible with unreliable communication → perfect coordination impossible.

**Bank runs**: Private knowledge that a bank is solvent doesn't prevent runs. If depositors don't know that *others* know the bank is solvent, each fears others will withdraw (stag hunt) → run occurs. **Public announcement** creates common knowledge → stabilizes.

**Market crashes**: Everyone might privately believe a stock is overvalued, but if it's not common knowledge that everyone believes this, no one sells (fear of selling too early). Public information (news, analyst reports) creates common knowledge → triggers selling.

**Applications**:
- Central bank announcements (create common knowledge to coordinate expectations)
- Public commitments vs private promises
- Advertising (creates common knowledge of brand quality)

## Key Terms

- **Nash Equilibrium**: No player improves by unilateral strategy change; mutual best responses
- **Dominant Strategy**: Best response regardless of others' strategies
- **Mixed Strategy**: Randomizing among strategies with specific probabilities
- **Subgame Perfect Equilibrium**: Nash equilibrium in every subgame; eliminates incredible threats
- **Backward Induction**: Solving sequential games from the end to the beginning
- **Folk Theorem**: Cooperation sustainable in repeated games with patient players
- **ESS** (Evolutionarily Stable Strategy): Strategy that can't be invaded by mutants; stable under replicator dynamics
- **Signaling**: Informed player reveals type through costly action (Spence)
- **Screening**: Uninformed player designs menu to induce self-selection
- **Common Knowledge**: Everyone knows X, everyone knows everyone knows X, ad infinitum
- **Bargaining Power**: Determined by outside options (disagreement payoff)
- **Trigger Strategy**: Cooperate until defection, then punish (grim trigger, tit-for-tat)
- **Bayesian Game**: Game with incomplete information; players have types and beliefs
- **Separating Equilibrium**: Different types choose different actions; signal is informative
- **Pooling Equilibrium**: All types choose same action; signal is uninformative

## Summary

Game theory provides frameworks for strategic interaction. Nash equilibrium — mutual best responses — is the central solution concept. Classic games capture recurring strategic structures: Prisoner's Dilemma (dominant strategies → suboptimal outcome), Stag Hunt (coordination with risk), Battle of the Sexes (coordination + distribution), Chicken (brinkmanship and commitment).

Mixed strategies explain randomization in penalty kicks, military tactics, and inspection. Sequential games require backward induction; subgame perfect equilibrium eliminates incredible threats. Commitment — limiting your options — can be strategically valuable (Schelling).

Repeated interaction enables cooperation through the folk theorem. Trigger strategies (grim trigger, tit-for-tat) sustain cooperation when players are patient, can observe actions, and interact repeatedly. The shadow of the future overcomes the Prisoner's Dilemma.

Incomplete information introduces Bayesian games, signaling, and screening. Spence's job market model shows education can be valuable as a signal even if unproductive. Employers screen by offering contracts that induce self-selection.

Evolutionary game theory drops rationality, studying strategy dynamics in populations. ESS are more robust than Nash equilibria. Hawk-Dove game explains limited aggression.

Bargaining theory (Nash solution, Rubinstein model) shows bargaining power depends on outside options and patience. Ultimatum game experiments reveal fairness norms override narrow self-interest.

Common knowledge — seemingly abstract — is essential for coordination and explains bank runs, market crashes, and the power of public information.

The practical lesson: Strategic situations require thinking about what others will do, what they think you'll do, what they think you think they'll do... Game theory formalizes this reasoning, revealing when cooperation is possible (repeated games), when commitment helps (sequential games), when randomization is optimal (mixed strategies), and when signals matter (incomplete information).
