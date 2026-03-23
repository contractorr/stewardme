# Introduction to Game Theory

## What is Game Theory?

**Game theory**: Mathematical study of strategic interaction—situations where your optimal choice depends on what others choose, and they face the same interdependence.

**Core insight**: Optimization alone is insufficient when outcomes depend on multiple decision-makers. You must anticipate others' choices, knowing they're anticipating yours.

**Contrast**:
- **Decision theory**: Single agent optimizing against nature (stock picking, engineering design, medical treatment selection)
- **Game theory**: Multiple agents optimizing against each other (price competition, arms races, evolution, negotiations)

**Fundamental question**: "What should I do, given that others are asking the same question about me?"

## Why Game Theory Matters

### It's a Universal Analytical Framework

Game theory applies wherever incentives interact:

| Domain | Without Game Theory | With Game Theory |
|--------|---------------------|------------------|
| **Economics** | Firms maximize profit independently | Recognize strategic interdependence → oligopoly theory, auctions, mechanism design |
| **Politics** | Voters/politicians optimize individually | Strategic voting, agenda control, commitment problems, coalitions |
| **Biology** | Organisms maximize fitness | Evolutionary stability, cooperation, costly signaling, parent-offspring conflict |
| **Military** | Maximize force/territory | Deterrence, credibility, escalation dynamics, second-strike capability |
| **Negotiation** | Maximize own surplus | Bargaining power, outside options, commitment, reputation |
| **Law** | Deter crime by punishment severity | Strategic crime (detection probability matters), plea bargaining, litigation vs settlement |
| **Computer Science** | Optimize algorithms | Multi-agent systems, network routing, resource allocation, mechanism design |

### It Reveals Hidden Structure

**Example 1: Price competition (Bertrand)**

**Naive analysis**: Firms have market power → charge high prices → earn large profits

**Game-theoretic analysis**:
- Two firms, identical products, zero marginal cost
- If I charge $10 and competitor charges $10 → we split market
- If I undercut to $9.99 → I capture entire market
- But competitor anticipates this → also undercuts
- **Equilibrium**: Both charge marginal cost (zero), earn zero profit
- **Result**: Duopoly (2 firms) acts like perfect competition

**Implication**: Concentration alone doesn't guarantee market power. Strategic interaction can dissipate profits.

**Example 2: Nuclear deterrence**

**Naive analysis**: More weapons → more secure

**Game-theoretic analysis**:
- If I have first-strike capability (can destroy enemy's nukes) → enemy fears I'll strike → crisis instability
- If both have second-strike capability (survive first strike, retaliate) → mutual deterrence → stability
- **Paradox**: Vulnerability (assured destruction if you strike first) creates security
- **Policy**: Survivable weapons (submarines, mobile launchers) stabilize; counterforce weapons (silo-busters) destabilize

**Implication**: Security isn't about absolute capability but strategic configuration.

**Example 3: Evolution of cooperation**

**Naive analysis**: Selfish genes → universal selfishness

**Game-theoretic analysis**:
- One-shot interaction: Defection dominates
- Repeated interaction: Cooperation sustainable if future matters (discounting < critical threshold)
- Tit-for-tat: Cooperate initially, then mirror opponent → beats pure strategies in evolutionary tournaments
- **Result**: Cooperation emerges not from altruism but from strategic logic of repeated games

**Implication**: Morality and self-interest needn't conflict when interactions repeat.

### It Exposes Failures of Naïve Reasoning

**Voting paradoxes**:
- **Condorcet cycle**: Group preferences can be intransitive even if individual preferences are rational
  - A beats B, B beats C, C beats A → no "will of the people"
- **Strategic voting**: Voting sincerely can be dominated by strategic voting
  - 3 candidates: Left, Center, Right
  - Your preference: Center > Left > Right
  - Polls: Right winning
  - Sincere vote (Center) wastes vote; strategic vote (Left) prevents worst outcome

**Auction failures**:
- **Winner's curse**: In common-value auctions (oil field, company acquisition), winner likely overestimated value
  - If 10 bidders independently estimate value, winner is bidder with highest (most optimistic) estimate
  - Rational bidders should shade bids, but naïve bidders overpay
  - Explains why M&A acquirers often destroy shareholder value

**Coordination failures**:
- **Bank runs**: Each depositor rational to withdraw if others withdraw, even if bank solvent
  - If bank illiquid (long-term assets, short-term liabilities), can't satisfy all withdrawals
  - Your money safe only if others don't withdraw
  - Self-fulfilling prophecy: Fear of run causes run
  - **Solution**: Deposit insurance (game-changer—removes incentive to run)

### It Provides Precision in Complex Domains

**Mechanism design**: Design institutions/rules to achieve desired outcomes given strategic agents

**Example: Spectrum auctions**
- **Problem**: Allocate radio spectrum to telecom firms
- **Traditional approach**: Beauty contest (regulator decides) or lottery
  - Beauty contest: Lobbying, corruption, inefficient allocation
  - Lottery: Random assignment, no guarantee high-value users get spectrum
- **Game-theoretic approach**: Simultaneous ascending auction
  - Firms bid on packages of licenses
  - Designed to reveal valuations, prevent collusion
  - **Result**: US 1994-1995 auctions raised $20 billion, allocated to high-value users
  - Designed by game theorists (Paul Milgrom, Robert Wilson)

**Applications**:
- Kidney exchange (match donors to recipients, accounting for strategic reporting)
- School choice (match students to schools, prevent gaming)
- Ad auctions (Google/Facebook auctions: billions of daily auctions designed via game theory)

## Historical Development

### Pre-History (Before 1900)

**Antoine Cournot (1838)**: First formal game-theoretic model (duopoly—two firms choosing quantities)
- Each firm best-responds to competitor's quantity
- **Cournot equilibrium**: Both firms simultaneously optimize
- Prefigured Nash equilibrium by 112 years

**Francis Edgeworth (1881)**: Contract curve in exchange (bilateral bargaining)

**Ernst Zermelo (1913)**: Proved chess is determined (either White wins, Black wins, or draw with perfect play)
- Used backward induction
- First theorem in game theory

### Foundational Period (1920s-1950s)

**John von Neumann (1928)**: "Zur Theorie der Gesellschaftsspiele" (On the Theory of Parlor Games)
- Proved minimax theorem: Zero-sum two-player games have equilibrium in mixed strategies
- Foundation for game theory as mathematical discipline

**John von Neumann & Oskar Morgenstern (1944)**: *Theory of Games and Economic Behavior*
- 600-page treatise
- Expected utility theory (preferences over lotteries)
- Extensive form games (game trees)
- Cooperative game theory (coalitions)
- **Impact**: Established game theory as field, but limited to zero-sum games

**John Nash (1950-1951)**: Nash equilibrium
- PhD thesis (27 pages): Generalized equilibrium to non-zero-sum games
- **Nash equilibrium**: Profile where each player best-responds to others
- **Existence theorem**: Every finite game has Nash equilibrium (possibly mixed)
- **Revolution**: Moved beyond zero-sum, opened economics/social sciences applications
- Nobel Prize (1994)

**Lloyd Shapley (1953)**: Shapley value (fair allocation in cooperative games)
- Nobel Prize (2012)

### Golden Age (1960s-1980s)

**Reinhard Selten (1965)**: Subgame perfect equilibrium
- Refined Nash equilibrium using backward induction
- Eliminates non-credible threats
- Nobel Prize (1994)

**John Harsanyi (1967-68)**: Games of incomplete information
- Bayesian Nash equilibrium (players have private information/types)
- Unified game theory with uncertainty
- Nobel Prize (1994)

**Robert Aumann (1976)**: Correlated equilibrium
- Players coordinate on signal
- Generalizes Nash equilibrium
- Nobel Prize (2005)

**Eric Maskin (1977)**: Mechanism design
- Implementation theory: Design games to achieve desired outcomes
- Nobel Prize (2007)

**Robert Axelrod (1984)**: *The Evolution of Cooperation*
- Computer tournaments: Tit-for-tat wins
- Showed cooperation sustainable in repeated games
- Influenced biology, political science, computer science

**David Kreps & Robert Wilson (1982)**: Sequential equilibrium
- Refinement incorporating beliefs at information sets
- Framework for dynamic games with incomplete information

### Modern Era (1990s-Present)

**Auction theory revolution**:
- Paul Milgrom, Robert Wilson (Nobel 2020): Spectrum auctions, electricity markets
- Revenue equivalence theorem, optimal auctions

**Behavioral game theory**:
- Colin Camerer, Ernst Fehr: Experiments show systematic deviations from Nash predictions
- Bounded rationality, fairness concerns, other-regarding preferences

**Algorithmic game theory**:
- Tim Roughgarden, Éva Tardos: Complexity of computing equilibria, price of anarchy
- Applications: Internet routing, sponsored search auctions

**Evolutionary game theory**:
- John Maynard Smith (1973, 1982): Evolutionarily stable strategies (ESS)
- Applied to biology, but also economics (learning dynamics)

## Core Concepts Preview

### Players

**Agents making decisions**. Can be:
- Individuals (consumers, voters)
- Firms (oligopolists)
- Countries (trade, war)
- Genes (evolutionary games)
- Algorithms (computer systems)

**Rationality assumption**: Players have preferences and choose optimally given beliefs

### Strategies

**Complete contingent plan**: Specifies action in every possible situation player might face

**Types**:
- **Pure strategy**: Deterministic choice (always play same action)
- **Mixed strategy**: Randomization over pure strategies (play each with some probability)

### Payoffs

**Numerical representation of preferences**. Encodes:
- What outcomes player prefers
- How much player cares about differences

**Assumptions**:
- **Ordinality**: Only ordering matters (payoffs 1,2,3 equivalent to 10,20,30)
- **Cardinality** (with mixed strategies): Intervals matter (2 vs 3 vs 4 different from 2 vs 10 vs 11)

### Information

**What players know when making decisions**:

**Perfect information**: All previous actions observed (chess, checkers)
**Imperfect information**: Some actions unobserved (poker, sealed-bid auctions)

**Complete information**: Payoff structure (game rules, preferences) common knowledge
**Incomplete information**: Players have private information (types, valuations)

### Equilibrium

**Solution concept**: Prediction of how rational players will play

**Nash equilibrium**: Each player's strategy is best response to others' strategies
- No player regrets choice given others' choices
- Self-enforcing (no incentive to deviate unilaterally)

**Refinements**:
- Subgame perfect: Rules out non-credible threats
- Bayesian Nash: Accounts for incomplete information
- Perfect Bayesian: Incorporates beliefs in dynamic games

## Game Theory vs Decision Theory

| Feature | Decision Theory | Game Theory |
|---------|-----------------|-------------|
| **Agents** | Single decision-maker | Multiple strategic agents |
| **Environment** | Passive (nature) | Active (anticipating opponents) |
| **Optimization** | Maximize expected utility | Best-respond to others' strategies |
| **Solution** | Optimal choice | Equilibrium (mutual best responses) |
| **Uncertainty** | Probabilistic (objective or subjective) | Strategic (opponent's choice) |
| **Example** | Portfolio allocation | Price competition |

**Key difference**: In decision theory, uncertainty is *exogenous* (weather, market returns). In game theory, uncertainty is *endogenous* (opponent's strategy choice).

## The Strategic Form (Normal Form)

**Representation**: Payoff matrix

**Example: Prisoner's Dilemma**

Two suspects interrogated separately. Payoffs = years in prison (negative = bad).

|               | Suspect 2: Cooperate (silent) | Suspect 2: Defect (confess) |
|---------------|-------------------------------|----------------------------|
| **Suspect 1: Cooperate** | -1, -1 | -5, 0 |
| **Suspect 1: Defect** | 0, -5 | -3, -3 |

**Notation**: (Payoff to Player 1, Payoff to Player 2)

**Analysis**:
- If Suspect 2 cooperates → Suspect 1 prefers defect (0 > -1)
- If Suspect 2 defects → Suspect 1 prefers defect (-3 > -5)
- **Dominant strategy**: Defect (best regardless of opponent)
- By symmetry, Suspect 2 also defects
- **Outcome**: (Defect, Defect) → both get -3
- **Tragedy**: Both would prefer (Cooperate, Cooperate) → both get -1
- But cooperation not equilibrium (incentive to deviate)

**Structure**: Individual rationality → collective irrationality

**Ubiquity**:
- Arms races (nations)
- Pollution (firms)
- Free riding (public goods)
- Overfishing (commons)
- Doping (athletes)

## The Extensive Form (Game Tree)

**Representation**: Decision nodes, branches, terminal nodes with payoffs

**Example: Entry Deterrence**

Entrant decides: Enter or Stay Out
If Enter → Incumbent decides: Accommodate or Fight

```
                    Entrant
                   /      \
             Enter          Stay Out
              /                   \
        Incumbent              (0, 10)
         /     \
   Accommodate  Fight
      /            \
   (2, 5)        (-1, 0)
```

**Payoffs**: (Entrant, Incumbent)

**Backward induction** (solve from end):
1. Incumbent node: Accommodate (5) > Fight (0) → choose Accommodate
2. Entrant anticipates Incumbent will Accommodate
3. Entrant compares: Enter → 2, Stay Out → 0
4. **Equilibrium**: Enter, Accommodate

**Incumbent's threat** ("I'll fight if you enter") **not credible**: Once entry occurred, fighting irrational (0 < 5).

**Commitment problem**: Incumbent would prefer to deter entry (10 > 5), but can't credibly threaten to fight.

**Solutions** (make threat credible):
- Invest in excess capacity (lowers cost of fighting → makes fight rational)
- Reputation (fight now to deter future entrants)
- Contract with manager (bonus for market share → manager fights)

## Applications Across Domains

### Economics

**Oligopoly theory**:
- Cournot (quantity competition)
- Bertrand (price competition)
- Stackelberg (sequential moves)

**Auctions**:
- Revenue equivalence theorem
- Optimal auction design
- Winner's curse

**Contracts**:
- Principal-agent (moral hazard)
- Screening (adverse selection)
- Signaling (education, warranties)

### Politics

**Voting**:
- Strategic voting (vote for lesser evil, not true preference)
- Median voter theorem
- Condorcet paradox

**Legislatures**:
- Agenda control
- Logrolling (vote trading)
- Filibuster as commitment device

**International relations**:
- Deterrence
- Alliances
- Trade agreements (tariffs as strategic)

### Biology

**Evolutionary games**:
- Hawk-Dove (aggression vs appeasement)
- Sex ratios (Fisher's principle)
- Costly signaling (peacock's tail)

**Cooperation**:
- Kin selection (Hamilton's rule)
- Reciprocal altruism (Trivers)
- Group selection

**Conflict**:
- Parent-offspring conflict (Trivers)
- Sexual conflict (infanticide, mate guarding)

### Military Strategy

**Deterrence**:
- Mutual Assured Destruction (MAD)
- First-strike vs second-strike capability
- Escalation dominance

**Tactics**:
- Bluffing (appear strong when weak)
- Commitment (burn bridges to signal resolve)
- Coordination (allied operations)

### Negotiations

**Bargaining power**:
- Outside options (BATNA)
- Patience (discount factor)
- Information asymmetry

**Tactics**:
- First-mover advantage (anchoring)
- Commitment (take options off table)
- Linking issues (package deals)

## Key Insights Game Theory Provides

### 1. Equilibrium ≠ Optimum

**Prisoner's Dilemma**: Equilibrium (Defect, Defect) inferior to (Cooperate, Cooperate)

**Implication**: Free markets don't automatically solve all coordination problems. Institutions matter.

### 2. More Options Can Hurt

**Commitment**: Ability to remove options paradoxically increases payoff

**Example: Cortés burning ships**
- Removed retreat option → soldiers fought harder → won
- If retreat available, soldiers might have fled → lost

**Bargaining**: "I have no authority to accept your offer" strengthens position (credibly refuses concessions)

### 3. Credibility is Everything

**Threat/promise credible only if ex-post rational** (rational to execute after situation arises)

**Non-credible**: "I'll blow up the world if you invade" (mutual destruction)
**Credible**: "I'll retaliate proportionally if you invade" (protects my interests)

**Policy**: Nuclear second-strike (credible—retaliation rational after absorbing first strike). Nuclear first-strike (incredible—initiating Armageddon irrational).

### 4. Information is Strategic

**Signaling games**: Actions reveal information

**Example: Education as signal** (Spence)
- Productivity unobservable by employers
- High-ability workers find education easier (lower cost)
- Education doesn't increase productivity but signals ability
- **Equilibrium**: High-ability get education, low-ability don't
- Employers pay more to educated workers (correctly infer high ability)
- **Result**: Education valuable even if it doesn't teach anything useful

**Screening**: Uninformed party designs menu to separate types
- Insurance companies offer high-deductible (low-premium) and low-deductible (high-premium) plans
- Healthy people choose high-deductible (low expected claims)
- Unhealthy people choose low-deductible (high expected claims)
- Insurer separates types via self-selection

### 5. Repetition Changes Everything

**One-shot Prisoner's Dilemma**: Defect dominates

**Repeated Prisoner's Dilemma**: Cooperation sustainable if discount factor high enough (players value future)

**Mechanisms**:
- Grim trigger: Cooperate until opponent defects once, then defect forever
- Tit-for-tat: Copy opponent's previous move
- Tit-for-two-tats: More forgiving

**Folk theorem**: In infinitely repeated games, wide range of outcomes sustainable as equilibria (including cooperative outcomes)

**Applications**:
- Cartels (cooperate on high prices if future profits matter)
- International cooperation (treaties sustainable without enforcement if repeated interaction)
- Social norms (cooperation enforced by reputation)

### 6. Randomness Can Be Rational

**Mixed strategies**: Optimal to randomize in some games

**Example: Penalty kicks (soccer)**
- Kicker: Shoot left or right
- Goalie: Dive left or right
- If kicker always shoots left → goalie always dives left → kicker should switch
- **Equilibrium**: Both randomize (kicker: 50-50, goalie: 50-50)
- Randomization keeps opponent guessing

**Applications**:
- Military tactics (unpredictable attack timing/location)
- Sports (play-calling)
- Tax audits (random audits deter evasion)
- Patent litigation (randomness of court decisions shapes settlement)

### 7. Forward Induction Conveys Information

**Logic**: Rational player wouldn't take action A unless planning to do B later

**Example: Burning money**
- Two firms: Incumbent, Entrant
- Incumbent can burn $1 million before Entrant decides to enter
- Entrant observes if Incumbent burned money
- If Incumbent burns money → signals irrational or desperate → Entrant enters
- If Incumbent doesn't burn money → signals rational → credible threat to fight → Entrant stays out
- **Weird conclusion**: Burning money (wasteful) can deter entry (by signaling type)

**Applications**:
- Advertising (conspicuous waste signals quality)
- Warfare (costly signal of resolve)
- Dating (expensive gifts signal commitment)

## Common Pitfalls

### 1. Confusing Equilibrium with Prediction

**Nash equilibrium**: No player regrets choice given others' choices

**Not claimed**:
- Players will find equilibrium (might require learning, iteration)
- Equilibrium is unique (many games have multiple equilibria)
- Equilibrium is Pareto-efficient (Prisoner's Dilemma: equilibrium dominated)

**Use**: Benchmark for analysis, not literal prediction

### 2. Assuming Common Knowledge of Rationality

**Common knowledge**: I know X, you know I know X, I know you know I know X, ad infinitum

**Required for**: Backward induction, iterated elimination of dominated strategies

**Rarely holds**: Real players have bounded rationality, don't think infinitely many steps ahead

**Implication**: Equilibrium refinements (subgame perfection, forward induction) might assume too much

### 3. Ignoring Behavioral Factors

**Standard game theory**: Players maximize expected utility, no other considerations

**Reality**:
- Fairness concerns (Ultimatum Game: reject unfair offers even when costly)
- Bounded rationality (limited computation, satisficing)
- Emotions (anger, fear, spite)
- Framing effects (risk-averse for gains, risk-seeking for losses)

**Behavioral game theory**: Incorporates these factors (Camerer, Fehr, Rabin)

### 4. Mistaking Tool for Reality

**Game theory**: Analytical framework (like calculus)

**Not**: Description of how people actually think

**Use**: Generate insights, organize thinking, derive implications

**Don't**: Assume people explicitly solve games in real-time

## How to Use This Guide

**Analytical toolkit**: Each chapter provides concepts applicable across domains

**Chapter 2-3: Foundations** (strategic form, Nash equilibrium, mixed strategies)
- Learn to represent strategic situations as games
- Solve for equilibria
- Understand when mixed strategies optimal

**Chapter 4: Sequential games** (extensive form, backward induction, subgame perfection)
- Analyze dynamic interactions
- Identify credible vs non-credible threats
- Apply to negotiations, deterrence, commitment

**Chapter 5: Repeated games** (cooperation, reputation, Folk theorem)
- Understand how repetition enables cooperation
- Design mechanisms for sustained collaboration
- Analyze breakdown of cooperation

**Chapter 6: Information asymmetry** (signaling, screening, Bayesian games)
- Model private information
- Design contracts/mechanisms to extract information
- Understand adverse selection and moral hazard

**Chapter 7: Applications** (auctions, voting, evolution, bargaining, mechanism design)
- See game theory in action across domains
- Recognize game-theoretic structures in real situations
- Apply appropriate solution concepts

**Chapter 8: Glossary**
- Reference for technical terms
- Quick lookup for concepts

**Multiplier effect**: Once you see the world through game-theoretic lens, you'll notice strategic interactions everywhere. Economics, politics, evolution, negotiations, warfare, dating, parenting—all involve anticipating others' anticipation of your choices. This guide provides the tools to think clearly about such situations.

## Key Terms

- **Game theory**: Mathematical study of strategic interaction—situations where optimal choice depends on others' choices
- **Strategy**: Complete contingent plan specifying action in every situation player might face
- **Payoff**: Numerical representation of preferences over outcomes
- **Nash equilibrium**: Strategy profile where each player best-responds to others' strategies
- **Dominant strategy**: Strategy best regardless of opponents' choices
- **Rationality**: Choosing optimally given beliefs and preferences
- **Common knowledge**: I know X, you know I know X, I know you know I know X, ad infinitum
- **Perfect information**: All previous actions observed (chess)
- **Complete information**: Payoff structure common knowledge
- **Backward induction**: Solving game from end to beginning
- **Subgame perfect equilibrium**: Equilibrium specifying Nash equilibrium in every subgame
- **Credible threat**: Threat rational to execute if situation arises
- **Commitment**: Removing options to gain strategic advantage

## Summary

Game theory is the mathematical study of strategic interaction—situations where your best choice depends on others' choices, and they face the same interdependence. Developed by von Neumann (1928), Nash (1950), and others, it provides rigorous tools for analyzing economics (oligopoly, auctions, contracts), politics (voting, deterrence, coalitions), biology (evolution, cooperation, conflict), military strategy (deterrence, credibility), and negotiations (bargaining power, commitment).

Core concepts: Players choose strategies maximizing payoffs given beliefs about others' strategies. Nash equilibrium—each player best-responds to others—is central solution concept, refined by subgame perfection (credibility), Bayesian Nash (incomplete information), and other concepts. Strategic form (payoff matrices) represents simultaneous games; extensive form (game trees) represents sequential games.

Key insights: (1) Equilibrium ≠ optimum (Prisoner's Dilemma), (2) removing options can increase payoffs (commitment), (3) credibility essential for threats/promises, (4) information is strategic (signaling, screening), (5) repetition enables cooperation (Folk theorem), (6) randomization rational (mixed strategies), (7) actions convey information (forward induction).

Game theory reveals hidden structure in strategic situations, exposes failures of naïve reasoning (voting paradoxes, winner's curse, coordination failures), and enables institutional design (auctions, matching markets, mechanism design). Once learned, it permanently changes how you see economics, politics, evolution, military strategy, and negotiations—a true multiplier effect on understanding.

Following chapters develop these concepts rigorously, showing how to model strategic situations, solve for equilibria, and apply insights across domains. This is not a subject but an analytical toolkit—learn it once, use it everywhere.
