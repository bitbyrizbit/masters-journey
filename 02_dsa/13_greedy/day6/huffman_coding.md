# Huffman Coding — Conceptual Analysis

## 1. Definition

**Huffman Coding** is a lossless data compression algorithm that assigns variable-length binary codes to symbols based on their frequency of occurrence. Symbols that appear more frequently receive shorter codes; symbols that appear rarely receive longer codes. This is the theoretically optimal prefix-free encoding.

A **prefix-free code** (also called a prefix code) is a code where no codeword is a prefix of any other codeword. This property ensures that any encoded bitstring can be uniquely decoded without ambiguity.

The algorithm was invented by David A. Huffman in 1952 and remains foundational in modern compression formats including ZIP, JPEG, MP3, and PNG.

---

## 2. Core Intuition

The compression gain comes from **matching code length to symbol probability**. In standard fixed-length ASCII encoding, every character costs 8 bits regardless of how often it appears. In Huffman coding, if 'e' appears 40% of the time, it gets 1-2 bits, saving vast amounts of space on average.

The key insight is to **build the encoding tree bottom-up by always merging the two least-frequent symbols first**. This greedily ensures the least frequent symbols are deepest in the tree (longest codes), while the most frequent symbols end up shallowest (shortest codes).

---

## 3. Why Greedy Works — The Exchange Argument

**Claim:** Huffman's greedy algorithm produces an optimal prefix-free code.

**Proof sketch (by exchange argument):**

Let $T^*$ be an optimal prefix-free tree. Consider the two symbols $x$ and $y$ with the lowest frequencies in the alphabet. In any optimal tree, $x$ and $y$ must be sibling leaves at the deepest level. Here's why:

- In an optimal tree $T^*$, there must exist a deepest pair of sibling leaves $a, b$.
- Since $x$ and $y$ have the smallest frequencies, swapping $a \leftrightarrow x$ and $b \leftrightarrow y$ cannot increase the total expected code length (lower frequency at deeper depth = smaller or equal cost contribution).
- Therefore, there exists an optimal tree where $x$ and $y$ are siblings at the deepest level.

Once we fix $x$ and $y$ as siblings, their parent becomes a new meta-symbol with frequency $f(x) + f(y)$. The remaining problem is a strictly smaller Huffman problem on $n-1$ symbols. By induction, the greedy choice at every level leads to the globally optimal tree.

---

## 4. Algorithm

```
HuffmanCode(symbols, frequencies):
    1. Create a leaf node for each symbol with its frequency.
    2. Insert all nodes into a Min-Priority Queue (keyed by frequency).
    3. While the queue has more than one node:
        a. Extract the two nodes with the lowest frequencies (left, right).
        b. Create an internal node with frequency = left.freq + right.freq.
        c. Assign left and right as children of this internal node.
        d. Insert the internal node back into the queue.
    4. The remaining node is the root of the Huffman Tree.
    5. Traverse the tree:
        - Going left adds '0' to the code.
        - Going right adds '1' to the code.
        - At each leaf, assign the accumulated binary string as the codeword.
```

---

## 5. Worked Example

Symbols and frequencies:

| Symbol | Frequency |
|--------|-----------|
| A      | 5         |
| B      | 9         |
| C      | 12        |
| D      | 13        |
| E      | 16        |
| F      | 45        |

**Step-by-step tree construction:**

```
Step 1: Merge A(5) + B(9) → AB(14)
        Queue: [C(12), D(13), AB(14), E(16), F(45)]

Step 2: Merge C(12) + D(13) → CD(25)
        Queue: [AB(14), E(16), CD(25), F(45)]

Step 3: Merge AB(14) + E(16) → ABE(30)
        Queue: [CD(25), ABE(30), F(45)]

Step 4: Merge CD(25) + ABE(30) → CDABE(55)
        Queue: [F(45), CDABE(55)]

Step 5: Merge F(45) + CDABE(55) → root(100)
```

**Resulting codes:**

| Symbol | Code | Length |
|--------|------|--------|
| F      | 0    | 1      |
| C      | 100  | 3      |
| D      | 101  | 3      |
| A      | 1100 | 4      |
| B      | 1101 | 4      |
| E      | 111  | 3      |

**Weighted Path Length (total bits):**
$$\text{WPL} = 5(4) + 9(4) + 12(3) + 13(3) + 16(3) + 45(1) = 224 \text{ bits}$$

Compare to fixed 3-bit encoding: $100 \times 3 = 300$ bits.
**Compression ratio:** $224 / 300 \approx 74.7\%$ — a 25.3% reduction.

---

## 6. Complexity

| Operation          | Complexity     |
|--------------------|----------------|
| Build initial heap | $O(N)$         |
| N−1 merges         | $O(N \log N)$  |
| Tree traversal     | $O(N)$         |
| **Total**          | **$O(N \log N)$** |
| **Space**          | **$O(N)$**     |

---

## 7. Optimality Guarantee

Huffman coding achieves the minimum possible average code length $\bar{L}$ over all prefix-free codes. Formally, if $H(X)$ is the Shannon entropy of the source:

$$H(X) \leq \bar{L} < H(X) + 1$$

where $H(X) = -\sum_{i} p_i \log_2 p_i$. Huffman coding comes within 1 bit per symbol of the theoretical entropy lower bound — this is proven to be tight.

---

## 8. Real-World Applications

- **ZIP / DEFLATE**: Uses Huffman coding as the final entropy coding stage after LZ77.
- **JPEG**: Huffman encodes DCT coefficient quantisation indices.
- **MP3**: Uses Huffman coding for quantised spectral coefficients.
- **PNG**: Uses DEFLATE (LZ77 + Huffman) internally.
- **HTTP/2 HPACK**: Uses a static Huffman table for header compression.

---

## 9. Key Takeaway

Huffman coding is the canonical proof that a local greedy decision — always merge the two cheapest nodes — yields a globally optimal structure. The exchange argument formalises why any deviation from the greedy choice cannot improve the result. It is both a compression algorithm and a masterclass in why greedy works.
