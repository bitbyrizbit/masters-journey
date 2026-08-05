# Dynamic Overlaps: The Calendar Series

## 1. Static vs. Dynamic Interval Problems

Until now, we have dealt with **Static Interval Problems**: you are given an array of intervals up front, you sort them once, and you sweep through them to find the answer.

The Calendar Series introduces **Dynamic Interval Problems**: you receive intervals one by one, and for *each* interval, you must immediately validate it or calculate a metric (like maximum concurrency) before accepting the next one. 
Because the data arrives dynamically, you cannot afford to sort the entire array from scratch on every insertion without incurring massive performance penalties over time. You need a data structure or strategy that handles incremental updates efficiently.

---

## 2. Brute Force Validation (Calendar I)

In My Calendar I, you are asked to validate whether a new event causes a double booking. 
The simplest approach is brute-force validation against an unstructured array.

When a new event `[start, end)` arrives, iterate through all existing events `[s, e)`.
Two events overlap if and only if:
`start < e` AND `s < end`

If the new event passes this check against all existing events, append it to the array. 
While this is $O(N)$ per query (and thus $O(N^2)$ for $N$ queries), it is acceptable when $N$ is small. (For a strictly $O(\log N)$ approach, a Balanced Binary Search Tree like a Red-Black Tree is required, but this is rarely expected to be coded from scratch in Python during an interview).

---

## 3. The Overlap Projection (Calendar II)

My Calendar II asks you to allow double bookings, but strictly forbid **triple bookings**.
How do you track the depth of overlaps dynamically?

The cleverest trick is **Overlap Projection**: maintaining a completely separate array just for the double-booked regions.
1.  **The Double Booking Array (`overlaps`)**: Stores the exact geometric bounds of any region where two events intersect.
2.  **The Single Booking Array (`calendar`)**: Stores all successfully booked events.

When a new event arrives:
1.  **Check the forbidden state first:** Does it overlap with anything in the `overlaps` array? If yes, that would create a triple booking. Return `False` immediately.
2.  **Update the forbidden state:** The event is valid! Now, check it against the `calendar` array. For every existing event it overlaps with, compute the exact intersecting region (`max(start, s)` to `min(end, e)`) and append it to the `overlaps` array.
3.  **Accept the event:** Append it to the `calendar` array.

This decoupled logic turns a highly complex state-tracking problem into two simple linear scans.

---

## 4. The Sweep-Line Delta Map (Calendar III)

My Calendar III drops the boolean validation entirely and asks: "What is the peak concurrency (maximum overlaps) across the entire calendar at this exact moment?"

This requires tracking the exact boundary events on a continuous timeline. 
The master pattern for this is the **Sweep-Line Delta Map** (or Boundary Count).

Instead of storing `[start, end]` objects, we map the timeline using a Dictionary (or TreeMap in Java/C++).
*   When an event starts at `start`, the concurrency increases: `delta[start] += 1`.
*   When an event ends at `end`, the concurrency decreases: `delta[end] -= 1`.

To find the peak concurrency at any moment:
1.  Extract all the keys (timestamps) from the dictionary and sort them chronologically.
2.  Sweep through the sorted timestamps, accumulating the deltas into a running `active` counter.
3.  The maximum value of `active` during this sweep is the peak concurrency.

Because Python dictionaries are unsorted, extracting and sorting the keys takes $O(K \log K)$ per query (where $K$ is the number of unique timestamps). This is acceptable for typical interview constraints.

---

## 5. Master Templates

```python
import collections

# Sweep-Line Delta Map (For K-Booking Peak Concurrency)
class SweepLineCalendar:
    def __init__(self):
        self.delta = collections.Counter()

    def book(self, start: int, end: int) -> int:
        # 1. Record the boundary events
        self.delta[start] += 1
        self.delta[end] -= 1
        
        active = 0
        max_active = 0
        
        # 2. Chronological Sweep
        for time in sorted(self.delta.keys()):
            active += self.delta[time]
            if active > max_active:
                max_active = active
                
        return max_active
```

---

## Problem: My Calendar I

* **Interview Difficulty:** Medium
* **Problem Type:** Dynamic Overlap Validation
* **Data Structure Used:** List
* **Optimized Approach:** Store accepted events in a simple list. For each new event, iterate through the list and check the overlap condition: `max(start1, start2) < min(end1, end2)`. If it holds true for any event, return `False`. Otherwise, append the event and return `True`.
* **Complexity:**
  * **Time:** $O(N)$ per `book()` call, leading to $O(N^2)$ for $N$ queries.
  * **Space:** $O(N)$ to store the events.
* **Pattern Recognition:**
  * On-the-fly validation of new intervals against a historical ledger.
* **Core Insight:** The universal formula for interval overlap is `start < e and s < end`. Memorize this. It is the cheapest and cleanest way to detect a collision without writing multiple nested `if` statements.

---

## Problem: My Calendar II

* **Interview Difficulty:** Medium
* **Problem Type:** Dynamic Overlap Projection
* **Data Structure Used:** Two Lists (`calendar` and `overlaps`)
* **Optimized Approach:** Maintain a list of all events and a separate list of all double-booked regions. When booking, first check if the new event overlaps with any double-booked region (which would cause a triple booking). If it's safe, find all overlaps with standard events, add those overlap boundaries to the double-booked list, and finally add the event to the standard list.
* **Complexity:**
  * **Time:** $O(N)$ per `book()` call.
  * **Space:** $O(N)$ for both arrays.
* **Pointer Flow:**
```text
book(10, 20) -> Safe. calendar=[(10,20)], overlaps=[]
book(50, 60) -> Safe. calendar=[(10,20), (50,60)], overlaps=[]
book(10, 40) -> Overlaps with (10,20)! 
                Add intersection (10,20) to overlaps.
                calendar=[(10,20), (50,60), (10,40)], overlaps=[(10,20)]
book(5, 15)  -> Checks overlaps: overlaps with (10,20)! 
                TRIPLE BOOKING. Return False.
```
* **Pattern Recognition:**
  * Keeping track of exactly 2-levels or 3-levels of overlap.
* **Core Insight:** By isolating the "forbidden state" (the double bookings) into its own array, validation remains an $O(N)$ linear scan. We don't need a complex Segment Tree just to prevent a degree-3 overlap.

---

## Problem: My Calendar III

* **Interview Difficulty:** Hard
* **Problem Type:** Boundary Counting / Sweep-Line Delta
* **Data Structure Used:** Hash Map / Counter
* **Optimized Approach:** Treat the start and end of intervals as discrete events. +1 for a start, -1 for an end. Upon every query, add the new events to the map. Then, extract all keys, sort them, and compute the running sum (prefix sum) to find the maximum active events at any point.
* **Complexity:**
  * **Time:** $O(N \log N)$ per `book()` call in Python (due to sorting the keys of the dictionary every time).
  * **Space:** $O(N)$ for the dictionary.
* **Pointer Flow:**
```text
book(10, 20): delta = {10: 1, 20: -1}. Max running sum = 1
book(50, 60): delta = {10: 1, 20: -1, 50: 1, 60: -1}. Max running sum = 1
book(10, 40): delta = {10: 2, 20: -1, 40: -1, 50: 1, 60: -1}. 
              Sweep: time 10 (+2) -> active=2. Max = 2.
book(5, 15):  delta = {5: 1, 10: 2, 15: -1, 20: -1, 40: -1, 50: 1, 60: -1}.
              Sweep: time 5 (+1) -> active=1
                     time 10 (+2) -> active=3. Max = 3!
```
* **Pattern Recognition:**
  * Finding the absolute maximum overlap depth (K-booking) at any point in time dynamically.
* **Core Insight:** We completely abandon the concept of "Intervals" and shift to "Boundary Events." An interval `[10, 20]` isn't a solid block anymore; it's a +1 charge at time 10, and a -1 discharge at time 20. Sweeping through these charges chronologically perfectly reconstructs the overlap depth at any coordinate.
