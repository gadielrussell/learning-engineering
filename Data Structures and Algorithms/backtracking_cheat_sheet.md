# Backtracking Mastery Cheat Sheet

## Credits
Adapted from [Teaching Misc.](https://github.com/jfarmer/teaching-misc) (GitHub) by [Jesse Farmer (@jfarmer)](https://github.com/jfarmer), used under [CC BY-NC-SA 4.0](https://github.com/jfarmer/teaching-misc/blob/main/LICENSE).

## Understanding Through the Maze Metaphor & DFS

### Core Concept: Backtracking = DFS + Undo

**Jesse Farmer's Key Insight:** Every backtracking problem is a depth-first search (DFS) of some tree. The tree represents your decision space.

### The "Gospel of Tree"
Every backtracking problem revolves around the depth-first traversal of SOME tree (call it the Problem Tree). If you make a program whose call tree looks like the Problem Tree then, congrats, you've solved the problem.

1. Get clear on the tree (as clear as you can)
2. Translate that tree into code as blindly/faithfully/religiously as possible (like a 4th-century religous scibr). OURS IS TO DO, NOT TO UNDERSTAND.
3. Optimize


Get it working, get it working right, get it working fast (in that order)
```
Maze Metaphor:
- You're exploring a maze systematically
- At each intersection (node), you make a choice
- If you hit a dead end (invalid state), you backtrack to the last intersection
- You mark your path to avoid cycles
- You continue until you find the exit (solution) or explore everything
```

---

### The Three Mental Models

#### 1. Physical Maze (Jesse's Model)
```
+---+----------+---+
| S...........A| C |  S = Start
| . -----------+ . |  X = Exit  
| ....B........... |  . = Path
+---- . +----+-----+  Letters = Decision Points
|D....E.....F|L... |
+---+ . +----+-- . |
| G | . | ...... H |
| . | . | . +--+ . |
| ....I...J...K| X |
+--------------+---+
```

#### 2. Decision Tree (What Actually Happens)
```
                    Start
                  /   |   \
                A     B     D
              /  \    |   /  \
             C   ..   E  G   E
                      |      |
                      F      I
                     /|\     |
                    H L K    J
                    |   |    |
                    X   X    K
                            |
                            X
```

#### 3. Code Execution (The Call Stack)
```python
explore(start)
  → explore(A)
    → explore(C) ✗ dead end, return
    ← backtrack to A
  ← backtrack to start
  → explore(B)
    → explore(E)
      → explore(F)
        → explore(H)
          → found X! ✓
```

## The Universal Backtracking Template

```python
def backtrack(state, path=[], all_solutions=[]):
    """
    state: Where we are now (current node in the decision tree)
    path: How we got here (breadcrumbs)
    all_solutions: Collection of valid solutions found
    """
    
    # BASE CASE: Are we at a solution?
    if is_solution(state):
        all_solutions.append(path.copy())  # Found one!
        return  # Could continue if multiple solutions needed
    
    # PRUNING: Can we bail early?
    if not is_valid(state):
        return  # Dead end, backtrack
    
    # EXPLORE: Try each possible next move
    for choice in get_choices(state):
        # MAKE the choice
        path.append(choice)
        new_state = apply_choice(state, choice)
        
        # EXPLORE recursively
        backtrack(new_state, path, all_solutions)
        
        # UNDO the choice (this is the "backtrack")
        path.pop()
    
    return all_solutions
```

---

## Parameter Decision Framework

### What Parameters Do You Need?

| Parameter Type | Purpose | When to Use | Example |
|---------------|---------|-------------|---------|
| **Current State** | Where are you in the problem space? | Always | `index`, `row/col`, `remaining_items` |
| **Path/Choices Made** | Track decisions to build solution | When building a solution | `current_path`, `selected_items` |
| **Constraints** | What limits/rules apply? | When validating choices | `budget_left`, `visited_cells` |
| **Solution Collector** | Where to store valid solutions | When finding all solutions | `results`, `all_paths` |

### Parameter Patterns by Problem Type

```python
# PERMUTATIONS: Track what's used
def permute(nums, current=[], used=set(), result=[]):
    # nums: original data (could be outside)
    # current: building current permutation
    # used: track what we've taken
    # result: collect all permutations

# MAZE/GRID: Track position and visited
def explore_maze(maze, row, col, path=[], visited=set()):
    # maze: the grid (usually constant)
    # row, col: current position
    # path: sequence of moves
    # visited: avoid cycles

# SUBSETS: Track index and current subset
def subsets(nums, index=0, current=[], result=[]):
    # nums: original array
    # index: position in decision tree
    # current: subset being built
    # result: all subsets

# N-QUEENS: Track board state
def n_queens(n, row=0, cols=set(), diags1=set(), diags2=set()):
    # n: board size
    # row: current row to place queen
    # cols, diags1, diags2: attacked positions
```

---

## Return Value Patterns

### When and What to Return?

| Goal | Return Pattern | Example |
|------|---------------|---------|
| **Find ONE solution** | Return immediately when found | `return path` or `return True` |
| **Find ALL solutions** | Accumulate, return at end | `return all_solutions` |
| **Count solutions** | Return count | `return count` |
| **Check if exists** | Return boolean | `return True/False` |
| **Optimize (min/max)** | Track best, return at end | `return best_solution` |

### Code Examples:

```python
# PATTERN 1: Find ONE Solution (early return)
def find_path(maze, start, end, path=[]):
    if start == end:
        return path + [end]  # Found it! Return immediately
    
    for next_pos in get_neighbors(start):
        if is_valid(next_pos):
            result = find_path(maze, next_pos, end, path + [start])
            if result:  # If found, propagate up immediately
                return result
    
    return None  # No solution from this branch

# PATTERN 2: Find ALL Solutions (accumulate)
def all_paths(graph, start, end, path=[], all_paths=[]):
    if start == end:
        all_paths.append(path + [end])
        return  # Don't return all_paths here, keep exploring!
    
    for neighbor in graph[start]:
        if neighbor not in path:  # Avoid cycles
            all_paths(graph, neighbor, end, path + [start], all_paths)
    
    return all_paths  # Return collection at the end

# PATTERN 3: Count Solutions
def count_ways(n, current=0):
    if current == n:
        return 1  # One valid way
    if current > n:
        return 0  # Invalid
    
    # Sum up all possibilities
    return count_ways(n, current + 1) + count_ways(n, current + 2)
```

---

## Complexity Analysis

### Time Complexity Formula

**Time = (Number of Nodes) × (Work per Node)**

For backtracking:
- **Number of Nodes** = Size of decision tree
- **Work per Node** = Validation + Choice generation + State updates

### Common Patterns:

| Problem | Time Complexity | Space Complexity | Why? |
|---------|----------------|------------------|------|
| **Permutations** | O(n! × n) | O(n) | n! permutations, O(n) to copy each |
| **Subsets** | O(2^n × n) | O(n) | 2^n subsets, O(n) to copy each |
| **N-Queens** | O(n!) | O(n) | n choices row 1, n-1 row 2, etc. |
| **Sudoku** | O(9^m) | O(81) | m empty cells, 9 choices each |
| **Maze/Grid DFS** | O(rows × cols) | O(rows × cols) | Visit each cell once |
| **Combination Sum** | O(2^n) | O(target) | Exponential decision tree |

### Decision Tree Size Calculation:

```
Branching Factor ^ Depth = Number of Nodes

Examples:
- Binary choices, depth d: 2^d nodes
- k choices, n positions: k^n nodes  
- Decreasing choices: n × (n-1) × (n-2) × ... = n! nodes
```

---

## Jesse's Permutation Example Decoded

```python
def permutations(string, prefix="", remaining=None, result=[]):
    """
    Tree Structure for "ABC":
                     ""
                /    |    \
              A      B      C
             / \    / \    / \
           AB  AC  BA  BC  CA  CB
           |   |   |   |   |   |
          ABC ACB BAC BCA CAB CBA
    """
    
    # Initialize on first call
    if remaining is None:
        remaining = string
    
    # BASE: No more choices, we have a complete permutation
    if not remaining:
        result.append(prefix)
        return
    
    # Try each remaining character as next choice
    for i in range(len(remaining)):
        # CHOOSE: Take character at index i
        chosen = remaining[i]
        new_remaining = remaining[:i] + remaining[i+1:]
        
        # EXPLORE: Recurse with this choice
        permutations(string, prefix + chosen, new_remaining, result)
        
        # No explicit UNDO needed (we're not modifying shared state)
    
    return result
```

---

## Common Pitfalls & Solutions

### 1. Forgetting to Undo (Most Common!)
```python
# WRONG - Modifies shared state without undoing
def wrong_permute(nums, path, result):
    for num in nums:
        path.append(num)  # Modifying shared list
        nums.remove(num)  # Modifying shared list
        wrong_permute(nums, path, result)
        # Forgot to undo!

# RIGHT - Proper backtracking
def right_permute(nums, path, result):
    for i, num in enumerate(nums):
        path.append(num)
        remaining = nums[:i] + nums[i+1:]  # Create new list
        right_permute(remaining, path, result)
        path.pop()  # UNDO!
```

### 2. Not Recognizing When to Stop Exploring
```python
# Add pruning to avoid unnecessary exploration
def solve_sudoku(board):
    if not is_valid_partial(board):
        return False  # Prune invalid branches early
    
    if is_complete(board):
        return True  # Stop when done
    
    # Continue exploring...
```

### 3. Incorrect Base Case
```python
# WRONG - Never reaches base case
def count_paths(n, current):
    if current == n:  # What if current starts > n?
        return 1
    # ...

# RIGHT - Handle all termination conditions  
def count_paths(n, current):
    if current == n:
        return 1
    if current > n:  # Handle overshoot
        return 0
    # ...
```

---

## Quick Decision Guide

### "What parameters do I need?"
1. **Where am I?** → Position parameter (index, row/col, node)
2. **What have I chosen?** → Path/collection parameter
3. **What can't I use?** → Used/visited set
4. **What are my limits?** → Constraint parameters

### "What do I return?"
1. **Finding one thing?** → Return it immediately when found
2. **Finding everything?** → Accumulate in list, return at end
3. **Counting?** → Return sum of recursive calls
4. **Checking existence?** → Return boolean

### "When do I make recursive calls?"
1. **When you have valid choices** → For each valid next step
2. **When not at a dead end** → After validation passes
3. **When not at solution** → Before base case is met

### "How do I undo?"
1. **Modified a list/set?** → Remove what you added
2. **Changed state?** → Restore previous state
3. **Using immutable approach?** → Nothing to undo!

---

## Remember:

1. **Backtracking = DFS + Undo Mechanism**
2. **Every problem is exploring a tree of choices**
3. **Parameters = State needed for current decision**
4. **Return = What you're trying to compute**
5. **Always undo changes to shared state**
6. **Prune early to avoid unnecessary exploration**
7. **Time complexity usually exponential (that's ok!)**
