# Module 17: Portfolio Construction

## Learning Objectives

By the end of this module, you will understand:
- Pacing models and commitment planning
- Vintage year diversification strategies
- Commitment vs exposure management
- Allocation frameworks for private markets
- Portfolio rebalancing approaches

---

## 17.1 The Portfolio Construction Challenge

### Private Markets vs Public Markets

```
PORTFOLIO CONSTRUCTION COMPARISON
─────────────────────────────────

PUBLIC MARKETS:
├── Instant deployment
├── Known current exposure
├── Easy rebalancing
├── Daily liquidity
└── Precise allocation control

PRIVATE MARKETS:
├── Commitment ≠ Exposure
├── Deployment over 3-5 years
├── J-curve cash flow profile
├── 10+ year illiquidity
└── Indirect control of allocation

THE FUNDAMENTAL CHALLENGE:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  You commit $100M today...                             │
│                                                         │
│  Year 1: Called $20M → Exposure $20M                   │
│  Year 2: Called $45M → Exposure $45M                   │
│  Year 3: Called $75M → Exposure $70M (some returned)   │
│  Year 4: Called $90M → Exposure $80M                   │
│  Year 5: Called $95M → Exposure $85M                   │
│                                                         │
│  Peak exposure ~85% of commitment                       │
│  Timing unpredictable                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Commitment vs Exposure vs NAV

```
KEY CONCEPTS
────────────

COMMITMENT:
├── Total amount promised to fund
├── Legal obligation
└── Does NOT equal actual investment

FUNDED/CALLED:
├── Capital actually invested
├── Drawn from commitment
└── Creates "exposure"

UNFUNDED:
├── Remaining commitment not yet called
├── Future obligation
└── "Dry powder"

EXPOSURE (NAV):
├── Current market value
├── Funded minus distributions plus/minus gains
└── What you actually "own"

EXAMPLE:
┌────────────────────────────────────────┐
│ Fund Commitment:      $100M            │
│ Called to date:       $70M             │
│ Unfunded:            $30M              │
│ Distributions:        $25M             │
│ Current NAV:          $80M             │
│                                        │
│ Exposure = $80M (NAV)                  │
│ NOT $100M (commitment)                 │
│ NOT $70M (called)                      │
└────────────────────────────────────────┘
```

---

## 17.2 Pacing Models

### What is a Pacing Model?

A **pacing model** forecasts how much to commit each year to achieve and maintain a target allocation.

```
PACING MODEL COMPONENTS
───────────────────────

INPUTS:                          OUTPUTS:
├── Current PE NAV               ├── Annual commitment targets
├── Unfunded commitments         ├── Expected NAV trajectory
├── Total portfolio size         ├── Expected cash flows
├── Target PE allocation         ├── Allocation forecast
├── Expected returns             └── Overcommitment ratio
├── Expected cash flows
└── Commitment period

BASIC FORMULA:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│ New Commitments = f(Target NAV - Projected NAV)        │
│                                                         │
│ Where Projected NAV =                                   │
│   Current NAV                                           │
│   + Expected calls (from unfunded)                     │
│   + Expected appreciation                               │
│   - Expected distributions                              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Simple Pacing Example

```
PACING MODEL EXAMPLE
────────────────────

ASSUMPTIONS:
├── Total portfolio: $1,000M
├── Target PE allocation: 15% ($150M NAV)
├── Current PE NAV: $100M
├── Unfunded commitments: $50M
├── Average fund life: 10 years
├── Expected gross return: 15%
├── Expected net distributions: 8% of NAV/year

YEAR 1 PROJECTION:
┌─────────────────────────────────────────────────────────┐
│ Starting NAV:                          $100M           │
│ + Expected calls (35% of unfunded):    $17.5M          │
│ + Appreciation (15% × starting NAV):   $15M            │
│ - Distributions (8% × starting NAV):   -$8M            │
│ ───────────────────────────────────                    │
│ Projected Year-End NAV:                $124.5M         │
│                                                         │
│ Target NAV:                            $150M           │
│ Gap:                                   $25.5M          │
│                                                         │
│ Adjustment for deployment time:        ×2.0            │
│ Recommended new commitment:            ~$50M           │
└─────────────────────────────────────────────────────────┘
```

### The Overcommitment Ratio

```
OVERCOMMITMENT CONCEPT
──────────────────────

Because PE money isn't called immediately:
├── Must commit MORE than target allocation
├── "Overcommit" to reach actual exposure
└── Ratio depends on pacing assumptions

OVERCOMMITMENT RATIO:
                    Total Unfunded Commitments
Overcommit Ratio = ─────────────────────────────
                    Target NAV Allocation

TYPICAL RATIOS:
├── Building program: 1.5-2.0x
├── Mature program: 1.0-1.3x
├── Aggressive growth: 2.0-2.5x

EXAMPLE:
┌─────────────────────────────────────────────────────────┐
│ Target PE allocation:      $150M NAV                    │
│ Total commitments:         $220M                        │
│ Current NAV:               $100M                        │
│ Unfunded:                  $80M                         │
│                                                         │
│ Overcommitment ratio:                                   │
│ ($80M unfunded + $150M target) / $150M = 1.53x         │
│                                                         │
│ Or: Total commits / Target NAV = $220M / $150M = 1.47x │
└─────────────────────────────────────────────────────────┘
```

### Pacing Model Assumptions

```
KEY PACING ASSUMPTIONS
──────────────────────

CONTRIBUTION RATES (% of unfunded called per year):
├── Year 1: 25-35%
├── Year 2: 25-30%
├── Year 3: 20-25%
├── Year 4: 10-15%
├── Year 5+: 5-10%
└── Total: 90-100% over 4-5 years

DISTRIBUTION RATES (% of NAV distributed per year):
├── Years 1-3: 0-5%
├── Years 4-5: 10-15%
├── Years 6-7: 15-25%
├── Years 8-10: 20-30%
└── Varies by strategy

GROWTH RATES:
├── NAV appreciation: 10-20% gross
├── Net of fees: 8-15%
└── Varies by strategy and vintage

SENSITIVITY MATTERS:
┌─────────────────────────────────────────────────────────┐
│ Small changes in assumptions → Big changes in output   │
│                                                         │
│ If distributions 5% higher than expected:              │
│ → NAV grows slower                                      │
│ → Need more commitments                                 │
│ → May exceed overcommit targets                         │
│                                                         │
│ Model quarterly, update assumptions regularly           │
└─────────────────────────────────────────────────────────┘
```

---

## 17.3 Vintage Year Diversification

### Why Vintage Diversification Matters

```
VINTAGE YEAR RETURNS VARY DRAMATICALLY
──────────────────────────────────────

US BUYOUT MEDIAN NET IRR BY VINTAGE:
(Illustrative)

2006: ████████████████████ 15%
2007: ████████████ 9%
2008: ██████████████ 11%
2009: ██████████████████████████ 19%
2010: ████████████████████████ 18%
2011: ██████████████████████ 17%
2012: ████████████████████ 16%
2013: ██████████████████ 14%
2014: ████████████████████ 15%
2015: ██████████████████████ 17%

ENTRY POINT DRIVES RETURNS:
├── 2007: Expensive entry, crisis exits = weak
├── 2009: Cheap entry, recovery exits = strong
└── Best manager in bad vintage may trail median in good vintage
```

### Building Vintage Diversification

```
VINTAGE DIVERSIFICATION STRATEGIES
──────────────────────────────────

APPROACH 1: CONSISTENT ANNUAL COMMITMENT
├── Commit similar amounts each year
├── "Dollar-cost averaging" for PE
├── Builds diversification naturally
└── Simple to implement

Year    Commitment    Vintage Exposure
────    ──────────    ────────────────
2020    $50M          2020: 20%
2021    $50M          2021: 20%
2022    $50M          2022: 20%
2023    $50M          2023: 20%
2024    $50M          2024: 20%

APPROACH 2: OPPORTUNISTIC / COUNTER-CYCLICAL
├── Increase commitments in downturns
├── Decrease in frothy markets
├── Requires market timing ability
└── Potentially higher returns, harder to execute

Year    Market      Commitment
────    ──────      ──────────
2019    Peak        $30M
2020    Crisis      $80M  ◄── Opportunistic
2021    Recovery    $50M
2022    Correction  $70M  ◄── Opportunistic
2023    Uncertain   $50M
```

### Measuring Vintage Concentration

```
VINTAGE CONCENTRATION ANALYSIS
──────────────────────────────

PORTFOLIO SNAPSHOT:
┌─────────────────────────────────────────────────────────┐
│ Vintage │ NAV    │ % of PE │ Assessment              │
│ ─────── │ ────── │ ─────── │ ─────────────────────── │
│ 2018    │ $12M   │ 8%      │ Mature, exiting         │
│ 2019    │ $18M   │ 12%     │ Harvest phase           │
│ 2020    │ $35M   │ 23%     │ ⚠️ Concentrated         │
│ 2021    │ $42M   │ 28%     │ ⚠️ Concentrated         │
│ 2022    │ $25M   │ 17%     │ Building value          │
│ 2023    │ $18M   │ 12%     │ J-curve                 │
│ ─────── │ ────── │ ─────── │                         │
│ Total   │ $150M  │ 100%    │                         │
└─────────────────────────────────────────────────────────┘

CONCENTRATION METRICS:
├── Top 2 vintages: 51% (2020+2021)
├── Herfindahl index: 0.19
└── Target: No vintage >25%, HHI <0.15

ACTIONS:
├── Reduce 2024 commitments to dilute 2020/2021
├── Or wait for 2020/2021 distributions
└── Consider secondary sales to rebalance
```

---

## 17.4 Allocation Frameworks

### Target Allocation Approaches

```
PE ALLOCATION FRAMEWORKS
────────────────────────

APPROACH 1: % OF TOTAL PORTFOLIO
├── Simple: "15% in private equity"
├── Based on total AUM
├── Includes all strategies
└── Most common approach

APPROACH 2: % OF ALTERNATIVES
├── PE as part of alternatives bucket
├── E.g., "50% of 30% alternatives allocation"
├── Allows flexibility within alts
└── Common for smaller allocators

APPROACH 3: RISK-BASED
├── Allocate based on risk contribution
├── PE typically higher risk weight
├── Integrates with total portfolio risk
└── More sophisticated

APPROACH 4: FACTOR-BASED
├── Target factor exposures
├── PE provides: illiquidity, leverage, equity beta
├── Complementary to public exposures
└── Most complex
```

### Strategy Allocation

```
PRIVATE EQUITY STRATEGY MIX
───────────────────────────

EXAMPLE: $200M PE PROGRAM

STRATEGY          │ TARGET │ RATIONALE
──────────────────┼────────┼─────────────────────────
Large Buyout      │ 25%    │ Lower risk, diversified
Mid-Market Buyout │ 30%    │ Core return driver
Growth Equity     │ 15%    │ Growth exposure
Venture Capital   │ 10%    │ Innovation/upside
Secondaries       │ 10%    │ J-curve mitigation
Co-investments    │ 10%    │ Fee savings
──────────────────┴────────┴─────────────────────────

STRATEGY ALLOCATION CONSIDERATIONS:
├── Return expectations by strategy
├── Risk tolerance
├── Access to top managers
├── Portfolio company exposure
├── Liquidity needs
└── Resource constraints
```

### Geographic Allocation

```
GEOGRAPHIC ALLOCATION
─────────────────────

GLOBAL PE MARKET (by AUM):
├── North America: 60%
├── Europe: 25%
├── Asia: 12%
├── ROW: 3%

TYPICAL LP ALLOCATION:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌────────────────────────────────────────────────┐    │
│  │                                                │    │
│  │ US/Canada  60-70%   █████████████████████████ │    │
│  │                                                │    │
│  │ Europe     15-25%   █████████████             │    │
│  │                                                │    │
│  │ Asia       5-15%    ███████                   │    │
│  │                                                │    │
│  │ ROW        0-5%     ██                        │    │
│  │                                                │    │
│  └────────────────────────────────────────────────┘    │
│                                                         │
│  HOME BIAS COMMON:                                      │
│  US pensions often 70-80% US                           │
│  European pensions often 50%+ Europe                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 17.5 Commitment vs Exposure Management

### The Commitment Gap

```
COMMITMENT GAP ILLUSTRATION
───────────────────────────

YEAR 0: New PE program

Target: $100M exposure (15% of $667M portfolio)

WRONG APPROACH:
├── Commit $100M
├── Year 1 exposure: ~$25M (only 4% allocation!)
├── Takes 4+ years to reach target
└── Significant underexposure

RIGHT APPROACH:
├── Commit $150-200M (1.5-2.0x target)
├── Year 1 exposure: $40-50M
├── Reach target exposure in Year 2-3
└── Account for distributions

COMMITMENT TRAJECTORY:
Year │ Commitment │ Unfunded │ NAV    │ Actual %
─────┼────────────┼──────────┼────────┼──────────
  0  │ $150M      │ $150M    │ $0     │ 0%
  1  │ $200M      │ $160M    │ $40M   │ 6%
  2  │ $240M      │ $150M    │ $85M   │ 11%
  3  │ $270M      │ $130M    │ $125M  │ 15% ✓
  4  │ $290M      │ $110M    │ $145M  │ 16%
  5  │ $300M      │ $90M     │ $155M  │ 17%
```

### Exposure Forecasting

```
EXPOSURE FORECAST MODEL
───────────────────────

INPUTS:
├── Existing NAV by fund
├── Unfunded by fund
├── Expected contribution schedule
├── Expected distribution schedule
├── Expected appreciation
└── New commitment plans

EXAMPLE 3-YEAR FORECAST:
┌─────────────────────────────────────────────────────────┐
│                   Year 1    Year 2    Year 3           │
│                   ──────    ──────    ──────           │
│ Starting NAV      $100M     $135M     $160M            │
│ + Contributions   +$45M     +$40M     +$35M            │
│ + Appreciation    +$15M     +$20M     +$24M            │
│ - Distributions   -$25M     -$35M     -$40M            │
│ ───────────────   ──────    ──────    ──────           │
│ Ending NAV        $135M     $160M     $179M            │
│                                                         │
│ Total Portfolio   $900M     $950M     $1,000M          │
│ PE Allocation     15.0%     16.8%     17.9%            │
│                                                         │
│ ACTION: Reduce new commitments if trending over target │
└─────────────────────────────────────────────────────────┘
```

### Managing the Denominator

```
DENOMINATOR EFFECT ON ALLOCATION
────────────────────────────────

SCENARIO: Public markets fall 20%

BEFORE DECLINE:
├── Total portfolio: $1,000M
├── PE NAV: $150M
├── PE allocation: 15% ✓

AFTER DECLINE (PE unchanged):
├── Total portfolio: $850M
├── PE NAV: $150M
├── PE allocation: 17.6% ⚠️

RESPONSE OPTIONS:

1. DO NOTHING
   └── Allocation drifts, rebalances naturally over time

2. REDUCE COMMITMENTS
   └── Lower new commitments, let distributions reduce PE

3. SELL SECONDARIES
   └── Active rebalancing via secondary market (costs involved)

4. ADJUST TARGET
   └── Temporarily raise PE target, recognizing illiquidity

BEST PRACTICE:
├── Define allocation RANGE not point (e.g., 12-18%)
├── Only act if outside range
├── Consider market conditions
└── Remember: selling PE at discount is value-destructive
```

---

## 17.6 Rebalancing Approaches

### Why Rebalancing is Difficult

```
PE REBALANCING CHALLENGES
─────────────────────────

PUBLIC MARKETS:
├── Overweight stocks? → Sell stocks, buy bonds
├── Execution: Same day
├── Cost: Low (bps)
└── Precision: Exact

PRIVATE MARKETS:
├── Overweight PE? → ???
├── Cannot easily reduce PE exposure
├── Cannot easily increase PE quickly
└── Illiquidity is structural

OPTIONS TO REDUCE PE:
┌─────────────────────────────────────────────────────────┐
│ Option          │ Time      │ Cost      │ Feasibility │
│ ────────────────┼───────────┼───────────┼──────────── │
│ Wait for exits  │ Years     │ None      │ High        │
│ Secondary sale  │ Months    │ 10-20%    │ Medium      │
│ Stop new commits│ Years     │ None      │ High        │
│ GP-led recap    │ Months    │ Varies    │ Low         │
└─────────────────────────────────────────────────────────┘

OPTIONS TO INCREASE PE:
┌─────────────────────────────────────────────────────────┐
│ Option          │ Time      │ Cost      │ Feasibility │
│ ────────────────┼───────────┼───────────┼──────────── │
│ New commitments │ Years     │ J-curve   │ High        │
│ Secondary buys  │ Months    │ Premium?  │ Medium      │
│ Co-investments  │ Immediate │ Diligence │ Medium      │
└─────────────────────────────────────────────────────────┘
```

### Rebalancing Strategies

```
REBALANCING APPROACHES
──────────────────────

1. COMMITMENT-BASED REBALANCING
   └── Adjust new commitment pace
   └── Slow and indirect
   └── Lowest cost

   Example: Overweight by 3%
   ├── Reduce annual commitments by 30%
   └── Takes 2-3 years to normalize

2. SECONDARY MARKET REBALANCING
   └── Buy/sell existing positions
   └── Faster but costly
   └── Market timing risk

   Example: Sell $30M at 10% discount
   ├── Immediate exposure reduction
   └── Cost: $3M in discount

3. PUBLIC MARKET OFFSET
   └── Adjust public allocations
   └── Use public equity to manage total equity beta
   └── Indirect but practical

   Example: PE 3% overweight
   ├── Reduce public equity by 3%
   └── Total equity exposure maintained

4. DERIVATIVE OVERLAY (Advanced)
   └── Use futures/swaps on public equity
   └── Hedge PE market exposure
   └── Complex, requires expertise
```

### Allocation Ranges and Bands

```
ALLOCATION BAND FRAMEWORK
─────────────────────────

Instead of: "Target 15% PE allocation"
Use: "Target 15% PE with 12-18% range"

┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ALLOCATION BANDS                                       │
│                                                         │
│  ◄─ Minimum ─┼─── Target ───┼─ Maximum ─►             │
│      12%         15%            18%                    │
│                                                         │
│  Below 12%: Accelerate commitments, consider secondary │
│  12-18%: Normal operations                             │
│  Above 18%: Reduce commitments, consider secondary sale│
│                                                         │
│  REBALANCE TRIGGERS:                                    │
│  ├── >2% deviation from target for 2+ quarters        │
│  ├── Breach of min/max bands                          │
│  └── Significant market dislocation                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 17.7 Summary

### Portfolio Construction Checklist

```
PE PORTFOLIO CONSTRUCTION CHECKLIST
───────────────────────────────────

PLANNING:
□ Define target allocation (NAV-based)
□ Set allocation range (e.g., +/- 3%)
□ Build pacing model with realistic assumptions
□ Determine overcommitment ratio

DIVERSIFICATION:
□ Vintage year targets (no single year >25%)
□ Strategy mix aligned with objectives
□ Geographic allocation defined
□ Manager concentration limits

MONITORING:
□ Quarterly exposure tracking
□ Annual pacing model update
□ Commitment vs exposure reconciliation
□ Denominator effect monitoring

REBALANCING:
□ Commitment pace adjustment triggers
□ Secondary market utilization policy
□ Public market offset approach
□ Emergency liquidity procedures
```

### Key Formulas

| Metric | Formula |
|--------|---------|
| Overcommitment Ratio | Total Commitments / Target NAV |
| Exposure | Current NAV |
| Unfunded Ratio | Unfunded / Total Commitments |
| Vintage Concentration | Single Vintage NAV / Total PE NAV |
| Allocation | PE NAV / Total Portfolio |

---

## Knowledge Check

1. Why must investors "overcommit" to reach their target PE allocation?
2. What are the key inputs to a pacing model?
3. Why is vintage diversification important?
4. How does the denominator effect impact PE allocations?
5. What are the options for rebalancing an overweight PE position?

<details>
<summary>Answers</summary>

1. Because PE capital is called gradually over 3-5 years, committing only the target amount results in actual exposure well below target. Overcommitting (typically 1.5-2x target) accounts for the delay between commitment and deployment, allowing actual NAV to reach the target level.

2. Key inputs: current PE NAV, unfunded commitments, total portfolio size, target allocation, expected contribution rates, expected distribution rates, expected appreciation rates, and time horizon.

3. Vintage year returns vary dramatically based on market entry/exit timing. Diversifying across vintages reduces the impact of committing heavily in a poor vintage year and smooths overall program returns.

4. When public markets decline, PE NAV typically doesn't adjust immediately (lag effect), causing PE allocation to rise as a percentage of a smaller total portfolio. This can push allocations above targets without any action by the LP.

5. Options include: (1) reduce new commitments (slow, no cost), (2) sell positions in secondary market (faster, 10-20% discount), (3) wait for natural distributions (no cost, uncertain timing), (4) offset via public market allocations.

</details>

---

## Exercise: Build a Simple Pacing Model

```
SCENARIO: New PE Program

Starting conditions:
├── Total portfolio: $500M
├── Current PE NAV: $0
├── Target allocation: 12% ($60M)
├── Annual commitment budget: $25M
├── Assume 30% of unfunded called per year
├── Assume 15% annual NAV appreciation
├── Assume 10% of NAV distributed per year (starting Year 3)

Build a 5-year projection:
1. Year-end NAV for years 1-5
2. PE allocation % each year
3. When do you reach target?
4. What overcommitment ratio do you need?
```

<details>
<summary>Answers</summary>

```
PACING MODEL SOLUTION:

Year 0: Commit $25M

Year 1:
├── Starting NAV: $0
├── Contributions: $25M × 30% = $7.5M
├── Appreciation: $7.5M × 15% × 0.5 = $0.6M (half-year)
├── Distributions: $0
├── Ending NAV: $8.1M
├── Allocation: $8.1M / $500M = 1.6%
└── Unfunded: $17.5M

Year 2 (commit another $25M):
├── Starting NAV: $8.1M
├── Contributions: $42.5M × 30% = $12.75M
├── Appreciation: ($8.1M + $6.4M avg) × 15% = $2.2M
├── Distributions: $0
├── Ending NAV: $23.0M
├── Allocation: $23.0M / $500M = 4.6%
└── Total committed: $50M, Unfunded: $27M

Year 3 (commit another $25M):
├── Starting NAV: $23.0M
├── Contributions: $52M × 30% = $15.6M
├── Appreciation: ~$5M
├── Distributions: $23M × 10% = $2.3M
├── Ending NAV: $41.3M
├── Allocation: 8.3%
└── Total committed: $75M, Unfunded: $36.4M

Year 4:
├── Ending NAV: ~$55M
├── Allocation: 11%

Year 5:
├── Ending NAV: ~$65M
├── Allocation: 13% ✓ TARGET REACHED

OVERCOMMITMENT RATIO AT YEAR 5:
Total committed: $125M
Target NAV: $60M
Ratio: 125/60 = 2.1x

Note: With $25M/year commitments, reach ~12% in Year 5.
To reach target faster, would need $30-35M/year.
```

</details>

---

[← Module 16: Fund Financing](16-fund-financing.md) | [Module 18: Benchmarking & Data →](18-benchmarking-data.md)

[← Back to Curriculum Overview](00-curriculum-overview.md)
