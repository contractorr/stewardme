# Computational Complexity

## Overview

Computational complexity theory classifies problems by how resource requirements scale with input size. Some problems can be solved efficiently (polynomial time). Others appear to require exponential time but no proof exists. Still others are provably intractable or undecidable. Understanding complexity separates tractable problems from intractable ones, guides algorithm design, and reveals fundamental limits of computation.

The P vs NP problem—whether every problem whose solution can be quickly verified can also be quickly solved—is the most important open question in computer science, with a $1 million Clay Mathematics Institute prize. Understanding complexity classes, reductions, and NP-completeness enables recognizing intractable problems and choosing appropriate approaches: exact algorithms for tractable problems, approximation algorithms for intractable ones, or heuristics when nothing better exists.

## Asymptotic Notation

Describes how runtime grows with input size n.

### Big O (Upper Bound)

**Definition:** f(n) = O(g(n)) if ∃ constants c, n₀ such that f(n) ≤ c·g(n) for all n ≥ n₀

**Intuition:** f grows no faster than g (up to constant factor)

**Example:** 3n² + 5n + 2 = O(n²)
- Choose c = 4, n₀ = 10
- For n ≥ 10: 3n² + 5n + 2 ≤ 4n²

**Common classes (ordered by growth):**
```
O(1)         Constant      Hash table lookup
O(log n)     Logarithmic   Binary search
O(n)         Linear        Linear search
O(n log n)   Linearithmic  Merge sort, heap sort
O(n²)        Quadratic     Bubble sort, nested loops
O(n³)        Cubic         Matrix multiplication (naive)
O(2ⁿ)        Exponential   Subset enumeration
O(n!)        Factorial     Permutation enumeration
```

**Common mistakes:**
- O(n) ≠ exactly n operations (ignores constants)
- O(n²) doesn't mean quadratic is bad (depends on n)
- Big O is upper bound, not tight bound

### Big Ω (Lower Bound)

**Definition:** f(n) = Ω(g(n)) if ∃ constants c, n₀ such that f(n) ≥ c·g(n) for all n ≥ n₀

**Intuition:** f grows at least as fast as g

**Example:** 3n² + 5n + 2 = Ω(n²)

### Big Θ (Tight Bound)

**Definition:** f(n) = Θ(g(n)) if f(n) = O(g(n)) and f(n) = Ω(g(n))

**Intuition:** f and g grow at same rate

**Example:** 3n² + 5n + 2 = Θ(n²)

**Usage:**
- O: Algorithm upper bound (worst case)
- Ω: Algorithm lower bound (best case)
- Θ: Tight bound (exact growth rate)

### Little o and ω

**Little o:** f(n) = o(g(n)) if lim[n→∞] f(n)/g(n) = 0
- f grows strictly slower than g
- Example: n = o(n²)

**Little ω:** f(n) = ω(g(n)) if lim[n→∞] f(n)/g(n) = ∞
- f grows strictly faster than g
- Example: n² = ω(n)

## Complexity Classes

### Class P (Polynomial Time)

**Definition:** Problems solvable by deterministic Turing machine in polynomial time.

**Formal:** L ∈ P if ∃ algorithm deciding L in O(n^k) for some constant k

**Examples:**
- Sorting: O(n log n)
- Shortest path: O(V² + E)
- Greatest common divisor: O(log n)
- Linear programming: O(n³)
- Primality testing: O(log⁶ n) [AKS algorithm]

**Why polynomial?**
- Practical: n³ is tractable for reasonable n
- Robust: Polynomial across computational models
- Closed under composition: Polynomial × polynomial = polynomial

**Not all polynomial algorithms are practical:**
- O(n^100) is polynomial but useless
- O(2^(log n)) = O(n) but suspicious
- Constants matter in practice

### Class NP (Non-deterministic Polynomial)

**Definition:** Problems where solution can be verified in polynomial time.

**Formal:** L ∈ NP if ∃ polynomial-time algorithm V such that:
- x ∈ L ⇔ ∃ certificate c where V(x, c) = YES
- Certificate length polynomial in |x|

**Examples:**
- **Subset Sum:** Given numbers, does subset sum to target?
  - Certificate: The subset
  - Verification: Add numbers, check sum (polynomial)

- **Hamiltonian Cycle:** Does graph have cycle visiting each vertex once?
  - Certificate: The cycle
  - Verification: Check cycle visits each vertex once (polynomial)

- **SAT (Boolean Satisfiability):** Is boolean formula satisfiable?
  - Certificate: Variable assignment
  - Verification: Evaluate formula (polynomial)

**NP does not mean "not polynomial":**
- Common misconception
- NP = Non-deterministic Polynomial
- P ⊆ NP (can verify solutions we can solve)

### The P vs NP Question

**Question:** Does P = NP?

**Implications if P = NP:**
- Every efficiently verifiable problem is efficiently solvable
- Dramatic impact on cryptography (most encryption broken)
- NP-complete problems solved efficiently
- Drug design, logistics, scheduling become tractable

**Implications if P ≠ NP:**
- Fundamental limits to computation
- Some problems inherently intractable
- Current cryptography remains secure
- Need approximation algorithms for hard problems

**Current consensus:**
- Most computer scientists believe P ≠ NP
- No proof exists (open for 50+ years)
- $1 million prize for solution

**Why hard to prove:**
- Must show no polynomial algorithm exists (not just that we haven't found one)
- Requires reasoning about all possible algorithms
- Similar to Gödel's incompleteness theorems

### NP-Complete Problems

**Definition:** A problem is NP-complete if:
1. It's in NP (solutions verifiable in polynomial time)
2. Every problem in NP reduces to it in polynomial time

**Intuition:** Hardest problems in NP—if any NP-complete problem is in P, then P = NP.

**Cook-Levin Theorem (1971):** SAT is NP-complete.

**Karp's 21 NP-complete problems (1972):**
- 3-SAT
- Clique
- Vertex Cover
- Hamiltonian Cycle
- Traveling Salesman
- Graph Coloring
- Subset Sum
- Knapsack
- Partition
- ...and 12 more

**Modern count:** Thousands of NP-complete problems identified

### NP-Hard Problems

**Definition:** At least as hard as NP-complete problems, but may not be in NP.

**Examples:**
- Halting problem: NP-hard but undecidable (not in NP)
- Optimization versions of NP-complete problems
- Games (chess, Go on arbitrary board size)

**Relationship:**
```
         All Problems
              |
         NP-Hard
         /        \
    NP-Complete   Undecidable
         |
        NP
         |
         P
```

### Other Complexity Classes

**Co-NP:**
- Complements of NP problems
- Certificate proves x ∉ L
- Example: Proving formula is unsatisfiable

**PSPACE:**
- Problems solvable with polynomial space
- P ⊆ NP ⊆ PSPACE
- Many game-related problems (chess endgames, generalized Sudoku)

**EXPTIME:**
- Problems requiring exponential time
- Generalized chess, checkers

**BPP (Bounded-error Probabilistic Polynomial):**
- Problems solvable by randomized algorithm in polynomial time with error ≤ 1/3
- Believed P = BPP (derandomization)

## Polynomial-Time Reductions

**Definition:** Problem A reduces to B (A ≤_p B) if:
- ∃ polynomial-time algorithm transforming A-instances to B-instances
- A-instance is YES ⇔ corresponding B-instance is YES

**Intuition:** If we can solve B efficiently, we can solve A efficiently.

**Implications:**
- A ≤_p B and B ∈ P ⇒ A ∈ P
- A ≤_p B and A ∉ P ⇒ B ∉ P (contrapositive)

### Proving NP-Completeness

**Steps to show problem X is NP-complete:**
1. Prove X ∈ NP (give polynomial-time verifier)
2. Choose known NP-complete problem Y
3. Show Y ≤_p X (reduce Y to X in polynomial time)

**Example: 3-SAT ≤_p Clique**

**3-SAT:** Is 3-CNF formula satisfiable?
```
(x₁ ∨ x₂ ∨ x₃) ∧ (¬x₁ ∨ ¬x₂ ∨ x₄) ∧ ...
```

**Clique:** Does graph have clique of size k?

**Reduction:**
1. For each clause (a ∨ b ∨ c), create 3 vertices
2. Connect vertices from different clauses unless they're contradictory literals
3. k = number of clauses
4. 3-SAT instance satisfiable ⇔ graph has k-clique

**Why:** Each vertex in clique corresponds to true literal in satisfying assignment.

### Classic Reductions

**3-SAT → Independent Set:**
- Same construction as clique (complement graph)

**Independent Set → Vertex Cover:**
- S is independent set ⇔ V\S is vertex cover

**3-SAT → Subset Sum:**
- Encode clauses and variables as integers
- Target sum encodes satisfying assignment

**Circuit SAT → SAT:**
- Convert circuit to CNF formula

These reductions form a web—proving one problem NP-complete gives a tool to prove others.

## Dealing with NP-Completeness

### 1. Exact Algorithms for Small Instances

**Backtracking with pruning:**
- Traveling Salesman: Branch and bound
- SAT: DPLL algorithm with conflict-driven learning

**Dynamic programming:**
- TSP: O(n² 2ⁿ) Held-Karp algorithm
- Better than O(n!) brute force

**Practical for n ≤ 20-30** depending on problem and optimizations.

### 2. Approximation Algorithms

**Definition:** Algorithm guaranteeing solution within factor α of optimal.

**Vertex Cover (2-approximation):**
```python
def approx_vertex_cover(graph):
    cover = set()
    edges = list(graph.edges())
    while edges:
        u, v = edges.pop()
        cover.add(u)
        cover.add(v)
        # Remove all edges incident to u or v
        edges = [(a, b) for a, b in edges if a not in {u, v} and b not in {u, v}]
    return cover
```

**Guarantee:** |solution| ≤ 2 × |optimal|

**Proof:** Each iteration covers edge. Optimal must include ≥1 endpoint. We include 2.

**TSP (2-approximation for metric TSP):**
1. Compute minimum spanning tree
2. Double edges to create Eulerian graph
3. Find Eulerian tour
4. Convert to Hamiltonian by skipping repeated vertices

**Guarantee:** Tour length ≤ 2 × optimal (using triangle inequality)

**Knapsack (FPTAS - Fully Polynomial Time Approximation Scheme):**
- For any ε > 0, get (1+ε)-approximation in O(n²/ε) time
- Trade accuracy for speed

**Approximation impossibility:**
- Some problems have no polynomial approximation unless P = NP
- Traveling Salesman (general): No constant approximation
- Clique: No n^(1-ε) approximation for any ε > 0

### 3. Heuristics

**No guarantee but often work well in practice.**

**Greedy heuristics:**
- TSP: Nearest neighbor (can be arbitrarily bad)
- Graph coloring: Color vertices in order

**Local search:**
- Start with random solution
- Iteratively improve by local changes
- Can get stuck in local optima

**Simulated annealing:**
- Local search with probability of accepting worse solutions
- Probability decreases over time ("cooling")

**Genetic algorithms:**
- Population of solutions
- Selection, crossover, mutation
- Evolution toward better solutions

**Tabu search:**
- Local search with memory
- Avoid recently visited solutions

### 4. Special Cases

**Recognize when NP-complete problem has efficient special case:**

**2-SAT:** O(n) (linear time)
- Unlike 3-SAT which is NP-complete
- Solvable via implication graph

**Planar graph 3-coloring:** O(n) (Grötzsch's theorem)
- Unlike general graph 3-coloring (NP-complete)

**Knapsack with small weights:** Pseudo-polynomial
- O(nW) dynamic programming
- Polynomial in W but W could be exponential in input size

**Tree-structured problems:**
- Many NP-complete problems become polynomial on trees
- Independent set, vertex cover, TSP on trees

### 5. Parameterized Complexity

**Fixed-parameter tractable (FPT):** O(f(k) × n^c) where k is parameter

**Example: Vertex Cover parameterized by solution size k**
- O(2^k × n) algorithm
- Efficient for small k even if n is large

**Example: TSP parameterized by treewidth**
- Polynomial for graphs with bounded treewidth

## Practical Complexity Analysis

### Amortized Analysis

**Average cost per operation over sequence.**

**Dynamic array insertion:**
- Single insert: O(n) worst case (resize)
- n inserts: O(n) total
- Amortized: O(1) per insert

**Methods:**
1. **Aggregate analysis:** Total cost / number of operations
2. **Accounting method:** Assign artificial costs, bank surplus
3. **Potential method:** Define potential function, analyze change

### Lower Bounds

**Proving algorithms can't do better.**

**Comparison-based sorting:** Ω(n log n)
**Proof:** Decision tree has n! leaves, height ≥ log(n!) = Ω(n log n)

**Element uniqueness:** Ω(n log n) in comparison model

**Adversarial arguments:**
- Prove any algorithm must take certain time
- Construct worst-case input

## Real-World Impact

### Tractable Problems (P)

**Optimization:**
- Network flow: O(VE²)
- Shortest paths: O(V² + E)
- Minimum spanning tree: O(E log V)

**Impact:** GPS navigation, internet routing, supply chains

### Intractable Problems (NP-Complete)

**When encountered:**
1. Verify it's truly NP-complete
2. Ask: Do I need optimal solution?
3. Consider problem size
4. Explore special cases
5. Use approximation or heuristics

**Examples:**
- **Scheduling:** NP-complete → heuristics widely used
- **Circuit design:** NP-complete → SAT solvers work well in practice
- **Protein folding:** NP-complete → approximations + simulations

### Cryptography Relies on Presumed Hardness

**RSA:** Assumes factoring large integers is hard
- Best known: Sub-exponential (not polynomial, not exponential)
- Broken if P = NP or efficient factoring found

**Discrete log:** Basis for Diffie-Hellman, El Gamal
**Lattice problems:** Post-quantum cryptography candidates

## Summary

Computational complexity theory classifies problems by scalability:

**P:** Efficiently solvable (polynomial time)
**NP:** Efficiently verifiable
**NP-Complete:** Hardest problems in NP
**NP-Hard:** At least as hard as NP-complete

**P vs NP** is central question: Can every efficiently verifiable problem be efficiently solved?

**Reductions** show problem equivalence—thousands of problems known NP-complete, meaning:
- No known polynomial algorithm
- Unlikely to find one (would imply P = NP)
- Need alternative approaches

**Practical approaches for NP-complete problems:**
1. Exact algorithms (small instances)
2. Approximation algorithms (guaranteed quality)
3. Heuristics (good in practice)
4. Special cases (recognize structure)
5. Parameterized algorithms (small parameters)

**Significance:** Understanding complexity prevents futile searches for efficient algorithms where none likely exist and guides appropriate problem-solving strategies. Recognizing NP-completeness is as valuable as finding efficient algorithms—it redirects effort toward productive approaches.
