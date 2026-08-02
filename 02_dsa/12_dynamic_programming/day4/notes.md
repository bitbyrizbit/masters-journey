# Knapsack DP & Capacity Optimization

## 1. What is Knapsack DP?

The **Knapsack Problem** forms the bedrock of capacity-based dynamic programming. It models a classic constraint scenario: we possess a container (the knapsack) with a strict maximum capacity (e.g., maximum weight, target sum, or limited budget). We must select items from a given inventory to fulfill an optimization metric (maximize profit, minimize coins, or determine boolean feasibility) without exceeding the container's strict limit.

While standard Decision DP (Day 2) simply iterates over indices `i`, Knapsack DP introduces a **secondary geometric dimension**: the remaining capacity constraint `w`.

---

## 2. State Design (The 2D Matrix)

Because the validity of taking an item depends entirely on whether we have enough remaining capacity to hold it, our state definition must track both variables simultaneously.

> **The Universal Knapsack State Definition:**
> `dp[i][w]` represents the optimal mathematical answer when considering items from index `0` up to `i`, constrained by a maximum available capacity of exactly `w`.

### Why the Weight Dimension is Mandatory
If we only tracked `dp[i]` (best answer up to item `i`), we would lack the physical context of the knapsack's current fullness. By incorporating `w`, we map out every possible permutation of the knapsack's capacity, from completely empty (`0`) up to its absolute maximum limit (`W`).

---

## 3. The Transition Engine (Take vs. Skip)

For every item `i` and every capacity `w`, we face a binary choice. However, the `Take` choice is physically blocked if the item's weight exceeds the current capacity column `w`.

```text
At Item i and Capacity w:
                   ┌─────────────────────────────┐
                   │        State (i, w)         │
                   └──────────────┬──────────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
      Choice 1: SKIP Item i               Choice 2: TAKE Item i
      ─────────────────────               ─────────────────────
      Ignore item i entirely.             (Only valid if weight[i] <= w)
      Inherit optimal answer              Subtract item weight from capacity.
      from row above:                     Add item value:
      dp[i-1][w]                          value[i] + dp[i-1][w - weight[i]]
                 │                                 │
                 └────────────────┬────────────────┘
                                  ▼
                   Take Optimal (Max, Min, or Boolean OR)
```

---

## 4. 0/1 Knapsack vs. Complete Knapsack

The fundamental distinction between the two major branches of capacity DP lies entirely in whether an item is permanently consumed after being taken.

| Property | 0/1 Knapsack | Complete (Unbounded) Knapsack |
| :--- | :--- | :--- |
| **Constraint** | Each item can be used at most **ONCE**. | Each item can be used **INFINITELY**. |
| **Skip Transition** | `dp[i-1][w]` | `dp[i-1][w]` |
| **Take Transition** | `dp[i-1][w - weight[i]]` (Move to previous item) | `dp[i][w - weight[i]]` (Stay on current item) |
| **Core Examples** | Subset Sum, Target Sum | Coin Change, Rod Cutting |

---

## 5. Space Optimization (1D Array Compression)

A 2D matrix of size `N * W` requires heavy memory allocations. However, if we carefully observe the `Take` vs `Skip` transitions, the current row `i` only ever relies directly on the immediately preceding row `i-1`. 

We can compress the `N * W` matrix into a single flat `1D` array of size `W + 1`.

### The Iteration Direction Rule (CRITICAL)
* **0/1 Knapsack:** We must iterate the capacity loop **BACKWARDS** (from `W` down to `0`). If we iterate forwards, modifying `dp[w]` could inadvertently provide an overwritten value to a subsequent `dp[w + weight]` check in the same loop pass, simulating infinite reusability.
* **Complete Knapsack:** We must iterate the capacity loop **FORWARDS** (from `0` up to `W`). Because items are infinite, we *want* the current item's choice to stack on top of a previously updated capacity in the same pass.

---

## 6. The Universal Knapsack Checklist

Before executing capacity logic, run this checklist:

```text
┌─────────────────────────────────────────────────────────────────┐
│  BOX 1 — CAPACITY CAP                                           │
│  What defines the maximum boundary column? (Target, amount)     │
├─────────────────────────────────────────────────────────────────┤
│  BOX 2 — 0/1 OR COMPLETE                                        │
│  Are items single-use (0/1) or infinitely reusable (Complete)?  │
├─────────────────────────────────────────────────────────────────┤
│  BOX 3 — TRANSITION (Max/Min/Count/Boolean)                     │
│  Are we taking max(), min(), summing (+), or logical ORing?     │
├─────────────────────────────────────────────────────────────────┤
│  BOX 4 — BASE CASE                                              │
│  What happens at capacity 0? (Usually 0, 1, or True).           │
├─────────────────────────────────────────────────────────────────┤
│  BOX 5 — TRAVERSAL ORDER                                        │
│  Backwards loop (0/1) vs Forwards loop (Complete).              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Problem: Partition Equal Subset Sum (416)

* **Interview Difficulty:** Medium
* **Parent Pattern:** 0/1 Knapsack Boolean DP
* **Problem Type:** Array Partitioning / Subset Feasibility
* **Data Structure Used:** 1D DP Array (`list[bool]`) representing target capacities.
* **Brute Force:** Explore all $2^N$ subset combinations recursively to see if any exactly equals `sum / 2`. Time Complexity: $O(2^N)$.
* **Optimized Approach:** Mathematical reduction. If the total array sum is odd, splitting it into two equal integers is mathematically impossible. If even, the problem morphs into a standard 0/1 Knapsack search for a capacity exactly equal to `sum / 2`. We use a flat 1D Boolean DP array, iterating backwards to enforce single-use constraints.

### DP State
`dp[target]` represents a **boolean (`True`/`False`) indicating whether a subset of the currently processed numbers can perfectly sum to the capacity `target`**.

### State Flow
```text
STATE: dp[current_target] = True if a valid subset exists, False otherwise.

↓

CHOICES for number `num`:
  SKIP: Inherit feasibility from previous iteration (already in dp[current_target]).
  TAKE: Check if (current_target - num) was feasible.

↓

TRANSITION: dp[current_target] = dp[current_target] OR dp[current_target - num]
```

### Recurrence
$$\text{dp}[w] = \text{dp}[w] \lor \text{dp}[w - \text{num}]$$

### Base Cases
* `dp[0] = True` (An empty subset always inherently yields a sum of 0).

### Traversal Order
**Outer Loop:** Iterate through `num` in `nums`.
**Inner Loop:** Iterate `w` **BACKWARDS** from `target` down to `num` (0/1 Knapsack).

### Pointer Flow
```text
Evaluating Partition for nums = [1, 5, 11, 5]. Total Sum = 22. Target = 11.
Base: dp[0] = True, all others False.

num = 1: 
  dp[1] = dp[1] OR dp[0] -> True
num = 5:
  dp[6] = dp[6] OR dp[1] -> True
  dp[5] = dp[5] OR dp[0] -> True
num = 11:
  dp[11] = dp[11] OR dp[0] -> True  <-- Target Reached!

Final Answer: dp[11] is True.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N * (Sum/2))                     │
│  Space Complexity │ O(Sum/2) (1D optimized array)      │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Problem requires dividing a pool of items.
* ✓ The metric is boolean feasibility (can we make it?).
* ✓ Items are single-use.
* $\rightarrow$ **0/1 Knapsack Boolean DP**

### Core Insight
A partitioning problem is just a subset sum problem hidden behind a mathematical mask. Finding two equal partitions is identical to finding one subset that equals exactly half the total global sum.

### Mistakes Made
* We attempted to iterate the inner capacity loop forward. This allowed a number like `1` to satisfy `dp[1] = True`, which then fed into `dp[2] = dp[2] OR dp[1]`, effectively allowing the number `1` to be used infinitely.

### What I Learned
The inner loop direction is the singular mechanical difference between infinite reuse and single-use constraints in space-optimized Knapsack engines.

---

## Problem: Target Sum (494)

* **Interview Difficulty:** Medium
* **Parent Pattern:** 0/1 Knapsack Counting DP
* **Problem Type:** Math Transformation / Subset Counting
* **Data Structure Used:** 1D DP Array (`list[int]`) tracking path counts.
* **Brute Force:** DFS evaluating `+` and `-` branches for every element. Time: $O(2^N)$.
* **Optimized Approach:** Pure math transformation. Instead of dynamically assigning signs, we partition the array into a `Positive` subset and a `Negative` subset. 
  `Sum(P) - Sum(N) = target`
  `Sum(P) + Sum(N) = total_sum`
  Adding both equations yields: `2 * Sum(P) = target + total_sum`.
  Therefore, we only need to find the number of subsets that sum exactly to `(target + total_sum) / 2`.

### DP State
`dp[w]` represents the **total count of distinct combinations that sum to exactly capacity `w`**.

### State Flow
```text
STATE: dp[w] = number of ways to create sum w.

↓

CHOICES for number `num`:
  SKIP: Keep existing paths to w (dp[w]).
  TAKE: Add all the paths that successfully reached (w - num).

↓

TRANSITION: dp[w] = dp[w] + dp[w - num]
```

### Recurrence
$$\text{dp}[w] = \text{dp}[w] + \text{dp}[w - \text{num}]$$

### Base Cases
* `dp[0] = 1` (Exactly 1 way to make a sum of 0: pick nothing).

### Traversal Order
**Outer Loop:** `num` in `nums`.
**Inner Loop:** `w` **BACKWARDS** from `subset_target` down to `num` (0/1 Knapsack).

### Pointer Flow
```text
nums = [1, 1, 1, 1, 1], target = 3, Total Sum = 5.
Subset Target = (5 + 3) / 2 = 4.
Base: dp = [1, 0, 0, 0, 0] (Capacity 0 to 4)

After Num 1 (first '1'):  dp = [1, 1, 0, 0, 0]
After Num 2 (second '1'): dp = [1, 2, 1, 0, 0]
After Num 3 (third '1'):  dp = [1, 3, 3, 1, 0]
After Num 4 (fourth '1'): dp = [1, 4, 6, 4, 1]
After Num 5 (fifth '1'):  dp = [1, 5, 10, 10, 5]

Final dp[4] = 5 distinct combinations.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N * subset_target)               │
│  Space Complexity │ O(subset_target)                   │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Elements require dynamic sign assignments (`+` or `-`).
* ✓ Requests the "total number of ways" (Counting metric).
* $\rightarrow$ **0/1 Knapsack Math Transformation**

### Core Insight
Algebraic transformations can completely bypass complex state tracking. By reducing the `+`/`-` problem into a static subset sum problem, we eliminated the need to track negative array indices entirely.

### Mistakes Made
* We failed to check for fractional targets. If `(total_sum + target) % 2 != 0`, no integer subset can mathematically satisfy the equation, meaning we must return 0 immediately.

### What I Learned
Invalid initial conditions (like `abs(target) > total_sum` or odd parity combinations) should be trapped immediately before allocating any DP matrix memory.

---

## Problem: Coin Change (322)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Complete Knapsack Minimum DP
* **Problem Type:** Unbounded Item Combinatorics
* **Data Structure Used:** 1D DP Array (`list[int]`) filled with `infinity` limits.
* **Brute Force:** DFS trying every coin combination recursively. Time: $O(C^N)$.
* **Optimized Approach:** Because coins are infinite, we utilize the Complete Knapsack forward-iteration template. We initialize our DP matrix with an impossibly high value (`float('inf')`) to serve as a ceiling proxy. At each capacity, we evaluate if subtracting the current coin yields a smaller total coin count than the existing record.

### DP State
`dp[w]` represents the **absolute minimum number of coins required to manufacture the amount `w`**.

### State Flow
```text
STATE: dp[w] = minimum coins to make amount w.

↓

CHOICES for `coin`:
  SKIP: Keep current minimum coin count for w.
  TAKE: Use 1 coin, plus the optimal minimum coin count to make (w - coin).

↓

TRANSITION: dp[w] = min(dp[w], 1 + dp[w - coin])
```

### Recurrence
$$\text{dp}[w] = \min(\text{dp}[w], \; 1 + \text{dp}[w - \text{coin}])$$

### Base Cases
* `dp[0] = 0` (It costs 0 coins to manufacture an amount of 0).
* All other `dp[w] = infinity`.

### Traversal Order
**Outer Loop:** `coin` in `coins`.
**Inner Loop:** `w` **FORWARDS** from `coin` up to `amount` (Complete Knapsack).

### Pointer Flow
```text
coins = [1, 2, 5], amount = 11.
Base: dp = [0, inf, inf, ... inf]

Processing Coin 1:
dp[1] = min(inf, 1 + dp[0]) = 1
dp[2] = min(inf, 1 + dp[1]) = 2  (Notice how forward iteration builds on itself!)
... dp = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

Processing Coin 2:
dp[2] = min(2, 1 + dp[0]) = 1
dp[4] = min(4, 1 + dp[2]) = 2
... dp = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6]

Processing Coin 5:
dp[5] = min(3, 1 + dp[0]) = 1
dp[10] = min(5, 1 + dp[5]) = 2
dp[11] = min(6, 1 + dp[6]) = 1 + 2 = 3.

Final output: 3 coins.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N * amount)                      │
│  Space Complexity │ O(amount)                          │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Target capacity constraint (Amount).
* ✓ Infinite supply of items (Coins).
* ✓ Minimization metric (Fewest coins).
* $\rightarrow$ **Complete Knapsack Minimum DP**

### Core Insight
Minimum optimization dictates that the baseline values must be initialized to infinity. If we initialize with zeros, the `min()` function will permanently lock every cell at 0.

### Mistakes Made
* We attempted to check `dp[amount] == 0` at the end to return `-1` if no solution was found. However, if `amount == 0`, the correct answer is `0`, not `-1`. The strict validation check must be `if dp[amount] != float('inf')`.

### What I Learned
Forward iteration loops naturally create the infinite reuse mechanic required for currency and capacity algorithms.

---

## Problem: Coin Change II (518)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Complete Knapsack Counting DP
* **Problem Type:** Infinite Path Combinatorics
* **Data Structure Used:** 1D DP Array (`list[int]`) tracking path counts.
* **Brute Force:** DFS counting all valid permutations. Time: $O(C^N)$.
* **Optimized Approach:** Identical architecture to Coin Change 1, but we shift the transition equation from a `min()` optimization to a sum accumulation (`+`) to track the volume of successful paths.

### DP State
`dp[w]` represents the **total number of distinct combinations of coins that sum to exactly amount `w`**.

### State Flow
```text
STATE: dp[w] = total combinations to make amount w.

↓

CHOICES for `coin`:
  SKIP: Keep existing combination count.
  TAKE: Accumulate the number of valid combinations that form (w - coin).

↓

TRANSITION: dp[w] = dp[w] + dp[w - coin]
```

### Recurrence
$$\text{dp}[w] = \text{dp}[w] + \text{dp}[w - \text{coin}]$$

### Base Cases
* `dp[0] = 1` (There is exactly 1 way to form amount 0: use zero coins).
* All other `dp[w] = 0`.

### Traversal Order
**Outer Loop:** `coin` in `coins`.
**Inner Loop:** `w` **FORWARDS** from `coin` up to `amount` (Complete Knapsack).

### Pointer Flow
```text
coins = [1, 2, 5], amount = 5.
Base: dp = [1, 0, 0, 0, 0, 0]

Coin 1: dp = [1, 1, 1, 1, 1, 1] (One way to make all amounts using only 1s)

Coin 2:
dp[2] += dp[0] -> 1 + 1 = 2
dp[3] += dp[1] -> 1 + 1 = 2
dp[4] += dp[2] -> 1 + 2 = 3
dp[5] += dp[3] -> 1 + 2 = 3

Coin 5:
dp[5] += dp[0] -> 3 + 1 = 4.

Final output: 4 distinct combinations.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N * amount)                      │
│  Space Complexity │ O(amount)                          │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Target capacity constraint (Amount).
* ✓ Infinite supply of items (Coins).
* ✓ Combinatorial metric (Total number of ways).
* $\rightarrow$ **Complete Knapsack Counting DP**

### Core Insight
Unlike permutation problems (like Climbing Stairs) where order matters (`1,2` is different from `2,1`), Knapsack combinations are order-agnostic. Because the outer loop strictly processes one coin entirely before moving to the next, it is structurally impossible for the DP engine to count `(1, 2)` and `(2, 1)` as two different paths.

### Mistakes Made
* We attempted to flip the loop order (Outer loop `amount`, Inner loop `coins`). This structurally changes the output from *Combinations* to *Permutations*, leading to vastly inflated and incorrect answers.

### What I Learned
The loop hierarchy defines the combinatorics limit. To prevent duplicate permutations, the `item` loop must always govern the outer structure, locking item ordering.

---

### Master Patterns Learned

#### 1. The Space-Optimized Knapsack Template
* **The Strategy:** Deploy this framework whenever capacity acts as a strict bounding constraint against item selection.
* **The Conceptual Mechanics:**
  - Collapse heavy 2D matrices into 1D tracking arrays.
  - Dictate item limits purely through loop traversal direction (Backwards = Single Use, Forwards = Infinite Use).
* **The Layout / Code Pattern:**
```python
def universal_knapsack(items, capacity):
    # Determine base case behavior (0, 1, True, inf) based on the metric
    dp = [0] * (capacity + 1)
    dp[0] = 1 
    
    for item_weight in items:
        # For 0/1 Knapsack: range(capacity, item_weight - 1, -1)
        # For Complete Knapsack: range(item_weight, capacity + 1)
        for w in range(capacity, item_weight - 1, -1):
            dp[w] = dp[w] + dp[w - item_weight] # Swap operator based on prompt
            
    return dp[capacity]
```

#### 2. The Subset Math Transformation
* **The Strategy:** Apply this technique to array problems involving positive/negative assignments or subset division. Instead of dealing with dual bounds, execute algebraic reductions (like `(sum + target) / 2`) to collapse the prompt into a static positive-only Subset Sum layout.

#### 3. Counting vs. Minimum Architecture
* **The Strategy:** 
  - **Counting:** Initialize with `0`s (base `0` is `1`). Transition via `+`.
  - **Minimum:** Initialize with `inf` (base `0` is `0`). Transition via `min()`.
  - **Boolean Feasibility:** Initialize with `False` (base `0` is `True`). Transition via `OR`.
