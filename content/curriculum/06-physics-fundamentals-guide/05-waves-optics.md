# Waves and Optics

## Overview

Waves are disturbances that propagate through space and time, transferring energy without transferring matter. From ocean waves to light to quantum matter waves, wave phenomena appear throughout physics. Optics, the study of light and its interactions with matter, reveals wave properties through interference, diffraction, and polarization—while also showing particle aspects (photons). Understanding waves is essential for acoustics, telecommunications, medical imaging, spectroscopy, and quantum mechanics. This chapter explores mechanical waves, sound, electromagnetic waves, and the behavior of light.

## Wave Fundamentals

### What is a Wave?

**Definition**: A wave is a disturbance that transfers energy through a medium or space without net transport of matter.

**Key characteristics**:
- Oscillation or vibration
- Propagation through space
- Energy transfer
- Can interfere with other waves

### Wave Classification

**By medium requirement**:
| Type | Requires Medium? | Examples |
|------|-----------------|----------|
| **Mechanical** | Yes | Sound, water waves, seismic waves |
| **Electromagnetic** | No (can travel in vacuum) | Light, radio waves, X-rays |
| **Matter waves** | N/A (quantum waves) | Electron waves, probability waves |

**By oscillation direction**:
| Type | Oscillation | Examples |
|------|------------|----------|
| **Transverse** | Perpendicular to propagation | Light, string waves, water surface waves |
| **Longitudinal** | Parallel to propagation | Sound, pressure waves, spring compression waves |
| **Surface** | Mixed (circular motion) | Ocean waves |

### Wave Parameters

**Wavelength (λ)**: Distance between consecutive peaks (or any corresponding points)
- Unit: meters (m)

**Frequency (f)**: Number of oscillations per second
- Unit: Hertz (Hz) = 1/s

**Period (T)**: Time for one complete oscillation
- T = 1/f
- Unit: seconds (s)

**Amplitude (A)**: Maximum displacement from equilibrium
- Measures energy (intensity ∝ A²)

**Wave speed (v)**: Speed of wave propagation
- **Fundamental relationship**: v = λf
- Depends on medium properties

**Phase (φ)**: Position within oscillation cycle (radians or degrees)

### Mathematical Description

**Sinusoidal wave traveling in +x direction**:
```
y(x,t) = A sin(kx - ωt + φ)
```

Where:
- k = 2π/λ (wave number, rad/m)
- ω = 2πf (angular frequency, rad/s)
- v = ω/k = λf

**Alternative forms**:
- y(x,t) = A sin[2π(x/λ - t/T)]
- y(x,t) = A cos(kx - ωt + φ)

### Wave Energy and Intensity

**Energy**: Proportional to amplitude squared (E ∝ A²)

**Power**: Energy per unit time (P = E/t)

**Intensity**: Power per unit area (I = P/A)

For waves spreading in 3D: I ∝ 1/r² (inverse square law)

## Mechanical Waves

### Waves on Strings

**Wave speed**:
```
v = √(T/μ)
```
- T = tension (N)
- μ = linear mass density (kg/m)

**Applications**: Musical instruments (guitar, violin, piano strings)

### Sound Waves

**Nature**: Longitudinal pressure waves in medium

**Speed** (depends on medium):
- Air (20°C): 343 m/s
- Water: ~1480 m/s
- Steel: ~5000 m/s

**General formula**: v = √(B/ρ)
- B = bulk modulus (resistance to compression)
- ρ = density

**Temperature dependence** (air): v ≈ 331 + 0.6T m/s (T in °C)

### Human Hearing

**Frequency range**: ~20 Hz to 20,000 Hz (20 kHz)
- **Infrasound**: < 20 Hz (elephants, earthquakes)
- **Ultrasound**: > 20 kHz (bats, medical imaging, sonar)

**Loudness and Decibels**:
- Intensity level: β = 10 log(I/I₀) dB
- I₀ = 10⁻¹² W/m² (threshold of hearing)

**Decibel scale examples**:
| Sound | Intensity Level (dB) |
|-------|---------------------|
| Threshold of hearing | 0 |
| Whisper | 20 |
| Normal conversation | 60 |
| Busy traffic | 80 |
| Jackhammer | 100 |
| Rock concert | 110 |
| Jet engine | 140 |
| Pain threshold | 120-130 |

**Logarithmic scale**: +10 dB = 10× intensity; +20 dB = 100× intensity

### Doppler Effect

**Definition**: Change in observed frequency due to relative motion between source and observer.

**Formulas**:

**Observer moving toward stationary source**:
```
f' = f(1 + vo/v)
```

**Source moving toward stationary observer**:
```
f' = f / (1 - vs/v)
```

**General case**:
```
f' = f(v ± vo) / (v ∓ vs)
```
- Upper signs: approaching
- Lower signs: receding
- v = wave speed
- vo = observer speed
- vs = source speed

**Applications**:
- Radar speed detection
- Redshift in astronomy (cosmological Doppler effect)
- Medical ultrasound (blood flow measurement)
- Weather radar

**Sonic boom**: Occurs when source exceeds wave speed (Mach number > 1)

## Wave Behavior

### Reflection

**Definition**: Wave bounces off boundary.

**Law of reflection**: θi = θr (angle of incidence = angle of reflection)

**Phase change**:
- Reflection from denser medium: 180° phase shift
- Reflection from less dense medium: No phase shift

**Applications**: Mirrors, echoes, sonar

### Refraction

**Definition**: Wave bends when entering different medium due to speed change.

**Snell's Law**:
```
n₁ sin θ₁ = n₂ sin θ₂
```
- n = refractive index = c/v (ratio of light speed in vacuum to speed in medium)
- θ = angle from normal

**Examples**:
- Pencil appearing bent in water (n_water ≈ 1.33)
- Atmospheric refraction (mirages, sun appearing higher at sunrise/sunset)
- Lenses focusing light

**Total internal reflection**: When light travels from denser to less dense medium at angle greater than critical angle
- θc = sin⁻¹(n₂/n₁)
- Used in fiber optics, prisms, diamonds' sparkle

### Superposition Principle

**Statement**: When two or more waves overlap, the resultant displacement equals the sum of individual displacements.

**Formula**: ytotal = y₁ + y₂ + y₃ + ...

**Types of interference**:
- **Constructive**: Waves in phase, amplitudes add (brighter/louder)
- **Destructive**: Waves out of phase, amplitudes subtract (darker/quieter)

### Standing Waves

**Definition**: Pattern formed when two identical waves traveling in opposite directions interfere.

**Characteristics**:
- **Nodes**: Points of zero amplitude (destructive interference)
- **Antinodes**: Points of maximum amplitude (constructive interference)
- Appears stationary (not traveling)

**String fixed at both ends**:
- Wavelengths: λn = 2L/n (n = 1, 2, 3, ...)
- Frequencies: fn = nv/(2L) = nf₁ (harmonics)
- f₁ = fundamental frequency

**Applications**:
- Musical instruments (strings, pipes, drums)
- Microwave ovens (standing waves heat food)
- Electron orbitals (quantum standing waves)

## Interference and Diffraction

### Two-Slit Interference (Young's Experiment)

**Setup**: Monochromatic light passes through two narrow slits, creates interference pattern.

**Condition for bright fringes**:
```
d sin θ = mλ (m = 0, ±1, ±2, ...)
```
- d = slit separation
- θ = angle from center
- m = order number

**Condition for dark fringes**:
```
d sin θ = (m + ½)λ
```

**Fringe spacing** (small angles): Δy = λL/d
- L = distance to screen

**Significance**: Demonstrates wave nature of light; disproved particle-only theories.

### Thin Film Interference

**Examples**: Soap bubbles, oil slicks, anti-reflective coatings

**Constructive interference**:
```
2nt = mλ (reflected light)
```
- n = film refractive index
- t = film thickness
- Includes phase shifts at boundaries

**Applications**:
- Anti-reflective lens coatings
- Optical filters
- Quality control (measuring thickness)

### Diffraction

**Definition**: Bending of waves around obstacles or through openings.

**Single-slit diffraction**:

**First minimum** (dark fringe):
```
a sin θ = λ
```
- a = slit width

**Central maximum width**: θ ≈ λ/a (for small angles)

**Key insight**: Narrower slit → wider diffraction pattern

**Diffraction grating**:
- Many equally spaced slits
- **Condition for maxima**: d sin θ = mλ
- Very sharp, bright lines
- Used in spectroscopy

**Resolution limits**:
- **Rayleigh criterion**: θmin ≈ 1.22λ/D
- D = aperture diameter
- Sets limit on telescope/microscope resolution

### Polarization

**Definition**: Restriction of transverse wave oscillations to specific plane.

**Natural light**: Unpolarized (oscillates in all perpendicular directions)

**Polarization methods**:
1. **Selective absorption**: Polaroid filters
2. **Reflection**: Brewster's angle (tan θB = n₂/n₁)
3. **Scattering**: Blue sky is partially polarized
4. **Birefringence**: Double refraction in crystals

**Malus's Law**: I = I₀ cos² θ
- θ = angle between polarizer axes
- Crossed polarizers (90°) block all light

**Applications**:
- Sunglasses (reduce glare)
- LCD displays
- 3D movies
- Stress analysis
- Optical microscopy

## Geometric Optics

### Ray Model

**Approximation**: When wavelength << object size, treat light as rays traveling in straight lines.

**Valid for**: Lenses, mirrors, many everyday optical phenomena

### Mirrors

**Plane mirror**:
- Virtual image (behind mirror)
- Same size as object
- Upright
- Image distance = object distance

**Spherical mirrors**:

**Concave (converging)**:
- Can form real or virtual images
- Used in telescopes, headlights, makeup mirrors

**Convex (diverging)**:
- Forms virtual, upright, reduced images
- Used in security mirrors, vehicle side mirrors

**Mirror equation**:
```
1/f = 1/do + 1/di
```
- f = focal length = R/2 (R = radius of curvature)
- do = object distance
- di = image distance (positive = real, negative = virtual)

**Magnification**:
```
m = -di/do = hi/ho
```
- Negative m = inverted image
- |m| > 1 = enlarged; |m| < 1 = reduced

### Lenses

**Converging (convex)**:
- Thicker in center
- Focuses parallel rays to focal point
- Can form real or virtual images

**Diverging (concave)**:
- Thinner in center
- Spreads parallel rays from focal point
- Forms virtual, upright, reduced images

**Thin lens equation** (same as mirror equation):
```
1/f = 1/do + 1/di
```

**Lensmaker's equation**:
```
1/f = (n - 1)(1/R₁ - 1/R₂)
```
- n = lens refractive index
- R₁, R₂ = radii of curvature

**Sign conventions**:
- Focal length: positive (converging), negative (diverging)
- Image distance: positive (real, same side as light exits), negative (virtual, opposite side)

**Applications**:
- Cameras (form real image on sensor)
- Projectors (magnified real image)
- Magnifying glass (virtual, enlarged image)
- Eyeglasses (correct vision)

### Optical Instruments

**Human eye**:
- Cornea and lens focus light on retina
- Lens changes shape (accommodation)
- **Near point**: ~25 cm (closest clear focus)
- **Far point**: Infinity (for normal vision)
- Defects: Myopia (nearsighted), hyperopia (farsighted), astigmatism

**Corrective lenses**:
- Myopia: Diverging lens
- Hyperopia: Converging lens

**Magnifying glass**:
- Angular magnification: M = 25 cm/f (when image at near point)

**Compound microscope**:
- Objective lens forms real, enlarged image
- Eyepiece acts as magnifying glass
- Total magnification: M = mobjective × meyepiece

**Telescope**:
- **Refracting**: Uses lenses
- **Reflecting**: Uses mirrors (larger apertures possible)
- Angular magnification: M = fobjective/feyepiece

**Camera**:
- Lens focuses real image on sensor/film
- f-number: f/# = f/D (focal length / aperture diameter)
- Lower f/# = more light, shallower depth of field

## Light as Electromagnetic Wave

### Nature of Light

**Dual nature**:
- **Wave**: Interference, diffraction, polarization
- **Particle** (photon): Photoelectric effect, Compton scattering

**Electromagnetic wave**:
- Oscillating electric and magnetic fields
- Perpendicular to each other and to propagation direction
- Travels at c = 3 × 10⁸ m/s in vacuum

### Speed of Light

**In vacuum**: c = 299,792,458 m/s (exact by definition)

**In medium**: v = c/n
- n = refractive index (≥ 1)

**Refractive indices**:
| Material | n |
|----------|---|
| Vacuum | 1 (exactly) |
| Air | 1.0003 |
| Water | 1.33 |
| Glass | 1.5 - 1.9 |
| Diamond | 2.42 |

### Dispersion

**Definition**: Different wavelengths travel at different speeds in medium (n depends on λ).

**Result**: White light separates into colors (spectrum)

**Examples**:
- Prism spreading white light into rainbow
- Rainbows (dispersion + internal reflection in water droplets)
- Chromatic aberration in lenses

**Wavelength dependence**: Generally n increases as λ decreases (blue light slower than red in glass)

### Color and Spectrum

**Visible spectrum**: ~400 nm (violet) to ~700 nm (red)

| Color | Wavelength Range (nm) | Frequency Range (THz) |
|-------|----------------------|----------------------|
| Violet | 380-450 | 670-790 |
| Blue | 450-495 | 610-670 |
| Green | 495-570 | 530-610 |
| Yellow | 570-590 | 510-530 |
| Orange | 590-620 | 480-510 |
| Red | 620-750 | 400-480 |

**Color perception**:
- Mixing colors: RGB (red, green, blue) primaries for light
- Complementary colors: Pairs that combine to white
- Human vision: Three types of cone cells (sensitive to different wavelengths)

## Real-World Applications

### Fiber Optics

**Principle**: Total internal reflection guides light through thin glass/plastic fiber

**Advantages**:
- High bandwidth (can carry multiple signals)
- Low loss over long distances
- Immune to electromagnetic interference
- Secure (difficult to tap)

**Applications**:
- Internet backbone
- Telecommunications
- Medical endoscopy
- Sensors

### Holography

**Definition**: Recording and reconstructing complete 3D light field (amplitude and phase)

**Process**:
1. Reference beam and object beam interfere
2. Interference pattern recorded
3. Illuminating hologram reconstructs 3D image

**Applications**:
- 3D imaging
- Data storage
- Art
- Security (credit cards, currency)

### Lasers

**LASER**: Light Amplification by Stimulated Emission of Radiation

**Properties**:
- **Monochromatic**: Single wavelength
- **Coherent**: All photons in phase
- **Collimated**: Narrow, parallel beam
- **Intense**: High power density

**Types**:
- Gas lasers (HeNe, CO₂)
- Solid-state lasers (ruby, Nd:YAG)
- Semiconductor lasers (diodes)
- Dye lasers

**Applications**:
- Surgery and medicine
- Cutting and welding
- Optical storage (CD, DVD, Blu-ray)
- Communication (fiber optics)
- Measurement (LIDAR, interferometry)
- Research and spectroscopy

### Medical Imaging

**Ultrasound**:
- Sound waves (1-20 MHz)
- Reflection from tissue boundaries
- Safe, real-time imaging (pregnancy, organs)

**Optical Coherence Tomography (OCT)**:
- Uses near-infrared light
- Interference-based imaging
- High-resolution cross-sections (especially eye)

**Endoscopy**:
- Fiber optic cables carry light into body
- Visual inspection of internal organs

### Telescopes and Astronomy

**Functions**:
1. Gather light (larger aperture = fainter objects visible)
2. Resolve detail (larger aperture = better resolution)
3. Magnify

**Types**:
- Optical (visible light)
- Radio (long wavelengths)
- Infrared (heat signatures)
- X-ray, gamma-ray (space-based, absorbed by atmosphere)

**Adaptive optics**: Correct atmospheric distortion in real-time

### Spectroscopy

**Principle**: Analyze light spectrum to determine composition, temperature, velocity

**Types**:
- **Emission**: Hot gas emits characteristic wavelengths
- **Absorption**: Cool gas absorbs specific wavelengths from continuous spectrum
- **Line spectra**: Each element has unique "fingerprint"

**Applications**:
- Chemical analysis
- Astronomy (star composition, redshift)
- Medical diagnostics
- Environmental monitoring

---

**Key Terms:**
- **Wave**: Disturbance propagating through space and time
- **Wavelength (λ)**: Distance between consecutive wave peaks
- **Frequency (f)**: Oscillations per second
- **Amplitude (A)**: Maximum displacement from equilibrium
- **Interference**: Superposition of waves (constructive or destructive)
- **Diffraction**: Wave bending around obstacles
- **Polarization**: Restriction of wave oscillations to specific direction
- **Reflection**: Wave bouncing off surface
- **Refraction**: Wave bending at boundary due to speed change
- **Doppler effect**: Frequency shift due to relative motion
- **Standing wave**: Interference pattern of opposing waves
- **Total internal reflection**: Complete reflection at boundary (critical angle)
- **Coherence**: Constant phase relationship between waves

---

## Summary

Waves transfer energy through oscillations, characterized by wavelength, frequency, amplitude, and speed (v = λf). Mechanical waves like sound require a medium, while electromagnetic waves like light can travel through vacuum. Waves exhibit superposition, interference (constructive and destructive), diffraction (bending around obstacles), and for transverse waves, polarization. The Doppler effect shifts frequency due to relative motion between source and observer. Standing waves form when oppositely traveling waves interfere, producing nodes and antinodes critical to musical instruments. Light behaves as both wave (interference patterns, diffraction) and particle (photons). Geometric optics uses rays to analyze mirrors and lenses through equations relating object distance, image distance, and focal length. Light refracts when entering different media (Snell's law), can undergo total internal reflection (fiber optics), and disperses into colors due to wavelength-dependent refractive index. Optical instruments—from eyeglasses to telescopes to microscopes—manipulate light to extend human vision. Applications span fiber-optic communication, laser technology, holography, medical imaging, spectroscopy, and astronomical observation, all built on understanding wave phenomena and light's electromagnetic nature.
