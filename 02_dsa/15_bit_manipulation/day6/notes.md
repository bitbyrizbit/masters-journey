# Master Bit Hacks

## 1. The Limit of Bit Manipulation

By Day 6, you have learned that bit manipulation is about understanding the hardware-level geometry of numbers. 
*   **Day 1 & 2** taught you how to isolate, toggle, and count bits using masks and shifts.
*   **Day 3** proved that entire arithmetic systems (addition) can be built from raw logic gates, and that bulk operations (ranges) can be bypassed by finding common prefixes.
*   **Day 4** showed how bitwise logic powers optimized data structures like Tries.
*   **Day 5** abstracted bits away from numbers entirely, using them as combinatorial state vectors for DP.
*   **Day 6** provides the algorithmic cheat codes used by competitive programmers to shave operations down to absolute hardware minimums.

## 2. Review: The Big Three Bit Hacks

If you forget everything else, memorize these three algorithmic cornerstones. They appear repeatedly in FAANG interviews.

**1. Brian Kernighan's (Drop Lowest Set Bit)**
`n & (n - 1)`
*Use case:* Counting bits, checking powers of 2.

**2. The Lowbit Extraction**
`n & -n`
*Use case:* Fenwick Trees (Binary Indexed Trees), finding the rightmost `1`.

**3. XOR Cancellation**
`a ^ a = 0`
*Use case:* Finding singletons in pairs, missing numbers in sequences.

---

*For detailed code templates on advanced hacks (Submask iteration, Smearing, Swapping), refer to `advanced_bit_hacks.md` in this directory.*
