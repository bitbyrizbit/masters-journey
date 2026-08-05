# Advanced XOR & Tries

## 1. The Anatomy of XOR Maximization

What does it mean to maximize the XOR of two numbers?
The XOR operation (`^`) yields a `1` only when the bits are different. 
Therefore, if you have a number `A`, the number `B` that maximizes `A ^ B` is the number that is the **exact bitwise inverse** of `A`.

If $A = 10110$, we ideally want to find a $B$ in our dataset that looks like $01001$.
Every time we find an opposite bit, we secure a `1` in our XOR result. Every time we are forced to pair a bit with an identical bit, we get a `0` in our result.

Crucially, **bits at higher positions are exponentially more valuable**. 
A single `1` at position 31 is worth more ($2^{31}$) than a `1` at every single position from 0 to 30 combined ($2^{31} - 1$).
Therefore, our search for the perfect opposite number MUST proceed strictly from the most significant bit (left) to the least significant bit (right). We must be perfectly greedy: we will sacrifice every lower bit if it means securing a difference at the current highest available bit.

---

## 2. The Bitwise Trie

To efficiently search for a number bit-by-bit from left to right, we use a Prefix Tree, commonly known as a **Trie**.

Instead of storing alphabetical characters (a-z), a Bitwise Trie only stores two possible children at each node: `0` or `1`.
The depth of the Trie is exactly 32 (representing the 32 bits of an integer). 

**Insertion:**
To insert a number, we iterate from bit 31 down to 0. If the bit is `1`, we traverse down the `1` branch. If `0`, we traverse down the `0` branch. If a branch doesn't exist, we create a new node.

**Greedy Traversal (The Magic):**
Once the Trie is built, how do we find the best pairing for a number $X$?
We start at the root of the Trie and look at bit 31 of $X$. 
*   If bit 31 of $X$ is `1`, we *want* to go down the `0` branch to maximize the XOR. We check if the current node has a `0` child. If it does, great! We take that path and record that we secured a `1` for bit 31 in our result.
*   If the `0` branch does NOT exist, we have no choice. We must go down the `1` branch. This means the XOR at this position will be `0`.
We repeat this, dynamically choosing the optimal path through the Trie based on whatever branches are actually available, always prioritizing the opposite bit.

By doing this, finding the optimal pairing for any number takes exactly 32 steps — an $O(1)$ operation!

---

## 3. Alternative: The Hash Set (Masking) Trick

There is a secondary, mathematically elegant way to find Maximum XOR without building a full Trie object. It relies on building the maximum possible answer bit by bit.

Starting from bit 31 down to 0:
1.  Assume the best possible XOR we could achieve up to this bit is `max_xor | (1 << i)`. Let's call this the `target`.
2.  Store all the prefixes of the numbers (chopped off below bit `i`) in a Hash Set.
3.  We know that `A ^ B = target`. By the properties of XOR, this also means `target ^ A = B`.
4.  For every prefix `A` in our set, we check if `target ^ A` also exists in our set! If it does, it proves that a valid pair `(A, B)` exists that achieves our `target`. We permanently update our `max_xor`.

While building a Trie is $O(N)$ and the Hash Set approach is also $O(N)$, the Hash Set often runs faster in Python due to the high overhead of instantiating thousands of `TrieNode` objects. However, the Bitwise Trie is the fundamental conceptual structure for all advanced bit-routing algorithms.

---

## Master Template

```python
class TrieNode:
    def __init__(self):
        self.children = {}

def build_and_search_trie(nums: list[int]) -> int:
    root = TrieNode()
    
    # 1. Build the Trie
    for num in nums:
        node = root
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            if bit not in node.children:
                node.children[bit] = TrieNode()
            node = node.children[bit]
            
    max_xor = 0
    
    # 2. Greedily Search for Opposites
    for num in nums:
        node = root
        curr_xor = 0
        for i in range(31, -1, -1):
            bit = (num >> i) & 1
            ideal_bit = 1 - bit
            
            if ideal_bit in node.children:
                curr_xor |= (1 << i)
                node = node.children[ideal_bit]
            else:
                node = node.children[bit]
                
        max_xor = max(max_xor, curr_xor)
        
    return max_xor
```

---

## Problem: Maximum XOR of Two Numbers in an Array

* **Interview Difficulty:** Medium/Hard
* **Problem Type:** Bitwise Trie / Greedy Prefix Search
* **Data Structure Used:** Binary Trie
* **Approach 1:** Double loop. Compare every number with every other number. Time: $O(N^2)$, which results in TLE for arrays larger than a few thousand elements.
* **Optimized Approach:** Insert all numbers into a 32-depth Bitwise Trie. Iterate through the array again. For each number, traverse the Trie from the root, greedily attempting to pick the branch that represents the opposite of the current bit. Keep a running tally of the XOR generated by the path taken, and update the global max. 
* **Complexity:**
  * **Time:** $O(32 \cdot N) = O(N)$
  * **Space:** $O(32 \cdot N) = O(N)$ to store the Trie.
* **Pattern Recognition:**
  * Maximizing/Minimizing bitwise outputs across pairs in an array.
* **Core Insight:** You cannot sort an array to find XOR proximities because XOR distances do not map cleanly to standard numerical distances (e.g., $7 \text{ (0111)}$ and $8 \text{ (1000)}$ are numerically adjacent, but their XOR is 15, which is huge). A Bitwise Trie acts as a custom sorting mechanism that perfectly clusters numbers by their bitwise similarities, allowing $O(1)$ optimal partner lookups.
