## Problem: Permutations of a Set

* **Problem Type:** Ordered Counting / Factorial Progression
* **Data Structure Used:** Scalar numeric variables
* **Approach 1:** Factorial calculation. Compute $P(n, r) = \frac{n!}{(n-r)!}$ by calculating both factorials fully and then dividing. This is $O(n)$ but is highly prone to integer overflow because factorials grow extremely fast (e.g. $21!$ exceeds the maximum value of a 64-bit unsigned integer).
* **Optimized Approach:** Iterative Product. Calculate the permutation value directly by multiplying the $r$ terms starting from $n$ downwards: $P(n, r) = n \cdot (n-1) \cdot ... \cdot (n-r+1)$. This avoids computing large intermediate factorials.
* **Complexity:**
  * **Time:** $O(r)$ time.
  * **Space:** $O(1)$ auxiliary space.
* **Pointer Flow:**
```text
Calculating permutations P(5, 3):
1. Initialize: res = 1, terms_left = 3
2. Multiply by n (5): res = 5. terms_left = 2.
3. Multiply by n-1 (4): res = 5 * 4 = 20. terms_left = 1.
4. Multiply by n-2 (3): res = 20 * 3 = 60. terms_left = 0.
5. Loop terminates. Return 60.
```
* **Pattern Recognition:**
  * Use Permutations when:
    - Counting the number of ways to arrange a subset of items where **order matters** (e.g., code locks, scheduling unique tasks).
    - Determining unique permutations of strings with duplicate characters.
* **Core Insight:** A permutation is a sequence of choices where the pool of available options shrinks by 1 at each step. For the first choice, we have $n$ options; for the second, $n-1$ options, and so on. We only need to multiply these options for the $r$ selections.
* **Mistakes Made:** A common mistake is not dividing out duplicate objects when the set contains identical items (e.g. permutations of "AAB"). If we have duplicate items, we must divide the total permutations by the factorials of the duplicate counts: $\frac{n!}{n_1! \cdot n_2!...}$.
* **What I Learned:** Choice sequences can be calculated iteratively. Breaking down formulas into direct choice steps avoids large intermediate factorials.

---

## Problem: Combinations (Binomial Coefficients)

* **Problem Type:** Selection Counting / Tabular DP
* **Data Structure Used:** 2D Array (DP Table)
* **Approach 1:** Factorial calculation. Compute $C(n, r) = \frac{n!}{r! \cdot (n-r)!}$ by calculating the three factorials and dividing. Similar to permutations, this causes overflow issues very early, even when the final combination value is small.
* **Optimized Approach:** Pascal's Triangle DP. Build a 2D DP table using Pascal's Identity: $C(n, r) = C(n-1, r-1) + C(n-1, r)$. This calculates combinations using addition only, avoiding factorials and preventing overflow.
* **Complexity:**
  * **Time:** $O(n \cdot r)$ time to fill the table.
  * **Space:** $O(n \cdot r)$ space to store the table. This can be optimized to $O(r)$ space by only keeping the previous row of the table.
* **Pointer Flow:**
```text
Calculating combinations C(4, 2) using DP:
1. Initialize table of size 5x3 with 0s. Set base cases: dp[i][0] = 1, dp[i][i] = 1.
2. Row 1: dp[1][0] = 1, dp[1][1] = 1
3. Row 2: dp[2][0] = 1
          dp[2][1] = dp[1][0] + dp[1][1] = 1 + 1 = 2
          dp[2][2] = 1
4. Row 3: dp[3][0] = 1
          dp[3][1] = dp[2][0] + dp[2][1] = 1 + 2 = 3
          dp[3][2] = dp[2][1] + dp[2][2] = 2 + 1 = 3
5. Row 4: dp[4][0] = 1
          dp[4][1] = dp[3][0] + dp[3][1] = 1 + 3 = 4
          dp[4][2] = dp[3][1] + dp[3][2] = 3 + 3 = 6
6. Return dp[4][2] = 6.
```
* **Pattern Recognition:**
  * Use Combinations when:
    - Choosing a subset of items where **order does not matter** (e.g., picking teams, selecting cards).
    - Counting grid paths (the number of paths from the top-left to the bottom-right of an $N \times M$ grid is $\binom{N+M-2}{N-1}$).
* **Core Insight:** Pascal's Identity states that to choose $r$ items from $n$ options, we can pick a specific item and then choose $r-1$ items from the remaining $n-1$ options, OR we can skip that item and choose all $r$ items from the remaining $n-1$ options. This breaks the problem down into two disjoint, smaller subproblems.
* **Mistakes Made:** When using the formula $C(n, r) = \frac{n \cdot (n-1)...(n-r+1)}{r!}$, if we do the divisions at the end, we still risk overflow. If we divide step-by-step during the iteration, we must ensure each intermediate division is an integer division. This is guaranteed if we divide by the loop counter $i$ on step $i$, because any product of $i$ consecutive integers is always divisible by $i!$.
* **What I Learned:** Addition-based DP eliminates multiplicative overflows. Using Pascal's identity allows us to compute large combinatorial values using simple additions.

---

### Master Patterns Learned

#### 1. Pascal's Triangle DP Frame
* **The Strategy:** Compute combinations dynamically using Pascal's Identity to build the values bottom-up using additions only.
* **Code Pattern:**
```python
def get_combinations(n, r):
    dp = [[0] * (r + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 1
        for j in range(1, min(i, r) + 1):
            if i == j:
                dp[i][j] = 1
            else:
                dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
    return dp[n][r]
```
*(For detailed combinatorial formulas on repetition and permutations, refer to the `combinatorics.md`, `permutations.md`, and `combinations.md` files in this directory).*
