# Classical Mechanics

## Overview

Classical mechanics describes the motion of macroscopic objects—from falling apples to orbiting planets. Developed primarily by Isaac Newton in the 17th century, it remains accurate for everyday situations where speeds are much less than light speed and objects are much larger than atoms. Classical mechanics forms the foundation for engineering, architecture, and our intuitive understanding of how things move.

## Newton's Laws of Motion

The three laws proposed by Isaac Newton in 1687 form the cornerstone of classical mechanics.

### First Law (Law of Inertia)

**Statement**: An object at rest stays at rest, and an object in motion stays in motion with constant velocity, unless acted upon by a net external force.

**Meaning**: Objects resist changes to their motion. This resistance is called **inertia**.

**Formula**: If ΣF = 0, then **v** = constant

**Real-World Examples**:
- Passengers lurch forward when a car brakes suddenly (their bodies want to maintain forward motion)
- A hockey puck slides across ice with minimal friction, continuing nearly indefinitely
- Spacecraft coast through space without engines once accelerated
- A tablecloth can be yanked from under dishes if pulled quickly enough

### Second Law (F = ma)

**Statement**: The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.

**Formula**:
```
ΣF = ma
```

Where:
- ΣF = net force (vector sum of all forces) in newtons (N)
- m = mass in kilograms (kg)
- a = acceleration in meters per second squared (m/s²)

**Alternative forms**:
- a = F/m (acceleration increases with force, decreases with mass)
- F = Δp/Δt (force equals rate of change of momentum)

**Real-World Examples**:
- Pushing an empty shopping cart vs. a full one—same force produces less acceleration with more mass
- Rocket engines: large force produces large acceleration
- An elephant requires more force to accelerate than a mouse

### Third Law (Action-Reaction)

**Statement**: For every action, there is an equal and opposite reaction. When object A exerts a force on object B, object B simultaneously exerts an equal force in the opposite direction on object A.

**Formula**: F₁₂ = -F₂₁

**Important Note**: Action-reaction pairs act on *different* objects, so they don't cancel out.

**Real-World Examples**:
- Rocket propulsion: gases pushed down by engine, rocket pushed up
- Walking: foot pushes backward on ground, ground pushes forward on foot
- Swimming: push water backward, water pushes you forward
- Recoil of a gun when firing

## Kinematics: Describing Motion

Kinematics describes motion without considering its causes (forces).

### Key Variables

| Symbol | Quantity | Unit |
|--------|----------|------|
| x, s, d | Position/displacement | m |
| v | Velocity | m/s |
| a | Acceleration | m/s² |
| t | Time | s |

### Motion with Constant Velocity

When acceleration = 0:
```
x = x₀ + vt
```

### Motion with Constant Acceleration

The **kinematic equations** apply when acceleration is constant:

1. **v = v₀ + at**
   - Final velocity from initial velocity and acceleration

2. **x = x₀ + v₀t + ½at²**
   - Position as function of time

3. **v² = v₀² + 2a(x - x₀)**
   - Velocity from position (time-independent)

4. **x = x₀ + ½(v₀ + v)t**
   - Average velocity form

### Free Fall

Objects falling under gravity alone experience constant acceleration:
- g = 9.8 m/s² (Earth's surface)
- Independent of mass (Galileo's discovery)
- Equations: v = v₀ + gt; y = y₀ + v₀t - ½gt²

**Example**: Drop a ball from 20 m height. How long to hit ground?
- y₀ = 20 m, y = 0, v₀ = 0, a = -9.8 m/s²
- 0 = 20 + 0 - ½(9.8)t²
- t = √(40/9.8) ≈ 2.0 s

## Vectors and Motion in 2D/3D

### Vector Basics

Vectors have magnitude and direction. Essential for representing:
- Displacement
- Velocity
- Acceleration
- Force

**Component form**: **v** = vₓ**i** + vᵧ**j** + vᵤ**k**

**Magnitude**: |**v**| = √(vₓ² + vᵧ² + vᵤ²)

### Projectile Motion

Objects launched at an angle follow parabolic trajectories.

**Key insight**: Horizontal and vertical motions are independent.

**Horizontal motion** (no acceleration):
- vₓ = v₀ cos θ
- x = v₀ cos θ × t

**Vertical motion** (gravity):
- vᵧ = v₀ sin θ - gt
- y = v₀ sin θ × t - ½gt²

**Range** (horizontal distance): R = (v₀² sin 2θ)/g

**Maximum range**: 45° angle gives longest horizontal distance

**Example**: Baseball hit at 30 m/s at 40° angle. How far does it travel?
- R = (30² × sin 80°)/9.8 ≈ 92 m

### Circular Motion

Object moving in circle at constant speed still accelerates (direction changes).

**Centripetal acceleration**: a = v²/r (directed toward center)

**Centripetal force**: F = mv²/r

**Period**: T = 2πr/v (time for one revolution)

**Real-World Examples**:
- Cars turning corners
- Satellites orbiting Earth
- Electrons orbiting nuclei (classical model)
- Centrifuges separating materials

## Forces and Free-Body Diagrams

### Common Forces

| Force | Symbol | Description | Formula |
|-------|--------|-------------|---------|
| **Gravity (Weight)** | Fg or W | Attraction to Earth | W = mg |
| **Normal Force** | N | Surface pushing perpendicular | N = mg cos θ (incline) |
| **Friction** | f | Opposes relative motion | f ≤ μN |
| **Tension** | T | Pull through rope/string | Varies by situation |
| **Spring Force** | Fs | Elastic restoration | Fs = -kx (Hooke's law) |
| **Drag** | Fd | Fluid resistance | Fd = ½ρv²CdA (turbulent) |

### Friction

**Static friction** (prevents motion): fs ≤ μs N
- μs = coefficient of static friction
- Acts to prevent slipping

**Kinetic friction** (during motion): fk = μk N
- μk = coefficient of kinetic friction
- Usually μk < μs (easier to keep moving than to start)

### Free-Body Diagrams

Systematic approach to solving force problems:

1. **Isolate object**: Focus on one object at a time
2. **Draw all forces**: Show every force as arrow from object's center
3. **Choose axes**: Usually parallel/perpendicular to motion
4. **Resolve components**: Break angled forces into x and y components
5. **Apply F = ma**: Write equations for each axis
6. **Solve**: Algebra to find unknowns

**Example**: Block on 30° incline, coefficient of friction μ = 0.3. Does it slide?
- Forces: gravity (mg), normal (N), friction (f)
- Parallel to incline: mg sin 30° - f = ma
- Perpendicular: N - mg cos 30° = 0
- N = mg cos 30°
- Maximum friction: fmax = μN = 0.3mg cos 30° ≈ 0.26mg
- Gravity component down incline: mg sin 30° = 0.5mg
- 0.5mg > 0.26mg → block slides!

## Momentum

**Definition**: Momentum is the product of mass and velocity.

**Formula**: **p** = m**v** (vector quantity)

**Units**: kg⋅m/s

### Conservation of Momentum

**Principle**: In an isolated system (no external forces), total momentum remains constant.

**Formula**: Σ**p**before = Σ**p**after

This is one of the most fundamental conservation laws in physics.

### Types of Collisions

**Elastic Collision**:
- Both momentum and kinetic energy conserved
- Objects bounce off each other
- Example: Billiard balls, atomic collisions

**Inelastic Collision**:
- Momentum conserved
- Kinetic energy NOT conserved (converted to heat, sound, deformation)
- Example: Car crashes, clay balls sticking together

**Perfectly Inelastic Collision**:
- Objects stick together after collision
- Maximum kinetic energy loss (but momentum still conserved)

**Example**: 1000 kg car at 20 m/s hits stationary 1500 kg truck. They stick together. Final velocity?
- pbefore = (1000)(20) + (1500)(0) = 20,000 kg⋅m/s
- pafter = (1000 + 1500)vf = 2500vf
- vf = 20,000/2500 = 8 m/s

### Impulse

**Definition**: Change in momentum caused by a force over time.

**Formula**:
```
J = Δp = FΔt
```

**Insight**: Same momentum change can result from large force over short time or small force over long time.

**Applications**:
- Airbags: extend collision time, reducing peak force
- Catching a ball: pull hands back to extend contact time
- Follow-through in sports: maximize contact time

## Energy

Energy is the capacity to do work. It's a scalar quantity measured in joules (J).

### Forms of Mechanical Energy

**Kinetic Energy (KE)**:
- Energy of motion
- Formula: KE = ½mv²
- Depends on speed squared

**Gravitational Potential Energy (PE)**:
- Energy due to position in gravitational field
- Formula: PEg = mgh
- h = height above reference point

**Elastic Potential Energy**:
- Energy stored in springs/elastic materials
- Formula: PEs = ½kx²
- k = spring constant, x = displacement from equilibrium

### Work-Energy Theorem

**Work** is energy transferred by a force over a distance.

**Formula**: W = Fd cos θ
- F = force magnitude
- d = displacement
- θ = angle between force and displacement

**Work-Energy Theorem**: Net work equals change in kinetic energy
```
Wnet = ΔKE = ½mv² - ½mv₀²
```

**Sign conventions**:
- Positive work: force component along motion (increases energy)
- Negative work: force component against motion (decreases energy)
- Zero work: force perpendicular to motion

### Conservation of Mechanical Energy

**Principle**: In the absence of non-conservative forces (like friction), total mechanical energy remains constant.

```
E = KE + PE = constant
```

Or: KEi + PEi = KEf + PEf

**Example**: Roller coaster at 40 m height, v = 0. What's velocity at bottom?
- Top: E = mgh + 0 = mg(40)
- Bottom: E = ½mv² + 0
- mg(40) = ½mv²
- v = √(2gh) = √(2 × 9.8 × 40) ≈ 28 m/s

### Power

**Definition**: Rate of energy transfer or work done per unit time.

**Formula**: P = W/t = E/t

**Alternative**: P = F⋅v (force times velocity)

**Unit**: Watt (W) = J/s

**Example**: 1000 kg car accelerates from 0 to 25 m/s in 10 s. What power is required?
- ΔKE = ½(1000)(25²) - 0 = 312,500 J
- P = 312,500/10 = 31,250 W = 31.25 kW

## Rotational Motion

Objects can rotate as well as translate. Rotational mechanics parallels linear mechanics.

### Rotational Variables

| Linear | Rotational | Relationship |
|--------|-----------|--------------|
| Position (x) | Angle (θ) | x = rθ |
| Velocity (v) | Angular velocity (ω) | v = rω |
| Acceleration (a) | Angular acceleration (α) | a = rα |
| Mass (m) | Moment of inertia (I) | I = Σmr² |
| Force (F) | Torque (τ) | τ = rF sin θ |
| Momentum (p) | Angular momentum (L) | L = Iω |

### Rotational Kinetic Energy

```
KErot = ½Iω²
```

**Total kinetic energy** for rolling object: KE = ½mv² + ½Iω²

### Torque

**Definition**: Rotational equivalent of force; causes angular acceleration.

**Formula**: τ = rF sin θ
- r = distance from rotation axis
- F = force magnitude
- θ = angle between r and F

**Torque and angular acceleration**: τ = Iα

### Angular Momentum

**Definition**: L = Iω

**Conservation**: In absence of external torques, angular momentum is conserved.

**Example**: Ice skater pulls arms in and spins faster
- I decreases (mass closer to axis)
- L = Iω = constant
- Therefore ω increases

## Gravity and Orbital Mechanics

### Newton's Law of Universal Gravitation

**Statement**: Every mass attracts every other mass with a force proportional to the product of their masses and inversely proportional to the square of the distance between them.

**Formula**:
```
F = G(m₁m₂)/r²
```

Where G = 6.674 × 10⁻¹¹ N⋅m²/kg²

### Gravitational Field

**Definition**: Force per unit mass at a location.

**Formula**: g = GM/r²

At Earth's surface: g = 9.8 m/s²

### Orbital Motion

Objects in orbit are in continuous free fall, but moving fast enough that they "miss" the planet.

**Orbital velocity**: v = √(GM/r)

**Orbital period**: T = 2π√(r³/GM)

**Kepler's Laws**:
1. Orbits are ellipses with the Sun at one focus
2. Equal areas swept in equal times (conservation of angular momentum)
3. T² ∝ r³ (period squared proportional to orbital radius cubed)

**Example**: International Space Station orbits at r ≈ 6,700 km from Earth's center.
- v = √(GM/r) ≈ 7.7 km/s
- T = 2π√(r³/GM) ≈ 93 minutes per orbit

---

**Key Terms:**
- **Inertia**: Resistance to changes in motion
- **Force**: Push or pull, measured in newtons (N)
- **Mass**: Amount of matter; measure of inertia
- **Weight**: Gravitational force on an object
- **Momentum**: Product of mass and velocity
- **Impulse**: Change in momentum; force applied over time
- **Work**: Energy transferred by force over distance
- **Power**: Rate of energy transfer
- **Kinetic Energy**: Energy of motion
- **Potential Energy**: Stored energy due to position
- **Torque**: Rotational force
- **Angular Momentum**: Rotational momentum

---

## Summary

Classical mechanics, founded on Newton's three laws of motion, describes how objects move and interact through forces. The first law establishes inertia, the second quantifies force-acceleration relationships (F = ma), and the third reveals action-reaction pairs. Kinematics equations describe motion mathematically, while dynamics explains motion through forces like gravity, friction, and tension. Two powerful conservation principles—momentum and energy—allow solving complex problems without tracking all forces. Momentum (p = mv) is conserved in isolated systems, governing collisions and explosions. Mechanical energy (kinetic plus potential) is conserved when only conservative forces act. These principles extend to rotational motion through analogous concepts: torque, angular momentum, and moment of inertia. Newton's law of universal gravitation explains both falling apples and orbiting planets, unifying terrestrial and celestial mechanics. Classical mechanics remains indispensable for engineering, sports, transportation, and understanding everyday motion, forming the foundation upon which relativity and quantum mechanics built modern physics.
