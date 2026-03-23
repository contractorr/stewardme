# Applications Across Domains

## Economics & Business

### Mechanism Design

**Goal**: Design institutions/rules achieving desired outcomes given strategic agents

**Revelation principle**: Any outcome achievable by mechanism can be achieved by direct mechanism where truthful revelation is equilibrium

**Classic problems**:

**1. Vickrey-Clarke-Groves (VCG) Mechanism**

**Problem**: Allocate indivisible good to bidders with private valuations

**Mechanism**:
- Each reports valuation vᵢ
- Allocate to highest reported value
- Winner pays externality imposed on others (second-highest bid in single-item case)

**Properties**:
- Truth-telling dominant strategy
- Efficient allocation (goes to highest valuation)
- Individual rationality (non-negative payoff)

**Application**: Google/Facebook ad auctions (generalized second-price auctions)

**2. Optimal Auctions** (Myerson, 1981)

**Problem**: Revenue-maximizing auction

**Result**: Set reserve price (minimum bid) even if no direct cost. Balances:
- Higher reserve → increases revenue conditional on sale
- But decreases probability of sale

**Optimal reserve**: r* where marginal revenue from higher price = marginal loss from reduced sale probability

**Application**: eBay reserve prices, spectrum auctions

**3. Matching Markets** (Gale-Shapley, 1962)

**Problem**: Match residents to hospitals, students to schools (can't use prices)

**Deferred acceptance algorithm**:
1. Each student proposes to top choice school
2. Schools tentatively accept top applicants (up to capacity), reject others
3. Rejected students propose to next choice
4. Repeat until all matched or exhausted options

**Properties**:
- Always produces stable matching (no blocking pairs)
- Strategy-proof for proposing side
- Not strategy-proof for receiving side (can manipulate via false preferences)

**Applications**:
- Medical residency (NRMP): ~45k residents matched annually
- NYC school choice: ~90k students
- Kidney exchange: Match donor-recipient pairs

### Bargaining

**Nash Bargaining Solution** (axiomatic, 1950):

**Setup**: Two players split surplus S. Disagreement payoffs (d₁, d₂).

**Axioms**:
1. Pareto efficiency
2. Symmetry (if symmetric positions, equal split)
3. Invariance to affine transformations
4. Independence of irrelevant alternatives

**Unique solution**: Maximize product of surplus gains:
```
max (x₁ - d₁)(x₂ - d₂) subject to x₁ + x₂ = S
```

**If d₁ = d₂ = 0**: Equal split (S/2, S/2)

**Rubinstein bargaining** (non-cooperative, 1982):
- Alternating offers, discounting δ
- SPE: Immediate agreement, first-mover advantage
- As δ → 1, converges to equal split

**Applications**:
- Labor negotiations (strikes = disagreement point)
- Divorce settlements (litigation = disagreement)
- International negotiations (war/sanctions = disagreement)

### Platform Competition

**Two-sided markets**: Platform connects two user groups (buyers-sellers, riders-drivers)

**Network effects**:
- **Direct**: More users of same type → more valuable (social networks)
- **Indirect (cross-side)**: More users of one type → more valuable for other type (credit cards: more merchants → more attractive to cardholders)

**Strategy**: Price below cost on one side (subsidize), extract rent from other side
- Uber: Subsidize riders (low fares, promotions), charge drivers commission
- Credit cards: Subsidize cardholders (cashback, points), charge merchants 2-3%
- Video game consoles: Sell consoles at loss, profit from game licensing

**Tipping**: Winner-take-all dynamics (one platform dominates due to network effects)
- VHS vs Betamax
- Windows vs Mac (in 1990s)
- Uber vs Lyft (local markets tip)

**Multi-homing**: Users join multiple platforms
- Reduces tipping (users hedge bets)
- Increases competition

## Politics & Governance

### Voting Systems

**Condorcet paradox**: Social preferences can cycle even if individual preferences transitive

**Example**: 3 voters, 3 candidates (A, B, C)
- Voter 1: A > B > C
- Voter 2: B > C > A
- Voter 3: C > A > B

**Pairwise votes**:
- A vs B: A wins (voters 1,3)
- B vs C: B wins (voters 1,2)
- C vs A: C wins (voters 2,3)

**Cycle**: A > B > C > A → no Condorcet winner

**Arrow's Impossibility Theorem** (1951): No voting system satisfies:
1. Unanimity (if all prefer A > B, society prefers A > B)
2. Independence of irrelevant alternatives
3. Non-dictatorship
4. Transitivity of social preferences

**Strategic voting**:

**Example**: 3 candidates (L, C, R), plurality rule, 100 voters
- 35: L > C > R
- 33: C > L > R
- 32: R > C > L

**Sincere voting**: L wins (35 > 33 > 32)

**Strategic voting**: C supporters might vote L (second choice) if polls show R close to winning. Prevents worst outcome (R).

**Median voter theorem** (Downs, 1957): With single-dimensional policy and symmetric distribution, candidates converge to median voter's position.

**Assumptions**: Complete info, single dimension, probabilistic voting

**Failures**: Multi-dimensional issues, asymmetric info, voter turnout considerations

### Political Economy

**Mancur Olson's Logic of Collective Action** (1965):

**Small groups**: Easier to organize (low free-riding, high per-capita benefit)
- Example: Agricultural subsidies (farmers concentrated, well-organized)

**Large groups**: Harder to organize (free-riding problem, dispersed costs)
- Example: Consumers (dispersed, each pays small amount → don't lobby effectively)

**Result**: Small special interests prevail over general public (concentrated benefits, dispersed costs)

**Rent-seeking**: Expend resources to capture transfers (lobbying, campaign contributions)
- Deadweight loss (resources wasted on political activity, not production)

**Public choice theory**: Apply game theory to political actors (politicians, bureaucrats, voters)
- Politicians maximize votes/power, not social welfare
- Bureaucrats maximize budgets/scope
- Voters rationally ignorant (cost of information > benefit)

### International Relations

**Deterrence**: Threaten punishment to prevent action

**Requirements for credibility**:
1. Capability (can execute threat)
2. Resolve (willing to execute)
3. Communication (threat known)

**Mutual Assured Destruction (MAD)**:
- Both sides have second-strike capability (survive first strike, retaliate)
- Nuclear war = both destroyed → deterrence stable
- **Paradox**: Vulnerability creates security (if can destroy enemy's nukes, crisis unstable)

**Cuban Missile Crisis** (1962):
- Game of Chicken: Both backing down > war, but unilateral backing down costly
- Kennedy chose "blockade" (middle option) → signaled resolve without forcing USSR to escalate or back down completely
- Khrushchev withdrew missiles (US secretly agreed to remove Turkish missiles later)

**Commitment problems in war**:
- **Preventive war**: State in decline may attack rising power preemptively
- **Bargaining failure**: Both would benefit from settlement avoiding war costs, but asymmetric info + commitment problems cause war

**Fearon's rationalist explanations for war** (1995):
1. Private information + incentive to misrepresent (bluffing about strength)
2. Commitment problems (shifts in power, cannot commit to future restraint)
3. Indivisible stakes (cannot split prize, though rare)

**Trade as peace**: Repeated interaction, economic interdependence → increase cost of war → deter conflict

## Biology & Evolution

### Evolutionarily Stable Strategy (ESS)

**Definition** (Maynard Smith, 1973): Strategy that, if adopted by population, cannot be invaded by rare mutant

**Formal**: Strategy σ* is ESS if for all σ ≠ σ*:
```
Either: u(σ*, σ*) > u(σ, σ*)  [strict Nash]
Or:     u(σ*, σ*) = u(σ, σ*) and u(σ*, σ) > u(σ, σ)  [stability condition]
```

**Interpretation**: Mutant doesn't outperform incumbent, or if tied against incumbent, loses against itself.

**Hawk-Dove ESS**:

|               | Hawk  | Dove  |
|---------------|-------|-------|
| **Hawk**      | (V-C)/2, (V-C)/2 | V, 0  |
| **Dove**      | 0, V  | V/2, V/2 |

V = value of resource, C = cost of fight

**Case 1**: V > C (resource valuable, fight cheap)
- Pure Hawk is ESS

**Case 2**: V < C (fight costly)
- Mixed ESS: Play Hawk with probability p = V/C
- No pure strategy ESS

**Bourgeois strategy**: "If owner, Hawk; if intruder, Dove"
- Respects property rights
- ESS if V > C (avoids costly conflicts)
- Observed in many territorial animals (birds, lizards, butterflies)

### Sex Ratios

**Fisher's principle** (1930): 1:1 sex ratio is ESS

**Logic**: Suppose population female-biased (more females than males)
- Male offspring have more mating opportunities → higher reproductive success
- Parents producing male-biased offspring have higher fitness
- Selection favors male production → ratio shifts toward 1:1
- At 1:1, neither sex has advantage → ESS

**Equal investment principle**: ESS is equal parental investment in males vs females (not necessarily equal numbers if costs differ)

**Observed**: Most species have ~1:1 sex ratios, consistent with Fisher's principle

**Exceptions**: Parasitic wasps (females control offspring sex, adjust ratio to local competition)

### Cooperation and Kin Selection

**Hamilton's rule** (1964): Altruistic behavior evolves if:
```
rB > C
```
- r = relatedness (probability allele shared)
- B = benefit to recipient
- C = cost to altruist

**Parent-offspring**: r = 1/2 → sacrifice worthwhile if B > 2C

**Siblings**: r = 1/2 → help sibling if B > 2C

**Cousins**: r = 1/8 → help if B > 8C

**Haldane's quip**: "I would lay down my life for two brothers or eight cousins."

**Eusocial insects** (ants, bees, termites):
- Workers sterile, help queen reproduce
- Haplodiploidy (bees): Sisters share 3/4 genes (r = 3/4) → higher relatedness than parent-offspring → evolution of worker caste
- Massive cooperation (colonies ~millions of individuals)

**Green-beard effect**: Gene causing:
1. Observable trait (e.g., green beard)
2. Recognition of trait in others
3. Preferential treatment of trait-bearers

Rare in nature (requires tight linkage, vulnerable to cheaters who display trait but don't reciprocate).

## Military Strategy

### Bluffing and Commitment

**Schelling's "Strategy of Conflict"** (1960):

**Commitment**: Eliminate options to strengthen position
- Burn bridges (Cortés)
- Tie hands (automated retaliation)
- Delegate to agent with different preferences (hardline general)

**Brinkmanship**: Push to edge of disaster to force opponent to back down
- Cuban Missile Crisis
- Chicken game dynamics

**Focal points**: Salient outcomes coordinate expectations
- Ceasefire lines (natural borders: rivers, mountains)
- Round numbers in negotiations ($1M, not $987,342)

**Limited war**: Restraints (no nukes, no invasion of homeland) prevent escalation
- Korea, Vietnam (US didn't invade North)
- Rules emerge from repeated interactions

### Guerrilla Warfare

**Asymmetric conflict**: Weak insurgent vs strong state

**Insurgent strategy**:
- Avoid direct confrontation (lose)
- Hit-and-run, blend into population
- Increase state's costs until withdrawal

**State challenges**:
- Distinguish insurgents from civilians (information problem)
- Harsh tactics alienate population → more recruits for insurgents
- Hearts-and-minds vs overwhelming force trade-off

**Game-theoretic model**: Insurgent has private info about location/strength. State searches, screens population. Type I vs Type II errors (punish innocent vs miss guilty).

### Nuclear Deterrence

**First-strike vs second-strike**:
- **First-strike capability**: Can destroy enemy's nukes preemptively → crisis instability (use-it-or-lose-it incentives)
- **Second-strike capability**: Survive first strike, retaliate → stable deterrence (no incentive to strike first)

**Survivability**: Submarines (SSBNs) optimal second-strike (hard to locate/destroy simultaneously)

**Arms control**: Limit counterforce weapons (silo-busters) → enhance second-strike → stability
- ABM Treaty (1972-2002): Limited missile defenses (defenses destabilize if allow first-striker to avoid retaliation)
- SALT/START: Cap strategic weapons

**Rationality paradox**: Deterrence requires credible threat of irrational response (massive retaliation). Solution: Delegation to military with automatic response, or reputation for irrationality.

## Negotiations & Law

### Litigation vs Settlement

**Priest-Klein model** (1984):

**Setup**:
- Plaintiff and defendant have private info about case strength
- Litigation costs: Cₚ for plaintiff, Cᴅ for defendant
- If trial, winner gets judgment J

**Settlement range**: [Plaintiff's expected payoff, Defendant's expected payoff]
- If positive overlap, settlement mutually beneficial (avoid litigation costs)

**Why cases go to trial**:
- **Asymmetric information**: Each side overestimates chance of winning
- **Divergent expectations**: Settlement range empty
- **Agency problems**: Lawyers paid per hour (prefer trial)
- **Reputation/precedent**: Repeat players care about reputation (insurance companies fight to deter future claims)

**Selection bias**: Cases going to trial are ~50-50 (marginal cases). Overwhelming cases settle. **Prediction**: Plaintiff wins ~50% of trials (observed empirically).

### Plea Bargaining

**Sequential game**:
1. Prosecutor offers plea (e.g., plead guilty → 5 years)
2. Defendant accepts or rejects
3. If reject, goes to trial (uncertain outcome)

**Prosecutor's incentive**: Save trial costs, guarantee conviction

**Defendant's incentive**: Reduce sentence, avoid risk of harsh sentence if convicted at trial

**Screening**: Innocents reject, guilty accept (if plea < expected sentence at trial)

**Coercion concern**: If innocent and trial risky (may be wrongly convicted), might plead guilty to avoid worse outcome

**Empirical**: ~95% of US federal cases resolved via plea bargaining

### Negotiations with Outside Options

**BATNA** (Best Alternative to Negotiated Agreement): Outside option if negotiation fails

**Strong BATNA**: High reservation price (minimum acceptable offer) → stronger bargaining position

**Example**: Job offer negotiation
- If have competing offer (strong BATNA), can demand more
- If unemployed with no prospects (weak BATNA), accept lower offer

**Strategy**: Improve BATNA before negotiating (generate competing offers, develop fallback plans)

**First offer advantage** (anchoring):
- First offer sets reference point
- Counteroffers adjusted from anchor
- Aggressive first offer (if justified) can increase final outcome

**Evidence**: Experimental studies show strong anchoring effects even with random anchors.

## Key Terms

- **Mechanism design**: Design rules/institutions achieving desired outcomes with strategic agents
- **VCG mechanism**: Truth-telling dominant strategy, efficient allocation
- **Matching markets**: Pairwise assignment without prices (residents-hospitals, students-schools)
- **Nash bargaining solution**: Axiomatic solution maximizing product of surplus gains
- **Network effects**: Value increases with number of users (direct or indirect/cross-side)
- **Condorcet paradox**: Collective preferences can cycle despite individual transitivity
- **Arrow's Impossibility Theorem**: No voting system satisfies unanimity, IIA, non-dictatorship, transitivity
- **Median voter theorem**: Candidates converge to median voter under single-dimensional policy
- **Deterrence**: Threaten punishment to prevent action (requires capability, resolve, communication)
- **ESS (Evolutionarily Stable Strategy)**: Strategy resisting invasion by mutants
- **Hamilton's rule**: Altruism evolves if rB > C (r=relatedness, B=benefit, C=cost)
- **BATNA**: Best Alternative to Negotiated Agreement (outside option)

## Summary

Mechanism design creates institutions achieving desired outcomes. VCG auctions: Truth-telling dominant strategy, efficient. Matching markets (Gale-Shapley): Stable pairings, strategy-proof for proposing side. Nash/Rubinstein bargaining: First-mover advantage, patient players get more. Platform competition: Two-sided markets, subsidize one side, network effects cause tipping.

Voting: Condorcet paradoxes, strategic voting, Arrow's Impossibility. Median voter theorem holds under restrictive assumptions. Public choice: Politicians maximize votes, special interests prevail (concentrated benefits, dispersed costs). International relations: Deterrence requires credibility (capability, resolve, communication). MAD stability paradox (vulnerability = security). Cuban Missile Crisis: Chicken dynamics. Wars from asymmetric info + commitment problems (Fearon).

Evolution: ESS resists mutant invasion. Hawk-Dove: Mixed ESS if V < C. Sex ratio: Fisher's 1:1 is ESS. Kin selection (Hamilton): Altruism if rB > C. Eusocial insects: High relatedness → worker sterility. Military: Commitment (burn bridges), brinkmanship (push to edge), nuclear deterrence (second-strike survivability = stability).

Negotiations: Litigation vs settlement (asymmetric info causes trials, selection bias → 50-50 plaintiff win rate). Plea bargaining: Screens guilty from innocent, but coerces risk-averse innocents. BATNA determines bargaining power. First offer anchoring. Game theory provides unified framework across economics (auctions, bargaining, mechanism design), politics (voting, deterrence), biology (evolution, cooperation), military (commitment, deterrence), law (litigation, plea bargaining)—revealing common strategic structures beneath superficially different domains.
