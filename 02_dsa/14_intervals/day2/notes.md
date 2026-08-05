# Scheduling & Overlap Minimization

## 1. The Duality of Sorting: Start vs. End

In Day 1, we learned that sorting by **start time** is the master heuristic for merging and combining intervals. It ensures a left-to-right chronology where overlaps are strictly adjacent.

In Day 2, we introduce the geometric opposite: sorting by **end time**. When is end-time sorting required? When the objective is to **keep as many non-overlapping intervals as possible** (or equivalently, remove the minimum number of intervals).

This is formally known as the **Activity Selection Problem**. The greedy heuristic is Earliest Finish Time First (EFTF). 
Why does EFTF work? Because the interval that finishes earliest frees up the remaining timeline for subsequent intervals sooner. If two intervals conflict, keeping the one that ends later is strictly inferior because it consumes more of the future, potentially blocking intervals that the earlier-ending one would have allowed.

*   **Sort by Start Time:** Use when merging, combining, or measuring peak overlap.
*   **Sort by End Time:** Use when selecting a maximum non-overlapping subset, or minimizing removals/arrows.

---

## 2. The Earliest Finish Sweep

The Earliest Finish Sweep operates on an end-time sorted array:

1.  **Anchor:** Sort by end time. Initialize `prev_end` to $-\infty$.
2.  **Sweep:** Iterate through the intervals.
3.  **Keep or Reject:**
    *   If the current interval starts at or after `prev_end` (`current.start >= prev_end`), it does not overlap with our last kept interval. **Keep it**, and update `prev_end = current.end`.
    *   If the current interval starts before `prev_end`, it overlaps. Because we sorted by end time, we know the *current* interval ends later (or at the same time) than the *previously kept* interval. Therefore, the previously kept interval was the better choice. **Reject (remove) the current interval**.

---

## 3. Resource Allocation and Peak Concurrency

A fundamentally different interval question asks: "How many parallel tracks do we need to process all these intervals simultaneously without conflict?" (e.g., Meeting Rooms II, Minimum Platforms).

This is asking for the **Peak Concurrency** — the maximum number of intervals active at any single moment in time.

Unlike Activity Selection, Resource Allocation requires us to process *all* intervals, so we cannot just reject overlapping ones. We must assign them to resources (rooms). Since all rooms are identical, the only state we care about for a room is **when it becomes free**.

The master pattern here is the **Min-Heap on End Times**:
1.  Sort intervals by start time to process them chronologically.
2.  Maintain a min-heap storing the end times of currently active rooms.
3.  For each interval:
    *   Look at the top of the heap (the earliest freeing room).
    *   If `heap[0] <= current.start`, the room is free! Pop the old end time, push the current interval's end time (this is `heapreplace`).
    *   If `heap[0] > current.start`, no rooms are free. Open a new room by pushing the current interval's end time onto the heap.
4.  The size of the heap is the number of active rooms. The maximum size of the heap is the answer.

---

## 4. Master Templates

```python
import heapq

# 1. Earliest Finish Sweep (Activity Selection / Max Non-Overlapping)
def erase_overlap_intervals(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda x: x[1])  # Sort by END time
    removals = 0
    prev_end = float('-inf')
    
    for start, end in intervals:
        if start >= prev_end:           # Safe to keep
            prev_end = end
        else:                           # Overlaps -> reject it
            removals += 1
            
    return removals


# 2. Peak Concurrency (Min-Heap End Time Tracking)
def min_meeting_rooms(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda x: x[0])  # Sort by START time
    heap = []                           # Min-heap of end times
    
    for start, end in intervals:
        if heap and heap[0] <= start:   # A room is free
            heapq.heapreplace(heap, end)
        else:                           # No room free, open a new one
            heapq.heappush(heap, end)
            
    return len(heap)
```

---

## Problem: Non-Overlapping Intervals

* **Interview Difficulty:** Medium
* **Problem Type:** End-Time Sort / Activity Selection
* **Data Structure Used:** Array + scalar `prev_end`
* **Approach 1:** Try all subsets of intervals and check if they are mutually non-overlapping, keeping the largest valid subset. Exponential $O(2^N)$ time.
* **Optimized Approach:** Sort by end time. Sweep through maintaining `prev_end`. If the interval starts at or after `prev_end`, it's valid to keep. Update `prev_end = end`. Otherwise, it overlaps with the previously kept interval. Increment a `removals` counter.
* **Complexity:**
  * **Time:** $O(N \log N)$ due to sorting. The sweep is $O(N)$.
  * **Space:** $O(1)$ auxiliary space.
* **Pointer Flow:**
```text
intervals = [[1,2],[2,3],[3,4],[1,3]]
Sorted by END time: [[1,2], [1,3], [2,3], [3,4]]

prev_end = -inf, removals = 0
[1,2]: 1 >= -inf -> KEEP. prev_end = 2
[1,3]: 1 >= 2? No -> REMOVE. removals = 1
[2,3]: 2 >= 2 -> KEEP. prev_end = 3
[3,4]: 3 >= 3 -> KEEP. prev_end = 4
```
* **Pattern Recognition:**
  * Use end-time sorting when you want to minimize removals or maximize the number of non-overlapping events.
* **Core Insight:** If you sort by start time, a massive interval that starts early but spans the whole day will be selected first, forcing you to delete many smaller intervals that come after it. Sorting by end time ensures you always greedily pick the event that finishes earliest, maximizing room for future events.

---

## Problem: Minimum Number of Arrows to Burst Balloons

* **Interview Difficulty:** Medium
* **Problem Type:** End-Time Sort / Overlap Maximization
* **Data Structure Used:** Array + scalar `current_arrow_pos`
* **Approach 1:** Exhaustive subset search over coordinates. Infeasible.
* **Optimized Approach:** This is a direct sibling to Non-Overlapping Intervals. Sort by end time. Place your first arrow at the very end of the first balloon (`current_arrow_pos = points[0][1]`). For every subsequent balloon, if it starts *after* the current arrow position (`start > current_arrow_pos`), the arrow missed it. You must shoot a new arrow, so place it at the end of this new balloon.
* **Complexity:**
  * **Time:** $O(N \log N)$
  * **Space:** $O(1)$ auxiliary space.
* **Pointer Flow:**
```text
points = [[10,16],[2,8],[1,6],[7,12]]
Sorted by END time: [[1,6], [2,8], [7,12], [10,16]]

arrows = 1, arrow_pos = 6 (end of first balloon)
[2,8]:   2 > 6? No -> popped by arrow at 6
[7,12]:  7 > 6? YES -> new arrow needed. arrows = 2, arrow_pos = 12
[10,16]: 10 > 12? No -> popped by arrow at 12
```
* **Pattern Recognition:**
  * Grouping intervals into the minimum number of overlapping clusters.
* **Core Insight:** Placing the arrow at the *end* of a balloon is the greedy optimal choice. It guarantees popping the current balloon while delaying the arrow's position as far right as possible, maximizing the chance of popping future balloons.

---

## Problem: Meeting Rooms

* **Interview Difficulty:** Easy
* **Problem Type:** Start-Time Sort / Adjacency Validation
* **Data Structure Used:** Array
* **Optimized Approach:** Sort by start time. Iterate through consecutive pairs. If the current meeting starts strictly before the previous meeting ends (`intervals[i].start < intervals[i-1].end`), there is a conflict. Return `False`.
* **Complexity:**
  * **Time:** $O(N \log N)$
  * **Space:** $O(1)$
* **Pattern Recognition:**
  * Validating a single sequence of events for any overlap.
* **Core Insight:** Sorting by start time reduces overlap checking to adjacent elements. Transitivity guarantees that if an interval overlaps with something earlier, it must overlap with its immediate predecessor.

---

## Problem: Meeting Rooms II

* **Interview Difficulty:** Medium
* **Problem Type:** Start-Time Sort / Peak Concurrency (Min-Heap)
* **Data Structure Used:** Sorted Array + Min-Heap
* **Optimized Approach:** Sort intervals by start time. Maintain a min-heap of the end times of active meetings. For each meeting, check if the earliest finishing meeting (`heap[0]`) is done. If `heap[0] <= current.start`, the room is free: use `heapreplace` to pop the old end time and push the new one. If not, push the new end time (allocating a new room). Return the length of the heap.
* **Complexity:**
  * **Time:** $O(N \log N)$ (sorting is $N \log N$, $N$ heap operations are $N \log N$).
  * **Space:** $O(N)$ (heap size up to $N$).
* **Pointer Flow:**
```text
intervals = [[0,30],[5,10],[15,20]]
Sorted by START time: [[0,30], [5,10], [15,20]]

heap = []
[0,30]:  heap is empty -> push 30. heap = [30]
[5,10]:  heap[0] (30) <= 5? No -> push 10. heap = [10, 30]
[15,20]: heap[0] (10) <= 15? YES -> replace 10 with 20. heap = [20, 30]

Result: len(heap) = 2
```
* **Pattern Recognition:**
  * Asking for "minimum resources," "maximum concurrent events," or "maximum overlap depth."
* **Core Insight:** We don't care *which* room a meeting uses, only *when* any room becomes free. A min-heap perfectly tracks the "soonest available resource" in $O(\log N)$ time, decoupling the complex interval overlap logic into a simple scalar comparison against the heap top.
