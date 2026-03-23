# Module 18: Benchmarking & Data

## Learning Objectives

By the end of this module, you will understand:
- Major PE data providers (Cambridge, Burgiss, Preqin, PitchBook)
- PME calculations and methodologies
- Peer group selection best practices
- Data limitations and survivorship bias
- How to interpret benchmark comparisons

---

## 18.1 The Benchmarking Challenge

### Why PE Benchmarking is Difficult

```
PE BENCHMARKING CHALLENGES
──────────────────────────

PUBLIC EQUITIES:
├── Returns observable daily
├── Standard calculation methods
├── Universal benchmarks (S&P 500)
├── No timing ambiguity
└── Complete data

PRIVATE EQUITY:
├── Returns reported quarterly (with lag)
├── Multiple calculation methods
├── No single standard benchmark
├── Cash flow timing matters
├── Incomplete, voluntary data
└── Survivorship bias

FUNDAMENTAL ISSUE:
┌─────────────────────────────────────────────────────────┐
│ Public benchmark: "What did the market return?"        │
│                   Clear answer: S&P 500 = 10.5%        │
│                                                         │
│ PE benchmark: "What did private equity return?"        │
│               Depends on:                               │
│               ├── Which data provider?                 │
│               ├── Which methodology?                   │
│               ├── Which peer group?                    │
│               ├── Which time period?                   │
│               └── Gross or net?                        │
└─────────────────────────────────────────────────────────┘
```

### Types of Benchmarks

```
BENCHMARK TYPES
───────────────

1. ABSOLUTE BENCHMARKS
   └── Target return (e.g., 15% net IRR)
   └── Simple but ignores market conditions

2. PEER GROUP BENCHMARKS
   └── Compare to similar funds
   └── Cambridge, Preqin pooled averages
   └── Most common approach

3. PUBLIC MARKET EQUIVALENT (PME)
   └── Compare to public market alternative
   └── Time-weighted public market comparison
   └── Answers: "Did PE beat public markets?"

4. POLICY BENCHMARKS
   └── Custom blend of public indices
   └── E.g., Russell 2000 + 300 bps
   └── Links to asset allocation policy
```

---

## 18.2 Major Data Providers

### Provider Overview

```
PE DATA PROVIDER LANDSCAPE
──────────────────────────

┌────────────────────────────────────────────────────────────────┐
│ Provider      │ Data Source    │ Strength           │ Users   │
│───────────────┼────────────────┼────────────────────┼─────────│
│ Cambridge     │ LP-submitted   │ Oldest, trusted    │ Inst'l  │
│ Associates    │ (voluntary)    │ benchmark standard │ LPs     │
│               │                │                    │         │
│ Burgiss       │ LP-submitted   │ Cash flow detail   │ LPs,    │
│               │ (via systems)  │ Portfolio-level    │ consult │
│               │                │                    │         │
│ Preqin        │ GP-reported    │ Breadth, emerging  │ GPs,    │
│               │ + research     │ managers, deal data│ LPs     │
│               │                │                    │         │
│ PitchBook     │ Research +     │ VC strength, deal  │ VCs,    │
│               │ LP submissions │ level, valuations  │ LPs     │
│               │                │                    │         │
│ Refinitiv/    │ Historical     │ Long history,      │ LPs     │
│ LSEG (Thomson)│ LP data        │ legacy data        │         │
└────────────────────────────────────────────────────────────────┘
```

### Cambridge Associates

```
CAMBRIDGE ASSOCIATES
────────────────────

HISTORY:
├── Founded 1973
├── Benchmarks since 1986
├── Gold standard for institutional LPs
└── Trusted by pension consultants

DATA SOURCE:
├── LP-submitted data (voluntary)
├── ~2,500+ funds in database
├── Quarterly performance updates
├── Cash flow level detail

BENCHMARK PRODUCTS:
├── US Private Equity Index
├── Global ex-US PE Index
├── Venture Capital Index
├── Real Estate Index
├── Private Credit Index
└── Strategy/geography sub-indices

METHODOLOGY:
├── Horizon pooled returns
├── Since inception pooled returns
├── Vintage year quartiles
├── Modified PME calculations
└── GIPS-compliant

PROS:
├── Industry standard
├── Long history
├── Trusted methodology
├── Consultant-accepted

CONS:
├── Voluntary = selection bias
├── Lag in data (quarters behind)
├── Limited emerging manager data
└── Expensive access
```

### Burgiss

```
BURGISS
───────

HISTORY:
├── Founded 1987
├── Originally LP software provider
├── Benchmark business from system data
└── Acquired by MSCI (2022)

DATA SOURCE:
├── Aggregated from LP software systems
├── ~10,000+ funds
├── Automatic data collection
├── Cash flow level detail

KEY PRODUCTS:
├── Private iQ (analytics platform)
├── Manager Universe
├── Total Plan benchmarks
└── Custom peer groups

METHODOLOGY:
├── Cash flow-based returns
├── Pooled and horizon returns
├── PME calculations
├── Custom benchmark builder

UNIQUE FEATURES:
├── Portfolio-level analytics
├── Factor analysis
├── Risk decomposition
├── LP-specific benchmarking

PROS:
├── Large dataset (automatic collection)
├── Cash flow detail
├── Sophisticated analytics
├── Portfolio-level tools

CONS:
├── Biased toward tech-enabled LPs
├── Newer than Cambridge
├── Less consultant familiarity
```

### Preqin

```
PREQIN
──────

HISTORY:
├── Founded 2003
├── Research-driven data collection
├── Acquired by Blackstone (2021)
└── Broadest alternative assets coverage

DATA SOURCE:
├── GP-reported data
├── FOIA requests
├── Research team outreach
├── LP submissions

KEY PRODUCTS:
├── Preqin Pro (database)
├── Benchmarks module
├── Fundraising data
├── Deal-level data
├── Investor profiles

COVERAGE:
├── Private Equity: 20,000+ funds
├── Real Estate: 8,000+ funds
├── Infrastructure: 3,000+ funds
├── Private Debt: 4,000+ funds
├── Hedge Funds: 25,000+ funds

PROS:
├── Broadest coverage
├── Emerging managers included
├── Fundraising data strength
├── Good for market research
├── More affordable

CONS:
├── GP-reported (potential bias)
├── Less LP adoption for benchmarks
├── Quality varies by strategy
├── Not as trusted for returns
```

### PitchBook

```
PITCHBOOK
─────────

HISTORY:
├── Founded 2007
├── VC/startup focus originally
├── Acquired by Morningstar (2016)
└── Expanded to full PE coverage

DATA SOURCE:
├── Research team
├── LP submissions
├── Public filings
├── GP relationships

KEY PRODUCTS:
├── PitchBook Platform
├── Fund performance data
├── Deal-level data
├── Valuation data
├── Company profiles

STRENGTHS:
├── Venture capital depth
├── Deal-level valuations
├── Company data
├── Exit data
├── GP/LP profiles

TYPICAL USERS:
├── VCs and growth investors
├── Corporate development
├── Investment banks
├── LPs (for deals)
└── Journalists/researchers

PROS:
├── Best VC data
├── Deal-level detail
├── User-friendly platform
├── Good for sourcing

CONS:
├── Newer PE benchmarks
├── Less institutional adoption
├── Focus on VC/growth
├── Not primary benchmark source
```

### Data Provider Comparison

```
PROVIDER COMPARISON MATRIX
──────────────────────────

                    Cambridge  Burgiss  Preqin  PitchBook
                    ─────────  ───────  ──────  ─────────
PE fund coverage    ★★★★       ★★★★★    ★★★★★   ★★★★
VC fund coverage    ★★★★       ★★★      ★★★★    ★★★★★
Cash flow detail    ★★★★       ★★★★★    ★★★     ★★★
Benchmark trust     ★★★★★      ★★★★     ★★★     ★★★
Deal-level data     ★★         ★★       ★★★★    ★★★★★
Fundraising data    ★★★        ★★       ★★★★★   ★★★★
Emerging managers   ★★★        ★★★      ★★★★★   ★★★★
Cost                $$$$$      $$$$     $$$     $$$
Ease of use         ★★★        ★★★★     ★★★★    ★★★★★

RECOMMENDATION BY USE CASE:
├── Institutional benchmarking: Cambridge
├── Portfolio analytics: Burgiss
├── Market research/fundraising: Preqin
├── VC/deal sourcing: PitchBook
└── Budget-conscious: Preqin or PitchBook
```

---

## 18.3 PME Calculations

### Public Market Equivalent Explained

```
PME CONCEPT
───────────

QUESTION PME ANSWERS:
"If I had invested my PE cash flows in public markets
instead, what would I have earned?"

METHODOLOGY:
┌─────────────────────────────────────────────────────────┐
│ For each PE cash flow:                                 │
│                                                         │
│ CONTRIBUTIONS (capital calls):                         │
│ └── Buy equivalent $ of public index                   │
│                                                         │
│ DISTRIBUTIONS:                                          │
│ └── Sell equivalent $ of public index                  │
│                                                         │
│ REMAINING NAV:                                          │
│ └── Compare to remaining public portfolio value        │
│                                                         │
│ PME > 1.0: PE outperformed public markets              │
│ PME < 1.0: PE underperformed public markets            │
└─────────────────────────────────────────────────────────┘
```

### PME Calculation Example

```
PME CALCULATION EXAMPLE
───────────────────────

PE Fund Cash Flows:
├── Year 0: -$100M (contribution)
├── Year 1: -$50M (contribution)
├── Year 3: +$40M (distribution)
├── Year 5: +$80M (distribution)
├── Year 5: NAV = $90M

S&P 500 Index Values:
├── Year 0: 1,000
├── Year 1: 1,100
├── Year 3: 1,300
├── Year 5: 1,600

STEP 1: Calculate FV of contributions in public index
┌─────────────────────────────────────────────────────────┐
│ Year 0 contribution: $100M × (1600/1000) = $160M       │
│ Year 1 contribution: $50M × (1600/1100) = $72.7M       │
│ ─────────────────────────────────────────────────────── │
│ Total FV of contributions: $232.7M                      │
└─────────────────────────────────────────────────────────┘

STEP 2: Calculate FV of distributions in public index
┌─────────────────────────────────────────────────────────┐
│ Year 3 distribution: $40M × (1600/1300) = $49.2M       │
│ Year 5 distribution: $80M × (1600/1600) = $80M         │
│ ─────────────────────────────────────────────────────── │
│ Total FV of distributions: $129.2M                      │
└─────────────────────────────────────────────────────────┘

STEP 3: Calculate PME
┌─────────────────────────────────────────────────────────┐
│ PE Total Value = Distributions + NAV = $120M + $90M    │
│                = $210M                                  │
│                                                         │
│ Public equivalent: $232.7M - $129.2M + reinvested     │
│                    = ~$185M (hypothetical)             │
│                                                         │
│ KAPLAN-SCHOAR PME = PE Value / Public Equivalent       │
│                   = $210M / $185M = 1.14               │
│                                                         │
│ INTERPRETATION: PE outperformed public markets by 14%  │
└─────────────────────────────────────────────────────────┘
```

### PME Methodologies

```
PME METHODOLOGY COMPARISON
──────────────────────────

1. KAPLAN-SCHOAR PME (KS-PME)
   └── Industry standard
   └── Ratio of PE wealth to public wealth
   └── Ignores timing differences
   └── PME > 1 = outperformed

2. PME+ (Cambridge)
   └── Scales distributions to match IRR
   └── Produces IRR-equivalent spread
   └── Better for comparing to IRR targets
   └── Output: IRR spread vs public

3. DIRECT ALPHA
   └── Geometric difference between PE and public
   └── Annualized outperformance
   └── Accounts for compounding
   └── Output: % per year

4. LONG-NICKELS PME
   └── Leverages public index to match PE risk
   └── Accounts for PE leverage
   └── More complex
   └── Controversial assumptions

PRACTICAL GUIDANCE:
├── Most use KS-PME or Cambridge PME+
├── Choose index that matches PE exposure
├── Consistency matters more than methodology
└── Always disclose methodology used
```

### Choosing the Right Public Index

```
PUBLIC INDEX SELECTION
──────────────────────

US BUYOUT:
├── S&P 500 (most common)
├── Russell 2000 (small/mid comparison)
├── Russell 2000 Value (value comparison)
└── Wilshire 5000 (broad market)

VENTURE CAPITAL:
├── NASDAQ Composite
├── Russell 2000 Growth
├── S&P 500 Info Tech
└── Custom tech indices

EUROPEAN PE:
├── MSCI Europe
├── STOXX Europe 600
├── Local indices (FTSE, DAX)

GLOBAL PE:
├── MSCI World
├── MSCI ACWI
└── Blended regional

BEST PRACTICE:
┌─────────────────────────────────────────────────────────┐
│ Match index to PE strategy characteristics:            │
│                                                         │
│ ├── Similar geography                                  │
│ ├── Similar size exposure                              │
│ ├── Similar sector exposure                            │
│ └── Similar risk profile                               │
│                                                         │
│ Example:                                                │
│ US mid-market buyout → Russell 2000 + leverage adj.   │
│ US growth equity → Russell 2000 Growth                 │
│ European buyout → MSCI Europe                          │
└─────────────────────────────────────────────────────────┘
```

---

## 18.4 Peer Group Selection

### Why Peer Groups Matter

```
PEER GROUP IMPACT ON QUARTILE
─────────────────────────────

Same fund, different peer groups:

FUND: Global Tech Growth IV
├── Net IRR: 18%

PEER GROUP A: All PE Funds (2018 vintage)
├── Median IRR: 14%
├── Top quartile: >18%
└── Fund ranking: BORDERLINE 1ST QUARTILE

PEER GROUP B: Growth Equity (2018 vintage)
├── Median IRR: 16%
├── Top quartile: >22%
└── Fund ranking: 2ND QUARTILE

PEER GROUP C: Tech-Focused Growth (2018 vintage)
├── Median IRR: 20%
├── Top quartile: >28%
└── Fund ranking: 3RD QUARTILE

SAME FUND = DIFFERENT QUARTILE DEPENDING ON PEER GROUP
```

### Peer Group Dimensions

```
PEER GROUP STRATIFICATION
─────────────────────────

DIMENSION 1: VINTAGE YEAR
├── Critical for fair comparison
├── Same market entry conditions
└── Usually exact year match

DIMENSION 2: STRATEGY
├── Buyout vs Venture vs Growth
├── Distressed vs Core
├── Primary vs Secondary
└── Generalist vs Sector-focused

DIMENSION 3: GEOGRAPHY
├── North America
├── Europe
├── Asia
├── Global
└── Emerging markets

DIMENSION 4: SIZE
├── Mega ($10B+)
├── Large ($5-10B)
├── Upper Mid ($1-5B)
├── Lower Mid ($250M-1B)
├── Small (<$250M)

EXAMPLE PEER GROUP:
"2019 Vintage North American Mid-Market Buyout"
├── Vintage: 2019
├── Strategy: Buyout
├── Geography: North America
├── Size: $500M - $2.5B
└── Sample size: ~80 funds
```

### Sample Size Considerations

```
PEER GROUP SAMPLE SIZE
──────────────────────

SAMPLE SIZE GUIDELINES:
┌─────────────────────────────────────────────────────────┐
│ Sample Size │ Statistical Reliability │ Guidance       │
│─────────────┼─────────────────────────┼────────────────│
│ <10 funds   │ Very low               │ Avoid using    │
│ 10-30 funds │ Low                    │ Use cautiously │
│ 30-50 funds │ Moderate               │ Acceptable     │
│ 50-100 funds│ Good                   │ Reliable       │
│ >100 funds  │ High                   │ Most reliable  │
└─────────────────────────────────────────────────────────┘

TRADEOFF:
├── More specific peer group = Better match but smaller sample
├── Broader peer group = Larger sample but less relevant

EXAMPLE:
┌─────────────────────────────────────────────────────────┐
│ "2020 Vintage Healthcare Buyout" = 15 funds            │
│ → Too small, consider broadening                        │
│                                                         │
│ Options:                                                │
│ ├── Expand to all sectors: 120 funds                   │
│ ├── Expand vintage range (2019-2021): 40 funds         │
│ └── Use sector + broader vintage: 50 funds             │
└─────────────────────────────────────────────────────────┘
```

### Quartile Distribution

```
QUARTILE INTERPRETATION
───────────────────────

HOW QUARTILES ARE CALCULATED:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│ 100 funds ranked by IRR:                               │
│                                                         │
│ ████████████████████████ Top 25 = 1st Quartile         │
│ ████████████████████████ Next 25 = 2nd Quartile        │
│ ████████████████████████ Next 25 = 3rd Quartile        │
│ ████████████████████████ Bottom 25 = 4th Quartile      │
│                                                         │
│ PERCENTILES:                                            │
│ ├── 75th percentile = Top of 2nd quartile              │
│ ├── 50th percentile = Median (top of 3rd)              │
│ ├── 25th percentile = Top of 4th quartile              │
│                                                         │
└─────────────────────────────────────────────────────────┘

PERSISTENCE QUESTION:
"Do top quartile managers stay top quartile?"

RESEARCH FINDINGS:
├── Some persistence in VC
├── Less persistence in buyout
├── Past performance less predictive than thought
├── Market conditions often dominate
└── Don't over-rely on quartile ranking
```

---

## 18.5 Data Limitations

### Survivorship Bias

```
SURVIVORSHIP BIAS
─────────────────

PROBLEM:
Failed or poor-performing funds less likely to report data

┌─────────────────────────────────────────────────────────┐
│ UNIVERSE OF FUNDS (100 funds raised)                   │
│                                                         │
│ ████████████████████ Strong performers (60%)           │
│ ██████████ Average performers (25%)                    │
│ █████ Weak performers (15%)                            │
│                                                         │
│ REPORTED TO DATABASE:                                   │
│                                                         │
│ ████████████████████ Strong performers (55 of 60)     │
│ ████████ Average performers (20 of 25)                 │
│ ██ Weak performers (5 of 15)                           │
│                                                         │
│ RESULT: Database shows better average than reality     │
│         True median: 12%  Database median: 14%         │
└─────────────────────────────────────────────────────────┘

IMPACT:
├── Benchmarks appear better than actual market
├── Comparing to biased benchmark flatters underperformers
├── Overstates PE asset class returns
└── Affects vintage years with more failures
```

### Valuation Lag

```
VALUATION LAG ISSUES
────────────────────

TIMELINE PROBLEM:
┌─────────────────────────────────────────────────────────┐
│ Quarter End: March 31                                   │
│ GP Finalizes NAV: April 30                             │
│ LP Receives Report: May 15                             │
│ Data Provider Updates: June 1                          │
│ Benchmark Published: July                              │
│                                                         │
│ RESULT: Benchmarks are 3-6 months stale               │
└─────────────────────────────────────────────────────────┘

SMOOTHING EFFECT:
├── PE NAV changes gradually
├── Public markets move daily
├── PE appears less volatile
├── Correlation to public markets understated
└── Creates false diversification benefit

STALE PRICING IN DOWNTURNS:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Q1: Public markets fall 20%                           │
│  Q1: PE NAV reported flat (based on prior quarter)     │
│  Q2: PE NAV down 10% (catching up)                     │
│  Q3: PE NAV down another 5%                            │
│                                                         │
│  PE looks defensive initially, then catches up         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Selection Bias

```
SELECTION BIAS
──────────────

TYPES OF SELECTION BIAS:

1. VOLUNTARY REPORTING
   └── Better performers more likely to report
   └── GPs report to databases they look good in

2. LP SELECTION
   └── Databases rely on certain LP types
   └── Sophisticated LPs may have different portfolios

3. ACCESS BIAS
   └── Best funds don't need database exposure
   └── Overweight funds seeking investors

4. GEOGRAPHIC BIAS
   └── US/Europe overrepresented
   └── Emerging markets underreported

EXAMPLE:
┌─────────────────────────────────────────────────────────┐
│ Fund ABC (poor performer):                             │
│ ├── Doesn't report to Cambridge (voluntary)            │
│ ├── Doesn't report to Preqin (no benefit)             │
│ ├── Only in Burgiss (via LP system)                   │
│                                                         │
│ Fund XYZ (strong performer):                           │
│ ├── Reports to Cambridge (bragging rights)             │
│ ├── Reports to Preqin (fundraising)                   │
│ ├── In Burgiss (via LP systems)                       │
│ ├── In PitchBook (marketing)                          │
│                                                         │
│ XYZ appears in more databases, inflating averages     │
└─────────────────────────────────────────────────────────┘
```

### Data Quality Issues

```
DATA QUALITY CHALLENGES
───────────────────────

1. INCONSISTENT DEFINITIONS
   ├── Gross vs Net IRR
   ├── Commitment date vs first close
   ├── Fund size (final close vs. largest)
   └── Strategy classification

2. TIMING DIFFERENCES
   ├── Different quarter-end dates
   ├── Fiscal year variations
   └── Reporting delays

3. CALCULATION DIFFERENCES
   ├── IRR methodology
   ├── NAV treatment
   ├── FX conversion
   └── Fee treatment

4. DATA ENTRY ERRORS
   ├── Manual input mistakes
   ├── Unit errors (M vs B)
   └── Sign errors (distributions as negative)

BEST PRACTICE:
┌─────────────────────────────────────────────────────────┐
│ □ Understand data source methodology                   │
│ □ Check for obvious errors                             │
│ □ Compare across providers                             │
│ □ Use consistent definitions                           │
│ □ Document assumptions                                 │
│ □ Apply appropriate skepticism                         │
└─────────────────────────────────────────────────────────┘
```

---

## 18.6 Practical Benchmarking

### Best Practices

```
BENCHMARKING BEST PRACTICES
───────────────────────────

1. USE APPROPRIATE PEER GROUP
   ├── Match vintage year
   ├── Match strategy
   ├── Match geography
   ├── Match size
   └── Ensure sufficient sample size

2. USE MULTIPLE METRICS
   ├── IRR (time-weighted return)
   ├── TVPI (cash multiple)
   ├── DPI (realized multiple)
   ├── PME (public market comparison)
   └── Don't rely on single metric

3. CONSIDER MATURITY
   ├── Early funds: Less reliable
   ├── Use DPI/TVPI for maturity context
   ├── Compare to same-age funds
   └── Adjust expectations by fund age

4. USE MULTIPLE SOURCES
   ├── Cross-reference providers
   ├── Understand methodology differences
   └── Reconcile discrepancies

5. DOCUMENT METHODOLOGY
   ├── Which provider/benchmark
   ├── Which peer group definition
   ├── Which time period
   └── Any adjustments made
```

### Sample Benchmark Report

```
FUND BENCHMARK ANALYSIS
───────────────────────

Fund: Midwest Growth Partners V
Vintage: 2019
Strategy: US Mid-Market Buyout
Size: $850M

PERFORMANCE METRICS (as of Q2 2024):
┌─────────────────────────────────────────────────────────┐
│ Metric    │ Fund    │ Median │ Top Q  │ Rank           │
│───────────┼─────────┼────────┼────────┼────────────────│
│ Net IRR   │ 16.2%   │ 12.8%  │ 18.5%  │ 2nd Quartile  │
│ TVPI      │ 1.52x   │ 1.38x  │ 1.65x  │ 2nd Quartile  │
│ DPI       │ 0.45x   │ 0.35x  │ 0.55x  │ 2nd Quartile  │
│ RVPI      │ 1.07x   │ 1.03x  │ 1.15x  │ 2nd Quartile  │
└─────────────────────────────────────────────────────────┘

PEER GROUP DETAILS:
├── Definition: 2019 NA Mid-Market Buyout ($500M-$2B)
├── Sample size: 65 funds
├── Data source: Cambridge Associates
└── As of: June 30, 2024

PME ANALYSIS:
├── S&P 500 PME: 1.08 (8% outperformance)
├── Russell 2000 PME: 1.15 (15% outperformance)
└── PME methodology: Kaplan-Schoar

CONTEXT:
├── Fund is 5 years into 10-year term
├── 45% realized (DPI/TVPI)
├── Performance becoming more meaningful
└── Above median but not top quartile
```

---

## 18.7 Summary

### Key Takeaways

```
BENCHMARKING SUMMARY
────────────────────

1. NO SINGLE "RIGHT" BENCHMARK
   └── Multiple providers, methods, peer groups

2. PEER GROUP SELECTION MATTERS
   └── Same fund can rank differently by peer group

3. PME ANSWERS PUBLIC VS PRIVATE QUESTION
   └── Time-weight adjusted comparison

4. DATA HAS LIMITATIONS
   └── Survivorship bias, lag, selection bias

5. MULTIPLE METRICS TELL FULLER STORY
   └── IRR, TVPI, DPI, PME together

6. MATURITY AFFECTS RELIABILITY
   └── Early funds = less meaningful benchmarks

7. CONSISTENCY OVER PERFECTION
   └── Use same methodology over time
```

### Provider Quick Reference

| Need | Provider |
|------|----------|
| Institutional benchmark | Cambridge |
| Portfolio analytics | Burgiss |
| Market research | Preqin |
| VC / deal data | PitchBook |
| Budget option | Preqin |

---

## Knowledge Check

1. What is PME and what question does it answer?
2. Why might the same fund rank in different quartiles?
3. What is survivorship bias and how does it affect benchmarks?
4. What are the four main dimensions for peer group selection?
5. Why should you use multiple performance metrics?

<details>
<summary>Answers</summary>

1. Public Market Equivalent (PME) compares PE returns to what an investor would have earned investing the same cash flows in a public market index. It answers: "Did PE outperform public markets on a time-weighted basis?"

2. Quartile rankings depend entirely on peer group definition. A fund could be top quartile in "All PE" but second quartile in "Growth Equity" and third quartile in "Tech Growth" depending on how competitive each peer group is.

3. Survivorship bias occurs when poor-performing funds are less likely to report to databases (voluntary reporting). This inflates reported benchmark averages because the sample over-represents successful funds.

4. The four main dimensions are: (1) Vintage year, (2) Strategy (buyout, venture, growth, etc.), (3) Geography (NA, Europe, Asia, etc.), and (4) Fund size (mega, large, mid, small).

5. Different metrics tell different stories: IRR is time-weighted but sensitive to timing; TVPI shows total value creation; DPI shows realized returns; PME compares to public alternatives. Using multiple metrics provides a more complete picture and prevents over-reliance on any single measure.

</details>

---

## Exercise: Benchmark Analysis

```
SCENARIO: You need to benchmark Fund XYZ

Fund XYZ Details:
├── Strategy: European mid-market buyout
├── Vintage: 2020
├── Fund size: EUR 750M
├── Net IRR: 14.5%
├── TVPI: 1.35x
├── DPI: 0.25x

Available benchmarks (2020 vintage):
┌─────────────────────────────────────────────────────────┐
│ Peer Group                    │ Med IRR │ Med TVPI │ N  │
│───────────────────────────────┼─────────┼──────────┼────│
│ All PE (global)               │ 11.2%   │ 1.28x    │ 450│
│ All Buyout (global)           │ 12.5%   │ 1.32x    │ 280│
│ European Buyout (all sizes)   │ 10.8%   │ 1.25x    │ 85 │
│ European Mid-Market Buyout    │ 13.5%   │ 1.30x    │ 28 │
└─────────────────────────────────────────────────────────┘

Questions:
1. Which peer group is most appropriate?
2. What concern do you have about that peer group?
3. How would you present the fund's performance?
```

<details>
<summary>Answers</summary>

```
1. MOST APPROPRIATE PEER GROUP:
   "European Mid-Market Buyout" (2020 vintage)
   ├── Matches strategy
   ├── Matches geography
   ├── Matches size segment
   └── Matches vintage

2. CONCERN:
   Sample size of 28 funds is borderline small
   ├── Quartile boundaries less reliable
   ├── Outliers have more impact
   ├── Consider showing both European MM and broader
       European Buyout for context

3. PRESENTATION:
   ┌─────────────────────────────────────────────────────┐
   │ Fund XYZ Performance (2020 Vintage)                │
   │                                                     │
   │ Primary Benchmark: European Mid-Market Buyout       │
   │ ├── Fund IRR: 14.5% vs Median 13.5%               │
   │ ├── Fund TVPI: 1.35x vs Median 1.30x              │
   │ └── Ranking: Above median (2nd quartile)          │
   │                                                     │
   │ Note: Peer group sample size (N=28) is small;     │
   │ broader European Buyout (N=85) shows Fund at      │
   │ 14.5% vs 10.8% median (well above median)         │
   │                                                     │
   │ Maturity Note: DPI of 0.25x indicates early stage;│
   │ performance metrics will become more meaningful    │
   │ as realizations occur.                            │
   └─────────────────────────────────────────────────────┘
```

</details>

---

[← Module 17: Portfolio Construction](17-portfolio-construction.md) | [Module 19: ESG & Impact →](19-esg-impact.md)

[← Back to Curriculum Overview](00-curriculum-overview.md)
