# Advanced Greedy — Two-Pass, Two-Pointer & Capacity

## 1. What is Advanced Greedy?

The first six days of greedy training covered problems where a single sort and a single sweep resolved everything. Advanced greedy captures the problems that resist this pattern — not because greedy is the wrong paradigm, but because the problem's constraints are richer and require a more structured view of the input.

Three structural techniques define this category:

**Two-Pass Greedy** applies when constraints operate simultaneously in both directions. A child must receive more candy than its left neighbour *and* more than its right neighbour if its rating is higher in both directions. A single left-to-right pass satisfies one directional constraint, then a right-to-left pass corrects for the other without undoing the first. The `max` operation at each step in the second pass is the key: it enforces the new constraint without ever reducing a value that was needed to satisfy the first constraint.

**Two-Pointer Greedy** applies when we can trade between two extremes — buying the cheapest token to gain score, or selling the most expensive token to gain power. Sorting enables us to always have the cheapest at one pointer and the most expensive at the other. The greedy choices at both ends are clear: buy cheapest when affordable, sell most expensive when necessary.

**Capacity Greedy (Density Sort)** applies when we have a fixed capacity and want to maximise total value loaded. When items come in varying quantities with a fixed value per unit, the density (value per capacity unit) determines loading priority. Sort by density descending and fill greedily until capacity is exhausted.

---

## 2. The Two-Pass Correctness Principle

The reason two passes work for bilateral constraints is an important structural insight: **the left-neighbour constraint and the right-neighbour constraint are directionally independent**. Satisfying the left-neighbour constraint from left to right creates a monotone non-decreasing sequence along increasing-rating runs. Then, when we correct for right-neighbour constraints in the reverse direction, the only modification we make is to increase values (never decrease). Since the `max` operation can only raise a value, the left-neighbour constraint (which required a higher value) is automatically preserved.

The proof of minimality is by contradiction: suppose any value can be reduced. If `candies[i] > 1`, then either a left or right neighbour has a higher rating that requires `candies[i]` to be greater than their candy count. Reducing `candies[i]` would violate at least one of these constraints. Therefore no value can be reduced — the two-pass result is the unique minimum distribution.

---

## 3. The Two-Pointer Exchange Principle

Bag of Tokens is a resource exchange problem where we hold two resources — power and score — and items (tokens) convert one to the other. Buying a token (paying power, gaining score) is profitable when tokens are cheap. Selling a token (paying score, gaining power) is necessary when we cannot afford the next buy but have score to spend.

The greedy insight is that **when buying, always buy the cheapest affordable token** (minimise power spent per score point), and **when selling, always sell the most expensive token** (maximise power gained per score point). Any other buy/sell pair produces a worse or equal exchange rate. The two-pointer on a sorted array enforces these boundary choices at every step.

The subtle non-obvious requirement is tracking `max_score` rather than just final score. Selling tokens after reaching a peak score reduces the final score below the peak. The answer is the highest score ever reached, not the final state.

---

## 4. The Density Sort Optimality Proof

For Capacity Greedy (Maximum Units), the exchange argument is direct:

Suppose we load box type $A$ with density $d_A$ before box type $B$ with density $d_B$, and $d_A < d_B$, and there is remaining capacity when we load $A$. Swapping the order (loading $B$ before $A$) increases the total units loaded, because we now fill capacity with higher-density boxes first. Therefore, always loading the highest-density box type first is uniquely optimal.

This is the fractional knapsack solution applied to integer box counts. The fractional knapsack is solvable by greedy (density sort) precisely because items can be taken partially — we can always fill remaining capacity with a partial box type, achieving the exact density optimum at the boundary.

---

## 5. Generic Advanced Greedy Templates

```python
# Two-Pass Bilateral Constraint Greedy
def two_pass_minimum_distribution(ratings: list[int]) -> int:
    n = len(ratings)
    values = [1] * n
    # Pass 1: Left to Right — satisfy left-neighbour constraint
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            values[i] = values[i - 1] + 1
    # Pass 2: Right to Left — satisfy right-neighbour constraint without undoing Pass 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            values[i] = max(values[i], values[i + 1] + 1)  # max preserves Pass 1
    return sum(values)


# Two-Pointer Resource Exchange
def two_pointer_max_score(tokens: list[int], power: int) -> int:
    tokens.sort()
    lo, hi = 0, len(tokens) - 1
    score = max_score = 0
    while lo <= hi:
        if power >= tokens[lo]:             # Buy cheapest affordable token
            power -= tokens[lo]
            score += 1
            max_score = max(max_score, score)
            lo += 1
        elif score > 0:                     # Sell most expensive for power
            power += tokens[hi]
            score -= 1
            hi -= 1
        else:
            break                           # Cannot buy or sell: terminate
    return max_score


# Capacity Density Sort
def capacity_density_greedy(box_types: list[list[int]], truck_size: int) -> int:
    box_types.sort(key=lambda x: x[1], reverse=True)   # Sort by units per box desc
    total_units = 0
    for num_boxes, units_per_box in box_types:
        take = min(num_boxes, truck_size)
        total_units += take * units_per_box
        truck_size -= take
        if truck_size == 0:
            break
    return total_units
```

---

## Problem: Candy

* **Problem Type:** Two-Pass Bilateral Constraint Propagation
* **Data Structure Used:** Integer array `candies` of size $N$, initialised to all 1s
* **Approach 1:** Enumerate all valid candy distributions satisfying the two neighbour constraints and return the one with minimum total. There is no known polynomial exhaustive method — the space of valid distributions is exponential in $N$.
* **Optimized Approach:** Two-Pass Greedy. Initialise every child with 1 candy (satisfies the base constraint that everyone gets at least one). **Pass 1 (left to right):** for each `i` from 1 to $N-1$, if `ratings[i] > ratings[i-1]`, set `candies[i] = candies[i-1] + 1`. This satisfies all left-neighbour constraints. **Pass 2 (right to left):** for each `i` from $N-2$ down to 0, if `ratings[i] > ratings[i+1]`, set `candies[i] = max(candies[i], candies[i+1] + 1)`. The `max` preserves Pass 1 results while enforcing right-neighbour constraints.
* **Complexity:**
  * **Time:** $O(N)$ — two linear passes of $N$ steps each.
  * **Space:** $O(N)$ — the `candies` array of size $N$.
* **Pointer Flow:**
```text
ratings = [1, 3, 4, 5, 2]
Initialise: candies = [1, 1, 1, 1, 1]

Pass 1 (L -> R):
  i=1: 3>1 -> candies[1]=candies[0]+1=2. candies=[1,2,1,1,1]
  i=2: 4>3 -> candies[2]=candies[1]+1=3. candies=[1,2,3,1,1]
  i=3: 5>4 -> candies[3]=candies[2]+1=4. candies=[1,2,3,4,1]
  i=4: 2>5? No.                          candies=[1,2,3,4,1]

Pass 2 (R -> L):
  i=3: 5>2 -> candies[3]=max(4,1+1)=4. No change.
  i=2: 4>5? No.
  i=1: 3>4? No.
  i=0: 1>3? No.

Final candies = [1,2,3,4,1]. Sum = 11.
```
* **Pattern Recognition:**
  * Use two-pass greedy when:
    - Constraints reference both left and right neighbours simultaneously.
    - A single left-to-right or right-to-left pass satisfies only one direction.
    - The second pass must use `max` (not direct assignment) to avoid undoing the first pass.
* **Core Insight:** Left-neighbour and right-neighbour constraints are directionally independent. Satisfying them one direction at a time — and using `max` in the second pass to preserve the first — is both necessary and sufficient. The `max` is the key: it means "set this value to at least what the first pass required, and also at least what the second pass requires." Only if both passes agree is any value deterministic; otherwise, the higher of the two constraints wins.
* **Mistakes Made:** We attempted both constraints in a single left-to-right pass. This fails on patterns like `[5, 3, 4]` where the rating peak forces both the left and right neighbour to have fewer candies — a simultaneous bilateral requirement that cannot be resolved incrementally in one direction.
* **What I Learned:** Bilateral constraints require bilateral passes. The `max` in the second pass is not an approximation — it is the exact operation that ensures correctness: it never reduces a value below what the first pass established.

---

## Problem: Bag of Tokens

* **Problem Type:** Two-Pointer Greedy / Bidirectional Resource Exchange
* **Data Structure Used:** Sorted array of token costs + two pointers `lo`, `hi`
* **Approach 1:** Try all $2^N$ subsequences of buy/sell decisions, tracking power and score for each. Return the maximum score ever achieved. Time: $O(2^N)$.
* **Optimized Approach:** Two-Pointer Boundary Exchange. Sort tokens by cost ascending. Initialise `lo = 0`, `hi = N-1`, `score = 0`, `max_score = 0`. At each step: if `power >= tokens[lo]`, buy the cheapest token (power decreases, score increases by 1, `lo` advances, update `max_score`). Else if `score > 0`, sell the most expensive token (`hi` decrements, score decreases by 1, power increases by `tokens[hi]`). Else, no move is possible — break.
* **Complexity:**
  * **Time:** $O(N \log N)$ — sorting; the two-pointer sweep is $O(N)$ since `lo` and `hi` together advance at most $N$ steps.
  * **Space:** $O(1)$ — four scalars beyond the sorted array.
* **Pointer Flow:**
```text
tokens=[100,200,300,400], power=200
Sorted: [100,200,300,400], lo=0, hi=3

power=200 >= tokens[lo]=100: buy. power=100, score=1, max=1. lo=1.
power=100  < tokens[lo]=200. score=1>0: sell tokens[hi]=400. power=500, score=0. hi=2.
power=500 >= tokens[lo]=200: buy. power=300, score=1, max=1. lo=2.
power=300 >= tokens[lo]=300: buy. power=0, score=2, max=2. lo=3.
lo(3) > hi(2) -> stop.

Answer: max_score = 2.
```
* **Pattern Recognition:**
  * Use two-pointer boundary exchange when:
    - Buying the cheapest item costs one resource and selling the most expensive item recovers a different resource.
    - The optimal strategy always operates at the two boundaries of a sorted collection.
    - The answer is the maximum of a running state value, not the final state.
* **Core Insight:** When we can trade between two resources and the trade rate is fixed (1 score per token bought, 1 score per token sold), the only thing that affects total value is which specific tokens we use. Always buying cheapest minimises power spent per score; always selling most expensive maximises power recovered per score. The sorted two-pointer guarantees both boundaries are maintained simultaneously without re-sorting after each decision.
* **Mistakes Made:** We tracked only the final score, not the running maximum. In the pointer flow above, score reaches 2 before dropping back to 0 (after selling). The final score after all operations is not necessarily the maximum reached during the process. Always maintain `max_score` separately.
* **What I Learned:** In exchange problems with both buy and sell operations, the terminal state can be worse than intermediate states. The answer is always a running maximum over the entire trajectory, not a final value. This is a subtle but critical design detail.

---

## Problem: Maximum Units on a Truck

* **Problem Type:** Capacity Greedy / Density Sort Maximisation
* **Data Structure Used:** Sorted 2D array of `[numBoxes, unitsPerBox]` pairs
* **Approach 1:** Try all subsets of box types and count how many units fit in the truck for each valid combination. Time: $O(2^N \cdot T)$ where $T$ is the truck capacity.
* **Optimized Approach:** Density Sort Capacity Fill. Sort box types by `unitsPerBox` descending (density sort — since each box occupies exactly 1 unit of truck space, `unitsPerBox` is both the density and the value). For each box type in sorted order: take as many boxes as the remaining truck space allows (`take = min(numBoxes, remaining_capacity)`), add `take * unitsPerBox` to total units, subtract `take` from remaining capacity. Stop when capacity is exhausted.
* **Complexity:**
  * **Time:** $O(N \log N)$ — sorting dominates; the greedy fill sweep is $O(N)$.
  * **Space:** $O(1)$ — two scalar counters beyond the sorted array.
* **Pointer Flow:**
```text
boxTypes = [[1,3],[2,2],[3,1]], truckSize = 4
Sorted by unitsPerBox desc: [[1,3],[2,2],[3,1]]

[1,3]: take=min(1,4)=1. units+=1*3=3. remaining=3.
[2,2]: take=min(2,3)=2. units+=2*2=4. remaining=1.
[3,1]: take=min(3,1)=1. units+=1*1=1. remaining=0.

Total units = 3+4+1 = 8. remaining=0 -> stop.
```
* **Pattern Recognition:**
  * Use density sort capacity fill when:
    - A fixed capacity must be filled with items of varying value-per-unit.
    - Each item has both a quantity (how many we can take) and a value-per-unit (how valuable each unit is).
    - The goal is to maximise total value within the capacity constraint.
* **Core Insight:** Density (value per unit of capacity consumed) is the only metric that matters for filling a fixed container optimally. A box type with 10 units per box is twice as valuable per truck space as one with 5 units per box — even if the latter comes in larger quantities. By sorting by density descending and filling greedily, we ensure the most valuable options are exploited first, leaving the capacity limit to cut off only the least valuable items.
* **Mistakes Made:** We sorted by total units per box type (`numBoxes * unitsPerBox`) instead of by `unitsPerBox` (density). This is incorrect because we can take partial quantities of each box type — a large quantity of low-density boxes may have a high total but a low per-unit value, and partial selection at the boundary must favour the highest density.
* **What I Learned:** When capacity can be filled partially from any item type, always sort by value per unit (density). Sorting by total value assumes you must take entire quantities — which is a completely different problem (0/1 knapsack) that greedy cannot solve optimally. Density sort is the greedy solution to the fractional (or partially-selectable) knapsack.

---

### Master Patterns Learned

#### 1. Two-Pass Bilateral Constraint Propagation (The Directional Decoupling Frame)
* **Applied to:** Candy
* **The Strategy:** Initialise all values to their minimum (usually 1). Pass 1 sweeps left to right, propagating left-neighbour constraints forward. Pass 2 sweeps right to left, propagating right-neighbour constraints backward using `max` to preserve Pass 1 results. Sum the final array.
* **The Conceptual Mechanics:**
  - **Directional Independence:** Left-to-right constraints and right-to-left constraints form two independent DAGs along the same array. Solving each direction in isolation and combining via `max` produces the unique minimum solution satisfying both.
  - **Max Preservation:** The `max` in Pass 2 is non-negotiable. It ensures that a value established in Pass 1 (because of a left-neighbour constraint) is never reduced by the right-neighbour correction in Pass 2.
* **The Layout / Code Pattern:**
```python
def candy(ratings: list[int]) -> int:
    n = len(ratings)
    candies = [1] * n
    for i in range(1, n):                             # Pass 1: L -> R
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):                   # Pass 2: R -> L
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return sum(candies)
```

#### 2. Two-Pointer Boundary Exchange (The Running Maximum Exchange Frame)
* **Applied to:** Bag of Tokens
* **The Strategy:** Sort the collection. Use `lo` and `hi` pointers. Buy (consume one resource, gain another) from the cheapest end; sell (consume the gained resource, recover the first) from the most expensive end. Track the running maximum of the gained resource throughout.
* **The Conceptual Mechanics:**
  - **Boundary Optimality:** When buying, the cheapest token minimises cost per unit of gain. When selling, the most expensive token maximises recovery per unit of loss. Any interior exchange is strictly dominated.
  - **Running Maximum Necessity:** Selling reduces the gained resource below its peak. The terminal state can be lower than the peak. The answer is always `max_score`, never `final_score`.
* **The Layout / Code Pattern:**
```python
def bag_of_tokens_score(tokens: list[int], power: int) -> int:
    tokens.sort()
    lo, hi = 0, len(tokens) - 1
    score = max_score = 0
    while lo <= hi:
        if power >= tokens[lo]:
            power -= tokens[lo]; score += 1
            max_score = max(max_score, score); lo += 1
        elif score > 0:
            power += tokens[hi]; score -= 1; hi -= 1
        else:
            break
    return max_score
```

#### 3. Density Sort Capacity Fill (The Fractional Knapsack Frame)
* **Applied to:** Maximum Units on a Truck
* **The Strategy:** Sort items by value-per-unit-of-capacity (density) descending. Sweep and greedily take as many units of each item type as the remaining capacity allows. Stop when capacity is full.
* **The Conceptual Mechanics:**
  - **Density as Currency:** Each unit of capacity is equally precious. Spending it on the highest-density item maximises returns. When capacity runs out, it cuts off only the lowest-density items — exactly the ones we want to exclude.
  - **Partial Selection Validity:** Density sort works because we can take partial quantities of any item type. If items were all-or-nothing (0/1 knapsack), greedy would fail and DP would be required.
* **The Layout / Code Pattern:**
```python
def maximum_units(box_types: list[list[int]], truck_size: int) -> int:
    box_types.sort(key=lambda x: x[1], reverse=True)   # Sort by units/box desc
    total_units = 0
    for num_boxes, units_per_box in box_types:
        take = min(num_boxes, truck_size)
        total_units += take * units_per_box
        truck_size -= take
        if truck_size == 0:
            break
    return total_units
```
