## Problem: Guess Number Higher or Lower

* Brute force: Scanning sequentially through every number from 1 up to n using a linear approach, querying the API for each number until the target picked value is successfully hit.
```python
def guess_number_brute(n):
    for i in range(1, n + 1):
        if guess(i) == 0:
            return i
    return -1
```
* Optimized: Running an iterative binary search across the search space [1, n], invoking the API on the midpoint during each iteration to instantly eliminate half of the remaining choices.
```python
def guess_number(n: int) -> int:
    low = 1
    high = n
    while low <= high:
        mid = (low + high) // 2
        res = guess(mid)
        
        if res == 0:
            return mid
        elif res == -1:
            high = mid - 1
        else:
            low = mid + 1 
    return -1
```
* Data structure used: None; handled exclusively using primitive index tracking boundary variables (`low`, `high`, `mid`).
* Complexity:
  * Brute Force: Time $O(n)$ proportional to sequential element lookups; Space $O(1)$ constant overhead memory.
  * Optimized: Time $O(\log n)$ because the remaining guess pool decreases by exactly half at every execution step; Space $O(1)$ constant auxiliary footprint.
* Pattern Recognition:
  * Use binary search when:
    - The search space is ordered, and each query gives directional feedback that eliminates one half of the remaining space.
    - An oracle API or condition tells you precisely which direction to search next (1 or -1).
* Core Insight:
  Instead of playing a guessing game linearly, the problem space is a classic ordered sequence where an API call acts as an absolute directional compass, allowing you to slice the problem size in half repeatedly.
* Mistakes made: Initial conceptual difficulty was mapping out the API's return outputs accurately since a return value of -1 indicates the target is lower, which requires decreasing the upper bound (`high = mid - 1`), while a return value of 1 requires shifting the lower bound up (`low = mid + 1`). 
* What I learned: Mapping external API directional keys onto binary search boundaries requires careful synchronization. Ensuring that the boundary condition `low <= high` runs through the full range prevents the algorithm from terminating prematurely right before uncovering the target pick value.

---

## Problem: First Bad Version

* Brute force: Querying the boolean `isBadVersion` API sequentially for every version starting from 1 up to n until the very first True status response is recorded.
```python
def firstBadVersion_brute(n):
    for i in range(1, n + 1):
        if isBadVersion(i):
            return i
    return n
```
* Optimized: Using a binary search variant where the bounds shrink inward continuously, maintaining a trailing lower pointer alignment that halts directly on the first instance of a failed status.
```python
def firstBadVersion(n: int) -> int:
    low = 1
    high = n
    while low < high:
        mid = low + (high - low) // 2
        if isBadVersion(mid):
            high = mid 
        else:
            low = mid + 1 
    return low
```
* Data structure used: Linear range boundary integers (`int`) for optimization paths.
* Complexity:
  * Brute Force: Time $O(n)$ via potential full iteration sweeps; Space $O(1)$ constant memory allocation.
  * Optimized: Time $O(\log n)$ through logarithmic truncation of versions; Space $O(1)$ auxiliary constant space.
* Pattern Recognition:
  * Use binary search boundary convergence when:
    - You are searching for a transition point or pivot in a binary sequence (e.g., False, False, True, True).
    - The target condition does not provide an instant "exact match" exit criterion.
* Core Insight:
  A history of app deployment versions splits perfectly into two distinct global halves: a block of entirely clean builds followed by a block of entirely broken builds which forms a monotonic boolean sequence, once True appears everything after it is also True. Identifying the structural transition boundary is achieved by dynamically shrinking the `high` boundary down to include the current bad midpoint version, rather than skipping past it entirely.
* Mistakes made: The primary cognitive hurdle was determining the exact loop condition and pointer adjustment mechanics. Using a traditional `low <= high` loop combined with `high = mid - 1` when a bad version is found can cause the upper pointer to accidentally skip past the very first bad version entirely. Shifting the structure to a strict convergence style (`low < high`) and anchoring `high = mid` preserves the current valid candidate safely.
* What I learned: When searching for the absolute beginning of a contiguous segment, you should avoid using an internal exact-match exit condition. Instead, let the loop narrow down the options until `low == high`. Also, calculating the midpoint as `low + (high - low) // 2` is a vital habit to protect your code against integer overflow errors in languages with fixed-size integers.

---

## Problem: Sqrt(x)

* Brute force: Multiplying every sequential integer by itself starting from 1 upwards (1 * 1, 2 * 2, 3 * 3, etc.) until the product exceeds the target value x, returning the preceding integer index.
```python
def mySqrt_brute(x):
    if x < 2: return x
    i = 1
    while i * i <= x:
        i += 1
    return i - 1
```
* Optimized: Executing binary search across the numerical search space from 1 up to x // 2, maintaining a tracking variable `ans` that logs the closest valid downward square integer boundary encountered on the fly.
```python
def mySqrt(x):
    if x < 2:
        return x 
    low = 1
    high = x // 2  
    ans = 0
    while low <= high:
        mid = low + (high - low) // 2
        num = mid * mid
        if num == x:
            return mid
        elif num < x:
            ans = mid      
            low = mid + 1  
        else:
            high = mid - 1             
    return ans
```
* Data structure used: None; numerical scalar trackers (`int`) are used exclusively.
* Complexity:
  * Brute Force: Time $O(\sqrt{x})$ since the loop increments one integer at a time up to the square root boundary; Space $O(1)$.
  * Optimized: Time $O(\log x)$ as the numerical search spectrum drops exponentially by half; Space $O(1)$ constant execution environment memory.
* Pattern Recognition:
  * Use binary search on value range (Binary Search on Answer) when:
    - You are searching for a specific integer inside a fixed mathematical range.
    - The target function is monotonic (as N increases, N * N increases steadily).
* Core Insight:
  The mathematical square root of an integer greater than 4 will never exceed its split quotient (x // 2). This mathematical property limits the search domain immediately, allowing the square root to be located cleanly using binary search within that range.
* Mistakes made: Initial difficulty was handling non-perfect squares (like 8, which must round down to return 2). The logical bottleneck was figuring out how to remember the largest valid perfect square candidate found so far before shifting the lower bound upward. I solved this by introducing a tracking variable `ans = mid` that caches the last successful configuration whenever `mid * mid < x`.
* What I learned: Binary search can be used for things beyond finding elements in an array; it can also look for a valid integer value across a numerical range. Handling edge cases early (x < 2) avoids creating an empty search range and directly returns mathematically trivial answers.