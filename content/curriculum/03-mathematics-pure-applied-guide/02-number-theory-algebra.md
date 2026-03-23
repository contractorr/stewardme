# Number Theory and Algebra

## Overview

Number theory studies the properties of integers—the whole numbers humans first learned to count with. Algebra generalizes arithmetic by introducing variables, operations, and abstract structures. Together, they form the foundation for cryptography, coding theory, abstract mathematics, and much of modern physics. What begins with simple questions about divisibility and prime numbers evolves into sophisticated theories about symmetry, groups, and fields.

## Number Theory: The Study of Integers

### The Fundamental Theorem of Arithmetic

Every integer greater than 1 can be expressed uniquely as a product of prime numbers (up to order):

**60 = 2² × 3 × 5**

This seemingly simple fact has profound consequences:
- Primes are the "atoms" of numbers
- Unique factorization enables modular arithmetic
- Breaking this in cryptography is computationally hard

### Prime Numbers

**Definition**: An integer p > 1 is prime if its only positive divisors are 1 and p.

**Euclid's Theorem (c. 300 BCE)**: There are infinitely many primes.

**Proof by contradiction**:
1. Assume finitely many primes: p₁, p₂, ..., pₙ
2. Consider N = (p₁ × p₂ × ... × pₙ) + 1
3. N is not divisible by any pᵢ (leaves remainder 1)
4. Either N is prime, or has prime factor not in list
5. Contradiction—there must be infinitely many primes

**Prime Distribution**:
- First few primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37...
- Primes become rarer as numbers grow, but never stop
- **Prime Number Theorem**: π(n) ≈ n/ln(n) (number of primes ≤ n)
- At n = 1,000,000: exactly 78,498 primes (formula gives ~72,382)

**Open Problems**:
- **Goldbach Conjecture** (1742): Every even number > 2 is sum of two primes (verified to 4×10¹⁸, unproven)
- **Twin Prime Conjecture**: Infinitely many pairs (p, p+2) both prime (e.g., 11-13, 17-19)
- **Riemann Hypothesis**: Deepest unsolved problem in mathematics, concerning prime distribution

### Divisibility and GCD

**Divisibility**: a divides b (written a|b) if b = ka for some integer k

**Greatest Common Divisor (GCD)**: Largest integer dividing both a and b

**Euclidean Algorithm** (c. 300 BCE): Most efficient method to compute GCD

```
GCD(48, 18):
48 = 2(18) + 12
18 = 1(12) + 6
12 = 2(6) + 0
→ GCD = 6
```

**Application**: Simplifying fractions, cryptography key generation

### Modular Arithmetic

**Definition**: a ≡ b (mod n) means n divides (a - b)

"a and b have same remainder when divided by n"

**Examples**:
- 17 ≡ 5 (mod 12) because 17 - 5 = 12
- 23 ≡ 3 (mod 10) (clock arithmetic: 23:00 = 11pm)

**Properties** (like regular arithmetic):
- If a ≡ b and c ≡ d (mod n), then:
  - a + c ≡ b + d (mod n)
  - a × c ≡ b × d (mod n)

**Applications**:
- **Check digits**: ISBN, credit cards use mod 10 or mod 11
- **Hash functions**: Map data to fixed-size values
- **Cryptography**: RSA encryption depends on modular exponentiation

### Fermat's Little Theorem

If p is prime and a is not divisible by p:

**aᵖ⁻¹ ≡ 1 (mod p)**

**Example**: 2⁶ = 64 ≡ 1 (mod 7)

**Application**:
- Primality testing (if aᵖ⁻¹ ≢ 1 (mod p), then p is not prime)
- Cryptographic protocols
- Efficient modular exponentiation

### RSA Cryptography (Real-World Application)

**How it works**:
1. Choose two large primes p, q (hundreds of digits)
2. Compute n = p × q
3. Choose public exponent e
4. Compute private exponent d such that ed ≡ 1 (mod φ(n))
5. **Public key**: (n, e); **Private key**: d

**Encryption**: c = mᵉ (mod n)
**Decryption**: m = cᵈ (mod n)

**Security**: Relies on difficulty of factoring large n. Best known algorithms take exponential time. A 2048-bit number (617 digits) is currently secure.

**Why it works**: Based on Fermat's Little Theorem and Euler's generalization

## Algebra: Abstraction and Structure

### Historical Development

- **Al-Khwarizmi (c. 820)**: *Al-Jabr* (the algebra)—solving linear/quadratic equations
- **Renaissance (1500s)**: Solutions to cubic and quartic equations
- **Galois (1832)**: Proved no general formula for quintic (5th degree)—birth of modern algebra
- **19th-20th century**: Shift from "solving equations" to "studying structures"

### Basic Algebra: Solving Equations

**Linear equation**: ax + b = 0 → x = -b/a

**Quadratic equation**: ax² + bx + c = 0

**Quadratic formula**:
**x = (-b ± √(b² - 4ac)) / 2a**

**Discriminant**: Δ = b² - 4ac
- Δ > 0: Two real solutions
- Δ = 0: One repeated solution
- Δ < 0: Two complex solutions

**Example**: x² - 5x + 6 = 0
- a=1, b=-5, c=6
- Δ = 25 - 24 = 1
- x = (5 ± 1)/2 = 3 or 2
- Check: (x-2)(x-3) = 0 ✓

### Polynomial Functions

**General form**: P(x) = aₙxⁿ + aₙ₋₁xⁿ⁻¹ + ... + a₁x + a₀

**Degree**: Highest power of x (n)

**Fundamental Theorem of Algebra**: Every polynomial of degree n has exactly n roots (counting multiplicity) in complex numbers

**Example**: x³ - 6x² + 11x - 6 = (x-1)(x-2)(x-3)
- Roots: 1, 2, 3

**Rational Root Theorem**: If p/q is a rational root of polynomial with integer coefficients, then:
- p divides constant term
- q divides leading coefficient

### Systems of Linear Equations

**Example**:
```
2x + 3y = 7
4x - y = 5
```

**Methods**:
1. **Substitution**: Solve one equation for variable, substitute
2. **Elimination**: Add/subtract equations to eliminate variable
3. **Matrix methods**: (See Linear Algebra chapter)

**Solution**: x = 2, y = 1

**Possibilities**:
- **Unique solution**: Lines intersect at one point
- **No solution**: Parallel lines (inconsistent)
- **Infinite solutions**: Same line (dependent)

### Abstract Algebra: Groups, Rings, Fields

Modern algebra studies **algebraic structures**—sets with operations satisfying specific properties.

#### Groups

**Definition**: A set G with operation • is a group if:
1. **Closure**: a • b ∈ G for all a, b ∈ G
2. **Associativity**: (a • b) • c = a • (b • c)
3. **Identity**: ∃e such that a • e = e • a = a
4. **Inverses**: For each a, ∃a⁻¹ such that a • a⁻¹ = e

**Examples**:
- **Integers under addition**: (ℤ, +)
  - Identity: 0
  - Inverse of n: -n

- **Nonzero reals under multiplication**: (ℝ*, ×)
  - Identity: 1
  - Inverse of x: 1/x

- **Symmetries of square**: Rotations and reflections form group
  - Captures geometric symmetry algebraically

**Why groups matter**:
- Symmetries in physics (Noether's theorem: conservation laws ↔ symmetries)
- Crystallography: classify crystal structures
- Cryptography: elliptic curve groups
- Particle physics: gauge groups (SU(3), SU(2), U(1))

#### Rings

**Definition**: A set R with two operations (+, ×) where:
- (R, +) is an abelian group
- Multiplication is associative
- Distributive law holds: a(b + c) = ab + ac

**Examples**:
- Integers (ℤ)
- Polynomials with real coefficients
- Matrices (with matrix multiplication)

**Not a ring**: Positive integers (no additive inverses)

#### Fields

**Definition**: A ring where every nonzero element has multiplicative inverse

**Examples**:
- Rational numbers (ℚ)
- Real numbers (ℝ)
- Complex numbers (ℂ)
- Finite field: ℤₚ (integers mod p, where p is prime)

**Applications**:
- Error-correcting codes (Reed-Solomon uses finite fields)
- Cryptography (AES operates in finite field GF(2⁸))
- Signal processing

### Complex Numbers

**Definition**: ℂ = {a + bi : a, b ∈ ℝ, i² = -1}

**Operations**:
- Addition: (a + bi) + (c + di) = (a+c) + (b+d)i
- Multiplication: (a + bi)(c + di) = (ac-bd) + (ad+bc)i

**Geometric interpretation**:
- Complex plane: real axis (horizontal), imaginary axis (vertical)
- |z| = √(a² + b²): Distance from origin (modulus)
- arg(z) = arctan(b/a): Angle from positive real axis (argument)

**Euler's Formula**:
**e^(iθ) = cos(θ) + i sin(θ)**

**Most beautiful equation**:
**e^(iπ) + 1 = 0**

Connects five fundamental constants: e, i, π, 1, 0

**Applications**:
- AC circuit analysis
- Quantum mechanics (wave functions are complex-valued)
- Signal processing (Fourier transforms)
- Fluid dynamics

## Real-World Applications

### Cryptography (RSA)

**Problem**: Send secure messages over insecure channels

**Mathematical foundation**:
- Prime factorization difficulty
- Modular exponentiation
- Fermat's Little Theorem

**Impact**: Secures all internet commerce, banking, communication

### Error-Correcting Codes

**Problem**: Transmit data reliably over noisy channels (space probes, CDs, cell phones)

**Mathematical foundation**:
- Finite fields
- Polynomial algebra
- Linear algebra

**Example - Reed-Solomon codes**:
- Add redundancy using polynomial evaluation
- Used in CDs, DVDs, QR codes, deep space communication
- Can recover data even if portion is corrupted

### Diffie-Hellman Key Exchange

**Problem**: Two parties establish shared secret over public channel

**Mathematical foundation**:
- Discrete logarithm problem in modular arithmetic
- Computing g^x mod p is easy
- Finding x given g^x mod p is hard (no efficient algorithm known)

**Impact**: Enables secure communication without pre-shared secrets

### Blockchain and Bitcoin

**Mathematical components**:
- Hash functions (SHA-256)
- Elliptic curve cryptography (ECDSA for signatures)
- Proof-of-work (modular exponentiation)

### Symmetry in Physics

**Noether's Theorem**: Every continuous symmetry corresponds to conservation law

Examples:
- Time translation symmetry → Energy conservation
- Space translation symmetry → Momentum conservation
- Rotation symmetry → Angular momentum conservation

**Gauge theories**: Standard Model of particle physics built on group theory (SU(3) × SU(2) × U(1))

## Problem-Solving Examples

### Example 1: Find GCD(252, 180)

**Euclidean Algorithm**:
```
252 = 1(180) + 72
180 = 2(72) + 36
72 = 2(36) + 0
```
**Answer**: GCD = 36

### Example 2: Solve 3x ≡ 7 (mod 11)

Need multiplicative inverse of 3 mod 11.

Try: 3 × 4 = 12 ≡ 1 (mod 11) ✓

So 3⁻¹ ≡ 4 (mod 11)

Multiply both sides by 4:
x ≡ 4 × 7 ≡ 28 ≡ 6 (mod 11)

**Answer**: x = 6 (plus any multiple of 11)

### Example 3: Factor x³ - 7x + 6

**Rational Root Theorem**: Try factors of 6: ±1, ±2, ±3, ±6

Test x = 1: 1 - 7 + 6 = 0 ✓

So (x - 1) is a factor.

Divide: x³ - 7x + 6 = (x - 1)(x² + x - 6) = (x - 1)(x - 2)(x + 3)

**Answer**: Roots are 1, 2, -3

## Key Terms

| Term | Definition |
|------|------------|
| **Prime number** | Integer > 1 with only divisors 1 and itself |
| **Composite number** | Integer > 1 that is not prime |
| **GCD** | Greatest common divisor of two integers |
| **Modular arithmetic** | Arithmetic with remainders after division |
| **Congruence** | a ≡ b (mod n) means n divides (a-b) |
| **Group** | Set with associative operation, identity, inverses |
| **Ring** | Structure with addition and multiplication |
| **Field** | Ring where all nonzero elements have multiplicative inverses |
| **Complex number** | Number of form a + bi where i² = -1 |
| **Polynomial** | Expression involving powers of variable with coefficients |

## Summary

Number theory investigates properties of integers—divisibility, primes, modular arithmetic—revealing deep patterns in the most fundamental objects in mathematics. These seemingly abstract questions power modern cryptography: RSA encryption, Diffie-Hellman key exchange, and blockchain all depend on computational difficulty of factoring, discrete logarithms, and modular arithmetic.

Algebra evolved from solving equations to studying abstract structures. Groups capture symmetry, enabling classification of crystals, particles, and conservation laws in physics. Rings and fields provide frameworks for error-correcting codes, algebraic geometry, and quantum field theory. Complex numbers, initially dismissed as "imaginary," prove essential for electrical engineering, quantum mechanics, and signal processing.

From ancient Babylonian tablets through Greek geometric algebra, Islamic preservation of classical knowledge, Renaissance equation solving, and modern structural abstraction, number theory and algebra have become the language of pattern, symmetry, and computational security. Mastering these foundations opens doors to cryptography, physics, computer science, and the deeper reaches of pure mathematics.
