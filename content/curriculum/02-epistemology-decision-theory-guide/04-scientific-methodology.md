# Scientific Methodology & Philosophy of Science

## Overview

How does science generate reliable knowledge about the world? This chapter examines the philosophical foundations of scientific inquiry, from the problem of induction to the replication crisis, providing tools for evaluating scientific claims critically without falling into either credulity or cynicism.

Science isn't just a body of facts — it's a method for systematically investigating nature, testing hypotheses, and updating our understanding when evidence demands. But the philosophical foundations are debated. Can induction be justified? What makes a theory scientific? How should we interpret statistical significance? When should we trust scientific consensus?

This chapter covers the major philosophical frameworks (Popper's falsificationism, Kuhn's paradigm shifts, Lakatos's research programmes), the replication crisis revealing methodological failures, and practical tools for evaluating scientific claims.

## The Problem of Induction (Hume)

All empirical science depends on induction: observing patterns and projecting them into the future or unobserved cases.

- The sun has risen every day for billions of years → the sun will rise tomorrow
- All observed ravens are black → all ravens are black
- Aspirin has relieved headaches in thousands of trials → aspirin will relieve my headache
- Water boils at 100°C at sea level in all observations → water will boil at 100°C next time

This seems obviously justified. Yet David Hume (1711-1776) demonstrated that induction cannot be rationally justified.

### The Argument

**Question**: What justifies inferring from "All observed Fs have been G" to "The next F will be G" or "All Fs are G"?

**Attempted justifications**:

**1. Deductive logic?** No. The inference isn't deductively valid. It's logically possible that all observed ravens are black but the next raven is white. The premises (past observations) don't entail the conclusion (future will resemble past).

**2. Induction itself?** "Induction has worked in the past, so induction will work in the future." This is circular — you're using induction to justify induction.

**3. Probability?** "Past patterns make future patterns probable." But probability theory itself presupposes that past frequencies predict future frequencies. This is the very assumption we're trying to justify.

**Hume's conclusion**: Induction is not rationally justified. It's a **psychological habit** ("custom"), not a logical principle. We can't help but form inductive expectations, but this doesn't make them rational.

### Implications

If Hume is right, **all empirical science rests on an unjustifiable foundation**. Every scientific law (gravity, thermodynamics, evolution) is an inductive generalization. Every experimental prediction assumes future will resemble past. Yet this assumption cannot be rationally defended.

**Responses**:

**Pragmatism** (Reichenbach): Induction works. If any method can predict the future, induction can. We're pragmatically justified in using it even if not logically justified.

**Critique**: "It works" is itself an inductive claim (it's worked in the past → it will work in the future).

**Bayesian**: We have prior probabilities over hypotheses. Observations update these via Bayes' theorem. This doesn't require assuming uniformity of nature, just having priors.

**Critique**: Where do priors come from? Ultimately, from past experience (induction) or arbitrary choice (subjective).

**Popper**: Science doesn't use induction — it uses **falsification**. We propose conjectures and try to refute them. Theories that survive severe tests are "corroborated" (not confirmed).

### Goodman's New Riddle of Induction

Nelson Goodman (1955) deepened the problem. Define "grue": an object is grue if observed before time T and green, or not observed before T and blue.

All emeralds observed before time T are green. Therefore:
- Induction 1: All emeralds are green
- Induction 2: All emeralds are grue (so after T, unobserved emeralds will be blue)

Both generalizations fit the data perfectly. Induction seems to require privileging "natural" properties (green) over "artificial" ones (grue). But what makes a property "natural"? This reintroduces the problem of justifying inductive practice.

**Practical lesson**: We can't escape induction in science or everyday life. But recognizing its philosophical vulnerability encourages epistemic humility and openness to evidence that contradicts established patterns.

## Falsificationism (Popper)

Karl Popper (1902-1994) proposed a solution to the problem of induction: science doesn't confirm theories; it **falsifies** them.

### The Core Idea

Science progresses not by accumulating confirming observations but by proposing **bold conjectures** and subjecting them to **severe tests** designed to falsify them. Theories that survive are "corroborated" (provisionally accepted), not proven.

### Demarcation Criterion

**A theory is scientific if and only if it is falsifiable** — it makes risky predictions that could be proven wrong by possible observations.

| Theory/Claim | Falsifiable? | Scientific? |
|-------------|-------------|-------------|
| "All swans are white" | Yes (one black swan falsifies) | Yes |
| "E = mc²" | Yes (failed experiments would falsify) | Yes |
| "Massive objects bend light" | Yes (eclipse observations could falsify) | Yes |
| "God works in mysterious ways" | No (compatible with any observation) | No |
| "The stock market will go up or down" | No (can't be wrong) | No |
| Freudian psychoanalysis | No (explains any behavior post hoc) | No |
| Astrology | No (predictions vague enough to fit anything) | No |

**Einstein's 1919 eclipse prediction**: General relativity predicted starlight would bend by a specific amount near the sun (1.75 arcseconds). Newtonian physics predicted a different amount (0.87 arcseconds). Eddington's eclipse measurements matched Einstein's prediction. The theory was corroborated because it took a real risk of falsification.

### Asymmetry of Verification and Falsification

- **Confirming observations** don't prove a universal theory (no matter how many white swans you've seen, the next could be black)
- **One disconfirming observation** can falsify a universal theory (one black swan proves "all swans are white" is false)

This asymmetry means science can't prove theories true, but can prove them false.

### Bold Conjectures and Severe Tests

Good science proposes **bold conjectures** — theories that make risky, precise, novel predictions — and subjects them to **severe tests** — experiments designed to falsify, not confirm.

**Bad**: "This drug has some effect on patients." (Vague, hard to falsify, low information content)
**Good**: "This drug reduces systolic blood pressure by 10-15 mmHg in hypertensive patients within 4 weeks." (Specific, falsifiable, informative)

Theories that survive severe tests are "corroborated" — we provisionally accept them, not because they're proven, but because they've passed hard tests.

### Criticisms of Popper

**1. Duhem-Quine Thesis**: No hypothesis is tested in isolation. Experiments test a "bundle" of hypotheses (the main theory + auxiliary assumptions + background theories + instrument reliability).

Example: We predict Neptune's orbit using Newton's gravity. Observations don't match. Does this falsify Newton's gravity? Or is the discrepancy due to:
- An unknown planet (Uranus)? (What actually happened — led to discovering Neptune)
- Instrument error?
- Incorrect auxiliary assumptions?

The Duhem-Quine thesis says **any** hypothesis can be saved by rejecting auxiliary assumptions. Falsification is never definitive.

**Popper's response**: Scientists have methodological rules — prefer simpler theories, don't make ad hoc modifications just to save a theory. But this reintroduces subjectivity.

**2. Probabilistic Theories**: Quantum mechanics, statistical mechanics, evolutionary biology make **probabilistic** predictions. A low-probability outcome doesn't strictly falsify the theory — it might be the unlikely case.

Example: QM predicts particle has 90% chance of being detected at position A. It's detected at position B (10% probability). Does this falsify QM? No — the theory predicted a 10% chance of this. But if you see B 90% of the time, you'd reject QM. Where do you draw the line?

**3. Confirmation Matters**: Scientists do consider confirming evidence, not just falsification. A theory explaining 100 disparate phenomena is stronger than one explaining 3, even if both are unfalsified.

**4. Normal Science**: Kuhn argued most science is "normal science" — puzzle-solving within an accepted paradigm, not bold conjecture and risky tests.

## Paradigm Shifts (Kuhn)

Thomas Kuhn's *The Structure of Scientific Revolutions* (1962) challenged the Popperian view. Kuhn argued science alternates between periods of "normal science" and "revolutionary science."

### Normal Science

**Paradigm**: A shared framework of concepts, methods, standards, and exemplary problem-solutions that defines a scientific community.

Examples:
- Newtonian mechanics (1687-1905)
- Dalton's atomic theory (1803-present, refined)
- Darwinian evolution (1859-present, refined)
- Plate tectonics (1960s-present)

During normal science:
- **Puzzle-solving**: Scientists work within the paradigm, solving "puzzles" — applying the paradigm to new cases
- **Anomalies tolerated**: Observations that don't quite fit are noted but explained away as measurement error, experimental artifacts, or future puzzles to solve
- **Textbook science**: Students learn the paradigm through exemplars (classic solved problems), not by questioning foundations

Normal science is **conservative** and **dogmatic**. This isn't a flaw — it's a feature. Deep investigation of a paradigm requires commitment, not constant skepticism.

### Crisis

Anomalies accumulate. Some prove resistant to solution despite intense effort. The paradigm increasingly fails to solve important problems. **Confidence erodes**.

Examples:
- Mercury's orbit anomaly for Newtonian mechanics (1859-1915)
- Ultraviolet catastrophe for classical thermodynamics (1900)
- Fossil gaps and variation patterns for fixity of species (1800s)

During crisis:
- Extraordinary research: Ad hoc modifications, exploring alternatives
- Philosophical debates: Questioning foundations
- Loss of confidence: Younger scientists more willing to abandon paradigm

### Scientific Revolution

A new paradigm emerges that resolves the anomalies. The scientific community undergoes a **paradigm shift** — allegiance transfers from old to new.

**Revolutionary shifts**:

| Old Paradigm | New Paradigm | Key Figure(s) | Dates | Anomaly Resolved |
|-------------|-------------|--------------|-------|------------------|
| Ptolemaic (geocentric) astronomy | Copernican (heliocentric) | Copernicus, Galileo, Kepler | 1543-1687 | Planetary retrograde motion, phase of Venus |
| Phlogiston theory of combustion | Oxygen theory | Lavoisier | 1770s-1780s | Weight gain in combustion |
| Caloric (fluid) theory of heat | Kinetic (motion) theory | Joule, Boltzmann, Maxwell | 1840s-1870s | Mechanical equivalent of heat |
| Newtonian mechanics | Einsteinian relativity | Einstein | 1905-1915 | Mercury's orbit, Michelson-Morley null result |
| Classical mechanics | Quantum mechanics | Planck, Bohr, Heisenberg | 1900-1927 | Blackbody radiation, atomic spectra |
| Fixity of species | Evolution by natural selection | Darwin, Wallace | 1859 | Fossil record, biogeography, variation |
| Classical genetics | Molecular genetics | Watson, Crick, Franklin | 1953 | Mechanism of heredity |
| Static continents | Plate tectonics | Wegener, Hess | 1960s | Continental fit, seafloor spreading |

### Incommensurability

Kuhn's most controversial claim: Old and new paradigms may be **incommensurable** — they use different concepts, standards, and methods. They're not directly comparable, so paradigm choice isn't purely rational.

**Example**: Newtonian "mass" is an intrinsic property. Einsteinian "mass" depends on reference frame (rest mass vs relativistic mass). Are they talking about the same thing?

Kuhn: Paradigms are like different languages or worlds. Scientists on opposite sides of a revolution "live in different worlds," even while looking at the same observations.

**Implications**:
- No neutral observation language (observations are theory-laden)
- No neutral standards for comparison (standards are paradigm-internal)
- Paradigm choice involves non-rational factors: aesthetics, values, sociology

**Criticism**: Kuhn overstates incommensurability. Scientists can and do compare paradigms rationally (Lakatos, Laudan). Scientific progress is real, not just paradigm replacement. There are paradigm-independent virtues: empirical adequacy, consistency, scope, simplicity.

### Kuhn vs Popper

| | Popper | Kuhn |
|--|--------|------|
| **Scientific progress** | Conjecture and refutation | Paradigm shifts |
| **Typical science** | Bold conjectures, severe tests | Normal science (puzzle-solving) |
| **Falsification** | Central | Rare; anomalies tolerated during normal science |
| **Rationality** | Objective methodological rules | Partly social, aesthetic, non-rational |
| **Scientific revolutions** | Gradual, continuous | Discontinuous, revolutionary |
| **Comparison of theories** | Possible (via falsification) | Difficult (incommensurability) |

**Kuhn's insight**: Science is sociologically and psychologically complex. Paradigms are resilient (not abandoned at first anomaly). Revolutionary science is rare; normal science is typical.

**Popper's insight**: Demarcation (scientific vs non-scientific) matters. Falsifiability is a useful criterion. Science should seek bold conjectures, not just puzzle-solving.

## Research Programmes (Lakatos)

Imre Lakatos (1922-1974) attempted to reconcile Popper and Kuhn. His **methodology of scientific research programmes** captures how real science works.

### Structure of a Research Programme

**1. Hard Core**: Central theoretical commitments, treated as **unfalsifiable by methodological decision**. If empirical evidence conflicts, you don't reject the hard core.

Examples:
- Newtonian programme: F = ma, law of gravity
- Darwinian programme: Descent with modification, natural selection
- Atomic programme: Matter composed of atoms

**2. Protective Belt**: Auxiliary hypotheses, initial conditions, observational theories, instrument theories. These absorb the impact of anomalies — they're modified, rejected, or replaced to protect the hard core.

Example (Newtonian):
- Hard core: Newton's laws
- Protective belt: Assumptions about planetary masses, absence of other bodies, instrument calibrations
- Anomaly: Uranus's orbit doesn't match predictions
- Response: Modify protective belt (posit unknown planet) → discover Neptune. Hard core protected.

**3. Positive Heuristic**: Research direction — what problems to pursue, what modifications to try, what predictions to seek.

Example (Darwinian):
- Apply natural selection to explain: adaptation, speciation, extinction, biogeography
- Look for: fossils, variation within populations, mechanisms of inheritance

**4. Negative Heuristic**: Directive to **not** subject the hard core to empirical testing. Protect it via auxiliary modifications.

### Progressive vs Degenerating Research Programmes

**Progressive**:
- Generates **novel predictions** (not just explaining known facts)
- Some predictions are **confirmed**
- Expands **scope** (explains more phenomena)

**Degenerating**:
- Makes only **ad hoc modifications** to accommodate anomalies
- No novel predictions, or predictions are disconfirmed
- Contracts scope, loses explanatory power

**Examples**:

**Newtonian mechanics** (progressive 1687-1900):
- Novel prediction: Return of Halley's comet (1758)
- Novel prediction: Neptune's existence (1846)
- Expanding scope: Celestial mechanics → terrestrial mechanics → thermodynamics

**Newtonian mechanics** (degenerating 1900-1920):
- Ad hoc modifications to save Mercury's orbit
- Failure to explain blackbody radiation, photoelectric effect
- Eventually replaced by Einstein's relativity and quantum mechanics

**Ptolemaic astronomy** (degenerating 1500s):
- Increasingly complex epicycles to fit observations
- No novel predictions
- Copernican system simpler, eventually more accurate

**Lakatos's lesson**: Evaluate research programmes over time, not individual theories at a moment. Don't abandon a programme at the first anomaly — see if it can progressively solve problems. But if a programme is degenerating (only ad hoc modifications, no novel success), consider alternatives.

## The Replication Crisis

Since ~2010, systematic attempts to replicate landmark findings have revealed **widespread failure to reproduce** published research.

### Replication Rates by Field

| Field | Replication Rate | Key Study |
|-------|-----------------|-----------|
| **Psychology** | 36-39% | Open Science Collaboration (2015): 97 studies from top journals, 36% replicated |
| **Cancer biology** | 11-25% | Begley & Ellis (2012): 6/53 landmark studies replicated; Errington et al. (2021): ongoing |
| **Preclinical medicine** | 11-25% | Prinz et al. (2011): 6/53 studies replicated |
| **Economics** | 61% | Camerer et al. (2016): 11/18 studies replicated |
| **Social sciences (general)** | ~50% | SCORE project: 16/21 replicated |

**Nature survey** (2016): 70% of researchers have failed to reproduce another scientist's experiment, 50% have failed to reproduce their own.

The **replication crisis** reveals that a substantial fraction — possibly majority — of published findings are false positives or inflated effect sizes.

### Causes

#### 1. P-Hacking (Data Dredging, Researcher Degrees of Freedom)

**Definition**: Running multiple analyses (trying different subgroups, excluding outliers, adding covariates, testing multiple outcomes) and reporting only those that achieve p < 0.05.

**Mechanism**: With α = 0.05, you expect 1 false positive out of 20 tests purely by chance. If you run 20 tests and report the one "significant" result, you're capitalizing on random noise.

**Simmons, Nelson, Simonsohn (2011)**: Showed that "researcher degrees of freedom" allow finding p < 0.05 for basically any hypothesis. They demonstrated (with p < 0.05!) that listening to "When I'm Sixty-Four" makes people younger.

**How common**: Incredibly common. John et al. (2012): surveyed 2,000 psychologists:
- 63% admitted to collecting data until p < 0.05
- 56% admitted to choosing which dependent variables to report post-hoc
- 58% admitted to "creative" exclusion of data

#### 2. Publication Bias (File Drawer Problem)

**Definition**: Journals prefer positive, statistically significant results. Negative results (no effect found) are filed away, never published.

**Consequence**: The published literature is a biased sample. If 20 teams independently test a false hypothesis (no effect exists), we expect 1 to find p < 0.05 by chance. That 1 study gets published. The 19 null results languish in file drawers. The literature falsely suggests the effect exists.

**Rosenthal's file drawer problem** (1979): If published studies show a small but significant effect, how many unpublished null studies would be needed to nullify the finding? Often the answer is surprisingly small.

**Evidence**:
- Funnel plot asymmetry: Studies with small samples (high noise) show more variation but are biased toward positive results (should be symmetric if no publication bias)
- Decline effect: Initial studies show large effects; later replications show smaller effects (regression to the mean + publication bias for exciting early results)

#### 3. HARKing (Hypothesizing After Results are Known)

**Definition**: Conducting exploratory analysis, finding an unexpected pattern, then writing the paper as if you predicted it a priori (confirmatory analysis).

**Why problematic**: Exploratory analysis has many more researcher degrees of freedom. Hypothesizing post hoc capitalizes on noise. Presenting it as confirmatory misleads readers about the evidential strength.

**Solution**: **Pre-registration** — declare hypotheses and analysis plan before seeing data.

#### 4. Low Statistical Power

**Power**: The probability of detecting an effect that actually exists. Depends on sample size, effect size, and α-level.

Many studies are **underpowered** (power < 0.5 means less than 50% chance of detecting a real effect).

**Button et al. (2013)**: Median power in neuroscience was ~21%. Most true effects went undetected.

**Consequence**:
- **Many false negatives** (miss real effects)
- **Winner's curse**: When an underpowered study does find a "significant" result, it's likely to have overestimated the effect size (selected the lucky high outlier)

#### 5. Perverse Incentives

**Publish or perish**: Academics need publications for jobs, tenure, promotion, funding. This rewards:
- Quantity over quality
- Positive results over null results
- Novel, "sexy" findings over replications

**Media attention**: Surprising, counterintuitive findings get press coverage, boosting career. Boring replications don't.

**Grant funding**: Need preliminary data showing effects to get funded. Null results don't attract funding.

**Result**: System incentivizes questionable research practices, not rigorous science.

### Solutions: Open Science Movement

| Reform | How It Helps | Adoption |
|--------|-------------|----------|
| **Pre-registration** | Declare hypotheses and analyses before seeing data → prevents p-hacking and HARKing | Growing; required by some journals (e.g., *Cortex*, *Comprehensive Results in Social Psychology*) |
| **Registered reports** | Peer review before data collection; publication guaranteed regardless of results → removes publication bias | ~300 journals now offer; still <5% of published articles |
| **Open data** | Share raw data publicly → allows reanalysis, checking for errors | Increasing; required by some funders (NSF, NIH), some journals |
| **Open materials** | Share experimental protocols, stimuli, code → enables replication | Increasing; platforms like OSF (Open Science Framework) |
| **Replication studies** | Directly test prior findings → establishes which results are robust | Rare; not incentivized; Replication journals exist but marginal |
| **Multi-site collaboration** | Same study run at multiple labs simultaneously → more power, less idiosyncrasy | Growing (e.g., ManyLabs, Psych Science Accelerator) |
| **Pre-prints** | Post manuscripts before peer review → faster dissemination, reduced publication bias | Standard in physics/math (arXiv); growing in bio (bioRxiv), psych (PsyArXiv) |
| **Blinding** | Analysts don't know which condition is which until after analysis → prevents motivated analysis | Rare outside RCTs; hard to implement |

**Resistance**:
- Cultural inertia (established researchers benefited from old system)
- Career costs (pre-registration takes time; replications don't get credit)
- Practical barriers (sharing data is work; not all data can be shared due to privacy)

**Progress**: Younger scientists more enthusiastic. Funders increasingly mandate open data. Journals increasingly adopt reforms.

## Statistical Significance and P-Values

### What P-Values Mean

The p-value is **the probability of observing data at least as extreme as what was observed, assuming the null hypothesis is true**.

```
p = P(data ≥ observed | H₀ true)
```

**NOT**:
- ❌ P(H₀ true | data)
- ❌ Probability the result is a fluke
- ❌ Probability the result will replicate
- ❌ 1 - p ≠ probability the result is real

### The Ritual of p < 0.05

**Ronald Fisher** (1925) suggested p = 0.05 as a rough guideline for "worth another look." It was never intended as a bright line.

**Neyman-Pearson** (1933) formalized hypothesis testing with Type I error (α = 0.05) and Type II error (β, power = 1-β).

**Modern practice**: p < 0.05 became a **dichotomous decision rule**: p < 0.05 → "significant" → publish, celebrate. p > 0.05 → "not significant" → file drawer.

**Problems**:
- **Arbitrary threshold**: Why 0.05 and not 0.049 or 0.051? The difference between p = 0.049 (significant!) and p = 0.051 (not significant) is trivial, yet treated as qualitatively different.
- **Ignores effect size**: With large samples, tiny, trivial effects become "significant." Statistical significance ≠ practical significance.
- **Ignores prior probability**: p-values don't tell you P(hypothesis true). They ignore base rates (Bayesian critique).

### Confidence Intervals

A 95% confidence interval (CI) means: **If you repeated the study many times, 95% of the resulting intervals would contain the true parameter value**.

**NOT**: "There's a 95% probability the true value is in this interval" (that's a Bayesian credible interval).

**Why CIs are better than p-values**:
- Show effect size and precision
- Indicate practical significance (Is the lower bound of the CI still a meaningful effect?)
- More informative (a p-value just says "surprising if H₀ true"; CI says "plausible range of values")

### Effect Sizes

**Cohen's d**: Standardized mean difference.
```
d = (mean₁ - mean₂) / pooled standard deviation
```

Interpretation:
- d = 0.2: Small effect
- d = 0.5: Medium effect
- d = 0.8: Large effect

**Correlation r**: Effect size for associations.
- r = 0.1: Small
- r = 0.3: Medium
- r = 0.5: Large

**Why effect sizes matter**: With n = 10,000, a correlation of r = 0.05 (tiny, trivial) is "statistically significant" (p < 0.001). The effect is real but useless. Focusing on effect sizes prevents conflating statistical significance with practical importance.

**Recommended practice** (Cumming, 2014): Report:
1. Effect size (e.g., Cohen's d)
2. Confidence interval (e.g., 95% CI)
3. p-value (optional, less important)

Example: "The treatment increased test scores by 0.3 SD (Cohen's d = 0.30, 95% CI [0.15, 0.45], p = 0.003)."

## Scientific Consensus

How does scientific consensus form, and when should we trust it?

### How Consensus Forms

- **Multiple independent lines of evidence** converging on a conclusion
- **Replication** across labs, methods, populations
- **Survival of attempts at falsification** (Popperian tests)
- **Peer review and criticism** by qualified experts
- **Integration with broader knowledge** (consistency with related fields)

**Example: Evolution by natural selection**

Evidence from:
- Fossil record (transitional forms, stratigraphic patterns)
- Comparative anatomy (homologous structures)
- Embryology (developmental similarities)
- Biogeography (species distribution patterns)
- Molecular biology (DNA sequence similarities)
- Direct observation (bacteria evolving resistance, rapid evolution in labs)

Consensus: ~97% of biologists accept evolution.

### When to Defer to Consensus

**Strong consensus** (>90% agreement among relevant experts) based on extensive, replicated evidence:

- Climate change is anthropogenic (97% of climate scientists)
- Vaccines don't cause autism (overwhelming consensus, dozens of large studies)
- Evolution by natural selection occurs (97% of biologists)
- Smoking causes cancer (universal consensus, decades of evidence)

**Rationale for deference**:
- Experts have specialized knowledge
- Collective expertise aggregates evidence you can't personally evaluate
- Base rate: Expert consensus is rarely overturned

**When not to defer**:
- **Weak or split consensus** (field divided 60-40)
- **Conflict of interest** (tobacco industry scientists on smoking)
- **Poor track record** (field with low replication rates)
- **Young field** with limited evidence
- **Politicized topic** where motivated reasoning likely

### When Consensus is Overturned

**Rare but notable examples**:

| Consensus | Overturned By | Year |
|-----------|--------------|------|
| Stomach ulcers caused by stress/diet | H. pylori bacteria (Marshall & Warren) | 1980s |
| Continental fixity | Plate tectonics | 1960s |
| Newtonian mechanics (absolute space/time) | Einstein's relativity | 1905-1915 |
| Phlogiston theory | Oxygen theory (Lavoisier) | 1770s |

**Common features**:
- New technology enabling novel observations (microscopes, seismology, precise clocks)
- Cumulative anomalies that old paradigm couldn't explain
- New paradigm explains anomalies + retains old successes

**Lesson**: Consensus can be wrong, but the base rate of overturning established consensus is low. Extraordinary claims (consensus is wrong) require extraordinary evidence.

## Pseudoscience: Red Flags

| Red Flag | Description | Example |
|----------|-------------|---------|
| **Unfalsifiable** | No possible evidence could disprove it; claims are vague or post-hoc | "It works through energy fields undetectable by instruments"; "If it didn't work, you didn't believe hard enough" |
| **No mechanism** | No plausible causal explanation for how it could work | Homeopathy (water "remembers" substance that's been diluted to nothing — violates chemistry) |
| **Violation of well-established science** | Contradicts core theories (thermodynamics, physics) without explaining how | Perpetual motion machines (violate conservation of energy) |
| **Cherry-picking** | Cites only favorable evidence; ignores contrary evidence | Anti-vaccine citing Wakefield study (retracted, fraudulent), ignoring dozens of large studies finding no link |
| **Ad hoc immunization** | Modifying claims after each refutation to evade disconfirmation | Astrology: "Mercury was in retrograde when I made that prediction, so it doesn't count" |
| **Anecdotal evidence** | Relying on testimonials rather than controlled studies | "My cousin's friend took this supplement and felt better!" (ignores placebo, regression to mean, selection bias) |
| **Appeal to authority** | Citing credentials or degrees rather than evidence | "As a doctor, I believe..." (credentials ≠ evidence) |
| **Conspiracy** | Claiming mainstream science is suppressing the truth | "Big Pharma is hiding the cure for cancer" (assumes massive conspiracy with no leaks) |
| **Lack of progress** | No advancement in understanding or predictive power over decades | Psychoanalysis (unfalsifiable, no progress in 100 years) |
| **Scientific-sounding jargon** without substance | Using technical language to sound credible without coherent theory | "Quantum healing" (quantum mechanics has nothing to do with healing) |

**Example: Homeopathy**

- **Claim**: Diluting a substance makes it more potent; water "remembers" the substance.
- **Mechanism**: None consistent with chemistry/physics. At 30C dilution (standard), probability of a single molecule remaining is ~10^-60.
- **Evidence**: Meta-analyses (Shang et al., 2005; NHMRC 2015) find no effects beyond placebo.
- **Unfalsifiable**: Practitioners claim it works for "constitutional types" — vague, post-hoc matching.
- **Verdict**: Pseudoscience.

**Example: Intelligent Design**

- **Claim**: Biological complexity is too great to have evolved; must be designed.
- **Unfalsifiable**: No way to test for a designer; any outcome is compatible ("The designer works in mysterious ways").
- **Ad hoc**: "Irreducible complexity" — claims system can't function without all parts. When evolutionary pathways are shown, ID proponents claim those parts are themselves irreducibly complex. (Moving goalposts.)
- **Lack of progress**: No research program, no novel predictions, no discoveries attributable to ID.
- **Verdict**: Pseudoscience (or religion dressed as science).

## Key Terms

- **Problem of Induction**: Inductive inferences can't be rationally justified (Hume); all empirical science depends on unjustifiable assumption
- **Falsifiability**: A theory is scientific iff it makes predictions that could be proven wrong (Popper)
- **Demarcation Criterion**: Boundary between science and non-science; Popper's criterion is falsifiability
- **Corroboration**: A theory is corroborated if it survives severe tests; not proven, just not-yet-falsified
- **Duhem-Quine Thesis**: No hypothesis is tested in isolation; auxiliary assumptions can always absorb anomalies
- **Paradigm**: Shared framework of concepts, methods, and exemplars defining a scientific community (Kuhn)
- **Normal Science**: Puzzle-solving within an accepted paradigm (Kuhn)
- **Scientific Revolution**: Paradigm shift; allegiance transfers from old to new framework (Kuhn)
- **Incommensurability**: Paradigms may use different concepts, making direct comparison difficult (Kuhn)
- **Research Programme**: Hard core (unfalsifiable commitments) + protective belt (modifiable auxiliaries) + heuristics (Lakatos)
- **Progressive Programme**: Generates confirmed novel predictions; expands scope
- **Degenerating Programme**: Only ad hoc modifications; no novel success; contracts scope
- **Replication Crisis**: Widespread failure to reproduce published findings; reveals methodological failures
- **P-hacking**: Running multiple analyses, reporting only significant ones; capitalizes on noise
- **Publication Bias**: Journals prefer positive results; null results filed away (file drawer problem)
- **HARKing**: Hypothesizing After Results are Known; exploratory analysis presented as confirmatory
- **Pre-registration**: Declaring hypotheses and analyses before data collection; prevents p-hacking
- **Registered Reports**: Peer review before data collection; publication guaranteed regardless of results
- **P-value**: P(data ≥ observed | H₀ true); NOT P(H₀ true | data)
- **Effect Size**: Magnitude of effect (Cohen's d, correlation r); independent of sample size
- **Confidence Interval**: Range of values; 95% of such intervals contain true parameter (not 95% probability)
- **Scientific Consensus**: Agreement among experts based on extensive converging evidence

## Summary

Science generates knowledge through systematic investigation and testing, but philosophical foundations are debated. Hume's problem of induction reveals that empirical science rests on an unjustifiable assumption (future resembles past). No solution is fully satisfying, yet science proceeds because induction works pragmatically.

Popper's falsificationism proposes that science progresses by falsifying theories, not confirming them. Falsifiability demarcates science from non-science. Bold conjectures subjected to severe tests are corroborated if they survive. But the Duhem-Quine thesis shows falsification is never definitive — auxiliary assumptions can absorb anomalies. Probabilistic theories can't be strictly falsified.

Kuhn's paradigm shifts describe science as alternating between normal science (puzzle-solving within accepted framework) and revolutions (paradigm replacement). Paradigms may be incommensurable, making theory choice partly non-rational. Lakatos's research programmes bridge Popper and Kuhn: core theories protected by auxiliary belts; progressive programmes generate novel confirmed predictions; degenerating programmes make only ad hoc modifications.

The replication crisis (2010s-present) revealed that many published findings don't replicate. Causes: p-hacking (researcher degrees of freedom), publication bias (file drawer problem), HARKing (exploratory results presented as confirmatory), low power (underpowered studies overestimate effects), and perverse incentives (publish or perish). Solutions include pre-registration, registered reports, open data, open materials, and replication studies. Adoption is growing but faces cultural and practical barriers.

P-values are widely misunderstood. p < 0.05 is an arbitrary threshold; it doesn't tell you P(hypothesis true). Effect sizes and confidence intervals are more informative. Scientific consensus forms through multiple independent lines of evidence, replication, and survival of falsification attempts. Strong consensus based on extensive evidence warrants deference, but consensus can be wrong (plate tectonics, ulcers from bacteria).

Pseudoscience exhibits red flags: unfalsifiability, lack of mechanism, cherry-picking evidence, ad hoc modifications, anecdotal evidence, appeals to authority, conspiracy claims, lack of progress. Homeopathy and intelligent design exemplify pseudoscience.

The practical lesson: Science is the best tool we have for understanding the world, but it's fallible. Critical evaluation requires understanding its methods and limitations. Trust strong consensus based on extensive replicated evidence, but maintain epistemic humility. Extraordinary claims require extraordinary evidence. And when evaluating individual studies, check for pre-registration, effect sizes, replication, and potential for p-hacking or publication bias.
