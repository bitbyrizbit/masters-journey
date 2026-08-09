## Binary Lifting & Lowest Common Ancestor (LCA)

* **Problem Type:** Tree Queries / Ancestor Jump Optimization
* **Data Structure Used:** 2D DP array (`up[u][i]`) and `depth[]` array
* **Approach 1:** Naive LCA. Given nodes $u$ and $v$, first equalize their depths by moving the deeper node up one step at a time. Then, move both nodes up simultaneously one step at a time until they meet. The node they meet at is the LCA. Time: $O(N)$ per query in a skewed tree (linked list). This is too slow for $Q$ queries ($O(Q \cdot N)$).
* **Optimized Approach:** Binary Lifting. Precompute an `up` table where `up[u][i]` stores the $2^i$-th ancestor of node $u$. This takes $O(N \log N)$ time.
  To answer an LCA query:
  1. **Phase 1 (Depth Equalization):** Find the depth difference $k$. Represent $k$ in binary, and jump the deeper node up by $2^i$ for every set bit in $k$. Now both nodes are at the same depth.
  2. **Phase 2 (Synchronized Climbing):** If $u == v$, return $u$. Otherwise, iterate $i$ from the highest bit $\lfloor \log_2 N \rfloor$ down to 0. If `up[u][i] != up[v][i]`, it means the $2^i$-th ancestors are *different*, so the LCA must be strictly higher. We safely jump both nodes: `u = up[u][i]`, `v = up[v][i]`. After this loop, $u$ and $v$ are guaranteed to be exactly one step below the LCA, so we return `up[u][0]`. Time: $O(\log N)$ per query.
* **Complexity:**
  * **Time:** $O(N \log N)$ for precomputation, $O(\log N)$ per LCA query.
  * **Space:** $O(N \log N)$ for the `up` table.
* **Pointer Flow:**
```text
Tree: root=0. Edges: 0-1, 1-3, 3-6. 0-2, 2-4. 2-5.
Depths: 0:0, 1:1, 2:1, 3:2, 4:2, 5:2, 6:3

up table for 3 levels (i=0, 1, 2 representing 1st, 2nd, 4th ancestor):
Node | i=0 (parent) | i=1 (2nd anc) | i=2 (4th anc)
  0  |      0       |       0       |      0
  1  |      0       |       0       |      0
  2  |      0       |       0       |      0
  3  |      1       |       0       |      0
  4  |      2       |       0       |      0
  5  |      2       |       0       |      0
  6  |      3       |       1       |      0

Query LCA(6, 4):
Phase 1: depth[6]=3, depth[4]=2. Diff = 1 = 2^0.
Jump deeper node (6) by 2^0: u = up[6][0] = 3.
Now u=3, v=4. Depths are equal (2).

Phase 2: Iterate i from 2 down to 0:
i=2: up[3][2]=0, up[4][2]=0. They match! Do NOT jump. (LCA is 0 or below 0).
i=1: up[3][1]=0, up[4][1]=0. They match! Do NOT jump.
i=0: up[3][0]=1, up[4][0]=2. Different! Jump: u=1, v=2.

Loop ends. LCA is up[u][0] = up[1][0] = 0.
Return 0. Correct!
```
* **Pattern Recognition:**
  * Use Binary Lifting when:
    - You need to query the LCA of many pairs in a static tree.
    - You need to jump exactly $K$ steps up a tree or functional graph efficiently.
    - You need to find the maximum/minimum edge weight on the path between $u$ and $v$ in a tree (store `max_edge[u][i]` alongside `up[u][i]`).
* **Core Insight:** Binary lifting exploits the fact that any integer $k$ can be uniquely represented as a sum of powers of 2 (binary representation). This means a jump of distance $k$ can be decomposed into at most $\log_2(k)$ jumps of power-of-2 distances.

  The construction recurrence `up[u][i] = up[ up[u][i-1] ][i-1]` is elegant: to jump $2^i$ steps, we first jump $2^{i-1}$ steps, and from that intermediate node, we jump another $2^{i-1}$ steps. $2^{i-1} + 2^{i-1} = 2^i$.

  In Phase 2 of the LCA query, we iterate from the highest bit to the lowest. This is a greedy approach. If `up[u][i] == up[v][i]`, the ancestors match. They might be the LCA, or they might be an ancestor *above* the LCA. Since we can't be sure, we do *not* jump. If `up[u][i] != up[v][i]`, the ancestors are different, which guarantees the LCA is strictly above them. Thus it is safe to jump. By processing from large jumps to small jumps, we push $u$ and $v$ as high as possible without them meeting. They stop exactly one step below the true LCA.
* **Mistakes Made:** In Phase 2, accidentally returning `up[u][i]` when they match. They might match at the root, but the actual LCA might be lower! We must only jump when they are *different*. Another mistake is starting the `up` table out of bounds; missing ancestors should point to a safe dummy node (like the root itself or -1).
* **What I Learned:** Any sequence of associative operations (like pointer chasing up a tree) can be accelerated using power-of-2 doubling. Binary lifting is the tree equivalent of Matrix Exponentiation for sequences.

---

### Master Patterns Learned

#### 1. The Binary Lifting / LCA Frame
* **Applied to:** Kth Ancestor Queries, LCA Queries, Path Aggregates in Trees
* **The Strategy:** Precompute `depth` and `up` table via a single DFS. Answer queries by depth equalization followed by synchronized bit-by-bit greedy jumping.
* **Code Pattern:**
```python
class TreeAncestor:
    def __init__(self, n, edges, root=0):
        self.LOG = 20  # ceil(log2(n)) + 1
        self.depth = [0] * n
        self.up = [[0] * self.LOG for _ in range(n)]
        
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
            
        def dfs(u, p, d):
            self.depth[u] = d
            self.up[u][0] = p if p != -1 else u
            for i in range(1, self.LOG):
                self.up[u][i] = self.up[ self.up[u][i-1] ][i-1]
                
            for v in adj[u]:
                if v != p:
                    dfs(v, u, d + 1)
                    
        dfs(root, -1, 0)

    def get_lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
            
        # Phase 1: Equalize depths
        diff = self.depth[u] - self.depth[v]
        for i in range(self.LOG):
            if (diff >> i) & 1:
                u = self.up[u][i]
                
        if u == v:
            return u
            
        # Phase 2: Synchronized climbing
        for i in range(self.LOG - 1, -1, -1):
            if self.up[u][i] != self.up[v][i]:
                u = self.up[u][i]
                v = self.up[v][i]
                
        # Return the parent of the stopping point
        return self.up[u][0]
```
