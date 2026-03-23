# Fundamental Data Structures

## Overview

Data structures organize information to enable efficient operations. Choosing the right data structure is often more important than choosing the right algorithm—a hash table can make the difference between O(1) and O(n) lookup time, transforming unusable software into responsive systems.

This chapter covers foundational structures: arrays, linked lists, stacks, queues, hash tables, trees, heaps, and graphs. Each structure optimizes different operations. Arrays provide fast random access but slow insertion. Linked lists provide fast insertion but slow random access. Hash tables provide fast lookup but no ordering. Trees provide ordered data with logarithmic operations. Understanding trade-offs guides structure selection.

## Arrays

### Static Arrays

Contiguous memory block storing fixed number of elements.

**Properties:**
- **Size**: Fixed at creation
- **Access**: O(1) by index
- **Insertion/Deletion**: O(n) (must shift elements)
- **Search**: O(n) unsorted, O(log n) sorted

**Memory Layout:**
```
[0][1][2][3][4] → consecutive memory addresses
```

**Operations:**
```
Access arr[i]:        O(1)  - address = base + i × element_size
Insert at end:        O(1)  - if space available
Insert at position:   O(n)  - shift n-i elements right
Delete at position:   O(n)  - shift elements left
Search:               O(n)  - linear scan (O(log n) if sorted)
```

**Advantages:**
- Constant-time random access
- Cache-friendly (contiguous memory)
- Low memory overhead
- Simple implementation

**Disadvantages:**
- Fixed size
- Expensive insertion/deletion
- Wasted space if partially filled

**Use Cases:**
- Known fixed size collections
- Frequent random access
- Implementing other structures (stacks, heaps)

### Dynamic Arrays

Automatically resizing arrays (Python list, Java ArrayList, C++ vector).

**Growth Strategy:**
- Start with capacity (e.g., 10)
- When full, allocate larger array (typically 2× size)
- Copy elements to new array
- Deallocate old array

**Amortized Analysis:**
- Single insertion: O(1) average, O(n) worst case
- Sequence of n insertions: O(n) total
- Amortized cost per insertion: O(1)

**Why doubling works:**
```
Insertions: 1, 2, 3, 4, 5, 6, 7, 8, 9, ...
Resize costs:    1     2        4        8
Total copies: 1 + 1 + 2 + 1 + 4 + 1 + 1 + 8 = 19 copies for 9 insertions
Average: ~2 copies per insertion (amortized O(1))
```

**Memory Usage:**
- Growth factor 2: 50% wasted space worst case
- Growth factor 1.5: 33% wasted space worst case
- Trade-off: smaller growth = more frequent resizing

**Use Cases:**
- Unknown size at creation
- Mostly append operations
- Occasional random access
- Default choice for general-purpose lists

## Linked Lists

### Singly Linked Lists

Nodes containing data and pointer to next node.

**Structure:**
```
[data|next] → [data|next] → [data|next] → null
```

**Operations:**
```
Access node i:           O(n)  - traverse from head
Insert at head:          O(1)  - create node, point to old head
Insert at tail:          O(n)  - traverse to end (O(1) with tail pointer)
Insert after node:       O(1)  - repoint next pointers
Delete at head:          O(1)  - move head pointer
Delete node:             O(n)  - need previous node
Search:                  O(n)  - linear scan
```

**Implementation:**
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_head(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete_node(self, data):
        if not self.head:
            return
        if self.head.data == data:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return
            current = current.next
```

**Advantages:**
- Dynamic size
- Efficient insertion/deletion at known positions
- No wasted space (grows/shrinks as needed)

**Disadvantages:**
- No random access
- Extra memory for pointers
- Poor cache performance (non-contiguous)

### Doubly Linked Lists

Nodes with pointers to both next and previous nodes.

**Structure:**
```
null ← [prev|data|next] ⇄ [prev|data|next] ⇄ [prev|data|next] → null
```

**Additional Operations:**
```
Delete node:             O(1)  - have prev pointer
Traverse backward:       O(n)  - follow prev pointers
```

**Advantages over singly:**
- Can delete node without traversing
- Can traverse backward
- Some algorithms simpler (e.g., LRU cache)

**Disadvantages:**
- Extra memory (two pointers per node)
- More pointer manipulation

**Use Cases:**
- LRU cache implementation
- Browser history (back/forward)
- Undo/redo functionality
- Implementing deques

### Circular Linked Lists

Last node points back to first (or head).

**Use Cases:**
- Round-robin scheduling
- Implementing circular buffers
- Multiplayer game turn tracking

## Stacks

LIFO (Last In, First Out) data structure.

**Core Operations:**
```
push(x):    Add element to top       O(1)
pop():      Remove top element        O(1)
peek():     View top element          O(1)
isEmpty():  Check if empty            O(1)
```

**Implementation Options:**

**Array-based:**
```python
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0
```

**Linked-list-based:**
- Push/pop at head
- No size limit (except memory)

**Applications:**

**1. Function Call Stack:**
```
main() calls foo()
foo() calls bar()
bar() calls baz()

Stack: [main, foo, bar, baz] ← top
When baz() returns, pop from stack
```

**2. Expression Evaluation:**
```
Infix:   (3 + 4) × 5
Postfix: 3 4 + 5 ×

Algorithm:
- For each token:
  - Number: push to stack
  - Operator: pop two operands, apply, push result
```

**3. Parenthesis Matching:**
```python
def is_balanced(expr):
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    for char in expr:
        if char in pairs:
            stack.append(char)
        elif char in pairs.values():
            if not stack or pairs[stack.pop()] != char:
                return False
    return len(stack) == 0
```

**4. Backtracking:**
- DFS graph traversal
- Maze solving
- Undo functionality

**5. Compiler Applications:**
- Parsing expressions
- Function call management
- Syntax checking

## Queues

FIFO (First In, First Out) data structure.

**Core Operations:**
```
enqueue(x):  Add element to rear     O(1)
dequeue():   Remove front element    O(1)
front():     View front element      O(1)
isEmpty():   Check if empty          O(1)
```

**Implementation Options:**

**Circular Array:**
```python
class Queue:
    def __init__(self, capacity):
        self.items = [None] * capacity
        self.front = 0
        self.rear = 0
        self.size = 0
        self.capacity = capacity

    def enqueue(self, item):
        if self.size == self.capacity:
            raise Exception("Queue full")
        self.items[self.rear] = item
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue empty")
        item = self.items[self.front]
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item
```

**Linked-list-based:**
- Enqueue at tail, dequeue at head
- No size limit

**Applications:**

**1. Task Scheduling:**
- CPU job scheduling
- Print queue
- Request handling in servers

**2. BFS Graph Traversal:**
```python
def bfs(graph, start):
    visited = set()
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            queue.extend(graph[node])
```

**3. Message Passing:**
- Inter-process communication
- Event handling systems
- Asynchronous processing

**4. Cache Implementations:**
- FIFO cache eviction
- Request buffering

### Priority Queues

Elements have priorities; highest priority dequeued first.

**Implementation:** Typically heap (covered in Advanced Data Structures)

**Operations:**
```
insert(x, priority):     O(log n)
extractMax():            O(log n)
peek():                  O(1)
```

**Applications:**
- Dijkstra's shortest path
- Huffman coding
- Event-driven simulation
- Job scheduling

## Hash Tables

Map keys to values using hash function.

**Core Concept:**
```
hash(key) → index in array
array[index] → value
```

**Properties:**
```
Insert:      O(1) average, O(n) worst
Delete:      O(1) average, O(n) worst
Search:      O(1) average, O(n) worst
```

### Hash Functions

**Requirements:**
1. Deterministic (same key → same hash)
2. Uniform distribution (avoid clustering)
3. Fast to compute

**Common hash functions:**

**Division method:**
```
h(k) = k mod m
Choose m prime, not near power of 2
```

**Multiplication method:**
```
h(k) = ⌊m × (k × A mod 1)⌋
A ≈ (√5 - 1)/2 (golden ratio)
```

**Universal hashing:**
```
h(k) = ((a × k + b) mod p) mod m
a, b random, p prime > max key
```

### Collision Resolution

**1. Chaining:**
- Each bucket → linked list
- Insert: add to list at hash(key)
- Search: scan list at hash(key)

```
[0] → 3 → 13 → 23
[1] → 1 → 11
[2] → 2
[3] → null
```

**Load factor α = n/m** (n items, m buckets)
- Average chain length: α
- Search time: O(1 + α)
- Keep α < 0.75 for good performance

**2. Open Addressing:**

**Linear probing:**
```
h(k, i) = (h(k) + i) mod m
Try slots: h(k), h(k)+1, h(k)+2, ...
```
- Simple but causes clustering

**Quadratic probing:**
```
h(k, i) = (h(k) + c₁i + c₂i²) mod m
Try slots: h(k), h(k)+1, h(k)+4, h(k)+9, ...
```
- Reduces clustering

**Double hashing:**
```
h(k, i) = (h₁(k) + i × h₂(k)) mod m
```
- Best distribution, like uniform hashing

### Resizing

**When to resize:**
- Load factor α exceeds threshold (typically 0.75)

**How to resize:**
1. Allocate new array (typically 2× size)
2. Rehash all existing keys
3. Insert into new array
4. Deallocate old array

**Cost:**
- Single resize: O(n)
- Amortized over n insertions: O(1) per insertion

### Applications

**1. Database Indexing:**
- Fast key lookup
- Join operations

**2. Caching:**
```python
class Cache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def put(self, key, value):
        self.cache[key] = value
```

**3. Symbol Tables (Compilers):**
- Variable names → memory locations
- Function names → addresses

**4. Sets:**
- Hash set: hash table without values
- Fast membership testing

**5. Counting:**
```python
def word_frequency(text):
    freq = {}
    for word in text.split():
        freq[word] = freq.get(word, 0) + 1
    return freq
```

## Binary Search Trees (BST)

Tree where each node has ≤ 2 children, with ordering property:
- Left subtree values < node value
- Right subtree values > node value

**Structure:**
```
      8
     / \
    3   10
   / \    \
  1   6   14
     / \  /
    4  7 13
```

**Operations:**
```
Search:         O(h)  where h = height
Insert:         O(h)
Delete:         O(h)
Min/Max:        O(h)
Inorder:        O(n)  yields sorted order
```

### BST Operations

**Search:**
```python
def search(root, key):
    if root is None or root.val == key:
        return root
    if key < root.val:
        return search(root.left, key)
    return search(root.right, key)
```

**Insert:**
```python
def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.val:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root
```

**Delete (3 cases):**
1. **Leaf node**: Simply remove
2. **One child**: Replace with child
3. **Two children**: Replace with inorder successor (leftmost in right subtree)

```python
def delete(root, key):
    if root is None:
        return root
    if key < root.val:
        root.left = delete(root.left, key)
    elif key > root.val:
        root.right = delete(root.right, key)
    else:
        # Node with only one child or no child
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left
        # Node with two children: get inorder successor
        temp = minValueNode(root.right)
        root.val = temp.val
        root.right = delete(root.right, temp.val)
    return root
```

**Traversals:**
```
Inorder (left, root, right):     1, 3, 4, 6, 7, 8, 10, 13, 14  (sorted!)
Preorder (root, left, right):    8, 3, 1, 6, 4, 7, 10, 14, 13
Postorder (left, right, root):   1, 4, 7, 6, 3, 13, 14, 10, 8
```

### BST Performance

**Best case:** Balanced tree
- Height h = O(log n)
- All operations: O(log n)

**Worst case:** Degenerate (linked list)
```
1
 \
  2
   \
    3
     \
      4
```
- Height h = O(n)
- All operations: O(n)

**Solution:** Self-balancing trees (AVL, Red-Black) keep h = O(log n)

### Applications

**1. Maintaining Sorted Data:**
- Insert/delete while maintaining order
- Range queries

**2. Database Indexing:**
- B-trees (generalization of BST)

**3. Priority Queues:**
- Alternative to heaps

**4. Symbol Tables:**
- Compiler variable lookups

## Summary

Fundamental data structures provide building blocks for efficient algorithms:

**Arrays:** Fast random access, fixed/growing size, contiguous memory
**Linked Lists:** Dynamic size, efficient insertion/deletion, no random access
**Stacks:** LIFO, function calls, expression evaluation, backtracking
**Queues:** FIFO, task scheduling, BFS, message passing
**Hash Tables:** O(1) average lookup, no ordering, collision handling
**BSTs:** O(log n) operations when balanced, maintain sorted order

Choosing the right structure requires understanding:
- What operations will be frequent?
- Is size known in advance?
- Is ordering needed?
- Is random access required?
- What are memory constraints?

These fundamentals appear everywhere—from operating system schedulers to database engines to web servers. Mastery enables recognizing when to apply each structure and understanding performance implications of choices made.
