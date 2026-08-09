## Catalan Numbers

* **Problem Type:** Structural Counting / Recursive Decomposition DP
* **Data Structure Used:** 1D DP array of size $N+1$
* **Approach 1:** Direct combinatorial formula $C_n = \frac{1}{n+1}\binom{2n}{n}$. Computing this requires calculating large factorials ($2n)!$ which causes integer overflow in many languages, and computing $\binom{2n}{n}$ is itself expensive without modular arithmetic tricks.
* **Optimized Approach:** Recurrence-based DP. Use Pascal-style buildup: $C_0 = 1$, and for each $n \ge 1$, accumulate: $C_n = \sum_{i=0}^{n-1} C_i \cdot C_{n-1-i}$. This builds each Catalan number from previously computed smaller ones, using only multiplication and addition.
* **Complexity:**
  * **Time:** $O(N^2)$ — for each of the $N$ values, we iterate over $N$ pairs of sub-values.
  * **Space:** $O(N)$ to store the DP array.
* **Pointer Flow:**
```text
Computing Catalan numbers C_0 through C_5:
1. dp = [1, 0, 0, 0, 0, 0]  (base: C_0 = 1)
2. C_1: i=0 -> dp[0]*dp[0] = 1. C_1 = 1.   dp = [1,1,0,0,0,0]
3. C_2: i=0 -> dp[0]*dp[1] = 1.
        i=1 -> dp[1]*dp[0] = 1. C_2 = 2.   dp = [1,1,2,0,0,0]
4. C_3: i=0 -> 1*2=2, i=1 -> 1*1=1, i=2 -> 2*1=2. C_3 = 5. dp=[1,1,2,5,0,0]
5. C_4: i=0->5, i=1->2, i=2->2, i=3->5. C_4 = 14.
6. C_5: i=0->14, i=1->5, i=2->4, i=3->5, i=4->14. C_5 = 42.
Final: [1, 1, 2, 5, 14, 42]
```
* **Pattern Recognition:**
  * Use Catalan DP when:
    - Counting valid pairs of balanced brackets/parentheses of length $2n$.
    - Finding the number of structurally unique binary search trees (BSTs) with exactly $n$ nodes.
    - Counting the ways to triangulate a convex polygon with $n+2$ vertices.
    - Counting mountain ranges (paths that go up and down without going below the baseline) of height $n$.
* **Core Insight:** The Catalan recurrence captures a fundamental principle of recursive decomposition. When counting valid structures of size $n$, we choose a "root" or "boundary" that splits the problem into two independent smaller problems of sizes $i$ and $n-1-i$. Every valid sub-configuration on the left can be paired with every valid sub-configuration on the right, so we multiply their counts. Summing over all split points gives the total for size $n$.

  For the BST application: if we choose node $k$ (where $1 \le k \le n$) as the root, the left subtree has exactly $k-1$ nodes (the nodes $1$ through $k-1$) and the right subtree has $n-k$ nodes (the nodes $k+1$ through $n$). The number of ways to build the left is $C_{k-1}$ and the right is $C_{n-k}$. Summing $\sum_{k=1}^{n} C_{k-1} \cdot C_{n-k}$ is exactly the Catalan recurrence.
* **Mistakes Made:** Confusing Catalan numbers with Fibonacci. Fibonacci sums two adjacent terms ($F_n = F_{n-1} + F_{n-2}$). Catalan sums all pairwise products of complementary terms. Implementing Fibonacci's recurrence for Catalan produces completely wrong values.
* **What I Learned:** A single recursive decomposition principle (split at every possible "boundary") generates an entire family of combinatorial structures. The same recurrence counts BSTs, parentheses, mountain ranges, and triangulations because they all share the same structural splitting geometry.

---

## Matrix Exponentiation

* **Problem Type:** Recurrence Acceleration / Linear Map Composition
* **Data Structure Used:** 2D Matrix (list of lists) as the state carrier
* **Approach 1:** Iterative DP. For Fibonacci: `a, b = b, a + b` repeated $N$ times. This is $O(N)$ time. When $N = 10^{18}$, even $O(N)$ iterations are computationally impossible.
* **Optimized Approach:** Express the recurrence as a matrix multiplication, then apply binary exponentiation to the matrix. This reduces $N$ iterations to $O(\log N)$ matrix multiplications.
* **Complexity:**
  * **Time:** $O(K^3 \cdot \log N)$ where $K$ is the size of the transition matrix. For Fibonacci, $K = 2$, so this is $O(8 \log N) \approx O(\log N)$.
  * **Space:** $O(K^2)$ to store the matrices.
* **Pointer Flow:**
```text
Computing Fibonacci(6) = 8 via Matrix Exponentiation:
Transition matrix T = [[1,1],[1,0]]
State vector V_1 = [F(1), F(0)] = [1, 0]
Goal: V_6 = T^5 * V_1

Binary exponentiation of T^5 (5 = binary 101):
1. bit 0 (=1): res = identity. Multiply res by T = T. Square T: T^2 = [[2,1],[1,1]].
2. bit 1 (=0): No multiply. Square T^2: T^4 = [[5,3],[3,2]].
3. bit 2 (=1): Multiply res (=T) by T^4:
   res = T * T^4 = [[1,1],[1,0]] * [[5,3],[3,2]]
   res[0][0] = 1*5 + 1*3 = 8
   res[0][1] = 1*3 + 1*2 = 5
   res[1][0] = 1*5 + 0*3 = 5
   res[1][1] = 1*3 + 0*2 = 3
   res = [[8,5],[5,3]]  (This is T^5)

Apply to V_1 = [1, 0]:
F(6) = T^5[0][0] * F(1) + T^5[0][1] * F(0)
F(6) = 8 * 1 + 5 * 0 = 8. Correct!
```
* **Pattern Recognition:**
  * Use Matrix Exponentiation when:
    - A linear recurrence of order $k$ needs to be evaluated at extremely large $N$ ($N > 10^7$).
    - Counting paths of length $N$ in a fixed graph (the adjacency matrix raised to power $N$ gives path counts).
    - Computing state transitions in tiled/grid DP problems with periodic structure.
* **Core Insight:** Any linear recurrence $F_n = a_1 F_{n-1} + a_2 F_{n-2} + ... + a_k F_{n-k}$ can be written as a matrix equation $\mathbf{v}_n = M \cdot \mathbf{v}_{n-1}$, where $\mathbf{v}_n = [F_n, F_{n-1}, ..., F_{n-k+1}]^T$ and $M$ is the companion matrix. By induction, $\mathbf{v}_n = M^{n-1} \cdot \mathbf{v}_1$. Matrix multiplication is associative, so binary exponentiation applies directly: $M^n = (M^{n/2})^2$ when $n$ is even, reducing the problem to $O(\log n)$ matrix multiplications.
* **Mistakes Made:** Forgetting to initialize the result matrix as the **identity matrix** (not the zero matrix) in matrix power functions. The identity matrix for $K \times K$ matrices has 1s on the diagonal and 0s elsewhere. Using the zero matrix as the starting result causes all outputs to be zero. A second common mistake is matrix dimension mismatches when the companion matrix size does not match the initial state vector dimension.
* **What I Learned:** Matrix multiplication can encode any sequence of linear transformations. Binary exponentiation is not specific to scalars — it applies to any associative operation with an identity element, including matrix multiplication, polynomial multiplication, and even graph edge compositions.

---

### Master Patterns Learned

#### 1. The Catalan Bilateral Accumulation Frame
* **Applied to:** Number of Unique BSTs, Valid Parentheses Counts, Polygon Triangulation
* **The Strategy:** Build a 1D DP array where each entry is the sum of all pairwise products of entries that split the index into two complementary parts.
* **Code Pattern:**
```python
def catalan(n):
    dp = [0] * (n + 1)
    dp[0] = dp[1] = 1
    for i in range(2, n + 1):
        for j in range(i):
            dp[i] += dp[j] * dp[i - 1 - j]
    return dp[n]
```

#### 2. The Matrix Power Recurrence Frame
* **Applied to:** Fast Fibonacci, Path Counting at Length N, Linear Recurrence Speedup
* **The Strategy:** Represent recurrence as a transition matrix, implement square matrix multiplication, then apply standard binary exponentiation using matrices instead of scalars.
* **Code Pattern:**
```python
def mat_mul(a, b):
    k = len(a)
    res = [[0] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            for m in range(k):
                res[i][j] += a[i][m] * b[m][j]
    return res

def mat_pow(mat, n):
    k = len(mat)
    res = [[1 if i == j else 0 for j in range(k)] for i in range(k)]
    base = [row[:] for row in mat]
    while n > 0:
        if n & 1:
            res = mat_mul(res, base)
        base = mat_mul(base, base)
        n >>= 1
    return res

def fib(n):
    if n <= 1:
        return n
    T = [[1, 1], [1, 0]]
    result = mat_pow(T, n - 1)
    return result[0][0]
```
