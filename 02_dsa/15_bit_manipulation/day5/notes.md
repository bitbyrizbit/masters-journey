# Subsets & DP Foundations

## 1. The Geometry of Subsets

In Day 5, we shift from operating on raw integers to using integers as **State Representations**.
A 32-bit integer is physically a row of 32 on/off switches. If you have a collection of up to 32 items, an integer is the perfect data structure to record exactly which items are currently "selected" and which are "deselected."

This bridges the gap between Bit Manipulation, Combinatorics, and Dynamic Programming.

## 2. Generating Combinations (Subsets)

The most common backtracking problem is generating all subsets (the Power Set) of an array.
While recursion is elegant, it has overhead. Bit manipulation offers a purely iterative $O(2^N)$ approach.

If an array has $N$ elements, there are exactly $2^N$ subsets.
Conveniently, if you loop an integer `mask` from $0$ up to $2^N - 1$, the binary representation of `mask` cycles through every possible combination of 0s and 1s of length $N$.
*   `mask = 0` (000) -> Empty set
*   `mask = 1` (001) -> Subset with item 0
*   `mask = 3` (011) -> Subset with item 0 and 1
*   `mask = 7` (111) -> Subset with all items

**The Algorithm:**
1. Determine total subsets: `total = 1 << N`.
2. Loop `mask` from `0` to `total - 1`.
3. For each `mask`, loop `i` from `0` to `N - 1`. Check if the $i$-th bit is active (`(mask >> i) & 1`). If it is, include `nums[i]` in the current subset.

## 3. Bitmask Dynamic Programming

When solving problems like the Traveling Salesperson Problem (TSP), you must remember *which* cities you have visited.
If you use an array `visited = [True, False, True]`, you cannot easily use that array as a key in a Hash Map to memoize your DP state. 
If you convert the array to a tuple, hashing it is slow ($O(N)$).

Bitmask DP replaces the `visited` array with a single integer.
*   **Hashable:** An integer is a primitive type; hashing it is instant $O(1)$.
*   **Immutable:** Modifying a state doesn't require copying an array. To visit city `i`, you just pass `mask | (1 << i)` to the next recursive call.

This technique is mandatory for DP problems where the state involves a combination of elements and $N \le 20$.

---

## 4. Master Patterns

**1. The Subset Generator loop:**
```python
# Assuming n <= 20
for mask in range(1 << n):
    subset = []
    for i in range(n):
        if (mask >> i) & 1:
            subset.append(nums[i])
    print(subset)
```

**2. Bitmask DP State Transitions:**
```python
# To check if 'i' is in the state:
is_visited = (mask >> i) & 1

# To ADD 'i' to the state:
new_mask = mask | (1 << i)

# To REMOVE 'i' from the state:
new_mask = mask & ~(1 << i)

# To check if ALL items are visited:
is_full = mask == (1 << n) - 1
```

*For detailed code templates on these subjects, refer to `subset_generation.md` and `bitmask_dp_intro.md` in this directory.*
