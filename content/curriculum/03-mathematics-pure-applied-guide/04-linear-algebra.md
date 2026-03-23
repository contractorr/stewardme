# Linear Algebra

## Overview

Linear algebra is the mathematics of vectors, matrices, and linear transformations. It provides a powerful framework for solving systems of equations, understanding high-dimensional geometry, and performing transformations. Linear algebra is foundational for computer graphics, machine learning, quantum mechanics, optimization, and data analysis. In the age of big data and AI, linear algebra has become perhaps the single most practically important branch of mathematics.

## Vectors: The Building Blocks

### Definition

**Vector**: An ordered list of numbers (can represent points, directions, forces, data)

**Notation**: **v** = ⟨v₁, v₂, ..., vₙ⟩ or column form

**Examples**:
- 2D vector: **v** = ⟨3, 4⟩ (point or displacement in plane)
- 3D vector: **w** = ⟨1, -2, 5⟩ (force, velocity, position)
- High-dimensional: Image as vector (millions of pixel values)

### Geometric Interpretation

**2D/3D**: Arrow from origin to point
- **Magnitude** (length): ||**v**|| = √(v₁² + v₂² + ... + vₙ²)
- **Direction**: Angle or unit vector **v**/||**v**||

**Example**: **v** = ⟨3, 4⟩
- Magnitude: ||**v**|| = √(9 + 16) = 5
- Unit vector: **v̂** = ⟨3/5, 4/5⟩

### Vector Operations

#### Addition
**u** + **v** = ⟨u₁+v₁, u₂+v₂, ...⟩

**Geometric**: Parallelogram rule (tip-to-tail)

**Example**: ⟨2, 1⟩ + ⟨3, 4⟩ = ⟨5, 5⟩

#### Scalar Multiplication
c**v** = ⟨cv₁, cv₂, ...⟩

**Geometric**: Stretches/compresses vector (reverses if c < 0)

**Example**: 3⟨1, 2⟩ = ⟨3, 6⟩

#### Dot Product (Inner Product)
**u** · **v** = u₁v₁ + u₂v₂ + ... + uₙvₙ

**Properties**:
- **u** · **v** = ||**u**|| ||**v**|| cos(θ) where θ is angle between vectors
- **u** · **v** = 0 ⟺ **u** ⊥ **v** (orthogonal/perpendicular)
- **u** · **u** = ||**u**||²

**Example**: ⟨3, 4⟩ · ⟨1, 2⟩ = 3(1) + 4(2) = 11

**Applications**:
- Test perpendicularity
- Projection: proj_**v**(**u**) = (**u**·**v**/||**v**||²)**v**
- Work: W = **F** · **d** (force dot displacement)

#### Cross Product (3D only)
**u** × **v** = vector perpendicular to both **u** and **v**

**Formula**: ⟨u₂v₃-u₃v₂, u₃v₁-u₁v₃, u₁v₂-u₂v₁⟩

**Magnitude**: ||**u** × **v**|| = ||**u**|| ||**v**|| sin(θ)

**Application**: Torque, angular momentum, surface normals (computer graphics)

## Matrices: Linear Transformations

### Definition

**Matrix**: Rectangular array of numbers

**Dimensions**: m × n (m rows, n columns)

**Example**: A = [1  2  3]
              [4  5  6]  (2×3 matrix)

### Matrix as Linear Transformation

Matrix multiplication **performs linear transformation** on vectors.

**A**v** transforms vector **v** according to matrix **A**

**Linear**:
- A(**u** + **v**) = A**u** + A**v**
- A(c**v**) = c(A**v**)

### Matrix Operations

#### Addition (same dimensions)
[a  b] + [e  f] = [a+e  b+f]
[c  d]   [g  h]   [c+g  d+h]

#### Scalar Multiplication
c[a  b] = [ca  cb]
 [c  d]   [cc  cd]

#### Matrix Multiplication

**Dimension requirement**: (m×n) × (n×p) → (m×p)

**Rule**: (AB)ᵢⱼ = Σₖ AᵢₖBₖⱼ (dot product of row i and column j)

**Example**:
[1  2] [5  6]   [1·5+2·7  1·6+2·8]   [19  22]
[3  4] [7  8] = [3·5+4·7  3·6+4·8] = [43  50]

**Properties**:
- **Not commutative**: AB ≠ BA (generally)
- **Associative**: (AB)C = A(BC)
- **Distributive**: A(B + C) = AB + AC

### Special Matrices

| Type | Definition | Properties |
|------|------------|------------|
| **Identity** (I) | Diagonal of 1s, rest 0s | AI = IA = A |
| **Zero** (0) | All entries 0 | 0A = A0 = 0 |
| **Diagonal** | Non-zero only on diagonal | Easy to compute powers |
| **Symmetric** | Aᵀ = A | Real eigenvalues, orthogonal eigenvectors |
| **Orthogonal** | QᵀQ = I | Preserves lengths and angles |

### Transpose

**Aᵀ**: Flip matrix across diagonal (rows ↔ columns)

[1  2  3]ᵀ   [1  4]
[4  5  6]  = [2  5]
             [3  6]

**Properties**:
- (Aᵀ)ᵀ = A
- (AB)ᵀ = BᵀAᵀ (reverse order!)

## Systems of Linear Equations

### Matrix Form

System:
```
2x + 3y = 7
4x - y = 5
```

**Matrix form**: A**x** = **b**

[2   3] [x]   [7]
[4  -1] [y] = [5]

### Solution Methods

#### 1. Gaussian Elimination

Transform augmented matrix [A|**b**] to row echelon form using:
- Swap rows
- Multiply row by nonzero constant
- Add multiple of one row to another

**Example**:
[2   3 | 7]    [1  1.5 | 3.5]    [1  1.5 | 3.5]
[4  -1 | 5] → [4   -1 | 5  ] → [0   -7 | -9 ]

Back substitution: y = 9/7, then x = 2

#### 2. Matrix Inverse (if exists)

A**x** = **b** → **x** = A⁻¹**b**

**Requirement**: A must be square and invertible (det(A) ≠ 0)

### Inverse Matrix

**Definition**: AA⁻¹ = A⁻¹A = I

**2×2 formula**:
[a  b]⁻¹    1    [ d  -b]
[c  d]   = ——— [-c   a]
           ad-bc

**Properties**:
- (AB)⁻¹ = B⁻¹A⁻¹ (reverse order!)
- (Aᵀ)⁻¹ = (A⁻¹)ᵀ
- Not all matrices have inverses (singular matrices)

**Example**:
[2   3]⁻¹    1   [-1  -3]   [-0.1  -0.3]
[4  -1]   = —— [ 4   2] = [ 0.4   0.2]
            -14

### Determinant

**2×2**: det([a b]) = ad - bc
           [c d]

**3×3**: Cofactor expansion or rule of Sarrus

**Properties**:
- det(AB) = det(A)det(B)
- det(Aᵀ) = det(A)
- det(A⁻¹) = 1/det(A)
- det(A) = 0 ⟺ A is not invertible

**Geometric interpretation**: Scaling factor for volume under transformation

## Vector Spaces

### Definition

**Vector space**: Set V with vector addition and scalar multiplication satisfying:
1. Closure under addition and scalar multiplication
2. Commutativity and associativity of addition
3. Identity element (zero vector)
4. Additive inverses
5. Distributive laws

**Examples**:
- ℝⁿ (n-dimensional Euclidean space)
- Polynomials of degree ≤ n
- Continuous functions on [a,b]
- Matrices of fixed size

### Subspace

**Subspace** of V: Subset that is itself a vector space

**Test**:
1. Contains zero vector
2. Closed under addition
3. Closed under scalar multiplication

**Examples in ℝ³**:
- Any plane through origin
- Any line through origin
- {**0**} and ℝ³ itself

### Linear Independence

Vectors **v₁**, ..., **vₖ** are **linearly independent** if:

c₁**v₁** + ... + cₖ**vₖ** = **0** only when all cᵢ = 0

**Interpretation**: None can be written as combination of others

**Example**: In ℝ²:
- ⟨1,0⟩, ⟨0,1⟩ are independent
- ⟨1,2⟩, ⟨2,4⟩ are dependent (second is 2× first)

### Span

**span{**v₁**, ..., **vₖ**}**: All linear combinations c₁**v₁** + ... + cₖ**vₖ**

**Example**:
- span{⟨1,0⟩, ⟨0,1⟩} = ℝ² (all of 2D plane)
- span{⟨1,2,3⟩} = line through origin in that direction

### Basis

**Basis**: Linearly independent set that spans the space

**Properties**:
- Every vector has **unique** representation as linear combination of basis vectors
- All bases for space V have same number of vectors

**Standard basis for ℝⁿ**:
**e₁** = ⟨1,0,...,0⟩, **e₂** = ⟨0,1,...,0⟩, etc.

### Dimension

**Dimension**: Number of vectors in basis

**Examples**:
- dim(ℝⁿ) = n
- dim(polynomials degree ≤ n) = n+1
- dim({**0**}) = 0

## Eigenvalues and Eigenvectors

### Definition

For matrix A, **v** is **eigenvector** with **eigenvalue** λ if:

**A**v** = λ**v****

**Interpretation**: Transformation A stretches **v** by factor λ (doesn't rotate)

### Finding Eigenvalues

Solve **characteristic equation**: det(A - λI) = 0

**Example**: A = [4  1]
              [2  3]

det([4-λ   1 ]) = (4-λ)(3-λ) - 2 = λ² - 7λ + 10 = (λ-5)(λ-2)
   [2   3-λ]

**Eigenvalues**: λ₁ = 5, λ₂ = 2

### Finding Eigenvectors

For each λ, solve (A - λI)**v** = **0**

**λ = 5**:
[-1  1] [v₁]   [0]
[ 2 -2] [v₂] = [0]

**Eigenvector**: **v₁** = ⟨1, 1⟩ (or any multiple)

**λ = 2**:
[2  1] [v₁]   [0]
[2  1] [v₂] = [0]

**Eigenvector**: **v₂** = ⟨1, -2⟩

### Applications

#### 1. Principal Component Analysis (PCA)

**Problem**: Reduce high-dimensional data to lower dimensions while preserving variance

**Solution**:
1. Compute covariance matrix of data
2. Find eigenvectors (principal components)
3. Project data onto top k eigenvectors

**Application**: Face recognition, dimensionality reduction, data visualization

#### 2. Google PageRank

**Problem**: Rank web pages by importance

**Solution**: Model web as graph, compute dominant eigenvector of adjacency matrix

**Interpretation**: Steady-state probability distribution of random surfer

#### 3. Differential Equations

System **x**' = A**x** has solutions involving eᵏᵗ**v** where λ, **v** are eigenvalue/eigenvector

**Application**: Coupled oscillators, population models, electrical circuits

#### 4. Quantum Mechanics

**Observable** = Hermitian matrix
**Measurement outcomes** = eigenvalues
**States** = eigenvectors

**Example**: Energy levels of atom are eigenvalues of Hamiltonian operator

### Diagonalization

If A has n independent eigenvectors **v₁**, ..., **vₙ** with eigenvalues λ₁, ..., λₙ:

**A = PDP⁻¹**

where P = [**v₁** ... **vₙ**], D = diagonal matrix of λᵢ

**Benefit**: Easy to compute powers:
**Aᵏ = PDᵏP⁻¹** (and Dᵏ is trivial—just raise diagonal entries to k)

## Orthogonality

### Orthogonal Vectors

**u** ⊥ **v** if **u** · **v** = 0

**Orthonormal**: Orthogonal unit vectors (||**v**|| = 1)

### Orthogonal Matrix

**Q** is orthogonal if **QᵀQ = I**

**Properties**:
- Columns are orthonormal vectors
- Preserves lengths: ||Q**x**|| = ||**x**||
- Preserves angles: (Q**u**) · (Q**v**) = **u** · **v**
- det(Q) = ±1

**Examples**: Rotations, reflections

### Gram-Schmidt Process

**Problem**: Convert basis to orthonormal basis

**Algorithm**:
1. **u₁** = **v₁**/||**v₁**||
2. **u₂** = (**v₂** - proj_**u₁**(**v₂**))/||...||
3. Continue for remaining vectors

**Application**: QR factorization, solving least squares problems

### Spectral Theorem

**For symmetric matrix A**: Can be diagonalized by orthogonal matrix

**A = QΛQᵀ** where Q orthogonal, Λ diagonal

**Significance**: Eigenvalues are real, eigenvectors are orthogonal

**Application**: Principal component analysis, quadratic forms

## Applications

### Computer Graphics

**Transformations**:
- **Translation**: Add vector
- **Rotation**: Multiply by orthogonal matrix
- **Scaling**: Multiply by diagonal matrix
- **Projection**: Linear transformation reducing dimension

**3D rotation around z-axis by angle θ**:
[cos θ  -sin θ  0]
[sin θ   cos θ  0]
[  0       0    1]

### Machine Learning

**Linear Regression**: Solve **Xw = y** for weights **w**
- Solution: **w** = (XᵀX)⁻¹Xᵀ**y** (normal equation)
- Or: gradient descent on ||**Xw** - **y**||²

**Neural Networks**:
- Each layer: linear transformation A**x** + **b** followed by nonlinearity
- Backpropagation: matrix calculus with chain rule

**Dimensionality Reduction**:
- PCA: Project onto top eigenvectors of covariance matrix
- SVD: Factor data matrix A = UΣVᵀ

### Image Compression (SVD)

**Singular Value Decomposition**: A = UΣVᵀ

**Image compression**:
1. Treat image as matrix
2. Compute SVD
3. Keep only largest k singular values
4. Reconstruct approximate image

**JPEG uses similar ideas with discrete cosine transform**

### Differential Equations

**System**: **x**' = A**x**

**Solution**: **x**(t) = c₁eᵏ¹ᵗ**v₁** + ... + cₙeᵏⁿᵗ**vₙ**

where λᵢ, **vᵢ** are eigenvalues/eigenvectors

**Stability**: System stable if all eigenvalues have negative real part

**Applications**: Population dynamics, chemical reactions, control theory

### Optimization

**Quadratic form**: f(**x**) = **x**ᵀA**x**

**Critical point**: ∇f = 0

**Second derivative test**:
- Positive definite (all eigenvalues > 0): Local minimum
- Negative definite (all eigenvalues < 0): Local maximum
- Indefinite (mixed signs): Saddle point

### Cryptography

**Hill cipher**: Encrypt message as matrix multiplication mod 26

**Lattice-based cryptography**: Security based on hard problems in high-dimensional lattices

## Key Terms

| Term | Definition |
|------|------------|
| **Vector** | Ordered list of numbers; represents point, direction, or data |
| **Matrix** | Rectangular array of numbers; represents linear transformation |
| **Linear transformation** | Function preserving vector addition and scalar multiplication |
| **Determinant** | Scalar value encoding volume scaling and invertibility |
| **Inverse matrix** | Matrix A⁻¹ such that AA⁻¹ = I |
| **Vector space** | Set with vector addition and scalar multiplication |
| **Basis** | Linearly independent set spanning space |
| **Dimension** | Number of vectors in basis |
| **Eigenvalue** | Scalar λ such that A**v** = λ**v** for some **v** |
| **Eigenvector** | Vector **v** scaled (not rotated) by transformation A |
| **Orthogonal** | Perpendicular (dot product zero) |

## Summary

Linear algebra studies vectors, matrices, and linear transformations—the mathematics of linearity and high-dimensional geometry. Vectors represent points, directions, and data. Matrices encode linear transformations and systems of equations. The dot product measures similarity and enables projections.

Eigenvalues and eigenvectors reveal the fundamental modes of linear transformations, powering Google's PageRank, principal component analysis, quantum mechanics, and stability analysis of differential equations. Orthogonality enables efficient computation and least-squares solutions. The spectral theorem guarantees symmetric matrices have real eigenvalues and orthogonal eigenvectors.

Linear algebra is foundational for computer graphics (transformations, projections), machine learning (regression, neural networks, PCA), quantum mechanics (operators, measurements), optimization (quadratic forms, convexity), and data science (SVD, dimensionality reduction). In the age of big data and artificial intelligence, linear algebra has become the essential mathematical language for working with high-dimensional data and computation at scale.
