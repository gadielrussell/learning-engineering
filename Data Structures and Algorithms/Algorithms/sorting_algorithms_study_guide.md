# Sorting Algorithms Study Guide

## Overview

This guide covers the fundamental sorting algorithms organized by their time complexity, with deep dives into Heap Sort and Insertion Sort as recommended by Andrew. We'll also explore the "K-Sorted Array" problem that demonstrates how understanding sorting mechanics enables optimization.

---

## Time Complexity Classifications

### O(n log n) Algorithms — The Efficient Tier

These algorithms achieve optimal comparison-based sorting performance through divide-and-conquer or heap-based approaches.

### O(n²) Algorithms — The Simple Tier

These algorithms use nested iterations, making them inefficient for large datasets but valuable for understanding fundamentals and specific use cases.

---

## The O(n²) Algorithms

### Bubble Sort

**The Concept:** Repeatedly step through the list, compare adjacent elements, and swap them if they're in the wrong order. The largest unsorted element "bubbles up" to its correct position each pass.

**How It Works:**
1. Compare elements at index 0 and 1, swap if needed
2. Compare elements at index 1 and 2, swap if needed
3. Continue until end of array (largest element now at end)
4. Repeat for remaining unsorted portion
5. Stop when no swaps occur in a complete pass

**Execution Trace:**
```
Array: [5, 3, 8, 1, 2]

Pass 1: [5,3,8,1,2] → [3,5,8,1,2] → [3,5,8,1,2] → [3,5,1,8,2] → [3,5,1,2,8]
Pass 2: [3,5,1,2,8] → [3,5,1,2,8] → [3,1,5,2,8] → [3,1,2,5,8]
Pass 3: [3,1,2,5,8] → [1,3,2,5,8] → [1,2,3,5,8]
Pass 4: [1,2,3,5,8] → no swaps, done!
```

**Complexity Analysis:**
| Case | Time | Space |
|------|------|-------|
| Best | O(n) — already sorted, single pass with no swaps | O(1) |
| Average | O(n²) | O(1) |
| Worst | O(n²) — reverse sorted | O(1) |

**Python Implementation:**
```python
def bubble_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    for i in range(n):
        swapped = False
        # Each pass bubbles the largest unsorted element to the end
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # Optimization: if no swaps occurred, array is sorted
        if not swapped:
            break
    return arr
```

**Key Insight:** The optimization flag transforms best-case from O(n²) to O(n). This is why understanding the mechanics matters—you can identify when early termination is possible.

---

### Insertion Sort ⭐ (Memorize This One)

**Why Memorize:** Most closely reflects how humans naturally sort things. Think of sorting playing cards in your hand—you pick up each card and insert it into its correct position among the cards you've already sorted.

**The Concept:** Build the sorted array one element at a time by repeatedly picking the next unsorted element and inserting it into its correct position within the already-sorted portion.

**How It Works:**
1. Consider the first element as a sorted subarray of size 1
2. Pick the next element (key)
3. Compare key with sorted elements from right to left
4. Shift larger elements one position right
5. Insert key into the gap created
6. Repeat until all elements processed

**Execution Trace:**
```
Array: [5, 3, 8, 1, 2]

Step 1: [5] | 3, 8, 1, 2    key=3, 3<5, shift 5 right → [3, 5]
Step 2: [3, 5] | 8, 1, 2    key=8, 8>5, no shift → [3, 5, 8]
Step 3: [3, 5, 8] | 1, 2    key=1, shift 8,5,3 right → [1, 3, 5, 8]
Step 4: [1, 3, 5, 8] | 2    key=2, shift 8,5,3 right, stop at 1 → [1, 2, 3, 5, 8]

Legend: [sorted portion] | unsorted portion
```

**Complexity Analysis:**
| Case | Time | Space |
|------|------|-------|
| Best | O(n) — already sorted, each element compared once | O(1) |
| Average | O(n²) | O(1) |
| Worst | O(n²) — reverse sorted, maximum shifts | O(1) |

**Python Implementation:**
```python
def insertion_sort(arr: list[int]) -> list[int]:
    for i in range(1, len(arr)):
        key = arr[i]  # Element to insert
        j = i - 1     # Start comparing with element to the left
        
        # Shift elements right until we find key's correct position
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]  # Shift right
            j -= 1
        
        arr[j + 1] = key  # Insert key into gap
    return arr
```

**Why It's Special:**
- **Adaptive:** Runs in O(n) time when array is nearly sorted
- **Stable:** Maintains relative order of equal elements
- **Online:** Can sort as elements arrive (streaming data)
- **In-place:** O(1) auxiliary space
- **Efficient for small arrays:** Often faster than O(n log n) algorithms for n < 10-20 due to low overhead

**Critical Insight for K-Sorted Problem:** When elements are at most k positions away from their sorted position, each element only needs to shift at most k times. This transforms the algorithm from O(n²) to O(nk).

---

### Selection Sort

**The Concept:** Repeatedly find the minimum element from the unsorted portion and place it at the beginning of the unsorted portion.

**How It Works:**
1. Find the minimum element in the entire array
2. Swap it with the first element
3. Find the minimum in the remaining unsorted portion
4. Swap it with the first unsorted element
5. Repeat until sorted

**Execution Trace:**
```
Array: [5, 3, 8, 1, 2]

Pass 1: Find min(5,3,8,1,2)=1, swap with index 0 → [1, 3, 8, 5, 2]
Pass 2: Find min(3,8,5,2)=2, swap with index 1   → [1, 2, 8, 5, 3]
Pass 3: Find min(8,5,3)=3, swap with index 2     → [1, 2, 3, 5, 8]
Pass 4: Find min(5,8)=5, already in place        → [1, 2, 3, 5, 8]
```

**Complexity Analysis:**
| Case | Time | Space |
|------|------|-------|
| Best | O(n²) — always scans entire unsorted portion | O(1) |
| Average | O(n²) | O(1) |
| Worst | O(n²) | O(1) |

**Python Implementation:**
```python
def selection_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    for i in range(n):
        min_idx = i
        # Find minimum in unsorted portion
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Swap minimum with first unsorted element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
```

**Key Characteristic:** Unlike Insertion Sort, Selection Sort always performs O(n²) comparisons regardless of input order. However, it minimizes swaps (exactly n-1), making it useful when write operations are expensive.

---

## The O(n log n) Algorithms

### Heap Sort ⭐ (Memorize This One First)

**Why Memorize:** Usually the most efficient in practice, keeps track of sorted items cleanly, and the behavior is predictable. Understanding heaps also unlocks solutions to many other problems (priority queues, k-way merge, top-k problems).

**The Concept:** Transform the array into a max-heap, then repeatedly extract the maximum element and place it at the end of the array.

**Prerequisites — Understanding Heaps:**

A **heap** is a complete binary tree stored as an array where:
- **Max-heap:** Every parent ≥ its children
- **Min-heap:** Every parent ≤ its children

**Array-to-tree index mapping:**
```
For element at index i:
- Parent: (i - 1) // 2
- Left child: 2*i + 1
- Right child: 2*i + 2

Array: [16, 14, 10, 8, 7, 9, 3]

Tree visualization:
           16(0)
         /      \
      14(1)     10(2)
      /   \     /   \
    8(3) 7(4) 9(5) 3(6)
```

**How Heap Sort Works:**
1. **Build max-heap:** Transform array into max-heap (heapify)
2. **Extract and place:** Swap root (max) with last element, reduce heap size, restore heap property
3. **Repeat:** Continue until heap size is 1

**The Heapify Operation (Sift Down):**
```
Starting from a node, compare with children and swap with larger child if necessary.
Repeat until heap property is satisfied.

Example - heapify at index 0:
[4, 14, 10, 8, 7, 9, 3]  Node 4 < children
      4
    /   \
   14    10

Swap 4 with 14 (larger child):
[14, 4, 10, 8, 7, 9, 3]
      14
    /    \
   4      10

Continue heapifying at new position of 4:
      14
    /    \
   4      10
  / \
 8   7

Swap 4 with 8:
[14, 8, 10, 4, 7, 9, 3]  Heap property restored!
```

**Building the Heap:**
```
Array: [5, 3, 8, 1, 2]

Start heapifying from last non-leaf node (index n//2 - 1 = 1)

Initial tree:
       5(0)
      /    \
    3(1)   8(2)
    /  \
  1(3) 2(4)

Heapify index 1: 3 vs children [1,2], 3 > both, no change
Heapify index 0: 5 vs children [3,8], swap with 8

       8(0)
      /    \
    3(1)   5(2)
    /  \
  1(3) 2(4)

Array is now: [8, 3, 5, 1, 2] — valid max-heap!
```

**Extraction Phase:**
```
Max-heap: [8, 3, 5, 1, 2]

Step 1: Swap root(8) with last(2), heap size = 4
[2, 3, 5, 1 | 8]  Heapify → [5, 3, 2, 1 | 8]

Step 2: Swap root(5) with last(1), heap size = 3
[1, 3, 2 | 5, 8]  Heapify → [3, 1, 2 | 5, 8]

Step 3: Swap root(3) with last(2), heap size = 2
[2, 1 | 3, 5, 8]  Heapify → [2, 1 | 3, 5, 8]

Step 4: Swap root(2) with last(1), heap size = 1
[1 | 2, 3, 5, 8]

Done: [1, 2, 3, 5, 8]
```

**Complexity Analysis:**
| Operation | Time | Explanation |
|-----------|------|-------------|
| Build heap | O(n) | Counterintuitive! Most nodes are near bottom with small heapify cost |
| Extract all | O(n log n) | n extractions × O(log n) heapify each |
| **Total** | **O(n log n)** | Dominates |
| Space | O(1) | In-place sorting |

**Python Implementation:**
```python
def heap_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    
    def heapify(size: int, root: int) -> None:
        """Restore max-heap property at root, assuming children are valid heaps."""
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2
        
        if left < size and arr[left] > arr[largest]:
            largest = left
        if right < size and arr[right] > arr[largest]:
            largest = right
        
        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            heapify(size, largest)  # Continue down the affected subtree
    
    # Phase 1: Build max-heap (start from last non-leaf node)
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    
    # Phase 2: Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Move max to sorted portion
        heapify(i, 0)  # Restore heap on reduced size
    
    return arr
```

**Why Heap Sort is Reliable:**
- **Guaranteed O(n log n):** No worst-case degradation like QuickSort
- **In-place:** O(1) auxiliary space unlike MergeSort's O(n)
- **Predictable:** Same performance regardless of input pattern
- **Partial sorting:** Can efficiently find top-k elements

**Critical Insight for K-Sorted Problem:** A min-heap of size k+1 always contains the next element to output. We only need O(log k) per element instead of O(log n).

---

### Merge Sort

**The Concept:** Divide the array in half recursively until single elements, then merge sorted halves back together.

**How It Works:**
1. **Divide:** Split array into two halves
2. **Conquer:** Recursively sort each half
3. **Combine:** Merge two sorted halves into one sorted array

**Execution Trace:**
```
Array: [5, 3, 8, 1, 2]

Divide phase:
[5, 3, 8, 1, 2]
       ↓
[5, 3, 8]  [1, 2]
    ↓         ↓
[5, 3] [8]  [1] [2]
  ↓
[5] [3]

Merge phase (bottom-up):
[5] [3] → compare, merge → [3, 5]
[3, 5] [8] → merge → [3, 5, 8]
[1] [2] → merge → [1, 2]
[3, 5, 8] [1, 2] → merge → [1, 2, 3, 5, 8]

Merge [3,5,8] and [1,2] in detail:
Compare 3 vs 1 → take 1 → [1]
Compare 3 vs 2 → take 2 → [1, 2]
Remaining [3,5,8] → [1, 2, 3, 5, 8]
```

**Complexity Analysis:**
| Case | Time | Space |
|------|------|-------|
| All cases | O(n log n) | O(n) auxiliary for merge buffer |

**Python Implementation:**
```python
def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Append remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Key Characteristics:**
- **Stable:** Preserves relative order of equal elements
- **Predictable:** Always O(n log n) regardless of input
- **Not in-place:** Requires O(n) additional space
- **Parallelizable:** Subarrays can be sorted independently

---

### Quick Sort

**The Concept:** Choose a pivot element, partition array so all elements less than pivot are left and greater are right, then recursively sort partitions.

**How It Works:**
1. **Choose pivot:** Select an element (various strategies exist)
2. **Partition:** Rearrange so elements < pivot are left, elements > pivot are right
3. **Recurse:** Apply to left and right partitions

**Execution Trace (using last element as pivot):**
```
Array: [5, 3, 8, 1, 2]  pivot=2

Partition around 2:
- Elements < 2: [1]
- Elements > 2: [5, 3, 8]
Result: [1, 2, 5, 3, 8]  (2 is now in correct position!)

Recurse left [1]: already sorted
Recurse right [5, 3, 8], pivot=8:
- Elements < 8: [5, 3]
- Elements > 8: []
Result: [5, 3, 8]

Recurse [5, 3], pivot=3:
Result: [3, 5]

Final: [1, 2, 3, 5, 8]
```

**Complexity Analysis:**
| Case | Time | Space |
|------|------|-------|
| Best | O(n log n) — pivot always splits evenly | O(log n) stack |
| Average | O(n log n) | O(log n) stack |
| Worst | O(n²) — pivot always min/max (already sorted input) | O(n) stack |

**Python Implementation:**
```python
def quick_sort(arr: list[int], low: int = 0, high: int = None) -> list[int]:
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
    
    return arr

def partition(arr: list[int], low: int, high: int) -> int:
    pivot = arr[high]  # Choose last element as pivot
    i = low - 1        # Index of smaller element boundary
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

**Key Characteristics:**
- **In-place:** O(log n) auxiliary space (stack only)
- **Not stable:** Equal elements may be reordered
- **Cache-friendly:** Sequential memory access patterns
- **Pivot selection matters:** Randomized pivot avoids worst-case on sorted input

---

## Sorting Algorithm Comparison Matrix

| Algorithm | Best | Average | Worst | Space | Stable | In-Place | Adaptive |
|-----------|------|---------|-------|-------|--------|----------|----------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | ✓ | ✓ | ✓ |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | ✓ | ✓ | ✓ |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | ✗ | ✓ | ✗ |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | ✗ | ✓ | ✗ |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | ✓ | ✗ | ✗ |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | ✗ | ✓ | ✗ |

**Terminology:**
- **Stable:** Equal elements maintain their original relative order
- **In-Place:** Uses O(1) auxiliary space (excluding recursion stack)
- **Adaptive:** Performs better on partially sorted input

---

## The K-Sorted Array Problem

### Problem Statement
> Given an array where each element is at most k positions away from its sorted position, fully sort the array.

**Inputs:** `arr: list[int]`, `k: int`

**Assumptions:**
- k ≥ 0
- If k = 0, array is already sorted

### Why This Problem is Brilliant

It forces you to understand sorting algorithms deeply enough to exploit domain knowledge.

### Analysis of Standard Approaches

**Naive approach:** Use any O(n log n) sort
- Works, but ignores the constraint
- Wastes the information we're given

**Key Insight:** If an element is at most k positions away from its final position, then:
- The smallest element must be within the first k+1 elements
- After placing the smallest, the next smallest must be within the next k+1 elements
- This sliding window property is the key!

### Solution 1: Modified Insertion Sort — O(nk)

Since each element is at most k positions away, each element needs at most k comparisons/shifts.

```python
def sort_k_sorted_insertion(arr: list[int], k: int) -> list[int]:
    """
    Time: O(nk) — each element shifts at most k positions
    Space: O(1)
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        # Only need to look back at most k positions
        while j >= max(0, i - k) and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr
```

**When is this good?** When k is very small (k << log n), this beats O(n log n)!

### Solution 2: Min-Heap of Size k+1 — O(n log k) ⭐

This is the optimal solution and demonstrates the power of understanding heap mechanics.

**The Insight:**
- The correct element for position 0 must be among indices 0 to k (k+1 elements)
- After extracting the minimum, add the next element to maintain the window
- A min-heap of size k+1 gives us the minimum in O(log k) time

```python
import heapq

def sort_k_sorted_heap(arr: list[int], k: int) -> list[int]:
    """
    Time: O(n log k) — n extractions/insertions on heap of size k+1
    Space: O(k) — heap storage
    """
    if k == 0:
        return arr
    
    n = len(arr)
    result = []
    
    # Initialize min-heap with first k+1 elements
    heap = arr[:min(k + 1, n)]
    heapq.heapify(heap)  # O(k)
    
    # Process remaining elements
    for i in range(k + 1, n):
        # Extract minimum (guaranteed to be correct for current position)
        result.append(heapq.heappop(heap))  # O(log k)
        # Add next element to maintain window
        heapq.heappush(heap, arr[i])        # O(log k)
    
    # Extract remaining elements from heap
    while heap:
        result.append(heapq.heappop(heap))
    
    return result
```

**Execution Trace:**
```
arr = [3, 2, 1, 5, 4, 7, 6, 8], k = 2

Initial heap (indices 0-2): [3, 2, 1] → heapify → [1, 2, 3]

Step 1: pop 1, push 5 → heap [2, 3, 5] → result [1]
Step 2: pop 2, push 4 → heap [3, 4, 5] → result [1, 2]
Step 3: pop 3, push 7 → heap [4, 5, 7] → result [1, 2, 3]
Step 4: pop 4, push 6 → heap [5, 6, 7] → result [1, 2, 3, 4]
Step 5: pop 5, push 8 → heap [6, 7, 8] → result [1, 2, 3, 4, 5]
Drain heap: → result [1, 2, 3, 4, 5, 6, 7, 8]
```

### Complexity Comparison for K-Sorted Array

| Approach | Time | Space | When to Use |
|----------|------|-------|-------------|
| Standard sort | O(n log n) | varies | When k is unknown or large |
| Insertion sort | O(nk) | O(1) | When k is very small (k < log n) |
| **Min-heap** | **O(n log k)** | O(k) | **Optimal for most cases** |

**The Math:**
- If k = O(1), insertion sort is O(n) — linear!
- If k = O(n), heap solution degrades to O(n log n) — same as standard
- For k = √n, heap gives O(n log √n) = O(n · ½ log n) — better than standard!

---

## Key Takeaways

### For Memorization (Andrew's Recommendation)

**1. Heap Sort — First Priority**
- Predictable O(n log n) always
- In-place (O(1) space)
- Understanding heaps unlocks many other problems
- The "keeps track of sorted items" property: extracted elements are guaranteed sorted

**2. Insertion Sort — Second Priority**
- Intuitive (like sorting cards)
- Adaptive (fast on nearly sorted data)
- The foundation for understanding why k-sorted arrays can be exploited

### For Interview Recognition

When you see constraints about "nearly sorted" or "at most k away":
1. Think sliding window
2. Think min-heap of bounded size
3. Calculate whether O(n log k) beats O(n log n) for the given k

### The Meta-Lesson

Understanding *how* sorting algorithms work—not just their complexity—enables you to:
- Recognize when constraints can be exploited
- Choose the right algorithm for specific scenarios
- Optimize by combining algorithmic insights with problem structure
