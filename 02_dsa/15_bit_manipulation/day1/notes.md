# Bitwise Fundamentals & XOR Properties

## 1. What is Bit Manipulation?

At the lowest level, computers store integers as a sequence of bits (0s and 1s). Bit manipulation allows you to operate directly on these individual bits. 
While high-level math like addition or modulo handles the numerical value, bitwise operations manipulate the binary structure itself. This leads to algorithms that are incredibly fast ($O(1)$ operations) and require minimal memory.

The core operators you must master are:
*   `&` (AND): 1 if both bits are 1, else 0.
*   `|` (OR): 1 if either bit is 1, else 0.
*   `^` (XOR): 1 if bits are DIFFERENT, 0 if they are the same.
*   `~` (NOT): Flips every bit (0 becomes 1, 1 becomes 0).
*   `<<` (Left Shift): Shifts bits left, filling with 0s. Mathematically, `x << 1` is $x \times 2$.
*   `>>` (Right Shift): Shifts bits right. Mathematically, `x >> 1` is $x \div 2$.

---

## 2. The Magic of XOR

XOR (Exclusive OR) is arguably the most powerful bitwise operator for technical interviews. It is defined as: "true if exactly one is true."
In binary:
`0 ^ 0 = 0`
`1 ^ 1 = 0`
`1 ^ 0 = 1`
`0 ^ 1 = 1`

XOR has three magical properties that form the foundation of many algorithms:
1.  **Identity:** `a ^ 0 = a` (Any number XORed with 0 remains unchanged).
2.  **Self-Inverse (Cancellation):** `a ^ a = 0` (Any number XORed with itself cancels out to 0).
3.  **Commutative & Associative:** `a ^ b ^ c = c ^ a ^ b`. (The order in which you XOR numbers doesn't matter).

Because of these properties, if you XOR a list of numbers where every number appears twice except for one, the duplicates will cancel each other out to `0`, leaving only `0 ^ single_number = single_number`. You don't need a Hash Map to find it!

---

## 3. Brian Kernighan's Algorithm: `n & (n - 1)`

How do you count the number of `1` bits in an integer?
A naive approach shifts the number to the right and checks the last bit (`n & 1`) 32 times.

A brilliant optimized approach is **Brian Kernighan's Algorithm**.
The core observation is what happens when you subtract 1 from a binary number:
`n     = 10110000`
`n - 1 = 10101111`
Subtracting 1 always flips the rightmost `1` to `0`, and flips all the `0`s to its right to `1`s.

If you then bitwise AND them:
`n & (n - 1) = 10110000 & 10101111 = 10100000`

The result is the exact same number `n`, but with its **lowest set bit erased**.
Instead of looping 32 times, this algorithm only loops exactly as many times as there are `1`s in the number!

---

## 4. DP and Bitwise Shifts

Bitwise operations heavily intersect with Dynamic Programming. Because shifting a number right (`>> 1`) divides it by 2, the bit representation of `n` is inherently tied to the bit representation of `n // 2`.

If you know the number of set bits in `x`, how many set bits are in `x * 2`? 
Exactly the same! Multiplying by 2 just adds a `0` to the right end (`101` becomes `1010`).
Therefore, `bits(i) = bits(i >> 1)`.

But what if `i` is odd? Then the rightmost bit is a `1`. 
So the universal DP relation for counting bits is:
`bits(i) = bits(i >> 1) + (i & 1)`

---

## 5. Master Templates

```python
# 1. XOR Cancellation Sweep
def find_single_element(nums: list[int]) -> int:
    res = 0
    for n in nums:
        res ^= n  # Duplicates cancel to 0
    return res

# 2. Dropping the lowest set bit
def count_set_bits(n: int) -> int:
    count = 0
    while n:
        n &= (n - 1) # Drops the lowest 1
        count += 1
    return count
```

---

## Problem: Single Number

* **Interview Difficulty:** Easy
* **Problem Type:** XOR Cancellation
* **Data Structure Used:** Scalar `res`
* **Approach 1:** Hash Map. Count frequencies, then iterate to find the one with count 1. Time: $O(N)$, Space: $O(N)$.
* **Optimized Approach:** XOR every number together. Due to commutativity and the self-inverse property, `a ^ b ^ a = b`. All pairs cancel to 0, leaving only the unique number.
* **Complexity:**
  * **Time:** $O(N)$
  * **Space:** $O(1)$
* **Pointer Flow:**
```text
nums = [4, 1, 2, 1, 2]
res = 0
n=4: res = 0 ^ 4 = 4
n=1: res = 4 ^ 1 = 5
n=2: res = 5 ^ 2 = 7
n=1: res = 7 ^ 1 = 6  (which is 4 ^ 2)
n=2: res = 6 ^ 2 = 4  (pairs canceled out!)
```
* **Pattern Recognition:**
  * Spot "every element appears exactly twice except one" constraints.
* **Core Insight:** XOR is a reversible accumulator. It "stores" the presence of a number without taking up space, and "erases" it when it sees it again.

---

## Problem: Missing Number

* **Interview Difficulty:** Easy
* **Problem Type:** Multi-Sequence XOR Cancellation
* **Data Structure Used:** Scalar `res`
* **Approach 1:** Gauss Sum Formula. Sum of `0..n` is `n*(n+1)//2`. Subtract the sum of the array from this expected sum to find the missing number. While $O(N)$ time and $O(1)$ space, summing can cause integer overflow in languages like C++/Java (though Python handles arbitrarily large integers).
* **Optimized Approach:** Use XOR. We know the array *should* contain all numbers from `0` to `n`. We initialize `res = n`. As we loop `i` from `0` to `n-1`, we XOR `res` with the expected index `i` AND the actual value `nums[i]`. Every number that is present will be XORed twice (once as an index, once as a value) and cancel out. The missing number will only be XORed once (as an index) and remain in `res`.
* **Complexity:**
  * **Time:** $O(N)$
  * **Space:** $O(1)$
* **Pointer Flow:**
```text
nums = [3, 0, 1]  (n=3, expecting [0, 1, 2, 3])
res = 3
i=0: res = 3 ^ 0 ^ nums[0](3) = 0
i=1: res = 0 ^ 1 ^ nums[1](0) = 1
i=2: res = 1 ^ 2 ^ nums[2](1) = 2
Return res = 2.
```
* **Pattern Recognition:**
  * Comparing an observed sequence to a perfectly complete expected sequence.
* **Core Insight:** You can construct the "expected" sequence on the fly using loop indices, folding both the expected universe and the actual universe into a single XOR chain.

---

## Problem: Number of 1 Bits (Hamming Weight)

* **Interview Difficulty:** Easy
* **Problem Type:** Bit Masking / Brian Kernighan's
* **Data Structure Used:** Scalar
* **Approach 1:** Loop 32 times. Check `n & 1`, then `n >>= 1`. Time: $O(32) = O(1)$.
* **Optimized Approach:** Brian Kernighan's trick: `n &= (n - 1)`. This definitively zeroes out the least significant `1` bit in a single CPU cycle. Increment a counter until `n` becomes 0.
* **Complexity:**
  * **Time:** $O(K)$ where $K$ is the number of set bits (1s).
  * **Space:** $O(1)$
* **Pointer Flow:**
```text
n = 11 (binary 1011)
count = 0
iter 1: n = 1011 & 1010 = 1010 (10). count = 1.
iter 2: n = 1010 & 1001 = 1000 (8).  count = 2.
iter 3: n = 1000 & 0111 = 0000 (0).  count = 3.
Return 3.
```
* **Pattern Recognition:**
  * Needs to count, isolate, or erase the lowest set bit.
* **Core Insight:** `n - 1` borrows from the lowest `1` bit, turning it to `0` and flipping all trailing `0`s to `1`s. ANDing it with the original `n` wipes the borrowed trail clean.

---

## Problem: Counting Bits

* **Interview Difficulty:** Easy
* **Problem Type:** Bitwise DP
* **Data Structure Used:** Array
* **Approach 1:** Call `hammingWeight(i)` for every number from `0` to `n`. Time: $O(N \log N)$ or $O(N \cdot K)$.
* **Optimized Approach:** Use Dynamic Programming. The number of 1s in `i` is identical to the number of 1s in `i // 2`, plus 1 if `i` is odd. In bitwise terms: `dp[i] = dp[i >> 1] + (i & 1)`.
* **Complexity:**
  * **Time:** $O(N)$
  * **Space:** $O(N)$ for the result array.
* **Pointer Flow:**
```text
n = 5. dp = [0, 0, 0, 0, 0, 0]
i=1: dp[1] = dp[0] + (1&1) = 0 + 1 = 1
i=2: dp[2] = dp[1] + (2&1) = 1 + 0 = 1
i=3: dp[3] = dp[1] + (3&1) = 1 + 1 = 2
i=4: dp[4] = dp[2] + (4&1) = 1 + 0 = 1
i=5: dp[5] = dp[2] + (5&1) = 1 + 1 = 2
```
* **Pattern Recognition:**
  * Generating sequences based on bit properties.
* **Core Insight:** Shifting right destroys exactly one piece of information: the lowest bit. Since we know what that bit was (via `i & 1`), we can reconstruct the total count from a previously computed state.
