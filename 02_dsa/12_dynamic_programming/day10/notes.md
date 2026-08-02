# Advanced DP Patterns & Structural Mashups

## 1. Beyond the Standard Grids

The first 9 days established the pure atomic frameworks of Dynamic Programming (1D states, 2D capacity grids, Tree postorder, and Bitmask graphs). However, in high-tier technical interviews (Meta, Google, HFTs), the problems rarely fit neatly into a single box. 

Advanced DP problems are **Structural Mashups**. They require marrying the memoization engine of DP with an entirely different algorithmic branch, such as Binary Search, Graph Theory (DAGs), or Game Theory.

---

## 2. DP + Binary Search (Weighted Interval Scheduling)

Standard DP scans all previous elements (`O(N)` historical lookup) leading to $O(N^2)$ time. But what if the historical states are naturally sorted?
If the data (like job end-times) is strictly increasing, we can replace the $O(N)$ linear historical scan with an **$O(\log N)$ Binary Search**, crushing the total time complexity from $O(N^2)$ down to $O(N \log N)$.

---

## 3. State Machine DP

In standard 1D DP, `dp[i]` holds a scalar value. In **State Machine DP**, an entity is physically transitioning through distinct phases of reality (e.g., "Not Holding Stock", "Holding Stock", "Cooldown"). The DP array bifurcates into multiple parallel arrays (or a 2D matrix), and the transitions map exactly to the edges of a Finite State Machine (FSM).

---

## 4. Game Theory DP (Minimax)

A subset of Interval and Bitmask DP where two perfect-logic agents play against each other. The core mathematical anomaly here is the **Relative Score Matrix**. Instead of maximizing raw points, `dp[i][j]` tracks the *difference* in score between Player A and Player B. A positive final state means Player A forces a mathematical victory.

---

## Problem: Maximum Profit in Job Scheduling (1235)

* **Interview Difficulty:** Hard
* **Parent Pattern:** DP + Binary Search (Weighted Interval Scheduling)
* **Problem Type:** Temporal Optimization
* **Data Structure Used:** 1D DP Array + Sorted Tuples Array.
* **Brute Force:** Try all non-overlapping job combinations. Time: $O(2^N)$.
* **Optimized Approach:** Sort all jobs by their **End Time**. We define `dp[i]` as the max profit taking a subset of the first `i` jobs. When evaluating job `i`, we can either SKIP it (`dp[i-1]`), or TAKE it. If we take it, we cannot just add `dp[i-1]` because job `i-1` might overlap. We must binary search the `end_times` array to find the *most recently completed job* that finishes before the current job starts.

### DP State
`dp[i]` represents the **maximum profit achievable by intelligently scheduling a non-overlapping subset drawn from the first `i` jobs**.

### State Flow
```text
STATE: dp[i] = max profit.

↓

CHOICES for job i (start, end, profit):
  Choice A (Skip):
    Profit = dp[i-1] (Inherit from the job immediately before this one)
    
  Choice B (Take):
    We must find the latest historical job 'idx' that ended <= current start time.
    Use Binary Search (bisect_right) to find this idx in O(log N).
    Profit = current_profit + dp[idx]

↓

TRANSITION: dp[i] = max(Choice A, Choice B)
```

### Recurrence
$$\text{dp}[i] = \max(\text{dp}[i-1], \; \text{profit}[i] + \text{dp}[\text{binary\_search\_idx}])$$

### Base Cases
* `dp[0] = 0` (0 jobs scheduled yields 0 profit).

### Traversal Order
**Left to Right (Iterative 1D).**

### Pointer Flow
```text
Jobs = [(start=1, end=3, $50), (2, 4, $10), (3, 5, $40), (3, 6, $70)] (Sorted by end time)
dp = [0, 0, 0, 0, 0]

Job 1 (1->3, $50): 
  Valid previous job? bisect_right for end <= 1 -> idx 0.
  dp[1] = max(dp[0], 50 + dp[0]) = 50.

Job 2 (2->4, $10):
  Valid previous job? bisect_right for end <= 2 -> idx 0.
  dp[2] = max(dp[1], 10 + dp[0]) = max(50, 10) = 50.

Job 3 (3->5, $40):
  Valid previous job? bisect_right for end <= 3 -> idx 1 (Job 1).
  dp[3] = max(dp[2], 40 + dp[1]) = max(50, 40 + 50) = 90.

Job 4 (3->6, $70):
  Valid prev? bisect_right for end <= 3 -> idx 1 (Job 1).
  dp[4] = max(dp[3], 70 + dp[1]) = max(90, 70 + 50) = 120.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N log N) (Sorting + N binary srch│
│  Space Complexity │ O(N) (1D tracking array)           │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Optimization over time intervals (start, end, weight).
* ✓ $N$ is massive ($10^5$), instantly disqualifying $O(N^2)$ LIS algorithms.
* $\rightarrow$ **Weighted Interval Scheduling (DP + BS)**

### Core Insight
Intervals sorted by end-time create a monotonically increasing timeline. Because the timeline is monotonic, searching for the "closest non-overlapping predecessor" is perfectly suited for binary search, cleanly decoupling the DP transition from an exhaustive $O(N)$ sweep.

### Mistakes Made
* We attempted to sort the jobs by *Start Time*. This crippled the binary search logic because knowing a job starts early provides zero mathematical guarantee about when it finishes, causing chaotic overlaps during the DP `Take` transition.

### What I Learned
In scheduling algorithms, End-Time is the absolute anchor of reality. It strictly dictates when resources are freed.

---

## Problem: Integer Break (343)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Mathematical Breakdown DP
* **Problem Type:** Recursive Partition Optimization
* **Data Structure Used:** 1D DP Array.
* **Brute Force:** Try all additive combinations via DFS. Time: $O(2^N)$.
* **Optimized Approach:** We want to break integer `i` into at least two parts to maximize their product. If we make a first cut of size `j`, the remaining piece is `(i - j)`. We have two choices for this remaining piece: we can leave it intact, or we can break it down further (which is `dp[i - j]`).

### DP State
`dp[i]` represents the **maximum product achievable by breaking the integer `i` into at least two positive integers**.

### State Flow
```text
STATE: dp[i] = max product.

↓

CHOICES for split point `j` (from 1 to i-1):
  Cut off a piece of size `j`. The remainder is `(i - j)`.
  
  Choice A: Do NOT break the remainder. Product = j * (i - j).
  Choice B: Break the remainder further. Product = j * dp[i - j].

↓

TRANSITION: dp[i] = max(dp[i], Choice A, Choice B)
```

### Recurrence
$$\text{dp}[i] = \max_{1 \le j < i} \Big( \text{dp}[i], \; j \times (i - j), \; j \times \text{dp}[i - j] \Big)$$

### Base Cases
* `dp[2] = 1`. (Integer 2 must be broken into $1+1$, yielding product $1 \times 1 = 1$).

### Traversal Order
**Outer Loop:** `i` from `3` to `N`.
**Inner Loop:** Split point `j` from `1` to `i-1`.

### Pointer Flow
```text
N = 4. dp = [0, 0, 1, 0, 0]

Calculate i = 3:
  j=1: max(1 * (2), 1 * dp[2]) = max(2, 1) = 2.
  dp[3] = 2.

Calculate i = 4:
  j=1: max(1 * 3, 1 * dp[3]) = max(3, 2) = 3.
  j=2: max(2 * 2, 2 * dp[2]) = max(4, 2) = 4.
  dp[4] = 4.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^2)                             │
│  Space Complexity │ O(N)                               │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Problem requires dividing a scalar integer into additive subsets.
* ✓ Objective is maximizing a multiplicative product.
* $\rightarrow$ **Mathematical Breakdown DP**

### Core Insight
The mathematical trap is assuming `dp[i]` is *always* larger than `i`. For small numbers like 2 and 3, breaking them yields a smaller number (e.g., $dp[3] = 2$). Therefore, the transition equation must explicitly evaluate leaving the chunk unbroken `j * (i-j)` against the recursive DP lookup `j * dp[i-j]`.

### Mistakes Made
* We originally just wrote `dp[i] = max(dp[i], j * dp[i-j])`. This failed for $N=4$ because `j=1 * dp[3]` yields `2`, missing the fact that keeping the remainder `3` completely unbroken yields `j=1 * 3 = 3`.

### What I Learned
When DP states represent physical fracturing, the transition logic must fundamentally account for the choice to *stop fracturing immediately*.

---

## Problem: Word Break (139)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Prefix Feasibility DP
* **Problem Type:** Dictionary Segmentation
* **Data Structure Used:** 1D Boolean DP Array + HashSet for dictionary lookups.
* **Brute Force:** Generate every substring and check dictionary. Time: $O(2^N)$.
* **Optimized Approach:** We track if the prefix ending at `i` can be perfectly segmented. To calculate `dp[i]`, we look backwards for a split point `j`. If the prefix up to `j` was valid (`dp[j] == True`), AND the substring from `j` to `i` is a valid dictionary word, then the entire string up to `i` is valid.

### DP State
`dp[i]` represents a **boolean indicating whether the prefix `s[0...i-1]` can be perfectly partitioned into valid dictionary words**.

### State Flow
```text
STATE: dp[i] = True/False.

↓

CHOICES for split point `j` (0 <= j < i):
  If dp[j] is True (The prefix up to j is valid):
    Check if the physical substring s[j:i] exists in the dictionary.
    If YES, dp[i] is True! We can immediately 'break' the inner loop.

↓

TRANSITION: dp[i] = True if (dp[j] and dict.contains(s[j:i])) for any j.
```

### Recurrence
$$\text{dp}[i] = \bigvee_{0 \le j < i} (\text{dp}[j] \land (\text{s}[j:i] \in \text{dict}))$$

### Base Cases
* `dp[0] = True`. An empty string requires 0 segments, which is technically a valid dictionary partition state.

### Traversal Order
**Outer Loop:** End index `i` from `1` to `len(s)`.
**Inner Loop:** Split point `j` from `0` to `i-1`.

### Pointer Flow
```text
s = "leetcode", dict = {"leet", "code"}
dp = [True, False, False, False, False, False, False, False, False]

i=4 ("leet"):
  j=0: dp[0] is True. s[0:4] = "leet". Found in dict!
  dp[4] = True. Break loop.
  
i=8 ("leetcode"):
  j=0...3: dp[j] is False. Ignore.
  j=4: dp[4] is True. s[4:8] = "code". Found in dict!
  dp[8] = True. Break loop.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^3) (nested loops + slicing O(N)│
│  Space Complexity │ O(N) (1D boolean tracking array)   │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Evaluating string segments against a master dictionary/set.
* ✓ Output requests a boolean validity (can it be done?).
* $\rightarrow$ **Prefix Feasibility DP**

### Core Insight
A string parsing problem is just an Interval DP anchored strictly to the `0` index. By iterating rightward and scanning backward for anchor points (`dp[j]`), we chain together independent valid segments without generating a massive recursion tree.

### Mistakes Made
* We executed dictionary checks on a `list`. The `in` operator on lists is $O(K)$, rocketing the time complexity into Time Limit Exceeded. Instantiating a `set()` from the dictionary on line 1 drops the lookup back to $O(1)$.

### What I Learned
The inner loop `break` statement is critical in boolean DP. Once a node is proven `True`, checking further permutations wastes CPU cycles.

---

## Problem: Best Time to Buy and Sell Stock IV (188)

* **Interview Difficulty:** Hard
* **Parent Pattern:** State Machine DP
* **Problem Type:** Transaction Bounds Optimization
* **Data Structure Used:** Dual 1D Arrays (`buy` and `sell`) sized to `K` transactions.
* **Brute Force:** DFS evaluating buy/sell/skip at every day. Time: $O(3^N)$.
* **Optimized Approach:** The state is 3-dimensional: (Day `i`, Transactions used `j`, Holding Status). We compress the `Day` dimension entirely out of existence. We track the max profit if we are currently `Holding` a stock on transaction `j`, and if we are `Not Holding` on transaction `j`. 

### DP State
* `buy[j]`: Max profit after `j` transactions ending in a **Holding** state.
* `sell[j]`: Max profit after `j` transactions ending in an **Empty** state.

### State Flow
```text
For a given `price` on Day i:

STATE: Updating transaction j (1 to K):

↓

CHOICES for `buy[j]`:
  Choice A: Do nothing. Keep holding the stock from yesterday. (buy[j])
  Choice B: Buy today. Pay the `price` using profits from the previous FULL transaction `j-1`. (sell[j-1] - price)

CHOICES for `sell[j]`:
  Choice A: Do nothing. Stay empty. (sell[j])
  Choice B: Sell today. Cash out the `buy[j]` state for the current `price`. (buy[j] + price)

↓

TRANSITION: buy[j] = max(buy[j], sell[j-1] - price)
            sell[j] = max(sell[j], buy[j] + price)
```

### Recurrence
(Direct execution of the state transitions defined above).

### Base Cases
* `buy` array initialized to `float('-inf')` (Buying costs money, putting profit in the negative. Zero is invalid).
* `sell` array initialized to `0`.

### Traversal Order
**Outer Loop:** Traverse `price` in `prices` array.
**Inner Loop:** Traverse transaction index `j` from `1` to `K`.

### Pointer Flow
```text
K = 2, prices = [2, 4, 1]
Base: buy = [-inf, -inf, -inf], sell = [0, 0, 0]

Day 1 (Price 2):
  j=1: buy[1] = max(-inf, sell[0] - 2) = -2. 
       sell[1] = max(0, buy[1] + 2) = max(0, -2 + 2) = 0.
  j=2: buy[2] = max(-inf, sell[1] - 2) = -2.
       sell[2] = max(0, -2 + 2) = 0.

Day 2 (Price 4):
  j=1: buy[1] = max(-2, 0 - 4) = -2.
       sell[1] = max(0, -2 + 4) = 2.
...
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N * K)                           │
│  Space Complexity │ O(K) (Two 1D arrays of size K)     │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Array of temporal sequence values (prices, temperatures).
* ✓ Strict upper limit on the number of phase changes (`K` limits).
* ✓ Binary/Ternary statuses (Holding vs Empty).
* $\rightarrow$ **State Machine DP**

### Core Insight
State Machine arrays simulate physical dimensions. Buying transfers data from the `sell` array into the `buy` array. Selling transfers data back. The $K$ limit acts as a strict spatial cap on how deep the data can bounce back and forth.

### Mistakes Made
* We ignored the $K \ge N/2$ edge case. If $K$ is massive (e.g., $10^9$), creating a $K$-sized array instantly crashes the memory limit. If $K \ge N/2$, the mathematical limit of transactions physically achievable on an $N$-length array is bypassed. The problem degrades into infinite transactions, which must be routed to a separate $O(N)$ $O(1)$-space greedy function.

### What I Learned
DP matrices tracking transaction counts can be flattened from 3D to 1D by relying entirely on overwriting `j` arrays in place.

---

## Problem: Stone Game (877)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Minimax Game Theory DP
* **Problem Type:** Two-Player Zero-Sum Game
* **Data Structure Used:** 2D DP Array for intervals.
* **Brute Force:** Evaluate all permutations of picking left vs right. Time: $O(2^N)$.
* **Optimized Approach:** We define `dp[i][j]` as the **Relative Score Difference** between the first player acting on the interval and the second player. If a player picks the left edge `piles[i]`, they gain those points, but they hand the remaining sub-interval `[i+1...j]` to the opponent, who will mathematically extract `dp[i+1][j]` points from them. 

### DP State
`dp[i][j]` represents the **maximum relative score advantage the current active player can extract from the physical interval starting at `i` and ending at `j`**.

### State Flow
```text
STATE: dp[i][j] = Relative Score Difference.

↓

CHOICES for active player:
  Choice A (Take Left):
    Gain piles[i]. Lose whatever advantage opponent extracts from remaining board.
    Score = piles[i] - dp[i+1][j]
    
  Choice B (Take Right):
    Gain piles[j]. Lose opponent's advantage from remaining board.
    Score = piles[j] - dp[i][j-1]

↓

TRANSITION: dp[i][j] = max(Choice A, Choice B)
```

### Recurrence
$$\text{dp}[i][j] = \max(\text{piles}[i] - \text{dp}[i+1][j], \; \text{piles}[j] - \text{dp}[i][j-1])$$

### Base Cases
* `dp[i][i] = piles[i]`. If only one pile exists, the player takes it, scoring a relative difference of exactly that pile's value.

### Traversal Order
**Interval DP Gap Method.** Length `L` from `2` to `N`.

### Pointer Flow
```text
piles = [5, 3, 4, 5]
Base (L=1): dp[i][i] = [5, 3, 4, 5]

L = 2:
  Interval (0,1) -> [5,3]: max(5-3, 3-5) = 2.
  Interval (1,2) -> [3,4]: max(3-4, 4-3) = 1.
  Interval (2,3) -> [4,5]: max(4-5, 5-4) = 1.

L = 3:
  Interval (0,2) -> [5,3,4]:
    Take left: 5 - dp[1][2] = 5 - 1 = 4.
    Take right: 4 - dp[0][1] = 4 - 2 = 2.
    dp[0][2] = max(4, 2) = 4.
...
Final DP[0][N-1] evaluates the relative score difference for the entire game.
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^2) (Interval Gap Traversal)    │
│  Space Complexity │ O(N^2) (2D tracking matrix)        │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Two-player game acting on opposite ends of a sequence.
* ✓ Evaluation requires checking who ultimately "wins" (has more points).
* $\rightarrow$ **Interval Minimax Game Theory DP**

### Core Insight
The subtractive operation (`piles[i] - dp_subproblem`) perfectly simulates a zero-sum game. You do not need two DP arrays to track Player A and Player B. The current player maximizes their gain MINUS the opponent's mathematically optimal future gain.

### Mistakes Made
* We attempted to track absolute scores by returning a tuple `(my_score, opp_score)`. While functional, this completely bloated the state architecture. Understanding that a zero-sum game is purely an evaluation of the mathematical delta (difference) between players crushes the data requirement down to a single scalar integer.

### What I Learned
Minimax DP without bitmasks operates almost identically to Interval DP. The only structural difference is injecting the subtraction operator into the subproblem inheritance to simulate passing the turn to a hostile agent.

---

### Master Patterns Learned

#### 1. DP + Binary Search Coupling
* **The Strategy:** Deploy when elements have temporal bounds (start, end) and constraints prohibit overlapping.
* **The Conceptual Mechanics:** Sort the sequence strictly by the variable that releases the resource (End Time). Use binary search to locate the most recently freed historical resource in $O(\log N)$, replacing the standard $O(N)$ DP inner sweep.

#### 2. The Multi-Array State Machine
* **The Strategy:** Deploy when the prompt enforces hard phase limits (e.g. at most K transactions, cooldown periods, buying/selling statuses).
* **The Conceptual Mechanics:** Establish parallel tracking arrays representing the distinct phases of reality. Edges between states execute via addition/subtraction across arrays (e.g., `sell` reads from `buy`).

#### 3. Zero-Sum Relative Scoring
* **The Strategy:** Deploy on two-player competitive turn-taking games.
* **The Conceptual Mechanics:** The DP engine does not know who Player 1 is. It only knows "Current Turn". By subtracting the DP subproblem from the current gain (`gain - dp[remaining]`), the math natively simulates the hostile opponent taking their best possible counter-move.
