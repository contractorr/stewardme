# Thermodynamics and Fluid Mechanics

## Overview

Thermodynamics is the science of energy, heat, and work—fundamental to power generation, engines, refrigeration, and chemical processes. Fluid mechanics studies how liquids and gases flow—essential for aerodynamics, pipelines, HVAC, and hydraulics. Together, they enable engineers to design systems that convert energy between forms, transport fluids, and extract work from heat—the engines powering modern civilization.

## Thermodynamics: The Science of Energy

### The Laws of Thermodynamics

#### Zeroth Law: Temperature Equilibrium

**Statement**: If A is in thermal equilibrium with C, and B is in equilibrium with C, then A is in equilibrium with B

**Significance**: Defines temperature as meaningful concept; enables thermometers

#### First Law: Energy Conservation

**Statement**: Energy cannot be created or destroyed, only converted between forms

**Equation**: ΔU = Q - W
- ΔU: Change in internal energy
- Q: Heat added to system
- W: Work done by system

**Implications**:
- Total energy of universe is constant
- Perpetual motion machine (type 1) impossible
- Can convert heat to work, but total energy conserved

**Example**: Car engine
- Q: Heat from burning gasoline
- W: Mechanical work (moving pistons)
- ΔU: Temperature change of engine

#### Second Law: Entropy Always Increases

**Statement**: Entropy of isolated system never decreases; heat flows spontaneously from hot to cold

**Entropy (S)**: Measure of disorder/randomness; dS ≥ dQ/T

**Implications**:
- **Heat engines cannot be 100% efficient**: Some heat must be rejected
- **Perpetual motion machine (type 2) impossible**: Cannot extract work from single temperature reservoir
- **Arrow of time**: Processes are irreversible; can't unmix scrambled eggs
- **Heat death**: Universe trending toward maximum entropy (uniform temperature, no useful work possible)

**Efficiency limit**: η_Carnot = 1 - T_cold/T_hot
- Maximum theoretical efficiency depends only on temperatures
- Real engines always worse than Carnot limit

**Example**: Power plant burning coal at 800 K, rejecting heat to river at 300 K
- Maximum efficiency: 1 - 300/800 = 62.5%
- Actual efficiency: ~40% (losses from friction, heat transfer, etc.)

#### Third Law: Absolute Zero Unattainable

**Statement**: Entropy of perfect crystal approaches zero as temperature approaches absolute zero (0 K = -273.15°C)

**Implication**: Cannot reach absolute zero in finite steps

### Thermodynamic Cycles

#### Heat Engine

**Purpose**: Convert thermal energy (heat) to mechanical work

**Components**:
1. **Hot reservoir**: Heat source (combustion, nuclear reactor, sun)
2. **Working fluid**: Undergoes thermodynamic cycle (steam, air, refrigerant)
3. **Engine**: Extracts work from fluid
4. **Cold reservoir**: Heat sink (atmosphere, river)

**Process**:
1. Absorb heat Q_H from hot reservoir
2. Convert some to work W
3. Reject remaining heat Q_C to cold reservoir
4. Return to initial state (cycle)

**Efficiency**: η = W/Q_H = (Q_H - Q_C)/Q_H

#### Carnot Cycle (Ideal)

**Four reversible steps**:
1. Isothermal expansion (absorb heat at T_H)
2. Adiabatic expansion (no heat transfer, temperature drops)
3. Isothermal compression (reject heat at T_C)
4. Adiabatic compression (temperature rises back to T_H)

**Maximum efficiency**: η = 1 - T_C/T_H

**Real engines approach but never reach Carnot efficiency**

#### Rankine Cycle (Steam Power Plants)

**Working fluid**: Water/steam

**Four steps**:
1. **Boiler**: Water heated to steam at high pressure
2. **Turbine**: Steam expands, drives turbine (work output)
3. **Condenser**: Steam cooled back to liquid
4. **Pump**: Liquid pumped back to high pressure

**Efficiency**: ~33-45% for coal plants, ~60% for combined cycle gas turbines

**Improvements**:
- **Superheating**: Heat steam above boiling point (higher T_H)
- **Reheating**: Expand in stages, reheat between stages
- **Regeneration**: Preheat feedwater with extracted steam

**Application**: Nearly all thermal power plants (coal, natural gas, nuclear)

#### Otto Cycle (Gasoline Engines)

**Working fluid**: Air-fuel mixture

**Four steps**:
1. **Intake**: Air-fuel drawn into cylinder
2. **Compression**: Piston compresses mixture (adiabatic)
3. **Combustion**: Spark ignites mixture (constant volume heat addition)
4. **Expansion**: Hot gases push piston (power stroke)
5. **Exhaust**: Waste gases expelled

**Compression ratio**: r = V_max/V_min
- Higher r → higher efficiency
- Limited by knocking (premature ignition)
- Typical: 8:1 to 12:1

**Efficiency**: η ≈ 1 - 1/r^(γ-1) where γ = 1.4 for air
- r = 10 → η ≈ 60% (theoretical)
- Actual: 25-30% (losses from friction, incomplete combustion, heat transfer)

#### Diesel Cycle

**Similar to Otto but**:
- Compresses air only (no fuel), higher compression ratio (14:1 to 25:1)
- Fuel injected at top of compression, self-ignites
- Combustion at constant pressure (vs. constant volume)

**Advantages**:
- Higher efficiency (~30-40%) due to higher compression
- Higher torque
- No spark plugs (simpler)

**Disadvantages**:
- Heavier, more expensive
- More emissions (NOx, particulates) without aftertreatment

#### Brayton Cycle (Gas Turbines, Jet Engines)

**Continuous flow** (not reciprocating like Otto/Diesel)

**Four steps**:
1. **Compressor**: Compress air
2. **Combustion chamber**: Add fuel, burn at constant pressure
3. **Turbine**: Hot gases expand through turbine
4. **Exhaust**: Gases expelled

**Jet engine**: Exhaust provides thrust

**Power generation**: Turbine drives generator

**Combined cycle**: Exhaust heat runs steam turbine (Rankine cycle)
- Overall efficiency: ~60% (best of any fossil fuel plant)

### Refrigeration and Heat Pumps

**Refrigerator**: Moves heat from cold space to warm space (opposite of heat engine)

**Requires work input** (violates spontaneous heat flow)

**Vapor-Compression Cycle**:
1. **Evaporator**: Liquid refrigerant absorbs heat, evaporates (inside refrigerator)
2. **Compressor**: Compress vapor (work input)
3. **Condenser**: Hot vapor condenses, rejects heat (coils on back of fridge)
4. **Expansion valve**: Pressure drops, liquid cools
5. Repeat

**Coefficient of Performance (COP)**: Q_C/W (heat removed per work input)
- Higher is better
- Typical refrigerator: COP = 2-3 (removes 2-3× work input as heat)
- Carnot maximum: COP = T_C/(T_H - T_C)

**Heat pump**: Same cycle, used for heating
- COP_heating = Q_H/W = COP_cooling + 1
- Can be very efficient (COP = 3-5), delivering more heat than electrical energy consumed

**Applications**:
- Refrigerators, freezers
- Air conditioning
- Heat pumps for buildings
- Industrial cooling

## Fluid Mechanics

### Fluid Properties

**Fluid**: Substance that deforms continuously under shear stress (liquids and gases)

**Density (ρ)**: Mass per volume (kg/m³)
- Water: 1000 kg/m³
- Air (sea level): 1.2 kg/m³
- Mercury: 13,600 kg/m³

**Viscosity (μ)**: Resistance to flow; internal friction
- **Water**: Low viscosity (flows easily)
- **Honey**: High viscosity (flows slowly)
- **Kinematic viscosity** (ν): μ/ρ

**Compressibility**:
- **Liquids**: Nearly incompressible (density constant)
- **Gases**: Compressible (density changes with pressure)

**Surface tension**: Cohesive force at liquid interface (water droplets, capillary action)

### Fluid Statics

**Pressure**: Force per unit area (Pa = N/m²)

**Pascal's Law**: Pressure in static fluid is same in all directions

**Hydrostatic pressure**: p = p_0 + ρgh
- p_0: Surface pressure
- ρ: Density
- g: Gravity (9.81 m/s²)
- h: Depth

**Example**: Water pressure at 10 m depth
- p = 101,325 Pa (1 atm) + (1000)(9.81)(10) = 199,425 Pa ≈ 2 atm

**Applications**:
- **Dams**: Water pressure increases with depth; thicker at bottom
- **Submarines**: Must withstand enormous pressure at depth
- **Hydraulics**: Transmit force through incompressible fluid

**Buoyancy** (Archimedes' Principle): Buoyant force = weight of displaced fluid
- Object floats if less dense than fluid
- Ships: Displace water volume weighing more than ship

### Fluid Dynamics

**Continuity Equation** (Mass conservation):
ρ₁A₁v₁ = ρ₂A₂v₂

For incompressible flow: A₁v₁ = A₂v₂
- Narrow pipe → higher velocity

**Bernoulli's Equation** (Energy conservation):
p + ½ρv² + ρgh = constant

- p: Static pressure
- ½ρv²: Dynamic pressure (kinetic energy)
- ρgh: Gravitational potential energy

**Implications**:
- **Higher velocity → lower pressure** (critical for lift)
- Narrowing pipe: Pressure drops as velocity increases
- Fluid rising: Pressure drops due to gravity

**Limitations**: Assumes inviscid (no viscosity), steady, incompressible flow

### Laminar vs. Turbulent Flow

**Reynolds Number**: Re = ρvD/μ (dimensionless)
- v: Velocity
- D: Characteristic length (pipe diameter)
- μ: Viscosity

**Re < 2300**: Laminar (smooth, parallel layers)
- Low velocity, high viscosity, or small dimensions
- Predictable, orderly

**Re > 4000**: Turbulent (chaotic, swirling eddies)
- High velocity, low viscosity, or large dimensions
- Unpredictable details, but statistically describable

**2300 < Re < 4000**: Transitional (unstable)

**Engineering significance**:
- **Laminar**: Lower friction, easier to model
- **Turbulent**: Higher friction, better mixing, harder to predict
- Most engineering flows are turbulent

### Drag and Lift

**Drag**: Force opposing motion through fluid

**Drag equation**: F_D = ½ρv²C_DA
- C_D: Drag coefficient (depends on shape)
- A: Reference area (frontal area)

**Drag coefficient examples**:
- Sphere: 0.47
- Streamlined shape: 0.04
- Flat plate perpendicular: 1.28
- Modern car: 0.25-0.35

**Minimizing drag**:
- Streamlined shapes (teardrop)
- Smooth surfaces
- Reduce frontal area
- **Critical for**: Aircraft, cars, ships, wind turbine efficiency

**Lift**: Force perpendicular to flow direction

**Airfoil**: Wing shape generating lift
- Curved upper surface
- Air travels faster over top (Bernoulli) → lower pressure above
- Net upward force

**Lift equation**: F_L = ½ρv²C_LA
- C_L: Lift coefficient (depends on angle of attack)

**Angle of attack**: Angle between wing chord and oncoming flow
- Increasing angle → more lift
- Too steep → **stall** (flow separation, lift collapses)

**Applications**: Aircraft wings, helicopter rotors, wind turbines, hydrofoils

### Pipe Flow

**Pressure drop** in pipe due to friction:
Δp = f(L/D)(½ρv²)

- f: Friction factor (depends on Re and surface roughness)
- L: Pipe length
- D: Diameter

**Darcy-Weisbach equation**: Fundamental for pipe design

**Key insights**:
- Pressure drop ∝ length
- Pressure drop ∝ 1/D⁵ (for laminar) or 1/D⁴·⁸⁵ (turbulent)
  - **Doubling diameter reduces pressure drop by ~30×**
- Doubling velocity quadruples pressure drop

**Applications**:
- Water distribution systems
- Oil/gas pipelines
- HVAC ductwork
- Sizing pumps (must overcome pressure drop)

### Pumps and Turbines

**Pump**: Adds energy to fluid (increases pressure, velocity, or elevation)

**Types**:
- **Centrifugal**: Spinning impeller increases velocity, converts to pressure
  - Most common (water supply, HVAC)
- **Positive displacement**: Traps fixed volume, forces through outlet
  - Pumps (piston, gear, screw)
  - Handles viscous fluids, consistent output

**Turbine**: Extracts energy from fluid flow

**Types**:
- **Impulse** (Pelton wheel): High-velocity jet strikes buckets
  - Hydroelectric dams with high head
- **Reaction** (Francis, Kaplan): Pressure change across blades
  - Most hydroelectric dams
- **Steam/gas turbines**: Same principles, different working fluid

**Pump/turbine similarity**: Reverse operation
- Turbine running backwards can pump

## Real-World Applications

### Steam Power Plant

**Coal-fired plant** (~600 MW typical):

**Energy flow**:
1. Coal combustion: Chemical energy → heat (3500°F flame)
2. Boiler: Heat → steam at 3500 psi, 1000°F
3. High-pressure turbine: Steam expands, drives turbine
4. Reheat: Steam reheated to 1000°F
5. Intermediate/low-pressure turbines: Further expansion
6. Condenser: Exhaust steam condensed at vacuum
7. Feedwater heaters: Preheat using extracted steam
8. Repeat

**Efficiency**: ~38-42%
- Lost to: Condenser cooling (largest), stack gases, auxiliaries, generator

**Combined cycle gas turbine**:
- Gas turbine (Brayton cycle): 38% efficient
- Exhaust heat → steam turbine (Rankine cycle): Additional 22%
- **Total: ~60% efficient** (best fossil fuel power generation)

### Aircraft Engine (Turbofan)

**Components**:
1. **Fan**: Large diameter, pulls air in
2. **Compressor**: 10-15 stages, increases pressure to 30-50× atmospheric
3. **Combustor**: Fuel + compressed air burned (3000°F)
4. **Turbine**: Extracts energy to drive compressor and fan
5. **Nozzle**: Accelerates exhaust, produces thrust

**Bypass ratio**: Air through fan vs. through core
- Low bypass (fighters): 0.5:1 (high speed)
- High bypass (airliners): 9:1 (fuel efficient, quiet)

**Thrust**: ~100,000 lbf (Boeing 777 engine)

**Efficiency**:
- Thermal efficiency: ~50% (energy from fuel)
- Propulsive efficiency: ~85% (kinetic energy → thrust)
- Overall: ~42%

**Materials challenge**: Turbine blades see 3000°F, 40,000 RPM, 100 tons force
- Nickel superalloys
- Single-crystal structure (no grain boundaries)
- Cooling passages inside blades

### Hydroelectric Dam

**Energy conversion**: Gravitational potential energy → kinetic energy → electricity

**Power**: P = ηρgQh
- η: Efficiency (~90%, very high!)
- ρ: Water density
- g: Gravity
- Q: Flow rate (m³/s)
- h: Head (height difference, m)

**Example - Hoover Dam**:
- Head: 180 m
- Flow: 1000 m³/s (max)
- Power: (0.9)(1000)(9.81)(1000)(180) = 1.6 GW

**Advantages**:
- Very high efficiency
- Fast response (spinning reserve for grid stability)
- No emissions
- Long lifespan (50-100 years)

**Disadvantages**:
- Geographic limitations
- Environmental impact (floods valley, blocks fish)
- High initial cost
- Drought vulnerability

### HVAC (Heating, Ventilation, Air Conditioning)

**Objectives**:
- Temperature control
- Humidity control
- Air quality (filtration, fresh air)
- Energy efficiency

**Components**:
1. **Heating**: Furnace (combustion), heat pump, or electric resistance
2. **Cooling**: Refrigeration cycle (air conditioner)
3. **Distribution**: Ductwork, fans (fluid mechanics)
4. **Controls**: Thermostats, dampers, variable-speed drives

**Design considerations**:
- **Heating/cooling loads**: Calculate heat gain/loss
  - Insulation, windows, occupants, lighting, equipment, solar gain
- **Duct sizing**: Balance pressure drop and noise
  - Higher velocity → smaller ducts (cheaper) but higher pressure drop (more fan power) and noise
- **Air changes**: Fresh air requirements for air quality

**Energy efficiency**:
- SEER (Seasonal Energy Efficiency Ratio): Higher is better (modern AC: 13-21 SEER)
- Heat pumps: COP of 3-5 (deliver 3-5× electrical input as heat)
- Building envelope: Insulation, air sealing, high-performance windows

**40% of building energy** in US is HVAC—major optimization opportunity

### Aerodynamics: Race Car Design

**Goal**: Maximize downforce (pushes car to track) while minimizing drag

**Wings**: Generate negative lift (downforce)
- Inverted airfoil shape
- Adjustable angle for different tracks

**Underbody**: Venturi effect
- Narrowing channel under car accelerates air (Bernoulli)
- Lower pressure underneath creates downforce

**Diffuser**: Gradually expanding section at rear
- Recovers pressure, reduces drag

**Formula 1**:
- Downforce: 5× car weight at top speed
- Allows extreme cornering (4-5 g lateral acceleration)

**Tradeoff**: Downforce increases drag → reduces top speed
- Balance depends on track (high downforce for tight corners, low for straights)

### Wind Turbine

**Energy conversion**: Kinetic energy of wind → rotation → electricity

**Betz limit**: Maximum 59.3% of wind's kinetic energy can be extracted
- If extract all energy, air would stop (no flow through turbine)

**Power**: P = ½ρAv³C_p
- ρ: Air density
- A: Rotor swept area (πR²)
- v: Wind velocity
- C_p: Power coefficient (<0.593)

**Key insight**: Power ∝ v³
- Doubling wind speed → 8× power
- Why turbines in windy locations (consistent high winds)

**Modern large turbines**:
- Rotor diameter: 150-200 m
- Power: 5-15 MW
- Efficiency: 45-50% (close to Betz limit)

**Blade design**: Airfoil shape optimized for lift
- Twisted (angle varies along length for optimal angle of attack)
- Composite materials (fiberglass, carbon fiber)

## Computational Fluid Dynamics (CFD)

**Goal**: Solve Navier-Stokes equations numerically for complex flows

**Process**:
1. Create geometry (CAD model)
2. Generate mesh (divide into small cells)
3. Specify boundary conditions (inlet velocity, outlet pressure, walls)
4. Solve governing equations (mass, momentum, energy)
5. Post-process results (visualize velocity, pressure, temperature)

**Navier-Stokes equations**: Describe fluid motion
- Nonlinear partial differential equations
- No general analytical solution
- Require massive computation for realistic flows

**Applications**:
- Aircraft design (airflow around wings, fuselage)
- Car aerodynamics (drag reduction)
- Turbomachinery (turbines, compressors, pumps)
- HVAC design (airflow in buildings)
- Weather forecasting (atmosphere is a fluid!)

**Validation critical**: CFD can give wrong answers if mesh too coarse, boundary conditions wrong, or model inappropriate
- Always validate with experiments or known solutions

## Key Terms

| Term | Definition |
|------|------------|
| **First Law of Thermodynamics** | Energy conservation; ΔU = Q - W |
| **Second Law** | Entropy increases; heat engines limited efficiency |
| **Carnot efficiency** | Maximum efficiency = 1 - T_C/T_H |
| **Heat engine** | Converts heat to work via thermodynamic cycle |
| **Refrigerator** | Moves heat from cold to hot (requires work) |
| **Bernoulli's equation** | Energy conservation in fluid flow |
| **Reynolds number** | Dimensionless ratio indicating laminar/turbulent flow |
| **Drag** | Force opposing motion through fluid |
| **Lift** | Force perpendicular to flow (enables flight) |
| **Viscosity** | Fluid's resistance to flow |
| **Compressibility** | Change in density with pressure |

## Summary

Thermodynamics governs energy conversion—the first law conserves energy while the second law limits efficiency and establishes entropy's inevitable increase. Heat engines (Otto, Diesel, Brayton, Rankine cycles) convert thermal energy to work, with efficiency fundamentally limited by Carnot's formula depending on temperature ratios. Real engines approach but never reach theoretical limits due to friction, heat transfer losses, and irreversibilities.

Fluid mechanics describes how liquids and gases flow. Bernoulli's equation relates pressure, velocity, and elevation, explaining lift generation and pressure drops in pipes. Reynolds number determines whether flow is smooth (laminar) or chaotic (turbulent), affecting drag, mixing, and predictability. Drag forces resist motion while lift forces enable flight—both scale with velocity squared and depend critically on shape.

Together, these disciplines enable power plants converting fuel to electricity at 40-60% efficiency, jet engines producing 100,000 pounds of thrust, hydroelectric dams at 90% efficiency, HVAC systems conditioning buildings, and wind turbines extracting energy from air. Understanding thermodynamic cycles, fluid flow, and energy conversion is essential for designing systems that generate, transport, and utilize energy—the engines powering modern civilization.

Computational fluid dynamics extends analysis to complex geometries impossible to solve analytically, though validation with experiments remains critical. From power generation to propulsion, refrigeration to aerodynamics—thermodynamics and fluid mechanics translate physical principles into working systems that move humanity and keep civilization running.
