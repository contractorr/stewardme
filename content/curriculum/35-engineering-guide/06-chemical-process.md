# Chemical and Process Engineering

## Overview

Chemical engineering applies chemistry, physics, and mathematics to transform raw materials into useful products at industrial scale. It's the discipline that takes laboratory reactions and scales them to factories producing millions of tons annually—from petroleum refining to pharmaceuticals, polymers to fertilizers. Process engineering, closely related, optimizes manufacturing operations across industries. Together, they enable the material abundance of modern life.

## Fundamentals

### Mass and Energy Balances

**Conservation principles**: Foundation of process analysis

**Mass balance**: Mass in = Mass out + Accumulation
- **Steady state**: Accumulation = 0
- Input streams = Output streams

**Energy balance**: Energy in = Energy out + Accumulation
- Includes: Enthalpy (heat content), kinetic energy, potential energy, work

**Example - Distillation column**:
- Feed: 1000 kg/hr ethanol-water mixture (40% ethanol)
- Products: Distillate (90% ethanol), bottoms (5% ethanol)
- **Mass balance** determines product flow rates
- **Energy balance** determines heat requirements (reboiler, condenser)

### Transport Phenomena

**Three fundamental transport processes**:

**Momentum transport** (Fluid mechanics):
- Viscous flow in pipes
- Pressure drop calculations
- Pump/compressor sizing

**Heat transport**:
- Conduction: Fourier's law (q = -kA dT/dx)
- Convection: Newton's cooling law (q = hA ΔT)
- Radiation: Stefan-Boltzmann law (q = σA T⁴)
- **Heat exchangers**: Transfer heat between fluids

**Mass transport**:
- Diffusion: Fick's law
- Convective mass transfer
- **Separation processes**: Distillation, absorption, extraction

### Reaction Engineering

**Chemical reactor**: Vessel where reactions occur

**Design objectives**:
- **Conversion**: Fraction of reactant converted to product
- **Selectivity**: Desired product vs. byproducts
- **Yield**: Product obtained per reactant fed

**Reactor types**:

**Batch**: Reactants added, allowed to react, then emptied
- Flexible (different products)
- Labor-intensive, low throughput
- **Pharma, specialty chemicals**

**Continuous Stirred-Tank Reactor (CSTR)**:
- Continuous feed and removal
- Well-mixed (uniform composition)
- Multiple CSTRs in series for higher conversion

**Plug Flow Reactor (PFR)**:
- Tubular, continuous flow
- Composition changes along length
- Higher conversion than CSTR for same volume
- **Petrochemicals, large-scale production**

**Packed bed**: Catalyst packed in tube, fluid flows through
- Heterogeneous catalysis
- Large surface area

**Fluidized bed**: Fluid (gas or liquid) passes upward through solid particles
- Excellent heat transfer, mixing
- **Catalytic cracking, combustion**

**Kinetics**: Reaction rate equations
- Arrhenius equation: k = A e^(-Ea/RT)
  - Rate increases exponentially with temperature
- Catalyst: Lowers activation energy Ea

## Unit Operations

Chemical plants composed of modular **unit operations**—standardized processing steps

### Separation Processes

**Distillation**: Separate based on boiling point differences
- Most common separation in chemical industry
- Vapor rises through trays/packing, liquid flows down
- Light components concentrate in vapor (top), heavy in liquid (bottom)
- **Energy-intensive** (reboiler heats, condenser cools)

**Crude oil distillation**:
- Atmospheric tower: Separate into fractions (gases, gasoline, diesel, etc.)
- Vacuum tower: Further process heavy residue

**Absorption**: Gas dissolved into liquid
- **Scrubbing**: Remove pollutants (SO₂, CO₂) from exhaust
- **Sour gas treatment**: Remove H₂S, CO₂ from natural gas

**Extraction**: Transfer component from one liquid phase to another
- Requires immiscible solvents
- **Caffeine removal**: Supercritical CO₂ extracts caffeine from coffee

**Crystallization**: Precipitate pure solid from solution
- **Purification**: Pharmaceuticals, minerals

**Membrane separation**: Selective permeation through membrane
- **Reverse osmosis**: Desalination (water purification)
- **Gas separation**: O₂/N₂, CO₂ removal
- Lower energy than distillation (for appropriate applications)

### Heat Exchange

**Shell-and-tube heat exchanger**: Most common type
- One fluid through tubes, other around tubes (shell side)
- Tube-side: High pressure, corrosive, or fouling fluids
- Shell-side: Low pressure, clean fluids

**Plate heat exchanger**: Corrugated plates with gaskets
- Compact, efficient
- Easy to clean
- **Food processing, HVAC**

**Design considerations**:
- Heat transfer coefficient (U)
- Log-mean temperature difference (LMTD)
- **Area required**: Q = UA LMTD
- Pressure drop
- Fouling (deposits reduce performance)

### Reaction Engineering Applications

**Haber-Bosch process** (Ammonia synthesis):
- N₂ + 3H₂ → 2NH₃
- High pressure (150-300 atm), moderate temperature (400-500°C)
- Iron catalyst
- **Feeds 50% of humanity** (fertilizer)
- **Most important industrial chemical process**

**Cracking**: Break large hydrocarbons into smaller (gasoline, ethylene)
- Thermal or catalytic
- Zeolite catalysts
- Fluidized bed reactors

**Polymerization**: Small molecules (monomers) → long chains (polymers)
- Polyethylene, polypropylene, PVC
- Batch or continuous
- Control molecular weight distribution

## Industrial Processes

### Petroleum Refining

**Crude oil**: Complex mixture of hydrocarbons

**Refining steps**:

1. **Desalting**: Remove salt, water (prevent corrosion)

2. **Distillation**: Separate into fractions
   - Gases (C1-C4)
   - Naphtha (C5-C9, gasoline range)
   - Kerosene (C10-C14, jet fuel)
   - Diesel (C15-C18)
   - Heavy gas oil (C19-C25)
   - Residue (>C25, asphalt, fuel oil)

3. **Conversion**: Break large molecules
   - **Fluid Catalytic Cracking (FCC)**: Heavy oil → gasoline, olefins
   - **Hydrocracking**: Add hydrogen, crack to diesel/jet fuel
   - **Coking**: Residue → lighter products + solid coke

4. **Treatment**: Remove sulfur, nitrogen
   - **Hydrotreating**: React with H₂ over catalyst (desulfurization)
   - Environmental regulations drive low-sulfur fuels

5. **Blending**: Mix to meet specifications
   - Gasoline: Octane rating, vapor pressure, additives
   - Diesel: Cetane number, cloud point

**Refinery complexity**: 20-50 major unit operations, 1000s of pipes and vessels

**Capacity**: 100,000-500,000 barrels/day (large refinery)

### Petrochemicals

**Feedstocks**: Naphtha, ethane, propane from refining

**Steam cracking**: Produce ethylene, propylene (building blocks)
- Heat to 800-900°C
- **Ethylene**: World's largest organic chemical (150M tons/year)
  - → Polyethylene (plastics), ethylene oxide, ethylene glycol (antifreeze)
- **Propylene**: → Polypropylene, propylene oxide

**Aromatics**: Benzene, toluene, xylenes (BTX)
- From catalytic reforming
- → Styrene, phenol, polyester, nylon

**Polymerization plants**: Convert olefins to polymers
- Control conditions (temperature, pressure, catalyst) for desired properties
- Molecular weight, density, branching affect final properties

### Pharmaceuticals

**Batch processes**: Flexibility for multiple products, small quantities

**Steps**:
1. **API synthesis** (Active Pharmaceutical Ingredient): Multi-step organic reactions
2. **Purification**: Crystallization, chromatography (very high purity required)
3. **Formulation**: Mix with excipients (binders, fillers, coatings)
4. **Tablet pressing or encapsulation**
5. **Quality control**: Test every batch (identity, purity, potency)

**Regulatory**: FDA approval requires demonstrated safety, efficacy, manufacturing consistency

**Challenges**:
- Complex synthesis (10-20 steps typical)
- High purity requirements (99.9%+)
- Scale-up from lab to manufacturing
- Chiral molecules (one form active, other may be harmful)

**Biologics** (proteins, antibodies): Produced in living cells
- Fermentation (grow cells in bioreactor)
- Downstream processing (purify protein)
- More complex than small molecules

### Chemical Plants: Safety and Scale

**Inherent hazards**:
- Flammable, toxic, corrosive chemicals
- High temperatures and pressures
- Exothermic reactions (runaway risk)

**Safety layers**:
1. **Process design**: Inherently safer (lower pressure/temperature if possible)
2. **Engineering controls**: Pressure relief valves, interlocks, alarms
3. **Administrative controls**: Procedures, training
4. **Personal protective equipment**: Last line of defense

**Process Safety Management** (PSM):
- Hazard analysis (HAZOP, FMEA)
- Mechanical integrity (inspection, testing)
- Operating procedures
- Training
- Incident investigation

**Disasters**:
- **Bhopal** (India, 1984): Methyl isocyanate release, 3,800+ killed
- **Texas City** (2005): Refinery explosion, 15 killed
- **Lessons**: Process safety critical; complacency deadly

## Process Control

### Control Systems

**Goal**: Maintain process variables (temperature, pressure, flow, composition) at setpoints

**Feedback control**: Measure output, adjust input
- **PID controller**: Standard (see Electrical Engineering chapter)

**Cascade control**: Inner and outer loops
- Faster inner loop handles disturbances
- **Example**: Reactor temperature (outer) controls cooling water valve; cooling water flow (inner) controls pump

**Feedforward control**: Measure disturbance, adjust before affects output
- **Example**: If feed flow increases, increase cooling preemptively

**Distributed Control System (DCS)**: Computer system controlling entire plant
- 100s-1000s of control loops
- Operator interface (HMI): Graphics showing plant status
- Historical data logging

### Process Optimization

**Objectives**:
- **Maximize**: Yield, throughput, profit
- **Minimize**: Energy consumption, waste, cost
- Subject to: Constraints (equipment limits, safety, environmental)

**Techniques**:
- **Mathematical programming**: Linear programming, nonlinear optimization
- **Simulation**: Model plant, test scenarios without risks
- **Model predictive control** (MPC): Optimize over future time horizon

**Energy integration**: Heat exchange network design
- Use hot streams to heat cold streams (reduce external heating/cooling)
- **Pinch analysis**: Systematic method for maximum energy recovery
- **Payback**: Often <2 years from energy savings

## Environmental Engineering

### Pollution Control

**Air pollution**:
- **Particulates**: Cyclones, electrostatic precipitators, baghouses
- **SO₂**: Scrubbing with limestone slurry (forms gypsum)
- **NOₓ**: Selective catalytic reduction (SCR)—inject ammonia over catalyst
- **VOCs** (Volatile Organic Compounds): Thermal oxidation, adsorption

**Water treatment** (industrial wastewater):
- **Biological**: Activated sludge (like municipal, but industrial strengths)
- **Chemical**: Precipitation, coagulation
- **Membranes**: Ultrafiltration, reverse osmosis
- **Advanced oxidation**: UV + H₂O₂ destroys recalcitrant organics

**Solid waste**:
- **Incineration**: Reduce volume, recover energy (requires air pollution control)
- **Landfill**: For non-hazardous
- **Hazardous waste**: Special disposal (secure landfills, deep well injection, detoxification)

### Green Chemistry

**Principles**:
1. **Prevention**: Prevent waste rather than treat
2. **Atom economy**: Incorporate all reactants into product
3. **Less hazardous synthesis**: Benign reagents
4. **Safer solvents**: Water, supercritical CO₂ vs. toxic organics
5. **Energy efficiency**: Room temperature/pressure if possible
6. **Renewable feedstocks**: Biomass vs. petroleum
7. **Catalysis**: Enable lower temperatures, higher selectivity
8. **Degradable products**: Don't persist in environment
9. **Real-time monitoring**: Detect problems immediately
10. **Safer chemistry**: Prevent accidents

**Bio-based chemicals**: Shift from petroleum to renewable feedstocks
- Ethanol from corn/cellulose
- Polylactic acid (PLA) from corn starch (biodegradable plastic)
- Biodiesel from vegetable oil

## Real-World Case Studies

### Ammonia Plant (Haber-Bosch)

**Capacity**: 1,000 tons/day (typical)

**Process**:
1. **Hydrogen production**: Steam reforming of natural gas
   - CH₄ + H₂O → CO + 3H₂ (reformer, 800-900°C)
   - CO + H₂O → CO₂ + H₂ (shift reactors)
   - Remove CO₂ (absorption)
2. **Nitrogen**: Air separation unit (cryogenic distillation)
3. **Compression**: 150-300 bar
4. **Synthesis**: N₂ + 3H₂ → 2NH₃ (400-500°C, iron catalyst)
   - Only ~15% conversion per pass (equilibrium limited)
   - Separate ammonia, recycle unconverted gas
5. **Refrigeration**: Condense ammonia (-33°C at 1 atm)

**Energy**: 28-30 GJ/ton NH₃ (modern plant)
- Natural gas: 75% feedstock, 25% fuel

**Economics**: Energy dominates cost (80%+)

### Ethylene Plant

**Feedstock**: Ethane (from natural gas) or naphtha (from oil)

**Steam cracker**:
- Mix with steam (dilutes, reduces coking)
- Heat to 800-900°C in furnace tubes (radiant section)
- Rapid quench (stop reactions)
- **Yields**: Ethylene (major), propylene, butadiene, aromatics, H₂, CH₄

**Separation train**: Multiple distillation columns
- Compression (remove water, acids)
- Demethanizer (remove H₂, CH₄)
- Deethanizer (separate C₂s)
- C₂ splitter (separate ethylene from ethane)
- Propylene recovery
- **C₂ splitter challenge**: Ethylene/ethane very close boiling points (6°C difference)
  - Requires 100+ trays, high reflux ratio
  - Most energy-intensive column in petrochemicals

**Capacity**: 1-2 million tons/year ethylene (world-scale plant)

**Economics**: Economies of scale—larger plants more efficient

### Wastewater Treatment Plant

**Industrial wastewater** from chemical plant:

**Characterization**:
- COD (Chemical Oxygen Demand): Organic content
- BOD (Biochemical Oxygen Demand): Biodegradable organics
- pH, suspended solids, toxics

**Treatment**:
1. **Equalization**: Dampen flow/concentration variations
2. **Neutralization**: Adjust pH (6-9 for biological)
3. **Primary treatment**: Settling (remove solids)
4. **Biological treatment**: Activated sludge
   - Bacteria consume organics
   - Aeration basin (provide O₂)
   - Clarifier (separate sludge, return some)
5. **Tertiary treatment** (if needed):
   - Nitrification/denitrification (remove nitrogen)
   - Phosphorus removal
   - Activated carbon (organics)
6. **Sludge treatment**: Thicken, digest, dewater

**Discharge**: Must meet permit limits (EPA/state regulations)

**Cost**: $1-3/m³ treated (typical industrial)

## Key Terms

| Term | Definition |
|------|------------|
| **Unit operation** | Standard processing step (distillation, filtration, etc.) |
| **Mass balance** | Input mass = Output mass + Accumulation |
| **Heat exchanger** | Transfers heat between fluids |
| **Distillation** | Separation based on boiling point |
| **Reactor** | Vessel where chemical reaction occurs |
| **Catalyst** | Speeds reaction without being consumed |
| **Conversion** | Fraction of reactant converted |
| **Selectivity** | Desired product vs. byproducts ratio |
| **Cracking** | Breaking large molecules into smaller |
| **Polymerization** | Joining monomers into polymer chains |
| **DCS** | Distributed Control System (plant automation) |

## Summary

Chemical engineering transforms raw materials into products at industrial scale through unit operations—distillation, reaction, heat exchange, separation—combined into complex processes. Mass and energy balances, transport phenomena (momentum, heat, mass), and reaction kinetics provide the quantitative foundation for design and optimization.

Petroleum refining separates crude oil into fractions, then converts heavy molecules through cracking while removing sulfur. Petrochemical plants produce building blocks (ethylene, propylene, aromatics) for polymers dominating modern materials. Pharmaceutical manufacturing synthesizes complex molecules at high purity under stringent regulations. The Haber-Bosch process produces ammonia feeding billions through fertilizer.

Process control maintains operations safely within specifications using feedback loops, cascades, and distributed control systems. Environmental engineering controls emissions—air pollutants scrubbed, wastewater biologically treated—while green chemistry principles guide toward inherently cleaner processes using renewable feedstocks and benign solvents.

Scale separates chemical engineering from chemistry—reactions feasible in flasks may be uneconomical or unsafe at thousands of tons per day. Engineers optimize for yield, selectivity, energy efficiency, and safety while navigating thermodynamic constraints and economic realities. From refining petroleum to synthesizing pharmaceuticals, chemical engineering enables the material abundance and chemical products modern civilization depends on.
