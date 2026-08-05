# Bitwise Math

## 1. Simulating Arithmetic with Bits

At the silicon level, CPUs do not possess magical "addition" circuits that know how to carry numbers like we do on paper. They use **Adders** constructed purely out of logic gates: XOR, AND, and OR gates.

When you are asked to add two numbers without using `+` or `-`, you are being asked to implement a Half-Adder and Full-Adder in software.

Addition can be broken down into two components:
1.  **The Base Sum (Without Carry):**
    If we add `0+0`, we get `0`.
    If we add `1+0`, we get `1`.
    If we add `0+1`, we get `1`.
    If we add `1+1`, we get `0` (and we carry a 1, which we ignore for a moment).
    Notice this truth table? It is EXACTLY the XOR operation! `a ^ b` represents addition where we ignore the carries.
2.  **The Carry:**
    A carry ONLY happens when both bits are `1`. The bitwise operation that perfectly isolates this is AND (`a & b`).
    However, a carry affects the *next* most significant bit, not the current one. Therefore, we must shift the carry left by 1: `(a & b) << 1`.

By repeatedly adding the "Base Sum" and the "Carry" together until the Carry becomes `0`, we successfully simulate hardware addition!

---

## 2. The Python 32-bit Problem

In Java, C++, or C, integers are exactly 32 bits wide. If an addition overflows the 32nd bit, it is silently dropped into the void, natively giving the correct negative number (Two's Complement).

Python, however, has **arbitrary-precision integers**. If you shift a bit past the 32nd slot, Python just makes a 33rd slot, and a 34th... creating an infinitely long number!
Because of this, we must manually force 32-bit behavior by masking.

*   `mask = 0xFFFFFFFF` (32 ones). We AND this with our variables on every step to instantly chop off any bits that exceed 32.
*   `max_int = 0x7FFFFFFF`. This is the maximum positive 32-bit integer. If our final answer exceeds this, it means the 32nd bit (the sign bit) is a `1`, so it's supposed to be a negative number.
*   To convert this weird pseudo-32-bit positive integer back into a true Python negative integer, we use `~(a ^ mask)`.

---

## 3. Range Bitwise AND

If you are asked to compute the bitwise AND of every number between `L` and `R` (inclusive), doing it with a loop will result in a Time Limit Exceeded (TLE) error if the range spans billions of numbers.

Instead of looking at the loop, look at the geometry of the bits.
Consider the range `[9, 12]`:
`9  = 1001`
`10 = 1010`
`11 = 1011`
`12 = 1100`

If you bitwise AND them all together, what survives?
For a bit to survive, it must be `1` in EVERY SINGLE NUMBER in that range.
Because numbers count up sequentially, the lowest bits flip constantly (`0, 1, 0, 1...`). They will never survive the AND process because a single `0` annihilates the column.

The ONLY part of the numbers that will survive is the **Common Prefix** — the high-order bits that are identical across all numbers in the range. The moment `L` and `R` differ in a column, every column to the right of it is guaranteed to have at least one `0` somewhere in the range sequence.

So, the algorithm to find the range AND is beautifully simple:
1. Shift both `L` and `R` to the right by 1 until `L == R`. This chops off the differing suffixes, leaving only the common prefix!
2. Track how many times you shifted (let's call it `shifts`).
3. Take that common prefix, and shift it left by `shifts` to restore its original magnitude, filling the destroyed suffix with `0`s.

---

## Master Templates

```python
# 1. Hardware Addition Simulation (Python Version)
def get_sum(a: int, b: int) -> int:
    mask = 0xFFFFFFFF
    while b:
        # Carry is where both are 1, shifted left
        carry = ((a & b) << 1) & mask
        # Sum is XOR
        a = (a ^ b) & mask
        b = carry
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)

# 2. Range Common Prefix Extraction
def range_bitwise_and(left: int, right: int) -> int:
    shifts = 0
    while left < right:
        left >>= 1
        right >>= 1
        shifts += 1
    return left << shifts
```

---

## Problem: Sum of Two Integers

* **Interview Difficulty:** Medium
* **Problem Type:** Arithmetic Simulation
* **Data Structure Used:** Two Scalars (`carry` and `sum`)
* **Optimized Approach:** Loop while the `carry` (stored in `b`) is not 0. Calculate `carry = (a & b) << 1`. Calculate `sum_without_carry = a ^ b`. Assign the sum to `a` and the carry to `b`. Apply `& 0xFFFFFFFF` to both on every step to prevent Python's integers from growing infinitely. Once the loop ends, cast the 32-bit masked number back to a native Python signed integer.
* **Complexity:**
  * **Time:** $O(1)$ (The loop runs at most 32 times).
  * **Space:** $O(1)$
* **Pointer Flow:**
```text
a = 1 (0001), b = 2 (0010)

iter 1:
carry = (0001 & 0010) << 1 = 0000
a = (0001 ^ 0010) = 0011 (3)
b = 0000 (0)

b == 0. Loop ends. Return a (3).
```
* **Pattern Recognition:**
  * Constraints strictly forbid `+` and `-`.
* **Core Insight:** `XOR` is addition without carry. `AND << 1` isolates the carry. By repeatedly adding the carry back into the sum, we ripple the bit changes up the chain until no carries remain.

---

## Problem: Bitwise AND of Numbers Range

* **Interview Difficulty:** Medium
* **Problem Type:** Common Prefix Extraction
* **Data Structure Used:** Two Scalars
* **Approach 1:** `for i in range(left, right+1): ans &= i`. Guaranteed TLE for large ranges. Time: $O(R - L)$.
* **Optimized Approach:** Shift both `left` and `right` rightward simultaneously (`left >>= 1`, `right >>= 1`) until they are equal. Keep a counter of the shifts. Once equal, shift `left` back to the left by the counter to pad it with zeros.
* **Complexity:**
  * **Time:** $O(1)$ (Maximum 32 shifts).
  * **Space:** $O(1)$
* **Pointer Flow:**
```text
left = 5 (0101), right = 7 (0111)

iter 1 (shift 1): left = 2 (010), right = 3 (011)
iter 2 (shift 2): left = 1 (01), right = 1 (01)

left == right! We stop.
Return 1 << 2 = 4 (0100).
```
* **Pattern Recognition:**
  * Bulk operations across a massive contiguous sequential range of numbers.
* **Core Insight:** In a sequential range, the right-side bits flip incredibly fast. The only bits that remain constant (and thus survive an AND cascade) are the high-order bits that are identical in BOTH the starting and ending number. Finding the common prefix is the true objective.
