# Normal Form Games & Nash Equilibrium

## Strategic Form (Normal Form) Representation

**Definition**: Game specified by:
1. **Players**: N = {1, 2, ..., n} (finite set)
2. **Strategy spaces**: Sᵢ for each player i (set of available strategies)
3. **Payoff functions**: uᵢ: S₁ × S₂ × ... × Sₙ → ℝ (maps strategy profile to player i's payoff)

**Strategy profile**: s = (s₁, s₂, ..., sₙ) where sᵢ ∈ Sᵢ

**Notation**:
- s₋ᵢ = (s₁, ..., sᵢ₋₁, sᵢ₊₁, ..., sₙ) (strategies of all players except i)
- (sᵢ, s₋ᵢ) = complete strategy profile with i playing sᵢ

**Payoff matrix** (2-player game):
- Rows: Player 1's strategies
- Columns: Player 2's strategies
- Cell (i,j): (u₁(sᵢ,sⱼ), u₂(sᵢ,sⱼ))

**Example: Matching Pennies**

|       | Heads | Tails |
|-------|-------|-------|
| **Heads** | 1, -1 | -1, 1 |
| **Tails** | -1, 1 | 1, -1 |

Player 1 wins if both show same side (1, -1). Player 2 wins if different (-1, 1). **Zero-sum**: Payoffs sum to zero in every cell.

## Best Response

**Definition**: Strategy sᵢ* is **best response** to s₋ᵢ if:

```
uᵢ(sᵢ*, s₋ᵢ) ≥ uᵢ(sᵢ, s₋ᵢ) for all sᵢ ∈ Sᵢ
```

Player i cannot do better than sᵢ* given opponents play s₋ᵢ.

**Best response correspondence**: BRᵢ(s₋ᵢ) = {sᵢ ∈ Sᵢ : sᵢ is best response to s₋ᵢ}
- May be single strategy (unique best response)
- May be multiple strategies (indifference)
- May be all strategies if payoffs independent of others' choices

**Example: Cournot Duopoly**

Two firms choose quantities q₁, q₂ simultaneously. Price: P(Q) = a - Q where Q = q₁ + q₂.
Firm i's profit: πᵢ = qᵢ(a - q₁ - q₂) - cqᵢ

Firm 1's best response to q₂:
```
max q₁(a - q₁ - q₂ - c)
q₁

FOC: a - 2q₁ - q₂ - c = 0
BR₁(q₂) = (a - c - q₂)/2
```

Symmetrically: BR₂(q₁) = (a - c - q₁)/2

**Graphically**: Best response functions are lines in (q₁, q₂) space. Intersection = Nash equilibrium.

## Nash Equilibrium

**Definition** (John Nash, 1950): Strategy profile s* = (s₁*, ..., sₙ*) is **Nash equilibrium** if each player's strategy is best response to others':

```
sᵢ* ∈ BRᵢ(s₋ᵢ*) for all i ∈ N
```

Equivalently: No player can profitably deviate unilaterally.

```
uᵢ(sᵢ*, s₋ᵢ*) ≥ uᵢ(sᵢ, s₋ᵢ*) for all sᵢ ∈ Sᵢ, for all i
```

**Interpretation**:
- Self-enforcing: No player regrets choice given others' choices
- Stable: No incentive for unilateral deviation
- Fixed point: Profile of mutual best responses

**Not claimed**:
- Pareto efficiency (can have inefficient equilibria)
- Uniqueness (can have multiple equilibria)
- Players will find it (might require learning/coordination)

**Example: Prisoner's Dilemma**

|               | Cooperate | Defect |
|---------------|-----------|--------|
| **Cooperate** | 3, 3      | 0, 5   |
| **Defect**    | 5, 0      | 1, 1   |

**Analysis**:
- BR₁(Cooperate) = Defect (5 > 3)
- BR₁(Defect) = Defect (1 > 0)
- Defect dominates Cooperate for Player 1
- By symmetry, Defect dominates for Player 2
- **Nash equilibrium**: (Defect, Defect) with payoffs (1, 1)
- (Cooperate, Cooperate) gives (3, 3) but not equilibrium (each wants to deviate to Defect)

**Cournot duopoly solution**:

Nash equilibrium where best responses intersect:
```
q₁* = (a - c - q₂*)/2
q₂* = (a - c - q₁*)/2

Solving: q₁* = q₂* = (a - c)/3
```

Total output: Q* = 2(a - c)/3
Price: P* = a - 2(a - c)/3 = (a + 2c)/3
Profit per firm: πᵢ* = [(a - c)/3]²

**Comparison**:
- Monopoly output: (a - c)/2 (lower)
- Competitive output: a - c (higher)
- Cournot: Between monopoly and competition

## Dominant Strategies

**Definition**: Strategy sᵢ **dominates** sᵢ' if:

```
uᵢ(sᵢ, s₋ᵢ) > uᵢ(sᵢ', s₋ᵢ) for all s₋ᵢ
```

Strategy sᵢ better than sᵢ' regardless of opponents' play.

**Strictly dominant**: Strictly better against all s₋ᵢ

**Weakly dominant**: At least as good against all s₋ᵢ, strictly better against some

**Dominated strategy**: Never best response to any s₋ᵢ (rational player never plays)

**Dominant strategy equilibrium**: Profile where each player plays dominant strategy
- Strongest solution concept (no coordination needed)
- Rare (most games lack dominant strategies)

**Example: Dominant strategy**

|               | L    | C    | R    |
|---------------|------|------|------|
| **U**         | 3, 2 | 4, 3 | 2, 1 |
| **M**         | 5, 1 | 6, 5 | 4, 2 |
| **D**         | 1, 4 | 2, 3 | 0, 2 |

Player 1: M dominates U (5>3, 6>4, 4>2), M dominates D (5>1, 6>2, 4>0) → M strictly dominant
Player 2: C weakly dominates L (3>2, 5≥1, 3<4), C dominates R (3>1, 5>2, 3>2) → C dominant
**Equilibrium**: (M, C) with payoffs (6, 5)

## Iterated Elimination of Dominated Strategies (IEDS)

**Procedure**:
1. Identify dominated strategies (never rational)
2. Eliminate them
3. Repeat on reduced game
4. Stop when no dominated strategies remain

**Order independence**: Final result same regardless of elimination order (for strictly dominated strategies)

**Rationality interpretation**:
- Round 1: I don't play dominated strategies (I'm rational)
- Round 2: Opponents don't play dominated strategies (they're rational)
- Round 3: I know opponents are rational, they know I'm rational
- Continues: Common knowledge of rationality

**Example: IEDS**

|               | L    | C    | R    |
|---------------|------|------|------|
| **U**         | 3, 0 | 1, 2 | 0, 1 |
| **M**         | 0, 3 | 2, 2 | 3, 0 |
| **D**         | 1, 0 | 0, 1 | 2, 2 |

**Round 1**: No dominated strategies
**Observation**: If Player 2 believes Player 1 might play U with high probability, Player 2 prefers C. But U doesn't dominate anything.

Actually, examining carefully:
- For Player 1: No dominated strategies (each strategy best against some Player 2 strategy)
- For Player 2: No dominated strategies

This game requires Nash equilibrium analysis (IEDS doesn't solve it).

**Better example**: Guessing game

10 players simultaneously guess integer 0-100. Winner: Closest to 2/3 of average.

**Round 1**: Any guess >67 dominated (if average ≤100, then 2/3·average ≤67)
**Round 2**: Any guess >45 dominated (if all guess ≤67, average ≤67, then 2/3·67 ≈45)
**Round 3**: Any guess >30 dominated
**Continues**: Converges to 0

**Nash equilibrium**: All guess 0 (only fixed point: 2/3·0 = 0)

**Experiments**: Most people guess 20-40 (2-3 rounds of reasoning). Some guess 0 (infinite rounds). Average ~25.

## Classic 2×2 Games

### Prisoner's Dilemma

|               | Cooperate | Defect |
|---------------|-----------|--------|
| **Cooperate** | 3, 3      | 0, 5   |
| **Defect**    | 5, 0      | 1, 1   |

**Structure**: T > R > P > S (Temptation > Reward > Punishment > Sucker)
- T = 5 (tempt to defect when opponent cooperates)
- R = 3 (reward for mutual cooperation)
- P = 1 (punishment for mutual defection)
- S = 0 (sucker payoff for cooperating when opponent defects)

**Equilibrium**: (Defect, Defect) = (1, 1)
**Pareto-efficient**: (Cooperate, Cooperate) = (3, 3) but unstable

**Real-world examples**:
- Arms races: Nations better off with arms control but individual incentive to arm
- Cartels: Firms better off with collusion but individual incentive to cheat
- Public goods: Everyone better off contributing but individual incentive to free-ride
- Climate change: Countries better off reducing emissions collectively but individual incentive to pollute
- Doping in sports: Clean sport preferable but individual incentive to dope

**Escape mechanisms**:
- Repetition (next section)
- Contracts (enforceable agreements)
- Altruism (change payoffs)
- Monitoring (detect defection)

### Coordination Game (Battle of the Sexes)

|               | Opera | Football |
|---------------|-------|----------|
| **Opera**     | 2, 1  | 0, 0     |
| **Football**  | 0, 0  | 1, 2     |

Both prefer coordinating to miscoordinating, but disagree on which option.

**Nash equilibria**: (Opera, Opera) and (Football, Football)
**Problem**: Multiple equilibria → coordination problem (which equilibrium?)

**Real-world**:
- Technology standards (VHS vs Betamax, Blu-ray vs HD-DVD)
- Driving side of road (left vs right)
- Language choice (which language in bilingual setting)
- Meeting point (where to meet without communication)

**Solutions**:
- Focal points (Schelling): Salient options (e.g., obvious meeting place)
- Conventions (social norms)
- Communication (pre-play)
- Correlation device (randomize between equilibria)

### Chicken (Hawk-Dove)

Two drivers race toward each other. Payoffs based on who swerves ("chicken") first.

|               | Swerve  | Straight |
|---------------|---------|----------|
| **Swerve**    | 0, 0    | -1, 1    |
| **Straight**  | 1, -1   | -10, -10 |

**Equilibria**: (Swerve, Straight) and (Straight, Swerve)
**Key**: Prefer being "tough" if opponent is "weak," but mutual toughness disastrous

**Real-world**:
- Cuban Missile Crisis: US and USSR brinkmanship (both backing down > war, but unilateral backing down costly)
- Labor disputes: Strike vs cave (both better off with settlement, but prefer opponent caves)
- Trade wars: Tariffs (both backing down > trade war, but unilateral backing down costly)

**Commitment value**: Player who credibly commits to Straight (e.g., throw steering wheel out window) forces opponent to Swerve. Removing options increases payoff.

### Stag Hunt

Two hunters: Hunt stag (requires cooperation) or hare (can hunt alone)

|               | Stag   | Hare   |
|---------------|--------|--------|
| **Stag**      | 4, 4   | 0, 3   |
| **Hare**      | 3, 0   | 3, 3   |

**Equilibria**: (Stag, Stag) = (4, 4) and (Hare, Hare) = (3, 3)
**Key**: (Stag, Stag) Pareto-dominates (Hare, Hare), but riskier (if partner defects to Hare, you get 0)

**Structure**: Cooperation is equilibrium but requires trust/coordination

**Real-world**:
- Technology adoption: New tech better if everyone adopts, but risky if you adopt alone
- Revolution: Uprising succeeds if everyone participates, fails if you participate alone
- Innovation: R&D collaboration more productive but risky if partner doesn't contribute

**Risk dominance**: (Hare, Hare) safer (eliminates risk of getting 0). Players with high risk aversion prefer Hare. (Stag, Stag) Pareto-dominates but requires confidence opponent will cooperate.

## Mixed Strategies

**Pure strategy**: Deterministic choice (always play same action)

**Mixed strategy**: Probability distribution over pure strategies

**Notation**: σᵢ ∈ Δ(Sᵢ) where Δ(Sᵢ) is set of probability distributions over Sᵢ

For finite Sᵢ = {s¹ᵢ, ..., sᴷᵢ}, mixed strategy σᵢ = (p₁, ..., pₖ) where:
- pₖ ≥ 0 for all k
- Σpₖ = 1
- pₖ = probability of playing sᵏᵢ

**Expected payoff**:
```
uᵢ(σ₁, ..., σₙ) = Σ ... Σ [σ₁(s₁) · ... · σₙ(sₙ) · uᵢ(s₁, ..., sₙ)]
```

Sum over all pure strategy profiles, weighted by probability.

**Mixed strategy Nash equilibrium**: Profile σ* where each player's mixed strategy is best response to others' mixed strategies.

**Example: Matching Pennies**

|       | Heads | Tails |
|-------|-------|-------|
| **Heads** | 1, -1 | -1, 1 |
| **Tails** | -1, 1 | 1, -1 |

No pure strategy Nash equilibrium (always incentive to deviate).

**Mixed strategy equilibrium**:

Let Player 1 play Heads with probability p, Tails with probability 1-p.
Let Player 2 play Heads with probability q, Tails with probability 1-q.

Player 1's expected payoff:
- Play Heads: q(1) + (1-q)(-1) = 2q - 1
- Play Tails: q(-1) + (1-q)(1) = 1 - 2q

For Player 1 to randomize, must be indifferent:
```
2q - 1 = 1 - 2q
4q = 2
q = 1/2
```

By symmetry, p = 1/2.

**Nash equilibrium**: Both play (1/2, 1/2) → both randomize 50-50.
**Expected payoffs**: (0, 0) (fair game)

### Why Randomize?

**Intuition**: Keep opponent guessing. If predictable, opponent exploits.

**Example: Penalty kicks**

Kicker chooses Left or Right. Goalie chooses Left or Right.
If both choose same side, goalie saves (kicker gets 0). If different, kicker scores (kicker gets 1).

|               | Goalie Left | Goalie Right |
|---------------|-------------|--------------|
| **Kick Left** | 0, 1        | 1, 0         |
| **Kick Right**| 1, 0        | 0, 1         |

**Mixed equilibrium**: Kicker and goalie both randomize 50-50.

**Data** (Chiappori, Levitt, Groseclose 2002): Professional penalty kicks approximately match mixed equilibrium predictions.

### Existence of Nash Equilibrium

**Nash's Theorem** (1950): Every finite game (finite players, finite strategies) has at least one Nash equilibrium (possibly in mixed strategies).

**Proof sketch**:
1. Define best response correspondence BRᵢ: Sₐₗₗ → Sₐₗₗ mapping strategy profiles to best responses
2. Nash equilibrium = fixed point of BR (profile where each strategy is best response to itself)
3. Kakutani's fixed point theorem: BR has fixed point under continuity/convexity conditions
4. Mixed strategies provide necessary convexity

**Implication**: Always have solution concept to apply (though may be in mixed strategies, which are more complex to find and interpret).

**Caution**: Existence doesn't imply:
- Uniqueness (many games have multiple equilibria)
- Easy to find (computing equilibria can be computationally hard—PPAD-complete)
- Players will reach equilibrium (may require learning, coordination)

## Pareto Efficiency

**Definition**: Outcome is **Pareto efficient** if no other outcome makes someone better off without making anyone worse off.

**Equivalently**: No outcome Pareto-dominates it.

**Pareto dominance**: Outcome x Pareto-dominates y if:
- uᵢ(x) ≥ uᵢ(y) for all i (weakly better for everyone)
- uⱼ(x) > uⱼ(y) for some j (strictly better for someone)

**Nash equilibrium vs Pareto efficiency**: Independent concepts

**Prisoner's Dilemma**:
- Nash equilibrium: (Defect, Defect) = (1, 1)
- Pareto-efficient: (Cooperate, Cooperate) = (3, 3)
- Equilibrium is Pareto-inefficient (both prefer (3,3) to (1,1))

**Coordination game**:
- Nash equilibria: (Opera, Opera) = (2, 1) and (Football, Football) = (1, 2)
- Both are Pareto-efficient (no outcome makes both better off)
- But (0, 0) is Pareto-inefficient (both equilibria Pareto-dominate it)

**Policy implication**: Markets may reach Nash equilibria that are socially inefficient. Institutions, regulations, or mechanisms needed to achieve efficient outcomes.

## Multiple Equilibria

**Problem**: Many games have multiple Nash equilibria. Which will occur?

**Example: Coordination**

|               | A     | B     |
|---------------|-------|-------|
| **A**         | 2, 2  | 0, 0  |
| **B**         | 0, 0  | 1, 1  |

**Nash equilibria**: (A, A) = (2, 2) and (B, B) = (1, 1)

**Selection criteria**:

**1. Pareto dominance**: (A, A) Pareto-dominates (B, B) → prefer (A, A)

**2. Risk dominance** (Harsanyi & Selten):
- Calculate "risk" of each equilibrium
- (A, A): If opponent plays A with prob p, my payoff from A is 2p, from B is 0. Indifferent when 2p = 0 → p = 0. So I need only slight belief (p > 0) that opponent plays A to prefer A.
- Actually, let me recalculate: If opponent plays A with prob p, my expected payoff from A is 2p + 0(1-p) = 2p. My expected payoff from B is 0p + 1(1-p) = 1-p. I prefer A if 2p > 1-p, i.e., 3p > 1, i.e., p > 1/3.
- For (B, B): If opponent plays B with prob q, my payoff from B is 1q, from A is 0. I prefer B if q > 0. Actually: Expected payoff from B is 1q + 0(1-q) = q. Expected payoff from A is 2(1-q). I prefer B if q > 2(1-q), i.e., 3q > 2, i.e., q > 2/3.
- (A, A) requires p > 1/3 (lower threshold) → less risky → risk-dominant

**3. Focal points** (Schelling): Salient features suggest equilibrium
- Drive on right in US (convention)
- Meet at Grand Central Station (famous landmark)
- Split 50-50 in bargaining (fairness norm)

**4. Forward induction**: Actions reveal information about intentions (covered later)

**5. Learning/evolution**: Equilibrium reached through dynamic process (covered later)

## Computing Nash Equilibria

### 2×2 Games

**Method**: Check all four pure strategy profiles, then check mixed strategy equilibrium.

**Pure strategy**: Profile is Nash equilibrium if no profitable deviation for either player.

**Mixed strategy** (if no pure equilibrium):
1. Find probabilities making opponent indifferent between pure strategies
2. Check that these probabilities are interior (between 0 and 1)
3. Verify mutual best responses

**Example: Hawk-Dove**

|               | Hawk   | Dove   |
|---------------|--------|--------|
| **Hawk**      | -1, -1 | 2, 0   |
| **Dove**      | 0, 2   | 1, 1   |

**Pure equilibria**: (Hawk, Dove) = (2, 0) and (Dove, Hawk) = (0, 2)

**Mixed equilibrium**: Player 1 plays Hawk with prob p, Player 2 plays Hawk with prob q.

Player 1's expected payoffs:
- Hawk: q(-1) + (1-q)(2) = 2 - 3q
- Dove: q(0) + (1-q)(1) = 1 - q

Indifferent when 2 - 3q = 1 - q → q = 1/2

By symmetry, p = 1/2.

**Mixed Nash**: Both play (1/2 Hawk, 1/2 Dove)
**Expected payoffs**: Each gets 1/2(-1) + 1/2(0) + 1/4(2) + 1/4(1) = -1/2 + 0 + 1/2 + 1/4 = 1/4

Wait, let me recalculate. If both play (1/2, 1/2):
- Prob(H, H) = 1/4 → payoff (-1, -1)
- Prob(H, D) = 1/4 → payoff (2, 0)
- Prob(D, H) = 1/4 → payoff (0, 2)
- Prob(D, D) = 1/4 → payoff (1, 1)

Player 1's expected payoff: (1/4)(-1) + (1/4)(2) + (1/4)(0) + (1/4)(1) = -1/4 + 1/2 + 0 + 1/4 = 1/2

So expected payoff is (1/2, 1/2).

### Larger Games

**Methods**:
- Support enumeration: Guess which strategies played with positive probability, solve system of indifference equations
- Linear complementarity problems (LCP)
- Lemke-Howson algorithm (2-player games)
- Simplicial subdivision (general case)

**Complexity**: Computing Nash equilibrium is PPAD-complete (Chen & Deng 2006). Not known to be NP-hard, but likely intractable for large games.

## Applications

### Cournot vs Bertrand

**Cournot** (quantity competition):
- Firms choose quantities simultaneously
- Price adjusts to clear market
- **Equilibrium**: Positive profits (between monopoly and perfect competition)

**Bertrand** (price competition):
- Firms choose prices simultaneously
- Consumers buy from lowest-priced firm
- **Equilibrium** (with identical products, zero marginal cost): Both charge marginal cost, zero profit (perfect competition outcome)

**Paradox**: Two firms sufficient for competitive outcome in Bertrand. Reality between extremes (product differentiation, capacity constraints, dynamic considerations).

### Oligopoly with n Firms (Cournot)

Demand: P(Q) = a - Q where Q = Σqᵢ
Firm i's profit: πᵢ = qᵢ(a - Q - c)

**Best response**:
```
∂πᵢ/∂qᵢ = a - 2qᵢ - Q₋ᵢ - c = 0
qᵢ = (a - c - Q₋ᵢ)/2
```

**Symmetric Nash equilibrium**: All firms produce same quantity q*.
```
Q₋ᵢ = (n-1)q*
q* = (a - c - (n-1)q*)/2
2q* = a - c - (n-1)q*
(n+1)q* = a - c
q* = (a - c)/(n + 1)
```

**Total output**: Q* = nq* = n(a - c)/(n + 1)

**Price**: P* = a - Q* = a - n(a - c)/(n + 1) = [a(n+1) - n(a - c)]/(n + 1) = (a + nc)/(n + 1)

**Limits**:
- n = 1 (monopoly): q* = (a - c)/2, P* = (a + c)/2
- n = 2 (duopoly): q* = (a - c)/3, P* = (a + 2c)/3
- n → ∞: q* → 0, Q* → a - c, P* → c (perfect competition)

**Implication**: As number of firms increases, oligopoly converges to competitive outcome.

### Public Goods Game (n-player Prisoner's Dilemma)

n players simultaneously decide contribution gᵢ ∈ [0, w] where w = endowment.

Total contribution: G = Σgᵢ

Payoff to player i:
```
uᵢ = w - gᵢ + α·G
```
- w - gᵢ: Endowment minus contribution (private benefit of keeping money)
- α·G: Benefit from public good (everyone benefits from total contributions)

Assume α < 1 (private return > public return per dollar) but nα > 1 (social return > private return).

**Best response**:
- If α < 1: ∂uᵢ/∂gᵢ = -1 + α < 0 → contribute 0 (free ride)
- Regardless of others' contributions, prefer gᵢ = 0

**Nash equilibrium**: gᵢ* = 0 for all i → G* = 0
**Efficient outcome**: gᵢ = w for all i → G = nw (if nα > 1, total benefit nα·nw > cost nw)

**Result**: Individual rationality → zero contribution. Social optimum requires cooperation mechanism.

**Experiments**: People contribute 40-60% on average initially, declining over rounds. Strong heterogeneity (some always cooperate, some always free-ride, some conditional cooperators).

### Voting (Strategic Voting)

**Setup**: 3 candidates (L, C, R), 3 voters with preferences:
- Voter 1: C > L > R
- Voter 2: C > L > R
- Voter 3: R > C > L

Plurality rule: Candidate with most votes wins.

**Sincere voting**: Each votes for top choice → C(2), R(1) → C wins

**Strategic voting**: Suppose poll shows R leading.
- Voter 1 & 2: Voting for C might waste vote (C likely third). Strategic vote for L (second choice) prevents worst outcome (R).
- If 1 & 2 vote L → L(2), C(0), R(1) → L wins
- Voter 3: Would prefer to vote R (sincere), but if knows 1 & 2 voting strategically for L, might vote C (second choice) to prevent L (worst for 3)

**Equilibrium depends on beliefs** about others' voting, which depend on polls, which depend on anticipated voting. Complex strategic interdependence.

**Duverger's Law**: Plurality rule tends toward two-party systems (voters abandon third parties to avoid "wasting" votes).

## Key Terms

- **Strategic form**: Representation of game by players, strategy sets, payoff functions
- **Strategy profile**: Specification of strategy for each player
- **Best response**: Strategy maximizing payoff given others' strategies
- **Nash equilibrium**: Profile of mutual best responses
- **Dominant strategy**: Best regardless of opponents' strategies
- **Dominated strategy**: Never a best response (rational player never plays)
- **Iterated elimination of dominated strategies (IEDS)**: Successively remove dominated strategies
- **Mixed strategy**: Probability distribution over pure strategies
- **Pure strategy**: Deterministic choice (special case of mixed strategy)
- **Pareto efficiency**: No outcome makes someone better off without hurting anyone
- **Risk dominance**: Equilibrium requiring weaker beliefs about opponents' play
- **Focal point**: Salient outcome coordinating players' expectations

## Summary

Normal form (strategic form) games represent simultaneous-move strategic interactions via payoff matrices. Nash equilibrium—mutual best responses—is central solution concept: no player regrets choice given others' choices. Dominant strategies (best regardless of opponents) guarantee unique equilibrium in dominant strategy equilibrium games (rare but powerful). Iterated elimination of dominated strategies (IEDS) refines strategy sets under common knowledge of rationality.

Classic 2×2 games illustrate key strategic structures: Prisoner's Dilemma (individual rationality → collective irrationality), Coordination (multiple equilibria, focal points matter), Chicken (commitment value), Stag Hunt (cooperation as equilibrium but risky). Mixed strategies—randomization over pure strategies—extend equilibrium concept (Nash's theorem: every finite game has equilibrium, possibly mixed). Players randomize to keep opponents indifferent, preventing exploitation.

Nash equilibrium ≠ Pareto efficiency: Prisoner's Dilemma equilibrium is inefficient (both prefer mutual cooperation). Multiple equilibria create selection problem (Pareto dominance, risk dominance, focal points guide). Applications: Cournot oligopoly (quantities), Bertrand oligopoly (prices), public goods (free-riding), strategic voting (insincere preferences).

Computing Nash equilibria: Check pure strategy profiles (mutual best responses), then solve for mixed strategies (indifference conditions). Larger games computationally hard (PPAD-complete). Nash equilibrium provides benchmark for strategic analysis, though real behavior may deviate due to bounded rationality, learning dynamics, or other-regarding preferences (covered in later chapters).

