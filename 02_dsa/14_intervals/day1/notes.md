# Interval Fundamentals: Coalescing and Insertion

## 1. What Are Intervals?

An interval is mathematically defined as a contiguous range of values between a lower bound (start) and an upper bound (end), usually represented as an array or tuple `[start, end]`. In technical interviews, intervals model spans of time (meetings, shifts, task durations) or geometric coordinates (lines on an axis, covered areas). 

The primary challenge in interval problems is managing **overlap**. Two intervals `A` and `B` overlap if and only if:
`max(A.start, B.start) <= min(A.end, B.end)`

However, directly comparing all intervals against each other to find overlaps is an $O(N^2)$ operation. The entire study of interval algorithms is dedicated to eliminating this quadratic comparison overhead.

---

## 2. The Power of Sorting

The master key to interval problems is **sorting**. Sorting transforms a chaotic 2D geometric problem (checking every interval against every other interval) into a 1D sequential sweep line problem.

**Sorting by Start Time:**
When we sort intervals by their start time, we guarantee a left-to-right chronological progression. The most profound consequence of this is **Transitivity of Non-Overlap**.
After sorting by start time:
*   If interval $I_k$ does not overlap with $I_{k-1}$ (i.e., $I_k.\text{start} > I_{k-1}.\text{end}$), then $I_k$ cannot possibly overlap with *any* interval before $I_{k-1}$.
*   Therefore, to check if a new interval overlaps with our currently merged continuous block, we only ever need to compare it against the **very last** interval in that block.

This single observation reduces overlap resolution from $O(N^2)$ to $O(N)$ after an $O(N \log N)$ sort.

---

## 3. The Coalesce Sweep (Merging)

The standard framework for combining overlapping intervals into solid blocks is the Coalesce Sweep. It operates sequentially:

1.  **Anchor:** Sort by start time. Initialize your result list with the first interval, which serves as the active, expanding block.
2.  **Sweep:** Iterate through the remaining intervals.
3.  **Absorb or Append:** 
    *   If the current interval starts before or exactly when the active block ends (`current.start <= active.end`), they overlap. **Absorb** it by extending the active block's end to the maximum of both ends (`active.end = max(active.end, current.end)`).
    *   If the current interval starts strictly after the active block ends, the active block is finalized. **Append** the current interval as the new active block.

---

## 4. The Three-Phase Pre-Sorted Insertion

When inserting a new interval into a list of intervals that is **already sorted and non-overlapping**, we don't need to re-sort the array (which would waste $O(N \log N)$ time). Instead, we can exploit the sorted structure to resolve the insertion in a single $O(N)$ sweep.

Because the array is sorted, the new interval divides the array into three distinct chronological zones:
1.  **The Past (No Overlap):** All intervals that end completely before the new interval starts. These can be appended as-is.
2.  **The Collision Zone (Overlap):** All intervals that overlap with the new interval. These form a single contiguous block in the sorted array. We merge them all into the new interval by dynamically stretching its start and end boundaries.
3.  **The Future (No Overlap):** All intervals that start completely after the new interval ends. These can be appended as-is.

This three-phase sweep is the canonical $O(N)$ solution for interval insertion.

---

## 5. Master Templates

```python
# 1. Start-Sort Coalescing (Merge Intervals)
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals: return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for i in range(1, len(intervals)):
        current = intervals[i]
        last_merged = merged[-1]
        if current[0] <= last_merged[1]:
            last_merged[1] = max(last_merged[1], current[1])
        else:
            merged.append(current)
            
    return merged


# 2. Three-Phase Insertion (Insert Interval)
def insert_interval(intervals: list[list[int]], new_interval: list[int]) -> list[list[int]]:
    result = []
    i, n = 0, len(intervals)
    
    # Phase 1: Past
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1
        
    # Phase 2: Collision
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)
    
    # Phase 3: Future
    while i < n:
        result.append(intervals[i])
        i += 1
        
    return result
```

---

## Problem: Merge Intervals

* **Interview Difficulty:** Medium
* **Problem Type:** Start-Time Sort / Sequential Region Coalescing
* **Data Structure Used:** Sorted 2D array of intervals + Result List
* **Approach 1:** For every pair of intervals, check if they overlap and merge them. Repeat until no more merges can be performed. This requires $O(N^2)$ pairwise comparisons per pass and up to $O(N)$ passes in the worst case, giving $O(N^3)$.
* **Optimized Approach:** Sort by start time, then execute a single-pass coalesce sweep. Initialize a result list with the first interval. For each subsequent interval, check if its start is less than or equal to the end of the last interval in the result. If yes, extend the last interval's end to `max(last_end, current_end)`. If no, the current interval is entirely separate — append it to the result.
* **Complexity:**
  * **Time:** $O(N \log N)$ — sorting dominates; the subsequent sweep is $O(N)$.
  * **Space:** $O(N)$ or $O(\log N)$ depending on the sorting algorithm's auxiliary space.
* **Pointer Flow:**
```text
intervals = [[1,3],[2,6],[8,10],[15,18]]
Sorted by start: [[1,3],[2,6],[8,10],[15,18]]

result = [[1,3]]
[2,6]:   2 <= 3 -> overlap -> extend max(3, 6): result = [[1,6]]
[8,10]:  8 > 6  -> no overlap -> append: result = [[1,6],[8,10]]
[15,18]: 15 > 10 -> no overlap -> append: result = [[1,6],[8,10],[15,18]]
```
* **Pattern Recognition:**
  * Use start-time sorted coalesce sweep when:
    - The problem requires combining all overlapping intervals into the minimum number of non-overlapping continuous regions.
    - The result must cover exactly the same total timeline space as the original fragments.
* **Core Insight:** Overlap is a geometric problem, but sorting by start time linearizes it. Once sorted, an interval can only overlap with the interval immediately preceding it in the merged list. No interval further back can reach it without also enveloping the intervals in between. Therefore, checking only the `result[-1]` boundary is geometrically sufficient to resolve all overlaps.
* **Mistakes Made:** We initially sorted by end time. Sorting by end time breaks coalescing because an interval that ends early but starts extremely early might be positioned after a short interval that ends earlier but starts later. Start-time sorting guarantees the left boundary moves monotonically rightward.
* **What I Learned:** Always sort by start time when the objective is to *merge* or *combine* intervals. It establishes a left-to-right chronological baseline where overlaps only occur adjacently.

---

## Problem: Insert Interval

* **Interview Difficulty:** Medium
* **Problem Type:** Pre-Sorted Interval Insertion / Three-Phase Sweep
* **Data Structure Used:** Input array (already sorted and disjoint) + Result List
* **Approach 1:** Append the `newInterval` to the array, sort the array by start time, and run standard Merge Intervals. Time: $O(N \log N)$ due to sorting.
* **Optimized Approach:** Three-Phase Sweep. Since the input is already sorted, we can use three while loops. Loop 1: skip and append all intervals ending before `newInterval` starts. Loop 2: for all intervals overlapping `newInterval`, merge them by shrinking `newInterval`'s start to the minimum start and expanding its end to the maximum end. Append the mutated `newInterval`. Loop 3: append all remaining intervals.
* **Complexity:**
  * **Time:** $O(N)$ — a single linear scan through the intervals.
  * **Space:** $O(N)$ — to store the newly created merged array.
* **Pointer Flow:**
```text
intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]

Phase 1: (end < 4)
  [1,2]: 2 < 4 -> append. result = [[1,2]]
  [3,5]: 5 < 4? False. Phase 1 ends.

Phase 2: (start <= 8)
  [3,5]: 3 <= 8 -> overlap. new = [min(4,3), max(8,5)] = [3,8]
  [6,7]: 6 <= 8 -> overlap. new = [min(3,6), max(8,7)] = [3,8]
  [8,10]: 8 <= 8 -> overlap. new = [min(3,8), max(8,10)] = [3,10]
  [12,16]: 12 <= 8? False. Phase 2 ends. Append new: result = [[1,2], [3,10]]

Phase 3: (remaining)
  [12,16] -> append. result = [[1,2], [3,10], [12,16]]
```
* **Pattern Recognition:**
  * Use the three-phase sweep when:
    - The input array is explicitly guaranteed to be sorted and non-overlapping.
    - You are injecting a new range that bridges multiple existing ranges.
* **Core Insight:** The sorted input means the overlap zone is perfectly contiguous. There are no overlapping intervals hiding before Phase 1 or after Phase 3. The `newInterval` acts as a sponge, moving through Phase 2 and absorbing everything it touches by pushing its boundaries outward.
* **Mistakes Made:** Trying to insert the interval and manipulate the list in-place using `splice` or `del` operations. Modifying an array in-place during iteration leads to index shifting bugs and $O(N^2)$ performance due to memory shifts. Building a new `result` array is safer and strictly $O(N)$.
* **What I Learned:** When a problem states the input is sorted, applying an $O(N \log N)$ sort is a failure to leverage the provided structure. The three-phase sweep is the standard pattern for exploiting pre-sorted sequence injection.

---

## Problem: Summary Ranges

* **Interview Difficulty:** Easy
* **Problem Type:** Consecutive Sequence Coalescing
* **Data Structure Used:** Array + Two Pointers (`start`, `i`)
* **Approach 1:** Iterate and build strings dynamically on every step. This leads to messy code trying to backtrack or rewrite strings when the range extends.
* **Optimized Approach:** Two-Pointer tracking. Keep a `start` variable initialized to the first number. Iterate from index 1. If `nums[i]` is exactly `nums[i-1] + 1`, the sequence continues — do nothing. The moment the sequence breaks (`nums[i] != nums[i-1] + 1`), the current range is finished. If `start == nums[i-1]`, it's a single number; otherwise, it's a range `"start->end"`. Append it to results, and reset `start` to `nums[i]`. Handle the final lingering range after the loop.
* **Complexity:**
  * **Time:** $O(N)$ — one linear scan.
  * **Space:** $O(1)$ auxiliary space (excluding the output array).
* **Pointer Flow:**
```text
nums = [0,1,2,4,5,7]

start = 0
i=1: nums[1](1) == nums[0](0)+1 -> continue
i=2: nums[2](2) == nums[1](1)+1 -> continue
i=3: nums[3](4) != nums[2](2)+1 -> BREAK!
     Range is 0 to 2 (0 != 2). Append "0->2". start = nums[3] = 4.
i=4: nums[4](5) == nums[3](4)+1 -> continue
i=5: nums[5](7) != nums[4](5)+1 -> BREAK!
     Range is 4 to 5 (4 != 5). Append "4->5". start = nums[5] = 7.
Loop ends.
Final range: start is 7, end is 7. Append "7".
Output: ["0->2", "4->5", "7"]
```
* **Pattern Recognition:**
  * Use sequence boundary tracking when:
    - You need to compress a sorted list of discrete integers into continuous bounding boxes.
* **Core Insight:** A range problem without explicit `[start, end]` arrays. The math $x_i \neq x_{i-1} + 1$ acts as the overlap detector. It perfectly mirrors the `current.start > active.end` condition from Merge Intervals, but applied to discrete integers.
* **Mistakes Made:** Forgetting to handle the final sequence after the loop terminates. Because a sequence only triggers its string-formatting when a *break* occurs, the very last sequence in the array never encounters a break to trigger its formatting. The post-loop flush is critical.
* **What I Learned:** Always remember the "post-loop flush" when tracking continuous sequences. The loop detects boundaries between sequences, but the end of the array is an implicit boundary that must be explicitly handled.
