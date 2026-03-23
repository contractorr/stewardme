# Module 08: NAV & Valuation

## Learning Objectives

By the end of this module, you will understand:
- What NAV represents and how it's calculated
- The fair value hierarchy (Levels 1, 2, 3)
- Common valuation methodologies
- How valuations impact reported performance
- Valuation governance and controls
- Signs of aggressive vs conservative valuation

---

## 8.1 What is NAV?

### Definition

**Net Asset Value (NAV)** is the total value of a fund's assets minus its liabilities. For an LP, their NAV represents their current estimated value in the fund.

### NAV Formula

```
FUND NAV CALCULATION
────────────────────

       Portfolio Investments (at Fair Value)
     + Cash and Cash Equivalents
     + Other Assets (receivables, etc.)
     - Liabilities (debt, payables, accruals)
     - Accrued Carried Interest
     ─────────────────────────────────────────
     = NET ASSET VALUE (NAV)

LP NAV = Fund NAV × LP Ownership %
```

### NAV Components Example

```
FUND NAV BREAKDOWN
──────────────────

ABC Partners Fund VII
As of December 31, 2024

ASSETS
├── Investments at Fair Value      $1,850,000,000
├── Cash and Equivalents              $75,000,000
├── Interest Receivable                $3,500,000
├── Dividends Receivable               $1,200,000
├── Other Assets                       $2,300,000
└── TOTAL ASSETS                   $1,932,000,000

LIABILITIES
├── Subscription Line Balance         $50,000,000
├── Accrued Expenses                   $8,500,000
├── Management Fee Payable             $7,500,000
├── Accrued Carried Interest         $142,000,000
├── Other Liabilities                  $4,000,000
└── TOTAL LIABILITIES                $212,000,000

NET ASSET VALUE                    $1,720,000,000

LP SHARE (2.5% ownership):
$1,720,000,000 × 2.5% = $43,000,000
```

---

## 8.2 The Fair Value Hierarchy

### ASC 820 / IFRS 13 Framework

Accounting standards require classifying investments by the reliability of inputs used in valuation:

```
FAIR VALUE HIERARCHY
────────────────────

┌─────────────────────────────────────────────────────────────┐
│  LEVEL 1: QUOTED PRICES IN ACTIVE MARKETS                   │
│  ──────────────────────────────────────────                 │
│  • Public stock prices                                      │
│  • Exchange-traded securities                               │
│  • Most reliable / objective                                │
│  • Rarely used in PE (investments are private)              │
│                                                             │
│  Reliability: ████████████████████████████████ HIGHEST      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  LEVEL 2: OBSERVABLE INPUTS                                 │
│  ──────────────────────────────────────────                 │
│  • Comparable public company multiples                      │
│  • Recent transaction prices (similar assets)               │
│  • Dealer quotes for similar instruments                    │
│  • Moderately reliable                                      │
│                                                             │
│  Reliability: ████████████████████░░░░░░░░░░ MODERATE       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  LEVEL 3: UNOBSERVABLE INPUTS                               │
│  ──────────────────────────────────────────                 │
│  • Internal models and assumptions                          │
│  • Management estimates                                     │
│  • DCF with projected cash flows                            │
│  • Most PE investments fall here                            │
│                                                             │
│  Reliability: ████████░░░░░░░░░░░░░░░░░░░░░░ LOWEST         │
└─────────────────────────────────────────────────────────────┘

TYPICAL PE FUND BREAKDOWN:
Level 1:  5%  (post-IPO holdings, public securities)
Level 2: 15%  (recent transactions, liquid comparables)
Level 3: 80%  (most portfolio companies)
```

### Why Level 3 Dominates PE

Private companies don't have market prices, so valuation requires:
- Selecting comparable companies
- Choosing appropriate multiples
- Making adjustments for differences
- Projecting future performance
- Applying discounts for illiquidity

All of these involve **judgment** = Level 3.

---

## 8.3 Valuation Methodologies

### Primary Methods

```
VALUATION METHODS OVERVIEW
──────────────────────────

1. MARKET APPROACH
   ├── Comparable Company Analysis ("Comps")
   ├── Precedent Transaction Analysis
   └── Recent Financing/Transaction Price

2. INCOME APPROACH
   └── Discounted Cash Flow (DCF)

3. COST APPROACH
   └── Cost basis (used for recent investments)

TYPICAL USAGE:
• Buyout: Market approach (EV/EBITDA multiples)
• VC: Recent round price, milestone-based
• Real Estate: Income approach (Cap rates, DCF)
• Credit: DCF on expected cash flows
```

### Comparable Company Analysis

```
COMPARABLE COMPANY VALUATION
────────────────────────────

STEP 1: IDENTIFY COMPARABLE COMPANIES
Select public companies with similar:
• Industry/business model
• Size (revenue, EBITDA)
• Growth profile
• Geography
• Risk characteristics

STEP 2: CALCULATE THEIR MULTIPLES
┌────────────────────────────────────────────────────────┐
│ Company          │ EV/EBITDA │ EV/Revenue │ P/E       │
├──────────────────┼───────────┼────────────┼───────────┤
│ Public Comp A    │   10.5x   │    2.8x    │   22.0x   │
│ Public Comp B    │   11.2x   │    3.1x    │   24.5x   │
│ Public Comp C    │    9.8x   │    2.5x    │   19.0x   │
│ Public Comp D    │   10.8x   │    2.9x    │   21.5x   │
├──────────────────┼───────────┼────────────┼───────────┤
│ Median           │   10.6x   │    2.85x   │   21.8x   │
└────────────────────────────────────────────────────────┘

STEP 3: APPLY TO PORTFOLIO COMPANY
Portfolio Company EBITDA: $25M
Comparable Median Multiple: 10.6x
Implied Enterprise Value: $265M

STEP 4: ADJUST
Less: Net Debt: ($80M)
Equity Value: $185M

STEP 5: APPLY DISCOUNTS
Illiquidity Discount (15%): ($28M)
Control Premium Adjustment: +$10M
FAIR VALUE: $167M
```

### Discounted Cash Flow (DCF)

```
DCF VALUATION
─────────────

STEP 1: PROJECT FREE CASH FLOWS
Year        1      2      3      4      5   Terminal
FCF ($M)   $15    $18    $22    $26    $30    $315

STEP 2: DETERMINE DISCOUNT RATE (WACC)
Cost of Equity:     15%
Cost of Debt:       7%
Tax Rate:           25%
Debt/Equity:        40/60
WACC: (60% × 15%) + (40% × 7% × (1-25%)) = 11.1%

STEP 3: DISCOUNT CASH FLOWS
           FCF      Discount Factor    Present Value
Year 1    $15M     0.900              $13.5M
Year 2    $18M     0.810              $14.6M
Year 3    $22M     0.729              $16.0M
Year 4    $26M     0.656              $17.1M
Year 5    $30M     0.591              $17.7M
Terminal  $315M    0.591              $186.2M
─────────────────────────────────────────────────
Enterprise Value                       $265.1M

STEP 4: BRIDGE TO EQUITY
Enterprise Value:    $265.1M
Less: Net Debt:      ($80.0M)
Equity Value:        $185.1M
```

### Recent Transaction Price

```
TRANSACTION-BASED VALUATION
───────────────────────────

Used when:
• Recent financing round occurred
• M&A transaction for similar company
• Less than 6-12 months old
• No material changes since transaction

EXAMPLE:
Series C funding round (6 months ago):
• Pre-money valuation: $150M
• Investment: $30M
• Post-money valuation: $180M

Current Valuation Assessment:
• Business on track? Yes
• Material changes? No significant
• Market conditions? Stable
• Fair Value: $180M (transaction price)

ADJUSTMENTS NEEDED IF:
• Performance above/below expectations
• Material business developments
• Significant time elapsed
• Market conditions changed
```

---

## 8.4 Valuation Adjustments

### Common Adjustments

```
VALUATION ADJUSTMENTS
─────────────────────

DISCOUNTS (Reduce Value)
├── Illiquidity Discount: 10-30%
│   └── Private shares can't be easily sold
├── Minority Discount: 15-25%
│   └── No control over company decisions
├── Marketability Discount: 10-20%
│   └── No ready market for shares
└── Key Person Discount: 5-15%
    └── Dependence on specific individuals

PREMIUMS (Increase Value)
├── Control Premium: 20-40%
│   └── Ability to control company decisions
├── Strategic Premium: 10-30%
│   └── Synergies with acquirer
└── Scarcity Premium: 5-15%
    └── Unique asset with limited supply

EXAMPLE APPLICATION:
Comparable public companies trade at 12x EBITDA
Portfolio company EBITDA: $20M
Implied value: $240M

Adjustments:
• Illiquidity discount (15%): -$36M
• Control premium (full control): +$48M
Adjusted Value: $252M
```

### Milestone-Based Adjustments (VC)

```
MILESTONE VALUATION (VENTURE)
─────────────────────────────

Last round valuation: $50M
Since then:

POSITIVE MILESTONES
├── Product launched              +20%
├── Revenue targets exceeded      +15%
├── Key partnership signed        +10%
└── Subtotal:                     +45%

NEGATIVE FACTORS
├── Key competitor emerged        -10%
├── Slower user growth            -5%
└── Subtotal:                     -15%

NET ADJUSTMENT:                   +30%
Updated Fair Value: $65M
```

---

## 8.5 Valuation Governance

### Who's Involved?

```
VALUATION GOVERNANCE STRUCTURE
──────────────────────────────

┌─────────────────────────────────────────────────────────────┐
│                    VALUATION COMMITTEE                       │
│  (GP senior partners, CFO, potentially external advisors)   │
│                                                             │
│  Responsibilities:                                          │
│  • Approve valuation policies                               │
│  • Review significant valuations                            │
│  • Ensure consistency                                       │
│  • Document rationale                                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  DEAL TEAM    │ │   FINANCE/    │ │   EXTERNAL    │
│               │ │  OPERATIONS   │ │   ADVISORS    │
│ • Proposes    │ │               │ │               │
│   valuations  │ │ • Reviews for │ │ • Independent │
│ • Provides    │ │   consistency │ │   valuations  │
│   company     │ │ • Applies     │ │ • Audit       │
│   updates     │ │   methodology │ │   review      │
└───────────────┘ └───────────────┘ └───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │     LPAC / AUDITORS           │
            │                               │
            │ • May review methodology      │
            │ • Auditors test valuations    │
            │ • Annual audit of fair value  │
            └───────────────────────────────┘
```

### Valuation Frequency

| Frequency | Typical Use | Notes |
|-----------|-------------|-------|
| **Quarterly** | Most PE funds | Required for LP reporting |
| **Annual** | Audited valuations | More rigorous review |
| **Transaction-driven** | When material events occur | IPO, sale, financing |

---

## 8.6 Valuation Bias

### Potential for Manipulation

```
WHY VALUATIONS CAN BE BIASED
────────────────────────────

GP INCENTIVES TO OVERVALUE:
├── Higher NAV = Better interim performance
├── Easier fundraising for next fund
├── Management fees on NAV (some funds)
├── Competitive rankings
└── Compensation tied to performance

GP INCENTIVES TO UNDERVALUE:
├── Exceed expectations at exit
├── Conservative reputation
├── Manage LP expectations
└── Reduce carried interest clawback risk

RESULT:
• Studies show slight upward bias on average
• Bias varies by GP and market conditions
• Exits typically within 5-15% of last mark
```

### Aggressive vs Conservative Valuation

```
VALUATION APPROACH SPECTRUM
───────────────────────────

AGGRESSIVE                              CONSERVATIVE
    │                                        │
    │  • Higher multiples                    │  • Lower multiples
    │  • Smaller discounts                   │  • Larger discounts
    │  • Optimistic projections              │  • Cautious projections
    │  • Quick mark-ups                      │  • Slow mark-ups
    │  • Slow write-downs                    │  • Quick write-downs
    │                                        │
    │         ◄─────────────────────►        │
    │                                        │
    │  RED FLAGS:                            │  SIGNS:
    │  • NAV >> exit prices                  │  • NAV << exit prices
    │  • Multiples above comps               │  • Multiples below comps
    │  • Few/no write-downs                  │  • Proactive write-downs
    │  • Rapid appreciation                  │  • Steady progression
    │                                        │
```

### How to Assess Valuation Quality

```
VALUATION QUALITY INDICATORS
────────────────────────────

POSITIVE SIGNS:
✓ Exit prices near or above last NAV
✓ Consistent methodology over time
✓ Independent valuation support
✓ Clear documentation of changes
✓ Write-downs when warranted
✓ Multiples in line with market

WARNING SIGNS:
⚠ Exits significantly below NAV
⚠ No write-downs in difficult markets
⚠ Methodology changes without explanation
⚠ Multiples significantly above comps
⚠ Lack of documentation
⚠ Aggressive revenue/EBITDA recognition

QUANTITATIVE CHECK:
              Exit Proceeds
Realization Ratio = ─────────────────────
                    NAV Before Exit

• Ratio > 1.0: Conservative (exits above marks)
• Ratio ≈ 1.0: Accurate (exits at marks)
• Ratio < 1.0: Aggressive (exits below marks)
```

---

## 8.7 NAV in LP Reports

### Capital Account NAV

```
NAV IN CAPITAL ACCOUNT
──────────────────────

Your capital account "Closing Balance" = Your NAV

COMPONENTS THAT AFFECT NAV:
+ Contributions (increases NAV)
- Distributions (decreases NAV)
+ Income (interest, dividends)
- Expenses (fees, costs)
+ Realized gains (crystallizes value)
+ Unrealized gains (mark-to-market increases)
- Realized losses
- Unrealized losses (mark-to-market decreases)
- Accrued carried interest

EXAMPLE MOVEMENT:
Opening NAV:           $45,000,000
+ Contributions:               $0
- Distributions:       ($2,500,000)
+ Net Income:             $150,000
- Expenses:              ($175,000)
+ Realized Gains:       $1,800,000
+ Unrealized Gains:     $2,200,000
- Accrued Carry:         ($475,000)
────────────────────────────────────
Closing NAV:           $46,000,000
```

### Schedule of Investments

```
SCHEDULE OF INVESTMENTS (SOI)
─────────────────────────────

The SOI shows each investment's contribution to NAV:

ABC Partners Fund VII
Schedule of Investments
December 31, 2024

                                              Fair         % of
Investment        Industry    Cost           Value        NAV
────────────────────────────────────────────────────────────────
TechCo Holdings   Software    $85M          $145M        8.4%
DataSoft Inc      SaaS        $62M          $98M         5.7%
ManuCorp          Industrial  $78M          $102M        5.9%
HealthPlus        Healthcare  $95M          $125M        7.3%
RetailMax         Consumer    $55M          $72M         4.2%
... (20 more investments)
────────────────────────────────────────────────────────────────
Total Investments             $1,450M       $1,850M      100%

Additional Info:
• Geographic breakdown
• Industry breakdown
• Valuation methodology notes
• Level 3 assumptions
```

---

## 8.8 Special Valuation Situations

### Write-Downs

```
WRITE-DOWN SCENARIOS
────────────────────

TRIGGERS FOR WRITE-DOWN:
├── Company missing performance targets
├── Loss of key customer/contract
├── Adverse market conditions
├── Competitive deterioration
├── Management issues
├── Liquidity problems
└── Industry downturn

WRITE-DOWN EXAMPLE:
Original investment: $50M (Year 1)
Year 2 NAV: $55M (10% appreciation)
Year 3: Company loses major customer
Year 3 NAV: $35M (36% write-down)
Year 4: Sold for $30M (realized loss of $20M)

IMPACT:
• NAV decreases
• TVPI decreases
• IRR decreases
• Unrealized loss becomes realized at exit
```

### Write-Ups

```
WRITE-UP SCENARIOS
──────────────────

TRIGGERS FOR WRITE-UP:
├── Strong financial performance
├── New funding round at higher valuation
├── Strategic developments
├── Market comparable expansion
├── Path to exit becomes clearer
└── Industry tailwinds

WRITE-UP EXAMPLE:
Original investment: $50M (Year 1)
Year 2: Company exceeds targets, market multiples expand
Year 2 NAV: $75M (50% appreciation)
Year 3: Preparing for exit
Year 3 NAV: $95M
Year 4: Sold for $100M (realized gain of $50M)

NOTE:
Write-ups based on NAV don't mean anything
until the investment is actually sold.
```

### Impairment vs Full Write-Off

```
DEGREES OF WRITE-DOWN
─────────────────────

PARTIAL IMPAIRMENT:
• Value reduced but company viable
• Expected to recover some value
• NAV marked down 20-80%

FULL WRITE-OFF:
• Company failed or will fail
• No expected recovery
• NAV = $0 or nominal amount
• May still hold legal position

EXAMPLE FUND PORTFOLIO:
20 investments total
├── 12 performing (NAV > cost)
├── 5 partially impaired (NAV < cost, > 0)
├── 2 fully written off (NAV = 0)
└── 1 exited above cost
```

---

## 8.9 Summary

### Key Concepts

```
NAV & VALUATION KEY POINTS
──────────────────────────

1. NAV = Assets - Liabilities
   └── LP NAV = Fund NAV × Ownership %

2. Most PE valuations are Level 3
   └── Rely on judgment and estimates

3. Common methods:
   ├── Comparable companies (market approach)
   ├── DCF (income approach)
   └── Recent transactions

4. Adjustments include:
   ├── Illiquidity discounts
   ├── Control premiums
   └── Market condition adjustments

5. Governance matters:
   ├── Valuation committees
   ├── Independent review
   └── Audit oversight

6. Watch for bias:
   ├── Compare exits to prior marks
   ├── Look for appropriate write-downs
   └── Compare to market conditions
```

---

## Knowledge Check

1. What does Level 3 in the fair value hierarchy mean?
2. Why are most PE investments classified as Level 3?
3. What is an illiquidity discount and why is it applied?
4. How can you tell if a GP's valuations are aggressive?
5. What happens to NAV when a portfolio company is written down?

<details>
<summary>Answers</summary>

1. Level 3 means valuations rely on unobservable inputs - internal models, management estimates, and assumptions rather than market prices
2. Private companies don't have quoted market prices, so valuations require judgment about comparable multiples, growth projections, and discounts
3. An illiquidity discount (typically 10-30%) reduces value because private shares can't be easily sold like public securities
4. Signs include: exit prices significantly below last NAV, no write-downs during market stress, multiples above comparable companies, lack of documentation
5. NAV decreases by the amount of the write-down, which reduces TVPI, RVPI, and IRR

</details>

---

## Next Module

[Module 09: Fee Structures →](09-fee-structures.md)

Understanding management fees, carried interest, and other fund economics.
