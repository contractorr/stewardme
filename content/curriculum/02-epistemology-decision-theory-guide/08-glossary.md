# Glossary

This comprehensive glossary covers key terms, formulas, cognitive biases, and major thinkers from epistemology, decision theory, causal inference, game theory, and forecasting. Terms are organized alphabetically with cross-references where appropriate.

## A-Z Terms

**Actively Open-Minded Thinking (AOT)**: Willingness to genuinely consider evidence against one's views and update beliefs accordingly. Key trait of superforecasters. Measured by scales assessing receptivity to contrary evidence, cognitive flexibility, and willingness to change one's mind.

**Affect Heuristic**: Using feelings ("Do I like/fear this?") as information about probability and risk. Nuclear power feels scary → judged as high risk despite statistics. Slovic's research showed affect (good/bad feeling) dominates statistical reasoning for most people.

**Anchoring**: Disproportionate influence of initial numerical values on subsequent judgments, even when anchors are arbitrary or irrelevant. Spinning a wheel showing 10 vs 65 changes estimates of African UN membership by ~20 percentage points. Robust even among experts and when people are warned.

**Arrow's Impossibility Theorem**: Kenneth Arrow's proof (1951) that no voting system with ≥3 options can simultaneously satisfy all fairness criteria (unrestricted domain, non-dictatorship, Pareto efficiency, independence of irrelevant alternatives). Foundational result in social choice theory.

**Average Treatment Effect (ATE)**: Expected difference E[Y₁ - Y₀] between treatment and control outcomes across the entire population. Differs from ATT (average treatment effect on the treated) and ATU (average treatment effect on the untreated) when treatment effects are heterogeneous.

**Availability Heuristic**: Judging frequency or probability by ease of recalling instances. Homicide feels more common than diabetes deaths because murders are memorable/reported, diabetes deaths are not. Media coverage massively distorts availability.

**Backward Induction**: Solving sequential games by reasoning from end to beginning. Determine last player's optimal move, then second-to-last player's optimal move knowing the last, etc. Foundational for subgame perfect equilibrium.

**Bargaining Power**: Determined by BATNA (Best Alternative To Negotiated Agreement) or disagreement payoff. Better outside option → higher share of surplus. Nash bargaining solution formalizes this.

**Base Rate**: Prior probability of a condition in the population before considering specific evidence. Essential for Bayesian updating. Often neglected (base rate neglect).

**Base Rate Neglect**: Ignoring prior probabilities when interpreting evidence. Focusing on P(test+ | disease) while ignoring P(disease), leading to wildly miscalibrated posterior probabilities. Major source of medical misdiagnosis.

**Bayes' Theorem**: Fundamental formula for updating beliefs with evidence.
```
P(H|E) = P(E|H) × P(H) / P(E)
```
Where P(H) = prior, P(E|H) = likelihood, P(H|E) = posterior, P(E) = marginal likelihood. The mathematically optimal way to combine prior knowledge with new data.

**Bayesian**: Interpreting probability as degree of belief or credence rather than long-run frequency. Bayesian statistics uses prior distributions and Bayes' theorem to update beliefs. Contrasts with frequentist interpretation.

**Bayesian Game**: Game with incomplete information where players have types (private information) and beliefs (probability distributions over others' types). Bayesian Nash equilibrium is the solution concept.

**Bayesian Nash Equilibrium**: In Bayesian games, a strategy profile where each player's strategy is a best response given their type and beliefs about other players' types.

**Berkson's Paradox**: Spurious negative correlation created by conditioning on a collider. Disease and toxic exposure both cause hospitalization → among hospitalized patients, disease and exposure appear negatively correlated even though they're independent in the general population.

**Bounded Rationality**: Herbert Simon's concept (Nobel 1978) that rationality is limited by information, cognitive capacity, and time. Leads to satisficing (choosing "good enough") rather than optimizing. Heuristics are adaptive responses to these bounds.

**Brier Score**: Mean squared error of probabilistic predictions: (1/N) Σ (pᵢ - oᵢ)². Range 0 (perfect) to 2 (worst). Score of 0.20 is good; 0.10 is excellent (superforecaster level). Decomposes into calibration, resolution, and uncertainty components.

**Calibration**: Match between stated confidence levels and actual accuracy frequencies. Perfectly calibrated: when you say 70%, you're right 70% of time. Most people overconfident (say 90%, right 75%).

**Causal Inference**: Methods for establishing cause-effect relationships from data. Includes RCTs (gold standard), instrumental variables, regression discontinuity, difference-in-differences, and structural causal models (DAGs).

**Collider**: Variable caused by two others (X → Z ← Y). Conditioning on a collider creates spurious association between X and Y even when they're independent. Example: Beauty and talent both cause being an actor → among actors, beauty and talent are negatively correlated (either suffices).

**Common Knowledge**: Everyone knows X, everyone knows that everyone knows X, everyone knows that everyone knows that everyone knows X, ad infinitum. Essential for coordination. Bank runs occur when solvency isn't common knowledge even if privately known.

**Conditional Probability**: P(A|B) — probability of A given that B has occurred. Foundation of Bayesian updating. Related to joint probability: P(A|B) = P(A and B) / P(B).

**Confidence Interval**: Frequentist: "95% of such intervals (in repeated sampling) contain the true parameter." NOT "95% probability the parameter is in this interval" (that's a Bayesian credible interval). Widely misinterpreted.

**Confirmation Bias**: Seeking, interpreting, and recalling information that confirms existing beliefs while ignoring or dismissing disconfirming evidence. Robust across domains and intelligence levels. Wason 2-4-6 task demonstrates it powerfully.

**Confounding**: Third variable Z causing both treatment X and outcome Y, creating spurious association. Ice cream sales and drowning correlate because summer causes both. Control for confounders to isolate causal effects (if backdoor criterion satisfied).

**Conjunction Fallacy**: Judging P(A and B) > P(A), violating probability axioms. Linda problem: "bank teller and feminist" judged more probable than "bank teller" because description is representative of feminists. System 1 overrides logical System 2.

**Corroboration**: Popper's term for theories that survive severe tests. Not confirmation (which implies induction), but provisional acceptance because the theory has withstood attempts at falsification. Degrees of corroboration reflect severity of tests survived.

**Counterfactual**: What would have happened if a different action had been taken. Y₀ = outcome without treatment (unobservable). Fundamental to causal inference. The fundamental problem: can't observe both Y₁ and Y₀ for same unit.

**Credible Interval**: Bayesian analog of confidence interval. "95% probability (given the data and prior) that the parameter is in this interval." More intuitive than frequentist confidence intervals but requires specifying a prior.

**Cromwell's Rule**: Never assign probability exactly 0 or 1 to empirical claims. Once P(H) = 0 or 1, no evidence can change it (Bayesian updating fails). Reserve 0 and 1 for logical truths/contradictions only.

**DAG (Directed Acyclic Graph)**: Visual representation of causal relationships. Nodes = variables, arrows = direct causal effects. No cycles (acyclic). Pearl's framework uses DAGs to identify when causal effects can be estimated from observational data (backdoor criterion, front-door criterion).

**Decision Theory**: Formal study of rational choice under uncertainty. Three branches: normative (how should perfectly rational agents decide?), descriptive (how do humans actually decide?), prescriptive (how can real decisions improve?).

**Demarcation Problem**: Popper's question: what distinguishes science from non-science? Popper's answer: falsifiability. Science makes risky predictions that could be proven wrong. Pseudoscience is unfalsifiable (compatible with any observation).

**Difference-in-Differences (DiD)**: Quasi-experimental method comparing changes over time between treatment and control groups. DiD = (Treatment_after - Treatment_before) - (Control_after - Control_before). Assumes parallel trends (counterfactual trends would be similar).

**Discount Factor (δ)**: In repeated games, how much future payoffs are valued relative to present. δ = 1 means future = present (perfectly patient). δ close to 1 is required for folk theorem cooperation. δ < 0.5 prevents cooperation even in infinitely repeated Prisoner's Dilemma.

**do-Calculus**: Pearl's formal system distinguishing observing (conditioning on P(Y|X)) from intervening (do-operator P(Y|do(X))). Barometer and storm: observing low barometer predicts storm; forcing barometer low doesn't cause storm. do-operator captures this.

**Dominant Strategy**: Strategy that is best response regardless of what opponents do. Defect dominates cooperate in Prisoner's Dilemma for both players. If all players have dominant strategies, game is dominance-solvable.

**Dual Process Theory**: Kahneman's framework. System 1 (fast, automatic, effortless, intuitive) vs System 2 (slow, deliberate, effortful, analytical). System 1 generates impressions; System 2 monitors and sometimes overrides. Biases arise when System 2 fails to override System 1 errors.

**Duhem-Quine Thesis**: No hypothesis is tested in isolation. Experiments test a bundle (main hypothesis + auxiliaries + background theories + instrument assumptions). Any hypothesis can be saved by rejecting auxiliaries. Falsification is never definitive.

**Dunning-Kruger Effect**: Low-skilled individuals overestimate their ability; high-skilled are well-calibrated or slightly underestimate. Bottom quartile think they're 60th percentile. Skill and meta-skill (ability to assess skill) are coupled. Incompetence prevents recognizing incompetence.

**Ecological Rationality**: Gigerenzer's framework: heuristics aren't biases but adaptive tools evolved to exploit environmental structure. Match strategy to environment. Simple heuristics can outperform complex models in uncertain, noisy environments.

**Effect Size**: Magnitude of an effect, independent of sample size. Cohen's d (standardized mean difference): 0.2 = small, 0.5 = medium, 0.8 = large. Correlation r: 0.1 = small, 0.3 = medium, 0.5 = large. Statistical significance ≠ practical significance.

**Empiricism**: View that all knowledge derives from sense experience (Locke, Hume). Contrasts with rationalism (reason is primary source of knowledge). Hume's problem of induction undermines pure empiricism.

**Endowment Effect**: People value objects more when they own them. Mug experiment: selling price (~$7) >> buying price (~$3) for identical mugs. Driven by loss aversion and status quo bias. Inconsistent with standard economic theory.

**Epistemic Rationality**: Forming true beliefs proportioned to evidence. Contrasts with instrumental rationality (choosing effective means to goals). Epistemic rationality generally serves instrumental rationality (accurate beliefs → better decisions).

**Epistemology**: Study of knowledge — its nature, sources, limits, and justification. Central questions: What is knowledge? How is it justified? What can we know? Sources of knowledge?

**ESS (Evolutionarily Stable Strategy)**: Strategy that, when adopted by the population, cannot be invaded by any mutant strategy. More robust than Nash equilibrium. Hawk-Dove game: mixed ESS with proportion Hawks = V/C. Explains limited aggression in animals.

**Expected Utility**: EU(A) = Σ P(Oᵢ|A) × U(Oᵢ). Probability-weighted average of outcome utilities. Von Neumann-Morgenstern proved: if preferences satisfy completeness, transitivity, continuity, independence, then you act as if maximizing expected utility.

**Expected Value**: EV = Σ pᵢ × vᵢ. Probability-weighted average of outcome values. Simplest decision criterion but ignores risk preferences. Works for risk-neutral agents or small stakes.

**External Validity**: Whether findings generalize beyond the study context (sample, setting, time). RCTs with volunteers may have high internal validity but low external validity if volunteers differ from target population.

**Falsifiability**: Popper's demarcation criterion. A theory is scientific iff it could be proven wrong by possible observations. "All swans are white" is falsifiable (black swan would disprove it). "God works in mysterious ways" is unfalsifiable.

**Fermi Estimation**: Decomposing complex questions into estimable components, multiplying estimates. Piano tuners in Chicago: population × households × piano ownership × tuning frequency / tunings per tuner = ~50-100. Individual errors cancel.

**Folk Theorem**: In infinitely repeated games (or finite with uncertain end), almost any feasible, individually rational outcome can be sustained as equilibrium via trigger strategies, if players are sufficiently patient (δ close enough to 1). Explains cooperation without external enforcement.

**Foundationalism**: View that knowledge rests on indubitable foundations not requiring further justification. Descartes: cogito ergo sum is foundation. Build all knowledge on this. Critics: few beliefs are truly indubitable; infinite regress can't be stopped.

**Framing Effect**: Logically equivalent information presented differently leads to different choices. Asian Disease Problem: same option framed as "200 saved" vs "400 die" reverses preferences. Driven by reference dependence and loss aversion.

**Frequentist**: Interpreting probability as long-run relative frequency in repeated trials. Frequentists can assign probabilities to repeatable random experiments but not to one-time events or hypotheses. Contrasts with Bayesian (probability as degree of belief).

**Fundamental Problem of Causal Inference**: Cannot observe both Y₁ᵢ (outcome with treatment) and Y₀ᵢ (outcome without treatment) for the same individual at the same time. Counterfactuals are unobservable. Solution: estimate average treatment effects by comparing groups.

**Gambler's Fallacy**: Belief that after streak, opposite outcome is "due." After 5 reds on roulette, black isn't more likely — wheel has no memory. Representativeness heuristic: short sequences should resemble long-run distribution.

**Game Theory**: Mathematical study of strategic interaction. Players, strategies, payoffs. Nash equilibrium: mutual best responses. Applications: economics, politics, biology, conflict, cooperation, bargaining.

**Gettier Problem**: Edmund Gettier (1963) showed justified true belief is insufficient for knowledge. Gettier cases: belief is justified, true, and believed, but arises from epistemic luck, not genuine knowledge. No consensus solution exists.

**Goodhart's Law**: When a measure becomes a target, it ceases to be a good measure. Test scores as measure of learning → teachers teach to test, learning declines. Citation counts → publish lots of low-quality papers.

**HARKing (Hypothesizing After Results are Known)**: Conducting exploratory analysis, finding pattern, then writing as if you predicted it a priori (confirmatory). Misleads about evidential strength. Solution: pre-registration.

**Heuristic**: Mental shortcut trading accuracy for speed and simplicity. Availability, representativeness, anchoring, affect. Can be biased (availability in media-saturated world) or adaptive (recognition heuristic in right environments).

**Hill's Criteria**: Bradford Hill's (1965) nine criteria for inferring causation from association: strength, consistency, specificity, temporality, dose-response, plausibility, coherence, experiment, analogy. Not necessary or sufficient, but useful heuristics. Temporality is essential.

**Hindsight Bias**: "I knew it all along" — overestimating how predictable an outcome was after learning it occurred. Fischhoff & Beyth: participants misremembered pre-Nixon-trip predictions as closer to actual outcomes. Creates illusion of inevitability, distorts learning.

**Incommensurability**: Kuhn's claim that different paradigms may use different concepts, standards, and methods, making direct comparison difficult or impossible. Newtonian mass vs Einsteinian mass — same concept? If not, paradigms are incommensurable. Controversial claim.

**Induction**: Inferring general principles from specific observations (all observed ravens are black → all ravens are black) or projecting past regularities into future (sun rose every day → sun will rise tomorrow). Hume: induction is rationally unjustifiable.

**Instrumental Rationality**: Choosing effective means to achieve goals. Given preferences and beliefs, choose actions that best satisfy preferences. Contrasts with epistemic rationality (forming true beliefs). Generally complementary.

**Instrumental Variable (IV)**: Variable Z that affects treatment X but affects outcome Y only through X (exclusion restriction). Z must be exogenous (uncorrelated with unobserved confounders). Distance to college as IV for education → earnings. IV estimates LATE (local average treatment effect for compliers).

**Intention-to-Treat**: Analyzing subjects as assigned (by randomization), not as actually treated. Preserves randomization even when some don't comply. Estimates effect of assignment, not effect of treatment itself (diluted by non-compliance).

**Justified True Belief (JTB)**: Classical definition of knowledge (Plato): S knows P iff (1) S believes P, (2) P is true, (3) S is justified in believing P. Gettier showed this is insufficient (Gettier problems).

**Kelly Criterion**: Optimal bet sizing for repeated bets with edge. f* = (pb - q)/b, where p = win probability, b = odds, q = 1-p. Maximizes long-run growth rate. Example: 60% win at 2:1 odds → bet 40% of bankroll. Overbetting risks ruin; underbetting suboptimal.

**Kuhn's Paradigm Shifts**: Science alternates between normal science (puzzle-solving within paradigm) and revolutions (paradigm replacement). Examples: Copernican revolution, Newtonian → Einsteinian, classical → quantum mechanics. Paradigm shifts are discontinuous, sometimes incommensurable.

**Lakatos's Research Programmes**: Hard core (unfalsifiable by methodological decision) + protective belt (modifiable auxiliaries) + positive heuristic (research direction) + negative heuristic (don't test hard core). Progressive programmes generate confirmed novel predictions; degenerating make only ad hoc modifications.

**LATE (Local Average Treatment Effect)**: Effect of treatment on **compliers** — those whose treatment status was affected by the instrument in IV estimation. Not necessarily the same as ATE (average treatment effect on population).

**Likelihood**: P(E|H) — probability of observing evidence E given hypothesis H is true. Key component of Bayes' theorem. Likelihood principle: all information data contains about parameters is in the likelihood function.

**Likelihood Ratio (LR)**: P(E|H) / P(E|¬H) — strength of evidence for H vs ¬H. LR > 1: evidence supports H. LR < 1: evidence opposes H. LR = 10: evidence is 10× more likely under H than ¬H. In odds form of Bayes: posterior odds = prior odds × LR.

**Log Score**: Logarithmic scoring rule: (1/N) Σ [oᵢ log(pᵢ) + (1-oᵢ) log(1-pᵢ)]. Heavily penalizes confident wrong predictions. If you say 99% and wrong: huge penalty. Proper scoring rule. More sensitive to extreme probabilities than Brier score.

**Loss Aversion**: Losses hurt ~2× more than equivalent gains feel good. Value function is steeper for losses. Explains endowment effect, disposition effect, status quo bias. Core component of prospect theory.

**Marginal Likelihood**: P(E) — total probability of observing evidence E, computed via law of total probability: P(E) = Σ P(E|Hᵢ) P(Hᵢ). Denominator in Bayes' theorem; normalizes posterior to sum to 1.

**Mediator**: Variable on causal path X → M → Y. Mechanism through which X affects Y. Education → Occupation → Income. Don't control for mediators if you want total effect; do control if you want direct effect (not through M).

**Meta-Knowledge**: Knowledge about knowledge; thinking about thinking. Epistemology and decision theory are meta-knowledge. Unlike domain knowledge (biology, history), meta-knowledge has compounding returns — improves learning across all domains.

**Minimax Regret**: Choosing option that minimizes worst-case regret (difference between outcome and best possible outcome). Useful when probabilities unknown (deep uncertainty). Example: invest (max regret $50K loss) vs don't invest (max regret $100K missed profit) → minimax regret says invest.

**Mixed Strategy**: Randomizing among pure strategies with specific probabilities. In Matching Pennies, only equilibrium is both players randomizing 50-50. In Hawk-Dove, ESS is population with fraction Hawks = V/C. Real-world: penalty kicks, military tactics, inspection.

**Moderator**: Variable M that changes the strength or direction of the effect of X on Y. Effect of tutoring on test scores differs by prior ability (high-ability benefit more). M doesn't cause X or Y but modifies the X → Y relationship. Estimate via interaction analysis.

**Motivated Reasoning**: Reasoning directed toward reaching desired conclusions rather than truth. Stronger in intelligent people (better at rationalizing). Political polarization: Republicans and Democrats interpret identical evidence oppositely. Cultural cognition.

**Nash Equilibrium**: Strategy profile where no player can improve by unilaterally changing strategy. Mutual best responses. Nash theorem: every finite game has ≥1 Nash equilibrium (possibly in mixed strategies). Not necessarily good outcomes (Prisoner's Dilemma), unique (Battle of Sexes), or stable (Chicken).

**Normal Science**: Kuhn's term for puzzle-solving within an accepted paradigm. Most science is normal science — applying paradigm to new cases, not questioning foundations. Conservative and dogmatic by design. Anomalies tolerated until crisis.

**Outside View**: Kahneman's reference class forecasting. Start with base rate of similar past cases (outside view) rather than reasoning from case-specific details (inside view). IT projects typically run 50% over time → use this as starting estimate, not your team's plan.

**Overconfidence**: Gap between confidence and actual accuracy. Most robust finding in judgment research. Experts are overconfident (especially hedgehogs). When people say 90% confident, they're right ~75%. Calibration training improves it.

**P-hacking**: Running multiple analyses (different subgroups, covariates, outlier exclusions, dependent variables), reporting only those achieving p < 0.05. Capitalizes on random noise. Simmons et al. showed you can find p < 0.05 for literally any hypothesis via researcher degrees of freedom.

**P-value**: Probability of observing data at least as extreme as what was observed, assuming null hypothesis is true: p = P(data ≥ observed | H₀). NOT P(H₀ true | data), not probability it's a fluke, not 1-p = probability it's real. Widely misinterpreted.

**Paradigm**: Kuhn's term for shared framework of concepts, methods, standards, exemplary problem-solutions defining a scientific community. Examples: Newtonian mechanics, Darwinian evolution, quantum mechanics, plate tectonics. Paradigms guide normal science and are replaced in revolutions.

**Parallel Trends Assumption**: In difference-in-differences, the assumption that treatment and control groups would have changed similarly over time absent treatment. Untestable (can't observe counterfactual trend). Can check pre-treatment trends but doesn't guarantee parallel post-treatment.

**Planning Fallacy**: Systematic underestimation of time, cost, and risk for future actions. Sydney Opera House: projected 4 years, $7M → actual 14 years, $102M. Big Dig: projected $2.6B → actual $14.6B. Flyvbjerg: 90% of megaprojects over budget/time. Remedy: reference class forecasting.

**Pooling Equilibrium**: In signaling games, equilibrium where all types choose same action. Signal reveals no information. Contrasts with separating equilibrium (different types choose different actions, signal is informative). Pooling is less efficient.

**Popper's Falsificationism**: Science progresses via bold conjectures and severe tests designed to falsify. Theories that survive are corroborated (not confirmed). Demarcation: science is falsifiable; pseudoscience is unfalsifiable. Criticisms: Duhem-Quine thesis, probabilistic theories, confirmation matters.

**Posterior**: P(H|E) — updated belief in hypothesis H after observing evidence E. Computed via Bayes' theorem: posterior = (likelihood × prior) / marginal likelihood. Posterior becomes prior for next update (Bayesian updating is iterative).

**Prediction Market**: Market where participants trade contracts on future events. Contract pays $1 if event occurs, $0 otherwise. Price reflects aggregated probability belief. Examples: PredictIt (US politics), Polymarket (crypto), Iowa Electronic Markets (academic). Beat polls in ~75% of elections.

**Pre-registration**: Declaring hypotheses, variables, and analysis plan before data collection. Prevents p-hacking and HARKing. Registered reports: peer review before data collection, publication guaranteed regardless of results. Growing adoption but still <5% of articles.

**Prior**: P(H) — belief in hypothesis H before observing evidence. Choice of prior is subjective (Bayesian view) but priors wash out with sufficient data. Types: uninformative (flat), weakly informative, informative (based on previous studies), reference (Jeffreys), conjugate (mathematical convenience).

**Problem of Induction**: Hume's demonstration that inductive inferences (past → future, observed → unobserved) cannot be rationally justified. Not justified deductively (logically invalid), not justified inductively (circular), not justified probabilistically (presupposes induction). All empirical science rests on unjustifiable foundation.

**Proper Scoring Rule**: Scoring rule that is optimized by reporting your true beliefs. Brier score and log score are proper. Percent correct is not proper (can be gamed by always saying 100%). Properness incentivizes honest probability reporting in forecasting tournaments, prediction markets.

**Prospect Theory**: Kahneman & Tversky's descriptive model of choice under risk. Components: reference dependence (evaluate as gains/losses), loss aversion (losses hurt ~2× gains), diminishing sensitivity (s-curve value function), probability weighting (overweight small probabilities, underweight medium-high). Explains violations of expected utility theory.

**Prosecutor's Fallacy**: Confusing P(evidence | innocent) with P(innocent | evidence). "DNA match is 1 in a million if innocent, therefore probability of innocence is 1 in a million." Wrong — need the prior. Sally Clark case: wrongfully convicted of double infanticide based on this fallacy.

**Publication Bias (File Drawer Problem)**: Journals prefer positive, significant results. Null results filed away. Published literature is biased sample. If 20 teams test false hypothesis, 1 finds p < 0.05 by chance, gets published. 19 null results remain in file drawers. Literature falsely suggests effect exists.

**Rationalism**: View that reason is primary source of knowledge, superior to senses. Descartes, Leibniz. Contrasts with empiricism (senses are primary). Kant synthesized both: synthetic a priori knowledge possible via reason structuring experience.

**Reference Class Forecasting**: Using base rates of similar past cases (outside view) as starting point, then adjusting for case-specific factors. IT projects run 50% over time on average → start with this, don't trust your team's optimistic estimate. Corrects planning fallacy.

**Regression Discontinuity (RD)**: Quasi-experimental method exploiting treatment cutoff on continuous variable. Test score ≥50 → pass. Compare just above (51) and just below (49) cutoff — nearly identical except for treatment. Difference at cutoff estimates causal effect. Sharp RD (jump 0→1) vs Fuzzy RD (probabilistic jump).

**Registered Reports**: Peer review before data collection. Study design/hypotheses reviewed. If accepted, publication guaranteed regardless of results. Removes publication bias, prevents p-hacking/HARKing. ~300 journals offer, but still <5% of articles.

**Reliabilism**: Epistemological view that knowledge requires belief produced by reliable cognitive process. Perception in good lighting is reliable; guessing is not. Response to Gettier: barn-façade Henry's belief isn't knowledge because perception isn't reliable in that environment (can't distinguish real barns from fakes).

**Replication Crisis**: Widespread failure to reproduce published findings when replicated. Psychology: 36% replicated. Cancer biology: 11-25%. Economics: 61%. Causes: p-hacking, publication bias, HARKing, low power. Solutions: pre-registration, registered reports, open data, replication studies.

**Representativeness Heuristic**: Judging probability by similarity to stereotype/prototype. Ignores base rates and sample size. Linda problem: "bank teller and feminist" judged more probable than "bank teller" because description representative of feminists. Conjunction fallacy.

**Research Programme** (Lakatos): Hard core (central unfalsifiable commitments) + protective belt (modifiable auxiliaries) + positive heuristic (what problems to pursue) + negative heuristic (protect hard core). Progressive: generates confirmed novel predictions. Degenerating: only ad hoc modifications.

**Resolution** (in forecasting): Ability to discriminate easy from hard questions. Give high probability to easy, low to hard. Good forecasters have both calibration (confidence matches accuracy) and resolution (distinguish easy/hard). Bad forecasters might be calibrated at 50% by always saying "50%" (no resolution).

**Satisficing**: Herbert Simon's term for choosing "good enough" rather than optimal. Bounded rationality: can't optimize due to information/cognition/time limits. Apartment search: find first meeting criteria, stop. Not irrational — adaptive response to constraints.

**Scope Insensitivity**: Failure to scale valuation with magnitude of outcome. Willingness to pay to save 2,000 birds ($80) ≈ 200,000 birds ($88). Affect heuristic: "saving birds" generates fixed feeling regardless of number. Remedy: "shut up and multiply" — force calculation.

**Screening**: Uninformed party designs menu of options to induce self-selection, revealing types. Insurance: high deductible/low premium (attracts low-risk) vs low deductible/high premium (attracts high-risk). Each type chooses contract designed for them. Contrasts with signaling (informed party sends signal).

**Separating Equilibrium**: In signaling games, equilibrium where different types choose different actions. Signal is informative. High-ability workers get education, low-ability don't → employers infer type from education. More efficient than pooling equilibrium.

**Signaling**: Informed player reveals type through costly action that types find differentially costly. Spence's job market: education separates high-ability (find it easy) from low-ability (find it prohibitively costly). Employers infer ability from education even if education doesn't increase productivity. Examples: warranties, dividends, advertising.

**Simpson's Paradox**: Association appears in every subgroup but reverses when aggregated (or vice versa). UC Berkeley admissions: women had higher rates in most departments but lower overall (applied to harder departments). Treatment A better than B in both mild and severe cases but worse overall (A given to severe cases disproportionately). Resolution depends on causal structure.

**Subgame Perfect Equilibrium**: Nash equilibrium that is also Nash in every subgame. Eliminates incredible threats — threats that wouldn't be carried out if tested. Found via backward induction. Example: Entry deterrence — threat to fight is not credible; accommodation is subgame perfect.

**Sunk Cost Fallacy**: Continuing activity because of past investment rather than future value. Finishing bad movie because you paid for ticket. Economically irrational (only future costs/benefits matter). Psychologically powerful (loss aversion, commitment, not wanting to "waste"). Remedy: evaluate only future, not past.

**Superforecaster**: Person consistently outperforming at probabilistic prediction. Tetlock's Good Judgment Project: top 2% had Brier scores 30% better than average, beat intelligence analysts with classified info, beat prediction markets. Traits: actively open-minded, granular probabilities, frequent updating, foxes not hedgehogs, numerate, ego-less, team players.

**SUTVA (Stable Unit Treatment Value Assumption)**: Assumption in causal inference that (1) no interference (your treatment doesn't affect my outcome) and (2) no hidden versions of treatment (treatment is well-defined). Required for potential outcomes framework. Often violated (vaccines have spillovers, "same" treatment varies in implementation).

**Synthetic A Priori**: Kant's category of knowledge that is informative (synthetic) yet known independently of experience (a priori). Examples: mathematics (7+5=12), causality (every event has a cause), geometry. Possible because mind actively structures experience via forms of intuition (space, time) and categories of understanding (causality, substance).

**System 1**: Fast, automatic, effortless, intuitive cognitive processing. Parallel, unconscious, associative. Generates impressions, feelings, impulses. Source of heuristics and biases. Examples: recognizing faces, detecting emotions, reading simple text, 2+2=?, driving on empty road.

**System 2**: Slow, deliberate, effortful, analytical cognitive processing. Serial, conscious, rule-based. Monitors System 1, sometimes overrides. Lazy — often endorses System 1 without checking. Examples: complex math, parking in tight space, checking logical validity, filing taxes.

**Trigger Strategy**: In repeated games, strategy that cooperates until opponent defects, then punishes. Grim trigger: defect forever after first defection. Tit-for-tat: mirror opponent's last move. Win-stay-lose-shift: if payoff good, repeat; if bad, switch. Sustains cooperation via folk theorem when players patient.

**Value Function**: In prospect theory, v(x) maps outcomes to subjective value. Concave for gains (risk averse), convex for losses (risk seeking), steeper for losses (loss aversion). Reference-dependent: evaluated as gains/losses from reference point, not absolute wealth.

---

## Key Formulas

| Formula | Name | Notes |
|---------|------|-------|
| P(H\|E) = P(E\|H) × P(H) / P(E) | **Bayes' Theorem** | Fundamental formula for updating beliefs with evidence |
| Posterior odds = Prior odds × LR | **Odds form of Bayes** | Likelihood ratio LR = P(E\|H) / P(E\|¬H) |
| EU(A) = Σ P(O\|A) × U(O) | **Expected Utility** | Von Neumann-Morgenstern normative standard |
| Brier = (1/N) Σ (pᵢ - oᵢ)² | **Brier Score** | Mean squared error of probabilistic predictions |
| Log score = (1/N) Σ [oᵢ log(pᵢ) + (1-oᵢ) log(1-pᵢ)] | **Log Score** | Logarithmic scoring rule, heavily penalizes confident errors |
| f* = (pb - q) / b | **Kelly Criterion** | Optimal bet sizing for repeated bets with edge |
| ATE = E[Y₁] - E[Y₀] | **Average Treatment Effect** | Expected difference between treatment and control outcomes |
| DiD = (T_after - T_before) - (C_after - C_before) | **Difference-in-Differences** | Compare changes over time between groups |
| IV = Cov(Y, Z) / Cov(X, Z) | **Instrumental Variables** | Estimand when Z is valid instrument for X → Y |
| v(x) = x^α (gains), -λ(-x)^β (losses) | **Prospect Theory Value Function** | α,β < 1 (diminishing sensitivity), λ ≈ 2-2.5 (loss aversion) |

---

## Cognitive Biases Quick Reference

| Bias | What It Does | Example | Antidote |
|------|-------------|---------|----------|
| **Anchoring** | Initial values bias subsequent judgments | Spin wheel 10 vs 65 → estimates differ by ~20 points | Generate multiple anchors; consider range |
| **Availability** | Ease of recall biases probability estimates | Homicide feels more common than diabetes | Seek base rates, not headlines |
| **Confirmation** | Seek/interpret evidence confirming beliefs | 2-4-6 task: test confirming, not disconfirming | Consider the opposite; seek disconfirming evidence |
| **Framing** | Presentation changes choice | 90% survival vs 10% mortality → different choices | Reframe from multiple angles |
| **Hindsight** | "I knew it all along" after outcome | Post-9/11: "attacks were obvious" | Decision journal with pre-outcome predictions |
| **Loss aversion** | Losses hurt ~2× gains | Selling price >> buying price for same mug | Expected value analysis; focus on final state |
| **Overconfidence** | Confidence exceeds accuracy | Say 90%, right 75% | Calibration training; track accuracy |
| **Planning fallacy** | Underestimate time/cost/risk | Projects run 50-200% over estimates | Reference class forecasting (outside view) |
| **Representativeness** | Judge by similarity, ignore base rates | Linda problem: conjunction fallacy | Apply Bayes' theorem; start with base rates |
| **Scope insensitivity** | Don't scale valuation with magnitude | Pay same to save 2K and 200K birds | Shut up and multiply; force calculation |
| **Sunk cost** | Continue due to past investment | Finish bad movie because paid for ticket | Evaluate only future costs/benefits |
| **Status quo** | Prefer current state | Default effects: opt-out 99% donors, opt-in 12% | Imagine choosing from scratch |

---

## Key Thinkers

| Thinker | Field | Key Contribution | Major Work |
|---------|-------|-----------------|------------|
| **Plato** (428-348 BCE) | Epistemology | Justified true belief; Theory of Forms | *Theaetetus*, *Republic* |
| **Aristotle** (384-322 BCE) | Logic, science | Syllogistic logic, empirical method | *Organon*, *Posterior Analytics* |
| **René Descartes** (1596-1650) | Epistemology | Radical doubt, cogito, foundationalism | *Meditations on First Philosophy* |
| **John Locke** (1632-1704) | Epistemology | Empiricism, tabula rasa | *Essay Concerning Human Understanding* |
| **David Hume** (1711-1776) | Epistemology | Problem of induction, causation as regularity | *Treatise of Human Nature*, *Enquiry* |
| **Immanuel Kant** (1724-1804) | Epistemology | Synthetic a priori, transcendental idealism | *Critique of Pure Reason* |
| **Thomas Bayes** (1701-1761) | Probability | Bayes' theorem | *Essay Towards Solving a Problem* |
| **Pierre-Simon Laplace** (1749-1827) | Probability | Bayesian probability, determinism | *Théorie Analytique des Probabilités* |
| **John Stuart Mill** (1806-1873) | Logic, ethics | Methods of induction, utilitarianism | *System of Logic*, *Utilitarianism* |
| **Karl Popper** (1902-1994) | Philosophy of science | Falsificationism, demarcation problem | *Logic of Scientific Discovery*, *Conjectures and Refutations* |
| **Thomas Kuhn** (1922-1996) | Philosophy of science | Paradigm shifts, normal science | *Structure of Scientific Revolutions* |
| **Imre Lakatos** (1922-1974) | Philosophy of science | Research programmes | *Methodology of Scientific Research Programmes* |
| **W.V.O. Quine** (1908-2000) | Epistemology, logic | Holism, naturalized epistemology | *Two Dogmas of Empiricism*, *Word and Object* |
| **Herbert Simon** (1916-2001) | Economics, AI | Bounded rationality, satisficing | *Administrative Behavior* (Nobel 1978) |
| **Daniel Kahneman** (b. 1934) | Psychology, economics | Prospect theory, heuristics and biases | *Judgment Under Uncertainty*, *Thinking, Fast and Slow* (Nobel 2002) |
| **Amos Tversky** (1937-1996) | Psychology | Prospect theory with Kahneman | *Judgment Under Uncertainty* |
| **John Nash** (1928-2015) | Game theory | Nash equilibrium | Game theory foundations (Nobel 1994) |
| **Thomas Schelling** (1921-2016) | Game theory | Strategy of conflict, commitment | *Strategy of Conflict* (Nobel 2005) |
| **Judea Pearl** (b. 1936) | Computer science, statistics | Causal inference, DAGs, do-calculus | *Causality*, *Book of Why* (Turing Award 2011) |
| **Philip Tetlock** (b. 1954) | Psychology, political science | Superforecasting, expert political judgment | *Expert Political Judgment*, *Superforecasting* |
| **Gerd Gigerenzer** (b. 1947) | Psychology | Ecological rationality, fast-and-frugal heuristics | *Simple Heuristics That Make Us Smart* |
| **Robert Nozick** (1938-2002) | Philosophy | Sensitivity/tracking account of knowledge | *Philosophical Explanations* |
| **Donald Rubin** (b. 1943) | Statistics | Potential outcomes framework (Rubin Causal Model) | Numerous papers on causal inference |
| **E.T. Jaynes** (1922-1998) | Physics, probability | Objective Bayesianism, maximum entropy | *Probability Theory: The Logic of Science* |

---

## Summary

This glossary provides comprehensive coverage of epistemology, decision theory, causal inference, game theory, and forecasting. Terms range from foundational concepts (Bayes' theorem, Nash equilibrium, justified true belief) to practical tools (Fermi estimation, reference class forecasting, pre-mortems) to cognitive phenomena (anchoring, loss aversion, Dunning-Kruger effect).

Key formulas include Bayes' theorem (fundamental for updating beliefs), expected utility (normative decision standard), Brier score (evaluating forecasts), Kelly criterion (optimal bet sizing), and causal inference estimands (ATE, DiD, IV).

Cognitive biases — anchoring, availability, confirmation, framing, hindsight, loss aversion, overconfidence, planning fallacy, representativeness, scope insensitivity, sunk cost, status quo — are systematic errors arising from heuristic processing. Each has specific antidotes: calibration training, reference class forecasting, considering the opposite, decision journals, expected value analysis.

Major thinkers shaped the field: Plato and Descartes on knowledge foundations, Hume on induction, Kant on synthesis, Bayes and Laplace on probability, Popper and Kuhn on science, Simon on bounded rationality, Kahneman and Tversky on cognitive psychology, Nash and Schelling on game theory, Pearl on causation, Tetlock on forecasting, Gigerenzer on ecological rationality.

The practical lesson: These concepts, formulas, and tools equip you for clearer thinking and better decisions. Epistemology provides foundations for evaluating claims. Decision theory guides choices under uncertainty. Causal inference distinguishes correlation from causation. Game theory illuminates strategic interaction. Forecasting improves predictions. Awareness of cognitive biases enables debiasing. Meta-knowledge compounds across all domains where knowledge and decisions matter — which is everything.
