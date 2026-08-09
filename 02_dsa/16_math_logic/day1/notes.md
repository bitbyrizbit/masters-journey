## Problem: Greatest Common Divisor (GCD)

* **Problem Type:** Mathematical Divisibility / Euclidean Reduction
* **Data Structure Used:** Pure scalar numeric state variables
* **Approach 1:** Factor Listing. Iterate from $1$ up to $\min(a, b)$, checking if each index divides both $a$ and $b$ with zero remainder. This brute-force scan has a worst-case time complexity of $O(\min(a, b))$, which completely chokes when operating on large 64-bit integers.
* **Optimized Approach:** Euclidean Algorithm. Recursively (or iteratively) replace the larger number with the remainder of dividing the larger number by the smaller one. By computing `a, b = b, a % b` until `b` becomes 0, we rapidly reduce the state space.
* **Complexity:**
  * **Time:** $O(\log(\min(a, b)))$ time. Lamé's Theorem proves that the number of steps in the Euclidean algorithm is at most 5 times the number of digits of the smaller number.
  * **Space:** $O(1)$ auxiliary space for the iterative loop, or $O(\log(\min(a, b)))$ stack frame space for recursive implementations.
* **Pointer Flow:**
```text
State tracing for gcd(48, 18):
1. Initial: a = 48, b = 18
2. Loop 1:  a % b = 48 % 18 = 12. Next: a = 18, b = 12.
3. Loop 2:  a % b = 18 % 12 = 6.  Next: a = 12, b = 6.
4. Loop 3:  a % b = 12 % 6 = 0.   Next: a = 6, b = 0.
5. Loop 4:  b is 0. Break loop. Return a = 6.
```
* **Pattern Recognition:**
  * Use Euclidean Reduction when:
    - The problem requires finding common periodic cycles (e.g. when do two rotating gears align).
    - Simplifying fractions to their lowest terms or solving linear Diophantine equations.
* **Core Insight:** If a number $d$ divides both $a$ and $b$, it must also divide any linear combination of $a$ and $b$. Specifically, it must divide the remainder $r = a - q \cdot b$. Therefore, the set of common divisors of $a$ and $b$ is identical to the set of common divisors of $b$ and $a \bmod b$.
* **Mistakes Made:** A common error is assuming recursive GCD handles negative numbers natively without precautions. In Python, `a % b` returns a result with the same sign as `b`. If either input is negative, the algorithm can get stuck in infinite loops or return incorrect negative GCDs. Always convert inputs using `abs()` to guarantee a positive GCD.
* **What I Learned:** Linear reduction can be bypassed by modulo operations. Modulo acts as a teleportation jump that skips multiple subtraction steps in a single step.

---

## Problem: Least Common Multiple (LCM)

* **Problem Type:** Mathematical Divisibility / Divisibility Duality
* **Data Structure Used:** Scalar numeric variables
* **Approach 1:** Multiple Scanning. Keep adding the smaller number to its running multiple until both multiples align. This takes $O(\max(a, b))$ in the worst case, which is computationally expensive for large numbers.
* **Optimized Approach:** GCD Reduction. Leverage the fundamental identity $a \cdot b = \text{gcd}(a, b) \cdot \text{lcm}(a, b)$ to calculate the LCM directly. We divide first and multiply second to prevent intermediate value overflow: `(a // gcd(a, b)) * b`.
* **Complexity:**
  * **Time:** $O(\log(\min(a, b)))$ because computing the GCD dominates the runtime.
  * **Space:** $O(1)$ auxiliary space.
* **Pointer Flow:**
```text
State tracing for lcm(12, 18):
1. Compute gcd(12, 18) -> 6
2. Divide one factor first: 12 // 6 = 2
3. Multiply by the other factor: 2 * 18 = 36
4. Return 36.
```
* **Pattern Recognition:**
  * Use GCD Reduction for LCM when:
    - Finding the synchronization time of multiple cyclical events (e.g., buses arriving at different intervals).
    - Finding the lowest common denominator for fraction addition.
* **Core Insight:** The prime factorization of $a \cdot b$ contains all prime factors of both numbers. The GCD contains the common prime factors in their minimum powers. By dividing the product of the two numbers by their GCD, we eliminate duplicate prime factors, leaving the exact prime factorization of the LCM.
* **Mistakes Made:** In languages with fixed-width integers, executing `(a * b) // gcd(a, b)` can cause an integer overflow during the multiplication `a * b` before the division by the GCD occurs. Always divide first: `(a // gcd(a, b)) * b`.
* **What I Learned:** Duality relationships in mathematics allow us to transform hard problems (finding multiples) into easier solved ones (finding divisors).

---

## Problem: Extended Euclidean Algorithm

* **Problem Type:** Diophantine Equations / Modular Inverse
* **Data Structure Used:** Scalar tuple states
* **Approach 1:** Brute force search. Try all combinations of $x$ and $y$ within a bounded range to satisfy $a \cdot x + b \cdot y = \text{gcd}(a, b)$. This is $O(N^2)$ and infeasible.
* **Optimized Approach:** Reverse Recursive Substitution. Unwind the Euclidean algorithm recursively, expressing the remainder at each step as a linear combination of the divisors, updating Bézout coefficients back up the call stack.
* **Complexity:**
  * **Time:** $O(\log(\min(a, b)))$
  * **Space:** $O(\log(\min(a, b)))$ stack frame space.
* **Pointer Flow:**
```text
Tracing ext_gcd(30, 20):
1. Call ext_gcd(30, 20) -> mod is 10. Calls ext_gcd(20, 10).
2. Call ext_gcd(20, 10) -> mod is 0. Calls ext_gcd(10, 0).
3. Base Case: ext_gcd(10, 0) returns (10, 1, 0) -> gcd=10, x1=1, y1=0.
4. Unwind 1: From ext_gcd(20, 10), we get g=10, x1=0, y1=1 from below.
             x = y1 - (20 // 10) * x1 = 1 - 2 * 0 = 1
             y = x1 = 0
             Returns (10, 1, 0)
5. Unwind 2: From ext_gcd(30, 20), we get g=10, x1=-1, y1=1 from below.
             x = y1 - (30 // 20) * x1 = 0 - 1 * 1 = -1
             y = x1 = 1
             Returns (10, -1, 1)
             Verification: 30 * (-1) + 20 * 1 = -10 != 10? Wait, let's look at the correct code:
             def ext_gcd(a, b):
                 if a == 0: return b, 0, 1
                 g, x1, y1 = ext_gcd(b % a, a)
                 return g, y1 - (b // a) * x1, x1
             Trace:
             ext_gcd(30, 20) -> calls ext_gcd(20, 30) because 20 % 30 is 20.
             ext_gcd(20, 30) -> calls ext_gcd(10, 20) because 30 % 20 is 10.
             ext_gcd(10, 20) -> calls ext_gcd(0, 10) because 20 % 10 is 0.
             ext_gcd(0, 10) -> base case, returns (10, 0, 1). So g=10, x1=0, y1=1.
             Unwind to ext_gcd(10, 20): a=10, b=20.
                 x = y1 - (20 // 10) * x1 = 1 - 2 * 0 = 1
                 y = x1 = 0
                 returns (10, 1, 0)
             Unwind to ext_gcd(20, 30): a=20, b=30. g=10, x1=1, y1=0.
                 x = y1 - (30 // 20) * x1 = 0 - 1 * 1 = -1
                 y = x1 = 1
                 returns (10, -1, 1)
             Unwind to ext_gcd(30, 20): a=30, b=20. g=10, x1=-1, y1=1.
                 x = y1 - (20 // 30) * x1 = 1 - 0 * (-1) = 1
                 y = x1 = -1
                 returns (10, 1, -1)
             Verification: 30 * 1 + 20 * (-1) = 10. Perfect!
```
* **Pattern Recognition:**
  * Use Extended GCD when:
    - Finding the Modular Multiplicative Inverse (needed when dividing under a modulo, i.e., $(a / b) \bmod m$).
    - Solving linear Diophantine equations of the form $a \cdot x + b \cdot y = c$.
* **Core Insight:** If we express $\text{gcd}(b \bmod a, a)$ as a linear combination:
$(b \bmod a) \cdot x_1 + a \cdot y_1 = g$
Since $b \bmod a = b - \lfloor b / a \rfloor \cdot a$, substituting this in gives:
$(b - \lfloor b / a \rfloor \cdot a) \cdot x_1 + a \cdot y_1 = g$
$a \cdot (y_1 - \lfloor b / a \rfloor \cdot x_1) + b \cdot x_1 = g$
This shows the new coefficients are $x = y_1 - \lfloor b / a \rfloor \cdot x_1$ and $y = x_1$.
* **Mistakes Made:** Forgetting that Bézout's coefficients can be negative. When computing the modular inverse, a negative coefficient must be converted to a positive equivalent under the modulo: `(x % m + m) % m`.
* **What I Learned:** Unwinding recursion provides algebraic solutions. Backtracking through division remainders allows us to compute coefficients that are otherwise hidden.

---

### Master Patterns Learned

#### 1. The Euclidean Reduction Frame
* **The Strategy:** Continuously replace the larger value with the remainder of the two values until the remainder reaches 0. This reduces state spaces logarithmically.
* **Code Pattern:**
```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
```

#### 2. Bézout's Coefficient Unwinding
* **The Strategy:** Use recursive mathematical induction to calculate linear combinations back up the recursion stack.
* **Code Pattern:**
```python
def ext_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = ext_gcd(b % a, a)
    return g, y1 - (b // a) * x1, x1
```
