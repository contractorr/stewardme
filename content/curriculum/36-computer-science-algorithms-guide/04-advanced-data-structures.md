# Advanced Data Structures

## Overview

Advanced data structures solve specialized problems or improve upon fundamental structures. Self-balancing trees guarantee O(log n) operations. Heaps enable efficient priority queues. Graphs model relationships. Tries optimize string operations. Union-find tracks disjoint sets. These structures transform intractable problems into efficient solutions and enable algorithms that would be impossible with basic structures alone.

This chapter covers structures used in production systems: AVL and Red-Black trees in language runtimes, heaps in schedulers, graphs in social networks, tries in autocomplete, Bloom filters in databases, and skip lists in distributed systems.

## Self-Balancing Binary Search Trees

Basic BSTs degrade to O(n) when unbalanced. Self-balancing trees maintain O(log n) height through rotations and rebalancing.

### AVL Trees

**Invented:** 1962 by Adelson-Velsky and Landis

**Invariant:** For every node, heights of left and right subtrees differ by at most 1.

**Balance Factor:**
```
BF(node) = height(left) - height(right)
Must be in {-1, 0, 1}
```

**Rotations:**

**Right rotation (LL case):**
```
      y                    x
     / \                  / \
    x   C    →           A   y
   / \                      / \
  A   B                    B   C
```

**Left rotation (RR case):**
```
    x                        y
   / \                      / \
  A   y        →           x   C
     / \                  / \
    B   C                A   B
```

**Left-Right (LR case):** Left rotate child, then right rotate parent
**Right-Left (RL case):** Right rotate child, then left rotate parent

**Implementation Details:**
```python
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

def height(node):
    return node.height if node else 0

def balance_factor(node):
    return height(node.left) - height(node.right)

def right_rotate(y):
    x = y.left
    T = x.right
    x.right = y
    y.left = T
    y.height = 1 + max(height(y.left), height(y.right))
    x.height = 1 + max(height(x.left), height(x.right))
    return x

def insert(root, key):
    # Standard BST insert
    if not root:
        return AVLNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)

    # Update height
    root.height = 1 + max(height(root.left), height(root.right))

    # Get balance factor
    balance = balance_factor(root)

    # LL case
    if balance > 1 and key < root.left.key:
        return right_rotate(root)

    # RR case
    if balance < -1 and key > root.right.key:
        return left_rotate(root)

    # LR case
    if balance > 1 and key > root.left.key:
        root.left = left_rotate(root.left)
        return right_rotate(root)

    # RL case
    if balance < -1 and key < root.right.key:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root
```

**Performance:**
```
Search:     O(log n) guaranteed
Insert:     O(log n) with ≤2 rotations
Delete:     O(log n) with ≤2 rotations
Space:      O(n) + height field per node
```

**Use Cases:**
- Frequent lookups, less frequent insertions
- Databases where read performance critical
- Applications requiring strict balance

### Red-Black Trees

**Properties:**
1. Every node is red or black
2. Root is black
3. Leaves (NIL) are black
4. Red node has black children (no consecutive reds)
5. All paths from node to descendant leaves have same number of black nodes

**Why these properties matter:** Guarantee height ≤ 2 log(n + 1)

**Advantages over AVL:**
- Fewer rotations (≤3 for insert, ≤3 for delete)
- Faster insertion/deletion
- More relaxed balancing (black height, not absolute height)

**Implementation:** More complex than AVL but widely used

**Insertion Cases:**
```
Case 1: Uncle is red
  → Recolor parent, uncle, grandparent

Case 2: Uncle is black, node is inner child
  → Rotate to convert to Case 3

Case 3: Uncle is black, node is outer child
  → Rotate and recolor
```

**Performance:**
```
Search:     O(log n)
Insert:     O(log n) with ≤3 rotations
Delete:     O(log n) with ≤3 rotations
```

**Real-World Usage:**
- Java TreeMap, TreeSet
- C++ std::map, std::set
- Linux kernel scheduler
- Most language standard libraries

**AVL vs Red-Black:**
| Aspect | AVL | Red-Black |
|--------|-----|-----------|
| Balance | Stricter (height diff ≤ 1) | Relaxed (height ≤ 2 log n) |
| Lookups | Slightly faster | Slightly slower |
| Insertions | Slower (more rotations) | Faster |
| Deletions | Slower | Faster |
| Use case | Read-heavy | Mixed read/write |

### B-Trees

**Generalization:** Each node has multiple keys and children

**Properties:**
- Minimum degree t: node has ≥t-1 keys (except root)
- Node has ≤2t-1 keys
- Internal node with k keys has k+1 children
- All leaves at same depth

**Structure (B-tree with t=3):**
```
              [10, 20, 30]
       /         |        |        \
  [1,5,8]  [11,15,18]  [21,25]  [31,35,40]
```

**Why B-trees:**
- Minimize disk reads (high branching factor)
- Good cache performance
- Balanced by construction

**Performance:**
```
Height:     O(log_t n)
Search:     O(log n) comparisons, O(log_t n) disk reads
Insert:     O(log n)
Delete:     O(log n)
```

**Applications:**
- Database indexes (B+ trees variant)
- File systems (NTFS, ext4, HFS+)
- Large datasets that don't fit in memory

## Heaps

**Definition:** Complete binary tree satisfying heap property.

**Max-heap property:** Parent ≥ children
**Min-heap property:** Parent ≤ children

**Structure (max-heap):**
```
        100
       /   \
      19    36
     / \   / \
    17  3 25  1
   / \
  2   7

Array: [100, 19, 36, 17, 3, 25, 1, 2, 7]
```

**Array representation:**
```
For node at index i:
  Parent:       (i-1) / 2
  Left child:   2i + 1
  Right child:  2i + 2
```

### Heap Operations

**Insert (bubble up):**
```python
def insert(heap, key):
    heap.append(key)
    i = len(heap) - 1
    # Bubble up
    while i > 0 and heap[parent(i)] < heap[i]:
        swap(heap, i, parent(i))
        i = parent(i)
```
Time: O(log n)

**Extract max (bubble down):**
```python
def extract_max(heap):
    if len(heap) == 0:
        return None
    max_val = heap[0]
    heap[0] = heap[-1]
    heap.pop()
    # Bubble down
    i = 0
    while True:
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < len(heap) and heap[left] > heap[largest]:
            largest = left
        if right < len(heap) and heap[right] > heap[largest]:
            largest = right
        if largest == i:
            break
        swap(heap, i, largest)
        i = largest
    return max_val
```
Time: O(log n)

**Build heap (heapify):**
```python
def heapify(arr):
    n = len(arr)
    # Start from last non-leaf and work up
    for i in range(n // 2 - 1, -1, -1):
        bubble_down(arr, i)
```
Time: O(n) — surprisingly not O(n log n)!

**Why O(n) for heapify:**
- Most nodes are near leaves (low height)
- Cost weighted by number of nodes at each level
- Sum: n/2 × 0 + n/4 × 1 + n/8 × 2 + ... = O(n)

### Applications

**1. Priority Queues:**
```python
import heapq

pq = []
heapq.heappush(pq, (priority, item))
priority, item = heapq.heappop(pq)
```

**2. Heap Sort:**
```python
def heap_sort(arr):
    heapify(arr)
    sorted_arr = []
    while arr:
        sorted_arr.append(extract_max(arr))
    return sorted_arr[::-1]
```
Time: O(n log n), Space: O(1) in-place

**3. K Largest/Smallest Elements:**
```python
def k_largest(arr, k):
    return heapq.nlargest(k, arr)
```
Time: O(n log k) using min-heap of size k

**4. Median Tracking:**
- Two heaps: max-heap for lower half, min-heap for upper half
- Median at top of one heap

**5. Graph Algorithms:**
- Dijkstra's shortest path
- Prim's minimum spanning tree
- A* pathfinding

## Graphs

**Definition:** G = (V, E) where V = vertices, E = edges

**Types:**

**Directed vs Undirected:**
```
Directed:          Undirected:
  A → B              A — B
  ↓   ↓              |   |
  C → D              C — D
```

**Weighted vs Unweighted:**
```
Weighted:          Unweighted:
  A -5→ B            A → B
  ↓     ↓            ↓   ↓
  C -2→ D            C → D
```

### Graph Representations

**1. Adjacency Matrix:**
```
   A B C D
A [0 1 1 0]
B [0 0 0 1]
C [0 0 0 1]
D [0 0 0 0]

Space: O(V²)
Edge check: O(1)
List neighbors: O(V)
```

**Advantages:**
- Fast edge existence check
- Simple implementation
- Good for dense graphs

**Disadvantages:**
- O(V²) space even for sparse graphs
- Slow to iterate neighbors

**2. Adjacency List:**
```python
graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': []
}

Space: O(V + E)
Edge check: O(degree)
List neighbors: O(degree)
```

**Advantages:**
- Space-efficient for sparse graphs
- Fast neighbor iteration
- Most real-world graphs are sparse

**Disadvantages:**
- Slower edge existence check
- More complex implementation

**3. Edge List:**
```python
edges = [('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')]
```

**Use cases:**
- Simple representation
- Good for algorithms that process all edges
- Kruskal's MST algorithm

### Graph Traversal

**Depth-First Search (DFS):**
```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    print(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited
```

**Properties:**
- Time: O(V + E)
- Space: O(V) for recursion stack
- Uses stack (explicit or recursion)

**Applications:**
- Topological sort
- Cycle detection
- Maze solving
- Pathfinding

**Breadth-First Search (BFS):**
```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        print(vertex)
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited
```

**Properties:**
- Time: O(V + E)
- Space: O(V) for queue
- Uses queue
- Finds shortest path in unweighted graphs

**Applications:**
- Shortest path (unweighted)
- Web crawling
- Social network distance
- Network broadcasting

### Graph Algorithms

**Dijkstra's Shortest Path:**
```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_dist, current = heapq.heappop(pq)

        if current_dist > distances[current]:
            continue

        for neighbor, weight in graph[current]:
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances
```

Time: O((V + E) log V) with heap

**Topological Sort:**
```python
def topological_sort(graph):
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)

    for node in graph:
        if node not in visited:
            dfs(node)

    return stack[::-1]
```

**Applications:**
- Task scheduling with dependencies
- Course prerequisites
- Build systems

## Tries (Prefix Trees)

**Structure:** Tree where each path represents a string

```
       root
      /  |  \
     c   t   i
    /    |    \
   a     o     s
  /  \   |
 t    r  p
[cat][car][top][is]
```

**Operations:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

**Complexity:**
```
Insert:         O(m) where m = word length
Search:         O(m)
Prefix search:  O(m)
Space:          O(ALPHABET_SIZE × N × M) worst case
```

**Applications:**
- Autocomplete
- Spell checkers
- IP routing tables
- Phone directories
- DNA sequence analysis

## Union-Find (Disjoint Set)

**Operations:**
- **Find:** Which set does element belong to?
- **Union:** Merge two sets

**Implementation with path compression + union by rank:**
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True
```

**Complexity:**
- Both operations: O(α(n)) where α = inverse Ackermann (effectively constant)

**Applications:**
- Kruskal's MST algorithm
- Detecting cycles in graphs
- Image segmentation
- Percolation theory
- Network connectivity

## Bloom Filters

**Probabilistic data structure** for set membership testing.

**Properties:**
- May have false positives (says element is in set when it's not)
- Never has false negatives (if says not in set, definitely not)
- Space-efficient

**How it works:**
1. Bit array of size m
2. k hash functions
3. Insert: set k bits to 1
4. Query: check if all k bits are 1

**Applications:**
- Web caching (avoid cache misses)
- Database query optimization
- Spell checkers
- Malware detection
- Bitcoin lightweight clients

## Skip Lists

**Probabilistic alternative to balanced trees.**

**Structure:** Linked list with multiple levels
```
Level 3:  1 ---------------→ 7 --------→ None
Level 2:  1 -----→ 4 -----→ 7 --------→ None
Level 1:  1 → 2 → 4 → 5 → 7 → 8 → 9 → None
```

**Properties:**
- Expected O(log n) search/insert/delete
- Simpler than balanced trees
- Good for concurrent access

**Applications:**
- Redis sorted sets
- LevelDB/RocksDB
- Distributed systems (easier to implement lock-free)

## Summary

Advanced data structures solve specialized problems efficiently:

**Self-balancing trees:** Guarantee O(log n) operations (AVL, Red-Black, B-trees)
**Heaps:** Priority queues, O(1) max/min access, O(log n) insert/delete
**Graphs:** Model relationships, enable network algorithms
**Tries:** Prefix-based operations, autocomplete
**Union-Find:** Track connected components, near-constant time
**Bloom Filters:** Space-efficient probabilistic membership
**Skip Lists:** Probabilistic alternative to balanced trees

Choosing advanced structures requires understanding:
- Worst-case vs average-case guarantees
- Read/write ratio
- Space constraints
- Implementation complexity
- Concurrency requirements

These structures power production systems—Red-Black trees in language runtimes, B-trees in databases, graphs in social networks, tries in search engines, union-find in network algorithms, Bloom filters in caches. Mastering them enables building scalable, efficient systems.
