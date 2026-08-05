# Optimal Merge & Priority Queue Greedy

## 1. What is Optimal Merge Greedy?

Optimal Merge Greedy is the family of problems where a binary combination cost — the price of combining two things equals the sum of their sizes — must be minimised across a sequence of merges that eventually produce a single result. This problem family is special because it connects two apparently different domains: **Huffman Coding** (data compression) and the **Optimal Merge Pattern** (file merging). Both are solved by an identical algorithm, both are proven optimal by an identical exchange argument, and both rest on the same core principle: **always merge the two smallest items first**.

The reason this principle is non-obvious is that it feels like it should matter *what* you merge, not just *which two are smallest*. But the mathematics reveals that the only property that determines the merge cost of an individual item is how many subsequent merges include it in their operands — which is exactly its depth in the merge tree. Smaller items placed at greater depth (merged later) contribute disproportionately more to the total cost. By merging small items early (at shallow depth), we keep the running cost low.

---

## 2. The Merge Tree and Weighted Path Length

Every sequence of binary merges can be visualised as a binary tree. Each leaf is an original item with weight $w_i$. Each internal node is a merged result whose weight equals the sum of its children's weights. Each merge operation costs the weight of the internal node created.

The total cost of all merges equals:

$$\text{Total Merge Cost} = \sum_{\text{internal nodes}} \text{weight(node)} = \sum_{\text{leaves}} w_i \cdot \text{depth}(i)$$

This second form is the **Weighted Path Length** of the tree. Minimising total merge cost is equivalent to minimising the weighted path length — which means we want items with larger weights to be at shallower depths (fewer merges include them) and items with smaller weights to be at deeper depths (more merges include them). The Huffman / Optimal Merge algorithm achieves this by always selecting the two smallest weights to merge next.

---

## 3. The Exchange Argument for Optimal Merge

**Claim:** Merging the two smallest items first is always optimal.

**Proof by exchange argument:** Suppose an optimal solution does not make the two globally smallest items $x$ and $y$ siblings at the deepest level. Instead, two other nodes $a$ and $b$ are the deepest siblings. Since $x$ and $y$ are the smallest, $w(x) \leq w(a)$ and $w(y) \leq w(b)$.

Now swap $x$ with $a$ (put $x$ in $a$'s position and $a$ in $x$'s position) and similarly swap $y$ with $b$. The change in total cost is:

$$\Delta = (w(x) - w(a)) \cdot (d_a - d_x) + (w(y) - w(b)) \cdot (d_b - d_y)$$

Since $w(x) \leq w(a)$ and $d_a \geq d_x$ (a and b are at the deepest level), the term $(w(x) - w(a))(d_a - d_x) \leq 0$. Similarly for the $y$/$b$ swap. Therefore $\Delta \leq 0$: the swap never increases total cost.

By repeatedly applying this swap, any optimal solution can be transformed into one where $x$ and $y$ are the deepest siblings — proving that the greedy choice (merge smallest two first) is achievable without cost. $\square$

---

## 4. Huffman Coding — Frequency as Weight

Huffman Coding applies the Optimal Merge framework to prefix-free binary code construction. Given symbols with frequencies $f_1, f_2, \ldots, f_k$, we want binary codes such that the total encoded message length

$$\text{Total Bits} = \sum_i f_i \cdot \text{len}(code_i)$$

is minimised. This is exactly the weighted path length problem: frequencies are the leaf weights, code lengths are the leaf depths. Minimising total bits = minimising weighted path length = Huffman's algorithm.

The algorithm builds the code tree bottom-up using a min-heap:
1. Push all (frequency, symbol) pairs into the heap.
2. Repeatedly pop the two minimum-frequency nodes, create an internal node with their combined frequency, push it back.
3. When one node remains, it is the root. The code for each symbol is the path from root to its leaf.

The resulting tree guarantees that the two rarest symbols are always siblings at the greatest depth — matching exactly what the exchange argument proves is optimal.

---

## 5. The Dual-Heap Sequential Unlock Pattern (IPO)

The IPO problem introduces a structurally different priority queue pattern: items have a **requirement** (minimum capital to access them) and a **value** (profit when completed). As we collect value, new items become accessible — there is a dynamic feedback loop between current capital and available choices.

This creates a two-dimensional constraint that neither a single sort nor a single heap can resolve alone. The solution is the **dual-heap pattern**:

*   A **min-heap keyed on requirements** serves as a gatekeeper: it efficiently identifies which items have become newly accessible as capital grows.
*   A **max-heap keyed on values** serves as a ranker: among all currently accessible items, it selects the one with maximum immediate gain.

At each step: drain newly accessible items from the min-heap into the max-heap (gate-pass), then extract the highest-value item from the max-heap (greedy selection). This combination ensures that we always make the best choice among all currently available options while automatically unlocking new options as our capital grows.

---

## 6. Generic Optimal Merge and Dual-Heap Templates

```python
import heapq

# Optimal Merge Pattern (Huffman-style)
def optimal_merge_cost(weights: list[int]) -> int:
    heap = weights[:]
    heapq.heapify(heap)
    total_cost = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        merged = a + b
        total_cost += merged
        heapq.heappush(heap, merged)
    return total_cost


# Dual-Heap Sequential Unlock (IPO)
def max_capital_greedy(k: int, w: int, profits: list[int], capital: list[int]) -> int:
    projects = sorted(zip(capital, profits))        # Sort by capital requirement
    available = []                                  # Max-heap (negated for Python)
    i = 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(available, -projects[i][1])   # Push profit (negated)
            i += 1
        if not available:
            break                                   # No accessible project
        w += -heapq.heappop(available)              # Add max profit to capital
    return w
```

---

## Problem: IPO — Maximise Capital

* **Problem Type:** Sequential Capital Unlocking / Dual-Heap Greedy
* **Data Structure Used:** Sorted list of `(capital_requirement, profit)` pairs + min-heap (gatekeeper) + max-heap via negated min-heap (ranker)
* **Approach 1:** At each of $k$ rounds, scan all projects to find those affordable with current capital, then pick the one with maximum profit. Each round is $O(N)$, and there are $k$ rounds, giving $O(kN)$. For $k, N = 10^5$, this is $10^{10}$ operations — infeasible.
* **Optimized Approach:** Dual-Heap Sequential Unlock. Sort projects by capital requirement. In each of $k$ rounds, advance a pointer to push all newly affordable projects (capital requirement ≤ current wealth) from the sorted list into a max-heap. Pop the maximum-profit project from the heap, add its profit to current capital. Repeat for $k$ rounds or until the heap is empty.
* **Complexity:**
  * **Time:** $O(N \log N + k \log N)$ — sorting is $O(N \log N)$; each of $N$ heap pushes costs $O(\log N)$; each of $k$ pops costs $O(\log N)$.
  * **Space:** $O(N)$ — both heaps together hold at most $N$ projects.
* **Pointer Flow:**
```text
k=2, w=0, profits=[1,2,3], capital=[0,1,1]
Sorted pairs: [(0,1),(1,2),(1,3)]

Round 1: Unlock (0,1) [capital 0<=0] -> max_heap=[-1]. No more. Pop -1. w=0+1=1.
Round 2: Unlock (1,2),(1,3) [capital 1<=1] -> max_heap=[-2,-3]. Pop -3. w=1+3=4.

Answer: 4.
```
* **Pattern Recognition:**
  * Use the dual-heap sequential unlock pattern when:
    - Items have a threshold requirement that must be met before they can be accessed.
    - Accessing an item increases your resource, which may unlock further items.
    - The greedy choice at each step is: among all currently accessible items, take the one with maximum value.
* **Core Insight:** The dual-heap separates two orthogonal concerns: **eligibility** (which projects can we afford now?) and **value** (which affordable project is most profitable?). Neither concern alone solves the problem — eligibility changes as capital grows, and value ranking is meaningless without eligibility filtering. The min-heap on requirements efficiently tracks eligibility boundary changes. The max-heap on profits efficiently ranks eligible items. Together, they maintain a real-time leaderboard of the best currently available project.
* **Mistakes Made:** We sorted by capital and linearly scanned for the max-profit affordable project on each round. This $O(kN)$ approach redoes the maximum-finding work from scratch every round. The max-heap retains the ranking across rounds — previously discovered affordable projects stay in the heap and need not be rediscovered.
* **What I Learned:** When the set of available choices expands dynamically as you make decisions, a static sort cannot model the evolving eligibility frontier. The dual-heap pattern dynamically maintains both boundaries — what is accessible and what is best among accessible — with logarithmic update cost per step.

---

## Problem: Huffman Coding (Conceptual)

* **Problem Type:** Optimal Merge / Minimum Weighted Path Length Tree Construction
* **Data Structure Used:** Min-heap of (frequency, node) pairs
* **Approach 1:** Greedily assign codes by hand without a structured tree. There is no efficient algorithm without the min-heap approach — the optimal code structure is not apparent from the frequencies alone.
* **Optimized Approach:** Bottom-up Huffman Tree Construction. Push all symbol frequencies into a min-heap. Repeatedly extract the two minimum-frequency nodes, create an internal node with their combined frequency, and push it back. Continue until one node remains (the root). Assign codes by traversing the tree from root to each leaf: left edge = `0`, right edge = `1`.
* **Complexity:**
  * **Time:** $O(N \log N)$ — $N-1$ merge operations, each involving two heap pops and one push at $O(\log N)$ cost.
  * **Space:** $O(N)$ — the heap holds at most $N$ nodes; the tree has $2N-1$ total nodes.
* **Pointer Flow:**
```text
Symbols: {A:45, B:13, C:12, D:16, E:9, F:5}
Heap (sorted): [(5,F),(9,E),(12,C),(13,B),(16,D),(45,A)]

Merge F(5)+E(9)  -> FE(14). Heap: [12,13,14,16,45]
Merge C(12)+B(13)-> CB(25). Heap: [14,16,25,45]
Merge FE(14)+D(16)-> FED(30). Heap: [25,30,45]
Merge CB(25)+FED(30)->CBFED(55). Heap: [45,55]
Merge A(45)+CBFED(55)-> root(100). Heap: [100]

A=0 (depth 1), CB branch=10/11, FED branch=111xx
Codes: A=0, C=100, B=101, F=1100, E=1101, D=111
Total bits = 45*1+13*3+12*3+16*3+9*4+5*4 = 224 bits.
```
* **Pattern Recognition:**
  * Use Huffman / Optimal Merge whenever:
    - The cost of a series of binary combinations equals the sum of the two operands' sizes (or weights).
    - The goal is to minimise the total combination cost across all merges.
    - The problem involves building a binary tree that minimises total weighted path length.
* **Core Insight:** The Huffman algorithm is not just a compression trick — it is a general framework for minimising any cost structure that is linear in element weights and tree depths. The min-heap naturally enforces the greedy order (always merge smallest first) without needing to re-sort after each merge. Each pop-pop-push cycle is exactly one merge step at $O(\log N)$ cost.
* **Mistakes Made:** We tried to build the tree top-down — starting from the root and recursively splitting the frequency set. Top-down approaches require choosing the split point optimally, which itself requires solving a subproblem — introducing exponential complexity. Bottom-up heap-driven merging is strictly simpler and correct by the exchange argument.
* **What I Learned:** Optimal Merge and Huffman Coding are identical algorithms in different clothing. Recognising this equivalence means one mental model resolves both. Whenever a problem involves combining items where cost = sum of sizes and you must minimise total cost, immediately reach for a min-heap and the smallest-first merge strategy.

---

## Problem: Optimal Merge Pattern (Conceptual)

* **Problem Type:** Minimum Total Merge Cost / Weighted Path Length Minimisation
* **Data Structure Used:** Min-heap of file/list sizes
* **Approach 1:** Merge files in arbitrary order (e.g., sequentially: merge file 1 with file 2, then with file 3, etc.). This produces a skewed merge tree where large files participate in many intermediate merges, incurring disproportionately high cost.
* **Optimized Approach:** Always merge the two smallest files. Use a min-heap. Pop the two smallest, create a merged file of their combined size, push it back. The total cost equals the sum of all merged file sizes created — which equals the sum of `weight[leaf] * depth[leaf]` over all original files.
* **Complexity:**
  * **Time:** $O(N \log N)$ — $N-1$ merge steps, each $O(\log N)$.
  * **Space:** $O(N)$ — the heap.
* **Pointer Flow:**
```text
Files: [2, 3, 4, 5, 6]
Heap: [2, 3, 4, 5, 6]

Merge 2+3=5. Cost=5. Heap: [4,5,5,6]
Merge 4+5=9. Cost=9. Heap: [5,6,9]
Merge 5+6=11. Cost=11. Heap: [9,11]
Merge 9+11=20. Cost=20. Heap: [20]

Total cost = 5+9+11+20 = 45.

Compare naive sequential (2+3=5, 5+4=9, 9+5=14, 14+6=20): Total = 5+9+14+20 = 48.
Greedy saves 3 cost units.
```
* **Pattern Recognition:**
  * Use optimal merge greedy whenever:
    - Items are combined pairwise with cost = sum of sizes.
    - The goal is to minimise total combination cost across all pairings.
* **Core Insight:** Merging in any non-greedy order causes some large files to participate in many intermediate merges, each time adding their full size to the running cost. By merging small files first, we defer the large-file contributions to as late as possible (shallow depth in the merge tree), minimising how many times they appear in the running sum.
* **Mistakes Made:** We merged files in sorted order sequentially (merge smallest with second-smallest, then merge result with third-smallest, etc.). This is partially greedy but not globally optimal because the merged intermediate results can be larger than remaining original files — a new result should re-enter the priority pool, not be forced to merge with the next original file.
* **What I Learned:** After each merge, the result must re-enter the priority queue — not automatically proceed to merge with the next item in the original sorted order. The key data structure insight is that the heap maintains a global minimum across both original items and intermediate merged results simultaneously.

---

### Master Patterns Learned

#### 1. Min-Heap Optimal Merge (The Smallest-First Combination Frame)
* **Applied to:** Optimal Merge Pattern, Huffman Coding
* **The Strategy:** Push all item weights into a min-heap. Repeatedly pop two smallest, merge them (cost = sum), push result back. Total cost = sum of all merged results. Stop when one item remains.
* **The Conceptual Mechanics:**
  - **Weighted Path Length Minimisation:** Each item's contribution to total cost equals `weight × depth`. By placing the smallest items at the greatest depth (merged first, sinking deeper in the tree), we minimise the overall weighted sum.
  - **Re-Entry Requirement:** Merged results must re-enter the heap — not be paired sequentially with the next original item. The heap globally ranks all items (original and intermediate) by size.
* **The Layout / Code Pattern:**
```python
def optimal_merge_cost(weights: list[int]) -> int:
    heap = weights[:]
    heapq.heapify(heap)
    total_cost = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        merged = a + b
        total_cost += merged
        heapq.heappush(heap, merged)
    return total_cost
```

#### 2. Dual-Heap Sequential Unlock (The Eligibility-Value Separation Frame)
* **Applied to:** IPO
* **The Strategy:** Sort items by requirement. Sweep with a pointer to push newly eligible items into a max-heap as current resources grow. At each step, pop the max-value eligible item and consume it. Repeat for up to $k$ steps.
* **The Conceptual Mechanics:**
  - **Eligibility Frontier:** As resources grow, the min-heap pointer advances, pushing newly eligible items into the max-heap. The pointer only moves forward — items never become ineligible once unlocked.
  - **Greedy Correctness:** Among all currently eligible items, selecting the highest-value one maximises the rate at which resources grow, which maximally expands the eligible set for subsequent steps. This is proven optimal by the greedy-stays-ahead argument.
* **The Layout / Code Pattern:**
```python
def max_capital(k: int, w: int, profits: list[int], capital: list[int]) -> int:
    projects = sorted(zip(capital, profits))
    max_heap = []
    i = 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(max_heap, -projects[i][1])   # Negate for max-heap
            i += 1
        if not max_heap:
            break
        w += -heapq.heappop(max_heap)
    return w
```
