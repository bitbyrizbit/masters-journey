## Problem: Find Median from Data Stream

* **Problem Type:** Dynamic Continuous Partitioning / Dual-Heap Balancing Architecture
* **Data Structure Used:** Max-Heap + Min-Heap (Two lists managed via `heapq`)
* **Approach 1:** Insertion Sort Stream. Maintain a standard Python list, insert each arriving stream number into its exact sorted position using `bisect.insort()`. While this keeps the array layout continuously sorted, shifting elements down an array on every injection forces a slow $O(n)$ time tax per number, completely bottlenecking long stream paths.
* **Optimized Approach:** Divide the stream dynamically into two symmetric halves. Store the lower half of the numbers inside a sign-inverted Max-Heap (`small`) and the upper half inside a standard Min-Heap (`large`). Drive an automated balancing pipeline on every insert: push to `small`, verify that the lower max doesn't cross the upper min, and enforce a size constraint where `small` can hold at most one extra element over `large`. This pins the median search to index `0` of both heaps in constant time.
* **Complexity:**
  * **Time:** `addNum` executes in $O(\log n)$ time due to heap insertion and balancing adjustments. `findMedian` executes in $O(1)$ constant time by reading root nodes.
  * **Space:** $O(n)$ linear heap buffer space required to store all incoming stream elements.
* **Pointer Flow:**
```text
Stream injections: 1, then 2, then 3
1. addNum(1) -> push to small -> small=[-1], large=[]
2. addNum(2) -> push to small -> small=[-2, -1], large=[]
                Cross Check -> large is empty -> Skip
                Size Check   -> len(small) > len(large)+1 -> Pop 2 to large
                Final: small=[-1], large=[2] -> Median: (1 + 2) / 2.0 = 1.5
3. addNum(3) -> push to small -> small=[-3, -1], large=[2]
                Cross Check -> -small[0] (3) > large[0] (2) - Move 3 from small to large.
                Final Balancing: small=[-2, -1], large=[3] -> Median: -small[0] = 2.0
```
* **Pattern Recognition:**
  * Use a dual-heap structural partition pattern when:
    - The problem requires tracking a rolling median, dynamic quantile, or midpoint across an ever-growing sequence of numbers.
    - Sorting an entire dataset on every update is too expensive, but you need constant-time extraction paths to the middle elements.
* **Core Insight:** The median depends exclusively on the two values right at the boundary of a sorted partition. By splitting the dataset down the center, the highest value of the lower half floats to the top of your Max-Heap, and the lowest value of the upper half floats to the top of your Min-Heap. The rest of the inner tree structures can stay unsorted, completely bypassing heavy sorting sweeps.
* **Mistakes Made:** The primary conceptual block was managing cross-heap element collisions. If a large number is pushed into `small`, it can violate the partition rule (`-small[0] > large[0]`). Forgetting to execute an immediate corrective swap step right after insertion allows values to overlap, corrupting the boundary threshold and resulting in incorrect median math calculations.
* **What I Learned:** Balancing two opposing priority queues locks data midpoints down cleanly. It transforms an expensive linear insertion task into two ultra-fast, symmetric logarithmic pointer adjustments.

---

## Problem: IPO

* **Problem Type:** Greedy Resource Optimization / Two-Stage Filtering Array + Heap
* **Data Structure Used:** Zipped Array Pointer + Max-Heap (Tuple filtering via sign-inversion)
* **Approach 1:** Exhaustive Linear Scanning. On each of the $k$ investment selections, scan the entire projects list to find all available elements where capital is less than or equal to current wealth $w$, pick the one with the maximum profit, delete it from the dataset, and repeat. This forces an expensive $O(k \cdot n)$ runtime crash that fails on wide project spaces.
* **Optimized Approach:** Decouple capital requirements from profit optimization. First, pre-sort the projects by their capital requirements in ascending order. Drive a loop exactly $k$ times: run a sliding index cursor `i` forward to ingest all newly affordable projects into a sign-inverted profit Max-Heap. Pop the highest profit available from the top, add it to your wealth $w$, and carry it forward as the new capital threshold for the next pass.
* **Complexity:**
  * **Time:** $O(n \log n + k \log n)$ where $n$ is total projects and $k$ is the selection cap, dominated by the initial sort and greedy heap extractions.
  * **Space:** $O(n)$ memory allocations required to house the zipped array tracking maps.
* **Pointer Flow:**
```text
Greedy resource selections with k = 2, w = 0, cap=[0,1,1], profits=[1,2,3]
Sorted projects: [(0, 1), (1, 2), (1, 3)]

Pass 1 (j=0): w=0. Slide i forward. proj[0] cap 0 <= 0. Push -1 to heap. i=1.
             Max-Heap: [-1]. Pop profit 1 -> w = 0 + 1 = 1.
Pass 2 (j=1): w=1. Slide i forward. proj[1] cap 1 <= 1 -> Push -2.
                                  proj[2] cap 1 <= 1 -> Push -3. i=3.
             Max-Heap: [-3, -2]. Pop profit 3 -> w = 1 + 3 = 4. Final wealth: 4.
```
* **Pattern Recognition:**
  * Use a two-stage filter (Sorted Array + Max-Heap) when:
    - You must optimize a greedy choice (maximize profits) subject to a constraint that grows monotonically (capital wealth $w$).
    - The pool of available choices expands dynamically as your baseline resource accumulator increases.
* **Core Insight:** Projects only become available when your wealth hits their capital wall. Sorting the projects by capital allows a single linear cursor `i` to safely sweep entries into the selection pool without ever looking backward. Once inside the heap, capital constraints disappear, allowing you to focus exclusively on profit maximization in pure logarithmic time.
* **Mistakes Made:** The primary cognitive challenge was preventing the sliding cursor `i` from resetting back to `0` on every project selection loop. Resetting the pointer re-evaluates previously pushed projects, creating a slow quadratic bottleneck. Leaving `i` as a progressive, non-local tracking variable guarantees that each project enters the heap exactly once across the entire timeline.
* **What I Learned:** Separating qualifying constraints from priority selection saves processing steps. Combining a pre-sorted array with a greedy heap extraction pipeline turns a messy multidimensional optimization problem into a clean, linear sweep.

---

## Problem: Design Twitter

* **Problem Type:** Multi-Stream Aggregation / Priority Queue K-Way Merge
* **Data Structure Used:** Hash Map + Deque + Min-Heap (`defaultdict` + `list` + `set`)
* **Approach 1:** Flatten and Sort. To build the news feed, pull every single tweet posted by all followed users into one massive global list array and run a heavy full sort loop on their timestamps. This implementation scales poorly because it wastes energy sorting old, historical logs when the query only asks for the top 10 most recent posts.
* **Optimized Approach:** k-Way Stream Merge (Heapsort variant). Track chronological posts using a global decreasing integer counter `self.count -= 1`. To pull the feed, peek *only* at the absolute most recent tweet pointer from each followee, and push them into a Min-Heap tracking tuples formatted as `[timestamp_count, tweetId, followeeId, index - 1]`. The most recent tweet has the smallest timestamp value. Pop the top item, add it to your results, read the decremented index offset variable, and instantly re-inject the next most recent tweet from *that specific user's stream* back into the heap. Repeat until 10 entries are collected.
* **Complexity:**
  * **Time:** `postTweet` runs in $O(1)$ constant time. `getNewsFeed` runs in $O(f + 10 \log f)$ time where $f$ is the number of followed accounts, as the heap size is capped tightly by the followee count.
  * **Space:** $O(u + t)$ where $u$ is total system users and $t$ is total tweets stored in history maps.
* **Pointer Flow:**
```text
k-Way Merge Feed Generation tracking for User 1 following User 2:
User 1 Tweets: [[0, tweet5]] -> pointer index = 0
User 2 Tweets: [[-1, tweet6]] -> pointer index = 0

1. Heapify Initialization (Peek at the tail end of each followee's list):
   min_heap = [[0, tweet5, user1, index=-1], [-1, tweet6, user2, index=-1]]
   heapq.heapify(min_heap) -> organizes so lowest timestamp count sits at top.

2. Feed Extraction Loop (Runs max 10 times):
   Pop top item: [-1, tweet6, user2, index=-1] -> Appends tweet6 to feed.
   Index is -1 (User 2 stream exhausted) -> Skip re-injection.
   Pop next item: [0, tweet5, user1, index=-1]  -> Appends tweet5 to feed. Loop terminates.
```
* **Core Insight:** This problem implements a classic **k-Way Merge** algorithm, matching core database indexing engines. Instead of wasting energy sorting thousands of historical entries, treating each user's timeline as an already sorted stream allows a priority queue to coordinate head elements. You only extract the globally newest item across the channels, pulling deeper elements from that specific timeline only when a spot opens up.
* **Mistakes Made:** The hardest thought-driven hurdle was figuring out how to handle the boundary state where a user follows themselves or follows accounts with zero posts. Forgetting to explicitly initialize a user's own account inside their follow map (`self.followMap[userId].add(userId)`) causes their own tweets to vanish from their personal timeline view entirely.
* **What I Learned:** Managing complex system data feeds requires structured coordinate index pointers. A k-way heap merge keeps extraction loops fast and independent of stream size, ensuring optimal runtime scaling.

---

### Master Patterns Learned

#### 1. Dual-Heap Boundary Partitioning (The Dynamic Quantile Frame)
* **Applied to:** Find Median from Data Stream
* **The Strategy:** Use this architectural blueprint when your system requires real-time, high-frequency extraction of a running midpoint, median, or dynamic quantile across an ever-growing, unstructured stream of data. Instead of wasting processing steps keeping a whole array sorted, partition the data domain down the middle using two opposing, balanced priority queues facing each other.
* **The Conceptual Mechanics:**
  - **Opposing Priority Alignment:** By storing the lower half of your numbers inside a sign-inverted Max-Heap (`small`) and the upper half inside a standard Min-Heap (`large`), the two boundary elements of the sorted partition float directly to the top of their respective structures. The root of `small` is the maximum value of the lower tier, and the root of `large` is the minimum value of the upper tier, isolating the median calculation to index `0` of both heaps.
  - **Dynamic Equilibrium:** Maintaining this structural orientation requires running two constraint checks on every insertion: a cross-over check (ensuring lower bounds never exceed upper bounds) and a size check (forcing the heaps to stay equal or at most +1 lopsided).
* **The Layout / Code Pattern:**
```python
import heapq

class ContinuousDomainPartition:
    def __init__(self):
        self.small_max_heap = []        # Stores lower half (Sign-Inverted)
        self.large_min_heap = []        # Stores upper half (Standard)
        
    def ingest_value(self, val: int) -> None:
        # 1. Pipeline entry: Route to lower pool first
        heapq.heappush(self.small_max_heap, -val)
        
        # 2. Corrective Cross-Over Check: Validate boundary alignment
        if (self.small_max_heap and self.large_min_heap and 
            (-self.small_max_heap[0] > self.large_min_heap[0])):
            maligned_lower_max = -heapq.heappop(self.small_max_heap)
            heapq.heappush(self.large_min_heap, maligned_lower_max)
            
        # 3. Structural Size Balance Check: Maintain equilibrium 
        if len(self.small_max_heap) > len(self.large_min_heap) + 1:
            lower_max = -heapq.heappop(self.small_max_heap)
            heapq.heappush(self.large_min_heap, lower_max)
        elif len(self.large_min_heap) > len(self.small_max_heap):
            upper_min = heapq.heappop(self.large_min_heap)
            heapq.heappush(self.small_max_heap, -upper_min)
            
    def extract_median(self) -> float:
        if len(self.small_max_heap) > len(self.large_min_heap):
            return float(-self.small_max_heap[0])
        return (-self.small_max_heap[0] + self.large_min_heap[0]) / 2.0
```
* **Examples:** Live sliding-window median filters, continuous running percentile monitors, database query optimization partitions, or dynamic thresholding sensors.

#### 2. Priority-Coordinated k-Way Stream Merging (The Multiplexed Data Combiner)
* **Applied to:** Design Twitter
* **The Strategy:** Use this pattern when you need to merge multiple independent, pre-sorted data streams into a single consolidated, top-$k$ output view (e.g., combining timeline logs from multiple channels). Instead of gathering and sorting entire datasets from scratch, initialize a priority queue by pulling *only the head element* of each individual stream. Pop the globally newest element, and use index tracking parameters to pull the next element from *that specific stream only*, keeping the heap size capped tightly by the number of streams.
* **The Conceptual Mechanics:**
  - **Leveraging Pre-Sorted Context:** Re-sorting data segments that are already ordered inside their home channels is redundant. Treating each channel as a sequential data stream allows the priority queue to act as a light coordinator, scanning only the active boundaries of the system.
  - **Index-Offset Memory Tracking:** To prevent pointer loss, every node inside the heap must carry its own structural metadata context formatted as `[priority_weight, payload, stream_source_id, parent_array_index]`. This metadata gives the pop loop a clear roadmap, telling it exactly which channel cursor to step forward next to refresh the selection pool.
* **The Layout / Code Pattern:**
```python
import heapq

def k_way_priority_merge(stream_map: dict, active_channels: list, top_k: int) -> list:
    min_heap = []
    consolidated_output = []
    
    # Phase 1: Initialize the coordinator with head items from each active channel
    for channel_id in active_channels:
        if channel_id in stream_map and stream_map[channel_id]:
            last_idx = len(stream_map[channel_id]) - 1
            priority_weight, payload = stream_map[channel_id][last_idx]
            
            # Pack comprehensive metadata tracking tuple
            min_heap.append([priority_weight, payload, channel_id, last_idx - 1])
            
    heapq.heapify(min_heap)         # Capped permanently at size of active channels
    
    # Phase 2: Interleaved extraction loop
    while min_heap and len(consolidated_output) < top_k:
        weight, payload, channel_id, current_cursor = heapq.heappop(min_heap)
        consolidated_output.append(payload)
        
        # Pull the next sequential item from the exhausted channel stream only
        if current_cursor >= 0:
            next_weight, next_payload = stream_map[channel_id][current_cursor]
            heapq.heappush(min_heap, [next_weight, next_payload, channel_id, current_cursor - 1])
            
    return consolidated_output
```
* **Examples:** Social media timeline feed consolidators, real-time log stream aggregators, merging pre-sorted external files (External Merge Sort), or distributed message brokers.