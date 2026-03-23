# Module 16: Fund Financing

## Learning Objectives

By the end of this module, you will understand:
- Subscription credit facilities and their mechanics
- NAV lending and hybrid financing solutions
- Differences between fund-level and deal-level leverage
- Impact of fund financing on LP returns and reporting
- Risk considerations for LPs

---

## 16.1 Overview of Fund Financing

### What is Fund Financing?

**Fund financing** refers to credit facilities and loans obtained by PE funds to manage liquidity, enhance returns, and optimize capital efficiency.

```
FUND FINANCING LANDSCAPE
────────────────────────

                    FUND LEVEL                  DEAL LEVEL
                        │                           │
        ┌───────────────┼───────────────┐          │
        │               │               │          │
    ┌───┴───┐      ┌───┴───┐      ┌───┴───┐  ┌───┴───┐
    │Subscr.│      │  NAV  │      │Hybrid │  │Deal   │
    │Lines  │      │Lending│      │Facil. │  │Debt   │
    └───────┘      └───────┘      └───────┘  └───────┘
        │               │               │          │
    Backed by       Backed by       Both        Backed by
    LP Commits      Portfolio      Sources      Company
                    NAV                         Assets
```

### Market Size

```
FUND FINANCING MARKET ($B)
──────────────────────────

SUBSCRIPTION LINES:
2015: ████████████████ $400B
2018: ████████████████████████ $600B
2021: ████████████████████████████████ $800B
2023: ██████████████████████████████████ $900B+

NAV LENDING:
2015: ████ $20B
2018: ████████ $40B
2021: ████████████████ $80B
2023: ████████████████████████ $120B+

TREND: NAV lending fastest-growing segment
```

---

## 16.2 Subscription Credit Facilities

### How Subscription Lines Work

```
SUBSCRIPTION LINE MECHANICS
───────────────────────────

STRUCTURE:
┌──────────────────────────────────────────────────────────┐
│                          BANK                            │
│                           │                              │
│                      Credit Line                         │
│                           │                              │
│                           ▼                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │                      FUND                          │ │
│  │                                                    │ │
│  │  Unfunded LP Commitments = $500M                  │ │
│  │  Credit Line = $250M (50% of commitments)         │ │
│  │                                                    │ │
│  │  COLLATERAL: Right to call capital from LPs       │ │
│  └────────────────────────────────────────────────────┘ │
│                           │                              │
│                      Investments                         │
│                           │                              │
│                           ▼                              │
│                    Portfolio Cos                         │
└──────────────────────────────────────────────────────────┘

KEY TERMS:
├── Facility size: 25-50% of commitments
├── Pricing: SOFR + 150-250 bps
├── Maturity: 1-3 years (renewable)
├── Borrowing base: LP commitment quality
└── Covenants: Coverage ratios, diversification
```

### LP Credit Analysis

```
LP CREDITWORTHINESS TIERS
─────────────────────────

TIER 1 (100% borrowing base credit):
├── Sovereign wealth funds
├── Top-tier public pensions
├── Large insurance companies
├── Investment-grade corporations
└── Major endowments

TIER 2 (75-90% credit):
├── Smaller pensions
├── Regional insurance
├── Mid-tier family offices
├── Corporate pensions
└── Fund of funds

TIER 3 (50-75% credit):
├── Smaller endowments
├── Non-rated family offices
├── High-net-worth individuals
└── Certain foreign investors

EXCLUDED (0% credit):
├── Unverified investors
├── High-risk jurisdictions
├── Non-cooperative LPs
└── LPs in default
```

### Subscription Line Example

```
SUBSCRIPTION LINE TRANSACTION FLOW
──────────────────────────────────

DAY 1: Fund needs $50M for investment
┌─────────────────────────────────────────────────────────┐
│ WITHOUT Sub Line:                                       │
│ ├── Send capital call notices to 40 LPs                │
│ ├── Wait 10-15 business days                           │
│ ├── Collect and reconcile wires                        │
│ └── Make investment                                     │
│     TOTAL TIME: 15-20 days                             │
│                                                         │
│ WITH Sub Line:                                          │
│ ├── Draw $50M from credit facility                     │
│ ├── Same-day funding                                    │
│ └── Make investment                                     │
│     TOTAL TIME: 1 day                                   │
└─────────────────────────────────────────────────────────┘

DAY 90: Fund issues capital call to repay facility
┌─────────────────────────────────────────────────────────┐
│ ├── Call $50M from LPs (covers draw + interest)        │
│ ├── Receive LP capital                                  │
│ └── Repay bank facility                                 │
│                                                         │
│ LP IMPACT:                                              │
│ ├── Capital called 90 days later                       │
│ ├── IRR appears higher (shorter hold period)           │
│ └── Same TVPI (cash-on-cash unchanged)                 │
└─────────────────────────────────────────────────────────┘
```

### Impact on IRR

```
IRR IMPACT OF SUBSCRIPTION LINES
────────────────────────────────

EXAMPLE: $100M investment, 5-year hold, $180M exit

SCENARIO A: No Subscription Line
├── Day 0: LP capital called $100M
├── Year 5: Distribution $180M
├── IRR: 12.5%
└── TVPI: 1.80x

SCENARIO B: 6-Month Subscription Line
├── Day 0: Fund draws from sub line
├── Month 6: LP capital called $101M (incl. interest)
├── Year 5: Distribution $180M
├── LP IRR: 13.3% (+80 bps)
└── LP TVPI: 1.78x (slightly lower due to interest)

SCENARIO C: 12-Month Subscription Line
├── Day 0: Fund draws from sub line
├── Month 12: LP capital called $103M
├── Year 5: Distribution $180M
├── LP IRR: 14.9% (+240 bps)
└── LP TVPI: 1.75x

IRR ENHANCEMENT DRIVERS:
├── Shorter measured investment period
├── Delayed capital call = later start date
├── Same exit proceeds, compressed timeline
└── Mathematical artifact, not value creation
```

### Disclosure Best Practices

```
SUBSCRIPTION LINE DISCLOSURE (ILPA GUIDELINES)
──────────────────────────────────────────────

SHOULD DISCLOSE:
├── IRR with and without sub line impact
├── Average days outstanding on facility
├── Facility size and utilization
├── Interest cost borne by fund/LPs
└── Policy on maximum usage period

EXAMPLE DISCLOSURE:
┌─────────────────────────────────────────────────────────┐
│ FUND PERFORMANCE METRICS                                │
│                                                         │
│                      Gross    Net     Net (ex-sub)      │
│                      ─────    ───     ────────────      │
│ IRR:                 22.4%    18.1%      15.3%          │
│ TVPI:                1.85x    1.72x      1.72x          │
│                                                         │
│ Average sub line usage: 142 days                        │
│ Max sub line usage: 365 days                            │
│ Interest cost YTD: $2.1M                               │
└─────────────────────────────────────────────────────────┘
```

---

## 16.3 NAV Lending

### What is NAV Lending?

```
NAV LENDING STRUCTURE
─────────────────────

┌──────────────────────────────────────────────────────────┐
│                        LENDER                            │
│    (Bank, direct lender, specialty finance)              │
│                           │                              │
│                     NAV Loan $100M                       │
│                           │                              │
│                           ▼                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │                      FUND                          │ │
│  │                                                    │ │
│  │  Portfolio NAV: $400M                             │ │
│  │  Loan: $100M (25% LTV)                            │ │
│  │                                                    │ │
│  │  COLLATERAL:                                       │ │
│  │  ├── Portfolio company equity interests           │ │
│  │  ├── Distribution proceeds                        │ │
│  │  └── Capital call rights (backup)                 │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  USE OF PROCEEDS:                                        │
│  ├── Fund investments / follow-ons                      │
│  ├── LP distributions (dividend recap)                  │
│  ├── GP liquidity needs                                 │
│  └── Bridge to expected exits                           │
└──────────────────────────────────────────────────────────┘
```

### NAV Loan Terms

```
TYPICAL NAV LOAN TERMS
──────────────────────

SIZING:
├── LTV: 15-35% of portfolio NAV
├── Minimum facility: $50M
├── Typical: $100M - $500M
└── Maximum single loan: $2B+

PRICING:
├── SOFR + 400-700 bps
├── Higher than sub lines
├── Risk-based pricing
└── Upfront fees: 50-100 bps

MATURITY:
├── 2-4 years typical
├── Amortization from distributions
├── PIK option in some cases
└── Extension options common

COVENANTS:
├── LTV maintenance (quarterly)
├── Portfolio concentration limits
├── Minimum NAV thresholds
├── Distribution waterfall requirements
└── Reporting obligations
```

### NAV Lending Use Cases

```
NAV LOAN USE CASES
──────────────────

1. PORTFOLIO ACCELERATION
   ├── Follow-on investments
   ├── Add-on acquisitions
   └── Growth capital for companies

   Example: Fund needs $75M for bolt-on
   ├── No unfunded commitments left
   ├── Borrow against NAV
   └── Returns enhanced if deal works

2. LP DISTRIBUTIONS (Dividend Recap)
   ├── Fund in J-curve, no exits yet
   ├── LPs want some liquidity
   └── Borrow to distribute

   Example: Year 4 fund, NAV $300M
   ├── Borrow $60M (20% LTV)
   ├── Distribute to LPs
   └── Repay from future exits

3. GP LIQUIDITY
   ├── Management fee bridge
   ├── GP commitment funding
   └── Operational needs

4. BRIDGE TO EXIT
   ├── Exit expected in 6-12 months
   ├── Need capital now
   └── Bridge loan repaid at exit

5. DEFENSIVE / RESCUE
   ├── Portfolio company needs capital
   ├── Fund fully invested
   └── Last resort financing
```

### Risks of NAV Lending

```
NAV LENDING RISK CONSIDERATIONS
───────────────────────────────

FOR LPs:

1. LEVERAGE AT FUND LEVEL
   ├── Portfolio already leveraged at company
   ├── NAV loan adds another layer
   └── Amplifies both gains and losses

   Example:
   ┌─────────────────────────────────────────┐
   │ Portfolio company: 5x leveraged         │
   │ Fund: 25% NAV loan                      │
   │                                         │
   │ Effective leverage: 6.25x               │
   │ Small NAV decline → large LP impact     │
   └─────────────────────────────────────────┘

2. SUBORDINATION OF LP INTERESTS
   ├── Lender has senior claim
   ├── LP distributions subordinated
   └── In distress, lender paid first

3. TRANSPARENCY CONCERNS
   ├── Not always disclosed
   ├── Impact on returns unclear
   └── Hidden fund-level risk

4. VALUATION RISK
   ├── Loan based on GP marks
   ├── If NAV drops, covenant breach
   └── Forced asset sales possible

5. DISTRIBUTION TIMING
   ├── Proceeds may repay loan first
   ├── LP waterfall affected
   └── Carry timing impacted
```

---

## 16.4 Hybrid Facilities

### What Are Hybrid Facilities?

```
HYBRID FACILITY STRUCTURE
─────────────────────────

Combines subscription line + NAV lending:

┌──────────────────────────────────────────────────────────┐
│                       HYBRID FACILITY                    │
│                                                          │
│  ┌─────────────────────┐  ┌─────────────────────┐       │
│  │  SUBSCRIPTION LINE  │  │    NAV TRANCHE      │       │
│  │                     │  │                     │       │
│  │  Secured by:        │  │  Secured by:        │       │
│  │  LP Commitments     │  │  Portfolio NAV      │       │
│  │                     │  │                     │       │
│  │  Size: $200M        │  │  Size: $100M        │       │
│  │  Rate: SOFR+175     │  │  Rate: SOFR+500     │       │
│  └─────────────────────┘  └─────────────────────┘       │
│                                                          │
│  TOTAL FACILITY: $300M                                   │
│  BLENDED RATE: ~SOFR+283                                │
│                                                          │
│  TRANSITION:                                             │
│  As commitments called → sub line shrinks               │
│  As portfolio builds → NAV capacity increases           │
└──────────────────────────────────────────────────────────┘
```

### Facility Evolution Over Fund Life

```
HYBRID FACILITY OVER FUND LIFECYCLE
───────────────────────────────────

YEAR 1-3 (Investment Period):
┌────────────────────────────────────┐
│ Unfunded commitments: $500M        │
│ Portfolio NAV: $150M               │
│                                    │
│ Sub line capacity: $250M ████████  │
│ NAV line capacity: $30M  ██        │
│                                    │
│ Primary use: Sub line              │
└────────────────────────────────────┘

YEAR 4-6 (Transition):
┌────────────────────────────────────┐
│ Unfunded commitments: $100M        │
│ Portfolio NAV: $450M               │
│                                    │
│ Sub line capacity: $50M  ██        │
│ NAV line capacity: $110M ██████    │
│                                    │
│ Balanced usage                     │
└────────────────────────────────────┘

YEAR 7-10 (Harvest):
┌────────────────────────────────────┐
│ Unfunded commitments: $0           │
│ Portfolio NAV: $300M               │
│                                    │
│ Sub line capacity: $0              │
│ NAV line capacity: $75M ████       │
│                                    │
│ Primary use: NAV line              │
└────────────────────────────────────┘
```

---

## 16.5 Fund-Level vs Deal-Level Leverage

### Understanding the Distinction

```
LEVERAGE COMPARISON
───────────────────

DEAL-LEVEL LEVERAGE:
┌─────────────────────────────────────────────────────────┐
│                    FUND                                 │
│                      │                                  │
│                 Equity $40M                             │
│                      │                                  │
│                      ▼                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │           PORTFOLIO COMPANY                      │   │
│  │                                                  │   │
│  │    Equity: $40M (40%)                           │   │
│  │    Debt: $60M (60%)                             │   │
│  │    ──────────────────                           │   │
│  │    EV: $100M                                    │   │
│  │                                                  │   │
│  │    Debt is at COMPANY level                     │   │
│  │    Non-recourse to fund                         │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘

FUND-LEVEL LEVERAGE:
┌─────────────────────────────────────────────────────────┐
│                    FUND                                 │
│                                                         │
│    LP Capital: $400M                                    │
│    Fund Debt: $100M (NAV loan)                         │
│    ─────────────────────                                │
│    Total Capital: $500M                                 │
│                      │                                  │
│                      ▼                                  │
│    Portfolio Companies (each with own leverage)         │
│                                                         │
│    Debt is at FUND level                               │
│    Recourse to fund assets                             │
└─────────────────────────────────────────────────────────┘
```

### Layered Leverage Risk

```
LAYERED LEVERAGE EXAMPLE
────────────────────────

Fund structure:
├── LP commitments: $500M
├── NAV loan: $125M (25% fund-level)
├── Total investable: $625M

Portfolio company:
├── Fund equity: $125M
├── Company debt: $375M (75% deal-level)
├── Company EV: $500M

TOTAL LEVERAGE CALCULATION:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  LP CAPITAL                                             │
│  $500M                                                  │
│      │                                                  │
│      ▼                                                  │
│  FUND (with NAV loan)                                   │
│  $625M total ──► 1.25x leverage on LP capital          │
│      │                                                  │
│      ▼                                                  │
│  PORTFOLIO CO (with deal debt)                          │
│  $500M EV on $125M equity ──► 4x leverage              │
│                                                         │
│  COMBINED LEVERAGE:                                     │
│  For every $1 of LP capital:                           │
│  $1 × 1.25 × 4 = $5 of company assets                  │
│                                                         │
│  5x effective leverage on LP capital!                   │
└─────────────────────────────────────────────────────────┘
```

### Leverage Limits in LPAs

```
TYPICAL LPA LEVERAGE RESTRICTIONS
─────────────────────────────────

SUBSCRIPTION LINES:
├── Cap: 25-35% of commitments
├── Duration: 6-18 months max
├── Purpose: Bridge to capital calls
└── Commonly accepted

NAV FACILITIES:
├── Cap: 15-25% of NAV (if permitted)
├── May require LPAC consent
├── Purpose restrictions common
└── More controversial

TOTAL FUND LEVERAGE:
├── Aggregate cap: 30-40% of NAV
├── Excludes deal-level debt
├── Reporting requirements
└── Increasingly negotiated

EXAMPLE LPA LANGUAGE:
┌─────────────────────────────────────────────────────────┐
│ "The Fund may incur indebtedness not to exceed the     │
│ lesser of (i) 25% of aggregate Capital Commitments     │
│ or (ii) 30% of Net Asset Value, provided that any      │
│ borrowings under NAV facilities in excess of 15% of    │
│ NAV shall require LPAC consent."                       │
└─────────────────────────────────────────────────────────┘
```

---

## 16.6 LP Considerations

### Questions LPs Should Ask

```
LP DUE DILIGENCE ON FUND FINANCING
──────────────────────────────────

SUBSCRIPTION LINES:
□ What is the maximum facility size?
□ What is the maximum borrowing period?
□ How is interest allocated?
□ Will you report IRR with/without sub line impact?
□ What triggers require capital calls vs draws?

NAV FACILITIES:
□ Does the LPA permit NAV borrowing?
□ What are the permitted uses?
□ What is the maximum LTV?
□ Is LPAC consent required?
□ How is NAV calculated for borrowing base?
□ What happens if NAV declines?

GENERAL:
□ What is total fund-level leverage exposure?
□ How do you monitor covenant compliance?
□ What is the repayment waterfall?
□ How does leverage affect GP carry?
□ What disclosure will be provided?
```

### Impact on LP Reporting

```
FINANCING IMPACT ON LP REPORTS
──────────────────────────────

CAPITAL ACCOUNT STATEMENT:
┌─────────────────────────────────────────────────────────┐
│ CAPITAL ACCOUNT                                         │
│                                                         │
│ Commitment:                    $50,000,000              │
│ Contributed capital:           $35,000,000              │
│ Remaining commitment:          $15,000,000              │
│                                                         │
│ NAV at period end:             $48,000,000              │
│ Distributions:                 $12,000,000              │
│                                                         │
│ LEVERAGE DISCLOSURE:                                    │
│ Fund sub line outstanding:     $45,000,000              │
│ Your share of sub line:        $4,500,000  (9%)         │
│ Fund NAV facility outstanding: $25,000,000              │
│ Your share of NAV debt:        $2,500,000  (5%)         │
│                                                         │
│ ADJUSTED METRICS:                                       │
│ IRR (as reported):             18.5%                    │
│ IRR (ex-subscription line):    15.2%                    │
│ Days sub line outstanding:     120 avg                  │
└─────────────────────────────────────────────────────────┘
```

### Best Practices (ILPA Recommendations)

```
ILPA FUND FINANCING PRINCIPLES
──────────────────────────────

1. TRANSPARENCY
   ├── Disclose all credit facilities
   ├── Report IRR with/without sub line
   ├── Provide utilization metrics
   └── Explain purposes of borrowing

2. LIMITS ON SUB LINES
   ├── Maximum period: 180 days recommended
   ├── Exceptions require justification
   └── No permanent leverage via sub lines

3. NAV LENDING GOVERNANCE
   ├── Clear LPA authorization required
   ├── LPAC oversight recommended
   ├── Use of proceeds restrictions
   └── Lender subordination provisions

4. REPORTING REQUIREMENTS
   ├── Quarterly disclosure
   ├── Separate line items
   ├── Impact quantification
   └── Covenant compliance status

5. GP ALIGNMENT
   ├── Interest expense reduces returns
   ├── Should affect carry calculation
   └── GP should not benefit at LP expense
```

---

## 16.7 Summary

### Fund Financing Comparison

| Type | Collateral | LTV | Pricing | Duration | Primary Use |
|------|------------|-----|---------|----------|-------------|
| Subscription Line | LP Commits | 25-50% | SOFR+150-250 | <1 year | Bridge calls |
| NAV Facility | Portfolio | 15-35% | SOFR+400-700 | 2-4 years | Various |
| Hybrid | Both | Varies | Blended | Fund life | Flexible |

### Key Takeaways

```
FUND FINANCING SUMMARY
──────────────────────

1. Subscription lines enhance IRR mathematically
   └── Same returns, shorter measured period

2. NAV lending adds real leverage risk
   └── Fund-level debt on top of deal debt

3. Transparency is critical for LPs
   └── Demand IRR with/without sub line impact

4. Governance increasingly important
   └── LPAC oversight of NAV facilities

5. Layered leverage can be significant
   └── 25% fund + 70% deal = 5x+ effective

6. Review LPA carefully
   └── Know what's permitted before committing
```

---

## Knowledge Check

1. How do subscription lines enhance reported IRR?
2. What's the key difference between subscription lines and NAV lending?
3. Why is "layered leverage" a concern for LPs?
4. What disclosure should LPs request regarding fund financing?
5. When might LPAC consent be required for fund borrowing?

<details>
<summary>Answers</summary>

1. Subscription lines delay when capital is called from LPs. Since IRR measures time-weighted returns, calling capital later (but still exiting at the same time) compresses the holding period, mathematically increasing IRR even though total cash-on-cash returns are unchanged or slightly lower.

2. Subscription lines are secured by unfunded LP commitments (very low risk, short-term bridge). NAV lending is secured by portfolio assets (higher risk, longer-term, adds real leverage). Sub lines don't add leverage risk; NAV loans do.

3. Layered leverage compounds: if the fund has 25% NAV-level debt and portfolio companies have 75% LTV, effective leverage on LP capital can exceed 5x. Small declines in asset values can result in large losses to LP equity.

4. LPs should request: IRR with and without subscription line impact, average days outstanding on facilities, facility sizes and utilization, interest costs, and any NAV facility details including covenants and permitted uses.

5. LPAC consent is typically required when NAV borrowing exceeds certain thresholds (e.g., 15-25% of NAV), when proceeds are used for distributions rather than investments, or when the borrowing falls outside LPA-defined permitted purposes.

</details>

---

## Exercise: Analyze Financing Impact

```
SCENARIO: Fund Performance with Subscription Line

Fund Statistics:
├── Investment date: January 1, 2020
├── Sub line drawn: January 1, 2020
├── LP capital called: July 1, 2020 (6 months later)
├── Called amount: $52M ($50M + $2M interest)
├── Exit date: January 1, 2025
├── Exit proceeds: $100M

Calculate:
1. IRR as reported (from LP capital call date)
2. IRR without sub line (from investment date)
3. TVPI as reported
4. Difference in IRR
```

<details>
<summary>Answers</summary>

```
1. IRR as Reported (from July 1, 2020):
   Investment: $52M
   Exit (4.5 years later): $100M
   IRR = ($100M/$52M)^(1/4.5) - 1 = 15.5%

2. IRR Without Sub Line (from Jan 1, 2020):
   Investment: $50M (original, no interest)
   Exit (5 years later): $100M
   IRR = ($100M/$50M)^(1/5) - 1 = 14.9%

3. TVPI as Reported:
   TVPI = $100M / $52M = 1.92x

   Note: Without sub line interest cost:
   TVPI would be = $100M / $50M = 2.00x

4. IRR Difference:
   15.5% - 14.9% = 0.6% (60 bps)

   The sub line enhanced reported IRR by 60bps
   but reduced TVPI from 2.0x to 1.92x due to
   interest costs.
```

</details>

---

[← Module 15: Secondaries Deep-Dive](15-secondaries.md) | [Module 17: Portfolio Construction →](17-portfolio-construction.md)

[← Back to Curriculum Overview](00-curriculum-overview.md)
