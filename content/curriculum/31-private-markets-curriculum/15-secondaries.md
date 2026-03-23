# Module 15: Secondaries Deep-Dive

## Learning Objectives

By the end of this module, you will understand:
- Different types of secondary transactions (LP-led vs GP-led)
- Continuation vehicles and their structure
- Pricing mechanics and NAV discounts/premiums
- How secondaries mitigate the J-curve
- Due diligence considerations for secondary buyers

---

## 15.1 Secondary Market Overview

### What Are Secondaries?

**Secondary transactions** involve buying existing fund interests or assets, rather than committing to new funds (primaries).

```
PRIMARY vs SECONDARY
────────────────────

PRIMARY:
LP commits $100M ──► NEW Fund ──► Invests in companies

SECONDARY:
Original LP sells ──► Secondary Buyer acquires
existing $100M       existing position in
fund interest        EXISTING fund
```

### Market Size & Growth

```
SECONDARY MARKET VOLUME ($B)
────────────────────────────

2015: ████████████████ $40B
2018: ████████████████████████ $72B
2021: ████████████████████████████████████ $132B
2022: ████████████████████████████ $108B
2023: ████████████████████████████████ $114B

DRIVERS:
├── Portfolio rebalancing needs
├── Liquidity requirements
├── GP-led restructurings
├── Regulatory changes
└── Denominator effect during downturns
```

### Key Market Participants

```
SECONDARY MARKET PARTICIPANTS
─────────────────────────────

SELLERS:                       BUYERS:
├── Pensions (rebalancing)     ├── Dedicated secondary funds
├── Endowments (liquidity)     │   • Ardian, Lexington, Coller
├── Banks (regulatory)         │   • HarbourVest, Partners Group
├── Funds-of-funds             ├── Direct secondary investors
├── Family offices             ├── Sovereign wealth funds
└── Insurance companies        └── Some primary fund managers

INTERMEDIARIES:
├── Lazard
├── Evercore
├── Jefferies
├── Campbell Lutyens
└── PJT Partners
```

---

## 15.2 LP-Led Secondaries

### Traditional LP Secondary

The seller (LP) transfers their fund interest to a buyer.

```
LP-LED SECONDARY TRANSACTION
────────────────────────────

BEFORE:
┌──────────────┐         ┌──────────────┐
│   Original   │────────►│     Fund     │
│      LP      │ Interest│  (Year 6)    │
└──────────────┘         └──────────────┘

TRANSACTION:
┌──────────────┐         ┌──────────────┐
│   Original   │──$90M──►│   Secondary  │
│      LP      │◄────────│    Buyer     │
└──────────────┘ Interest└──────────────┘

AFTER:
┌──────────────┐         ┌──────────────┐
│   Secondary  │────────►│     Fund     │
│    Buyer     │ Interest│  (Year 6)    │
└──────────────┘         └──────────────┘

KEY ELEMENTS:
• NAV: $100M (as of last report)
• Price: $90M (10% discount to NAV)
• Buyer assumes unfunded commitment
• GP consent typically required
```

### Pricing Mechanics

```
SECONDARY PRICING EXAMPLE
─────────────────────────

Fund Position Details:
├── Original commitment: $50M
├── Called capital: $40M
├── Remaining unfunded: $10M
├── Current NAV: $55M
├── Distributions to date: $15M

PRICING CALCULATION:
┌─────────────────────────────────────────────┐
│ NAV (Net Asset Value)            $55.0M     │
│ Agreed discount                  × 0.90     │
│ ─────────────────────────────────────────── │
│ Price for NAV                    $49.5M     │
│                                             │
│ PLUS buyer assumes unfunded      $10.0M     │
│ ─────────────────────────────────────────── │
│ Total economic cost              $59.5M     │
└─────────────────────────────────────────────┘

DISCOUNT/PREMIUM DRIVERS:
├── Fund quality / GP reputation
├── Portfolio company outlook
├── Remaining fund life
├── Size of unfunded commitment
├── Market conditions
└── Deal complexity
```

### Portfolio Sales

```
PORTFOLIO SALE STRUCTURE
────────────────────────

Seller has multiple fund positions:
┌────────────────────────────────────────────┐
│  PORTFOLIO FOR SALE                        │
│                                            │
│  Fund A: NAV $20M, Unfunded $5M            │
│  Fund B: NAV $35M, Unfunded $3M            │
│  Fund C: NAV $15M, Unfunded $8M            │
│  Fund D: NAV $25M, Unfunded $2M            │
│  Fund E: NAV $18M, Unfunded $4M            │
│  ──────────────────────────────────        │
│  Total NAV: $113M, Unfunded: $22M          │
└────────────────────────────────────────────┘

BLENDED PRICING:
• Strong funds (A, B): Priced near par
• Weak fund (C): Deep discount (30%)
• Average funds (D, E): Modest discount (10%)
• Blended portfolio discount: ~12%
• Price: $99M for $113M NAV
```

---

## 15.3 GP-Led Secondaries

### What Are GP-Led Transactions?

GP-led secondaries involve the fund manager restructuring existing investments, typically through continuation vehicles.

```
GP-LED MARKET GROWTH
────────────────────

% of Secondary Market (GP-led):

2015: ████ 10%
2018: ████████ 20%
2021: ██████████████████████ 55%
2022: ██████████████████ 45%
2023: ████████████████████ 50%

GP-led has become ~50% of secondary volume
```

### Continuation Vehicles (CVs)

```
CONTINUATION VEHICLE STRUCTURE
──────────────────────────────

BEFORE: Original Fund (Year 8 of 10)
┌──────────────────────────────────────────┐
│                                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│  │Company A│ │Company B│ │Company C│    │
│  │ (sold)  │ │ (hold)  │ │ (hold)  │    │
│  └─────────┘ └─────────┘ └─────────┘    │
│              ◄──── "Crown Jewels" ────►  │
│                                          │
│  Original LPs want exit                  │
│  GP wants more time with B & C           │
└──────────────────────────────────────────┘

TRANSACTION:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Original Fund ──► Continuation Vehicle (NEW FUND)      │
│                                                         │
│  LPs CHOOSE:                                            │
│  ├── Option 1: SELL to CV at agreed price              │
│  │   └── Receive cash, exit completely                 │
│  │                                                      │
│  └── Option 2: ROLL into CV                            │
│      └── Maintain exposure, new fund terms             │
│                                                         │
│  Secondary Buyer: Provides capital for sellers          │
│  GP: Continues managing assets in new vehicle           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### CV Transaction Example

```
CONTINUATION VEHICLE EXAMPLE
────────────────────────────

Scenario:
├── Fund VII (2016 vintage) holds 3 portfolio companies
├── Combined NAV: $500M
├── GP believes 3-5 more years of value creation
├── Fund term ending, LPs want liquidity

CV TRANSACTION:
┌─────────────────────────────────────────────────────────┐
│ CAPITAL SOURCES                                         │
│                                                         │
│ Original LPs who SELL:        60% × $500M = $300M      │
│ Original LPs who ROLL:        15% × $500M = $75M       │
│ New Secondary Investor:       20% × $500M = $100M      │
│ GP Rollover:                  5%  × $500M = $25M       │
│                               ─────────────────────     │
│                               Total CV:     $500M      │
│                                                         │
│ CONSIDERATION PAID:                                     │
│ Secondary Buyer pays:         $300M (to selling LPs)    │
│ + committed for follow-on:    $50M                      │
│ ─────────────────────────                               │
│ Total secondary capital:      $350M                     │
└─────────────────────────────────────────────────────────┘

CV TERMS:
├── New 5-year fund life
├── Fresh carry (crystallized at transfer)
├── Management fee: 1.5% on NAV
├── Carry: 20% with 8% hurdle
└── GP commits 5%
```

### Types of GP-Led Transactions

```
GP-LED TRANSACTION TYPES
────────────────────────

1. SINGLE-ASSET CV
   └── One company transferred to new vehicle
   └── Maximum value creation focus
   └── Concentrated risk for buyer

2. MULTI-ASSET CV
   └── 2-5 companies transferred
   └── Some diversification
   └── "Best of" portfolio

3. STRIP SALE / FUND RESTRUCTURING
   └── Entire fund restructured
   └── All LPs offered options
   └── Full fund continuation

4. TENDER OFFER
   └── GP facilitates buyer offer to LPs
   └── LPs choose to sell or hold
   └── Fund structure unchanged

5. NAV LOAN + RECAP
   └── Fund borrows against NAV
   └── Distributions to LPs
   └── Hybrid liquidity solution
```

---

## 15.4 Pricing: Discounts and Premiums

### Historical Pricing Trends

```
SECONDARY PRICING TRENDS (Discount to NAV)
──────────────────────────────────────────

2015: ████████████████ -16% discount
2017: ██████████ -10% discount
2019: ██████ -6% discount
2021: ██ -2% discount (near par)
2022: ████████████████████ -20% discount
2023: ████████████████ -15% discount

WHAT DRIVES PRICING SHIFTS:
├── Buyer capital availability
├── Seller urgency
├── Public market valuations
├── Interest rates
└── GP marks (lag effect)
```

### Pricing by Fund Type

```
TYPICAL DISCOUNTS BY CATEGORY
─────────────────────────────

                          2021    2023
                          ────    ────
Buyout (top quartile)     Par     -5%
Buyout (median)           -3%     -12%
Buyout (bottom quartile)  -15%    -30%

Venture Capital           -10%    -25%
Growth Equity             -5%     -18%
Real Estate               -8%     -20%
Infrastructure            Par     -5%

GP-LED (quality assets)   Par     -5%
GP-LED (challenged)       -10%    -20%

FACTORS:
├── Asset quality matters more than ever
├── High rates pressure growth names
├── Infrastructure seen as defensive
└── GP-led premium for governance benefits
```

### The "Denominator Effect"

```
DENOMINATOR EFFECT ON SECONDARY SUPPLY
──────────────────────────────────────

SCENARIO: Public markets fall 30%

BEFORE:                    AFTER:
┌─────────────────────┐   ┌─────────────────────┐
│ Total Portfolio:$1B │   │ Total Portfolio:     │
│ ──────────────────  │   │ ──────────────────   │
│ Public:     $600M   │   │ Public:     $420M    │
│ (60%)               │   │ (51%)                │
│                     │   │                      │
│ Private:    $400M   │   │ Private:    $400M    │
│ (40%)               │   │ (49%) ◄── OVER!     │
└─────────────────────┘   └─────────────────────┘

• Target PE allocation: 40%
• Actual PE allocation: 49%
• Need to sell ~$80M of PE to rebalance
• Creates secondary supply
• Drives discounts wider
```

---

## 15.5 J-Curve Mitigation

### How Secondaries Eliminate the J-Curve

```
J-CURVE: PRIMARY vs SECONDARY
─────────────────────────────

PRIMARY INVESTMENT (new fund commitment):
IRR │
    │                              ╱────
+20%│                           ╱
    │                        ╱
+10%│                     ╱
    │                  ╱
  0%│───────────────╱─────────────────
    │            ╱
-10%│         ╱
    │      ╱
-20%│   ╱
    └─────────────────────────────────►
      1   2   3   4   5   6   7   8   Year

SECONDARY INVESTMENT (buy Year 5 position at discount):
IRR │
    │       ╱──────────────────────
+20%│    ╱
    │  ╱
+10%│╱
    │
  0%│─────────────────────────────────
    │
    └─────────────────────────────────►
         5   6   7   8   9   10   Year

SECONDARY BENEFITS:
├── No J-curve: Buying mature assets
├── Discount: Built-in margin of safety
├── Faster distributions: Assets closer to exit
├── Known portfolio: Can evaluate actual companies
└── Shorter duration: 3-5 years vs 10-12 years
```

### Return Profile Comparison

```
RETURN COMPARISON EXAMPLE
─────────────────────────

PRIMARY INVESTMENT:
├── Commit Year 0: $100M
├── IRR Years 1-3: Negative (J-curve)
├── Final IRR Year 10: 18%
├── Duration: 10 years
└── DPI after 5 years: 0.4x

SECONDARY INVESTMENT (buy same fund at Year 5):
├── Purchase Year 5: $85M for $100M NAV (15% discount)
├── IRR Year 1: Positive (no J-curve)
├── Final IRR Year 5: 20%
├── Duration: 5 years
└── DPI after 2 years: 0.6x

WHY SECONDARY RETURNS CAN BE HIGHER:
├── Discount to NAV provides "buffer"
├── Buying into value creation already done
├── Avoiding fee drag of early years
├── More visibility into portfolio
└── GP already de-risked investments
```

### Pacing with Secondaries

```
PORTFOLIO CONSTRUCTION WITH SECONDARIES
───────────────────────────────────────

Traditional Primary-Only Approach:
Year 1: Commit $100M → Deploy over 3-5 years
Year 2: Commit $100M → Deploy over 3-5 years
Year 3: Commit $100M → Deploy over 3-5 years
...
Takes 5-7 years to reach target exposure

Primary + Secondary Approach:
Year 1: Commit $50M primary + $50M secondary
├── Primary: Builds future exposure
└── Secondary: Immediate exposure, faster returns

SECONDARY FOR "INSTANT" EXPOSURE:
┌─────────────────────────────────────────────┐
│ New allocation to PE: $200M target          │
│                                             │
│ Option A: 100% Primary                      │
│ ├── Year 1 actual exposure: ~$30M           │
│ └── Reach target: Year 5-6                  │
│                                             │
│ Option B: 50% Primary + 50% Secondary       │
│ ├── Year 1 actual exposure: ~$115M          │
│ └── Reach target: Year 2-3                  │
└─────────────────────────────────────────────┘
```

---

## 15.6 Due Diligence for Secondary Buyers

### LP-Led Due Diligence

```
LP-LED SECONDARY DUE DILIGENCE
──────────────────────────────

1. PORTFOLIO COMPANY ANALYSIS
   ├── Financial performance (revenue, EBITDA)
   ├── Valuation methodology review
   ├── Comparable company analysis
   ├── Exit pathway assessment
   └── Management team quality

2. GP ASSESSMENT
   ├── Track record analysis
   ├── Team stability
   ├── Strategy consistency
   ├── Reference calls
   └── Reputation in market

3. FUND TERMS REVIEW
   ├── Remaining fund life
   ├── Extension provisions
   ├── Fee structure (step-down?)
   ├── Carried interest waterfall
   └── Key person provisions

4. UNFUNDED ANALYSIS
   ├── Remaining commitment size
   ├── Expected call schedule
   ├── Follow-on reserves
   └── Recycling provisions

5. LEGAL/STRUCTURAL
   ├── Transfer restrictions
   ├── GP consent process
   ├── ROFR provisions
   ├── Tax considerations
   └── ERISA/regulatory issues
```

### GP-Led Due Diligence

```
GP-LED / CV DUE DILIGENCE
─────────────────────────

ADDITIONAL CONSIDERATIONS:

1. CONFLICT OF INTEREST ANALYSIS
   ├── Is price fair to rolling LPs?
   ├── Is price fair to new investors?
   ├── GP economic incentives
   ├── Independent fairness opinion?
   └── LPAC involvement

2. CV TERMS SCRUTINY
   ├── New carry structure
   ├── Management fee economics
   ├── GP commitment size
   ├── Governance rights
   └── Exit provisions

3. BUSINESS PLAN REVIEW
   ├── Why does GP need more time?
   ├── Value creation plan credibility
   ├── Required capital investment
   ├── Exit timeline assumptions
   └── Downside scenarios

4. MARKET CHECK
   ├── Was asset marketed broadly?
   ├── Competitive bidding process?
   ├── Price discovery quality
   └── Alternatives considered

RED FLAGS:
⚠ GP received no competing bids
⚠ Very high management fees
⚠ No GP co-investment
⚠ Unrealistic projections
⚠ Compressed timeline for decision
```

### Valuation Considerations

```
SECONDARY VALUATION APPROACHES
──────────────────────────────

1. NAV ANCHOR
   ├── Start with GP's reported NAV
   ├── Adjust for staleness (3-6 month lag)
   ├── Compare to public comps
   └── Apply discount/premium

2. BOTTOM-UP COMPANY VALUATION
   ├── Value each portfolio company
   ├── Apply appropriate multiples
   ├── Sum of parts vs NAV
   └── Identify gaps

3. IMPLIED RETURNS ANALYSIS
   ├── At purchase price, what IRR needed?
   ├── Sensitivity to exit multiples
   ├── Sensitivity to timing
   └── Compare to target returns

EXAMPLE:
┌─────────────────────────────────────────────┐
│ NAV: $100M                                  │
│ Purchase at 15% discount: $85M              │
│ Expected exit value (3 yrs): $130M          │
│                                             │
│ Implied IRR: ($130M/$85M)^(1/3) - 1 = 15%  │
│                                             │
│ SENSITIVITY:                                │
│ Exit at $110M: IRR = 9%                     │
│ Exit at $150M: IRR = 21%                    │
│ Exit takes 5 yrs at $130M: IRR = 9%         │
└─────────────────────────────────────────────┘
```

---

## 15.7 Secondary Market Dynamics

### Buyer Strategies

```
SECONDARY BUYER STRATEGIES
──────────────────────────

1. DIVERSIFIED FUND BUYER
   ├── Large portfolios at discounts
   ├── Diversification benefit
   ├── Volume-based approach
   └── Target: 14-16% net IRR

2. CONCENTRATED / GP-LED SPECIALIST
   ├── Single/multi-asset CVs
   ├── Deep due diligence
   ├── Higher conviction
   └── Target: 18-22% net IRR

3. TAIL-END SPECIALIST
   ├── Very mature funds (Year 10+)
   ├── Deep discounts
   ├── Short duration
   └── Target: Quick realizations

4. PREFERRED EQUITY PROVIDER
   ├── NAV loans / structured solutions
   ├── Downside protection
   ├── Current yield
   └── Target: 12-15% IRR

5. DIRECT SECONDARY
   ├── Acquire companies directly
   ├── Not fund interests
   ├── Control orientation
   └── Hybrid PE/secondary
```

### Market Cycles

```
SECONDARY MARKET CYCLE
──────────────────────

                         SELLER'S       BUYER'S
                         MARKET         MARKET
                            │              │
                            ▼              ▼
PRICE    │    ╱╲          ╱╲          ╱╲
(% NAV)  │   ╱  ╲        ╱  ╲        ╱  ╲
 100%    │──╱────╲──────╱────╲──────╱────╲───
         │ ╱      ╲    ╱      ╲    ╱      ╲
  80%    │╱        ╲  ╱        ╲  ╱        ╲
         │          ╲╱          ╲╱
  60%    │
         └──────────────────────────────────►
            2007  2009  2014  2019  2022

SELLER'S MARKET:
├── More buyers than sellers
├── Prices near/above NAV
├── Competitive bidding
└── Quick transactions

BUYER'S MARKET:
├── More sellers than buyers
├── Deep discounts
├── Selective buying
└── Extended timelines
```

---

## 15.8 Summary

### Secondary Transaction Types

| Type | Description | Typical Discount | Duration |
|------|-------------|------------------|----------|
| LP Portfolio | Multi-fund sale | 10-20% | Varies |
| Single LP Interest | One fund sale | 5-15% | 3-5 yrs |
| Single-Asset CV | One company | 0-10% | 3-5 yrs |
| Multi-Asset CV | 2-5 companies | 0-10% | 3-5 yrs |
| Tender Offer | GP-facilitated | 10-15% | N/A |
| Tail-End | Mature funds | 20-40% | 1-2 yrs |

### Key Takeaways

```
SECONDARY MARKET SUMMARY
────────────────────────

1. Liquidity solution for illiquid asset class
2. GP-led now ~50% of market volume
3. Discounts vary with market conditions
4. Mitigates J-curve for buyers
5. Shorter duration than primaries
6. Due diligence critical on valuations
7. Continuation vehicles require conflict analysis
8. Strategic tool for portfolio construction
```

---

## Knowledge Check

1. What's the difference between LP-led and GP-led secondaries?
2. What is a continuation vehicle and why do GPs use them?
3. Why do secondary transactions mitigate the J-curve?
4. What is the "denominator effect" and how does it impact secondaries?
5. What are the key conflict considerations in GP-led transactions?

<details>
<summary>Answers</summary>

1. LP-led: Existing LP sells their fund interest to a buyer. GP-led: The GP restructures the fund, typically creating a new vehicle for select assets, giving LPs options to sell or roll their interest.

2. A continuation vehicle is a new fund created by the GP to hold select assets from an existing fund. GPs use them to gain more time for value creation when fund terms are expiring but they believe significant upside remains.

3. Secondary buyers acquire mature fund positions that have already weathered the J-curve period. The discount provides a margin of safety, and assets are closer to exit, generating faster distributions.

4. When public markets fall, PE allocation as a percentage of total portfolio increases (denominator shrinks). LPs become "overweight" PE and need to sell, increasing secondary supply and driving discounts wider.

5. Key conflicts: GP setting price that affects both selling and rolling LPs; GP economic incentives (new carry, fresh fees); whether process was competitive; fairness to all parties. Independent fairness opinions and LPAC involvement help address conflicts.

</details>

---

## Exercise: Secondary Transaction Analysis

```
SCENARIO: You're evaluating an LP secondary purchase

Fund Information:
├── Fund: Growth Partners V (2019 vintage)
├── Strategy: Growth equity
├── Original commitment: $75M
├── Called capital: $65M
├── Remaining unfunded: $10M
├── Current NAV: $90M
├── Distributions: $20M
├── Fund term: Year 5 of 10

Seller is offering at 12% discount to NAV.

Calculate:
1. Purchase price for NAV
2. Total economic cost (including unfunded)
3. Current TVPI and DPI
4. Implied TVPI needed for 15% IRR over 4 years
```

<details>
<summary>Answers</summary>

```
1. Purchase Price for NAV:
   NAV × (1 - discount) = $90M × 0.88 = $79.2M

2. Total Economic Cost:
   Purchase price + unfunded assumption
   = $79.2M + $10M = $89.2M

3. Current Fund Metrics:
   TVPI = (NAV + Distributions) / Called
        = ($90M + $20M) / $65M = 1.69x

   DPI = Distributions / Called
       = $20M / $65M = 0.31x

4. Implied TVPI for 15% IRR:
   Total outlay: $79.2M (purchase) + $10M (unfunded) = $89.2M

   Required proceeds in 4 years at 15% IRR:
   $89.2M × (1.15)^4 = $156.0M

   Already have $20M in distributions, need ~$136M more

   From buyer perspective:
   Invested $79.2M, need $79.2M × 1.15^4 = $138.5M
   Plus unfunded $10M returning at least $10M

   Implied exit TVPI from purchase price:
   $138.5M / $79.2M = 1.75x on entry price
```

</details>

---

[← Module 14: LP Customer Segments](14-lp-customer-segments.md) | [Module 16: Fund Financing →](16-fund-financing.md)

[← Back to Curriculum Overview](00-curriculum-overview.md)
