# Reachability Greedy

## 1. What is Reachability Greedy?

Reachability Greedy is the family of problems where the core question is not "what is the optimal value?" but rather **"can you get there from here?"** — and if so, **how few moves does it take?**

What makes these problems challenging is that progress is self-referential: the positions you can reach from index `i` depend on the value at `i`, and those positions then determine what you can reach next. A naive brute-force DFS treats every position as a branching node and explores every possible jump path, building an exponential decision tree that revisits the same positions repeatedly.

The greedy insight that collapses this tree is: **the exact sequence of jumps taken to reach a position is irrelevant — only the furthest reachable frontier matters**. Once we accept that identity, the entire tree reduces to a single rolling scalar tracking the farthest reachable index at any point in the sweep. This scalar is called `max_reach`, and it is the foundation of all reachability greedy.

---

## 2. The Maximum Reach Invariant

The engine of reachability greedy is maintaining one invariant across a single left-to-right sweep: `max_reach` — the furthest index reachable from any position we have passed through.

At each position `i`, exactly one of two things is true:

*   `i > max_reach`: Position `i` is unreachable. No jump from any earlier position could land here. Since reachability is monotone — if position `i` is unreachable, everything beyond it is also unreachable — we can immediately terminate and return `False`.
*   `i <= max_reach`: We can stand at `i`. Update `max_reach = max(max_reach, i + nums[i])`. This greedily extends the frontier as far as the current position allows.

The proof that this is correct: if any position within `[0, max_reach]` is reachable, then by a sequence of steps through that interval, we can reach `max_reach`. We never need to reconstruct the actual path — only the boundary of what is reachable.

---

## 3. Implicit BFS Level Counting

Jump Game II extends the reachability problem: instead of asking *can* you reach the end, it asks *how few jumps* does it take? The optimal structure here is Breadth-First Search — each BFS layer corresponds to one jump. However, a queue-based BFS on this problem requires $O(N)$ memory and processes each position multiple times.

The greedy insight is that BFS layers can be tracked implicitly with two scalars:

*   `current_end` — the right boundary of the current BFS layer (the farthest position reachable with the number of jumps used so far).
*   `farthest` — the right boundary of the next BFS layer (the farthest position reachable with one additional jump).

As we sweep left to right, we update `farthest` continuously. When `i == current_end`, the current layer is exhausted — we are forced to make one more jump to go further. At that point, we increment the jump count and advance `current_end = farthest`. This implicit counting eliminates the queue entirely and runs in $O(N)$ time with $O(1)$ space.

---

## 4. The Circular Tour Invariant

The Gas Station problem introduces a structural twist: you must complete a **closed circular route**, meaning every prefix of the journey must maintain a non-negative running fuel surplus. This is not a simple reachability problem — it is a circular feasibility problem.

The **Total Surplus Theorem** resolves it: if the total gas across all stations is greater than or equal to the total cost, a valid starting station always exists. Existence is guaranteed by the global condition; finding it requires the local reset rule.

The local rule: sweep left to right maintaining `current_surplus`. Whenever `current_surplus` drops below zero at station `i`, the current start candidate cannot complete the circuit — neither can any station between the current start and `i`. Reset the start to `i + 1` and reset `current_surplus = 0`. If the global surplus is non-negative, the final `start` value is the answer.

Why the reset is valid: if starting at `s` and reaching station `f` causes a negative surplus, then starting at any station between `s` and `f` enters the problematic segment with less fuel than starting at `s` (because it skips the surplus accumulated from `s` to that point). All intermediate candidates fail. The only valid candidate is `f + 1`.

---

## 5. Generic Reachability Template

```python
def max_reach_greedy(nums: list[int]) -> bool:
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False            # Unreachable: stuck before index i
        max_reach = max(max_reach, i + nums[i])
    return True


def implicit_bfs_min_jumps(nums: list[int]) -> int:
    jumps = 0
    current_end = 0
    farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:       # Layer exhausted: commit to one more jump
            jumps += 1
            current_end = farthest
    return jumps
```

---

## Problem: Jump Game

* **Problem Type:** Reachability Greedy / Boolean Feasibility
* **Data Structure Used:** Single scalar `max_reach` (`int`)
* **Approach 1:** DFS/BFS from index 0, treating every position as a branching node and exploring every possible jump path. The worst-case branching factor is `max(nums)`, leading to $O(2^N)$ time.
* **Optimized Approach:** Maximum Reach Scalar Sweep. Maintain `max_reach = 0`. Loop left to right. At each index `i`, if `i > max_reach`, the position is unreachable — return `False`. Otherwise, update `max_reach = max(max_reach, i + nums[i])`. After the loop, return `True` if `max_reach >= last_index`.
* **Complexity:**
  * **Time:** $O(N)$ — a single linear left-to-right pass through the array.
  * **Space:** $O(1)$ — one scalar variable irrespective of input size.
* **Pointer Flow:**
```text
nums = [2, 3, 1, 1, 4]

i=0: 0 <= 0. max_reach = max(0, 0+2) = 2.
i=1: 1 <= 2. max_reach = max(2, 1+3) = 4.
i=2: 2 <= 4. max_reach = max(4, 2+1) = 4.
i=3: 3 <= 4. max_reach = max(4, 3+1) = 4.
i=4: 4 <= 4. max_reach = max(4, 4+4) = 8.
Last index = 4 <= max_reach = 8 -> True.

nums = [3, 2, 1, 0, 4]

i=0: max_reach = 3.
i=1: max_reach = max(3, 3) = 3.
i=2: max_reach = max(3, 3) = 3.
i=3: max_reach = max(3, 3) = 3.
i=4: 4 > max_reach(3) -> Unreachable -> False.
```
* **Pattern Recognition:**
  * Use the max_reach scalar whenever:
    - The problem asks whether the end of an array or some target index is reachable via variable-length jumps.
    - The exact sequence of jumps does not matter — only the maximum possible reach at each position.
* **Core Insight:** Reachability is a frontier problem, not a path problem. The moment you stop asking "which exact path reaches the destination?" and start asking "what is the farthest boundary I can push from here?", the exponential search tree collapses to a single scalar sweep. The key property that enables this is monotonicity: if you can reach position `i`, the maximum reach from all positions up to `i` is already encoded in `max_reach`.
* **Mistakes Made:** We simulated explicit jumps by building a visited set and stepping through each reachable position from the current one — effectively BFS without a queue. While conceptually correct, this is $O(N \cdot \text{max jump})$ in the worst case. The scalar `max_reach` eliminates redundant revisits entirely.
* **What I Learned:** Reachability is not a path-finding problem — it is a boundary-tracking problem. The distinction determines whether you write BFS ($O(N^2)$) or a scalar sweep ($O(N)$).

---

## Problem: Jump Game II

* **Problem Type:** Reachability Greedy / Minimum Jump Counting
* **Data Structure Used:** Three scalars: `jumps`, `current_end`, `farthest`
* **Approach 1:** BFS with an explicit queue. Initialize the queue with index 0. At each BFS layer, process all positions in the current layer, compute their reach, and enqueue newly reachable positions. Layer count = minimum jumps. Time: $O(N)$, Space: $O(N)$ for the queue.
* **Optimized Approach:** Implicit BFS Layer Tracking. Instead of a queue, track `current_end` (the right boundary of the current BFS layer) and `farthest` (the maximum reach seen within this layer). Sweep from 0 to `n-2`. At every step, update `farthest = max(farthest, i + nums[i])`. When `i == current_end`, the current layer is fully explored — increment `jumps` and advance `current_end = farthest`.
* **Complexity:**
  * **Time:** $O(N)$ — a single forward sweep ending at index `n-2` (the last index needs no jump from it).
  * **Space:** $O(1)$ — three scalar variables only.
* **Pointer Flow:**
```text
nums = [2, 3, 1, 1, 4]

jumps=0, current_end=0, farthest=0

i=0: farthest = max(0, 0+2) = 2.
     i == current_end(0) -> jumps=1, current_end=2.
i=1: farthest = max(2, 1+3) = 4.
i=2: farthest = max(4, 2+1) = 4.
     i == current_end(2) -> jumps=2, current_end=4.
i=3: farthest = max(4, 3+1) = 4.
Loop ends (stop at n-2=3). Answer: 2 jumps.
```
* **Pattern Recognition:**
  * Use implicit BFS layer counting when:
    - The problem requires the minimum number of discrete moves to traverse a sequence.
    - Each position provides variable-length moves, and all moves within a single jump count are equivalent in cost.
* **Core Insight:** Jump Game II is BFS without the queue. The `current_end` scalar serves as the layer boundary, and `farthest` serves as the next layer's boundary. Committing to a new jump when `i == current_end` is identical to dequeuing an entire BFS layer and starting the next. The queue is implicit in the boundary scalars — all positions within `[prev_end+1, current_end]` form exactly one BFS layer.
* **Mistakes Made:** We incremented the jump counter every time `farthest` improved (i.e., every time we found a position with a better reach). This over-counts because multiple positions within the same BFS layer can all extend the frontier, but they all cost the same single jump.
* **What I Learned:** Minimum-moves problems on linear arrays are implicit BFS problems. The BFS layer boundary — not the individual position — is what determines when a jump is taken. Tracking the boundary with a scalar is strictly superior to maintaining an explicit queue.

---

## Problem: Gas Station

* **Problem Type:** Circular Feasibility / Greedy Starting Point Detection
* **Data Structure Used:** Three scalars: `total_surplus`, `current_surplus`, `start`
* **Approach 1:** Brute-force simulation. For each station `i`, simulate the complete circular route beginning at `i`. Return `i` if the route completes without running out of gas. Time: $O(N^2)$. Space: $O(1)$.
* **Optimized Approach:** Two-Condition Single Pass. Accumulate `total_surplus += gas[i] - cost[i]` throughout the entire loop (global feasibility check). Simultaneously track `current_surplus`. When `current_surplus < 0`, the current start candidate is invalid — reset `start = i + 1` and `current_surplus = 0`. After the loop: if `total_surplus < 0`, return -1 (globally infeasible). Otherwise, return `start`.
* **Complexity:**
  * **Time:** $O(N)$ — one pass accumulating both global and local surplus simultaneously.
  * **Space:** $O(1)$ — three integer scalars.
* **Pointer Flow:**
```text
gas  = [1, 2, 3, 4, 5]
cost = [3, 4, 5, 1, 2]

total=0, current=0, start=0

i=0: net=-2. total=-2, current=-2. current<0 -> start=1, current=0.
i=1: net=-2. total=-4, current=-2. current<0 -> start=2, current=0.
i=2: net=-2. total=-6, current=-2. current<0 -> start=3, current=0.
i=3: net=+3. total=-3, current=3.
i=4: net=+3. total=0, current=6.

total=0 >= 0 -> feasible. Answer: start = 3.
```
* **Pattern Recognition:**
  * Use the single-pass circular feasibility sweep when:
    - The problem involves completing a circular traversal where each node provides some resource and consumes some resource.
    - The question is whether any starting point exists that keeps the running balance non-negative throughout the circuit.
* **Core Insight:** Two independent facts are combined into one sweep: (1) global feasibility — total gas >= total cost means a valid start exists; (2) local start detection — reset the candidate start whenever the running surplus drops negative. These two checks are decoupled: the reset logic correctly identifies the start even while the global surplus is still accumulating a negative intermediate value. The key insight is that if starting at `s` fails at `f`, starting at any station between `s` and `f` fails even earlier because it begins the problematic segment with less accumulated fuel.
* **Mistakes Made:** We ran the global feasibility check (`sum(gas) >= sum(cost)`) as a separate preliminary pass, then ran the start-detection as a second pass. These can be collapsed into a single sweep because the two accumulators (`total_surplus` and `current_surplus`) are completely independent of each other.
* **What I Learned:** Circular problems often have a global condition (total feasibility) that is independent of the local detection logic (which start is valid). Combining them into one pass requires recognizing that the local reset does not interfere with the global accumulator.

---

### Master Patterns Learned

#### 1. Maximum Reach Scalar (The Frontier Tracking Frame)
* **Applied to:** Jump Game
* **The Strategy:** Replace path-based BFS/DFS with a single scalar `max_reach` tracking the farthest reachable index from any position visited so far. Sweep left to right. At each position, if it exceeds `max_reach`, the answer is unreachable. Otherwise, update the frontier.
* **The Conceptual Mechanics:**
  - **Frontier Monotonicity:** Once a position is within the reachable frontier, all intermediate positions are also reachable. The frontier can only expand — never contract. This monotone property makes the scalar a complete representation of reachable state.
  - **Path Irrelevance:** Reachability doesn't require knowing which path was taken — only that the destination index lies within the current frontier. Discarding path information collapses $O(2^N)$ to $O(N)$.
* **The Layout / Code Pattern:**
```python
def max_reach_feasibility(nums: list[int]) -> bool:
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False                      # Position unreachable: frontier passed
        max_reach = max(max_reach, i + nums[i])  # Greedily expand the frontier
    return True
```

#### 2. Implicit BFS Layer Counting (The Jump Window Frame)
* **Applied to:** Jump Game II
* **The Strategy:** Replace an explicit BFS queue with two scalars — `current_end` (current layer boundary) and `farthest` (next layer boundary). Increment jump count every time the sweep reaches the current layer boundary. Advance the boundary to `farthest`.
* **The Conceptual Mechanics:**
  - **Layer Equivalence:** All positions within `[prev_boundary+1, current_end]` are reachable in the same number of jumps. They form a single BFS layer. No queue is needed to group them — their shared boundary scalar serves the same purpose.
  - **Greedy Optimality:** Within a layer, we always extend `farthest` as far as possible. A shorter reach within the same layer would only reduce options in the next layer, never help.
* **The Layout / Code Pattern:**
```python
def implicit_bfs_min_jumps(nums: list[int]) -> int:
    jumps = 0
    current_end = 0
    farthest = 0
    for i in range(len(nums) - 1):         # Last index needs no jump from it
        farthest = max(farthest, i + nums[i])
        if i == current_end:               # Current BFS layer exhausted
            jumps += 1
            current_end = farthest
    return jumps
```

#### 3. Circular Feasibility Reset (The Surplus Drain & Reset Frame)
* **Applied to:** Gas Station
* **The Strategy:** Sweep once, maintaining two accumulators: `total_surplus` (global check) and `current_surplus` (local start detection). Reset `current_surplus` and advance `start` whenever the running balance goes negative. After the sweep, check the global condition.
* **The Conceptual Mechanics:**
  - **Cascading Failure:** When `current_surplus < 0` at station `i`, all stations from the previous `start` up to `i` are proven invalid. The next candidate is `i + 1` — the station immediately after the point of failure.
  - **Global-Local Decoupling:** The total surplus accumulator and the local surplus accumulator are fully independent. Resetting `current_surplus` does not corrupt `total_surplus`, allowing both checks to coexist in a single pass.
* **The Layout / Code Pattern:**
```python
def find_gas_station_start(gas: list[int], cost: list[int]) -> int:
    total_surplus = 0
    current_surplus = 0
    start = 0
    for i in range(len(gas)):
        net = gas[i] - cost[i]
        total_surplus += net
        current_surplus += net
        if current_surplus < 0:          # Current start candidate fails here
            start = i + 1               # Reset: next candidate is i+1
            current_surplus = 0
    return start if total_surplus >= 0 else -1
```
