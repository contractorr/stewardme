# Module 07: Performance Metrics

## Learning Objectives

By the end of this module, you will understand:
- How IRR is calculated and interpreted
- The difference between gross and net IRR
- What TVPI, DPI, and RVPI measure
- How to use metrics together for complete assessment
- PME benchmarking methodology
- Common pitfalls in performance measurement

---

## 7.1 Overview of Performance Metrics

### The Core Metrics

```
┌─────────────────────────────────────────────────────────────────┐
│                 PRIVATE EQUITY PERFORMANCE METRICS               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIME-WEIGHTED                    MONEY-WEIGHTED                │
│  ────────────                     ──────────────                │
│                                                                 │
│  IRR (Internal Rate              TVPI (Total Value to          │
│       of Return)                      Paid-In)                  │
│  • Annualized return             • Total return multiple        │
│  • Accounts for timing           • Ignores timing               │
│  • Most common metric            • Easy to understand           │
│                                                                 │
│                                  DPI (Distributions to          │
│                                       Paid-In)                  │
│                                  • Realized return              │
│                                  • "Cash on cash"               │
│                                                                 │
│                                  RVPI (Residual Value to        │
│                                        Paid-In)                 │
│                                  • Unrealized return            │
│                                  • Value still in fund          │
│                                                                 │
│                                                                 │
│  RELATIONSHIP: TVPI = DPI + RVPI                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Why Multiple Metrics?

| Metric | Answers | Limitation |
|--------|---------|------------|
| **IRR** | "What's my annualized return?" | Sensitive to timing, can be manipulated |
| **TVPI** | "How much total value was created?" | Doesn't show timing or realization |
| **DPI** | "How much cash have I received?" | Ignores unrealized value |
| **RVPI** | "How much is still invested?" | Subject to valuation uncertainty |

**Best practice**: Use IRR and TVPI together, with DPI/RVPI context.

---

## 7.2 IRR (Internal Rate of Return)

### Definition

**IRR** is the discount rate that makes the Net Present Value (NPV) of all cash flows equal to zero.

### The IRR Formula

For cash flows C₀, C₁, C₂, ... Cₙ at times t₀, t₁, t₂, ... tₙ:

```
              C₁           C₂                 Cₙ
C₀ + ──────────────── + ──────────────── + ... + ──────────────── = 0
     (1 + IRR)^(t₁-t₀)  (1 + IRR)^(t₂-t₀)      (1 + IRR)^(tₙ-t₀)
```

**Convention**:
- Contributions (outflows) are **negative**
- Distributions (inflows) are **positive**
- NAV at end is treated as a final positive cash flow

### IRR Calculation Example

```
SIMPLE IRR EXAMPLE
──────────────────

Cash Flows:
Year 0: -$100M  (investment)
Year 5: +$200M  (exit)

Find IRR where:
-100 + 200/(1+IRR)^5 = 0

200/(1+IRR)^5 = 100
(1+IRR)^5 = 2
1+IRR = 2^(1/5)
1+IRR = 1.1487
IRR = 14.87%

VERIFICATION:
-100 + 200/(1.1487)^5 = -100 + 200/2.0 = -100 + 100 = 0 ✓
```

### Complex IRR Example

```
MULTI-PERIOD IRR EXAMPLE
────────────────────────

Date          Cash Flow    Description
──────────    ─────────    ───────────
Jan 1, 2020   -$20M        First call
Jul 1, 2020   -$15M        Second call
Jan 1, 2021   -$25M        Third call
Jul 1, 2021   +$10M        First distribution
Jan 1, 2022   -$10M        Fourth call
Jan 1, 2023   +$30M        Distribution
Jan 1, 2024   +$45M        Final distribution + NAV

Total Out: $70M
Total In:  $85M
Multiple: 1.21x

IRR CALCULATION:
Solve iteratively (no closed-form solution)

Using financial calculator or Excel XIRR:
IRR = 11.8%

This means a 11.8% annualized return accounting for
all the timing of contributions and distributions.
```

### Gross vs Net IRR

```
GROSS VS NET IRR
────────────────

GROSS IRR:
• Calculated BEFORE fees and carry
• Shows investment performance
• Used to evaluate GP skill
• What the portfolio returned

NET IRR:
• Calculated AFTER fees and carry
• What LP actually receives
• Most important for LP
• Usually 2-5% lower than gross

EXAMPLE:
Fund Performance:
• Gross IRR: 22%
• Less: Management fee drag: ~2%
• Less: Carried interest: ~3%
• Net IRR: 17%

Spread depends on:
• Fee level
• Fund size and deployment
• Return level (higher returns = more carry)
```

### IRR Sensitivities

```
FACTORS AFFECTING IRR
─────────────────────

TIMING (Most Important)
├── Earlier distributions = Higher IRR
├── Later contributions = Higher IRR
├── Subscription lines can boost early IRR
└── Same multiple, different IRR based on timing

EXAMPLE - SAME 2.0x MULTIPLE:
                        IRR
Scenario A: Exit in Year 3      26%
Scenario B: Exit in Year 5      15%
Scenario C: Exit in Year 7      10%

CONTRIBUTION TIMING:
Early deployment → Lower IRR (J-curve)
Late deployment → Higher IRR (less time)

DISTRIBUTION TIMING:
Early exits → Higher IRR
Late exits → Lower IRR
```

---

## 7.3 TVPI (Total Value to Paid-In)

### Definition

**TVPI** measures total value created relative to capital invested.

### Formula

```
         Distributions + NAV
TVPI = ────────────────────────
           Paid-In Capital
```

Or equivalently:

```
TVPI = DPI + RVPI
```

### TVPI Example

```
TVPI CALCULATION
────────────────

LP Investment in Fund:
• Commitment: $50M
• Called (Paid-In): $45M
• Distributed: $35M
• Current NAV: $40M

        $35M + $40M
TVPI = ─────────────
           $45M

TVPI = $75M / $45M = 1.67x

INTERPRETATION:
For every $1 invested, LP has received or
holds $1.67 in value (67% gain).
```

### TVPI Ranges

| TVPI | Interpretation |
|------|---------------|
| < 1.0x | Loss (haven't recovered cost) |
| 1.0x | Breakeven |
| 1.0-1.5x | Below average return |
| 1.5-2.0x | Good return |
| 2.0-2.5x | Strong return |
| 2.5-3.0x | Excellent return |
| > 3.0x | Exceptional return |

---

## 7.4 DPI (Distributions to Paid-In)

### Definition

**DPI** measures cash actually returned relative to capital invested.

### Formula

```
       Cumulative Distributions
DPI = ──────────────────────────
          Paid-In Capital
```

### DPI Example

```
DPI CALCULATION
───────────────

From previous example:
• Paid-In: $45M
• Distributed: $35M

        $35M
DPI = ────────
        $45M

DPI = 0.78x

INTERPRETATION:
LP has received back 78% of invested capital
in actual cash distributions.
```

### Why DPI Matters

```
DPI: "CASH ON CASH"
───────────────────

DPI shows REALIZED returns:
• Actual money in pocket
• No valuation subjectivity
• Truly returned capital

DPI MILESTONES:
< 0.5x  →  Early stage, few exits
0.5-1.0x → Returning capital, some gains
1.0x    →  BREAKEVEN - all money back
> 1.0x  →  All original capital + profits returned
> 1.5x  →  Strong realized returns
```

---

## 7.5 RVPI (Residual Value to Paid-In)

### Definition

**RVPI** measures unrealized value relative to capital invested.

### Formula

```
         Net Asset Value (NAV)
RVPI = ─────────────────────────
          Paid-In Capital
```

### RVPI Example

```
RVPI CALCULATION
────────────────

From previous example:
• Paid-In: $45M
• NAV: $40M

        $40M
RVPI = ────────
        $45M

RVPI = 0.89x

INTERPRETATION:
LP still holds 89% of original investment
value in unrealized positions.
```

### RVPI Considerations

```
RVPI RELIABILITY
────────────────

HIGH RVPI (>0.5x):
• Significant unrealized value
• Subject to valuation uncertainty
• Could go up or down
• Not yet "locked in"

LOW RVPI (<0.3x):
• Most value realized
• Returns more certain
• Fund nearly complete
• Less valuation risk

RVPI OVER FUND LIFE:

Year:   1    2    3    4    5    6    7    8    9   10
RVPI: 0.95 0.95 0.90 0.80 0.65 0.50 0.35 0.20 0.08 0.00
        ▲                                            ▲
     Early (all NAV)                          Late (all cash)
```

---

## 7.6 The TVPI = DPI + RVPI Relationship

### The Fundamental Identity

```
TVPI = DPI + RVPI (Always)

This must hold true for any valid set of metrics.

EXAMPLE:
TVPI = 1.67x
DPI = 0.78x
RVPI = 0.89x

CHECK: 0.78 + 0.89 = 1.67 ✓
```

### Evolution Over Fund Life

```
TVPI/DPI/RVPI OVER TIME
───────────────────────

Year  TVPI   DPI    RVPI   % Realized
────  ────   ────   ────   ──────────
  1   0.90   0.00   0.90      0%
  2   0.95   0.00   0.95      0%
  3   1.10   0.10   1.00      9%
  4   1.25   0.25   1.00     20%
  5   1.40   0.45   0.95     32%
  6   1.55   0.70   0.85     45%
  7   1.65   1.00   0.65     61%
  8   1.70   1.25   0.45     74%
  9   1.73   1.50   0.23     87%
 10   1.75   1.75   0.00    100%

OBSERVATION:
• TVPI grows over time (value creation)
• DPI grows as exits occur
• RVPI shrinks as portfolio is liquidated
• % Realized increases toward 100%
```

### Visual Representation

```
                    TVPI COMPOSITION OVER TIME
                    ──────────────────────────

         │
    2.0x │                              ┌─────────────────
         │                         ┌────┤     DPI
    1.5x │                    ┌────┤    │ (Realized)
         │               ┌────┤    │    │
    1.0x │          ┌────┤    │    │    │
         │     ┌────┤    │    │    │    │
    0.5x │┌────┤    │    │    │    │    │
         ││ R  │ R  │ R  │ R  │ R  │ R  │
    0.0x │└────┴────┴────┴────┴────┴────┴─────────────────
         └────────────────────────────────────────────────►
           Y1   Y2   Y3   Y4   Y5   Y6   Y7   Y8   Y9   Y10

         R = RVPI (Unrealized)    Upper section = DPI (Realized)
```

---

## 7.7 Using Metrics Together

### Complete Performance Picture

```
METRIC INTERPRETATION FRAMEWORK
───────────────────────────────

HIGH IRR + HIGH TVPI:
✓ Strong returns
✓ Good value creation
✓ Efficient capital deployment
Example: IRR 25%, TVPI 2.2x → Excellent fund

HIGH IRR + LOW TVPI:
⚠ Check for subscription line usage
⚠ May have early exits, low total value
⚠ Timing manipulation possible
Example: IRR 30%, TVPI 1.3x → Investigate

LOW IRR + HIGH TVPI:
⚠ Slow deployment or late exits
⚠ Value created but timing poor
⚠ May still be good outcome
Example: IRR 10%, TVPI 2.0x → Long hold periods

LOW IRR + LOW TVPI:
✗ Poor performance
✗ Both timing and value weak
Example: IRR 5%, TVPI 1.1x → Underperforming
```

### DPI vs RVPI Assessment

```
REALIZATION ANALYSIS
────────────────────

HIGH DPI (>1.0x):
• Significant cash returned
• Returns more certain
• Less valuation risk
• Fund mature

HIGH RVPI (>0.8x):
• Most value unrealized
• Subject to market changes
• Valuation uncertainty
• Fund less mature

HEALTHY PROGRESSION:
Early Fund: DPI low, RVPI high → Normal
Mid Fund:   DPI growing, RVPI stable → Good
Late Fund:  DPI high, RVPI low → Normal

WARNING SIGNS:
Late Fund: DPI low, RVPI high → Why no exits?
Any Time:  RVPI declining without DPI growth → Write-downs
```

### Metric Dashboard Example

```
═══════════════════════════════════════════════════════════════
           FUND PERFORMANCE DASHBOARD
           ABC Partners Fund VII
           As of December 31, 2024
═══════════════════════════════════════════════════════════════

OVERVIEW
────────────────────────────────────────────────────────────────
Vintage Year:        2019          Fund Age:        6 years
Fund Size:           $2.0B         Called:          $1.85B
Strategy:            Buyout        Invested:        $1.72B

PERFORMANCE METRICS
────────────────────────────────────────────────────────────────
                    Gross       Net        Benchmark (Median)
                    ─────       ───        ──────────────────
IRR                 21.5%      17.2%           14.5%
TVPI                1.82x      1.64x           1.52x
DPI                 0.95x      0.85x           0.72x
RVPI                0.87x      0.79x           0.80x

QUARTILE RANKING
────────────────────────────────────────────────────────────────
Net IRR:            1st Quartile (Top 25%)
Net TVPI:           1st Quartile (Top 25%)

MATURITY
────────────────────────────────────────────────────────────────
% Realized:         52% (DPI/TVPI)
% Called:           93% (Called/Commitment)
Status:             Mature - Active harvesting phase

PME ANALYSIS
────────────────────────────────────────────────────────────────
vs S&P 500:         1.18x (outperformed by 18%)
vs Russell 2000:    1.25x (outperformed by 25%)
═══════════════════════════════════════════════════════════════
```

---

## 7.8 Gross vs Net Calculations

### Fee Impact on Returns

```
GROSS TO NET BRIDGE
───────────────────

GROSS PERFORMANCE (Before fees)
├── Represents portfolio return
├── Used to evaluate investment skill
└── What the investments generated

Minus:
├── Management fees (~1.5-2% annually)
├── Fund expenses (~0.1-0.2% annually)
└── Carried interest (~20% of profits)

Equals:
NET PERFORMANCE (After fees)
├── What LP actually receives
├── Most important metric for LPs
└── Basis for benchmarking

EXAMPLE CALCULATION:
─────────────────────
Gross IRR:           22.0%
Management fee drag:  -1.8%
Expense drag:        -0.2%
Carry drag:          -2.5%
─────────────────────────────
Net IRR:             17.5%

Fee drag is higher when:
• Returns are higher (more carry)
• Fund is smaller (fees as % of returns)
• Deployment is slower (fees on uncalled)
```

### Gross to Net Multiple

```
TVPI GROSS TO NET
─────────────────

Gross TVPI: 2.0x

Fee Calculation (simplified):
• Management fees (10 years × 1.5%): ~15% of commitment
• Carry (20% of profits above hurdle): ~16% of profits

Gross Value:     $200M (2.0x on $100M)
Less Fees:       ($15M)
Less Carry:      (~$17M) [20% × ($200-$100-$15)]
Net Value:       $168M

Net TVPI:        1.68x

Gross-to-Net Ratio: 1.68/2.0 = 84%
```

---

## 7.9 PME (Public Market Equivalent)

### Why PME?

Private equity should beat public markets to justify:
- Illiquidity (10+ year lockup)
- Risk concentration
- Higher fees
- Complexity

### PME Methodologies

| Method | Description | Use Case |
|--------|-------------|----------|
| **Kaplan-Schoar PME** | Standard, intuitive | Most common |
| **Long-Nickels PME** | Adjusts for leverage | Buyout funds |
| **Direct Alpha** | Shows return spread | Quantifying value-add |
| **mPME** | Modified for NAV timing | Addresses biases |

### Kaplan-Schoar PME Calculation

```
KAPLAN-SCHOAR PME
─────────────────

For each cash flow, calculate what investing
in the index would have returned:

Future Value of Contributions:
FV(Contributions) = Σ [Contribution × (Index_end / Index_at_contribution)]

Future Value of Distributions:
FV(Distributions) = Σ [Distribution × (Index_end / Index_at_distribution)]

                    Distributions + NAV
PME = ─────────────────────────────────────────────────
      FV(Contributions) - FV(Distributions) + NAV_public

Where NAV_public = what public portfolio would be worth

SIMPLIFIED:
If PME > 1.0: Fund outperformed public markets
If PME < 1.0: Fund underperformed public markets
If PME = 1.0: Fund matched public markets
```

### PME Example

```
PME CALCULATION EXAMPLE
───────────────────────

Fund Cash Flows and S&P 500 Index:

Date         Flow      S&P 500   Index Return
─────────    ─────     ───────   ────────────
Jan 2020    -$100M     3,250     (base)
Jan 2021    -$50M      3,700     13.8%
Jan 2022    +$40M      4,500     21.6%
Jan 2023    +$80M      4,000     -11.1%
Dec 2024    +$120M     5,200     30.0%
            NAV: $30M

FUND PERFORMANCE:
Total In: $150M
Total Out: $270M (incl NAV)
TVPI: 1.80x
IRR: 16.2%

PUBLIC EQUIVALENT:
$100M invested Jan 2020 → $160M by Dec 2024 (60% gain)
$50M invested Jan 2021 → $70M by Dec 2024 (40% gain)
Distributions reinvested at S&P returns...

Public Portfolio Value: $225M (hypothetical)
TVPI equivalent: 1.50x

PME = 1.80 / 1.50 = 1.20

INTERPRETATION:
Fund generated 20% more value than public markets
16.2% IRR vs ~12% S&P equivalent = ~4% alpha
```

---

## 7.10 IRR Manipulation Concerns

### Subscription Line Impact

```
SUBSCRIPTION LINE IRR ENHANCEMENT
─────────────────────────────────

WITHOUT SUB LINE:
Year 0: Call $100M from LPs, invest immediately
Year 4: Exit for $180M
IRR: 15.8%

WITH SUB LINE:
Year 0: Borrow $100M from sub line, invest
Year 1: Call $100M from LPs, repay line
Year 4: Exit for $180M
IRR: 21.7%

SAME MULTIPLE (1.8x)
DIFFERENT IRR (+6% boost)

Why?
• LP cash outflow delayed by 1 year
• IRR formula rewards later contributions
• No actual improvement in investment returns
```

### Other IRR Considerations

| Issue | Description | Mitigation |
|-------|-------------|------------|
| **Sub lines** | Inflate early IRR | Look at multiple too |
| **Early exits** | Boost IRR on winners | Consider total value |
| **Selective realization** | Exit winners first | Look at RVPI quality |
| **Interim NAV** | Aggressive marks boost interim IRR | Wait for realizations |

### Best Practices

```
IRR EVALUATION BEST PRACTICES
─────────────────────────────

1. Always pair IRR with multiple (TVPI)
2. Ask about subscription line usage
3. Look at DPI for realized returns
4. Compare to same-vintage peers
5. Consider fund maturity
6. Request IRR without sub line impact
7. Focus on net (not gross) for LP returns
```

---

## 7.11 Summary: Metric Selection Guide

### Which Metric When?

| Question | Best Metric |
|----------|-------------|
| "What's the annualized return?" | IRR (Net) |
| "How much total value was created?" | TVPI |
| "How much cash have I received?" | DPI |
| "How much is still at risk?" | RVPI |
| "Did it beat public markets?" | PME |
| "How mature is the fund?" | DPI/TVPI ratio |

### Metric Quick Reference

```
METRIC CHEAT SHEET
──────────────────

IRR = Annualized return (time-weighted)
    • >20% = Excellent
    • 15-20% = Good
    • 10-15% = Average
    • <10% = Below average

TVPI = Total Value / Paid-In
    • >2.0x = Excellent
    • 1.5-2.0x = Good
    • 1.2-1.5x = Average
    • <1.2x = Below average

DPI = Distributions / Paid-In
    • >1.5x = Excellent realized
    • 1.0-1.5x = Good realized
    • <1.0x = Still returning capital

RVPI = NAV / Paid-In
    • High = More uncertainty
    • Low = More certain returns

PME = Fund TVPI / Public Equivalent
    • >1.15 = Clear outperformance
    • 1.0-1.15 = Modest outperformance
    • <1.0 = Underperformance
```

---

## Knowledge Check

1. If a fund has IRR of 18% and TVPI of 1.3x, what might explain the discrepancy?
2. A fund shows TVPI 1.6x, DPI 0.2x, RVPI 1.4x. What does this tell you?
3. What's the difference between gross and net IRR?
4. Why might you not trust a young fund's IRR?
5. What does PME of 1.25 mean?

<details>
<summary>Answers</summary>

1. High IRR with low multiple suggests fast returns but limited total value - could be early exits, short holding periods, or subscription line usage boosting IRR
2. The fund has created good total value (1.6x) but most is unrealized (1.4x RVPI = 88% unrealized). This is a young or slow-exiting fund with significant valuation risk.
3. Gross IRR is before fees and carry; Net IRR is after fees and carry. Net IRR is what LPs actually receive.
4. Young funds are in J-curve territory where fees create negative returns before investments appreciate. Also, NAV-based returns are unproven until realized.
5. The fund generated 25% more value than equivalent investment in public markets, suggesting meaningful outperformance.

</details>

---

## Calculation Exercise

```
Calculate all metrics for this fund:

Fund: Growth Partners VI
Commitment: $30,000,000
Called: $27,500,000
Distributed: $18,000,000
NAV: $28,000,000

Cash Flow Timeline:
2019: -$10M (call)
2020: -$10M (call)
2021: -$7.5M (call)
2022: +$5M (distribution)
2023: +$8M (distribution)
2024: +$5M (distribution)
End 2024: NAV = $28M
```

<details>
<summary>Answers</summary>

```
TVPI = (Distributions + NAV) / Called
     = ($18M + $28M) / $27.5M
     = $46M / $27.5M
     = 1.67x

DPI = Distributions / Called
    = $18M / $27.5M
    = 0.65x

RVPI = NAV / Called
     = $28M / $27.5M
     = 1.02x

CHECK: DPI + RVPI = 0.65 + 1.02 = 1.67 = TVPI ✓

% Realized = DPI / TVPI = 0.65 / 1.67 = 39%

IRR Calculation (using XIRR):
Cash flows: -10, -10, -7.5, +5, +8, +5+28
Years: 0, 1, 2, 3, 4, 5
IRR ≈ 14.8%

INTERPRETATION:
• Good total return (1.67x)
• Still early in realizations (39% realized)
• Healthy NAV position (1.02x RVPI)
• Decent IRR given 5-year timeframe
```

</details>

---

## Next Module

[Module 08: NAV & Valuation →](08-nav-valuation.md)

Understanding how private investments are valued and how NAV is calculated.
