# Systems Architecture

## Overview

Systems architecture bridges theory and practice—how abstract algorithms execute on physical hardware, how operating systems manage resources, how compilers translate high-level code to machine instructions, and how distributed systems coordinate across networks. Understanding systems architecture reveals why some theoretically equivalent algorithms perform drastically differently, explains performance bottlenecks, and enables building reliable software at scale.

This chapter covers the computational stack: hardware (CPU, memory hierarchy, I/O), operating systems (processes, scheduling, memory management), compilers (lexing, parsing, optimization, code generation), and distributed systems (consistency, fault tolerance, scalability). These layers transform human-readable code into coordinated execution across billions of transistors.

## Computer Organization

### Von Neumann Architecture

**Components:**
1. **CPU (Central Processing Unit):** Executes instructions
2. **Memory:** Stores instructions and data
3. **Input/Output:** Communicates with external world
4. **Bus:** Connects components

**Key insight:** Programs and data share same memory (stored-program concept).

**Fetch-Decode-Execute Cycle:**
```
1. Fetch: Read instruction from memory at program counter (PC)
2. Decode: Determine operation and operands
3. Execute: Perform operation
4. Update PC: Move to next instruction
```

**Limitations:**
- **Von Neumann bottleneck:** CPU and memory communicate via single bus
- Memory access slower than CPU → CPU often waits
- Modern solutions: caching, pipelining, parallelism

### CPU Architecture

**Components:**

**1. Control Unit:**
- Directs operation of processor
- Fetches, decodes instructions
- Coordinates data flow

**2. Arithmetic Logic Unit (ALU):**
- Performs arithmetic (add, subtract, multiply, divide)
- Performs logic (AND, OR, NOT, XOR)
- Handles comparison operations

**3. Registers:**
- Small, fast storage in CPU
- Program counter (PC): Next instruction address
- Instruction register (IR): Current instruction
- Accumulator: Stores computation results
- General-purpose registers: Temporary values

**4. Cache:**
- L1: Smallest, fastest (32-64 KB, 1-2 cycles)
- L2: Larger, slower (256 KB - 1 MB, 10-20 cycles)
- L3: Largest, slowest (8-32 MB, 40-75 cycles)

**Instruction Set Architecture (ISA):**

**CISC (Complex Instruction Set Computing):**
- Many instructions, some complex
- Variable-length instructions
- Example: x86
- Pros: Code density, powerful instructions
- Cons: Complex to decode, harder to pipeline

**RISC (Reduced Instruction Set Computing):**
- Fewer, simpler instructions
- Fixed-length instructions
- Example: ARM, RISC-V
- Pros: Easier pipelining, predictable timing
- Cons: More instructions per program

### Memory Hierarchy

**Registers:** 1 cycle, KB
**L1 Cache:** 1-3 cycles, tens of KB
**L2 Cache:** 10-20 cycles, hundreds of KB
**L3 Cache:** 40-75 cycles, MB
**Main Memory (RAM):** 100-300 cycles, GB
**SSD:** ~100,000 cycles, TB
**HDD:** ~10,000,000 cycles, TB

**Why hierarchy works: Locality**

**Temporal locality:** Recently accessed data likely accessed again soon
**Spatial locality:** Nearby addresses likely accessed soon

**Example:**
```python
# Good locality
for i in range(n):
    sum += arr[i]  # Sequential access

# Poor locality
for i in range(n):
    sum += arr[random.randint(0, n-1)]  # Random access
```

**Cache principles:**

**Cache line:** Minimum unit (typically 64 bytes)
**Cache hit:** Data in cache (fast)
**Cache miss:** Data not in cache (slow, fetch from lower level)

**Hit rate:** Fraction of accesses that hit
**Miss penalty:** Cost of cache miss

**Effective access time:** hit_rate × hit_time + (1 - hit_rate) × (hit_time + miss_penalty)

**Cache mapping:**

**1. Direct-mapped:**
- Each memory block → exactly one cache location
- Fast but high conflict misses

**2. Fully associative:**
- Any memory block → any cache location
- Flexible but expensive search

**3. N-way set associative:**
- Compromise: N possible locations per block
- Modern CPUs typically 8-16 way

**Cache coherence (multicore):**
- Multiple cores, each with cache
- Must keep caches consistent
- Protocols: MESI, MOESI

### Pipelining

**Idea:** Overlap instruction execution stages.

**Stages:**
1. **IF (Instruction Fetch):** Read instruction from memory
2. **ID (Instruction Decode):** Decode and read registers
3. **EX (Execute):** Perform operation
4. **MEM (Memory Access):** Read/write memory
5. **WB (Write Back):** Write result to register

**Without pipelining:** 5 cycles per instruction
**With pipelining:** 1 instruction per cycle (after pipeline fills)

**Hazards:**

**1. Data hazard:** Instruction depends on previous result
```assembly
ADD R1, R2, R3    # R1 = R2 + R3
SUB R4, R1, R5    # Needs R1 from previous instruction
```
**Solution:** Forwarding/bypassing, stalling

**2. Control hazard:** Branch changes program flow
```assembly
BEQ R1, R2, LABEL  # Branch if equal
ADD R3, R4, R5     # Should this execute?
```
**Solution:** Branch prediction, speculative execution

**3. Structural hazard:** Resource conflict
**Solution:** Duplicate resources

**Branch prediction:**
- **Static:** Always predict taken/not taken
- **Dynamic:** Track branch history
- Modern CPUs: >95% accuracy

### Parallelism

**Instruction-Level Parallelism (ILP):**
- Superscalar: Execute multiple instructions per cycle
- Out-of-order execution: Execute when ready, not in program order
- Speculative execution: Execute before knowing if needed

**Data-Level Parallelism:**
- SIMD (Single Instruction, Multiple Data): Same operation on multiple data
- Vector processors
- GPU: Thousands of cores for graphics/ML

**Thread-Level Parallelism:**
- Multiple cores execute different threads
- Hyperthreading/SMT: Multiple threads per core

**Multi-core vs Many-core:**
- Multi-core: Few powerful cores (4-16)
- Many-core: Many simple cores (GPU: thousands)

## Operating Systems

**Purpose:**
1. **Resource management:** CPU, memory, I/O
2. **Abstraction:** Hide hardware complexity
3. **Protection:** Isolate processes
4. **Efficiency:** Maximize resource utilization

### Processes and Threads

**Process:** Instance of running program
- Own address space
- Resources (files, sockets)
- At least one thread

**Thread:** Execution context within process
- Share address space with other threads
- Own stack, registers, program counter
- Cheaper than processes

**Process states:**
```
New → Ready → Running → Terminated
         ↑        ↓
         └─ Blocked
```

**Context switch:** Save/restore CPU state when switching processes
- Save registers, PC, stack pointer
- Load new process state
- Flush TLB, caches (expensive)
- Typical cost: 1-10 μs

**Process vs Thread creation:**
- Process: ~1000 μs (allocate address space, copy resources)
- Thread: ~10 μs (share address space)

### CPU Scheduling

**Goal:** Maximize CPU utilization, throughput; minimize turnaround time, waiting time, response time.

**Scheduling algorithms:**

**1. First-Come, First-Served (FCFS):**
- Simple: Queue in arrival order
- Problem: Convoy effect (short jobs wait for long jobs)

**2. Shortest Job First (SJF):**
- Optimal average waiting time
- Problem: Need to know job lengths, starvation of long jobs

**3. Round Robin (RR):**
- Time quantum (e.g., 10ms)
- Preempt after quantum, move to back of queue
- Fair, good response time
- Problem: Context switch overhead

**4. Priority Scheduling:**
- Each process has priority
- Problem: Starvation (low-priority may never run)
- Solution: Aging (increase priority over time)

**5. Multi-level Feedback Queue:**
- Multiple queues, different priorities
- Processes move between queues based on behavior
- Used in Unix, Windows

**Real-time scheduling:**
- **Hard real-time:** Deadlines must be met (life-critical systems)
- **Soft real-time:** Prefer meeting deadlines (multimedia)
- Earliest Deadline First (EDF), Rate Monotonic Scheduling (RMS)

### Memory Management

**Address space:** Virtual addresses process can use

**Physical memory:** Actual RAM

**Memory Management Unit (MMU):** Translates virtual → physical addresses

**Goals:**
1. Allow multiple processes to coexist
2. Protect processes from each other
3. Enable processes larger than physical memory
4. Provide illusion of contiguous memory

**Techniques:**

**1. Paging:**
- Divide virtual/physical memory into fixed-size pages (typically 4 KB)
- Page table maps virtual pages → physical frames
- Page fault: Access to non-resident page → OS loads from disk

**Page table entry:**
```
| Valid | Dirty | Referenced | Protection | Frame Number |
```

**Multi-level page tables:**
- Single-level: 2^20 entries for 32-bit address, 4 KB pages
- Multi-level: Tree structure, sparse representation
- x86-64: 4-level page table

**Translation Lookaside Buffer (TLB):**
- Cache for page table entries
- Small (64-1024 entries) but high hit rate (>95%)
- TLB miss: Access page table (slow)

**2. Segmentation:**
- Variable-size segments (code, data, stack)
- Segment table maps segment → physical memory
- Can combine with paging

**Page replacement algorithms:**

**LRU (Least Recently Used):**
- Replace page not used for longest time
- Approximates optimal
- Implementation: Expensive (track all accesses)

**Clock (Second Chance):**
- Circular buffer with reference bit
- Skip pages with reference bit = 1, set to 0
- Replace first page with reference bit = 0

**Working set:**
- Pages process actively uses
- Thrashing: Working set > physical memory → constant paging

### File Systems

**Abstraction:** Persistent storage as hierarchical namespace of files/directories

**Operations:** open, read, write, close, seek

**Implementation:**

**Disk structure:**
- **Superblock:** Metadata (size, block size, free blocks)
- **Inode table:** File metadata (permissions, size, timestamps, block pointers)
- **Data blocks:** File contents
- **Free space bitmap:** Track free blocks

**Inode structure:**
```
- Direct pointers (12): Point directly to data blocks
- Single indirect: Points to block of pointers
- Double indirect: Points to block of indirect pointers
- Triple indirect: Points to block of double indirect pointers
```

**Allows large files with compact inode.**

**Directory:** File mapping names → inode numbers

**Hard link:** Multiple directory entries → same inode
**Soft link (symlink):** File containing path to another file

**Journaling:**
- Log changes before applying
- Recover from crashes (replay log)
- Examples: ext3, ext4, NTFS

**Performance optimizations:**
- **Buffer cache:** Cache disk blocks in memory
- **Read-ahead:** Prefetch sequential blocks
- **Write-behind:** Delay writes, batch them

## Compilers

**Purpose:** Translate high-level code → machine code

**Phases:**

### 1. Lexical Analysis (Scanning)

**Input:** Source code (character stream)
**Output:** Token stream

**Example:**
```python
if x < 10:
    y = x + 5
```

**Tokens:**
```
IF, IDENTIFIER(x), LESS, NUMBER(10), COLON, NEWLINE,
INDENT, IDENTIFIER(y), EQUALS, IDENTIFIER(x), PLUS, NUMBER(5)
```

**Implementation:** Finite automata (regex)

### 2. Syntax Analysis (Parsing)

**Input:** Token stream
**Output:** Abstract Syntax Tree (AST)

**Grammar:**
```
stmt → IF expr COLON stmt
expr → expr OP expr | NUMBER | IDENTIFIER
```

**AST:**
```
       IF
      /  \
   LT     ASSIGN
  / \     /    \
 x  10   y     PLUS
              /   \
             x     5
```

**Techniques:**
- Top-down: Recursive descent, LL parsing
- Bottom-up: LR parsing, LALR (used by yacc)

### 3. Semantic Analysis

**Type checking:**
```python
x = "hello"
y = x + 5  # Type error: str + int
```

**Symbol table:** Track variable types, scopes

**Scope resolution:**
```python
x = 10      # Global
def foo():
    x = 5   # Local
    print(x)  # Refers to local x
```

### 4. Intermediate Representation (IR)

**Three-address code:**
```
t1 = x + 5
y = t1
```

**Static Single Assignment (SSA):**
- Each variable assigned exactly once
- Enables powerful optimizations

**Example:**
```
# Before SSA
x = a + b
x = x * 2
y = x + 1

# After SSA
x1 = a + b
x2 = x1 * 2
y = x2 + 1
```

### 5. Optimization

**Local optimizations:**
- **Constant folding:** 3 + 5 → 8
- **Constant propagation:** x = 5; y = x + 3 → y = 8
- **Dead code elimination:** Remove unreachable code
- **Algebraic simplification:** x * 0 → 0, x * 1 → x

**Global optimizations:**
- **Common subexpression elimination:**
  ```
  a = b + c
  d = b + c  # Reuse a instead
  ```

- **Loop-invariant code motion:**
  ```
  for i in range(n):
      x = y + z  # y, z don't change → move outside loop
      a[i] = x * i
  ```

**Interprocedural optimizations:**
- Inline small functions
- Devirtualization (replace virtual calls with direct calls)

**Register allocation:**
- Map infinite virtual registers → finite physical registers
- Graph coloring problem (NP-complete)
- Linear scan (fast approximation)

### 6. Code Generation

**Instruction selection:** IR → machine instructions
**Instruction scheduling:** Reorder to avoid hazards
**Register allocation:** Assign variables to registers

**Example:**
```
# IR
t1 = a + b
c = t1 * 2

# x86 assembly
mov eax, [a]
add eax, [b]
shl eax, 1      # Shift left = multiply by 2
mov [c], eax
```

### Just-In-Time (JIT) Compilation

**Idea:** Compile at runtime, optimize for actual execution

**Advantages:**
- Profile-guided optimization
- Specialize for input data
- Adaptive optimization

**Tiered compilation:**
1. Interpret initially (fast startup)
2. Compile hot functions (frequently executed)
3. Recompile with aggressive optimization

**Examples:** Java HotSpot, JavaScript V8, .NET CoreCLR

## Distributed Systems

**Challenge:** Coordinate multiple computers communicating via network.

**Difficulties:**
- **Partial failure:** Some nodes fail while others continue
- **Latency:** Network communication slow, variable
- **Asynchrony:** No global clock
- **Concurrency:** Many things happening simultaneously

### Communication

**Remote Procedure Call (RPC):**
- Make network call look like local function call
- Transparency: Hide network complexity
- Examples: gRPC, Apache Thrift

**Message Passing:**
- Explicit send/receive
- More control, less abstraction
- Examples: ZeroMQ, RabbitMQ

**REST (Representational State Transfer):**
- HTTP-based
- Stateless requests
- Standard methods: GET, POST, PUT, DELETE

### Consistency Models

**Strong consistency:** All nodes see same data at same time
- Easiest for programmers
- Performance cost (coordination)

**Eventual consistency:** All nodes converge to same state eventually
- High availability, performance
- Temporary inconsistencies

**CAP Theorem (Brewer 2000):**
- **Consistency:** All nodes see same data
- **Availability:** Every request gets response
- **Partition tolerance:** System works despite network partitions

**Can have at most 2 of 3.**

**In practice:** Network partitions happen (must tolerate)
→ Choose between consistency (CP) and availability (AP)

**Examples:**
- **CP:** Traditional databases (sacrifice availability during partition)
- **AP:** Amazon Dynamo, Cassandra (sacrifice consistency)

**PACELC Theorem:** Extension of CAP
- If Partition: Choose between Availability and Consistency
- Else (no partition): Choose between Latency and Consistency

### Consensus

**Problem:** Multiple nodes agree on value despite failures.

**Uses:**
- Leader election
- Distributed locking
- Configuration management

**Paxos (Lamport 1989):**
- Provably correct
- Complex to implement
- Single-value consensus

**Raft (Ongaro, Ousterhout 2014):**
- Easier to understand than Paxos
- Leader-based
- Multi-Paxos equivalent

**Two-Phase Commit (2PC):**
- Coordinator + participants
- Phase 1: Prepare (can you commit?)
- Phase 2: Commit/abort (all agree)
- **Problem:** Blocking (coordinator failure blocks all)

**Three-Phase Commit (3PC):**
- Non-blocking
- More complex

### Replication

**Why replicate:**
- Fault tolerance
- Performance (serve from nearest replica)
- Availability

**Single-leader replication:**
- One leader (write), many followers (read)
- Simple but leader is bottleneck/single point of failure

**Multi-leader replication:**
- Multiple leaders accept writes
- Must resolve conflicts

**Leaderless replication:**
- All nodes accept reads/writes
- Quorum: w + r > n (w writes, r reads, n nodes)

**Conflict resolution:**
- Last-write-wins (LWW): Use timestamp
- Version vectors: Track causality
- Application-specific: Let app resolve
- CRDTs: Data structures with commutative merges

### Partitioning (Sharding)

**Why partition:** Data too large for single machine

**Strategies:**

**Key-range partitioning:**
- A-M → partition 1, N-Z → partition 2
- Range queries efficient
- Problem: Hot spots (uneven load)

**Hash partitioning:**
- hash(key) mod n → partition
- Even distribution
- Problem: Range queries require all partitions

**Consistent hashing:**
- Nodes arranged on ring
- Add/remove nodes affects only neighbors
- Used by Dynamo, Cassandra

**Secondary indexes:**
- **Document-partitioned:** Each partition indexes own data (scatter/gather for queries)
- **Term-partitioned:** Global index partitioned by term

### Transactions

**ACID properties:**
- **Atomicity:** All or nothing
- **Consistency:** Invariants maintained
- **Isolation:** Concurrent transactions don't interfere
- **Durability:** Committed data survives crashes

**Isolation levels:**

**Read Uncommitted:** See uncommitted changes (dirty reads)
**Read Committed:** See only committed changes
**Repeatable Read:** Snapshot of database
**Serializable:** Equivalent to serial execution

**Implementation:**
- **Locks:** 2PL (two-phase locking)
- **MVCC (Multi-Version Concurrency Control):** Keep multiple versions
- **Optimistic concurrency:** Check for conflicts at commit

**Distributed transactions:**
- Harder: Need consensus
- 2PC common but blocking
- Often avoided (use eventual consistency, sagas)

## Summary

Systems architecture spans multiple abstraction layers:

**Hardware:**
- Von Neumann architecture: CPU, memory, I/O
- Memory hierarchy: Registers → cache → RAM → disk
- Pipelining, parallelism, branch prediction

**Operating Systems:**
- Process/thread management
- CPU scheduling (FCFS, SJF, RR, priority)
- Memory management (paging, segmentation, TLB)
- File systems (inodes, journaling)

**Compilers:**
- Lexing → parsing → semantic analysis → IR → optimization → code generation
- Optimizations: Constant folding, CSE, loop optimizations
- JIT compilation for dynamic languages

**Distributed Systems:**
- Communication (RPC, messages, REST)
- Consistency (CAP theorem, eventual consistency)
- Consensus (Paxos, Raft, 2PC)
- Replication, partitioning, transactions

Understanding systems architecture reveals:
- Why algorithm choice matters (cache-friendly code)
- How abstractions work (virtual memory, processes)
- What compilers optimize (enable compiler-friendly code)
- How to build scalable systems (replication, partitioning)

This knowledge bridges theoretical CS and practical engineering—enabling building efficient, reliable, scalable software.
