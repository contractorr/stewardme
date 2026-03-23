# Behavioral Economics

## Overview

Behavioral economics combines insights from psychology and economics to understand how people actually make decisions, as opposed to how traditional economic models assume they decide. While classical economics assumes people are rational, self-interested, and have stable preferences, behavioral economics documents systematic deviations from these assumptions.

The field exploded in importance after Daniel Kahneman won the Nobel Prize (2002) and Richard Thaler won (2017), with applications in policy (nudges), marketing, finance, healthcare, and more. It challenges the "homo economicus" model while preserving economics' analytical tools.

## Bounded Rationality

### Concept

**Herbert Simon (1955)**: People are "boundedly rational" - they seek satisfactory solutions rather than optimal ones due to:
- **Cognitive limitations**: Limited working memory, processing power, attention
- **Information constraints**: Incomplete, costly, or inaccessible information
- **Time constraints**: Decisions must be made quickly

**Satisficing**: Choosing the first option that meets minimum criteria rather than exhaustively searching for the best option.

**Real-World Example**: Choosing a college
- **Rational model**: Evaluate all colleges, calculate expected lifetime earnings, optimal fit, etc.
- **Reality**: Visit a few nearby colleges, pick one that feels good and is affordable
- Satisficing is adaptive - comprehensive search would be impossibly costly

### Heuristics

**Definition**: Mental shortcuts or rules of thumb that simplify decision-making.

**Benefits**: Fast, require little information, often accurate
**Costs**: Systematic biases and errors in certain situations

| Heuristic | Description | When It Works | When It Fails |
|-----------|-------------|---------------|---------------|
| **Availability** | Judge probability by ease of recall | Recent/memorable events indicative | Rare but vivid events overestimated |
| **Representativeness** | Judge probability by similarity to stereotype | Stereotypes accurate on average | Ignores base rates |
| **Anchoring** | Rely heavily on first piece of information | Anchor is relevant | Arbitrary anchors influence decisions |
| **Affect** | Decisions driven by emotional reactions | Intuition captures important info | Emotions mislead (fear, greed) |

### Availability Heuristic

**Mechanism**: Events that are easier to recall seem more probable.

**Examples**:
- After airplane crash, people overestimate flight risk (though driving is more dangerous)
- Shark attacks receive massive media coverage → people fear sharks more than coconuts (which kill more people)
- Vivid crime stories → perception that crime is rising even when statistics show it's falling

**Real-World Application - Insurance**: People over-insure against dramatic but unlikely events (terrorism, plane crashes) and under-insure against boring but common risks (fire, flood).

### Representativeness Heuristic

**Mechanism**: Judge probability based on how similar something is to a typical case, ignoring base rates.

**Classic Example - Linda Problem** (Kahneman & Tversky):
> Linda is 31, single, outspoken, and very bright. She majored in philosophy and was concerned with discrimination and social justice.
>
> Which is more probable?
> A) Linda is a bank teller
> B) Linda is a bank teller and active in the feminist movement

Most people choose B, violating probability logic (B is a subset of A, so cannot be more probable).

**Real-World Example - Startup Evaluation**: Entrepreneurs who fit the "tech founder" stereotype (young, Stanford dropout) get funded more easily, even controlling for business fundamentals.

### Anchoring

**Mechanism**: Initial number (even if arbitrary) disproportionately influences subsequent estimates.

**Experiments**:
- Spin a wheel (randomly lands on 10 or 65), then estimate percentage of African countries in UN
- Result: Those seeing 10 estimate ~25%, those seeing 65 estimate ~45%
- Wheel is obviously irrelevant but still anchors estimates

**Real-World Applications**:
- **Negotiations**: First offer anchors discussion (why sellers list high, buyers offer low)
- **Real estate**: List price anchors buyer perceptions of value
- **Retail**: Original price (before sale) anchors perceived deal quality
- **Salary negotiations**: First number mentioned anchors negotiation range

**Policy Application**: Default retirement contribution rates anchor what people save. Changing default from 3% to 6% dramatically increases average savings.

## Prospect Theory

### Core Insights

**Daniel Kahneman & Amos Tversky (1979)**: Alternative to expected utility theory, better describes actual behavior.

**Key Features**:

1. **Reference Dependence**: Evaluate outcomes relative to a reference point (usually status quo), not absolute wealth
2. **Loss Aversion**: Losses hurt more than equivalent gains feel good (losses weigh ~2x gains)
3. **Diminishing Sensitivity**: First dollar matters more than 1,000th dollar (concave for gains, convex for losses)
4. **Probability Weighting**: Overweight small probabilities, underweight moderate/high probabilities

### Value Function

Traditional utility function: U = f(wealth)

Prospect theory value function: V = f(change from reference point)

```
        Value
          ↑
          |
          |     Gains (concave)
          |    /
          |   /
  --------+---------- Change
         /|
        / |
   Losses |
  (convex)|
  steeper |
```

**Shape**:
- Steeper for losses than gains (loss aversion)
- Concave for gains (diminishing returns)
- Convex for losses (risk-seeking in losses)

### Loss Aversion

**Definition**: Pain of losing $100 exceeds pleasure of gaining $100.

**Experiments**: Most people reject 50/50 bet to win $110 or lose $100, even though expected value is +$5. Need ~$200 gain to accept $100 loss risk (2:1 ratio).

**Real-World Examples**:

**Endowment Effect**: Owners value items more than buyers
- Experiment: Give people coffee mugs, then offer to buy them back
- Result: Sellers want ~$7, buyers offer ~$3 (same mugs)
- Explanation: Selling feels like a loss; buying feels like foregone gain

**Status Quo Bias**: Preference for current state
- People stick with default options (retirement plans, organ donation, insurance)
- Inertia is powerful even when change would be beneficial

**Sunk Cost Fallacy**: Continue investing in failing projects because of past investment
- "I've already spent $1,000 on this car repair, might as well spend $500 more" (even if buying a new car is cheaper going forward)
- Rational approach: Ignore sunk costs, evaluate only future costs/benefits

**Housing Market**: Homeowners refuse to sell at loss even when waiting costs more
- 2008 crisis: Many held underwater homes rather than sell at loss
- Sellers list prices above purchase price even when market has fallen

**Sports**: Teams keep underperforming players because of high draft position or salary
- Escalation of commitment to justify past decisions

### Risk Attitudes

**Traditional Economics**: People are consistently risk-averse (prefer certainty to gambles with same expected value).

**Prospect Theory**: Risk attitude depends on domain:
- **Risk-averse for gains**: Prefer sure $50 over 50% chance of $100
- **Risk-seeking for losses**: Prefer 50% chance to lose $100 over sure loss of $50

**Real-World Example - Insurance and Lotteries**:
- Same people buy insurance (risk-averse for large losses) and lottery tickets (risk-seeking for small gains)
- Traditional theory struggles to explain; prospect theory explains through probability weighting and value function shape

**Investing**: Investors hold losing stocks too long (risk-seeking in loss domain, hoping to break even) and sell winners too quickly (risk-averse in gain domain, locking in gains). Opposite of "cut losses, let winners run."

### Framing Effects

**Definition**: Presentation of identical information in different ways changes decisions.

**Classic Example - Asian Disease Problem**:
> Imagine US is preparing for outbreak of disease expected to kill 600 people. Two programs are proposed:
>
> Frame 1 (Gains):
> - Program A: 200 people will be saved (72% choose)
> - Program B: 1/3 probability 600 saved, 2/3 probability nobody saved (28% choose)
>
> Frame 2 (Losses):
> - Program C: 400 people will die (22% choose)
> - Program D: 1/3 probability nobody dies, 2/3 probability 600 die (78% choose)

Outcomes are identical (A=C, B=D), but framing shifts preferences. Gain frame → risk aversion (choose sure thing); loss frame → risk seeking (take gamble).

**Real-World Applications**:

**Marketing**:
- "90% fat-free" vs "10% fat" (same, but first sounds better)
- "Save $5" vs "Avoid losing $5" (loss frame more motivating)

**Policy**:
- Opt-out organ donation (default = donor) vs opt-in (default = non-donor)
- Countries with opt-out have 90%+ donation rates vs 10-20% with opt-in

**Healthcare**:
- "Surgery has 90% survival rate" vs "10% mortality rate"
- Patients more likely to choose surgery with positive frame

## Time Inconsistency and Hyperbolic Discounting

### The Problem

**Traditional Economics**: People discount future exponentially with constant discount rate.
- Prefer $100 today over $105 in a week
- Implies also prefer $100 in 52 weeks over $105 in 53 weeks (same one-week delay)

**Reality**: People show **present bias** - disproportionately weight present over future.
- Prefer $100 today over $105 in a week
- BUT prefer $105 in 53 weeks over $100 in 52 weeks
- Inconsistent discounting

**Hyperbolic Discounting**: Discount rate declines with time horizon. Near future discounted heavily; distant future discounted less.

### Real-World Examples

**Exercise and Dieting**:
- Always plan to start "tomorrow" (future self will be disciplined)
- Tomorrow arrives, future becomes present, postpone again
- Present self enjoys cake, future self deals with consequences

**Saving for Retirement**:
- Undersave because retirement is distant (future self problem)
- As retirement approaches, regret not saving more (present self problem)
- Pre-commitment devices help: automatic enrollment, increasing default contributions

**Procrastination**:
- Delay unpleasant tasks (taxes, medical checkups) despite knowing future costs
- Last-minute rush, missed deadlines, penalties

**Credit Cards**:
- Enjoy consumption now, discount future payment
- High interest rates reflect this present bias
- Many people carry balances and pay substantial interest

### Solutions

**Commitment Devices**: Voluntarily restrict future choices
- **Examples**: Gym membership (sunk cost motivates attendance), retirement accounts with penalties, apps that block social media during work hours
- **Real-World**: StickK.com - commit to goal, lose money if fail

**Automatic Enrollment**: Exploit inertia
- Save More Tomorrow plan (Thaler & Benartzi): Commit to save portion of future raises
- Participation rates increased from 30% to 80%+

**Deadlines**: External constraints overcome procrastination
- Students complete assignments just before deadlines
- Experiment: Self-imposed deadlines improve performance (though not as much as externally imposed)

## Social Preferences

### Beyond Self-Interest

**Traditional Economics**: People are purely self-interested.

**Reality**: People care about fairness, reciprocity, social norms, others' outcomes.

### Fairness and Reciprocity

**Ultimatum Game**:
- Player 1 proposes split of $10
- Player 2 accepts (both get proposed amounts) or rejects (both get $0)
- **Rational prediction**: Player 1 offers $0.01, Player 2 accepts (better than nothing)
- **Reality**: Offers below $3 usually rejected; modal offer is $5 (50/50 split)

**Explanation**: People reject unfair offers to punish selfishness, even at personal cost.

**Dictator Game**:
- Player 1 divides $10, Player 2 has no choice
- **Rational prediction**: Player 1 keeps entire $10
- **Reality**: Average offer is $2-3; many offer $5

**Explanation**: People have preferences for fairness, not just maximizing own payoff.

**Public Goods Game**:
- Each player contributes to public pool (multiplied, then divided equally)
- **Rational prediction**: Contribute nothing (free ride)
- **Reality**: Average contribution is 40-60% initially, declining over rounds

**Explanation**: People are conditionally cooperative - cooperate if others do, defect if others don't.

### Reciprocity

**Positive Reciprocity**: Rewarding kind behavior
- Workers paid above-market wages exert more effort (efficiency wages)
- Gift exchange: Restaurant tips, despite one-time interaction

**Negative Reciprocity**: Punishing unkind behavior
- Employees retaliate against perceived unfairness with sabotage, shirking
- Trade wars: Countries retaliate against tariffs even when harmful to self

**Real-World Example - Uber Surge Pricing**:
- During high demand (New Year's Eve), prices rise
- Economically efficient (rations scarce rides)
- Customers perceive as unfair ("gouging"), hurt brand reputation
- Fairness concerns constrain profit-maximizing pricing

### Social Norms

**Definition**: Informal rules governing behavior in groups.

**Examples**:
- Tipping 15-20% at restaurants
- Queuing (first-come, first-served)
- Gift giving (reciprocal, appropriate value)
- Voting (civic duty, despite negligible impact)

**Enforcement**: Social approval/disapproval, guilt, reputation

**Crowding Out Intrinsic Motivation**:
- Introducing monetary incentives can backfire by replacing social norms with market norms

**Experiment - Daycare Late Pickups** (Gneezy & Rustichini):
- Daycare introduced fine for late pickups
- Result: Late pickups INCREASED
- Explanation: Fine transformed social norm ("don't inconvenience teachers") into market transaction ("I paid for extra time")

**Real-World Application**: Paying blood donors reduces donations (countries with payment have lower supply). Social motivation (helping others) stronger than small payment.

## Nudges and Choice Architecture

### Libertarian Paternalism

**Concept** (Thaler & Sunstein, 2008): Design choice environments to steer people toward better decisions while preserving freedom of choice.

**Libertarian**: Preserve choice (no mandates)
**Paternalism**: Guide toward choices improving welfare

**Justification**: If choices are biased (predictably irrational), choice architecture inevitably influences decisions. Might as well design it to help people.

### Types of Nudges

| Nudge Type | Description | Example |
|------------|-------------|---------|
| **Default Options** | Preset choice people adopt by doing nothing | Opt-out retirement enrollment, organ donation |
| **Simplification** | Reduce complexity | One-page financial aid form |
| **Social Norms** | Highlight what others do | "90% of hotel guests reuse towels" |
| **Salience** | Make important information prominent | Calorie counts on menus |
| **Commitment Devices** | Allow self-binding | Save More Tomorrow plan |
| **Reminders** | Prompt action | Text reminders for appointments |
| **Incentives** | Small rewards for desired behavior | Pay-as-you-throw garbage fees |

### Default Options

**Power**: People stick with defaults due to inertia, implied endorsement, loss aversion (changing feels like loss).

**Real-World Applications**:

**Retirement Savings**:
- Traditional: Opt-in (must actively enroll)
- Automatic enrollment: Opt-out (enrolled by default)
- Result: Participation rates 90%+ with opt-out vs 40-60% with opt-in

**Organ Donation**:
- Opt-in countries (US, UK, Germany): 10-20% consent rates
- Opt-out countries (Austria, Spain): 90%+ consent rates
- Same population, different default = dramatic difference

**Green Energy**:
- Default electricity from renewables (opt-out to conventional)
- Participation rates 80-90% vs 10-20% when renewable is opt-in

**Criticism**: Manipulative? Undermines autonomy? Can be used for good or bad purposes.

### Social Norms Nudges

**Mechanism**: People conform to perceived norms (what others do, what others approve).

**Examples**:

**Energy Conservation**:
- Utility bills showing household usage vs neighbors
- Result: High users reduce consumption; low users increase slightly (unintended effect)
- Solution: Add smiley face for low users (reinforces good behavior)

**Tax Compliance**:
- Letters stating "9 out of 10 people pay taxes on time"
- Result: Increased compliance among late payers

**Hotel Towel Reuse**:
- Sign: "75% of guests reuse towels"
- More effective than environmental appeal ("save the planet")

**Voting**:
- "Your neighbors are voting" increases turnout more than civic duty appeals

**Criticism**: Privacy concerns; what if social norm is undesirable?

### Commitment Devices

**Examples**:

**Save More Tomorrow**:
- Employees commit now to save percentage of future raises
- Takes advantage of loss aversion (future money less painful to commit)
- Increased savings rates dramatically

**Gym Memberships**:
- Pay upfront for year (commitment) vs pay-per-visit
- Many don't maximize usage but having sunk cost increases attendance

**Public Commitments**:
- Weight loss groups, smoking cessation support
- Social pressure and accountability increase success

**Apps**:
- Forest (phone usage) - plant virtual tree, dies if you use phone
- Beeminder - financial penalty if miss goals

## Mental Accounting

### Concept

**Richard Thaler**: People categorize money into mental "accounts" based on source or intended use, treating dollars differently depending on account.

**Violation of Fungibility**: Money is money; $1 should be valued the same regardless of source or label. Mental accounting violates this.

### Examples

**Windfall Gains vs Earned Income**:
- Tax refund often spent on luxury ("found money")
- Regular income carefully budgeted
- Both are income but treated differently

**Segregation of Losses**:
- Prefer two $50 losses to one $100 loss (separate accounts feel less painful)

**Integration of Gains**:
- Prefer one $100 gain to two $50 gains (combined feels bigger)

**Sunk Costs**:
- Ticket to concert cost $100, night of show it's snowing
- More likely to attend because of sunk cost (shouldn't be relevant to decision)
- If ticket was free, less likely to brave snow

**Payment Decoupling**:
- All-inclusive resort: Having already paid, food feels "free," encourages overconsumption
- Credit cards decouple payment from consumption, increasing spending
- Gift cards feel like "free money," spent more readily than cash

### Real-World Applications

**Budgeting**:
- Envelope method (cash for groceries, entertainment, etc.)
- Prevents overspending in one category
- Effective despite violating fungibility

**Rebates and Bonuses**:
- Companies pay bonuses rather than equivalent salary increase
- Bonus is "extra," more likely spent on luxuries (greater value to employee perceived)

**Marketing**:
- "Gas surcharge" feels less painful than equivalent price increase
- Partitioned pricing (base price + fees) feels better than total price

**Investment**:
- Hold stocks in "retirement account" vs "trading account"
- Same stocks, different mental accounts, different risk tolerance

## Applications

### Policy

**UK Nudge Unit** (Behavioral Insights Team):
- Simplified tax letters (increased compliance)
- Donor default (increased organ donation)
- "Plain English" government forms

**US Social and Behavioral Sciences Team**:
- Simplified financial aid forms (FAFSA)
- Email reminders for benefits enrollment
- Veterans pension application assistance

**Results**: Often 10-30% improvements in outcomes at minimal cost.

### Marketing and Business

**Pricing**:
- Charm pricing ($9.99 vs $10) - left digit matters disproportionately
- Decoy pricing - introduce expensive option to make target option seem reasonable

**Subscriptions**:
- Automatic renewal (defaults)
- Free trial then paid (present bias, people forget to cancel)

**Loss Aversion**:
- "Don't miss out" vs "Get this deal"
- Free shipping thresholds ("Spend $25 more to avoid $5 shipping")

**Scarcity**:
- "Only 2 left in stock" creates urgency
- Limited-time offers leverage loss aversion

### Healthcare

**Medication Adherence**:
- Reminders and simplified regimens increase compliance
- Pill packaging with days labeled

**Healthy Choices**:
- Place healthy foods at eye level in cafeterias
- Smaller plates reduce portions consumed (anchoring)
- Calorie labeling nudges healthier choices

**Savings**:
- Health Savings Accounts (HSAs) - mental accounting encourages saving for medical expenses

### Personal Finance

**Retirement Savings**:
- Automatic enrollment and escalation
- Employer matching (loss aversion: "free money")

**Budgeting Apps**:
- Visualize spending across categories (mental accounting)
- Alerts for overspending

**Commitment Savings**:
- Freeze access until goal reached
- Particularly effective in developing countries (SEED accounts)

## Criticisms and Limitations

### Methodological Concerns

**External Validity**: Lab experiments may not reflect real-world behavior
- Small stakes, artificial settings, unusual subject pool (college students)

**Replication Crisis**: Some famous findings don't replicate
- Ego depletion, priming effects questioned

**Context Dependence**: Effects vary by population, culture, stakes
- Limits generalizability

### Ethical Concerns

**Manipulation**: Is steering choices paternalistic overreach?
- Who decides what's "better" for people?
- Slippery slope to authoritarianism?

**Autonomy**: Even if freedom preserved, nudging undermines autonomy
- People should make own mistakes

**Asymmetric Application**: Corporations and governments have vastly more resources to employ behavioral insights than individuals to defend against them

**Transparency**: Should nudges be disclosed?
- Disclosure may reduce effectiveness
- But secret manipulation seems unethical

### Theoretical Concerns

**Ad Hoc Nature**: Collection of biases without unified theory
- Difficult to predict which bias applies when

**Context-Dependent**: Framing effects, social norms vary by culture, situation
- Limits predictive power

**Doesn't Replace Incentives**: Nudges work at the margin; can't substitute for strong incentives
- Small effects (10-30% improvements)

**Debiasing**: If people learn about biases, do they correct them?
- Evidence mixed; many biases persist even with knowledge

## **Key Terms**

- **Bounded Rationality**: Limited cognitive ability leads to satisficing, not optimizing
- **Heuristics**: Mental shortcuts that simplify decision-making
- **Availability Heuristic**: Judge probability by ease of recall
- **Representativeness Heuristic**: Judge probability by similarity to stereotype
- **Anchoring**: Initial number disproportionately influences estimates
- **Prospect Theory**: Decisions based on changes from reference point, not absolute outcomes
- **Loss Aversion**: Losses hurt more than equivalent gains feel good
- **Framing Effects**: Presentation of identical information changes decisions
- **Hyperbolic Discounting**: Present-biased time preferences
- **Mental Accounting**: Categorizing money differently based on source or use
- **Nudge**: Choice architecture steering toward better decisions while preserving choice
- **Default Option**: Preset choice adopted by inaction

## Summary

Behavioral economics documents systematic deviations from rational decision-making assumptions. People are boundedly rational, using heuristics (availability, representativeness, anchoring) that create predictable biases. Prospect theory explains risk attitudes through reference dependence, loss aversion, and diminishing sensitivity, with framing effects demonstrating that identical options presented differently yield different choices.

Time inconsistency and hyperbolic discounting cause present bias - procrastination, undersaving, overconsumption. Social preferences for fairness and reciprocity contradict pure self-interest, with people rejecting unfair offers and cooperating in public goods despite individual incentives to defect. Mental accounting treats money differently based on source or intended use, violating fungibility.

Nudges and choice architecture leverage these insights to improve decisions while preserving freedom. Default options, simplification, social norms, and commitment devices yield substantial impacts at low cost. Applications span policy (organ donation, retirement savings), marketing (pricing, framing), healthcare (medication adherence), and personal finance (automatic enrollment).

Criticisms include methodological concerns (external validity, replication), ethical issues (manipulation, autonomy), and theoretical limitations (ad hoc nature, context dependence). Nevertheless, behavioral economics has transformed economics, policy, and business by providing more realistic models of human behavior.

Understanding behavioral economics enhances self-awareness of decision-making biases, critical evaluation of marketing tactics, and design of policies and environments that help people achieve their goals.
