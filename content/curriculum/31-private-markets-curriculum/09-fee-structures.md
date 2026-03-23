# Module 09: Fee Structures

## Learning Objectives

By the end of this module, you will understand:
- How management fees work and are calculated
- Fee offsets and rebates
- Partnership expenses vs management company costs
- Organizational expenses
- The total cost of fund investing
- How to analyze fee impact on returns

---

## 9.1 Overview of Fund Fees

### Fee Categories

```
PRIVATE FUND FEE STRUCTURE
──────────────────────────

┌─────────────────────────────────────────────────────────────┐
│                     FEE CATEGORIES                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MANAGEMENT FEE                                          │
│     └── Annual fee to GP for managing fund                  │
│         Typically 1.5-2.0% of capital                       │
│                                                             │
│  2. CARRIED INTEREST (covered in Module 10)                 │
│     └── GP's share of profits                               │
│         Typically 20%                                       │
│                                                             │
│  3. PARTNERSHIP EXPENSES                                    │
│     └── Fund operating costs                                │
│         Legal, audit, admin, etc.                           │
│                                                             │
│  4. ORGANIZATIONAL EXPENSES                                 │
│     └── One-time fund formation costs                       │
│         Typically capped                                    │
│                                                             │
│  5. TRANSACTION/PORTFOLIO FEES                              │
│     └── Fees from portfolio companies                       │
│         Often offset management fees                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Fee Summary by Fund Type

| Fund Type | Mgmt Fee | Carry | Hurdle | Typical Expenses |
|-----------|----------|-------|--------|------------------|
| Buyout | 1.5-2.0% | 20% | 8% | 0.1-0.2% |
| Growth | 1.5-2.0% | 20% | 8% | 0.1-0.2% |
| Venture | 2.0-2.5% | 20-30% | 0-8% | 0.2-0.3% |
| Real Estate | 1.0-1.5% | 20% | 8-10% | 0.1-0.2% |
| Credit | 1.0-1.5% | 15-20% | 6-8% | 0.1-0.2% |
| FoF | 0.5-1.0% | 5-10% | 6-8% | 0.1-0.2% |

---

## 9.2 Management Fee Deep Dive

### What Management Fee Covers

```
MANAGEMENT FEE USAGE
────────────────────

PAID TO MANAGEMENT COMPANY FOR:
├── Investment professional salaries & bonuses
├── Office rent and operations
├── Research and due diligence resources
├── Travel and deal sourcing
├── Technology and systems
├── Back-office staff
├── Compliance and legal (internal)
└── General overhead

NOT COVERED (Charged to Fund):
├── External legal fees
├── Audit fees
├── Fund administrator
├── Deal-specific costs
└── Placement agent fees
```

### Fee Basis: Investment Period vs Post-Investment

```
MANAGEMENT FEE CALCULATION
──────────────────────────

INVESTMENT PERIOD (Years 1-5)
─────────────────────────────
Fee Basis: COMMITTED CAPITAL
Rate: 2.0% (typical buyout)

Example:
Commitment: $500M
Annual Fee: $500M × 2.0% = $10M
Quarterly Fee: $2.5M

IMPORTANT: Fee on committed, not called
• Year 1: Only 20% called, still pay on $500M
• This creates early J-curve drag


POST-INVESTMENT PERIOD (Years 6+)
─────────────────────────────────
Fee Basis: INVESTED CAPITAL, NAV, or LOWER RATE
Rate: 1.5% (typical step-down)

Option A: Invested Capital (most common)
• Fee on capital actually invested (at cost)
• Excludes written-off investments
• Excludes realized investments

Option B: Net Asset Value
• Fee on current NAV
• Aligns fee with remaining value

Option C: Reduced Rate on Commitment
• Same basis, lower percentage
• Simple but less aligned

Example (Invested Capital):
Year 6: $400M still invested
Fee: $400M × 1.5% = $6M (vs $10M in investment period)
```

### Fee Calculation Example Over Fund Life

```
10-YEAR FEE CALCULATION
───────────────────────

$500M Fund, 2%/1.5% Structure

Year  Fee Basis        Rate    Annual Fee   Cumulative
────  ────────────     ────    ──────────   ──────────
  1   $500M (commit)   2.0%    $10.0M       $10.0M
  2   $500M (commit)   2.0%    $10.0M       $20.0M
  3   $500M (commit)   2.0%    $10.0M       $30.0M
  4   $500M (commit)   2.0%    $10.0M       $40.0M
  5   $500M (commit)   2.0%    $10.0M       $50.0M
  6   $400M (invested) 1.5%    $6.0M        $56.0M
  7   $350M (invested) 1.5%    $5.3M        $61.3M
  8   $250M (invested) 1.5%    $3.8M        $65.0M
  9   $150M (invested) 1.5%    $2.3M        $67.3M
 10   $75M (invested)  1.5%    $1.1M        $68.4M
────────────────────────────────────────────────────
TOTAL MANAGEMENT FEES:                      $68.4M

As % of Commitment: 68.4/500 = 13.7%
```

---

## 9.3 Fee Offsets

### What Are Fee Offsets?

Many GPs receive fees from portfolio companies. **Fee offsets** reduce LP management fees by a portion of these amounts.

```
FEE OFFSET STRUCTURE
────────────────────

PORTFOLIO COMPANY FEES:
├── Transaction Fees: 1-2% of deal value
├── Monitoring Fees: $0.5-2M annually per company
├── Director Fees: $50-200K per board seat
├── Advisory Fees: Varies
└── Break-up Fees: From failed deals

OFFSET MECHANISM:
GP receives $2M monitoring fee from portfolio company
Offset rate: 80%
Fee offset: $2M × 80% = $1.6M
LP management fee reduced by $1.6M

TYPICAL OFFSET RATES:
• 80% offset: Most common
• 100% offset: LP-friendly
• 50% offset: Less common today
• 0% offset: Rare, old-style funds
```

### Fee Offset Example

```
FEE OFFSET CALCULATION
──────────────────────

QUARTERLY MANAGEMENT FEE (before offsets):
Commitment: $500M
Rate: 2%
Quarterly Fee: $500M × 2% × 1/4 = $2,500,000

PORTFOLIO COMPANY FEES RECEIVED (quarter):
Transaction fee from new deal:   $1,500,000
Monitoring fees (5 companies):   $500,000
Director fees:                   $75,000
────────────────────────────────────────────
Total Portfolio Fees:            $2,075,000

OFFSET CALCULATION (80% offset):
Fee Offset: $2,075,000 × 80% = $1,660,000

NET MANAGEMENT FEE:
Gross Fee:          $2,500,000
Less Offset:        ($1,660,000)
Net Fee:            $840,000

LP SAVINGS: $1,660,000 this quarter
```

### Fee Income Disclosure

LPs can see fee income in reports:

```
FEE INCOME DISCLOSURE (Sample)
──────────────────────────────

For the Year Ended December 31, 2024

Portfolio Company Fee Income:
├── Transaction Fees              $4,500,000
├── Monitoring Fees              $2,800,000
├── Director Fees                  $450,000
├── Advisory Fees                  $350,000
├── Break-up Fees                  $200,000
└── Total Fee Income             $8,300,000

Fee Offset to Limited Partners (80%):
                                 $6,640,000

Fee Income Retained by GP (20%):
                                 $1,660,000
```

---

## 9.4 Partnership Expenses

### What Qualifies as Partnership Expenses?

```
PARTNERSHIP EXPENSES
────────────────────

TYPICALLY FUND-BORNE:
├── Legal fees (fund-related)
│   ├── Annual compliance
│   ├── LP matters
│   └── Transaction legal (sometimes capitalized)
│
├── Audit and tax
│   ├── Annual audit
│   ├── Tax preparation
│   └── K-1 preparation
│
├── Administration
│   ├── Fund administrator fees
│   ├── Custodian fees
│   └── Banking fees
│
├── Regulatory
│   ├── SEC registration fees
│   ├── Form PF filing
│   └── Blue sky filings
│
├── Investor relations
│   ├── Annual meeting costs
│   ├── Reporting systems
│   └── (Travel typically GP cost)
│
└── Insurance
    ├── D&O insurance
    └── Professional liability

NOT FUND-BORNE (GP Pays):
├── GP salaries and overhead
├── Office rent
├── GP travel (usually)
├── GP technology
└── Marketing/fundraising
```

### Expense Caps

Most funds have **expense caps** to protect LPs:

```
EXPENSE CAP STRUCTURE
─────────────────────

TYPICAL CAP: 0.10-0.25% of Commitments Annually

EXAMPLE:
Fund Size: $500M
Expense Cap: 0.15%
Annual Cap: $750,000

IF EXPENSES EXCEED CAP:
• GP pays excess from management fee
• Or GP absorbs excess directly
• Protects LPs from cost overruns

EXCLUDED FROM CAP (Sometimes):
• Broken deal expenses
• Litigation costs
• Extraordinary items
```

---

## 9.5 Organizational Expenses

### Fund Formation Costs

```
ORGANIZATIONAL EXPENSES
───────────────────────

ONE-TIME COSTS AT FUND LAUNCH:
├── Legal
│   ├── LPA drafting
│   ├── PPM preparation
│   ├── Side letter negotiations
│   └── Regulatory filings
│
├── Accounting
│   ├── Fund structure setup
│   └── Tax planning
│
├── Other
│   ├── Placement agent fees
│   ├── Marketing materials
│   └── Entity formation
│
└── TYPICAL TOTAL: $1.0-3.0M

ORG EXPENSE CAP:
• Usually capped at $1.5-2.5M
• Excess paid by GP
• Amortized over fund life (sometimes)
```

### Placement Agent Fees

```
PLACEMENT AGENT FEES
────────────────────

WHAT THEY DO:
• Help GP raise capital
• Introduce LPs
• Coordinate due diligence
• Sometimes ongoing advisory

FEE STRUCTURE:
• 1-2% of capital raised
• Sometimes tiered (lower for larger funds)
• May be paid by fund or GP

EXAMPLE:
$500M fund
Placement agent helped raise $300M
Fee: 1.5% × $300M = $4.5M

WHO PAYS?
• Older funds: Fund pays (controversial)
• Modern trend: GP pays
• Hybrid: Split or capped at org expense level
```

---

## 9.6 Total Cost Analysis

### Total LP Cost Example

```
COMPREHENSIVE FEE ANALYSIS
──────────────────────────

ABC Partners Fund VII - $500M Commitment
10-Year Fund Life

MANAGEMENT FEES:
Investment Period (Years 1-5):
$500M × 2.0% × 5 years = $50.0M

Post-Investment (Years 6-10):
Declining invested capital basis = $18.4M
(as calculated earlier)

Total Management Fees: $68.4M

LESS: FEE OFFSETS
Estimated portfolio fees: ($15.0M)
Offset rate: 80%
Total Offset: ($12.0M)

NET MANAGEMENT FEES: $56.4M

PARTNERSHIP EXPENSES:
$500M × 0.15% × 10 years = $7.5M

ORGANIZATIONAL EXPENSES: $2.0M

CARRIED INTEREST (if 2.0x return):
Contributed: $450M
Distributed + NAV: $900M
Profit: $450M
Carry (20%): $90.0M

─────────────────────────────────────────────
TOTAL COSTS OVER FUND LIFE:

Fees and Expenses:
  Net Management Fees:     $56.4M
  Partnership Expenses:     $7.5M
  Organizational:           $2.0M
  Subtotal:               $65.9M

Performance Fee:
  Carried Interest:        $90.0M

TOTAL COST:              $155.9M
─────────────────────────────────────────────

AS PERCENTAGE OF:
• Commitment ($500M):      31.2%
• Contributed ($450M):     34.6%
• Gross Returns ($900M):   17.3%
• Profit ($450M):          34.6%
```

### Fee Drag on Returns

```
FEE IMPACT ON RETURNS
─────────────────────

HYPOTHETICAL FUND:
Gross TVPI: 2.0x
Gross IRR: 18%

After Fees:
Net TVPI: ~1.70x
Net IRR: ~14%

FEE DRAG:
TVPI reduced by: 0.30x (15%)
IRR reduced by: 4% (22%)

HIGHER FEES = MORE DRAG
Lower returning funds feel this more acutely:

Gross TVPI 2.5x → Net TVPI ~2.10x (16% drag)
Gross TVPI 2.0x → Net TVPI ~1.70x (15% drag)
Gross TVPI 1.5x → Net TVPI ~1.28x (15% drag)
Gross TVPI 1.2x → Net TVPI ~1.05x (13% drag)

For low-returning funds, fees can consume
most or all of the gains.
```

---

## 9.7 Fee Negotiations & Side Letters

### What LPs Negotiate

```
COMMON FEE NEGOTIATIONS
───────────────────────

MANAGEMENT FEE DISCOUNTS:
• 25-50 bps reduction for large commitments
• Example: $100M+ commitment gets 1.75% vs 2.0%

PREFERRED INVESTMENT TERMS:
• No fee on co-investments
• Reduced fee on certain sleeves

OFFSET ENHANCEMENTS:
• 100% offset vs 80%
• Broader offset categories

EXPENSE CAPS:
• Lower cap percentage
• More exclusions from cap

MOST FAVORED NATION (MFN):
• LP gets best terms given to any LP
• "If you give anyone a better deal, I get it too"
```

### Sample Side Letter Terms

```
SIDE LETTER EXCERPT (Fee Terms)
──────────────────────────────

MANAGEMENT FEE:
Notwithstanding Section 4.1 of the Partnership
Agreement, the Limited Partner shall pay a
Management Fee calculated as follows:

• Investment Period: 1.75% of Commitment
  (versus 2.00% standard)
• Post-Investment: 1.25% of Invested Capital
  (versus 1.50% standard)

FEE OFFSET:
The Limited Partner shall receive 100% offset
of all Portfolio Company fees (versus 80% standard).

CO-INVESTMENT:
Any co-investment offered to Limited Partner
shall be on a no-fee, no-carry basis.

MFN:
If more favorable economic terms are granted to
any Limited Partner, such terms shall automatically
apply to this Limited Partner.
```

### Fee Tiers by Commitment Size

```
TIERED FEE STRUCTURE (Example)
──────────────────────────────

Commitment Size      Mgmt Fee    Carry
──────────────────   ────────    ─────
< $25M               2.00%       20%
$25M - $50M          1.875%      20%
$50M - $100M         1.75%       20%
$100M - $200M        1.625%      20%
> $200M              1.50%       20%

GP Commit            0%          20%
Employees            0%          0%
```

---

## 9.8 Fee Trends

### Evolution of Fund Terms

```
FEE TREND OVER TIME
───────────────────

               1990s    2000s    2010s    2020s
               ─────    ─────    ─────    ─────
Mgmt Fee       2.0%     2.0%     1.75%    1.5-1.75%
Carry          20%      20%      20%      20%
Hurdle         0-8%     8%       8%       8%
Fee Offset     50-80%   80%      80-100%  80-100%
Expense Cap    None     0.25%    0.15%    0.10-0.15%

TRENDS:
• Management fees under pressure
• Offsets increasing to 100%
• More transparency on expenses
• Expense caps tightening
• Carry remains sticky at 20%
• Top-tier funds can still charge premium
```

### Emerging Fee Structures

```
NEW FEE APPROACHES
──────────────────

1. DEAL-BY-DEAL CARRY
   • Carry on each investment (not whole fund)
   • More common in Europe
   • LP-friendlier (no cross-subsidization)

2. HURDLE CATCH-UP MODIFICATIONS
   • 50/50 catch-up (vs 100% GP)
   • Higher hurdle rates (10%+)
   • Compound vs simple hurdle

3. FEE BUDGETS
   • Fixed dollar fee (not percentage)
   • GP proposes annual budget
   • LPAC approves

4. NAV-BASED FEES
   • Fee on NAV (not commitment)
   • Better alignment (fee drops with value)
   • Growing in credit/real assets

5. PERFORMANCE FEE CRYSTALLIZATION
   • Carry locks in annually
   • Reduces clawback risk
   • GP prefers, LPs less so
```

---

## 9.9 Reading Fee Disclosures

### Where to Find Fee Information

```
FEE DISCLOSURE LOCATIONS
────────────────────────

1. LIMITED PARTNERSHIP AGREEMENT (LPA)
   • Definitive fee terms
   • Section 4: Fees and Expenses (typical)
   • Most detailed source

2. PRIVATE PLACEMENT MEMORANDUM (PPM)
   • Summary of fee terms
   • Good for quick reference
   • May lack nuance

3. QUARTERLY/ANNUAL REPORTS
   • Fees actually charged
   • Fee offsets received
   • Expense breakdown

4. CAPITAL ACCOUNT STATEMENT
   • Your specific fee allocation
   • Net fees charged to you

5. AUDITED FINANCIALS
   • Management fee expense line
   • Related party transactions note
   • Most accurate historical data
```

### Sample Fee Note (Audited Financials)

```
NOTE 4: RELATED PARTY TRANSACTIONS (Excerpt)
─────────────────────────────────────────────

Management Fee:
The Fund pays the Management Company an annual
management fee of 2.0% of aggregate Capital
Commitments during the Investment Period and
1.5% of aggregate Invested Capital thereafter.

For the year ended December 31, 2024:
• Management fee charged:      $18,500,000
• Portfolio company fee offset: ($3,200,000)
• Net management fee:          $15,300,000

Carried Interest:
The General Partner is entitled to 20% of net
profits after Limited Partners receive return
of capital and an 8% preferred return.

As of December 31, 2024:
• Accrued carried interest:    $42,000,000
• Carried interest paid:       $18,000,000
```

---

## 9.10 Summary

### Fee Structure Checklist

```
LP FEE ANALYSIS CHECKLIST
─────────────────────────

MANAGEMENT FEE:
☐ Rate (investment period)
☐ Rate (post-investment)
☐ Fee basis (commitment vs invested vs NAV)
☐ Step-down timing
☐ Offset rate

PARTNERSHIP EXPENSES:
☐ What's included
☐ What's excluded
☐ Annual cap

ORGANIZATIONAL EXPENSES:
☐ Cap amount
☐ What's included
☐ Amortization treatment

CARRIED INTEREST:
☐ Rate
☐ Hurdle rate
☐ Catch-up structure
☐ Waterfall type (European vs American)
☐ Clawback provisions

SPECIAL TERMS:
☐ Side letter discounts
☐ MFN rights
☐ Co-investment terms
```

---

## Knowledge Check

1. What's the typical management fee structure over a fund's life?
2. What are fee offsets and why do LPs want them?
3. What's the difference between partnership expenses and organizational expenses?
4. How does a "most favored nation" clause work?
5. Why does management fee drag hurt low-returning funds more?

<details>
<summary>Answers</summary>

1. Typically 2% on committed capital during investment period (years 1-5), stepping down to 1.5% on invested capital or NAV during harvest period (years 6+)
2. Fee offsets reduce LP management fees by a portion of fees the GP earns from portfolio companies (transaction fees, monitoring fees, etc.). LPs want them to avoid paying twice.
3. Partnership expenses are ongoing fund operating costs (legal, audit, admin). Organizational expenses are one-time fund formation costs (LPA drafting, entity setup).
4. MFN gives an LP the right to receive any better economic terms granted to any other LP in the fund.
5. Fees are relatively fixed costs. If returns are low, fees consume a larger proportion of gains. A fund returning 1.2x gross might only return 1.05x net after fees.

</details>

---

## Next Module

[Module 10: Waterfall & Carried Interest →](10-waterfall-carry.md)

Deep dive into distribution waterfalls, preferred returns, carried interest mechanics, and clawback provisions.
