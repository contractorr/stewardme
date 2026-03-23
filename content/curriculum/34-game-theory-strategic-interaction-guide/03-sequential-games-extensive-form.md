# Sequential Games & Extensive Form

## Extensive Form Representation

**Game tree**: Graphical representation of sequential game showing:
1. **Decision nodes**: Points where player chooses action
2. **Branches**: Available actions at each node
3. **Terminal nodes**: End points with payoffs
4. **Information sets**: Nodes player cannot distinguish

**Components**:
- **Initial node**: Starting point (usually nature or first mover)
- **Player labels**: Which player moves at each node
- **Action labels**: What choices available
- **Payoffs**: Outcome at terminal nodes (ordered tuple)

**Example: Entry Deterrence**

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

Player labels at nodes, payoffs (Entrant, Incumbent) at terminal nodes.

## Backward Induction

**Algorithm**: Solve game from end to beginning

**Steps**:
1. Start at terminal nodes
2. At each penultimate decision node, identify player's optimal action (compare payoffs at resulting terminal nodes)
3. Replace subgame with payoffs from optimal action
4. Move backward to previous decision nodes
5. Repeat until reaching initial node

**Entry Deterrence Solution**:
1. Incumbent's node: Compare Accommodate (5) vs Fight (0) → Accommodate
2. Entrant's initial node: Compare Enter → 2 (anticipating Accommodate) vs Stay Out → 0
3. **Outcome**: Enter, Accommodate → (2, 5)

**Incumbent's threat** "Fight if entry" is **non-credible**: Once entry occurred, Incumbent prefers Accommodate (5 > 0).

## Subgame Perfect Equilibrium (SPE)

**Definition** (Reinhard Selten, 1965): Nash equilibrium in every subgame

**Subgame**: Portion of game tree starting from single node that:
1. Includes all successors of that node
2. Doesn't break information sets (if node in information set, all nodes in that set must be included)

**SPE requirement**: Strategies specify Nash equilibrium not only in full game but in every continuation (subgame).

**Refinement**: SPE ⊂ Nash equilibrium (every SPE is Nash, but not vice versa)
- SPE eliminates non-credible threats/promises
- Requires sequential rationality at every node

**Entry Deterrence**:

**Nash equilibria**:
1. (Enter, Accommodate) → (2, 5)
2. (Stay Out, Fight) → (0, 10)

Second equilibrium uses threat "Fight if entry." But threat not credible (subgame starting from Incumbent's node, Fight not best response).

**SPE**: Only (Enter, Accommodate)

### Stackelberg Duopoly

**Sequential quantity competition**: Leader moves first, follower observes, then moves.

Inverse demand: P = a - Q where Q = q₁ + q₂
Firm i profit: πᵢ = qᵢ(a - q₁ - q₂ - c)

**Backward induction**:

**Stage 2** (Follower): Chooses q₂ to maximize π₂ given q₁
```
∂π₂/∂q₂ = a - q₁ - 2q₂ - c = 0
q₂(q₁) = (a - c - q₁)/2  [Follower's reaction function]
```

**Stage 1** (Leader): Anticipates q₂(q₁), chooses q₁ to maximize π₁
```
π₁ = q₁[a - q₁ - q₂(q₁) - c]
   = q₁[a - q₁ - (a - c - q₁)/2 - c]
   = q₁[(a - c - q₁)/2]

∂π₁/∂q₁ = (a - c)/2 - q₁ = 0
q₁* = (a - c)/2
```

**Substitute back**:
```
q₂* = (a - c - q₁*)/2 = (a - c - (a - c)/2)/2 = (a - c)/4
```

**SPE outcome**:
- Leader: q₁* = (a - c)/2, π₁* = [(a - c)/2]²
- Follower: q₂* = (a - c)/4, π₂* = [(a - c)/4]²
- Total output: Q* = 3(a - c)/4

**Comparison**:
- **Cournot** (simultaneous): q₁ = q₂ = (a - c)/3
- **Stackelberg**: q₁ = (a - c)/2, q₂ = (a - c)/4
- **First-mover advantage**: Leader produces more, earns higher profit

**Intuition**: Leader commits to high quantity. Follower best-responds to this commitment. If simultaneous, both would produce less (Cournot).

## Credible Threats and Commitment

**Credibility**: Threat/promise is credible if ex-post rational (carrying it out is optimal once situation arises)

**Non-credible threat example**: Parent threatens child "If you misbehave, I'll cancel Christmas."
- Once December arrives and child misbehaved months ago, canceling Christmas hurts parent (and siblings) → not credible
- Child anticipates, doesn't believe threat

**Credible threat example**: "If you misbehave, you're grounded tonight."
- Low cost to parent → credible

### Commitment Devices

**Removing options**: Paradoxically increases payoffs by making threats credible

**Cortés burning ships** (Mexico, 1519):
- Eliminated retreat option
- Soldiers knew: Fight or die (no escape)
- Increased fighting intensity → victory
- If ships available, soldiers might have retreated → defeat

**Dr. Strangelove's Doomsday Machine**:
- Automatic retaliation (nuclear device triggers if USSR attacked)
- Removes choice → threat credible (cannot be called back)
- Problem: Must be known to deter (in movie, USSR failed to announce it)

**Union strikes**:
- Pre-committed to strike if demands unmet
- Credible because stopping strike requires re-vote (coordination problem)
- Makes threat of strike credible → increases bargaining power

### Finite Horizon Commitment

**Chain store paradox** (Selten, 1978):

Chain store operates in 20 towns. In each town, potential entrant decides to enter or stay out. If entry, chain decides to fight (costly) or accommodate.

**Payoffs per town**:
- No entry: Chain gets 5
- Entry + Accommodate: Chain gets 2, Entrant gets 2
- Entry + Fight: Chain gets 0, Entrant gets -1

**Backward induction**:
- Town 20 (last): Chain prefers Accommodate (2 > 0) → Entrant enters
- Town 19: Chain knows reputation irrelevant (Town 20 entrant will enter regardless). Prefer Accommodate → Entrant 19 enters
- Town 18: Same logic → Entrant 18 enters
- **Unraveling**: By backward induction, entry occurs in all 20 towns

**SPE**: Entry in all towns, Chain accommodates all

**Intuition**: Finite horizon → no future to invest in reputation → reputation can't sustain deterrence

**Contrast with infinite/uncertain horizon**: If indefinite future, reputation valuable → fighting early to deter future entry can be optimal.

## Ultimatum Game

**Structure**:
- Proposer offers division of $10: ($x, $10-x) where x ∈ [0, 10]
- Responder accepts or rejects
- If accept: Payoffs as proposed
- If reject: Both get $0

**Backward induction**:
- Responder: Accept if $10 - x ≥ 0, i.e., x ≤ 10
- Responder accepts any positive offer (even $0.01)
- Proposer: Knowing Responder accepts anything, offers minimum (e.g., ($9.99, $0.01))

**SPE**: Proposer takes nearly everything, Responder accepts

**Experimental results** (consistent across cultures):
- Modal offer: 40-50% split
- Offers <20% rejected ~50% of time
- Mean offer: ~40%

**Interpretation**:
- Fairness norms (people dislike inequality)
- Spite/punishment (rejecting unfair offers to punish proposer)
- Strategic uncertainty (if responder might reject, safer to offer more)
- Reputation concerns (if repeated or observed)

**Implications**: Standard game theory (pure self-interest) doesn't fully capture human behavior. Behavioral game theory incorporates fairness, reciprocity, bounded rationality.

## Centipede Game

Two players alternate taking large share ($L$) or passing. Pot grows each round. If pass, opponent chooses take or pass (larger pot). Final round: Last player takes entire pot.

```
          1        2        1        2        1
         / \      / \      / \      / \      / \
      (1,0) (0,2) (3,1) (2,4) (5,3) (4,6) (7,5) (6,8)
       Take Pass  Take Pass  Take Pass  Take Pass
```

**Payoffs**: (Player 1, Player 2) if taking at that node. If pass, next player decides.

**Backward induction**:
- Final node (Player 1): Take (7) vs Pass → opponent gets 8, Player 1 gets 6. Take.
- Previous node (Player 2): Anticipate Player 1 takes at next node → Player 2 gets 5. Compare to taking now (6). Take.
- **Unraveling**: Backward induction → both take at first opportunity → (1, 0)

**SPE**: Player 1 takes immediately → (1, 0)

**Experiments**: Players pass multiple times before someone takes. Average payoffs much higher than (1, 0).

**Explanations**:
- Bounded rationality (don't backward induct fully)
- Altruism (prefer joint payoff maximization)
- Uncertainty about opponent's type (might be altruistic or irrational)

**Implication**: Strict backward induction requires strong assumptions (common knowledge of rationality, expected utility maximization, no regard for others' payoffs).

## Bargaining: Rubinstein Model

**Infinite-horizon alternating-offers bargaining** (Ariel Rubinstein, 1982):

Players 1 and 2 bargain over division of $1 pie.
- Period 1: Player 1 proposes split (x, 1-x). Player 2 accepts or rejects.
  - If accept: Game ends, payoffs (x, 1-x)
  - If reject: Move to Period 2
- Period 2: Player 2 proposes (y, 1-y). Player 1 accepts or rejects.
- Continue indefinitely until agreement.

**Discount factors**: δ₁, δ₂ ∈ (0, 1) (players prefer earlier agreement)

**SPE** (unique):

Player 2 indifferent between:
- Accepting x today: Gets 1 - x
- Rejecting, proposing y next period: Gets δ₂·y

Indifference: 1 - x = δ₂·y → x = 1 - δ₂·y ... (1)

Player 1 indifferent between:
- Accepting y today: Gets y
- Rejecting, proposing x next period: Gets δ₁·x

Indifference: y = δ₁·x ... (2)

Substitute (2) into (1):
```
x = 1 - δ₂·δ₁·x
x(1 + δ₁δ₂) = 1
x* = 1/(1 + δ₁δ₂)

y* = δ₁·x* = δ₁/(1 + δ₁δ₂)
```

**Immediate agreement**: Player 1 proposes x*, Player 2 accepts.

**Special case** (δ₁ = δ₂ = δ):
```
x* = 1/(1 + δ)
y* = δ/(1 + δ)
```

As δ → 1 (patient): x* → 1/2, y* → 1/2 (equal split)

**First-mover advantage**: x* > 1/2 if δ < 1 (Player 1 gets more as proposer)

**Comparative statics**:
- More patient (higher δᵢ): Larger share (can credibly reject unfavorable offers)
- More impatient (lower δᵢ): Smaller share (eager to settle quickly)

**Applications**:
- Labor negotiations: Strike = delay → impatience matters
- International negotiations: Patient party (secure alternatives) gets more
- Legal settlements: Side facing higher litigation costs more impatient → settles for less

## Perfect Information vs Imperfect Information

**Perfect information**: Every decision node is singleton information set (player knows exactly where they are in game tree)
- Examples: Chess, checkers, tic-tac-toe
- Backward induction applies directly

**Imperfect information**: Some decision nodes grouped into information sets (player cannot distinguish between nodes)
- Examples: Poker, sealed-bid auctions, simultaneous moves

**Representing simultaneous moves**: Place nodes in same information set

**Example: Prisoner's Dilemma (extensive form)**

```
         Player 1
         /      \
    Coop        Defect
     /            \
Player 2        Player 2
 /    \          /    \
C      D        C      D
|      |        |      |
(3,3) (0,5)   (5,0)  (1,1)
```

Player 2's two decision nodes in same information set (doesn't observe Player 1's move). Equivalent to normal form game.

## Applications

### Patent Race

Two firms racing to patent innovation. First to succeed gets entire market profit Π. R&D requires investment I.

**Sequential** (one firm starts earlier):
- Leader invests I → patents innovation → gets Π
- Follower sees this → doesn't invest (cannot overtake)
- **Outcome**: Leader gets Π - I, Follower gets 0

**Simultaneous** (both start same time):
- Prob of success for firm i: pᵢ = f(Iᵢ) (increasing, concave)
- Firm i expected profit: pᵢΠ - Iᵢ - (1 - pᵢ)pⱼΠ (last term = Prob opponent succeeds when you fail × loss)
- **Equilibrium**: Both invest, both have chance of winning → dissipation of rents

**First-mover advantage**: Sequential race has only one investor (more efficient). Simultaneous race has duplicated effort (social waste).

### Reputation in Repeated Trust Game

**One-shot Trust Game**:
```
         Trustor
         /      \
     Trust    Not Trust
      /            \
  Trustee         (1, 1)
   /    \
Return  Keep
  |      |
(2,2)  (0,3)
```

Trustee prefers Keep (3 > 2). Trustor anticipates, chooses Not Trust. **Outcome**: (1, 1)

**Repeated**: If game repeats indefinitely (or with probability of continuation), Trustee may Return to build reputation → induce future trust → higher long-term payoff.

**Example**: eBay sellers build reputation (honest transactions) to attract buyers. Short-term temptation to cheat outweighed by long-term reputation value.

**Finite repetition**: Backward induction unravels cooperation (similar to chain store). Last round: Trustee keeps. Round T-1: Knowing T-th round will fail, Trustor doesn't trust. Unravels to first round.

**Escape**: Uncertainty about final round, uncertainty about opponent's type (possibly irrational or altruistic), bounded rationality.

## Key Terms

- **Extensive form**: Game tree representation of sequential game
- **Decision node**: Point where player chooses action
- **Terminal node**: Endpoint with payoffs
- **Information set**: Nodes player cannot distinguish (imperfect information)
- **Backward induction**: Solving game from end to beginning
- **Subgame**: Portion of game tree starting from single node
- **Subgame perfect equilibrium (SPE)**: Nash equilibrium in every subgame
- **Credible threat**: Threat that is optimal to execute ex-post
- **Commitment**: Removing options to make threats/promises credible
- **First-mover advantage**: Benefit from moving first (commitment, leadership)
- **Perfect information**: All previous actions observed
- **Imperfect information**: Some actions unobserved

## Summary

Extensive form (game tree) represents sequential games with decision nodes, branches, and terminal payoffs. Backward induction solves by working from end to beginning. Subgame perfect equilibrium (SPE)—Nash equilibrium in every subgame—refines Nash by eliminating non-credible threats. Entry Deterrence: Incumbent's threat to fight is incredible (prefers accommodate ex-post) → entrant enters. Stackelberg duopoly: Leader commits to high quantity → follower best-responds → first-mover advantage.

Credibility distinguishes SPE from Nash. Commitment devices (removing options) paradoxically increase payoffs by making threats credible (Cortés burning ships, Doomsday Machine, union strike commitments). Chain store paradox: Finite horizon unravels reputation (backward induction → entry in all towns). Infinite/uncertain horizon sustains reputation.

Ultimatum Game: SPE predicts proposer takes nearly everything, but experiments show 40-50% offers (fairness norms, rejection of unfair offers). Centipede Game: SPE predicts immediate defection, but players cooperate multiple rounds (bounded rationality, altruism, uncertainty about types). Rubinstein bargaining: Unique SPE with immediate agreement, first-mover advantage, patient player gets more.

Perfect vs imperfect information: Perfect (chess)—backward induction applies directly. Imperfect (poker, simultaneous moves)—information sets group indistinguishable nodes. Applications: Patent races (first-mover advantage avoids duplicated R&D), reputation in trust games (future value sustains current honesty). SPE provides powerful solution concept for dynamic games, though requires strong rationality assumptions.
