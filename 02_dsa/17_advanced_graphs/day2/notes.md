## Kruskal's Minimum Spanning Tree Algorithm

* **Problem Type:** Minimum Spanning Tree (MST) / Edge-Centric Greedy
* **Data Structure Used:** Sorted edge list + Disjoint Set Union (DSU)
* **Approach 1:** Brute force. Enumerate all possible subsets of $V-1$ edges from $E$ total edges. Check if the subset forms a spanning tree (connected, no cycles). Keep the subset with minimum total weight. There are $\binom{E}{V-1}$ subsets, making this exponential and completely infeasible.
* **Optimized Approach:** Kruskal's Algorithm. Sort all edges by weight in ascending order. Initialize a DSU with all $V$ nodes as separate components. Greedily add edges: for each edge $(u, v, w)$ in sorted order, if `find(u) != find(v)` (they are in different components), add this edge to the MST and call `union(u, v)`. Stop when $V-1$ edges have been added. The result is the minimum spanning tree.
* **Complexity:**
  * **Time:** $O(E \log E)$ dominated by the sorting step. The DSU operations across all edges take $O(E \cdot \alpha(V)) \approx O(E)$.
  * **Space:** $O(V + E)$ for the DSU arrays and edge list.
* **Pointer Flow:**
```text
Graph: 4 nodes (0..3), edges by (weight, u, v):
  (1, 0, 1), (2, 1, 2), (3, 0, 3), (4, 2, 3), (5, 1, 3)

Sorted edges: [(1,0,1),(2,1,2),(3,0,3),(4,2,3),(5,1,3)]
DSU: parent=[0,1,2,3], rank=[1,1,1,1], mst_cost=0, edges_used=0

1. Edge (1, 0, 1): find(0)=0, find(1)=1. Different! union(0,1).
   mst_cost=1, edges_used=1. parent=[0,0,2,3]

2. Edge (2, 1, 2): find(1)->parent[1]=0->root 0. find(2)=2. Different!
   union(0,2). mst_cost=3, edges_used=2. parent=[0,0,0,3]

3. Edge (3, 0, 3): find(0)=0. find(3)=3. Different!
   union(0,3). mst_cost=6, edges_used=3. parent=[0,0,0,0]
   edges_used == V-1 = 3. STOP!

MST edges: (0,1,w=1), (1,2,w=2), (0,3,w=3). Total weight = 6.
```
* **Pattern Recognition:**
  * Use Kruskal's when:
    - The graph is sparse (few edges relative to $V^2$) because sorting $E$ edges is cheap.
    - You have all edges available upfront (static graph).
    - You need to build an MST incrementally edge by edge.
* **Core Insight:** Kruskal's correctness rests on the **Cut Property** of MSTs: for any partition of the graph's vertices into two non-empty sets $S$ and $V \setminus S$, the minimum weight edge crossing the cut belongs to every MST.

  When Kruskal's picks the globally cheapest edge that doesn't form a cycle, it is implicitly working with the cut defined by the two components being merged. At that moment, the picked edge is the minimum weight edge crossing that cut (by the sorting order). Since no cheaper crossing edge exists, including it in the MST is optimal.

  This proves that every edge Kruskal's adds is "safe" — it belongs to at least one MST. Since we add exactly $V-1$ safe edges, the final result is a valid MST.
* **Mistakes Made:** Forgetting to terminate early when $V-1$ edges have been added. Without early termination, we continue processing all remaining edges unnecessarily. Also, confusing Kruskal's (which sorts edges globally) with Prim's (which grows a tree locally). In Kruskal's, edges from any part of the graph can be added in any order as long as they are safe — this is the global vs local distinction.
* **What I Learned:** Greedy algorithms work when a locally optimal choice (cheapest safe edge) is globally optimal. The Cut Property provides the mathematical guarantee that justifies greedy edge selection for MSTs.

---

### Master Patterns Learned

#### 1. The Density-Sorted DSU Sweep (Kruskal's)
* **Applied to:** MST, Minimum Cost to Connect All Points
* **The Strategy:** Flatten all edges into a list, sort by weight, sweep through adding safe edges using DSU cycle detection, terminate when V-1 edges are added.
* **Code Pattern:**
```python
def kruskal(n, edges):
    edges.sort()
    parent = list(range(n))

    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]

    mst_cost = 0
    edges_used = 0
    for w, u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[rv] = ru
            mst_cost += w
            edges_used += 1
            if edges_used == n - 1:
                break
    return mst_cost
```
