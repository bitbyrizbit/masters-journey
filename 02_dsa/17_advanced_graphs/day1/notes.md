## Disjoint Set Union (DSU / Union-Find)

* **Problem Type:** Dynamic Connectivity / Connected Components Maintenance
* **Data Structure Used:** Two integer arrays: `parent[]` and `rank[]`
* **Approach 1:** BFS/DFS repeated per query. For each connectivity query or edge addition, re-run a full DFS to discover all connected components. This takes $O(V + E)$ per operation. If we add $E$ edges one by one and query between each addition, the total cost becomes $O(E \cdot (V + E))$, which is quadratic and completely infeasible for large graphs.
* **Optimized Approach:** DSU with Path Compression and Union by Rank. Maintain a `parent` array where `parent[i]` is the parent of node `i` (root nodes are their own parents). The `find(i)` operation follows parent pointers up to the root. The `union(i, j)` operation connects two components by linking their roots. Two critical optimizations collapse the time per operation to effectively $O(1)$.
* **Complexity:**
  * **Time:** $O(\alpha(N))$ amortized per operation, where $\alpha$ is the Inverse Ackermann function. For all practical inputs ($N < 10^{80}$), $\alpha(N) \le 4$. This is as close to $O(1)$ as any algorithm gets.
  * **Space:** $O(N)$ for the two arrays.
* **Pointer Flow:**
```text
Tracing union-find on nodes 0..4 with edges: (0,1),(2,3),(1,2),(3,4)
Initial: parent = [0,1,2,3,4], rank = [1,1,1,1,1]

union(0, 1): find(0)=0, find(1)=1. Different roots. rank[0]==rank[1], so
             parent[1]=0, rank[0]=2. parent=[0,0,2,3,4], rank=[2,1,1,1,1]

union(2, 3): find(2)=2, find(3)=3. Different roots.
             parent[3]=2, rank[2]=2. parent=[0,0,2,2,4]

union(1, 2): find(1): parent[1]=0. 0 is root. Returns 0.
             find(2): parent[2]=2. Returns 2.
             Root 0 (rank 2) vs Root 2 (rank 2). Equal ranks.
             parent[2]=0, rank[0]=3. parent=[0,0,0,2,4]
             (Now node 3's parent still points to 2, which points to 0 -- path compression
              will fix this on the next find(3) call.)

union(3, 4): find(3): parent[3]=2, parent[2]=0, parent[0]=0. Root is 0.
             PATH COMPRESSION: parent[3] is set to 0. parent=[0,0,0,0,4]
             find(4)=4. Different roots.
             rank[0]=3 > rank[4]=1, so parent[4]=0. parent=[0,0,0,0,0]

Final: All nodes in one component, rooted at 0.
```
* **Pattern Recognition:**
  * Use DSU when:
    - Edges are added dynamically (online queries) and we must answer connectivity queries between each addition.
    - Detecting cycles in an undirected graph (if `union(u, v)` returns False, the edge `(u,v)` creates a cycle).
    - Kruskal's MST algorithm (adding edges in sorted order, checking if they create cycles).
    - Grouping elements into equivalence classes.
* **Core Insight:** Path Compression exploits the idempotent nature of the `find` operation. Every time we traverse the path from a node to the root, we have the perfect opportunity to flatten all those intermediate steps by pointing every node directly to the root. The next query on any of those nodes becomes a single step. Critically, this doesn't change which root each node belongs to — it only optimizes the path to reach that root.

  Union by Rank ensures that when two components merge, the smaller (shallower) tree is always attached under the root of the larger (taller) tree. This prevents the tree from degenerating into a linked list where every `find` is $O(N)$.
* **Mistakes Made:** Calling `find` multiple times without storing the result. Since path compression modifies the parent array, two calls to `find(i)` both return the same root but cause path compression on the first call. The real bug is: when doing `union(i, j)`, forgetting to call `find` first and directly comparing `parent[i] == parent[j]`. This is wrong because `parent[i]` may not be the root.
* **What I Learned:** DSU separates the logical concept (connected component membership) from the physical representation (parent array). Path compression and union by rank are two independent optimizations that combine to give near-constant amortized time, proving that data structure design can collapse exponential-looking problems into constant-time operations.

---

## Problem: Number of Provinces

* **Problem Type:** Connected Component Counting via DSU
* **Data Structure Used:** DSU (parent array + union by rank)
* **Approach 1:** BFS/DFS per unvisited node. Mark all nodes reachable from a starting node. Count how many times we had to start a fresh BFS. Time: $O(N^2)$ (due to adjacency matrix traversal). Space: $O(N)$.
* **Optimized Approach:** DSU. Initialize `ans = n`. For every pair $(i, j)$ where `isConnected[i][j] == 1` and `i < j`, call `union(i, j)`. Every successful union (nodes that were in different components) decrements `ans` by 1. After processing all edges, `ans` holds the number of distinct components.
* **Complexity:**
  * **Time:** $O(N^2 \cdot \alpha(N))$ due to scanning the full adjacency matrix.
  * **Space:** $O(N)$ for the DSU arrays.
* **Pointer Flow:**
```text
isConnected = [[1,1,0],[1,1,0],[0,0,1]] (3 nodes: 0 and 1 are connected, 2 is isolated)
Initial: parent=[0,1,2], rank=[1,1,1], ans=3

i=0, j=1: isConnected[0][1]=1. union(0,1): different roots -> merge. ans=2.
i=0, j=2: isConnected[0][2]=0. Skip.
i=1, j=2: isConnected[1][2]=0. Skip.

ans = 2. Provinces: {0,1} and {2}.
```
* **Core Insight:** Starting with `ans = n` (every node is its own province) and decrementing on each successful merge is an elegant way to count components without explicitly tracking which nodes belong to which component.

---

## Problem: Redundant Connection

* **Problem Type:** Cycle Detection in Undirected Graph via DSU
* **Data Structure Used:** DSU
* **Approach 1:** Build the graph incrementally and after adding each edge, run a DFS to check if a cycle exists. Time: $O(E \cdot (V + E))$.
* **Optimized Approach:** Process edges one by one using DSU. For each edge `(u, v)`: if `find(u) == find(v)`, they are already connected — adding this edge creates a cycle. This is the redundant connection. Return it immediately. Otherwise, call `union(u, v)` to merge the components.
* **Complexity:**
  * **Time:** $O(E \cdot \alpha(V))$ — one DSU operation per edge.
  * **Space:** $O(V)$.
* **Pointer Flow:**
```text
edges = [[1,2],[1,3],[2,3]]
Initial: parent=[0,1,2,3] (1-indexed, node 0 unused), rank=[1,1,1,1]

Edge [1,2]: find(1)=1, find(2)=2. Different. union(1,2). parent=[0,1,1,3]
Edge [1,3]: find(1)=1, find(3)=3. Different. union(1,3). parent=[0,1,1,1]
Edge [2,3]: find(2): parent[2]=1, root=1. find(3): parent[3]=1, root=1.
            Same root! This edge creates a cycle. Return [2,3].
```
* **Core Insight:** In a tree with $V$ vertices, there are exactly $V-1$ edges. Adding one more edge always creates exactly one cycle. The first edge whose endpoints already share a root in the DSU is precisely that cycle-creating edge.

---

### Master Patterns Learned

#### 1. The Canonical DSU Frame (Path Compression + Union by Rank)
* **Applied to:** All union-find problems
* **The Strategy:** Maintain parent and rank arrays. Path-compress every find. Union always attaches smaller-rank tree under larger-rank tree.
* **Code Pattern:**
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [1] * n

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        ri = self.find(i)
        rj = self.find(j)
        if ri == rj:
            return False
        if self.rank[ri] > self.rank[rj]:
            self.parent[rj] = ri
        elif self.rank[ri] < self.rank[rj]:
            self.parent[ri] = rj
        else:
            self.parent[rj] = ri
            self.rank[ri] += 1
        return True
```

#### 2. The Component Count Decrement Frame
* **Applied to:** Number of Provinces, Number of Islands (with DSU), Friend Circles
* **The Strategy:** Initialize ans = total_nodes. Decrement ans on each successful union. Return ans as final component count.
* **Code Pattern:**
```python
def count_components(n, edges):
    parent = list(range(n))
    def find(i):
        if parent[i] != i:
            parent[i] = find(parent[i])
        return parent[i]
    ans = n
    for u, v in edges:
        if find(u) != find(v):
            parent[find(v)] = find(u)
            ans -= 1
    return ans
```
