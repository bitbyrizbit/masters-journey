## Floyd-Warshall All-Pairs Shortest Path

* **Problem Type:** All-Pairs Shortest Path (APSP) / Dynamic Programming on Graphs
* **Data Structure Used:** 2D Distance Matrix of size $V \times V$
* **Approach 1:** Run Dijkstra's from every source vertex. Time: $O(V \cdot (V + E) \log V)$. This works for non-negative weights but fails for negative edges. With Bellman-Ford as SSSP: $O(V^2 \cdot E)$. For dense graphs where $E \approx V^2$, Floyd-Warshall's $O(V^3)$ is competitive or better.
* **Optimized Approach:** Floyd-Warshall DP. Define the state: `dist[i][j]` = shortest path from $i$ to $j$ using a progressively expanding set of allowed intermediate vertices. Expand the allowed set one vertex at a time (the outer loop over $k$). For each pair $(i, j)$, decide whether routing through vertex $k$ is cheaper: `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.
* **Complexity:**
  * **Time:** $O(V^3)$ — three nested loops, each of size $V$.
  * **Space:** $O(V^2)$ for the distance matrix.
* **Pointer Flow:**
```text
Graph: 4 nodes (0..3). Initial dist matrix (inf where no direct edge):
        0    1    2    3
  0: [  0,   3, inf,   7 ]
  1: [  8,   0,   2, inf ]
  2: [  5, inf,   0,   1 ]
  3: [  2, inf, inf,   0 ]

k=0 (allow node 0 as intermediate):
  i=1,j=3: dist[1][0]+dist[0][3] = 8+7 = 15. Currently inf. Update: dist[1][3]=15.
  i=2,j=0: dist[2][0]+dist[0][0] = 5+0 = 5. Same. No change.
  i=3,j=1: dist[3][0]+dist[0][1] = 2+3 = 5. Currently inf. Update: dist[3][1]=5.
  i=3,j=3: dist[3][0]+dist[0][3] = 2+7 = 9. Currently 0. No change.

k=1 (allow nodes 0,1 as intermediate):
  i=0,j=2: dist[0][1]+dist[1][2] = 3+2 = 5. Currently inf. Update: dist[0][2]=5.
  i=2,j=2: no useful update (0).
  i=3,j=2: dist[3][1]+dist[1][2] = 5+2 = 7. Currently inf. Update: dist[3][2]=7.

k=2, k=3: Further refinements...
Final dist matrix converges to all-pairs shortest paths.
```
* **Pattern Recognition:**
  * Use Floyd-Warshall when:
    - You need shortest paths between **all pairs** of vertices.
    - The graph is small enough ($V \le 500$) for $O(V^3)$ to be feasible.
    - The graph may contain negative edges (but no negative cycles).
    - You need the transitive closure (can $i$ reach $j$?) — replace min with OR.
* **Core Insight:** The correctness of Floyd-Warshall comes from the DP state definition: after processing the outer loop for $k = 0, 1, ..., K$, `dist[i][j]` holds the shortest path from $i$ to $j$ using only vertices $\{0, 1, ..., K\}$ as intermediaries.

  The recurrence is: $\text{dist}[i][j]^{(k)} = \min(\text{dist}[i][j]^{(k-1)}, \text{dist}[i][k]^{(k-1)} + \text{dist}[k][j]^{(k-1)})$

  This says: either we don't use vertex $k$ as an intermediate (first term), or we route through $k$ — going from $i$ to $k$ optimally, then from $k$ to $j$ optimally, both using only vertices $0..k-1$ as intermediaries.

  **Why must $k$ be the outermost loop?** If $i$ or $j$ were the outermost loop, when we compute `dist[i][j]` for some inner $k$, we might use a `dist[i][k]` that was computed using vertex $j$ as an intermediate — creating a circular dependency. With $k$ outermost, when we process pair $(i, j)$ for intermediate node $k$, both `dist[i][k]` and `dist[k][j]` have been fully optimized using only nodes $0..k-1$, which is exactly the state we need.

  **Detecting negative cycles:** After running Floyd-Warshall, if `dist[i][i] < 0` for any node $i$, then node $i$ lies on a negative cycle.
* **Mistakes Made:** Getting the loop order wrong. Putting $i$ or $j$ as the outermost loop is a classic error that produces incorrect results on graphs with multi-hop paths. The safe mnemonic: "K is King — it goes on the outside."
* **What I Learned:** Floyd-Warshall elegantly solves APSP by expanding the allowed set of intermediate nodes one at a time, turning a seemingly $O(V^3)$ brute force into a principled DP. The three-line implementation (three nested loops + one min operation) is deceptively simple but carries deep mathematical correctness.

---

### Master Patterns Learned

#### 1. The Intermediary Node Triplet Frame (Floyd-Warshall)
* **Applied to:** APSP, Transitive Closure, Minimum Bottleneck Paths
* **The Strategy:** Initialize the distance matrix from the adjacency structure. Run the K-I-J triple nested loop with K outermost. Update via the intermediary relaxation formula.
* **Code Pattern:**
```python
def floyd_warshall(n, graph):
    dist = [[float('inf')] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        for v, w in graph[i]:
            dist[i][v] = min(dist[i][v], w)

    for k in range(n):          # K MUST be outermost
        for i in range(n):
            for j in range(n):
                if dist[i][k] != float('inf') and dist[k][j] != float('inf'):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return dist
```
