# Resource Allocation Greedy

## 1. What is Resource Allocation Greedy?

Resource allocation problems ask: given a collection of demands — meetings, trains, or jobs — that each require exclusive use of some resource (a room, a platform, a machine) for a fixed duration, what is the **minimum number of identical resources** needed to serve all demands without conflict?

This is a fundamentally different question from interval scheduling, which asks which demands to *keep*. Resource allocation assumes we must serve *all* demands and simply wants to know how many parallel resources are required. The answer is mathematically precise: it is the maximum number of demands simultaneously active at any single point in time — the **peak concurrency depth**.

$$\text{minimum resources} = \max_{t} |I_t|$$

where $|I_t|$ is the number of intervals active at time $t$. The entire problem reduces to finding this maximum.

---

## 2. The Peak Concurrency Insight

The reason greedy solves this so cleanly is a deeper observation: all resources are functionally identical. A meeting assigned to Room A versus Room B produces exactly the same outcome. This means we never need to track which specific resource a demand is assigned to — only whether *any* free resource exists at the moment a new demand begins.

This abstraction collapses the entire assignment problem into a single scalar question: at each new demand's start time, is there a currently free resource? The answer is determined by the earliest-ending currently active demand. If the earliest-ending active demand finishes before the new one starts, that resource is free to reuse. Otherwise, a new resource must be opened.

A **min-heap of end times** answers this question in $O(\log N)$ per demand:
*   **Heap top end time ≤ new demand's start:** A resource is free — pop the heap, update the end time, push it back (or simply push the new end time to the already-popped slot).
*   **Heap top end time > new demand's start:** No resource is free — push the new demand's end time (opening a new resource). The heap grows by one.

The heap size at any moment equals the number of simultaneously active demands. Its peak size equals the minimum resources needed.

---

## 3. The Two-Pointer Alternative

When arrivals and departures are given as two separate sorted arrays (common in platform/train problems), the same peak-concurrency answer can be computed without a heap. Instead, model arrivals and departures as two independent event streams and sweep through them with two pointers.

*   If the next event is an arrival (arrival time ≤ departure time): a new resource is consumed — increment the active count.
*   If the next event is a departure (departure time < arrival time): a resource is freed — decrement the active count.
*   Track the maximum active count throughout.

This produces the same answer as the heap but uses $O(1)$ extra space after sorting and avoids heap operations entirely. The critical difference: when arrival time equals departure time, process the departure first (a room freed at time $t$ can be reused at time $t$).

---

## 4. Why Greedy is Provably Optimal

The formal proof combines a lower and upper bound:

**Lower Bound:** At the moment of peak concurrency $d$, there are $d$ demands simultaneously active. No two can share a resource (they are in conflict). Therefore, we need **at least** $d$ resources.

**Upper Bound:** Our algorithm opens a new resource only when every existing resource is occupied — precisely when there are already $d$ active demands. Therefore, the algorithm opens **at most** $d$ resources.

Since lower and upper bounds both equal $d$, the algorithm is exactly optimal. No other algorithm can do better than $d$ resources, and our algorithm never uses more than $d$.

---

## 5. Generic Resource Allocation Templates

```python
import heapq

# Min-Heap Template (Meeting Rooms II)
def min_resources_heap(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda x: x[0])     # Sort by start time
    heap = []                               # Min-heap of active end times
    for start, end in intervals:
        if heap and heap[0] <= start:       # A resource becomes free
            heapq.heapreplace(heap, end)    # Reuse it: update its end time
        else:
            heapq.heappush(heap, end)       # No free resource: open a new one
    return len(heap)


# Two-Pointer Template (Minimum Platforms)
def min_resources_two_pointer(arrivals: list[int], departures: list[int]) -> int:
    arrivals.sort()
    departures.sort()
    platforms = max_platforms = 0
    i = j = 0
    while i < len(arrivals):
        if arrivals[i] <= departures[j]:   # Arrival comes first (or tie)
            platforms += 1
            max_platforms = max(max_platforms, platforms)
            i += 1
        else:                              # Departure comes first
            platforms -= 1
            j += 1
    return max_platforms
```

---

## Problem: Meeting Rooms

* **Problem Type:** Single Resource Feasibility / Adjacency Overlap Detection
* **Data Structure Used:** Sorted 2D array of intervals
* **Approach 1:** Compare every pair of intervals for overlap. If any pair satisfies `a.end > b.start` (where `a` starts before `b`), they conflict. Time: $O(N^2)$.
* **Optimized Approach:** Sort by start time, then sweep consecutively. For any consecutive pair of intervals in sorted order, if the first interval ends after the second starts, they overlap — one person cannot attend both. Return `False` immediately. If no consecutive pair overlaps, return `True`.
* **Complexity:**
  * **Time:** $O(N \log N)$ — sorting dominates; the adjacency scan is $O(N)$.
  * **Space:** $O(1)$ — no additional data structure beyond the sort.
* **Pointer Flow:**
```text
intervals = [[0,30],[5,10],[15,20]]
Sorted by start: [[0,30],[5,10],[15,20]]

i=1: intervals[1].start=5 < intervals[0].end=30 -> OVERLAP -> return False.
```
* **Pattern Recognition:**
  * Use sort + adjacency scan when:
    - The problem asks whether a single person (or single resource) can attend all events without conflict.
    - No resource allocation is needed — a simple boolean feasibility answer suffices.
* **Core Insight:** Sorting by start time makes overlaps locally detectable. If two intervals overlap at all, the one that starts later must start before the one that starts earlier ends. After sorting, this condition can only occur between consecutive pairs — a non-consecutive pair's overlap would imply a consecutive pair overlap by transitivity. A single adjacency scan is therefore both necessary and sufficient.
* **Mistakes Made:** We compared every pair of intervals with a nested loop before recognising that sorting makes non-adjacent overlaps transitively impossible. After sorting, the problem reduces from $O(N^2)$ pairwise checking to $O(N)$ linear scanning.
* **What I Learned:** When checking for any conflict in a set of sorted intervals, adjacency comparison is equivalent to all-pairs comparison. Transitivity of overlap (if A overlaps B and B overlaps C in sorted order, then A and B are already detected as conflicting) makes the full pairwise check redundant.

---

## Problem: Meeting Rooms II

* **Problem Type:** Multi-Resource Allocation / Minimum Rooms via Peak Concurrency
* **Data Structure Used:** Sorted 2D array of intervals + min-heap of active end times
* **Approach 1:** For each meeting, scan all currently in-use rooms to find the earliest one that becomes free. Assign the meeting to that room, or open a new one. Each scan is $O(N)$, and there are $N$ meetings, giving $O(N^2)$ overall.
* **Optimized Approach:** Min-Heap End Time Tracking. Sort intervals by start time. Maintain a min-heap of end times of ongoing meetings. For each meeting: if the heap is non-empty and the earliest-ending meeting (`heap[0]`) finishes at or before the current meeting's start, a room is free — replace its end time with the current meeting's end time (`heapreplace`). Otherwise, no room is free — push the current end time as a new room.
* **Complexity:**
  * **Time:** $O(N \log N)$ — sorting is $O(N \log N)$; $N$ heap operations each cost $O(\log N)$.
  * **Space:** $O(N)$ — the heap holds at most $N$ end times simultaneously (worst case: all meetings overlap).
* **Pointer Flow:**
```text
intervals = [[0,30],[5,10],[15,20]]
Sorted by start: [[0,30],[5,10],[15,20]]

[0,30]:  heap=[]       -> push 30. heap=[30]
[5,10]:  heap[0]=30 > 5 -> no free room -> push 10. heap=[10,30]
[15,20]: heap[0]=10 <= 15 -> free room! -> replace with 20. heap=[20,30]

Answer: len(heap) = 2 rooms.
```
* **Pattern Recognition:**
  * Use min-heap end time tracking when:
    - All resources are functionally identical (any free room works for any meeting).
    - The goal is the minimum number of parallel resources to handle all overlapping demands.
* **Core Insight:** The heap abstracts away the assignment entirely. We never need to know which specific room hosted which meeting — only which room finishes earliest. The heap top always answers this in $O(1)$. The heap's size at any moment equals the number of simultaneously active meetings. Its maximum size across the entire sweep equals the peak concurrency and thus the minimum rooms needed.
* **Mistakes Made:** We tracked full interval lists per room and scanned each room's current interval to detect conflicts. This per-room scan is $O(\text{rooms})$ per meeting — equivalent to $O(N)$ per meeting — giving $O(N^2)$ overall. The heap reduces this to $O(\log N)$ per meeting by tracking only the scalar that determines reusability (end time), discarding all assignment history.
* **What I Learned:** When resources are identical, replace assignment tracking with resource-state tracking. The only state that matters for a room is when it next becomes free. A min-heap on a single scalar (end time) replaces a full room-assignment data structure and reduces complexity from $O(N^2)$ to $O(N \log N)$.

---

## Problem: Minimum Platforms

* **Problem Type:** Multi-Resource Allocation / Two-Pointer Peak Concurrency Sweep
* **Data Structure Used:** Two sorted arrays (arrivals, departures) + two pointers
* **Approach 1:** For each train, count how many other trains overlap with its time window. The maximum such count is the answer. Each count requires scanning all other trains: $O(N^2)$.
* **Optimized Approach:** Two-Pointer Sorted Event Sweep. Sort arrival times and departure times independently. Use two pointers `i` (arrival index) and `j` (departure index). If the next arrival comes at or before the next departure (`arrivals[i] <= departures[j]`), a new platform is needed — increment the counter. Otherwise, a train departs first — decrement the counter. Track the maximum counter value throughout.
* **Complexity:**
  * **Time:** $O(N \log N)$ — sorting two arrays; the two-pointer sweep is $O(N)$.
  * **Space:** $O(1)$ — only two pointer variables and two counters beyond the sorted arrays.
* **Pointer Flow:**
```text
arrivals:   [900, 940, 950, 1100, 1500, 1800]
departures: [910, 1120, 1130, 1200, 1900, 2000]

i=0,j=0: 900<=910  -> arrive. platforms=1, max=1. i=1.
i=1,j=0: 940>910   -> depart. platforms=0. j=1.
i=1,j=1: 940<=1120 -> arrive. platforms=1, max=1. i=2.
i=2,j=1: 950<=1120 -> arrive. platforms=2, max=2. i=3.
i=3,j=1: 1100<=1120-> arrive. platforms=3, max=3. i=4.
i=4,j=1: 1500>1120 -> depart. platforms=2. j=2.
i=4,j=2: 1500>1130 -> depart. platforms=1. j=3.
i=4,j=3: 1500>1200 -> depart. platforms=0. j=4.
i=4,j=4: 1500<=1900-> arrive. platforms=1, max=3. i=5.
i=5,j=4: 1800<=1900-> arrive. platforms=2, max=3. i=6. i exhausted.

Answer: max_platforms = 3.
```
* **Pattern Recognition:**
  * Use two-pointer event sweep when:
    - The input is naturally structured as two separate arrays (arrivals and departures), not as `[start, end]` pairs.
    - No heap operations are needed — both arrays are independently sorted and can be merged via two pointers.
* **Core Insight:** The two-pointer sweep constructs the same event timeline as merging all arrivals and departures into one sorted stream, but without actually building that stream. Arrival events increment the active count; departure events decrement it. The maximum counter value is the peak concurrency. The critical tie-breaking rule — process departures before arrivals when they occur at the same time — ensures that a platform freed at time $t$ can be reused by a train arriving at time $t$.
* **Mistakes Made:** We built a combined event list of (time, type) pairs, sorted it, and swept through. While correct, this requires $O(2N)$ memory for the combined list and more complex tie-breaking logic (events at the same time must be ordered: departure before arrival). The two-pointer approach on separate sorted arrays is simpler and uses $O(1)$ extra space.
* **What I Learned:** When a resource allocation problem provides arrivals and departures as separate arrays, the two-pointer sweep is strictly preferable to building a combined event list. Both approaches are $O(N \log N)$, but the two-pointer version uses less memory, requires no event-type tagging, and is easier to reason about tie-breaking.

---

### Master Patterns Learned

#### 1. Sort + Adjacency Scan (The Single Resource Feasibility Frame)
* **Applied to:** Meeting Rooms
* **The Strategy:** Sort intervals by start time. Check consecutive pairs for overlap: if `intervals[i].start < intervals[i-1].end`, they conflict. A conflict found means the sequence is infeasible for a single resource.
* **The Conceptual Mechanics:**
  - **Transitivity of Overlap:** After sorting by start, if interval A overlaps interval C (where B is between them), then either A overlaps B or B overlaps C — a consecutive conflict already exists. Non-adjacent overlaps reduce to adjacent ones.
  - **Constant Decision:** The decision is a single comparison per consecutive pair — constant time per interval after sorting.
* **The Layout / Code Pattern:**
```python
def can_attend_all(intervals: list[list[int]]) -> bool:
    intervals.sort(key=lambda x: x[0])              # Sort by start time
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:     # Next starts before previous ends
            return False
    return True
```

#### 2. Min-Heap End Time Tracking (The Peak Concurrency Heap Frame)
* **Applied to:** Meeting Rooms II
* **The Strategy:** Sort by start time. Maintain a min-heap of end times of active resources. For each interval, reuse the earliest-ending free resource (if available) or open a new one. The final heap size equals the minimum resources needed.
* **The Conceptual Mechanics:**
  - **Resource Identity Abstraction:** All resources are interchangeable. The only distinguishing property is when each becomes free. The min-heap on end times is the minimal data structure encoding this property.
  - **Greedy Optimality:** Opening a new resource only when strictly necessary (no free resource exists) ensures the heap never exceeds peak concurrency. Reusing the earliest-ending free resource ensures future resources are maximally available.
* **The Layout / Code Pattern:**
```python
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda x: x[0])
    heap = []                                        # Min-heap of active end times
    for start, end in intervals:
        if heap and heap[0] <= start:                # Earliest room is free
            heapq.heapreplace(heap, end)             # Reuse it
        else:
            heapq.heappush(heap, end)                # Open a new room
    return len(heap)
```

#### 3. Two-Pointer Event Sweep (The Separate Stream Peak Count Frame)
* **Applied to:** Minimum Platforms
* **The Strategy:** Sort arrivals and departures independently. Merge-sweep with two pointers. Increment count on arrival events; decrement on departure events. Return the maximum count across the sweep.
* **The Conceptual Mechanics:**
  - **Implicit Event Merge:** The two-pointer sweep implicitly constructs the merged chronological event stream without allocating it. At each step, the smaller of `arrivals[i]` and `departures[j]` is the next event.
  - **Tie-Breaking Rule:** When arrival and departure occur simultaneously, process the departure first. This reflects the real-world constraint that a platform freed at time $t$ can host a train arriving at time $t$, and avoids over-counting simultaneous events.
* **The Layout / Code Pattern:**
```python
def min_platforms(arrivals: list[int], departures: list[int]) -> int:
    arrivals.sort()
    departures.sort()
    platforms = max_platforms = 0
    i = j = 0
    while i < len(arrivals):
        if arrivals[i] <= departures[j]:             # Arrival event
            platforms += 1
            max_platforms = max(max_platforms, platforms)
            i += 1
        else:                                        # Departure event
            platforms -= 1
            j += 1
    return max_platforms
```
