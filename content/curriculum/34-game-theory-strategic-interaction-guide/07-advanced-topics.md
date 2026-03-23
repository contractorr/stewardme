# Advanced Topics & Extensions

## Equilibrium Refinements

**Problem**: Many games have multiple Nash equilibria or equilibria relying on incredible threats. Refinements select "reasonable" equilibria.

### Trembling-Hand Perfect Equilibrium (Selten, 1975)

**Idea**: Players occasionally tremble (make mistakes with small probability)

**Definition**: Nash equilibrium that is limit of equilibria in perturbed games where players tremble

**Effect**: Eliminates equilibria relying on incredible threats (opponent must consider possibility of off-path actions due to trembles)

**Example**: Entry game with threatened Fight
- Nash: (Stay Out, Fight)
- Not trembling-hand perfect: If trembling means Entrant might Enter, Incumbent must plan response → prefers Accommodate → threat not credible

**Application**: Rules out weakly dominated strategies in equilibrium

### Sequential Equilibrium (Kreps-Wilson, 1982)

**For extensive-form games**: Refines Perfect Bayesian Equilibrium

**Requirements**:
1. **Sequential rationality**: At every information set, strategy optimal given beliefs
2. **Consistent beliefs**: Beliefs derived from Bayes' rule whenever possible (on-path), consistent with equilibrium strategies

**Stronger than subgame perfection** (applies to games with imperfect information)

**Application**: Signaling games, repeated games with incomplete info

### Forward Induction

**Logic**: Rational player wouldn't take action A unless planning action B later

**Example**: Burning money
- Two firms: Incumbent can burn $1M before Entrant decides
- If Incumbent burns money, signals desperation or irrationality → Entrant infers Incumbent will fight
- Forward induction: "Why would Incumbent burn money unless planning to fight?"

**Refines equilibria**: Eliminates equilibria inconsistent with forward-induction reasoning

**Controversial**: Requires strong assumptions about common knowledge of rationality

## Behavioral Game Theory

**Observations**: Systematic deviations from Nash predictions in experiments

### Bounded Rationality

**Level-k reasoning** (Stahl-Wilson, 1994; Nagel, 1995):
- L0: Random play
- L1: Best responds to L0
- L2: Best responds to L1
- Lk: Best responds to Lk-1

**Guessing game** (2/3 of average):
- Nash: Everyone guesses 0
- Observed: Modal guess around 22-33 (L1-L2 reasoning)
- Distribution fits mixture of L0-L3 types

**Quantal response equilibrium** (McKelvey-Palfrey, 1995):
- Players best-respond noisily (higher-payoff actions more likely, but not deterministic)
- Equilibrium: Consistent with noisy best-response assumption

**Applications**: Explains overbidding in auctions, non-Nash play in coordination games

### Social Preferences

**Standard model**: Players maximize own payoff

**Evidence**: Players care about fairness, reciprocity, others' payoffs

**Ultimatum Game**: Offers of 40-50% (not 0), rejection of low offers

**Models**:

**Inequality aversion** (Fehr-Schmidt, 1999; Bolton-Ockenfels, 2000):
```
Uᵢ = xᵢ - α·(1/n)Σ max(xⱼ - xᵢ, 0) - β·(1/n)Σ max(xᵢ - xⱼ, 0)
```
- α > β: Dislike disadvantageous inequality more than advantageous
- Explains rejection of unfair offers (prefer (0,0) to (2,8))

**Reciprocity** (Rabin, 1993; Dufwenberg-Kirchsteiger, 2004):
- Reward kind actions, punish unkind actions
- Intention matters (not just outcome)

**Trust and trustworthiness**: Trust game experiments show ~50% return (despite dominant strategy to keep)

### Learning in Games

**Fictitious play**: Update beliefs about opponents' strategies based on observed frequencies, best-respond to beliefs

**Converges to Nash** in some games (2x2 games with unique mixed equilibrium, zero-sum games), not others

**Reinforcement learning**: Repeat actions with higher payoffs more frequently (Bush-Mosteller, Erev-Roth)

**Evolutionary dynamics**: Strategies with higher payoffs grow (replicator dynamics)

**Applications**: Explains convergence to equilibria in repeated play, coordination on focal points

## Evolutionary Game Theory

**Replicator dynamics**: Strategies replicate proportionally to fitness (payoffs)

**Equation**:
```
dx_i/dt = xᵢ[u(sᵢ, x) - u(x, x)]
```
- xᵢ = frequency of strategy sᵢ
- u(sᵢ, x) = fitness of sᵢ in population x
- u(x, x) = average fitness

**Strategy grows if above-average fitness**

**ESS = stable rest point** of replicator dynamics

**Hawk-Dove example**:
- Mixed ESS p* = V/C
- Replicator dynamics converge to p*
- If p < p*, Hawks have above-average fitness → p increases
- If p > p*, Doves have above-average fitness → p decreases

**Advantages over Nash**:
- No rationality required (just differential reproduction)
- Explains dynamics (how equilibrium reached)
- Applicable to biology, cultural evolution, learning

**Applications**:
- Evolution of cooperation (prisoner's dilemma in populations)
- Sex ratios (Fisher's principle)
- Biological arms races (predator-prey coevolution)

## Correlated Equilibrium (Aumann, 1974)

**Idea**: Players receive correlated signals, condition strategies on signals

**Setup**:
- Mediator draws state ω according to distribution p(ω)
- Sends private recommendation aᵢ(ω) to each player i
- Players follow recommendations if incentive-compatible

**Example**: Traffic light
- Red: Stop
- Green: Go
- Coordinates drivers (both stop or both go)
- Pareto-dominates independent randomization

**Chicken game**:
|               | Swerve | Straight |
|---------------|--------|----------|
| **Swerve**    | 0, 0   | -1, 1    |
| **Straight**  | 1, -1  | -10, -10 |

**Nash**: (Swerve, Straight) and (Straight, Swerve), each probability 1/2 → expected payoff (0, 0)

**Correlated equilibrium**: Mediator flips coin
- Heads: Recommend (Swerve, Straight)
- Tails: Recommend (Straight, Swerve)
- Each player gets payoff 0 (same as Nash) but avoids (-10,-10) entirely

**Can strictly Pareto-dominate Nash equilibria**: Correlation can improve welfare

**Interpretation**: Social norms, public signals, conventions

## Algorithmic Game Theory

**Complexity of computing Nash equilibria**:
- **PPAD-complete** (Chen-Deng, 2006): Not known to be NP-hard, but likely intractable
- Contrast with LP (polynomial), SAT (NP-complete)

**Price of Anarchy** (PoA): Ratio of social welfare at worst Nash equilibrium to social optimum

**Example**: Selfish routing (Pigou's example)
- Two routes: Fast (congestion-sensitive), Slow (constant time)
- Nash: All drivers use Fast → congestion
- Optimum: Split traffic → lower average delay
- PoA measures efficiency loss from selfish behavior

**Mechanism design for computationally bounded agents**:
- VCG computationally expensive (NP-hard in combinatorial auctions)
- Approximate mechanisms trade off incentive compatibility for computational efficiency

**Applications**:
- Internet routing (BGP strategic behavior)
- Cloud computing resource allocation
- Sponsored search auctions (Google, Bing)

## Common Knowledge

**Definition**: Event E is common knowledge if:
- Everyone knows E
- Everyone knows everyone knows E
- Everyone knows everyone knows everyone knows E
- Ad infinitum

**Notation**: K(E) = "Everyone knows E"
- Common knowledge: K(E), K(K(E)), K(K(K(E))), ...

**Electronic mail game** (Rubinstein, 1989):
- Two generals coordinate attack (both attack → win; one attacks → lose)
- Communication via unreliable email (with acknowledgments)
- No matter how many acknowledgments, common knowledge not achieved
- Backward induction → never attack

**Importance**:
- Backward induction requires common knowledge of rationality
- Coordination requires common knowledge of focal point
- Public announcements create common knowledge

**Agreeing to disagree** (Aumann, 1976): If rational agents share prior and posteriors are common knowledge, posteriors must be identical. "Agree to disagree" impossible if rational and posteriors common knowledge.

**Applications**: Market microstructure (no-trade theorems), communication protocols, coordination

## Repeated Games with Imperfect Monitoring

**Setup**: Players don't observe actions directly, only noisy signals

**Example**: Duopoly with demand shocks
- Firms choose prices
- Sales depend on prices + random demand shock
- Low sales could be: opponent cheated (undercut price) or bad demand
- Cannot distinguish perfectly

**Challenge**: Distinguish intentional deviation from bad luck

**Green-Porter model** (1984):
- **Trigger strategy**: Cooperate (high price) unless sales below threshold → price war for T periods
- Occasional price wars even on equilibrium path (bad demand triggers punishment)
- Imperfect monitoring makes cooperation harder to sustain (requires harsher punishments)

**Folk theorem with imperfect monitoring** (Fudenberg-Levine-Maskin, 1994):
- Cooperative outcomes sustainable if signals sufficiently informative
- Requires more patience (higher δ) than perfect monitoring

**Applications**:
- Cartels (detect cheating via market shares, prices)
- Employment (monitor worker effort imperfectly)
- International agreements (monitor compliance via imperfect signals)

## Global Games

**Technique**: Introduce small incomplete information to select unique equilibrium

**Example**: Coordination game with multiple equilibria + small private info about payoffs
- Without incomplete info: Multiple equilibria (coordination problem)
- With private signals about payoffs: Unique equilibrium selected (iterated deletion of dominated strategies)

**Currency attacks** (Morris-Shin, 1998):
- Multiple investors decide whether to attack currency
- Attack succeeds if enough investors attack
- Private signals about fundamentals → unique threshold equilibrium
- Explains sudden currency crises

**Bank runs**: Private signals about bank solvency → unique equilibrium (avoids multiplicity of Diamond-Dybvig model)

**Applications**: Coordination failures, regime change (revolutions), technology adoption

## Auction Design in Practice

**FCC spectrum auctions** (1994-):
- Simultaneous ascending auction (multiple licenses auctioned simultaneously)
- Allows bidders to assemble packages (complementarities)
- Activity rules prevent late bidding
- Revenue: $100+ billion total

**Google/Facebook ad auctions**:
- Generalized second-price (GSP): Each advertiser pays next-highest bid
- Not exactly incentive-compatible (truthful bidding not dominant strategy)
- But approximately truthful + computationally simple
- Billions of daily auctions

**Electricity markets**:
- Suppliers bid supply curves, demand aggregated, market clears
- Strategic behavior: Withholding capacity to raise price
- Market power mitigation: Price caps, demand response

**Kidney exchange**:
- Patients with willing incompatible donors
- Cycles of exchanges (2-way, 3-way, chains)
- Challenge: Incentive compatibility (misreport preferences to get better match)
- NRMP: ~1,000 transplants/year via exchange

## Experimental Methods

**Lab experiments**:
- Control environment, test theory
- Subject pools: Students, online (MTurk)
- Typical payment: $10-30 for 1-hour session

**Field experiments**:
- Natural setting (firms, schools, markets)
- Higher external validity
- Less control

**Key findings**:
- **Ultimatum**: 40-50% offers, low offers rejected
- **Public goods**: 40-60% contribute initially, decay over rounds
- **Trust game**: ~50% return despite dominant strategy to keep
- **Beauty contest** (guess 2/3 of average): Modal guess 20-40 (L1-L2), not 0 (Nash)

**Criticisms**:
- Student subjects (WEIRD: Western, Educated, Industrialized, Rich, Democratic)
- Stakes too low (would behavior differ with $10k, $1M?)
- Context-free (framing matters in real world)

**Responses**:
- High-stakes replication (TV game shows): Similar results
- Cross-cultural studies (Henrich et al.): Qualitative patterns robust
- Field experiments: Behavior similar in markets (some differences)

## Open Problems

1. **Equilibrium selection**: Multiple equilibria—which occurs? Focal points, learning, evolutionary dynamics partial answers.

2. **Bounded rationality**: How to model limits on computation, attention, memory? Level-k, QRE are start but incomplete.

3. **Non-equilibrium dynamics**: Most real interactions out of equilibrium (learning, adaptation). How do populations reach equilibrium (if ever)?

4. **Robust mechanism design**: Design mechanisms robust to misspecification (false common prior, incorrect beliefs about rationality)

5. **Large games**: Computational challenges with many players. Approximation algorithms, mean-field games.

6. **Networks**: Strategic interaction on networks (contagion, diffusion, peer effects). Graph structure matters.

## Key Terms

- **Trembling-hand perfect**: Equilibrium surviving small probability of mistakes
- **Sequential equilibrium**: Sequential rationality + consistent beliefs (Kreps-Wilson)
- **Forward induction**: Infer opponent's plans from past actions
- **Level-k reasoning**: Players best-respond to Lk-1 types (bounded rationality)
- **Quantal response equilibrium (QRE)**: Noisy best-response, higher-payoff actions more likely
- **Inequality aversion**: Disutility from payoff differences
- **Fictitious play**: Update beliefs from observed play, best-respond
- **Replicator dynamics**: Strategies grow proportionally to fitness
- **Correlated equilibrium**: Players condition on correlated signals (Aumann)
- **PPAD-complete**: Complexity class of Nash equilibrium computation
- **Price of Anarchy**: Efficiency loss from selfish behavior (worst Nash vs optimum)
- **Common knowledge**: Everyone knows, everyone knows everyone knows, ad infinitum
- **Global games**: Small incomplete info selects unique equilibrium

## Summary

Equilibrium refinements (trembling-hand perfect, sequential equilibrium, forward induction) eliminate unreasonable Nash equilibria relying on incredible threats or dominated strategies. Behavioral game theory incorporates bounded rationality (level-k, QRE) and social preferences (inequality aversion, reciprocity) explaining systematic deviations from Nash (Ultimatum offers 40-50%, low offers rejected). Learning dynamics (fictitious play, reinforcement learning) and evolutionary dynamics (replicator dynamics) explain how populations reach equilibria.

Correlated equilibrium (Aumann): Players condition on public signal → can Pareto-dominate Nash (traffic light coordinates drivers). Algorithmic game theory: Computing Nash is PPAD-complete (likely intractable). Price of Anarchy measures efficiency loss from selfish behavior. Mechanism design in practice: FCC spectrum auctions ($100B+ revenue), Google ad auctions (billions daily), kidney exchange (1,000+ transplants/year).

Common knowledge required for backward induction, coordination. Electronic mail game: Unreliable communication prevents common knowledge → coordination fails. Imperfect monitoring (Green-Porter): Firms observe noisy sales → occasional price wars even on-path (bad luck triggers punishment). Global games: Small incomplete info selects unique equilibrium in coordination games (currency attacks, bank runs).

Experiments show robust patterns: Ultimatum 40-50% offers, trust game ~50% return, public goods 40-60% contribute initially (decay), beauty contest modal 20-40 (L1-L2 not Nash 0). Open problems: Equilibrium selection, bounded rationality modeling, out-of-equilibrium dynamics, robust mechanism design, large games, networks. Game theory remains active research area with theoretical advances and practical applications expanding scope beyond traditional economics to computer science, biology, political science, and engineering.
