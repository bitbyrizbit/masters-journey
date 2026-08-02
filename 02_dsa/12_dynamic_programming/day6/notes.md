# String / Sequence DP

## 1. What is Prefix DP?

String DP (or Sequence DP) is technically a subset of Grid DP, but instead of traversing physical geographic coordinates, we traverse the **prefixes** of two independent strings (or two independent arrays). 

When we place String A on the vertical axis (rows) and String B on the horizontal axis (columns), the resulting 2D matrix operates identically to a grid. The critical difference lies in the transition triggers: movement is strictly governed by whether the current character in String A matches the current character in String B.

---

## 2. Matching States & Diagonal Transitions

The foundational architecture of String DP relies on observing the terminal characters of the current prefixes being evaluated.

> **The Universal String State Definition:**
> `dp[i][j]` represents the optimal mathematical answer when comparing the prefix of `String1` (up to index `i-1`) against the prefix of `String2` (up to index `j-1`).

### The Golden Rule of String DP Transitions
When evaluating `String1[i-1]` against `String2[j-1]`:
1. **If the characters MATCH:** We possess a free pass. The optimal answer is purely derived from the state *before* either of these characters existed. Geometrically, this means inheriting from the **Top-Left Diagonal (`dp[i-1][j-1]`)**.
2. **If the characters MISMATCH:** The chain is broken. We must mathematically determine which string to penalize (delete, insert, skip). We inherit from either the **Top (`dp[i-1][j]`)** or the **Left (`dp[i][j-1]`)**.

---

## 3. The 1D Diagonal Cache (Space Optimization)

Just like Grid DP, we only need the previous row to compute the current row. However, because String DP frequently inherits from the `Top-Left Diagonal`, standard space compression faces a unique hazard.

When we update `dp[j]`, we overwrite the value from the previous row. If `dp[j+1]` later needs its top-left diagonal, it expects the *old* `dp[j]`, not the one we just updated!

**The Solution:** We must introduce a temporary scalar variable (usually named `prev`) to cache the old `dp[j]` just before it gets overwritten, preserving the diagonal data for the next column's calculation.

---

## Problem: Longest Common Subsequence (1143)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Parent String DP
* **Problem Type:** Sequence Alignment
* **Data Structure Used:** 1D Space-Optimized Array with a `prev` diagonal cache.
* **Brute Force:** Generate all $2^M$ subsequences of `text1` and check if they exist in `text2`. Time: $O(2^M \cdot N)$.
* **Optimized Approach:** We map `text1` against `text2`. If the current characters match, we extend the LCS from the diagonal. If they mismatch, we take the absolute maximum of skipping the current character in `text1` (top) vs skipping the current character in `text2` (left). 

### DP State
`dp[i][j]` represents the **length of the longest common subsequence between `text1[0...i-1]` and `text2[0...j-1]`**.

### State Flow
```text
STATE: dp[i][j] = length of LCS of the two prefixes.

↓

CHOICES when evaluating text1[i-1] and text2[j-1]:
  Condition A: Characters match!
    Extend the sequence from the state before both chars: (Top-Left Diagonal + 1)
  
  Condition B: Characters mismatch.
    We must drop one char. We take the Max of:
      - Dropping from text1 (Inherit from Top)
      - Dropping from text2 (Inherit from Left)

↓

TRANSITION: 
  If match: dp[j] = prev_diagonal + 1
  Else: dp[j] = max(dp[j], dp[j-1])
```

### Recurrence
$$\text{dp}[j] = \begin{cases} \text{prev\_diagonal} + 1 & \text{if } \text{text1}[i-1] == \text{text2}[j-1] \\ \max(\text{dp}[j], \text{dp}[j-1]) & \text{otherwise} \end{cases}$$

### Base Cases
* If either string is empty, the LCS is exactly `0`. The 1D array is initialized entirely to `0`.

### Traversal Order
**Outer Loop:** `i` from `1` to `M` (Length of `text1`).
**Inner Loop:** `j` from `1` to `N` (Length of `text2`).

### Pointer Flow
```text
text1 = "abcde", text2 = "ace"
Base 1D array (row 0): dp = [0, 0, 0, 0] (representing matching against empty string)

Processing Row 1 ('a'):
  j=1 ('a'): Match! dp[1] = prev_diag (0) + 1 = 1
  j=2 ('c'): Mismatch. dp[2] = max(top=0, left=1) = 1
  j=3 ('e'): Mismatch. dp[3] = max(top=0, left=1) = 1
  dp state: [0, 1, 1, 1]

Processing Row 2 ('b'):
  j=1 ('a'): Mismatch. max(top=1, left=0) = 1
  j=2 ('c'): Mismatch. max(top=1, left=1) = 1
  j=3 ('e'): Mismatch. max(top=1, left=1) = 1
  dp state: [0, 1, 1, 1]

Processing Row 3 ('c'):
  j=1 ('a'): Mismatch -> 1
  j=2 ('c'): Match! dp[2] = prev_diag (1 from 'a') + 1 = 2
  ...
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(M * N)                           │
│  Space Complexity │ O(min(M, N)) (1D optimized array)  │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Comparing two independent arrays or strings.
* ✓ Seeking the "longest" or "maximum" overlap that isn't strictly contiguous.
* $\rightarrow$ **Prefix DP (LCS Framework)**

### Core Insight
Subsequences allow gaps. The `max(top, left)` transition perfectly models the behavior of "skipping a character" to hunt for a better match deeper in the opposing string.

### Mistakes Made
* We attempted space optimization without the `prev` variable. When a character matched, `dp[j] = dp[j-1] + 1` was executed, which erroneously inherited data from the current row (simulating infinite character reuse) rather than the previous row's diagonal.

### What I Learned
The `prev` cache variable is non-negotiable in String DP when collapsing 2D matrices into 1D arrays. It mathematically isolates the temporal state of `(i-1, j-1)`.

---

## Problem: Edit Distance (72)

* **Interview Difficulty:** Hard
* **Parent Pattern:** Classic String Operations DP
* **Problem Type:** Min Cost Sequence Alignment
* **Data Structure Used:** 1D DP Array tracking operation counts.
* **Brute Force:** Recursive DFS executing all 3 operations (insert, delete, replace) at every mismatch. Time: $O(3^{\max(M, N)})$.
* **Optimized Approach:** We measure the minimum steps to mutate `word1` into `word2`. A match costs 0 (diagonal inheritance). A mismatch costs 1 step plus the minimum of three historical paths: Insert (left), Delete (top), Replace (diagonal).

### DP State
`dp[i][j]` represents the **absolute minimum operations required to convert `word1[0...i-1]` into `word2[0...j-1]`**.

### State Flow
```text
STATE: dp[i][j] = min operations for prefix conversion.

↓

CHOICES when evaluating word1[i-1] and word2[j-1]:
  Match! Cost = 0.
    Inherit from Top-Left Diagonal.
  
  Mismatch! Cost = 1.
    Take the minimum of:
      1. Replace char (Diagonal)
      2. Delete char from word1 (Top)
      3. Insert char into word1 (Left)

↓

TRANSITION: 
  If match: dp[j] = prev_diagonal
  Else: dp[j] = 1 + min(prev_diagonal, dp[j], dp[j-1])
```

### Recurrence
$$\text{dp}[j] = \begin{cases} \text{prev\_diagonal} & \text{if match} \\ 1 + \min(\text{prev\_diagonal}, \text{dp}[j], \text{dp}[j-1]) & \text{if mismatch} \end{cases}$$

### Base Cases
* `dp` array initialization (row 0): To convert an empty `word1` into `word2` of length `j`, we must execute exactly `j` insertions. `dp[j] = j`.
* Column 0 initialization (`prev = dp[0]` for row `i`): To convert `word1` of length `i` into an empty `word2`, we must execute exactly `i` deletions. `dp[0] = i`.

### Traversal Order
**Outer Loop:** `i` from `1` to `M`.
**Inner Loop:** `j` from `1` to `N`.

### Pointer Flow
*(Standard nested double loop identical to LCS, swapping `max` for `min` and altering base cases).*

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(M * N)                           │
│  Space Complexity │ O(N) (1D optimized array)          │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Mutating or morphing one sequence into another.
* ✓ Operations involve strict insertions, deletions, or substitutions.
* $\rightarrow$ **Edit Distance DP**

### Core Insight
Edit distance mathematically quantifies the "difference" between two strings. The base cases (row 0 and col 0) aren't `0`; they are strictly linear scales `(1, 2, 3...)` because deleting/inserting against an empty string scales directly with the length of the opposing string.

### Mistakes Made
* We initialized the 1D array with `0`s. This crippled the algorithm because the `min()` function perpetually dragged the cost back down to `0`. The 0th row MUST be populated with `1, 2, 3, 4...` to represent base insertion costs.

### What I Learned
Base case boundary initializations dictate the mathematical floor of the DP engine. If boundaries are flawed, the internal transitions will propagate garbage data across the entire matrix.

---

## Problem: Longest Palindromic Subsequence (516)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Reverse String DP
* **Problem Type:** Single-String Structure Parsing
* **Data Structure Used:** 1D DP Array (Standard LCS architecture).
* **Brute Force:** DFS evaluating two pointers expanding from every possible center. Time: $O(2^N)$.
* **Optimized Approach:** A massive conceptual shortcut: A palindrome mathematically reads identically forwards and backwards. Therefore, the Longest Palindromic Subsequence of a string `s` is perfectly equivalent to the Longest Common Subsequence between `s` and `reverse(s)`.

### DP State
`dp[i][j]` evaluates the LCS between `s` and `s[::-1]`.

### State Flow
*(Identical to Problem 1: Longest Common Subsequence)*

### Recurrence
*(Identical to Problem 1: Longest Common Subsequence)*

### Base Cases
*(Identical to Problem 1: Longest Common Subsequence)*

### Traversal Order
*(Identical to Problem 1: Longest Common Subsequence)*

### Pointer Flow
*(Identical to Problem 1: Longest Common Subsequence)*

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(N^2) (Where N is len(s))         │
│  Space Complexity │ O(N) (1D optimized array)          │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Problem requests the longest internal palindrome.
* ✓ Subsequence rules (non-contiguous characters allowed).
* $\rightarrow$ **Reverse String DP (LCS Hack)**

### Core Insight
Why invent a complex 2-pointer interval DP state when we can elegantly mutate the input and run a solved algorithm? Passing `s` and `reverse(s)` into an off-the-shelf LCS function solves the problem natively.

### Mistakes Made
* Initially, we attempted to write a complex 2D interval DP tracking `left` and `right` indices. While correct, it was highly prone to off-by-one boundary errors. Re-routing the problem into the LCS template is vastly safer.

### What I Learned
Many advanced string problems are secretly just LCS or Edit Distance hidden behind a clever input transformation.

---

## Problem: Distinct Subsequences (115)

* **Interview Difficulty:** Hard
* **Parent Pattern:** Counting String DP
* **Problem Type:** Prefix Combinatorics
* **Data Structure Used:** 1D Space-Optimized Array tracking combinatorial paths.
* **Brute Force:** Generate all $2^M$ subsequences of `s` and count how many exactly match `t`. Time: $O(2^M \cdot N)$.
* **Optimized Approach:** We are counting the number of ways `t` can be mathematically carved out of `s`. Because we are counting paths, we switch to a `+` accumulator. Crucially, multiple characters in `s` can map to the same character in `t`. To avoid infinite reuse in a 1D array, the inner loop evaluating `t` MUST run backwards (identical to 0/1 Knapsack constraints).

### DP State
`dp[j]` represents the **total number of distinct ways to form the prefix of `t` (of length `j`) using the currently processed characters of `s`**.

### State Flow
```text
STATE: dp[j] = total ways to form t[0...j-1].

↓

CHOICES when evaluating s[i-1] against t[j-1]:
  Condition A: Characters match!
    We have two valid paths:
      1. IGNORE this match and use older matches (dp[j])
      2. USE this match, and append it to the paths that formed the previous prefix (dp[j-1])
    Total = dp[j] + dp[j-1]
    
  Condition B: Characters mismatch.
    We CANNOT use this character. Inherit older matches only.
    Total = dp[j]

↓

TRANSITION: If match, dp[j] = dp[j] + dp[j-1]
```

### Recurrence
$$\text{dp}[j] = \begin{cases} \text{dp}[j] + \text{dp}[j-1] & \text{if } \text{s}[i-1] == \text{t}[j-1] \\ \text{dp}[j] & \text{otherwise} \end{cases}$$

### Base Cases
* `dp[0] = 1`. There is exactly `1` way to form an empty string `t`: by deleting all characters in `s`.

### Traversal Order
**Outer Loop:** `i` from `1` to `M` (Length of `s`).
**Inner Loop (CRITICAL):** `j` **BACKWARDS** from `N` down to `1` (Length of `t`).

### Pointer Flow
```text
s = "babgbag", t = "bag"
Base: dp = [1, 0, 0, 0] (Capacity to form prefixes of len 0, 1, 2, 3)

s[0] = 'b': Matches t[0]. dp[1] += dp[0] -> 1. dp = [1, 1, 0, 0]
s[1] = 'a': Matches t[1]. dp[2] += dp[1] -> 1. dp = [1, 1, 1, 0]
s[2] = 'b': Matches t[0]. dp[1] += dp[0] -> 2. dp = [1, 2, 1, 0]
s[3] = 'g': Matches t[2]. dp[3] += dp[2] -> 1. dp = [1, 2, 1, 1]
...
```

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(M * N)                           │
│  Space Complexity │ O(N) (1D optimized array)          │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Counting permutations or distinct ways one string exists inside another.
* ✓ Subsequence rules (gaps allowed).
* $\rightarrow$ **Counting String DP**

### Core Insight
This is literally 0/1 Knapsack masked as a string problem. The characters of `s` are the items. The characters of `t` are the capacity constraints. Because an index of `s` can only be consumed once, the inner loop must strictly traverse backward.

### Mistakes Made
* Running the inner loop forwards triggered a catastrophic failure where a single `'b'` in `s` would satisfy a `'b'` in `t`, and then immediately feed itself to satisfy another `'b'` further down the `t` string in the same loop pass.

### What I Learned
The Backward Inner Loop is the universal locking mechanism for enforcing single-use combinatorics in space-optimized DP arrays, regardless of whether the domain is physical capacity (Knapsacks) or string indices.

---

## Problem: Minimum ASCII Delete Sum for Two Strings (712)

* **Interview Difficulty:** Medium
* **Parent Pattern:** Weighted LCS DP
* **Problem Type:** Min Cost Sequence Alignment
* **Data Structure Used:** 1D DP Array tracking ASCII penalties.
* **Brute Force:** DFS generating all matching branches and calculating ASCII deletion sums. Time: $O(2^{\max(M, N)})$.
* **Optimized Approach:** An exact replica of the Edit Distance and LCS frameworks, but instead of the deletion penalty being `+1`, the penalty is mathematically weighted by the exact ASCII integer value of the deleted character (`ord(char)`).

### DP State
`dp[i][j]` represents the **absolute minimum ASCII sum of deleted characters required to make `s1[0...i-1]` exactly equal to `s2[0...j-1]`**.

### State Flow
```text
STATE: dp[i][j] = min ASCII delete sum.

↓

CHOICES when evaluating s1[i-1] against s2[j-1]:
  Condition A: Characters match!
    No deletions necessary. Inherit from Top-Left Diagonal.
    Cost = prev_diagonal
    
  Condition B: Characters mismatch.
    We must delete one. Take the minimum cost path:
      1. Delete from s1: Inherit from Top (dp[i-1][j]) + ord(s1[i-1])
      2. Delete from s2: Inherit from Left (dp[i][j-1]) + ord(s2[j-1])

↓

TRANSITION: If match, dp[j] = prev_diagonal
            Else, dp[j] = min(top + ord(s1), left + ord(s2))
```

### Recurrence
$$\text{dp}[j] = \begin{cases} \text{prev\_diagonal} & \text{if match} \\ \min(\text{dp}[j] + \text{ord}(\text{s1}[i-1]), \; \text{dp}[j-1] + \text{ord}(\text{s2}[j-1])) & \text{if mismatch} \end{cases}$$

### Base Cases
* Row 0 Initialization: Deleting all characters from `s2` to match an empty `s1`. `dp[j] = dp[j-1] + ord(s2[j-1])`.
* Column 0 Initialization: Deleting all characters from `s1` to match an empty `s2`. `prev = dp[0]`, then `dp[0] = dp[0] + ord(s1[i-1])`.

### Traversal Order
**Outer Loop:** `i` from `1` to `M`.
**Inner Loop:** `j` from `1` to `N`.

### Pointer Flow
*(Standard nested double loop identical to Edit Distance).*

### Complexity
```text
┌────────────────────────────────────────────────────────┐
│  Time Complexity  │ O(M * N)                           │
│  Space Complexity │ O(N) (1D optimized array)          │
└────────────────────────────────────────────────────────┘
```

### Recognition
* ✓ Evolving one string into another.
* ✓ Penalties/Costs are tied to specific physical properties of the items (ASCII values).
* $\rightarrow$ **Weighted String Operations DP**

### Core Insight
String operations DP is completely modular. The "+1" penalty in Edit Distance is just a placeholder variable. We can swap it for ASCII values, dictionary weights, or arbitrary integer arrays without altering the underlying nested loop matrix architecture.

### Mistakes Made
* We failed to properly initialize the base boundaries. We initially populated row 0 with just `ord(s2)`, forgetting that to delete `3` characters, the cost is the *cumulative sum* of all 3 ASCII values, not just the single terminal character.

### What I Learned
Boundary initialization on weighted DP problems requires cumulative prefix sums, unlike standard DP which only requires scalar scaling `(1, 2, 3)`.

---

### Master Patterns Learned

#### 1. The Prefix Alignment Matrix (The LCS Engine)
* **The Strategy:** Deploy this dual-string loop structure whenever a prompt requests evaluating overlapping sequences, substrings, or morphing operations.
* **The Conceptual Mechanics:** `String A` governs the vertical `Top` inheritances (row drops). `String B` governs the horizontal `Left` inheritances (column drops). Perfect matches bypass both dimensions and inherit directly from the temporal past (the Top-Left Diagonal).

#### 2. The Diagonal Cache (`prev`)
* **The Strategy:** A mandatory requirement for space-optimizing any 2D sequence matching matrix down to 1D.
* **The Conceptual Mechanics:** Because `dp[j]` naturally acts as the `Top` cell, overwriting it destroys the historical data required for the `Top-Left Diagonal` of the next step. Caching `temp = dp[j]` before the transition block and executing `prev = temp` afterward isolates the temporal state flawlessly.

#### 3. Reversed Inner Loops (String Combinatorics)
* **The Strategy:** Used specifically when counting occurrences (Distinct Subsequences).
* **The Conceptual Mechanics:** When tracking combinatorial path construction across sequences where elements cannot be reused for the same prefix step, executing the inner loop backward acts as a mechanical lock against infinite loop self-feeding.
