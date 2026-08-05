# Advanced Bit Hacks

Competitive programming and high-performance algorithms rely on obscure but mathematically beautiful bitwise hacks. Here are the most essential ones to know for top-tier technical interviews.

## 1. The Lowbit Trick (`x & -x`)

What does `x & -x` do? It extracts the **lowest set bit** of `x`, leaving all other bits as `0`.

**How it works:**
In computers, negative numbers are stored using Two's Complement.
To get `-x`, the CPU takes `x`, flips every single bit (`~x`), and then adds `1`.
When you add `1` to the flipped number, it cascades from the right, flipping `1`s to `0`s until it hits the first `0` and turns it into a `1`.
This perfectly restores the original lowest set bit, while everything to the left of it remains inverted.

When you AND `x` and `-x`, all the inverted bits on the left cancel out to `0`. The lowest set bit (which is `1` in both) survives.
`x      = 01010100`
`-x     = 10101100`
`x & -x = 00000100`

**Application:** 
This is the foundational engine of the **Binary Indexed Tree (Fenwick Tree)**, used for incredibly fast $O(\log N)$ prefix sum queries and dynamic array updates.

## 2. Iterating Through Submasks

If you have a bitmask representing a set (e.g., `mask = 13`, binary `1101`), how do you iterate through all valid submasks (subsets of that specific set) efficiently without looping all the way from $0$ to $mask$ and checking if `submask | mask == mask`?

The optimal way is the Submask Iteration Hack:
```python
submask = mask
while submask > 0:
    print(submask)
    # The Magic Line:
    submask = (submask - 1) & mask
```

**How it works:**
Subtracting `1` from `submask` borrows from its lowest set bit.
ANDing it with the original `mask` immediately wipes out any bits that "turned on" during the subtraction but weren't part of the original `mask`.
This mathematically guarantees you step through every valid submask in descending order. It runs in $O(2^K)$ time (where $K$ is the number of set bits in `mask`), rather than $O(M)$ time (where $M$ is the numerical value of the mask).

## 3. Swapping Without Temp Variables

You can swap two integers using only XOR. No temporary memory allocated.
```python
a ^= b
b ^= a
a ^= b
```
*Note: This is mostly a neat party trick. In production, Python's `a, b = b, a` is safer and highly optimized.*

## 4. Power of 2 Floor (Smearing)

To find the largest power of 2 less than or equal to $N$:
```python
# Smear the highest 1-bit downward to fill all lower bits with 1s
n |= n >> 1
n |= n >> 2
n |= n >> 4
n |= n >> 8
n |= n >> 16

# 'n' is now a solid block of 1s (e.g., 00111111).
# We isolate the highest bit by subtracting its right-shifted self:
ans = n - (n >> 1)
```
This is a bitwise technique to avoid using `math.log2(n)`.
