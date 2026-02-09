# DSA Anki Deck — Master Build Plan

## Overview
- **Target**: 525+ cards across 10 topic batches
- **Format**: Tab-separated text files with Anki file headers, importable directly
- **Card Type**: Basic (Front / Back)
- **Code**: HTML-formatted `<pre><code>` blocks where applicable
- **Difficulty Distribution**: ~60% fundamentals/easy, ~40% medium-hard concepts
- **Weak Area Weighting**: Recursion & Backtracking gets extra depth

---

## Batch Breakdown

| Batch | Topic | Cards | Difficulty Split |
|-------|-------|-------|-----------------|
| 1 | Arrays & Strings | ~65 | 60/40 |
| 2 | Linked Lists (Singly & Doubly) | ~55 | 60/40 |
| 3 | Stacks & Queues | ~40 | 60/40 |
| 4 | Binary Trees & BST | ~70 | 55/45 |
| 5 | Heaps & Priority Queues | ~30 | 60/40 |
| 6 | Tries & Advanced Trees | ~25 | 50/50 |
| 7 | Graphs & Matrices | ~55 | 50/50 |
| 8 | Recursion & Backtracking | ~70 | 40/60 |
| 9 | Sorting Algorithms | ~50 | 60/40 |
| 10 | DP, Complexity & General Patterns | ~65 | 50/50 |
| **Total** | | **~525** | | |

---

## Batch 1: Arrays & Strings (~65 cards)

### Fundamentals (15 cards)
1. What is an array and how is it stored in memory?
2. Time complexity: access by index
3. Time complexity: search (unsorted)
4. Time complexity: search (sorted — binary search)
5. Time complexity: insert at end (dynamic array)
6. Time complexity: insert at beginning
7. Time complexity: insert at middle
8. Time complexity: delete at end
9. Time complexity: delete at beginning
10. Difference between static and dynamic arrays
11. What is amortized O(1) for dynamic array append?
12. What is a string in Python (immutable sequence)?
13. Time complexity of string concatenation in a loop
14. StringBuilder equivalent in Python
15. Array vs linked list: when to choose each

### Two Pointer Techniques (10 cards)
16. What is the two-pointer technique?
17. Opposite-end two pointers (sorted array sum)
18. Same-direction two pointers (fast/slow)
19. Partitioning with two pointers (Dutch National Flag)
20. Remove duplicates from sorted array in-place
21. Reverse an array/string in place
22. Is palindrome check with two pointers
23. Container with most water approach
24. Move zeroes to end pattern
25. Three-sum reduction to two-sum

### Sliding Window (10 cards)
26. What is the sliding window technique?
27. Fixed-size sliding window pattern
28. Variable-size sliding window pattern
29. When to expand vs shrink the window
30. Maximum sum subarray of size k
31. Longest substring without repeating characters approach
32. Minimum window substring approach
33. Sliding window with a frequency map
34. How to track window state with a hash map
35. Time complexity of sliding window algorithms

### String Manipulation (15 cards)
36. Reverse a string: two-pointer approach
37. Check anagram: frequency count approach
38. Group anagrams: sorted-string key approach
39. Valid parentheses: stack approach
40. Longest common prefix approach
41. String to integer (atoi) edge cases
42. Encode/decode strings pattern
43. KMP algorithm: what problem does it solve?
44. Rabin-Karp: rolling hash for substring search
45. Character frequency counting with hash map
46. ASCII vs Unicode awareness in string problems
47. Python string slicing: time complexity
48. Immutability impact on string operations
49. Trie vs hash map for prefix problems
50. Z-algorithm: pattern matching

### Array Algorithms & Patterns (15 cards)
51. Binary search: iterative template
52. Binary search: when to use left < right vs left <= right
53. Kadane's algorithm: maximum subarray
54. Prefix sum technique
55. Prefix sum: range query in O(1)
56. Product of array except self: approach
57. Trapping rain water: two-pointer approach
58. Next greater element: monotonic stack approach
59. Merge intervals: sort + sweep
60. Meeting rooms: overlap detection
61. Rotate array by k positions
62. Boyer-Moore voting algorithm (majority element)
63. Dutch National Flag: 3-way partition
64. Binary search on answer (search space reduction)
65. Cyclic sort for [1, n] range problems

---

## Batch 2: Linked Lists (~55 cards)

### Singly Linked List Fundamentals (15 cards)
- Node structure, head pointer
- Traversal pattern
- Insert at head, tail, middle
- Delete at head, tail, by value
- Search for a value
- Get length
- Time complexities for all operations

### Doubly Linked List Fundamentals (10 cards)
- Node structure (prev + next)
- Advantages over singly linked
- Insert/delete operations
- When to use doubly vs singly
- LRU cache connection

### Linked List Patterns (15 cards)
- Dummy/sentinel node technique
- Fast/slow pointer (tortoise & hare)
- Runner technique for midpoint
- Cycle detection (Floyd's)
- Finding cycle start
- Two-pointer for nth from end

### Linked List Algorithms (15 cards)
- Reverse a linked list (iterative)
- Reverse a linked list (recursive)
- Merge two sorted lists
- Detect palindrome (reverse second half)
- Intersection of two lists
- Remove nth node from end
- Reorder list pattern
- Sort a linked list (merge sort)
- Add two numbers (digit lists)
- Deep copy with random pointers

---

## Batch 3: Stacks & Queues (~40 cards)

### Stack Fundamentals (10 cards)
- LIFO principle, operations, complexities
- Array-based vs linked list-based
- Call stack and recursion connection
- Stack underflow/overflow

### Queue Fundamentals (10 cards)
- FIFO principle, operations, complexities
- Deque (double-ended queue)
- Circular queue
- Priority queue intro

### Monotonic Stack/Queue (10 cards)
- Monotonic increasing/decreasing stack
- Next greater/smaller element pattern
- Daily temperatures approach
- Largest rectangle in histogram

### Applications (10 cards)
- Evaluate reverse Polish notation
- Min stack design
- Implement queue using stacks
- Implement stack using queues
- Asteroid collision pattern
- Balanced brackets checking

---

## Batch 4: Binary Trees & BST (~70 cards)

### Tree Fundamentals (10 cards)
- Node structure, root, leaf, height, depth
- Binary tree properties
- Complete, full, perfect, balanced definitions
- Height vs depth

### Traversals — DFS (20 cards)
- Pre-order: concept, use cases, recursive code
- In-order: concept, use cases, recursive code
- Post-order: concept, use cases, recursive code
- Pre-order iterative with stack
- In-order iterative with stack
- Post-order iterative approaches
- When to use pre vs in vs post
- V-shape visualization of recursion
- Processing order decision framework

### Traversals — BFS (10 cards)
- Level-order with queue
- Level-order tracking level boundaries
- Zigzag level order
- Right side view
- Level averages

### BST Operations (15 cards)
- BST property definition
- Search in BST
- Insert in BST
- Delete from BST (3 cases)
- Find min/max
- In-order gives sorted output
- Validate BST (bounds passing)
- BST time complexities (balanced vs skewed)

### Tree Patterns & Algorithms (15 cards)
- Max/min depth
- Diameter of tree
- Lowest common ancestor
- Path sum (root to leaf)
- Invert/mirror tree
- Serialize/deserialize
- Build tree from traversals
- Check symmetric tree
- Collect leaves by level (the V-shape problem)

---

## Batch 5: Heaps & Priority Queues (~30 cards)

- Min-heap vs max-heap properties
- Heap operations: insert, extract, peek
- Heapify: what and why
- Build heap from array: O(n)
- Python heapq module
- Top-k elements pattern
- K-sorted array optimization
- Merge k sorted lists
- Median of stream (two heaps)
- Heap vs BST: when to use which

---

## Batch 6: Tries & Advanced Trees (~25 cards)

- Trie node structure
- Insert, search, startsWith operations
- Trie time/space complexity
- Trie vs hash map for prefix queries
- Autocomplete/typeahead design
- T9 dictionary problem approach
- N-ary tree traversal
- N-ary tree vs binary tree

---

## Batch 7: Graphs & Matrices (~55 cards)

### Graph Fundamentals (10 cards)
- Vertices, edges, directed vs undirected
- Adjacency list vs adjacency matrix
- Weighted vs unweighted
- Sparse vs dense graphs

### Graph Traversals (15 cards)
- DFS on graph (recursive)
- DFS on graph (iterative with stack)
- BFS on graph (queue)
- Visited set: why needed for graphs but implicit for trees
- Connected components
- DFS vs BFS: when to choose which

### Matrix as Graph (10 cards)
- Matrix cells as nodes, adjacency via neighbors
- 4-directional vs 8-directional movement
- Boundary checking pattern
- Number of islands (BFS/DFS)
- Flood fill
- Rotting oranges (multi-source BFS)

### Graph Algorithms (20 cards)
- Topological sort (DFS-based)
- Topological sort (Kahn's BFS)
- Dijkstra's shortest path
- Bellman-Ford
- Union-Find (disjoint set)
- Cycle detection (directed vs undirected)
- Minimum spanning tree concepts
- Bipartite graph check
- Clone graph pattern

---

## Batch 8: Recursion & Backtracking (~70 cards) ⭐ WEIGHTED

### Recursion Fundamentals (15 cards)
- What is recursion? Base case + recursive case
- Call stack mechanics
- Stack overflow: when and why
- Recursion vs iteration: trade-offs
- Tail recursion concept
- Recursive leap of faith
- The "V-shape" of recursion (down = explore, bottom = base case, up = return)

### Recursive Function Design (15 cards)
- Choosing base cases
- What information to pass as parameters
- Mutable vs immutable parameter passing
- What to return from recursive calls
- How to combine results from child calls
- When to use helper functions
- Accumulator pattern
- Global/nonlocal variable pattern vs return values

### Backtracking Template & Patterns (20 cards)
- Backtracking definition: explore → choose → recurse → unchoose
- Generic backtracking template code
- State mutation vs immutable state
- When to undo choices (mutable shared state)
- Pruning: what and why
- Permutations approach
- Combinations approach
- Subsets approach
- N-Queens setup
- Sudoku solver approach

### Backtracking Problems (20 cards)
- Generate parentheses
- Letter combinations of phone number
- Word search in grid
- Combination sum (with/without reuse)
- Palindrome partitioning
- Restore IP addresses
- Path problems in trees
- Maze solving approach
- Decision tree visualization for backtracking
- Identifying when a problem needs backtracking

---

## Batch 9: Sorting Algorithms (~50 cards)

### Sorting Overview (10 cards)
- Comparison-based sorting lower bound: O(n log n)
- Stable vs unstable sorts
- In-place vs not in-place
- Adaptive sorts
- Sorting algorithm comparison table

### Individual Sorts (35 cards, ~5-7 each)
- **Bubble Sort**: concept, code, complexities, optimization flag
- **Insertion Sort**: concept, code, complexities, card-sorting analogy
- **Merge Sort**: concept, code, divide-and-conquer, space overhead
- **Quick Sort**: concept, code, pivot selection, partition
- **Heap Sort**: concept, code, heapify, in-place O(1) space
- **Counting Sort**: concept, when to use, non-comparison
- **Radix Sort**: concept, digit-by-digit
- **Bucket Sort**: concept, distribution-based

### Sorting Applications (5 cards)
- K-sorted array: heap optimization
- When to use which sort
- Sort stability: why it matters
- Custom comparators in Python

---

## Batch 10: DP, Complexity Analysis & General Patterns (~65 cards)

### Dynamic Programming (30 cards)
- What is DP? Overlapping subproblems + optimal substructure
- Memoization (top-down) vs tabulation (bottom-up)
- Fibonacci: naive → memo → tabulation → space-optimized
- Climbing stairs
- Coin change
- Longest common subsequence
- 0/1 Knapsack
- DP state identification
- DP recurrence relations
- When DP vs greedy vs backtracking

### Complexity Analysis (20 cards)
- Big-O, Big-Omega, Big-Theta definitions
- Common complexities ranked
- How to analyze nested loops
- How to analyze recursive algorithms (recurrence relations)
- Amortized analysis concept
- Space complexity: auxiliary vs total
- Master theorem basics
- Log n: why it appears (halving problems)
- n!: when it appears (permutations)
- 2^n: when it appears (subsets/power sets)

### General Algorithmic Patterns (15 cards)
- Greedy: concept and when it works
- Divide and conquer: concept
- Binary search on answer
- Bit manipulation basics (XOR, AND, shifts)
- Hash map: O(1) lookup enabling patterns
- Frequency counting pattern
- In-place modification techniques
- Sentinel/dummy values
- Problem decomposition strategies
- How to identify which pattern to apply

---

## Import Instructions

Each batch is a `.txt` file with Anki file headers:
```
#separator:Tab
#html:true
#tags column:3
#deck:DSA Master Deck
```

To import into Anki:
1. Open Anki → File → Import
2. Select the `.txt` file
3. Verify: Type = "Basic", Deck = "DSA Master Deck"
4. Ensure "Allow HTML in fields" is checked
5. Field 1 → Front, Field 2 → Back, Field 3 → Tags
6. Import

Import each batch file separately. Tags will auto-organize cards by topic.

---

## Spaced Repetition Schedule

See the accompanying `dsa_tracking_worksheet.xlsx` for:
- Weekly review schedule (which batches to study when)
- Daily new card + review card targets
- Progress tracking by topic
- Mastery level tracking
