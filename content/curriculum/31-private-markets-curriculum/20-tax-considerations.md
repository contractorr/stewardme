# Module 20: Tax Considerations

## Learning Objectives

By the end of this module, you will understand:
- K-1 reporting mechanics and timeline
- UBTI (Unrelated Business Taxable Income) basics
- ECI (Effectively Connected Income) for foreign investors
- Blocker structures and feeder funds
- Tax reporting complexity and planning considerations

---

## 20.1 Overview of PE Taxation

### Why Tax Matters for PE

```
TAX COMPLEXITY IN PRIVATE EQUITY
────────────────────────────────

PUBLIC EQUITIES:
├── Buy stock → Get 1099
├── Sell stock → Capital gain/loss
├── Simple, immediate reporting
└── Tax status rarely affects investment decision

PRIVATE EQUITY:
├── Complex partnership structures
├── K-1 reporting (often late, amended)
├── UBTI concerns for tax-exempts
├── ECI concerns for foreign investors
├── State tax nexus issues
├── Different treatment by LP type
└── Tax considerations influence structure

LP TYPE MATTERS:
┌─────────────────────────────────────────────────────────────────┐
│ LP Type              │ Key Tax Concerns                        │
│──────────────────────┼─────────────────────────────────────────│
│ Taxable US LP        │ K-1 timing, state taxes                 │
│ Tax-exempt US LP     │ UBTI from leverage/operations           │
│ Foreign LP           │ ECI, withholding, treaty benefits       │
│ Pension fund         │ UBTI (minor), unrelated to mission      │
│ Insurance company    │ Separate account vs general account     │
└─────────────────────────────────────────────────────────────────┘
```

### Fund Structure Overview

```
TYPICAL PE FUND STRUCTURE
─────────────────────────

BASIC STRUCTURE:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    LIMITED PARTNERS (LPs)                       │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
│   │ Pension │  │ Endow-  │  │ Family  │  │ Foreign │          │
│   │  Fund   │  │  ment   │  │ Office  │  │   LP    │          │
│   └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘          │
│        │            │            │            │                 │
│        └────────────┴────────────┴────────────┘                 │
│                          │                                      │
│                          ▼                                      │
│              ┌───────────────────────┐                         │
│              │    PE FUND LP         │                         │
│              │   (Delaware LP)       │  ◄── Pass-through       │
│              │                       │      entity             │
│              └───────────┬───────────┘                         │
│                          │                                      │
│              ┌───────────┴───────────┐                         │
│              ▼                       ▼                         │
│     ┌─────────────────┐    ┌─────────────────┐                │
│     │  Portfolio Co A │    │  Portfolio Co B │                │
│     └─────────────────┘    └─────────────────┘                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 20.2 K-1 Reporting

### What is a K-1?

```
SCHEDULE K-1 BASICS
───────────────────

WHAT IT IS:
├── Tax form reporting LP's share of partnership income/loss
├── Issued by the fund (GP) to each LP
├── Used to complete LP's own tax return
└── Form 1065 Schedule K-1 for partnerships

KEY INFORMATION REPORTED:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  BOX 1:  Ordinary business income (loss)                       │
│  BOX 2:  Net rental real estate income                         │
│  BOX 3:  Other net rental income                               │
│  BOX 4:  Guaranteed payments                                   │
│  BOX 5:  Interest income                                       │
│  BOX 6:  Dividends                                             │
│  BOX 7:  Royalties                                             │
│  BOX 8:  Net short-term capital gain                           │
│  BOX 9:  Net long-term capital gain                            │
│  BOX 10: Net Section 1231 gain                                 │
│  BOX 11: Other income                                          │
│  BOX 12: Section 179 deduction                                 │
│  BOX 13: Other deductions                                      │
│  ...                                                           │
│  BOX 20: Other information (foreign taxes, etc.)               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### K-1 Timing Challenges

```
K-1 TIMELINE PROBLEM
────────────────────

TAX FILING DEADLINES:
├── Individual returns: April 15 (or October 15 extended)
├── Corporate returns: April 15 (calendar year)
├── Partnership K-1s due: March 15
└── BUT PE funds often late...

TYPICAL PE K-1 TIMELINE:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ Dec 31:     Fund year-end                                       │
│ Jan-Feb:    Fund receives portfolio company financials          │
│ Feb-Mar:    Fund prepares draft K-1s                           │
│ Mar 15:     Deadline (often extended)                          │
│ Apr-May:    Draft K-1s issued                                  │
│ May-Jun:    Final K-1s issued                                  │
│ Jul-Sep:    Amended K-1s (common!)                             │
│                                                                 │
│ RESULT: LP often can't file tax return on time                 │
│         Must file extension, wait for K-1s                     │
│         May need to amend return later                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

WHY K-1s ARE LATE:
├── Fund invests in multiple portfolio companies
├── Portfolio companies have own reporting timelines
├── Complex structures (holding companies, blockers)
├── International investments
├── Audit requirements
└── Amendment cascade (one change → re-issue all K-1s)
```

### K-1 Example

```
SAMPLE K-1 DATA
───────────────

LP: Midwest Pension Fund
Fund: ABC Partners VII, L.P.
Tax Year: 2024
LP Ownership: 5%

INCOME/(LOSS) ITEMS:
┌─────────────────────────────────────────────────────────────────┐
│ Box │ Description                    │ Amount                  │
│─────┼────────────────────────────────┼─────────────────────────│
│ 1   │ Ordinary business income       │ $125,000                │
│ 5   │ Interest income                │ $18,500                 │
│ 6a  │ Qualified dividends            │ $42,000                 │
│ 8   │ Net short-term capital gain    │ ($15,000)               │
│ 9a  │ Net long-term capital gain     │ $2,450,000              │
│ 11  │ Other income (Section 1256)    │ $8,200                  │
│ 13K │ Section 754 deductions         │ ($45,000)               │
│ 20  │ Foreign taxes paid             │ $12,500                 │
└─────────────────────────────────────────────────────────────────┘

CAPITAL ACCOUNT:
├── Beginning balance:     $12,500,000
├── Capital contributions: $1,500,000
├── Distributions:        ($800,000)
├── Share of income:       $2,583,700
├── Ending balance:        $15,783,700

STATE TAX ATTACHMENTS:
├── CA Schedule K-1
├── NY Schedule K-1
├── TX (no state income tax)
└── DE (no state income tax on LPs)
```

---

## 20.3 UBTI (Unrelated Business Taxable Income)

### What is UBTI?

```
UBTI BASICS
───────────

APPLIES TO:
├── Tax-exempt organizations
├── Pension funds (401k, defined benefit)
├── Endowments and foundations
├── IRAs and retirement accounts
├── Some governmental entities
└── Charities (501(c)(3))

CONCEPT:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ Tax-exempt entities don't pay tax on investment income...      │
│                                                                 │
│ BUT they DO pay tax on "unrelated business" income             │
│                                                                 │
│ WHY? To prevent unfair competition with taxable businesses     │
│                                                                 │
│ EXAMPLES:                                                       │
│ ├── University endowment owns a hotel → UBTI                   │
│ ├── Pension fund receives dividends → NOT UBTI                 │
│ ├── Foundation earns interest → NOT UBTI                       │
│ ├── Endowment receives income from leveraged investment → UBTI │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### UBTI Sources in PE

```
UBTI TRIGGERS IN PRIVATE EQUITY
───────────────────────────────

1. DEBT-FINANCED INCOME
   └── Income from assets acquired with debt
   └── Most common UBTI source in PE

   Example:
   ├── Fund uses leverage to buy company
   ├── Company generates income
   ├── Portion attributable to debt = UBTI
   └── Even dividends/cap gains can be UBTI if leveraged

2. OPERATING BUSINESS INCOME
   └── Pass-through of active business income
   └── Fund receives K-1 with ordinary income

   Example:
   ├── Portfolio company is operating business
   ├── Structured as LLC or partnership
   ├── Income flows through to fund, then to LP
   └── Flow-through operating income = UBTI

3. CERTAIN SERVICE INCOME
   └── GP management company income
   └── Usually not applicable to LP

UBTI CALCULATION (Debt-Financed):
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ UBTI = Investment Income × Average Debt/Average Asset Basis    │
│                                                                 │
│ Example:                                                        │
│ ├── Investment income: $100,000                                │
│ ├── Average debt: $60M                                         │
│ ├── Average adjusted basis: $100M                              │
│ ├── Debt fraction: 60%                                         │
│ └── UBTI: $100,000 × 60% = $60,000 taxable                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### UBTI Management

```
UBTI MITIGATION STRATEGIES
──────────────────────────

1. BLOCKER CORPORATIONS
   └── Interpose C-corp between fund and LP
   └── Corp pays tax; LP receives dividends (not UBTI)
   └── Cost: Corporate tax layer

2. UBTI-SENSITIVE FUND STRUCTURES
   └── Fund documents address UBTI
   └── GP monitors and manages UBTI exposure
   └── Allocations structured to minimize

3. UBTI TOLERANCE
   └── Some tax-exempts accept modest UBTI
   └── File Form 990-T
   └── Pay tax at trust rates (up to 37%)
   └── Administrative burden but manageable

4. ASSET SELECTION
   └── Avoid investments generating UBTI
   └── Less leverage, fewer operating company pass-throughs
   └── May limit investment universe

UBTI THRESHOLDS:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ $1,000 DE MINIMIS:                                              │
│ ├── First $1,000 of UBTI exempt                                │
│ └── But administrative burden remains                          │
│                                                                 │
│ PRACTICAL TOLERANCE:                                            │
│ ├── Many pensions tolerate some UBTI                           │
│ ├── Balance: Return potential vs tax/admin cost                │
│ └── Monitor cumulative exposure across funds                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 20.4 ECI (Effectively Connected Income)

### What is ECI?

```
ECI BASICS
──────────

APPLIES TO:
├── Non-US investors (foreign LPs)
├── Foreign governments/sovereigns
├── Foreign pension funds
├── Foreign individuals
└── Foreign corporations

CONCEPT:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ Foreign investors generally not taxed on US investment income  │
│ (dividends, interest, capital gains on securities)             │
│                                                                 │
│ BUT they ARE taxed on income "effectively connected" with      │
│ a US trade or business (ECI)                                   │
│                                                                 │
│ ECI CONSEQUENCES:                                               │
│ ├── Taxed at US rates (up to 37% individual, 21% corp)        │
│ ├── Must file US tax return                                    │
│ ├── Withholding requirements                                   │
│ └── Branch profits tax (additional 30%)                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### ECI Sources in PE

```
ECI TRIGGERS FOR FOREIGN LPs
────────────────────────────

1. US OPERATING BUSINESS
   └── PE fund invests in US operating company
   └── Structured as partnership/LLC (pass-through)
   └── Operating income flows to foreign LP
   └── = ECI

2. DEBT-FINANCED US REAL ESTATE
   └── FIRPTA rules
   └── Gains on US real property interests
   └── Subject to US tax

3. US TRADE OR BUSINESS ACTIVITY
   └── Portfolio company activities
   └── Active management in US
   └── Creates US tax nexus

ECI vs NON-ECI INCOME:
┌─────────────────────────────────────────────────────────────────┐
│ Income Type              │ Typical Treatment for Foreign LP    │
│──────────────────────────┼─────────────────────────────────────│
│ Portfolio dividends      │ 30% withholding (or treaty rate)   │
│ Portfolio interest       │ Generally exempt                    │
│ Capital gains (stock)    │ Generally exempt                    │
│ US operating income      │ ECI - taxed at US rates            │
│ US real estate gains     │ FIRPTA - taxed at US rates         │
│ Pass-through income      │ ECI if trade or business           │
└─────────────────────────────────────────────────────────────────┘
```

### ECI Management

```
ECI MITIGATION STRATEGIES
─────────────────────────

1. BLOCKER CORPORATIONS
   └── Most common solution
   └── US or offshore corporation
   └── Corp invests in fund
   └── Foreign LP owns corp stock
   └── Corp receives ECI, pays US tax
   └── LP receives dividends (withholding, not ECI)

   Structure:
   ┌─────────────────────────────────────────────────────────┐
   │                                                         │
   │     Foreign LP                                          │
   │         │                                               │
   │         │ (Stock ownership)                             │
   │         ▼                                               │
   │    ┌─────────────┐                                     │
   │    │  BLOCKER    │  ◄── Cayman or Delaware corp       │
   │    │  CORP       │      Pays US tax on ECI            │
   │    └──────┬──────┘                                     │
   │           │                                             │
   │           │ (LP interest)                               │
   │           ▼                                             │
   │    ┌─────────────┐                                     │
   │    │  PE FUND    │                                     │
   │    └─────────────┘                                     │
   │                                                         │
   └─────────────────────────────────────────────────────────┘

2. PARALLEL FUND STRUCTURES
   └── Separate vehicles for foreign investors
   └── Structured to avoid ECI

3. TREATY BENEFITS
   └── Some treaties reduce/eliminate certain taxes
   └── Depends on LP jurisdiction
   └── Requires proper documentation
```

---

## 20.5 Blocker Structures

### Why Use Blockers?

```
BLOCKER CORPORATION RATIONALE
─────────────────────────────

PURPOSE:
├── Shield LPs from UBTI (tax-exempt)
├── Shield LPs from ECI (foreign)
├── Simplify tax reporting (one corporate return vs K-1s)
└── Provide investment flexibility

HOW IT WORKS:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ WITHOUT BLOCKER:                                                │
│                                                                 │
│ Tax-Exempt LP ──► Fund ──► Portfolio Co (operating income)     │
│                                                                 │
│ Result: UBTI flows through, LP pays tax                        │
│                                                                 │
│ ──────────────────────────────────────────────────────────────  │
│                                                                 │
│ WITH BLOCKER:                                                   │
│                                                                 │
│ Tax-Exempt LP ──► Blocker Corp ──► Fund ──► Portfolio Co       │
│                                                                 │
│ Result: Blocker pays corporate tax                             │
│         LP receives dividends (exempt income)                  │
│         No UBTI to LP                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Blocker Economics

```
BLOCKER TAX ANALYSIS
────────────────────

SCENARIO: $1,000 of operating income

WITHOUT BLOCKER (UBTI):
├── Income to tax-exempt LP: $1,000
├── UBTI tax (37% rate): $370
├── Net to LP: $630
└── Effective rate: 37%

WITH BLOCKER:
├── Income to blocker corp: $1,000
├── Corporate tax (21%): $210
├── After-tax profit: $790
├── Dividend to LP: $790
├── LP tax on dividend: $0 (tax-exempt)
├── Net to LP: $790
└── Effective rate: 21%

BLOCKER BENEFIT: 16% tax savings (21% vs 37%)

ADDITIONAL COSTS:
├── Blocker formation: $10-25K
├── Annual administration: $10-20K
├── Corporate tax returns: $5-15K
└── Liquidation costs: $10-25K

BREAKEVEN:
├── Need sufficient UBTI to justify blocker costs
├── Rule of thumb: >$50K annual UBTI makes sense
├── Consider fund-level blockers (shared costs)
```

### Types of Blockers

```
BLOCKER STRUCTURES
──────────────────

1. US C-CORPORATION
   ├── Simple, domestic structure
   ├── 21% federal corporate tax
   ├── Dividend withholding on foreign owners
   └── Most common for US tax-exempts

2. OFFSHORE CORPORATION (Cayman, Luxembourg)
   ├── No local tax in offshore jurisdiction
   ├── Still pays US tax on ECI
   ├── Avoids branch profits tax
   ├── Common for foreign investors
   └── More complex/costly

3. FUND-LEVEL BLOCKER
   ├── GP creates blocker for all UBTI-sensitive LPs
   ├── Shared administrative costs
   ├── Investors subscribe to blocker
   └── Most efficient for multiple investors

4. LP-SPECIFIC BLOCKER
   ├── Individual LP creates own blocker
   ├── Full control and flexibility
   ├── Higher cost per LP
   └── Common for large allocators

PARALLEL FUND STRUCTURE:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐       │
│  │ US Taxable   │   │ Tax-Exempt   │   │ Foreign      │       │
│  │ LPs          │   │ LPs          │   │ LPs          │       │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘       │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐       │
│  │ MAIN FUND    │   │ BLOCKER      │   │ OFFSHORE     │       │
│  │ (Direct)     │   │ FUND         │   │ FEEDER       │       │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘       │
│         │                  │                  │                 │
│         └──────────────────┼──────────────────┘                 │
│                            │                                    │
│                            ▼                                    │
│                   ┌─────────────────┐                          │
│                   │ MASTER FUND     │                          │
│                   │ (Investments)   │                          │
│                   └─────────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 20.6 State Tax Considerations

### Multi-State Nexus

```
STATE TAX NEXUS IN PE
─────────────────────

PROBLEM:
├── PE fund invests in companies across multiple states
├── Each state may claim taxing right
├── Creates compliance burden for LPs
└── State K-1s/filing requirements

NEXUS TRIGGERS:
├── Portfolio company operations in state
├── Real property in state
├── Employees in state
├── Sales into state (economic nexus)
└── LP residence in state

EXAMPLE K-1 STATE ATTACHMENTS:
┌─────────────────────────────────────────────────────────────────┐
│ Fund ABC Partners VII has nexus in:                            │
│                                                                 │
│ State        │ LP Share of State Income │ Filing Required?     │
│──────────────┼──────────────────────────┼─────────────────────│
│ California   │ $125,000                 │ Yes                  │
│ New York     │ $89,000                  │ Yes                  │
│ Texas        │ N/A (no income tax)      │ No                   │
│ Illinois     │ $42,000                  │ Yes                  │
│ Massachusetts│ $18,000                  │ Maybe (threshold)    │
│ Florida      │ N/A (no income tax)      │ No                   │
│                                                                 │
│ LP may need to file 4-5 state returns from ONE fund!           │
└─────────────────────────────────────────────────────────────────┘
```

### Composite Returns

```
COMPOSITE RETURNS
─────────────────

WHAT THEY ARE:
├── Fund files state returns on behalf of LPs
├── LP doesn't file individual state return
├── Fund withholds and remits state tax
└── Simplifies LP compliance

AVAILABILITY:
├── Most states allow composite filing
├── Usually optional for LPs
├── Some restrictions (minimum income, LP type)
└── Check fund LPA for composite provisions

EXAMPLE:
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│ WITHOUT COMPOSITE:                                              │
│ ├── LP receives CA K-1 showing $50,000 income                  │
│ ├── LP files CA nonresident return                             │
│ ├── LP pays CA tax (~$4,500)                                   │
│ └── Administrative burden on LP                                │
│                                                                 │
│ WITH COMPOSITE:                                                 │
│ ├── Fund files composite return including LP                   │
│ ├── Fund withholds $4,500 from distributions                   │
│ ├── LP receives net distribution                               │
│ └── No CA filing required by LP                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 20.7 Tax Reporting Timeline

### Annual Tax Calendar

```
PE TAX REPORTING CALENDAR
─────────────────────────

DECEMBER 31: Fund year-end (most common)

JANUARY - FEBRUARY:
├── Fund collects portfolio company financials
├── Fund accountants begin K-1 preparation
└── LPs should plan for extensions

MARCH 15:
├── Partnership K-1 deadline
├── Most PE funds file extension
└── Estimate K-1s may be provided

APRIL 15:
├── Individual/corporate tax deadline
├── LPs without K-1s must extend
└── Estimated tax payments due

APRIL - JUNE:
├── Draft K-1s typically received
├── Final K-1s issued
└── LPs can begin return preparation

JULY - SEPTEMBER:
├── Amended K-1s common
├── May require LP amended returns
└── Fund audit completion

OCTOBER 15:
├── Extended individual deadline
├── Most LPs file by this date
└── Some K-1s still pending

DECEMBER:
├── Late amended K-1s possible
└── Plan for next year
```

### Managing K-1 Complexity

```
LP K-1 MANAGEMENT BEST PRACTICES
────────────────────────────────

1. EXPECT DELAYS
   └── Budget for extensions
   └── Don't promise timely filing
   └── Plan cash for estimated taxes

2. TRACK K-1s ACROSS FUNDS
   └── Spreadsheet: Fund, status, received date
   └── Follow up proactively
   └── Know which funds are historically late

3. COORDINATE WITH TAX ADVISOR
   └── Share fund documents early
   └── Discuss blocker/structure decisions
   └── Review K-1s promptly when received

4. UNDERSTAND AMENDMENTS
   └── Amended K-1s are normal
   └── May require amended returns
   └── Track changes year-over-year

5. STATE TAX PLANNING
   └── Opt into composite returns where available
   └── Understand nexus obligations
   └── Consider state-specific structures

6. UBTI/ECI MONITORING
   └── Track cumulative UBTI across funds
   └── Evaluate blocker cost/benefit annually
   └── Review fund structures at commitment
```

---

## 20.8 Summary

### Key Concepts

| Concept | Applies To | Issue | Solution |
|---------|-----------|-------|----------|
| K-1 | All LPs | Late reporting | Plan for delays |
| UBTI | Tax-exempt | Tax on leveraged/operating income | Blocker corp |
| ECI | Foreign | US tax on trade/business | Blocker corp |
| State tax | All US | Multi-state nexus | Composite returns |

### Key Takeaways

```
TAX SUMMARY
───────────

1. K-1s ARE ALWAYS LATE
   └── Plan tax timeline around delays and amendments

2. UBTI AFFECTS TAX-EXEMPTS
   └── Leverage and operating income create tax

3. ECI AFFECTS FOREIGN INVESTORS
   └── US trade or business income taxed

4. BLOCKERS SOLVE MANY PROBLEMS
   └── Trade corporate tax for simpler structure

5. STATE NEXUS CREATES COMPLEXITY
   └── Multiple state filings from PE investments

6. STRUCTURE DECISIONS MATTER
   └── Evaluate tax implications before committing
```

---

## Knowledge Check

1. What is a K-1 and why are they often delayed?
2. What is UBTI and which investors are affected?
3. What is ECI and how does it differ from UBTI?
4. How does a blocker corporation work?
5. What is a composite return?

<details>
<summary>Answers</summary>

1. A K-1 (Schedule K-1) is a tax form reporting an LP's share of partnership income, deductions, and credits. They're often delayed because PE funds must wait for portfolio company financials, have complex multi-layered structures, and may need to aggregate data from many investments before preparing LP-specific reports.

2. UBTI (Unrelated Business Taxable Income) is income from activities unrelated to an organization's tax-exempt purpose. It affects tax-exempt investors (pensions, endowments, foundations, IRAs). In PE, UBTI commonly arises from debt-financed income or pass-through operating business income.

3. ECI (Effectively Connected Income) is income connected to a US trade or business, which subjects foreign investors to US taxation. UBTI affects tax-exempt US investors; ECI affects foreign investors. Both can be blocked by corporate structures.

4. A blocker corporation sits between the LP and the fund. The corporation receives the problematic income (UBTI or ECI-generating), pays corporate tax, and distributes dividends to the LP. The LP receives dividends instead of pass-through income, avoiding UBTI or ECI treatment.

5. A composite return is a state tax return filed by the fund on behalf of multiple LPs. It simplifies compliance by eliminating the need for each LP to file individual nonresident state returns. The fund withholds state tax from distributions and remits on behalf of participating LPs.

</details>

---

## Exercise: Tax Structure Analysis

```
SCENARIO: New LP evaluating fund investment

LP Profile:
├── Type: University endowment (tax-exempt)
├── AUM: $2 billion
├── Current PE allocation: $200M across 15 funds
├── Average UBTI per fund: $25,000/year

New Fund:
├── Strategy: US mid-market buyout
├── Target return: 2.5x, 20% IRR
├── Leverage: 50-60% at deal level
├── Expected UBTI per LP: ~$75,000/year
├── GP offers blocker option (+15 bps fee)

Questions:
1. Why might this fund generate more UBTI than average?
2. Should the endowment use the blocker?
3. What other factors should influence this decision?
```

<details>
<summary>Answers</summary>

```
1. WHY MORE UBTI:
   ├── 50-60% deal leverage is moderately high
   ├── Debt-financed income creates UBTI
   ├── Mid-market buyout typically involves
   │   operating companies (vs pure holding)
   ├── Pass-through operating income adds UBTI
   └── $75K estimate suggests significant exposure

2. BLOCKER ANALYSIS:
   Without blocker:
   ├── UBTI: $75,000
   ├── Tax at 37%: $27,750/year
   ├── Plus: Filing Form 990-T
   └── Plus: Administrative burden

   With blocker:
   ├── Corporate tax at 21%: $15,750
   ├── Additional fee: 15 bps on NAV
   │   (If $10M investment, ~$15K/year)
   ├── Blocker admin costs: ~$10K/year
   └── Total cost: ~$40K/year

   RECOMMENDATION: Likely USE blocker
   ├── Tax savings: $12,000/year ($27,750 - $15,750)
   ├── Fees: ~$25K/year
   ├── Net cost: ~$13K more with blocker
   ├── BUT: Eliminates filing burden,
   │   simplifies reporting, reduces risk
   └── Breakeven shifts if UBTI higher than expected

3. OTHER FACTORS:
   ├── Endowment's overall UBTI position
   ├── Existing blocker infrastructure (cost sharing)
   ├── Risk tolerance for UBTI variability
   ├── Administrative capacity for 990-T filing
   ├── Board/investment committee preferences
   └── Expected investment size (larger = more benefit)
```

</details>

---

[← Module 19: ESG & Impact](19-esg-impact.md) | [Module 21: GP/LP Negotiations →](21-gp-lp-negotiations.md)

[← Back to Curriculum Overview](00-curriculum-overview.md)
