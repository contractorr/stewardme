# Algorithm Design Paradigms

## Overview

Algorithm design paradigms are general approaches for solving computational problems. Rather than memorizing individual algorithms, understanding paradigms enables solving novel problems by recognizing which approach fits. Divide and conquer breaks problems into smaller pieces. Greedy algorithms make locally optimal choices. Dynamic programming solves overlapping subproblems once. Backtracking explores solution spaces systematically.

These paradigms aren't mutually exclusive—sophisticated algorithms often combine approaches. Quicksort uses divide-and-conquer. Dijkstra's algorithm is greedy. The Bellman-Ford algorithm uses dynamic programming. Understanding when each paradigm applies and how to combine them separates algorithmic thinking from code implementation.

## Divide and Conquer

**Strategy:**
1. **Divide:** Break problem into smaller subproblems
2. **Conquer:** Solve subproblems recursively
3. **Combine:** Merge solutions to get final answer

**When to use:**
- Problem can be broken into independent subproblems
- Subproblems have same structure as original
- Combination step is efficient

### Merge Sort

**Idea:** Recursively divide array in half, sort halves, merge sorted halves.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # Divide
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    # Combine
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Analysis:**
- Recurrence: T(n) = 2T(n/2) + O(n)
- Solution: O(n log n)
- Space: O(n) for merge array
- Stable: Yes (maintains relative order)

**Advantages:**
- Guaranteed O(n log n)
- Stable sorting
- Good for linked lists (no random access needed)

**Disadvantages:**
- O(n) extra space
- Slower than quicksort in practice (more data movement)

### Quick Sort

**Idea:** Choose pivot, partition array around pivot, recursively sort partitions.

```python
def quick_sort(arr, low, high):
    if low < high:
        # Partition and get pivot index
        pi = partition(arr, low, high)

        # Recursively sort before and after partition
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

**Analysis:**
- Best/Average: O(n log n)
- Worst: O(n²) — occurs with bad pivots (already sorted)
- Space: O(log n) recursion stack
- In-place: Yes
- Stable: No

**Pivot Selection Strategies:**
- **Last element:** Simple but vulnerable to sorted input
- **Random:** Expected O(n log n)
- **Median-of-three:** Choose median of first, middle, last
- **Median-of-medians:** Guarantees O(n log n) but high constant

**Why quicksort dominates in practice:**
- Cache-friendly (locality of reference)
- In-place (no extra memory)
- Fewer comparisons than merge sort average case
- Easily parallelizable

### Binary Search

**Idea:** Repeatedly halve search space in sorted array.

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

**Analysis:**
- Time: O(log n)
- Space: O(1) iterative, O(log n) recursive

**Variants:**
- **Lower bound:** First position ≥ target
- **Upper bound:** First position > target
- **Search rotated array:** Handle sorted + rotated
- **Search 2D matrix:** Apply twice

### Master Theorem

**Solves recurrences of form:** T(n) = aT(n/b) + f(n)

**Cases:**
1. If f(n) = O(n^(log_b a - ε)) for ε > 0: T(n) = Θ(n^log_b a)
2. If f(n) = Θ(n^log_b a): T(n) = Θ(n^log_b a × log n)
3. If f(n) = Ω(n^(log_b a + ε)) for ε > 0 and af(n/b) ≤ cf(n): T(n) = Θ(f(n))

**Examples:**
```
Merge sort: T(n) = 2T(n/2) + O(n)
  a=2, b=2, log_b a = 1
  f(n) = O(n) = Θ(n^1) → Case 2 → T(n) = O(n log n)

Binary search: T(n) = T(n/2) + O(1)
  a=1, b=2, log_b a = 0
  f(n) = O(1) = Θ(n^0) → Case 2 → T(n) = O(log n)

Karatsuba multiplication: T(n) = 3T(n/2) + O(n)
  a=3, b=2, log_b a = log_2 3 ≈ 1.585
  f(n) = O(n) = O(n^1.585 - ε) → Case 1 → T(n) = O(n^1.585)
```

## Greedy Algorithms

**Strategy:** Make locally optimal choice at each step, hoping to find global optimum.

**When greedy works:**
- **Greedy choice property:** Local optimum leads to global optimum
- **Optimal substructure:** Optimal solution contains optimal subsolutions

**When greedy fails:**
- Most problems (greedy usually doesn't work)
- Need proof or counterexample to verify

### Activity Selection

**Problem:** Select maximum number of non-overlapping activities.

```
Activities (start, end):
(1,3), (2,5), (4,7), (1,8), (5,9), (8,10)
```

**Greedy strategy:** Always pick activity with earliest end time.

```python
def activity_selection(activities):
    # Sort by end time
    activities.sort(key=lambda x: x[1])

    selected = [activities[0]]
    last_end = activities[0][1]

    for activity in activities[1:]:
        if activity[0] >= last_end:
            selected.append(activity)
            last_end = activity[1]

    return selected
```

**Analysis:**
- Time: O(n log n) for sorting
- Greedy gives optimal solution

**Proof:** If greedy choice (earliest end) is wrong, can replace any other choice with greedy choice without decreasing solution size.

### Huffman Coding

**Problem:** Optimal prefix-free binary encoding for characters based on frequency.

**Idea:** Build binary tree where frequent characters have shorter codes.

```python
import heapq

def huffman_coding(freq):
    # Create leaf nodes
    heap = [[weight, [char, ""]] for char, weight in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)

        # Add 0 to left subtree codes, 1 to right
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]

        # Merge
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
```

**Example:**
```
Frequencies: A:45, B:13, C:12, D:16, E:9, F:5
Codes: A:0, C:100, B:101, F:1100, E:1101, D:111
Average bits per char: 2.224 vs 3.0 for fixed-length
```

**Properties:**
- Optimal prefix-free code
- Time: O(n log n)
- Used in: ZIP, JPEG, MP3

### Interval Scheduling Maximization

**Problem:** Assign jobs to minimum number of resources.

**Greedy strategy:** Sort by start time, assign to first available resource.

```python
def min_resources(intervals):
    if not intervals:
        return 0

    # Sort by start time
    intervals.sort()

    # Track end times of resources
    resources = []

    for start, end in intervals:
        # Find resource that finishes before this starts
        placed = False
        for i in range(len(resources)):
            if resources[i] <= start:
                resources[i] = end
                placed = True
                break

        if not placed:
            resources.append(end)

    return len(resources)
```

**Analysis:**
- Time: O(n²) naive, O(n log n) with heap
- Greedy gives optimal solution

### Dijkstra's Algorithm

**Problem:** Single-source shortest paths in weighted graph (non-negative weights).

**Greedy choice:** Always expand closest unvisited vertex.

```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    visited = set()

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current in visited:
            continue
        visited.add(current)

        for neighbor, weight in graph[current]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances
```

**Analysis:**
- Time: O((V + E) log V) with binary heap
- Time: O(V² + E) with array (dense graphs)
- Fails with negative weights (use Bellman-Ford)

**Correctness:** Greedy choice (nearest vertex) is always part of optimal path when weights are non-negative.

## Dynamic Programming

**Strategy:** Solve subproblems once, store results, reuse when needed.

**Requirements:**
1. **Optimal substructure:** Optimal solution contains optimal subsolutions
2. **Overlapping subproblems:** Same subproblems recur multiple times

**Approaches:**
- **Top-down (memoization):** Recursion + cache
- **Bottom-up (tabulation):** Iteratively fill table

### Fibonacci Numbers

**Naive recursion:** T(n) = T(n-1) + T(n-2) + O(1) → O(2^n)

**Memoization:**
```python
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]
```
Time: O(n), Space: O(n)

**Tabulation:**
```python
def fib_tab(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```
Time: O(n), Space: O(n)

**Space-optimized:**
```python
def fib_opt(n):
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
```
Time: O(n), Space: O(1)

### Longest Common Subsequence (LCS)

**Problem:** Find longest subsequence common to two strings.

```
LCS("ABCDGH", "AEDFHR") = "ADH" (length 3)
```

**DP formulation:**
```
LCS(i, j) = {
  0                           if i=0 or j=0
  LCS(i-1, j-1) + 1           if X[i]=Y[j]
  max(LCS(i-1,j), LCS(i,j-1)) otherwise
}
```

**Implementation:**
```python
def lcs(X, Y):
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]
```

**Analysis:**
- Time: O(mn)
- Space: O(mn) — can optimize to O(min(m,n))

**Applications:**
- Diff tools
- DNA sequence alignment
- Version control

### 0/1 Knapsack

**Problem:** Maximize value of items in knapsack with weight limit.

```
Items: [(value, weight)]
Capacity: W
Goal: Select subset maximizing value subject to weight ≤ W
```

**DP formulation:**
```
K(i, w) = {
  0                              if i=0 or w=0
  K(i-1, w)                      if weight[i] > w
  max(K(i-1,w),                  otherwise
      value[i] + K(i-1, w-weight[i]))
}
```

**Implementation:**
```python
def knapsack(values, weights, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    values[i-1] + dp[i-1][w - weights[i-1]],
                    dp[i-1][w]
                )
            else:
                dp[i][w] = dp[i-1][w]

    return dp[n][capacity]
```

**Analysis:**
- Time: O(nW)
- Space: O(nW) — can optimize to O(W)
- Pseudo-polynomial: Not polynomial in input size (W could be exponential in bits)

### Edit Distance

**Problem:** Minimum operations (insert, delete, substitute) to transform one string to another.

```
Edit distance("kitten", "sitting") = 3
  kitten → sitten (substitute k→s)
  sitten → sittin (substitute e→i)
  sittin → sitting (insert g)
```

**DP formulation:**
```
ED(i, j) = {
  i                           if j=0
  j                           if i=0
  ED(i-1, j-1)                if X[i]=Y[j]
  1 + min(ED(i-1,j),          otherwise
          ED(i,j-1),
          ED(i-1,j-1))
}
```

**Implementation:**
```python
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],      # delete
                    dp[i][j-1],      # insert
                    dp[i-1][j-1]     # substitute
                )

    return dp[m][n]
```

**Analysis:**
- Time: O(mn)
- Space: O(mn)

**Applications:**
- Spell checking
- DNA sequence alignment
- Plagiarism detection

### Matrix Chain Multiplication

**Problem:** Find optimal parenthesization to minimize scalar multiplications.

```
A₁(10×20) × A₂(20×30) × A₃(30×40)

(A₁A₂)A₃: 10×20×30 + 10×30×40 = 18,000
A₁(A₂A₃): 20×30×40 + 10×20×40 = 32,000
Optimal: (A₁A₂)A₃
```

**DP formulation:**
```
M[i,j] = min{M[i,k] + M[k+1,j] + cost of multiplying M[i,k] and M[k+1,j]}
         for i ≤ k < j
```

**Analysis:**
- Time: O(n³)
- Space: O(n²)

## Backtracking

**Strategy:** Build solution incrementally, abandon paths that violate constraints.

**Template:**
```python
def backtrack(solution, constraints):
    if is_complete(solution):
        process_solution(solution)
        return

    for candidate in generate_candidates(solution):
        if is_valid(candidate, constraints):
            solution.append(candidate)
            backtrack(solution, constraints)
            solution.pop()  # Backtrack
```

### N-Queens

**Problem:** Place N queens on N×N board so none attack each other.

```python
def solve_n_queens(n):
    def is_safe(board, row, col):
        # Check column
        for i in range(row):
            if board[i] == col:
                return False
        # Check diagonals
        for i in range(row):
            if abs(board[i] - col) == abs(i - row):
                return False
        return True

    def backtrack(board, row):
        if row == n:
            solutions.append(board[:])
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(board, row + 1)
                board[row] = -1

    solutions = []
    backtrack([-1] * n, 0)
    return solutions
```

**Analysis:**
- Worst case: O(n!) — exponential
- Pruning dramatically reduces actual runtime

### Sudoku Solver

```python
def solve_sudoku(board):
    def is_valid(board, row, col, num):
        # Check row
        if num in board[row]:
            return False
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        # Check 3×3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False
        return True

    def backtrack():
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    for num in '123456789':
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            if backtrack():
                                return True
                            board[i][j] = '.'
                    return False
        return True

    backtrack()
    return board
```

## Summary

Algorithm design paradigms provide systematic approaches to problem-solving:

**Divide and Conquer:**
- Break into subproblems, solve recursively, combine
- Examples: Merge sort, quick sort, binary search
- Analyze with Master Theorem

**Greedy:**
- Make locally optimal choices
- Works when greedy choice property + optimal substructure hold
- Examples: Activity selection, Huffman coding, Dijkstra's

**Dynamic Programming:**
- Solve overlapping subproblems once
- Requires optimal substructure + overlapping subproblems
- Examples: LCS, knapsack, edit distance
- Trade space for time

**Backtracking:**
- Explore solution space systematically
- Prune branches violating constraints
- Examples: N-queens, Sudoku, graph coloring
- Exponential but practical with pruning

**Choosing paradigms:**
- Divide and conquer: Independent subproblems
- Greedy: Local choice leads to global optimum
- DP: Overlapping subproblems
- Backtracking: Constraint satisfaction

Mastering paradigms enables recognizing problem patterns and selecting appropriate approaches—the essence of algorithmic thinking.
