# Forecasting & Calibration

## Overview

Making predictions and evaluating their accuracy is where epistemology meets practice. Calibration — having your confidence levels match actual outcomes — is a trainable skill. Superforecasters demonstrate that some people consistently outpredict experts, intelligence analysts with classified information, and prediction markets. This chapter covers the science of prediction.

Forecasting isn't about certainty — it's about quantifying uncertainty accurately. A well-calibrated forecaster saying "70% confident" is right 70% of the time, wrong 30% of the time. Most people are poorly calibrated, typically overconfident. Understanding forecasting improves decision-making across domains: business strategy, medical diagnosis, personal life choices, public policy.

## What is Calibration?

**Calibration** is the match between stated confidence levels and actual accuracy frequencies.

**Perfectly calibrated forecaster**:
- When they say 70% confident, they're right exactly 70% of the time
- When they say 90% confident, they're right exactly 90% of the time
- When they say 50% confident, they're right exactly 50% of the time (no better than chance)

**Calibration curve**: Plot confidence (x-axis) vs actual accuracy (y-axis). Perfect calibration = 45° line (y = x).

### Typical Calibration Patterns

**Overconfidence** (most common):
- Say 90% confident → right ~75% of time
- Say 99% confident → right ~85% of time
- Confidence-accuracy gap widens at higher confidence levels

**Underconfidence** (rare):
- Say 70% confident → right ~80% of time
- More common among experts in narrow domains where they know the limits

**Well-calibrated**:
- Confidence matches accuracy at all levels
- Superforecasters achieve this through training and tracking

### Calibration vs Resolution

**Calibration**: Do your stated probabilities match frequencies? (70% confident → 70% accurate)
**Resolution** (discrimination): Can you distinguish easy from hard questions? (90% on easy, 60% on hard)

Good forecasters have both high calibration and high resolution. Bad forecasters might be well-calibrated at 50% by always saying "50% confident" (no resolution) — useless.

## Scoring Rules

To evaluate forecasts, we need proper **scoring rules** that reward accuracy and penalize error.

### Brier Score

**Formula**:
```
Brier = (1/N) Σ (pᵢ - oᵢ)²
```

Where:
- p = predicted probability (0 to 1)
- o = outcome (1 if event occurred, 0 if not)
- N = number of forecasts

**Range**: 0 (perfect) to 2 (worst possible, always wrong with 100% confidence)

**Interpretation**:

| Brier Score | Quality |
|-------------|---------|
| 0.00 | Perfect (impossible in practice) |
| 0.10 | Excellent (superforecaster level) |
| 0.20 | Good |
| 0.25 | Random guessing (always say 50%) |
| 0.50 | Always wrong at 100% confidence |

**Example**:
- Forecast 1: 70% rain, it rained → (0.7 - 1)² = 0.09
- Forecast 2: 60% win, they lost → (0.6 - 0)² = 0.36
- Forecast 3: 90% pass, they passed → (0.9 - 1)² = 0.01
- Brier = (0.09 + 0.36 + 0.01) / 3 = 0.153 (good)

**Decomposition** (Murphy, 1973):
```
Brier = Calibration + Resolution - Uncertainty
```

This separates:
- **Calibration**: How well do probabilities match frequencies?
- **Resolution**: Can you discriminate between events of different difficulty?
- **Uncertainty**: Inherent unpredictability (you can't control this)

### Log Score (Logarithmic Scoring Rule)

**Formula**:
```
Log score = (1/N) Σ [oᵢ log(pᵢ) + (1-oᵢ) log(1-pᵢ)]
```

**Properties**:
- Heavily penalizes confident wrong predictions
- If you say 99% and you're wrong, massive penalty
- If you say 1% and you're right, massive reward
- More sensitive to extreme probabilities than Brier score

**Example**: Forecast 99% it will rain, it doesn't rain.
- Brier: (0.99 - 0)² = 0.98
- Log: log(1 - 0.99) = log(0.01) = -4.6 (huge penalty)

Log score rewards well-calibrated extreme confidence but punishes poorly-calibrated extremes harshly.

### Proper Scoring Rules

A scoring rule is **proper** if it's optimized by reporting your true beliefs. You can't game the system by strategically misreporting probabilities.

**Brier and log scores are proper**. Your expected score is maximized by honest reporting.

**Percent correct is NOT proper**. You can game it by always saying 100% (maximizes expected score if you're right >50% of time, but gives no probability information).

**Why properness matters**: Proper scoring rules incentivize honest forecasting. In forecasting tournaments, prediction markets, and expert elicitation, use proper scoring rules.

## Superforecasting (Tetlock)

Philip Tetlock's Good Judgment Project (2011-2015), funded by IARPA, identified and studied **superforecasters** — ordinary people who consistently outperform.

### The Research

**Design**:
- 20,000+ forecasters made >1 million predictions on ~500 questions
- Geopolitical events: "Will Greece leave the euro by Dec 2015?" "Will Assad fall by June 2013?"
- Questions resolved definitively (yes/no or numerical answer)
- Brier scores calculated for all forecasts

**Results**:
- Top ~2% (superforecasters) had Brier scores ~30% better than average
- Superforecasters beat prediction markets
- Superforecasters beat intelligence analysts with access to classified information
- Superforecasters in teams beat superforecasters working alone
- Performance persisted across years — it's skill, not luck

### What Makes Superforecasters?

| Trait | Description | Example |
|-------|-------------|---------|
| **Actively open-minded thinking** | Genuinely consider evidence against views; update readily | "I thought X, but this evidence suggests Y. Let me revise." |
| **Granularity** | Use precise probabilities (73%, not "likely") | "67% chance" not "probably" |
| **Frequent updating** | Revise forecasts often as new information arrives | Update daily or weekly, not just once |
| **Foxes not hedgehogs** | Know many things (fox) vs one big thing (hedgehog) | Synthesize from economics, history, psychology, politics vs applying one framework |
| **Growth mindset** | Believe forecasting skill is improvable through practice | "I can get better at this" vs "I'm not good at predictions" |
| **Numerate** | Comfortable with probability, statistics, base rates | Calculate using Bayes' theorem, think in frequencies |
| **Ego-less** | Value accuracy over being right; admit error readily | "I was wrong. What did I miss?" vs defending prior view |
| **Team players** | Share reasoning, learn from disagreement | Engage with opposing views constructively |
| **Scope sensitivity** | Adjust predictions appropriately for different time horizons | 60% for 1 year ≠ 60% for 5 years |
| **Tip-of-your-nose perspective** | Start with status quo, adjust incrementally | "What's changed since yesterday?" vs "Big picture speculation" |

### Foxes vs Hedgehogs (Isaiah Berlin)

**Hedgehogs**: Have one big idea. Force everything into their framework. (Marxism explains everything, free markets solve everything, realism governs all geopolitics)

**Foxes**: Draw from many frameworks. Synthesize eclectically. ("Economics suggests X, but history shows Y, and psychology implies Z. Weighing them...")

**Tetlock's finding**: **Foxes dramatically outperform hedgehogs at forecasting**.

**Why hedgehogs fail**:
- Overconfident (their framework explains everything, so they're certain)
- Ignore disconfirming evidence (doesn't fit the framework → dismiss it)
- Make bold predictions (frameworks give clear answers)
- Famous hedgehogs get media attention (bold, confident, quotable) but are terrible forecasters

**Why foxes succeed**:
- Modest (many frameworks → uncertainty about which applies)
- Update readily (new evidence → revise framework weights)
- Make calibrated predictions (integrate multiple signals)
- Boring to media (tentative, nuanced, "on the other hand...") but accurate

**Implication**: Beware confident pundits with grand theories. Seek fox-like thinkers who hedge, equivocate, and synthesize.

### Superforecaster Techniques

**Fermi decomposition** (see below): Break complex questions into estimable components.

**Base rates first**: Start with outside view (what happened in similar cases?), then adjust for specifics.

**Multiple models**: Consider several frameworks, weight them probabilistically.

**Scenario analysis**: Enumerate paths to Yes and No, estimate probabilities of each path.

**Frequent small updates**: Don't wait for major news. Update incrementally as small signals arrive.

**Team deliberation**: Share reasoning, debate cruxes, synthesize perspectives.

**Pre-mortems**: "Assume I'm wrong. Why?" Surfaces overlooked risks.

**Extremizing**: When aggregating team forecasts, move toward extremes (wisdom-of-crowds forecasts are too moderate).

## Reference Class Forecasting

Daniel Kahneman's **outside view**: Instead of reasoning from the specifics of your case (inside view), find the base rate of similar past cases.

**Inside view**: "Our project will take 6 months because we have a strong team, a clear plan, and good resources."

**Outside view**: "Similar IT projects in our industry take 12-18 months on average, with 30% running over 2 years."

**Why outside view is better**: Inside view suffers from planning fallacy, optimism bias, and neglect of unknown unknowns. Outside view captures actual historical performance.

### How to Apply

1. **Identify the reference class**: What category does this belong to? (IT projects in finance, product launches in consumer electronics, FDA drug approvals, etc.)

2. **Find the base rate**: What's the distribution of outcomes in this class? (Mean, median, variance, tail probabilities)

3. **Adjust modestly**: Are there specific factors that make this case different? How much should you adjust from the base rate?

4. **Don't over-adjust**: Specific evidence is often weaker than it feels. Regression to the mean is powerful.

**Example**: Startup success rate.

Inside view: "Our startup will succeed because we have a great team, innovative product, and strong demand signals."

Outside view: "90% of startups fail within 5 years. For tech startups in this industry, the failure rate is 85%. Conditional on raising Series A, failure rate drops to 75%."

Start with base rate (75% failure), adjust modestly for specific strengths. Don't go from 75% failure to 10% failure based on inside view — the evidence isn't that strong.

### Clash of Views

Kahneman advocates **starting with outside view, adjusting slightly for inside view**.

Tetlock finds superforecasters **blend both** — start with base rates but update significantly for case-specific information.

Key: Don't ignore either view. Base rates anchor you; specifics update you. The question is how much weight to give each.

## Prediction Markets

**Prediction markets**: Markets where participants trade contracts on future events. Prices reflect aggregated beliefs about probabilities.

### How They Work

A contract pays $1 if event occurs, $0 if not. If the contract trades at $0.60, the market implies 60% probability.

**Example**: "Will Biden win the 2024 election?" contract.
- If trading at $0.55, market says 55% Biden wins
- If you think Biden has 70% chance, you buy (expected value = $0.70, costs $0.55, expected profit $0.15)
- If you think Biden has 40% chance, you sell (expected value = $0.40, receive $0.55, expected profit $0.15)
- Trading continues until price reflects aggregate beliefs

### Major Prediction Markets

| Market | Type | Strengths | Weaknesses |
|--------|------|-----------|------------|
| **PredictIt** | Real money (capped $850) | Liquid for US politics, diverse traders | Low limits, US only, high fees |
| **Polymarket** | Crypto-based | High volume, no limits, global | Crypto barrier, legal gray zone |
| **Metaculus** | Community forecasting (no money) | High-quality forecasters, diverse questions | No money → less skin in game |
| **Iowa Electronic Markets** | Real money (academic) | Long track record, academic credibility | Very limited questions, low volume |
| **Kalshi** | CFTC-regulated real money | Legal, regulated, growing | New (2021), limited liquidity |

### Advantages of Prediction Markets

**Information aggregation**: Diverse participants with different information trade → prices aggregate dispersed knowledge.

**Incentives for accuracy**: Money on the line → traders research, think carefully.

**Real-time updating**: Prices update instantly as news breaks.

**Reveal probabilities**: Directly produce probability estimates (unlike polls).

**Hard to manipulate**: Manipulators lose money to informed traders (unless manipulator has deep pockets and doesn't care about losses).

### Limitations

**Thin markets**: Many questions have low volume → prices noisy, manipulable.

**Legal restrictions**: Many countries prohibit real-money prediction markets → limits participation.

**Irrational traders**: Wishful thinking, biases can distort prices temporarily.

**Longshot bias**: Markets overestimate low-probability events (~5% traded at 10%).

**Favorite-longshot bias**: Favorites underpriced, longshots overpriced (also seen in horse racing).

**Can't handle very low probabilities**: $0.01 contract (1% probability) is hard to trade efficiently.

### Evidence for Accuracy

**Presidential elections**: Prediction markets beat polls consistently. Iowa Electronic Markets beat polls in 75% of elections since 1988.

**Sports**: Betting markets are well-calibrated. When markets say 70%, favorites win ~70% of time.

**Comparison to experts**: Berg et al. (2008): Prediction markets outperformed expert forecasts in 75% of comparisons.

**Tetlock's finding**: Superforecaster teams beat prediction markets. This suggests forecaster skill > crowd wisdom in some contexts.

## Fermi Estimation

Enrico Fermi's technique: **Break complex questions into estimable components**, multiply the estimates.

### The Method

1. Decompose the question into factors you can estimate
2. Estimate each factor (order-of-magnitude is good enough)
3. Multiply the estimates
4. Check if the result passes sanity checks

**Why it works**: Individual errors tend to cancel (some too high, some too low). Decomposition prevents gross errors.

### Classic Example: Piano Tuners in Chicago

**Question**: How many piano tuners in Chicago?

**Decomposition**:
- Chicago population: ~2.7 million people
- Average household size: ~2.5 people → ~1.1 million households
- Fraction with pianos: ~5% (guess) → ~55,000 pianos
- Tuning frequency: ~1/year → 55,000 tunings/year
- Tunings per tuner per day: ~4 (travel time, tuning time)
- Working days: ~250/year → 1,000 tunings/tuner/year
- Tuners needed: 55,000 / 1,000 ≈ **50-55 piano tuners**

**Actual**: ~100-150 (varies by source). We're within an order of magnitude — success for Fermi estimation!

**Where we might be off**:
- Piano ownership might be higher (10% → 100 tuners)
- Tunings might be less frequent (every 2 years → 25 tuners)
- Tuners might do fewer tunings per day (3 → 70 tuners)

But the method got us in the ballpark.

### More Examples

**Global annual CO₂ emissions from aviation**:
- Flights per year globally: ~40 million
- Average passengers per flight: ~100 → 4 billion passenger-flights
- CO₂ per passenger-km: ~0.1 kg
- Average flight distance: ~1,500 km
- Total: 4 billion × 1,500 km × 0.1 kg/km = 600 million tons CO₂
- (Actual: ~900 million tons. Close!)

**Number of gas stations in the US**:
- US population: ~330 million
- Households: ~130 million
- Cars per household: ~2 → 260 million cars
- Refueling frequency: ~1/week → 260 million refuelings/week = ~37 million/day
- Customers per gas station per day: ~200
- Stations: 37 million / 200 ≈ **185,000 gas stations**
- (Actual: ~150,000. Within 25%!)

**Key insight**: You don't need precise numbers. Order-of-magnitude estimates, when combined, give surprisingly accurate results.

## Decision-Making Under Uncertainty

### Expected Value

**Formula**:
```
EV = Σ pᵢ × vᵢ
```

Choose the option with highest expected value.

**Example**: Bet: 50% win $100, 50% lose $40.
- EV = 0.5($100) + 0.5(-$40) = $50 - $20 = **$30**
- Take the bet (positive EV)

**Limitation**: Ignores risk preferences. You might decline a 50-50 bet to win $1 billion or lose $500,000 even though EV = +$499.75 million.

### Expected Utility

**Formula**:
```
EU = Σ pᵢ × U(vᵢ)
```

Where U(v) is utility function (subjective value, not money).

**Properties**:
- Accounts for risk aversion (concave U)
- Accounts for diminishing marginal utility
- Different people have different U functions

**Example**: Risk-averse person.
- U($0) = 0, U($50,000) = 70, U($100,000) = 100
- Bet: 50% win $100K, 50% lose $0 (lose initial $50K)
- EU(bet) = 0.5(100) + 0.5(0) = 50
- EU(no bet, keep $50K) = 70
- Don't bet (higher expected utility)

### Kelly Criterion

Optimal bet sizing for repeated bets with an edge.

**Formula**:
```
f* = (p × b - q) / b
```

Where:
- f* = fraction of bankroll to bet
- p = probability of winning
- q = 1 - p
- b = odds received (e.g., b=2 means win doubles your bet)

**Example**: 60% chance to win, odds pay 2-to-1 (win $2 for every $1 bet).
- f* = (0.6 × 2 - 0.4) / 2 = (1.2 - 0.4) / 2 = **0.4 = 40% of bankroll**

**Key insights**:
- Even with edge, don't bet everything (risk of ruin)
- Kelly maximizes long-term growth rate
- Kelly is aggressive (many use fractional Kelly, e.g., half-Kelly = f*/2)
- Overbetting (> f*) risks ruin; underbetting leaves money on table

**Application**: Investment sizing (not literal betting). If you have edge in markets, Kelly suggests position sizing.

### Minimax Regret

Choose the option that **minimizes worst-case regret** (difference between outcome and best possible outcome).

**Example**: Investment decision.

| | Economy Good | Economy Bad |
|--|-------------|-------------|
| **Invest** | $100K profit | $50K loss |
| **Don't invest** | $0 | $0 |

**Regret table**:

| | Economy Good | Economy Bad |
|--|-------------|-------------|
| **Invest** | $0 (best outcome) | $50K (could have had $0) |
| **Don't invest** | $100K (could have had $100K) | $0 (best outcome) |

**Max regret**:
- Invest: max($0, $50K) = **$50K**
- Don't invest: max($100K, $0) = **$100K**

**Minimax regret → Invest** (minimizes worst-case regret to $50K).

**When to use**: Deep uncertainty (don't know probabilities), want to avoid worst regret.

## Forecasting Failures and Successes

### Why Experts Fail

**Hedgehog thinking**: Apply one framework to everything. The world is more complex than any single framework.

**Overconfidence**: Experts are more confident than accurate. Expertise increases confidence faster than accuracy.

**Incentive misalignment**: Media rewards bold, confident predictions (interesting, quotable). Accuracy is unrewarded or punished (boring, hedging, "I don't know").

**Political/ideological distortion**: Motivated reasoning. Experts with policy preferences distort forecasts to support preferred policies.

**Narrative bias**: Compelling stories feel accurate. Experts construct narratives that sound plausible but don't predict.

**Failure to update**: Anchoring on initial assessment. New evidence triggers rationalization, not updating.

**Narrow expertise**: Deep knowledge of one domain but poor general knowledge. Missing cross-domain signals.

### When Forecasting Works

**Short time horizons**: Weather (1-7 days), elections (weeks before), sports (game-day).

**Stable systems**: Phenomena with regular patterns, good historical data, stationary processes.

**Decomposable problems**: Can be broken into estimable components (Fermi estimation).

**Aggregated predictions**: Average of many forecasters, prediction markets, ensembles beat individuals.

**Well-defined questions**: Clear resolution criteria, not ambiguous.

**Frequent feedback**: Many similar predictions, rapid resolution, tight feedback loop for learning.

### When Forecasting Fails

**Long time horizons**: Technology in 20 years, geopolitics in 50 years, existential risks.

**Unprecedented events**: COVID-19, 9/11, 2008 financial crisis. No reference class, no base rates.

**Reflexive systems**: Predictions change the thing being predicted (markets, elections when polls influence voters).

**Complex adaptive systems**: Many interacting components, nonlinear feedback, tipping points.

**Ambiguous questions**: "Will AI be transformative?" (Define transformative? When? How measure?)

**Adversarial contexts**: Other agents trying to deceive you (warfare, espionage, competitive business).

## Personal Calibration Training

### The Process

1. **Make explicit probabilistic predictions**: State beliefs as probabilities, not vague "I think" or "probably."

2. **Track outcomes**: Record predictions and results systematically. Spreadsheet, app, journal.

3. **Review calibration**: Plot confidence vs accuracy. Am I right 70% of the time when I say 70%?

4. **Identify patterns**: Where am I overconfident? Underconfident? In which domains?

5. **Adjust**: If overconfident at 90%, lower future 90% predictions to 80%. If underconfident at 60%, raise to 70%.

6. **Iterate**: Repeat for 100+ predictions. Calibration improves with feedback.

### Calibration Exercises

**Trivia questions with confidence**:
- Question: "What year was the Eiffel Tower completed?"
- Answer: "1889. Confidence: 70%."
- After many questions, check: When you said 70%, were you right 70% of the time?

**Prediction tournaments**: Join Metaculus, Good Judgment Open, Manifold Markets. Free, provides feedback, community.

**Daily predictions**: "Will it rain tomorrow? 40%." "Will my meeting start on time? 60%." Track outcomes.

**Calibration games**: "Guess the % of countries in the UN that are in Africa? Confidence: 70% it's between 20-30%." (Actual: 28%, 55/193)

### Common Adjustments

**When you feel certain (90%+)**: Try 85%. True certainty is rare.

**When you feel uncertain (~50%)**: Try 60% or 65%. Pure coin-flip is rare; you usually have some signal.

**When you feel "pretty sure" (70-80%)**: Might be right. Check if you're actually right 70-80% at this level.

**Equivalent bet test**: "Would I bet $X at these odds?" If you say 70%, would you bet $70 to win $100 (implied 41% probability)? If not, you don't actually believe 70%.

**Consider the opposite**: What would make me wrong? If many plausible paths to being wrong, lower confidence.

**Pre-hindsight**: "In a world where I'm wrong, what happened?" Surfaces scenarios you're neglecting.

## Key Terms

- **Calibration**: Match between stated confidence levels and actual accuracy frequencies
- **Brier Score**: Mean squared error of probabilistic predictions; (1/N) Σ (p - o)²; lower = better
- **Proper Scoring Rule**: Scoring rule optimized by reporting true beliefs (Brier, log score)
- **Superforecaster**: Person consistently outperforming at probabilistic prediction (Tetlock)
- **Reference Class Forecasting**: Using base rates of similar cases (outside view)
- **Inside vs Outside View**: Specific case reasoning vs base rate reasoning (Kahneman)
- **Fermi Estimation**: Decomposing complex questions into estimable components
- **Kelly Criterion**: Optimal bet sizing formula; f* = (pb - q)/b; maximizes long-run growth
- **Minimax Regret**: Minimizing worst-case regret
- **Prediction Market**: Market where prices reflect aggregated beliefs about event probabilities
- **Foxes vs Hedgehogs**: Eclectic synthesizers vs single-framework thinkers (Berlin, Tetlock)
- **Log Score**: Logarithmic scoring rule; heavily penalizes confident wrong predictions
- **Resolution**: Ability to discriminate easy from hard questions; calibration + resolution = skill

## Summary

Calibration — matching confidence to accuracy — is the core skill of good forecasting. Most people are overconfident, especially at high confidence levels. Superforecasters achieve good calibration through deliberate practice, frequent updating, granular probabilities, and actively open-minded thinking.

Tetlock's research shows foxes (eclectic synthesizers) dramatically outperform hedgehogs (single-framework thinkers). Superforecasters blend inside view (case specifics) with outside view (base rates), decompose questions (Fermi estimation), update frequently on small signals, and work in teams that aggregate diverse perspectives.

Scoring rules measure forecast accuracy. Brier score (mean squared error) is intuitive and proper. Log score heavily penalizes confident wrong predictions. Proper scoring rules incentivize honest probability reporting.

Reference class forecasting (outside view) corrects planning fallacy by anchoring on base rates of similar past cases. Fermi estimation decomposes complex questions into estimable components — errors cancel, yielding surprisingly accurate results.

Prediction markets aggregate diverse information through prices. Empirically, they beat polls (politics), beat experts (many domains), and are well-calibrated. Limitations include thin markets, legal restrictions, and longshot bias.

Decision-making under uncertainty uses expected value (risk-neutral), expected utility (accounts for risk preferences), Kelly criterion (optimal bet sizing for repeated bets), and minimax regret (minimize worst-case regret when probabilities unknown).

Forecasting works best for short horizons, stable systems, decomposable problems, and aggregated predictions. It fails for long horizons, unprecedented events, reflexive systems, and complex adaptive systems.

Personal calibration is trainable: make explicit probabilistic predictions, track outcomes, review calibration curves, identify overconfidence/underconfidence patterns, and adjust. Tools include prediction tournaments (Metaculus), trivia with confidence intervals, and daily predictions.

The practical lesson: Forecasting isn't about certainty or perfection. It's about quantifying uncertainty accurately and updating as evidence arrives. Even small improvements in calibration compound over time, yielding better decisions in every domain where the future matters.