# Time & Space Complexity: A Complete Study Guide

> *"Complexity analysis is the art of predicting how algorithms behave as problems grow."*

---

## Table of Contents

1. [The Big Picture](#the-big-picture)
2. [Defining Your Variables](#defining-your-variables)
3. [Time Complexity Deep Dive](#time-complexity-deep-dive)
4. [Space Complexity: Stack vs Heap](#space-complexity-stack-vs-heap)
5. [The Complexity Hierarchy](#the-complexity-hierarchy)
6. [Comparing Algorithms: The Tradeoff Matrix](#comparing-algorithms-the-tradeoff-matrix)
7. [Choosing the Right Tool](#choosing-the-right-tool)
8. [Edge Cases & Gotchas](#edge-cases--gotchas)
9. [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)

---

## The Big Picture

### Why We Analyze Complexity

Complexity analysis answers one question: **How does this algorithm scale?**

Think of it like predicting traffic. If a road handles 100 cars fine, will it handle 10,000? Will it gridlock at 1 million? Complexity tells us when our algorithm will "gridlock."

### The Golden Rule: Ignore Output

Every algorithm solving the same problem produces the same output. If you're finding all permutations of `n` items, every correct solution outputs `n!` permutations.

**Output doesn't differentiate algorithms—process does.**

```python
# Both produce the same output, but HOW they get there differs
def find_max_brute(arr):      # O(n²) - compares every pair
def find_max_optimal(arr):    # O(n) - single pass
```

When analyzing, focus on the **work done**, not the result produced.

### What Counts Against Space Complexity?

| Counts ✓ | Doesn't Count ✗ |
|----------|-----------------|
| New data structures you create | The input itself |
| Recursive call stack depth | Variables that don't scale with input |
| Temporary storage that grows with input | Constant-size variables |

**Example:**
```python
def process(arr):           # arr is INPUT - doesn't count
    n = len(arr)            # O(1) - constant, doesn't scale
    result = []             # O(n) at worst - THIS counts
    temp = [0] * n          # O(n) - THIS counts
    i = 0                   # O(1) - constant
    return result
```

---

## Defining Your Variables

### The Art of Naming Complexity Components

When you write `O(n)`, what is `n`? Interviewers want to see that you understand **what drives complexity**.

**Always define your variables explicitly:**

```python
# "n is the number of nodes, m is the number of edges"
def traverse_graph(nodes, edges):  # O(n + m) time
```

### Common Variable Conventions

| Variable | Typical Meaning |
|----------|-----------------|
| `n` | Primary input size (array length, number of nodes) |
| `m` | Secondary dimension (edges in graph, columns in matrix) |
| `k` | A constraint or parameter (top-k elements, window size) |
| `h` | Height (of tree, recursion depth) |
| `d` | Depth or degree |

### Breaking Down Composite Complexity

**Don't simplify prematurely.** Show your understanding first.

```python
def find_top_k(arr, k):
    # Step 1: Build min-heap of size k    → O(k)
    # Step 2: Process remaining n-k items → O((n-k) log k)
    # Total: O(k + (n-k) log k) = O(n log k)
    pass
```

**Bad answer:** "It's O(n log k)"  
**Good answer:** "Building the initial heap is O(k), then we process n-k elements, each taking O(log k) for heap operations. Combined: O(k + (n-k) log k), which simplifies to O(n log k) when n >> k."

### When Variables Combine vs. Simplify

| Expression | Simplifies To | When |
|------------|---------------|------|
| `O(n + n)` | `O(n)` | Same variable, add constants |
| `O(n + m)` | `O(n + m)` | Different variables, keep both |
| `O(n + k)` where `k ≤ n` | `O(n)` | If k is bounded by n |
| `O(n * m)` | `O(n * m)` | Multiplication stays |

---

## Time Complexity Deep Dive

### The Complexity Hierarchy (Slowest to Fastest)

```
SLOWER ←――――――――――――――――――――――――――――――――――――――→ FASTER

O(n!)    O(2ⁿ)    O(n²)    O(n log n)    O(n)    O(log n)    O(1)
 ↑         ↑        ↑          ↑           ↑         ↑         ↑
Factorial Expon.  Quadratic Linearithmic Linear  Logarithmic Constant
```

### Detailed Breakdown

#### O(1) — Constant Time
*"The same work regardless of input size"*

```python
def get_first(arr):
    return arr[0]           # Always one operation

def hash_lookup(dict, key):
    return dict[key]        # Hash tables: O(1) average
```

**Real-world analogy:** Looking up a contact by name in your phone.

---

#### O(log n) — Logarithmic Time
*"Halving the problem each step"*

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1      # Eliminate half
        else:
            right = mid - 1     # Eliminate half
    return -1
```

**Why logarithmic?** Each step eliminates half the remaining elements.
- n=1000 → ~10 steps
- n=1,000,000 → ~20 steps
- n=1,000,000,000 → ~30 steps

**Real-world analogy:** Finding a word in a dictionary by opening to the middle.

---

#### O(n) — Linear Time
*"Touch each element once"*

```python
def find_max(arr):
    max_val = arr[0]
    for num in arr:         # One pass through n elements
        max_val = max(max_val, num)
    return max_val
```

**Real-world analogy:** Reading every page of a book once.

---

#### O(n log n) — Linearithmic Time
*"Do log n work for each of n elements"*

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])    # log n levels
    right = merge_sort(arr[mid:])   # log n levels
    return merge(left, right)        # O(n) merge at each level
```

**Why n log n?** The recursion tree has `log n` levels, and each level does `O(n)` total work.

**Real-world analogy:** Organizing a tournament bracket.

---

#### O(n²) — Quadratic Time
*"Compare every element with every other element"*

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):              # n iterations
        for j in range(n - 1):      # n iterations each
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
```

**Pattern recognition:** Nested loops over the same data usually means O(n²).

**Real-world analogy:** In a room of n people, everyone shakes hands with everyone else.

---

#### O(2ⁿ) — Exponential Time
*"Double the work with each additional input"*

```python
def fibonacci_naive(n):
    if n <= 1:
        return n
    return fibonacci_naive(n-1) + fibonacci_naive(n-2)  # Two branches each call
```

**Growth rate:**
- n=10 → ~1,000 operations
- n=20 → ~1,000,000 operations
- n=30 → ~1,000,000,000 operations

**Real-world analogy:** The "grain of rice on a chessboard" story.

---

#### O(n!) — Factorial Time
*"Generate all possible arrangements"*

```python
def permutations(arr):
    if len(arr) <= 1:
        return [arr]
    result = []
    for i in range(len(arr)):
        rest = arr[:i] + arr[i+1:]
        for p in permutations(rest):  # (n-1)! recursive calls
            result.append([arr[i]] + p)
    return result
```

**Growth rate:**
- n=5 → 120 permutations
- n=10 → 3,628,800 permutations
- n=15 → 1,307,674,368,000 permutations

**Real-world analogy:** Arranging n books on a shelf in every possible order.

---

## Space Complexity: Stack vs Heap

### The Two Memory Arenas

Understanding WHERE memory is used is crucial for accurate analysis.

```
┌─────────────────────────────────────┐
│            HEAP MEMORY              │
│  (Data structures, objects, arrays) │
│  - Persists until explicitly freed  │
│  - Shared across function calls     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│            STACK MEMORY             │
│  (Function calls, local variables)  │
│  - Automatic cleanup on return      │
│  - One frame per active call        │
└─────────────────────────────────────┘
```

### Analyzing Both Components

**Template for space analysis:**
```
Total Space = Stack Space + Heap Space (Auxiliary)
```

### Example: Backtracking with BFS Queue

```python
def solve_maze(maze):
    n = len(maze)
    
    # HEAP: Queue for BFS - worst case holds O(n²) cells
    queue = deque([(0, 0)])
    
    # HEAP: Visited set - worst case O(n²) cells
    visited = set()
    
    def backtrack(path):
        # STACK: Each recursive call stores:
        #   - path reference (pointer, O(1))
        #   - local variables
        #   - return address
        # Max depth: O(n²) in worst case
        
        if is_solution(path):
            return path
        for next_move in get_moves(path[-1]):
            path.append(next_move)
            result = backtrack(path)  # Recursive call adds to stack
            path.pop()
        return None
```

**Space Breakdown:**
| Component | Location | Complexity | Notes |
|-----------|----------|------------|-------|
| `queue` | Heap | O(n²) | BFS frontier |
| `visited` | Heap | O(n²) | Tracking visited cells |
| Recursion | Stack | O(n²) | Max path length |
| **Total** | | **O(n²)** | Dominated by largest term |

### Stack vs Heap: Key Differences

| Aspect | Stack | Heap |
|--------|-------|------|
| **Allocation** | Automatic (function entry) | Manual (`new`, `[]`, `{}`) |
| **Deallocation** | Automatic (function return) | Garbage collected / manual |
| **Growth** | Recursion depth | Data structure size |
| **Limit** | Often ~1MB default | Limited by system RAM |
| **Access** | Fast (LIFO) | Slower (random) |

### Common Patterns

```python
# Pattern 1: Iteration (Stack: O(1), Heap: depends on data)
def iterative_sum(arr):
    total = 0                   # Stack: O(1)
    for num in arr:
        total += num
    return total

# Pattern 2: Recursion (Stack: O(n), Heap: O(1))
def recursive_sum(arr, i=0):
    if i == len(arr):
        return 0
    return arr[i] + recursive_sum(arr, i + 1)  # Stack grows to O(n)

# Pattern 3: Recursion + Data Structure (Stack: O(n), Heap: O(n))
def build_tree(arr, i=0):
    if i >= len(arr):
        return None
    node = TreeNode(arr[i])     # Heap: O(n) nodes total
    node.left = build_tree(arr, 2*i + 1)   # Stack: O(log n) for balanced
    node.right = build_tree(arr, 2*i + 2)
    return node
```

---

## Comparing Algorithms: The Tradeoff Matrix

### The Three-Dimensional Evaluation

When comparing algorithms, consider:

1. **Time Complexity** — How fast does it run?
2. **Space Complexity** — How much memory does it use?
3. **Implementation Difficulty** — How hard is it to code correctly?

### Difficulty Scale (1-5)

| Score | Description | Characteristics |
|-------|-------------|-----------------|
| 1 | Trivial | Single loop, basic operations |
| 2 | Easy | Familiar patterns, few edge cases |
| 3 | Moderate | Multiple components, careful indexing |
| 4 | Hard | Complex logic, many edge cases |
| 5 | Expert | Intricate algorithms, easy to get wrong |

### Example: Finding Duplicates

| Algorithm | Time | Space | Difficulty | Best When |
|-----------|------|-------|------------|-----------|
| Brute Force (nested loops) | O(n²) | O(1) | 1 | n < 100, memory critical |
| Sort First | O(n log n) | O(1)* | 2 | Can modify input |
| Hash Set | O(n) | O(n) | 2 | Speed matters most |
| Bit Manipulation | O(n) | O(1) | 4 | Fixed range, memory critical |

*\*O(log n) stack space for recursive sort implementations*

### Example: Shortest Path

| Algorithm | Time | Space | Difficulty | Best When |
|-----------|------|-------|------------|-----------|
| BFS (unweighted) | O(V + E) | O(V) | 2 | Unweighted graphs |
| Dijkstra | O((V + E) log V) | O(V) | 3 | Positive weights |
| Bellman-Ford | O(V × E) | O(V) | 3 | Negative weights |
| Floyd-Warshall | O(V³) | O(V²) | 2 | All pairs, dense graphs |

### Example: String Matching

| Algorithm | Time | Space | Difficulty | Best When |
|-----------|------|-------|------------|-----------|
| Brute Force | O(n × m) | O(1) | 1 | Short patterns |
| KMP | O(n + m) | O(m) | 4 | Long text, repeated search |
| Rabin-Karp | O(n + m) avg | O(1) | 3 | Multiple pattern matching |
| Trie-based | O(n × L) build | O(Σ × L × n) | 3 | Prefix matching, autocomplete |

---

## Choosing the Right Tool

### Data Structure Selection Guide

| Problem Type | Best Structure | Why | Avoid |
|--------------|---------------|-----|-------|
| **Autocomplete / Prefix search** | Trie | O(L) lookup for length-L prefix | Hash table (no prefix support) |
| **Priority scheduling** | Heap | O(log n) insert/extract-min | Sorted array (O(n) insert) |
| **Range queries** | Segment Tree | O(log n) query and update | Array (O(n) range sum) |
| **Undo/Redo functionality** | Stack | O(1) push/pop, LIFO order | Queue (wrong order) |
| **LRU Cache** | HashMap + DLL | O(1) access and eviction | Array (O(n) eviction) |
| **Union-Find / Connectivity** | Disjoint Set | Near O(1) union/find | DFS (O(V+E) per query) |

### Algorithm Selection by Problem Pattern

| Pattern | Algorithm Choice | Time | When to Use |
|---------|------------------|------|-------------|
| **"Find all subsets"** | Backtracking | O(2ⁿ) | Explore all combinations |
| **"Shortest path"** | BFS / Dijkstra | O(V+E) | Unweighted / weighted |
| **"Maximum/minimum something"** | Dynamic Programming | Varies | Overlapping subproblems |
| **"Top K elements"** | Heap | O(n log k) | When k << n |
| **"Find in sorted"** | Binary Search | O(log n) | Sorted data, find target |
| **"Sliding window"** | Two Pointers | O(n) | Contiguous subarrays |

### Production Considerations

| Scenario | Prioritize | Accept Tradeoff |
|----------|------------|-----------------|
| Real-time systems | Low latency (time) | Higher memory |
| Embedded devices | Low memory (space) | Slower speed |
| One-time scripts | Simplicity (difficulty) | Suboptimal complexity |
| High-traffic APIs | Throughput | Development time |
| Data pipelines | Correctness | Some inefficiency |

### When NOT to Use

| Structure | Avoid When |
|-----------|-----------|
| **Trie** | Memory constrained, non-string data, no prefix queries |
| **Graph** | Data is naturally sequential, relationships are 1:1 |
| **Heap** | Need arbitrary access, sorted traversal required |
| **Hash Table** | Need ordered iteration, range queries |
| **Balanced BST** | Simple lookups suffice, memory critical |

---

## Edge Cases & Gotchas

### Common Mistakes in Analysis

#### 1. Forgetting Hidden Loops
```python
def has_duplicate(arr):
    return len(arr) != len(set(arr))  # set() is O(n)!
```
This is O(n), not O(1). Building the set iterates through all elements.

#### 2. String Concatenation Trap
```python
def build_string(n):
    s = ""
    for i in range(n):
        s += str(i)    # Creates new string each time!
    return s
```
This is **O(n²)**, not O(n)! Each concatenation copies the entire string.

**Fix:** Use `"".join(list)` for O(n).

#### 3. Slice Copies
```python
def process(arr):
    return helper(arr[1:])  # arr[1:] creates a copy! O(n)
```
Pass indices instead when possible.

#### 4. Amortized vs Worst Case
```python
arr = []
for i in range(n):
    arr.append(i)  # O(1) amortized, but O(n) worst case (resize)
```

### Constants That Actually Matter

While we ignore constants in Big-O, they matter in practice:

```python
# Both O(n), but very different real performance
def sum_1(arr):  # ~1n operations
    return sum(arr)

def sum_2(arr):  # ~100n operations
    total = 0
    for x in arr:
        for _ in range(100):
            total += x / 100
    return total
```

### Best, Average, Worst Cases

| Algorithm | Best | Average | Worst |
|-----------|------|---------|-------|
| Quick Sort | O(n log n) | O(n log n) | O(n²) |
| Hash Table Lookup | O(1) | O(1) | O(n) |
| Binary Search | O(1) | O(log n) | O(log n) |
| Insertion Sort | O(n) | O(n²) | O(n²) |

**When to specify:** Always mention if worst case differs significantly from average.

### The Recursion Stack Trap

```python
def countdown(n):
    if n == 0:
        return
    countdown(n - 1)  # Stack depth: O(n)
```

Even with O(1) work per call, space is O(n) due to the call stack.

**Python default recursion limit: ~1000.** Deep recursion needs iteration or `sys.setrecursionlimit()`.

---

## Quick Reference Cheat Sheet

### Complexity at a Glance

```
Time Complexity Comparison (n = 1,000,000):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
O(1)        →  1 operation
O(log n)    →  20 operations
O(n)        →  1,000,000 operations
O(n log n)  →  20,000,000 operations
O(n²)       →  1,000,000,000,000 operations
O(2ⁿ)       →  ∞ (universe ends first)
```

### Data Structure Operations

| Structure | Access | Search | Insert | Delete |
|-----------|--------|--------|--------|--------|
| Array | O(1) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1)* | O(1)* |
| Hash Table | N/A | O(1) | O(1) | O(1) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) |
| Heap | N/A | O(n) | O(log n) | O(log n) |

*\*At known position*

### Sorting Algorithm Summary

| Algorithm | Time (Best) | Time (Worst) | Space | Stable |
|-----------|-------------|--------------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(1) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n) | Yes |
| Quick Sort | O(n log n) | O(n²) | O(log n) | No |
| Heap Sort | O(n log n) | O(n log n) | O(1) | No |
| Counting Sort | O(n + k) | O(n + k) | O(k) | Yes |

### Interview Response Template

> "Let me break down the complexity:
> 
> **Defining variables:** Let `n` be [primary input], and `k` be [secondary constraint].
> 
> **Time Analysis:**
> - Step 1: [operation] takes O(...)
> - Step 2: [operation] takes O(...)
> - Total: O(...) because [reason]
> 
> **Space Analysis:**
> - Stack: O(...) from [recursion depth / call stack]
> - Heap: O(...) from [data structures]
> - Total auxiliary space: O(...)
> 
> **Tradeoffs:** This approach prioritizes [time/space] at the cost of [the other]. An alternative would be [other approach] which trades [X for Y]."

---

## Final Thoughts

### The Complexity Mindset

1. **Start with the question:** What is the input? What grows?
2. **Define your variables:** Be explicit about what n, m, k represent
3. **Break it down:** Analyze each component separately
4. **Combine carefully:** Know when variables add vs. multiply
5. **Consider both dimensions:** Time AND space, stack AND heap
6. **Know the tradeoffs:** There's rarely a universally "best" solution

### Remember

- **Output doesn't differentiate algorithms** — focus on the process
- **Input doesn't count against space** — only what YOU create
- **Constants don't matter in Big-O** — but they matter in practice
- **Showing your work matters** — O(n + k) before simplifying shows understanding
- **Context determines the best choice** — consider time, space, AND implementation difficulty

---

*Good luck with your interviews! Understanding complexity deeply will set you apart.*
