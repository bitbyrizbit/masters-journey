## Problem: Dijkstra's Shortest Path

* **Problem Type:** Single-Source Shortest Path (SSSP) / Non-Negative Weighted Graphs
* **Data Structure Used:** Distance array + Min-Heap
* **Approach 1:** BFS on weighted graphs. BFS finds the fewest-edge path, not the minimum-weight path. Counter-example: a direct edge from $A$ to $B$ with weight 100, but a 3-hop path $A \to C \to D \to B$ with weights 1+1+1=3. BFS picks the direct edge. This is wrong.
* **Optimized Approach:** Dijkstra's Algorithm. Initialize `dist[source] = 0` and `dist[v] = inf` for all others. Push `(0, source)` to a min-heap. Greedily pop the vertex $u$ with the smallest tentative distance. For each neighbor $v$ of $u$, relax the edge: if `dist[u] + w(u,v) < dist[v]`, update `dist[v]` and push the new distance to the heap. Skip stale heap entries using the staleness check.
* **Complexity:**
  * **Time:** $O((V + E) \log V)$ with a binary heap. Each vertex is finalized once, each edge causes at most one heap push.
  * **Space:** $O(V + E)$ for the distance array and heap.
* **Pointer Flow:**
```text
Network Delay Time: n=4, k=2, times=[[2,1,1],[2,3,1],[3,4,1]]
adj[2] = [(1,1),(3,1)], adj[3] = [(4,1)]
dist = [inf, inf, 0, inf, inf] (1-indexed), heap = [(0, 2)]

Pop (0, 2): d=0 == dist[2]=0. Process neighbors:
  (1,1): dist[1] > 0+1=1. Update dist[1]=1. Push (1,1).
  (3,1): dist[3] > 0+1=1. Update dist[3]=1. Push (1,3).
  heap = [(1,1),(1,3)]

Pop (1, 1): d=1 == dist[1]=1. No outgoing edges from node 1. No updates.

Pop (1, 3): d=1 == dist[3]=1. Process neighbors:
  (4,1): dist[4] > 1+1=2. Update dist[4]=2. Push (2,4).

Pop (2, 4): d=2 == dist[4]=2. No outgoing edges. Done.
dist = [inf, 1, 0, 1, 2]. Max = 2. Return 2.
```
* **Pattern Recognition:**
  * Use Dijkstra's when:
    - All edge weights are **non-negative**.
    - You need shortest paths from one source to all other nodes.
    - The graph is sparse to medium density (heap-based Dijkstra) or dense (matrix-based Dijkstra with $O(V^2)$).
* **Core Insight:** Dijkstra's correctness rests on the **Greedy Choice Property**: once a vertex $u$ is popped from the min-heap (with its minimum tentative distance $d$), that distance is guaranteed to be the true shortest path distance. Why? Because all edge weights are non-negative. Any alternative path to $u$ through other unvisited vertices would have to traverse at least one edge with weight $\ge 0$, making it at least as long as $d$. So the heap's minimum is always finalized.

  This is precisely why Dijkstra's fails with negative edges: a negative edge could create an alternate path that is shorter than what the heap says, but we would have already finalized $u$'s distance before discovering it.

  The **staleness check** (`if d > dist[u]: continue`) is essential. When a shorter path to $u$ is found after $u$ was already pushed to the heap, both the old and new entries coexist. When the stale old entry is popped, we skip it to avoid reprocessing $u$ with an outdated (larger) distance.
* **Mistakes Made:** Forgetting the staleness check. Without it, stale heap entries cause redundant neighbor relaxations and, worse, incorrect updates if we process the same node twice with different distances. Also, using a max-heap instead of a min-heap — Dijkstra's requires minimum first because we are minimizing distances.
* **What I Learned:** Dijkstra's is essentially BFS supercharged with a priority queue. The non-negative weight constraint is not a limitation — it is the mathematical guarantee that justifies the greedy finalization of each popped vertex.

---

## Problem: Network Delay Time

* **Problem Type:** Single-Source Shortest Path Application
* **Data Structure Used:** Distance dictionary + Min-Heap + Adjacency list
* **Approach 1:** Bellman-Ford. Relax all edges $V-1$ times. Works correctly but runs in $O(V \cdot E)$, which is slower than Dijkstra's for non-negative weights.
* **Optimized Approach:** Dijkstra's from source $k$. After computing all shortest paths, the answer is the maximum value in the distance dictionary (the time for the last node to receive the signal). If any node has distance $\infty$ (unreachable), return $-1$.
* **Complexity:**
  * **Time:** $O((V + E) \log V)$
  * **Space:** $O(V + E)$
* **Core Insight:** The signal reaches all nodes simultaneously, but each node receives it at the time equal to the shortest path from the source. The delay for the entire network is determined by the slowest node — the maximum shortest path distance.

---

### Master Patterns Learned

#### 1. The Min-Heap Relaxation Frame (Dijkstra's)
* **Applied to:** Network Delay Time, Cheapest Paths, Shortest Path Grid Problems
* **The Strategy:** Initialize source distance to 0. Use min-heap to always process the minimum tentative distance next. Skip stale entries. Relax neighbors on each processed vertex.
* **Code Pattern:**
```python
import heapq
import collections

def dijkstra(n, times, src):
    adj = collections.defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))

    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[src] = 0
    heap = [(0, src)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))

    mx = max(dist.values())
    return mx if mx != float('inf') else -1
```
