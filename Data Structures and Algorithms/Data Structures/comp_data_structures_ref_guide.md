# Comprehensive Data Structures Reference Guide

> **Legend**:  
> - Time complexities shown as **Average / Worst** where they differ  
> - `n` = number of elements, `k` = key length (for tries), `h` = height (for trees)

---

## Table of Contents

### [Part 1: Common Data Structures](#part-1-common-data-structures)

| Linear | Hash-Based | Trees | Graphs |
|--------|------------|-------|--------|
| [Array](#array-dynamic-array) | [Hash Table](#hash-table-hash-map) | [Binary Tree](#binary-tree) | [Adjacency Matrix](#adjacency-matrix) |
| [Linked List](#linked-list) | [Hash Set](#hash-set) | [Binary Search Tree](#binary-search-tree-bst) | [Adjacency List](#adjacency-list) |
| [Stack](#stack) | | [Heap](#heap-binary-heap) | |
| [Queue](#queue) | | | |

### [Part 2: Uncommon Data Structures](#part-2-uncommon-data-structures)

| Linear | Hash-Based | Trees | Specialized |
|--------|------------|-------|-------------|
| [Deque](#deque-double-ended-queue) | [Bloom Filter](#bloom-filter) | [AVL Tree](#avl-tree) | [Disjoint Set (Union-Find)](#disjoint-set-union-find) |
| [Circular Buffer](#circular-buffer-ring-buffer) | | [Red-Black Tree](#red-black-tree) | [LRU Cache](#lru-cache) |
| [Monotonic Stack](#monotonic-stack) | | [Trie](#trie-prefix-tree) | [Skip List](#skip-list) |
| [Monotonic Queue](#monotonic-queue) | | [Segment Tree](#segment-tree) | [Suffix Array / Tree](#suffix-array--suffix-tree) |
| | | [Fenwick Tree](#fenwick-tree-binary-indexed-tree) | |
| | | [B-Tree / B+ Tree](#b-tree--b-tree) | |

### [Part 3: Quick Reference](#part-3-quick-reference)
- [When to Use What](#when-to-use-what)
- [Time Complexity Cheat Sheet](#time-complexity-cheat-sheet)

---

# Part 1: Common Data Structures

These are the foundational structures you'll encounter most frequently in interviews and everyday programming.

---

## Linear Structures

---

### Array (Dynamic Array)

| Operation | Average | Worst |
|-----------|---------|-------|
| Access | `O(1)` | `O(1)` |
| Search | `O(n)` | `O(n)` |
| Insert (end) | `O(1)` | `O(n)`* |
| Insert (middle) | `O(n)` | `O(n)` |
| Delete (end) | `O(1)` | `O(1)` |
| Delete (middle) | `O(n)` | `O(n)` |

**Space Complexity**: `O(n)`

**Description**  
A contiguous block of memory storing elements of the same type, accessed via zero-based indices. Dynamic arrays (like Python's `list`) automatically resize when capacity is exceeded, which triggers an `O(n)` copy operation (amortized `O(1)` for append).

**Best Used When**
- Random access by index is frequent
- Elements are mostly added/removed from the end
- Memory locality matters for cache performance

**Language Implementations**  
- **Python**: `list`, `array.array` (typed)  
- **C#**: `List<T>`, `T[]`

[↑ Back to Table of Contents](#table-of-contents)

---

### Linked List

| Operation | Singly | Doubly |
|-----------|--------|--------|
| Access | `O(n)` | `O(n)` |
| Search | `O(n)` | `O(n)` |
| Insert (head) | `O(1)` | `O(1)` |
| Insert (tail)* | `O(n)` / `O(1)` | `O(1)` |
| Insert (middle) | `O(n)` | `O(n)` |
| Delete (head) | `O(1)` | `O(1)` |
| Delete (known node) | `O(n)` | `O(1)` |

*With tail pointer, singly linked list tail insertion is `O(1)`

**Space Complexity**: `O(n)` — Singly: +1 pointer/node, Doubly: +2 pointers/node

**Description**  
A sequence of nodes where each node contains data and pointer(s) to adjacent nodes. **Singly linked** lists have a `next` pointer only; **doubly linked** lists have both `next` and `prev` pointers.

**Best Used When**
- Frequent insertions/deletions at known positions
- No need for random access
- Implementing stacks, queues, or LRU caches

**Language Implementations**  
- **Python**: `collections.deque` (doubly-linked), custom implementation  
- **C#**: `LinkedList<T>`

[↑ Back to Table of Contents](#table-of-contents)

---

### Stack

| Operation | Time |
|-----------|------|
| Push | `O(1)` |
| Pop | `O(1)` |
| Peek/Top | `O(1)` |
| Search | `O(n)` |
| IsEmpty | `O(1)` |

**Space Complexity**: `O(n)`

**Description**  
A **LIFO** (Last In, First Out) data structure. Elements are added and removed from the same end (the "top"). Think of a stack of plates—you can only add or remove from the top.

**Best Used When**
- Tracking function calls (call stack)
- Undo/redo functionality
- Parsing expressions (balanced parentheses)
- DFS traversal (iterative)
- Backtracking algorithms

**Language Implementations**  
- **Python**: `list` (use `.append()` and `.pop()`), `collections.deque`  
- **C#**: `Stack<T>`

[↑ Back to Table of Contents](#table-of-contents)

---

### Queue

| Operation | Time |
|-----------|------|
| Enqueue | `O(1)` |
| Dequeue | `O(1)` |
| Peek/Front | `O(1)` |
| Search | `O(n)` |
| IsEmpty | `O(1)` |

**Space Complexity**: `O(n)`

**Description**  
A **FIFO** (First In, First Out) data structure. Elements are added at the rear (enqueue) and removed from the front (dequeue). Think of a line at a store—first person in line is served first.

**Best Used When**
- BFS traversal
- Task scheduling
- Buffer for data streams
- Print job management

**Language Implementations**  
- **Python**: `collections.deque` (use `.append()` and `.popleft()`)  
- **C#**: `Queue<T>`

[↑ Back to Table of Contents](#table-of-contents)

---

## Hash-Based Structures

---

### Hash Table (Hash Map)

| Operation | Average | Worst |
|-----------|---------|-------|
| Access | `O(1)` | `O(n)` |
| Search | `O(1)` | `O(n)` |
| Insert | `O(1)` | `O(n)` |
| Delete | `O(1)` | `O(n)` |

**Space Complexity**: `O(n)`

**Description**  
Stores key-value pairs using a hash function to compute indices. **Collisions** (different keys mapping to same index) are handled via chaining (linked lists) or open addressing (probing). Worst case `O(n)` occurs with poor hash functions causing many collisions.

**Key Concepts**
- **Load Factor**: ratio of elements to buckets; triggers resize when exceeded
- **Hash Function**: must be deterministic and distribute keys uniformly

**Best Used When**
- Fast lookups by key
- Counting frequencies
- Caching/memoization
- Deduplication

**Language Implementations**  
- **Python**: `dict`, `collections.defaultdict`, `collections.Counter`  
- **C#**: `Dictionary<K,V>`, `Hashtable`

[↑ Back to Table of Contents](#table-of-contents)

---

### Hash Set

| Operation | Average | Worst |
|-----------|---------|-------|
| Contains | `O(1)` | `O(n)` |
| Insert | `O(1)` | `O(n)` |
| Delete | `O(1)` | `O(n)` |

**Space Complexity**: `O(n)`

**Description**  
An unordered collection of unique elements using hash-based storage. Essentially a hash table that only stores keys (no values).

**Best Used When**
- Membership testing
- Removing duplicates
- Set operations (union, intersection, difference)

**Language Implementations**  
- **Python**: `set`, `frozenset` (immutable)  
- **C#**: `HashSet<T>`

[↑ Back to Table of Contents](#table-of-contents)

---

## Tree Structures

---

### Binary Tree

| Operation | Average | Worst |
|-----------|---------|-------|
| Access | `O(n)` | `O(n)` |
| Search | `O(n)` | `O(n)` |
| Insert | `O(n)` | `O(n)` |
| Delete | `O(n)` | `O(n)` |

**Space Complexity**: `O(n)`

**Description**  
A hierarchical structure where each node has at most two children (left and right). The topmost node is the **root**. Nodes with no children are **leaves**.

**Key Terminology**
- **Height**: longest path from root to leaf
- **Depth**: distance from root to a node
- **Complete**: all levels full except possibly last (filled left to right)
- **Perfect**: all internal nodes have 2 children, all leaves same level
- **Full**: every node has 0 or 2 children

**Traversals** (all `O(n)`)

| Traversal | Order | Common Use |
|-----------|-------|------------|
| Preorder | Root → Left → Right | Copy tree, prefix expression |
| Inorder | Left → Root → Right | Sorted order for BST |
| Postorder | Left → Right → Root | Delete tree, postfix expression |
| Level-order | BFS by level | Find min depth |

**Language Implementations**  
- **Python**: Custom implementation  
- **C#**: Custom implementation

[↑ Back to Table of Contents](#table-of-contents)

---

### Binary Search Tree (BST)

| Operation | Average | Worst* |
|-----------|---------|--------|
| Search | `O(log n)` | `O(n)` |
| Insert | `O(log n)` | `O(n)` |
| Delete | `O(log n)` | `O(n)` |
| Min/Max | `O(log n)` | `O(n)` |

*Worst case when tree becomes a linear chain (unbalanced)

**Space Complexity**: `O(n)`

**Description**  
A binary tree with the **BST property**: for every node, all values in its left subtree are smaller, and all values in its right subtree are larger. This ordering enables efficient binary search.

**Key Operations**
- **Successor**: next larger element (leftmost in right subtree, or first right ancestor)
- **Predecessor**: next smaller element (rightmost in left subtree)

**Best Used When**
- Ordered data with dynamic insertions/deletions
- Range queries
- Implementing ordered maps/sets

**Language Implementations**  
- **Python**: Custom implementation, `sortedcontainers.SortedDict`  
- **C#**: `SortedDictionary<K,V>` (typically Red-Black Tree internally)

[↑ Back to Table of Contents](#table-of-contents)

---

### Heap (Binary Heap)

| Operation | Time |
|-----------|------|
| Find Min/Max | `O(1)` |
| Insert | `O(log n)` |
| Extract Min/Max | `O(log n)` |
| Heapify | `O(n)` |
| Delete | `O(log n)` |

**Space Complexity**: `O(n)`

**Description**  
A **complete binary tree** satisfying the **heap property**:
- **Min-Heap**: parent ≤ children (root is minimum)
- **Max-Heap**: parent ≥ children (root is maximum)

Typically implemented as an array where for index `i`:
- Parent: `(i - 1) // 2`
- Left child: `2i + 1`
- Right child: `2i + 2`

**Key Operations**
- **Sift Up**: after insertion, bubble element up
- **Sift Down**: after extraction, bubble root down

**Best Used When**
- Priority queues
- Finding k largest/smallest elements
- Heap sort
- Graph algorithms (Dijkstra's, Prim's)
- Median maintenance (two heaps)

**Language Implementations**  
- **Python**: `heapq` (min-heap only; negate values for max-heap)  
- **C#**: `PriorityQueue<T, TPriority>` (.NET 6+)

[↑ Back to Table of Contents](#table-of-contents)

---

## Graph Structures

---

### Adjacency Matrix

| Operation | Time |
|-----------|------|
| Check Edge | `O(1)` |
| Add Edge | `O(1)` |
| Remove Edge | `O(1)` |
| Get Neighbors | `O(V)` |
| Add Vertex | `O(V²)` |

**Space Complexity**: `O(V²)`

**Description**  
A 2D matrix where `matrix[i][j]` indicates an edge from vertex `i` to `j`. Can store weights for weighted graphs. Undirected graphs have symmetric matrices.

**Best Used When**
- Dense graphs (E ≈ V²)
- Quick edge existence checks
- Small graphs
- Floyd-Warshall algorithm

**Language Implementations**  
- **Python**: `list` of `list`, `numpy` array  
- **C#**: `int[,]` or `bool[,]`

[↑ Back to Table of Contents](#table-of-contents)

---

### Adjacency List

| Operation | Time |
|-----------|------|
| Check Edge | `O(degree)` |
| Add Edge | `O(1)` |
| Remove Edge | `O(degree)` |
| Get Neighbors | `O(1)` |
| Add Vertex | `O(1)` |

**Space Complexity**: `O(V + E)`

**Description**  
Each vertex stores a list of its adjacent vertices. More space-efficient for sparse graphs. Can be implemented with array of lists or hash map.

**Best Used When**
- Sparse graphs (E << V²)
- Most graph algorithms (BFS, DFS, Dijkstra)
- Memory efficiency matters

**Language Implementations**  
- **Python**: `dict` of `list` or `set`, `defaultdict(list)`  
- **C#**: `Dictionary<T, List<T>>`

[↑ Back to Table of Contents](#table-of-contents)

---

# Part 2: Uncommon Data Structures

These are more specialized structures you'll encounter in advanced problems, competitive programming, or specific domains.

---

## Linear Structures

---

### Deque (Double-Ended Queue)

| Operation | Time |
|-----------|------|
| Insert Front | `O(1)` |
| Insert Rear | `O(1)` |
| Delete Front | `O(1)` |
| Delete Rear | `O(1)` |
| Peek Front/Rear | `O(1)` |
| Access by Index | `O(n)` |

**Space Complexity**: `O(n)`

**Description**  
A generalized queue that supports insertion and deletion at both ends. Can function as both a stack and a queue.

**Best Used When**
- Sliding window problems
- Implementing work-stealing algorithms
- Palindrome checking
- Browser history (back/forward)

**Language Implementations**  
- **Python**: `collections.deque`  
- **C#**: Custom implementation or `LinkedList<T>`

[↑ Back to Table of Contents](#table-of-contents)

---

### Circular Buffer (Ring Buffer)

| Operation | Time |
|-----------|------|
| Insert | `O(1)` |
| Delete | `O(1)` |
| Access | `O(1)` |
| Search | `O(n)` |

**Space Complexity**: `O(k)` where k = fixed buffer size

**Description**  
A fixed-size buffer that wraps around using modular arithmetic. When full, new elements overwrite the oldest. Uses two pointers (head and tail) that wrap around.

**Best Used When**
- Streaming data with fixed memory
- Audio/video buffering
- Producer-consumer scenarios
- Recent history logging

**Language Implementations**  
- **Python**: `collections.deque(maxlen=k)`  
- **C#**: Custom implementation

[↑ Back to Table of Contents](#table-of-contents)

---

### Monotonic Stack

| Operation | Time |
|-----------|------|
| Push | `O(1)` amortized |
| Pop | `O(1)` |

**Space Complexity**: `O(n)`

**Description**  
A stack that maintains elements in sorted (monotonic) order. Elements are popped before pushing a new element that would violate the ordering.

**Example Implementation**
```python
def next_greater_element(nums):
    result = [-1] * len(nums)
    stack = []  # stores indices
    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] < num:
            result[stack.pop()] = num
        stack.append(i)
    return result
```

**Best Used When**
- Next greater/smaller element
- Largest rectangle in histogram
- Trapping rain water
- Stock span problems

[↑ Back to Table of Contents](#table-of-contents)

---

### Monotonic Queue

| Operation | Time |
|-----------|------|
| Push | `O(1)` amortized |
| Pop | `O(1)` |
| Get Min/Max | `O(1)` |

**Space Complexity**: `O(k)` for window size k

**Description**  
A deque maintaining elements in monotonic order, supporting efficient sliding window min/max queries.

**Best Used When**
- Sliding window maximum/minimum
- Constrained subsequence problems

[↑ Back to Table of Contents](#table-of-contents)

---

## Hash-Based Structures

---

### Bloom Filter

| Operation | Time |
|-----------|------|
| Insert | `O(k)` |
| Query | `O(k)` |
| Delete | ❌ Not supported |

*k = number of hash functions*

**Space Complexity**: `O(m)` where m = bit array size (much smaller than storing elements)

**Description**  
A probabilistic data structure for membership testing. Uses multiple hash functions mapping to a bit array.

**Key Property**  
- ✅ **No false negatives**: if it says element doesn't exist, it definitely doesn't
- ⚠️ **False positives possible**: may say element exists when it doesn't

**Best Used When**
- Approximate membership testing at scale
- Reducing expensive lookups (check bloom filter first)
- Spell checkers, web crawlers, database queries
- Network routers, CDN caching

**Language Implementations**  
- **Python**: `pybloom-live`, `mmh3` + custom  
- **C#**: Custom implementation

[↑ Back to Table of Contents](#table-of-contents)

---

## Tree Structures

---

### AVL Tree

| Operation | Time |
|-----------|------|
| Search | `O(log n)` |
| Insert | `O(log n)` |
| Delete | `O(log n)` |

**Space Complexity**: `O(n)`

**Description**  
A **self-balancing BST** where the heights of left and right subtrees differ by at most 1 (balance factor ∈ {-1, 0, 1}). Uses **rotations** to maintain balance after insertions/deletions.

**Rotations**

| Case | Rotation |
|------|----------|
| Right subtree too tall | Left Rotation |
| Left subtree too tall | Right Rotation |
| Left child is right-heavy | Left-Right |
| Right child is left-heavy | Right-Left |

**vs Red-Black Trees**: AVL is more strictly balanced → faster lookups but slower insertions/deletions due to more rotations.

**Best Used When**
- Lookup-heavy workloads
- Database indexing

[↑ Back to Table of Contents](#table-of-contents)

---

### Red-Black Tree

| Operation | Time |
|-----------|------|
| Search | `O(log n)` |
| Insert | `O(log n)` |
| Delete | `O(log n)` |

**Space Complexity**: `O(n)`

**Description**  
A self-balancing BST with nodes colored red or black following specific rules:
1. Root is black
2. Red nodes cannot have red children
3. All paths from root to null have same number of black nodes

**vs AVL**: Less strictly balanced (height ≤ 2 log n vs 1.44 log n) → fewer rotations on insert/delete but slightly slower lookups.

**Best Used When**
- Write-heavy workloads
- Standard library implementations (`std::map`, `TreeMap`)

**Language Implementations**  
- **Python**: Custom implementation  
- **C#**: `SortedSet<T>`, `SortedDictionary<K,V>` (internal)

[↑ Back to Table of Contents](#table-of-contents)

---

### Trie (Prefix Tree)

| Operation | Time |
|-----------|------|
| Insert | `O(k)` |
| Search | `O(k)` |
| Delete | `O(k)` |
| Prefix Search | `O(k)` |

*k = length of key/word*

**Space Complexity**: `O(n × k × alphabet_size)` worst case

**Description**  
A tree structure for storing strings where each node represents a character. Paths from root to nodes represent prefixes. Each node may have up to `alphabet_size` children.

**Optimization**: **Compressed Trie** (Radix Tree) combines chains of single-child nodes.

**Best Used When**
- Autocomplete/typeahead
- Spell checking
- IP routing (longest prefix match)
- Word games (Boggle, Scrabble)

**Language Implementations**  
- **Python**: Custom implementation, `pygtrie`  
- **C#**: Custom implementation

[↑ Back to Table of Contents](#table-of-contents)

---

### Segment Tree

| Operation | Time |
|-----------|------|
| Build | `O(n)` |
| Query (range) | `O(log n)` |
| Update (point) | `O(log n)` |
| Update (range)* | `O(log n)` |

*With lazy propagation

**Space Complexity**: `O(n)` — typically `4n` array

**Description**  
A binary tree for efficient range queries (sum, min, max, GCD) and updates on arrays. Each node stores aggregate information about a range; leaves represent individual elements.

**Key Concepts**
- **Lazy Propagation**: defer range updates for efficiency
- Each node covers range `[l, r]`, children cover `[l, mid]` and `[mid+1, r]`

**Best Used When**
- Range sum/min/max queries with updates
- Competitive programming
- Computational geometry

**Language Implementations**  
- **Python**: Custom implementation  
- **C#**: Custom implementation

[↑ Back to Table of Contents](#table-of-contents)

---

### Fenwick Tree (Binary Indexed Tree)

| Operation | Time |
|-----------|------|
| Build | `O(n)` |
| Prefix Sum | `O(log n)` |
| Point Update | `O(log n)` |
| Range Sum | `O(log n)` |

**Space Complexity**: `O(n)`

**Description**  
A compact data structure for cumulative frequency tables. Uses clever bit manipulation (lowest set bit) to traverse tree implicitly stored in array. Simpler and lower constant factor than segment trees but less versatile.

**Key Operations**
- Update index `i`: traverse indices `i += i & (-i)`
- Query prefix sum to `i`: traverse indices `i -= i & (-i)`

**Best Used When**
- Prefix sums with updates
- Counting inversions
- Range sum queries (simpler than segment tree)

**Language Implementations**  
- **Python**: Custom implementation  
- **C#**: Custom implementation

[↑ Back to Table of Contents](#table-of-contents)

---

### B-Tree / B+ Tree

| Operation | Time |
|-----------|------|
| Search | `O(log n)` |
| Insert | `O(log n)` |
| Delete | `O(log n)` |

**Space Complexity**: `O(n)`

**Description**  
Self-balancing trees optimized for systems that read/write large blocks of data. Nodes can have many children (order `m`), keeping tree shallow. **B+ Trees** store all data in leaves with leaves linked for range scans.

**Key Properties** (order m)
- Each node has at most `m` children
- Non-leaf nodes have at least `⌈m/2⌉` children
- All leaves at same depth

**Best Used When**
- Database indexing
- File systems
- Disk-based storage

[↑ Back to Table of Contents](#table-of-contents)

---

## Specialized Structures

---

### Disjoint Set (Union-Find)

| Operation | Time* |
|-----------|-------|
| Find | `O(α(n))` ≈ `O(1)` |
| Union | `O(α(n))` ≈ `O(1)` |
| Connected | `O(α(n))` ≈ `O(1)` |

*With path compression and union by rank; α = inverse Ackermann function

**Space Complexity**: `O(n)`

**Description**  
Tracks elements partitioned into disjoint (non-overlapping) sets. Supports efficient union of sets and finding which set an element belongs to.

**Optimizations**
- **Path Compression**: flatten tree during find
- **Union by Rank/Size**: attach smaller tree under larger

**Reference Implementation**
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
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]: px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]: self.rank[px] += 1
        return True
```

**Best Used When**
- Kruskal's MST algorithm
- Detecting cycles in undirected graphs
- Connected components
- Network connectivity
- Percolation problems

[↑ Back to Table of Contents](#table-of-contents)

---

### LRU Cache

| Operation | Time |
|-----------|------|
| Get | `O(1)` |
| Put | `O(1)` |

**Space Complexity**: `O(capacity)`

**Description**  
A cache with fixed capacity that evicts the **Least Recently Used** item when full. Implemented using a **hash map** (for O(1) access) combined with a **doubly linked list** (for O(1) reordering).

**Reference Implementation**
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key: int) -> int:
        if key not in self.cache: return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

**Best Used When**
- Caching with memory limits
- Database query caching
- Web browser history
- Operating system page replacement

**Language Implementations**  
- **Python**: `functools.lru_cache`, `collections.OrderedDict`  
- **C#**: Custom implementation, `MemoryCache`

[↑ Back to Table of Contents](#table-of-contents)

---

### Skip List

| Operation | Average | Worst |
|-----------|---------|-------|
| Search | `O(log n)` | `O(n)` |
| Insert | `O(log n)` | `O(n)` |
| Delete | `O(log n)` | `O(n)` |

**Space Complexity**: `O(n)` average, `O(n log n)` worst

**Description**  
A probabilistic data structure with multiple layers of linked lists. Bottom layer contains all elements; each higher layer acts as "express lane" with ~50% of elements from layer below. Achieves BST-like performance with simpler implementation.

**Best Used When**
- Alternative to balanced BSTs
- Concurrent data structures (easier to lock)
- Redis sorted sets

**Language Implementations**  
- **Python**: Custom implementation  
- **C#**: Custom implementation

[↑ Back to Table of Contents](#table-of-contents)

---

### Suffix Array / Suffix Tree

**Suffix Array**

| Operation | Time |
|-----------|------|
| Build | `O(n log n)` |
| Pattern Search | `O(m log n)` |

**Space**: `O(n)`

**Suffix Tree**

| Operation | Time |
|-----------|------|
| Build | `O(n)` |
| Pattern Search | `O(m)` |

**Space**: `O(n)` but large constant factor

*m = pattern length*

**Description**  
Structures for efficient string operations. **Suffix Array** is a sorted array of all suffixes' starting indices. **Suffix Tree** is a compressed trie of all suffixes.

**Best Used When**
- Pattern matching in large texts
- Finding repeated substrings
- Bioinformatics (DNA sequence analysis)
- Longest common substring

[↑ Back to Table of Contents](#table-of-contents)

---

# Part 3: Quick Reference

---

## When to Use What

| Need | Data Structure |
|------|----------------|
| Fast access by index | Array |
| Fast insert/delete at ends | Deque, Linked List |
| LIFO operations | Stack |
| FIFO operations | Queue |
| Fast lookup by key | Hash Table |
| Unique elements | Hash Set |
| Ordered data + fast search | BST, AVL, Red-Black |
| Priority/ordering | Heap |
| Prefix matching | Trie |
| Range queries | Segment Tree, Fenwick Tree |
| Disjoint sets/connectivity | Union-Find |
| Caching with eviction | LRU Cache |
| Probabilistic membership | Bloom Filter |
| Graph (dense) | Adjacency Matrix |
| Graph (sparse) | Adjacency List |
| Next greater element | Monotonic Stack |
| Sliding window min/max | Monotonic Deque |

[↑ Back to Table of Contents](#table-of-contents)

---

## Time Complexity Cheat Sheet

### Common Structures

| Structure | Access | Search | Insert | Delete |
|-----------|--------|--------|--------|--------|
| Array | O(1) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1)* | O(1)* |
| Stack | O(n) | O(n) | O(1) | O(1) |
| Queue | O(n) | O(n) | O(1) | O(1) |
| Hash Table | — | O(1) | O(1) | O(1) |
| BST (balanced) | — | O(log n) | O(log n) | O(log n) |
| Heap | — | O(n) | O(log n) | O(log n) |

*At known position

### Uncommon Structures

| Structure | Key Operation | Time |
|-----------|---------------|------|
| Trie | Search/Insert | O(k) |
| Segment Tree | Range Query | O(log n) |
| Fenwick Tree | Prefix Sum | O(log n) |
| Union-Find | Find/Union | O(α(n)) ≈ O(1) |
| LRU Cache | Get/Put | O(1) |
| Bloom Filter | Insert/Query | O(k) |
| Skip List | Search | O(log n) avg |

[↑ Back to Table of Contents](#table-of-contents)
