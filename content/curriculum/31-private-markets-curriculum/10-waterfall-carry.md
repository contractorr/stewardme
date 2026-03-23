# Module 10: Waterfall & Carried Interest

## Learning Objectives

By the end of this module, you will understand:
- What a distribution waterfall is and why it exists
- Preferred return (hurdle rate) mechanics
- The catch-up provision
- Carried interest calculations
- European vs American waterfalls
- Clawback provisions and how they protect LPs

---

## 10.1 Introduction to Waterfalls

### What is a Distribution Waterfall?

A **waterfall** defines the order and allocation of distributions between LPs and GP. It determines who gets paid, when, and how much.

```
WATERFALL CONCEPT
─────────────────

                    FUND PROCEEDS
                         │
                         ▼
              ┌──────────────────────┐
              │  STEP 1: Return of   │
              │       Capital        │────► To LPs
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  STEP 2: Preferred   │
              │  Return (Hurdle)     │────► To LPs
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  STEP 3: GP Catch-Up │────► To GP
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  STEP 4: Profit      │────► 80% LP
              │        Split         │────► 20% GP
              └──────────────────────┘
```

### Why Waterfalls Exist

| Purpose | Explanation |
|---------|-------------|
| **LP Protection** | LPs get money back first before GP profit share |
| **Return Threshold** | GP only earns carry on good performance |
| **Alignment** | GP incentivized to generate strong returns |
| **Clarity** | Explicit rules prevent disputes |

---

## 10.2 Waterfall Components

### Step 1: Return of Capital

```
RETURN OF CAPITAL
─────────────────

FIRST TIER: 100% to LPs until they receive
back their contributed capital.

PURPOSE:
• LPs shouldn't pay carry until they're "whole"
• GP has no claim until LP investment returned

WHAT COUNTS AS "CAPITAL":
• Called capital for investments
• Called for management fees
• Called for expenses
• (Sometimes excludes fees - varies by fund)

EXAMPLE:
LP Contributed: $100M
First $100M of distributions → 100% to LP
GP receives $0 until this is complete
```

### Step 2: Preferred Return (Hurdle Rate)

```
PREFERRED RETURN
────────────────

SECOND TIER: 100% to LPs until they receive
a minimum return on their capital.

TYPICAL HURDLE: 8% annually (IRR-based)

HOW IT WORKS:
• Compounds from date of each contribution
• Not a guaranteed return
• Threshold for GP to earn carry
• GP shares nothing until hurdle is cleared

CALCULATION OPTIONS:

1. COMPOUNDING HURDLE (Most Common)
   LP must achieve 8% IRR on contributions
   before GP receives any carry.

2. SIMPLE HURDLE (Less Common)
   LP must receive 8% × years × contributions
   (non-compounding)

EXAMPLE:
LP Contributed $100M over Years 1-2
8% compound hurdle over 5 years
Required return: ~$46M above capital
($100M × 1.08^5 - $100M ≈ $46M)
```

### Step 3: GP Catch-Up

```
GP CATCH-UP
───────────

THIRD TIER: GP receives 100% of next distributions
until GP has received 20% of total profits.

WHY IT EXISTS:
• GP got $0 during return of capital
• GP got $0 during preferred return
• Now GP "catches up" to their 20% share

CATCH-UP PERCENTAGES:

100% CATCH-UP (Standard):
• GP gets 100% until at 20% of profits
• Most common structure

50% CATCH-UP (LP-Friendly):
• GP gets 50%, LP gets 50%
• Takes longer for GP to catch up
• Less common but gaining traction

0% CATCH-UP (No Catch-Up):
• Skip to 80/20 split immediately
• Very LP-friendly, rare

EXAMPLE (100% Catch-Up):
Profit so far to LPs (hurdle): $46M
GP target share (20% of $46M): $11.5M
Catch-up amount: $11.5M goes 100% to GP
After catch-up: LP has $46M, GP has $11.5M
GP now at 20% of total profit distributed
```

### Step 4: Carried Interest Split

```
CARRIED INTEREST SPLIT
──────────────────────

FOURTH TIER: All remaining distributions
split 80% LP / 20% GP.

This continues until fund is fully liquidated.

EXAMPLE:
After catch-up, $50M remaining to distribute
LP receives: $50M × 80% = $40M
GP receives: $50M × 20% = $10M

THE 20% TO GP IS "CARRIED INTEREST"
• GP's profit share
• Also called "carry" or "promote"
• Typically taxed as capital gains
• What makes PE lucrative for GPs
```

---

## 10.3 Complete Waterfall Example

### Scenario Setup

```
WATERFALL CALCULATION EXAMPLE
─────────────────────────────

FUND DETAILS:
• Committed Capital: $500M
• Contributed Capital: $450M
• Total Distributions: $900M
• Hurdle Rate: 8% (compounded annually)
• Carry: 20%
• Catch-up: 100%
• Assume all capital called Year 1
• All distributions Year 5
• (Simplified for clarity)
```

### Step-by-Step Calculation

```
STEP 1: RETURN OF CAPITAL
─────────────────────────
Contributed Capital: $450M
Distributions to LPs: $450M
Remaining to Distribute: $450M

STEP 2: PREFERRED RETURN
────────────────────────
Calculate 8% hurdle on $450M over 4 years:
$450M × (1.08^4 - 1) = $450M × 0.3605 = $162M

Distributions to LPs: $162M
Remaining to Distribute: $288M

CHECKPOINT:
• LPs have received: $450M + $162M = $612M
• GP has received: $0
• Total profit distributed: $162M
• GP's target (20%): $40.5M

STEP 3: GP CATCH-UP
───────────────────
GP needs to "catch up" to 20% of profits.
Current profit: $162M
GP target: 20% × $162M = $32.4M

But catch-up also generates more profit...
The math: GP gets 100% until GP = 20% of ALL profits

Catch-up calculation:
Let X = catch-up amount
GP total = X
Total profit = $162M + X
GP target = 20% × ($162M + X)

Solving: X = 20% × ($162M + X)
X = $32.4M + 0.2X
0.8X = $32.4M
X = $40.5M

GP receives: $40.5M (100%)
Remaining to Distribute: $247.5M

CHECKPOINT:
• Total profit: $162M + $40.5M = $202.5M
• GP has: $40.5M = 20% of $202.5M ✓

STEP 4: CARRIED INTEREST SPLIT
──────────────────────────────
Remaining: $247.5M
Split: 80% LP / 20% GP

LP receives: $247.5M × 80% = $198M
GP receives: $247.5M × 20% = $49.5M

─────────────────────────────────────────
FINAL SUMMARY:
─────────────────────────────────────────
                        LP          GP
                        ──          ──
Return of Capital:      $450.0M     $0
Preferred Return:       $162.0M     $0
Catch-up:              $0          $40.5M
Carried Interest Split: $198.0M     $49.5M
─────────────────────────────────────────
TOTAL:                  $810.0M     $90.0M

VERIFICATION:
Total Distributed: $810M + $90M = $900M ✓
GP as % of Profit: $90M / $450M = 20% ✓
LP Multiple: $810M / $450M = 1.80x (net)
```

---

## 10.4 European vs American Waterfalls

### Key Difference

```
WATERFALL TYPES
───────────────

EUROPEAN (WHOLE-FUND) WATERFALL:
• GP only receives carry after ALL capital returned
• Calculated on whole fund basis
• LP-friendlier
• More common in Europe, increasingly global

AMERICAN (DEAL-BY-DEAL) WATERFALL:
• GP can receive carry on individual deals
• Before all capital is returned
• GP-friendlier
• Traditional US structure
• Clawback provision critical
```

### European Waterfall

```
EUROPEAN WATERFALL
──────────────────

STEP 1: Return of ALL Contributed Capital
        └── 100% to LPs

STEP 2: Preferred Return on ALL Capital
        └── 100% to LPs

STEP 3: GP Catch-up
        └── 100% to GP

STEP 4: 80/20 Split
        └── Carried Interest begins


TIMING:
Deal 1 exit → Return of Deal 1 capital (to LP)
Deal 2 exit → Return of Deal 2 capital (to LP)
...
Deal N exit → Once ALL capital returned + hurdle met
              → THEN GP catch-up begins
              → THEN 80/20 split

GP WAITS LONGER but no clawback risk
```

### American Waterfall

```
AMERICAN (DEAL-BY-DEAL) WATERFALL
─────────────────────────────────

APPLIED TO EACH DEAL SEPARATELY:

DEAL 1:
  Step 1: Return Deal 1 capital → LP
  Step 2: Preferred return on Deal 1 → LP
  Step 3: Catch-up → GP
  Step 4: 80/20 split

DEAL 2:
  (Same steps applied to Deal 2 proceeds)

PROBLEM:
• Early winners: GP gets carry
• Later losers: GP already has carry
• Fund overall might not earn hurdle
• GP was "overpaid"

SOLUTION: CLAWBACK PROVISION
• At fund end, calculate whole-fund performance
• If GP received too much carry, they pay it back
```

### Comparison Example

```
EUROPEAN vs AMERICAN: SAME FUND
───────────────────────────────

FUND:
• $100M committed, $90M invested
• Deal A: $30M in → $60M out (2.0x) Year 3
• Deal B: $30M in → $30M out (1.0x) Year 5
• Deal C: $30M in → $45M out (1.5x) Year 7
• Total: $90M in → $135M out = 1.5x

AMERICAN WATERFALL:
Deal A (Year 3):
  Return of capital: $30M to LP
  Profit: $30M
  After hurdle/catch-up: ~$24M to LP, ~$6M to GP

Deal B (Year 5):
  Return of capital: $30M to LP
  No profit, no carry

Deal C (Year 7):
  Return of capital: $30M to LP
  Profit: $15M
  After hurdle/catch-up: ~$12M to LP, ~$3M to GP

GP TOTAL CARRY: ~$9M (paid as exits happen)

EUROPEAN WATERFALL:
All proceeds pooled:
  Return of all capital: $90M to LP first
  Then preferred return, catch-up, split

Fund overall profit: $45M
After hurdle calculation: ~$36M to LP, ~$9M to GP

GP TOTAL CARRY: ~$9M (but paid later, after all exits)

SAME ECONOMICS, DIFFERENT TIMING
In American: GP got $6M in Year 3
In European: GP waits until Year 7
```

---

## 10.5 Clawback Provisions

### What is Clawback?

```
CLAWBACK DEFINITION
───────────────────

A CLAWBACK requires the GP to return previously
distributed carried interest if the fund
ultimately doesn't achieve the hurdle return.

WHY IT'S NEEDED:
• American waterfall pays carry early
• Later losses might mean GP was overpaid
• Clawback "claws back" the excess

EUROPEAN WATERFALLS:
• No clawback needed
• GP doesn't get carry until fund succeeds
```

### Clawback Example

```
CLAWBACK EXAMPLE
────────────────

FUND HISTORY:
Year 3: Deal A exits at 3.0x
        GP receives $8M carry

Year 5: Deal B exits at 2.0x
        GP receives $5M carry

Year 7: Deal C written off (0x)
Year 8: Deal D exits at 0.5x
Year 9: Deal E exits at 1.0x

FUND TOTALS:
• Total invested: $100M
• Total returned: $120M
• Multiple: 1.2x
• Below 8% hurdle

CLAWBACK CALCULATION:
GP received: $13M in carry
GP entitled to (fund-level): $0 (below hurdle)
Clawback amount: $13M

GP MUST REPAY $13M TO LPs
```

### Clawback Mechanics

```
CLAWBACK STRUCTURE
──────────────────

WHEN CALCULATED:
• At fund termination
• After all assets liquidated
• Final accounting

PAYMENT MECHANICS:
• GP must pay from personal funds
• Often secured by escrow
• GP partners personally liable

ESCROW PROVISIONS:
• Some funds require GP to escrow portion of carry
• Typical: 20-30% of carry in escrow
• Released after final clawback calculation

PARTNER GUARANTEE:
• Individual GP partners guarantee clawback
• Joint and several liability
• Ensures LP can collect

TAX COMPLICATIONS:
• GP paid taxes on carry when received
• If clawed back, tax issues arise
• Some funds have tax gross-up provisions
```

### Clawback Limitations

```
CLAWBACK CONCERNS
─────────────────

POTENTIAL PROBLEMS:
├── GP may not have funds to repay
├── Partners may have left the firm
├── Tax already paid, hard to recover
├── Litigation to collect
└── Time value of money lost

PROTECTIONS:
├── Escrow requirements
├── Personal guarantees
├── Insurance (rare)
├── Conservative distribution policies
└── European waterfall (avoids issue)

PRACTICAL REALITY:
• Clawbacks are relatively rare
• Most funds do earn hurdle
• But protection is important
• Market trend toward European waterfall
```

---

## 10.6 Variations and Special Terms

### Hurdle Rate Variations

```
HURDLE RATE VARIATIONS
──────────────────────

STANDARD: 8% Compounding IRR
• Most common
• Hurdle compounds from each contribution

NO HURDLE (0%):
• GP earns carry on all profits
• Common in top-tier VC
• Very GP-friendly

HIGHER HURDLE (10%+):
• Seen in credit, infrastructure
• Matches lower return expectations
• LP-friendly for lower-return strategies

TIERED HURDLE:
• 8% hurdle for 20% carry
• 10% hurdle for 25% carry
• Rewards exceptional performance
```

### Catch-Up Variations

```
CATCH-UP VARIATIONS
───────────────────

100% CATCH-UP (Standard):
• GP gets 100% until at 20% of profits
• Fastest catch-up

80/20 CATCH-UP:
• GP gets 80%, LP gets 20%
• Slower catch-up
• Slightly LP-friendlier

50/50 CATCH-UP:
• GP and LP split 50/50
• Much slower catch-up
• LP-friendly

NO CATCH-UP:
• Skip directly to 80/20 split
• GP never "catches up"
• Very LP-friendly, rare
```

### Super Carry

```
SUPER CARRY (TIERED CARRY)
──────────────────────────

Some funds have escalating carry at higher returns:

EXAMPLE STRUCTURE:
• 8% hurdle: 20% carry (standard)
• 15% hurdle: 25% carry
• 25% hurdle: 30% carry

WHY IT EXISTS:
• Rewards exceptional performance
• Aligns GP with highest returns
• More common in growth/VC

EXAMPLE:
Fund returns 28% IRR
• First 8% return: No carry (to LP hurdle)
• 8-15% return: 20% carry
• 15-25% return: 25% carry
• 25%+ return: 30% carry
```

---

## 10.7 Calculating Your Carry/Waterfall

### LP Perspective

```
WHAT LP SHOULD TRACK
────────────────────

FROM YOUR REPORTS:

1. REALIZED CARRY
   • Carry actually paid to GP
   • Reduces your distributions
   • "Realized carried interest" line item

2. ACCRUED/UNREALIZED CARRY
   • Carry calculated but not yet paid
   • Reduces your NAV
   • "Accrued carried interest" in capital account

3. TOTAL CARRY
   • Realized + Unrealized
   • Full GP profit share to date

EXAMPLE FROM CAPITAL ACCOUNT:
Unrealized carried interest:    ($4,500,000)
(This is deducted from your NAV)

Realized carried interest (cumulative): $2,200,000
(This was deducted from distributions)

Total Carry Impact: $6,700,000
```

### Verify Waterfall Math

```
WATERFALL VERIFICATION
──────────────────────

GIVEN FUND DATA:
• Total Contributions: $450M
• Total Distributions: $900M
• Hurdle: 8%
• Years: 5

STEP 1: Check Return of Capital
Distributions should exceed contributions first
$900M > $450M ✓

STEP 2: Estimate Hurdle
$450M × 1.08^5 = $661M required for hurdle
Available: $900M, so hurdle cleared ✓

STEP 3: Calculate Total Profit
Profit = $900M - $450M = $450M

STEP 4: GP Share (Simplified)
GP should get ~20% of profit
$450M × 20% = $90M

STEP 5: Verify
LP receives: $900M - $90M = $810M
LP multiple: $810M / $450M = 1.80x net
Gross multiple: $900M / $450M = 2.0x

Looks reasonable ✓
```

---

## 10.8 Waterfall in Reports

### Distribution Notice Breakdown

```
DISTRIBUTION NOTICE (Sample)
────────────────────────────

ABC Partners Fund VII
Distribution Notice #12

Total Distribution: $150,000,000

WATERFALL ALLOCATION:
                              LP Share    GP Share
                              ────────    ────────
Return of Capital:            $85,000,000  $0
Preferred Return:             $35,000,000  $0
GP Catch-up:                  $0           $7,500,000
Carried Interest Split:       $18,000,000  $4,500,000
─────────────────────────────────────────────────────
TOTAL:                        $138,000,000 $12,000,000

YOUR SHARE (2.5% LP Interest):
Total LP Distribution:        $138,000,000
Your Share (2.5%):           $3,450,000

Wire Date: January 15, 2025
```

### Audited Financial Statement

```
STATEMENT OF CHANGES IN PARTNERS' CAPITAL
─────────────────────────────────────────

                           Limited    General
                           Partners   Partner    Total
                           ────────   ────────   ─────
Opening Balance            $1,500M    $15M       $1,515M

Capital Contributions      $0         $0         $0

Distributions:
  Return of Capital        ($200M)    $0         ($200M)
  Preferred Return         ($50M)     $0         ($50M)
  Carried Interest         ($40M)     ($10M)     ($50M)

Net Investment Income      $180M      $2M        $182M
Net Realized Gain          $120M      $3M        $123M
Net Unrealized Gain        $95M       $2M        $97M

Closing Balance            $1,605M    $12M       $1,617M

MEMO: Accrued Carried Interest
Opening:                   $42M
Change:                    $8M
Distributed:               ($10M)
Closing:                   $40M
```

---

## 10.9 Summary

### Key Waterfall Concepts

```
WATERFALL SUMMARY
─────────────────

1. RETURN OF CAPITAL
   • 100% to LPs
   • First priority

2. PREFERRED RETURN (HURDLE)
   • Typically 8% IRR
   • 100% to LPs
   • Threshold for GP profit

3. CATCH-UP
   • GP receives 100% (typically)
   • Until GP at 20% of profits

4. CARRIED INTEREST SPLIT
   • 80% LP / 20% GP
   • Continues until fund liquidated

WATERFALL TYPES:
• European: Whole-fund basis, GP waits
• American: Deal-by-deal, needs clawback

CLAWBACK:
• GP returns excess carry if fund underperforms
• Critical protection in American waterfall
```

---

## Knowledge Check

1. What is the purpose of a preferred return (hurdle rate)?
2. Explain the catch-up provision in your own words.
3. What's the main difference between European and American waterfalls?
4. Why is a clawback provision necessary?
5. If a fund has 20% carry and 8% hurdle, and returns 1.5x over 5 years, roughly what percentage of profits goes to GP?

<details>
<summary>Answers</summary>

1. The hurdle ensures LPs receive a minimum return (typically 8% IRR) before the GP participates in profits. It protects LPs from paying carry on mediocre returns.
2. After LPs get return of capital and hurdle, the GP received nothing. Catch-up lets the GP receive 100% of next distributions until the GP has 20% of all profits distributed so far, then they split 80/20 going forward.
3. European waterfall calculates carry on the whole fund (GP waits until all capital returned + hurdle). American waterfall allows carry deal-by-deal (GP gets carry earlier but needs clawback protection).
4. In American waterfall, GP receives carry on early winners. If later deals lose money, fund might not achieve hurdle overall. Clawback requires GP to return the "excess" carry.
5. At 1.5x over 5 years, IRR is ~8.4% - barely above hurdle. After hurdle, catch-up, and split, GP gets roughly 20% of profits ($50M profit × 20% = ~$10M), but the exact amount depends on the waterfall calculation.

</details>

---

## Calculation Exercise

```
Calculate the waterfall distribution:

Fund Details:
• Contributed Capital: $200M
• Total Distributions: $400M
• Fund Duration: 6 years
• Hurdle: 8% compound
• Carry: 20%
• Catch-up: 100%

Calculate:
1. Preferred return amount
2. Catch-up amount
3. Total to GP (carry)
4. Total to LP
5. LP net multiple
```

<details>
<summary>Answers</summary>

```
1. PREFERRED RETURN:
   $200M × (1.08^6 - 1) = $200M × 0.5869 = $117M

2. CATCH-UP:
   Profit after hurdle: $117M
   GP target: 20% of profit
   Catch-up: $117M × 20% / 80% = $29.3M
   (GP gets 100% until at 20% of total profit)

3. REMAINING TO SPLIT:
   Total: $400M
   - Return of capital: $200M
   - Preferred return: $117M
   - Catch-up: $29.3M
   Remaining: $53.7M

   GP share: $53.7M × 20% = $10.7M
   LP share: $53.7M × 80% = $43.0M

4. TOTAL TO GP (CARRY):
   Catch-up: $29.3M
   Profit split: $10.7M
   Total: $40.0M (20% of $200M profit ✓)

5. TOTAL TO LP:
   Return of capital: $200M
   Preferred return: $117M
   Profit split: $43M
   Total: $360M

   LP Net Multiple: $360M / $200M = 1.80x

VERIFICATION:
LP + GP = $360M + $40M = $400M ✓
GP = 20% of profit ($200M) = $40M ✓
```

</details>

---

## Next Module

[Module 11: Reading LP Reports →](11-lp-reports.md)

Learn to navigate and interpret the various reports LPs receive from GPs.
