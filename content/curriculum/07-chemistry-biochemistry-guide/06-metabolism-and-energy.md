# Metabolism and Energy

## Overview

Metabolism is the sum of all chemical reactions in organisms, extracting energy from nutrients and using it to build molecules and perform work. Understanding metabolic pathways—glycolysis, citric acid cycle, oxidative phosphorylation, and their interconnections—reveals how life captures, stores, transforms, and expends energy.

## Thermodynamics of Metabolism

### Energy and Life

**Living systems**:
- Maintain low entropy (high order) in a universe trending toward disorder
- Continuously expend energy to maintain organization
- Couple exergonic reactions (release energy) to endergonic reactions (require energy)

### Gibbs Free Energy in Biochemistry

**ΔG = ΔH - TΔS**

**Standard Free Energy (ΔG°')**:
- Standard conditions: pH 7 (not pH 0), 25°C, 1 M concentrations
- **ΔG°'** refers to biochemical standard state

**Relationship to Equilibrium**:
- **ΔG°' = -RT ln K**
  - R = 8.314 J/(mol·K)
  - T = temperature (K)
  - K = equilibrium constant

**Actual Free Energy**:
- **ΔG = ΔG°' + RT ln([products]/[reactants])**
- Cellular conditions differ from standard; ΔG differs from ΔG°'

### ATP: The Energy Currency

**Structure**: Adenosine + 3 phosphate groups
- Adenine base
- Ribose sugar
- Triphosphate chain (α, β, γ)

**ATP Hydrolysis**:
- ATP + H₂O → ADP + Pᵢ (inorganic phosphate)
- **ΔG°' = -7.3 kcal/mol** (under standard conditions)
- Actual cellular ΔG ≈ -12 kcal/mol (conditions far from equilibrium)

**Why ATP is High-Energy**:
1. **Electrostatic repulsion**: Negative charges on phosphates repel
2. **Resonance stabilization**: Products (ADP + Pᵢ) have more resonance forms than ATP
3. **Ionization**: Products ionize more readily at physiological pH
4. **Hydration**: Products bind water better (stabilizing)

**ATP Regeneration**:
- Humans hydrolyze and resynthesize body weight in ATP daily
- Coupled to exergonic reactions (glucose oxidation, photosynthesis)

### Other High-Energy Compounds

| Compound | ΔG°' (kcal/mol) | Function |
|----------|----------------|----------|
| Phosphoenolpyruvate (PEP) | -14.8 | Glycolysis intermediate |
| 1,3-Bisphosphoglycerate | -11.8 | Glycolysis intermediate |
| Creatine phosphate | -10.3 | Muscle energy buffer |
| ATP → ADP + Pᵢ | -7.3 | Energy currency |
| Glucose-6-phosphate | -3.3 | Glycolysis intermediate |

**Energy Coupling**: Reactions with ΔG > 0 coupled to ATP hydrolysis
- Example: Glucose + Pᵢ → Glucose-6-phosphate (ΔG°' = +3.3)
  - Non-spontaneous alone
  - Coupled with ATP hydrolysis: Net ΔG°' = -4.0 (spontaneous)

### Electron Carriers

**NAD⁺/NADH**:
- Nicotinamide adenine dinucleotide
- Derived from niacin (vitamin B₃)
- **NAD⁺ + 2e⁻ + H⁺ → NADH**
- Primary electron acceptor in catabolism

**FAD/FADH₂**:
- Flavin adenine dinucleotide
- Derived from riboflavin (vitamin B₂)
- **FAD + 2e⁻ + 2H⁺ → FADH₂**
- Stronger oxidizer than NAD⁺ (accepts electrons from less reduced compounds)

**NADP⁺/NADPH**:
- Structurally similar to NAD⁺ (extra phosphate)
- Primary electron donor in biosynthesis (anabolic reactions)
- Also used in photosynthesis

## Catabolism: Breaking Down for Energy

### Overview of Glucose Metabolism

**Complete Oxidation**:
- C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O
- **ΔG°' = -686 kcal/mol**
- Captured in ~32 ATP molecules (~240 kcal)
- Efficiency: ~35%

**Four Stages**:
1. **Glycolysis**: Glucose → 2 Pyruvate (cytoplasm)
2. **Pyruvate oxidation**: Pyruvate → Acetyl-CoA (mitochondrial matrix)
3. **Citric acid cycle**: Acetyl-CoA → CO₂ (mitochondrial matrix)
4. **Oxidative phosphorylation**: NADH, FADH₂ → ATP (inner mitochondrial membrane)

### Glycolysis

**Location**: Cytoplasm

**Overall Reaction**:
- Glucose + 2 NAD⁺ + 2 ADP + 2 Pᵢ → 2 Pyruvate + 2 NADH + 2 ATP + 2 H₂O

**Phases**:

**Phase 1: Energy Investment** (Steps 1-5)
- Glucose → Fructose-1,6-bisphosphate
- Consumes 2 ATP
- Phosphorylates and traps glucose in cell

**Phase 2: Energy Payoff** (Steps 6-10)
- Fructose-1,6-bisphosphate → 2 Pyruvate
- Generates 4 ATP (net: 2 ATP)
- Generates 2 NADH

**Key Steps**:

**Step 1**: Glucose → Glucose-6-phosphate
- Enzyme: Hexokinase
- Uses 1 ATP
- Traps glucose in cell (charged molecule can't cross membrane)

**Step 3**: Fructose-6-phosphate → Fructose-1,6-bisphosphate
- Enzyme: Phosphofructokinase (PFK)
- Uses 1 ATP
- **Rate-limiting step** (key regulatory point)

**Step 7**: 1,3-Bisphosphoglycerate → 3-Phosphoglycerate
- Enzyme: Phosphoglycerate kinase
- Generates 1 ATP per molecule (substrate-level phosphorylation)

**Step 10**: Phosphoenolpyruvate → Pyruvate
- Enzyme: Pyruvate kinase
- Generates 1 ATP per molecule

**Regulation**:
- PFK inhibited by: ATP, citrate (indicators of sufficient energy)
- PFK activated by: AMP, ADP (indicators of energy need)

### Fermentation (Anaerobic)

When O₂ unavailable, pyruvate reduced to regenerate NAD⁺:

**Lactic Acid Fermentation** (muscle, some bacteria):
- Pyruvate + NADH → Lactate + NAD⁺
- Allows glycolysis to continue without O₂
- Causes muscle fatigue (lactate accumulation)

**Alcoholic Fermentation** (yeast):
- Pyruvate → Acetaldehyde + CO₂
- Acetaldehyde + NADH → Ethanol + NAD⁺
- Used in brewing, baking

**Net ATP**: Only 2 ATP per glucose (from glycolysis)
- Far less efficient than aerobic respiration (~32 ATP)

### Pyruvate Oxidation

**Location**: Mitochondrial matrix

**Reaction**:
- Pyruvate + NAD⁺ + CoA → Acetyl-CoA + NADH + CO₂

**Enzyme Complex**: Pyruvate dehydrogenase
- Irreversible reaction
- Connects glycolysis to citric acid cycle
- Generates 1 NADH per pyruvate (2 per glucose)

**Coenzyme A (CoA)**:
- Carries acetyl group (2-carbon)
- High-energy thioester bond

### Citric Acid Cycle (Krebs Cycle)

**Location**: Mitochondrial matrix

**Overview**:
- Acetyl-CoA (2C) + Oxaloacetate (4C) → Citrate (6C)
- Citrate oxidized back to oxaloacetate
- Regenerates oxaloacetate (cyclic pathway)
- Completes glucose oxidation (produces CO₂)

**Net per Acetyl-CoA**:
- 3 NADH
- 1 FADH₂
- 1 GTP (≈ ATP)
- 2 CO₂

**Per Glucose** (2 acetyl-CoA):
- 6 NADH
- 2 FADH₂
- 2 GTP
- 4 CO₂

**Key Steps**:

**Step 1**: Acetyl-CoA + Oxaloacetate → Citrate
- Enzyme: Citrate synthase
- Condensation reaction

**Step 3**: Isocitrate → α-Ketoglutarate + CO₂ + NADH
- Enzyme: Isocitrate dehydrogenase
- **Rate-limiting step**
- Activated by ADP, Ca²⁺
- Inhibited by ATP, NADH

**Step 4**: α-Ketoglutarate → Succinyl-CoA + CO₂ + NADH
- Enzyme: α-Ketoglutarate dehydrogenase complex
- Similar to pyruvate dehydrogenase

**Step 5**: Succinyl-CoA → Succinate + GTP
- Enzyme: Succinyl-CoA synthetase
- Substrate-level phosphorylation

**Step 6**: Succinate → Fumarate + FADH₂
- Enzyme: Succinate dehydrogenase
- Only enzyme embedded in inner membrane
- Part of Complex II in electron transport chain

**Regulation**:
- Activated by: ADP, Ca²⁺ (energy demand, muscle contraction)
- Inhibited by: ATP, NADH (energy sufficiency)

### Oxidative Phosphorylation

**Location**: Inner mitochondrial membrane

**Components**:
1. **Electron Transport Chain** (Complexes I-IV)
2. **ATP Synthase** (Complex V)

**Electron Transport Chain**:

**Complex I**: NADH dehydrogenase
- NADH → NAD⁺ + 2e⁻
- Pumps 4 H⁺ to intermembrane space

**Complex II**: Succinate dehydrogenase
- FADH₂ → FAD + 2e⁻
- Does not pump H⁺
- Electrons enter at lower energy than Complex I

**Complex III**: Cytochrome bc₁
- Pumps 4 H⁺

**Complex IV**: Cytochrome c oxidase
- Transfers electrons to O₂ (final electron acceptor)
- O₂ + 4e⁻ + 4H⁺ → 2H₂O
- Pumps 2 H⁺

**Chemiosmotic Theory** (Peter Mitchell):

1. Electron transport pumps H⁺ from matrix to intermembrane space
2. Creates electrochemical gradient (proton-motive force)
3. H⁺ flow back through ATP synthase drives ATP synthesis
4. **Coupling**: Electron transport coupled to ATP synthesis via gradient

**ATP Synthase**:
- F₀ portion: Proton channel in membrane
- F₁ portion: Catalytic subunit in matrix
- Rotary mechanism: H⁺ flow rotates central shaft, changing conformation of active sites
- Synthesizes ATP: ADP + Pᵢ → ATP

**ATP Yield**:
- 1 NADH → ~2.5 ATP
- 1 FADH₂ → ~1.5 ATP
- **Total per glucose**: ~32 ATP (varies by shuttle system)

**Breakdown**:
- Glycolysis: 2 ATP + 2 NADH (→ 5 ATP total)
- Pyruvate oxidation: 2 NADH (→ 5 ATP)
- Citric acid cycle: 2 GTP + 6 NADH + 2 FADH₂ (→ 20 ATP)
- **Total**: ~32 ATP

### Other Fuel Molecules

**Fats (Triacylglycerols)**:

**β-Oxidation**:
- Fatty acids broken into 2-carbon acetyl-CoA units
- Each cycle: 1 FADH₂ + 1 NADH
- Acetyl-CoA enters citric acid cycle

**Example**: Palmitic acid (16C)
- 7 cycles → 8 Acetyl-CoA
- Generates: 7 FADH₂, 7 NADH, 8 Acetyl-CoA
- Total: ~108 ATP (more than double glucose per carbon)

**Proteins (Amino Acids)**:
- Deamination removes amino group (→ urea)
- Carbon skeleton enters metabolism at various points:
  - Pyruvate
  - Acetyl-CoA
  - Citric acid cycle intermediates

**Glycogenic** amino acids → glucose (via gluconeogenesis)
**Ketogenic** amino acids → ketone bodies or acetyl-CoA

## Anabolism: Building Up

### Biosynthesis Requires Energy

Most biosynthetic pathways:
- Endergonic (ΔG > 0)
- Driven by ATP hydrolysis or NADPH oxidation
- Often not simply reversal of catabolism

### Gluconeogenesis

**Synthesis of glucose from non-carbohydrate precursors**

**Substrates**:
- Lactate (from muscle)
- Glycerol (from fat)
- Amino acids (from protein)
- Pyruvate, oxaloacetate

**Location**: Primarily liver, some kidney

**Pathway**: Essentially reverses glycolysis with 4 different enzymes to bypass irreversible steps
- Uses 6 ATP equivalents per glucose

**Regulation**:
- Reciprocally regulated with glycolysis
- Activated when blood glucose low
- Hormones: Glucagon activates; insulin inhibits

### Fatty Acid Synthesis

**Location**: Cytoplasm (differs from β-oxidation in mitochondria)

**Precursor**: Acetyl-CoA
- Transported from mitochondria as citrate

**Enzyme**: Fatty acid synthase (multi-enzyme complex)

**Process**:
- Adds 2 carbons per cycle
- Requires NADPH (from pentose phosphate pathway)
- Produces palmitate (16C saturated fatty acid)
- Further elongated and desaturated by other enzymes

**Energy Cost**: 7 ATP + 14 NADPH per palmitate

**Regulation**:
- Activated by: Insulin, high carbohydrate intake
- Inhibited by: Glucagon, epinephrine, high fatty acid levels

### Amino Acid Synthesis

**Essential amino acids**: Must be obtained from diet (9 in humans)
- Histidine, isoleucine, leucine, lysine, methionine, phenylalanine, threonine, tryptophan, valine

**Non-essential amino acids**: Can be synthesized
- Often from citric acid cycle intermediates
- Example: α-Ketoglutarate → Glutamate → Glutamine, Proline, Arginine

### Nucleotide Synthesis

**De novo synthesis**:
- Purines: Built on ribose-5-phosphate scaffold
- Pyrimidines: Ring synthesized first, then attached to ribose

**Salvage pathways**:
- Recycle bases from nucleotide degradation
- Less energy-intensive than de novo

**Regulation**:
- Feedback inhibition by end products
- Balanced synthesis of purines and pyrimidines

## Metabolic Integration and Regulation

### Key Regulatory Enzymes

**Glycolysis**: Phosphofructokinase (PFK)
**Citric Acid Cycle**: Isocitrate dehydrogenase
**Gluconeogenesis**: Fructose-1,6-bisphosphatase
**Fatty Acid Synthesis**: Acetyl-CoA carboxylase
**β-Oxidation**: Carnitine palmitoyltransferase I

### Allosteric Regulation

**Feedback Inhibition**: End product inhibits early enzyme
- Example: ATP inhibits PFK

**Feedforward Activation**: Substrate activates downstream enzyme
- Example: AMP activates PFK

**Energy Charge**: [ATP] + 0.5[ADP]) / ([ATP] + [ADP] + [AMP])
- High energy charge: Inhibit catabolism, activate anabolism
- Low energy charge: Activate catabolism, inhibit anabolism

### Hormonal Regulation

**Insulin** (fed state):
- Promotes glucose uptake
- Activates glycolysis, fatty acid synthesis, protein synthesis
- Inhibits gluconeogenesis, β-oxidation

**Glucagon** (fasting state):
- Promotes glucose release
- Activates gluconeogenesis, β-oxidation
- Inhibits glycolysis, fatty acid synthesis

**Epinephrine** (stress/exercise):
- Mobilizes glucose (glycogen breakdown)
- Activates lipolysis (fat breakdown)

### Tissue-Specific Metabolism

**Brain**:
- Obligate glucose user (normally)
- Can use ketone bodies during prolonged fasting
- High energy demand (~20% of resting metabolism)

**Muscle**:
- Uses glucose and fatty acids
- Stores glycogen for intense activity
- Produces lactate during anaerobic exercise

**Liver**:
- Metabolic hub
- Gluconeogenesis, glycogen storage
- Fatty acid synthesis and oxidation
- Amino acid metabolism, urea synthesis
- Detoxification

**Adipose Tissue**:
- Fat storage (triacylglycerols)
- Hormone production (leptin, adiponectin)
- Lipolysis releases fatty acids during fasting

### Metabolic States

**Fed State** (post-meal):
- High insulin
- Glucose uptake, glycogen synthesis
- Lipid synthesis
- Protein synthesis

**Fasting State**:
- High glucagon
- Glycogen breakdown
- Gluconeogenesis
- Fat oxidation

**Starvation**:
- Extended gluconeogenesis (using amino acids)
- Ketone body production (from fat)
- Muscle protein breakdown
- Brain adapts to use ketones

---

## Key Terms

- **Metabolism**: Sum of all chemical reactions in organism
- **Catabolism**: Breaking down molecules for energy
- **Anabolism**: Building molecules from precursors
- **ATP**: Adenosine triphosphate; energy currency
- **Glycolysis**: Glucose → pyruvate; produces ATP, NADH
- **Citric acid cycle**: Acetyl-CoA oxidation; produces CO₂, NADH, FADH₂
- **Oxidative phosphorylation**: Electron transport + ATP synthesis
- **Electron transport chain**: Series of redox reactions pumping H⁺
- **Chemiosmotic coupling**: H⁺ gradient drives ATP synthesis
- **Gluconeogenesis**: Synthesizing glucose from non-carbohydrate sources
- **β-Oxidation**: Breaking fatty acids into acetyl-CoA units

---

## Summary

Metabolism encompasses all cellular chemical reactions, divided into catabolism (energy-releasing) and anabolism (energy-requiring). ATP serves as the universal energy currency, with ΔG°' = -7.3 kcal/mol for hydrolysis. Glucose catabolism proceeds through glycolysis (cytoplasm), pyruvate oxidation, citric acid cycle (mitochondrial matrix), and oxidative phosphorylation (inner mitochondrial membrane), yielding ~32 ATP. Electron transport chains pump protons, creating gradients that drive ATP synthase. Fats undergo β-oxidation, producing more ATP per carbon than carbohydrates. Anabolic pathways—gluconeogenesis, fatty acid synthesis, amino acid and nucleotide synthesis—require ATP and NADPH. Metabolism is tightly regulated through allosteric control, covalent modification, and hormonal signaling (insulin, glucagon, epinephrine), ensuring appropriate responses to fed, fasting, and stress states. Different tissues specialize: brain demands glucose, muscle stores glycogen, liver performs gluconeogenesis, adipose stores fat. Understanding metabolism reveals how organisms capture energy from nutrients, store it efficiently, and allocate it to maintain life's complex organization.
