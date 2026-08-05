# Dual Stream & Coverage Analysis

## 1. Multi-Stream Merging

Until now, we have mostly processed single lists of intervals. Day 3 introduces problems where intervals come from multiple sources — either an array of arrays (Employee Free Time) or two distinct lists (Interval Intersections).

There are two primary ways to handle multi-stream interval problems:
1.  **Flatten and Sort:** If the streams don't need to maintain their individual identities, flatten them all into a single 1D array and sort by start time. This reduces the problem back to the Day 1 Coalesce Sweep.
2.  **Two-Pointer Sweep:** If the streams are already sorted independently (like in Interval Intersections), you can sweep through both simultaneously using two pointers, avoiding the $O(N \log N)$ cost of a full combined sort.

---

## 2. The Free Time Gap Detection

When merging intervals, we normally look for overlaps (`start <= prev_end`). But what if we are looking for the *absence* of overlaps? 

In Employee Free Time, the objective is to find contiguous blocks of time where *no* employee is working.
If we flatten all schedules and sort by start time, we create a chronological timeline of work blocks. 
As we sweep through this timeline, we track the `max_end` (the furthest into the future any currently running work block extends). 
*   If the next work block starts **before or at** `max_end`, there is no gap. The timeline is continuous. We just update `max_end`.
*   If the next work block starts **strictly after** `max_end`, the entire system was idle between `max_end` and `next.start`! This is a universal free time block.

This inversion — searching for the gaps between merged blocks instead of the blocks themselves — is a powerful variation of the Coalesce Sweep.

---

## 3. The Dual-Pointer Intersection

How do you find the overlapping region of two intervals `A` and `B`?
The overlap mathematically exists between the **maximum of their starts** and the **minimum of their ends**:
`intersect_start = max(A.start, B.start)`
`intersect_end = min(A.end, B.end)`

If `intersect_start <= intersect_end`, that region is a valid intersection.

When comparing two sorted lists of intervals, we can use a two-pointer approach (`i` for list 1, `j` for list 2). We compute the intersection of `list1[i]` and `list2[j]`. 
The critical decision is: **which pointer do we advance?**
We always advance the pointer of the interval that **ends earliest**. Why? Because the interval that ends earliest has completely exhausted its timeline. It is mathematically impossible for it to intersect with any future intervals in the other list (since they are sorted). The interval that ends later might still stretch far enough to intersect the next element in the other list.

---

## 4. The Coverage Tie-Breaker

Remove Covered Intervals introduces a subtle geometric problem: finding intervals completely swallowed by others.
Interval `B` is covered by Interval `A` if: `A.start <= B.start` AND `A.end >= B.end`.

A standard sort by start time (`intervals.sort(key=lambda x: x[0])`) gets us halfway there: it guarantees `A.start <= B.start`. As we sweep, we track the `max_end` we've seen. If `B.end <= max_end`, it's covered.

But there's a fatal flaw: **what if they have the exact same start time?**
If `A = [1, 4]` and `B = [1, 8]`, a naive sort might put `[1,4]` first. `max_end` becomes 4. Then we see `[1,8]`. `8 > 4`, so we say it's valid. But wait — `[1,4]` is covered by `[1,8]`! We missed it because the smaller one came first and failed to set the boundary high enough.

The solution is the **Coverage Tie-Breaker**: Sort by start time ASCENDING, and end time **DESCENDING** for ties.
`intervals.sort(key=lambda x: (x[0], -x[1]))`
This forces `[1,8]` to appear before `[1,4]`. The massive interval sets the `max_end` to 8 immediately, properly swallowing the `[1,4]` that follows.

---

## 5. Master Templates

```python
# 1. Gap Detection Sweep (Employee Free Time)
def employee_free_time(schedule):
    intervals = sorted([iv for emp in schedule for iv in emp], key=lambda x: x.start)
    free_time = []
    max_end = intervals[0].end
    
    for i in range(1, len(intervals)):
        if intervals[i].start > max_end:
            free_time.append(Interval(max_end, intervals[i].start))
        max_end = max(max_end, intervals[i].end)
        
    return free_time


# 2. Dual-Pointer Intersection (Interval Intersections)
def interval_intersection(list1, list2):
    i = j = 0
    ans = []
    while i < len(list1) and j < len(list2):
        start = max(list1[i][0], list2[j][0])
        end = min(list1[i][1], list2[j][1])
        if start <= end:
            ans.append([start, end])
        if list1[i][1] < list2[j][1]:
            i += 1
        else:
            j += 1
    return ans
```

---

## Problem: Employee Free Time

* **Interview Difficulty:** Hard
* **Problem Type:** Start-Time Sort / Gap Detection
* **Data Structure Used:** Flattened Array
* **Approach 1:** A priority queue (min-heap) keeping track of the earliest starting interval among all employees, merging them on the fly. This avoids flattening the entire array at once, yielding $O(N \log K)$ time where $K$ is the number of employees.
* **Optimized Approach:** Flatten the jagged array into a single 1D list of intervals. Sort by start time. Maintain the `max_end` seen so far. If the next interval starts strictly after `max_end`, the space between `max_end` and `next.start` is a block of free time. Update `max_end` on every step. Time is $O(N \log N)$ where $N$ is total intervals across all employees. Both approaches are acceptable in interviews.
* **Complexity:**
  * **Time:** $O(N \log N)$
  * **Space:** $O(N)$
* **Pointer Flow:**
```text
schedule = [[[1,2],[5,6]], [[1,3]], [[4,10]]]
Flattened & Sorted: [[1,2], [1,3], [4,10], [5,6]]

max_end = 2 (from first interval [1,2])
[1,3]:  start(1) > max_end(2)? No. max_end = max(2, 3) = 3
[4,10]: start(4) > max_end(3)? YES! Gap found: [3, 4]. max_end = max(3, 10) = 10
[5,6]:  start(5) > max_end(10)? No. max_end = max(10, 6) = 10
```
* **Pattern Recognition:**
  * Searching for gaps in overlapping multi-source timelines.
* **Core Insight:** If you flatten the matrix, the problem is literally just "Merge Intervals" but instead of saving the merged blocks, you save the empty spaces between the merges.

---

## Problem: Interval List Intersections

* **Interview Difficulty:** Medium
* **Problem Type:** Two-Pointer Synchronized Sweep
* **Data Structure Used:** Two Pointers
* **Optimized Approach:** Use pointers `i` and `j`. The intersection of `list1[i]` and `list2[j]` is `[max(start1, start2), min(end1, end2)]`. If this is valid (start <= end), append it. To advance, look at the end times: increment the pointer for whichever interval ends earlier, because it cannot intersect with any future intervals.
* **Complexity:**
  * **Time:** $O(M + N)$ where M and N are lengths of the lists.
  * **Space:** $O(1)$ auxiliary space.
* **Pointer Flow:**
```text
list1 = [[0,2],[5,10]]
list2 = [[1,5],[8,12]]

i=0, j=0: A=[0,2], B=[1,5]
          start = max(0,1)=1, end = min(2,5)=2. Valid: [1,2]. 
          A ends earlier (2 < 5). i++
i=1, j=0: A=[5,10], B=[1,5]
          start = max(5,1)=5, end = min(10,5)=5. Valid: [5,5].
          B ends earlier (5 < 10). j++
```
* **Pattern Recognition:**
  * Comparing two independent, pre-sorted timelines.
* **Core Insight:** The logic for advancing pointers mimics the merge phase of Merge Sort. You advance the "smaller" item. In the world of intervals, the "smaller" item is the one that *finishes first*, because it is the bottleneck preventing further intersections.

---

## Problem: Remove Covered Intervals

* **Interview Difficulty:** Medium
* **Problem Type:** Custom Tie-Breaker Sort / Max-End Tracking
* **Data Structure Used:** Array + scalar `max_end`
* **Optimized Approach:** Sort intervals by start time ASCENDING, and end time DESCENDING for ties. Maintain a `max_end` scalar initialized to -1. As you iterate, if the current interval's end is strictly greater than `max_end`, it is NOT covered (increment `valid_count`, update `max_end`). If it is $\leq$ `max_end`, it is completely covered by whatever interval previously pushed `max_end` out so far.
* **Complexity:**
  * **Time:** $O(N \log N)$
  * **Space:** $O(1)$ auxiliary space.
* **Pointer Flow:**
```text
intervals = [[1,4],[3,6],[2,8]]
Custom Sort (start ASC, end DESC): [[1,4], [2,8], [3,6]]

valid = 0, max_end = -1
[1,4]: end(4) > -1 -> valid=1, max_end=4
[2,8]: end(8) > 4  -> valid=2, max_end=8
[3,6]: end(6) > 8? No. It's covered by [2,8]!
```
* **Pattern Recognition:**
  * Finding subsets, subsumed intervals, or Russian-doll style encapsulation.
* **Core Insight:** The tie-breaker is the entire problem. If two intervals start at the exact same moment, the longer one must be processed first to establish the boundary. If the shorter one is processed first, it updates the boundary too conservatively, and the longer one will appear "valid" when it should have actually swallowed the shorter one.
