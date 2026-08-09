## Problem: Sieve of Eratosthenes

* **Problem Type:** Prime Number Generation / Composite Elimination
* **Data Structure Used:** Boolean state array (lookup table)
* **Approach 1:** Linear Primality Scan. For every number $x$ from $2$ to $n$, test if $x$ is prime by iterating $d$ from $2$ to $\sqrt{x}$ and checking if $x \bmod d == 0$. This naive check takes $O(N \sqrt{N})$ time, which is highly inefficient for generating primes up to $10^6$ or larger.
* **Optimized Approach:** Sieve of Eratosthenes. Maintain a boolean array `is_prime` initialized to `True`. Starting at $2$, when we find a prime, we greedily mark all of its multiples starting from $i^2$ up to $n$ as `False` (composite). By skipping already marked numbers, we avoid redundant calculations.
* **Complexity:**
  * **Time:** $O(N \log \log N)$ time. The sum of the reciprocals of prime numbers up to $n$ is $O(\log \log N)$, leading to near-linear complexity.
  * **Space:** $O(N)$ space complexity to store the state array of size $n+1$.
* **Pointer Flow:**
```text
Sieve simulation up to n = 10:
1. Initialize: is_p = [F, F, T, T, T, T, T, T, T, T, T] (indices 0..10)
2. i = 2: is_p[2] is True. Prime! Mark multiples starting from 2*2 = 4:
         is_p[4] = F
         is_p[6] = F
         is_p[8] = F
         is_p[10] = F
3. i = 3: is_p[3] is True. Prime! Mark multiples starting from 3*3 = 9:
         is_p[9] = F
4. i = 4: 4 > sqrt(10) (which is 3.16). Loop terminates.
5. Filter indices with True flags: [2, 3, 5, 7]
```
* **Pattern Recognition:**
  * Use the Sieve of Eratosthenes when:
    - You need to query the primality of multiple numbers in the range $[1, N]$ repeatedly (precompute once, query in $O(1)$).
    - Finding all prime numbers below a given limit.
* **Core Insight:** Instead of checking each number for factors (division-based search), we push the factors forward onto their multiples (multiplication-based exclusion). This replaces expensive division operations with cheap array writes.
* **Mistakes Made:** A common optimization mistake is starting the inner loop of multiples at $2 \cdot i$. However, any multiple $k \cdot i$ where $k < i$ must have a prime factor smaller than $i$. Therefore, that multiple has already been marked as composite by that smaller prime factor. Starting the inner loop at $i^2$ eliminates these redundant operations.
* **What I Learned:** Marking composites from $i^2$ forward turns division-heavy primality scans into a fast, addition-based elimination grid.

---

## Problem: Prime Factorization (Trial Division)

* **Problem Type:** Integer Factorization / Prime Decompositions
* **Data Structure Used:** List to store prime factors
* **Approach 1:** Complete division scan. Iterate $d$ from $2$ to $n-1$, dividing $n$ by $d$ whenever possible. This takes $O(n)$ time in the worst case (when $n$ is prime), which times out for large integers.
* **Optimized Approach:** $\sqrt{N}$ Trial Division. Maintain a divisor $d$ starting at $2$. While $d^2 \le n$, repeatedly divide $n$ by $d$ and record $d$ as a factor until $n \bmod d \neq 0$. Then increment $d$. Once the loop terminates, if the remaining $n > 1$, it must be prime — append it to the factors.
* **Complexity:**
  * **Time:** $O(\sqrt{N})$ in the worst case (when $n$ is prime, or a product of two large primes). If $n$ has small prime factors, it shrinks rapidly, running much faster than $\sqrt{N}$ in practice.
  * **Space:** $O(\log N)$ auxiliary space to store the prime factors (since $n$ can have at most $\log_2 N$ factors).
* **Pointer Flow:**
```text
Decomposing n = 36:
1. Initialize: res = [], d = 2
2. d = 2: 2*2 <= 36. 36 % 2 == 0 -> divide. res = [2], n = 18.
         18 % 2 == 0 -> divide. res = [2, 2], n = 9.
         9 % 2 != 0 -> stop division. Increment d to 3.
3. d = 3: 3*3 <= 9. 9 % 3 == 0 -> divide. res = [2, 2, 3], n = 3.
         3 % 3 == 0 -> divide. res = [2, 2, 3, 3], n = 1.
         1 % 3 != 0 -> stop division. Increment d to 4.
4. d = 4: 4*4 (16) > 1. Loop terminates.
5. n is 1 (not > 1). Return res = [2, 2, 3, 3].
```
* **Pattern Recognition:**
  * Use $\sqrt{N}$ Trial Division when:
    - Finding the prime factors of a single large integer.
    - Determining the number of unique prime factors or calculating Euler's totient function.
* **Core Insight:** If a composite number $N$ is decomposed into two factors $a \cdot b = N$, then at least one factor must be $\le \sqrt{N}$. If we check all divisors up to $\sqrt{N}$ and find none, the remaining number must be prime.
* **Mistakes Made:** Forgetting to handle the remaining $n$ after the loop terminates. If $n$ has a prime factor larger than $\sqrt{n}$ (such as 14, where the factors are 2 and 7, and $7 > \sqrt{14} \approx 3.74$), the loop ends at $d=2$ with $n=7$. If we don't check `if n > 1` post-loop, the factor 7 is lost.
* **What I Learned:** Decomposing numbers dynamically reduces the search boundary. Every division by a factor lowers the ceiling for the remaining search.

---

### Master Patterns Learned

#### 1. The Sieve Elimination Frame
* **The Strategy:** Use a lookup table to mark multiples of identified primes, starting from $i^2$ to eliminate redundant checks.
* **Code Pattern:**
```python
def sieve(n):
    is_p = [True] * (n + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_p[i]:
            for j in range(i * i, n + 1, i):
                is_p[j] = False
    return [i for i, p in enumerate(is_p) if p]
```

#### 2. The $\sqrt{N}$ Trial Division Frame
* **The Strategy:** Test divisors up to the square root of the running value of $N$, dividing it down dynamically to shrink the search space.
* **Code Pattern:**
```python
def factorize(n):
    res = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            res.append(d)
            n //= d
        d += 1
    if n > 1:
        res.append(n)
    return res
```
