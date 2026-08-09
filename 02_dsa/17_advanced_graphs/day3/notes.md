## Prim's Minimum Spanning Tree Algorithm

* **Problem Type:** Minimum Spanning Tree / Vertex-Centric Greedy
* **Data Structure Used:** Boolean `visited` array + Min-Heap
* **Approach 1:** For each vertex not yet in the MST, scan all edges to find the minimum weight edge connecting it to the current MST. This is $O(V^2)$ per addition and $O(V^3)$ total — acceptable for dense graphs but slow for sparse graphs with a heap.
* **Optimized Approach:** Prim's with Lazy Deletion via Min-Heap. Start from an arbitrary seed vertex with cost 0. Maintain a min-heap of `(weight, vertex)` tuples. Pop the minimum weight vertex, mark it visited, add its weight to the MST cost, and push all unvisited neighbors to the heap. Stale entries (vertices already visited) are simply skipped when popped.
* **Complexity:**
  * **Time:** $O(E \log E)$ with lazy deletion. Every edge can be pushed to the heap at most twice (once from each endpoint), giving $O(E)$ heap operations each costing $O(\log E)$.
  * **Space:** $O(V + E)$ for the visited array and heap.
* **Pointer Flow:**
```text
Graph: 3 nodes (0,1,2), edges: 0-1 weight 2, 0-2 weight 3, 1-2 weight 1
Adjacency: adj[0]=[(1,2),(2,3)], adj[1]=[(0,2),(2,1)], adj[2]=[(0,3),(1,1)]

Initial: visited=[F,F,F], heap=[(0,0)], mst_cost=0, cnt=0

Pop (0, 0): visited[0]=True, mst_cost=0, cnt=1
  Push neighbors: heap=[(2,1),(3,2)]

Pop (2, 1): visited[1]=True, mst_cost=2, cnt=2
  Push unvisited neighbors: heap=[(1,2),(3,2)] (push (1,2) from adj[1])

Pop (1, 2): visited[2]=True, mst_cost=3, cnt=3. cnt==V=3. Done!
  (Entry (3,2) is now stale and will be ignored when popped)

MST cost = 3. Edges used: (0,1,w=2), (1,2,w=1).
```
* **Pattern Recognition:**
  * Use Prim's when:
    - The graph is dense ($E$ is close to $V^2$) because $O(V^2)$ Prim's without a heap outperforms Kruskal's $O(E \log E)$ in this regime.
    - The graph is given as an adjacency matrix rather than an edge list.
    - You want to grow the MST incrementally from a specific root vertex.
* **Core Insight:** Prim's and Kruskal's are both correct because they both apply the Cut Property. At every step of Prim's, there is a natural cut: the visited cloud (current MST) on one side and all unvisited nodes on the other side. The heap always gives the minimum weight edge crossing this cut. By the Cut Property, this edge belongs to some MST. Prim's greedily selects these edges in sequence, producing a valid MST.

  The key difference from Kruskal's: Prim's grows a single connected tree from one vertex outward (vertex-centric), while Kruskal's merges disconnected components from globally cheapest edges (edge-centric). For sparse graphs, Kruskal's is preferable because sorting $E$ edges is cheaper. For dense graphs, Prim's $O(V^2)$ matrix-based version outperforms Kruskal's $O(E \log E) = O(V^2 \log V)$.
* **Mistakes Made:** Not implementing the staleness check. When a cheaper path to a vertex $v$ is found after $v$ was already pushed to the heap, the old entry becomes stale. If we process it again and re-add $v$'s edges, we either double-count the MST cost or add non-optimal edges. Always check `if visited[u]: continue` immediately after popping.
* **What I Learned:** Lazy deletion is a powerful pattern for priority queues. Instead of maintaining a heap with unique entries (which requires decrease-key operations), we allow stale entries and simply skip them. This trades a smaller heap for simpler code and is valid whenever processing a stale entry has no side effects (just skip it).

---

### Master Patterns Learned

#### 1. The Vertex Expansion Min-Heap Frame (Prim's)
* **Applied to:** Prim's MST, Minimum Cost to Connect Points
* **The Strategy:** Seed the heap with (0, start_vertex). Pop minimum cost entry, mark visited, add to MST, push all unvisited neighbors. Skip already-visited vertices when popped.
* **Code Pattern:**
```python
import heapq

def prim(n, adj):
    visited = [False] * n
    heap = [(0, 0)]
    mst_cost = 0
    cnt = 0

    while cnt < n:
        w, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        mst_cost += w
        cnt += 1
        for v, wt in adj[u]:
            if not visited[v]:
                heapq.heappush(heap, (wt, v))

    return mst_cost
```
