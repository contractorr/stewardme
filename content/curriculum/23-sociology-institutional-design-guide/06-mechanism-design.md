# Mechanism Design & Social Engineering

## Overview

Mechanism design is "reverse game theory" — instead of analyzing what agents do given the rules, you design rules to achieve desired outcomes. From auction design to school choice to voting systems to cryptocurrency protocols, mechanism design addresses the fundamental question: how do you create institutions that align individual incentives with collective goals?

The field has profoundly practical applications. Mechanism design determines how spectrum licenses worth billions are allocated, how medical students match to residency programs, how kidneys reach transplant recipients, and how online platforms coordinate buyers and sellers. Understanding mechanism design means understanding how to engineer cooperation and efficiency through institutional rules.

This chapter examines the theoretical foundations (revelation principle, incentive compatibility), major applications (auctions, matching markets, voting), practical successes (spectrum auctions, kidney exchange), and limitations (knowledge problem, unintended consequences, technocracy concerns).

## What is Mechanism Design?

In game theory, you take the rules as given and predict behavior. In mechanism design, you take desired behavior/outcomes as given and ask: what rules produce them?

**Traditional game theory**: Rules → behavior → outcomes
**Mechanism design**: Desired outcomes → design rules → hope agents produce outcomes

### The Revelation Principle

Fundamental insight that simplifies mechanism design enormously. Roger Myerson (Nobel Prize, 2007) formalized it.

**Statement**: Any outcome achievable by any mechanism can also be achieved by a **direct revelation mechanism** where agents truthfully report their private information.

**Implication**: You only need to check whether truthful reporting is an equilibrium in the direct revelation mechanism. Don't need to consider all possible complex mechanisms — just focus on truth-telling.

**Example**: In an auction, instead of designing complex bidding rules, you can restrict attention to mechanisms where bidders simply report their true valuations. If you can't get truth-telling in the direct mechanism, you can't get it with any mechanism.

**Why it works**: Any equilibrium in a complex mechanism can be replicated by having agents report which strategy they would play in the complex mechanism, then having the mechanism simulate the outcome. This is "truth-telling" about strategy choice.

### Incentive Compatibility

A mechanism is **incentive compatible** (IC) if truthful reporting is a best response. Types:

**Dominant strategy IC (DSIC)**: Truth-telling is best regardless of others' strategies. Strongest form. Vickrey auction is DSIC — bid your true value no matter what others do.

**Bayesian IC (BIC)**: Truth-telling is best given beliefs about others' types. Weaker but more flexible. First-price auction isn't DSIC (you should shade your bid below true value) but mechanisms can be designed to be BIC.

**Why IC matters**: If mechanism isn't incentive compatible, agents lie, game the system, expend resources strategizing. You want agents to reveal information truthfully so the mechanism can allocate efficiently.

### Participation Constraints

Beyond IC, mechanisms must satisfy **individual rationality** (IR): agents must prefer participating over not participating. If mechanism can make you worse off than your outside option, you won't participate.

**Types**:
- **Ex-ante IR**: Expected utility from participating ≥ outside option (before knowing type)
- **Interim IR**: Expected utility ≥ outside option (after knowing type, before mechanism runs)
- **Ex-post IR**: Utility ≥ outside option (after mechanism runs, in every possible outcome)

Ex-post IR is strongest, hardest to satisfy. Ex-ante IR is weakest, easiest.

## Auction Design

Auctions are the most successful practical application of mechanism design. Governments use auctions to allocate spectrum, oil leases, timber rights. Companies use auctions for procurement, ad space (Google AdWords), computation (AWS spot instances).

### Common Auction Types

| Type | Rule | Bidder Strategy | Revenue | Efficiency | Information |
|------|------|-----------------|---------|------------|-------------|
| **English (ascending)** | Open bidding, highest wins, pays highest | Bid up to true value | High | High (winner has highest value) | Public (others observe bids) |
| **Dutch (descending)** | Price drops until someone claims | Strategic timing, shade bid | Lower | Moderate | Limited |
| **First-price sealed** | Highest sealed bid wins, pays bid | Shade bid below value | Medium | High (winner likely has highest value) | Private |
| **Vickrey (second-price)** | Highest bid wins, pays second-highest | Bid true value (dominant strategy) | Medium | High (winner has highest value) | Private |

### Vickrey's Insight

William Vickrey (Nobel Prize, 1996): In a second-price auction, bidding your true value is a **dominant strategy**.

**Proof**:
- Suppose your value is $V$
- **Overbidding** ($bid > V$): If second-highest bid is between your true value and your bid, you win but pay more than your value (loss). If second-highest is below your value, overbidding doesn't change outcome. Overbidding can hurt, can't help.
- **Underbidding** ($bid < V$): If second-highest bid is between your bid and true value, you lose when you would have profited (paying second-highest < your value). If second-highest is above your value, underbidding doesn't change outcome (you lose either way). Underbidding can hurt, can't help.
- **Truth-telling** ($bid = V$): You win whenever second-highest < your value (profitable), lose whenever second-highest > your value (avoid loss). Dominant strategy.

**Why this matters**: Bidders don't need to guess others' values or strategies. They just report truth. Mechanism is efficient (highest-value bidder wins) and strategy-proof.

**Real-world use**: eBay uses second-price auctions ("proxy bidding"). Google AdWords originally used generalized second-price auctions. Philately stamp auctions historically used Vickrey format.

### Revenue Equivalence Theorem

Under standard assumptions, all four auction types yield the same expected revenue.

**Assumptions**:
- Bidders are risk-neutral
- Independent private values (your value doesn't depend on others' information)
- Bidders are symmetric (drawn from same distribution)

**Intuition**: What you pay on average equals your expected value conditional on winning, minus your "information rent" (advantage from possibly having low value). This is the same across auction formats.

**Implication**: For revenue, format doesn't matter much under ideal conditions. Choose format based on other criteria (simplicity, speed, transparency, robustness to collusion).

**When it breaks down**:
- **Risk aversion**: Risk-averse bidders bid more aggressively in first-price (paying for sure) than second-price (uncertain payment). First-price generates more revenue.
- **Common values**: If my value depends on others' information (oil field value, company acquisition), winners may overpay ("winner's curse"). English auction reveals information through bidding process, reducing curse.
- **Collusion**: Open ascending auctions vulnerable to bidder rings. Sealed-bid auctions harder to collude in.

### Spectrum Auctions

The FCC's spectrum auctions (starting 1994) are mechanism design's greatest practical triumph. Before auctions, spectrum was allocated through beauty contests (comparative hearings) or lotteries. Both were inefficient and corrupt.

**Designers**: Paul Milgrom and Robert Wilson (Nobel Prize, 2020), Preston McAfee, and others.

**Challenges**:
- **Complementarities**: Bidders want packages of licenses (national coverage requires many regional licenses)
- **Substitutes**: Some licenses are substitutes for others (two licenses in same region)
- **Budget constraints**: Small firms can't bid against giants
- **Strategic behavior**: Bidders may signal, collude, or game the system

**Solution: Simultaneous ascending auction**:
- Multiple licenses bid on simultaneously (not sequentially)
- **Activity rules**: Must bid actively or lose eligibility (prevents "wait and see")
- **Information revelation**: Bidding is public, allowing price discovery
- **Combinatorial bidding** (later versions): Bid on packages of licenses
- **Anonymous bidding** (some versions): Reduces signaling and collusion

**Results**:
- **Revenue**: Raised $100+ billion for US government (1994-2020)
- **Efficiency**: Licenses went to highest-value users
- **Speed**: Allocated thousands of licenses in weeks vs years of hearings
- **Global adoption**: 100+ countries now use spectrum auctions

**Complications**:
- **Strategic bidding**: Bidders found ways to signal (using last digits of bids to coordinate)
- **Demand reduction**: Bidders shade bids to avoid paying high prices
- **Budget constraints**: Small firms still struggle against large firms
- **Combinatorial complexity**: Package bidding computationally hard

Despite challenges, spectrum auctions are a massive success. Mechanism design moved from theory to billions of dollars of practical impact.

## Matching Markets (Roth)

Alvin Roth (Nobel Prize, 2012) applied mechanism design to matching — markets where prices don't work. Can't pay for kidneys, medical residencies aren't priced, school choice shouldn't depend on ability to pay. Yet these resources must be allocated. How?

### The Problem

**Decentralized matching fails**:
- **Unraveling**: Offers made earlier and earlier (medical residencies offered 2 years before graduation)
- **Congestion**: Too many offers to evaluate simultaneously
- **Exploding offers**: Accept immediately or lose opportunity (coercive)
- **Instability**: Students and residencies prefer other matches to what they got

### Gale-Shapley Deferred Acceptance Algorithm

David Gale and Lloyd Shapley (Nobel Prize, 2012 posthumously to Shapley) designed an algorithm producing stable matchings.

**Problem**: Match students to schools (or residents to hospitals, workers to firms).

**Algorithm** (student-proposing version):
1. Each student proposes to their top-choice school
2. Each school tentatively accepts its best applicant(s) (up to capacity), rejects rest
3. Rejected students propose to next choice
4. Schools hold best offers so far, reject newly dominated offers
5. Repeat until no rejections

**Terminates**: Students run out of schools to propose to (finite process)

**Properties**:
1. **Stable**: No student-school pair prefers each other to their assigned match. If student S prefers school T to their match, then T rejected S for better applicants and prefers them to S.
2. **Student-optimal**: Produces the best stable matching for students among all stable matchings. Every student gets their favorite school among all schools they could be matched to in *any* stable matching.
3. **Strategy-proof for students**: Truthfully reporting preferences is a dominant strategy (can't benefit by lying about preferences).
4. **School-pessimal**: Produces worst stable matching for schools (but still better than unstable matchings).

**Example**:
- Students: A, B, C
- Schools: X, Y, Z (each capacity 1)
- Student preferences: A: X>Y>Z, B: Y>X>Z, C: X>Y>Z
- School preferences: X: C>A>B, Y: A>B>C, Z: A>B>C

**Run algorithm**:
- Round 1: A→X, B→Y, C→X. X tentatively accepts C (rejects A). Y accepts B.
- Round 2: A→Y. Y rejects B (prefers A). B→X. X rejects B (prefers C).
- Round 3: B→Z. Z accepts B.
- **Result**: A-Y, B-Z, C-X. Stable.

### Applications

**National Resident Matching Program (NRMP)**: Medical residency matching in US since 1952. Originally used student-proposing algorithm. Problem: Couples want to match to same city. 1997: Redesigned using Roth's modifications handling couples (computationally complex). Now ~40,000 residents matched annually.

**School choice**: Boston, New York City, and others use deferred acceptance for public school assignment. Before: Immediate acceptance (parents ranked schools; schools immediately accepted/rejected). Problem: Gaming (parents didn't list true first choice if unlikely to get in). New: Deferred acceptance makes truth-telling incentive-compatible.

**Kidney exchange**: Roth's design enables paired kidney donations. Patient A needs kidney, Donor A incompatible. Patient B needs kidney, Donor B incompatible with B but compatible with A, and Donor A compatible with B. **Swap**: A→B, B→A. Both patients get kidneys.

**Complexity**: Can extend to 3-way, 4-way, even longer chains. Non-directed donors (altruistic strangers) can start chains: Altruistic donor → Patient 1 (Donor 1 incompatible) → Donor 1 → Patient 2 (Donor 2 incompatible) → Donor 2 → Patient 3... Chains of 20+ transplants have occurred.

**Results**: From ~0 kidney exchanges in 2000 to ~1,000/year in US by 2020. Thousands of lives saved. Roth's algorithm deployed through National Kidney Registry and other organizations.

### Why Matching Markets Are Different

**No prices**: Can't use market-clearing prices for kidneys, residencies, school slots (ethical/legal constraints). Must allocate without prices.

**Two-sided**: Both sides have preferences (students choose schools, schools choose students). Unlike auctions where goods don't have preferences.

**Congestion**: Can't make everyone wait indefinitely to evaluate all options. Need timely decisions.

**Thickness**: Need many participants simultaneously for good matching (thin markets don't find good matches).

**Stability matters**: Unstable matchings unravel (matched parties defect to form better matches outside system).

## Voting Systems

Voting systems are mechanisms for aggregating preferences into collective decisions.

| System | Method | Pros | Cons | Used Where |
|--------|--------|------|------|------------|
| **Plurality** | Most first-choice votes wins | Simple, decisive | Spoiler effect, minority winners, strategic voting | US (mostly), UK, Canada |
| **Ranked-choice (IRV)** | Eliminate last place iteratively, redistribute votes | Reduces spoilers, allows sincere ranking | Complex count, non-monotonic, can still have spoilers | Australia, San Francisco, Maine |
| **Approval** | Vote for as many as you approve, most votes wins | Simple, less strategic than plurality | Doesn't capture preference intensity well | Some professional societies, US political reformers propose |
| **Condorcet** | Winner beats all others head-to-head | Majority preferred if exists | May not exist (Condorcet paradox), complex count | Academic interest, rarely used |
| **Borda count** | Points for rank (n-1 points for 1st, n-2 for 2nd, etc.) | Considers full ranking, rewards consensus | Vulnerable to strategic manipulation, irrelevant alternatives matter | Some European contexts |
| **Score/Range** | Rate each candidate 0-10, highest average wins | Allows intensity expression, less strategic | Unfamiliar to voters | Some online platforms |

### Arrow's Impossibility Theorem

Kenneth Arrow (1951, Nobel Prize 1972): No ranked voting system with ≥3 candidates satisfies all fairness criteria simultaneously.

**Conditions**:
1. **Unanimity/Pareto efficiency**: If everyone prefers A to B, A ranks above B
2. **Independence of irrelevant alternatives** (IIA): Ranking of A vs B shouldn't depend on C's presence
3. **Non-dictatorship**: No single voter determines the outcome
4. **Transitivity**: If A > B and B > C, then A > C (social preferences are coherent)
5. **Unrestricted domain**: Any pattern of individual preferences is allowed

**Result**: Impossible to satisfy all five simultaneously (given 3+ candidates).

**Implication**: All voting systems with ≥3 candidates are imperfect. No aggregation of preferences perfectly represents the "will of the people." This is a fundamental limit on democracy, not a design flaw to be fixed. Must accept tradeoffs.

**What gets violated**: Most systems violate IIA. Plurality, IRV, Borda all fail IIA (adding/removing candidate changes outcome between others). Approval violates unanimity in edge cases. Only dictatorship satisfies all conditions.

### Gibbard-Satterthwaite Theorem

Allan Gibbard (1973) and Mark Satterthwaite (1975): Any non-dictatorial voting system with ≥3 candidates is susceptible to strategic voting (voting insincerely to achieve a better outcome).

**Implication**: Can't design a voting rule that's both democratic and strategy-proof. Either someone dictates, or people have incentives to lie about preferences.

**Example (plurality voting)**:
- True preferences: 35% A>B>C, 33% B>C>A, 32% C>B>A
- **Sincere**: A wins (35% > 33% > 32%)
- **Strategic**: The 32% who prefer C>B>A realize C can't win, so they vote B. B wins (65% vs 35%).
- Insincere voting produces better outcome for strategic voters.

**Practical implication**: Voters must think strategically. "Who can win?" matters as much as "Who do I prefer?" This explains why third parties struggle (rational voters abandon them to avoid "wasting" votes).

## Market Design

Roth's broader concept: **market design** applies mechanism design to real-world problems where prices don't clear markets.

### Repugnant Markets

Michael Sandel: Some things "money can't buy" — not because of scarcity but ethics. Organs, babies, votes, grades, draft deferments, jury verdicts.

**Result**: Can't use prices to allocate. But resources are scarce and must be allocated. Mechanism design creates non-price allocation systems that are still efficient.

**Examples**:
- **Kidneys**: Illegal to buy/sell (National Organ Transplant Act, 1984). Allocation through matching algorithms + waiting lists + priority rules.
- **School admissions**: Can't sell admission slots (illegal, but wealthy still have advantages through tutoring, legacy preferences, "donations"). Public schools use catchment areas or matching algorithms.
- **Immigration**: Can't sell citizenship (though investor visas exist). Allocation through rules (family reunification, employment sponsorship, diversity lottery).

### Two-Sided Platforms

Platforms (Uber, Airbnb, Amazon, eBay) are designed markets connecting two sides:

**Design elements**:
1. **Matching algorithms**: Connect supply and demand (Uber drivers and riders, Airbnb hosts and guests)
2. **Pricing**: Platform sets prices or facilitates negotiation. Often subsidizes one side to attract it (riders get discounts, drivers pay fees).
3. **Trust mechanisms**: Ratings, reviews, verified accounts, insurance, dispute resolution. Solve information asymmetry.
4. **Governance**: Rules for participation, moderation, conflict resolution. Platform acts as private regulator.
5. **Network effects**: More users on each side attract more on the other (cross-side network effects). Creates winner-take-all dynamics.

**Example: Uber**:
- **Matching**: Algorithm assigns nearby driver to rider (minimizes wait time, maximizes matches)
- **Pricing**: Surge pricing adjusts to balance supply/demand. Higher prices during high demand attract more drivers, ration riders.
- **Trust**: Two-way ratings (riders rate drivers, drivers rate riders). Low-rated users kicked off platform.
- **Governance**: Background checks, insurance, community guidelines, appeals process
- **Network effects**: More drivers → lower wait times → more riders → more demand → attracts more drivers

**Challenges**:
- **Chicken-and-egg**: How to get both sides simultaneously? Often subsidize one side initially.
- **Power imbalances**: Platform can exploit participants (Amazon squeezing sellers, Uber lowering driver pay). Who governs the governors?
- **Regulation**: Platforms claim to be neutral intermediaries but shape markets through algorithmic rules. Should they be regulated like traditional firms?

## Nudge Theory (Thaler & Sunstein)

Richard Thaler (Nobel Prize, 2017) and Cass Sunstein: **Libertarian paternalism** — design choice environments to steer people toward better decisions while preserving freedom to choose otherwise.

**Core insight**: Choice architecture matters. How choices are presented affects decisions. Designers can nudge toward better outcomes without coercion.

### Key Nudges

| Nudge Type | Mechanism | Example | Evidence | Why It Works |
|-----------|-----------|---------|----------|--------------|
| **Default** | Most people stick with default option | Opt-out organ donation (Austria: 99% vs Germany: 12% opt-in) | Massive effect in organ donation, retirement savings | Inertia, implicit endorsement, avoiding decision |
| **Salience** | Make information visible and comprehensible | Calorie counts on menus (reduced calorie consumption 3-15%) | Modest effect on consumption | Attention, awareness |
| **Social proof** | Show what others do (descriptive norms) | "Most guests reuse towels" (increased reuse 10-30%) | Moderate effect | Conformity, information about appropriate behavior |
| **Simplification** | Remove friction and complexity | Pre-filled tax forms (increased filing), simplified financial aid (increased college enrollment) | Large effect on participation | Reduces cognitive costs, saves time |
| **Commitment device** | Lock in future behavior | Save More Tomorrow (auto-escalating savings increased participation 78% → 98%) | Large effect | Binds future self, exploits present bias |
| **Feedback** | Show consequences of behavior | Energy usage compared to neighbors (reduced consumption 2-3%) | Small but sustained effect | Social comparison, motivation |
| **Framing** | Emphasize gains vs losses | "Save $100/year" vs "Lose $100/year" (loss frame more effective) | Moderate effect | Loss aversion |
| **Anchoring** | Provide reference points | Suggest donation amounts ($50, $100, $200 vs $25, $50, $100) | Large effect on donation size | Initial value anchors judgment |

### Save More Tomorrow

Behavioral economics' greatest practical success. Designed by Thaler and Shlomo Benartzi.

**Problem**: People undersave for retirement. Standard economic advice: Save more now. But present bias, self-control problems prevent it.

**Solution**: Commit to save *more later* (from future raises).
1. Workers choose to participate (no coercion)
2. Contribution increases occur with future pay raises (painless — take-home pay doesn't fall)
3. Auto-escalation continues until hitting cap or worker opts out
4. Easy to opt out anytime (preserving freedom)

**Results**: Participation increased from 78% to 98%. Average savings rates tripled (3.5% to 11.6%). Workers wealthier at retirement without feeling constrained in present.

**Adoption**: Used by major employers. Inspired auto-enrollment and auto-escalation features in 401(k) plans. Pension Protection Act (2006) encouraged adoption.

### Critiques of Nudging

**Manipulation**: Who decides what's "better"? Nudges serve designers' preferences, not necessarily subjects'. Organ donation opt-out assumes donating is better — but what if you disagree?

**Slippery slope**: Nudges may become coercion. "Libertarian" paternalism may lose "libertarian" part. Easy to opt out today; harder tomorrow?

**Knowledge problem** (Hayek): Designers don't know what's best for individuals. Central planner designing choice architecture faces same problem as central planner setting prices — lacks local, tacit knowledge.

**Sludge** (Sunstein's later concept): Friction deliberately designed to prevent choices. Canceling subscriptions is hard (complex process, phone call required, retention specialists pressure you). Claiming benefits is hard (complex forms, documentation requirements). This is "dark nudging" — using choice architecture against people's interests.

**Effectiveness limits**: Nudges have small to moderate effects. Can't solve major problems through nudges alone (won't solve retirement crisis or obesity epidemic with menu calorie counts). May distract from structural reforms (easier to nudge than pass legislation).

**Heterogeneity**: One-size-fits-all nudges may harm some while helping others. Calorie counts help some people diet but trigger eating disorders in others.

## Constitutional Design as Mechanism Design

Constitutions are mechanisms — rules designed to produce desired political outcomes given self-interested politicians and citizens.

**Separation of powers**: Creates checks and balances by giving each branch incentive to resist encroachment by others. Executive wants power; legislature wants power; judiciary wants independence. Each checks the others not from public spiritedness but self-interest. Madison: "Ambition must be made to counteract ambition."

**Federalism**: Competition among jurisdictions incentivizes good governance. Tiebout: "voting with your feet" — citizens move to jurisdictions matching their preferences. States compete for residents/businesses by offering better services or lower taxes. Creates discipline similar to market competition.

**Independent judiciary**: Insulating judges from political pressure (life tenure, salary protection) enables credible commitment to rule of law. Politicians can't threaten judges who rule against them. Makes constitutional constraints credible.

**Electoral systems**: Different systems produce different party structures:
- **Duverger's Law**: Plurality voting (first-past-the-post) → two parties. Voters abandon third parties to avoid "wasting" votes. US exemplifies.
- **Proportional representation** → multiparty systems. Votes translate proportionally to seats; small parties viable. Most European countries.

**Bicameralism**: Two legislative chambers can represent different constituencies (House = population, Senate = states) and slow hasty legislation (requires passage in both chambers). Creates additional veto point reducing policy volatility but potentially creating gridlock.

**Supermajority requirements**: Some decisions require more than 50%+1 (constitutional amendments typically require 2/3 of legislatures + 3/4 of states in US). Protects minority rights, ensures broad consensus, but creates status quo bias.

## Critique: Limits of Design

### Hayek's Knowledge Problem

F.A. Hayek: Central designers lack the distributed, tacit knowledge held by millions of individuals. Markets aggregate this knowledge through prices — millions of decentralized decisions produce emergent order.

**Implication**: Designed mechanisms may be less efficient than evolved institutions. Markets, common law, cultural norms evolved without top-down design but often work well. Designers' hubris risks disrupting what works.

**Response**: Some problems require coordination that markets can't provide (public goods, externalities, market failures). Mechanism design addresses these. Also, evolved institutions may be adapted to past environments, not current ones.

### Unintended Consequences

Every intervention changes incentives in unpredictable ways. Designed mechanisms may produce:

**Gaming**: Participants exploit rules in unintended ways. Teachers teach to tests when test scores determine funding. Welfare recipients structure behavior to maintain eligibility. Bankers exploit regulations through loopholes.

**Crowding out**: External incentives destroy intrinsic motivation. Paying children to read may make reading feel like work, reducing reading for pleasure. Fines for late daycare pickup made parents arrive later (converted moral obligation to price).

**Complexity**: More rules → more loopholes → more rules to close loopholes → complexity spirals. Tax code is 70,000+ pages because every attempted simplification creates new exploits.

**Rigidity**: Designed systems may not adapt to changing conditions. Constitutions designed for 18th century may not suit 21st century. Rules optimized for one environment fail in another.

**Cobra effects**: Incentives cause opposite of intended effect (bounty for cobras → cobra farming → more cobras).

### Technocracy Concerns

Mechanism design assumes designers know the right objectives. But who decides what outcomes are "desirable"? Designing institutions concentrates power in designers' hands.

**Concerns**:
- **Democratic legitimacy**: Should unelected experts design social rules? Or should democratic processes decide?
- **Value conflicts**: Efficiency isn't the only value. Fairness, equality, liberty, community matter too. Mechanism designers may optimize one dimension while ignoring others.
- **Capture**: Who designs the designers? Powerful interests may shape mechanism design to serve their interests (regulatory capture at meta-level).

**Response**: Mechanism design should inform democratic deliberation, not replace it. Designers provide options; democratic processes choose among them. Transparency and accountability essential.

## Key Terms

- **Mechanism Design**: Designing rules to achieve desired outcomes; "reverse game theory"
- **Incentive Compatibility**: Truthful reporting is a best strategy (DSIC = dominant strategy, BIC = Bayesian)
- **Revelation Principle**: Any mechanism outcome achievable via truthful direct revelation mechanism
- **Vickrey Auction**: Second-price sealed bid — truth-telling is dominant strategy; efficient allocation
- **Revenue Equivalence**: Under standard assumptions, auction formats yield equal revenue
- **Gale-Shapley Algorithm**: Deferred acceptance producing stable matchings
- **Stable Matching**: No unmatched pair prefers each other to assigned matches
- **Strategy-Proof**: Can't benefit from lying about preferences
- **Nudge**: Choice architecture steering toward better decisions while preserving freedom
- **Libertarian Paternalism**: Designing helpful defaults while allowing opt-out (Thaler & Sunstein)
- **Market Design**: Applying mechanism design where prices don't clear markets (Roth)
- **Knowledge Problem**: Central designers lack distributed, tacit knowledge (Hayek)
- **Arrow's Impossibility**: No voting system satisfies all fairness criteria with 3+ candidates
- **Gibbard-Satterthwaite**: All non-dictatorial voting rules manipulable (strategic voting possible)
- **Separation of Powers**: Constitutional mechanism creating checks via competing interests
- **Two-Sided Platform**: Market connecting two sides with network effects (Uber, Airbnb)

## Summary

Mechanism design is reverse game theory — designing rules to produce desired outcomes. The revelation principle simplifies analysis: focus on truth-telling in direct mechanisms. Incentive compatibility makes truth-telling optimal; participation constraints ensure agents prefer participating.

Auction theory shows that truthful bidding can be incentive-compatible (Vickrey). Revenue equivalence says format matters less than expected under ideal conditions. Spectrum auctions ($100+ billion allocated efficiently) demonstrate practical success. Milgrom and Wilson's simultaneous ascending auction design solved complementarities, information revelation, and strategic behavior challenges.

Matching algorithms (Gale-Shapley deferred acceptance) produce stable outcomes without prices. Applications include medical residencies (40,000 matched annually), school choice (truth-telling made dominant strategy), and kidney exchange (1,000+ transplants yearly). Roth's work shows market design succeeds where prices fail or are ethically unacceptable.

Voting systems all involve tradeoffs. Arrow's impossibility theorem proves no system satisfies all fairness criteria. Gibbard-Satterthwaite shows all systems are manipulable (strategic voting). Plurality has spoilers, IRV is non-monotonic, Condorcet may not exist, Borda is manipulable. Must accept imperfection and choose carefully.

Nudge theory designs choice architectures leveraging behavioral biases. Defaults, salience, social proof, simplification, commitment devices, and feedback steer toward better choices while preserving freedom. Save More Tomorrow increased retirement savings massively through auto-escalation from future raises. But nudges face critiques: manipulation, knowledge problem, effectiveness limits, sludge.

Constitutional design is mechanism design: separation of powers uses ambition to counteract ambition; federalism creates competitive discipline; independent judiciary enables credible commitment; electoral systems shape party structures. But mechanism design faces limits: Hayek's knowledge problem (designers lack distributed information), unintended consequences (gaming, crowding out, complexity, rigidity), and technocracy concerns (who decides what's desirable?).

The best institutions often combine designed and evolved elements. Markets evolved but require legal infrastructure (contract enforcement, property rights) that must be designed. Mechanism design provides tools for engineering cooperation and efficiency, but must be applied with humility about the limits of design and the value of emergent order.
