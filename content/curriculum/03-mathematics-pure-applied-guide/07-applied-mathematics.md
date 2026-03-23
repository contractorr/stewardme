# Applied Mathematics

## Overview

Applied mathematics uses mathematical methods to solve real-world problems in science, engineering, business, and industry. It bridges pure mathematics and practical applications through mathematical modeling, differential equations, optimization, numerical methods, and computational mathematics. Applied mathematicians translate problems into mathematical language, solve them using appropriate techniques, and interpret results back in the original context.

## Mathematical Modeling

### The Modeling Process

**Steps**:
1. **Identify problem**: What question needs answering?
2. **Make assumptions**: Simplify reality to tractable problem
3. **Formulate model**: Translate into mathematical equations
4. **Solve**: Apply mathematical techniques
5. **Interpret**: Translate results back to real-world context
6. **Validate**: Compare predictions with data
7. **Refine**: Iterate if necessary

**Key principle**: "All models are wrong, but some are useful" (George Box)

### Example: Cooling Coffee

**Problem**: How long until coffee reaches drinkable temperature?

**Assumptions**:
- Room temperature constant
- Coffee loses heat proportional to temperature difference (Newton's Law of Cooling)

**Model**: dT/dt = -k(T - Tᵣₒₒₘ)

**Solution**: T(t) = Tᵣₒₒₘ + (T₀ - Tᵣₒₒₘ)e⁻ᵏᵗ

**Interpretation**: Temperature decays exponentially to room temperature

**Validation**: Measure actual coffee temperature over time, fit k

### Types of Models

| Type | Characteristics | Example |
|------|-----------------|---------|
| **Deterministic** | No randomness; same input → same output | Planetary motion |
| **Stochastic** | Includes randomness/probability | Stock prices |
| **Discrete** | Integer time steps | Population year-by-year |
| **Continuous** | Continuous time | Chemical reactions |
| **Static** | Single snapshot | Force balance |
| **Dynamic** | Evolution over time | Epidemic spread |

## Differential Equations

### Ordinary Differential Equations (ODEs)

**Definition**: Equations involving function and its derivatives

**Example**: dy/dx = 2x

**Solution**: y = x² + C (family of parabolas)

### First-Order ODEs

**Separable**: dy/dx = f(x)g(y)

**Solution method**: Separate variables, integrate both sides

**Example**: dy/dx = y
- dy/y = dx
- ln|y| = x + C
- y = Aeˣ (exponential growth/decay)

**Linear**: dy/dx + P(x)y = Q(x)

**Solution**: Use integrating factor μ(x) = e^(∫P(x)dx)

### Second-Order ODEs

**General form**: a(d²y/dx²) + b(dy/dx) + cy = f(x)

**Homogeneous** (f(x) = 0): Solve characteristic equation ar² + br + c = 0

**Cases**:
- **Distinct real roots** r₁, r₂: y = c₁e^(r₁x) + c₂e^(r₂x)
- **Repeated root** r: y = (c₁ + c₂x)e^(rx)
- **Complex roots** α ± βi: y = e^(αx)(c₁cos(βx) + c₂sin(βx))

**Non-homogeneous**: Find particular solution + homogeneous solution

### Applications

**Mechanics** - Spring-mass system:
m(d²x/dt²) + c(dx/dt) + kx = F(t)
- m: mass, c: damping, k: spring constant, F: external force

**Electrical circuits** - RLC circuit:
L(d²q/dt²) + R(dq/dt) + q/C = V(t)
- L: inductance, R: resistance, C: capacitance, V: voltage

**Population dynamics** - Logistic growth:
dP/dt = rP(1 - P/K)
- r: growth rate, K: carrying capacity
- Solution: S-shaped curve (exponential then saturates)

**Chemical kinetics** - Reaction rates:
d[A]/dt = -k[A]ⁿ
- n = 1: First-order (exponential decay)
- n = 2: Second-order (inverse relationship)

### Partial Differential Equations (PDEs)

**Definition**: Equations with partial derivatives (multiple independent variables)

**Heat equation**: ∂u/∂t = α(∂²u/∂x²)
- Models temperature diffusion
- α: thermal diffusivity

**Wave equation**: ∂²u/∂t² = c²(∂²u/∂x²)
- Models vibrating strings, sound waves, light
- c: wave speed

**Laplace's equation**: ∂²u/∂x² + ∂²u/∂y² = 0
- Models steady-state temperature, electrostatics, fluid flow
- Solutions are harmonic functions

**Applications**:
- Heat conduction in materials
- Electromagnetic waves (Maxwell's equations)
- Fluid dynamics (Navier-Stokes equations)
- Quantum mechanics (Schrödinger equation)
- Finance (Black-Scholes equation)

## Optimization

### Unconstrained Optimization

**Problem**: Minimize (or maximize) f(x)

**One variable**:
- Find critical points: f'(x) = 0
- Test: f''(x) > 0 → minimum, f''(x) < 0 → maximum

**Multiple variables**:
- Gradient: ∇f = 0
- Hessian matrix H: Check eigenvalues for type of critical point

**Example - Minimize** f(x,y) = x² + y² - 4x - 6y + 13:
- ∇f = ⟨2x - 4, 2y - 6⟩ = ⟨0, 0⟩
- Solution: x = 2, y = 3
- f(2,3) = 0 (minimum)

### Constrained Optimization

**Lagrange Multipliers**: Optimize f(x,y) subject to g(x,y) = c

**Method**: Solve ∇f = λ∇g (gradient of f parallel to gradient of constraint)

**Example**: Maximize f(x,y) = xy subject to x + y = 10
- ∇f = ⟨y, x⟩
- ∇g = ⟨1, 1⟩
- y = λ, x = λ, so x = y
- From constraint: x = y = 5
- Maximum: f(5,5) = 25

### Linear Programming

**Standard form**:
Maximize: c₁x₁ + c₂x₂ + ... + cₙxₙ
Subject to: Aₓ ≤ b, x ≥ 0

**Geometric interpretation**: Feasible region is polyhedron; optimal solution at vertex

**Simplex algorithm** (Dantzig, 1947): Move along edges to better vertices

**Example - Production planning**:
- Make products A (profit $30) and B (profit $40)
- Constraints: Labor hours, materials, demand
- Find production mix maximizing profit

**Applications**:
- Resource allocation
- Supply chain optimization
- Portfolio optimization (Markowitz model)
- Diet problem (minimize cost meeting nutritional requirements)

### Nonlinear Optimization

**Gradient Descent**: Iteratively move in direction of steepest descent
- xₖ₊₁ = xₖ - α∇f(xₖ)
- α: step size (learning rate)

**Newton's Method**: Uses second-order information (Hessian)
- Faster convergence but more expensive per iteration

**Applications**:
- Machine learning (training neural networks)
- Engineering design (structural optimization)
- Operations research (facility location)

## Numerical Methods

### Motivation

Many problems lack closed-form solutions:
- Most differential equations
- Complicated integrals
- Nonlinear systems

**Numerical methods**: Approximate solutions using algorithms

### Root Finding

**Problem**: Solve f(x) = 0

**Bisection method**:
- Start with interval [a,b] where f(a)f(b) < 0
- Repeatedly halve interval
- Slow but guaranteed convergence

**Newton's method**:
- xₙ₊₁ = xₙ - f(xₙ)/f'(xₙ)
- Fast convergence (quadratic) near root
- Requires derivative; may not converge if bad starting point

**Example**: Find √2 (solve x² - 2 = 0)
- Newton: xₙ₊₁ = xₙ - (xₙ² - 2)/(2xₙ) = (xₙ + 2/xₙ)/2
- Start x₀ = 1: x₁ = 1.5, x₂ = 1.4167, x₃ = 1.4142 (accurate to 4 places!)

### Numerical Integration

**Problem**: Approximate ∫ₐᵇ f(x)dx

**Trapezoidal rule**: Approximate curve with trapezoids
- ∫ₐᵇ f(x)dx ≈ (b-a)[f(a) + f(b)]/2

**Simpson's rule**: Use parabolas (quadratic approximations)
- More accurate than trapezoid rule
- Error O(h⁵) vs O(h³)

**Monte Carlo integration**: Random sampling (useful in high dimensions)

**Applications**:
- Physics simulations
- Probability (expected values)
- Computer graphics (rendering equations)

### Numerical Differential Equations

**Euler's method** (simplest):
- yₙ₊₁ = yₙ + hf(xₙ, yₙ)
- h: step size

**Runge-Kutta methods**: More accurate
- RK4 (4th order): Industry standard
- Balance accuracy and computational cost

**Example**: Solve dy/dx = y, y(0) = 1 numerically
- Exact: y = eˣ
- Euler with h = 0.1: Approximates exponential

**Applications**:
- Weather forecasting (atmosphere dynamics)
- Spacecraft trajectory
- Chemical reaction simulation
- Epidemiological models (COVID-19 spread)

### Numerical Linear Algebra

**Solving Ax = b**:
- Direct: Gaussian elimination, LU decomposition
- Iterative: Jacobi, Gauss-Seidel, conjugate gradient (for large sparse systems)

**Eigenvalue algorithms**:
- Power iteration: Finds dominant eigenvalue
- QR algorithm: Finds all eigenvalues

**Applications**:
- Finite element analysis (structural engineering)
- Google PageRank (sparse matrix, billions of dimensions)
- Quantum chemistry (molecular orbitals)

## Dynamical Systems

### Definition

**Dynamical system**: Mathematical model of time-dependent process

**State space**: Set of all possible states
**Phase portrait**: Visualization of trajectories in state space

### Equilibria and Stability

**Equilibrium**: State where system doesn't change (dx/dt = 0)

**Stability**:
- **Stable**: Small perturbations decay back to equilibrium
- **Unstable**: Small perturbations grow
- **Asymptotically stable**: Perturbations decay to equilibrium

**Linearization**: Approximate nonlinear system near equilibrium using Jacobian matrix
- Eigenvalues determine stability

**Example - Pendulum**:
- Equilibria: Hanging down (stable), pointing up (unstable)
- Phase portrait shows oscillations around stable equilibrium

### Chaos Theory

**Sensitive dependence on initial conditions**: Tiny differences lead to vastly different outcomes

**Lorenz system** (1963): Weather model
- dx/dt = σ(y - x)
- dy/dt = x(ρ - z) - y
- dz/dt = xy - βz

**Strange attractor**: Butterfly-shaped fractal structure

**Implications**: Long-term weather forecasting fundamentally limited

**Applications**:
- Climate modeling
- Population dynamics
- Economics (market crashes)
- Cryptography (pseudo-random number generation)

### Bifurcations

**Bifurcation**: Qualitative change in dynamics as parameter varies

**Example - Logistic map**: xₙ₊₁ = rxₙ(1 - xₙ)
- r < 1: Population dies out
- 1 < r < 3: Stable fixed point
- 3 < r < ~3.57: Periodic oscillations (period doubling)
- r > ~3.57: Chaos

**Feigenbaum constant** (δ ≈ 4.669): Universal ratio in period-doubling route to chaos

## Fourier Analysis

### Fourier Series

**Idea**: Decompose periodic function into sum of sines and cosines

**Formula**:
f(x) = a₀/2 + Σₙ₌₁^∞ [aₙcos(nx) + bₙsin(nx)]

**Coefficients**:
- aₙ = (1/π)∫₋π^π f(x)cos(nx)dx
- bₙ = (1/π)∫₋π^π f(x)sin(nx)dx

**Example - Square wave**: Can be represented as infinite sum of odd harmonics

**Applications**:
- Signal processing (decompose signal into frequencies)
- Heat equation (separation of variables)
- Music (overtones and timbre)

### Fourier Transform

**Extension to non-periodic functions**:
F(ω) = ∫₋∞^∞ f(t)e^(-iωt)dt

**Inverse transform**:
f(t) = (1/2π)∫₋∞^∞ F(ω)e^(iωt)dω

**Properties**:
- Linearity
- Convolution theorem: Convolution in time ↔ Multiplication in frequency
- Parseval's theorem: Energy conservation

**Applications**:
- **Image processing**: JPEG compression (discrete cosine transform)
- **Audio**: MP3 compression, equalizers
- **Solving PDEs**: Transform differential equation to algebraic equation
- **Quantum mechanics**: Position ↔ Momentum representations
- **MRI**: Reconstructing images from frequency data

### Fast Fourier Transform (FFT)

**Algorithm** (Cooley-Tukey, 1965): Compute discrete Fourier transform efficiently
- Naive: O(n²) operations
- FFT: O(n log n) operations

**Impact**: Revolutionary for signal processing, enabled real-time applications

## Probability and Stochastic Processes

### Random Walk

**1D random walk**: Start at 0, each step ±1 with equal probability

**Properties**:
- Expected position after n steps: 0
- Expected distance from origin: √n (grows as square root of time)

**Gambler's ruin**: Eventually reach boundary (win or lose all money)

**Applications**:
- Stock prices (with drift and volatility)
- Diffusion of particles
- Polymer physics

### Markov Chains

**Definition**: Sequence where future depends only on present, not past

**Transition matrix** P: Pᵢⱼ = probability of moving from state i to state j

**Stationary distribution** π: Long-run probabilities
- Satisfies πP = π

**Example - Weather model**:
- States: {Sunny, Rainy}
- If sunny today, 70% chance sunny tomorrow
- If rainy today, 60% chance rainy tomorrow

**Applications**:
- Google PageRank (random surfer model)
- Speech recognition (Hidden Markov Models)
- Genetics (evolution models)
- Queuing theory

### Brownian Motion

**Continuous random walk**: Limiting case as time steps → 0

**Properties**:
- Nowhere differentiable (infinitely jagged)
- Self-similar (fractal-like)
- Quadratic variation = t

**Stochastic differential equation** (SDE):
dX = μdt + σdW
- μ: drift, σ: diffusion, W: Wiener process

**Itô calculus**: Calculus for stochastic processes

**Applications**:
- **Finance**: Black-Scholes model (stock prices as geometric Brownian motion)
- **Physics**: Particle diffusion
- **Biology**: Molecular motion

### Black-Scholes Equation

**Option pricing** (Nobel Prize 1997):

∂V/∂t + (1/2)σ²S²(∂²V/∂S²) + rS(∂V/∂S) - rV = 0

- V: option value
- S: stock price
- σ: volatility
- r: risk-free rate

**Solution**: Closed-form formula for European call/put options

**Impact**: Created modern quantitative finance industry

## Control Theory

### Concept

**Goal**: Design inputs to make system behave as desired

**Feedback control**: Adjust input based on output measurements

**Example - Cruise control**:
- Measure speed
- Compare to desired speed
- Adjust throttle accordingly

### PID Controller

**Proportional-Integral-Derivative control**:

u(t) = Kₚe(t) + Kᵢ∫e(τ)dτ + Kₐ(de/dt)

- e(t): error (difference from target)
- Kₚ, Kᵢ, Kₐ: tuning parameters

**Components**:
- **P**: Proportional to current error
- **I**: Accounts for accumulated past error
- **D**: Anticipates future error based on rate of change

**Applications**:
- Industrial process control
- Robotics
- Autopilot systems
- Temperature regulation

### Optimal Control

**Problem**: Choose control to minimize cost functional

**Linear Quadratic Regulator (LQR)**: Minimize quadratic cost subject to linear dynamics

**Pontryagin's Maximum Principle**: Necessary conditions for optimal control

**Applications**:
- Spacecraft trajectory optimization
- Economic planning
- Drug dosing schedules

## Real-World Case Studies

### COVID-19 Modeling

**SIR Model**:
- S: Susceptible
- I: Infected
- R: Recovered

**Equations**:
- dS/dt = -βSI/N
- dI/dt = βSI/N - γI
- dR/dt = γI

**Basic reproduction number** R₀ = β/γ:
- R₀ > 1: Epidemic grows
- R₀ < 1: Epidemic dies out

**Extensions**: SEIR (add Exposed), age structure, spatial models, vaccination

**Applications**: Policy decisions (lockdowns, social distancing, vaccine allocation)

### Weather Forecasting

**Numerical weather prediction**:
1. Discretize atmosphere into grid
2. Encode physics (Navier-Stokes, thermodynamics) as PDEs
3. Solve numerically with supercomputers
4. Ensemble forecasts (multiple initial conditions)

**Challenges**:
- Chaotic dynamics (error growth)
- Resolution vs computation tradeoff
- Parameterization of small-scale processes

**Success**: 5-day forecasts now as accurate as 2-day forecasts 30 years ago

### Structural Engineering

**Finite Element Method (FEM)**:
1. Divide structure into small elements
2. For each element, write equations (equilibrium, material properties)
3. Assemble into large system: Ku = f
4. Solve for displacements u
5. Compute stresses, check safety

**Applications**:
- Bridge design
- Airplane wings
- Earthquake-resistant buildings

### Machine Learning

**Mathematical foundations**:
- Linear algebra (matrix operations)
- Calculus (gradient descent, backpropagation)
- Probability (Bayesian inference, probabilistic models)
- Optimization (training algorithms)

**Neural network training**: Minimize loss function
- Forward pass: Compute predictions
- Backward pass: Gradient via chain rule (automatic differentiation)
- Update: Gradient descent or variants (Adam, RMSprop)

## Key Terms

| Term | Definition |
|------|------------|
| **Mathematical model** | Mathematical representation of real-world system |
| **ODE** | Ordinary differential equation (one independent variable) |
| **PDE** | Partial differential equation (multiple independent variables) |
| **Optimization** | Finding best solution from set of alternatives |
| **Lagrange multiplier** | Method for constrained optimization |
| **Numerical method** | Algorithm for approximating mathematical solutions |
| **Dynamical system** | System evolving in time according to fixed rule |
| **Chaos** | Sensitive dependence on initial conditions |
| **Fourier transform** | Decomposition of function into frequencies |
| **Stochastic process** | Random process evolving in time |

## Summary

Applied mathematics translates real-world problems into mathematical language, solves them with rigorous techniques, and interprets results back in practical context. Mathematical modeling requires balancing realism with tractability, capturing essential features while remaining solvable. Validation against data ensures models are useful approximations of reality.

Differential equations describe how systems change over time—from coffee cooling to epidemic spread to quantum mechanics. Optimization finds best solutions under constraints, powering logistics, engineering design, and machine learning. Numerical methods enable approximate solutions when closed forms don't exist, making weather forecasting and structural analysis possible.

Dynamical systems theory reveals how simple rules generate complex behavior, including chaos where tiny differences cascade into vastly different outcomes. Fourier analysis decomposes signals into frequencies, enabling compression, filtering, and PDE solutions. Stochastic processes model randomness, from molecular diffusion to stock prices, with Brownian motion and Itô calculus providing mathematical framework.

From COVID-19 modeling to weather forecasting, structural engineering to quantitative finance, machine learning to control systems, applied mathematics provides the tools to understand, predict, and optimize complex real-world systems. Every technology, every engineering achievement, every data-driven decision relies on these mathematical foundations.
