# Interval Greedy

## 1. What is Interval Greedy?

Interval problems present us with a collection of ranges on a timeline, each defined by a `[start, end]` pair. The task varies by problem — merge overlapping ranges into the fewest non-overlapping regions, remove the minimum number of intervals so no two conflict, insert a new interval without creating gaps, or partition a string into the smallest number of non-overlapping segments. Despite their surface diversity, every interval problem is fundamentally solved by the same two-step framework: **choose the right sort key**, then **sweep linearly and make one local decision per interval**.

The reason greedy works so powerfully on intervals is that once the right sort key is established, the global structure of the problem collapses into a locally deterministic sequence. The decision at each step depends only on the current interval and one tracked variable — never on future intervals or alternative choices. This is the definition of greedy applicability.

---

## 2. Sorting by Start vs. End — The Master Decision

The most consequential design choice in any interval problem is whether to sort by start time or by end time. This choice encodes the entire greedy strategy, and choosing the wrong direction produces silently incorrect results on specific inputs.

**Sort by start time** when the objective is to **combine or coalesce** intervals. Processing in order of their left boundary guarantees that consecutive intervals in the sorted order are the only pairs that can possibly share an overlap zone. Intervals far apart in sorted order cannot overlap because their left boundaries are far apart. This makes merging a simple one-pass decision: if `current_interval.start <= running_end`, they share overlap and we extend the boundary; otherwise we finalize the current region and begin a new one.

**Sort by end time** when the objective is to **maximize the number of non-overlapping selections** or **minimize the number of removals/arrows**. The Earliest Finish Time First (EFTF) heuristic drives this: by always selecting the interval that completes soonest, we free the maximum possible timeline for future selections. This greedy choice is provably optimal by the exchange argument — swapping a later-finishing interval for an earlier one can only help, never hurt.

Mixing up these two sort directions produces incorrect results because they encode fundamentally different geometric objectives.

---

## 3. The Sweep Line Technique

The sweep line is the mechanical backbone of all interval greedy. Conceptualize a vertical line that sweeps left to right across the timeline. As it crosses each interval's start or end point, it executes one decision:

*   **Start event encountered:** Should we open/extend/track a new region?
*   **End event encountered:** Should we close the current region?

After sorting, the decision at each event depends only on two things: the current event and the current state of the sweep (the last active boundary, the partition tracker, or the arrow position). No future events can alter this decision. This local independence is what makes the sweep greedy-complete.

---

## 4. Last Occurrence Window Expansion

Partition Labels introduces a third interval pattern that operates differently from start/end sorting. Here, the intervals are not provided — they are **implied by character constraints**. Every character must appear entirely within one partition, and the boundary of a partition is forced by the last occurrence of any character seen within it.

The greedy resolution is a two-pass window expansion strategy: pre-compute the last occurrence of each character in one pass, then sweep and expand the current partition's boundary dynamically as characters with later last-occurrences are encountered. The moment the sweep index matches the current boundary, the partition cannot extend further — it closes, and a new one begins.

---

## Problem: Partition Labels

* **Problem Type:** Last-Occurrence Window Expansion / Dynamic Partition Boundary
* **Data Structure Used:** Hash Map (`dict[char, int]` for last occurrence) + two boundary scalars `start`, `end`
* **Approach 1:** For every possible partition point, verify that no character appears both inside and outside the partition by scanning forward and backward. This is $O(N^2)$ per candidate point, producing $O(N^3)$ overall.
* **Optimized Approach:** Two-Pass Last-Occurrence Window Expansion. In the first pass, record the last index of every character in a hash map (`last[char] = i`). In the second pass, sweep left to right. At each character `c`, extend the current partition boundary: `end = max(end, last[c])`. When `i == end`, no character within `[start, end]` appears after position `end` — the partition is complete. Record `end - start + 1` as the partition size, then advance `start = end + 1`.
* **Complexity:**
  * **Time:** $O(N)$ — two linear passes; the hash map holds at most 26 entries for a fixed lowercase alphabet.
  * **Space:** $O(1)$ — the character frequency map is bounded by the fixed alphabet size, independent of input length.
* **Pointer Flow:**
```text
s = "ababcbacadefegdehijhklij"
last = {a:8, b:5, c:7, d:14, e:15, f:11, g:13, h:19, i:22, j:23, k:20, l:21}

start=0, end=0
i=0 'a': end=max(0,8)=8.
i=1 'b': end=max(8,5)=8.
i=2 'a': end=max(8,8)=8.
...
i=8 'a': end=max(8,8)=8. i==end -> partition [0..8], size=9. start=9, end=9.
i=9 'd': end=max(9,14)=14.
...
i=15 'e': i==end=15 -> partition [9..15], size=7. start=16, end=16.
...
i=23 'j': i==end=23 -> partition [16..23], size=8. start=24.
Output: [9, 7, 8]
```
* **Pattern Recognition:**
  * Use last-occurrence window expansion when:
    - Each element must appear entirely within a single partition, and no element can span multiple partition boundaries.
    - The partition boundary is not given explicitly but must be inferred from element constraint properties (last occurrence, last required position, etc.).
* **Core Insight:** The boundary of each partition is not a choice — it is a forced constraint. Once a character with a later last-occurrence is encountered, the partition cannot close earlier than that last occurrence. The window expansion algorithm encodes this forcing: `end = max(end, last[char])` is a mandatory extension, not a preference. The only moment we have actual freedom is when `i == end` — at that point, no constraint forces an extension, so we are allowed (and obligated) to close.
* **Mistakes Made:** We attempted to identify partition boundaries by scanning backward from each candidate closing position to verify that all characters appeared earlier. This double scan is $O(N^2)$. Precomputing last occurrences in a single forward pass eliminates all backward scanning.
* **What I Learned:** When a partition problem constrains elements to appear entirely within one region, pre-compute the "last anchor point" of each element type. The window boundary is then the maximum of all last anchor points of elements seen so far — a dynamic maximum that reveals itself in a single forward sweep.

---

## Problem: Merge Intervals

* **Problem Type:** Start-Time Sort / Sequential Region Coalescing
* **Data Structure Used:** Sorted 2D array of intervals + result list
* **Approach 1:** For every pair of intervals, check if they overlap and merge them. Repeat until no more merges can be performed. This requires $O(N^2)$ pairwise comparisons per pass and up to $O(N)$ passes in the worst case, giving $O(N^3)$.
* **Optimized Approach:** Sort by start time, then execute a single-pass coalesce sweep. Initialize a result list with the first interval. For each subsequent interval, check if its start is less than or equal to the end of the last interval in the result. If yes, extend the last interval's end to `max(last_end, current_end)`. If no, the current interval is entirely separate — append it to the result.
* **Complexity:**
  * **Time:** $O(N \log N)$ — dominated by the sort; the subsequent merge sweep is $O(N)$.
  * **Space:** $O(N)$ — the result list holds at most $N$ non-overlapping merged intervals.
* **Pointer Flow:**
```text
intervals = [[1,3],[2,6],[8,10],[15,18]]
Sorted by start: [[1,3],[2,6],[8,10],[15,18]]

result = [[1,3]]
[2,6]:   2 <= 3 -> overlap -> extend: result = [[1,6]]
[8,10]:  8 >  6 -> no overlap -> append: result = [[1,6],[8,10]]
[15,18]: 15 > 10 -> no overlap -> append: result = [[1,6],[8,10],[15,18]]
```
* **Pattern Recognition:**
  * Use start-time sorted coalesce sweep when:
    - The problem requires combining all overlapping intervals into the minimum number of non-overlapping regions.
    - The result must preserve all covered ranges with no gaps and no duplicates.
* **Core Insight:** Sorting by start time transforms the overlap detection problem from a 2D pairwise comparison into a 1D adjacency check. After sorting, an interval can only overlap with the immediately preceding merged region (because its start is the earliest among all remaining intervals). No earlier-in-list interval can retroactively create an overlap. Therefore, one comparison per interval — `current.start <= result.last.end` — is sufficient to resolve the entire merging decision.
* **Mistakes Made:** We sorted by end time instead of start time. When sorted by end, an interval with a very late start might overlap with a previously finalized region that was already committed to the result list, requiring backward correction that the algorithm does not support.
* **What I Learned:** The sort key completely encodes the directional relationship exploited by the sweep. Start-sort enables forward coalescing. End-sort enables backward pruning. These are geometrically opposite operations, and the sort key must match the operation.

---

## Problem: Insert Interval

* **Problem Type:** Pre-Sorted Interval Insertion / Three-Phase Sweep-and-Merge
* **Data Structure Used:** Input interval list (pre-sorted by start) + result list
* **Approach 1:** Insert the new interval into the list, re-sort the entire list, then run standard Merge Intervals. Time: $O(N \log N)$ due to re-sorting.
* **Optimized Approach:** Three-Phase Sweep exploiting the pre-sorted structure. Phase 1 — collect all intervals that end before the new interval starts (no overlap possible): `end < newInterval.start`. Phase 2 — merge all intervals that overlap with the new interval: `start <= newInterval.end`. At each overlapping interval, expand the new interval's boundaries: `newInterval = [min(new.start, cur.start), max(new.end, cur.end)]`. Phase 3 — append all remaining intervals unchanged.
* **Complexity:**
  * **Time:** $O(N)$ — a single linear pass through the pre-sorted list; no sorting required.
  * **Space:** $O(N)$ — the result list.
* **Pointer Flow:**
```text
intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]

Phase 1 (end < 4): [1,2]: 2<4 -> add. [3,5]: 5>=4 -> stop.
result = [[1,2]]

Phase 2 (start <= 8):
  [3,5]: 3<=8 -> new=[min(4,3),max(8,5)]=[3,8].
  [6,7]: 6<=8 -> new=[min(3,6),max(8,7)]=[3,8].
  [8,10]: 8<=8 -> new=[min(3,8),max(8,10)]=[3,10].
  [12,16]: 12>8 -> stop. Add [3,10].
result = [[1,2],[3,10]]

Phase 3: [12,16] -> result = [[1,2],[3,10],[12,16]]
```
* **Pattern Recognition:**
  * Use three-phase pre-sorted insertion when:
    - The input is already guaranteed to be sorted, making a re-sort wasteful.
    - The new element being inserted creates a contiguous overlap zone that can be identified and resolved in a single linear pass.
* **Core Insight:** The pre-sorted input is a structural gift that converts a logarithmic problem into a linear one. The overlapping intervals form a contiguous block in the sorted list — there is a definite entry point (when `end >= newInterval.start`) and a definite exit point (when `start > newInterval.end`). This block structure means no backward scanning is ever needed; the three phases map directly to three geometrically distinct zones of the timeline.
* **Mistakes Made:** We sorted the array after appending the new interval, which wastes the pre-sorted structure and introduces an unnecessary $O(N \log N)$ overhead. The problem guarantees sorted input precisely so that this linear solution is achievable.
* **What I Learned:** When the problem explicitly guarantees sorted input, always exploit that structure before considering a sort. A linear three-phase scan on a pre-sorted list is the canonical response to interval insertion problems.

---

## Problem: Non-Overlapping Intervals

* **Problem Type:** End-Time Sort / Maximum Non-Overlapping Selection (Activity Selection)
* **Data Structure Used:** Sorted 2D array of intervals + `prev_end` scalar
* **Approach 1:** Brute-force subset enumeration. Try every possible subset of intervals and verify that the selected subset is pairwise non-overlapping. Return the size of the maximum valid subset. Time: $O(2^N \cdot N)$.
* **Optimized Approach:** Activity Selection via End-Sort Sweep. Sort intervals by end time. Maintain `prev_end` (the end time of the last kept interval). For each interval: if its start >= `prev_end`, it does not overlap with the last kept interval — keep it and update `prev_end = current.end`. Otherwise, it overlaps — remove it (it has the later end time, since we are sorted by end) and keep `prev_end` unchanged. Count removals.
* **Complexity:**
  * **Time:** $O(N \log N)$ — dominated by sorting; the sweep is $O(N)$.
  * **Space:** $O(1)$ — one scalar `prev_end`.
* **Pointer Flow:**
```text
intervals = [[1,2],[2,3],[3,4],[1,3]]
Sorted by end: [[1,2],[2,3],[1,3],[3,4]]

prev_end=-inf, removals=0.
[1,2]:  1 >= -inf -> keep. prev_end=2.
[2,3]:  2 >= 2   -> keep. prev_end=3.
[1,3]:  1 <  3   -> overlaps. Remove it. removals=1.
[3,4]:  3 >= 3   -> keep. prev_end=4.

Answer: 1 removal (N - max_kept = 4 - 3 = 1).
```
* **Pattern Recognition:**
  * Use end-time sorted activity selection when:
    - The problem requires keeping or selecting the maximum number of non-overlapping intervals, or equivalently, removing the minimum number.
    - The greedy correctness rests on the Earliest Finish Time First exchange argument.
* **Core Insight:** When two intervals conflict, the one with the later end time is the one to remove. It extends further into the timeline, potentially blocking more future intervals than the earlier-ending one. Keeping the earlier-ending interval always leaves at least as much room for future selections — this is the exchange argument in action. Sorting by end time places this "better" interval first, making the sweep naturally select it without any comparison.
* **Mistakes Made:** We sorted by start time and tried to resolve conflicts by comparing interval durations, reasoning that shorter intervals block fewer future ones. This is incorrect — a short interval starting late may conflict with more future intervals than a long interval that ends early, because end time, not duration, determines what conflicts with what.
* **What I Learned:** In interval selection problems, the currency of value is not duration but end time. An interval that ends earlier is worth more — it frees more of the future timeline. End-time sorting makes this explicit and allows the sweep to always make the locally and globally optimal choice with a single comparison.

---

### Master Patterns Learned

#### 1. Last-Occurrence Window Expansion (The Dynamic Partition Boundary Frame)
* **Applied to:** Partition Labels
* **The Strategy:** Pre-compute the last occurrence index of every element in one pass. Then sweep and dynamically expand the partition boundary to `max(boundary, last[element])` at each step. Close the partition when the sweep index reaches the boundary.
* **The Conceptual Mechanics:**
  - **Forced Extension:** Every character encountered with a later last-occurrence mandatorily extends the boundary. There is no greedy "choice" — the extension is forced by the constraint that each character appears entirely within one partition.
  - **Closure Uniqueness:** The partition closes at the exact first moment when no character forces a further extension. This moment is unique and deterministic, making the partition size uniquely optimal.
* **The Layout / Code Pattern:**
```python
def partition_labels(s: str) -> list[int]:
    last = {char: i for i, char in enumerate(s)}    # Pre-compute last occurrences
    result = []
    start = end = 0
    for i, char in enumerate(s):
        end = max(end, last[char])                   # Forced extension
        if i == end:                                 # Partition closure moment
            result.append(end - start + 1)
            start = end + 1
    return result
```

#### 2. Start-Sort Coalesce Sweep (The Region Merging Frame)
* **Applied to:** Merge Intervals, Insert Interval
* **The Strategy:** Sort by start time. Maintain the current merged region's right boundary. For each interval: if it overlaps (start <= boundary), extend the boundary. If it doesn't, commit the region and start a new one.
* **The Conceptual Mechanics:**
  - **Adjacency Sufficiency:** After start-sort, overlap can only occur between consecutively positioned intervals in the sorted list. Checking only the current interval against the last committed region is necessary and sufficient.
  - **Right-Boundary Maximization:** When merging, always take `max(prev_end, cur_end)` because the incoming interval might be entirely contained within the current region (`cur_end < prev_end`), requiring no extension.
* **The Layout / Code Pattern:**
```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda x: x[0])              # Sort by start time
    result = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= result[-1][1]:                   # Overlapping: extend right boundary
            result[-1][1] = max(result[-1][1], end)
        else:                                        # Non-overlapping: commit and start new
            result.append([start, end])
    return result
```

#### 3. End-Sort Activity Selection (The Earliest Finish Sweep Frame)
* **Applied to:** Non-Overlapping Intervals, Minimum Arrows to Burst Balloons
* **The Strategy:** Sort by end time. Sweep left to right maintaining `prev_end`. Keep each interval if its start does not overlap `prev_end`. Skip/remove if it does. Always keep the earlier-ending interval when there is a conflict.
* **The Conceptual Mechanics:**
  - **Earliest Finish Optimality:** The exchange argument proves that replacing any kept interval with one that ends earlier is always non-worse. Sorting by end time makes the earliest-finishing interval in any conflict zone appear first, naturally selecting it without explicit comparison.
  - **Minimum Removals Equivalence:** Maximum selections = N - minimum removals. The end-sort sweep maximizes selections; subtracting from N gives minimum removals.
* **The Layout / Code Pattern:**
```python
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda x: x[1])              # Sort by end time (EFTF)
    prev_end = float('-inf')
    removals = 0
    for start, end in intervals:
        if start >= prev_end:                        # No overlap: keep this interval
            prev_end = end
        else:                                        # Overlap: remove later-ending one
            removals += 1                            # prev_end stays (earlier-ending kept)
    return removals
```
