# Discrete Mathematics and Logic

## Overview

Discrete mathematics studies structures that are fundamentally countable and distinct, as opposed to continuous. It includes logic, set theory, combinatorics, graph theory, and algorithms—the mathematical foundations of computer science. Logic provides the framework for rigorous reasoning and proof. Together, these subjects underpin programming, cryptography, algorithm design, artificial intelligence, and the foundations of mathematics itself.

## Mathematical Logic: The Language of Reasoning

### Propositional Logic

**Proposition**: Statement that is either true or false (not both)

**Examples**:
- "2 + 2 = 4" (true)
- "5 is prime" (true)
- "This sentence is false" (not a proposition—paradox!)

**Logical operators**:

| Symbol | Name | Meaning | Example | Truth |
|--------|------|---------|---------|-------|
| ¬ | NOT | Negation | ¬(2 > 3) | True |
| ∧ | AND | Conjunction | (2 > 1) ∧ (3 > 1) | True |
| ∨ | OR | Disjunction | (2 > 3) ∨ (3 > 1) | True |
| ⇒ | IMPLIES | Conditional | (x > 0) ⇒ (x² > 0) | True (for x ≠ 0) |
| ⇔ | IFF | Biconditional | (x = 0) ⇔ (x² = 0) | True |

**Truth tables**: Define operator behavior

**Example - Implication (P ⇒ Q)**:

| P | Q | P ⇒ Q |
|---|---|-------|
| T | T | T |
| T | F | F |
| F | T | T |
| F | F | T |

**Key insight**: "If P then Q" is only false when P is true but Q is false. Vacuously true when P is false.

**Tautology**: Always true (e.g., P ∨ ¬P)

**Contradiction**: Always false (e.g., P ∧ ¬P)

**Logical equivalence**: P ≡ Q if same truth table

**Important equivalences**:
- De Morgan's Laws: ¬(P ∧ Q) ≡ (¬P) ∨ (¬Q), ¬(P ∨ Q) ≡ (¬P) ∧ (¬Q)
- Contrapositive: (P ⇒ Q) ≡ (¬Q ⇒ ¬P)
- Material implication: (P ⇒ Q) ≡ (¬P ∨ Q)

### Predicate Logic (First-Order Logic)

**Extends propositional logic** with quantifiers and predicates

**Predicate**: Statement depending on variables (e.g., P(x): "x is prime")

**Quantifiers**:
- **Universal (∀)**: "For all"
  - ∀x P(x): "For all x, P(x) is true"
  - Example: ∀x (x² ≥ 0) — "All numbers squared are non-negative"

- **Existential (∃)**: "There exists"
  - ∃x P(x): "There exists x such that P(x) is true"
  - Example: ∃x (x² = 2) — "There exists x whose square is 2"

**Negation of quantifiers**:
- ¬(∀x P(x)) ≡ ∃x ¬P(x) — "Not all satisfy P" means "Some doesn't satisfy P"
- ¬(∃x P(x)) ≡ ∀x ¬P(x) — "None exists satisfying P" means "All fail to satisfy P"

**Example**: "Every positive number has a square root"
- Formal: ∀x (x > 0 ⇒ ∃y (y² = x))

### Rules of Inference

**Modus Ponens**:
```
P ⇒ Q
P
-------
∴ Q
```

**Modus Tollens**:
```
P ⇒ Q
¬Q
-------
∴ ¬P
```

**Hypothetical Syllogism**:
```
P ⇒ Q
Q ⇒ R
-------
∴ P ⇒ R
```

**Applications**:
- Computer science: Prolog, automated theorem proving
- Artificial intelligence: Expert systems, knowledge representation
- Formal verification: Prove software correctness

## Set Theory: The Foundation

### Basic Concepts

**Set**: Collection of distinct objects

**Notation**:
- Roster: A = {1, 2, 3, 4, 5}
- Set-builder: B = {x | x is prime and x < 20}

**Membership**: 3 ∈ A (3 is element of A)

**Subset**: A ⊆ B if every element of A is in B

**Power set**: 𝒫(A) = set of all subsets of A
- If |A| = n, then |𝒫(A)| = 2ⁿ

### Set Operations

| Operation | Notation | Definition |
|-----------|----------|------------|
| **Union** | A ∪ B | Elements in A or B (or both) |
| **Intersection** | A ∩ B | Elements in both A and B |
| **Difference** | A - B | Elements in A but not B |
| **Complement** | Aᶜ | Elements not in A (relative to universal set) |
| **Cartesian product** | A × B | All ordered pairs (a, b) where a ∈ A, b ∈ B |

**Example**: A = {1, 2, 3}, B = {3, 4, 5}
- A ∪ B = {1, 2, 3, 4, 5}
- A ∩ B = {3}
- A - B = {1, 2}
- A × B = {(1,3), (1,4), (1,5), (2,3), (2,4), (2,5), (3,3), (3,4), (3,5)}

### Laws of Set Theory

**Commutative**: A ∪ B = B ∪ A, A ∩ B = B ∩ A

**Associative**: (A ∪ B) ∪ C = A ∪ (B ∪ C)

**Distributive**: A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C)

**De Morgan's Laws**: (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ, (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ

### Cardinality and Infinity

**Finite set**: |A| = n for some natural number n

**Cantor's discoveries** (1870s-1890s):

**Countably infinite**: Same size as natural numbers ℕ
- Integers ℤ: countable (surprising!)
- Rationals ℚ: countable (very surprising!)
- Algebraic numbers: countable

**Uncountably infinite**: Strictly larger than ℕ
- Real numbers ℝ: uncountable (Cantor's diagonal argument)
- Power set of ℕ: uncountable
- Complex numbers ℂ: uncountable

**Continuum hypothesis**: No set has cardinality strictly between ℕ and ℝ
- Proved independent of ZFC axioms (Gödel 1940, Cohen 1963)
- Cannot be proved or disproved from standard axioms!

## Combinatorics: Counting

### Basic Principles

**Addition Principle**: If choosing from n₁ options OR n₂ options (disjoint):
Total = n₁ + n₂

**Multiplication Principle**: If choosing n₁ options AND THEN n₂ options:
Total = n₁ × n₂

**Example**: License plates with 3 letters then 4 digits
- Letters: 26³ = 17,576 choices
- Digits: 10⁴ = 10,000 choices
- Total: 26³ × 10⁴ = 175,760,000

### Permutations

**Permutation**: Ordered arrangement

**Formula**: n! = n × (n-1) × (n-2) × ... × 2 × 1

**Example**: Arrange 5 books on shelf: 5! = 120 ways

**k-permutations of n**: P(n,k) = n!/(n-k)!
- Choose and arrange k objects from n

**Example**: Top 3 finishers from 10 runners: P(10,3) = 10!/7! = 720

### Combinations

**Combination**: Unordered selection

**Formula**: C(n,k) = n!/(k!(n-k)!) (also written as (ⁿₖ) or "n choose k")

**Example**: Choose 3 pizza toppings from 10: C(10,3) = 120

**Pascal's Triangle**:
```
       1
      1 1
     1 2 1
    1 3 3 1
   1 4 6 4 1
```

Each entry: C(n,k) = C(n-1,k-1) + C(n-1,k)

**Binomial Theorem**:
**(x + y)ⁿ = Σₖ₌₀ⁿ C(n,k) xⁿ⁻ᵏyᵏ**

**Example**: (x + y)³ = x³ + 3x²y + 3xy² + y³

### Pigeonhole Principle

**Statement**: If n+1 pigeons occupy n holes, at least one hole contains ≥2 pigeons

**Generalized**: If kn+1 pigeons occupy n holes, at least one hole contains ≥k+1 pigeons

**Example**: In any group of 13 people, at least 2 have birthdays in the same month

**Applications**:
- Computer science: Hash collisions inevitable
- Number theory: Many results about divisibility
- Ramsey theory: Guarantees structure in large systems

### Inclusion-Exclusion Principle

**Two sets**: |A ∪ B| = |A| + |B| - |A ∩ B|

**Three sets**: |A ∪ B ∪ C| = |A| + |B| + |C| - |A ∩ B| - |A ∩ C| - |B ∩ C| + |A ∩ B ∩ C|

**Example**: Students taking math (50), physics (40), both (20)
- Total: 50 + 40 - 20 = 70

**Application**: Counting problems, probability calculations

## Graph Theory

### Basic Definitions

**Graph**: G = (V, E) where V is set of vertices, E is set of edges

**Edge**: Connection between two vertices

**Types**:
- **Undirected**: Edges have no direction
- **Directed (digraph)**: Edges have direction (arrows)
- **Weighted**: Edges have numerical values
- **Simple**: No loops (edge from vertex to itself) or multiple edges

**Degree**: Number of edges incident to vertex
- In directed graph: in-degree (incoming) and out-degree (outgoing)

**Path**: Sequence of vertices connected by edges

**Cycle**: Path starting and ending at same vertex

**Connected**: Path exists between any two vertices

### Special Graphs

**Complete graph Kₙ**: Every pair of vertices connected
- K₅ has 5 vertices, 10 edges

**Bipartite graph**: Vertices divided into two sets; edges only between sets
- Example: Employees and projects (edges show assignments)

**Tree**: Connected graph with no cycles
- n vertices ⇒ n-1 edges
- Unique path between any two vertices

**Planar graph**: Can be drawn on plane without edge crossings
- Example: K₄ is planar, K₅ is not

### Euler Paths and Circuits

**Euler path**: Path using each edge exactly once

**Euler circuit**: Euler path starting and ending at same vertex

**Theorem**:
- Euler circuit exists ⟺ every vertex has even degree
- Euler path exists ⟺ exactly 0 or 2 vertices have odd degree

**Application**: Route planning (snow plowing, mail delivery)

**Seven Bridges of Königsberg** (Euler, 1736):
- Historical problem: Can you cross all 7 bridges exactly once?
- Answer: No (all 4 landmasses have odd degree)
- Birth of graph theory

### Hamilton Paths and Circuits

**Hamilton path**: Path visiting each vertex exactly once

**Hamilton circuit**: Hamilton path returning to start

**No simple characterization** (unlike Euler paths)—determining existence is NP-complete

**Traveling Salesman Problem (TSP)**:
- Find shortest Hamilton circuit in weighted graph
- NP-hard (no known efficient algorithm)
- Applications: Logistics, manufacturing (circuit board drilling), DNA sequencing

### Graph Coloring

**Vertex coloring**: Assign colors so adjacent vertices have different colors

**Chromatic number χ(G)**: Minimum colors needed

**Examples**:
- Tree: χ = 2 (bipartite)
- Odd cycle: χ = 3
- Complete graph Kₙ: χ = n

**Four-Color Theorem**: Any planar graph has χ ≤ 4

**Applications**:
- Scheduling (vertices = tasks, edges = conflicts)
- Register allocation in compilers
- Sudoku (graph coloring problem)

### Graph Algorithms

**Dijkstra's Algorithm**: Shortest path in weighted graph (no negative weights)
- Used in GPS navigation, routing protocols

**Breadth-First Search (BFS)**: Explore graph level by level
- Shortest path in unweighted graph
- Used in social networks (degrees of separation)

**Depth-First Search (DFS)**: Explore as far as possible before backtracking
- Detect cycles, topological sorting
- Used in maze solving, puzzle solving

**Kruskal's/Prim's Algorithm**: Minimum spanning tree
- Connect all vertices with minimum total edge weight
- Applications: Network design (roads, cables, pipelines)

## Boolean Algebra and Circuits

### Boolean Algebra

**Boolean values**: 0 (false), 1 (true)

**Operations**:
- AND (∧ or ·): 1 · 1 = 1, all else 0
- OR (∨ or +): 0 + 0 = 0, all else 1
- NOT (¬ or '): 0' = 1, 1' = 0

**Laws** (same as set theory, replacing ∪→+, ∩→·, ᶜ→'):
- Commutative, associative, distributive
- De Morgan's: (x + y)' = x' · y', (x · y)' = x' + y'
- Identity: x + 0 = x, x · 1 = x
- Complement: x + x' = 1, x · x' = 0

### Logic Gates

| Gate | Symbol | Boolean | Truth |
|------|--------|---------|-------|
| **AND** | · | x · y | Only 1 if both 1 |
| **OR** | + | x + y | 1 if any 1 |
| **NOT** | ' | x' | Inverts |
| **NAND** | ↑ | (x · y)' | Universal gate |
| **NOR** | ↓ | (x + y)' | Universal gate |
| **XOR** | ⊕ | x ⊕ y | 1 if different |

**Universal gates**: NAND and NOR can implement any Boolean function

### Digital Circuits

**Example - Half Adder** (adds two bits):
- Inputs: A, B
- Outputs: Sum = A ⊕ B, Carry = A · B

**Full Adder** (adds three bits including carry-in):
- Enables multi-bit addition in computers

**Multiplexer**: Selects one of multiple inputs based on control signals

**Applications**: All digital electronics (CPUs, memory, communication)

## Algorithms and Complexity

### Recursion

**Recursive function**: Calls itself with simpler input

**Example - Factorial**:
```
factorial(n):
    if n = 0: return 1
    else: return n × factorial(n-1)
```

**Example - Fibonacci**:
```
fib(n):
    if n ≤ 1: return n
    else: return fib(n-1) + fib(n-2)
```

**Applications**: Tree traversal, divide-and-conquer algorithms, fractals

### Computational Complexity

**Big O Notation**: Describes algorithm efficiency as input size grows

**Common complexities**:

| Class | Name | Example |
|-------|------|---------|
| **O(1)** | Constant | Array access |
| **O(log n)** | Logarithmic | Binary search |
| **O(n)** | Linear | Linear search |
| **O(n log n)** | Linearithmic | Merge sort |
| **O(n²)** | Quadratic | Bubble sort |
| **O(2ⁿ)** | Exponential | Brute force TSP |
| **O(n!)** | Factorial | Generate all permutations |

**P vs NP Problem**:
- **P**: Problems solvable in polynomial time
- **NP**: Problems verifiable in polynomial time
- **Question**: Does P = NP? (Million-dollar Millennium Prize Problem)
- **Significance**: If yes, many "hard" problems become easy (cryptography breaks, optimization becomes tractable)

**NP-complete**: Hardest problems in NP (TSP, graph coloring, SAT)
- If any NP-complete problem has polynomial solution, then P = NP

## Real-World Applications

### Computer Science

**Data structures**: Trees, graphs, hash tables
**Algorithms**: Sorting, searching, graph algorithms
**Databases**: Relational algebra (set theory)
**Cryptography**: Number theory, Boolean functions
**Artificial intelligence**: Logic, graph search, constraint satisfaction

### Network Analysis

**Social networks**: Graph theory
- Vertices = people, edges = friendships
- Centrality measures, community detection

**Internet routing**: Shortest path algorithms
**Epidemic modeling**: Graph structure determines spread

### Optimization

**Scheduling**: Graph coloring, constraint satisfaction
**Logistics**: TSP, vehicle routing
**Resource allocation**: Matching problems in bipartite graphs

### Cryptography

**Public-key cryptography**: Number theory (RSA)
**Hash functions**: Boolean functions
**Zero-knowledge proofs**: Logic and complexity theory

## Key Terms

| Term | Definition |
|------|------------|
| **Proposition** | Statement that is true or false |
| **Tautology** | Proposition always true |
| **Predicate** | Statement depending on variables |
| **Quantifier** | ∀ (for all) or ∃ (there exists) |
| **Set** | Collection of distinct objects |
| **Cardinality** | Size of set (number of elements) |
| **Permutation** | Ordered arrangement |
| **Combination** | Unordered selection |
| **Graph** | Set of vertices connected by edges |
| **Tree** | Connected graph with no cycles |
| **NP-complete** | Hardest problems verifiable in polynomial time |

## Summary

Discrete mathematics studies countable structures—the mathematics of the distinct rather than continuous. Mathematical logic provides the foundation for rigorous reasoning, with propositional and predicate logic enabling formal proof and automated reasoning. Set theory, developed by Cantor, revealed surprising results about infinity and became the foundation for modern mathematics.

Combinatorics addresses counting problems using permutations, combinations, pigeonhole principle, and inclusion-exclusion. Graph theory, born from Euler's analysis of the Königsberg bridges, models networks and relationships, enabling algorithms for routing, scheduling, and optimization. Boolean algebra and logic gates form the mathematical basis for all digital circuits and computer hardware.

These subjects are foundational for computer science—data structures, algorithms, complexity theory, cryptography, and artificial intelligence all depend on discrete mathematics. From the P vs NP problem to internet routing, from DNA sequencing to social network analysis, discrete mathematics provides the tools to reason about finite, countable structures in our increasingly digital world.
