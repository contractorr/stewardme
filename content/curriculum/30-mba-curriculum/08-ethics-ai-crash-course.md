# Module 8: Ethics & AI Governance

**Time Investment:** ~10 hours
**Deep-Dive Book:** *Weapons of Math Destruction* by Cathy O'Neil

---

## Why This Matters for You

As AI becomes central to products, PMs face ethical decisions daily: What data to collect? What predictions to automate? Who bears the risk when systems fail? These aren't abstract philosophical questions—they're product decisions with real consequences.

**What AI can do:** Identify patterns, flag potential biases, audit systems.
**What you must do:** Make judgment calls, balance competing interests, take responsibility.

---

## Part 1: Stakeholder vs Shareholder Capitalism

### The Debate

**Shareholder primacy (Friedman):**
- Corporation's purpose: maximize shareholder value
- Social responsibility = use resources efficiently
- Let markets and government handle externalities
- Clear, measurable objective

**Stakeholder capitalism:**
- Corporation serves multiple stakeholders
- Employees, customers, communities, environment—not just shareholders
- Long-term sustainability over short-term returns
- More complex, harder to measure

### Why It Matters for PMs

Every product decision balances stakeholders:

| Decision | Stakeholder Tensions |
|----------|---------------------|
| Data collection | User privacy vs business value |
| Pricing | Customer affordability vs shareholder returns |
| Launch timing | Engineer wellbeing vs market opportunity |
| Feature cuts | Customer needs vs investor expectations |
| Supplier choice | Cost vs worker conditions |

**The question isn't whether to balance—it's how.**

### The Business Case for Ethics

Ethical behavior often aligns with long-term business interest:

- **Trust:** Ethical companies build customer loyalty
- **Talent:** Top people want to work for ethical companies
- **Risk:** Unethical behavior creates legal/reputational risk
- **Sustainability:** Stakeholder alignment = sustainable success

But not always. Sometimes doing right costs money. That's when values matter.

---

## Part 2: Ethical Frameworks

### Three Major Approaches

**1. Utilitarianism (Consequentialism)**
- **Principle:** Maximize overall well-being
- **Decision:** Which action produces best outcomes for most people?
- **Strength:** Practical, quantifiable
- **Weakness:** Can justify harming minorities for majority benefit

**2. Deontology (Kant)**
- **Principle:** Follow moral rules/duties regardless of outcome
- **Decision:** Is this action inherently right or wrong?
- **Strength:** Protects individual rights
- **Weakness:** Rules can conflict; inflexible

**3. Virtue Ethics (Aristotle)**
- **Principle:** Act as a virtuous person would
- **Decision:** What would a person of good character do?
- **Strength:** Develops moral judgment
- **Weakness:** Subjective; culture-dependent

### Applying Frameworks

**Scenario:** Should you launch a feature that helps 95% of users but creates problems for 5%?

**Utilitarian:** Calculate net benefit. If 95% benefit outweighs 5% harm, launch.

**Deontological:** Is knowingly harming 5% of users a violation of duty? If so, don't launch regardless of majority benefit.

**Virtue ethics:** Would a person of integrity launch this? What character does this decision reflect?

**In practice:** Most difficult decisions require weighing all three perspectives. Pure application of one framework rarely feels right.

### Quick Ethical Test

Before a decision, ask:

1. **Newspaper test:** Would I be comfortable if this decision appeared on the front page?
2. **Reversal test:** Would I accept this if I were in the affected group?
3. **Sleep test:** Can I sleep well after making this decision?
4. **Mother test:** Would I explain this decision proudly to my mother?

---

## Part 3: AI-Specific Ethics

### Unique Challenges of AI

**Scale:** Decisions affecting millions, automated in milliseconds

**Opacity:** Complex models difficult to explain or audit

**Feedback loops:** AI systems can amplify their own biases

**Delegation:** Who's responsible when the algorithm decides?

### Bias in AI Systems

**Sources of bias:**

1. **Training data bias**
   - Historical data reflects historical discrimination
   - Example: Resume screening trained on past hires perpetuates who got hired

2. **Selection bias**
   - Data collected doesn't represent population
   - Example: Healthcare AI trained on hospital data misses uninsured

3. **Measurement bias**
   - Proxies used don't measure what we intend
   - Example: Using zip code as proxy for creditworthiness = racial proxy

4. **Algorithmic bias**
   - Model architecture amplifies certain patterns
   - Example: Recommendation systems favoring engagement over quality

**Why bias persists:**
- "Objective" algorithms feel fair (but aren't)
- Bias can improve accuracy (on biased metrics)
- Detection is difficult (need to look for it)
- Fixing one bias may create another

### Transparency & Explainability

**The problem:**
- Users can't see why decisions affect them
- Regulators can't audit systems
- Errors are hard to identify and fix
- Trust erodes when decisions are opaque

**Levels of transparency:**

| Level | What's Visible |
|-------|----------------|
| Black box | Only outputs |
| Input transparency | What data goes in |
| Model transparency | How model works |
| Outcome transparency | Why this specific decision |

**Explainable AI (XAI):**
- Model-agnostic explanations (LIME, SHAP)
- Inherently interpretable models (decision trees, linear models)
- Trade-off: complexity often increases accuracy

### Accountability

**The accountability gap:**
- User blames company
- Company blames data
- Data team blames model
- Model team blames training data
- No one is responsible

**Closing the gap:**
- Clear ownership of AI system outcomes
- Human-in-the-loop for high-stakes decisions
- Appeals processes for affected individuals
- Regular audits and accountability reviews

---

## Part 4: Regulatory Landscape

### EU AI Act

**Risk-based approach:**

**Unacceptable risk (banned):**
- Social scoring by governments
- Real-time biometric identification in public spaces (with exceptions)
- Manipulation of vulnerable groups

**High risk (strict requirements):**
- Employment decisions
- Credit scoring
- Education access
- Essential services
- Law enforcement

**Limited risk (transparency requirements):**
- Chatbots (must disclose AI)
- Deepfakes (must label)
- Emotion recognition

**Minimal risk (no restrictions):**
- Spam filters
- Video games

### US Approach (Fragmented)

**No comprehensive federal AI law. Instead:**
- Sector-specific regulations (healthcare, finance)
- State laws (California, Illinois)
- Existing laws applied to AI (civil rights, fair lending)
- Executive orders (guidance, not law)

**Key existing laws affecting AI:**
- Fair Credit Reporting Act (credit decisions)
- Equal Credit Opportunity Act (discrimination)
- HIPAA (health data)
- State biometric privacy laws

### Emerging Global Trends

**Common themes:**
- Risk-based classification
- Transparency requirements
- Human oversight for high-stakes decisions
- Impact assessments before deployment
- Audit requirements

**For PMs:** Assume regulation is coming. Build ethical AI practices before they're required.

---

## Part 5: Building Ethical AI Products

### Ethical AI Framework

```
1. DEFINE PURPOSE
   - What problem are we solving?
   - For whom?
   - What are potential harms?

2. ASSESS DATA
   - Is training data representative?
   - What biases might exist?
   - What's the provenance?

3. DESIGN SAFEGUARDS
   - Human oversight where needed
   - Opt-out mechanisms
   - Appeals processes

4. TEST FOR HARM
   - Demographic fairness testing
   - Edge case analysis
   - Red team exercises

5. DEPLOY RESPONSIBLY
   - Gradual rollout
   - Monitoring for issues
   - Clear escalation paths

6. MONITOR & IMPROVE
   - Ongoing bias audits
   - User feedback loops
   - Regular reviews
```

### Fairness Metrics

**Multiple definitions (often in tension):**

**Demographic parity:**
- Equal positive rates across groups
- Same % approved across demographics
- Problem: Ignores base rate differences

**Equalized odds:**
- Equal true positive and false positive rates across groups
- Fair performance regardless of group
- Problem: May not achieve equal outcomes

**Calibration:**
- Predictions mean the same thing across groups
- 80% confidence = 80% accurate for all groups
- Problem: Can still have disparate impact

**The impossibility theorem:** In most cases, you can't satisfy all fairness definitions simultaneously. You must choose which fairness matters most.

### Human Oversight

**When to require human review:**
- High stakes (life, liberty, livelihood)
- Irreversible decisions
- Novel situations (out of training distribution)
- Edge cases
- Appeals

**Human-in-the-loop vs human-on-the-loop:**
- In the loop: Human approves every decision
- On the loop: Human monitors and can intervene
- Over the loop: Human sets policy, AI executes

**Choosing the right level:**
- Higher stakes → more human involvement
- Higher volume → more automation needed
- Balance: Human review of samples + edge cases

### Documentation Practices

**Model cards:**
- What the model does
- Training data description
- Intended use cases
- Known limitations
- Fairness evaluation results

**Data sheets:**
- How data was collected
- Who's represented (and who isn't)
- Known biases or issues
- Ethical review conducted

**Impact assessments:**
- Potential harms to users
- Risks to disadvantaged groups
- Mitigation strategies
- Monitoring plan

---

## Part 6: Long-term vs Short-term Tradeoffs

### The Time Horizon Problem

Short-term pressures:
- Quarterly earnings
- Launch deadlines
- Competitive threats
- Growth targets

Long-term concerns:
- Sustainable business model
- Societal impact
- Environmental footprint
- Trust and reputation

### Discount Rates

Economics uses discount rates: future value is worth less than present value.

**Applied to ethics:**
- Future harms get discounted
- Present benefits get prioritized
- Long-term consequences underweighted

**Example:** Launch now vs fix bias later
- Launch now: Immediate revenue
- Fix bias: Future harm avoided

If we heavily discount the future, we'll always launch now.

### Making Long-term Decisions

**Techniques:**

1. **Pre-mortem**
   - Imagine the future where this went wrong
   - What happened? How could we prevent it?

2. **Stakeholder mapping over time**
   - Who's affected now vs later?
   - Whose interests are underrepresented?

3. **Institutional memory**
   - Document decisions and rationale
   - Future teams can learn from past choices

4. **Long-term incentives**
   - Executive comp tied to long-term outcomes
   - Metrics that reflect sustainability

### Tragedy of the Commons

When individual short-term interests conflict with collective long-term interests:

- Each company has incentive to collect more data (competitive advantage)
- Collectively, this erodes user privacy (bad for everyone)
- No individual company can solve this alone

**Solutions:**
- Industry standards
- Regulation
- Consumer pressure
- Long-term thinking

---

## Part 7: Practical Ethics for PMs

### The PM's Ethical Responsibilities

**You're not just building features—you're making choices:**

1. **What to build** — Some things shouldn't be built
2. **How to build** — Process matters, not just outcomes
3. **For whom** — Whose interests are centered
4. **What to measure** — Metrics shape behavior
5. **When to stop** — Some projects should be killed

### Red Flags

**Watch for:**
- "The data made us do it" (hiding behind algorithms)
- "Users agreed to the terms" (consent theater)
- "It's technically legal" (law as ceiling, not floor)
- "Everyone else does it" (industry norms aren't ethics)
- "We'll fix it later" (technical debt for ethics)

### Having Ethics Conversations

**When you see something wrong:**

1. **Name the concern specifically**
   - Not "this feels wrong"
   - But "this feature could discriminate against X group because Y"

2. **Frame as business risk**
   - Not just "it's unethical"
   - But "this creates legal risk and reputational exposure"

3. **Propose alternatives**
   - Not just "we shouldn't do this"
   - But "we could achieve the same goal by..."

4. **Escalate appropriately**
   - Start with direct conversation
   - Document if needed
   - Use formal channels if concerns aren't addressed

### When to Walk Away

**Questions to ask:**
- Is this a one-time lapse or systemic pattern?
- Can I change things from the inside?
- Am I being complicit by staying?
- What's my personal ethical line?

There's no shame in leaving. Sometimes that's the most ethical act.

---

## Exercises

### Exercise 1: Stakeholder Analysis

For a product decision you're facing:

1. List all stakeholders (include future/indirect)
2. For each: What do they gain? What might they lose?
3. Whose interests are being prioritized? Deprioritized?
4. How would you rebalance?

**Time:** 30 minutes

### Exercise 2: Framework Application

Take an ethical dilemma (real or hypothetical):

1. Analyze from utilitarian perspective
2. Analyze from deontological perspective
3. Analyze from virtue ethics perspective
4. What does each suggest?
5. Where do they conflict?

**Time:** 45 minutes

### Exercise 3: Bias Audit

For an AI system you work with (or use):

1. What decisions does it make or influence?
2. What data was it likely trained on?
3. What groups might be underrepresented?
4. What proxies might introduce bias?
5. How would you test for fairness?

**Time:** 45 minutes

### Exercise 4: Regulatory Readiness

For your product or company:

1. What AI-powered features exist?
2. How would each be classified under EU AI Act?
3. What documentation would be required?
4. What gaps exist in current practices?

**Time:** 45 minutes

### Exercise 5: Ethical Pre-mortem

For an upcoming launch or feature:

1. Imagine it's one year later and things went terribly wrong
2. Write the negative news story
3. What happened? Who was harmed?
4. What warning signs existed?
5. What could prevent this?

**Time:** 30 minutes

### Exercise 6: Ethics Conversation

Think of an ethical concern you've observed but not raised:

1. Write out the specific concern
2. Frame it as business risk
3. Develop alternative approach
4. Practice the conversation (with trusted colleague)
5. Decide: Will you raise it?

**Time:** 45 minutes

---

## Checklist: Are You Ready?

- [ ] Articulate stakeholder vs shareholder perspectives
- [ ] Apply utilitarian, deontological, and virtue ethics frameworks
- [ ] Identify sources of bias in AI systems
- [ ] Explain key provisions of emerging AI regulations
- [ ] Design AI systems with fairness and transparency
- [ ] Balance short-term pressures with long-term ethics
- [ ] Have productive ethics conversations at work
- [ ] Know your personal ethical lines

---

## Key Frameworks Summary

| Framework | Use When | Core Insight |
|-----------|----------|--------------|
| Stakeholder Analysis | Balancing interests | Map who's affected and how |
| Ethical Frameworks | Making judgment calls | Utilitarian vs Deontological vs Virtue |
| Bias Sources | Auditing AI | Data, selection, measurement, algorithmic |
| Risk Classification | Regulatory compliance | Unacceptable → High → Limited → Minimal |
| Fairness Metrics | Evaluating AI | Demographic parity, equalized odds, calibration |

---

## Key Concepts Quick Reference

| Concept | Definition |
|---------|------------|
| Shareholder Primacy | Corporation exists to maximize shareholder value |
| Stakeholder Capitalism | Corporation serves multiple stakeholders |
| Utilitarianism | Maximize overall well-being |
| Deontology | Follow moral rules regardless of outcome |
| Virtue Ethics | Act as person of good character would |
| Algorithmic Bias | Systematic error creating unfair outcomes |
| Explainability | Ability to understand AI decisions |
| Human-in-the-loop | Human reviews AI decisions |

---

## Next Steps

1. **Read:** *Weapons of Math Destruction* by Cathy O'Neil — Compelling examples of how algorithms cause harm. Accessible, well-researched, eye-opening.

2. **Practice:** Exercise 3 (Bias Audit) on an AI system you interact with. Start seeing the world through this lens.

3. **Act:** Identify one ethical concern in your current work. Have the conversation.

---

*Congratulations on completing the MBA Essentials curriculum.*

---

## Curriculum Complete

You now have frameworks for:
1. **Finance** — Speaking CFO language, building business cases
2. **Communication** — Influencing executives, storytelling with data
3. **Strategy** — Making choices, understanding competitive dynamics
4. **Negotiation** — Getting to yes while protecting interests
5. **Leadership** — Motivating teams, navigating organizations
6. **Marketing** — Positioning, customer psychology, pricing
7. **Operations** — Bottlenecks, throughput, continuous improvement
8. **Ethics** — AI governance, responsible product decisions

**The journey continues:**
- Deep-dive books expand each topic
- Exercises build practical skill
- Real application cements learning

**Remember:** The goal isn't knowing frameworks—it's developing judgment. Frameworks are tools. Judgment comes from application.

Good luck.
