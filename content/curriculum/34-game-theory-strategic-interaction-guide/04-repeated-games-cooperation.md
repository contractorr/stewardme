# Repeated Games & Cooperation

## Infinitely Repeated Games

**Setup**: Stage game G played repeatedly, infinitely many times

**Observation**: After each round t, all previous actions (a₁, ..., aₜ) observed (complete history)

**Strategy**: Contingent plan specifying action in round t as function of history (a₁, ..., aₜ₋₁)

**Payoffs**: Discounted sum of stage game payoffs
```
Uᵢ = Σ δᵗ uᵢ(aₜ) for t = 0 to ∞
```
where δ ∈ (0, 1) is discount factor (patience parameter)

**Interpretation of δ**:
- δ close to 1: Patient (values future almost as much as present)
- δ close to 0: Impatient (heavily discounts future)
- Can also represent continuation probability (game continues next round with prob δ)

## Repeated Prisoner's Dilemma

**Stage game**:
|               | Cooperate | Defect |
|---------------|-----------|--------|
| **Cooperate** | 3, 3      | 0, 5   |
| **Defect**    | 5, 0      | 1, 1   |

**One-shot**: Unique Nash equilibrium (Defect, Defect) = (1, 1)

**Infinitely repeated**: Can sustain cooperation as equilibrium

### Grim Trigger Strategy

**Definition**: Cooperate until opponent defects once, then defect forever

**Analysis**: Suppose both play grim trigger

**If both cooperate forever**:
```
Payoff = 3 + δ·3 + δ²·3 + ... = 3/(1 - δ)
```

**If deviate to Defect (then opponent triggers)**:
```
Payoff = 5 + δ·1 + δ²·1 + ... = 5 + δ/(1 - δ)
```

**Cooperation sustained if**:
```
3/(1 - δ) ≥ 5 + δ/(1 - δ)
3 ≥ 5(1 - δ) + δ
3 ≥ 5 - 5δ + δ
4δ ≥ 2
δ ≥ 1/2
```

**Result**: If δ ≥ 1/2 (sufficiently patient), mutual cooperation is Nash equilibrium

**Intuition**: Short-term gain from defection (5 vs 3 = +2) outweighed by long-term loss from permanent retaliation (3 vs 1 = -2 per period, forever)

### Tit-for-Tat

**Definition**: Cooperate in round 1. In round t > 1, copy opponent's round t-1 action.

**Properties**:
- **Nice**: Never defects first
- **Retaliatory**: Punishes defection immediately
- **Forgiving**: Returns to cooperation if opponent does

**Axelrod tournaments** (1980s):
- Computer simulation: Strategies compete in round-robin repeated Prisoner's Dilemma
- Tit-for-tat (submitted by Anatol Rapoport) won both tournaments
- Beat complex strategies despite simplicity

**Robustness**: Tit-for-tat performs well against wide variety of strategies (never exploited badly, reciprocates cooperation)

**Weakness**: Error-prone. If one player mistakenly defects, triggers alternating retaliation (D-C-D-C-...). **Tit-for-two-tats** (forgive one defection) more robust.

### Folk Theorem

**Theorem**: In infinitely repeated game, if players sufficiently patient (δ close to 1), any individually rational payoff profile can be sustained as Nash equilibrium.

**Individually rational**: Payoffs ≥ minimax payoffs (worst opponent can force you to)

**Prisoner's Dilemma example**:
- Minimax payoff: 1 (opponent defects, I defect)
- Any payoff profile (p₁, p₂) where p₁, p₂ ∈ [1, 3] sustainable if δ high enough
- Includes (3, 3), (2, 2.5), (1.5, 2), etc.

**Mechanism**: Threaten to revert to minimax punishment if deviation occurs. If threat credible and future valuable, compliance optimal.

**Implication**: Wide range of outcomes possible. Repetition enables cooperation, but equilibrium selection remains problem (which of many equilibria will occur?).

**Applications**:
- Cartels: Firms collude on high prices (above Bertrand = marginal cost). Deviation (undercut price) triggers price war. Sustainable if future profits valuable.
- International treaties: Countries cooperate (e.g., reduce emissions). Defection triggers retaliation. Sustainable without enforcement if interactions repeat.
- Social norms: Community enforces cooperative behavior. Violators punished (ostracism, reputational harm). Stable if community long-lived.

## Finitely Repeated Games

**Backward induction logic**: In final round, play one-shot Nash equilibrium. Knowing this, round T-1 identical to one-shot → play Nash. Unravels to first round.

**Prisoner's Dilemma** (finite T rounds):
- Round T: Defect (one-shot Nash)
- Round T-1: Cooperation not sustainable (no future to punish in)
- **Unraveling**: Defect in all rounds

**Exception**: If stage game has multiple Nash equilibria, can coordinate on preferable equilibria in early rounds (threatened switch to worse equilibrium if deviation).

**Example: Battle of Sexes** (repeated T times):
- Two Nash: (Opera, Opera) = (2, 1) and (Football, Football) = (1, 2)
- Can alternate: Opera in odd rounds, Football in even
- Average payoffs: (1.5, 1.5) better than always one equilibrium
- Deviation triggers reversion to worse equilibrium for deviator

## Reputation and Trust

**Reputation**: Belief about opponent's type based on observed behavior

**Repeated Trust Game** (infinite horizon):
- Each round: Trustor decides Trust or Not Trust
- If Trust, Trustee decides Return or Keep
- Payoffs: (Return: 2, 2), (Keep: 0, 3), (Not Trust: 1, 1)
- One-shot: Trustee keeps → Trustor doesn't trust

**Reputation equilibrium**:
- Trustee returns to build reputation (signal trustworthiness)
- Trustor trusts as long as Trustee has returned previously
- Deviation (keep) ends relationship
- Sustainable if δ high enough

**Calculation**:
Always return: Payoff = 2/(1 - δ)
Defect at round t: Payoff = 3 + δ·1/(1 - δ)
Require: 2/(1 - δ) ≥ 3 + δ/(1 - δ) → δ ≥ 1/2

**Applications**:
- eBay/Amazon marketplace: Sellers build reputation → buyers trust → repeat business
- Employment: Worker builds reputation → promotions, wage increases
- Business relationships: Supplier reliability → long-term contracts

**Empirical**: Online markets heavily reputation-dependent. Sellers with higher ratings command price premiums, higher sales volume.

## Cooperation in Nature: Evolutionary Game Theory

**Biological applications**: Genes/organisms as players, fitness as payoffs

**Repeated interactions**: Many organisms interact repeatedly (same individuals or genetic relatives)

**Hawk-Dove Game** (animal contests over resources):

|               | Hawk  | Dove  |
|---------------|-------|-------|
| **Hawk**      | -1,-1 | 2, 0  |
| **Dove**      | 0, 2  | 1, 1  |

- Hawk: Escalate (fight)
- Dove: Display only
- If both Hawk: Fight (both injured, -1)
- If Hawk vs Dove: Hawk wins resource (2, 0)
- If both Dove: Share resource (1, 1)

**One-shot**: Two pure Nash equilibria (H, D) and (D, H). Mixed equilibrium: both play H with prob 1/2.

**Repeated**: Bourgeois strategy (common in nature):
- If territory owner: Play Hawk
- If intruder: Play Dove
- Respects property rights

**ESS (Evolutionarily Stable Strategy)**: Strategy that, if adopted by population, cannot be invaded by mutant strategy

Bourgeois is ESS: Respect property → avoids costly conflicts. Invader playing "always Hawk" would lose on average (wins when intruding but loses when defending).

**Vampire bats**: Share blood with roost-mates (reciprocal altruism). Bats that shared previously more likely to receive donations. Defectors (don't share when fed) punished (denied donations). Sustained by repeated interactions + kin selection.

**Prisoner's Dilemma in bacteria**: Yeast cells secrete invertase (enzyme digesting sucrose). Costly to produce but benefits all nearby cells. Cooperator: Secretes. Defector: Doesn't secrete. In well-mixed populations, defection spreads. In spatially structured populations (clumps), cooperation stable (cooperators interact with cooperators).

## Collusion and Antitrust

**Cartel**: Firms coordinate to raise prices above competitive level

**Bertrand competition** (one-shot):
- Price competition
- Nash equilibrium: P = marginal cost (zero profit)

**Repeated Bertrand**:
- Firms can sustain P > MC via trigger strategies
- Deviation: Undercut price slightly → capture entire market temporarily
- Punishment: Revert to P = MC (competitive pricing) forever

**Sustainability condition**:
Let P* = collusive price, MC = marginal cost, Q = market quantity

Collusion payoff per period: π* = (P* - MC)·Q/n (assume equal shares among n firms)

Deviation: Undercut → capture full market → π_dev ≈ (P* - MC)·Q

Collusion forever:
```
Payoff = π* + δπ* + δ²π* + ... = π*/(1 - δ)
```

Deviate + punishment:
```
Payoff = π_dev + δ·0 + δ²·0 + ... = π_dev
```

Collusion sustained if:
```
π*/(1 - δ) ≥ π_dev
π*/n ≥ (1 - δ)·π*
1/n ≥ 1 - δ
δ ≥ 1 - 1/n = (n - 1)/n
```

**Implication**: More firms → harder to collude (higher δ required)
- n = 2 (duopoly): δ ≥ 1/2
- n = 5: δ ≥ 4/5
- n → ∞: δ → 1 (nearly impossible)

**Antitrust policy**: Break up cartels (increase n), increase detection probability (lowers effective δ via legal penalties), limit communication (prevents coordination on equilibrium).

**OPEC example**: Oil cartel attempts to restrict supply → raise prices. But:
- Cheating temptation (produce above quota)
- Detection lags (production hard to monitor)
- Many producers (OPEC = 13 members, non-OPEC = rest of world)
- Result: Frequent quota violations, periodic price collapses

**Airline pricing**: Implicitly coordinated (especially on routes with 2-3 carriers). Price changes announced publicly → rivals match. Enables soft collusion without explicit communication.

## Renegotiation and Pareto-Improving Punishments

**Problem with grim trigger**: Punishment (permanent defection) hurts both punisher and punished. After deviation, both would prefer renegotiate back to cooperation.

**Renegotiation-proof equilibrium**: Equilibrium where, at every history, continuation play is Pareto-efficient (no renegotiation incentive)

**Example**: Prisoner's Dilemma with grim trigger
- After deviation, revert to (D, D) = (1, 1) forever
- Both prefer return to (C, C) = (3, 3)
- If renegotiation possible, threat not credible → original cooperation not sustainable

**Solutions**:
- **Finite punishment**: Defect for T periods, then return to cooperation. Pareto-efficient if T chosen correctly.
- **Asymmetric punishment**: Punish deviator more than punisher (requires ability to identify deviator).
- **Contractual commitment**: External enforcement prevents renegotiation (courts, third-party monitoring).

**Abreu's "optimal penal codes"** (1986): Design punishments that are severe enough to deter, but minimal (Pareto-efficient along punishment path).

## Experiments and Behavioral Findings

**Repeated Prisoner's Dilemma experiments**:
- Initial cooperation: 40-60% cooperate in early rounds
- Decay over repetitions: Cooperation declines (10-30% by final rounds in finite games)
- **End-game effect**: Defection spikes in last few rounds (anticipation of final period)
- Partner effects: Fixed pairs cooperate more than randomly rematched pairs

**Heterogeneity**:
- ~25% always defect (free-riders)
- ~25% always cooperate (unconditional cooperators)
- ~50% conditional cooperators (cooperate if partner cooperates, defect if partner defects)

**Cultural differences** (Henrich et al., 2001):
- Ultimatum Game offers vary across cultures (15-50% modal offers)
- Repeated games: Cooperation rates vary but qualitative patterns similar

**Reciprocity**: Strong evidence for direct reciprocity (tit-for-tat-like behavior) and indirect reciprocity (helping those who helped others → reputation).

## Key Terms

- **Infinitely repeated game**: Stage game played infinite times with discounting
- **Discount factor δ**: Weight on future payoffs (δ ∈ (0,1); higher = more patient)
- **Grim trigger**: Cooperate until opponent defects once, then defect forever
- **Tit-for-tat**: Cooperate initially, then copy opponent's previous move
- **Folk theorem**: Wide range of payoffs sustainable as equilibria if players sufficiently patient
- **Minimax payoff**: Worst outcome opponent can force player to
- **Renegotiation-proof**: Equilibrium with no incentive to renegotiate at any history
- **ESS (Evolutionarily Stable Strategy)**: Strategy that resists invasion by mutants
- **Cartel**: Firms coordinating to raise prices above competitive level

## Summary

Infinite repetition transforms incentives. Prisoner's Dilemma: One-shot Nash = (Defect, Defect), but repeated → cooperation sustainable via grim trigger if δ ≥ 1/2. Tit-for-tat (cooperate initially, copy opponent's previous move) won Axelrod tournaments—simple, robust, never exploited badly. Folk Theorem: Any individually rational payoffs sustainable if players sufficiently patient (δ near 1). Mechanism: Threaten reversion to punishment if deviation.

Finite repetition unravels via backward induction (Prisoner's Dilemma: defect all rounds), but exceptions exist with multiple stage-game equilibria. Reputation sustains cooperation: Trust game experiments show relationship-building (e.g., eBay sellers, employment). Evolutionary games: Hawk-Dove → Bourgeois strategy (respect property) is ESS. Vampire bats, yeast cooperate via repeated interactions.

Collusion in oligopolies: Repeated Bertrand → firms sustain P > MC via trigger strategies. Sustainability requires δ ≥ (n-1)/n (more firms → harder to collude). Antitrust breaks cartels. OPEC struggles (cheating, detection lags, many producers). Renegotiation problem: Grim trigger hurts both players → incentive to renegotiate → undermines deterrence. Solutions: Finite punishment, optimal penal codes, external enforcement.

Experiments: Initial cooperation (40-60%) decays over rounds. Heterogeneity: Unconditional cooperators (~25%), conditional cooperators (~50%), free-riders (~25%). End-game effect in finite games. Reciprocity (direct and indirect) documented cross-culturally. Repetition enables cooperation, but sustainability depends on patience (δ), observability, credibility of punishment, and absence of renegotiation opportunities.
