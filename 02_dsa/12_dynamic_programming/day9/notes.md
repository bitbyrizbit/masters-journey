# Bitmask DP & State Compression

## 1. The Anatomy of Bitmask DP

Bitmask Dynamic Programming is widely considered one of the hardest classical DP families. It is deployed when the "State" of the problem requires tracking exactly which items from a small, finite set have been used or visited.

Normally, tracking the exact presence of $N$ items would require an array or a hash set: `visited = [True, False, True, False]`. However, using arrays as state keys is mechanically slow and memory-intensive. 
Because binary integers naturally consist of $0$s and $1$s, we can **compress** an entire boolean array into a single integer. 

The binary number `1010` (Integer `10`) perfectly represents that items at index `1` and index `3` are currently active, while items at `0` and `2` are inactive. This scalar integer is called a **Bitmask**.

---

## 2. Core Bitwise Operations (The Toolkit)

To manipulate our compressed state, we must use raw CPU bitwise operators. 

Let `mask` be our state integer, and `i` be the target index (0-indexed).

| Objective | Logic | Bitwise Code |
| :--- | :--- | :--- |
| **Check** if item `i` is active | Bitwise AND with a shifted `1` | `(mask & (1 << i)) != 0` |
| **Turn ON** item `i` | Bitwise OR with a shifted `1` | `new_mask = mask | (1 << i)` |
| **Turn OFF** item `i` | Bitwise AND with a negated shifted `1` | `new_mask = mask & ~(1 << i)` |
| **Check if ALL** $N$ items are on | Compare to $2^N - 1$ | `mask == (1 << n) - 1` |

---

## 3. The Performance Threshold

Because an array of size $N$ generates $2^N$ possible bitmask combinations, Bitmask DP algorithms operate at $O(2^N)$ state space. This hardcodes a strict physical limit on when this pattern can be applied.

> **The Bitmask Feasibility Rule:**
> Bitmask DP is almost exclusively deployed when $N \le 20$. If $N > 25$, the state space ($2^{25} \approx 33$ million states) will trigger a Time Limit Exceeded (TLE) error. If you see $N \le 16$ in the constraints, it is virtually a mathematical guarantee that the problem requires Bitmask DP.

---

## Problem: Partition to K Equal Sum Subsets (698)

* **Interview Difficulty:** Hard
* **Parent Pattern:** Mask Combinatorics
* **Problem Type:** Subset Packing
* **Data Structure Used:** Dictionary (`memo`) storing solved bitmask integers.
* **Brute Force:** Backtracking trying to place every number into `K` buckets. Time: $O(K^N)$.
* **Optimized Approach:** We calculate the required `target_sum = sum(nums) / K`. Our state is simply a bitmask representing which numbers have already been packed into buckets. The DP loop iterates over all available numbers. If adding an available number perfectly hits the `target_sum`, the next level of recursion starts a brand new bucket (resetting `current_sum` to `0`). We cache the boolean feasibility of the bitmask to aggressively prune duplicate permutations.

### DP State
`dfs(mask, current_sum)` returns `True` if it is physically possible to perfectly partition all remaining available numbers (defined by `mask`) into valid buckets.

### State Flow
```text
STATE: memo[mask] = True/False

↓

CHOICES for number at index `i`:
  If `mask & (1 << i)` is 0 (Number is AVAILABLE):
    Try adding it: new_sum = current_sum + nums[i]
    
    If new_sum < target:
      Recurse with updated mask and updated sum.
      
    If new_sum == target:
      A bucket is perfectly filled! 
      Recurse with updated mask, but reset sum to 0 for the next bucket.

↓

TRANSITION: If any choice yields True, memo[mask] = True.
```

### Recurrence
(Implemented implicitly via the recursive branching logic returning boolean ORs).

### Base Cases
* If `total_sum % K != 0`, return `False` immediately.
* If `mask == (1 << n) - 1`, all numbers are successfully used. Return `True`.

### Traversal Order
**Top-Down Recursive DFS.** Start with an empty mask (`0`) and sum (`0`), mutating bits until the mask hits full capacity.

### Pointer Flow
```text
nums = [4, 3, 2, 3, 5, 2, 1], K = 4. Target = 5.
Sorted Descending: [5, 4, 3, 3, 2, 2, 1] (Massive heuristic optimization)

mask = 0 (0000000)

i=0 (num=5): 
  Available! new_sum = 0 + 5 = 5 (Hits Target!)
  Bucket full. Recursion -> next_sum = 0. new_mask = 1 (0000001)

mask = 1 (0000001)
i=0 (num=5): Unavailable (bit 0 is 1).
i=1 (num=4): 
  Available! new_sum = 0 + 4 = 4. 
  Bucket partially full. Recursion -> next_sum = 4. new_mask = 3 (0000011)

mask = 3 (0000011), current_sum = 4
i=0, i=1: Unavailable.
i=2 (num=3): new_sum = 4 + 3 = 7. (> Target). Skip.
...
i=6 (num=1): new_sum = 4 + 1 = 5. (Hits Target!). new_mask = 67.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N * 2^N)                         │
│  Space Complexity │ O(2^N) (Memoization dictionary)    │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Dividing an array into independent groups.
* ✓ Array length $N \le 16$.
* $\rightarrow$ **Bitmask Combinatorics DP**

### Core Insight
A naive backtracking algorithm treats the physical buckets as the state (`bucket1_sum`, `bucket2_sum`). This fails because the buckets are symmetrical and orderless, causing catastrophic redundant processing. By tracking the *used items* (the mask) instead of the *buckets*, we compress symmetrical permutations into a single identical integer state.

### Mistakes Made
* We initially forgot to sort the `nums` array descending. While the DP logic was mathematically perfect, it resulted in TLE on large arrays because the algorithm wasted millions of cycles trying to fit tiny numbers (like `1`) into buckets, only to fail at the very end when a massive number didn't fit anywhere. Sorting descending forces early failures, massively pruning the recursion tree.

### What I Learned
In Combinatorial Mask DP, sorting inputs descending is a non-negotiable heuristic optimization. Forcing the largest constraints into the algorithm first creates immediate structural bottlenecks, terminating doomed branches milliseconds after they spawn.

---

## Problem: Matchsticks to Square (473)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Mask Combinatorics
* **Problem Type:** Geometric Subset Packing
* **Data Structure Used:** Dictionary (`memo`) storing solved bitmasks.
* **Brute Force:** Try rotating/placing every matchstick onto 4 sides. Time: $O(4^N)$.
* **Optimized Approach:** A square inherently has exactly 4 equal sides. Therefore, determining if matchsticks can form a square is mathematically, logically, and algorithmically identical to `Partition to K Equal Sum Subsets` where `K = 4`. 

### DP State
*(Identical to Partition to K Equal Sum Subsets)*

### State Flow
*(Identical to Partition to K Equal Sum Subsets)*

### Recurrence
*(Identical to Partition to K Equal Sum Subsets)*

### Base Cases
* If `total_sum % 4 != 0`, return `False`.
* If any single matchstick `> target`, return `False` immediately.
* If `mask == (1 << n) - 1`, return `True`.

### Traversal Order
*(Identical to Partition to K Equal Sum Subsets)*

### Pointer Flow
*(Identical to Partition to K Equal Sum Subsets)*

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N * 2^N)                         │
│  Space Complexity │ O(2^N)                             │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Geometry problem requiring forming an equilateral shape.
* ✓ Matchsticks length $N \le 15$.
* $\rightarrow$ **Bitmask Combinatorics DP (K=4)**

### Core Insight
Never let the semantic phrasing of a geometry problem distract from its underlying algebraic signature. A square is just four buckets of equal capacity.

### Mistakes Made
* We forgot the initial geometric edge-case check: a matchstick longer than the target side length is an immediate failure. The recursion tree would eventually figure this out, but testing it at $O(1)$ time on line 1 is far superior.

### What I Learned
Always translate physics and geometry constraints back down into raw array-summing logic before drafting an architecture.

---

## Problem: Can I Win (464)

* **Interview Difficulty:** Hard
* **Parent Pattern:** Game Theory Bitmask DP
* **Problem Type:** Minimax Combinatorics
* **Data Structure Used:** Dictionary (`memo`) storing bitmask integer states.
* **Brute Force:** Minimax evaluating every possible branching game tree. Time: $O(N!)$.
* **Optimized Approach:** Two players are picking integers from a shared pool (`1` to `N`), attempting to reach a `desiredTotal`. We use a bitmask to track which numbers have been picked. The DP state evaluates: *"From this current state, can the current player force a win?"* A player forces a win if they can pick a number that instantly reaches the total OR if they can pick a number that leaves the opponent in a state from which the opponent is mathematically guaranteed to lose.

### DP State
`dfs(mask, current_total)` returns `True` if the player whose turn it currently is can guaranteeably force a victory from this state.

### State Flow
```text
STATE: memo[mask] = True (Current player wins) or False.

↓

CHOICES for selecting integer `i`:
  If `mask & (1 << i)` is 0 (Integer i is available):
    
    Condition A (Instant Kill):
      If current_total + i >= desiredTotal:
        We win immediately! Return True.
        
    Condition B (Minimax Poison):
      Assume we take `i`. The new state passed to the opponent is `mask | (1 << i)`.
      If `dfs(new_state) == False`, it means the opponent CANNOT win from that state.
      If the opponent loses, we win! Return True.

↓

TRANSITION: If any choice satisfies Cond A or Cond B, memo[mask] = True.
```

### Recurrence
(Logic branching based on Opponent state evaluation).

### Base Cases
* If `desiredTotal <= maxChoosableInteger`: return `True` (Player 1 wins on turn 1).
* If `sum(all_integers) < desiredTotal`: return `False` (Game is un-winnable).

### Traversal Order
**Top-Down Recursive DFS (Minimax).**

### Pointer Flow
```text
maxInt = 10, target = 11.
P1 starts. mask = 0, total = 0.

P1 evaluates choosing 10:
  Instant Kill? 0 + 10 = 10 (Not >= 11).
  Minimax Check: Opponent's turn with mask = 1024, total = 10.
  
  P2's turn: mask = 1024, total = 10.
  P2 evaluates choosing 1:
    Instant Kill? 10 + 1 = 11 (>= 11). P2 WINS! Returns True.
    
  Because P2 returns True, P1's choice of 10 was a BAD MOVE.

P1 evaluates choosing 9:
  Instant Kill? No (9).
  Minimax: Opponent gets mask = 512, total = 9.
  P2 evaluates choosing 2: 9 + 2 = 11. P2 WINS! Bad move for P1.
  ...
This minimax bubbling eventually realizes P1 cannot force a win.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N * 2^N)                         │
│  Space Complexity │ O(2^N)                             │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Two-player game with perfect information (no dice/RNG).
* ✓ Shared pool of limited resources $N \le 20$.
* $\rightarrow$ **Game Theory Minimax DP**

### Core Insight
Game Theory DP does not require modeling Player 1 vs Player 2 variables. Because the game is perfectly symmetrical, the `dfs` function strictly evaluates the perspective of the *Current Player*. Passing the state to `dfs()` effectively flips the board and asks the opponent to evaluate their own chances. If they report `False` (I lose), you win.

### Mistakes Made
* We attempted to track an `is_player_one` boolean variable inside the state tuple. This doubled the size of our memoization cache needlessly. In perfectly alternating combinatorial games, the boolean state of the board completely dictates whose turn it is natively.

### What I Learned
Minimax logic on combinatorial sets collapses beautifully when we realize that forcing the recursive call to return `False` is mathematically synonymous with achieving a personal victory.

---

## Problem: Travelling Salesman Problem (Conceptual)

* **Interview Difficulty:** Hard
* **Parent Pattern:** Bitmask Matrix DP
* **Problem Type:** Shortest Path Graph Optimization
* **Data Structure Used:** 2D DP Matrix (`dp[mask][current_city]`).
* **Brute Force:** Try all permutations of visiting cities. Time: $O(N!)$.
* **Optimized Approach:** We must visit every node exactly once and return to the start. The state requires tracking two pieces of information: exactly which cities we have visited (the `mask`), and the city we are *currently standing in* (to calculate the physical distance to the next unvisited city). We initialize the matrix to `inf`. From any state `(mask, i)`, we loop over all unvisited cities `j`, updating the state `(mask | (1 << j), j)` with the minimum cost.

### DP State
`dp[mask][i]` represents the **minimum distance traveled to visit all the cities flipped ON in the `mask`, ending exactly at city index `i`**.

### State Flow
```text
STATE: dp[mask][i] = min distance.

↓

CHOICES from city `i`:
  For every other city `j`:
    If `j` is unvisited (mask & (1<<j) == 0):
      We travel from i to j.
      The new state mask is `mask | (1<<j)`.
      Cost = Current distance (dp[mask][i]) + graph[i][j]

↓

TRANSITION: dp[next_mask][j] = min(dp[next_mask][j], cost)
```

### Recurrence
$$\text{dp}[\text{mask} \lor (1 \ll j)][j] = \min(\text{dp}[\text{mask} \lor (1 \ll j)][j], \; \text{dp}[\text{mask}][i] + \text{graph}[i][j])$$

### Base Cases
* If city 0 is our starting origin: `dp[1][0] = 0`. (Mask `0...01` signifies city 0 is visited, distance traveled is 0).

### Traversal Order
**Bottom-Up Iterative.**
Outer loop: `mask` from `1` to `2^N - 1`.
Middle loop: Origin city `i` from `0` to `N-1`.
Inner loop: Destination city `j` from `0` to `N-1`.

### Pointer Flow
```text
N = 3 cities. Origin is 0.
Base: dp[1][0] = 0. (Mask 1)

Iterate Mask = 1 (Visited: {0}, Ending at 0):
  Can move to City 1: Next Mask = 3 ({0,1}). dp[3][1] = min(inf, dp[1][0] + graph[0][1])
  Can move to City 2: Next Mask = 5 ({0,2}). dp[5][2] = min(inf, dp[1][0] + graph[0][2])

Iterate Mask = 3 (Visited: {0,1}, Ending at 1):
  Can move to City 2: Next Mask = 7 ({0,1,2}). dp[7][2] = min(inf, dp[3][1] + graph[1][2])

Iterate Mask = 5 (Visited: {0,2}, Ending at 2):
  Can move to City 1: Next Mask = 7 ({0,1,2}). dp[7][1] = min(inf, dp[5][2] + graph[2][1])
...
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^2 * 2^N)                       │
│  Space Complexity │ O(N * 2^N) (2D tracking array)     │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Problem requires visiting every single node in a graph exactly once (Hamiltonian path).
* ✓ $N \le 18$.
* $\rightarrow$ **Bitmask Matrix DP**

### Core Insight
Unlike permutation arrays, graph traversal distance is entirely dependent on the *last node* you visited. The DP matrix must expand into 2D to log `current_city`. Two paths might visit the exact same set of cities (same mask), but if one ends at City 3 and the other ends at City 5, their transition costs to City 6 are mathematically incomparable.

### Mistakes Made
* We attempted to resolve TSP using standard Top-Down recursion with a 1D `memo[mask]` dictionary. We quickly realized the dictionary was returning garbage data because it was ignoring *where* we currently were on the map. Expanding the state key to `memo[(mask, current_city)]` (which is functionally identical to the 2D array) completely resolved the anomaly.

### What I Learned
State compression doesn't mean state elimination. If a transition cost is physically dependent on a geometric location, that location MUST exist as an independent dimension in the DP architecture, functioning parallel to the bitmask.

---

### Master Patterns Learned

#### 1. The Integer Compression Vault (Bitmask Mechanics)
* **The Strategy:** Deploy whenever tracking the specific availability/usage of an array of items where $N \le 20$.
* **The Conceptual Mechanics:** Replace hash sets and boolean arrays with a single integer. Use bitwise `&` to check availability, and bitwise `|` to consume resources. Use `memo[mask]` to cache the temporal permutations.

#### 2. Minimax Adversarial Combinatorics
* **The Strategy:** Deploy on perfect-information turn-based games evaluating a "forced win".
* **The Conceptual Mechanics:** Do not track player identity. Assume the perspective of the current turn. Search for a move that yields an instant kill, or a move that passes an unwinnable state (a state that returns `False`) to the opponent.

#### 3. Spatial Mask Integration (2D Bitmasking)
* **The Strategy:** Deploy on Hamiltonian graph problems (TSP) where transition costs are governed by adjacency.
* **The Conceptual Mechanics:** Because the cost to reach an unvisited node relies on physical geography, the DP array must scale out to `dp[mask][current_node]` to prevent spatial state-collisions.
