# Pharmacology

## Fundamentals

### How Drugs Work

Most drugs act by binding to **receptors** (proteins on/in cells):

| Concept | Definition |
|---|---|
| **Agonist** | Binds receptor, activates it (mimics natural ligand) |
| **Antagonist** | Binds receptor, blocks it (prevents activation) |
| **Partial agonist** | Binds and partially activates (ceiling effect) |
| **Inverse agonist** | Binds and produces opposite effect to agonist |
| **Allosteric modulator** | Binds different site; enhances or inhibits receptor response |
| **Affinity** | How strongly drug binds to receptor |
| **Efficacy** | Maximum response drug can produce |
| **Potency** | Amount of drug needed for given effect (EC50) |

### Dose-Response
- Sigmoidal curve: increasing dose → increasing effect → plateau (Emax)
- **EC50/ED50:** Dose effective in 50% of population
- **TD50:** Dose toxic in 50%
- **LD50:** Dose lethal in 50%

### Therapeutic Index (TI = TD50 / ED50)

| Drug | TI | Implication |
|---|---|---|
| Warfarin | ~2 | Very narrow; requires INR monitoring |
| Lithium | ~3 | Narrow; serum level monitoring |
| Digoxin | ~2-3 | Narrow; toxicity common |
| Penicillin | >100 | Very wide; safe |
| Acetaminophen | ~4-10 | Moderate; toxic dose not far from therapeutic |

Narrow TI → requires therapeutic drug monitoring (TDM).

---

## Pharmacokinetics (ADME)

### Absorption

| Route | Bioavailability | Speed | Notes |
|---|---|---|---|
| IV | 100% | Immediate | Direct systemic; precise dosing |
| IM | 75-100% | 10-20 min | Depot effect possible |
| Oral (PO) | 5-100% (variable) | 30-90 min | Most common; first-pass effect |
| Sublingual | ~75% | Minutes | Bypasses first-pass; nitroglycerin |
| Inhalation | 80-100% (lungs) | Very fast | Anesthetics, asthma inhalers |
| Transdermal | Variable | Slow, sustained | Fentanyl patches, nicotine |

**First-pass metabolism:** Oral drugs → portal vein → liver metabolism before systemic circulation. Can dramatically reduce bioavailability. Morphine oral bioavailability ~25%; nitroglycerin ~1% (hence sublingual).

### Distribution
- **Volume of distribution (Vd):** High Vd = drug in tissues (chloroquine ~15,000L); Low Vd = stays in plasma (warfarin ~8L)
- **Plasma protein binding:** Only unbound drug is active. Warfarin 99% bound; displacement → toxicity risk
- **Blood-brain barrier:** Tight junctions; only small, lipophilic, uncharged molecules cross
- **Placental transfer:** Most drugs cross; teratogenicity concern

### Metabolism (Biotransformation)
Primarily **liver.** Converts lipophilic → hydrophilic for excretion.

**Phase I (CYP450 system):**

| Enzyme | % Drug Metabolism | Key Substrates |
|---|---|---|
| CYP3A4 | ~50% | Statins, cyclosporine, many antibiotics |
| CYP2D6 | ~25% | Codeine, SSRIs, beta-blockers |
| CYP2C9 | ~15% | Warfarin, NSAIDs, phenytoin |
| CYP2C19 | ~10% | Omeprazole, clopidogrel |
| CYP1A2 | ~5% | Caffeine, theophylline |

**Important inhibitors** (↑ drug levels → toxicity):
- Grapefruit juice (CYP3A4) — hence warning labels
- Ketoconazole, erythromycin, ritonavir (CYP3A4)
- Fluoxetine (CYP2D6)

**Important inducers** (↓ drug levels → treatment failure):
- Rifampin (most potent; CYP3A4, 2C9, 2C19; reduces oral contraceptive efficacy)
- St. John's wort (CYP3A4)
- Chronic alcohol (CYP2E1)

**Phase II:** Conjugation (glucuronidation, sulfation) → water-soluble metabolites for excretion.

**Pharmacogenomics:** Genetic CYP variants affect drug response. CYP2D6 poor metabolizers: codeine ineffective (can't convert to morphine). CYP2C19 poor metabolizers: clopidogrel won't activate → stent thrombosis risk.

### Excretion
- **Renal (primary):** Filtration + tubular secretion; dose adjustment in CKD
- **Biliary:** Large molecules; enterohepatic circulation can prolong effects
- **Pulmonary:** Volatile anesthetics

### Half-Life and Steady State
- **t½:** Time for plasma concentration to drop 50%
- **Steady state:** Reached in ~4-5 half-lives with repeated dosing

| Drug | Half-Life | Steady State |
|---|---|---|
| Ibuprofen | ~2 hours | ~10 hours |
| Metformin | ~5 hours | ~1 day |
| Warfarin | ~36-42 hours | ~7-10 days |
| Fluoxetine | 1-3 days (metabolite: 4-16 days) | 4-8 weeks |
| Amiodarone | ~40-55 days | 6-12 months |

---

## Major Drug Classes

### Antibiotics

**Mechanism Categories:**
- **Cell wall synthesis inhibitors:** Target peptidoglycan synthesis unique to bacteria (humans lack cell walls → selective toxicity). β-lactams (penicillins, cephalosporins, carbapenems) bind penicillin-binding proteins (PBPs) → prevent cross-linking of peptidoglycan → osmotic lysis. Resistance: β-lactamases cleave β-lactam ring; overcome by adding β-lactamase inhibitors (amoxicillin + clavulanate = Augmentin; piperacillin + tazobactam = Zosyn).
- **Protein synthesis inhibitors:** Target bacterial ribosomes (70S = 30S + 50S) vs human ribosomes (80S) → selective toxicity. 30S: tetracyclines (block tRNA binding), aminoglycosides (cause misreading of mRNA, bactericidal). 50S: macrolides (block translocation), chloramphenicol, linezolid, clindamycin.
- **DNA/RNA synthesis inhibitors:** Fluoroquinolones inhibit DNA gyrase (gram-neg) and topoisomerase IV (gram-pos) → prevent DNA replication/transcription. Rifampin inhibits RNA polymerase (key for TB).
- **Folate synthesis inhibitors:** Trimethoprim-sulfamethoxazole (TMP-SMX) blocks sequential steps in bacterial folate synthesis (humans get folate from diet → selective toxicity). Synergistic combination.

| Class | Mechanism | Key Drugs | Coverage | Key Side Effects |
|---|---|---|---|---|
| Penicillins | Cell wall (PBP binding) | Amoxicillin, ampicillin, piperacillin | Narrow (penicillin) → broad (piperacillin) | ~10% allergy (90% not true allergy); anaphylaxis ~0.05% |
| Cephalosporins | Cell wall (PBP, broader each gen) | Cephalexin (1st), cefazolin (1st IV), ceftriaxone (3rd), cefepime (4th) | 1st: gram-pos; 3rd: gram-neg + CNS; 5th: MRSA | ~2% cross-reactivity with penicillin allergy |
| Carbapenems | Cell wall (broadest β-lactam) | Meropenem, imipenem, ertapenem | Broadest spectrum; ESBL-producers | Reserve for resistant infections; seizures (imipenem) |
| Fluoroquinolones | DNA gyrase/topoisomerase IV | Ciprofloxacin, levofloxacin, moxifloxacin | Broad; respiratory (levofloxacin), urinary (cipro) | Tendon rupture, aortic dissection, neuropathy, QT prolongation; FDA black box |
| Macrolides | 50S ribosome (translocation block) | Azithromycin, erythromycin, clarithromycin | Atypicals (Mycoplasma, Chlamydia, Legionella), respiratory | QT prolongation, GI upset; CYP3A4 inhibition (erythromycin) |
| Tetracyclines | 30S ribosome (tRNA block) | Doxycycline, minocycline | Broad; Lyme, MRSA (doxy), acne, Rickettsia | Photosensitivity, teeth staining (children), esophagitis |
| Aminoglycosides | 30S ribosome (misreading, bactericidal) | Gentamicin, tobramycin, amikacin | Gram-neg aerobes; synergy with β-lactams | Nephrotoxicity, ototoxicity (irreversible); TDM required |
| Vancomycin | Cell wall (binds D-Ala-D-Ala terminal) | Vancomycin | MRSA, C. diff (oral), gram-pos | Red man syndrome (histamine release, slow infusion prevents); nephrotoxicity; TDM |
| Linezolid | 50S ribosome (unique binding site) | Linezolid | VRE, MRSA | Thrombocytopenia, serotonin syndrome (MAO inhibitor activity), lactic acidosis |
| Metronidazole | DNA damage (free radicals in anaerobes) | Metronidazole | Anaerobes, C. diff, parasites (Giardia, ameba) | Disulfiram-like reaction with alcohol; metallic taste; neuropathy |

### Analgesics

**NSAIDs (Non-Steroidal Anti-Inflammatory Drugs):**
- Mechanism: Inhibit cyclooxygenase (COX) enzymes → ↓ prostaglandin synthesis → ↓ pain, inflammation, fever. COX-1 = constitutive (GI mucosal protection, platelet aggregation, renal blood flow); COX-2 = inducible at sites of inflammation.
- Non-selective (ibuprofen, naproxen, aspirin): Inhibit both COX-1 and COX-2. GI bleeding (COX-1 inhibition removes mucosal protection; risk ↑ with age, concurrent steroids, anticoagulants), renal impairment (prostaglandins maintain renal blood flow in hypovolemia → NSAIDs can precipitate AKI), cardiovascular risk (non-aspirin NSAIDs ↑ MI/stroke risk via ↓ PGI2 vasodilation).
- COX-2 selective (celecoxib): Less GI bleeding but same cardiovascular risk; rofecoxib (Vioxx) withdrawn 2004 due to ↑ MI risk — landmark drug safety case.
- **Aspirin:** Unique — irreversibly acetylates COX-1 in platelets (platelets can't make new COX, effect lasts platelet lifespan ~7-10 days); low-dose (81mg) for CVD prevention. Also inhibits COX-2 at higher doses (anti-inflammatory). Reye's syndrome: aspirin + viral illness in children → hepatic/cerebral damage (rare but serious; why children get acetaminophen/ibuprofen instead).

**Acetaminophen (Paracetamol):**
- Mechanism: Probably central COX inhibition and/or endocannabinoid system modulation; NOT anti-inflammatory (no peripheral COX inhibition). Antipyretic + analgesic only.
- Safe at therapeutic doses (≤4g/day; some guidelines now say ≤3g/day for chronic use). Hepatotoxic in overdose: metabolized by CYP2E1 to NAPQI (toxic metabolite); normally conjugated with glutathione → harmless. Overdose → glutathione depleted → NAPQI accumulates → hepatocyte necrosis → acute liver failure. Treatment: N-acetylcysteine (NAC) replenishes glutathione; must be given within 8-10 hours of ingestion for best results.
- #1 cause of acute liver failure in US/UK; often accidental (multiple acetaminophen-containing products).

**Opioids:**
- Mechanism: Bind mu (μ), kappa (κ), delta (δ) opioid receptors. Mu = primary analgesic target: activate inhibitory G-proteins → ↓ cAMP → close Ca²⁺ channels (presynaptic, ↓ neurotransmitter release) + open K⁺ channels (postsynaptic, hyperpolarization) → ↓ pain signal transmission in dorsal horn of spinal cord + ascending pathways. Also activate mesolimbic dopamine pathway → euphoria → addiction potential.
- Effects: Analgesia, euphoria, respiratory depression (↓ medullary response to CO₂ — cause of death in overdose), constipation (↓ GI motility via enteric receptors — tolerance does NOT develop to this effect), miosis (pinpoint pupils — diagnostic sign), nausea, cough suppression.
- Tolerance: Repeated exposure → ↓ receptor sensitivity → need higher doses. Physical dependence: abrupt cessation → withdrawal (not life-threatening but extremely unpleasant: sweating, diarrhea, myalgia, anxiety). Addiction: compulsive use despite harm.
- Potency range: codeine (0.1x morphine) → tramadol (0.1x) → morphine (reference) → oxycodone (1.5x) → hydromorphone (5x) → fentanyl (100x) → carfentanil (10,000x).
- Naloxone (Narcan): Competitive mu-receptor antagonist; reverses overdose within 1-2 minutes IV; shorter half-life than most opioids → re-sedation risk → may need repeat doses. Available as nasal spray (OTC in many states).

**Adjuvant Analgesics (for chronic/neuropathic pain):**
- Gabapentin/pregabalin: Bind α2δ subunit of voltage-gated Ca²⁺ channels → ↓ excitatory neurotransmitter release. Used for neuropathic pain, fibromyalgia. Not traditional analgesics but increasingly important.
- Duloxetine (SNRI): ↑ serotonin + norepinephrine in descending pain inhibitory pathways. Approved for diabetic neuropathy, fibromyalgia, chronic musculoskeletal pain.
- Tricyclic antidepressants (amitriptyline): Same descending inhibition mechanism; also Na⁺ channel blockade. First-line for some neuropathic pain conditions.

### Cardiovascular (Detailed Mechanisms)

| Class | Mechanism (Detail) | Primary Use | Key Side Effects |
|---|---|---|---|
| **ACE inhibitors** (-pril: lisinopril, enalapril, ramipril) | Block angiotensin-converting enzyme → ↓ angiotensin II (vasoconstrictor) + ↓ aldosterone (Na⁺ retention) + ↑ bradykinin (vasodilator). Reduce cardiac remodeling post-MI. Also ↓ intraglomerular pressure → renoprotective. | HTN, HF, diabetic nephropathy, post-MI | Dry cough (10-20%, from ↑ bradykinin), angioedema (rare but dangerous), hyperkalemia, teratogenic |
| **ARBs** (-sartan: losartan, valsartan) | Block angiotensin II type 1 (AT1) receptor directly → same downstream effects as ACE-I but no bradykinin accumulation → no cough | Same as ACE-I; if ACE-I causes cough | Hyperkalemia, teratogenic; generally well-tolerated |
| **Beta-blockers** (-olol: metoprolol, atenolol, carvedilol, propranolol) | Block β-adrenergic receptors → β1 (heart): ↓ HR, contractility, conduction, renin release; β2 (lungs/vessels): bronchoconstriction, vasoconstriction (non-selective). Cardioselective (metoprolol, atenolol) = β1 preferential. Carvedilol also blocks α1 → vasodilation. Reduce myocardial O₂ demand; prevent remodeling in HF (paradoxical: start low, go slow). | HTN, HF (carvedilol, metoprolol succinate, bisoprolol), post-MI, rate control in AF, migraine prophylaxis, performance anxiety | Bradycardia, fatigue, sexual dysfunction, mask hypoglycemia symptoms in diabetics, bronchospasm (avoid non-selective in asthma), rebound tachycardia if stopped abruptly |
| **CCBs** | Two subclasses: **Dihydropyridines** (amlodipine, nifedipine): block L-type Ca²⁺ channels in vascular smooth muscle → vasodilation; minimal cardiac effects. **Non-dihydropyridines** (diltiazem, verapamil): block Ca²⁺ channels in heart + vessels → ↓ HR, ↓ contractility, ↓ conduction + vasodilation. | HTN (amlodipine), angina (both), rate control AF (diltiazem, verapamil) | Peripheral edema + flushing (dihydropyridines); constipation (verapamil); bradycardia (non-DHP); avoid verapamil + beta-blocker (additive cardiac depression) |
| **Statins** (-statin: atorvastatin, rosuvastatin) | Inhibit HMG-CoA reductase (rate-limiting step in hepatic cholesterol synthesis) → ↓ intracellular cholesterol → ↑ LDL receptor expression on hepatocytes → ↑ LDL clearance from blood. Also: pleiotropic effects (anti-inflammatory, plaque stabilization, endothelial function). ↓ LDL 30-50%. | Primary/secondary CVD prevention, hyperlipidemia | Myalgia (5-10%), rhabdomyolysis (rare but serious), ↑ liver enzymes, ↑ diabetes risk (modest); CYP3A4 interactions (atorvastatin, simvastatin — not rosuvastatin) |
| **Thiazide diuretics** (HCTZ, chlorthalidone, indapamide) | Inhibit NCC (Na⁺-Cl⁻ cotransporter) in distal convoluted tubule → ↑ Na⁺/water excretion. Long-term: vasodilation (mechanism unclear). Also ↑ Ca²⁺ reabsorption (useful in osteoporosis). | First-line HTN (chlorthalidone preferred for outcomes data); edema; nephrolithiasis prevention (calcium stones) | Hypokalemia, hyponatremia, hyperuricemia (gout), hyperglycemia, hypercalcemia |
| **Loop diuretics** (furosemide, bumetanide, torsemide) | Inhibit NKCC2 (Na⁺-K⁺-2Cl⁻ cotransporter) in thick ascending limb of Loop of Henle → most potent diuresis (up to 25% of filtered Na⁺ excreted). Abolish medullary gradient → can't concentrate urine. | Acute decompensated HF (IV for rapid diuresis), edema, CKD (still work when GFR low, unlike thiazides), hypercalcemia | Hypokalemia, ototoxicity (high doses), hypovolemia/hypotension, hypomagnesemia |
| **SGLT2 inhibitors** (-gliflozin: empagliflozin, dapagliflozin) | Block sodium-glucose cotransporter 2 in proximal tubule → glycosuria (glucose excretion in urine) → ↓ blood glucose. Also: osmotic diuresis, natriuresis, ↓ intraglomerular pressure, ↓ preload/afterload, metabolic substrate shift (↑ ketone use by heart). | T2D, HF (both HFrEF and HFpEF — regardless of diabetes status), CKD. Triple threat drug class. | UTIs, genital fungal infections, euglycemic DKA (rare), Fournier's gangrene (very rare) |
| **DOACs** (rivaroxaban, apixaban, edoxaban = factor Xa inhibitors; dabigatran = direct thrombin inhibitor) | Directly inhibit specific coagulation factors (no need for antithrombin like heparin). Predictable PK → fixed dosing, no routine monitoring (unlike warfarin). | AF stroke prevention, DVT/PE treatment/prevention | Bleeding (no reliable reversal agent for Xa inhibitors until idarucizumab for dabigatran and andexanet alfa for Xa inhibitors), renal dosing needed, GI bleeding (dabigatran, rivaroxaban) |
| **Warfarin** | Inhibits vitamin K epoxide reductase → ↓ synthesis of clotting factors II, VII, IX, X and proteins C, S. Takes 3-5 days for full effect (existing factors must be cleared). | AF, mechanical heart valves (DOACs not approved), DVT/PE | Narrow TI; requires INR monitoring (target 2-3); many drug/food interactions (CYP2C9 substrate; vitamin K-rich foods); teratogenic; skin necrosis (rare, protein C depletion) |
| **Antiplatelet agents** | Aspirin: irreversible COX-1 → ↓ thromboxane A2. Clopidogrel/ticagrelor: P2Y12 receptor blockers → ↓ ADP-mediated platelet activation (clopidogrel is prodrug requiring CYP2C19 activation — pharmacogenomics important). Dual antiplatelet therapy (DAPT: aspirin + P2Y12 inhibitor) after stent placement for 6-12 months. | Post-MI, post-stent, stroke prevention | Bleeding; clopidogrel: CYP2C19 poor metabolizers → ↓ efficacy → stent thrombosis |

### Psychiatric (Detailed Mechanisms)

**Antidepressants:**

| Class | Mechanism (Detail) | Examples | Key Side Effects |
|---|---|---|---|
| **SSRIs** | Block serotonin reuptake transporter (SERT) → ↑ synaptic serotonin. Therapeutic effect takes 2-4 weeks (not explained by immediate receptor blockade; likely involves downstream neuroplasticity, BDNF upregulation, hippocampal neurogenesis). Most prescribed antidepressant class. | Fluoxetine (Prozac), sertraline (Zoloft), escitalopram (Lexapro) | Sexual dysfunction (30-50%), GI (nausea, diarrhea), weight gain (long-term), emotional blunting, serotonin syndrome risk with MAOIs, discontinuation syndrome (brain zaps — taper gradually) |
| **SNRIs** | Block both SERT and norepinephrine transporter (NET) → ↑ serotonin + NE. Dual mechanism may help when SSRIs insufficient; NE component useful for pain, fatigue, concentration. | Venlafaxine (Effexor), duloxetine (Cymbalta) | Similar to SSRIs + dose-dependent hypertension (NE effect); duloxetine also approved for neuropathic pain, fibromyalgia |
| **Bupropion** | Inhibits dopamine and NE reuptake (NDRI); no serotonin effect → no sexual dysfunction | Bupropion (Wellbutrin) | Insomnia, seizure risk (dose-dependent; contraindicated in eating disorders); also for smoking cessation (Zyban); weight-neutral |
| **TCAs** | Block SERT + NET + muscarinic, histamine, α1 receptors → effective but more side effects | Amitriptyline, nortriptyline | Anticholinergic effects, sedation, orthostatic hypotension, cardiac conduction abnormalities (lethal in OD — Na⁺ channel blockade → wide QRS) |
| **MAOIs** | Inhibit monoamine oxidase → ↑ all monoamines. Very effective but last-line. | Phenelzine, tranylcypromine | **Tyramine crisis:** dietary tyramine → massive NE release → hypertensive emergency. Must avoid aged cheese, cured meats. Fatal serotonin syndrome with SSRIs. |

**Serotonin Syndrome:** Triad: altered mental status + autonomic instability (hyperthermia, tachycardia) + neuromuscular hyperactivity (clonus, rigidity, tremor). Caused by excess serotonergic activity (MAOI + SSRI most dangerous). Treatment: stop agent, cyproheptadine (serotonin antagonist), supportive care.

**Anxiolytics/Sedatives:**

| Class | Mechanism | Examples | Key Notes |
|---|---|---|---|
| **Benzodiazepines** | Positive allosteric modulators of GABA-A receptor → ↑ frequency of Cl⁻ channel opening → neuronal hyperpolarization. Require GABA present (unlike barbiturates). | Diazepam, alprazolam, lorazepam, midazolam | Rapid anxiolysis; also for seizures, alcohol withdrawal. Physical dependence in 2-4 weeks daily use; withdrawal can be fatal (seizures) → must taper. Flumazenil = reversal agent. Elderly: ↑ fall risk, cognitive impairment. |
| **Buspirone** | 5-HT1A partial agonist → anxiolytic without sedation/dependence | Buspirone | Takes 2-4 weeks; no abuse potential; good for GAD but patients used to benzo speed often disappointed |

**Antipsychotics:**

| Generation | Mechanism | Examples | Key Side Effects |
|---|---|---|---|
| **1st gen (typical)** | D2 receptor antagonism (mesolimbic → ↓ positive symptoms; also blocks D2 elsewhere → EPS) | Haloperidol, chlorpromazine | EPS: dystonia, akathisia, parkinsonism, tardive dyskinesia (irreversible). Hyperprolactinemia. **NMS:** rigidity, hyperthermia, ↑ CK — emergency. |
| **2nd gen (atypical)** | D2 + 5-HT2A antagonism → ↓ EPS risk; may help negative symptoms | Olanzapine, quetiapine, risperidone, aripiprazole (partial D2 agonist), clozapine | Metabolic syndrome (weight, diabetes, dyslipidemia). **Clozapine:** most effective; treatment-resistant schizophrenia; ↓ suicidality; requires blood monitoring for agranulocytosis (~1%). |

**Mood Stabilizers:**
- **Lithium:** Multiple mechanisms (inhibits GSK-3β, modulates inositol signaling, neuroprotective). Gold standard for bipolar; anti-suicidal. Narrow TI (~0.6-1.2 mEq/L); monitoring: thyroid, renal, levels. Dehydration/NSAIDs → toxicity.
- **Valproate:** ↑ GABA, blocks Na⁺ channels. Bipolar mania, seizures. Teratogenic (neural tube defects — avoid in women of childbearing age), hepatotoxicity, weight gain.
- **Lamotrigine:** Blocks Na⁺ channels → ↓ glutamate. Bipolar depression (better for depressive than manic poles). Must titrate slowly — Stevens-Johnson syndrome risk.

### Diabetes Drugs (Detailed)

| Class | Mechanism | Key Drug | Notes |
|---|---|---|---|
| **Metformin** | ↓ Hepatic glucose production (AMPK activation), ↑ insulin sensitivity, ↓ intestinal glucose absorption | Metformin | First-line T2D for decades; weight-neutral; GI side effects; lactic acidosis rare; may have longevity benefits (TAME trial) |
| **Sulfonylureas** | Bind SUR1 on β-cell K-ATP channels → close channels → depolarization → insulin secretion (glucose-independent) | Glipizide, glyburide, glimepiride | Hypoglycemia (major risk — acts regardless of glucose), weight gain; cheap |
| **GLP-1 receptor agonists** | Mimic incretin GLP-1: ↑ glucose-dependent insulin secretion, ↓ glucagon, slow gastric emptying, ↑ satiety (hypothalamic action) | Semaglutide (Ozempic/Wegovy), liraglutide, tirzepatide (dual GLP-1/GIP) | 15-22% weight loss; CV mortality benefit; pancreatitis risk (rare); GI side effects (nausea); ~$1000/month; thyroid C-cell tumors in rodents (not proven in humans) |
| **DPP-4 inhibitors** | Inhibit DPP-4 enzyme that degrades endogenous GLP-1/GIP → ↑ incretin levels | Sitagliptin, linagliptin | Weight-neutral; well-tolerated; modest efficacy; no CV benefit |
| **SGLT2 inhibitors** | See cardiovascular section | Empagliflozin, dapagliflozin | CV + renal benefits beyond glucose; revolutionary for HF/CKD |
| **Thiazolidinediones** | PPARγ agonists → ↑ adiponectin, ↑ insulin sensitivity in muscle/fat | Pioglitazone | Weight gain, fluid retention (contraindicated in HF), fracture risk; rosiglitazone restricted due to CV concerns |
| **Insulin** | Exogenous replacement. Rapid (lispro, aspart: onset 15 min, peak 1h), short (regular: onset 30 min, peak 2-4h), intermediate (NPH: 6-12h), long-acting (glargine, detemir: ~24h, peakless basal coverage) | Various | Always needed in T1D; sometimes in T2D. Hypoglycemia is main risk; weight gain. Insulin pump + CGM = "artificial pancreas" systems. |

### Biologics and Targeted Therapies

**Monoclonal Antibodies (naming: -mab):**
- Naming convention: -ximab (chimeric, mouse/human), -zumab (humanized), -mumab (fully human)
- **Adalimumab (Humira):** Anti-TNF-α; RA, Crohn's, psoriasis; was world's top-selling drug (~$20B/year); now has biosimilars
- **Pembrolizumab (Keytruda):** Anti-PD-1 checkpoint inhibitor; now world's top-selling drug; melanoma, lung, many cancers
- **Rituximab:** Anti-CD20 (B-cell surface); depletes B-cells; lymphoma, RA, some autoimmune diseases
- **Trastuzumab (Herceptin):** Anti-HER2; HER2+ breast cancer; transformed prognosis
- **Bevacizumab (Avastin):** Anti-VEGF; inhibits tumor angiogenesis; colorectal, lung, renal cancers
- **Dupilumab:** Anti-IL-4Rα; blocks IL-4/IL-13 signaling; atopic dermatitis, asthma
- **Natalizumab:** Anti-α4 integrin; blocks immune cell migration into CNS; multiple sclerosis (risk of PML)
- **Denosumab:** Anti-RANKL; blocks osteoclast activation; osteoporosis

**Small Molecule Targeted Therapies (naming: -nib = kinase inhibitor, -mib = proteasome inhibitor):**
- **Imatinib (Gleevec):** BCR-ABL tyrosine kinase inhibitor; CML 5-year survival 10% → 90%; poster child for targeted therapy
- **PARP inhibitors (olaparib):** Block DNA repair in BRCA-mutated cancers → synthetic lethality
- **JAK inhibitors (tofacitinib, baricitinib):** Block Janus kinases; RA, atopic dermatitis, myelofibrosis; risk of infections, VTE

---

## Drug Interactions (Comprehensive)

### Types of Drug Interactions

| Type | Mechanism | Example |
|---|---|---|
| **Pharmacokinetic (PK)** | One drug alters ADME of another | Rifampin induces CYP3A4 → ↓ oral contraceptive levels → contraceptive failure |
| **Pharmacodynamic (PD)** | Drugs have additive/synergistic/antagonistic effects at same or different targets | Benzodiazepine + opioid → additive respiratory depression (leading cause of overdose death) |
| **Drug-food** | Food alters drug absorption or metabolism | Grapefruit inhibits intestinal CYP3A4 → ↑ levels of statins, CCBs, cyclosporine |
| **Drug-disease** | Drug worsens pre-existing condition | NSAIDs in CKD → further renal impairment; β-blockers in severe asthma → bronchospasm |

### High-Risk Drug Interaction Table

| Combination | Mechanism | Consequence |
|---|---|---|
| **Warfarin + NSAIDs** | NSAIDs inhibit platelets + cause GI erosion; some inhibit CYP2C9 (warfarin metabolism) | Major GI bleeding |
| **ACE-I/ARB + K⁺-sparing diuretic + K⁺ supplement** | All ↑ potassium | Life-threatening hyperkalemia → arrhythmia |
| **SSRI/SNRI + MAOI** | Massive serotonin excess | Fatal serotonin syndrome (must have 14-day washout, 5 weeks for fluoxetine) |
| **Methotrexate + TMP-SMX** | Both are folate antagonists; TMP-SMX ↓ renal clearance of methotrexate | Pancytopenia, death |
| **Opioid + benzodiazepine + alcohol** | Additive CNS/respiratory depression | Respiratory arrest — FDA black box warning on co-prescription |
| **Statin (simvastatin) + CYP3A4 inhibitor (erythromycin, ketoconazole)** | ↑ Statin levels 5-20x | Rhabdomyolysis (muscle breakdown → myoglobin → renal failure) |
| **Clopidogrel + omeprazole** | Omeprazole inhibits CYP2C19 (needed to activate clopidogrel prodrug) | ↓ Antiplatelet effect → stent thrombosis; use pantoprazole instead |
| **Lithium + NSAIDs/ACE-I/diuretics** | All ↓ renal lithium clearance | Lithium toxicity (tremor → seizures → death) |
| **Metformin + IV contrast dye** | Contrast can cause AKI → metformin accumulates → lactic acidosis | Hold metformin 48h around contrast procedures |
| **Fluoroquinolone + antacid/iron/calcium** | Chelation in GI tract → ↓ quinolone absorption | Treatment failure; space by 2 hours |
| **Digoxin + amiodarone** | Amiodarone inhibits P-glycoprotein → ↓ digoxin clearance | Digoxin toxicity (nausea, arrhythmia, yellow vision) — halve digoxin dose |
| **QT-prolonging drugs combined** (macrolides, antipsychotics, fluoroquinolones, ondansetron, methadone) | Additive QT interval prolongation | Torsades de pointes (polymorphic ventricular tachycardia) → sudden cardiac death |

### Pharmacogenomic Interactions

| Gene | Drug Affected | Clinical Impact |
|---|---|---|
| CYP2D6 poor metabolizer | Codeine | Can't convert to morphine → no analgesia |
| CYP2D6 ultra-rapid metabolizer | Codeine | Excessive morphine production → respiratory depression/death (especially children) |
| CYP2C19 poor metabolizer | Clopidogrel | ↓ Active metabolite → ↑ stent thrombosis; use ticagrelor/prasugrel instead |
| CYP2C9 variants + VKORC1 | Warfarin | ↓ Metabolism + ↑ sensitivity → ↑ bleeding risk; FDA recommends genotype-guided dosing |
| HLA-B*5701 | Abacavir (HIV) | Severe hypersensitivity reaction; mandatory testing before prescribing |
| HLA-B*1502 | Carbamazepine | Stevens-Johnson syndrome; prevalent in SE Asian populations; test before prescribing |
| TPMT deficiency | Azathioprine/6-MP | Can't metabolize → severe myelosuppression → death; test before prescribing |

---

## Drug Development Pipeline

| Phase | Duration | Purpose | Success Rate |
|---|---|---|---|
| Discovery | 2-5 years | Target identification, lead optimization | — |
| Preclinical | 1-3 years | Animal safety/efficacy | ~50% proceed |
| Phase I | ~1 year | 20-100 healthy volunteers; safety, PK | ~70% proceed |
| Phase II | 1-3 years | 100-500 patients; efficacy, dosing | ~33% proceed |
| Phase III | 2-4 years | 1,000-5,000+ patients; confirmatory | ~25-30% proceed |
| FDA review | 6-18 months | NDA/BLA review | ~85% approved |
| Phase IV | Post-approval | Post-marketing surveillance | Ongoing |

**Total:** ~10-15 years, ~$1-2B per successful drug (including failures). Overall success rate ~5-10%.

### Generic vs Brand
- Brand: 20 years patent (usually 7-12 years market exclusivity after approval)
- Generic: ANDA (abbreviated application); bioequivalence study only; 80-85% cheaper
- **Biosimilars:** Generic equivalents for biologics; more complex approval (not identical copies)

### Off-Label Use (~20% of prescriptions)
- Gabapentin: approved for seizures; used for neuropathic pain, anxiety
- Metformin: approved for T2D; used for PCOS, weight management
- Trazodone: approved for depression; used mostly for insomnia
