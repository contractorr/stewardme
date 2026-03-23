# Electromagnetism

## Overview

Electromagnetism describes electric and magnetic phenomena and their deep interconnection. Unified by James Clerk Maxwell in the 1860s, it's one of the four fundamental forces of nature. Electromagnetism governs chemistry, light, electricity, magnetism, and all electromagnetic radiation. From the chemical bonds holding molecules together to radio waves carrying information across space, electromagnetic forces shape our world. This field underlies virtually all modern technology: computers, telecommunications, power generation, motors, and medical imaging.

## Electric Charge

### Fundamental Properties

**Electric charge** is an intrinsic property of matter, analogous to mass but with two types:
- **Positive charge**: Protons carry +e
- **Negative charge**: Electrons carry -e
- **Elementary charge**: e = 1.602 × 10⁻¹⁹ C (coulomb)

**Key Principles**:
1. **Conservation**: Total charge in an isolated system never changes
2. **Quantization**: All charges are integer multiples of e
3. **Like charges repel, opposite charges attract**
4. **Charge is relativistic invariant** (same in all reference frames)

### Conductors vs. Insulators

**Conductors**: Materials where charges move freely
- Metals (copper, aluminum, gold, silver)
- Plasma, saltwater, graphite
- Free electrons can drift through material

**Insulators (Dielectrics)**: Materials where charges are bound
- Rubber, glass, plastic, wood, air
- Charges cannot move freely
- Can be polarized (charge separation within molecules)

**Semiconductors**: Intermediate behavior
- Silicon, germanium
- Conductivity controlled by doping and temperature
- Foundation of modern electronics

### Charging Methods

1. **Friction**: Transfer electrons by rubbing (e.g., balloon on hair)
2. **Contact**: Touch charged object to neutral object
3. **Induction**: Bring charged object near, rearrange charges without contact

## Electric Force and Coulomb's Law

### Coulomb's Law

**Statement**: Electric force between two point charges is proportional to the product of charges and inversely proportional to the square of distance between them.

**Formula**:
```
F = k(q₁q₂)/r²
```

Where:
- F = force magnitude (N)
- k = Coulomb's constant = 8.99 × 10⁹ N⋅m²/C²
- q₁, q₂ = charges (C)
- r = separation distance (m)

**Alternative form**: k = 1/(4πε₀)
- ε₀ = permittivity of free space = 8.85 × 10⁻¹² C²/N⋅m²

**Vector form**: **F** = k(q₁q₂)/r² **r̂**
- **r̂** = unit vector from q₁ to q₂
- Positive F means repulsion, negative means attraction

**Comparison to Gravity**:
| Property | Gravity | Electricity |
|----------|---------|-------------|
| Always attractive? | Yes | No (can attract or repel) |
| Relative strength | Extremely weak | Strong |
| Constant | G = 6.67 × 10⁻¹¹ | k = 8.99 × 10⁹ |
| Range | Infinite | Infinite |

**Example**: Two electrons 1 nm apart. What's the repulsive force?
- F = k(e²)/r² = (8.99 × 10⁹)(1.602 × 10⁻¹⁹)²/(10⁻⁹)²
- F ≈ 2.3 × 10⁻¹⁰ N

### Superposition Principle

**Principle**: Total force on a charge equals the vector sum of forces from all other charges.

**Formula**: **F**total = **F**₁ + **F**₂ + **F**₃ + ...

This linearity simplifies calculations for multiple charges.

## Electric Field

### Definition

**Electric field** (**E**) is the force per unit charge at a point in space.

**Formula**: **E** = **F**/q

**Units**: N/C or V/m (equivalent)

**Meaning**: Electric field exists independently of test charge; it's a property of space created by source charges.

### Field from Point Charge

**Formula**:
```
E = kq/r²
```

Direction: Radially outward from positive charge, inward toward negative charge.

**Visualization**: Field lines (never cross, density indicates strength, point from + to -)

### Field from Multiple Charges

Use superposition: **E**total = **E**₁ + **E**₂ + **E**₃ + ...

### Uniform Electric Field

**Between parallel plates**:
```
E = V/d = σ/ε₀
```
- V = voltage difference
- d = plate separation
- σ = surface charge density

Field points from positive to negative plate, constant between plates.

### Electric Dipole

**Definition**: Pair of equal and opposite charges separated by distance d.

**Dipole moment**: **p** = q**d** (vector from negative to positive)

**Applications**:
- Water molecules (polar)
- Antenna radiation patterns
- Molecular interactions

## Electric Potential Energy and Potential

### Electric Potential Energy

**Definition**: Energy stored in configuration of charges.

**For two point charges**:
```
U = kq₁q₂/r
```

**Meaning**:
- U > 0: Repulsive (positive energy, would repel if released)
- U < 0: Attractive (negative energy, bound system)
- U = 0 at r = ∞ (reference point)

### Electric Potential (Voltage)

**Definition**: Potential energy per unit charge.

**Formula**: V = U/q = kQ/r (for point charge Q)

**Unit**: Volt (V) = J/C

**Potential Difference**: ΔV = VB - VA = -∫**E**·d**l** (work per charge to move from A to B)

**Relationship to Field**: **E** = -∇V (field points from high to low potential)

**Equipotential Surfaces**:
- Surfaces of constant potential
- Field lines perpendicular to equipotential surfaces
- No work to move along equipotential

### Electron Volt

**Definition**: Energy gained by electron moving through 1 V potential difference.

**Value**: 1 eV = 1.602 × 10⁻¹⁹ J

**Usage**: Convenient unit for atomic/particle physics
- Visible light photons: 1.8-3.1 eV
- Chemical bonds: 1-10 eV
- X-ray photons: 100 eV - 100 keV

## Capacitance

### Definition

**Capacitor**: Device that stores electric charge and energy.

**Capacitance**: Charge stored per unit voltage.

**Formula**: C = Q/V

**Unit**: Farad (F) = C/V

### Parallel Plate Capacitor

**Capacitance**:
```
C = ε₀A/d
```
- A = plate area
- d = plate separation
- ε₀ = permittivity of free space

**With dielectric**: C = κε₀A/d
- κ = dielectric constant (≥ 1)

### Energy Stored

**Formula**:
```
U = ½QV = ½CV² = Q²/(2C)
```

**Energy density** (between plates): u = ½ε₀E²

### Capacitors in Circuits

**Series**: 1/Ctotal = 1/C₁ + 1/C₂ + ...

**Parallel**: Ctotal = C₁ + C₂ + ...

**Applications**:
- Energy storage (camera flash, defibrillator)
- Filtering (smooth power supplies)
- Timing circuits (RC circuits)
- Tuning (radio receivers)
- Memory (DRAM)

## Electric Current

### Definition

**Electric current**: Flow of electric charge.

**Formula**: I = dQ/dt (charge per unit time)

**Unit**: Ampere (A) = C/s

**Convention**: Current flows from + to - (opposite to electron flow)

### Current Density

**Definition**: J = I/A (current per unit area)

**Relationship to drift velocity**: J = nqvd
- n = charge carrier density
- q = charge per carrier
- vd = drift velocity (average velocity of carriers)

**Typical drift velocity**: ~10⁻⁴ m/s (much slower than signal propagation ~10⁸ m/s)

## Resistance and Ohm's Law

### Resistance

**Definition**: Opposition to current flow.

**Formula**: R = ρL/A
- ρ = resistivity (material property)
- L = length
- A = cross-sectional area

**Unit**: Ohm (Ω)

**Temperature dependence**: R = R₀[1 + α(T - T₀)]
- α = temperature coefficient

### Ohm's Law

**Statement**: Current through conductor is proportional to voltage across it (for constant temperature).

**Formula**:
```
V = IR
```

**Alternative forms**:
- I = V/R
- R = V/I

**Power Dissipation**:
```
P = IV = I²R = V²/R
```

**Ohmic vs. Non-Ohmic**:
- Ohmic: Resistance constant (metals)
- Non-Ohmic: Resistance varies (diodes, transistors)

### Resistors in Circuits

**Series**: Rtotal = R₁ + R₂ + ...
- Same current through all
- Voltages add

**Parallel**: 1/Rtotal = 1/R₁ + 1/R₂ + ...
- Same voltage across all
- Currents add

## DC Circuits

### Kirchhoff's Laws

**Current Law (KCL)**: Sum of currents entering a junction equals sum leaving.
- ΣIin = ΣIout
- Conservation of charge

**Voltage Law (KVL)**: Sum of voltage changes around any closed loop is zero.
- ΣV = 0
- Conservation of energy

### RC Circuits

**Charging capacitor**:
- Q(t) = Q₀(1 - e^(-t/RC))
- V(t) = V₀(1 - e^(-t/RC))
- I(t) = I₀e^(-t/RC)

**Discharging capacitor**:
- Q(t) = Q₀e^(-t/RC)
- V(t) = V₀e^(-t/RC)

**Time constant**: τ = RC
- Time to reach 63% of final value
- After 5τ, essentially complete

## Magnetism

### Magnetic Field

**Definition**: Field created by moving charges or magnetic materials.

**Symbol**: **B**

**Unit**: Tesla (T) = N/(A⋅m) = Wb/m²
- Also: Gauss (1 G = 10⁻⁴ T)

**Sources**:
- Moving charges (currents)
- Magnets (aligned atomic dipoles)
- Changing electric fields

**Properties**:
- Field lines form closed loops (no magnetic monopoles)
- Point from north to south outside magnet
- Point from south to north inside magnet

### Magnetic Force

**Force on moving charge**:
```
**F** = q**v** × **B**
```

**Magnitude**: F = qvB sin θ
- Maximum when v ⊥ B
- Zero when v ∥ B

**Direction**: Right-hand rule
- Point fingers along **v**
- Curl toward **B**
- Thumb points along **F** (for positive q)

**Circular motion**: Magnetic force provides centripetal acceleration
- r = mv/(qB) (radius of circular path)
- Applications: Mass spectrometry, particle accelerators

**Force on current-carrying wire**:
```
**F** = I**L** × **B**
```
- **L** = length vector along current direction

### Magnetic Field from Current

**Long straight wire**:
```
B = μ₀I/(2πr)
```
- μ₀ = permeability of free space = 4π × 10⁻⁷ T⋅m/A
- r = distance from wire
- Direction: Right-hand rule (thumb along current, fingers curl around wire)

**Center of circular loop**:
```
B = μ₀I/(2R)
```
- R = loop radius

**Solenoid** (long coil):
```
B = μ₀nI
```
- n = turns per unit length
- Uniform field inside, nearly zero outside

**Toroid**: B = μ₀NI/(2πr)
- N = total turns
- r = distance from center

### Ampère's Law

**Statement**: Line integral of **B** around closed loop equals μ₀ times enclosed current.

**Formula**: ∮**B**·d**l** = μ₀Ienc

**Applications**:
- Calculate fields with high symmetry
- Analogous to Gauss's law for electricity

## Electromagnetic Induction

### Faraday's Law

**Statement**: Changing magnetic flux induces electromotive force (EMF).

**Formula**:
```
ε = -dΦB/dt = -d/dt(∫**B**·d**A**)
```

**Magnetic flux**: ΦB = BA cos θ (for uniform field)

**Negative sign**: Lenz's law (induced EMF opposes change)

**Ways to change flux**:
1. Change B (field strength)
2. Change A (area)
3. Change θ (orientation)

**Example**: Move magnet toward coil → increasing flux → induced current creates opposing field.

### Lenz's Law

**Statement**: Induced current flows to oppose the change in flux that produced it.

**Meaning**: Nature's resistance to change; consequence of energy conservation.

**Application**: Determines direction of induced current.

### Motional EMF

**Conductor moving through field**:
```
ε = BLv
```
- L = length of conductor
- v = velocity perpendicular to B

**Electric generator principle**: Rotate coil in magnetic field, continuously changing flux.

### Inductance

**Self-inductance** (L): Induced EMF opposes change in current through same circuit.

**Formula**: ε = -L(dI/dt)

**Unit**: Henry (H) = Wb/A = V⋅s/A

**Solenoid inductance**: L = μ₀n²AL
- n = turns per length
- A = cross-sectional area
- L = length

**Energy stored**: U = ½LI²

### RL Circuits

**Current growth**: I(t) = I₀(1 - e^(-t/τ))

**Current decay**: I(t) = I₀e^(-t/τ)

**Time constant**: τ = L/R

## Maxwell's Equations

The four fundamental equations unifying electricity and magnetism:

### 1. Gauss's Law (Electric)

**Integral form**: ∮**E**·d**A** = Qenc/ε₀

**Meaning**: Electric flux through closed surface equals enclosed charge divided by ε₀.

**Differential form**: ∇·**E** = ρ/ε₀

### 2. Gauss's Law (Magnetic)

**Integral form**: ∮**B**·d**A** = 0

**Meaning**: No magnetic monopoles; magnetic field lines form closed loops.

**Differential form**: ∇·**B** = 0

### 3. Faraday's Law

**Integral form**: ∮**E**·d**l** = -dΦB/dt

**Meaning**: Changing magnetic flux induces electric field.

**Differential form**: ∇×**E** = -∂**B**/∂t

### 4. Ampère-Maxwell Law

**Integral form**: ∮**B**·d**l** = μ₀Ienc + μ₀ε₀(dΦE/dt)

**Meaning**: Magnetic field created by current and by changing electric field (displacement current).

**Differential form**: ∇×**B** = μ₀**J** + μ₀ε₀(∂**E**/∂t)

### Electromagnetic Waves

**Prediction**: Maxwell showed his equations predict waves traveling at speed:
```
c = 1/√(μ₀ε₀) ≈ 3 × 10⁸ m/s
```

**Conclusion**: Light is an electromagnetic wave!

**Properties**:
- **E** and **B** perpendicular to each other and to propagation direction
- Transverse waves
- Don't require medium (travel through vacuum)
- Carry energy and momentum

## Electromagnetic Spectrum

**All electromagnetic radiation**—same physics, different frequencies:

| Type | Wavelength | Frequency | Energy | Sources/Uses |
|------|-----------|-----------|--------|--------------|
| **Radio** | > 1 mm | < 300 GHz | < 10⁻³ eV | Broadcasting, communication |
| **Microwave** | 1 mm - 1 m | 300 MHz - 300 GHz | 10⁻³ - 1 eV | Radar, cooking, WiFi |
| **Infrared** | 700 nm - 1 mm | 300 GHz - 430 THz | 1 - 1.8 eV | Heat, night vision, remote controls |
| **Visible** | 400 - 700 nm | 430 - 750 THz | 1.8 - 3.1 eV | Human vision, photosynthesis |
| **Ultraviolet** | 10 - 400 nm | 750 THz - 30 PHz | 3 - 124 eV | Sterilization, tanning |
| **X-rays** | 0.01 - 10 nm | 30 PHz - 30 EHz | 124 eV - 124 keV | Medical imaging, crystallography |
| **Gamma rays** | < 0.01 nm | > 30 EHz | > 124 keV | Nuclear reactions, cancer treatment |

**Relationships**:
- c = λf (speed = wavelength × frequency)
- E = hf (photon energy = Planck constant × frequency)

## Real-World Applications

### Electric Power

**Generation**: Rotating magnets induce current in coils (Faraday's law)

**Transmission**: High voltage reduces I²R losses (P = VI, so higher V allows lower I)

**Transformers**: Change AC voltage using mutual inductance

**AC vs. DC**:
- AC: Easily transformed, standard for power grids
- DC: Used in electronics, efficient for long-distance transmission (HVDC)

### Motors and Generators

**Motor**: Current in magnetic field produces force (converts electrical → mechanical)

**Generator**: Motion in magnetic field induces current (converts mechanical → electrical)

**Same device, opposite operation**

### Telecommunications

**Radio/TV**: Oscillating current in antenna produces EM waves

**Cell phones**: Microwave frequencies (850 MHz - 5 GHz)

**Fiber optics**: Light pulses through glass, total internal reflection

**WiFi**: 2.4 GHz and 5 GHz microwaves

### Medical Applications

**MRI**: Strong magnetic fields (1-3 T) align proton spins; radio waves probe, detect signals

**Defibrillator**: Capacitor discharges through heart to restore rhythm

**X-ray imaging**: Short-wavelength EM radiation penetrates tissue

**Radiation therapy**: High-energy photons or particles kill cancer cells

### Electronics

**Transistors**: Semiconductor switches, amplifiers

**Integrated circuits**: Billions of transistors on chip

**Displays**: LCD (liquid crystals), LED (light-emitting diodes), OLED

**Memory**: Flash (charge storage), DRAM (capacitors), magnetic (hard drives)

---

**Key Terms:**
- **Electric charge**: Fundamental property; two types (positive/negative)
- **Electric field**: Force per unit charge
- **Electric potential (voltage)**: Potential energy per unit charge
- **Current**: Flow of charge
- **Resistance**: Opposition to current flow
- **Capacitance**: Charge stored per unit voltage
- **Magnetic field**: Field created by moving charges
- **Magnetic flux**: Measure of field through surface
- **Inductance**: Opposition to change in current; induced EMF
- **Electromagnetic wave**: Self-propagating oscillation of E and B fields
- **Maxwell's equations**: Four fundamental laws unifying electromagnetism

---

## Summary

Electromagnetism unifies electric and magnetic phenomena into a single fundamental force. Electric charges create electric fields and exert forces following Coulomb's law (F = kq₁q₂/r²). Moving charges constitute electric current, governed by Ohm's law (V = IR) in resistive materials. Capacitors store charge and energy, while inductors resist current changes. Magnetic fields exert forces on moving charges (**F** = q**v** × **B**) and are produced by currents (Ampère's law). Faraday discovered that changing magnetic flux induces electric fields and EMF, the principle behind generators and transformers. Maxwell synthesized electricity and magnetism into four elegant equations, predicting electromagnetic waves traveling at light speed—revealing light itself as electromagnetic radiation. The electromagnetic spectrum spans radio waves to gamma rays, all following the same physics but at different frequencies. This framework underpins virtually all modern technology: electric power generation and transmission, motors, telecommunications, computers, medical imaging, and countless other applications that define contemporary civilization.
