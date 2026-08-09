## Bridges and Articulation Points

* **Problem Type:** Network Vulnerability / Critical Edge & Vertex Detection
* **Data Structure Used:** DFS tracking arrays (`dfn`, `low`)
* **Approach 1:** Brute force. To find all bridges, iterate over every edge $e$. Temporarily remove $e$. Run a BFS/DFS to check if the number of connected components has increased. Restore $e$. For articulation points, do the same by removing each vertex $v$ and its incident edges. Time: $O(E \cdot (V + E))$ for bridges, $O(V \cdot (V + E))$ for articulation points. Too slow for large graphs.
* **Optimized Approach:** Tarjan's bridge-finding algorithm. Run a single DFS. Maintain `dfn[u]` (discovery time) and `low[u]` (lowest discovery time reachable from $u$ or its descendants via exactly one back-edge). 
  - **Bridge condition:** For a tree edge $u \to v$, if `low[v] > dfn[u]`, then the edge $(u, v)$ is a bridge.
  - **Articulation Point condition:** For a non-root vertex $u$ with tree child $v$, if `low[v] >= dfn[u]`, then $u$ is an articulation point. If $u$ is the DFS root, it is an articulation point if and only if it has $\ge 2$ independent DFS children.
* **Complexity:**
  * **Time:** $O(V + E)$ — a single DFS pass.
  * **Space:** $O(V + E)$ for the recursion stack and tracking arrays.
* **Pointer Flow:**
```text
Graph (Butterfly): 0-1, 1-2, 2-0, 2-3, 3-4, 4-2
dfn=[-1]*5, low=[-1]*5, timer=0

dfs(0, parent=-1): dfn[0]=low[0]=0.
  dfs(1, parent=0): dfn[1]=low[1]=1.
    dfs(2, parent=1): dfn[2]=low[2]=2.
      -> edge 2-0: 0 is visited and 0 != parent(1). Back-edge!
         low[2] = min(low[2], dfn[0]) = min(2, 0) = 0.
      dfs(3, parent=2): dfn[3]=low[3]=3.
        dfs(4, parent=3): dfn[4]=low[4]=4.
          -> edge 4-2: 2 is visited and 2 != parent(3). Back-edge!
             low[4] = min(low[4], dfn[2]) = min(4, 2) = 2.
        return to 3: low[3] = min(low[3], low[4]) = min(3, 2) = 2.
        check bridge: low[4] > dfn[3]? (2 > 3) False. 3-4 is not a bridge.
        check AP: low[4] >= dfn[3]? (2 >= 3) False.
      return to 2: low[2] = min(low[2], low[3]) = min(0, 2) = 0.
      check bridge: low[3] > dfn[2]? (2 > 2) False. 2-3 is not a bridge.
      check AP: low[3] >= dfn[2]? (2 >= 2) True! Node 2 is an Articulation Point.
    return to 1: low[1] = min(low[1], low[2]) = min(1, 0) = 0.
    check bridge: low[2] > dfn[1]? (0 > 1) False. 1-2 is not a bridge.
    check AP: low[2] >= dfn[1]? (0 >= 1) False.
  return to 0: low[0] = min(low[0], low[1]) = min(0, 0) = 0.
  check bridge: low[1] > dfn[0]? (0 > 0) False. 0-1 is not a bridge.
  check AP: node 0 is root. Has only 1 DFS child (node 1). Not an AP.

Final APs: {2}. Bridges: None.
```
* **Pattern Recognition:**
  * Use this pattern when:
    - Identifying "critical connections" or "single points of failure" in a network.
    - Solving problems involving separating a graph into biconnected components.
* **Core Insight:** The DFS tree imposes a strict hierarchical structure on the graph. An edge from $u \to v$ in the DFS tree is the *only* way for $u$ to reach $v$'s subtree. 

  If a back-edge exists from $v$'s subtree to $u$ or any of $u$'s ancestors, it provides an alternate route. The `low[v]` value captures the highest ancestor (lowest `dfn`) reachable via a back-edge from $v$'s subtree.
  
  - **Bridge (`low[v] > dfn[u]`):** If `low[v] > dfn[u]`, it means the highest ancestor $v$'s subtree can reach is strictly *below* $u$. Thus, there is no back-edge bypassing $u \to v$. Removing $u \to v$ perfectly disconnects $v$'s subtree.
  
  - **Articulation Point (`low[v] >= dfn[u]`):** If `low[v] >= dfn[u]`, it means $v$'s subtree can reach *at highest* $u$ itself, but not strictly above $u$. If we remove vertex $u$, $v$'s subtree loses its connection to everything above $u$. Thus, $u$ is an articulation point. (Notice the strict inequality `>` for bridges, but $\ge$ for APs).

  **The Multi-Edge Problem:** In undirected graphs, the edge $u-v$ appears in both $u$'s and $v$'s adjacency lists. During `dfs(u)`, we must ignore the edge leading immediately back to the parent $v$ to avoid falsely interpreting it as a back-edge. However, if there are *multiple distinct edges* between $u$ and $v$ (a multigraph), ignoring by vertex `if neighbor == parent` will wrongly ignore parallel edges. To safely handle multigraphs, track the **edge index** passed from the parent and ignore `if edge_index == parent_edge_index`.
* **Mistakes Made:** Using `low[u] = min(low[u], low[neighbor])` when processing a back-edge. It must be `low[u] = min(low[u], dfn[neighbor])`. Using `low[neighbor]` allows a node to "borrow" the low value of an ancestor, falsely making it seem like a node can reach higher than it actually can via exactly one back-edge.
* **What I Learned:** The DFS tree combined with back-edges elegantly classifies the connectivity of undirected graphs. The distinction between `>` for bridges and $\ge$ for articulation points perfectly captures the difference between removing an edge vs removing a vertex.

---

### Master Patterns Learned

#### 1. The Bridge-Finding Frame (Critical Connections)
* **Applied to:** Critical Connections in a Network (LeetCode 1192)
* **The Strategy:** Maintain `dfn` and `low`. For each unvisited neighbor, DFS and update `low[u] = min(low[u], low[v])`. If `low[v] > dfn[u]`, the edge is a bridge. For a visited neighbor (back-edge), update `low[u] = min(low[u], dfn[v])` (ignoring the parent).
* **Code Pattern:**
```python
def find_bridges(n, adj):
    dfn = [-1] * n
    low = [-1] * n
    timer = 0
    bridges = []

    def dfs(u, p=-1):
        nonlocal timer
        dfn[u] = low[u] = timer
        timer += 1

        for v in adj[u]:
            if v == p:
                continue
            if dfn[v] != -1:
                # Back-edge
                low[u] = min(low[u], dfn[v])
            else:
                # Tree-edge
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > dfn[u]:
                    bridges.append([u, v])

    for i in range(n):
        if dfn[i] == -1:
            dfs(i)
    return bridges
```

#### 2. The Articulation Point Frame
* **Applied to:** Single Points of Failure, AP identification
* **The Strategy:** Similar to bridges, but check `low[v] >= dfn[u]`. Also, explicitly track the number of DFS children for the root node.
* **Code Pattern:**
```python
def find_articulation_points(n, adj):
    dfn = [-1] * n
    low = [-1] * n
    timer = 0
    is_ap = [False] * n

    def dfs(u, p=-1):
        nonlocal timer
        dfn[u] = low[u] = timer
        timer += 1
        children = 0

        for v in adj[u]:
            if v == p:
                continue
            if dfn[v] != -1:
                low[u] = min(low[u], dfn[v])
            else:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if p != -1 and low[v] >= dfn[u]:
                    is_ap[u] = True
        
        # Root condition
        if p == -1 and children > 1:
            is_ap[u] = True

    for i in range(n):
        if dfn[i] == -1:
            dfs(i)
            
    return [i for i in range(n) if is_ap[i]]
```
