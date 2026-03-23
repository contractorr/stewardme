# Mechanics and Materials Engineering

## Overview

Mechanics is the physics of forces and motion applied to engineering. Materials science studies how material properties arise from structure and how to select or design materials for specific applications. Together, they form the foundation for mechanical, civil, and aerospace engineering—every physical structure must resist forces without failing, and choosing the right material is as important as the design itself.

## Statics: Forces in Equilibrium

### Fundamental Concepts

**Force**: Push or pull; vector with magnitude and direction (measured in Newtons, N)

**Equilibrium**: Object at rest or moving at constant velocity
- **Σ**F** = 0**: Sum of forces = zero
- **Στ = 0**: Sum of torques (moments) = zero

**Free body diagram (FBD)**: Isolated object showing all forces acting on it—essential first step in analysis

### Types of Forces

**Applied forces**: External loads, pushes, pulls

**Reaction forces**: Support reactions (ground, walls, hinges)

**Tension**: Force along rope/cable/chain (always pulls)

**Compression**: Pushing force (columns, struts)

**Friction**: Resists sliding; f ≤ μN where μ = coefficient of friction, N = normal force

**Example - Simple Bridge**:
```
Person (700 N) stands on center of beam supported at ends:
- Each support reaction: 350 N upward
- Σ Forces: 700 N down + 350 N up + 350 N up = 0 ✓
```

### Moments (Torque)

**Moment**: Rotational effect of force; τ = F × d where d = perpendicular distance to pivot

**Sign convention**: Counterclockwise positive, clockwise negative

**Equilibrium requires**: Sum of moments about any point = 0

**Example - Lever**:
- 100 N force at 2 m from pivot lifts 200 N weight at 1 m
- (100 N)(2 m) = (200 N)(1 m) → 200 N⋅m = 200 N⋅m ✓
- Mechanical advantage = 2

### Trusses

**Truss**: Framework of members connected at joints (triangular patterns)

**Assumptions**:
- Members connected by frictionless pins
- Loads applied only at joints
- Members carry only axial forces (tension or compression)

**Method of joints**: Analyze equilibrium at each joint

**Method of sections**: Cut through truss, analyze portion

**Application**: Bridges, roof structures, towers—efficient way to span distances

**Why triangles**: Only rigid polygon; can't deform without changing member lengths

## Strength of Materials

### Stress and Strain

**Stress (σ)**: Force per unit area; σ = F/A (units: Pa = N/m²)
- **Tensile**: Pulling apart
- **Compressive**: Pushing together
- **Shear**: Sliding parallel to surface

**Strain (ε)**: Deformation per unit length; ε = ΔL/L (dimensionless, often given as %)

**Young's Modulus (E)**: Stiffness; σ = Eε in elastic region
- Steel: ~200 GPa (very stiff)
- Aluminum: ~70 GPa
- Wood: ~10 GPa
- Rubber: ~0.01 GPa (flexible)

### Stress-Strain Curve

**Typical metal behavior**:

1. **Elastic region**: Linear, reversible deformation (Hooke's Law)
2. **Yield point**: Permanent deformation begins
3. **Plastic region**: Irreversible deformation
4. **Ultimate strength**: Maximum stress before necking
5. **Fracture**: Material breaks

**Ductile materials** (steel, aluminum): Large plastic deformation before fracture
- Warning before failure (bends visibly)
- Can absorb energy

**Brittle materials** (glass, concrete, cast iron): Little plastic deformation
- Sudden catastrophic failure
- No warning

### Beam Bending

**Beams**: Structural members resisting loads perpendicular to length

**Moment diagram**: Shows bending moment along beam

**Key equation**: σ = My/I
- σ: Bending stress
- M: Bending moment
- y: Distance from neutral axis
- I: Second moment of area (depends on cross-section shape)

**Maximum stress**: At top/bottom surfaces (furthest from neutral axis)

**Deflection**: Beam sags under load; δ = (force × length³)/(modulus × moment of inertia)

**Example - Beam shapes**:
| Shape | I (proportional to) | Why used |
|-------|---------------------|----------|
| Solid rectangle | bh³/12 | Simple |
| I-beam | Material at top/bottom | Efficient—puts material where stress is highest |
| Hollow tube | ~D⁴ (outer diameter) | Very efficient for torsion and bending |

### Columns and Buckling

**Buckling**: Sudden sideways collapse of slender column under compression

**Euler buckling load**: Pᶜʳⁱᵗ = π²EI/(KL)²
- E: Young's modulus
- I: Moment of inertia
- L: Length
- K: End condition factor (0.5 to 2)

**Key insight**: Failure load drops as square of length—long thin columns buckle at low loads

**Prevention**:
- Shorter columns
- Larger cross-section
- Bracing/lateral support
- Stronger material (limited help—geometry matters more)

**Real-world**: Structural columns in buildings designed for buckling, not material strength

## Dynamics: Forces and Motion

### Newton's Laws Applied

**Newton's Second Law**: F = ma
- Force causes acceleration
- More mass → more force needed for same acceleration

**Work-Energy**: W = F⋅d = ΔKE
- Work done by force changes kinetic energy
- KE = ½mv²

**Power**: P = dW/dt = F⋅v
- Rate of doing work
- Units: Watts (W) = J/s

### Rotational Dynamics

**Moment of inertia (I)**: Rotational analog of mass
- Resistance to angular acceleration
- Depends on mass distribution: I = Σmᵢrᵢ²

**Rotational kinetic energy**: KE = ½Iω²
- ω: Angular velocity (rad/s)

**Torque and angular acceleration**: τ = Iα
- α: Angular acceleration

**Example - Flywheel**:
- Stores rotational energy
- High I → resists speed changes
- Used in engines (smooth power delivery), power grids (frequency stability)

### Vibrations

**Natural frequency**: Rate at which system oscillates when disturbed

**Simple harmonic motion**: f = (1/2π)√(k/m)
- k: Spring stiffness
- m: Mass

**Resonance**: When driving frequency matches natural frequency → large amplitudes
- Can cause catastrophic failure

**Damping**: Energy dissipation reduces vibration amplitude
- Critical for preventing resonance disasters

**Famous failure**: Tacoma Narrows Bridge (1940)—wind-induced resonance caused collapse

**Engineering solution**: Avoid resonance frequencies, add damping, tune mass dampers

## Materials Science

### Material Structure

**Atomic bonding**:
- **Metallic**: Delocalized electrons; ductile, conductive
- **Covalent**: Shared electrons; strong, directional (diamond, silicon)
- **Ionic**: Electrostatic attraction; brittle but hard (ceramics)

**Crystalline vs. amorphous**:
- **Crystalline**: Ordered atomic arrangement (metals, salt)
- **Amorphous**: Disordered (glass, some polymers)

**Grain structure**: Metals are polycrystalline (many small crystals)
- Grain boundaries strengthen material
- Smaller grains → stronger (grain boundary strengthening)

### Material Classes

#### Metals

**Properties**:
- Ductile (can deform plastically)
- Conductive (electrical and thermal)
- Strong, tough
- Heavy

**Common metals**:

| Metal | Density (g/cm³) | Strength (MPa) | Key properties |
|-------|----------------|----------------|----------------|
| Steel | 7.8 | 400-2000 | Strong, cheap, heavy |
| Aluminum | 2.7 | 300-600 | Light, corrosion-resistant |
| Titanium | 4.5 | 900-1200 | Very strong, very light, expensive |
| Copper | 8.9 | 200-400 | Highly conductive |

**Alloys**: Mixtures of metals with improved properties
- Carbon steel: Iron + carbon (stronger than pure iron)
- Stainless steel: + chromium (corrosion resistant)
- Bronze: Copper + tin (harder than copper)

#### Ceramics

**Properties**:
- Very hard
- Brittle (crack easily)
- High melting point
- Chemically inert
- Insulators

**Examples**:
- **Traditional**: Clay, pottery, bricks, concrete
- **Advanced**: Silicon carbide (cutting tools), alumina (bearings), silicon nitride (engine parts)

**Applications**: Where hardness, heat resistance, or chemical resistance needed

#### Polymers (Plastics)

**Structure**: Long chain molecules (organic)

**Categories**:
- **Thermoplastics**: Soften when heated (polyethylene, PVC, nylon)
  - Can be recycled, reshaped
- **Thermosets**: Harden permanently (epoxy, polyurethane)
  - Cannot be remelted

**Properties**:
- Light
- Corrosion-resistant
- Low strength compared to metals
- Temperature-sensitive

**Applications**: Packaging, consumer goods, automotive parts, insulation

#### Composites

**Concept**: Combine materials to get best of both

**Common composites**:

**Fiberglass**: Glass fibers in polymer matrix
- Strong, light, corrosion-resistant
- Boats, car bodies, wind turbine blades

**Carbon fiber**: Carbon fibers in epoxy
- Very high strength-to-weight ratio
- Expensive
- Aircraft, race cars, sporting equipment

**Reinforced concrete**: Steel rebar in concrete
- Concrete strong in compression, weak in tension
- Steel strong in tension
- Together: ideal for structures

**Plywood**: Wood layers with alternating grain direction
- Stronger than solid wood in multiple directions

### Material Selection

**Ashby charts**: Plot material properties (strength vs. density, stiffness vs. cost)

**Selection process**:
1. Define requirements (loads, environment, cost, weight, lifespan)
2. Identify candidate materials
3. Compare properties
4. Consider manufacturing constraints
5. Optimize for primary objective (minimize weight, cost, etc.)

**Example - Aircraft wing**:
- Requirements: High strength, low weight, fatigue resistance
- Early planes: Wood (light, but weak, degrades)
- WWII: Aluminum (good strength-to-weight, durable)
- Modern: Aluminum alloys, carbon fiber composites (Boeing 787: 50% composite)

### Material Properties

| Property | Definition | Significance |
|----------|------------|--------------|
| **Strength** | Stress at failure | How much load material can handle |
| **Stiffness** | Young's modulus | How much it deforms under load |
| **Toughness** | Energy to fracture | Resists crack propagation |
| **Hardness** | Resist surface indentation | Wear resistance |
| **Ductility** | Plastic deformation before fracture | Warning before failure |
| **Fatigue strength** | Resist cyclic loading | Prevents failure from repeated stress |
| **Creep resistance** | Resist deformation under load over time | Important at high temperature |
| **Corrosion resistance** | Resist chemical degradation | Lifespan in environment |

### Failure Modes

**Yielding**: Permanent deformation when stress exceeds yield strength

**Fracture**: Material breaks
- **Ductile**: Gradual, with warning (metal bends first)
- **Brittle**: Sudden, catastrophic (glass shatters)

**Fatigue**: Failure from repeated loading below ultimate strength
- Cracks initiate, grow slowly, then suddenly fracture
- **Example**: Metal paper clip bent back and forth breaks after ~10 cycles
- **Engineering**: Design for stress levels that survive millions of cycles

**Creep**: Slow deformation under constant stress at high temperature
- Jet engine turbine blades, power plant piping

**Buckling**: Instability failure (see above)

**Corrosion**: Chemical degradation
- Rust (iron + oxygen + water)
- Galvanic corrosion (dissimilar metals in contact)
- **Prevention**: Coatings, cathodic protection, corrosion-resistant alloys

## Real-World Applications

### Suspension Bridge

**Forces**:
- Main cables in tension (hang in catenary curve)
- Towers in compression
- Deck in bending from traffic, wind

**Materials**:
- **Cables**: High-strength steel wires (1800+ MPa)
  - Each wire can support ~10 tons
  - Thousands of wires bundled
- **Towers**: Reinforced concrete or steel
- **Deck**: Steel or concrete with steel reinforcement

**Analysis**:
- Dead load (bridge weight): Constant
- Live load (vehicles): Variable, must consider patterns
- Wind load: Can be enormous (design for hurricane-force)
- Seismic load: Earthquake forces

**Golden Gate Bridge**:
- Main cables: 36 inches diameter, 27,572 strands
- Tension: 63,500 tons (per cable)
- Towers: 746 feet tall, reinforced concrete

### Aircraft Structure

**Requirements**: Minimize weight while maintaining strength and damage tolerance

**Key loads**:
- **Aerodynamic**: Lift (up to 2.5× weight in maneuvers)
- **Inertial**: Acceleration forces
- **Pressurization**: Cabin pressure 8 psi higher than outside at altitude

**Materials evolution**:
- **1900s-1940s**: Wood, fabric (Wright Flyer, WWI planes)
- **1940s-2000s**: Aluminum alloys (2024, 7075)
  - Good strength-to-weight
  - Easy to machine and form
  - Fatigue issues (Comet disasters 1950s)
- **2000s+**: Composites (carbon fiber)
  - 20% lighter than aluminum for same strength
  - No corrosion, better fatigue resistance
  - More expensive, harder to inspect/repair

**Boeing 787 Dreamliner**: 50% composite, 20% aluminum, 15% titanium, 10% steel, 5% other
- Wings: Carbon fiber-reinforced polymer
- Fuselage: Carbon fiber barrel sections (one piece, no rivets)

### Automotive Chassis

**Design considerations**:
- **Crashworthiness**: Absorb impact energy, protect occupants
- **Stiffness**: Good handling (resist twist and flex)
- **Weight**: Fuel efficiency

**Crumple zones**: Front/rear designed to deform in crash, absorbing energy
- Passenger compartment: Rigid cage resists deformation

**Materials**:
- **Body panels**: Steel, aluminum (outer skin)
- **Structure**: High-strength steel (frame, pillars)
- **Safety cage**: Ultra-high-strength steel or boron steel
- **Hoods/doors**: Aluminum or composites (weight reduction)

**Trend**: More aluminum, magnesium, carbon fiber as fuel economy standards tighten

### Concrete Structures

**Concrete**: Cement + sand + gravel + water
- **Compressive strength**: Excellent (20-40 MPa typical, up to 100+ MPa high-performance)
- **Tensile strength**: ~10% of compressive (weak!)

**Reinforced concrete**: Steel rebar provides tensile strength
- Rebar placement critical—must be where tension occurs
- Concrete protects steel from corrosion

**Prestressed concrete**: Rebar tensioned before load applied
- Puts concrete in compression (its strength)
- Allows longer spans, thinner sections
- Used in bridges, parking structures

**Example - Hoover Dam**:
- 3.25 million cubic yards of concrete
- Thickness: 660 feet at base, 45 feet at crest
- Must resist water pressure, weight, thermal expansion
- Poured in blocks with cooling pipes (concrete generates heat curing)

## Testing and Analysis

### Experimental Testing

**Tensile test**: Pull specimen until breaks
- Measures stress-strain curve
- Determines yield strength, ultimate strength, Young's modulus, ductility

**Hardness test**: Indent surface, measure indentation
- Quick, non-destructive (small sample)
- Correlates with strength

**Impact test** (Charpy, Izod): Strike notched specimen
- Measures toughness, brittle-ductile transition temperature

**Fatigue test**: Cycle loading repeatedly
- Determines safe stress levels for repeated loading
- S-N curve: Stress vs. cycles to failure

**Non-destructive testing**:
- **Ultrasonic**: Sound waves detect internal cracks
- **X-ray/CT**: Image internal structure
- **Dye penetrant**: Reveals surface cracks
- **Magnetic particle**: Detects cracks in ferromagnetic materials

### Computational Analysis

**Finite Element Analysis (FEA)**:
1. Divide structure into small elements (mesh)
2. Apply material properties and boundary conditions
3. Solve system of equations for each element
4. Compute stress, strain, displacement

**Advantages**:
- Analyze complex geometries
- Test design before building prototype
- Optimize quickly

**Limitations**:
- Garbage in, garbage out (requires correct inputs)
- Mesh quality matters
- Cannot predict all failure modes
- **Must validate with testing**

**Modern design workflow**: CAD model → FEA → optimize → prototype → test → refine

## Key Terms

| Term | Definition |
|------|------------|
| **Stress** | Force per unit area (Pa) |
| **Strain** | Deformation per unit length (dimensionless) |
| **Young's Modulus** | Stiffness; stress/strain in elastic region |
| **Yield strength** | Stress where permanent deformation begins |
| **Ultimate strength** | Maximum stress before necking |
| **Ductility** | Ability to deform plastically before fracture |
| **Brittleness** | Little plastic deformation before fracture |
| **Toughness** | Energy absorbed before fracture |
| **Fatigue** | Failure from repeated cyclic loading |
| **Buckling** | Instability failure of slender compression member |
| **Moment of inertia** | Resistance to bending; depends on shape |
| **Factor of safety** | Ratio of strength to expected load |

## Summary

Mechanics and materials engineering applies physics to design structures and machines that withstand forces without failing. Statics analyzes forces in equilibrium—essential for buildings, bridges, and frameworks. Understanding stress, strain, and material behavior enables engineers to predict when structures will yield, buckle, or fracture.

Materials selection balances competing properties—metals offer strength and ductility, ceramics provide hardness and heat resistance, polymers are light and corrosion-resistant, composites combine advantages. Each application demands specific properties: aircraft require high strength-to-weight ratios (aluminum alloys, carbon fiber), buildings need compression strength (concrete, steel), bearings need hardness (ceramics).

Failure modes—yielding, fracture, fatigue, creep, buckling, corrosion—must be anticipated and designed against using factors of safety, appropriate materials, and proper geometry. Testing validates designs through tensile tests, fatigue tests, and non-destructive inspection. Finite element analysis enables optimization of complex structures before building prototypes.

From suspension bridges carrying traffic loads to aircraft structures withstanding aerodynamic forces, from automotive crashworthiness to concrete dams resisting water pressure—mechanics and materials form the foundation for translating engineering concepts into safe, reliable physical systems.
