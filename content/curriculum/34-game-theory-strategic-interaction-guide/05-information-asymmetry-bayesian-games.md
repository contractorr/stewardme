# Information Asymmetry & Bayesian Games

## Incomplete Information

**Complete information**: Payoff functions common knowledge (all players know structure, all know that all know, ad infinitum)

**Incomplete information**: Players have private information (types, valuations, costs) unknown to others

**Examples**:
- Auctions: Bidders know own valuation, not others'
- Insurance: Insured knows health status (risk type)
- Employment: Worker knows ability, employer doesn't
- Poker: Players know own cards, not opponents'
- Negotiations: Each side knows own reservation price

**Harsanyi transformation** (John Harsanyi, 1967-68): Convert incomplete information game to imperfect information game by introducing "Nature" as player who assigns types according to common prior beliefs.

## Bayesian Nash Equilibrium

**Setup**:
- Each player i has type θᵢ drawn from set Θᵢ according to distribution p(θᵢ)
- Type θᵢ is private information (player knows own type, others don't)
- **Common prior**: Distribution p(θ) common knowledge

**Strategy**: Function sᵢ(θᵢ) mapping type to action

**Bayesian Nash Equilibrium (BNE)**: Strategy profile s* = (s₁*, ..., sₙ*) such that each type of each player maximizes expected payoff given beliefs about others' types and strategies:

```
s*ᵢ(θᵢ) ∈ argmax E[uᵢ(sᵢ, s*₋ᵢ(θ₋ᵢ), θᵢ, θ₋ᵢ) | θᵢ]
```

Expected value taken over distribution of opponents' types θ₋ᵢ.

**Interpretation**: Each type plays best response to distribution of opponents' actions (determined by their types and strategies).

**Example: First-Price Sealed-Bid Auction**

n bidders, each has private valuation vᵢ ∈ [0, 1] drawn independently from uniform distribution.

Bidder i submits bid bᵢ. Highest bidder wins, pays own bid. Payoff:
- Win: vᵢ - bᵢ
- Lose: 0

**Symmetric BNE**: All bidders use same strategy b(v)

**Derivation** (n = 2 case):

Bid function: b(v) = αv (linear strategy, solve for α)

Bidder 1 with value v₁ maximizes:
```
max Pr(win) × (v₁ - b₁)
 b₁

= Pr(b₁ > b₂) × (v₁ - b₁)
= Pr(b₁ > αv₂) × (v₁ - b₁)
= Pr(v₂ < b₁/α) × (v₁ - b₁)
= b₁/α × (v₁ - b₁)  [since v₂ uniform on [0,1]]
```

FOC:
```
(v₁ - b₁)/α - b₁/α = 0
v₁ - 2b₁ = 0
b₁ = v₁/2
```

**BNE**: Bid half your valuation, b*(v) = v/2

**General n bidders**: b*(v) = [(n-1)/n]v (bid increasingly aggressive fraction as more bidders)

**Revenue**: Expected revenue ≈ E[max{v₁,...,vₙ}] × (n-1)/n

## Signaling Games

**Structure**:
1. Nature draws Sender's type θ ∈ Θ according to prior p(θ)
2. Sender observes θ, chooses signal/action s ∈ S
3. Receiver observes s (not θ), chooses response r ∈ R
4. Payoffs: uₛ(θ, s, r) for Sender, uᵣ(θ, s, r) for Receiver

**Key**: Sender has private information, uses signal to communicate (credibly or not)

**Perfect Bayesian Equilibrium (PBE)**: Refinement of BNE for dynamic games
- **Strategies**: s*(θ) for Sender, r*(s) for Receiver
- **Beliefs**: μ(θ|s) = Receiver's posterior belief about type after observing signal s
- **Requirements**:
  1. **Sequential rationality**: Strategies are best responses given beliefs
  2. **Consistent beliefs**: Bayes' rule applied where possible

### Job Market Signaling (Spence, 1973)

**Setup**:
- Worker has ability θ ∈ {H, L} (high or low), privately known
- Worker chooses education level e ≥ 0 (signal)
- Firm observes e, offers wage w(e)
- Productivity: θ (education doesn't increase productivity, just signals)
- Education cost: c(e, θ) with cₑ > 0 (costly), cₑₜ < 0 (lower cost for high type—single-crossing condition)

**Example**: c(e, H) = e, c(e, L) = 2e (high type finds education half as costly)

**Payoffs**:
- Worker: w(e) - c(e, θ)
- Firm: θ - w (profit)

**Separating equilibrium**: High and low types choose different education levels → Firm infers type perfectly

**Candidate equilibrium**:
- High type: e*_H
- Low type: e*_L = 0
- Firm: w(e ≥ e*_H) = H, w(e < e*_H) = L

**Incentive compatibility**:

Low type doesn't want to mimic high type:
```
L - 0 ≥ H - 2e*_H
H - L ≤ 2e*_H
e*_H ≥ (H - L)/2
```

High type doesn't want to mimic low type:
```
H - e*_H ≥ L - 0
e*_H ≤ H - L
```

**Equilibrium exists if** (H - L)/2 ≤ e*_H ≤ H - L

Any e*_H in this range supports separating equilibrium. **Multiple equilibria**—coordination problem.

**Least-cost separating equilibrium**: e*_H = (H - L)/2 (minimizes wasteful signaling)

**Welfare**:
- High types: Get high wage but waste resources on education
- Low types: Paid true productivity
- **Inefficiency**: Education costly but doesn't increase productivity (pure signal)

**Pooling equilibrium**: Both types choose same education → no information conveyed → both paid expected productivity E[θ]. May exist depending on off-equilibrium beliefs.

### Costly Signaling in Nature

**Zahavi's handicap principle**: Exaggerated traits (peacock's tail) signal genetic quality precisely because costly

**Peacock's tail**:
- Costly to grow, reduces mobility (predation risk)
- Only healthy males can afford large tail
- Females select mates by tail size → signals genetic fitness
- Honest signal: Unhealthy males cannot fake (too costly)

**Alarm calls** (ground squirrels):
- Costly (attracts predator attention)
- Signals: "I'm vigilant, healthy, can escape" → deters predator
- Also warns kin (kin selection component)

**Stotting** (gazelles):
- Jumping high when predator nearby
- Costly (energy, time)
- Signals: "I'm fast/healthy, don't bother chasing"
- Predators often abandon chase after observing stotting

**General principle**: For signal to be credible, must be differentially costly (high-quality types find signal less costly than low-quality types—single-crossing property).

## Screening

**Screening**: Uninformed party designs menu to induce informed party to reveal information via self-selection

**Example: Insurance Contracts**

**Setup**:
- Customers have private information about risk type: θ ∈ {H, L} (high-risk, low-risk)
- Proportion p high-risk, 1-p low-risk
- Insurer doesn't observe type, offers menu of contracts

**Contract**: (Premium P, Coverage Q) where Q ∈ [0, 1] (fraction of loss covered)

**Pooling contract**: Single contract for all types
- Adverse selection: High-risk types more likely to buy → raises costs → premiums increase → low-risk types drop out ("death spiral")

**Separating contracts**: Menu designed so types self-select
- High coverage, high premium (attractive to high-risk)
- Low coverage, low premium (attractive to low-risk)

**Rothschild-Stiglitz equilibrium** (1976):
- High-risk get full insurance at actuarially fair price (for high-risk)
- Low-risk get partial insurance at actuarially fair price (for low-risk)
- Low-risk would prefer full insurance but constrained (otherwise high-risk would mimic)
- **Incentive compatibility** binds for high-risk type

**No cross-subsidization**: Each type pays according to own risk. Competitive market ensures zero profit.

**May not exist**: In some parameter ranges, no pure-strategy equilibrium (Wilson, Miyazaki, others explored alternatives).

### Screening in Labor Markets

**Employer screens workers** via job requirements, wages, contracts

**Example: Educational requirements**
- Require degree for job (doesn't teach necessary skills)
- High-ability workers find degree easier to obtain
- Self-selection: High-ability get degree, low-ability don't
- Employer infers ability from degree

**Efficiency wage**: Pay above market-clearing
- Attracts higher-quality applicants
- Reduces turnover (workers don't want to lose good job)
- Incentivizes effort (monitoring incomplete)

## Auctions

**Common value vs private value**:
- **Private value**: Each bidder knows own value (art for personal consumption)
- **Common value**: True value same for all, but estimates differ (oil field, company acquisition)
- **Affiliated values**: Mixture (value depends on own taste + objective quality)

### Auction Formats

| Format | Description | Strategic Behavior |
|--------|-------------|-------------------|
| **First-price sealed-bid** | Highest bid wins, pays own bid | Shade bid below value (trade off win probability vs surplus) |
| **Second-price sealed-bid (Vickrey)** | Highest bid wins, pays second-highest bid | Bid true value (dominant strategy) |
| **English (ascending)** | Open bidding, price rises until one bidder remains | Similar to second-price in private-value settings |
| **Dutch (descending)** | Price starts high, falls until someone accepts | Strategically equivalent to first-price sealed-bid |

### Vickrey Auction (Second-Price)

**Mechanism**:
- Each bidder submits sealed bid bᵢ
- Highest bidder wins, pays second-highest bid

**Theorem**: Bidding true valuation is dominant strategy.

**Proof**:
Let vᵢ = your valuation, b₋ᵢ = max of others' bids

Case 1: bᵢ > b₋ᵢ (you win)
- Pay b₋ᵢ
- Payoff: vᵢ - b₋ᵢ if vᵢ > b₋ᵢ, negative otherwise
- Bidding bᵢ < vᵢ: Risk losing if b₋ᵢ ∈ (bᵢ, vᵢ) → foregoes positive surplus
- Bidding bᵢ > vᵢ: Risk winning if b₋ᵢ ∈ (vᵢ, bᵢ) → forces negative payoff

Case 2: bᵢ < b₋ᵢ (you lose)
- Payoff: 0
- Bidding higher/lower doesn't help (either still lose, or win but pay more than value)

**Conclusion**: Truthful bidding optimal regardless of others' bids (dominant strategy).

**Revenue Equivalence Theorem** (Myerson, 1981; Riley & Samuelson, 1981):
In private-value auctions with symmetric bidders, any mechanism that:
1. Allocates to highest valuation bidder, and
2. Charges zero to losers
generates same expected revenue.

**Implication**: First-price, second-price, English, Dutch auctions all yield same expected revenue (though strategic complexity differs).

### Winner's Curse

**Common-value auctions**: Winner likely overestimated value (most optimistic bidder wins)

**Example**: Oil lease auction
- True value V unknown
- Each bidder receives signal sᵢ = V + εᵢ (noise)
- Signals independent, mean zero noise
- Naive bidding (bid = sᵢ) → winner has highest signal → highest positive error → pays more than V on average

**Rational bidding**: Condition estimate on winning (shade bid)
- If I win with signal sᵢ, what does that tell me about V?
- Winning means all others' signals < sᵢ → V likely below my signal
- Optimal bid: b(sᵢ) < sᵢ (shade)

**Empirical evidence**:
- M&A: Acquirers often destroy shareholder value (overpay)
- Book publishing: Rights auctions for unknown authors (winners often lose money)
- Baseball free agency: Teams bidding for players (winners overpay)

**Mitigation**: Experience (learn to shade), structural remedies (common ownership to internalize externalities).

## Cheap Talk

**Cheap talk**: Communication without direct payoff consequences (costless, non-binding)

**Crawford-Sobel model** (1982):

- Sender has private information θ ∈ [0, 1]
- Sender sends message m (costless, not verified)
- Receiver chooses action a ∈ ℝ
- Payoffs:
  - Sender: -(a - θ - b)² (wants action a = θ + b; bias b)
  - Receiver: -(a - θ)² (wants action a = θ; unbiased)

**Bias b**: Sender prefers higher action than Receiver

**Fully revealing equilibrium**: Sender reports θ truthfully, Receiver sets a = θ

**Incentive compatibility**: For type θ to report truthfully when Receiver will set a = θ:
```
Sender's payoff from truth: -(θ - θ - b)² = -b²
Sender's payoff from claiming θ': -(θ' - θ - b)²
```

For truth to be optimal for all θ: -b² ≥ -(θ' - θ - b)² for all θ'

**Impossible if b ≠ 0**: Sender always wants to inflate report (push action upward by b).

**Equilibrium**: Partial revelation (finite partition)
- Interval types pool on same message
- Number of intervals decreases with bias b
- As b → 0, approaches full revelation
- As b → ∞, babbling equilibrium (messages uninformative)

**Applications**:
- **Expert advice**: Biased expert (investment advisor with commissions) → advice less informative
- **Political communication**: Politician's speech (cheap talk) → voters skeptical
- **Management-worker**: Manager's encouragement (biased toward effort) → partially informative

**Credibility enhancements**:
- Costly signals (warranties, certifications)
- Reputation (repeated interactions)
- Third-party verification (audits)

## Applications

### Lemon's Problem (Akerlof, 1970)

**Used car market**:
- Sellers know quality: Good (value $5k) or Lemon (value $2k)
- Buyers don't observe quality before purchase
- Proportion p good cars

**Buyer's willingness to pay**: p·$5k + (1-p)·$2k

**If p = 0.5**: Buyers pay $3.5k

**Problem**: Good car owners won't sell for $3.5k (value $5k) → only lemons sold → buyers learn → willing to pay only $2k

**Adverse selection**: Asymmetric information drives high-quality out of market

**Solutions**:
- **Warranties**: Costly for lemons, cheaper for good cars → separates types
- **Reputation**: Dealers stake reputation on quality
- **Certification**: Third-party inspection (Carfax, mechanical inspection)

### Corporate Finance: Pecking Order

**Myers & Majluf** (1984): Managers have private information about firm value

**Implications**:
- **Equity issuance**: Negative signal (managers issue equity when overvalued) → stock price drops
- **Pecking order**: Prefer internal funds > debt > equity
- **Underinvestment**: May forgo positive-NPV projects if require equity issuance (dilution too costly)

**Evidence**: Equity issues followed by negative abnormal returns (stock price decline). Supports adverse selection story.

### Political Communication

**Campaign promises**: Cheap talk (non-binding)

**Credibility mechanisms**:
- **Reputation**: Past promise-keeping
- **Pandering**: Say what voters want (pooling), but uninformative
- **Signaling via actions**: Costly campaign investments signal commitment

**Median voter theorem**: In single-dimensional policy space, candidates converge to median voter's preference. But holds only under complete information. With asymmetric information about candidates' types, divergence possible (candidates signal ideology to base).

## Key Terms

- **Incomplete information**: Players have private information (types) unknown to others
- **Complete information**: Payoff structure common knowledge
- **Bayesian Nash Equilibrium (BNE)**: Each type maximizes expected payoff given beliefs
- **Signaling game**: Sender has private info, sends costly signal; Receiver responds
- **Screening**: Uninformed party designs menu to induce self-selection
- **Perfect Bayesian Equilibrium (PBE)**: BNE + consistent beliefs via Bayes' rule
- **Separating equilibrium**: Different types choose different actions
- **Pooling equilibrium**: All types choose same action
- **Single-crossing condition**: High type finds signal less costly (enables separation)
- **Adverse selection**: Asymmetric info causes low-quality types to dominate market
- **Winner's curse**: Highest bidder likely overestimated value (common-value auctions)
- **Cheap talk**: Costless, non-binding communication

## Summary

Incomplete information: Players have private types (valuations, costs, abilities) unknown to others. Bayesian Nash Equilibrium: Each type maximizes expected payoff given beliefs about opponents' types. First-price auction BNE: Bid below value (shade), b*(v) = [(n-1)/n]v for n bidders. Signaling games: Sender privately informed, sends costly signal; Receiver infers type and responds. Spence job market signaling: Education separates high/low ability (single-crossing: high types find education cheaper) → wasteful but informative. Costly signaling in nature: Peacock's tail, stotting (handicap principle—only healthy types afford signal).

Screening: Uninformed party designs menu inducing self-selection. Insurance: High-risk get full coverage (high premium), low-risk get partial coverage (low premium)—separating equilibrium prevents adverse selection. Auctions: Vickrey (second-price) has dominant strategy (bid true value). Revenue Equivalence: First/second-price, English/Dutch yield same expected revenue under standard assumptions. Winner's curse: Common-value auctions require shading (condition on winning → infer overestimation).

Cheap talk (Crawford-Sobel): Costless communication → partially revealing equilibrium (bias limits information transmission). Adverse selection (Akerlof lemons): Asymmetric info drives high quality from market. Corporate finance: Equity issuance negative signal (pecking order). Political campaigns: Promises cheap talk → credibility via reputation, costly actions.

Perfect Bayesian Equilibrium: Strategies sequentially rational, beliefs consistent (Bayes' rule on-path, reasonable off-path). Information asymmetry central to auctions, insurance, labor markets, finance, politics—strategic communication and mechanism design critical for extracting information and achieving efficiency.
