# Module 13: Regulatory & Compliance Context

## Learning Objectives

By the end of this module, you will understand:
- Regulatory frameworks affecting different LP types
- GIPS standards and their application to private markets
- ESG reporting frameworks and requirements
- Key regulatory filings (Form PF, AIFMD, etc.)
- How compliance needs drive LP reporting requirements
- Data needs for LP stakeholder reporting

---

## 13.1 LP Regulatory Landscape

### Why LP Regulation Matters for Reporting

LPs aren't just passive investors - they have their own reporting obligations:

```
LP REPORTING CHAIN
──────────────────

    ┌─────────────┐
    │     GP      │
    │  (Reports   │
    │   to LPs)   │
    └──────┬──────┘
           │
           │ Quarterly/Annual Reports
           ▼
    ┌─────────────┐
    │     LP      │
    │  (Pension,  │
    │  Endowment) │
    └──────┬──────┘
           │
           │ LP must report to:
           ▼
    ┌─────────────────────────────────────────┐
    │                                         │
    │  ┌───────────┐  ┌───────────┐  ┌─────┐ │
    │  │  Board /  │  │Regulators │  │FOIA │ │
    │  │Beneficiar-│  │(DOL, SEC, │  │/Pub-│ │
    │  │   ies     │  │ State)    │  │lic  │ │
    │  └───────────┘  └───────────┘  └─────┘ │
    │                                         │
    └─────────────────────────────────────────┘
```

### Regulatory Framework by LP Type

```
LP TYPE REGULATORY OVERVIEW
───────────────────────────

┌─────────────────────────────────────────────────────────────┐
│ PUBLIC PENSION FUNDS                                         │
├─────────────────────────────────────────────────────────────┤
│ Regulators:     State laws, DOL (ERISA for some)            │
│ Oversight:      State legislature, pension board            │
│ Key Rules:      Prudent investor standard                   │
│ Transparency:   High (FOIA requests, public meetings)       │
│ Reporting:      Board reports, actuarial filings            │
│                                                             │
│ Data Needs:                                                 │
│ • Performance vs benchmark (for board)                      │
│ • Asset allocation compliance                               │
│ • Fee transparency (public scrutiny)                        │
│ • ESG metrics (increasing requirement)                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ CORPORATE PENSION FUNDS (ERISA)                              │
├─────────────────────────────────────────────────────────────┤
│ Regulators:     DOL, PBGC, IRS                              │
│ Oversight:      Plan fiduciaries, corporate board           │
│ Key Rules:      ERISA fiduciary duties, prohibited trans.   │
│ Transparency:   Moderate (Form 5500, participant rights)    │
│ Reporting:      Form 5500, Schedule C, actuarial cert       │
│                                                             │
│ Data Needs:                                                 │
│ • ERISA compliance documentation                            │
│ • Fee disclosure (408(b)(2))                               │
│ • Plan asset rules compliance                               │
│ • Fiduciary process documentation                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ INSURANCE COMPANIES                                          │
├─────────────────────────────────────────────────────────────┤
│ Regulators:     State insurance commissioners, NAIC         │
│ Oversight:      State regulators, rating agencies           │
│ Key Rules:      Statutory accounting (SAP), RBC             │
│ Transparency:   Moderate (statutory filings public)         │
│ Reporting:      Statutory annual statement, Schedule BA     │
│                                                             │
│ Data Needs:                                                 │
│ • Statutory vs GAAP valuations                              │
│ • Risk-Based Capital (RBC) calculations                     │
│ • Investment schedule detail                                │
│ • Admitted vs non-admitted asset classification             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ ENDOWMENTS & FOUNDATIONS                                     │
├─────────────────────────────────────────────────────────────┤
│ Regulators:     IRS, State AG (charity oversight)           │
│ Oversight:      Board of trustees, donors                   │
│ Key Rules:      UPMIFA, 4942 distribution requirements      │
│ Transparency:   Moderate (Form 990-PF public)               │
│ Reporting:      Form 990/990-PF, board reports              │
│                                                             │
│ Data Needs:                                                 │
│ • Spending policy calculations                              │
│ • Investment pool performance                               │
│ • Mission-related investing metrics                         │
│ • UBIT exposure                                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ SOVEREIGN WEALTH FUNDS                                       │
├─────────────────────────────────────────────────────────────┤
│ Regulators:     Home country government/ministry            │
│ Oversight:      Government, sometimes parliament            │
│ Key Rules:      Santiago Principles (voluntary)             │
│ Transparency:   Varies widely by country                    │
│ Reporting:      Government reports, some publish annually   │
│                                                             │
│ Data Needs:                                                 │
│ • Country-of-origin reporting                               │
│ • Currency exposure                                         │
│ • Sector/geographic allocation                              │
│ • Transparency reporting (Santiago compliance)              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ EUROPEAN INSTITUTIONAL INVESTORS                             │
├─────────────────────────────────────────────────────────────┤
│ Regulators:     National regulators, ESMA, ECB              │
│ Oversight:      Varies by type                              │
│ Key Rules:      AIFMD, Solvency II, IORP II                │
│ Transparency:   High (regulatory reporting)                 │
│ Reporting:      AIFMD Annex IV, Solvency II templates       │
│                                                             │
│ Data Needs:                                                 │
│ • Look-through reporting                                    │
│ • SFDR sustainability disclosures                           │
│ • Solvency capital requirements                             │
│ • Remuneration disclosures                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 13.2 GIPS Standards

### What is GIPS?

**GIPS (Global Investment Performance Standards)** are voluntary, ethical standards for calculating and presenting investment performance. Created by CFA Institute.

```
GIPS OVERVIEW
─────────────

PURPOSE:
• Ensure fair, comparable performance presentation
• Establish global best practices
• Protect investors from misleading claims
• Build trust in performance reporting

WHO CLAIMS COMPLIANCE:
• Asset managers (including PE GPs)
• Required by many institutional LPs
• Voluntary but increasingly expected

KEY PRINCIPLE:
"Fair representation and full disclosure"
```

### GIPS for Private Equity

```
GIPS PRIVATE EQUITY PROVISIONS
──────────────────────────────

COMPOSITES:
• Group similar funds into composites
• Vintage year composites common
• Strategy-based composites

REQUIRED DISCLOSURES:
├── Composite description
├── Benchmark description
├── Vintage year
├── Total committed capital
├── Cumulative paid-in capital
├── Cumulative distributions
├── Total value (NAV + distributions)
├── SI-IRR (Since Inception IRR)
├── Investment multiple (TVPI)
├── PIC multiple (Paid-In Capital Multiple)
├── Realization multiple (DPI)
└── Unrealized multiple (RVPI)

VALUATION REQUIREMENTS:
• Fair value per GIPS Valuation Principles
• At least quarterly valuation
• External valuation annually (recommended)
• Consistent methodology

TIME-WEIGHTED VS MONEY-WEIGHTED:
• PE uses money-weighted (IRR) not time-weighted
• Because GP controls timing of cash flows
• SI-IRR is the standard
```

### GIPS Calculation Standards

```
GIPS IRR CALCULATION
────────────────────

SI-IRR (Since Inception IRR):
• Annualized IRR from fund inception
• Uses daily cash flows (or monthly minimum)
• Includes all cash flows and ending value

FORMULA:
Solve for IRR where:
Σ CF_i × (1 + IRR)^((End Date - CF Date)/365) + NAV = 0

EXAMPLE:
Date         Cash Flow    Days to End
01/01/2020   -$100M      1826 (5 years)
07/01/2020   -$50M       1644
01/01/2022   +$30M       1096
12/31/2024   +$180M + NAV $80M = $260M  0

SI-IRR ≈ 18.2%

GIPS SPECIFIC REQUIREMENTS:
• Net-of-fees IRR required
• Gross IRR recommended
• Annualized for periods > 1 year
• Clearly labeled with fee treatment
```

### GIPS Compliance Checklist

```
GIPS COMPLIANCE REQUIREMENTS (PE)
─────────────────────────────────

FUNDAMENTALS:
☐ Firm-wide compliance (all portfolios)
☐ Consistent valuation policies
☐ Maintain records to support calculations
☐ No cherry-picking results

COMPOSITE CONSTRUCTION:
☐ Include all fee-paying portfolios
☐ Consistent vintage year grouping
☐ Document composite definitions
☐ No retroactive changes

PRESENTATION:
☐ 5+ years of history (or since inception)
☐ Annual returns for each year
☐ Required statistics (IRR, multiples)
☐ Benchmark comparison
☐ Disclosure of fees and expenses

VERIFICATION (Recommended):
☐ Independent verification
☐ Performance examination
☐ Updated annually
```

---

## 13.3 ESG Reporting Frameworks

### ESG Landscape for Private Markets

```
ESG REPORTING EVOLUTION
───────────────────────

     2010         2015         2020         2025
       │            │            │            │
       │  PRI       │ SDGs       │ SFDR       │ Mandatory
       │  Launch    │ Adopted    │ Effective  │ Climate
       │            │            │            │ Disclosure
       │            │            │            │
       ▼            ▼            ▼            ▼
    Voluntary → Standards → Regulation → Required
    Principles   Emerge      Begins       Reporting

TODAY'S STATE:
• Mix of voluntary and mandatory
• Fragmented standards
• Rapid regulatory evolution
• LP pressure increasing
```

### Key ESG Frameworks

```
ESG FRAMEWORKS COMPARISON
─────────────────────────

┌─────────────────────────────────────────────────────────────┐
│ UN PRI (Principles for Responsible Investment)              │
├─────────────────────────────────────────────────────────────┤
│ Type:           Voluntary principles + reporting            │
│ Signatories:    5,000+ (most large GPs and LPs)            │
│ Focus:          Incorporation of ESG in investment process  │
│                                                             │
│ LP Requirements:                                            │
│ • Annual PRI Transparency Report                            │
│ • Report on ESG integration                                 │
│ • Stewardship activities                                    │
│                                                             │
│ Data Needed from GPs:                                       │
│ • ESG policy description                                    │
│ • ESG due diligence process                                 │
│ • Portfolio company ESG metrics                             │
│ • Engagement/stewardship examples                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ SFDR (EU Sustainable Finance Disclosure Regulation)         │
├─────────────────────────────────────────────────────────────┤
│ Type:           Mandatory regulation (EU)                   │
│ Effective:      March 2021 (Level 1), 2023 (Level 2)       │
│ Scope:          EU managers + funds marketed to EU          │
│                                                             │
│ Fund Classifications:                                       │
│ • Article 6: No sustainability claims                       │
│ • Article 8: "Light green" - promotes ESG                   │
│ • Article 9: "Dark green" - sustainable objective           │
│                                                             │
│ Data Needed from GPs:                                       │
│ • Sustainability risk integration                           │
│ • Principal Adverse Impact (PAI) indicators                 │
│ • Pre-contractual disclosures                               │
│ • Periodic reporting (annual)                               │
│                                                             │
│ PAI Indicators (18 mandatory for companies):                │
│ • GHG emissions (Scope 1, 2, 3)                            │
│ • Carbon footprint                                          │
│ • Biodiversity impact                                       │
│ • Water usage                                               │
│ • Waste generation                                          │
│ • Social/employee matters                                   │
│ • Human rights                                              │
│ • Anti-corruption                                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ TCFD (Task Force on Climate-Related Financial Disclosures)  │
├─────────────────────────────────────────────────────────────┤
│ Type:           Voluntary framework (becoming mandatory)    │
│ Focus:          Climate risk and opportunity disclosure     │
│ Status:         Required in UK, EU; expected globally       │
│                                                             │
│ Four Pillars:                                               │
│ 1. Governance - Board/management climate oversight          │
│ 2. Strategy - Climate risks and opportunities               │
│ 3. Risk Management - Climate risk identification            │
│ 4. Metrics & Targets - GHG emissions, climate targets       │
│                                                             │
│ Data Needed from GPs:                                       │
│ • Portfolio company emissions data                          │
│ • Climate scenario analysis                                 │
│ • Physical and transition risk assessment                   │
│ • Net zero targets and progress                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ EDCI (ESG Data Convergence Initiative)                      │
├─────────────────────────────────────────────────────────────┤
│ Type:           Industry-led standardization                │
│ Participants:   300+ GPs and LPs                            │
│ Focus:          Standardized ESG metrics for PE             │
│                                                             │
│ Core Metrics (Portfolio Company Level):                     │
│ • Scope 1 & 2 GHG emissions                                │
│ • Renewable energy percentage                               │
│ • Board diversity                                           │
│ • Work-related injuries                                     │
│ • Net new hires                                             │
│ • Employee engagement                                       │
│                                                             │
│ Why It Matters:                                             │
│ • Enables LP aggregation across funds                       │
│ • Reduces GP reporting burden (one standard)                │
│ • Facilitates benchmarking                                  │
└─────────────────────────────────────────────────────────────┘
```

### ESG Data Collection Challenges

```
ESG DATA CHALLENGES IN PE
─────────────────────────

PORTFOLIO COMPANY LEVEL:
├── Private companies have no disclosure requirements
├── Data collection systems often lacking
├── Inconsistent measurement methodologies
├── Historical data may not exist
└── Resource constraints at smaller companies

FUND LEVEL:
├── Aggregation across diverse companies
├── Sector-appropriate metrics vary
├── Comparability across strategies
└── Attribution of improvements to GP actions

LP AGGREGATION:
├── Different GPs report different metrics
├── Timing mismatches
├── Currency and geography issues
├── Avoiding double-counting in FoF
└── Materiality thresholds vary

SOLUTIONS EMERGING:
├── EDCI standardization
├── Third-party ESG data providers
├── GP ESG due diligence improvement
└── Technology platforms for collection
```

---

## 13.4 Regulatory Filings

### Form PF (US)

```
FORM PF OVERVIEW
────────────────

WHAT:     Private Fund Adviser reporting to SEC/CFTC
WHO:      SEC-registered advisers to private funds
WHEN:     Quarterly (large advisers), Annually (others)
THRESHOLD: $150M+ in private fund AUM

FORM PF CONTENT:

SECTION 1: Basic Information (All Filers)
├── Fund identification
├── AUM and NAV
├── Investor composition
├── Leverage/borrowing
├── Trading/clearing information
└── Investment strategy

SECTION 2: Hedge Funds (Large Hedge Fund Advisers)
├── Detailed risk metrics
├── Counterparty exposure
├── Financing/liquidity
└── Investment positions

SECTION 4: Private Equity (Large PE Advisers)
├── Fund-by-fund reporting
├── Performance metrics
├── Controlled portfolio companies
├── Leverage at portfolio company level
├── Geographic concentration
└── Industry concentration

LARGE PE ADVISER: $2B+ in PE AUM

DATA ELEMENTS:
• NAV
• Gross and net IRR
• Gross and net MOIC
• Quarterly contributions and distributions
• Leverage ratios
• Sector and geographic breakdowns
```

### AIFMD (Europe)

```
AIFMD ANNEX IV REPORTING
────────────────────────

WHAT:     Alternative Investment Fund Managers Directive
WHO:      EU AIFMs or non-EU managers marketing to EU
WHEN:     Semi-annual or annual depending on size
          Quarterly for €1B+ funds

ANNEX IV CONTENT:

FUND IDENTIFICATION
├── LEI and fund identifiers
├── AIF type (PE, real estate, hedge, etc.)
├── Master/feeder structure
└── Domicile and marketing countries

INVESTMENT STRATEGY
├── Strategy description
├── Geographic focus
├── Position concentration
└── Investor concentration

INSTRUMENTS & EXPOSURES
├── Asset type breakdown
├── Long/short exposures
├── Currency exposure
├── Commodity exposure
└── Turnover

RISK PROFILE
├── Market risk
├── Counterparty risk
├── Liquidity risk
├── Operational risk
└── Risk measures (VaR where applicable)

LEVERAGE
├── Gross method
├── Commitment method
├── Leverage limits and usage
└── Rehypothecation

LIQUIDITY
├── Investor liquidity profile
├── Portfolio liquidity profile
├── Redemption arrangements
└── Special arrangements
```

### Solvency II (Insurance)

```
SOLVENCY II REQUIREMENTS
────────────────────────

WHO:      European insurers (and groups)
WHAT:     Prudential regulation including reporting

RELEVANT TO PE INVESTMENTS:

PILLAR 1: QUANTITATIVE REQUIREMENTS
├── Solvency Capital Requirement (SCR)
│   └── PE classified as "Type 2 equity" (49% stress)
├── Look-through approach required
│   └── Must identify underlying assets of funds
└── Investment limits

PILLAR 3: REPORTING
├── QRT (Quantitative Reporting Templates)
│   ├── S.06.02 - List of assets
│   ├── S.06.03 - Collective investment undertakings (look-through)
│   └── SCR templates
└── SFCR (Solvency and Financial Condition Report)

DATA NEEDED FROM GPs:
• Underlying asset look-through
• Asset type classification
• Geographic breakdown
• Currency exposure
• Leverage information
• Detailed holdings for SCR calculation

LOOK-THROUGH IMPLICATIONS:
Insurers must "look through" PE funds to
underlying portfolio companies for:
• SCR calculation
• Asset diversification
• Reporting templates

This drives significant data requests to GPs.
```

### Other Regulatory Requirements

```
ADDITIONAL REGULATORY REQUIREMENTS
──────────────────────────────────

US PUBLIC PENSION TRANSPARENCY
├── State-specific disclosure laws
├── Freedom of Information Act (FOIA)
├── Public posting of commitments
├── Fee disclosure requirements
└── Growing trend toward more transparency

UK/FCA REQUIREMENTS
├── FCA registration for UK managers
├── PRIIPs (retail investor disclosures)
├── Consumer Duty (if applicable)
└── Senior Managers & Certification Regime

OECD COMMON REPORTING STANDARD (CRS)
├── Automatic exchange of financial info
├── Identifying investors by tax residence
├── Annual reporting to tax authorities
└── Affects fund admin and reporting

FATCA (US)
├── Foreign Account Tax Compliance Act
├── Identifies US persons globally
├── Withholding on non-compliant entities
└── Annual reporting to IRS

MiFID II (If Applicable)
├── Costs and charges disclosure
├── Best execution
├── Product governance
└── Generally less relevant for PE
```

---

## 13.5 LP Stakeholder Reporting

### Board Reporting Requirements

```
PENSION BOARD REPORTING
───────────────────────

TYPICAL BOARD REPORT CONTENT:

EXECUTIVE SUMMARY
├── Total alternatives allocation
├── Performance vs policy benchmark
├── Notable developments
└── Recommended actions

PERFORMANCE SECTION
├── By strategy (PE, VC, RE, etc.)
├── By vintage year
├── Comparison to public markets
├── Comparison to peers/benchmarks
└── Attribution analysis

RISK SECTION
├── Concentration analysis
├── Liquidity analysis
├── Pacing model status
├── Unfunded commitment coverage
└── Currency exposure

ACTIVITY SECTION
├── New commitments
├── Exits and realizations
├── Capital calls and distributions
├── Fund developments
└── Manager updates

COMPLIANCE SECTION
├── Investment policy compliance
├── Allocation vs targets
├── Eligible investment confirmation
└── Proxy voting summary

FREQUENCY:
• Summary: Monthly or quarterly
• Detailed: Quarterly
• Annual review: Deep dive
```

### Insurance Company Reporting

```
INSURANCE STATUTORY REPORTING
─────────────────────────────

STATUTORY ANNUAL STATEMENT
├── Schedule BA: Other Long-Term Invested Assets
│   ├── PE fund holdings detail
│   ├── Cost vs admitted value
│   ├── Investment category codes
│   └── NAIC designation
│
├── Schedule D: Bonds and Stocks
│   └── Any public securities from PE
│
└── Investment Schedule Detail
    ├── Acquisition date and cost
    ├── Current admitted value
    └── Impairment status

STATUTORY VS GAAP DIFFERENCES:
┌────────────────────────────────────────────────────┐
│ Item              │ GAAP          │ Statutory     │
├───────────────────┼───────────────┼───────────────┤
│ Valuation basis   │ Fair value    │ Varies        │
│ PE fund holding   │ Fair value    │ GAAP equity   │
│ Goodwill          │ Capitalize    │ Non-admitted  │
│ Deferred tax      │ Recorded      │ Often limited │
│ AVR/IMR           │ N/A           │ Required      │
└────────────────────────────────────────────────────┘

RISK-BASED CAPITAL (RBC):
PE funds typically classified as:
• Common stock (Class 5): 30% factor
• Schedule BA (Other): 20% factor
Different treatment drives structure preferences
```

### Endowment/Foundation Reporting

```
ENDOWMENT REPORTING REQUIREMENTS
────────────────────────────────

FORM 990-PF (Private Foundations)
├── Part IV: Capital Gains and Losses
├── Part VII-B: Investment Returns
├── Part X: Minimum Investment Return
├── Part XI: Distributable Amount
└── Schedule B: Contributors

NACUBO SURVEY (Endowments)
├── Voluntary participation
├── Asset allocation disclosure
├── Returns by asset class
├── Spending rate
└── Published annually (benchmarking)

SPENDING POLICY CALCULATION:
Most use rolling average of NAV
PE creates challenges:
• NAV is estimated (not market)
• Volatility affects calculation
• Liquidity mismatch with spending needs

UBIT CONSIDERATIONS:
├── Debt-financed income from PE
├── Operating company income
├── Blockers to manage UBIT
└── Require detailed K-1 analysis
```

---

## 13.6 Data Requirements Summary

### Mapping Regulations to Data Needs

```
REGULATORY DATA REQUIREMENTS MATRIX
───────────────────────────────────

Data Element              │ GIPS │ SFDR │Form PF│AIFMD │Solv II│
──────────────────────────┼──────┼──────┼───────┼──────┼───────┤
SI-IRR (Net)              │  R   │      │   R   │      │       │
SI-IRR (Gross)            │  R   │      │   R   │      │       │
TVPI                      │  R   │      │   R   │      │       │
DPI                       │  R   │      │   R   │      │       │
RVPI                      │  R   │      │       │      │       │
NAV                       │  R   │  R   │   R   │  R   │   R   │
Contributions             │  R   │      │   R   │      │       │
Distributions             │  R   │      │   R   │      │       │
Committed Capital         │  R   │      │   R   │  R   │       │
Unfunded Commitment       │      │      │   R   │  R   │   R   │
GHG Emissions             │      │  R   │       │      │       │
ESG Metrics (PAI)         │      │  R   │       │      │       │
Look-through Holdings     │      │      │       │  R   │   R   │
Leverage (Fund)           │      │      │   R   │  R   │   R   │
Leverage (Portfolio Co)   │      │      │   R   │      │   R   │
Geographic Breakdown      │      │      │   R   │  R   │   R   │
Sector Breakdown          │      │      │   R   │  R   │   R   │
Currency Exposure         │      │      │       │  R   │   R   │
Investor Breakdown        │      │      │   R   │  R   │       │
Liquidity Profile         │      │      │       │  R   │       │
───────────────────────────────────────────────────────────────
R = Required
```

### Feature Implications

```
PLATFORM FEATURE IMPLICATIONS
─────────────────────────────

DATA COLLECTION:
├── Standardized metrics (IRR, multiples, NAV)
├── Cash flow detail with dates
├── Look-through capability for holdings
├── ESG metrics at portfolio company level
├── Geographic and sector classifications
└── Fee breakdown detail

CALCULATION ENGINE:
├── GIPS-compliant IRR calculation
├── Multiple computation methodologies
├── Currency conversion
├── Benchmark comparison
└── PME calculation

REPORTING OUTPUT:
├── GIPS-compliant presentations
├── Regulatory report templates
├── Board report formats
├── Customizable for LP requirements
└── Audit-ready documentation

AGGREGATION:
├── Cross-fund performance
├── Cross-GP performance
├── Vintage year composites
├── Strategy-level composites
└── ESG metric aggregation

TIMELINESS:
├── Quarterly minimum for most
├── Monthly estimates for some
├── Look-back capability
└── Point-in-time reporting
```

---

## 13.7 Compliance Best Practices

### GP Reporting Best Practices

```
GP COMPLIANCE BEST PRACTICES
────────────────────────────

PERFORMANCE REPORTING:
☐ Follow GIPS standards
☐ Clear gross vs net labeling
☐ Consistent methodology documentation
☐ Regular independent verification
☐ Benchmark selection rationale

VALUATION:
☐ Documented valuation policy
☐ Quarterly valuations minimum
☐ Annual external valuation support
☐ LPAC oversight documented
☐ Methodology consistency

ESG:
☐ Adopt recognized framework
☐ Collect standardized metrics (EDCI)
☐ Regular portfolio company reporting
☐ Progress toward targets
☐ Third-party assurance (emerging)

REGULATORY:
☐ Timely Form PF/Annex IV filing
☐ Accurate investor categorization
☐ Look-through data available
☐ AIFMD Annex IV ready
☐ CRS/FATCA compliance
```

### LP Due Diligence on Reporting

```
LP DUE DILIGENCE: REPORTING QUALITY
───────────────────────────────────

QUESTIONS TO ASK GPs:

PERFORMANCE:
• Are you GIPS compliant/verified?
• How do you calculate IRR (daily/monthly)?
• What's included/excluded in net returns?
• How often do you update valuations?

VALUATION:
• What's your valuation policy?
• Do you use external valuation advisors?
• What's your LPAC's role in valuations?
• How do exits compare to last marks?

ESG:
• What framework do you follow?
• How do you collect portfolio company data?
• Can you provide SFDR PAI indicators?
• What are your climate/DEI targets?

REGULATORY:
• Can you provide look-through data?
• What's your timeline for quarterly reports?
• Can you accommodate custom reporting?
• How do you handle regulatory changes?
```

---

## 13.8 Summary

### Key Regulatory Considerations

```
REGULATORY SUMMARY
──────────────────

1. LPs HAVE THEIR OWN REPORTING OBLIGATIONS
   • Pension boards, insurance regulators, tax authorities
   • GP data quality directly impacts LP compliance

2. GIPS IS THE PERFORMANCE STANDARD
   • Required by many institutional LPs
   • Specific provisions for private equity
   • Verification adds credibility

3. ESG IS RAPIDLY EVOLVING
   • SFDR mandatory for EU exposure
   • TCFD becoming required
   • EDCI standardizing PE metrics
   • Data collection is the main challenge

4. REGULATORY REPORTING VARIES BY LP TYPE
   • Form PF, AIFMD, Solvency II, etc.
   • Look-through requirements common
   • Drives data granularity needs

5. ANTICIPATE FUTURE REQUIREMENTS
   • Climate disclosure expanding
   • Transparency increasing
   • Standards converging
   • Build flexibility into systems
```

---

## Knowledge Check

1. What does GIPS stand for and why do LPs care if a GP is GIPS compliant?
2. What are the three SFDR fund classifications?
3. Why do Solvency II insurers need "look-through" data from PE funds?
4. What is Form PF and who files it?
5. What is the EDCI and why is it important?

<details>
<summary>Answers</summary>

1. Global Investment Performance Standards. LPs care because GIPS ensures fair, consistent performance calculation and presentation, enabling reliable comparisons across managers.

2. Article 6 (no sustainability claims), Article 8 ("light green" - promotes ESG characteristics), Article 9 ("dark green" - has sustainable investment as objective).

3. Solvency II requires insurers to calculate capital requirements based on underlying assets. They must "look through" PE funds to the portfolio companies to properly classify assets and calculate risk charges.

4. Form PF is SEC/CFTC reporting for US-registered private fund advisers. Large PE advisers ($2B+ AUM) file quarterly with detailed fund-level performance and portfolio data.

5. ESG Data Convergence Initiative - industry effort to standardize ESG metrics for PE. Important because it enables LPs to aggregate ESG data across their portfolio and reduces GP reporting burden.

</details>

---

## Additional Resources

### Regulatory Links

- [GIPS Standards (CFA Institute)](https://www.gipsstandards.org)
- [SFDR (European Commission)](https://ec.europa.eu/sustainable-finance)
- [Form PF Instructions (SEC)](https://www.sec.gov/forms)
- [AIFMD (ESMA)](https://www.esma.europa.eu)
- [TCFD (FSB)](https://www.fsb-tcfd.org)
- [EDCI](https://www.esgdc.org)
- [UN PRI](https://www.unpri.org)

---

[← Back to Curriculum Overview](00-curriculum-overview.md)
