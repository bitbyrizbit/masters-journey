# Interval DP & Split Architecture

## 1. What is Interval DP?

Interval DP is a specialized class of Dynamic Programming used to solve problems where the optimal solution for a large sequence (or array) is derived by mathematically combining the optimal solutions of its smaller, contiguous **subarrays (intervals)**.

Instead of processing elements left-to-right (`dp[i]`) or tracking prefixes (`dp[i][j]`), we track **start and end boundaries**. We define an interval from index `i` to index `j`, and we systematically search for the absolute best `split point k` that divides this interval into two optimal, independent sub-intervals.

---

## 2. Interval States & The Gap Method Traversal

Because an interval is defined by two boundaries, the state is always 2D.

> **The Universal Interval State Definition:**
> `dp[i][j]` represents the optimal mathematical answer for the strictly bounded subarray starting at index `i` and ending at index `j`.

### The Gap Method (CRITICAL TRAVERSAL RULE)
In 1D or 2D Grid DP, we usually iterate `i` from `0` to `N`. In Interval DP, this standard Cartesian iteration **fails completely**. 
To solve a large interval (length 5), we absolutely must have already solved all smaller intervals (lengths 2, 3, and 4) that exist inside it. 

Therefore, our outer loop does not iterate over starting indices; **it iterates over the LENGTH of the interval (`L`)**. We solve all intervals of length 2, then length 3, expanding outward until we solve the entire array of length `N`.

---

## 3. The Split Point Engine (`k`)

Once we lock our boundaries at `i` and `j`, we execute a third nested loop to find the optimal split point `k`. 
The split point breaks the parent problem into:
1. The Left Subproblem: `dp[i][k]`
2. The Right Subproblem: `dp[k+1][j]`
3. The Cost to Combine them.

```text
At Interval (i, j):
                [ i . . . . . . . . . . . . j ]
                              │
                    Split Point k Chosen
                              │
                [ i . . k ]       [ k+1 . . j ]
                 Left Cost         Right Cost
                 dp[i][k]          dp[k+1][j]
                              
          Total = Left Cost + Right Cost + Merge Cost
```

---

## Problem: Matrix Chain Multiplication

* **Interview Difficulty:** Hard
* **Parent Pattern:** Parent Interval DP
* **Problem Type:** Cost Minimization
* **Data Structure Used:** 2D DP Array (`list[list[int]]`)
* **Brute Force:** Catalan number of parenthesis combinations. Time: $O(4^N / N^{1.5})$.
* **Optimized Approach:** We define `dp[i][j]` as the min cost to multiply matrices from `i` to `j`. We loop over interval length `L` from 2 to N. Inside, we loop over all possible start points `i`. For each interval, we try every split point `k` between `i` and `j-1`, adding the precomputed cost of the left group, the right group, and the mechanical multiplication cost of joining the two resultant matrices.

### DP State
`dp[i][j]` represents the **absolute minimum operations required to multiply the contiguous chain of matrices from index `i` to index `j`**.

### State Flow
```text
STATE: dp[i][j] = min cost for interval [i, j].

↓

CHOICES for split point `k` (where i <= k < j):
  Split the chain into two independent matrix blocks:
  Left Block: matrices from i to k (Cost = dp[i][k])
  Right Block: matrices from k+1 to j (Cost = dp[k+1][j])
  
  Joining Cost:
  The left block yields a matrix of size: arr[i-1] x arr[k]
  The right block yields a matrix of size: arr[k] x arr[j]
  Cost to multiply them = arr[i-1] * arr[k] * arr[j]

↓

TRANSITION: dp[i][j] = min(dp[i][j], Left Cost + Right Cost + Joining Cost)
```

### Recurrence
$$\text{dp}[i][j] = \min_{i \le k < j} \Big( \text{dp}[i][k] + \text{dp}[k+1][j] + (\text{arr}[i-1] \times \text{arr}[k] \times \text{arr}[j]) \Big)$$

### Base Cases
* `dp[i][i] = 0`. A single matrix requires 0 operations to multiply.

### Traversal Order
**Outer Loop:** Length `L` from `2` to `n`.
**Middle Loop:** Start index `i` from `1` to `n - L + 1`.
**Inner Loop:** Split point `k` from `i` to `j - 1`.

### Pointer Flow
```text
Dimensions array: [40, 20, 30, 10, 30]
Matrices: A1(40x20), A2(20x30), A3(30x10), A4(10x30). (n = 4 matrices)

L = 2 (Length 2 intervals):
  i=1, j=2: dp[1][2] = A1 * A2 = 40*20*30 = 24000
  i=2, j=3: dp[2][3] = A2 * A3 = 20*30*10 = 6000
  i=3, j=4: dp[3][4] = A3 * A4 = 30*10*30 = 9000

L = 3 (Length 3 intervals):
  i=1, j=3: Try k=1: dp[1][1] + dp[2][3] + (40*20*10) = 0 + 6000 + 8000 = 14000
            Try k=2: dp[1][2] + dp[3][3] + (40*30*10) = 24000 + 0 + 12000 = 36000
            dp[1][3] = min(14000, 36000) = 14000
...
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^3) (L, i, and k loops)         │
│  Space Complexity │ O(N^2) (2D tracking array)         │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Problem requires dividing a sequence into hierarchical nested groups (like parentheses).
* ✓ A merge operation between two groups relies on the physical properties of the boundary elements.
* $\rightarrow$ **Interval Split DP**

### Core Insight
Matrix chain groupings perfectly map to a binary tree. The split point `k` acts as the root node joining a left subtree and a right subtree. The recursion bubbles from the leaves (length 1) up to the root (length N).

### Mistakes Made
* We attempted to execute the outer loop over `i` and the inner loop over `j`. This resulted in `dp[1][3]` attempting to query `dp[2][3]` before the `(2,3)` interval had actually been processed. Interval DP *demands* the Length-based Gap Method traversal.

### What I Learned
The Gap Method guarantees that no matter what split point `k` is selected, the left and right sub-intervals are mathematically guaranteed to be strictly shorter than `L`, and therefore are already fully solved and cached in the DP array.

---

## Problem: Burst Balloons (312)

* **Interview Difficulty:** Hard
* **Parent Pattern:** Interval DP (Reverse Action)
* **Problem Type:** Sequential Array Destruction
* **Data Structure Used:** 2D DP Array with `1`s padded on boundaries.
* **Brute Force:** Try bursting every balloon, generating a new smaller array, and recursing. Time: $O(N!)$.
* **Optimized Approach:** If we define `k` as the *first* balloon to burst, the adjacent neighbors shift and merge, meaning the left subproblem `(i, k)` dynamically alters the adjacent boundaries of the right subproblem `(k, j)`. This destroys the independence principle of DP. 
**The architectural brilliance:** Define `k` as the **LAST** balloon to burst in the interval. If `k` bursts last, all balloons between `i` and `k`, and all balloons between `k` and `j` have *already been burst*. Therefore, `k`'s physical neighbors are mathematically guaranteed to be the immutable outer boundaries `i` and `j`.

### DP State
`dp[i][j]` represents the **maximum coins generated by bursting all balloons STRICTLY BETWEEN index `i` and index `j` (exclusive)**.

### State Flow
```text
STATE: dp[i][j] = max coins from bursting everything inside (i, j).

↓

CHOICES for balloon `k` (the LAST balloon to burst inside this interval):
  Because k is the last survivor inside (i, j):
  Its left neighbor is `i`. Its right neighbor is `j`.
  Coins from bursting k = A[i] * A[k] * A[j]
  
  Add the max coins previously earned from completely clearing the left gap (i, k)
  Add the max coins previously earned from completely clearing the right gap (k, j)

↓

TRANSITION: dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + (A[i] * A[k] * A[j]))
```

### Recurrence
$$\text{dp}[i][j] = \max_{i < k < j} \Big( \text{dp}[i][k] + \text{dp}[k][j] + (\text{A}[i] \times \text{A}[k] \times \text{A}[j]) \Big)$$

### Base Cases
* Pad the input array with `1` on both ends: `A = [1] + nums + [1]`.
* Intervals of length 1 (e.g. `(0, 1)`) contain no balloons strictly between them. `dp[i][i+1] = 0`.

### Traversal Order
**Outer Loop:** Length `L` from `2` to `N` (length of padded array).
**Middle Loop:** Start index `i` from `0` to `N - L`.
**Inner Loop:** Split point `k` from `i + 1` to `j - 1`.

### Pointer Flow
*(Standard Gap Method traversal mirroring Matrix Chain Multiplication, updating `max` instead of `min`).*

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^3)                             │
│  Space Complexity │ O(N^2) (2D tracking array)         │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Elements in an array are being destroyed/removed.
* ✓ The removal of an element physically alters the adjacency of remaining elements.
* $\rightarrow$ **Interval DP (Backwards Time Reversal)**

### Core Insight
Dynamic Programming requires subproblems to be entirely independent. If an action in subproblem A alters the boundaries of subproblem B, DP crashes. By operating time in reverse (calculating the last survivor instead of the first casualty), the boundaries become static and immutable, restoring DP independence.

### Mistakes Made
* We attempted to define `dp[i][j]` as the interval *inclusive* of `i` and `j`. This forced us to track the elements outside the boundary to calculate the multiplication, which broke the state logic. Using an *exclusive* boundary definition solves this constraint elegantly.

### What I Learned
Whenever element deletion alters adjacent structural relationships, running the time sequence backward (identifying the last operation instead of the first) is the ultimate pattern break for Hard-level destruction problems.

---

## Problem: Minimum Cost to Cut a Stick (1547)

* **Interview Difficulty:** Hard
* **Parent Pattern:** Interval Split DP
* **Problem Type:** Physical Fragmentation
* **Data Structure Used:** Sorted 1D Array + 2D DP Array.
* **Brute Force:** Try all permutations of cuts. Time: $O(C!)$ where C is the number of cuts.
* **Optimized Approach:** The physical stick has a length, but our DP state should not map the physical stick length (which could be $10^6$ and cause Memory Limit Exceeded). Instead, we DP over the **indices of the cuts array**. We sort the cuts and append `0` and `N` (the stick endpoints). The cost of executing a cut `k` between boundaries `i` and `j` is the length of the current physical fragment: `cuts[j] - cuts[i]`.

### DP State
`dp[i][j]` represents the **minimum cost to execute all valid cuts lying strictly between index `i` and index `j` of the sorted cuts array**.

### State Flow
```text
STATE: dp[i][j] = min cost to execute cuts inside (i, j).

↓

CHOICES for executing cut `k` FIRST:
  Executing cut k splits the stick into two independent sticks.
  Left stick requires cuts from i to k (Cost: dp[i][k])
  Right stick requires cuts from k to j (Cost: dp[k][j])
  
  The physical cost of this specific cut is the length of the current stick fragment.
  Fragment Length = cuts[j] - cuts[i]

↓

TRANSITION: dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + (cuts[j] - cuts[i]))
```

### Recurrence
$$\text{dp}[i][j] = \min_{i < k < j} \Big( \text{dp}[i][k] + \text{dp}[k][j] + (\text{cuts}[j] - \text{cuts}[i]) \Big)$$

### Base Cases
* `dp[i][i+1] = 0`. An interval spanning adjacent cut indices contains zero cuts inside it, costing 0.

### Traversal Order
**Outer Loop:** Length `L` from `2` to `M` (Length of padded cuts array).
**Middle Loop:** Start index `i` from `0` to `M - L`.
**Inner Loop:** Split point `k` from `i + 1` to `j - 1`.

### Pointer Flow
*(Standard Gap Method traversal, replacing matrix joining logic with linear length calculations).*

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(M^3) (where M is number of cuts) │
│  Space Complexity │ O(M^2) (2D tracking array)         │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Physical continuous line/stick partitioned by discrete coordinates.
* ✓ Cost is proportional to the physical length of the segment being cut.
* $\rightarrow$ **Interval Split DP on Coordinate Indices**

### Core Insight
Do not build DP arrays based on massive physical dimensions if the operational points (cuts) are sparse. Compress the state space by building the DP strictly over the indices of the sparse operations.

### Mistakes Made
* We failed to sort the cuts array before executing the DP. Interval DP boundaries rely entirely on strict chronological/spatial ordering. An unsorted cuts array destroys the geometric logic of left and right sub-sticks.

### What I Learned
Appending the physical absolute boundaries (`0` and `N`) into the operations array standardizes the mathematics, allowing boundary endpoints to be treated identically to standard interior cut points.

---

## Problem: Palindrome Partitioning II (132)

* **Interview Difficulty:** Hard
* **Parent Pattern:** 1D / 2D Hybrid Split DP
* **Problem Type:** Substring Feasibility Optimization
* **Data Structure Used:** 2D Boolean Array (Precomputation) + 1D DP Array (Optimization).
* **Brute Force:** Pure backtracking trying every substring split. Time: $O(2^N)$.
* **Optimized Approach:** While technically an interval splitting problem, this can be heavily optimized down to 1D space. We first build a 2D boolean DP (`is_pal[i][j]`) that instantly answers if `s[i:j+1]` is a palindrome. Then, we execute a 1D DP where `min_cuts[i]` tracks the minimum cuts needed for the prefix ending at `i`. We iterate a split point `j` before `i`. If `s[j+1:i+1]` is a palindrome, we can attach it to the optimal cuts for the prefix ending at `j`.

### DP State
* `is_pal[i][j]`: Boolean indicating if substring `s[i:j+1]` is a palindrome.
* `min_cuts[i]`: Minimum number of partitions required for the prefix `s[0:i+1]`.

### State Flow
```text
STATE: min_cuts[i] = optimal cuts for prefix up to i.

↓

CHOICES for split point `j` (where 0 <= j < i):
  If the right side of the split (s[j+1...i]) is a valid palindrome:
    We can make a single cut at j to separate it.
    Total Cuts = min_cuts[j] (cuts needed for left side) + 1 (the physical cut)

↓

TRANSITION: min_cuts[i] = min(min_cuts[i], min_cuts[j] + 1)
```

### Recurrence
$$\text{min\_cuts}[i] = \min_{0 \le j < i, \; \text{is\_pal}[j+1][i] == \text{True}} (\text{min\_cuts}[j] + 1)$$

### Base Cases
* If `is_pal[0][i]` is True, the entire prefix is a palindrome. `min_cuts[i] = 0`.
* Default worst-case initialization: `min_cuts[i] = i` (Cutting every single character individually).

### Traversal Order
**Step 1 (Precompute):** Standard 2D gap method traversal to build `is_pal`.
**Step 2 (Optimize):** 1D Left-to-Right loop `i`, with inner nested loop `j` checking previous split boundaries.

### Pointer Flow
```text
s = "aab"
Step 1: is_pal matrix built. is_pal[0][1] ('aa') is True. is_pal[2][2] ('b') is True.

Step 2: min_cuts array initialization = [0, 1, 2]
i=0 ('a'): is_pal[0][0] is True -> min_cuts[0] = 0
i=1 ('a'): is_pal[0][1] is True -> min_cuts[1] = 0
i=2 ('b'): 
  Try j=0: is_pal[1][2] ('ab') is False.
  Try j=1: is_pal[2][2] ('b') is True -> min_cuts[2] = min(2, min_cuts[1] + 1) = 0 + 1 = 1.

Final Answer: min_cuts[2] = 1.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^2)                             │
│  Space Complexity │ O(N^2) (Boolean pal cache)         │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Dividing an entire string into discrete valid structural chunks.
* ✓ Minimization of splits/groups.
* $\rightarrow$ **1D / 2D Hybrid Split DP**

### Core Insight
Interval DP ($O(N^3)$) is often overkill when the problem is strictly anchored to the starting index `0`. By decoupling the palindrome validation ($O(N^2)$) from the cut optimization ($O(N^2)$), we reduce a cubic problem into two parallel quadratic loops.

### Mistakes Made
* We attempted to calculate palindrome validity dynamically inside the `j` loop using a `is_palindrome(s)` helper function. This caused a hidden $O(N)$ nested execution, dragging the time complexity back to $O(N^3)$ and causing a Time Limit Exceeded error. Precomputing all palindrome states into a matrix is mathematically required to maintain $O(1)$ lookup speeds inside the main loop.

### What I Learned
When an optimization state relies heavily on complex string/array validation (like palindromes or dictionary checks), isolating the validation logic into a dedicated pre-processing DP matrix is a massively powerful architectural optimization.

---

### Master Patterns Learned

#### 1. The Gap Method Architecture
* **The Strategy:** Deploy whenever computing an interval strictly requires combining the results of smaller internal segments.
* **The Conceptual Mechanics:** Cartesian loops (`0 to N`) fail because they evaluate endpoints chronologically. The Gap Method loop (`L from 2 to N`) evaluates intervals geometrically, ensuring subproblems grow outward perfectly, guaranteeing prerequisite dependencies are solved.

#### 2. Time-Reversed Destruction (The Burst Balloons Paradigm)
* **The Strategy:** Deploy when elements are being removed/merged, causing dynamic shifts in array adjacency.
* **The Conceptual Mechanics:** Forward time tracking fails because boundaries warp unpredictably. By defining the split point `k` as the *last* surviving element, the temporal timeline is reversed. This permanently anchors the outer bounds of the sub-interval, successfully restoring the DP Principle of Independence.

#### 3. State Compression via Operation Indices
* **The Strategy:** Deploy when facing massive physical dimensions (e.g. stick length $10^6$) that host sparse operational coordinates.
* **The Conceptual Mechanics:** Shift the state tracker off the physical geography entirely. Build the DP tracking matrix strictly over the sorted indices of the operational cut array, dynamically calculating physical length metrics only inside the transition equation.
