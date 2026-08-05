# Generating Subsets using Bitmasks

One of the most profound applications of bit manipulation is using an integer to represent a **Subset** (or a combination) of a larger set.

If you have a set of $N$ items, there are exactly $2^N$ possible subsets.
Conveniently, an $N$-bit integer can hold exactly $2^N$ different values (from $0$ to $2^N - 1$).
We can create a perfect 1-to-1 mapping between integers and subsets:
*   The $i$-th bit of the integer corresponds to the $i$-th item in the set.
*   If the bit is `1`, the item is IN the subset.
*   If the bit is `0`, the item is OUT of the subset.

## The Generation Loop

Generating all subsets of an array of length $N$ requires NO recursion and NO backtracking. You simply loop a counter from $0$ to $2^N - 1$.

```python
def generate_subsets(nums):
    n = len(nums)
    subsets = []
    
    # 1 << n is mathematically 2^n
    for mask in range(1 << n):
        current_subset = []
        
        # Check every bit position from 0 to n-1
        for i in range(n):
            # If the i-th bit is set in the mask, include nums[i]
            if (mask >> i) & 1:
                current_subset.append(nums[i])
                
        subsets.append(current_subset)
        
    return subsets
```

## Why use Bitmasks over Backtracking?
1.  **Code Brevity:** It's a simple double `for` loop. No complex recursive state management.
2.  **State Hashing:** If you need to memoize a state in Dynamic Programming, you can't easily use an array `[1, 3, 4]` as a key. But you CAN use the integer `mask = 26` as a perfectly compact, $O(1)$ lookup key. This transitions directly into Bitmask DP.
