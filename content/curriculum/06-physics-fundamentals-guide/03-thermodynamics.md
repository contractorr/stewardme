# Thermodynamics

## Overview

Thermodynamics is the study of heat, energy, and work, and how they interconvert. It governs everything from engines and refrigerators to stars and living organisms. Developed during the Industrial Revolution to understand steam engines, thermodynamics now underpins chemistry, biology, cosmology, and information theory. Unlike mechanics, which focuses on individual particles, thermodynamics deals with macroscopic systems containing vast numbers of particles, using statistical averages rather than tracking each molecule.

## Temperature and Heat

### Temperature

**Definition**: Measure of average kinetic energy of particles in a substance.

**Temperature Scales**:

| Scale | Freezing Point of Water | Boiling Point of Water | Absolute Zero |
|-------|-------------------------|------------------------|---------------|
| **Celsius** (°C) | 0°C | 100°C | -273.15°C |
| **Fahrenheit** (°F) | 32°F | 212°F | -459.67°F |
| **Kelvin** (K) | 273.15 K | 373.15 K | 0 K |

**Conversions**:
- K = °C + 273.15
- °F = (9/5)°C + 32
- °C = (5/9)(°F - 32)

**Absolute Zero** (0 K = -273.15°C): The lowest possible temperature where particles have minimum kinetic energy. Nothing can be cooled below this point (third law of thermodynamics).

### Heat

**Definition**: Energy transferred between systems due to temperature difference.

**Symbol**: Q

**Unit**: Joule (J), or calorie (1 cal = 4.184 J)

**Direction**: Heat flows spontaneously from hot to cold, never the reverse without external work.

### Thermal Equilibrium

**Definition**: State where two systems in contact have the same temperature and no net heat flow occurs.

**Zeroth Law of Thermodynamics**: If system A is in thermal equilibrium with system C, and system B is in thermal equilibrium with system C, then A and B are in thermal equilibrium with each other. This allows us to define temperature consistently.

### Heat Capacity and Specific Heat

**Heat Capacity (C)**: Amount of heat needed to raise temperature of an object by 1 K.

**Specific Heat (c)**: Heat capacity per unit mass.

**Formula**: Q = mcΔT
- Q = heat transferred (J)
- m = mass (kg)
- c = specific heat (J/kg⋅K)
- ΔT = temperature change (K or °C)

**Specific Heat Values**:
| Material | Specific Heat (J/kg⋅K) |
|----------|----------------------|
| Water | 4,186 |
| Ice | 2,090 |
| Steam | 2,010 |
| Aluminum | 897 |
| Copper | 385 |
| Iron | 449 |
| Air | 1,005 |

**Example**: How much energy to heat 2 kg of water from 20°C to 100°C?
- Q = mcΔT = (2)(4,186)(80) = 669,760 J ≈ 670 kJ

### Phase Changes

When substances change phase (solid ↔ liquid ↔ gas), temperature remains constant while heat is added or removed.

**Latent Heat**: Energy required for phase change per unit mass.

**Heat of Fusion** (Lf): Solid ↔ liquid
- Water: Lf = 334,000 J/kg

**Heat of Vaporization** (Lv): Liquid ↔ gas
- Water: Lv = 2,260,000 J/kg

**Formula**: Q = mL

**Example**: Energy to melt 1 kg of ice at 0°C?
- Q = mLf = (1)(334,000) = 334 kJ

## Heat Transfer Mechanisms

### 1. Conduction

**Definition**: Heat transfer through direct contact; energy passed from molecule to molecule.

**Mechanism**: Faster-moving molecules collide with slower neighbors, transferring kinetic energy.

**Formula**: Q/t = kA(TH - TC)/d
- k = thermal conductivity (W/m⋅K)
- A = cross-sectional area
- TH, TC = hot and cold temperatures
- d = thickness

**Good Conductors**: Metals (copper, aluminum, iron)
**Poor Conductors (Insulators)**: Wood, plastic, air, fiberglass

**Examples**:
- Metal spoon getting hot in coffee
- Heat spreading through a frying pan
- Touching ice feels cold (heat conducted away from your hand)

### 2. Convection

**Definition**: Heat transfer through fluid (liquid or gas) motion.

**Mechanism**: Hot fluid expands, becomes less dense, rises; cool fluid sinks, creating circulation.

**Types**:
- **Natural convection**: Driven by buoyancy (density differences)
- **Forced convection**: Driven by pumps, fans, wind

**Examples**:
- Boiling water: hot water rises from bottom
- Ocean currents distributing heat globally
- Room heating: warm air rises from radiator
- Wind chill: moving air carries away body heat faster

### 3. Radiation

**Definition**: Heat transfer through electromagnetic waves; doesn't require a medium.

**Mechanism**: All objects emit electromagnetic radiation based on temperature.

**Stefan-Boltzmann Law**: P = σAT⁴
- P = radiated power (W)
- σ = 5.67 × 10⁻⁸ W/m²⋅K⁴ (Stefan-Boltzmann constant)
- A = surface area
- T = absolute temperature (K)

**Examples**:
- Feeling warmth from sunlight (travels through vacuum of space)
- Infrared heaters
- Thermal imaging cameras
- Cooling of Earth by radiating heat to space

## The Four Laws of Thermodynamics

### Zeroth Law (Temperature Definition)

**Statement**: If two systems are in thermal equilibrium with a third, they are in equilibrium with each other.

**Significance**: Establishes temperature as a well-defined, transitive property. Allows thermometers to work.

### First Law (Energy Conservation)

**Statement**: Energy cannot be created or destroyed, only converted from one form to another.

**Formula**:
```
ΔU = Q - W
```

Where:
- ΔU = change in internal energy of system
- Q = heat added to system
- W = work done by system

**Sign Conventions**:
- Q > 0: heat added to system
- Q < 0: heat removed from system
- W > 0: system does work on surroundings (expansion)
- W < 0: surroundings do work on system (compression)

**Alternative form**: Q = ΔU + W (heat added equals internal energy increase plus work done)

**Meaning**: The energy of the universe is constant. Energy can flow as heat or work, but total energy is conserved.

**Example**: Gas in cylinder heated with 500 J while expanding and doing 200 J of work.
- Q = +500 J (heat added)
- W = +200 J (work by system)
- ΔU = 500 - 200 = 300 J (internal energy increases)

### Second Law (Entropy)

**Statement** (multiple equivalent formulations):
1. **Clausius**: Heat cannot spontaneously flow from cold to hot
2. **Kelvin-Planck**: No heat engine can be 100% efficient
3. **Entropy**: In an isolated system, entropy never decreases

**Formula**: ΔS ≥ 0 (for isolated systems)

**Entropy (S)**: Measure of disorder or number of microscopic configurations.

**Meaning**:
- Natural processes increase total entropy
- Organized systems tend toward disorder
- Time has a direction (arrow of time)
- Perfect efficiency is impossible

**Real-World Examples**:
- Ice melts in warm room (never spontaneously freezes)
- Perfume disperses throughout room (never reconcentrates)
- Broken glass doesn't reassemble itself
- Coffee cools to room temperature
- Stars radiate energy and increase universal entropy

### Third Law (Absolute Zero)

**Statement**: As temperature approaches absolute zero (0 K), the entropy of a perfect crystal approaches a constant minimum (often taken as zero).

**Meaning**:
- Absolute zero cannot be reached in finite steps
- At 0 K, particles are in ground state with minimal uncertainty
- Provides absolute reference point for entropy

**Practical Implication**: Lowest achieved temperature is about 10⁻¹⁰ K, but 0 K is unattainable.

## Thermodynamic Processes

Systems can undergo various processes. Key variables: Pressure (P), Volume (V), Temperature (T).

### Types of Processes

| Process | What's Constant | Characteristics |
|---------|----------------|-----------------|
| **Isothermal** | Temperature (T) | ΔU = 0, Q = W |
| **Adiabatic** | No heat transfer (Q = 0) | ΔU = -W, temperature changes |
| **Isobaric** | Pressure (P) | W = PΔV |
| **Isochoric** | Volume (V) | W = 0, Q = ΔU |

### Ideal Gas Law

**Formula**: PV = nRT
- P = pressure (Pa)
- V = volume (m³)
- n = number of moles
- R = gas constant = 8.314 J/mol⋅K
- T = absolute temperature (K)

**Alternative form**: PV = NkBT
- N = number of molecules
- kB = Boltzmann constant = 1.381 × 10⁻²³ J/K

### Work Done by Gas

**General formula**: W = ∫P dV

**Constant pressure**: W = PΔV

**Isothermal process** (ideal gas): W = nRT ln(Vf/Vi)

## Heat Engines and Efficiency

### Heat Engine

**Definition**: Device that converts heat into mechanical work.

**Components**:
- Hot reservoir (TH): Heat source
- Cold reservoir (TC): Heat sink
- Working substance: Undergoes cyclic process

**Operation**:
1. Absorb heat QH from hot reservoir
2. Convert some to work W
3. Expel remaining heat QC to cold reservoir
4. Return to initial state

**Energy Conservation**: QH = W + QC

### Efficiency

**Definition**: Fraction of input heat converted to useful work.

**Formula**:
```
η = W/QH = (QH - QC)/QH = 1 - QC/QH
```

**Typical Efficiencies**:
- Gasoline car engine: 20-30%
- Diesel engine: 30-40%
- Steam power plant: 35-40%
- Modern gas turbine: 40-50%
- Combined cycle plant: 50-60%

**Why Not 100%?**: Second law requires heat rejection to cold reservoir. Some energy must be "wasted."

### Carnot Engine

**Definition**: Theoretically most efficient heat engine possible between two temperatures.

**Carnot Efficiency**:
```
ηCarnot = 1 - TC/TH
```

(Temperatures must be in Kelvin)

**Significance**:
- Sets upper limit on efficiency
- All real engines less efficient than Carnot
- Depends only on reservoir temperatures

**Example**: Engine operating between 500 K and 300 K.
- ηCarnot = 1 - 300/500 = 0.40 = 40%
- Real engine might achieve 30-35%

**Increasing Efficiency**:
- Increase TH (hotter combustion)
- Decrease TC (cooler exhaust)
- Practical limits: material strength, environmental temperature

### Refrigerators and Heat Pumps

**Refrigerator**: Removes heat from cold space and expels to warm space (requires work).

**Coefficient of Performance (COP)**:
```
COPref = QC/W
```

**Heat Pump**: Similar device used for heating.

```
COPheat = QH/W
```

**Relation**: COPheat = COPref + 1

**Example**: Refrigerator removes 1000 J from interior using 400 J of work.
- COPref = 1000/400 = 2.5

## Entropy in Detail

### Microscopic View

**Boltzmann's Formula**: S = kB ln Ω
- S = entropy
- kB = Boltzmann constant
- Ω = number of microstates (arrangements) corresponding to macrostate

**Insight**: More possible arrangements = higher entropy.

### Entropy Changes

**For reversible processes**:
```
ΔS = ∫(dQ/T)
```

**For irreversible processes**: ΔS > ∫(dQ/T)

**Isothermal process**: ΔS = Q/T

**Example**: 1 kg of ice melts at 0°C (273 K). Entropy change?
- Q = mLf = (1)(334,000) = 334 kJ
- ΔS = Q/T = 334,000/273 ≈ 1224 J/K

### Entropy and Disorder

Common (simplified) interpretation: Entropy measures disorder.

**More precise**: Entropy measures information uncertainty or number of accessible microstates.

**Examples of Entropy Increase**:
- Gas expanding into vacuum (more volume = more arrangements)
- Mixing two gases (more mixed configurations than separated)
- Heat flowing from hot to cold (energy spreads out)

## Real-World Applications

### Internal Combustion Engine

**Four-Stroke Cycle**:
1. **Intake**: Fuel-air mixture enters (isobaric expansion)
2. **Compression**: Mixture compressed (adiabatic compression)
3. **Power**: Fuel ignites, expands (isochoric heat addition, adiabatic expansion)
4. **Exhaust**: Spent gases expelled (isochoric cooling, isobaric compression)

**Efficiency factors**:
- Compression ratio
- Fuel properties
- Friction losses
- Heat losses through cylinder walls

### Power Plants

**Steam Cycle (Rankine Cycle)**:
1. Water heated to steam in boiler (heat from coal, gas, nuclear)
2. High-pressure steam drives turbine (work output)
3. Steam condensed in condenser (heat rejected to cooling water)
4. Pump returns water to boiler (work input)

**Improvements**:
- Superheating: raise TH
- Reheating: multi-stage expansion
- Combined cycle: gas turbine + steam turbine

### Climate and Weather

**Atmospheric Thermodynamics**:
- Solar radiation heats Earth's surface
- Convection creates wind and weather patterns
- Water evaporation and condensation transport massive energy
- Greenhouse gases affect energy balance (trap infrared radiation)

**Heat Capacity of Water**:
- Ocean stores vast thermal energy
- Moderates coastal climates
- Drives hurricanes and El Niño

### Life and Thermodynamics

**Living Organisms**:
- Are NOT closed systems (exchange energy and matter)
- Maintain low entropy locally by increasing environmental entropy
- Metabolism converts chemical energy to work and heat
- Food → energy → biological processes + heat

**Example**: Humans radiate ~100 W continuously, balancing metabolic heat production.

### Information Theory

**Thermodynamic Entropy and Information Entropy**:
- Related by Boltzmann constant
- Erasing 1 bit of information increases entropy by kB ln 2
- Landauer's principle: links computation and thermodynamics
- Black holes have entropy proportional to surface area

---

**Key Terms:**
- **Temperature**: Measure of average kinetic energy of particles
- **Heat**: Energy transferred due to temperature difference
- **Internal Energy**: Total microscopic kinetic and potential energy of system
- **Work**: Energy transferred by force through distance (in thermodynamics, often P-V work)
- **Entropy**: Measure of disorder or number of microstates
- **Thermal Equilibrium**: State of equal temperature with no net heat flow
- **Adiabatic**: Process with no heat transfer
- **Isothermal**: Process at constant temperature
- **Reversible Process**: Idealized process that could run backward, no entropy generation
- **Heat Engine**: Device converting heat to work
- **Efficiency**: Ratio of useful work output to heat input
- **Carnot Engine**: Most efficient possible heat engine between two temperatures

---

## Summary

Thermodynamics governs energy, heat, and entropy in macroscopic systems. Temperature measures average particle kinetic energy, while heat is energy transferred between systems at different temperatures through conduction, convection, or radiation. The four laws provide fundamental constraints: the zeroth defines temperature, the first mandates energy conservation (ΔU = Q - W), the second requires entropy increase in isolated systems (establishing time's arrow and limiting efficiency), and the third sets absolute zero as unattainable. Heat engines convert thermal energy to work but can never be perfectly efficient—Carnot efficiency (1 - TC/TH) sets the theoretical maximum, explaining why power plants and car engines waste significant energy as heat. Entropy quantifies disorder and information uncertainty, increasing naturally as systems evolve toward equilibrium. These principles underlie technologies from refrigerators to power plants, explain atmospheric phenomena and climate, govern biological metabolism, and even connect to information theory. Thermodynamics reveals that while energy is conserved, its quality degrades irreversibly, with universal entropy marching ever upward.
