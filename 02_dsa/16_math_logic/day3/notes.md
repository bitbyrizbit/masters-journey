## Problem: Fast Power (Binary Exponentiation)

* **Problem Type:** Logarithmic Power Calculation / State Doubling
* **Data Structure Used:** Scalar numeric variables
* **Approach 1:** Linear multiplication. Multiply the base $x$ by itself $n$ times: `for _ in range(n): res *= x`. This takes $O(n)$ time, which times out when the exponent $n$ reaches $10^9$ or larger.
* **Optimized Approach:** Binary Exponentiation. Decompose the exponent $n$ into its binary representation. We maintain a running squared base `cur` ($x, x^2, x^4, x^8...$). If the current bit of $n$ is `1` (`n & 1`), we multiply the result by `cur`. We shift $n$ right (`n >>= 1`) and square `cur` on every step.
* **Complexity:**
  * **Time:** $O(\log n)$ time because the exponent is halved at each step.
  * **Space:** $O(1)$ auxiliary space for the iterative approach.
* **Pointer Flow:**
```text
Computing my_pow(2, 10):
1. Initialize: res = 1, cur = 2, n = 10 (binary 1010)
2. Step 1: n = 10 (even, lowest bit 0) -> no multiply.
           cur = 2 * 2 = 4
           n = 10 >> 1 = 5 (binary 0101)
3. Step 2: n = 5 (odd, lowest bit 1) -> multiply.
           res = 1 * 4 = 4
           cur = 4 * 4 = 16
           n = 5 >> 1 = 2 (binary 0010)
4. Step 3: n = 2 (even, lowest bit 0) -> no multiply.
           cur = 16 * 16 = 256
           n = 2 >> 1 = 1 (binary 0001)
5. Step 4: n = 1 (odd, lowest bit 1) -> multiply.
           res = 4 * 256 = 1024
           cur = 256 * 256 = 65536
           n = 1 >> 1 = 0
6. n is 0. Loop terminates. Return res = 1024.
```
* **Pattern Recognition:**
  * Use Binary Exponentiation when:
    - The problem requires calculating $x^n$ where $n$ can be extremely large.
    - Solving linear recurrences via Matrix Exponentiation.
* **Core Insight:** We exploit the mathematical identity $x^{a + b} = x^a \cdot x^b$. By representing the exponent $n$ as a sum of powers of 2 (e.g. $10 = 8 + 2$), we can calculate $x^{10}$ as $x^8 \cdot x^2$. We only need $\log_2 n$ multiplications to generate all the power-of-2 bases.
* **Mistakes Made:** Forgetting to handle negative exponents. If $n < 0$, we must invert the base `x = 1 / x` and make the exponent positive `n = -n` before entering the loop. In languages with fixed-width integers, changing `n = -n` when `n = -2^31` can cause an integer overflow.
* **What I Learned:** Exponentiation can be mapped to binary search-like division. Decomposing the exponent into powers of 2 turns a linear series of operations into a logarithmic tree.

---

## Problem: Modular Exponentiation

* **Problem Type:** Bounded Power Calculation / Modulo Arithmetic
* **Data Structure Used:** Scalar numeric variables
* **Approach 1:** Calculate the full power $b^e$ using binary exponentiation, and then apply the modulo: `(b ** e) % m`. While the binary exponentiation is fast, the intermediate value $b^e$ can grow to millions of digits, consuming massive memory and slowing down arithmetic operations.
* **Optimized Approach:** Modulo-Injected Binary Exponentiation. Apply the modulo operator to the base initially, and wrap every multiplication step inside the binary exponentiation loop with a modulo operation. This ensures all intermediate values remain strictly bounded.
* **Complexity:**
  * **Time:** $O(\log e)$ time.
  * **Space:** $O(1)$ auxiliary space.
* **Pointer Flow:**
```text
Computing mod_pow(3, 5, 7):
1. Initialize: res = 1, b = 3 % 7 = 3, e = 5 (binary 101)
2. Step 1: e = 5 (odd, lowest bit 1) -> multiply and mod.
           res = (1 * 3) % 7 = 3
           b = (3 * 3) % 7 = 2
           e = 5 >> 1 = 2 (binary 010)
3. Step 2: e = 2 (even, lowest bit 0) -> no multiply.
           b = (2 * 2) % 7 = 4
           e = 2 >> 1 = 1 (binary 001)
4. Step 3: e = 1 (odd, lowest bit 1) -> multiply and mod.
           res = (3 * 4) % 7 = 5
           b = (4 * 4) % 7 = 2
           e = 1 >> 1 = 0
5. e is 0. Loop terminates. Return res = 5.
```
* **Pattern Recognition:**
  * Use Modular Exponentiation when:
    - Solving problems that require calculating $b^e \bmod m$ where $e$ is extremely large.
    - Implementing cryptographic algorithms (like RSA) or hashing functions.
* **Core Insight:** The multiplicative property of modulo states that $(x \cdot y) \bmod m = ((x \bmod m) \cdot (y \bmod m)) \bmod m$. This allows us to apply the modulo operation at each intermediate step, preventing the numbers from growing large while preserving the correct mathematical result.
* **Mistakes Made:** A common error is not handling the case where `m = 1`. Any number modulo 1 is 0. If `m = 1`, the code should return `0` immediately to prevent division-by-zero or incorrect outputs.
* **What I Learned:** Modulo arithmetic scales down computation. By injecting mod into every step, we keep the numbers small and the operations fast without changing the final result.

---

### Master Patterns Learned

#### 1. The Binary Exponentiation Frame
* **The Strategy:** Iterate through the binary representation of the exponent from right to left, squaring the active base on every step and accumulating it into the result whenever a set bit is detected.
* **Code Pattern:**
```python
def my_pow(x, n):
    if n < 0:
        x = 1 / x
        n = -n
    res = 1
    cur = x
    while n > 0:
        if n & 1:
            res *= cur
        cur *= cur
        n >>= 1
    return res
```

#### 2. The Modulo-Injected Multiplication Frame
* **The Strategy:** Bind all intermediate products to a modular range by applying the mod operator to the base initially and after every single multiplication step.
* **Code Pattern:**
```python
def mod_pow(b, e, m):
    if m == 1:
        return 0
    res = 1
    b = b % m
    while e > 0:
        if e & 1:
            res = (res * b) % m
        b = (b * b) % m
        e >>= 1
    return res
```
