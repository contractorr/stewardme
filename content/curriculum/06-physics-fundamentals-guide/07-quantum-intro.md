# Introduction to Quantum Mechanics

## Overview

Quantum mechanics governs the behavior of matter and energy at atomic and subatomic scales. Developed in the early 20th century to explain phenomena classical physics could not, it reveals a world fundamentally different from everyday experience: particles behave as waves, measurements affect reality, and uncertainty is built into nature. Despite its counterintuitive nature, quantum mechanics is the most precisely tested theory in science, underlying chemistry, solid-state physics, electronics, and modern technology from semiconductors to lasers to quantum computers. This chapter introduces the key concepts that revolutionized physics and continue to shape our understanding of reality.

## The Quantum Revolution

### Limitations of Classical Physics

By 1900, physics appeared nearly complete, but several observations defied explanation:

**1. Blackbody radiation**:
- Classical prediction: Infinite energy radiated at short wavelengths ("ultraviolet catastrophe")
- Reality: Energy distribution peaks at specific wavelength, depends on temperature

**2. Photoelectric effect**:
- Light ejects electrons from metal
- Classical prediction: Brighter light → more energetic electrons
- Reality: Frequency determines electron energy; intensity only affects number

**3. Atomic spectra**:
- Atoms emit/absorb light at discrete wavelengths (line spectra)
- Classical physics predicted continuous spectra
- Each element has unique "fingerprint"

**4. Stability of atoms**:
- Classical theory: Orbiting electrons should radiate energy, spiral into nucleus in ~10⁻¹¹ s
- Reality: Atoms are stable

**5. Specific heats**:
- Classical predictions for heat capacity failed at low temperatures

### Timeline of Quantum Mechanics

| Year | Scientist | Discovery |
|------|-----------|-----------|
| 1900 | Max Planck | Energy quantization (E = hf) |
| 1905 | Albert Einstein | Photoelectric effect, light quanta (photons) |
| 1913 | Niels Bohr | Quantum model of hydrogen atom |
| 1923 | Louis de Broglie | Matter waves (λ = h/p) |
| 1925 | Werner Heisenberg | Matrix mechanics, uncertainty principle |
| 1926 | Erwin Schrödinger | Wave equation |
| 1926 | Max Born | Probability interpretation of wave function |
| 1927 | Davisson-Germer | Electron diffraction (confirmed matter waves) |
| 1928 | Paul Dirac | Relativistic quantum mechanics, antimatter |
| 1932 | Carl Anderson | Discovered positron (antimatter) |

## Planck and Quantization

### Blackbody Radiation Problem

**Blackbody**: Ideal object that absorbs/emits all frequencies of radiation

**Classical prediction** (Rayleigh-Jeans law): Intensity → ∞ as wavelength → 0

**Observation**: Intensity peaks at λmax ∝ 1/T, then decreases (Wien's displacement law)

### Planck's Solution (1900)

**Radical assumption**: Energy is quantized—can only take discrete values.

**Energy quanta**:
```
E = nhf (n = 0, 1, 2, 3, ...)
```
- h = Planck's constant = 6.626 × 10⁻³⁴ J⋅s
- f = frequency

**Planck's Law**: Correctly predicted blackbody spectrum

**Significance**: First quantum hypothesis—energy comes in indivisible "chunks"

## Photoelectric Effect

### Experimental Observations

**Setup**: Shine light on metal surface, measure ejected electrons.

**Findings**:
1. Electrons ejected immediately (no time delay), even for dim light
2. Maximum electron kinetic energy depends on light frequency, not intensity
3. Threshold frequency f₀ below which no electrons ejected (regardless of intensity)
4. Brighter light → more electrons, but same maximum energy

**Classical physics prediction**: Brighter light → more energy → more energetic electrons ❌

### Einstein's Explanation (1905)

**Light quanta (photons)**: Light consists of particle-like packets of energy.

**Energy per photon**: E = hf

**Photoelectric equation**:
```
KEmax = hf - φ
```

Where:
- KEmax = maximum kinetic energy of ejected electron
- hf = photon energy
- φ = work function (minimum energy to remove electron from metal)

**Explanation**:
- One photon ejects one electron (instantaneous)
- Photon energy must exceed work function: hf > φ
- Threshold frequency: f₀ = φ/h
- Extra energy becomes kinetic energy
- Intensity affects photon number (electrons ejected), not individual photon energy

**Nobel Prize**: Einstein received 1921 Nobel Prize for this explanation, not for relativity!

### Implications

**Particle-like behavior of light**:
- Contradicted classical wave theory
- Light exhibits both wave properties (interference, diffraction) and particle properties (photoelectric effect)
- Beginning of wave-particle duality

## Bohr Model of the Atom

### Problems with Classical Atom

**Rutherford's discovery** (1911): Atom has tiny, dense nucleus with electrons orbiting

**Problem**: Accelerating charges radiate energy (Maxwell). Electrons should spiral into nucleus → atoms unstable ❌

### Bohr's Postulates (1913)

**1. Quantized orbits**: Electrons occupy discrete energy levels without radiating

**2. Angular momentum quantization**:
```
L = nℏ (n = 1, 2, 3, ...)
```
- ℏ = h/(2π) = 1.055 × 10⁻³⁴ J⋅s (reduced Planck constant)
- n = principal quantum number

**3. Photon emission/absorption**: Electron transitions between levels emit/absorb photons
```
ΔE = hf
```

### Energy Levels of Hydrogen

**Allowed energies**:
```
En = -13.6 eV / n² (n = 1, 2, 3, ...)
```

**Ground state** (n = 1): E₁ = -13.6 eV (most stable)

**Excited states**: Higher n values, less negative energy

**Ionization**: E = 0 (electron removed)

### Atomic Spectra

**Emission**: Electron drops from higher to lower level
- Energy released as photon: hf = Ehi - Elo
- Creates line spectrum (discrete wavelengths)

**Absorption**: Electron jumps from lower to higher level
- Absorbs photon of specific energy
- Creates dark lines in continuous spectrum

**Spectral series** (hydrogen):
- **Lyman series**: Transitions to n = 1 (ultraviolet)
- **Balmer series**: Transitions to n = 2 (visible)
- **Paschen series**: Transitions to n = 3 (infrared)

**Success**: Bohr model correctly predicted hydrogen spectrum

**Limitation**: Failed for multi-electron atoms; replaced by quantum mechanics

## Matter Waves (De Broglie Hypothesis)

### Wave-Particle Duality for Matter

**Einstein showed**: Light has both wave and particle properties.

**De Broglie (1923)**: If light (wave) can behave as particles, can particles behave as waves?

**De Broglie wavelength**:
```
λ = h/p
```

Where:
- λ = wavelength
- h = Planck's constant
- p = momentum = mv

**Implications**:
- All matter has associated wavelength
- For macroscopic objects (large p), λ is tiny, unobservable
- For electrons, atoms, λ is significant

### Examples

**Electron** (100 eV kinetic energy):
- p = √(2mKE) ≈ 5.4 × 10⁻²⁴ kg⋅m/s
- λ = h/p ≈ 0.12 nm (atomic scale!)

**Baseball** (40 m/s):
- p = mv ≈ 6 kg⋅m/s
- λ = h/p ≈ 10⁻³⁴ m (impossibly small, no wave behavior observable)

### Experimental Confirmation

**Davisson-Germer experiment (1927)**:
- Fired electrons at nickel crystal
- Observed interference pattern (like X-ray diffraction)
- Proved electrons behave as waves
- Measured wavelength matched de Broglie prediction

**Other confirmations**:
- Neutron diffraction
- Atomic and molecular beams show interference
- Electron microscopes exploit wave nature

## Wave Function and Probability

### The Schrödinger Equation

**Schrödinger (1926)** developed equation describing matter waves:

**Time-independent Schrödinger equation**:
```
-ℏ²/(2m) ∇²ψ + Vψ = Eψ
```

**Wave function** (ψ): Mathematical description of quantum state
- Complex-valued function
- Contains all information about system

**Not directly observable**: ψ itself has no physical meaning

### Born's Probability Interpretation

**Max Born (1926)**: |ψ|² gives probability density

**Probability of finding particle in region**:
```
P = ∫|ψ(x)|² dx
```

**Normalization**: Total probability = 1
```
∫₋∞^∞ |ψ(x)|² dx = 1
```

**Interpretation**:
- Quantum mechanics is inherently probabilistic
- Can only predict probabilities, not definite outcomes
- Measurement "collapses" wave function to definite value

### Example: Particle in a Box

**Setup**: Particle confined to region 0 < x < L, infinite potential walls outside

**Allowed energies** (quantized):
```
En = n²π²ℏ²/(2mL²) (n = 1, 2, 3, ...)
```

**Wave functions**:
```
ψn(x) = √(2/L) sin(nπx/L)
```

**Key features**:
- Only discrete energies allowed (quantization)
- Ground state (n = 1) has nonzero energy (zero-point energy)
- Higher n → more nodes (zeros) in wave function
- Probability density |ψ|² shows where particle likely found

## The Uncertainty Principle

### Heisenberg's Uncertainty Principle (1927)

**Statement**: Certain pairs of properties cannot be simultaneously known with arbitrary precision.

**Position-Momentum**:
```
Δx Δp ≥ ℏ/2
```

**Energy-Time**:
```
ΔE Δt ≥ ℏ/2
```

**Meaning**:
- Not about measurement limitations or disturbance
- Fundamental property of nature
- The more precisely you know position, the less precisely you know momentum (and vice versa)

### Implications

**Not experimental error**: No improvement in instruments can circumvent uncertainty

**Not about disturbing system**: Wave nature of matter inherently has spread in position and momentum

**Examples**:
- Confine electron to small space (small Δx) → large momentum uncertainty (large Δp)
- Measure energy precisely (small ΔE) → large time uncertainty (large Δt)

### Virtual Particles

**Energy-time uncertainty**: ΔE Δt ≥ ℏ/2

**Implication**: Energy can fluctuate by ΔE for time Δt ≈ ℏ/(2ΔE)

**Virtual particles**: Particle-antiparticle pairs can briefly appear from vacuum
- Exist for ~ℏ/(2mc²)
- Too short to violate energy conservation
- Measurable effects (Casimir effect, Lamb shift)

### Zero-Point Energy

**Consequence**: Ground state cannot have zero energy

**Reasoning**: If E = 0, both position and momentum would be exactly known → violates uncertainty principle

**Particle in box**: E₁ = π²ℏ²/(2mL²) ≠ 0

**Applications**:
- Helium remains liquid at absolute zero (zero-point motion prevents freezing)
- Quantum vacuum energy (possibly related to dark energy)

## Quantum Tunneling

### Classical vs. Quantum Barrier

**Classical**: Particle cannot pass barrier if KE < barrier height
- Ball rolling toward hill: turns around if insufficient energy

**Quantum**: Wave function penetrates barrier
- Non-zero probability of finding particle on other side
- Particle can "tunnel" through barrier even if E < V

### Tunneling Probability

**Transmission coefficient**: T ≈ e^(-2κL)
- κ = √[2m(V-E)/ℏ²]
- L = barrier width
- V = barrier height
- E = particle energy

**Factors increasing tunneling**:
- Thinner barrier (smaller L)
- Lower barrier (smaller V - E)
- Lighter particle (smaller m)

### Applications

**1. Nuclear fusion (Sun and stars)**:
- Nuclei must overcome Coulomb repulsion to fuse
- Classical temperature required: ~10¹⁰ K
- Actual temperature: ~10⁷ K
- **Quantum tunneling** allows fusion at lower temperatures

**2. Alpha decay**:
- Alpha particles trapped in nucleus by strong force
- Classically cannot escape
- Tunnel through barrier → radioactive decay

**3. Scanning tunneling microscope (STM)**:
- Electron tunneling between sharp tip and surface
- Measures surface topology at atomic resolution
- Can image and manipulate individual atoms

**4. Tunnel diodes and transistors**:
- Fast switching in electronics
- Essential for modern microprocessors

**5. DNA mutation**:
- Proton tunneling can cause spontaneous mutations

## Quantum States and Superposition

### Superposition Principle

**Definition**: A quantum system can exist in a combination (superposition) of multiple states simultaneously.

**Mathematical form**: ψ = c₁ψ₁ + c₂ψ₂ + ...
- c₁, c₂ = complex coefficients
- |c₁|² = probability of measuring system in state ψ₁

**Example**: Electron can be in superposition of spin up and spin down until measured

### Wave Function Collapse

**Before measurement**: System in superposition of states

**Measurement**: Wave function "collapses" to one definite state
- Probabilistic: |cn|² gives probability of outcome n
- Instantaneous and irreversible
- Measurement problem: Unsolved philosophical issue

### Quantum Entanglement

**Definition**: Two or more particles in correlated quantum state; measuring one instantly affects the other.

**EPR paradox** (Einstein, Podolsky, Rosen, 1935):
- Argued quantum mechanics incomplete
- "Spooky action at a distance"

**Bell's theorem (1964)**:
- Testable predictions distinguish quantum mechanics from local hidden variable theories
- Experiments confirm quantum mechanics

**Properties**:
- Correlations stronger than classically possible
- No faster-than-light communication (no information transmitted)
- Fundamental feature of quantum mechanics

**Applications**:
- Quantum cryptography (secure communication)
- Quantum teleportation (state transfer)
- Quantum computing (quantum algorithms)

## Double-Slit Experiment

### The Quintessential Quantum Experiment

**Setup**: Particles (electrons, photons, atoms) fired at barrier with two slits, detector screen behind.

**Classical expectation** (particles): Two bands on screen (some through slit 1, some through slit 2)

**Classical expectation** (waves): Interference pattern (constructive and destructive interference)

### Observations

**1. Both slits open**: Interference pattern appears
- Even one particle at a time!
- Each particle interferes with itself
- Particle goes through both slits simultaneously (superposition)

**2. Measure which slit**: Interference disappears
- Two bands appear (particle behavior)
- Measurement collapses wave function
- Determines which slit, destroys superposition

**3. Delayed choice**: Decide to measure after particle passes slits
- Still affects interference pattern
- Suggests measurement affects past?
- Actually: no paradox, wave function encompasses entire experiment

### Interpretation

**Wave-particle duality**: Particle exhibits wave or particle behavior depending on observation

**Complementarity** (Bohr): Wave and particle descriptions are complementary, not contradictory

**Measurement affects reality**: Observer plays active role in quantum phenomena

## Quantum Numbers and Atomic Structure

### Four Quantum Numbers

Describe electron state in atom:

**1. Principal quantum number (n)**:
- n = 1, 2, 3, ... (shell)
- Determines energy and size of orbital
- Higher n → higher energy, larger orbital

**2. Angular momentum quantum number (l)**:
- l = 0, 1, 2, ..., n-1 (subshell)
- Determines shape of orbital
- l = 0 (s), 1 (p), 2 (d), 3 (f)

**3. Magnetic quantum number (ml)**:
- ml = -l, -l+1, ..., 0, ..., l-1, l
- Determines orbital orientation
- 2l + 1 possible values

**4. Spin quantum number (ms)**:
- ms = +½ or -½ (spin up or down)
- Intrinsic angular momentum
- Not classical spinning, but quantum property

### Pauli Exclusion Principle

**Statement**: No two electrons in an atom can have the same set of four quantum numbers.

**Consequence**: Electrons fill orbitals from lowest to highest energy

**Explains**:
- Atomic structure
- Periodic table organization
- Chemical bonding
- Electron configuration

### Electron Configuration

**Aufbau principle**: Fill lowest energy orbitals first

**Hund's rule**: Maximize parallel spins in degenerate orbitals

**Example (Carbon, 6 electrons)**:
- 1s² 2s² 2p²
- Two electrons in 1s, two in 2s, two in 2p

## Real-World Applications

### Semiconductors and Electronics

**Band structure**: Quantum mechanics explains energy bands in solids
- Valence band (filled)
- Conduction band (empty in insulators, partially filled in conductors)
- Band gap (energy difference)

**Semiconductors** (Si, Ge):
- Small band gap (~1 eV)
- Conductivity controlled by doping, temperature, light

**Transistors**: Quantum mechanical switches
- Foundation of all digital electronics
- Billions per microchip

**LEDs and lasers**: Quantum transitions produce light

### Magnetic Resonance Imaging (MRI)

**Principle**: Quantum spin of protons (in water/fat)
- Strong magnetic field aligns spins
- Radio waves flip spins
- Relaxation time depends on tissue type
- Map creates detailed images

**Advantages**:
- Non-invasive
- No ionizing radiation
- Excellent soft-tissue contrast

### Quantum Computing

**Qubit**: Quantum bit, can be 0, 1, or superposition of both

**Advantages**:
- Massive parallelism (exponentially many states)
- Quantum algorithms (Shor's factoring, Grover's search)
- Potentially solve intractable problems

**Challenges**:
- Decoherence (interaction with environment destroys superposition)
- Error correction
- Scaling to many qubits

**Current state**: 50-1000 qubits, demonstrating quantum advantage for specific problems

### Lasers

**LASER**: Light Amplification by Stimulated Emission of Radiation

**Quantum process**:
1. Pump electrons to excited state
2. Stimulated emission: Photon triggers identical photon emission
3. Cascade creates coherent light

**Properties**: Monochromatic, coherent, collimated, intense

**Applications**: Surgery, cutting, communication, measurement, spectroscopy, entertainment

### Chemistry and Materials

**Chemical bonds**: Quantum mechanics explains covalent, ionic, metallic bonding

**Molecular structure**: Electron orbitals determine geometry

**Spectroscopy**: Analyze materials by quantum transitions

**Superconductivity**: Quantum phenomenon (zero resistance below critical temperature)

**Superfluidity**: Quantum fluid with zero viscosity

---

**Key Terms:**
- **Quantum**: Discrete, indivisible unit
- **Photon**: Quantum of light (particle of electromagnetic radiation)
- **Wave-particle duality**: Particles exhibit wave properties, waves exhibit particle properties
- **Wave function (ψ)**: Mathematical description of quantum state
- **Probability density**: |ψ|² gives probability of finding particle
- **Uncertainty principle**: Fundamental limit on simultaneous knowledge of conjugate variables
- **Quantization**: Restriction to discrete values (energy, angular momentum)
- **Tunneling**: Quantum penetration through classically forbidden barriers
- **Superposition**: Simultaneous existence in multiple states
- **Entanglement**: Quantum correlation between particles
- **Wave function collapse**: Transition from superposition to definite state upon measurement
- **Zero-point energy**: Minimum energy of quantum system (nonzero)
- **Pauli exclusion principle**: No two fermions can occupy same quantum state

---

## Summary

Quantum mechanics emerged from early 20th-century crises in physics, beginning with Planck's energy quantization (E = hf) to explain blackbody radiation and Einstein's photons explaining the photoelectric effect. Bohr's atomic model introduced quantized energy levels, successfully predicting hydrogen spectra. De Broglie proposed matter waves (λ = h/p), confirmed experimentally, establishing wave-particle duality as fundamental. Schrödinger's wave equation describes quantum systems, with |ψ|² interpreted as probability density (Born), making quantum mechanics inherently probabilistic. Heisenberg's uncertainty principle (Δx Δp ≥ ℏ/2) reveals fundamental limits on simultaneous knowledge, not mere measurement errors. Quantum phenomena like tunneling enable nuclear fusion in stars and underpin scanning tunneling microscopes. Superposition allows systems to exist in multiple states simultaneously until measurement collapses the wave function. The double-slit experiment epitomizes wave-particle duality and measurement's role. Quantum numbers and Pauli's exclusion principle explain atomic structure and the periodic table. Applications span semiconductors, lasers, MRI, quantum computing, and chemistry. Despite its counterintuitive nature—with particles that tunnel, interfere with themselves, and exhibit "spooky" entanglement—quantum mechanics is spectacularly successful, precisely tested, and foundational to modern technology and our understanding of nature at its smallest scales.
