# Calculus and Analysis

## Overview

Calculus is the mathematics of change and accumulation. It enables us to reason about instantaneous rates of change (derivatives), areas under curves (integrals), and infinite processes (limits and series). Calculus is the essential tool for physics, engineering, economics, and any field involving dynamic systems. Analysis extends calculus to rigorous foundations, studying continuity, convergence, and the behavior of functions with mathematical precision.

## Historical Context

### The Invention of Calculus

**Independent Discovery** (1660s-1680s):
- **Isaac Newton** (1643-1727): Developed "fluxions" for physics problems (motion, gravity)
- **Gottfried Leibniz** (1646-1716): Developed differential and integral calculus with notation we use today

**Priority dispute**: Bitter controversy, but both deserve credit. Newton discovered first but published later; Leibniz published first with superior notation.

### Precursors

- **Archimedes** (287-212 BCE): Method of exhaustion (proto-integration)
- **Fermat** (1607-1665): Found tangent lines (proto-differentiation)
- **Cavalieri** (1598-1647): Method of indivisibles for areas/volumes

### Rigorization (1800s)

Early calculus relied on intuition about "infinitesimals"—philosophically problematic.

**Cauchy, Weierstrass** (1820s-1870s): Rebuilt calculus on rigorous foundation:
- **Limits**: Formal ε-δ definition
- **Continuity**: Precise characterization
- **Convergence**: Criteria for infinite series

This transformed calculus into **real analysis**—the rigorous theory of real numbers and functions.

## Limits: The Foundation

### Intuitive Definition

**lim[x→a] f(x) = L** means: As x gets arbitrarily close to a, f(x) gets arbitrarily close to L.

### Examples

**Example 1**: lim[x→2] (x² - 4)/(x - 2)

Cannot substitute directly (0/0). Factor:
```
(x² - 4)/(x - 2) = (x + 2)(x - 2)/(x - 2) = x + 2  (for x ≠ 2)
```
**Answer**: lim[x→2] = 2 + 2 = 4

**Example 2**: lim[x→∞] (3x² + 5x)/(2x² - x)

Divide numerator and denominator by x²:
```
(3 + 5/x)/(2 - 1/x)
```
As x → ∞, terms with x in denominator → 0

**Answer**: 3/2

### Important Limit

**lim[h→0] (sin h)/h = 1**

Foundational for derivatives of trigonometric functions.

### Continuity

**Definition**: f is continuous at x = a if:
1. f(a) is defined
2. lim[x→a] f(x) exists
3. lim[x→a] f(x) = f(a)

**Intuition**: Graph has no breaks, jumps, or holes at a

**Examples**:
- Continuous: Polynomials, sin(x), cos(x), eˣ, ln(x) on domain
- Discontinuous: 1/x at x=0, floor function, Heaviside step function

## Derivatives: Instantaneous Rate of Change

### Definition

**f'(x) = lim[h→0] [f(x+h) - f(x)]/h**

Measures instantaneous rate of change at x.

**Notations**: f'(x), df/dx, dy/dx, Df(x)

### Geometric Interpretation

**Derivative = slope of tangent line** at point (x, f(x))

### Computing Derivatives from Definition

**Example**: f(x) = x²

```
f'(x) = lim[h→0] [(x+h)² - x²]/h
      = lim[h→0] [x² + 2xh + h² - x²]/h
      = lim[h→0] [2xh + h²]/h
      = lim[h→0] (2x + h)
      = 2x
```

**Answer**: d/dx(x²) = 2x

### Basic Derivative Rules

| Function | Derivative |
|----------|------------|
| **Power rule**: xⁿ | nxⁿ⁻¹ |
| **Constant**: c | 0 |
| **Sum**: f + g | f' + g' |
| **Product**: fg | f'g + fg' |
| **Quotient**: f/g | (f'g - fg')/g² |
| **Chain rule**: f(g(x)) | f'(g(x)) · g'(x) |

### Common Derivatives

| Function f(x) | Derivative f'(x) |
|---------------|------------------|
| xⁿ | nxⁿ⁻¹ |
| eˣ | eˣ |
| ln(x) | 1/x |
| sin(x) | cos(x) |
| cos(x) | -sin(x) |
| tan(x) | sec²(x) |
| aˣ | aˣ ln(a) |

### Example: Chain Rule

**Find d/dx[sin(x²)]**

Outer function: f(u) = sin(u), f'(u) = cos(u)
Inner function: g(x) = x², g'(x) = 2x

**Chain rule**: d/dx[sin(x²)] = cos(x²) · 2x = 2x cos(x²)

### Applications of Derivatives

#### 1. Velocity and Acceleration

**Position**: s(t)
**Velocity**: v(t) = s'(t) (rate of change of position)
**Acceleration**: a(t) = v'(t) = s''(t) (rate of change of velocity)

**Example**: A ball thrown upward: s(t) = -16t² + 64t + 6 (feet)
- v(t) = -32t + 64
- At t = 0: v(0) = 64 ft/s (initial velocity)
- Max height when v = 0: -32t + 64 = 0 → t = 2 seconds
- s(2) = -64 + 128 + 6 = 70 feet

#### 2. Optimization

Find maximum/minimum values using derivatives.

**Critical points**: Where f'(x) = 0 or f'(x) undefined

**Second derivative test**:
- If f''(x) > 0: Local minimum (concave up)
- If f''(x) < 0: Local maximum (concave down)

**Example**: Maximize area of rectangle with perimeter 100

Let width = x, length = 50 - x
Area: A(x) = x(50 - x) = 50x - x²

A'(x) = 50 - 2x = 0 → x = 25

A''(x) = -2 < 0 (maximum)

**Answer**: Square with side 25 maximizes area (A = 625)

#### 3. Related Rates

Find rate of change of one quantity given rate of change of related quantity.

**Example**: Ladder sliding down wall

Ladder (10 ft) leaning against wall. Bottom slides away at 2 ft/s. How fast is top descending when bottom is 6 ft from wall?

**Setup**: x² + y² = 100 (Pythagorean theorem)

Differentiate with respect to time:
2x(dx/dt) + 2y(dy/dt) = 0

When x = 6: y = √(100-36) = 8

Substitute: 2(6)(2) + 2(8)(dy/dt) = 0
24 + 16(dy/dt) = 0
dy/dt = -1.5 ft/s

**Answer**: Top descending at 1.5 ft/s

#### 4. Linear Approximation

Near x = a: **f(x) ≈ f(a) + f'(a)(x - a)**

**Example**: Approximate √101

Use f(x) = √x near a = 100:
- f(100) = 10
- f'(x) = 1/(2√x), so f'(100) = 1/20

f(101) ≈ 10 + (1/20)(1) = 10.05

**Actual**: √101 = 10.04987... (excellent approximation!)

## Integrals: Accumulation and Area

### Definition (Riemann Integral)

**∫ₐᵇ f(x)dx** = limit of Riemann sums (approximating area with rectangles)

**Interpretation**: Signed area between curve and x-axis from a to b

### Fundamental Theorem of Calculus

**Part 1**: If F'(x) = f(x), then:

**∫ₐᵇ f(x)dx = F(b) - F(a)**

**Part 2**: If g(x) = ∫ₐˣ f(t)dt, then g'(x) = f(x)

**Significance**: Connects differentiation and integration (inverse operations)

### Computing Integrals

**Antiderivatives**: Reverse of differentiation

| Function f(x) | Antiderivative F(x) |
|---------------|---------------------|
| xⁿ (n ≠ -1) | xⁿ⁺¹/(n+1) + C |
| 1/x | ln\|x\| + C |
| eˣ | eˣ + C |
| sin(x) | -cos(x) + C |
| cos(x) | sin(x) + C |
| sec²(x) | tan(x) + C |

**Note**: Always include constant of integration C for indefinite integrals!

### Example: Definite Integral

**Evaluate ∫₀^π sin(x)dx**

Antiderivative: F(x) = -cos(x)

∫₀^π sin(x)dx = F(π) - F(0) = -cos(π) - (-cos(0)) = -(-1) - (-1) = 2

**Interpretation**: Area under one arch of sine curve

### Integration Techniques

#### 1. Substitution (Chain rule in reverse)

**Example**: ∫ 2x cos(x²)dx

Let u = x², then du = 2x dx

∫ cos(u)du = sin(u) + C = sin(x²) + C

#### 2. Integration by Parts (Product rule in reverse)

**Formula**: ∫ u dv = uv - ∫ v du

**Example**: ∫ x eˣ dx

Let u = x, dv = eˣ dx
Then du = dx, v = eˣ

∫ x eˣ dx = x eˣ - ∫ eˣ dx = x eˣ - eˣ + C = eˣ(x - 1) + C

#### 3. Partial Fractions

For rational functions: decompose into simpler fractions

**Example**: ∫ 1/(x² - 1)dx

Factor: x² - 1 = (x-1)(x+1)

Partial fractions: 1/(x² - 1) = A/(x-1) + B/(x+1)

Solve: A = 1/2, B = -1/2

∫ [1/(2(x-1)) - 1/(2(x+1))]dx = (1/2)[ln|x-1| - ln|x+1|] + C

### Applications of Integrals

#### 1. Area Between Curves

**Area** = ∫ₐᵇ [f(x) - g(x)]dx (where f(x) ≥ g(x))

**Example**: Area between y = x² and y = x from x = 0 to x = 1

∫₀¹ [x - x²]dx = [x²/2 - x³/3]₀¹ = 1/2 - 1/3 = 1/6

#### 2. Volume of Revolution

Rotate region around x-axis:

**V** = π ∫ₐᵇ [f(x)]²dx

**Example**: Rotate y = √x from x = 0 to x = 4 around x-axis

V = π ∫₀⁴ x dx = π[x²/2]₀⁴ = 8π cubic units

#### 3. Work

**Work** = ∫ₐᵇ F(x)dx (force times distance)

**Example**: Spring with force F(x) = kx (Hooke's law)

Work to stretch from 0 to d: W = ∫₀ᵈ kx dx = kd²/2

#### 4. Average Value

**Average value of f on [a,b]** = (1/(b-a)) ∫ₐᵇ f(x)dx

**Example**: Average temperature if T(t) = 60 + 10sin(πt/12) over 24 hours

Avg = (1/24)∫₀²⁴ [60 + 10sin(πt/12)]dt = 60°F
(sine oscillations integrate to zero over full period)

## Sequences and Series

### Sequences

**Definition**: Ordered list {aₙ} = a₁, a₂, a₃, ...

**Convergence**: lim[n→∞] aₙ = L if terms approach L

**Examples**:
- {1/n}: 1, 1/2, 1/3, ... → 0
- {(-1)ⁿ}: -1, 1, -1, 1, ... (diverges, oscillates)

### Series

**Definition**: Sum of sequence: Σ(n=1 to ∞) aₙ = a₁ + a₂ + a₃ + ...

**Geometric series**: Σ(n=0 to ∞) arⁿ
- Converges to a/(1-r) if |r| < 1
- Diverges if |r| ≥ 1

**Example**: Σ(n=0 to ∞) (1/2)ⁿ = 1/(1 - 1/2) = 2

**Harmonic series**: Σ(n=1 to ∞) 1/n = 1 + 1/2 + 1/3 + ... = ∞ (diverges!)

### Tests for Convergence

| Test | When to Use | Conclusion |
|------|-------------|------------|
| **Divergence test** | Always try first | If lim aₙ ≠ 0, diverges |
| **Geometric series** | aₙ = arⁿ | Converges if \|r\| < 1 |
| **p-series** | Σ 1/nᵖ | Converges if p > 1 |
| **Ratio test** | Factorials, exponentials | If lim \|aₙ₊₁/aₙ\| < 1, converges |
| **Integral test** | Can integrate | If ∫f(x)dx converges, so does Σf(n) |
| **Comparison test** | Similar to known series | Compare to geometric or p-series |

### Taylor Series

**Idea**: Approximate function as infinite polynomial

**Taylor series centered at a**:

**f(x) = f(a) + f'(a)(x-a) + f''(a)(x-a)²/2! + f'''(a)(x-a)³/3! + ...**

**Maclaurin series** (a = 0):

| Function | Series |
|----------|--------|
| eˣ | 1 + x + x²/2! + x³/3! + ... |
| sin(x) | x - x³/3! + x⁵/5! - ... |
| cos(x) | 1 - x²/2! + x⁴/4! - ... |
| 1/(1-x) | 1 + x + x² + x³ + ... (\|x\| < 1) |
| ln(1+x) | x - x²/2 + x³/3 - ... (\|x\| < 1) |

**Example**: Approximate e

e = e¹ = 1 + 1 + 1/2! + 1/3! + 1/4! + ...
≈ 1 + 1 + 0.5 + 0.167 + 0.042 + ... ≈ 2.718...

## Multivariable Calculus (Brief Introduction)

### Partial Derivatives

For f(x, y): ∂f/∂x means differentiate with respect to x, treating y as constant

**Example**: f(x, y) = x²y + 3xy²
- ∂f/∂x = 2xy + 3y²
- ∂f/∂y = x² + 6xy

**Application**: In economics, partial derivatives represent marginal effects

### Multiple Integrals

**Double integral**: ∫∫ᴿ f(x,y) dA (volume under surface over region R)

**Triple integral**: ∫∫∫ f(x,y,z) dV (integrate over 3D region)

**Applications**: Mass, center of mass, probability (joint distributions)

### Gradient

**Gradient**: ∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z)

- Points in direction of steepest increase
- Perpendicular to level curves/surfaces
- Used in optimization algorithms (gradient descent)

## Real-World Applications

### Physics

**Newton's Second Law**: F = ma = m(dv/dt) = m(d²s/dt²)

Solving differential equations gives motion.

**Maxwell's Equations**: Describe all classical electromagnetism using partial derivatives and integrals

### Economics

**Marginal Cost**: MC = dC/dq (derivative of cost function)

**Consumer Surplus**: ∫[demand above price] (integral of difference)

**Elasticity**: E = (dQ/dP)(P/Q) (derivative measuring responsiveness)

### Machine Learning

**Gradient Descent**: Iteratively minimize loss function:
θ ← θ - α∇L(θ)

Used to train neural networks (backpropagation computes gradients via chain rule)

### Signal Processing

**Fourier Transform**: Decomposes signal into frequencies using integrals of sines/cosines

Applications: MP3 compression, image processing, quantum mechanics

## Key Terms

| Term | Definition |
|------|------------|
| **Limit** | Value function approaches as input approaches point |
| **Continuity** | Function has no breaks or jumps |
| **Derivative** | Instantaneous rate of change; slope of tangent line |
| **Integral** | Accumulation; area under curve |
| **Antiderivative** | Function whose derivative is given function |
| **Critical point** | Where derivative equals zero or undefined |
| **Series** | Sum of infinitely many terms |
| **Convergence** | Series/sequence approaches finite limit |
| **Taylor series** | Function represented as infinite polynomial |
| **Partial derivative** | Derivative with respect to one variable, others fixed |

## Summary

Calculus, independently invented by Newton and Leibniz, provides the mathematical framework for understanding change and accumulation. Limits define instantaneous rates rigorously. Derivatives measure rates of change, enabling optimization, related rates problems, and linear approximation. The Fundamental Theorem of Calculus reveals derivatives and integrals as inverse operations, connecting instantaneous change with total accumulation.

Integration computes areas, volumes, work, and average values. Series extend calculus to infinite sums, with Taylor series approximating functions as polynomials. Multivariable calculus extends these ideas to functions of several variables, using partial derivatives and gradients.

Calculus is indispensable for physics (mechanics, electromagnetism, quantum theory), engineering (optimization, signal processing), economics (marginal analysis, growth models), and machine learning (gradient descent, backpropagation). Real analysis provides the rigorous foundations, transforming intuitive infinitesimals into precise ε-δ arguments. From planetary motion to neural networks, calculus remains the essential language of continuous change.
