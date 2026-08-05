# Advanced Interval State Tracking

## 1. Beyond Sweeping: Active State Management

In the previous days, sweeping over intervals involved maintaining simple scalar states (e.g., `prev_end`, `max_end`, or `active_count`). Day 5 tackles problems where the state at any point in the sweep line is complex, requiring you to track the exact properties of multiple overlapping intervals simultaneously.

This transitions the sweep line from a simple chronological pass into an event-driven architecture, where discrete "START" and "END" boundaries dynamically update an active data structure (usually a Max-Heap or a custom array).

---

## 2. The Skyline Silhouette

The Skyline Problem is the ultimate test of interval mastery. You are given buildings (intervals with a height) and must return the contour of their combined silhouette.

Why does a simple sweep line fail here?
Because when the tallest building ends, the new height of the skyline is determined by the **second tallest building that is still active**. A simple scalar `max_height` variable cannot remember the second tallest building. We need a data structure that provides the maximum element instantly, while also allowing elements to be removed when they expire.

The master pattern is the **Event-Driven Max-Heap Sweep**:
1.  **Deconstruct into Events:** Split every building `[left, right, height]` into two events: an Entry `(left, height)` and an Exit `(right, height)`. 
2.  **Sort the Events:** Process them left to right.
3.  **Active State Heap:** Maintain a max-heap of all currently active buildings. When you process an Entry, push it to the heap.
4.  **Lazy Deletion:** When a building exits, finding it in the heap to delete it takes $O(N)$. Instead, we do **lazy deletion**. We store the `right` boundary in the heap alongside the height: `(-height, right)`. At any given sweep point `x`, before querying the maximum height, we simply `pop` the top of the heap if its `right` boundary is $\leq x$. If the expired building is buried deep in the heap, we just leave it there until it eventually floats to the top and is popped!
5.  **Record Changes:** After lazy deletion, the top of the heap is the true current height. If it differs from the last recorded height in our answer array, we add a new key point to the skyline.

---

## 3. The Edge Case of Vertical Overlaps

Sorting the deconstructed events in the Skyline problem requires extreme precision to handle ties at the same X-coordinate.
If you process an Exit before an Entry at the exact same X-coordinate, the heap might temporarily empty out, creating a fake drop to height 0 in the skyline before the new building is added.

To perfectly resolve ties:
*   Entries must be processed before Exits.
*   If two Entries share an X, the TALLER one must be processed first (so the skyline jumps directly to the highest point without generating intermediate steps).
*   If two Exits share an X, the SHORTER one must be processed first.

A brilliant Python trick is encoding the Entry height as a negative number: `(left, -height, right)`. When Python sorts tuples, it sorts by X. If X ties, it sorts by the negative height, which natively forces taller Entries to process first! Exit events are encoded with 0 height `(right, 0, 0)`, ensuring they naturally sort appropriately.

---

## 4. The Path-Compressed Jump Array

The "Amount of New Area Painted Each Day" problem asks us to track intervals dynamically, but with a twist: we only care about the *new* area covered. If you paint `[1, 5]` and then `[2, 8]`, the second day only paints the sub-interval `[5, 8]`.

While this can be solved with a Segment Tree, a uniquely elegant and fast approach for 1D intervals is the **Jump Array**.
Instead of sweeping the whole timeline, we use an array `jumps` where `jumps[i]` stores the coordinate of the next unpainted pixel if pixel `i` is already painted.

1.  If `jumps[curr] == 0`, the pixel is unpainted. Paint it, and set `jumps[curr] = curr + 1`.
2.  If `jumps[curr] != 0`, the pixel is already painted! Instead of looping through painted pixels one by one (which causes $O(N^2)$ TLE), we jump instantly: `curr = jumps[curr]`.
3.  **Path Compression:** Every time we jump, we update the jump pointer to the very end of the current paint job: `jumps[curr] = max(jumps[curr], end)`. This ensures that subsequent operations skip massive painted blocks in $O(1)$ amortized time.

This technique is mathematically identical to the Disjoint Set Union (Union-Find) algorithm with path compression, applied to a 1D timeline!

---

## 5. Master Templates

```python
import heapq

# 1. Event-Driven Max-Heap (Skyline)
def get_skyline(buildings):
    events = []
    for l, r, h in buildings:
        events.append((l, -h, r))  # Entry (negative height for tie-breaking)
        events.append((r, 0, 0))   # Exit
    events.sort()
    
    active = [(0, float('inf'))]   # Max-heap: (-height, right_bound)
    res = []
    
    for x, neg_h, right in events:
        if neg_h != 0:
            heapq.heappush(active, (neg_h, right))
            
        # Lazy Deletion
        while active[0][1] <= x:
            heapq.heappop(active)
            
        curr_max = -active[0][0]
        if not res or res[-1][1] != curr_max:
            res.append([x, curr_max])
            
    return res


# 2. Path-Compressed Jump Array (Amount Painted)
def amount_painted(paint):
    max_pos = max(end for _, end in paint)
    jumps = [0] * (max_pos + 1)
    res = []
    
    for start, end in paint:
        work = 0
        curr = start
        while curr < end:
            if jumps[curr] == 0:
                work += 1
                jumps[curr] = curr + 1
                curr += 1
            else:
                next_pos = jumps[curr]
                jumps[curr] = max(jumps[curr], end) # Compress path
                curr = next_pos
        res.append(work)
        
    return res
```

---

## Problem: The Skyline Problem

* **Interview Difficulty:** Hard
* **Problem Type:** Event-Driven Sweep Line / Max-Heap with Lazy Deletion
* **Data Structure Used:** Sorted Event Array + Max-Heap
* **Optimized Approach:** Deconstruct buildings into Entry and Exit events. Sort by X-coordinate. Sweep through events, pushing Entries to a max-heap. For Exits, rely on lazy deletion: only pop the top of the heap if its right boundary is less than or equal to the current X. The height of the skyline is always the height of the valid building at the top of the heap.
* **Complexity:**
  * **Time:** $O(N \log N)$ (sorting events + heap operations).
  * **Space:** $O(N)$ for the events array and the heap.
* **Pointer Flow:**
```text
buildings = [[2,9,10], [3,7,15]]
Events: (2, -10, 9), (3, -15, 7), (7, 0, 0), (9, 0, 0)
Heap starts: [(0, inf)]

(2, -10, 9): Push. Heap=[(-10,9), (0,inf)]. Top is 10. Res=[[2,10]]
(3, -15, 7): Push. Heap=[(-15,7), (-10,9), (0,inf)]. Top is 15. Res=[[2,10], [3,15]]
(7, 0, 0):   Cleanup loop: Top is (-15,7). 7 <= current X(7). POP IT!
             Heap=[(-10,9), (0,inf)]. Top is 10. Res=[[2,10], [3,15], [7,10]]
(9, 0, 0):   Cleanup loop: Top is (-10,9). 9 <= current X(9). POP IT!
             Heap=[(0,inf)]. Top is 0. Res=[[2,10], [3,15], [7,10], [9,0]]
```
* **Pattern Recognition:**
  * Determining the "maximum" or "winning" interval among multiple overlapping intervals at any coordinate.
* **Core Insight:** Lazy Deletion is the secret weapon of heap-based sweep lines. Finding and removing an element in a heap is $O(N)$. By ignoring expired elements until they reach the top, we maintain $O(\log N)$ performance and completely eliminate the need for complex balanced BSTs.

---

## Problem: Amount of New Area Painted Each Day

* **Interview Difficulty:** Hard
* **Problem Type:** Path-Compressed Jump Array (1D Union-Find)
* **Data Structure Used:** Array
* **Optimized Approach:** Use a `jumps` array initialized to 0. For each paint interval, iterate `curr` from `start` to `end`. If `jumps[curr] == 0`, the spot is unpainted; paint it, increment work, and step forward. If `jumps[curr] != 0`, it's painted; jump `curr` to `jumps[curr]` immediately. Crucially, apply path compression during jumps: `jumps[curr] = max(jumps[curr], end)` so future sweeps skip the whole block at once.
* **Complexity:**
  * **Time:** Amortized $O(N + M)$ where $N$ is intervals and $M$ is the max coordinate, due to path compression skipping overlaps.
  * **Space:** $O(M)$ for the jump array.
* **Pattern Recognition:**
  * Painting, filling, or counting unique coverage on a timeline with heavy redundant overlaps.
* **Core Insight:** If a coordinate is already processed, you shouldn't step through it again. The jump array creates a teleportation network across the timeline that dynamically updates itself to skip known territory, mirroring the exact mechanics of Disjoint Set Union (DSU) without the overhead of tree structures.
