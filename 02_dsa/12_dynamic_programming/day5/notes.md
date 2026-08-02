# Grid DP & 2D States

## 1. The Anatomy of Grid DP

**Grid DP** shifts the environment from a linear 1D array to a 2D matrix structure. Instead of evaluating sequence elements left-to-right, we evaluate physical coordinate cells, typically traversing from the top-left corner `(0, 0)` to the bottom-right corner `(m-1, n-1)`. 

While the data structures physically appear different, the algorithmic DNA is identical to 1D DP: the optimal answer for the current cell is derived exclusively from the optimal answers of its immediate adjacent neighbors.

---

## 2. Grid States & Movement Vectors

In Grid DP, the state requires two tracking parameters because we operate in a 2D coordinate system.

> **The Universal Grid State Definition:**
> `dp[i][j]` represents the optimal mathematical answer when traversing from the starting origin exactly up to the cell at `(i, j)`.

### Movement Constraints dictates Dependencies
The rules of traversal defined by the problem completely dictate our DP state dependencies. 
If a problem states: *"You can only move DOWN or RIGHT"*, then to reach cell `(i, j)`, we must have physically stepped from either:
1. The cell directly above: `(i-1, j)` (moving DOWN)
2. The cell directly left: `(i, j-1)` (moving RIGHT)

Therefore, `dp[i][j]` is entirely dependent on `dp[i-1][j]` and `dp[i][j-1]`.

---

## 3. Boundary Cells & Initialization

The most common failure point in Grid DP is stepping out of bounds. The top row `(i=0)` has no cells above it. The left column `(j=0)` has no cells to its left. 

We have two architectural choices to handle boundaries safely:
1. **Explicit Initialization:** Manually pre-compute and fill the entire 0th row and 0th column before running the main nested loop starting from `(1, 1)`.
2. **Padding / Matrix Expansion:** Expand the DP array to size `(m+1) x (n+1)` and initialize the dummy 0th row/col with neutral values (`0` for counting, `inf` for minimums). The physical grid then maps from `1` to `m/n`.

---

## 4. Space Compression (The O(N) Revolution)

A full DP matrix requires $O(M \cdot N)$ memory space. However, if our traversal rule is strictly "DOWN or RIGHT", calculating the current row `i` only ever requires looking at the immediately preceding row `i-1`. We do not need the historical data from rows `i-2`, `i-3`, etc.

We can completely crush the spatial footprint by utilizing a single 1D array of size `N`.
* `dp[j]` represents the value directly above us (from row `i-1`).
* `dp[j-1]` represents the value directly to our left (from the current row `i` that we just updated).

```python
# The 1D Space Compression Transition
dp[j] = grid[i][j] + min(dp[j], dp[j-1])
```

---

## Problem: Unique Paths (62)

* **Interview Difficulty:** Easy
* **Parent Pattern:** Counting Grid DP
* **Problem Type:** Path Combinatorics
* **Data Structure Used:** 1D Space-Optimized Array (`list[int]`)
* **Brute Force:** Pure recursive DFS branching into `dfs(i+1, j)` and `dfs(i, j+1)`. Time Complexity: $O(2^{M+N})$.
* **Optimized Approach:** Because we only care about the total *number* of unique paths, and movement is restricted to DOWN and RIGHT, the number of ways to enter a cell is simply the sum of the ways to enter the cell above it and the cell to its left. We deploy a 1D array of size $N$ initialized entirely to `1` (representing the top boundary row).

### DP State
`dp[i][j]` represents the **total number of distinct unique paths starting from `(0,0)` and terminating exactly at cell `(i, j)`**.

### State Flow
```text
STATE: dp[i][j] = total distinct paths to cell (i, j).

↓

CHOICES for reaching (i, j):
  Come from ABOVE: path count is dp[i-1][j]
  Come from LEFT: path count is dp[i][j-1]

↓

TRANSITION: dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

### Recurrence
$$\text{dp}[j] = \text{dp}[j] + \text{dp}[j-1]$$
*(Using 1D Space Compression: `dp[j]` acts as top, `dp[j-1]` acts as left).*

### Base Cases
* `dp[0][j] = 1` for all `j` (Top edge can only be traversed by moving strictly right).
* `dp[i][0] = 1` for all `i` (Left edge can only be traversed by moving strictly down).

### Traversal Order
**Left to Right, Top to Bottom (Rows `1` to `M-1`, Cols `1` to `N-1`).**

### Pointer Flow
```text
Grid 3x3.
Base 1D array representing row 0: dp = [1, 1, 1]

Row 1 calculation:
  j=1: dp[1] = dp[1] + dp[0] -> 1 + 1 = 2
  j=2: dp[2] = dp[2] + dp[1] -> 1 + 2 = 3
  dp array state: [1, 2, 3]

Row 2 calculation:
  j=1: dp[1] = dp[1] + dp[0] -> 2 + 1 = 3
  j=2: dp[2] = dp[2] + dp[1] -> 3 + 3 = 6
  dp array state: [1, 3, 6]

Final Answer at dp[2] = 6.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(M * N) (Full grid traversal)     │
│  Space Complexity │ O(N) (1D optimized array row)      │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Operating inside a 2D physical grid constraint.
* ✓ Problem requests "total number of ways" (Counting metric).
* ✓ Movement is strictly directional (no backtracking/cycles).
* $\rightarrow$ **Counting Grid DP**

### Core Insight
Grid combinatorics follow a direct translation of Pascal's Triangle mapped onto a Cartesian plane. We don't need to generate the paths; we just inherit the sum of incoming vectors.

### Mistakes Made
* Initially, we attempted to map a full $M \times N$ matrix. While correct, it wastes $O(M \cdot N)$ memory. Recognizing that `dp[i][j]` only requests data from row `i` and row `i-1` allowed us to immediately flatten the architecture to $O(N)$.

### What I Learned
A 1D array naturally stores the "row above" in `dp[j]` until the exact moment we overwrite it. The cell to our left `dp[j-1]` is naturally updated just milliseconds prior during the same loop pass. The architecture flawlessly self-regulates.

---

## Problem: Unique Paths II (63)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Obstacle Grid DP
* **Problem Type:** Path Combinatorics with Invalid States
* **Data Structure Used:** 1D Space-Optimized Array (`list[int]`)
* **Brute Force:** Recursive DFS that simply returns `0` upon hitting an obstacle coordinate. Time: $O(2^{M+N})$.
* **Optimized Approach:** Identical architecture to Unique Paths 1, but we inject a condition gate. If the physical grid contains an obstacle `1` at `(i, j)`, we immediately override the DP cell to `0`. A value of `0` ensures that any downstream cells checking this coordinate inherit `0` paths, naturally pruning the blocked branch.

### DP State
`dp[i][j]` represents the **total number of distinct unique paths terminating exactly at cell `(i, j)` without traversing any obstacles**.

### State Flow
```text
STATE: dp[i][j] = total distinct paths to cell (i, j).

↓

CHOICES for reaching (i, j):
  If grid[i][j] is an Obstacle (1):
    Paths = 0 (Dead end)
  Else:
    Paths = dp[i-1][j] (from above) + dp[i][j-1] (from left)

↓

TRANSITION: dp[j] = 0 (if obstacle) OR dp[j] + dp[j-1]
```

### Recurrence
$$\text{dp}[j] = \begin{cases} 0 & \text{if obstacle} \\ \text{dp}[j] + \text{dp}[j-1] & \text{otherwise} \end{cases}$$

### Base Cases
* If `grid[0][0] == 1` or `grid[m-1][n-1] == 1`, return `0` immediately (Start or End is blocked).
* `dp[0] = 1`.

### Traversal Order
**Left to Right, Top to Bottom (Rows `0` to `M-1`, Cols `0` to `N-1`).**

### Pointer Flow
```text
Grid 3x3 with obstacle at (1,1): [[0,0,0],[0,1,0],[0,0,0]]
Base 1D array: dp = [1, 0, 0]

Row 0 calculation:
  j=0: Valid -> dp[0] = 1
  j=1: dp[1] += dp[0] -> 1
  j=2: dp[2] += dp[1] -> 1
  dp array state: [1, 1, 1]

Row 1 calculation:
  j=0: Valid -> dp[0] = 1
  j=1: Obstacle! -> dp[1] = 0   <-- Pruned!
  j=2: Valid -> dp[2] += dp[1] -> 1 + 0 = 1
  dp array state: [1, 0, 1]

Row 2 calculation:
  j=0: Valid -> dp[0] = 1
  j=1: Valid -> dp[1] += dp[0] -> 0 + 1 = 1
  j=2: Valid -> dp[2] += dp[1] -> 1 + 1 = 2
  dp array state: [1, 1, 2]
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(M * N)                           │
│  Space Complexity │ O(N) (1D optimized array row)      │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Grid traversal combinatorics.
* ✓ Physical barriers block standard transition inheritance.
* $\rightarrow$ **Obstacle Grid DP**

### Core Insight
Obstacles do not require complex path-routing algorithms. By forcing the DP state at the obstacle's coordinate to `0`, the mathematics naturally annihilate any combinatorial branches that attempt to cross it.

### Mistakes Made
* We failed to check if the starting coordinate `(0,0)` itself was an obstacle before executing the loop. If the origin is blocked, the total paths must be identically `0` regardless of the rest of the matrix.

### What I Learned
In space-compressed grid setups, obstacles require an explicit override assignment (`dp[j] = 0`). If we merely `continue` or skip the addition step, `dp[j]` will falsely retain the path count from the row directly above it, effectively allowing paths to ghost through the wall.

---

## Problem: Minimum Path Sum (64)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Minimum Grid DP
* **Problem Type:** Min Cost Pathfinding
* **Data Structure Used:** 1D Space-Optimized Array (`list[int]`) initialized with `infinity`.
* **Brute Force:** DFS evaluating every path sum, tracking the global minimum. Time: $O(2^{M+N})$.
* **Optimized Approach:** We shift from a combinatorial `+` operation to an optimization `min()` operation. The cost to reach any cell is the physical value inside that cell PLUS the minimum cost of the two valid entry vectors (above or left).

### DP State
`dp[i][j]` represents the **absolute minimum sum accumulated along a valid path terminating exactly at cell `(i, j)`**.

### State Flow
```text
STATE: dp[i][j] = min path sum to cell (i, j).

↓

CHOICES for reaching (i, j):
  Path from ABOVE: cost is dp[i-1][j]
  Path from LEFT: cost is dp[i][j-1]
  (We MUST take the minimum of these two incoming vectors)

↓

TRANSITION: dp[j] = grid[i][j] + min(dp[j], dp[j-1])
```

### Recurrence
$$\text{dp}[j] = \text{grid}[i][j] + \min(\text{dp}[j], \; \text{dp}[j-1])$$

### Base Cases
* `dp[0] = grid[0][0]` (Cost to stand on the origin is just the origin's value).
* Boundary row `0` relies exclusively on values from its left. Boundary column `0` relies exclusively on values from above.

### Traversal Order
**Left to Right, Top to Bottom (Rows `1` to `M-1`, Cols `1` to `N-1`).**

### Pointer Flow
```text
Grid: [[1,3,1],
       [1,5,1]]

Pre-process Row 0 (only leftward movement possible):
  dp = [1, 4, 5]

Process Row 1:
  j=0: Only from above -> dp[0] += grid[1][0] -> 1 + 1 = 2
  j=1: min(dp[1] (above=4), dp[0] (left=2)) + 5 -> 2 + 5 = 7. dp = [2, 7, 5]
  j=2: min(dp[2] (above=5), dp[1] (left=7)) + 1 -> 5 + 1 = 6. dp = [2, 7, 6]

Final Answer: dp[2] = 6.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(M * N)                           │
│  Space Complexity │ O(N) (1D optimized array row)      │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Operating inside a 2D physical grid.
* ✓ Problem requests the "minimum cost" or "shortest distance".
* ✓ Cells possess varied weights/values.
* $\rightarrow$ **Min Cost Grid DP**

### Core Insight
Grid optimization separates the *current cell penalty* from the *historical path penalty*. The formula elegantly isolates the local cost (`grid[i][j]`) from the optimal historical decision (`min(above, left)`).

### Mistakes Made
* We tried to use `0` as the initialization padding for boundaries. Because the transition utilizes `min()`, initializing outer boundaries to `0` falsely pulls paths outside the grid. Optimization boundaries must ALWAYS be initialized to an infinity proxy (`float('inf')`).

### What I Learned
Pre-processing the 0th row explicitly outside the main loop is significantly cleaner and less error-prone than embedding complex boundary `if/else` checks deep inside the inner double-loop block.

---

## Problem: Triangle (120)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Variable-width Grid DP
* **Problem Type:** Unstructured Grid Pathfinding
* **Data Structure Used:** 1D DP Array initialized to the bottom row of the triangle.
* **Brute Force:** DFS tracking indices from the apex downwards. Time: $O(2^N)$.
* **Optimized Approach:** Instead of a strict Cartesian grid, we face a jagged structure where row widths expand. If we process Top-Down, we are forced to execute complex out-of-bounds checks for the expanding left and right edges. If we flip the architecture and process **Bottom-Up**, we completely eliminate boundary edge cases because a narrower top row mathematically guarantees its children exist in the wider row below it.

### DP State
`dp[i]` represents the **minimum path sum from the current tier down to the absolute bottom of the triangle**.

### State Flow
```text
STATE: dp[i] = min sum to reach bottom from index i.

↓

CHOICES moving downwards from (row, i):
  Step to Left Child: cost is dp[i] (from row below)
  Step to Right Child: cost is dp[i+1] (from row below)

↓

TRANSITION: dp[i] = triangle[row][i] + min(dp[i], dp[i+1])
```

### Recurrence
$$\text{dp}[i] = \text{triangle}[\text{row}][i] + \min(\text{dp}[i], \; \text{dp}[i+1])$$

### Base Cases
* `dp` array is identically initialized as the raw elements of the final bottom row of the triangle.

### Traversal Order
**Bottom to Top (Rows `N-2` down to `0`, Cols `0` to `width of row`).**

### Pointer Flow
```text
Triangle: [[2], [3,4], [6,5,7], [4,1,8,3]]

Initialization (Bottom Row): dp = [4, 1, 8, 3]

Process Row 2 [6, 5, 7]:
  i=0: 6 + min(4, 1) = 7
  i=1: 5 + min(1, 8) = 6
  i=2: 7 + min(8, 3) = 10
  dp state = [7, 6, 10, 3]

Process Row 1 [3, 4]:
  i=0: 3 + min(7, 6) = 9
  i=1: 4 + min(6, 10) = 10
  dp state = [9, 10, 10, 3]

Process Row 0 [2]:
  i=0: 2 + min(9, 10) = 11.
  
Final Answer: dp[0] = 11.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^2) (Total elements in triangle)│
│  Space Complexity │ O(N) (1D array sized for bottom row│
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Grid-like structure with expanding/variable width boundaries.
* ✓ Path finding rules restrict movement to specific diagonal elements.
* $\rightarrow$ **Variable-width Reverse Grid DP**

### Core Insight
Top-Down traversal requires answering "Where did I come from?", forcing us to check if edges exist. Bottom-Up traversal answers "Where can I go?", which is universally valid because the triangle organically expands downwards.

### Mistakes Made
* We attempted to solve it Top-Down, triggering `IndexError` crashes on the far-right diagonal edges because the row above it was narrower than the current row.

### What I Learned
In hierarchical tree/triangle structures, inverting the DP traversal direction from Top-Down to Bottom-Up effortlessly destroys edge-case boundary logic.

---

## Problem: Maximal Square (221)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Neighbour-based Grid DP
* **Problem Type:** 2D Geometric Constraint Maximization
* **Data Structure Used:** 1D DP Array tracking square edge limits + scalar `prev` for diagonal tracking.
* **Brute Force:** From every '1' in the matrix, verify the entire area expanding outward. Time: $O((M \cdot N)^2)$.
* **Optimized Approach:** To form a square of size $K$ ending at bottom-right corner `(i, j)`, we must absolutely possess valid squares of size $K-1$ at our top, our left, and our top-left diagonal. If any of those three neighboring regions are structurally deficient, the larger square collapses to the size of the smallest neighbor. 

### DP State
`dp[i][j]` represents the **maximum physical edge length of a square whose absolute bottom-right corner terminates at `(i, j)`**.

### State Flow
```text
STATE: dp[i][j] = max edge length of square ending here.

↓

CHOICES for extending a square at (i, j):
  If grid[i][j] == '0', a square cannot terminate here -> dp = 0.
  If grid[i][j] == '1', a square is possible.
  Check 3 structural anchors:
    1. Top (dp[i-1][j])
    2. Left (dp[i][j-1])
    3. Top-Left Diagonal (dp[i-1][j-1])
  
  The maximum square we can build is bottlenecked by the WEAKEST structural anchor!

↓

TRANSITION: dp[j] = min(top, left, diagonal) + 1
```

### Recurrence
$$\text{dp}[j] = \min(\text{dp}[j], \text{dp}[j-1], \text{prev\_diagonal}) + 1$$

### Base Cases
* If `grid[i][j] == '0'`, `dp[j] = 0`.
* A `1` floating in the top row or left column has no valid top/left neighbors, creating a base square of size `1`.

### Traversal Order
**Left to Right, Top to Bottom (Rows `1` to `M`, Cols `1` to `N`).** (Requires 1-indexed padding to prevent out of bounds).

### Pointer Flow
*(Due to the 3-neighbor dependency, we maintain `prev` to cache `dp[i-1][j-1]` before it gets overwritten).*
```text
Grid: 
1 1
1 1

Row 1 processing: dp = [0, 1, 1]
Row 2 processing:
  j=1: matrix='1'. min(top=1, left=0, diag=0) + 1 = 1. dp = [0, 1, 1]
  j=2: matrix='1'. min(top=1, left=1, diag=1) + 1 = 2. dp = [0, 1, 2]

Max side length observed = 2. Area = 2 * 2 = 4.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(M * N)                           │
│  Space Complexity │ O(N) (1D optimized array + 1 var)  │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Seeking largest physical block/square in a binary matrix.
* ✓ Sub-problems require evaluating more than 2 orthogonal axes.
* $\rightarrow$ **Neighbour-based Grid DP**

### Core Insight
A geometric square is constrained by its weakest internal quadrant. The `min(top, left, diagonal)` operation mathematically mirrors the physical reality that a $3 \times 3$ square cannot exist unless a perfect $2 \times 2$ square exists in all three overlapping neighbor coordinates.

### Mistakes Made
* We executed the 1D space optimization but forgot to cache the `dp[j]` variable before updating it. Because we need the top-left diagonal, overwriting `dp[j]` destroys the diagonal data required for the next `j+1` calculation. Introducing the temporary `prev` scalar resolves this entirely.

### What I Learned
When a grid transition equation relies on the diagonal coordinate `(i-1, j-1)`, standard 1D space compression fails unless we explicitly implement a single scalar variable (`prev`) to buffer the old value right before it is overwritten by the local row assignment.

---

## Problem: Dungeon Game (174)

* **Interview Difficulty:** Hard
* **Parent Pattern:** Reverse Grid DP
* **Problem Type:** Threshold Feasibility Pathfinding
* **Data Structure Used:** 1D DP Array initialized to `infinity` (padded to size $N+1$).
* **Brute Force:** Top-down recursive DFS evaluating minimum health tracking bounds. Time: $O(2^{M+N})$.
* **Optimized Approach:** If we start traversing from the top-left Knight origin, our DP state faces two mathematically conflicting unknown variables: we need to track the absolute path sum, but we ALSO need to track the deepest negative dip (which dictates our starting health threshold). 
To collapse two unknowns into one, we reverse the perspective. We start at the bottom-right Princess coordinate and ask: *"What is the absolute minimum health required to survive moving BACKWARDS to the current cell?"*

### DP State
`dp[i][j]` represents the **minimum health threshold required to survive the journey starting from cell `(i, j)` and terminating at the Princess**.

### State Flow
```text
STATE: dp[i][j] = min HP required to survive path from here to the end.

↓

CHOICES moving towards the Princess from (i, j):
  Step DOWN: we must survive current cell + health needed for cell below (dp[i+1][j]).
  Step RIGHT: we must survive current cell + health needed for cell right (dp[i][j+1]).
  (We take the path requiring the MINIMUM future health).

↓

TRANSITION: min_hp_needed = min(down, right) - dungeon[i][j]
            dp[j] = max(1, min_hp_needed)
```

### Recurrence
$$\text{dp}[j] = \max(1, \; \min(\text{dp}[j], \text{dp}[j+1]) - \text{dungeon}[i][j])$$

### Base Cases
* If `min_health_needed <= 0` (because a potion healed us massively), our DP state must reset to `1`. A Knight must eternally maintain a minimum of `1` HP to stay alive. A required starting HP of `0` or `-5` is physically invalid.
* Dummy boundaries to the immediate right and bottom of the Princess cell are hardcoded to require `1` HP to force the Princess cell to evaluate strictly against its own local penalty.

### Traversal Order
**Bottom-Right to Top-Left (Rows `M-1` down to `0`, Cols `N-1` down to `0`).**

### Pointer Flow
```text
Dungeon: [[-2, -3,  3],
          [-5, -10, 1],
          [10,  30,-5]]

Dummy initialization for bottom boundary: dp = [inf, inf, inf, 1]

Process Row 2 (Bottom):
  j=2 (-5): max(1, min(inf, 1) - (-5)) = 6. (Takes 6 HP to survive Princess).
  j=1 (30): max(1, min(inf, 6) - 30) = 1. (Potion heals for 30, resets to 1).
  j=0 (10): max(1, min(inf, 1) - 10) = 1.
  dp array state: [1, 1, 6, inf]

Process Row 1:
  j=2 (1) : max(1, min(6, inf) - 1) = 5
  j=1 (-10): max(1, min(1, 5) - (-10)) = 11
  j=0 (-5): max(1, min(1, 11) - (-5)) = 6
  dp array state: [6, 11, 5, inf]

Process Row 0 (Top):
  j=2 (3) : max(1, min(5, inf) - 3) = 2
  j=1 (-3): max(1, min(11, 2) - (-3)) = 5
  j=0 (-2): max(1, min(6, 5) - (-2)) = 7

Final Answer at dp[0] = 7 starting HP required.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(M * N)                           │
│  Space Complexity │ O(N) (1D padding right boundary)   │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Operating inside a 2D physical grid with varied numerical weights.
* ✓ Prompt requires a threshold/baseline guarantee (e.g., minimum starting value, health, fuel) to survive the sequence.
* $\rightarrow$ **Reverse Grid DP**

### Core Insight
When a grid pathfinding state requires tracking both a sum accumulation *and* a critical threshold threshold barrier concurrently, flipping the traversal direction from End-to-Start seamlessly collapses the dual-variable conflict into a single optimization metric.

### Mistakes Made
* We originally processed the array Top-Down. We tracked the minimum HP seen so far, but were paralyzed when encountering a branch that required massive initial HP but resulted in a huge potion at the end, vs a branch with tiny initial HP drops but no potions. Top-Down logic fundamentally cannot resolve this paradox without generating $O(2^N)$ state permutations.

### What I Learned
Boundary management on Reverse Grid DP requires surgical precision. We must reset the dummy right-boundary padding cell `dp[n]` to `infinity` at the absolute conclusion of every row iteration loop. If we forget, rows sitting physically higher than the Princess will falsely attempt to use the dummy boundary as a valid $1$ HP "escape route" off the map.

---

### Master Patterns Learned

#### 1. The Space-Crushed 1D Grid Matrix
* **The Strategy:** Deploy this spatial layout for any Grid DP problem restricting vectors to orthogonal forward movements (DOWN, RIGHT).
* **The Conceptual Mechanics:** Because row `i` only ever accesses data from row `i-1`, the $O(M \cdot N)$ matrix collapses into an $O(N)$ row block. `dp[j]` represents the cell ABOVE; `dp[j-1]` represents the cell to the LEFT.

#### 2. Reverse Threshold Mapping
* **The Strategy:** Apply this to grid systems mandating a survival threshold or minimum starting fuel. 
* **The Conceptual Mechanics:** Reverse the iteration loops to anchor at the destination. This completely nullifies the necessity of tracking historical accumulation drops, as the mathematics now cleanly represent exactly what is required to survive the journey moving forward.

#### 3. Obstacle & Dead-End Pruning
* **The Strategy:** Handle impassable terrain immediately at the transition level.
* **The Conceptual Mechanics:** Do not write complex router bounds. Simply evaluate `if obstacle: dp[j] = 0`. The integer `0` organically cascades through all mathematical `+` and `min()` combinations, flawlessly neutralizing dead branches without bespoke pathfinding logic.
