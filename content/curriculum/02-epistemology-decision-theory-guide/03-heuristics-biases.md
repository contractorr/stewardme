# Heuristics & Cognitive Biases

## Overview

Humans don't reason like Bayesian calculators. Evolution optimized us for survival in ancestral environments — small groups, immediate threats, visible cause-effect relationships. Modern contexts — statistics, long-term planning, abstract probabilities, complex systems — trigger cognitive mechanisms that systematically misfire. We use heuristics — mental shortcuts that are fast, effortless, and often effective but produce predictable errors in specific contexts.

Understanding heuristics and biases isn't about condemning human reasoning as "irrational." It's about recognizing the mismatch between our cognitive architecture and modern decision environments, identifying when to trust intuition and when to override it with deliberate analysis.

This chapter examines the major heuristics (availability, representativeness, anchoring, affect), core biases (confirmation, overconfidence, hindsight, sunk cost), and the dual-process framework that explains why these patterns persist despite education and intelligence.

## Dual Process Theory

Daniel Kahneman's framework, synthesizing decades of cognitive psychology, divides thinking into two systems with fundamentally different operating characteristics:

| Feature | System 1 (Intuitive) | System 2 (Reflective) |
|---------|---------------------|----------------------|
| **Speed** | Fast, automatic, instant | Slow, deliberate, effortful |
| **Effort** | Effortless, parallel processing | Effortful, capacity-limited |
| **Awareness** | Unconscious, opaque to introspection | Conscious, reportable |
| **Control** | Involuntary, cannot be "turned off" | Voluntary, can be engaged or disengaged |
| **Capacity** | High-bandwidth, processes many inputs simultaneously | Low-bandwidth, serial, one thing at a time |
| **Content** | Percepts, impressions, feelings, associations | Beliefs, choices, explicit reasoning, calculations |
| **Evolutionary age** | Ancient, shared with animals | Recent, distinctly human |
| **Examples** | Recognizing faces, detecting anger in voices, driving on empty roads, reading simple text, 2+2=? | Parking in a narrow space, complex mental arithmetic, filling out tax forms, checking the validity of a logical argument |
| **Errors** | Systematic biases from heuristic processing | Laziness, premature termination, insufficient override of System 1 |
| **Learning** | Associative, pattern-based, gradual | Rule-based, explicit, can learn from single instances |

### How They Interact

System 1 continuously runs, generating impressions, feelings, and intuitions. System 2 monitors these outputs and sometimes intervenes to correct, refine, or override. The critical insight: **System 2 is lazy**. It endorses System 1's suggestions without checking them unless:

1. System 1 signals uncertainty or conflict (e.g., the bat and ball problem creates a feeling of wrongness)
2. The situation is explicitly recognized as requiring calculation (e.g., formal logic, unfamiliar math)
3. Incentives or norms demand effortful reasoning (e.g., high-stakes decisions, professional requirements)

When System 2 fails to engage — due to cognitive load, time pressure, lack of motivation, or simple laziness — System 1's biases go uncorrected.

**Evidence for dual processes**:
- **Cognitive load**: Forcing people to remember an 8-digit number (occupying System 2) increases reliance on stereotypes, makes them more susceptible to anchoring, and reduces self-control
- **Individual differences**: People with higher cognitive reflection test (CRT) scores override intuitive wrong answers more often
- **Time pressure**: Forcing fast responses increases bias; allowing time for deliberation reduces it
- **Priming**: Subtle cues activate System 1 associations that influence judgments (though replication has been mixed)

### The Bat and Ball Problem

**Question**: A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?

**System 1 answer**: $0.10 (fast, feels right, wrong)
**System 2 answer**: $0.05 (requires checking: ball = $0.05, bat = $1.05, total = $1.10)

Over 50% of students at Harvard, MIT, and Princeton gave the intuitive wrong answer. Intelligence doesn't eliminate System 1; it just makes System 2 better at *rationalizing* System 1's outputs when engaged.

## The Major Heuristics

### Availability Heuristic

**Definition**: Judging the frequency or probability of events by the ease with which instances come to mind.

**Mechanism**: System 1 uses "ease of retrieval" as a proxy for "actual frequency." In ancestral environments, this worked — memorable events (predator attacks, poisonous foods) were often common or important. In modern media-saturated environments, it systematically misfires.

**Classic examples**:

| People Estimate... | Reality |
|-------------------|---------|
| Homicide > Diabetes deaths | Diabetes kills ~5x more |
| Tornado > Asthma deaths | Asthma kills ~20x more |
| Shark attacks are common | ~10 deaths/year globally vs ~40K drowning deaths |
| Terrorism is major cause of death | ~50 deaths/year in US vs ~600K cancer, ~600K heart disease |
| Plane crashes are dangerous | Driving is ~100x more dangerous per mile |

**Why?**: Media coverage makes rare, dramatic events vivid and easy to recall. Deaths from chronic diseases are mundane, dispersed, and underreported.

**Tversky & Kahneman study** (1973): Participants heard a list of 39 names — 19 famous women (e.g., Elizabeth Taylor) and 20 non-famous men. Later asked "Were there more men or women?" they said women. Famous names were easier to recall, inflating perceived frequency.

**Real-world consequences**:

**Post-9/11 driving**: Increased fear of flying led Americans to drive more. Estimated ~1,500 additional highway deaths in the year following 9/11 (Gigerenzer 2004) — more than died in the attacks. Availability made flying feel dangerous, driving feel safe.

**Vaccine fears**: Andrew Wakefield's fraudulent 1998 study linking MMR vaccine to autism (retracted 2010) created vivid, emotionally compelling anecdotes. Availability of "my child was fine, then got vaccinated, then developed autism" narratives overwhelmed statistical evidence. Measles cases surged.

**Nuclear vs coal**: Nuclear accidents (Three Mile Island, Chernobyl, Fukushima) are vivid, available, and scary. Coal kills ~10,000 Americans annually through air pollution (and hundreds of thousands globally) — but deaths are dispersed, invisible, and unavailable. Result: exaggerated fear of nuclear, insufficient concern about coal.

### Representativeness Heuristic

**Definition**: Judging the probability of an event by how much it resembles a typical case (stereotype or prototype), ignoring base rates and sample size.

**Mechanism**: System 1 assesses similarity, not probability. "Does this person seem like an engineer?" substitutes for "What's the probability this person is an engineer given the base rate?"

#### The Linda Problem (Tversky & Kahneman, 1983)

**Description**: Linda is 31 years old, single, outspoken, and very bright. She majored in philosophy. As a student, she was deeply concerned with issues of discrimination and social justice, and participated in anti-nuclear demonstrations.

**Question**: Which is more probable?
(a) Linda is a bank teller
(b) Linda is a bank teller and is active in the feminist movement

**Result**: 85-90% of respondents choose (b), committing the **conjunction fallacy**.

**Why it's wrong**: P(A and B) ≤ P(A) always. The set of "feminist bank tellers" is a subset of "bank tellers." Adding a condition cannot increase probability.

**Why people err**: The description is highly representative of feminists, not of bank tellers. System 1 says "Linda sounds like a feminist" and endorses (b). System 2 doesn't engage to check the logic.

**Variations**: Even telling people "by probability, we mean mathematical probability, you can't choose the conjunction" doesn't eliminate the fallacy. Changing to frequency format ("How many out of 100 people like Linda...?") reduces but doesn't eliminate it.

#### Base Rate Neglect

**Kahneman & Tversky's taxicab problem**:

A hit-and-run taxi accident occurs at night. Two taxi companies operate in the city: Green (85% of taxis) and Blue (15% of taxis). A witness says the taxi was Blue. The court tests the witness under nighttime conditions and finds he correctly identifies each color 80% of the time but makes errors 20% of the time.

**Question**: What's the probability the taxi was actually Blue?

**Intuitive answer**: 80% (the witness accuracy)

**Correct answer**: ~41%

Using Bayes' theorem:
```
P(Blue | witness says Blue) = P(witness says Blue | Blue) × P(Blue) / P(witness says Blue)

P(witness says Blue) = P(witness says Blue | Blue) × P(Blue) + P(witness says Blue | Green) × P(Green)
                     = 0.80 × 0.15 + 0.20 × 0.85
                     = 0.12 + 0.17
                     = 0.29

P(Blue | witness says Blue) = (0.80 × 0.15) / 0.29 = 0.12 / 0.29 ≈ 0.41 or 41%
```

The base rate (85% Green) overwhelms the witness testimony. But representativeness focuses on the testimony (specific, causal, vivid) and ignores the base rate (abstract, statistical, pallid).

**Engineer/lawyer problem**:

100 people: 70 engineers, 30 lawyers. Here's a description: "Jack is 45 years old. He is conservative, careful, and ambitious. He shows no interest in political issues and spends his free time on carpentry and solving mathematical puzzles."

**Question**: What's the probability Jack is an engineer?

**Modal answer**: ~90% (description is highly representative of engineers)

**Correct starting point**: 70% (base rate). The description should update from 70%, but not all the way to 90% unless it's extremely diagnostic.

Now flip it: 30 engineers, 70 lawyers. Same description. Many people still say ~90% engineer. They ignore the base rate entirely, using only representativeness.

#### The Gambler's Fallacy

A fair roulette wheel has hit red 5 times in a row. What's more likely on the next spin: red, black, or equally likely?

**Correct**: Equally likely (50-50, wheel has no memory)

**Gambler's fallacy**: Black is "due" (representativeness says a short sequence should resemble the long-run distribution — roughly equal reds and blacks)

**Hot hand fallacy**: Basketball player makes 3 shots in a row. Is the next shot more likely to go in? Intuition says yes ("hot hand"). Analysis of NBA data: No. Prior makes don't predict future makes beyond baseline skill level. People see patterns in randomness.

### Anchoring and Adjustment

**Definition**: Numerical judgments are disproportionately influenced by initial values (anchors), even when the anchor is obviously arbitrary.

**Classic demonstration** (Tversky & Kahneman, 1974):

Spin a wheel of fortune rigged to stop at 10 or 65. Then ask: "What percentage of African nations are members of the United Nations?"

**Result**:
- Participants who saw 10: median estimate ~25%
- Participants who saw 65: median estimate ~45%

The wheel was manifestly random and irrelevant, yet it anchored estimates by ~20 percentage points.

**Mechanism**: Two processes:
1. **Insufficient adjustment**: Start at the anchor and adjust, but adjustments are typically insufficient (System 2 stops adjusting too early)
2. **Selective accessibility**: The anchor activates anchor-consistent information in memory

**Real-world anchoring effects**:

| Context | Anchor | Effect |
|---------|--------|--------|
| **Negotiation** | First offer | Powerfully anchors final settlement (even with experienced negotiators) |
| **Real estate** | Listing price | Anchors buyer valuation and final sale price |
| **Retail** | MSRP / original price | "Was $100, now $60!" feels like a deal even if $60 is the normal price |
| **Sentencing** | Prosecutor's recommendation | Judges' sentences correlate with prosecutor recommendations (even experienced judges) |
| **Damage awards** | Plaintiff's demand | Jury awards correlate with plaintiff demands |
| **Salary negotiation** | Initial offer | First number anchors subsequent counteroffers |

**Study** (Englich & Mussweiler, 2001): Experienced German judges read a case description and a prosecutor's sentencing recommendation (randomly either 2 months or 34 months). Average sentence:
- 2-month anchor: 18 months
- 34-month anchor: 28 months

The judges adamantly denied being influenced and rated the recommendations as "extremely inappropriate." Anchoring operated unconsciously.

**Debiasing**: Extremely difficult. Awareness helps only slightly. **Considering the opposite** — explicitly generating reasons the anchor might be too high or too low — reduces but doesn't eliminate anchoring. **Using your own anchor first** before hearing others' can help in negotiations.

### Affect Heuristic

**Definition**: Using current feelings ("Do I like/fear this?") as information about probability and risk.

**Mechanism**: System 1 generates affective responses (good/bad feelings) to stimuli automatically. When asked to judge probability or risk, System 1 substitutes the easier question "How do I feel about this?" for the harder question "What are the statistics?"

**Slovic's risk matrix**:

People judge technologies simultaneously on two dimensions: benefit and risk. Rationally, these should be independent or even negatively correlated (high-benefit technologies might justify accepting higher risks). Empirically, they're strongly negatively correlated in public perception:

| Technology | Feeling | Perceived Risk | Perceived Benefit |
|-----------|---------|---------------|------------------|
| Nuclear power | Negative affect | Very high | Very low |
| Solar power | Positive affect | Very low | Very high |
| X-rays | Neutral/positive | Medium | High |

**Reality**: Nuclear has killed far fewer per kWh than coal but feels scarier. The affect heuristic dominates statistical reasoning.

**Affect and numeracy**: Showing "98% survival rate" vs "2% mortality rate" for the same surgery changes decisions. Mortality (negative affect) looms larger than survival (positive affect), even though they're mathematically equivalent.

**Finucane et al. (2000)**: Experimentally manipulating affect (describing benefits positively) caused perceived risks to drop. People appear to have a single "good/bad" attitude toward technologies and read both benefit and risk from that attitude.

**Applications**:
- **GMO foods**: Feel "unnatural" (negative affect) → high perceived risk, low perceived benefit (regardless of evidence)
- **Organic foods**: Feel "natural" (positive affect) → low perceived risk, high perceived benefit
- **Terrorism vs car accidents**: Terrorism triggers intense fear → massive investment in security. Car accidents feel mundane → insufficient safety investment despite ~40K annual US deaths

## Confirmation Bias

Perhaps the most pernicious and robust cognitive bias. The tendency to search for, interpret, favor, and recall information in a way that confirms preexisting beliefs.

### Manifestations

**1. Selective Search**: Seeking evidence that confirms beliefs, avoiding evidence that might disconfirm.

**Wason's 2-4-6 task**: I'm thinking of a rule that generates number sequences. "2, 4, 6" fits the rule. Generate other sequences to discover the rule.

Most people generate: 8, 10, 12 (fits!) → 20, 22, 24 (fits!) → rule is "consecutive even numbers"

Actual rule: "Any ascending sequence."

People test hypothesis-confirming examples (all ascending sequences of even numbers) rather than hypothesis-disconfirming examples (e.g., 1, 2, 3 or 10, 20, 30 or 5, 4, 3).

**Google**: Searching "vaccines cause autism" yields confirming results. Searching "vaccine autism evidence" yields more balanced results. People who fear vaccines search confirmingly.

**2. Biased Interpretation**: Same evidence, opposite conclusions depending on prior beliefs.

**Lord, Ross & Lepper (1979)**: Participants with strong views on capital punishment read two studies — one supporting deterrence, one opposing. Both sides claimed the studies confirmed their views:
- Pro-capital punishment: Found the pro-deterrence study convincing, the anti-deterrence study flawed
- Anti-capital punishment: Found the anti-deterrence study convincing, the pro-deterrence study flawed

Identical evidence → opposite conclusions → increased polarization.

**3. Selective Memory**: Remembering hits, forgetting misses.

**Horoscopes**: "You will face a challenge this week" → you face challenges every week, but you remember the week when the horoscope "predicted" it.

**Confirmation in medicine**: Doctors remember the patient where their diagnosis was correct, forget the false positives. Subjective sense of diagnostic accuracy exceeds objective accuracy.

### Motivated Reasoning (Kahan et al.)

Stronger form: Reasoning deployed in service of desired conclusions, not truth.

**Political polarization study** (Kahan, 2013):

Show a graph of data on skin rash treatment: Does the treatment work?

Participants with high numeracy correctly analyzed the data.

Now show the *identical* data labeled "gun control and crime." Half saw it framed as "gun control reduces crime," half as "gun control increases crime."

**Result**: Among low-numeracy participants, political views modestly influenced interpretation. Among **high-numeracy** participants, political views **strongly** influenced interpretation.

**Implication**: Intelligence and numeracy don't reduce motivated reasoning — they make you better at constructing sophisticated justifications for what you want to believe.

**Cultural cognition**: Climate change, GMOs, nuclear power. Scientific literacy correlates with *increased* polarization, not consensus. More knowledgeable people are better at cherry-picking and interpreting evidence to fit group identity.

### Debiasing Confirmation Bias

**1. Consider the opposite**: Force yourself to generate reasons your belief might be wrong. Reduces but doesn't eliminate bias.

**2. Red teams**: Assign someone the role of arguing against the consensus. Must be empowered and incentivized (not token dissent).

**3. Pre-commitment**: Specify in advance what evidence would change your mind. "If X occurs, I'll update to Y credence."

**4. Steel-manning**: Argue the strongest version of the opposing view, not the weakest (vs straw-manning).

**5. Blind analysis**: Analyze data without knowing which hypothesis corresponds to which outcome (hard to implement outside formal research).

**6. Adversarial collaboration**: Researchers with opposing views design and conduct a study together (Kahneman & Klein on expert intuition; Tetlock's adversarial collaborations).

## Overconfidence

Possibly the most robust finding in all of judgment and decision-making research. Across domains, cultures, and contexts: People are overconfident.

### Three Varieties

**1. Calibration Overconfidence**: When people say "90% confident," they're right ~70-80% of the time. When they say "99% confident," they're right ~85-90% of the time.

**Classic study** (Fischhoff et al., 1977): Participants answered general knowledge questions and stated confidence. Results:

| Stated Confidence | Actual Accuracy |
|------------------|-----------------|
| 50% ("no idea, pure guess") | 60% (people know more than they think) |
| 70% | 65% |
| 90% | 75% |
| 100% ("absolutely certain") | 85% |

The confidence-accuracy gap widens at higher confidence levels.

**Expert overconfidence**: Doctors, lawyers, engineers, CIA analysts — all exhibit substantial overconfidence. Expertise reduces errors but increases confidence more, widening the gap.

**2. Better-Than-Average Effect**: Most people rate themselves above average (which is logically impossible for most).

- 93% of US drivers rate themselves "above average" drivers
- 94% of college professors rate themselves above-average teachers
- 68% of lawyers at a firm rated themselves in the top 25%
- 90% of managers rate their performance in the top 10%

Partly this reflects ambiguity (defining "good driver" subjectively), but genuine overconfidence contributes.

**3. Planning Fallacy**: Systematic tendency to underestimate time, costs, and risks of future actions while overestimating benefits.

### The Planning Fallacy in Detail

**Sydney Opera House**:
- Projected: 4 years, $7 million AUD
- Actual: 14 years, $102 million

**The Big Dig** (Boston):
- Projected: 1991-1998, $2.6 billion
- Actual: 1991-2007, $14.6 billion (560% cost overrun)

**California High-Speed Rail**:
- Projected (2008): Completion 2020, $33 billion
- Current (2024): Partial completion ~2030, $100+ billion

**Bent Flyvbjerg's megaproject data** (2003):

Analyzed 258 transportation projects across 20 nations, 70 years:

| Project Type | Average Cost Overrun | Projects Over Budget |
|-------------|---------------------|---------------------|
| Rail | 45% | 90% |
| Bridges/Tunnels | 34% | 75% |
| Roads | 20% | 70% |

**Average** delay: 9 months. Cost and time overruns haven't declined over 70 years despite better planning tools.

**Why?**:
- **Inside view**: Focus on project-specific plans, ignoring base rates of similar projects
- **Optimism bias**: Focus on best-case scenarios
- **Anchoring**: Initial estimates anchor later estimates, adjustments are insufficient
- **Strategic misrepresentation**: Deliberately lowballing to secure approval (agencies know projects will exceed estimates but can't admit it)

**Solution**: **Reference class forecasting** (Kahneman). Instead of estimating "inside" (our project, our plan), find the base rate of similar past projects (the "outside view").

Example: "We estimate 12 months." → "Similar IT projects in our industry average 18 months, with 30% exceeding 24 months." → Start with 18 months, adjust modestly based on specific factors.

### Dunning-Kruger Effect

**Finding** (Kruger & Dunning, 1999): Incompetent people:
1. Overestimate their own skill
2. Fail to recognize genuine skill in others
3. Fail to recognize the extremity of their inadequacy

Bottom quartile performers estimated they were at the 60th percentile.

Top quartile performers slightly underestimated (estimated 75th percentile, were 88th percentile) — they assumed others were nearly as competent.

**Mechanism**: Skill and meta-skill (ability to evaluate skill) are coupled. To recognize incompetence requires the very competence you lack. "The fool doth think he is wise, but the wise man knows himself to be a fool." (Shakespeare)

**Domain-specific**: Being competent in X doesn't prevent Dunning-Kruger in Y. A brilliant physicist can be a dunning-kruger victim about economics.

**Replication**: Robust across many domains — logical reasoning, grammar, emotional intelligence, medical knowledge, lab skills, humor. The effect is real.

**Not symmetric**: Low performers vastly overestimate. High performers modestly underestimate or are well-calibrated. It's not that everyone thinks they're above average equally.

## Additional Important Biases

### Hindsight Bias ("I Knew It All Along")

**Definition**: After learning an outcome, people falsely believe they "would have predicted it."

**Fischhoff & Beyth (1975)**: Before Nixon's 1972 China trip, participants estimated probabilities of various outcomes. Afterward, asked to recall their original estimates. Participants systematically misremembered their estimates as closer to what actually happened.

**9/11**: After 9/11, many claimed the attacks were "obvious," citing all the warning signs. Pre-9/11, those signs were ambiguous and lost in noise. Hindsight creates an illusion of inevitability.

**Financial crises**: The 2008 crash was "obvious in retrospect" (housing bubble, subprime mortgages, excessive leverage). Yet few predicted timing or magnitude beforehand.

**Consequence**: Outcomes feel more predictable than they were → we blame decision-makers for failing to foresee the "obvious" → discourages risk-taking → distorts learning (can't learn from history if you think outcomes were inevitable).

**Remedy**: **Decision journals**. Record your predictions and reasoning before outcomes. Compare to actual outcomes. This forces confrontation with genuine ex-ante uncertainty.

### Sunk Cost Fallacy

**Definition**: Continuing an endeavor because of previously invested resources (time, money, effort), even when continuing is not justified by future expected value.

**Examples**:
- Finishing a bad movie because you paid $15 for the ticket
- Continuing a failing project because you've invested 2 years
- Staying in a bad relationship because "we've been together so long"
- Businesses pouring money into doomed products because of R&D investment

**Normative economics**: Only future costs and benefits matter. Sunk costs are irrelevant to rational choice.

**Psychology**: Loss aversion + commitment + desire not to "waste" investment.

**Concorde fallacy**: British/French governments continued funding the Concorde supersonic jet despite it being clear it would never be profitable. "Too much invested to quit."

**Escalation of commitment** (Staw, 1976): Vietnam War. Continued escalation partly because of sunk costs ("We can't let their sacrifice be in vain").

**Why hard to avoid**: Social pressure, ego, fear of admitting error, lack of clear alternative, hope that "just a bit more" will turn it around.

**Remedy**: **Pre-mortems**, **decision checkpoints** (specify in advance what would trigger abandonment), **separate decision-makers** (those who decide to continue weren't those who made initial investment).

### Status Quo Bias

**Definition**: Disproportionate preference for current state; resistance to change even when change is beneficial.

**Default effects**: Defaults have enormous influence.

| Country | Organ Donor Consent | Donor Rate |
|---------|-------------------|-----------|
| Austria | Opt-out (default = donor) | 99% |
| Germany | Opt-in (default = not donor) | 12% |
| Denmark | Opt-in | 4% |
| France | Opt-out | 98% |

Genetically similar populations, huge differences driven entirely by defaults.

**Retirement savings**: Automatic enrollment in 401(k) → ~90% participation. Opt-in enrollment → ~40% participation. Identical benefits, different defaults.

**Inertia**: People stick with current insurance, phone plan, bank — even when switching would save hundreds of dollars with minimal effort.

**Endowment effect** (Kahneman, Knetsch, Thaler): People demand ~2x more to give up an object than they'd pay to acquire the identical object. Loss aversion + status quo bias.

**Remedy**: "Choosing from scratch" thought experiment. If you didn't currently have X, would you choose it? If no, seriously consider switching.

### Framing Effects

**Definition**: Logically equivalent information presented differently leads to different choices.

**Asian Disease Problem** (Tversky & Kahneman, 1981):

Imagine a disease outbreak expected to kill 600 people. Two programs proposed:

**Frame 1 (lives saved)**:
- Program A: 200 people will be saved (72% choose)
- Program B: 1/3 probability that 600 saved, 2/3 probability that 0 saved (28% choose)

**Frame 2 (lives lost)**:
- Program C: 400 people will die (22% choose)
- Program D: 1/3 probability that 0 die, 2/3 probability that 600 die (78% choose)

A and C are identical (200 saved = 400 die out of 600). B and D are identical. Yet framing reverses preferences:
- Gain frame → risk averse (prefer certainty)
- Loss frame → risk seeking (gamble to avoid sure loss)

**Medical framing**: "90% survival rate" vs "10% mortality rate" for surgery → different choices, same facts.

**Remedy**: Reframe deliberately from multiple angles. Ask "How would this look framed as a gain? As a loss? As a percentage? As absolute numbers?"

### Scope Insensitivity

**Definition**: Failure to scale valuation in proportion to magnitude.

**Desvousges et al. (1993)**: Willingness to pay to save migratory birds from drowning in oil ponds:
- Save 2,000 birds: $80
- Save 20,000 birds: $78
- Save 200,000 birds: $88

10-100x difference in outcome → no meaningful difference in valuation.

**Mechanism**: Affect heuristic. "Saving birds" generates a good feeling. That feeling doesn't scale with numbers. System 1 responds to "saving birds" (category), not "saving 200,000 birds" (magnitude).

**Real-world**: Foreign aid, public health spending, environmental protection — political support often doesn't scale with scope of benefit.

**"Identifiable victim effect"**: One child trapped in a well → national outpouring of resources. Thousands dying from preventable disease → shrug. Specific, identifiable victims generate affect; statistical lives don't.

**Remedy**: "Shut up and multiply" (Yudkowsky). Force yourself to calculate. If saving 2,000 birds is worth $80, saving 200,000 should be worth ~$8,000. Use System 2 to override System 1.

## Prospect Theory (Kahneman & Tversky, 1979)

The most influential descriptive model of decision-making under risk. Directly challenged expected utility theory by documenting systematic violations.

### Core Components

**1. Reference Dependence**: Outcomes evaluated as gains or losses relative to a reference point (usually status quo), not as absolute final wealth.

Losing $100 when you have $1,000 ≠ not gaining $100 when you have $900, even though both result in $900.

**2. Loss Aversion**: Losses loom larger than gains. The pain of losing $X ≈ the pleasure of gaining $2X.

Value function:
```
v(x) = x^α for x ≥ 0 (gains, α ≈ 0.88)
v(x) = -λ(-x)^β for x < 0 (losses, λ ≈ 2.25, β ≈ 0.88)
```

The function is steeper for losses (λ ≈ 2-2.5).

**Graph shape**: S-curve. Concave for gains (diminishing sensitivity — $100→$200 feels bigger than $1,100→$1,200), convex for losses (same diminishing sensitivity).

**3. Diminishing Sensitivity**: The marginal impact of changes decreases with distance from reference point.

$0→$100 feels larger than $1,000→$1,100
Losing $100→$200 feels worse than losing $1,100→$1,200

**4. Probability Weighting**: People transform probabilities nonlinearly.

Weighting function π(p):
- Overweights small probabilities: π(0.01) ≈ 0.05
- Underweights medium-to-high probabilities: π(0.5) ≈ 0.42, π(0.9) ≈ 0.71
- Near-linear at extremes: π(0) = 0, π(1) = 1

**Fourfold pattern**:

| | Gains | Losses |
|--|-------|--------|
| **Low probability** (overweighted) | Risk-seeking (buy lottery tickets) | Risk-averse (buy insurance) |
| **High probability** (underweighted) | Risk-averse (prefer sure gain) | Risk-seeking (gamble to avoid sure loss) |

This explains seemingly contradictory behaviors: The same person buys lottery tickets (low-prob gain, risk-seeking) and insurance (low-prob loss, risk-averse).

### Applications

**Disposition effect** (Shefrin & Statman): Investors sell winners too early (lock in gains, risk-averse for gains) and hold losers too long (avoid realizing losses, risk-seeking for losses). Systematically reduces returns.

**Endowment effect** (Thaler): Mug experiment. Give half of people mugs. Then allow trading. Rational prediction: ~50% trade (random initial assignment, some prefer mug, some prefer money). Actual: ~10% trade. Loss aversion → selling price (~$7) >> buying price (~$3).

**Labor supply** (Camerer et al.): NYC cab drivers. Rational: Drive more when demand is high (rainy days, events). Actual: Many have daily income targets (reference points). On high-earning days, quit early (reached target). On low-earning days, work longer (try to reach target). Driven by reaching reference point, not by maximizing income.

**Negotiation**: First offer sets reference point. From that reference, concessions feel like losses. Framing concessions as "smaller losses" vs "foregone gains" changes willingness to accept.

## Debiasing Strategies

| Strategy | Description | Target Biases | Effectiveness |
|----------|-------------|---------------|---------------|
| **Consider the opposite** | Explicitly generate reasons your belief might be wrong | Confirmation bias, overconfidence | Moderate |
| **Reference class forecasting** | Use base rates from similar past cases | Planning fallacy, overconfidence | High |
| **Pre-mortem** | Imagine failure, explain why it happened | Overconfidence, planning fallacy, groupthink | High |
| **Red team** | Assign someone to argue against the plan | Confirmation bias, groupthink | High (if empowered) |
| **Calibration training** | Practice making probabilistic predictions, track accuracy | Overconfidence, calibration | High |
| **Decision journal** | Record decisions, reasoning, predicted outcomes; review later | Hindsight bias, outcome bias, overconfidence | Moderate-High |
| **Checklists** | Standardized list for critical decisions | Omission errors, availability, overconfidence | High (for routine tasks) |
| **Outside view** | Ask "What happened in similar cases?" before inside analysis | Planning fallacy, optimism, uniqueness bias | High |
| **Prospective hindsight** | "Assume we failed. Why?" (same as pre-mortem) | Overconfidence, overlooked risks | High |
| **Devil's advocate** | Formal role to critique the plan | Groupthink, confirmation bias | Moderate (often not taken seriously) |
| **Reframing** | Present same info in different frames | Framing effects | Moderate |
| **Sleeping on it** | Delay for System 2 to engage | Affect heuristic, System 1 dominance | Moderate |
| **Accountability** | Know you'll have to justify decisions to others | Confirmation bias, overconfidence | Moderate |
| **Incentives** | Reward accuracy, not confidence | Overconfidence, motivated reasoning | High (if designed well) |

**Key insight**: Awareness alone has minimal effect. Effective debiasing requires **procedural changes** (checklists, pre-mortems, decision journals) and **structural changes** (accountability, incentives, red teams).

## When Heuristics Work: Ecological Rationality (Gigerenzer)

Gerd Gigerenzer argues that framing heuristics as "biases" misunderstands their function. Heuristics are **adaptive tools** evolved to exploit environmental structure. The question isn't "Are heuristics biased?" but "In what environments do heuristics succeed or fail?"

### Fast-and-Frugal Heuristics

**Take-the-best**: Choose the option with the best value on the single most valid cue. Ignore all other cues.

Example: Choosing between two cities on population. Use recognition. If you recognize one but not the other, choose the recognized one. (Recognition correlates with size for laypeople.)

**Performance**: In many real environments, take-the-best matches or beats complex multiple regression models using all available cues.

**Why**: Heuristics are robust to overfitting. Complex models fit noise in training data, perform worse out-of-sample. Simple heuristics generalize better (bias-variance tradeoff).

### Recognition Heuristic

**Domain**: Inferring criterion values (e.g., city size, company success, sports outcomes).

**Rule**: If you recognize A but not B, infer that A has the higher value on the criterion.

**When it works**: When recognition correlates with the criterion. For laypeople, recognition correlates with city size (you've heard of large cities, not small ones).

**Goldstein & Gigerenzer (2002)**: German students vs American students predicting which of two US cities is larger. German students outperformed Americans — because Germans' recognition was more diagnostic (they'd only heard of truly large US cities), while Americans had heard of many mid-sized cities.

### Less-is-More Effects

**Expert stock pickers vs index funds**: Active management underperforms passive indexes ~80% of the time over 15 years (Malkiel, 2003). Experts have more information but worse performance.

**Why**: Financial markets are adversarial, efficient. "Exploitable" patterns are quickly arbitraged away. Experts mistake noise for signal, overtrade, and incur costs.

**Simple models vs experts**: Across many domains (medical diagnosis, parole decisions, graduate admissions), simple linear models match or beat expert judgment (Meehl, 1954; Dawes, 1979).

**Why**: Experts are inconsistent, swayed by irrelevant factors, subject to fatigue and mood. Simple models are consistent.

### Ecological Rationality Criteria

**Match heuristic to environment**:

| Environment Feature | Good Heuristic | Bad Heuristic |
|-------------------|---------------|---------------|
| **High uncertainty** | Simple rules | Complex models (overfit) |
| **Stable relationships** | Complex models | Heuristics (leave gains on table) |
| **Adversarial (others adapting)** | Unpredictable / random | Patterns (exploitable) |
| **Cooperative** | Reciprocity | Unconditional defection |
| **Redundant cues** | Take-the-best | Unit weighting (wastes info) |
| **Non-redundant, all valid** | Linear models | Take-the-best (ignores valid info) |

**Key lesson**: The "best" reasoning strategy is environment-dependent. There is no universally optimal heuristic. Rationality is ecological — it's about fit between cognitive strategy and environmental structure.

## Key Terms

- **System 1**: Fast, automatic, intuitive cognitive processing; operates effortlessly, unconsciously, in parallel
- **System 2**: Slow, deliberate, analytical cognitive processing; effortful, conscious, serial
- **Availability Heuristic**: Judging frequency/probability by ease of recall; vivid, recent events inflate estimates
- **Representativeness Heuristic**: Judging probability by similarity to prototype; ignores base rates, sample size
- **Anchoring**: Disproportionate influence of initial numerical values on subsequent judgments
- **Affect Heuristic**: Using feelings (like/dislike, fear/safety) as information about probability and risk
- **Confirmation Bias**: Seeking, interpreting, and recalling information that confirms existing beliefs
- **Motivated Reasoning**: Reasoning deployed to reach desired conclusions rather than truth
- **Overconfidence**: Gap between subjective confidence and objective accuracy; robust across domains
- **Calibration**: Match between stated confidence levels and actual accuracy frequencies
- **Planning Fallacy**: Systematic underestimation of time, cost, and risk for future actions
- **Dunning-Kruger Effect**: Incompetent people overestimate ability; competent people are well-calibrated
- **Hindsight Bias**: "I knew it all along" — post-outcome inflation of prior predictability
- **Sunk Cost Fallacy**: Continuing endeavor due to past investment despite negative future expected value
- **Status Quo Bias**: Disproportionate preference for current state; defaults powerfully influence choices
- **Framing Effect**: Logically equivalent information presented differently → different choices
- **Scope Insensitivity**: Failure to scale valuation in proportion to magnitude of outcome
- **Loss Aversion**: Losses hurt ~2× more than equivalent gains; core component of prospect theory
- **Prospect Theory**: Descriptive model: reference dependence + loss aversion + probability weighting
- **Conjunction Fallacy**: Judging P(A and B) > P(A); violates probability axioms (Linda problem)
- **Ecological Rationality**: Heuristics adapted to environmental structure; match strategy to environment
- **Pre-mortem**: Imagining failure before it happens to identify risks; highly effective debiasing tool

## Summary

Human reasoning is shaped by heuristics — fast, effortless mental shortcuts that work well in many environments but systematically misfire in others. The dual-process framework explains this: System 1 (intuitive, automatic) generates impressions and suggestions; System 2 (reflective, deliberate) monitors and sometimes overrides, but is lazy and often fails to engage.

The availability heuristic inflates estimates of vivid, recent, or emotionally salient events (terrorism > diabetes, plane crashes > car accidents). The representativeness heuristic judges by similarity to prototypes while ignoring base rates and sample size (Linda problem, engineer/lawyer problem, gambler's fallacy). Anchoring makes initial values disproportionately influence judgments, even when anchors are manifestly irrelevant. The affect heuristic substitutes feelings for statistical reasoning.

Confirmation bias — seeking confirming evidence, interpreting ambiguously, remembering selectively — is pervasive and worsened by motivated reasoning (more intelligent people construct better justifications for desired conclusions). Overconfidence appears in calibration (90% confident → 75% accurate), planning (Sydney Opera House: 4 years → 14 years), and self-assessment (better-than-average effect, Dunning-Kruger). Additional biases — hindsight, sunk cost, status quo, framing, scope insensitivity — systematically distort judgment and choice.

Prospect theory provides the dominant descriptive model: reference dependence (gains/losses vs absolute levels), loss aversion (losses hurt ~2× gains), diminishing sensitivity (s-curve value function), and probability weighting (overweight small probabilities, underweight moderate-high). This explains the disposition effect (sell winners, hold losers), endowment effect (selling price >> buying price), and fourfold risk pattern.

Debiasing strategies work but require deliberate implementation: consider the opposite, reference class forecasting, pre-mortems, red teams, calibration training, decision journals, checklists. Awareness alone is insufficient.

Gigerenzer's ecological rationality program reframes heuristics not as biases but as adaptive tools. Simple heuristics (take-the-best, recognition) often match or beat complex models in uncertain environments. The key is matching cognitive strategy to environmental structure. Rationality is ecological, not universal.

The practical lesson: Recognize the environments where intuition misleads (statistics, long-term planning, low-probability events, unfamiliar domains) and deploy System 2 override mechanisms (external tools, procedures, accountability). Heuristics aren't failures of rationality — they're features of our cognitive architecture. The challenge is knowing when to trust them and when to override.
