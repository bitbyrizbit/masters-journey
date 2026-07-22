# Dynamic Programming

## 1. Why DP Exists

Every problem-solving discipline has a moment where brute force collapses under its own weight. For dynamic programming, that moment arrives when a recursive algorithm starts solving the same sub-problems repeatedly — not just twice, but exponentially many times. The naive recursive solution to Fibonacci, for example, calculates `fib(30)` using over a million function calls when the actual work can be done in 30.

Dynamic Programming is not a data structure. It is not a specific algorithm. It is a **problem-solving design paradigm** — a mental framework for transforming a recursive solution that re-solves the same state over and over into one that solves each state exactly once, stores that result, and looks it up instantly on all future encounters.

It sits at the intersection of two fundamental computer science concepts:

*   **Recursion:** Breaking a large problem into smaller, structurally identical sub-problems.
*   **Caching / Memoization:** Storing results of sub-problems so they are never computed twice.

### The Core Contract of DP

For a problem to be solvable by Dynamic Programming, it must satisfy two non-negotiable mathematical properties:

1.  **Overlapping Subproblems** — The same smaller sub-problems recur multiple times across different branches of the solution tree.
2.  **Optimal Substructure** — The globally optimal solution can be built by combining the optimal solutions of its smaller sub-problems.

If either property is absent, Dynamic Programming cannot be applied. If both are present, DP can reduce an exponential-time brute-force solution to polynomial time.

---

## 2. Overlapping Subproblems

### The Definition

A problem exhibits **overlapping subproblems** when, during recursive exploration, identical sub-calls appear in multiple branches of the recursion tree simultaneously. The key word is *identical* — the same input parameters, the same state, reaching the same function call from different places in the call tree.

### The Fibonacci Illustration

The most direct demonstration is the classic Fibonacci calculation. The recursive definition states:

$$F(n) = F(n-1) + F(n-2)$$

When you evaluate `F(5)` with a naive recursive implementation, the call tree expands like this:

```text
Naive Recursive Call Tree for F(5):

                    F(5)
                  /      \
              F(4)        F(3)
             /    \       /   \
          F(3)   F(2)  F(2)  F(1)
          /  \   /  \  /  \
        F(2) F(1) F(1) F(0) F(1) F(0)
        / \
      F(1) F(0)

Unique Problems:   F(0), F(1), F(2), F(3), F(4), F(5)  →  6 problems
Total Calls Made:  15 function calls to compute F(5)
F(3) computed:     2 times   ← OVERLAPPING SUBPROBLEM
F(2) computed:     3 times   ← OVERLAPPING SUBPROBLEM
F(1) computed:     5 times   ← OVERLAPPING SUBPROBLEM
```

The recursive tree is doing **redundant work** on a massive scale. As `n` grows, the work explodes exponentially at $O(2^n)$. This overlap is what DP is designed to eliminate.

### Why Overlap Matters

Without overlap, every sub-problem is unique and there is nothing to cache. With overlap, every repeated sub-problem is wasted computation. The greater the overlap, the greater the speedup DP provides.

---

## 3. Optimal Substructure

### The Definition

A problem has **optimal substructure** when the optimal solution to the full problem can be constructed directly from the optimal solutions to its sub-problems. This means you never need to re-examine a sub-problem once its optimal answer is known — that answer can be used as a permanent building block.

### The Fibonacci Case

This is straightforward: the exact value of `F(n)` depends only on the exact values of `F(n-1)` and `F(n-2)`. There is no alternative formulation. The optimal sub-problem results feed directly into the optimal final result.

### The Shortest Path Case

In Dijkstra's algorithm, the shortest path from `A` to `D` going through `B` and `C` means the sub-path from `A` to `C` must also be the shortest path from `A` to `C`. If it were possible to improve the sub-path, the full path could be improved too — which would contradict its optimality. This self-referential property is optimal substructure.

### Problems That Lack Optimal Substructure

The **Longest Path Problem** in a graph with cycles does **not** have optimal substructure. Adding the longest path from `A` to `B` and the longest path from `B` to `C` can create cycles, making the combined result invalid. This is why DP cannot be applied there.

---

## 4. Recursion vs Memoization

### Phase 1: Naive Recursion

The natural human approach to a recursive problem is to simply implement the mathematical definition directly. For the Climbing Stairs problem (how many ways to reach step `n` taking 1 or 2 steps at a time):

```python
def climb_naive(n):
    if n <= 1:
        return 1
    return climb_naive(n - 1) + climb_naive(n - 2)
```

This is correct but catastrophically slow for large `n`. For `n = 40`, this triggers over a billion recursive calls. The time complexity is $O(2^n)$ with $O(n)$ stack space.

### Phase 2: The Recursion Tree Problem (Visualized)

```text
climb(4) Call Tree — Overlapping Subproblems Highlighted:

           climb(4)
          /        \
      climb(3)    climb(2)
      /      \    /      \
  climb(2) climb(1) climb(1) climb(0)
  /      \
climb(1) climb(0)

climb(2) → computed TWICE
climb(1) → computed THREE TIMES
```

The redundancy is visible. Each node on the left side is re-evaluated from scratch instead of looking up a cached result.

### Phase 3: Top-Down DP (Memoization)

Memoization fixes the redundancy by adding a dictionary cache. Before computing a result, check if it already exists. If it does, return it instantly. If not, compute it, store it, and return it.

```python
def climb_memo(n, memo={}):
    if n <= 1:
        return 1
    if n in memo:
        return memo[n]              # Cache hit: instant return
    memo[n] = climb_memo(n - 1, memo) + climb_memo(n - 2, memo)
    return memo[n]
```

```text
Memoized Execution for climb(4):

climb(4) → not in memo → compute:
  └── climb(3) → not in memo → compute:
        ├── climb(2) → not in memo → compute:
        │     ├── climb(1) → base case → return 1
        │     └── climb(0) → base case → return 1
        │     memo[2] = 2 → return 2
        └── climb(1) → base case → return 1
        memo[3] = 3 → return 3
  └── climb(2) → IN MEMO → return 2  ← Cache hit!
memo[4] = 5 → return 5

Total unique states computed: 4 (instead of 9)
```

Time complexity drops to $O(n)$. Space stays $O(n)$ for the memo cache plus $O(n)$ call stack depth.

---

## 5. Bottom-Up DP (Tabulation)

### The Philosophy Shift

Top-Down DP still relies on recursion — it still builds a call stack, it still has the overhead of function calls, and it still risks hitting Python's recursion depth limit on large inputs. Tabulation eliminates recursion entirely by flipping the direction of computation.

Instead of starting at the problem and recursively breaking it down, **Bottom-Up DP starts at the smallest possible sub-problems and iteratively builds up to the answer**.

This is called **Tabulation** because you literally fill in a table of values from the bottom up, one cell at a time.

### The Core Idea

For Climbing Stairs:
*   We know `dp[1] = 1` (one way to reach step 1: take one step).
*   We know `dp[2] = 2` (two ways to reach step 2: 1+1 or 2).
*   For any `i > 2`: `dp[i] = dp[i-1] + dp[i-2]` — the number of ways to reach step `i` is the sum of ways to arrive from step `i-1` and from step `i-2`.

We fill the table left to right. When we need `dp[i]`, both `dp[i-1]` and `dp[i-2]` are already computed and sitting in the table.

```python
def climb_tabulation(n):
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

```text
Table Fill for climb(6):

Index:  0    1    2    3    4    5    6
dp:    [0,   1,   2,   3,   5,   8,  13]

Step 3: dp[3] = dp[2] + dp[1] = 2 + 1 = 3
Step 4: dp[4] = dp[3] + dp[2] = 3 + 2 = 5
Step 5: dp[5] = dp[4] + dp[3] = 5 + 3 = 8
Step 6: dp[6] = dp[5] + dp[4] = 8 + 5 = 13
```

Time: $O(n)$. Space: $O(n)$ for the dp array. No recursion, no call stack, no risk of stack overflow.

### Why Left-to-Right is Valid

This is not obvious and interviewers ask about it. The reason a single forward pass works is a mathematical guarantee rooted in the recurrence structure itself.

At every iteration `i`, the recurrence `dp[i] = dp[i-1] + dp[i-2]` only reads from indices strictly less than `i`. Both `dp[i-1]` and `dp[i-2]` were computed in earlier iterations and are already finalized. No future state `dp[j]` where `j > i` can modify them. This means:

```text
When the loop reaches iteration i:

  dp[i-2] → computed at iteration i-2 → FINALIZED ✓
  dp[i-1] → computed at iteration i-1 → FINALIZED ✓
  dp[i]   → safe to compute now       → no dependency on future states

Therefore: a single left-to-right pass is both necessary and sufficient.
```

This is the core reason tabulation works. The recurrence only looks backward, never forward. If a recurrence looked forward (e.g., `dp[i] = dp[i+1] + something`), you would need a right-to-left pass instead. The traversal order is always dictated by the direction the recurrence looks.

---

## 6. Top-Down DP vs Bottom-Up DP

| Attribute | Top-Down (Memoization) | Bottom-Up (Tabulation) |
| :--- | :--- | :--- |
| **Direction** | Starts at the big problem, recurses down | Starts at smallest base case, builds up |
| **Mechanism** | Recursion + dictionary cache | Iterative loop + array |
| **Computation Style** | Lazy (only computes what's needed) | Eager (computes all states in order) |
| **Call Stack Risk** | Yes — can hit recursion depth limit | No — pure iteration, no stack frames |
| **Code Clarity** | Natural translation of recursive formula | Requires deliberate ordering of states |
| **Space Usage** | $O(n)$ cache + $O(n)$ call stack | $O(n)$ dp array only |
| **When to Prefer** | Complex dependency graphs, not all states needed | Sequential problems where all states are required |

### Critical Insight

In competitive programming and interviews, **Bottom-Up is generally preferred** because:
1.  It eliminates recursion overhead.
2.  It is immune to Python's default recursion limit of 1000 frames.
3.  It naturally leads into Space Optimization (see next section).
4.  It often runs faster in practice due to cache coherence of sequential array access.

Both approaches have identical time complexity for the same DP formulation. The difference is in execution style and practical constraints.

---

## 7. Space Optimization

### The Key Observation

In most 1D DP problems (problems with a single linear dimension of state), each new `dp[i]` only depends on a **fixed number of previous entries** — not the entire history of the dp array.

For Climbing Stairs: `dp[i] = dp[i-1] + dp[i-2]`

You only ever need the **last two values**. Once you've computed `dp[i]`, you will never look at `dp[i-2]` again. Keeping the full dp array is wasteful.

### Rolling Variables Optimization

Instead of maintaining an array of size $n+1$, collapse it to just two variables. Each variable is named to carry semantic meaning — this is critical for understanding the code six months later:

```python
def climb_optimized(n):
    if n <= 2:
        return n
    prev2 = 1   # Ways to reach step i-2 (the step two behind current)
    prev1 = 2   # Ways to reach step i-1 (the step one behind current)
    for i in range(3, n + 1):
        curr  = prev1 + prev2   # Ways to reach step i (current target step)
        prev2 = prev1           # Shift window: i-2 becomes old i-1
        prev1 = curr            # Shift window: i-1 becomes the step we just computed
    return prev1                # prev1 now holds ways to reach step n
```

```text
Rolling Window Execution for n=5:

                   prev2                prev1               curr
                (ways to i-2)       (ways to i-1)       (ways to i)

Initial:  prev2=1 [ways to step 1], prev1=2 [ways to step 2]
i=3:  curr = 2 + 1 = 3  →  prev2=2 [ways to step 2], prev1=3 [ways to step 3]
i=4:  curr = 3 + 2 = 5  →  prev2=3 [ways to step 3], prev1=5 [ways to step 4]
i=5:  curr = 5 + 3 = 8  →  prev2=5 [ways to step 4], prev1=8 [ways to step 5]
Return prev1 = 8  (ways to reach step 5)
```

Space drops from $O(n)$ to $O(1)$ — constant space regardless of how large `n` gets.

### When Space Optimization Is Possible

Space optimization applies when:
*   Each state depends only on a fixed, small number of preceding states.
*   You can identify those exact states and name them as variables.

It does **not** apply when you need to reconstruct the actual solution path (e.g., which items were included in a knapsack), because rolling variables discard history.

---

## 8. Complexity Analysis

### Time Complexity: $O(n)$

Every DP formulation for 1D problems visits each of the $n$ states exactly once. Inside each state, a constant amount of work is done (looking up previous values, computing a max or min, adding a constant number of operands). There is no branching, no re-computation, no nested looping over states. Total: $O(n \cdot 1) = O(n)$.

Compare this to naive recursion at $O(2^n)$ — for $n = 40$, that is the difference between 40 operations and over 1 trillion.

### Space Complexity

| Approach | Space |
| :--- | :--- |
| Naive Recursion | $O(n)$ call stack depth |
| Top-Down Memoization | $O(n)$ memo cache + $O(n)$ call stack = $O(n)$ |
| Bottom-Up Tabulation | $O(n)$ dp array |
| Space-Optimized | $O(1)$ — just rolling variables |

---

## 9. DP Template

The structural skeleton for any 1D DP problem follows the same five-step ritual:

```python
def dp_template(n, input_data):
    # Step 1: Define the DP array and what dp[i] represents
    dp = [0] * (n + 1)
    
    # Step 2: Initialize base cases (the ground truth anchors)
    dp[0] = <base_case_value_for_0>
    dp[1] = <base_case_value_for_1>
    
    # Step 3: Fill the table iteratively from the bottom up
    for i in range(2, n + 1):
        # Step 4: Apply the recurrence relation
        # dp[i] = some combination of dp[i-1], dp[i-2], input_data[i], etc.
        dp[i] = max(dp[i - 1], dp[i - 2] + input_data[i])  # example
    
    # Step 5: Return the answer (often dp[n] or max of a subset)
    return dp[n]
```

### The Five-Step Mental Checklist

Before writing a single line of code for any DP problem:

1.  **What is `dp[i]`?** Define precisely what value is stored at each index. If you cannot articulate this in one clear sentence, you are not ready to write the recurrence.
2.  **What are the base cases?** What are the smallest inputs you can answer directly without recursion?
3.  **What is the recurrence relation?** How does `dp[i]` depend on previous values?
4.  **What order do we fill the table?** Left to right, right to left, or something else?
5.  **Where is the final answer?** Is it `dp[n]`, `max(dp)`, `dp[-1]`, or something else?

---

## 10. Universal DP Checklist

Every single DP problem in existence — from beginner to advanced — can be fully specified by filling in these six boxes before writing a single line of code. Use this as your checklist in every interview.

```text
┌─────────────────────────────────────────────────────────────────┐
│  BOX 1 — STATE                                                  │
│  What does dp[i] represent?                                     │
│  Write it in one complete English sentence.                     │
│  e.g. "dp[i] = max money robbed from first i houses"           │
├─────────────────────────────────────────────────────────────────┤
│  BOX 2 — TRANSITION (State → Choices → Recurrence)             │
│  What are the choices at state i?                               │
│  How does dp[i] depend on previous states?                      │
│  e.g. "Skip i → dp[i-1]   |   Rob i → nums[i] + dp[i-2]"      │
│       "Take better: dp[i] = max(dp[i-1], nums[i] + dp[i-2])"  │
├─────────────────────────────────────────────────────────────────┤
│  BOX 3 — BASE CASES                                             │
│  What are the smallest sub-problems you can answer directly?    │
│  e.g. "dp[0] = 0 (no houses), dp[1] = nums[0]"                │
├─────────────────────────────────────────────────────────────────┤
│  BOX 4 — TRAVERSAL ORDER                                        │
│  In which direction must you fill the table?                    │
│  e.g. "Left to right — dp[i] only reads from dp[i-1], dp[i-2]"│
├─────────────────────────────────────────────────────────────────┤
│  BOX 5 — ANSWER LOCATION                                        │
│  Where in the dp array does the final answer live?              │
│  e.g. "dp[n]" or "max(dp)" or "dp[n][m]"                      │
├─────────────────────────────────────────────────────────────────┤
│  BOX 6 — OPTIMIZATION                                           │
│  Can space be reduced? How many previous states are needed?     │
│  e.g. "Only dp[i-1] and dp[i-2] → two rolling variables → O(1)"│
└─────────────────────────────────────────────────────────────────┘
```

If you can fill all six boxes before opening your editor, you will not get stuck on the implementation. The boxes force you to think before coding.

---

## 11. Common Applications

Dynamic Programming appears across nearly every domain of algorithm design:

*   **Sequence Optimization:** Longest Increasing Subsequence, Longest Common Subsequence, Edit Distance.
*   **Path Problems:** Minimum Path Sum in a grid, Unique Paths, Dungeon Game.
*   **Decision Problems:** 0/1 Knapsack, Coin Change, Partition Equal Subset Sum.
*   **String Problems:** Palindrome partitioning, Word Break, Regular Expression Matching.
*   **Game Theory:** Stone Game, Burst Balloons, optimal strategy problems.
*   **Counting Problems:** Count ways to climb stairs, decode ways, number of ways to tile a board.

1D DP is the gateway. Once its mental model is internalized, 2D DP (grids), interval DP, and tree DP all follow naturally — the only change is the dimensionality of the state space.

---

## 12. Common Mistakes

*   **Not defining `dp[i]` clearly before writing code.** This is the single most common root cause of wrong answers in DP. The recurrence relation must fall directly out of the definition of `dp[i]`.
*   **Getting base cases wrong.** Off-by-one errors in DP base cases cascade through the entire table. Always verify `dp[0]` and `dp[1]` manually before trusting the loop.
*   **Accessing `dp[i-1]` when `i=0`.** This causes an index-out-of-bounds error. Guard base cases before starting the loop, or start the loop at index 2.
*   **Mutating input during space optimization.** When compressing the dp array to variables, ensure you update in the correct order — computing the new value before overwriting the old one.
*   **Confusing Top-Down with Bottom-Up.** Recursion + memo = Top-Down. Iteration + table = Bottom-Up. They solve the same problem but require different mental models.
*   **Forgetting to handle the circular constraint in variants (like House Robber II).** Not all DP problems are linear. Recognize when the structure imposes additional constraints that break the standard recurrence.
*   **Not labeling rolling variables.** After space optimization, variables like `prev1` and `prev2` look identical to someone reading the code cold. Always comment what each variable represents semantically — not just its position in the array.

---

## DP Recognition Signals

This is the most important skill in dynamic programming. Getting the right answer on a problem you've memorized means nothing. Recognizing that an unfamiliar problem is a DP problem and building the solution from scratch is what mastery looks like.

### The Core Question to Ask

> "If I solve this smaller version of the problem optimally, does that help me solve the larger version optimally?"

If yes, you likely have optimal substructure. Now ask:

> "Would a naive recursive approach re-solve the same sub-problem multiple times?"

If yes, you have overlapping subproblems. Together, they confirm: **this is a DP problem**.

### Keyword Red Flags in the Problem Statement

When you see these phrases, your brain should immediately activate DP mode:

| Signal Phrase | What It Hints At |
| :--- | :--- |
| **"Maximum"** or **"Minimum"** | Optimization DP — maximize or minimize some value |
| **"Count ways"** or **"Number of ways"** | Counting DP — count distinct sequences or arrangements |
| **"Can we reach..."** | Feasibility DP — determine if a state is reachable |
| **"Number of paths"** | Path DP — count distinct routes through a structure |
| **"Choose or skip"** | Include/Exclude DP — at each step, make a binary decision |
| **"Previous decision affects future"** | State dependency — classic DP signal |
| **"Repeated recursive states"** | Direct confirmation of overlapping subproblems |
| **"Optimal strategy"** | Game theory DP or decision DP |
| **"Partition"** or **"Split"** | Interval DP or subset DP |

### Structural Red Flags

Beyond keywords, look at the structure of the problem itself:

*   **Linear sequence:** An array or string where you make a decision at each position, and that decision affects what choices are available later. *(Climbing Stairs, House Robber)*
*   **Two sequences:** You are comparing or aligning two strings or arrays. *(Longest Common Subsequence, Edit Distance)*
*   **A grid:** You traverse a 2D matrix from one corner to another. *(Unique Paths, Min Path Sum)*
*   **A circular constraint:** The problem has the same structure as a linear DP but the first and last elements are connected. *(House Robber II)*
*   **Exponential brute-force:** If the obvious recursive solution branches into two or more recursive sub-calls and the problem size is large, the solution tree has likely $2^n$ or more leaves — DP is the fix.

### The "Previous Decision Affects Future" Test

The most reliable mental test: **"Does what I choose at step `i` constrain my options at step `i+1`?"**

*   Climbing Stairs: If I'm currently on step `i`, I could have arrived from step `i-1` or `i-2`. The number of ways to reach `i` depends on previous counts. ✓
*   House Robber: If I rob house `i`, I cannot rob house `i+1`. My decision at `i` directly constrains step `i+1`. ✓
*   Simple array sum: Every element is always included regardless of what came before. ✗ — No DP needed.

### The DP Decision Tree

Once you believe a problem is DP, use this three-step decision tree to choose your implementation strategy:

```text
Does the recursion tree repeat the same state?
           │
           ▼ YES
    Apply Memoization (Top-Down)
    → Add a cache dict, return cached values
           │
           ▼
Can the recurrence be computed in a fixed left-to-right order?
           │
           ▼ YES
    Switch to Tabulation (Bottom-Up)
    → Replace recursion + cache with an iterative dp[] array
           │
           ▼
Does dp[i] only need the last k states (k is small and fixed)?
           │
           ▼ YES
    Apply Space Optimization
    → Replace dp[] array with k rolling variables → O(1) space
```

This is the universal DP implementation pipeline. Every problem you encounter follows this exact progression.

### Master Construction Sequence

Once you confirm this is a DP problem, follow this exact construction sequence:

```text
Step 1:  Identify the state variable(s).
         What information uniquely defines a sub-problem?
         → Usually the index i, and possibly one or two additional parameters.

Step 2:  Define dp[i] precisely.
         "dp[i] is the ___ for the sub-problem involving the first i elements."

Step 3:  Enumerate the choices at state i.
         What are all possible last actions that could have led to state i?
         These choices become the branches of your recurrence.

Step 4:  Derive the recurrence relation from the choices.
         For each choice, express the cost/count in terms of previous dp values.
         Then combine them (max, min, sum, etc.).

Step 5:  Identify base cases.
         What are the smallest inputs you can answer directly?
         These anchor the entire table.

Step 6:  Determine traversal order and answer location.
         Fill left to right if recurrence reads backward. Return dp[n] or similar.

Step 7:  Code → bottom-up table → then space optimize if possible.
```

---

## Problem: Climbing Stairs

*   **Interview Difficulty:** Easy
*   **Parent Pattern:** Linear DP — Fibonacci Recurrence (Counting)
*   **Problem Type:** 1D DP / Counting Ways / Linear Recurrence
*   **Data Structure Used:** DP Array (`list[int]`) → Space-Optimized to Two Variables
*   **Approach 1:** Naive Recursion. Define `f(n) = f(n-1) + f(n-2)` with base cases `f(1)=1`, `f(2)=2`. This mirrors the Fibonacci sequence exactly. Correct, but $O(2^n)$ time due to exponential re-computation of overlapping sub-calls.
*   **Optimized Approach:** Bottom-Up Tabulation with space optimization.

### State → Choices → Transition → Recurrence

```text
STATE
─────
dp[i] = number of distinct ways to reach step i

↓

CHOICES at step i
─────────────────
There are exactly two possible last moves that land on step i:

  Choice 1: Arrived from step i-1 (took a 1-step jump)
  Choice 2: Arrived from step i-2 (took a 2-step jump)

↓

TRANSITION
──────────
These two choices are exhaustive — no other move can land on step i.
They are also mutually exclusive — a path arriving via choice 1
cannot simultaneously arrive via choice 2.

Therefore, the total ways to reach step i is the union of both:
  Ways arriving via 1-step = dp[i-1]   (all ways to be at i-1, then jump once)
  Ways arriving via 2-step = dp[i-2]   (all ways to be at i-2, then jump twice)

↓

RECURRENCE (derived from choices)
──────────────────────────────────
dp[i] = dp[i-1] + dp[i-2]
```

### Recurrence Derivation

Why is it `dp[i-1] + dp[i-2]` and not something else?

To be standing on step `i`, you must have come from exactly one of two places: step `i-1` or step `i-2`. There is no third option — the problem only allows 1-step or 2-step moves. These two origin states are completely independent: the paths that pass through `i-1` and the paths that pass through `i-2` are disjoint sets with zero overlap. For disjoint sets of outcomes, we add their counts. Therefore: $dp[i] = dp[i-1] + dp[i-2]$.

*   **Complexity:**
    *   **Time:** $O(n)$ — each of the $n$ states is computed exactly once in a single forward pass.
    *   **Space:** $O(1)$ after space optimization — only two scalar variables are maintained regardless of input size.
*   **Pointer Flow:**
```text
Counting ways to reach step n = 5:

dp[1] = 1  (base: only one way to reach step 1 → take one 1-step)
dp[2] = 2  (base: two ways → {1+1} or {2})

i=3: dp[3] = dp[2] + dp[1] = 2 + 1 = 3   → {1,1,1} or {1,2} or {2,1}
i=4: dp[4] = dp[3] + dp[2] = 3 + 2 = 5
i=5: dp[5] = dp[4] + dp[3] = 5 + 3 = 8

Answer: 8 distinct ways to climb 5 stairs.

Space-Optimized Rolling Window:

                   prev2                   prev1               curr
             (ways to step i-2)      (ways to step i-1)   (ways to step i)

Initial:  prev2=1 [ways to step 1], prev1=2 [ways to step 2]
i=3:  curr=3  →  prev2=2 [ways to step 2], prev1=3 [ways to step 3]
i=4:  curr=5  →  prev2=3 [ways to step 3], prev1=5 [ways to step 4]
i=5:  curr=8  →  prev2=5 [ways to step 4], prev1=8 [ways to step 5]
Return prev1 = 8
```
*   **Pattern Recognition:**
    *   Use 1D counting DP with a Fibonacci-style recurrence when:
        *   You can reach state `i` from a fixed, small set of preceding states (here, `i-1` and `i-2`).
        *   The number of ways to reach state `i` is the sum of ways to reach each of its predecessors.
*   **Core Insight:** This problem is Fibonacci in disguise. The number of ways to reach step `n` is exactly `fib(n)` when indexed from step 1. Recognizing the Fibonacci pattern immediately points to the recurrence relation. The transition `dp[i] = dp[i-1] + dp[i-2]` encodes the two choices available at every step: arrive via a single step or a double step. The structure is additive, not multiplicative, because the two paths are mutually exclusive alternatives.
*   **Mistakes Made:** The initial trap is starting the base case at `dp[0] = 1`, `dp[1] = 1` (like Fibonacci indexed from 0) and accidentally returning `dp[n]` when the problem is 1-indexed. This causes an off-by-one error for small inputs. Always re-derive the base cases from the problem statement directly rather than importing them from memory.
*   **What I Learned:** DP problems often wear disguises. Climbing Stairs looks like a novel problem but reduces to Fibonacci the moment you write the recurrence. The skill is not memorizing that Climbing Stairs = Fibonacci, but developing the habit of writing the recurrence first and recognizing familiar patterns from there.

---

## Problem: Min Cost Climbing Stairs

*   **Interview Difficulty:** Easy
*   **Parent Pattern:** Linear DP — Minimum Cost Optimization
*   **Problem Type:** 1D DP / Optimization / Minimum Cost Path
*   **Data Structure Used:** DP Array (`list[int]`) with a virtual "top" node beyond the array
*   **Approach 1:** Greedy. Try to always pick the cheaper stair. This fails because locally cheap choices can force you into an expensive sequence later. Greedy cannot handle decisions that ripple across multiple future states.
*   **Optimized Approach:** Bottom-Up Tabulation with a virtual top node at index `n`.

### State → Choices → Transition → Recurrence

```text
STATE
─────
dp[i] = minimum cost to ARRIVE at position i
        (you have not yet paid for stepping off from i)

↓

CHOICES at position i
─────────────────────
To arrive at position i, you must have departed from one of two places:

  Choice 1: Departed from position i-1 (paid cost[i-1] to jump one step)
  Choice 2: Departed from position i-2 (paid cost[i-2] to jump two steps)

↓

TRANSITION
──────────
These two departure points are exhaustive — no other origin can
reach position i in a single legal move.

  Cost via choice 1: dp[i-1] + cost[i-1]
                     (cheapest way to reach i-1) + (cost of stepping off i-1)

  Cost via choice 2: dp[i-2] + cost[i-2]
                     (cheapest way to reach i-2) + (cost of stepping off i-2)

We want the minimum:

↓

RECURRENCE (derived from choices)
──────────────────────────────────
dp[i] = min(dp[i-1] + cost[i-1],  dp[i-2] + cost[i-2])

The "top" of the staircase is index n (one past the last stair).
dp[0] = dp[1] = 0 because you can start at step 0 or step 1 for free —
you haven't departed from anywhere yet.
```

### Recurrence Derivation

Why does the cost attach to the *departure* stair, not the *arrival* stair?

Because `cost[i]` is defined as the cost you pay when you *step off* from stair `i`. You are not charged for landing on a stair — you are charged for leaving it. So to compute the total cost of arriving at position `i` via step `i-1`, the formula is: (best cost to get to `i-1`) + (cost of leaving `i-1`). The destination `i` itself incurs no cost in this formula — it will only incur a cost if we later depart *from* `i` toward a higher position. This is why the virtual top node at index `n` has no departure cost: it is the final destination, never a departure point.

*   **Complexity:**
    *   **Time:** $O(n)$ — a single left-to-right pass filling $n+1$ states.
    *   **Space:** $O(n)$ for the dp array, optimizable to $O(1)$ by keeping only two rolling variables.
*   **Pointer Flow:**
```text
Minimum cost path through cost = [10, 15, 20]:
n = 3  →  dp has indices 0..3, where index 3 is the "top" (exit point)

dp[0] = 0   (arrive at step 0 for free — you start here, no departure was made)
dp[1] = 0   (arrive at step 1 for free — you start here, no departure was made)

i=2:  dp[2] = min(dp[1] + cost[1],   dp[0] + cost[0])
            = min(0    + 15,          0    + 10)
            = min(15, 10) = 10
            (cheaper: jump from step 0, pay cost[0]=10)

i=3:  dp[3] = min(dp[2] + cost[2],   dp[1] + cost[1])
            = min(10   + 20,          0    + 15)
            = min(30, 15) = 15
            (cheaper: jump from step 1, pay cost[1]=15)

Answer: dp[3] = 15

Rolling Variables:
                   prev2                   prev1               curr
          (min cost to arrive i-2)  (min cost to arrive i-1)  (min cost to arrive i)

Initial:  prev2=0 [cost to reach step 0], prev1=0 [cost to reach step 1]
i=2:  curr=10  →  prev2=0 [step 1], prev1=10 [step 2]
i=3:  curr=15  →  prev2=10 [step 2], prev1=15 [step 3 = top]
Return prev1 = 15
```
*   **Pattern Recognition:**
    *   Use minimum-cost 1D DP when:
        *   You are traversing a sequence and must pay a cost at each position you visit.
        *   You can skip positions (jump over them), so greedy fails because bypassing an expensive position requires looking ahead.
        *   The recurrence relates the cost to reach state `i` as a minimum of costs to reach its predecessors plus the transition cost.
*   **Core Insight:** The key design decision is defining `dp[i]` as the cost to *arrive at* position `i` — not the cost to *leave from* position `i`. This allows the virtual top node at index `n` to serve as the exit point with no cost of its own. The cost you pay is attached to the stair you *depart from*, not the one you land on. Keeping the departure cost at `cost[i-1]` and `cost[i-2]` instead of `cost[i]` ensures you pay correctly for the stair you pushed off from.
*   **Mistakes Made:** The most common error is building the dp array of size `n` instead of `n+1`, making the exit point impossible to represent. The second mistake is setting base cases as `dp[0] = cost[0]` and `dp[1] = cost[1]` — this is wrong because you haven't paid any cost yet simply by standing at the start. You only pay when you take a step upward, so the base cases must be `dp[0] = dp[1] = 0`.
*   **What I Learned:** The definition of `dp[i]` determines everything — the base cases, the recurrence, and where the answer lives. Spending 30 seconds to precisely define what `dp[i]` means before touching the keyboard eliminates the majority of DP bugs before they are born.

---

## Problem: House Robber

*   **Interview Difficulty:** Medium
*   **Parent Pattern:** Linear DP — Include/Exclude Decision
*   **Problem Type:** 1D DP / Optimization / Include-Exclude Decision
*   **Data Structure Used:** DP Array (`list[int]`) → Space-Optimized to Two Rolling Variables
*   **Approach 1:** Naive Brute Force. Try every subset of non-adjacent houses and track the maximum sum. This is $O(2^n)$ because there are $2^n$ possible subsets, making it completely infeasible for large inputs.
*   **Optimized Approach:** Bottom-Up Include-Exclude DP with space optimization.

### State → Choices → Transition → Recurrence

```text
STATE
─────
dp[i] = maximum money that can be robbed from the first i houses
        (houses indexed 1 to i, where house i corresponds to nums[i-1])

↓

CHOICES at house i
──────────────────
At every house, there are exactly two decisions:

  Choice 1: SKIP house i
            → Don't rob house i. Best answer remains whatever we had before.
            → Contribution: dp[i-1]

  Choice 2: ROB house i
            → Rob house i for nums[i] dollars.
            → Cannot have robbed house i-1 (adjacency constraint).
            → Must go back to the best answer ending at house i-2.
            → Contribution: dp[i-2] + nums[i]

↓

TRANSITION
──────────
Skip and Rob are mutually exclusive — you cannot do both.
They are also exhaustive — no third option exists.
We want to maximize loot, so we take whichever choice yields more:

  If Skip wins:  dp[i] = dp[i-1]
  If Rob wins:   dp[i] = dp[i-2] + nums[i]
  In general:    dp[i] = max of both

↓

RECURRENCE (derived from choices)
──────────────────────────────────
dp[i] = max(dp[i-1],  nums[i] + dp[i-2])
             ↑ skip        ↑ rob
```

### Recurrence Derivation

Why is there no other option besides `dp[i-1]` and `dp[i-2] + nums[i]`?

Think about it from the perspective of the last house robbed before or at position `i`:

*   If the last robbed house is **not** `i`: Then house `i` was skipped. The answer is the same as the best answer achievable in houses 1 through `i-1`, which is exactly `dp[i-1]`.
*   If the last robbed house **is** `i`: Then house `i-1` must have been skipped (the adjacency rule). The last robbed house before `i` can be at most `i-2`. The best answer up to `i-2` is `dp[i-2]`, and adding `nums[i]` gives the total.

These two cases cover all possibilities with no overlap. Therefore the recurrence is exactly `max(dp[i-1], dp[i-2] + nums[i])` — no other cases exist.

*   **Complexity:**
    *   **Time:** $O(n)$ — single forward pass through the array, one comparison per house.
    *   **Space:** $O(1)$ — only two variables maintained at any time regardless of input size.
*   **Pointer Flow:**
```text
Maximum loot from nums = [2, 7, 9, 3, 1]:

                   prev2                        prev1                   curr
          (max loot from first i-2 houses)  (max loot from first i-1)  (max loot at i)

Initial: prev2=0 [loot with 0 houses], prev1=0 [loot with 0 houses]

num=2:  curr = max(prev1=0, prev2+2=0+2=2) = 2  →  prev2=0, prev1=2  [max from house 1]
num=7:  curr = max(prev1=2, prev2+7=0+7=7) = 7  →  prev2=2, prev1=7  [max from houses 1-2]
num=9:  curr = max(prev1=7, prev2+9=2+9=11)= 11 →  prev2=7, prev1=11 [max from houses 1-3]
num=3:  curr = max(prev1=11,prev2+3=7+3=10)= 11 →  prev2=11,prev1=11 [max from houses 1-4]
num=1:  curr = max(prev1=11,prev2+1=11+1=12)=12 →  prev2=11,prev1=12 [max from houses 1-5]

Answer: prev1 = 12  → Rob houses at indices 0 (2), 2 (9), 4 (1) = 2 + 9 + 1 = 12
```
*   **Pattern Recognition:**
    *   Use Include-Exclude DP when:
        *   You must make a binary decision at each position (include or skip this element).
        *   Including an element at position `i` prevents you from including the element at `i+1` (adjacency constraint).
        *   You want to maximize the total value of included elements.
*   **Core Insight:** The elegance of House Robber is that the constraint ("cannot rob adjacent houses") translates perfectly into the recurrence. The "skip" branch carries forward the best answer without touching position `i`. The "rob" branch skips two positions back to `dp[i-2]` to enforce the no-adjacency rule. These two branches are mutually exclusive at every step, making the problem perfectly suited to bottom-up DP without backtracking or branch tracking.
*   **Mistakes Made:** The primary trap is starting the loop at index 0 and accessing `dp[-2]` which wraps around in Python and returns the last element of the array — a silent bug that corrupts results for small arrays. Always pad the dp array or initialize `prev2 = 0` before the first element to represent the "no houses yet" base state cleanly.
*   **What I Learned:** "Previous decision affects future" is the most reliable DP trigger phrase. The moment you see a problem where choosing an element eliminates neighboring choices, the Include-Exclude DP pattern applies. The rolling variable optimization is especially natural here because `dp[i]` only ever needs `dp[i-1]` and `dp[i-2]`.

---

## Problem: House Robber II

*   **Interview Difficulty:** Medium
*   **Parent Pattern:** Linear DP — Circular Constraint Decomposition
*   **Problem Type:** 1D DP / Optimization / Circular Array Constraint Decomposition
*   **Data Structure Used:** Two separate House Robber I runs on sliced sub-arrays
*   **Approach 1:** Brute Force. Try every valid subset of non-adjacent houses in the circular layout. Exponential time, completely infeasible.
*   **Optimized Approach:** Circular Constraint Decomposition into two linear sub-problems.

### State → Choices → Transition → Recurrence

```text
STATE
─────
Same as House Robber I: dp[i] = max loot from first i houses in a sub-range.

But the circular constraint adds a new dependency:
  house[0] and house[n-1] are NEIGHBORS — cannot rob both.

↓

CHOICES at the top level (before any house-level decisions)
───────────────────────────────────────────────────────────
The constraint "house 0 and house n-1 cannot both be robbed" implies:

  Choice A: Exclude house n-1 from consideration
            → Run House Robber I on houses [0 ... n-2]
            → House 0 may be freely included

  Choice B: Exclude house 0 from consideration
            → Run House Robber I on houses [1 ... n-1]
            → House n-1 may be freely included

↓

TRANSITION
──────────
These two cases are exhaustive: in every valid solution, at least one
of {house 0, house n-1} must be excluded (or both excluded).
Both cases are covered by the two slices.

We want the global maximum across both scenarios:

↓

RECURRENCE (derived from choices)
──────────────────────────────────
answer = max( house_robber_I(nums[:-1]),   house_robber_I(nums[1:]) )
                    ↑ Choice A                     ↑ Choice B
```

### Recurrence Derivation

Why does running House Robber I on the two slices guarantee correctness?

In any optimal solution for the circular problem, house `0` and house `n-1` cannot both be robbed. This means every valid solution falls into one of three sub-cases:
1.  House `0` is robbed, house `n-1` is not → captured by `nums[:-1]` (excludes last).
2.  House `n-1` is robbed, house `0` is not → captured by `nums[1:]` (excludes first).
3.  Neither is robbed → captured by **both** slices (since excluding either endpoint still considers solutions that skip both).

All three sub-cases are covered by the maximum of the two slice results. No valid optimal solution can escape both slices simultaneously, so the maximum is guaranteed to be the global optimum.

*   **Complexity:**
    *   **Time:** $O(n)$ — two separate $O(n)$ linear passes over arrays of length $n-1$ each.
    *   **Space:** $O(1)$ — both sub-runs use rolling variables with no extra allocation.
*   **Pointer Flow:**
```text
Maximum loot from circular nums = [2, 3, 2]:
n = 3

CHOICE A — Exclude last house: rob_range([2, 3])

                prev2                   prev1               curr
         (max loot 0 houses)      (max loot 0 houses)   (max loot current)

  prev2=0, prev1=0
  num=2: curr=max(prev1=0, prev2+2=2)=2   → prev2=0 [0 houses], prev1=2 [house 0]
  num=3: curr=max(prev1=2, prev2+3=3)=3   → prev2=2 [house 0],  prev1=3 [houses 0-1]
  Result A = 3

CHOICE B — Exclude first house: rob_range([3, 2])

  prev2=0, prev1=0
  num=3: curr=max(prev1=0, prev2+3=3)=3   → prev2=0 [0 houses], prev1=3 [house 1]
  num=2: curr=max(prev1=3, prev2+2=2)=3   → prev2=3 [house 1],  prev1=3 [houses 1-2]
  Result B = 3

Answer: max(3, 3) = 3
Validation: Cannot rob both house 0 (val=2) and house 2 (val=2) as circular neighbors.
Best = rob house 1 (val=3) only.
```
*   **Pattern Recognition:**
    *   Use circular array decomposition when:
        *   The problem is a direct extension of a linear DP problem with an additional constraint connecting the first and last elements.
        *   The circular constraint creates a dependency that cannot be captured in a single recurrence over the full array.
        *   You can enforce the constraint by eliminating one endpoint at a time and solving two independent linear instances.
*   **Core Insight:** The insight that makes this problem tractable is recognizing that the circular adjacency constraint can be broken into two mutually exclusive and exhaustive cases. In *any* valid solution, house `0` and house `n-1` are never both robbed. Therefore, exactly one of the two scenarios (exclude first, exclude last) must contain the global optimum. Running House Robber I on both sub-arrays and taking the maximum is guaranteed to find it. This is a classic example of **constraint decomposition** — reducing an apparently harder problem into two instances of a problem you already know how to solve.
*   **Mistakes Made:** The primary edge case to handle before the two-slice approach is `len(nums) == 1`. If there is only one house, neither slice works correctly (both slices would be empty arrays). Guard this with an early return: `if len(nums) == 1: return nums[0]`.
*   **What I Learned:** When a DP problem adds a circular or wrapped constraint on top of a known linear structure, the strategy is to break that constraint with exhaustive case decomposition rather than inventing a new recurrence. Recognizing that House Robber II is House Robber I applied twice cuts what looks like a harder problem back down to a known template.

---

## Pattern Summary

Quick-revision reference for all patterns introduced in Day 1. Every future DP day will extend this table.

| Problem | State `dp[i]` | Transition (Recurrence) | Optimization |
| :--- | :--- | :--- | :--- |
| **Climbing Stairs** | Ways to reach step `i` | `dp[i-1] + dp[i-2]` | Two rolling vars: `prev2` (ways to i-2), `prev1` (ways to i-1) |
| **Min Cost Climbing Stairs** | Min cost to *arrive* at position `i` | `min(dp[i-1]+cost[i-1], dp[i-2]+cost[i-2])` | Two rolling vars: `prev2` (cost to i-2), `prev1` (cost to i-1) |
| **House Robber** | Max loot from first `i` houses | `max(dp[i-1], nums[i]+dp[i-2])` | Two rolling vars: `prev2` (max to i-2), `prev1` (max to i-1) |
| **House Robber II** | Same as above, applied twice on slices | `max(rob(nums[:-1]), rob(nums[1:]))` | Two slice calls, each $O(1)$ space internally |

---

## Master Patterns Learned

#### 1. Linear Counting DP (The Fibonacci Recurrence Template)

*   **Recognition:** "Count ways" or "How many distinct paths" over a linear sequence where each state is reachable from a fixed number of prior states.
*   **State:** `dp[i]` = number of distinct ways to reach state `i`.
*   **Transition:** `dp[i] = dp[i-1] + dp[i-2]` — counts from independent predecessor states add together because they represent disjoint paths.
*   **Traversal Order:** Left to right — `dp[i]` only reads from `dp[i-1]` and `dp[i-2]`, both already finalized.
*   **Optimization:** Two rolling variables. `prev2` = ways to reach `i-2`. `prev1` = ways to reach `i-1`. After each step: `curr = prev1 + prev2`, then shift the window.
*   **Examples:** Climbing Stairs, Fibonacci Number, Decode Ways, Tile a Floor.

```python
def linear_counting_dp(n: int) -> int:
    if n <= 2:
        return n
    prev2 = 1   # Ways to reach step i-2 (the step two behind current)
    prev1 = 2   # Ways to reach step i-1 (the step one behind current)
    for i in range(3, n + 1):
        curr  = prev1 + prev2   # Ways to reach step i: sum of two predecessor counts
        prev2 = prev1           # Shift: i-2 slot becomes old i-1
        prev1 = curr            # Shift: i-1 slot becomes newly computed i
    return prev1                # Holds ways to reach step n
```

---

#### 2. Include-Exclude Decision DP (The Non-Adjacent Selection Template)

*   **Recognition:** "Maximum/minimum from an array where adjacent elements cannot both be chosen." Binary decision (include or skip) at every position, where include forbids the next position.
*   **State:** `dp[i]` = maximum value achievable using elements from positions 1 through `i`.
*   **Transition:** `dp[i] = max(dp[i-1], nums[i] + dp[i-2])` — skip (carry forward `dp[i-1]`) or rob (add current value to best-before-previous `dp[i-2]`).
*   **Traversal Order:** Left to right — at each `i`, both `dp[i-1]` (skip branch) and `dp[i-2]` (rob branch) are finalized.
*   **Optimization:** Two rolling variables. `prev2` = max loot up to position `i-2`. `prev1` = max loot up to position `i-1`. After each step: `curr = max(prev1, prev2 + num)`.
*   **Examples:** House Robber, Delete and Earn, alternating sequence maximization.

```python
def include_exclude_dp(nums: list[int]) -> int:
    prev2 = 0   # Max loot achievable from positions ending two before current
    prev1 = 0   # Max loot achievable from positions ending one before current
    for num in nums:
        curr  = max(prev1, prev2 + num)   # Skip (prev1) vs Rob (prev2 + current value)
        prev2 = prev1                      # Shift window forward
        prev1 = curr                       # New best becomes i-1 for next iteration
    return prev1                           # Holds max loot from all n positions
```

---

#### 3. Circular Constraint Decomposition (The Two-Slice Reduction)

*   **Recognition:** A linear DP problem where the first and last elements are declared neighbors, creating a circular constraint. The phrase "arranged in a circle" or "first and last are adjacent" is the trigger.
*   **State:** Same state definition as the underlying linear DP, applied independently to two sub-arrays.
*   **Transition:** Decompose the circular constraint into two exhaustive cases — exclude the first element OR exclude the last element. Run the linear DP on each slice. The answer is the maximum of both results.
*   **Traversal Order:** Same as underlying linear DP (left to right) applied twice on sliced sub-arrays.
*   **Optimization:** Each slice runs in $O(1)$ space using rolling variables. Total: two $O(n)$ passes, $O(1)$ space.
*   **Examples:** House Robber II, circular array maximum non-adjacent sum.

```python
def circular_dp_reduction(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]   # Edge case: single element, only one house

    def linear_rob(arr):
        prev2, prev1 = 0, 0             # prev2: max to i-2,  prev1: max to i-1
        for num in arr:
            curr = max(prev1, prev2 + num)
            prev2, prev1 = prev1, curr
        return prev1

    # Case A: Exclude house n-1 → house 0 is free to include
    # Case B: Exclude house 0   → house n-1 is free to include
    return max(linear_rob(nums[:-1]), linear_rob(nums[1:]))
```
