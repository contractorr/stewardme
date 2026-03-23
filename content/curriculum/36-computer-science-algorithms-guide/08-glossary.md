# Glossary

## A

**Abstract Syntax Tree (AST):** Tree representation of syntactic structure of source code produced by parser. Used by compilers for semantic analysis and code generation.

**Abstraction:** Hiding implementation details behind clean interface. Fundamental principle in CS enabling modularity and reducing complexity.

**Algorithm:** Step-by-step procedure for solving computational problem. Analyzed by time/space complexity.

**Amortized Analysis:** Technique for analyzing average cost per operation over sequence of operations. Used when occasional expensive operations are amortized across many cheap ones.

**Arithmetic Hierarchy:** Classification of problems by levels of undecidability. Level 0 = decidable, Level 1 = recursively enumerable, etc.

**Array:** Contiguous memory block storing fixed or dynamic number of elements with O(1) random access.

**Asymptotic Notation:** Mathematical notation (Big O, Ω, Θ) describing how function grows as input approaches infinity.

**AVL Tree:** Self-balancing binary search tree where height difference between left and right subtrees is at most 1. Guarantees O(log n) operations.

## B

**Backtracking:** Algorithm design paradigm that incrementally builds solutions and abandons paths violating constraints. Used for constraint satisfaction problems.

**Balanced Tree:** Tree where height is O(log n), ensuring efficient operations. Examples: AVL, Red-Black trees.

**B-Tree:** Self-balancing tree with multiple keys per node, optimized for systems reading/writing large blocks of data. Used in databases and filesystems.

**Big O Notation:** O(f(n)) describes upper bound on function growth. f(n) = O(g(n)) if f grows no faster than g.

**Big Ω Notation:** Ω(f(n)) describes lower bound on function growth. f(n) = Ω(g(n)) if f grows at least as fast as g.

**Big Θ Notation:** Θ(f(n)) describes tight bound—both upper and lower bound. f(n) = Θ(g(n)) if f and g grow at same rate.

**Binary Search:** Divide-and-conquer algorithm finding element in sorted array in O(log n) time by repeatedly halving search space.

**Binary Search Tree (BST):** Binary tree where left subtree values < node < right subtree values. Supports O(h) operations where h = height.

**Bloom Filter:** Space-efficient probabilistic data structure for set membership testing. May have false positives but never false negatives.

**Branch Prediction:** CPU technique predicting which way branch will go to avoid pipeline stalls. Modern CPUs achieve >95% accuracy.

**Breadth-First Search (BFS):** Graph traversal algorithm visiting all nodes at distance k before visiting nodes at distance k+1. Uses queue. Finds shortest path in unweighted graphs.

## C

**Cache:** Small, fast memory storing frequently accessed data. CPU caches (L1, L2, L3) exploit locality to hide memory latency.

**Cache Coherence:** Protocol ensuring multiple CPU caches maintain consistent view of memory in multicore systems.

**CAP Theorem:** In distributed system with network partitions, can achieve at most two of: Consistency, Availability, Partition tolerance.

**Church-Turing Thesis:** Any function computable by effective mechanical procedure can be computed by Turing machine. Establishes well-defined notion of "computable."

**CISC (Complex Instruction Set Computing):** CPU design with many complex, variable-length instructions. Example: x86.

**Clique:** Complete subgraph where every pair of vertices is connected. Finding maximum clique is NP-complete.

**Compiler:** Program translating high-level source code to machine code through lexing, parsing, semantic analysis, optimization, and code generation.

**Complexity Class:** Set of problems with similar resource requirements. Examples: P, NP, NP-complete, PSPACE.

**Computability:** Whether problem can be solved by any algorithm. Halting problem is uncomputable.

**Computational Complexity:** Study of resources (time, space) required to solve problems as input size grows.

**Consensus:** Problem of multiple nodes agreeing on value despite failures. Algorithms: Paxos, Raft, 2PC.

**Context Switch:** Saving state of one process/thread and loading state of another. Expensive operation (1-10 μs).

**Co-NP:** Complexity class of complements of NP problems. Problem is in co-NP if "no" instances have polynomial-time verifiable proofs.

## D

**Data Structure:** Way of organizing data to enable efficient operations. Examples: arrays, trees, graphs, hash tables.

**Deadlock:** Situation where processes wait for each other's resources cyclically, preventing progress.

**Decidable:** Problem is decidable if algorithm exists that always halts and correctly answers yes/no. Opposite: undecidable.

**Depth-First Search (DFS):** Graph traversal algorithm exploring as far as possible along each branch before backtracking. Uses stack (or recursion).

**Dijkstra's Algorithm:** Greedy algorithm for single-source shortest paths in graphs with non-negative edge weights. Time: O((V+E) log V) with heap.

**Distributed System:** Multiple computers coordinating via network to appear as single coherent system. Challenges: partial failure, latency, concurrency.

**Divide and Conquer:** Algorithm design paradigm breaking problem into smaller subproblems, solving recursively, and combining solutions. Examples: merge sort, quicksort.

**Dynamic Array:** Automatically resizing array. When full, allocates larger array (typically 2× size), copies elements, deallocates old. Amortized O(1) insertion.

**Dynamic Programming:** Algorithm design paradigm solving problems with optimal substructure and overlapping subproblems by storing solutions to avoid recomputation.

## E

**Edit Distance:** Minimum number of insertions, deletions, substitutions to transform one string to another. Solved with DP in O(mn) time.

**EXPTIME:** Complexity class of problems solvable in exponential time. Includes generalized chess, checkers.

**Eventual Consistency:** Consistency model where replicas converge to same state eventually, but may be temporarily inconsistent. Enables high availability.

## F

**Finite Automaton:** Simplest computational model with finite states, transitions, and no memory. Recognizes regular languages.

**FPTAS (Fully Polynomial Time Approximation Scheme):** For any ε > 0, produces (1+ε)-approximation in time polynomial in input size and 1/ε.

## G

**Graph:** G = (V, E) where V = vertices, E = edges. Can be directed/undirected, weighted/unweighted. Used to model relationships.

**Greedy Algorithm:** Makes locally optimal choice at each step hoping to find global optimum. Works when problem has greedy choice property and optimal substructure.

## H

**Halting Problem:** Given program P and input I, does P halt on I? Proved undecidable by Turing (1936). Fundamental limit of computation.

**Hash Function:** Maps keys to array indices. Good hash function is deterministic, uniform, and fast.

**Hash Table:** Data structure using hash function to map keys to values. Average O(1) insert/delete/search. Handles collisions via chaining or open addressing.

**Heap:** Complete binary tree satisfying heap property (parent ≥ children for max-heap). Enables O(log n) insert/delete and O(1) find-max.

**Heuristic:** Algorithm without optimality guarantee but often works well in practice. Used when exact solution intractable.

**Huffman Coding:** Greedy algorithm for optimal prefix-free binary encoding based on character frequencies. Used in compression.

## I

**In-place Algorithm:** Algorithm using O(1) extra space beyond input. Example: quicksort.

**Instruction-Level Parallelism (ILP):** Executing multiple instructions simultaneously through pipelining, superscalar execution, out-of-order execution.

**Intermediate Representation (IR):** Compiler's internal representation of program, independent of source/target language. Enables optimization.

**Intractable:** Problem with no known polynomial-time algorithm. Often refers to NP-complete problems.

## J

**JIT (Just-In-Time) Compilation:** Compiling code at runtime rather than ahead of time. Enables profile-guided optimization and specialization.

**Journaling:** File system technique logging changes before applying them. Enables crash recovery by replaying log.

## K

**Knapsack Problem:** Given items with values and weights, maximize value subject to weight constraint. 0/1 knapsack is NP-complete. Pseudo-polynomial DP solution exists.

## L

**Lambda Calculus:** Model of computation based on function abstraction and application. Church-Turing equivalent to Turing machines. Foundation of functional programming.

**Lexical Analysis:** Compiler phase converting source code character stream to token stream. Implemented with finite automata.

**Linked List:** Data structure where elements (nodes) contain data and pointer to next node. Enables O(1) insertion/deletion at known positions but O(n) random access.

**Locality:** Principle that programs access small portion of address space at any time. Temporal: recently accessed data accessed again. Spatial: nearby addresses accessed.

**Longest Common Subsequence (LCS):** Longest sequence appearing in same order in two strings (need not be contiguous). Solved with DP in O(mn) time.

## M

**Master Theorem:** Solves recurrences T(n) = aT(n/b) + f(n) by comparing f(n) with n^(log_b a).

**Memory Hierarchy:** Organization of memory from fast/small (registers) to slow/large (disk). Exploits locality for performance.

**Merge Sort:** Divide-and-conquer sorting algorithm with guaranteed O(n log n) time. Stable but requires O(n) space.

**Memoization:** Top-down dynamic programming approach caching function results to avoid recomputation.

**Multi-level Page Table:** Hierarchical page table structure reducing memory overhead for sparse address spaces.

## N

**NP (Non-deterministic Polynomial):** Complexity class of problems where solution can be verified in polynomial time. P ⊆ NP.

**NP-Complete:** Hardest problems in NP. A problem is NP-complete if: (1) it's in NP, (2) every NP problem reduces to it in polynomial time. If any NP-complete problem is in P, then P = NP.

**NP-Hard:** At least as hard as NP-complete problems but may not be in NP (may not have polynomial-time verifiable solutions).

## O

**Operating System:** Software managing hardware resources and providing abstraction for applications. Handles processes, memory, I/O, file systems.

**Optimal Substructure:** Property where optimal solution contains optimal solutions to subproblems. Required for dynamic programming and greedy algorithms.

**Oracle Machine:** Turing machine with access to oracle (black box instantly solving some problem). Used in computability theory to study relative computational power.

## P

**P (Polynomial Time):** Complexity class of problems solvable by deterministic Turing machine in polynomial time. Considered "efficiently solvable."

**Page Fault:** Exception when program accesses memory page not in physical memory. OS loads page from disk.

**Paging:** Memory management scheme dividing virtual/physical memory into fixed-size pages/frames. Enables non-contiguous memory allocation.

**Parsing:** Compiler phase analyzing token stream according to grammar rules to produce abstract syntax tree.

**Partition (Sharding):** Splitting dataset across multiple machines. Strategies: key-range, hash, consistent hashing.

**Paxos:** Consensus algorithm guaranteeing agreement among distributed nodes despite failures. Provably correct but complex.

**Pipelining:** CPU technique overlapping instruction execution stages. Increases throughput to ~1 instruction per cycle.

**Priority Queue:** Abstract data type where each element has priority. Highest priority element dequeued first. Typically implemented with heap.

**Process:** Instance of running program with own address space and resources. Contains at least one thread.

**PSPACE:** Complexity class of problems solvable with polynomial space. P ⊆ NP ⊆ PSPACE.

**Pushdown Automaton:** Finite automaton with stack. Recognizes context-free languages (can parse programming languages).

## Q

**Queue:** FIFO (First In, First Out) data structure. Operations: enqueue (add to rear), dequeue (remove from front). Used in BFS, scheduling.

**Quicksort:** Divide-and-conquer sorting algorithm with average O(n log n), worst O(n²). In-place and fast in practice due to cache efficiency.

## R

**Raft:** Consensus algorithm designed to be more understandable than Paxos. Leader-based with follower replication.

**Recursion:** Function calling itself. Must have base case to terminate. Natural for problems with recursive structure (trees, divide-and-conquer).

**Recursively Enumerable:** Language L is recursively enumerable if Turing machine exists accepting all strings in L (but may loop on strings not in L).

**Red-Black Tree:** Self-balancing BST with color properties guaranteeing O(log n) operations. Faster insertion/deletion than AVL but slightly slower lookup. Used in most language standard libraries.

**Reduction:** Transforming instances of problem A to instances of problem B. If A reduces to B and B is solvable efficiently, so is A. Used to prove NP-completeness.

**Register:** Small, fast storage location in CPU. Typically 8-64 general-purpose registers holding temporary values.

**Replication:** Maintaining copies of data on multiple nodes. Increases availability and fault tolerance. Types: single-leader, multi-leader, leaderless.

**Rice's Theorem:** Any non-trivial semantic property of programs is undecidable. Fundamental limit on automated program analysis.

**RISC (Reduced Instruction Set Computing):** CPU design with few simple, fixed-length instructions. Examples: ARM, RISC-V. Easier to pipeline than CISC.

**Round Robin:** CPU scheduling algorithm giving each process fixed time quantum in circular order. Fair with good response time.

## S

**Semantic Analysis:** Compiler phase performing type checking, scope resolution, and other semantic verification.

**Skip List:** Probabilistic data structure with multiple levels of linked lists. Expected O(log n) operations. Alternative to balanced trees, easier to implement lock-free.

**Spatial Locality:** Principle that if memory location accessed, nearby locations likely accessed soon. Exploited by cache lines.

**Stable Sort:** Sorting algorithm maintaining relative order of equal elements. Merge sort is stable; quicksort is not.

**Stack:** LIFO (Last In, First Out) data structure. Operations: push (add to top), pop (remove from top). Used for function calls, recursion, backtracking, DFS.

**Strong Consistency:** All nodes see same data at same time. Requires coordination, reduces availability during partitions.

**Superscalar:** CPU executing multiple instructions per cycle. Requires instruction-level parallelism and out-of-order execution.

**Symbol Table:** Data structure mapping identifiers to information (type, scope, location). Used by compilers.

## T

**Tabulation:** Bottom-up dynamic programming approach iteratively filling table with subproblem solutions.

**Temporal Locality:** Principle that if memory location accessed, it will likely be accessed again soon. Exploited by caches.

**Thread:** Execution context within process. Shares address space with other threads but has own stack and registers. Cheaper than processes.

**TLB (Translation Lookaside Buffer):** Cache for virtual→physical address translations. Small but high hit rate (>95%). TLB miss requires page table walk.

**Topological Sort:** Linear ordering of directed acyclic graph vertices such that for every edge u→v, u comes before v. Used for scheduling tasks with dependencies.

**Tractable:** Problem with known polynomial-time algorithm. Generally considered efficiently solvable.

**Transaction:** Sequence of operations executed as single atomic unit. ACID properties: Atomicity, Consistency, Isolation, Durability.

**Traveling Salesman Problem (TSP):** Find shortest route visiting all cities exactly once. NP-complete. Exact solutions exist but exponential; approximation algorithms for special cases.

**Tree:** Connected acyclic graph. Used to represent hierarchical relationships. Binary tree: each node has ≤2 children.

**Trie (Prefix Tree):** Tree where each path represents string. Edges labeled with characters. Enables O(m) insert/search where m = string length. Used for autocomplete, spell checking.

**Turing Machine:** Mathematical model of computation defined by Turing (1936). Consists of infinite tape, read/write head, finite states, and transition function. Foundation of computability theory.

**Two-Phase Commit (2PC):** Distributed transaction protocol with prepare and commit phases. Ensures atomicity but blocking on coordinator failure.

## U

**Undecidable:** Problem with no algorithm that always halts and correctly answers yes/no. Examples: halting problem, Rice's theorem problems.

**Union-Find (Disjoint Set):** Data structure tracking partition of set into disjoint subsets. Near-constant time operations with path compression and union by rank. Used in Kruskal's MST, cycle detection.

**Universal Turing Machine:** Turing machine that can simulate any other Turing machine. Establishes that computation can be universal—one machine can run any program.

## V

**Vertex Cover:** Set of vertices such that every edge has at least one endpoint in set. Finding minimum vertex cover is NP-complete. 2-approximation algorithm exists.

**Virtual Memory:** Abstraction giving each process illusion of large, contiguous address space. Implemented with paging. Enables processes larger than physical memory and isolation between processes.

**Von Neumann Architecture:** Computer architecture with CPU, memory, and I/O connected by bus. Programs and data stored in same memory (stored-program concept).

## W

**Working Set:** Pages process actively uses. If working set > physical memory, thrashing occurs (constant paging).

## Other

**2-SAT:** Boolean satisfiability with clauses of size ≤2. Solvable in linear time (unlike 3-SAT which is NP-complete). Shows how small changes affect tractability.

**3-SAT:** Boolean satisfiability with clauses of exactly 3 literals. First problem proved NP-complete (Cook-Levin theorem). Many reductions start from 3-SAT.

## Summary

This glossary covers fundamental concepts across:
- **Theory:** Computability, complexity classes, Turing machines
- **Algorithms:** Sorting, searching, graph algorithms, paradigms
- **Data Structures:** Arrays, trees, graphs, hash tables, heaps
- **Systems:** Computer architecture, operating systems, compilers, distributed systems

Understanding these terms provides vocabulary for discussing, analyzing, and designing computational systems. They represent accumulated knowledge from 90+ years of computer science—concepts that remain relevant regardless of programming language, framework, or hardware platform.
