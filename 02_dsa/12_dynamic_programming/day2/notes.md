# 1D Decision DP

## 1. Decision DP

At its core, **Decision DP** is the algorithmic formalization of optimal decision-making over sequential choices. In a Decision DP problem, you stand at index `i` of a sequence and must make a discrete choice — typically a binary decision: **Take (Include)** or **Skip (Exclude)**.

Unlike simple greedy algorithms that lock in locally attractive choices, Decision DP evaluates every available choice at step `i` by combining the immediate reward/cost of that choice with the optimal future (or past) outcome of remaining states.

### Core Mechanics of Decision DP

```text
At State i:
                   ┌─────────────────────────────┐
                   │        State (i)            │
                   └──────────────┬──────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
       Choice 1: SKIP (Exclude)       Choice 2: TAKE (Include)
       ────────────────────────       ────────────────────────
       Immediate Gain: 0              Immediate Gain: Value(i)
       Next State: i - 1              Next State: i - k (or i + k)
       Sub-result: dp[i-1]            Sub-result: Value(i) + dp[i-k]
                  │                               │
                  └───────────────┬───────────────┘
                                  ▼
                    Take Optimal (Max / Min)
                    dp[i] = max(dp[i-1], Value(i) + dp[i-k])
```

1. **Optimization Focus:** Find the global maximum profit, minimum cost, or boolean feasibility across a decision tree.
2. **Sequential Decisions:** Decisions are made element-by-element along an array, string, or range.
3. **State Dependencies:** The choice made at step `i` dictates which previous states (or future states) can be legally combined.

---

## 2. DP State Design

Before writing a single line of code or recurrence relation, you **must** write down a precise, unambiguous definition of what `dp[i]` represents.

> **Rule of Thumb:** If you cannot complete the sentence *"dp[i] represents _______"*, you are not ready to write the recurrence.

### The 5 Essential Components of DP Design

```text
┌─────────────────────────────────────────────────────────────────┐
│ 1. State Definition   │ What does dp[i] store?                  │
│ 2. Transition Choices │ What decisions can be made at state i?  │
│ 3. Recurrence Formula │ Mathematical combination of choices     │
│ 4. Base Cases         │ Smallest sub-problems known directly    │
│ 5. Traversal Order    │ Direction to fill                       │
└─────────────────────────────────────────────────────────────────┘
```

### Practice: Defining `dp[i]`

* **House Robber:** `dp[i]` represents the *maximum money robbed from the first i houses*.
* **Delete and Earn:** `dp[v]` represents the *maximum points earned considering values up to v*.
* **Max Alternating Subsequence Sum:** `dp[i][even]` represents *max alternating sum up to index i ending with addition (+)*; `dp[i][odd]` represents *max alternating sum up to index i ending with subtraction (-)*.
* **Solving Questions With Brainpower:** `dp[i]` represents the *maximum points achievable from question i to question n-1*.

---

## 3. Why Greedy Fails

Greedy algorithms choose the locally largest value at each step. In Decision DP, **local optimum $\neq$ global optimum** because taking one item can block two larger neighbors downstream. DP evaluates both possibilities before committing.

### Counter-Example: Delete and Earn

Suppose total points per value are: `Value 2: 5 pts`, `Value 3: 6 pts`, `Value 4: 5 pts`.

```text
Greedy Strategy (Pick locally largest value):
  1. Pick 3 (earns 6 points).
  2. Rule: Delete adjacent values 2 and 4!
  3. Total Earned = 6 points.

DP Strategy (Evaluates both Take and Skip):
  1. Skip 3 → Free to pick 2 (5 pts) AND 4 (5 pts).
  2. Total Earned = 5 + 5 = 10 points.  <-- GREEDY FAILS!
```

### Why DP Succeeds
Greedy cannot look ahead to see that taking a slightly less valuable element now unlocks multiple valuable choices later. DP systematically compares **Taking** vs **Skipping** across the full state space, guaranteeing the global optimum.

---

## 4. Include–Exclude Pattern

The **Include–Exclude Pattern** is the primary template of 1D Decision DP. At each position `i`, you weigh two fundamental choices:

$$\text{dp}[i] = \max\Big(\text{SKIP}(i), \; \text{TAKE}(i)\Big)$$

```text
                      ┌───────────────────────────┐
                      │    Include - Exclude      │
                      └─────────────┬─────────────┘
                                    │
               ┌────────────────────┴────────────────────┐
               ▼                                         ▼
      SKIP Current Element                      TAKE Current Element
      ────────────────────                      ────────────────────
      Inherit best answer from                  Gain value at i + best answer
      previous state:                           from last valid non-conflicting
      dp[i-1]                                   state: val[i] + dp[i - jump]
               │                                         │
               └────────────────────┬────────────────────┘
                                    ▼
                         Take Maximum / Minimum
```

### Recurring Applications of Include–Exclude

| Problem | SKIP Choice | TAKE Choice | State Jump |
| :--- | :--- | :--- | :--- |
| **House Robber** | `dp[i-1]` | `nums[i] + dp[i-2]` | Fixed jump of 2 (`i-2`) |
| **Delete and Earn** | `dp[v-1]` | `points[v] + dp[v-2]` | Fixed jump of 2 (`v-2`) |
| **Brainpower (2140)** | `dp[i+1]` | `pts[i] + dp[i + skip + 1]` | Variable jump (`i + skip + 1`) |
| **0/1 Knapsack** | `dp[i-1][w]` | `val[i] + dp[i-1][w - wt[i]]` | Weight jump (`w - wt[i]`) |
| **Weighted Job Scheduling**| `dp[i-1]` | `profit[i] + dp[latest_non_overlapping]`| Binary search jump |

---

## 5. Rolling Variable Optimization

When `dp[i]` depends only on a small, fixed window of preceding states (e.g., `dp[i-1]` and `dp[i-2]`), keeping an entire array of size $N$ wastes $O(N)$ memory.

We can compress the array into **$k$ rolling variables**, reducing auxiliary space from $O(N)$ to $O(1)$.

```text
Array Representation O(N):
[ dp[0],  dp[1],  dp[2],  dp[3],  ...  dp[i-2],  dp[i-1],  dp[i] ]
                                           │        │        │
                                           └────────┼────────┘
                                                    ▼
Compressed Variable Representation O(1):
                                       [ prev2 ,  prev1 ]  ──►  curr
```

---

## 6. Universal DP Checklist

Fill in these 6 boxes for every DP problem before writing code:

```text
┌─────────────────────────────────────────────────────────────────┐
│  BOX 1 — STATE                                                  │
│  Define dp[i] in one complete English sentence.                 │
├─────────────────────────────────────────────────────────────────┤
│  BOX 2 — TRANSITION (State → Choices → Recurrence)             │
│  List all choices at state i and write the recurrence formula.  │
├─────────────────────────────────────────────────────────────────┤
│  BOX 3 — BASE CASES                                             │
│  Identify ground truth values for smallest sub-problems.        │
├─────────────────────────────────────────────────────────────────┤
│  BOX 4 — TRAVERSAL ORDER                                        │
│  Determine order of filling (Left→Right or Right→Left) + WHY.   │
├─────────────────────────────────────────────────────────────────┤
│  BOX 5 — ANSWER LOCATION                                        │
│  Specify exact variable/cell containing final answer.          │
├─────────────────────────────────────────────────────────────────┤
│  BOX 6 — OPTIMIZATION                                           │
│  Can space be compressed to O(1) rolling variables?             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. DP Decision Tree

```text
                    Is the problem an optimization/counting task?
                                       │
                                       ▼ YES
               Does a naive recursive solution re-solve identical states?
                                       │
                                       ▼ YES
                            Apply Memoization (Top-Down)
                                       │
                                       ▼
                 Can states be evaluated in a deterministic order?
                                       │
                                       ▼ YES
                            Switch to Tabulation (Bottom-Up)
                                       │
                                       ▼
                    Does dp[i] only look back k fixed steps?
                                      / \
                                YES  /   \  NO
                                    /     \
                                   ▼       ▼
                        Roll k Variables  Keep Full DP Array
                           (O(1) Space)     (O(N) Space)
```

---

## Problem 1: Delete and Earn

* **Interview Difficulty:** Medium
* **Parent Pattern:** 1D Decision DP — House Robber Transformation
* **Problem Type:** Array Transformation / Frequency Preprocessing / Include-Exclude DP
* **Data Structure Used:** Frequency Points Array (`list[int]`) + 2 Rolling Variables (`prev2`, `prev1`)
* **Brute Force:** Generate all $2^N$ subsets of `nums`. For each subset, check if it contains conflicting values ($v$ and $v+1$). Calculate sum of valid subsets and return maximum. $O(2^N \cdot N)$ time, $O(N)$ space.

### DP State
`dp[v]` represents the **maximum points earned considering all values from 0 up to v**.

### State Flow

```text
STATE: dp[v] = max points considering numbers with value <= v

↓

CHOICES at value v:
  Choice 1: SKIP value v  → Inherit dp[v-1]
  Choice 2: TAKE value v  → Gain points[v] + dp[v-2] (cannot take v-1)

↓

TRANSITION: dp[v] = max(dp[v-1], points[v] + dp[v-2])
```

### Recurrence
$$\text{dp}[v] = \max\Big(\text{dp}[v-1], \; \text{points}[v] + \text{dp}[v-2]\Big)$$

**Derivation:**
Taking value `v` yields `points[v] = v * count[v]`. The problem statement dictates that taking `v` deletes all instances of `v-1` and `v+1`. Therefore, we cannot take any points from value `v-1`. The last value we could have safely earned points from is `v-2`, giving `points[v] + dp[v-2]`. Skipping `v` incurs no penalty, leaving `dp[v-1]`. Taking `max(SKIP, TAKE)` yields the optimal `dp[v]`.

### Base Cases
* `dp[0] = 0` (No points from value 0).
* `dp[1] = points[1]` (Only value 1 taken, no negative values exist to delete).

### Traversal Order
**Left to Right (Value 0 $\rightarrow$ Max Value):**
Filled from `v = 2` up to `max(nums)` because `dp[v]` depends on `dp[v-1]` and `dp[v-2]`.

### Pointer Flow

Input: `nums = [3, 4, 2]` $\rightarrow$ `points = [0, 0, 2, 3, 4]`

| Value ($v$) | `points[v]` | `prev2` (val $v-2$) | `prev1` (val $v-1$) | `curr` = $\max(\text{prev1}, \text{prev2} + p)$ | Action |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **0** | 0 | 0 | 0 | **0** | Base 0 |
| **1** | 0 | 0 | 0 | **0** | Base 1 |
| **2** | 2 | 0 | 0 | **2** | Take 2 |
| **3** | 3 | 0 | 2 | **3** | Take 3 (overrides 2) |
| **4** | 4 | 2 | 3 | **6** | Take 4 + 2 (6 > 3) |

**Final Answer:** `prev1 = 6` (Earn value 2 [2 pts] + value 4 [4 pts] = 6)

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N + K)  (N = len(nums), K = max) │
│  Space Complexity │ O(K)      (Frequency points array) │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Taking element $x$ deletes adjacent values $x-1$ and $x+1$
* ✓ Constraint operates on **values**, not array indices
* ✓ Optimization problem (maximize points)
* $\rightarrow$ **Value-Domain Include/Exclude DP**

### Core Insight
Transform the problem from **index-space** to **value-space**. Creating a bucket array `points[v] = v * count[v]` collapses the problem into **House Robber** on `points`, since taking value `v` forbids value `v-1`.

### Common Pitfalls
* Trying to sort `nums` and run DP directly on array indices without grouping identical numbers first.
* Forgetting that taking `v` grants points for **all** occurrences of `v` (`v * count[v]`).

### Key Takeaway
Transforming input data into a frequency/value domain converts an unfamiliar problem into a classic DP template.

---

## Problem 2: Maximum Alternating Subsequence Sum

* **Interview Difficulty:** Medium
* **Parent Pattern:** 1D Decision DP — Multi-State / Parity State Machine
* **Problem Type:** Subsequence Optimization / State Machine DP
* **Data Structure Used:** Two Rolling State Variables (`even`, `odd`)
* **Brute Force:** Generate all $2^N$ subsequences. For each subsequence, evaluate its alternating sum ($x_0 - x_1 + x_2 - x_3 \dots$). Return max sum. $O(2^N \cdot N)$ time, $O(N)$ space.

### DP State
We maintain **two state variables** at index `i`:
* `even`: Max alternating sum ending with an addition (`+`), ready to subtract next.
* `odd`: Max alternating sum ending with a subtraction (`-`), ready to add next.

### State Flow

```text
At element num:
                 ┌──────────────────────────────────────────────┐
                 │                State Machine                 │
                 └──────────────────────┬───────────────────────┘
                                        │
             ┌──────────────────────────┴──────────────────────────┐
             ▼                                                     ▼
   EVEN State (Next op is +)                             ODD State (Next op is -)
   ─────────────────────────                             ────────────────────────
   Option 1: Skip num → keep even                        Option 1: Skip num → keep odd
   Option 2: Add num to odd state                        Option 2: Subtract num from even
             → odd + num                                           → even - num
   ─────────────────────────                             ────────────────────────
   next_even = max(even, odd + num)                      next_odd = max(odd, even - num)
```

### Recurrence
$$\text{next\_even} = \max(\text{even}, \; \text{odd} + \text{num})$$
$$\text{next\_odd} = \max(\text{odd}, \; \text{even} - \text{num})$$

**Derivation:**
To form a subsequence ending with addition (`even`), we either skip `num` (`even`) or append `num` as an addition to a previous odd-ending sequence (`odd + num`). To form a subsequence ending with subtraction (`odd`), we either skip `num` (`odd`) or append `num` as a subtraction to an even-ending sequence (`even - num`).

### Base Cases
* `even = 0`, `odd = 0` (No elements taken yet).

### Traversal Order
**Left to Right (Index 0 $\rightarrow$ N-1):**
Process numbers sequentially as state transitions at index `i` depend on index `i-1`.

### Pointer Flow

Input: `nums = [4, 2, 5, 3]`

| `num` | `even` (ending with `+`) | `odd` (ending with `-`) | Sequence Represented |
| :---: | :---: | :---: | :--- |
| **Start** | 0 | 0 | Empty |
| **4** | $\max(0, 0+4) = \mathbf{4}$ | $\max(0, 0-4) = \mathbf{0}$ | `[4]` |
| **2** | $\max(4, 0+2) = \mathbf{4}$ | $\max(0, 4-2) = \mathbf{2}$ | `[4, 2]` |
| **5** | $\max(4, 2+5) = \mathbf{7}$ | $\max(2, 4-5) = \mathbf{2}$ | `[4, 2, 5]` |
| **3** | $\max(7, 2+3) = \mathbf{7}$ | $\max(2, 7-3) = \mathbf{4}$ | `[4, 2, 5, 3]` |

**Final Answer:** `even = 7` (Subsequence `[4, 2, 5]` $\rightarrow 4 - 2 + 5 = 7$)

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N)  (Single pass through array)  │
│  Space Complexity │ O(1)  (Two scalar state variables) │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Operations alternate (+ and -) across subsequence elements
* ✓ State transitions swap based on parity/mode
* ✓ Optimization problem (maximize sum)
* $\rightarrow$ **Multi-State Parity State Machine DP**

### Core Insight
Instead of tracking subsequence indices or lengths, maintain two running state accumulators: one representing max sum ending in `+`, and one ending in `-`. Each element `num` offers a choice between staying in the current state or switching states.

### Common Pitfalls
* Returning `odd` instead of `even`. An optimal alternating sum should always end on an addition (`+`) to avoid subtracting an unnecessary value.

### Key Takeaway
State Machine DP turns alternating/parity constraints into clean $O(1)$ space transitions by representing each operational mode as a separate state variable.

---

## Problem 3: Solving Questions With Brainpower

* **Interview Difficulty:** Medium
* **Parent Pattern:** 1D Decision DP — Right-to-Left / Variable Jump DP
* **Problem Type:** Decision DP / Skip-Jump Optimization
* **Data Structure Used:** 1D DP Array (`list[int]`) of size $N+1$
* **Brute Force:** Recursive DFS branching into Solve `i` (jump to `i + brainpower[i] + 1`) vs Skip `i` (move to `i + 1`). $O(2^N)$ time, $O(N)$ recursion stack.

### DP State
`dp[i]` represents the **maximum points achievable considering questions from index i to N-1**.

### State Flow

```text
STATE: dp[i] = max points achievable from index i to end of array

↓

CHOICES at question i:
  Choice 1: SKIP Question i   → dp[i + 1]
  Choice 2: SOLVE Question i  → points[i] + dp[i + brainpower[i] + 1]

↓

TRANSITION: dp[i] = max(dp[i + 1], points[i] + dp[i + brainpower[i] + 1])
```

### Recurrence
$$\text{dp}[i] = \max\Big(\text{dp}[i + 1], \; \text{points}[i] + \text{dp}[\min(N, \; i + \text{brainpower}[i] + 1)]\Big)$$

**Derivation:**
When standing at question `i`, solving it forces a jump to `next_q = i + brainpower[i] + 1`. The value of `dp[i]` depends on `dp[next_q]`, which is **ahead** in the array (`next_q > i`).

> **Golden Rule:** **Traversal order is determined by dependency.** Since current states depend on future states (`next_q > i`), we MUST process the array Right-to-Left (backwards).

### Base Cases
* `dp[N] = 0` (Out of bounds past last question yields 0 points).

### Traversal Order
**Right to Left (Index N-1 $\rightarrow$ 0):**
Iterating `i` from `N-1` down to `0` guarantees `dp[i+1]` and `dp[next_q]` are finalized before computing `dp[i]`.

### Pointer Flow

Input: `questions = [[3, 2], [4, 3], [4, 4], [2, 5]]` ($N = 4$)

| Index ($i$) | `points[i]` | `brainpower[i]` | `next_q` | `solve` choice | `skip` choice | `dp[i]` |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **4** | — | — | — | — | — | **0** (Base) |
| **3** | 2 | 5 | 9 ($\ge 4$) | $2 + 0 = 2$ | `dp[4]` = 0 | **2** |
| **2** | 4 | 4 | 7 ($\ge 4$) | $4 + 0 = 4$ | `dp[3]` = 2 | **4** |
| **1** | 4 | 3 | 5 ($\ge 4$) | $4 + 0 = 4$ | `dp[2]` = 4 | **4** |
| **0** | 3 | 2 | 3 ($< 4$) | $3 + \text{dp}[3] = 5$ | `dp[1]` = 4 | **5** |

**Final Answer:** `dp[0] = 5` (Solve q0 [3 pts] + jump to q3 [2 pts] = 5 pts)

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N)  (Single backwards pass)      │
│  Space Complexity │ O(N)  (DP table for variable jumps)│
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Decision skips variable distance (`i + jump`)
* ✓ Future state required to compute current state
* ✓ Optimization problem (maximize points)
* $\rightarrow$ **Right-to-Left Variable Jump DP**

### Core Insight
**Traversal order is determined by dependency.** When choices jump forward into the future, iterating backwards converts forward dependencies into pre-computed lookups.

### Common Pitfalls
* Attempting a forward (left-to-right) DP loop without realizing `dp[i]` depends on uncomputed future cells.
* Array index out-of-bounds errors when `i + brainpower[i] + 1 >= N`. A padded array of size $N+1$ handles jumps past the array end cleanly.

### Key Takeaway
If state transitions look forward (`i -> i + k`), process the DP table backwards (`N-1 -> 0`).

---

## Problem 4: Jump Game

* **Interview Difficulty:** Medium
* **Parent Pattern:** 1D Decision DP — Feasibility DP
* **Problem Type:** Boolean Feasibility DP / Reachability Analysis
* **Data Structure Used:** 1D Boolean DP Array (`list[bool]`) of size $N$
* **Brute Force:** Backtracking DFS exploring all jump lengths from index 0. $O(2^N)$ time, $O(N)$ recursion stack.

> **Interview Note:** **DP exists ($O(N^2)$), but Greedy is preferred ($O(N)$) in interviews.** Still learn DP first because it explains WHY Greedy works.

### DP State
`dp[i]` is a **boolean (`True`/`False`) representing whether index N-1 is reachable from index i**.

### State Flow

```text
STATE: dp[i] = True if last index is reachable from index i, else False

↓

CHOICES at index i: Jump any distance j from 1 to nums[i]

↓

TRANSITION: dp[i] = True if ANY dp[i + j] == True, else False
```

### Recurrence
$$\text{dp}[i] = \bigvee_{j=1}^{\text{nums}[i]} \text{dp}[i + j]$$

**Derivation:**
From index `i`, we can jump to any `i + j` where $1 \le j \le \text{nums}[i]$. If *at least one* reachable target index `i + j` can reach the end (`dp[i + j] == True`), then index `i` is also capable of reaching the end.

### Base Cases
* `dp[N-1] = True` (Last index is trivially reachable from itself).

### Traversal Order
**Right to Left (Index N-2 $\rightarrow$ 0):**
Since `dp[i]` queries future indices `i + j > i`, process in reverse order.

### Pointer Flow

Input: `nums = [2, 3, 1, 1, 4]` ($N = 5$)

| Index ($i$) | `nums[i]` | Reachable Range | Valid Path Found? | `dp[i]` |
| :---: | :---: | :---: | :---: | :---: |
| **4** | 4 | Base Target | — | **True** |
| **3** | 1 | `[4]` | `dp[4]` is True | **True** |
| **2** | 1 | `[3]` | `dp[3]` is True | **True** |
| **1** | 3 | `[2, 3, 4]` | `dp[2]` is True | **True** |
| **0** | 2 | `[1, 2]` | `dp[1]` is True | **True** |

**Final Answer:** `dp[0] = True`

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^2) DP  |  O(N) Greedy          │
│  Space Complexity │ O(N) DP    |  O(1) Greedy          │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Boolean question: *"Is it possible to reach X?"*
* ✓ Range of choices at each index
* ✓ Feasibility problem
* $\rightarrow$ **Boolean Feasibility DP**

### Core Insight
DP provides the fundamental reachability model. Once you see that you only care about the *earliest reachable index*, you can collapse the $O(N^2)$ DP loop into an $O(N)$ Greedy target-tracking algorithm (`goal = i if i + nums[i] >= goal`). Learning DP first explains why Greedy works.

### Common Pitfalls
* Inner loop scanning past index `N-1`. Clamping jump boundary with `min(i + nums[i], N - 1)` prevents out-of-bounds.
* Not breaking early upon finding the first `True` neighbor.

### Key Takeaway
DP builds the mental foundation for reachability. Greedy optimizations are discovered by simplifying DP state lookups.

---

## Pattern Summary

| Family Badge | Problem | State `dp[i]` | Transition (Recurrence) | Optimization |
| :---: | :--- | :--- | :--- | :--- |
| `[House Robber Family]` | **Delete and Earn** | Max points up to value `v` | `max(dp[v-1], points[v] + dp[v-2])` | 2 Rolling Vars $\rightarrow O(1)$ space |
| `[State Machine]` | **Max Alternating Subseq** | `even`: sum (+), `odd`: sum (-) | `even = max(even, odd + num)`<br>`odd = max(odd, even - num)` | 2 State Vars $\rightarrow O(1)$ space |
| `[Variable Jump]` | **Brainpower Questions** | Max points from index `i` to $N-1$ | `max(dp[i+1], pts[i] + dp[i + skip + 1])` | Right-to-Left Pass $\rightarrow O(N)$ space |
| `[Feasibility DP]` | **Jump Game** | Boolean: can reach end from index `i` | `OR_{j=1}^{nums[i]} (dp[i + j])` | Right-to-Left Pass $\rightarrow O(N)$ DP / $O(1)$ Greedy |

---

## Master Patterns Learned

#### 1. Preprocessed Value-Domain DP `[House Robber Family]`
* **Recognition:**
  ✓ Operations apply to element values
  ✓ Choosing value $v$ eliminates adjacent values $v-1$ and $v+1$
  ✓ Optimization problem
  $\rightarrow$ **Value-Domain Include/Exclude DP**
* **State:** `dp[v]` = Max score considering values from $0$ up to $v$.
* **Transition:** `dp[v] = max(dp[v-1], points[v] + dp[v-2])`
* **Traversal Order:** Left to Right (Value $0 \rightarrow \max(nums)$).
* **Optimization:** 2 rolling variables (`prev2`, `prev1`) for $O(1)$ space.
* **Examples:** Delete and Earn, House Robber, Earn and Delete variants.

```python
def value_domain_dp(nums: list[int]) -> int:
    if not nums:
        return 0
    max_val = max(nums)
    points = [0] * (max_val + 1)
    for num in nums:
        points[num] += num
        
    prev2, prev1 = 0, 0
    for p in points:
        curr = max(prev1, prev2 + p)
        prev2, prev1 = prev1, curr
    return prev1
```

---

#### 2. Multi-State Parity DP `[State Machine]`
* **Recognition:**
  ✓ Operations alternate (+ and -) or swap states on each choice
  ✓ Finite set of operational modes
  ✓ Optimization problem
  $\rightarrow$ **State Machine Parity DP**
* **State:** `even` (max value after addition), `odd` (max value after subtraction).
* **Transition:**
  * `next_even = max(even, odd + num)`
  * `next_odd = max(odd, even - num)`
* **Traversal Order:** Left to Right (Index $0 \rightarrow N-1$).
* **Optimization:** 2 scalar state variables for $O(1)$ space.
* **Examples:** Max Alternating Subsequence Sum, Best Time to Buy/Sell Stock with State Machine.

```python
def parity_state_dp(nums: list[int]) -> int:
    even, odd = 0, 0
    for num in nums:
        even, odd = max(even, odd + num), max(odd, even - num)
    return even
```

---

#### 3. Right-to-Left Variable Jump DP `[Variable Jump]`
* **Recognition:**
  ✓ Decision skips variable distance (`i + jump`)
  ✓ Future state required to compute current state
  ✓ Optimization problem
  $\rightarrow$ **Right-to-Left Variable Jump DP**
* **State:** `dp[i]` = Maximum total reward from index $i$ to end of array.
* **Transition:** `dp[i] = max(dp[i+1], val[i] + dp[i + jump[i] + 1])`
* **Traversal Order:** Right to Left (Index $N-1 \rightarrow 0$).
* **Optimization:** Requires full $O(N)$ DP table due to variable jump distances.
* **Examples:** Solving Questions With Brainpower, Jump Game, Job Scheduling with Variable Skips.

```python
def variable_jump_dp(questions: list[list[int]]) -> int:
    n = len(questions)
    dp = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        pts, skip = questions[i]
        next_q = i + skip + 1
        solve = pts + (dp[next_q] if next_q < n else 0)
        dp[i] = max(dp[i + 1], solve)
    return dp[0]
```

---

## How to Recognize Decision DP in the Wild

When given a brand-new problem in an interview, run through this 5-point checklist:

```text
□ Is this an optimization or feasibility problem? (Max, Min, Can reach?)
□ Can I make a choice at each step to either TAKE or SKIP an element?
□ Does taking an element constrain or dictate future choices?
□ Would a naive recursive decision tree re-solve identical states?
□ Can I state "dp[i] represents ______" in one complete sentence?
```

If you answered **YES** to these questions $\rightarrow$ **Think Decision DP!**
