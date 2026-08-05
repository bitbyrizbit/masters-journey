# Shifting & Bit Masks

## 1. Bit Shifting: The Geometric Movement

Bit shifting is literally moving the binary bits left or right within their memory slots. 

**Left Shift (`<<`):** 
Shifting left by $k$ places adds $k$ zeros to the right. 
Mathematically, `n << k` is exactly equal to $n \times 2^k$.
`1 << 3` = `0001` becomes `1000` (which is $8$, or $1 \times 2^3$).

**Right Shift (`>>`):** 
Shifting right by $k$ places removes $k$ bits from the right.
Mathematically, `n >> k` is exactly equal to integer division $n \div 2^k$.
`10 >> 1` = `1010` becomes `0101` (which is $5$).

### The Coordinate System of Bits
Think of a 32-bit integer as an array of length 32, indexed from right to left (index 0 is the least significant bit, index 31 is the most significant bit). 
If you want to construct an integer with a `1` exclusively at index `i`, you simply write `1 << i`. 

---

## 2. Bit Masking: Isolation and Inspection

A "mask" is a specially crafted binary sequence used in conjunction with a bitwise operator to extract, modify, or erase specific bits in a target number.

**1. Checking if the $i$-th bit is set:**
Create a mask with a 1 at index $i$: `mask = 1 << i`.
AND it with the number: `n & mask`.
If the result is non-zero, the bit was 1. If 0, the bit was 0.

**2. Setting the $i$-th bit to 1:**
Create a mask with a 1 at index $i$: `mask = 1 << i`.
OR it with the number: `n | mask`.
The OR operator forces the bit to 1, leaving all other bits completely unchanged.

**3. Isolating a single bit at position 0:**
Sometimes we don't want to move a mask to the bit; we want to move the bit to the mask!
Shift the number right by $i$ places: `n >> i`. This puts the bit we want at index 0.
AND it with 1: `(n >> i) & 1`. 
This wipes out everything except that specific bit, yielding exactly `1` or `0`.

---

## 3. Detecting Powers of Two

A number is a power of 2 ($2, 4, 8, 16...$) if and only if it has **exactly one bit set to 1** in its entire binary representation.
`2 = 0010`
`4 = 0100`
`8 = 1000`

How do we check if a number has exactly one 1 bit? We use Brian Kernighan's trick from Day 1!
`n & (n - 1)` drops the lowest set bit.
If the number had exactly one bit, dropping it makes the number exactly `0`.
Therefore, the definitive $O(1)$ check for a power of 2 is:
`n > 0 and (n & (n - 1)) == 0`
(We check `n > 0` because 0 or negative numbers cannot be powers of 2).

---

## 4. The Alternating Mask for Powers of Four

Powers of 4 ($4, 16, 64...$) are a subset of powers of 2. 
If we look at their bit positions:
`1 = 000001` (index 0)
`4 = 000100` (index 2)
`16= 010000` (index 4)

A power of 4 is a power of 2 where the single `1` bit is located at an **even index**.
How do we verify it's at an even index? We use a Hexadecimal Bit Mask.

`0x55555555` is hexadecimal for the binary sequence `0101010101010101...` 
It has a `1` in every even index, and a `0` in every odd index.
If we AND our number with this mask (`n & 0x55555555`), the result will equal `n` ONLY if `n`'s single bit lines up perfectly with one of the `1`s in the mask.

---

## Problem: Reverse Bits

* **Interview Difficulty:** Easy
* **Problem Type:** Bit Extraction and Assembly
* **Data Structure Used:** Scalar
* **Optimized Approach:** Iterate 32 times. For each index `i`, extract the $i$-th bit of `n` using `(n >> i) & 1`. Once extracted, shift it left to its mirrored position `31 - i`, and OR it into a running `res` variable.
* **Complexity:**
  * **Time:** $O(1)$ (exactly 32 operations).
  * **Space:** $O(1)$
* **Pointer Flow:**
```text
n = 0011 (pretend 4-bit)
i=0: extract bit 0 (1). Shift to index 3 (3-0). res = 1000
i=1: extract bit 1 (1). Shift to index 2 (3-1). res = 1000 | 0100 = 1100
i=2: extract bit 2 (0). Shift to index 1 (3-2). res = 1100 | 0000 = 1100
i=3: extract bit 3 (0). Shift to index 0 (3-3). res = 1100 | 0000 = 1100
Final reversed = 1100.
```
* **Pattern Recognition:**
  * Iterating through bits to build a new number from scratch.
* **Core Insight:** You cannot reliably reverse bits "in place" because swapping them overwrites data. Building a completely new number by picking bits one by one and placing them in their destination slots is the canonical safe approach.

---

## Problem: Power of Two

* **Interview Difficulty:** Easy
* **Problem Type:** Brian Kernighan's Property
* **Data Structure Used:** Logic Statement
* **Optimized Approach:** The expression `n & (n - 1)` removes the lowest set bit. If `n` is a power of two, it only has one set bit. Thus, removing it results in `0`. Also, ensure `n > 0`.
* **Complexity:**
  * **Time:** $O(1)$
  * **Space:** $O(1)$
* **Pattern Recognition:**
  * "Power of two" is mathematically synonymous with "Single set bit".
* **Core Insight:** Division by 2 in a while loop takes $O(\log N)$ time. The bitwise hack checks the entire structural identity of the number in a single CPU tick.

---

## Problem: Power of Four

* **Interview Difficulty:** Easy
* **Problem Type:** Constant Masking
* **Data Structure Used:** Logic Statement
* **Optimized Approach:** First, check if it's a valid power of two (`n > 0 and (n & (n-1)) == 0`). Second, verify the bit is in an even index using the mask `0x55555555`. If `(n & 0x55555555) == n`, the bit is correctly aligned.
* **Complexity:**
  * **Time:** $O(1)$
  * **Space:** $O(1)$
* **Pattern Recognition:**
  * Subsetting powers based on index parity (even/odd positions).
* **Core Insight:** Hexadecimal masks are the industry standard way to apply repeating binary patterns. `0x55` is `01010101`, and `0xAA` is `10101010`. These two masks perfectly slice a 32-bit integer into its even-indexed and odd-indexed halves.
