# 1D Longest DP & Sequence Extensions

## 1. The Anatomy of Longest DP

While standard Decision DP focuses on boolean optimization (maximizing profit, minimizing cost, or evaluating feasibility via a binary "Take vs. Skip" mechanic), **Longest DP** addresses structural sequence validity. It asks us to find the maximum *length*, *size*, or *depth* of a valid chain embedded within a larger dataset.

This introduces a fundamental shift in how state transitions are evaluated. Instead of looking backward at a fixed, predetermined jump (e.g., `dp[i-1]` or `dp[i-2]`), the algorithm must look backward across **every single previously processed state** and ask a structural validation question: *"Can we mathematically or logically connect the current element to this previous sequence?"*

### The Core Algorithmic Difference

| Algorithmic Vector | Decision DP (Take vs. Skip) | Longest DP (Sequence Extension) |
| :--- | :--- | :--- |
| **Primary Question** | "Do we include this element or skip it?" | "Which previous element can we legally attach to?" |
| **Dependency Horizon** | Fixed and shallow (usually $O(1)$ lookbacks) | Exhaustive and deep (requires scanning all $j < i$) |
| **State Output** | Scalar accumulation (Total sum, boolean) | Sequence metric (Length, count, or subset size) |
| **Time Complexity** | Typically $O(N)$ due to fixed transitions | Typically $O(N^2)$ due to exhaustive $j < i$ sweeps |

---

## 2. State Architecture & Design

In Longest DP, the definition of the state is universally rigid. It serves as the foundational anchor for all future sequence extensions.

> **The Golden State Definition:**
> `dp[i]` represents the length of the longest valid structure (subsequence, chain, or subset) **strictly ending at index `i`**.

### Why "Strictly Ending at `i`"?
If we loosely define `dp[i]` as "the longest subsequence found anywhere within the prefix up to `i`" (acting as a running maximum), we lose the sequence's terminal anchor. To evaluate whether element `i+1` can legally extend a sequence, we absolutely *must* know the exact value of the sequence's final element. By forcing `dp[i]` to mandate that `nums[i]` is the absolute final element of the chain, we guarantee that future transitions have a valid, known endpoint to compare against.

---

## 3. Why Greedy Algorithms Fail Here

Greedy algorithms attempt to construct the longest sequence by immediately snapping to the next "best-looking" available element. This localized tunnel vision fundamentally fails because choosing an element that appears optimal now can inadvertently lock us out of a significantly longer, more optimal sequence downstream.

### Structural Counter-Example: Longest Increasing Subsequence (LIS)

Consider the input array: `nums = [10, 9, 2, 5, 3, 7, 101, 18]`

```text
Greedy Traversal (Picking the immediate next larger element):
  1. Start at 10. The next available larger element is 101.
  2. Resulting Sequence: [10, 101] -> Length = 2.
  
  Alternative Greedy (Start at minimum value 2):
  1. Start at 2. Pick next larger 5. Pick next larger 7. Pick next larger 101.
  2. Resulting Sequence: [2, 5, 7, 101] -> Length = 4.
  3. But wait! What if the array was [2, 5, 3, 4, 6]? 
     Greedy picking 5 blocks the sequence [3, 4, 6]. 
     The greedy algorithm possesses no mechanism to "skip" 5 in favor of 3.
```

### The DP Resolution
Dynamic Programming refuses to guess. It computes the absolute best valid chain ending at *every single index* mathematically, and then extends those chains whenever the problem's specific validation constraints are met, completely neutralizing the greedy trap.

---

## 4. The Transition Engine

This represents the largest conceptual leap in 1D DP. Instead of executing a simple `max(take, skip)` comparison, the transition executes a historical loop over the entire processed prefix array.

```text
At index i:
  For every previous index j (where 0 <= j < i):
    Does nums[i] mathematically connect to nums[j]?
      YES ↓
         candidate_length = dp[j] + 1
         dp[i] = max(dp[i], candidate_length)
      NO  ↓
         Ignore and evaluate the next j
```

### The Universal Longest DP Template

```python
for i in range(n):
    dp[i] = 1                 # Base State: An isolated element is a sequence of length 1
    for j in range(i):        # Exhaustive historical sweep of all previous elements
        if can_extend(j, i):  # The problem-specific connection rule (e.g., nums[j] < nums[i])
            dp[i] = max(dp[i], dp[j] + 1)
```

Memorizing this nested double-loop architecture is the key to unlocking dozens of medium and hard sequence optimization problems.

---

## 5. Parent Pointer Reconstruction

Many technical requirements extend beyond just identifying the maximum length; they demand the extraction of the actual sequence elements. To fulfill this, we introduce a secondary tracking structure called the `parent` array.

The `parent[i]` array operates as a linked list in reverse. Whenever `dp[i]` is successfully extended by a previous optimal state `dp[j]`, we log `j` as the parent of `i`.

### Reconstruction Execution Trace
Suppose we have evaluated an array to find its Largest Divisible Subset: `nums = [1, 3, 6, 24]`.

```text
Index Mapping:  0   1   2   3
nums payload:   1   3   6  24
dp lengths  :   1   2   3   4
parent logs :  -1   0   1   2
```

**Backtracking the Solution Space:**
1. Scan `dp` to locate the absolute maximum length. (Found `4` at index `3`). Initialize `curr_node = 3`.
2. Append `nums[3]` (`24`) to the output buffer. `curr_node = parent[3]` (`2`).
3. Append `nums[2]` (`6`) to the output buffer. `curr_node = parent[2]` (`1`).
4. Append `nums[1]` (`3`) to the output buffer. `curr_node = parent[1]` (`0`).
5. Append `nums[0]` (`1`) to the output buffer. `curr_node = parent[0]` (`-1`). Loop terminates.
6. Reverse the output buffer to restore chronological order: `[1, 3, 6, 24]`.

This exact backtracking payload extraction technique applies identically across LIS, Divisible Subsets, String Chains, and DAG pathfinding.

---

## 6. The Universal DP Checklist

Before writing execution logic, map the problem constraints against this 6-box matrix:

```text
┌─────────────────────────────────────────────────────────────────┐
│  BOX 1 — STATE                                                  │
│  Define dp[i] in one complete, unambiguous English sentence.    │
├─────────────────────────────────────────────────────────────────┤
│  BOX 2 — TRANSITION (State → Choices → Recurrence)             │
│  Define the connection validation rules and the max/min formula.│
├─────────────────────────────────────────────────────────────────┤
│  BOX 3 — BASE CASES                                             │
│  Establish the absolute baseline metric (usually 1 for LIS).    │
├─────────────────────────────────────────────────────────────────┤
│  BOX 4 — TRAVERSAL ORDER                                        │
│  Establish the loop execution direction (Left→Right standard).  │
├─────────────────────────────────────────────────────────────────┤
│  BOX 5 — ANSWER LOCATION                                        │
│  Determine if the answer is max(dp) or dp[N-1].                 │
├─────────────────────────────────────────────────────────────────┤
│  BOX 6 — OPTIMIZATION                                           │
│  Analyze if binary search (Patience Sorting) can reduce O(N^2). │
└─────────────────────────────────────────────────────────────────┘
```

---

## Problem: Longest Increasing Subsequence (300)

* **Interview Difficulty:** Medium (DP) / Hard (Binary Search)
* **Parent Pattern:** 1D Longest DP — The Root Archetype
* **Problem Type:** Subsequence Optimization
* **Data Structure Used:** 1D DP Array (`list[int]`)
* **Brute Force:** Generate all $2^N$ subsequences recursively, validate if each sequence is strictly increasing, and record the maximum length. Time Complexity: $O(2^N \cdot N)$, rendering it fundamentally unusable for arrays larger than 20 elements.
* **Optimized Approach (DP):** Deploy the Universal Longest DP template. Initialize a `dp` array where every cell is `1`. For every element `i`, iterate a secondary pointer `j` from `0` to `i-1`. If `nums[j] < nums[i]`, validate the extension: `dp[i] = max(dp[i], dp[j] + 1)`. Extract `max(dp)` at the end.

### DP State
`dp[i]` represents the **length of the longest strictly increasing subsequence strictly ending exactly at index i**.

### State Flow
```text
STATE: dp[i] = length of LIS ending at nums[i]

↓

CHOICES at index i:
  Look back at ALL previous elements j (0 <= j < i).
  If nums[j] < nums[i]:
    We can extend the chain ending at j!
    Candidate length = dp[j] + 1
  Else:
    Cannot extend. Ignore j.

↓

TRANSITION: dp[i] = max(dp[i], dp[j] + 1) for all valid j.
```

### Recurrence
$$\text{dp}[i] = \max_{0 \le j < i, \; \text{nums}[j] < \text{nums}[i]} \Big( \text{dp}[j] + 1 \Big)$$

### Base Cases
* `dp[i] = 1` for all `i`. (Every isolated element constitutes an increasing subsequence of length 1 by itself).

### Traversal Order
**Left to Right (Outer Loop `i` from 0 to N-1, Inner Loop `j` from 0 to `i-1`):**
Because extending a chain at `i` requires definitively knowing the optimal chain lengths for all $j < i$.

### Pointer Flow
```text
Evaluating LIS for nums = [10, 9, 2, 5, 3, 7]:
Base Initialization: dp = [1, 1, 1, 1, 1, 1]

i=0 (10): No history. dp[0] = 1.
i=1 (9):  nums[0] (10) > 9. Cannot connect. dp[1] = 1.
i=2 (2):  nums[0], nums[1] > 2. Cannot connect. dp[2] = 1.
i=3 (5):  nums[2] (2) < 5. Extension valid! dp[3] = dp[2] + 1 = 2.
i=4 (3):  nums[2] (2) < 3. Extension valid! dp[4] = dp[2] + 1 = 2.
i=5 (7):  nums[2] (2) < 7 -> dp[5]=2
          nums[3] (5) < 7 -> dp[5]=3  (overwrites 2)
          nums[4] (3) < 7 -> dp[5]=3  (ties with 3)
          Final dp[5] = 3.

Target Result: max(dp) = 3 (Sequence: [2, 5, 7] or [2, 3, 7])
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^2) DP  |  O(N log N) BS        │
│  Space Complexity │ O(N)       |  O(N)                 │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ The requirement asks for a "longest" or "maximum size" sequence.
* ✓ Elements do not need to be physically contiguous (subsequence rules).
* ✓ A specific mathematical rule dictates whether element B can follow element A.
* $\rightarrow$ **1D Longest DP Pattern**

### Core Insight
The state definition must strictly anchor the subsequence to ending exactly at `i`. If `dp[i]` acts as a generalized running maximum of the prefix, we lose the terminal integer value, making it mathematically impossible to evaluate the `nums[j] < nums[i]` extension condition for future elements.

### Mistakes Made
* We attempted to return `dp[-1]` as the final answer. The longest increasing subsequence does not guaranteeably end on the final array element. The correct answer resides at `max(dp)`.
* Initializing the `dp` array with `0`s. An isolated integer constitutes a valid increasing subsequence of length 1, so the absolute baseline floor for every index is `1`.

### What I Learned
The $O(N^2)$ nested loop architecture is the beating heart of all connection-based DP problems. For the highly optimized $O(N \log N)$ solution variant, we must switch paradigms away from DP entirely and utilize "Patience Sorting" (Binary Search via `bisect_left` on an active tracking tails array).

---

## Problem: Number of Longest Increasing Subsequences (673)

* **Interview Difficulty:** Medium
* **Parent Pattern:** 1D Longest DP — Combinatorial State Tracking
* **Problem Type:** Sequence Combinatorics
* **Data Structure Used:** Dual 1D Arrays (`length` array and `count` array)
* **Brute Force:** Finding all LIS paths via pure recursion scaling up to $O(2^N)$ time complexity.
* **Optimized Approach:** Expanding the standard LIS architecture to track two parallel states simultaneously. `length[i]` stores the max length ending at `i`, while `count[i]` tracks the number of distinct valid paths that yield that exact length. When iterating `j` before `i`, if `length[j] + 1 > length[i]`, a strictly longer path is discovered: update the length and completely inherit the `count` from `j`. If `length[j] + 1 == length[i]`, an equally optimal alternative path is found: add `count[j]` to `count[i]`.

### DP State
* `length[i]`: Length of the strictly increasing subsequence ending exactly at index `i`.
* `count[i]`: Number of distinct LIS paths that end exactly at index `i` (possessing length `length[i]`).

### State Flow
```text
At index i, checking valid previous index j (nums[j] < nums[i]):

  Condition A: length[j] + 1 > length[i]
    → We found a strictly longer sequence!
    → length[i] = length[j] + 1
    → count[i] = count[j]  (Inherit the path count of this new best)

  Condition B: length[j] + 1 == length[i]
    → We found another way to make the CURRENT best length!
    → count[i] += count[j]  (Add these paths to our total)
```

### Recurrence
$$\text{length}[i] = \max_{j} (\text{length}[j] + 1)$$
$$\text{count}[i] = \sum_{j} \text{count}[j] \quad \text{where} \quad \text{length}[j] + 1 == \text{length}[i]$$

### Base Cases
* `length[i] = 1` for all `i`.
* `count[i] = 1` for all `i`. (Every single element has exactly 1 way to form a sequence of length 1).

### Traversal Order
**Left to Right (Outer Loop `i` from 0 to N-1, Inner Loop `j` from 0 to `i-1`).**

### Pointer Flow
```text
Evaluating Path Counts for nums = [1, 3, 5, 4, 7]:
Base: length = [1,1,1,1,1], count = [1,1,1,1,1]

i=1 (3): Extends from 1 -> length[1]=2, count[1]=1
i=2 (5): Extends from 3 -> length[2]=3, count[2]=1
i=3 (4): Extends from 3 -> length[3]=3, count[3]=1
i=4 (7): 
  - Extends from 5 (length 3): length[4] = 4, count[4] = count[2] = 1
  - Extends from 4 (length 3): 3+1 == length[4]. Tie detected! 
    -> count[4] += count[3] -> count[4] = 2.

Global Max Length = 4. 
Summing all count[i] where length[i] == 4 yields Total = 2.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^2) (Standard historical sweep) │
│  Space Complexity │ O(N) (Dual tracking arrays)        │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ The problem asks for the "number of ways" or "total count".
* ✓ It applies to an optimal geometric structure (like LIS).
* $\rightarrow$ **Combinatorial State Tracking DP**

### Core Insight
Combinatorial sequence tracking mandates bifurcating the state. We cannot optimize a metric and count the paths leading to it within the same variable space. Overwriting occurs when a new absolute maximum is discovered; accumulation (summing) occurs when an identical parallel maximum is found.

### Mistakes Made
* We initially assumed the final answer would simply be `count[-1]`. We must identify the global maximum length across the entire `length` array first, and then sum the `count[i]` values for all indices that share that exact global maximum length.

### What I Learned
When mixing optimization DP with combinatorial counting, we must maintain two completely decoupled arrays and merge their transition conditions based strictly on strict superiority (`>`) vs equality (`==`).

---

## Problem: Largest Divisible Subset (368)

* **Interview Difficulty:** Medium
* **Parent Pattern:** 1D Longest DP — Parent Reconstruction
* **Problem Type:** Subset Optimization / Transitive Sorting
* **Data Structure Used:** 1D DP Array (`dp`) + Backtracking Ledger (`parent`)
* **Brute Force:** Checking all possible subsets $O(2^N)$ for complete internal divisibility.
* **Optimized Approach:** Sort the array ascending immediately. Sorting activates the mathematical property of transitivity: if $A < B < C$, and $C \% B == 0$ and $B \% A == 0$, then $C \% A == 0$ is guaranteed. Initialize a `dp` array for lengths and a `parent` array filled with `-1`. Run standard LIS evaluating `nums[i] % nums[j] == 0`. When a valid extension maximizes the length, record $j$ into `parent[i]`. Finally, locate the index of the max length and walk backward through the `parent` ledger to compile the elements.

### DP State
`dp[i]` represents the **length of the largest divisible subset where the largest element is exactly `nums[i]`**.

### State Flow
```text
STATE: dp[i] = length of subset ending with nums[i]

↓

PRE-REQUISITE: Sort `nums` ascending!
Why? If nums is sorted, and nums[i] % nums[j] == 0, then by transitivity,
nums[i] is divisible by ALL elements in the subset ending at nums[j].

↓

CHOICES at index i:
  For every j < i:
    If nums[i] % nums[j] == 0:
      If dp[j] + 1 > dp[i]:
        dp[i] = dp[j] + 1
        parent[i] = j   <-- Record who gave us this optimal length!
```

### Recurrence
$$\text{dp}[i] = \max_{0 \le j < i, \; \text{nums}[i] \% \text{nums}[j] == 0} \Big( \text{dp}[j] + 1 \Big)$$

### Base Cases
* `dp[i] = 1` for all `i`.
* `parent[i] = -1` for all `i` (indicates no parent exists yet).

### Traversal Order
**Left to Right (Outer Loop `i` from 0 to N-1, Inner Loop `j` from 0 to `i-1`).**

### Pointer Flow
```text
Evaluating Largest Divisible Subset for nums = [1, 2, 4, 8] (Pre-sorted):
Base Initialization: dp = [1, 1, 1, 1], parent = [-1, -1, -1, -1]

i=1 (2): 2%1 == 0 -> dp[1]=2, parent[1]=0
i=2 (4): 4%2 == 0 -> dp[2]=3, parent[2]=1
i=3 (8): 8%4 == 0 -> dp[3]=4, parent[3]=2

Reconstruction starting at max_idx = 3:
  Append nums[3] (8) -> Jump to parent[3] (2)
  Append nums[2] (4) -> Jump to parent[2] (1)
  Append nums[1] (2) -> Jump to parent[1] (0)
  Append nums[0] (1) -> Jump to parent[0] (-1) -> Halt.
Result: [8, 4, 2, 1] reversed to [1, 2, 4, 8].
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^2) (DP loop) + O(N log N) Sort │
│  Space Complexity │ O(N) (dp and parent tracking arrays│
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ The prompt requests returning the *exact constituent elements* of the optimal sequence, rather than just its scalar integer length.
* ✓ Subset conditions evaluate relative mathematical properties (divisibility).
* $\rightarrow$ **Longest DP with Parent Reconstruction**

### Core Insight
Divisibility requires a specific hierarchical order to function transitively. By sorting the array ascending prior to running the DP logic, we transform a chaotic subset problem into a strictly directional sequence extension problem, identical in architecture to standard LIS.

### Mistakes Made
* We initially forgot to sort the `nums` array. The transitivity rule (`a|b` and `b|c` $\rightarrow$ `a|c`) only functions correctly if the elements are evaluated in strictly ascending magnitude order.

### What I Learned
The `parent` array operates as a foundational backward-chaining linked list. This technique is universally applicable to any DP algorithm requiring path payload extraction, including string alignments and graph traversal tracking.

---

## Problem: Russian Doll Envelopes (354)

* **Interview Difficulty:** Hard
* **Parent Pattern:** 1D Longest DP — 2D Constraint Reduction
* **Problem Type:** 2D Box Nesting / Sorting Reduction
* **Data Structure Used:** Sorting Engine + $O(N \log N)$ Binary Search LIS
* **Brute Force:** Formulating an $O(N^2)$ LIS comparing both width and height yields Time Limit Exceeded (TLE) on large test suites.
* **Optimized Approach:** The problem requires strict increasing dimensions across both width and height ($W_1 < W_2$ AND $H_1 < H_2$). The architectural trick is dimensional reduction: sort the envelopes by Width ascending. If widths are tied, sort Height descending. Extract the heights into a flat 1D array. Run a highly optimized $O(N \log N)$ Binary Search LIS exclusively on the heights array.

### DP State (Conceptual)
`dp[i]` represents the **maximum number of envelopes we can strictly nest ending with exactly envelope `i`**.

### State Flow
```text
The problem asks for strictly increasing dimensions in both width and height.

Step 1: Sort by Width (Ascending)
  Now we only need to find an increasing subsequence of Heights!

Step 2: Conflict Resolution
  If widths are equal (e.g., [6, 4] and [6, 7]), we CANNOT nest them.
  If we sort heights ascending for equal widths, LIS might illegally pick both.
  Solution: Sort heights DESCENDING for equal widths.
  Now, an increasing sequence of heights will never pick two envelopes of the same width.

Step 3: Run O(N log N) LIS purely on the newly extracted Heights array.
```

### Recurrence
(Reduced entirely to the 1D LIS `bisect_left` tails update architecture)

### Base Cases
* Handled natively by the binary search tails array instantiation.

### Traversal Order
**Sorting Phase first, then Left to Right processing on the height extraction.**

### Pointer Flow
```text
Evaluating Russian Doll Envelopes for envelopes = [[5, 4], [6, 4], [6, 7], [2, 3]]:

Step 1 (Sorting Engine Activation):
  Sort Widths Ascending.
  If Widths Tie, Sort Heights DESCENDING.
  Sorted Array: [[2, 3], [5, 4], [6, 7], [6, 4]]

Step 2 (Dimensional Flattening):
  Extract Heights: [3, 4, 7, 4]

Step 3 (1D LIS execution):
  Run optimal LIS on [3, 4, 7, 4].
  The sequence [3, 4, 7] yields length 3.
  (Notice how the descending sort on width 6 forced the 7 before the 4, 
  making it impossible for the LIS to illegally nest [6,4] inside [6,7]).
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N log N) (Sort + Binary Search)  │
│  Space Complexity │ O(N) (Tails array for BS LIS)      │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Confronting 2D geometric constraints (e.g., nesting boxes, stacking blocks).
* ✓ Mandates strict increases across both axes simultaneously.
* $\rightarrow$ **2D Constraint Reduction to 1D LIS**

### Core Insight
Sorting on the primary axis (Width) effectively solves half the problem. The brilliant counter-intuitive maneuver is sorting the secondary axis (Height) *descending* on ties. This guarantees that an increasing subsequence algorithm scanning the heights will never select two envelopes sharing the exact same width, elegantly enforcing the strict nested constraint natively within the sort layout.

### Mistakes Made
* We originally sorted both dimensions in ascending order, which caused the LIS logic to falsely identify envelopes of identical widths as valid nesting candidates. The descending tie-breaker sort is mathematically mandatory.

### What I Learned
Complex multi-dimensional DP problems can frequently be collapsed into single-dimensional LIS sequences through intelligent, conflict-resolving preliminary data sorting techniques.

---

### Master Patterns Learned

#### 1. The Connection-Based Sequence Extender (LIS Framework)
* **Applied to:** Longest Increasing Subsequence, Largest Divisible Subset
* **The Strategy:** Deploy this framework when a problem demands the maximum length of a sequence derived from a specific mathematical validation rule. Force the state definition `dp[i]` to strictly anchor at the endpoint of the sequence. Execute a nested historical iteration, validating connection constraints across all previously processed elements $j < i$, overriding the active state with `dp[j] + 1` whenever the resulting chain proves structurally superior.
* **The Conceptual Mechanics:**
  - **Historical Sweeps:** Unlike local step choices, sequence validation demands a comprehensive review of all previous optimal termination points.
  - **Anchor Forcing:** A state that does not end exactly on the processing index cannot act as a valid foundation for future extension checks.
* **The Layout / Code Pattern:**
```python
def longest_sequence_template(elements: list[int]) -> int:
    sequence_lengths = [1] * len(elements)      # Base case: every element is a valid sequence of length 1
    
    for current_index in range(len(elements)):
        for historical_index in range(current_index):
            # The abstract validation rule (e.g., elements[historical_index] < elements[current_index])
            if custom_validation_rule(elements[historical_index], elements[current_index]):
                sequence_lengths[current_index] = max(
                    sequence_lengths[current_index], 
                    sequence_lengths[historical_index] + 1
                )
                
    return max(sequence_lengths) if sequence_lengths else 0
```

#### 2. Combinatorial Sequence Tracking
* **Applied to:** Number of Longest Increasing Subsequences
* **The Strategy:** Utilize this dual-state architecture when tasked with finding the total volume of paths that yield an optimal configuration. Dedicate one array to track the primary optimization metric (length) and a parallel array to accumulate path frequencies (count). Overwrite the count variable when breaching a new performance ceiling; sum the count variables when tying a known performance ceiling.
* **The Conceptual Mechanics:**
  - **State Bifurcation:** The logic separating path superiority from path equality guarantees that combinatorial branches are logged cleanly without overwriting valid alternative lanes.

#### 3. 2D Constraint Reduction (The Russian Doll Maneuver)
* **Applied to:** Russian Doll Envelopes
* **The Strategy:** Apply this technique to multi-dimensional geometric stacking problems. By commanding the sorting engine to order the primary constraint ascending and the secondary constraint *descending* on ties, we mathematically neutralize conflicts on the primary axis. This cleanly reduces a heavy $O(N^2)$ 2D graph traversal into a blazingly fast $O(N \log N)$ 1D binary search problem.

---

## How to Recognize Longest DP in the Wild

When we evaluate a brand-new problem in a high-pressure interview context, cross-reference the prompt against this structural checklist:

```text
□ Does the core prompt request the "longest", "largest", or "maximum size" of an assembly?
□ Are the data elements permitted to be non-contiguous (e.g., a subsequence or independent subset)?
□ Does a specific internal constraint rule dictate whether element B can legally append to element A?
□ Must we compare the active element against multiple previously logged elements to ensure validity?
□ Can the optimal state be perfectly summarized by the sentence: "The longest sequence strictly ending at index i"?
```

If we answered **YES** to these parameters $\rightarrow$ **Execute Longest DP!**
