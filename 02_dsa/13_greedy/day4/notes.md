# Scheduling Greedy & Frequency Ordering

## 1. What is Scheduling Greedy?

Scheduling problems place us in a world where we must arrange a set of items — people, tasks, cards — into a specific order or grouping that satisfies structural constraints. The objective is not merely to find *an* arrangement but the *best* one: the order that maximises throughput, minimises idle time, or forms the fewest number of groups.

What separates scheduling from interval problems is that scheduling usually requires us to place **all** elements, not just select a subset. The challenge shifts from "which elements should I keep?" to "in what order or grouping should I place everything?". The answer, in almost every scheduling problem, is rooted in one principle: **the most constrained element must be placed first**.

If the tallest person in a queue has a rigid constraint about how many people stand in front of them, they must be placed before shorter people (who have more flexible positions). If the most frequent task in a cooldown schedule defines the structural skeleton of the timeline, it should define the frame first and let all other tasks fill around it. If the smallest card must begin a consecutive straight, it must be the anchor before any larger cards are committed. In every case, the most constrained element has the least freedom, and processing it first eliminates ambiguity.

---

## 2. The Constraint Dominance Principle

The formal name for the core intuition is the **Constraint Dominance Principle**: when elements have ordering or grouping constraints relative to each other, process the element with the most restrictive constraint first. Placing less-constrained elements before more-constrained ones creates a situation where the most constrained element has nowhere valid to go — you are forced to rearrange backward, which is an $O(N^2)$ process. Processing in constraint-descending order from the start makes each element's placement immediately deterministic.

The exchange argument formalises this: if an optimal solution places a less-constrained element before a more-constrained one, swapping them produces an arrangement that is at least as good and is aligned with the greedy order. Therefore, the greedy order is always achievable without penalty.

---

## 3. The Frequency Frame Insight

Task Scheduler introduces a fundamentally different scheduling variant: temporal cooldown. Instead of positional constraints, we have a minimum gap between identical tasks. The brute force approach — simulate the scheduler step by step using a max-heap and a cooldown queue — produces the correct answer but at $O(N \log N)$ with substantial implementation complexity.

The deeper insight is that simulation is unnecessary. The **minimum possible timeline** can be derived mathematically from a single observation: the most frequent task is the bottleneck. It must appear $f$ times, separated by $n$ slots each time. This creates a rigid frame of $(f-1) \times (n+1)$ slots with $k$ additional tail slots (where $k$ is the number of tasks tied at maximum frequency). All other tasks fill into this frame's idle slots. If there are more tasks than idle slots, no idle time exists at all and the total time equals the task count. The minimum of these two cases is the answer.

---

## 4. The Minimum Anchor Principle

Hand of Straights introduces yet another variant: consecutive grouping. Each card must be assigned to a straight (a group of consecutive values). The critical observation is that the smallest currently available card cannot be the middle or end of a straight — it can only be the **start**. There is no smaller card available to precede it, making its anchor position uniquely forced.

The **Minimum Anchor Principle**: in consecutive grouping problems, always anchor the current group at the minimum available element. Once the anchor is fixed, the next $\text{groupSize}-1$ consecutive values must each be consumed exactly once to complete the straight. If any required value is missing or insufficient, the assignment is impossible.

---

## 5. Generic Scheduling Templates

```python
# Constraint Dominance — sort descending by constraint, insert at index k
def schedule_by_constraint(people):
    people.sort(key=lambda x: (-x[0], x[1]))   # Tallest first, smallest k first
    result = []
    for person in people:
        result.insert(person[1], person)         # Insert at position k
    return result


# Frequency Frame — closed-form minimum timeline calculation
def min_task_timeline(tasks, n):
    from collections import Counter
    freq = Counter(tasks)
    max_freq = max(freq.values())
    max_count = sum(1 for v in freq.values() if v == max_freq)
    return max(len(tasks), (max_freq - 1) * (n + 1) + max_count)


# Minimum Anchor — consecutive grouping via frequency map
def can_form_straights(hand, group_size):
    from collections import Counter
    counts = Counter(hand)
    for card in sorted(counts):
        if counts[card] > 0:
            for i in range(group_size - 1, -1, -1):
                counts[card + i] -= counts[card]
                if counts[card + i] < 0:
                    return False
    return True
```

---

## Problem: Queue Reconstruction by Height

* **Problem Type:** Constraint Dominance / Positional Insertion by Rank
* **Data Structure Used:** Sorted list with index-based insertion
* **Approach 1:** Try all $N!$ permutations and verify which satisfies all `k` constraints. Completely infeasible for any non-trivial $N$.
* **Optimized Approach:** Constraint Dominance Insertion. Sort people by height **descending** (tallest first), breaking ties by `k` **ascending** (smallest count first). Then insert each person into a result list at index `k`. Because all previously inserted people are taller than or equal to the current person, inserting at index `k` guarantees exactly `k` people of equal or greater height appear before them.
* **Complexity:**
  * **Time:** $O(N^2)$ — sorting is $O(N \log N)$; each list insertion is $O(N)$ due to shifting, for $N$ insertions total.
  * **Space:** $O(N)$ — the result list.
* **Pointer Flow:**
```text
people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
Sorted (desc height, asc k): [[7,0],[7,1],[6,1],[5,0],[5,2],[4,4]]

Insert [7,0] at 0 -> [[7,0]]
Insert [7,1] at 1 -> [[7,0],[7,1]]
Insert [6,1] at 1 -> [[7,0],[6,1],[7,1]]
Insert [5,0] at 0 -> [[5,0],[7,0],[6,1],[7,1]]
Insert [5,2] at 2 -> [[5,0],[7,0],[5,2],[6,1],[7,1]]
Insert [4,4] at 4 -> [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
```
* **Pattern Recognition:**
  * Use descending-priority insertion when:
    - Elements have a positional rank constraint that references elements of higher or equal magnitude.
    - The validity of placing a smaller element never depends on the positions of elements smaller than it (shorter people are "invisible" to taller people's constraints).
* **Core Insight:** Processing tallest people first isolates their constraints: when a tall person is inserted, no shorter person exists yet in the result to interfere with their count. Shorter people, inserted later, are invisible to the already-placed taller people because the `k` constraint only counts people of equal or greater height. Each subsequent insertion of a shorter person into position `k` is therefore guaranteed to be correct without disturbing any earlier insertions.
* **Mistakes Made:** We attempted to sort by height ascending, placing shorter people first. This fails because when we later insert a taller person, they push shorter people forward, invalidating already-satisfied `k` constraints for the previously placed shorter people.
* **What I Learned:** The insertion order in constraint satisfaction must respect the direction of influence. Taller people's constraints reference taller people — so taller people must be placed first. Shorter people's constraints are satisfied by their rank among taller people already placed.

---

## Problem: Task Scheduler

* **Problem Type:** Frequency Frame Optimisation / Closed-Form Timeline Minimisation
* **Data Structure Used:** Hash map (frequency counter) — no simulation required
* **Approach 1:** Simulate the scheduler step-by-step with a max-heap (for selecting the highest-frequency ready task) and a cooldown queue (for tracking tasks in cooldown). Each simulation step is $O(\log N)$ and runs for the total timeline duration, giving $O(\text{timeline} \cdot \log N)$ time.
* **Optimized Approach:** Mathematical Frequency Frame. Count task frequencies. Find `max_freq` (highest frequency) and `max_count` (number of tasks tied at that frequency). Compute `frame = (max_freq - 1) * (n + 1) + max_count`. The answer is `max(len(tasks), frame)`. The frame represents the structural skeleton imposed by the most frequent task; `len(tasks)` represents the case where all slots are filled with no idle time.
* **Complexity:**
  * **Time:** $O(N)$ — counting frequencies; the mathematical computation is constant time.
  * **Space:** $O(1)$ — at most 26 task types in a fixed uppercase alphabet.
* **Pointer Flow:**
```text
tasks = ["A","A","A","B","B","B"], n = 2
Counts: {A:3, B:3} -> max_freq=3, max_count=2

Frame = (3-1)*(2+1) + 2 = 6+2 = 8
Total tasks = 6
Answer: max(6, 8) = 8

Visualised layout:
[A, B, idle, A, B, idle, A, B]
 ^ slot 1    ^ slot 2    ^ tail (max_count=2)
```
* **Pattern Recognition:**
  * Use the frequency frame formula when:
    - A cooldown constraint prevents repeating the same task within `n` time units.
    - The objective is the minimum total time to complete all tasks, including mandatory idle slots.
* **Core Insight:** The most frequent task creates an unavoidable structural skeleton. It must appear `max_freq` times, and between each pair of consecutive appearances, at least `n` other units of work (or idle) must occur. This rigid structure produces `(max_freq - 1)` internal gaps of size `n + 1` (the `+1` is the task's own slot), plus a tail of `max_count` final appearances. Every other task is filler. If there are enough other tasks to eliminate all idle time, the total time is simply the task count.
* **Mistakes Made:** We implemented the full max-heap simulation before recognising the closed-form solution. The heap simulation is correct but involves significant implementation overhead with a cooldown queue, edge case handling for empty queues, and careful time-step management.
* **What I Learned:** Before writing a simulation, always ask whether a closed-form lower bound exists. Scheduling problems with uniform cooldowns almost always have a mathematical expression — the frequency frame — that is faster to compute and simpler to implement than the simulation equivalent.

---

## Problem: Hand of Straights

* **Problem Type:** Minimum Anchor / Consecutive Group Feasibility Check
* **Data Structure Used:** Counter (frequency map) + sorted unique keys
* **Approach 1:** Try all possible assignments of cards to straights using DFS. The branching factor at each step is the number of groups currently being formed, producing an exponential time complexity.
* **Optimized Approach:** Minimum Anchor Greedy. Count card frequencies with a Counter. Sort the unique card values. For each unique card value `c` in ascending order: if `counts[c] > 0`, this card must start exactly `counts[c]` new straights. For each of the next `groupSize - 1` cards (`c+1, c+2, ..., c+groupSize-1`), decrement their counts by `counts[c]`. If any required card has insufficient count, return `False`. If all cards are consumed, return `True`.
* **Complexity:**
  * **Time:** $O(U \log U + N)$ where $U$ = number of unique cards (sorting unique keys) and $N$ = total cards (building the counter). The sweep over unique keys is $O(U \cdot \text{groupSize})$.
  * **Space:** $O(U)$ — the frequency map.
* **Pointer Flow:**
```text
hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
Counts: {1:1, 2:2, 3:2, 4:1, 6:1, 7:1, 8:1}
Sorted keys: [1, 2, 3, 4, 6, 7, 8]

Key 1 (count=1): Start 1 straight [1,2,3]. Consume 1 each of {1,2,3}.
  -> Counts: {2:1, 3:1, 4:1, 6:1, 7:1, 8:1}
Key 2 (count=1): Start 1 straight [2,3,4]. Consume 1 each of {2,3,4}.
  -> Counts: {6:1, 7:1, 8:1}
Key 6 (count=1): Start 1 straight [6,7,8]. Consume 1 each of {6,7,8}.
  -> Counts: {} -> All consumed. Return True.
```
* **Pattern Recognition:**
  * Use minimum anchor greedy when:
    - Elements must form consecutive groups of fixed size `groupSize`.
    - The smallest available element is the only valid anchor for the current group (no smaller element exists to precede it).
* **Core Insight:** The minimum card has no smaller predecessor. It can only anchor a new straight — it cannot be the middle or end of any existing straight. This makes its assignment uniquely forced. Once the anchor is committed, the next `groupSize - 1` cards are also forced: exactly one copy of each must be consumed. The entire assignment is deterministic from the minimum card upward, leaving no choices to explore.
* **Mistakes Made:** We sorted the entire hand array and tried to build straights by iterating through elements and matching consecutive runs. Managing duplicates by tracking how many copies of each card remain in a raw sorted array is complex and error-prone. The Counter + sorted unique keys approach handles duplicates cleanly via frequency arithmetic.
* **What I Learned:** When elements must form consecutive sequences, operating on unique keys with frequency counts is far cleaner than operating on the raw duplicated array. The minimum anchor principle eliminates all ambiguity about which straight a card belongs to, converting an apparently combinatorial problem into a deterministic greedy sweep.

---

### Master Patterns Learned

#### 1. Constraint Dominance Insertion (The Descending Priority Placement Frame)
* **Applied to:** Queue Reconstruction by Height
* **The Strategy:** Sort by constraint magnitude descending. For elements tied in magnitude, sort by rank (position index) ascending. Insert each element into the result list at its rank index. Elements placed later have smaller magnitude and are invisible to the constraints of already-placed elements.
* **The Conceptual Mechanics:**
  - **Invisible Smaller Elements:** In positional rank problems, constraints reference elements of equal or greater magnitude. Smaller-magnitude elements placed later cannot invalidate the rank counts of larger-magnitude elements already placed.
  - **Rank Index Validity:** Because all previously placed elements are larger or equal, inserting at index `k` always creates exactly `k` larger-or-equal elements in front — the constraint is satisfied by construction.
* **The Layout / Code Pattern:**
```python
def reconstruct_queue(people: list[list[int]]) -> list[list[int]]:
    # Sort: tallest first (desc height), smallest k first (asc k) for ties
    people.sort(key=lambda x: (-x[0], x[1]))
    result = []
    for person in people:
        result.insert(person[1], person)     # Insert at index k
    return result
```

#### 2. Frequency Frame Calculation (The Skeleton Timeline Frame)
* **Applied to:** Task Scheduler
* **The Strategy:** Count element frequencies. Find the maximum frequency `f` and the count of elements tied at `f`. Compute the structural frame `(f-1)*(n+1) + max_count`. The answer is `max(total_elements, frame)`. No simulation needed.
* **The Conceptual Mechanics:**
  - **Skeleton Dominance:** The most frequent element creates a rigid frame that all other elements must fill around. The frame size is determined entirely by this single element — everything else is filler.
  - **Idle Elimination:** If total tasks exceed the frame size (enough filler to eliminate all idle slots), the answer is simply the total task count. The frame is then a non-binding lower bound.
* **The Layout / Code Pattern:**
```python
def least_interval(tasks: list[str], n: int) -> int:
    from collections import Counter
    freq = Counter(tasks)
    max_freq = max(freq.values())
    max_count = sum(1 for v in freq.values() if v == max_freq)
    frame = (max_freq - 1) * (n + 1) + max_count
    return max(len(tasks), frame)
```

#### 3. Minimum Anchor Grouping (The Consecutive Forcing Frame)
* **Applied to:** Hand of Straights
* **The Strategy:** Build a frequency map. Sort unique keys. For each key in ascending order, if it has remaining count, it must anchor exactly that many new groups. Consume one copy of each of the next `groupSize-1` consecutive values. Fail immediately if any required value is missing.
* **The Conceptual Mechanics:**
  - **Uniqueness of Anchor:** The minimum card with positive count has no valid predecessor — it cannot join any existing in-progress straight. Its assignment as a new straight anchor is forced.
  - **Cascade Consumption:** Once the anchor count is determined, the consumption of the next consecutive values is fully determined. There are no choices to make — only verification that the required cards exist.
* **The Layout / Code Pattern:**
```python
def is_n_straight_hand(hand: list[int], group_size: int) -> bool:
    from collections import Counter
    counts = Counter(hand)
    for card in sorted(counts):
        if counts[card] > 0:
            count = counts[card]
            for i in range(group_size):
                counts[card + i] -= count
                if counts[card + i] < 0:
                    return False
    return True
```
