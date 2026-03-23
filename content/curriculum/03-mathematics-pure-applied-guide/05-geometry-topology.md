# Geometry and Topology

## Overview

Geometry studies shapes, sizes, positions, and spatial relationships. Topology studies properties preserved under continuous deformations—the "rubber sheet geometry" where stretching and bending are allowed but tearing and gluing are not. Together, they provide frameworks for understanding space at all scales, from the microscopic structure of molecules to the large-scale structure of the universe.

## Euclidean Geometry: The Classical Framework

### Historical Foundation

**Euclid's Elements** (c. 300 BCE): Most influential mathematics text ever written. Based on:

**Five Postulates** (axioms):
1. A straight line can be drawn between any two points
2. A line segment can be extended indefinitely
3. A circle can be drawn with any center and radius
4. All right angles are equal
5. **Parallel Postulate**: If a line intersects two lines forming interior angles summing to less than 180°, the lines meet on that side

The fifth postulate seemed more complex—attempts to derive it from the other four eventually led to non-Euclidean geometry.

### Basic Euclidean Facts

**Pythagorean Theorem**: In right triangle with legs a, b and hypotenuse c:

**a² + b² = c²**

**Proof**: Hundreds exist; fundamental to distance and trigonometry

**Triangle properties**:
- Interior angles sum to 180°
- Exterior angle equals sum of non-adjacent interior angles
- Similar triangles have proportional sides

**Circle properties**:
- Circumference: C = 2πr
- Area: A = πr²
- Inscribed angle is half central angle

### Coordinate Geometry (Analytic Geometry)

**Descartes' insight** (1637): Represent geometric objects with equations

**Distance formula** (Pythagorean theorem in coordinates):
d = √[(x₂-x₁)² + (y₂-y₁)²]

**Line**: y = mx + b (slope-intercept form)
- Slope: m = (y₂-y₁)/(x₂-x₁)
- Parallel lines: equal slopes
- Perpendicular lines: slopes multiply to -1

**Circle**: (x-h)² + (y-k)² = r²
- Center: (h, k)
- Radius: r

**Conic sections** (intersections of plane and cone):
- **Parabola**: y = ax² + bx + c
- **Ellipse**: (x²/a²) + (y²/b²) = 1
- **Hyperbola**: (x²/a²) - (y²/b²) = 1

**Applications**:
- Parabolas: Projectile motion, satellite dishes (focus property)
- Ellipses: Planetary orbits (Kepler's first law)
- Hyperbolas: Navigation (LORAN), lens design

### Three-Dimensional Geometry

**Distance in 3D**: d = √[(x₂-x₁)² + (y₂-y₁)² + (z₂-z₁)²]

**Plane equation**: ax + by + cz = d
- Normal vector: **n** = ⟨a, b, c⟩ (perpendicular to plane)

**Sphere**: (x-h)² + (y-k)² + (z-l)² = r²

**Volume formulas**:
- Sphere: V = (4/3)πr³
- Cylinder: V = πr²h
- Cone: V = (1/3)πr²h

## Non-Euclidean Geometry: Breaking Euclid's Fifth

### Historical Revolution

**19th century**: Mathematicians questioned parallel postulate

**Gauss** (1820s): Discovered non-Euclidean geometry but didn't publish (feared controversy)

**Bolyai & Lobachevsky** (1830s): Independently published hyperbolic geometry

**Riemann** (1854): Developed elliptic geometry and general theory of curved spaces

**Impact**: Shattered 2000-year assumption that Euclidean geometry was the only possibility. Paved way for Einstein's general relativity.

### Hyperbolic Geometry

**Parallel postulate replaced**: Through point not on line, **infinitely many** parallels exist

**Model**: Poincaré disk (circles and circular arcs)

**Properties**:
- Triangles have angle sum **< 180°**
- Circumference of circle grows exponentially with radius
- Area of triangle determined solely by angles

**Applications**:
- Special relativity (hyperbolic rotations = Lorentz transformations)
- Hyperbolic space in neural networks (better embeddings for hierarchical data)
- Theoretical physics (AdS/CFT correspondence)

### Elliptic Geometry (Spherical Geometry)

**Parallel postulate replaced**: **No** parallel lines exist (all lines intersect)

**Model**: Surface of sphere (great circles are "lines")

**Properties**:
- Triangles have angle sum **> 180°**
- Finite unbounded space (travel far enough, return to start)
- Antipodal points identified (opposite points of sphere are "same")

**Applications**:
- Navigation (Earth's surface approximately spherical)
- General relativity (positive curvature spacetimes)
- Spherical trigonometry (astronomy, geodesy)

### Curvature

**Gaussian curvature** K:
- **K > 0**: Elliptic (sphere-like) — triangles have angle sum > 180°
- **K = 0**: Euclidean (flat) — triangles have angle sum = 180°
- **K < 0**: Hyperbolic (saddle-like) — triangles have angle sum < 180°

**Gauss's Theorema Egregium**: Curvature is **intrinsic** (determined by measurements within surface, not embedding in higher dimension)

**Significance**: An ant on a surface can determine its curvature without leaving the surface

## Differential Geometry

### Curves

**Parametric representation**: **r**(t) = ⟨x(t), y(t), z(t)⟩

**Tangent vector**: **r**'(t) = ⟨x'(t), y'(t), z'(t)⟩

**Arc length**: L = ∫ ||**r**'(t)|| dt

**Curvature** κ: Measures how quickly curve bends

**Applications**:
- Computer graphics (Bézier curves, splines)
- Robotics (path planning)
- Physics (particle trajectories)

### Surfaces

**Parameterization**: **r**(u, v) = ⟨x(u,v), y(u,v), z(u,v)⟩

**Normal vector**: **n** = (∂**r**/∂u) × (∂**r**/∂v)

**Gaussian curvature**: Intrinsic measure of bending

**Mean curvature**: Average of principal curvatures (extrinsic)

**Minimal surfaces**: Zero mean curvature everywhere
- Soap films naturally form minimal surfaces
- Applications: architecture, materials science

### Riemannian Geometry

**Generalization**: Study curved spaces of any dimension

**Metric tensor**: g gives notion of distance and angle in curved space

**Geodesics**: Shortest paths in curved space (generalizations of straight lines)
- On sphere: Great circles
- In spacetime: Trajectories of freely falling objects

**Christoffel symbols**: Encode how to take derivatives in curved space

**Riemann curvature tensor**: Complete description of curvature

**Einstein's general relativity**:
**Gμν = (8πG/c⁴)Tμν**

Geometry of spacetime (left side) determined by matter/energy (right side)

## Topology: The Mathematics of Continuity

### Basic Concepts

**Topological space**: Set with notion of "nearness" (open sets)

**Continuous function**: f: X → Y where preimages of open sets are open

**Intuition**: Can be drawn without lifting pen; no sudden jumps

**Homeomorphism**: Continuous bijection with continuous inverse

**Topological equivalence**: Objects related by homeomorphism (same from topology's viewpoint)

### The Coffee Cup and Donut

**Famous example**: Coffee cup is homeomorphic to donut (torus)

**Reason**: Both have one hole. Can continuously deform one into other (stretching, bending—no tearing or gluing).

**Not equivalent**: Sphere (no holes) is not homeomorphic to torus (one hole)

### Topological Invariants

Properties preserved under homeomorphism:

#### 1. Euler Characteristic (χ)

**Formula**: χ = V - E + F (vertices - edges + faces)

**Examples**:
- Sphere: χ = 2
- Torus: χ = 0
- Double torus: χ = -2
- In general: χ = 2 - 2g (where g = number of holes/genus)

**Application**: If χ differs, objects cannot be homeomorphic

#### 2. Genus (Number of Holes)

- Sphere: g = 0
- Torus: g = 1
- Pretzel with n holes: g = n

#### 3. Fundamental Group

Classifies loops in space:
- Sphere: All loops contractible (can shrink to point)
- Torus: Non-contractible loops exist (around hole)

**Applications**: Robotics (configuration spaces), data analysis (topological data analysis)

### Surfaces

**Classification Theorem**: Every compact surface without boundary is homeomorphic to:
- Sphere
- Connected sum of n tori (n-holed torus)
- Connected sum of n projective planes

**Orientability**:
- **Orientable**: Has consistent "inside" and "outside" (sphere, torus)
- **Non-orientable**: Möbius strip, Klein bottle (one-sided surfaces)

**Möbius strip**: Take rectangle, give one end half-twist, glue ends
- One side, one edge
- Walking along strip returns you upside-down

**Klein bottle**: Möbius strip with no boundary (4D to embed without self-intersection)

### Knot Theory

**Knot**: Closed loop in 3D space

**Question**: When are two knots equivalent (can one be continuously deformed into other)?

**Unknot**: Simple loop with no crossings (topologically trivial)

**Trefoil knot**: Simplest non-trivial knot

**Knot invariants**: Properties distinguishing knots
- Alexander polynomial
- Jones polynomial
- Knot genus

**Applications**:
- DNA topology (how DNA strands tangle/untangle)
- Quantum field theory (Chern-Simons theory)
- Chemistry (molecular knots)

### Algebraic Topology

**Idea**: Assign algebraic objects (groups, rings) to topological spaces

**Homology groups**: Detect holes of various dimensions
- H₀: Connected components
- H₁: 1D holes (loops)
- H₂: 2D holes (voids)

**Example - Torus**:
- H₀ = ℤ (one component)
- H₁ = ℤ ⊕ ℤ (two independent loops)
- H₂ = ℤ (one 2D void)

**Applications**:
- Topological data analysis (TDA): Find structure in high-dimensional data
- Sensor networks: Coverage and connectivity
- Materials science: Porous materials characterization

## Advanced Topics

### Manifolds

**Definition**: Space locally resembling Euclidean space

**Examples**:
- 1-manifold: Circle, line
- 2-manifold: Sphere, torus, plane
- 3-manifold: 3-sphere S³, 3-torus
- n-manifold: n-dimensional "surface"

**Differentiable manifold**: Can do calculus (smooth structure)

**Applications**:
- Physics: Configuration spaces, spacetime
- Robotics: Robot arm positions form manifold
- Machine learning: Data often lies on low-dimensional manifold in high-dimensional space

### Four-Color Theorem

**Statement**: Every planar map can be colored with 4 colors so adjacent regions have different colors

**History**:
- Conjectured 1852
- First "proof" 1879 (flawed)
- Valid proof 1976 (Appel & Haken)—first major theorem proved by computer

**Significance**: Demonstrated computers can assist in proofs; sparked debate about nature of mathematical proof

### Poincaré Conjecture (Now Theorem)

**Statement**: Every simply connected, closed 3-manifold is homeomorphic to 3-sphere

**History**:
- Conjectured 1904 by Henri Poincaré
- One of seven Millennium Prize Problems
- Proved 2003 by Grigori Perelman (declined Fields Medal and $1M prize)

**Significance**: Classifies 3-manifolds (like Earth's spatial shape if universe is closed)

## Real-World Applications

### General Relativity

**Einstein's insight**: Gravity is curvature of spacetime

**Mathematics**: Riemannian geometry (4D spacetime with Lorentzian metric)

**Geodesics**: Free-fall trajectories (planets orbit Sun along geodesics)

**Predictions**:
- Bending of light by massive objects (confirmed 1919)
- Gravitational time dilation (GPS must account for this)
- Black holes (regions where curvature becomes infinite)
- Gravitational waves (ripples in spacetime curvature, detected 2015)

### Computer Graphics

**3D modeling**: Objects represented as meshes (vertices, edges, faces)

**Rendering**: Project 3D scene onto 2D screen (perspective transformation)

**Texture mapping**: Map 2D images onto 3D surfaces using parametrization

**Curvature**: Shading and lighting calculations depend on surface normals and curvature

### Robotics

**Configuration space**: Positions/orientations of robot form manifold

**Path planning**: Find geodesic in configuration space avoiding obstacles

**Inverse kinematics**: Given desired endpoint, find joint angles (topology of solution space matters)

### Data Analysis (Topological Data Analysis)

**Problem**: Understand shape of high-dimensional data

**Method**:
1. Build simplicial complex from point cloud
2. Compute persistent homology (tracks features across scales)
3. Identify topological features (clusters, loops, voids)

**Applications**:
- Image recognition
- Sensor networks
- Biological shape analysis (protein folding)

### GPS and Navigation

**Problem**: Find shortest path on Earth's surface

**Solution**: Great circle routes (geodesics on sphere)

**Spherical trigonometry**: Calculate distances and directions

### Materials Science

**Porous materials**: Topology characterizes connectivity of pores

**Crystals**: Symmetry groups (combination of geometry and group theory)

**Liquid crystals**: Topological defects (singularities in orientation field)

## Key Terms

| Term | Definition |
|------|------------|
| **Euclidean geometry** | Geometry based on Euclid's axioms (flat space) |
| **Non-Euclidean geometry** | Hyperbolic or elliptic geometry (curved spaces) |
| **Curvature** | Measure of how space deviates from flatness |
| **Geodesic** | Shortest path in curved space |
| **Topology** | Study of properties preserved under continuous deformations |
| **Homeomorphism** | Continuous bijection with continuous inverse |
| **Euler characteristic** | Topological invariant: χ = V - E + F |
| **Genus** | Number of "holes" in surface |
| **Manifold** | Space locally resembling Euclidean space |
| **Differential geometry** | Geometry using calculus (curves, surfaces, curvature) |

## Summary

Geometry studies shape, size, and spatial relationships. Euclidean geometry, codified in Euclid's Elements 2300 years ago, dominated mathematics until the 19th century discovery of non-Euclidean geometries—hyperbolic and elliptic—where the parallel postulate fails. These reveal that multiple consistent geometric systems exist, distinguished by curvature.

Differential geometry applies calculus to study curves and surfaces, introducing concepts like curvature and geodesics. Riemannian geometry generalizes to curved spaces of any dimension, providing the mathematical language for Einstein's general relativity, where gravity emerges as spacetime curvature.

Topology studies properties preserved under continuous deformations—the "rubber sheet geometry" where shapes can stretch and bend but not tear. Topological invariants like Euler characteristic and genus distinguish spaces. Knot theory classifies tangled loops. Algebraic topology uses groups and homology to detect holes and classify spaces.

Applications span physics (general relativity, quantum field theory), computer graphics (3D modeling, rendering), robotics (configuration spaces, path planning), and data science (topological data analysis). From ancient Greek geometry through Gaussian curvature, non-Euclidean geometries, Einstein's spacetime, and modern topological data analysis, these fields continue revealing the deep structure of space at all scales.
