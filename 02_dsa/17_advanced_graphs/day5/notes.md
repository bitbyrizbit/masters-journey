## Problem: Bellman-Ford SSSP

* **Problem Type:** Single-Source Shortest Path / Negative Edge Handling
* **Data Structure Used:** Flat edge list + Distance array
* **Approach 1:** Dijkstra's on graphs with negative weights. Dijkstra's greedy choice property breaks immediately. Counter-example: nodes A, B, C. Edges: A->B weight 10, A->C weight 2, C->B weight -5. The shortest A->B path is through C: 2 + (-5) = -3. But Dijkstra's finalizes B's distance as 10 the first time B is popped (since 10 < inf when A is processed), and never reconsiders. The correct answer -3 is missed.
* **Optimized Approach:** Bellman-Ford. Iterate $V-1$ times over all edges. In each iteration, for each edge $(u, v, w)$, relax: if `dist[u] + w < dist[v]`, update `dist[v] = dist[u] + w`. After $V-1$ rounds, all shortest paths are discovered. Run a $V$-th round: if any distance can still be reduced, a negative cycle exists and shortest paths are undefined ($-\infty$).
* **Complexity:**
  * **Time:** $O(V \cdot E)$ — $V-1$ iterations, each scanning all $E$ edges.
  * **Space:** $O(V)$ for the distance array.
* **Pointer Flow:**
```text
Graph: 3 nodes (0,1,2). Edges: (0->1, w=4), (0->2, w=2), (2->1, w=-1).
dist = [0, inf, inf]

Round 1 (relaxing all edges):
  Edge (0->1, 4): dist[0]+4=4 < inf. dist[1]=4.
  Edge (0->2, 2): dist[0]+2=2 < inf. dist[2]=2.
  Edge (2->1,-1): dist[2]+(-1)=1 < dist[1]=4. dist[1]=1.
  After round 1: dist = [0, 1, 2]

Round 2 (no updates since graph has no further chains):
  All edges: no improvements possible.
  After round 2: dist = [0, 1, 2]

No negative cycle (V-th round: no improvements). Answer: dist = [0, 1, 2].
```
* **Pattern Recognition:**
  * Use Bellman-Ford when:
    - The graph contains **negative edge weights**.
    - You need to detect negative cycles.
    - The number of edges is small relative to $V$ (since runtime is $O(VE)$).
* **Core Insight:** Why $V-1$ iterations? In a graph with $V$ vertices and no negative cycles, the shortest path between any two vertices can use at most $V-1$ edges (any longer path must revisit a vertex, forming a cycle, which can only increase or maintain the path weight in a non-negative-cycle graph). After $k$ iterations of Bellman-Ford, `dist[v]` is guaranteed to be the shortest path using at most $k$ edges. So after $V-1$ iterations, all shortest paths are found.

  If a distance can still be reduced after $V-1$ iterations (the $V$-th iteration finds an improvement), it means there exists a cycle of length $V$ that is shorter than any path of length $V-1$. This is only possible if the cycle has negative total weight.

  The relaxation order within a round does not matter for correctness — the order only affects how many rounds are needed.
* **Mistakes Made:** Thinking that only one iteration is needed if edges happen to be given in topological order. While this is true for DAGs (one pass suffices), for general graphs with cycles, we truly need $V-1$ rounds. Another common mistake: forgetting to check for negative cycles after the algorithm terminates.
* **What I Learned:** Bellman-Ford trades Dijkstra's greedy speed for generality. By iterating multiple times, it propagates improvements through long chains of edges that Dijkstra's would have finalized prematurely.

---

## Problem: Cheapest Flights Within K Stops

* **Problem Type:** Constrained Shortest Path / Step-Limited Bellman-Ford
* **Data Structure Used:** Distance array + snapshot array
* **Approach 1:** BFS with a priority queue and stop count tracking. While feasible, it requires careful state management `(cost, node, stops_remaining)` and can have large state space.
* **Optimized Approach:** Step-Limited Bellman-Ford. Run exactly $K+1$ relaxation rounds (representing $K$ stops = $K+1$ edges). The critical fix: at the start of each round, copy `dist` to `tmp`. All reads come from `dist`, all writes go to `tmp`. Assign `dist = tmp` after each round. This prevents "chaining" — a single round inadvertently using edges from earlier in the same round to form a multi-hop path.
* **Complexity:**
  * **Time:** $O((K+1) \cdot E)$
  * **Space:** $O(V)$
* **Pointer Flow:**
```text
n=3, flights=[[0,1,100],[1,2,100],[0,2,500]], src=0, dst=2, k=1
dist = [0, inf, inf]

Round 1 (K+1=2 rounds total, this is round 1):
  tmp = [0, inf, inf]  (snapshot!)
  Edge (0->1, 100): dist[0]+100=100 < inf. tmp[1]=100.
  Edge (1->2, 100): dist[1]=inf, skip.
  Edge (0->2, 500): dist[0]+500=500 < inf. tmp[2]=500.
  dist = [0, 100, 500]

Round 2:
  tmp = [0, 100, 500]  (snapshot!)
  Edge (0->1, 100): dist[0]+100=100 >= tmp[1]=100. No update.
  Edge (1->2, 100): dist[1]+100=200 < tmp[2]=500. tmp[2]=200.
  Edge (0->2, 500): no update.
  dist = [0, 100, 200]

Return dist[2] = 200.
```
  Why is the snapshot critical? Without it:
  In Round 1 without snapshot, when we process edge (1->2), dist[1] has already been updated to 100 in the same round. So dist[1]+100=200 gets written. This is a 2-hop path computed in Round 1 — but Round 1 should only discover 1-hop paths. With K=1, we'd incorrectly use a 2-hop path!
* **Core Insight:** The snapshot (`tmp = list(dist)`) is the key insight distinguishing this from standard Bellman-Ford. Standard Bellman-Ford doesn't care about the per-round hop count — it just wants convergence. But the K-stops variant strictly enforces: round $i$ discovers paths using exactly $i$ edges. By reading from the old `dist` and writing to `tmp`, we prevent intra-round chaining. This transforms Bellman-Ford from a convergence algorithm into an exact hop-counting shortest path algorithm.
* **Mistakes Made:** Forgetting the snapshot (`tmp = list(dist)`) is the single most common bug in this problem. It looks like a minor detail but completely changes the semantic of a round from "at most $i$ hops" to "possibly unlimited hops."
* **What I Learned:** The snapshot pattern converts a relaxation-convergence algorithm into a step-counting algorithm. This technique appears in other problems too (e.g. BFS level-by-level tracking).

---

### Master Patterns Learned

#### 1. The Edge List Iterative Relaxation Frame (Bellman-Ford)
* **Applied to:** Bellman-Ford SSSP, Negative Cycle Detection
* **Code Pattern:**
```python
def bellman_ford(n, edges, src):
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # Negative cycle
    return dist
```

#### 2. The Snapshot-Bounded Relaxation Frame (K-Stop Bellman-Ford)
* **Applied to:** Cheapest Flights Within K Stops
* **Code Pattern:**
```python
def cheapest_flights(n, flights, src, dst, k):
    dist = [float('inf')] * n
    dist[src] = 0
    for _ in range(k + 1):
        tmp = list(dist)
        for u, v, w in flights:
            if dist[u] != float('inf') and dist[u] + w < tmp[v]:
                tmp[v] = dist[u] + w
        dist = tmp
    return dist[dst] if dist[dst] != float('inf') else -1
```
