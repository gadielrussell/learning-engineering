# Matrix Algorithms: A Comprehensive Problem-Solving Framework

## Table of Contents
1. [The Mental Model: What IS a Matrix Problem?](#the-mental-model-what-is-a-matrix-problem)
2. [Problem Assessment Framework](#problem-assessment-framework)
3. [The Five Core Matrix Patterns](#the-five-core-matrix-patterns)
4. [Pattern 1: Simple Traversal & Direction-Based](#pattern-1-simple-traversal--direction-based)
5. [Pattern 2: BFS - Shortest Path & Level-Based](#pattern-2-bfs---shortest-path--level-based)
6. [Pattern 3: DFS - Connected Components & Exploration](#pattern-3-dfs---connected-components--exploration)
7. [Pattern 4: Graph Transformation Problems](#pattern-4-graph-transformation-problems)
8. [Pattern 5: Dynamic Programming on Matrices](#pattern-5-dynamic-programming-on-matrices)
9. [Common Pitfalls & Edge Cases](#common-pitfalls--edge-cases)
10. [Quick Reference Cheat Sheet](#quick-reference-cheat-sheet)

---

## The Mental Model: What IS a Matrix Problem?

A matrix is fundamentally a **graph in disguise**. Every cell is a node, and adjacency (up/down/left/right, sometimes diagonals) defines edges. The key insight is:

> **A matrix is just a graph with implicit edges based on spatial relationships.**

This reframing is powerful because it means all graph algorithms apply—but the matrix structure gives us additional properties we can exploit (like coordinates, boundaries, and spatial locality).

### The Three Ways to View a Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│  VIEW 1: Grid of Values     VIEW 2: Implicit Graph              │
│  ┌───┬───┬───┐              (0,0)───(0,1)───(0,2)               │
│  │ 1 │ 0 │ 1 │                │       │       │                 │
│  ├───┼───┼───┤              (1,0)───(1,1)───(1,2)               │
│  │ 1 │ 1 │ 0 │                │       │       │                 │
│  ├───┼───┼───┤              (2,0)───(2,1)───(2,2)               │
│  │ 0 │ 1 │ 1 │                                                  │
│  └───┴───┴───┘                                                  │
│                                                                 │
│  VIEW 3: Explicit Graph (when needed)                           │
│  {                                                              │
│    (0,0): [(0,1), (1,0)],                                       │
│    (0,1): [(0,0), (0,2), (1,1)],                                │
│    ...                                                          │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Problem Assessment Framework

When you see a matrix problem, ask these questions **in order**:

### Step 1: What Am I Looking For?

| Looking For... | Likely Pattern |
|----------------|----------------|
| Shortest path/distance | **BFS** |
| Count of regions/islands/components | **DFS or BFS** (either works) |
| Can I reach from A to B? | **DFS** (simpler) or **BFS** |
| All paths / explore all possibilities | **DFS with backtracking** |
| Optimal value (min cost, max path) | **DP** or **BFS** (depends on weights) |
| Transform/merge based on relationships | **Graph construction + Union-Find or DFS** |
| Specific traversal order (spiral, diagonal) | **Simple traversal with careful indexing** |

### Step 2: What Are the "Edges"?

| Edge Definition | Implementation |
|-----------------|----------------|
| Adjacent cells (4-directional) | `directions = [(0,1), (0,-1), (1,0), (-1,0)]` |
| Adjacent cells (8-directional) | Add diagonals: `[(1,1), (1,-1), (-1,1), (-1,-1)]` |
| Cells with same value | May need explicit graph or Union-Find |
| Cells satisfying condition | Filter in your neighbor loop |
| Non-adjacent relationships | **Must build explicit graph** |

### Step 3: Is There a "Weight" or "Cost"?

| Scenario | Algorithm |
|----------|-----------|
| All moves cost the same | **BFS** (guarantees shortest path) |
| Moves have different costs | **Dijkstra's** or **DP** |
| Binary costs (0 or 1) | **0-1 BFS** (deque trick) |

### Step 4: Do I Need to Track State Beyond Position?

| Extra State Needed | Approach |
|--------------------|----------|
| Just visited/not visited | Simple `visited` set |
| Number of steps taken | BFS naturally tracks this |
| Keys collected, walls broken | State tuple: `(row, col, keys)` or `(row, col, walls_broken)` |
| Path taken | DFS with backtracking, maintain path list |

---

## The Five Core Matrix Patterns

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        MATRIX PROBLEM PATTERNS                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                   │
│  │   SIMPLE    │   │    BFS      │   │    DFS      │                   │
│  │  TRAVERSAL  │   │  (Shortest  │   │  (Explore   │                   │
│  │             │   │   Path)     │   │   All)      │                   │
│  └─────────────┘   └─────────────┘   └─────────────┘                   │
│        │                 │                 │                            │
│        ▼                 ▼                 ▼                            │
│  • Spiral order    • Min distance    • Count islands                   │
│  • Diagonal scan   • Nearest X       • Flood fill                      │
│  • Rotate matrix   • Level by level  • Find all paths                  │
│                    • Multi-source    • Connected components            │
│                                                                         │
│  ┌─────────────┐   ┌─────────────┐                                     │
│  │   GRAPH     │   │     DP      │                                     │
│  │ TRANSFORM   │   │  (Optimal   │                                     │
│  │             │   │   Value)    │                                     │
│  └─────────────┘   └─────────────┘                                     │
│        │                 │                                              │
│        ▼                 ▼                                              │
│  • Account merge   • Min path sum                                      │
│  • Word ladder     • Unique paths                                      │
│  • Complex deps    • Maximal square                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Pattern 1: Simple Traversal & Direction-Based

### When to Use
- Problem asks for specific traversal order (spiral, diagonal, snake)
- Need to rotate, transpose, or transform the matrix
- Looking in directions from each cell without graph traversal

### Core Template: Direction Vectors

```python
from typing import List, Tuple

# 4-directional movement
DIRECTIONS_4 = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

# 8-directional movement (includes diagonals)
DIRECTIONS_8 = [
    (0, 1), (0, -1), (1, 0), (-1, 0),      # cardinal
    (1, 1), (1, -1), (-1, 1), (-1, -1)     # diagonal
]

def is_valid(row: int, col: int, rows: int, cols: int) -> bool:
    """Check if coordinates are within matrix bounds."""
    return 0 <= row < rows and 0 <= col < cols

def get_neighbors(row: int, col: int, rows: int, cols: int, 
                  directions: List[Tuple[int, int]] = DIRECTIONS_4) -> List[Tuple[int, int]]:
    """Get all valid neighboring coordinates."""
    neighbors = []
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if is_valid(new_row, new_col, rows, cols):
            neighbors.append((new_row, new_col))
    return neighbors
```

### Example: Spiral Matrix Traversal

```python
def spiral_order(matrix: List[List[int]]) -> List[int]:
    """
    Traverse matrix in spiral order (clockwise from outside in).
    
    Example:
        Input:  [[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 9]]
        Output: [1, 2, 3, 6, 9, 8, 7, 4, 5]
    
    Approach: Maintain four boundaries and shrink them as we traverse.
    """
    if not matrix or not matrix[0]:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # Traverse right along top row
        for col in range(left, right + 1):
            result.append(matrix[top][col])
        top += 1
        
        # Traverse down along right column
        for row in range(top, bottom + 1):
            result.append(matrix[row][right])
        right -= 1
        
        # Traverse left along bottom row (if still valid)
        if top <= bottom:
            for col in range(right, left - 1, -1):
                result.append(matrix[bottom][col])
            bottom -= 1
        
        # Traverse up along left column (if still valid)
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][left])
            left += 1
    
    return result
```

### Example: Rotate Matrix 90° Clockwise

```python
def rotate_matrix(matrix: List[List[int]]) -> None:
    """
    Rotate matrix 90 degrees clockwise IN-PLACE.
    
    Key insight: rotation = transpose + reverse each row
    
    Example:
        [[1,2,3],      [[1,4,7],      [[7,4,1],
         [4,5,6],  →    [2,5,8],  →    [8,5,2],
         [7,8,9]]       [3,6,9]]       [9,6,3]]
        (original)     (transpose)    (reverse rows)
    """
    n = len(matrix)
    
    # Step 1: Transpose (swap matrix[i][j] with matrix[j][i])
    for i in range(n):
        for j in range(i + 1, n):  # j starts at i+1 to avoid double-swapping
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    
    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()
```

---

## Pattern 2: BFS - Shortest Path & Level-Based

### When to Use
- **"Shortest"** or **"minimum"** in the problem
- Need distance from one point to another
- Need to process level-by-level
- All moves have equal cost

### Why BFS Guarantees Shortest Path

BFS explores in "waves" - all cells at distance 1, then all at distance 2, etc. The first time you reach a cell is guaranteed to be via the shortest path.

```
Start: S                     BFS Exploration Order:
┌───┬───┬───┬───┐           ┌───┬───┬───┬───┐
│ S │   │   │   │           │ 0 │ 1 │ 2 │ 3 │
├───┼───┼───┼───┤           ├───┼───┼───┼───┤
│   │ X │ X │   │    →      │ 1 │ X │ X │ 4 │
├───┼───┼───┼───┤           ├───┼───┼───┼───┤
│   │   │   │ E │           │ 2 │ 3 │ 4 │ 5 │
└───┴───┴───┴───┘           └───┴───┴───┴───┘
                            (numbers = distance from S)
```

### Core BFS Template

```python
from collections import deque
from typing import List, Optional, Set, Tuple

def bfs_shortest_path(
    matrix: List[List[int]], 
    start: Tuple[int, int], 
    end: Tuple[int, int]
) -> int:
    """
    Find shortest path from start to end in a matrix.
    Returns -1 if no path exists.
    
    Time: O(rows × cols) - visit each cell at most once
    Space: O(rows × cols) - for visited set and queue
    """
    rows, cols = len(matrix), len(matrix[0])
    
    # Edge case: start or end is blocked
    if matrix[start[0]][start[1]] == 1 or matrix[end[0]][end[1]] == 1:
        return -1
    
    # BFS setup
    queue = deque([(start[0], start[1], 0)])  # (row, col, distance)
    visited: Set[Tuple[int, int]] = {start}
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        row, col, distance = queue.popleft()
        
        # Found the target!
        if (row, col) == end:
            return distance
        
        # Explore neighbors
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check bounds, obstacles, and visited
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                matrix[new_row][new_col] == 0 and 
                (new_row, new_col) not in visited):
                
                visited.add((new_row, new_col))
                queue.append((new_row, new_col, distance + 1))
    
    return -1  # No path found
```

### Example: Rotting Oranges (Multi-Source BFS)

This is a classic problem that demonstrates **multi-source BFS** - starting from multiple points simultaneously.

```python
def oranges_rotting(grid: List[List[int]]) -> int:
    """
    LeetCode 994: Rotting Oranges
    
    0 = empty, 1 = fresh orange, 2 = rotten orange
    Each minute, rotten oranges rot adjacent fresh oranges.
    Return minutes until no fresh oranges remain, or -1 if impossible.
    
    Key insight: This is multi-source BFS. Start with ALL rotten oranges
    in the queue simultaneously - they all "spread" at the same rate.
    
    Example:
        [[2,1,1],      minute 0: 1 rotten      [[2,2,1],
         [1,1,0],  →   minute 1: 2 rotten  →    [2,1,0],
         [0,1,1]]      minute 2: ...            [0,1,1]]
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh_count = 0
    
    # Initialize: find all rotten oranges and count fresh ones
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))  # (row, col, time)
            elif grid[r][c] == 1:
                fresh_count += 1
    
    # Edge case: no fresh oranges
    if fresh_count == 0:
        return 0
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    max_time = 0
    
    # BFS from all rotten oranges simultaneously
    while queue:
        row, col, time = queue.popleft()
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # If we find a fresh orange, rot it
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                grid[new_row][new_col] == 1):
                
                grid[new_row][new_col] = 2  # Mark as rotten (also serves as visited)
                fresh_count -= 1
                max_time = time + 1
                queue.append((new_row, new_col, time + 1))
    
    return max_time if fresh_count == 0 else -1
```

### Example: Shortest Path with Obstacles Elimination (State-Based BFS)

Sometimes you need to track more than just position - this requires **state-based BFS**.

```python
def shortest_path(grid: List[List[int]], k: int) -> int:
    """
    LeetCode 1293: Shortest Path in a Grid with Obstacles Elimination
    
    Find shortest path from (0,0) to (rows-1, cols-1).
    You can eliminate at most k obstacles (1s).
    
    Key insight: State is (row, col, obstacles_remaining).
    We might visit the same cell multiple times with different remaining k values.
    
    Time: O(rows × cols × k)
    Space: O(rows × cols × k)
    """
    rows, cols = len(grid), len(grid[0])
    
    # Edge case: already at destination
    if rows == 1 and cols == 1:
        return 0
    
    # State: (row, col, remaining_eliminations)
    queue = deque([(0, 0, k, 0)])  # (row, col, k_left, steps)
    visited = {(0, 0, k)}
    
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        row, col, k_left, steps = queue.popleft()
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            if 0 <= new_row < rows and 0 <= new_col < cols:
                # Calculate new k value
                new_k = k_left - grid[new_row][new_col]
                
                # Check if this state is valid and unvisited
                if new_k >= 0 and (new_row, new_col, new_k) not in visited:
                    # Found destination!
                    if new_row == rows - 1 and new_col == cols - 1:
                        return steps + 1
                    
                    visited.add((new_row, new_col, new_k))
                    queue.append((new_row, new_col, new_k, steps + 1))
    
    return -1
```

---

## Pattern 3: DFS - Connected Components & Exploration

### When to Use
- Count number of islands/regions/components
- Flood fill (paint bucket tool)
- Check if path exists (when you don't need shortest)
- Explore all possibilities (with backtracking)

### DFS vs BFS for Matrix Problems

| Aspect | DFS | BFS |
|--------|-----|-----|
| Shortest path | ❌ No guarantee | ✅ Guaranteed |
| Memory | O(max depth) stack | O(width) queue |
| Implementation | Often simpler/recursive | Iterative with queue |
| Use when | Exploring, counting components | Finding distances |

### Core DFS Template (Recursive)

```python
def dfs_recursive(
    matrix: List[List[int]], 
    row: int, 
    col: int, 
    visited: Set[Tuple[int, int]]
) -> None:
    """
    Basic recursive DFS template for matrix exploration.
    """
    rows, cols = len(matrix), len(matrix[0])
    
    # Base cases: out of bounds, already visited, or obstacle
    if (row < 0 or row >= rows or 
        col < 0 or col >= cols or 
        (row, col) in visited or 
        matrix[row][col] == 0):  # 0 represents obstacle/water
        return
    
    # Mark as visited
    visited.add((row, col))
    
    # Explore all four directions
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        dfs_recursive(matrix, row + dr, col + dc, visited)
```

### Core DFS Template (Iterative)

```python
def dfs_iterative(
    matrix: List[List[int]], 
    start_row: int, 
    start_col: int
) -> Set[Tuple[int, int]]:
    """
    Iterative DFS using explicit stack.
    Useful when recursion depth might cause stack overflow.
    """
    rows, cols = len(matrix), len(matrix[0])
    visited: Set[Tuple[int, int]] = set()
    stack = [(start_row, start_col)]
    
    while stack:
        row, col = stack.pop()
        
        if (row < 0 or row >= rows or 
            col < 0 or col >= cols or 
            (row, col) in visited or 
            matrix[row][col] == 0):
            continue
        
        visited.add((row, col))
        
        # Add neighbors to stack
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            stack.append((row + dr, col + dc))
    
    return visited
```

### Example: Number of Islands

```python
def num_islands(grid: List[List[str]]) -> int:
    """
    LeetCode 200: Number of Islands
    
    '1' = land, '0' = water
    Count number of islands (connected land regions).
    
    Approach: For each unvisited land cell, do DFS to mark entire island,
    then increment count.
    
    Time: O(rows × cols)
    Space: O(rows × cols) for visited set (or O(1) if we modify grid)
    """
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    visited: Set[Tuple[int, int]] = set()
    island_count = 0
    
    def dfs(row: int, col: int) -> None:
        """Sink the entire island starting from (row, col)."""
        if (row < 0 or row >= rows or 
            col < 0 or col >= cols or 
            (row, col) in visited or 
            grid[row][col] == '0'):
            return
        
        visited.add((row, col))
        
        # Explore all four directions
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)
    
    # Main loop: find each island
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(r, c)
                island_count += 1
    
    return island_count
```

### Example: Flood Fill

```python
def flood_fill(
    image: List[List[int]], 
    sr: int, 
    sc: int, 
    color: int
) -> List[List[int]]:
    """
    LeetCode 733: Flood Fill (Paint Bucket Tool)
    
    Starting from pixel (sr, sc), change the color of all connected
    pixels with the same color to the new color.
    
    Time: O(rows × cols)
    Space: O(rows × cols) for recursion stack in worst case
    """
    rows, cols = len(image), len(image[0])
    original_color = image[sr][sc]
    
    # Edge case: new color is same as original
    if original_color == color:
        return image
    
    def dfs(row: int, col: int) -> None:
        if (row < 0 or row >= rows or 
            col < 0 or col >= cols or 
            image[row][col] != original_color):
            return
        
        # Paint this pixel
        image[row][col] = color
        
        # Recursively paint neighbors
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)
    
    dfs(sr, sc)
    return image
```

### Example: DFS with Backtracking - Find All Paths

```python
def find_all_paths(
    grid: List[List[int]], 
    start: Tuple[int, int], 
    end: Tuple[int, int]
) -> List[List[Tuple[int, int]]]:
    """
    Find ALL paths from start to end (not just shortest).
    
    Key insight: We need backtracking because we want to explore
    multiple paths, so we must UN-visit cells after exploring.
    
    Time: O(4^(rows×cols)) worst case - exponential!
    Space: O(rows × cols) for path and visited
    """
    rows, cols = len(grid), len(grid[0])
    all_paths: List[List[Tuple[int, int]]] = []
    current_path: List[Tuple[int, int]] = []
    visited: Set[Tuple[int, int]] = set()
    
    def dfs(row: int, col: int) -> None:
        # Base cases
        if (row < 0 or row >= rows or 
            col < 0 or col >= cols or 
            (row, col) in visited or 
            grid[row][col] == 1):  # 1 = obstacle
            return
        
        # Add to current path
        current_path.append((row, col))
        visited.add((row, col))
        
        # Check if we've reached the end
        if (row, col) == end:
            all_paths.append(current_path.copy())  # Save a copy!
        else:
            # Explore all directions
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(row + dr, col + dc)
        
        # BACKTRACK: remove from path and visited
        current_path.pop()
        visited.remove((row, col))
    
    dfs(start[0], start[1])
    return all_paths
```

---

## Pattern 4: Graph Transformation Problems

### When to Use
- Relationships aren't based on adjacency
- Need to merge/group entities based on shared attributes
- Problem involves equivalence relationships
- Matrix is just input format, not the actual graph structure

### The Key Insight

Some problems give you data in matrix or list format, but the **actual graph** is defined by relationships between entities, not spatial adjacency. You must **build the graph explicitly**.

### Example: Accounts Merge

```python
from collections import defaultdict
from typing import List, Dict, Set

def accounts_merge(accounts: List[List[str]]) -> List[List[str]]:
    """
    LeetCode 721: Accounts Merge
    
    Each account is [name, email1, email2, ...]
    Merge accounts that share any email.
    
    Key insight: Emails form a graph where edges connect emails in the same account.
    We need to find connected components.
    
    Approach:
    1. Build a graph where emails are connected if they appear in the same account
    2. Use DFS/BFS to find all connected components
    3. Group emails by component, attach the name
    
    Time: O(N × K × log(NK)) where N = accounts, K = max emails per account
    Space: O(N × K)
    """
    # Step 1: Build the graph
    # Edge: email1 <-> email2 if they appear in the same account
    graph: Dict[str, Set[str]] = defaultdict(set)
    email_to_name: Dict[str, str] = {}
    
    for account in accounts:
        name = account[0]
        first_email = account[1]
        
        for email in account[1:]:
            # Connect this email to the first email in the account
            # (This creates a star topology for each account)
            graph[first_email].add(email)
            graph[email].add(first_email)
            email_to_name[email] = name
    
    # Step 2: Find connected components using DFS
    visited: Set[str] = set()
    result: List[List[str]] = []
    
    def dfs(email: str, component: List[str]) -> None:
        """Collect all emails in this connected component."""
        if email in visited:
            return
        
        visited.add(email)
        component.append(email)
        
        for neighbor in graph[email]:
            dfs(neighbor, component)
    
    # Step 3: Process each component
    for email in graph:
        if email not in visited:
            component: List[str] = []
            dfs(email, component)
            
            # Format: [name, sorted_emails...]
            name = email_to_name[component[0]]
            result.append([name] + sorted(component))
    
    return result
```

### Alternative: Union-Find Approach

For problems involving merging/grouping, Union-Find is often more efficient:

```python
class UnionFind:
    """
    Disjoint Set Union (DSU) data structure with path compression
    and union by rank for near O(1) operations.
    """
    def __init__(self):
        self.parent: Dict[str, str] = {}
        self.rank: Dict[str, int] = {}
    
    def find(self, x: str) -> str:
        """Find root of x with path compression."""
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
        
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x: str, y: str) -> None:
        """Union two sets by rank."""
        root_x, root_y = self.find(x), self.find(y)
        
        if root_x == root_y:
            return
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1


def accounts_merge_union_find(accounts: List[List[str]]) -> List[List[str]]:
    """
    Accounts Merge using Union-Find.
    
    Approach:
    1. Union all emails within each account
    2. Group emails by their root
    3. Reconstruct accounts
    """
    uf = UnionFind()
    email_to_name: Dict[str, str] = {}
    
    # Step 1: Union emails and track names
    for account in accounts:
        name = account[0]
        first_email = account[1]
        
        for email in account[1:]:
            email_to_name[email] = name
            uf.union(first_email, email)
    
    # Step 2: Group emails by root
    root_to_emails: Dict[str, List[str]] = defaultdict(list)
    for email in email_to_name:
        root = uf.find(email)
        root_to_emails[root].append(email)
    
    # Step 3: Build result
    result = []
    for root, emails in root_to_emails.items():
        name = email_to_name[root]
        result.append([name] + sorted(emails))
    
    return result
```

### When to Build Explicit Graph vs Use Implicit Graph

| Scenario | Approach |
|----------|----------|
| Adjacency-based relationships | Use implicit graph (directions array) |
| Value-based relationships | Build explicit graph |
| Need to merge groups | Union-Find or DFS on explicit graph |
| Complex edge conditions | Build explicit graph with those conditions |

---

## Pattern 5: Dynamic Programming on Matrices

### When to Use
- Finding optimal value (min/max) over all paths
- Counting number of ways
- Problem has overlapping subproblems
- Can only move in limited directions (e.g., right and down only)

### Core DP Template

```python
def min_path_sum(grid: List[List[int]]) -> int:
    """
    LeetCode 64: Minimum Path Sum
    
    Find path from top-left to bottom-right with minimum sum.
    Can only move right or down.
    
    DP Definition:
    dp[i][j] = minimum sum to reach cell (i, j)
    
    Recurrence:
    dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
    
    Time: O(rows × cols)
    Space: O(cols) with optimization, O(rows × cols) without
    """
    rows, cols = len(grid), len(grid[0])
    
    # Initialize DP table
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]
    
    # Fill first row (can only come from left)
    for c in range(1, cols):
        dp[0][c] = dp[0][c-1] + grid[0][c]
    
    # Fill first column (can only come from above)
    for r in range(1, rows):
        dp[r][0] = dp[r-1][0] + grid[r][0]
    
    # Fill rest of table
    for r in range(1, rows):
        for c in range(1, cols):
            dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1])
    
    return dp[rows-1][cols-1]


def min_path_sum_optimized(grid: List[List[int]]) -> int:
    """
    Space-optimized version using only one row.
    """
    rows, cols = len(grid), len(grid[0])
    dp = [0] * cols
    
    for r in range(rows):
        for c in range(cols):
            if r == 0 and c == 0:
                dp[c] = grid[0][0]
            elif r == 0:
                dp[c] = dp[c-1] + grid[r][c]
            elif c == 0:
                dp[c] = dp[c] + grid[r][c]
            else:
                dp[c] = grid[r][c] + min(dp[c], dp[c-1])
    
    return dp[cols-1]
```

### Example: Unique Paths with Obstacles

```python
def unique_paths_with_obstacles(obstacle_grid: List[List[int]]) -> int:
    """
    LeetCode 63: Unique Paths II
    
    Count paths from top-left to bottom-right avoiding obstacles.
    0 = empty, 1 = obstacle
    
    DP Definition:
    dp[i][j] = number of ways to reach cell (i, j)
    
    Recurrence:
    If obstacle: dp[i][j] = 0
    Else: dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    Time: O(rows × cols)
    Space: O(cols)
    """
    rows, cols = len(obstacle_grid), len(obstacle_grid[0])
    
    # Edge case: start or end is blocked
    if obstacle_grid[0][0] == 1 or obstacle_grid[rows-1][cols-1] == 1:
        return 0
    
    dp = [0] * cols
    dp[0] = 1
    
    for r in range(rows):
        for c in range(cols):
            if obstacle_grid[r][c] == 1:
                dp[c] = 0  # Can't reach obstacle
            elif c > 0:
                dp[c] += dp[c-1]  # Add paths from left
            # dp[c] already has paths from above
    
    return dp[cols-1]
```

### Example: Maximal Square

```python
def maximal_square(matrix: List[List[str]]) -> int:
    """
    LeetCode 221: Maximal Square
    
    Find the largest square containing only 1s, return its area.
    
    DP Definition:
    dp[i][j] = side length of largest square with bottom-right corner at (i, j)
    
    Recurrence:
    If matrix[i][j] == '0': dp[i][j] = 0
    Else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    Visual intuition: To extend a square, we need:
    - Cell above to be part of a square
    - Cell to left to be part of a square  
    - Cell diagonal to be part of a square
    The limiting factor is the smallest of these three.
    
    Time: O(rows × cols)
    Space: O(cols)
    """
    if not matrix or not matrix[0]:
        return 0
    
    rows, cols = len(matrix), len(matrix[0])
    dp = [0] * cols
    max_side = 0
    prev_diagonal = 0  # dp[r-1][c-1] from previous iteration
    
    for r in range(rows):
        for c in range(cols):
            temp = dp[c]  # Save before overwriting (this becomes prev_diagonal)
            
            if matrix[r][c] == '0':
                dp[c] = 0
            elif r == 0 or c == 0:
                dp[c] = 1
            else:
                dp[c] = 1 + min(dp[c], dp[c-1], prev_diagonal)
            
            max_side = max(max_side, dp[c])
            prev_diagonal = temp
    
    return max_side * max_side
```

---

## Common Pitfalls & Edge Cases

### 1. Off-by-One Errors in Bounds Checking

```python
# ❌ WRONG: Using <= instead of <
if row <= len(matrix) and col <= len(matrix[0]):  # Index out of bounds!

# ✅ CORRECT: Strict inequality
if row < len(matrix) and col < len(matrix[0]):
```

### 2. Forgetting to Check Empty Matrix

```python
# ✅ Always check at the start
def solution(matrix):
    if not matrix or not matrix[0]:
        return 0  # or appropriate default
    
    rows, cols = len(matrix), len(matrix[0])
    # ... rest of solution
```

### 3. Modifying Matrix vs Using Visited Set

```python
# Approach 1: Modify matrix (saves space, but destructive)
def dfs_modify(matrix, r, c):
    if matrix[r][c] == 0:
        return
    matrix[r][c] = 0  # Mark visited by changing value
    # ... continue DFS

# Approach 2: Separate visited set (preserves matrix)
def dfs_visited(matrix, r, c, visited):
    if (r, c) in visited:
        return
    visited.add((r, c))
    # ... continue DFS

# Use Approach 2 when:
# - You need to preserve the original matrix
# - You might need to "unvisit" (backtracking)
# - Multiple traversals with different visited states
```

### 4. BFS: Adding to Visited at Wrong Time

```python
# ❌ WRONG: Mark visited when popping
while queue:
    row, col = queue.popleft()
    if (row, col) in visited:  # Too late! Duplicates already in queue
        continue
    visited.add((row, col))

# ✅ CORRECT: Mark visited when adding to queue
while queue:
    row, col = queue.popleft()
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if (new_row, new_col) not in visited:
            visited.add((new_row, new_col))  # Mark immediately!
            queue.append((new_row, new_col))
```

### 5. Forgetting to Handle Diagonals When Needed

```python
# Check problem statement carefully!
# "Adjacent" sometimes means 4 directions, sometimes 8

# 4-directional (most common)
directions = [(0,1), (0,-1), (1,0), (-1,0)]

# 8-directional (when diagonals count)
directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
```

### 6. State-Based BFS: Insufficient State Tracking

```python
# ❌ WRONG: Only tracking position when state matters
visited = {(start_row, start_col)}

# ✅ CORRECT: Track full state tuple
visited = {(start_row, start_col, initial_keys, initial_walls_broken)}
```

---

## Quick Reference Cheat Sheet

### Decision Tree

```
Is this a matrix problem?
│
├── Need SHORTEST PATH?
│   └── YES → BFS (with state if needed)
│
├── Need to COUNT REGIONS/COMPONENTS?
│   └── YES → DFS (simpler) or BFS
│
├── Need ALL PATHS or EXPLORE ALL?
│   └── YES → DFS with backtracking
│
├── Relationships NOT based on adjacency?
│   └── YES → Build explicit graph, then DFS/BFS/Union-Find
│
├── Need OPTIMAL VALUE (with constraints)?
│   └── YES → DP (if limited directions) or Dijkstra (if varied costs)
│
└── Special traversal order?
    └── YES → Careful index manipulation
```

### Complexity Quick Reference

| Algorithm | Time | Space | Use For |
|-----------|------|-------|---------|
| BFS | O(V + E) = O(rows × cols) | O(V) = O(rows × cols) | Shortest path, level order |
| DFS | O(V + E) = O(rows × cols) | O(V) stack | Components, all paths |
| DP (2D) | O(rows × cols) | O(rows × cols) or O(cols) | Optimal paths, counting |
| Union-Find | O(α(n)) ≈ O(1) per op | O(n) | Merging groups |

### Common Patterns at a Glance

```python
# BFS Template
from collections import deque
queue = deque([(start_r, start_c, 0)])  # (row, col, distance)
visited = {(start_r, start_c)}
while queue:
    r, c, dist = queue.popleft()
    for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
        nr, nc = r + dr, c + dc
        if valid(nr, nc) and (nr, nc) not in visited:
            visited.add((nr, nc))
            queue.append((nr, nc, dist + 1))

# DFS Template
def dfs(r, c, visited):
    if not valid(r, c) or (r, c) in visited:
        return
    visited.add((r, c))
    for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
        dfs(r + dr, c + dc, visited)

# DP Template (right/down only)
dp = [[0] * cols for _ in range(rows)]
dp[0][0] = grid[0][0]
for r in range(rows):
    for c in range(cols):
        if r > 0: dp[r][c] = f(dp[r][c], dp[r-1][c])
        if c > 0: dp[r][c] = f(dp[r][c], dp[r][c-1])
```

---

## Practice Problems by Pattern

### Simple Traversal
- [48. Rotate Image](https://leetcode.com/problems/rotate-image/)
- [54. Spiral Matrix](https://leetcode.com/problems/spiral-matrix/)
- [73. Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/)

### BFS (Shortest Path)
- [994. Rotting Oranges](https://leetcode.com/problems/rotting-oranges/)
- [1091. Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/)
- [1293. Shortest Path with Obstacles Elimination](https://leetcode.com/problems/shortest-path-in-a-grid-with-obstacles-elimination/)
- [542. 01 Matrix](https://leetcode.com/problems/01-matrix/)

### DFS (Components/Exploration)
- [200. Number of Islands](https://leetcode.com/problems/number-of-islands/)
- [695. Max Area of Island](https://leetcode.com/problems/max-area-of-island/)
- [733. Flood Fill](https://leetcode.com/problems/flood-fill/)
- [79. Word Search](https://leetcode.com/problems/word-search/)
- [130. Surrounded Regions](https://leetcode.com/problems/surrounded-regions/)

### Graph Transformation
- [721. Accounts Merge](https://leetcode.com/problems/accounts-merge/)
- [684. Redundant Connection](https://leetcode.com/problems/redundant-connection/)
- [547. Number of Provinces](https://leetcode.com/problems/number-of-provinces/)

### DP on Matrices
- [62. Unique Paths](https://leetcode.com/problems/unique-paths/)
- [64. Minimum Path Sum](https://leetcode.com/problems/minimum-path-sum/)
- [221. Maximal Square](https://leetcode.com/problems/maximal-square/)
- [1314. Matrix Block Sum](https://leetcode.com/problems/matrix-block-sum/)

---

*Remember: The pattern matters more than memorizing solutions. When you see a matrix problem, first identify WHAT you're looking for, then match it to the appropriate pattern.*
