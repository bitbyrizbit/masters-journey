## Strongly Connected Components (SCC)

* **Problem Type:** Directed Graph Connectivity / DFS Tree Analysis
* **Data Structure Used:** Adjacency list (forward and transpose graphs) or DFS tracking arrays (`dfn`, `low`, `stack`, `in_stack`)
* **Approach 1:** Brute force. For every pair of vertices $(u, v)$, run a BFS/DFS to check if $u$ can reach $v$ and $v$ can reach $u$. This takes $O(V \cdot (V + E))$, which is far too slow for large graphs.
* **Optimized Approach 1 (Kosaraju's Algorithm):** Two-pass DFS. First pass: DFS on the original graph, pushing each node to a stack when its DFS finishes (building a topological order of the condensation DAG). Second pass: DFS on the transposed graph (edges reversed), popping nodes from the stack to use as roots. Each full DFS from a root in the second pass discovers exactly one SCC. Time: $O(V + E)$, Space: $O(V + E)$.
* **Optimized Approach 2 (Tarjan's Algorithm):** Single-pass DFS. Maintain `dfn[u]` (discovery time) and `low[u]` (lowest discovery time reachable from $u$'s subtree via a back/cross edge). Also maintain a stack of currently visited nodes. If after exploring all children of $u$, `dfn[u] == low[u]`, then $u$ is the "root" of an SCC. Pop from the stack until $u$ is popped to extract the SCC.
* **Complexity:**
  * **Time:** $O(V + E)$ for either Tarjan's or Kosaraju's. Every edge and vertex is processed a constant number of times.
  * **Space:** $O(V + E)$ for adjacency lists and recursion stacks.
* **Pointer Flow:**
```text
Tarjan's trace on graph: 5 nodes, edges 0->1, 1->2, 2->0, 2->3, 3->4, 4->3
dfn=[-1]*5, low=[-1]*5, stack=[], in_stack=[F]*5, timer=0

dfs(0): dfn[0]=low[0]=0. stack=[0]. in_stack[0]=T.
  dfs(1): dfn[1]=low[1]=1. stack=[0,1]. in_stack[1]=T.
    dfs(2): dfn[2]=low[2]=2. stack=[0,1,2]. in_stack[2]=T.
      -> edge 2->0: 0 is in_stack! Back-edge found. low[2] = min(low[2], dfn[0]) = 0.
      dfs(3): dfn[3]=low[3]=3. stack=[0,1,2,3]. in_stack[3]=T.
        dfs(4): dfn[4]=low[4]=4. stack=[0,1,2,3,4]. in_stack[4]=T.
          -> edge 4->3: 3 is in_stack! Back-edge found. low[4] = min(low[4], dfn[3]) = 3.
        return to 3: low[3] = min(low[3], low[4]) = 3.
        node 3 children done. dfn[3]==low[3] (3==3). SCC root!
        pop stack: pop 4, pop 3. SCC: {4, 3}. in_stack[4]=F, in_stack[3]=F.
      return to 2: low[2] = min(low[2], low[3]) = 0.
    return to 1: low[1] = min(low[1], low[2]) = 0.
  return to 0: low[0] = min(low[0], low[1]) = 0.
  node 0 children done. dfn[0]==low[0] (0==0). SCC root!
  pop stack: pop 2, pop 1, pop 0. SCC: {2, 1, 0}.
```
* **Pattern Recognition:**
  * Use SCC algorithms when:
    - You need to group nodes in a directed graph where every node can reach every other node in the group.
    - Condensing a cyclic directed graph into a Directed Acyclic Graph (DAG) for DP.
    - Solving 2-SAT problems.
* **Core Insight:** In Kosaraju's algorithm, the key insight is that reversing the edges of a graph perfectly preserves its SCCs, but reverses the topological relationships between SCCs. By finishing the deepest nodes first (Phase 1), the nodes at the top of the stack are guaranteed to belong to "source" SCCs in the original graph, which means they belong to "sink" SCCs in the reversed graph. A DFS on the reversed graph starting from these nodes cannot escape the SCC, perfectly extracting it.

  In Tarjan's algorithm, `dfn` marks when we first see a node, and `low` tracks how far "up" the DFS tree we can reach from this node's subtree. A node $u$ with `dfn[u] == low[u]` means its subtree has no back-edges reaching strictly higher than $u$ itself. Thus, $u$ is the entry point (root) of an SCC, and everything currently on the stack above $u$ belongs to that SCC.
* **Mistakes Made:** In Tarjan's, updating `low[u] = min(low[u], low[v])` when processing a back-edge to an already visited node $v$ is incorrect. It must be `low[u] = min(low[u], dfn[v])`. While this distinction rarely breaks basic SCC extraction, it strictly defines `low` correctly and is essential when extending these ideas to bridges and articulation points. In Kosaraju's, forgetting to reverse the graph in Phase 2 is a common implementation error.
* **What I Learned:** SCC algorithms beautifully exploit the properties of DFS trees. Kosaraju leverages the post-order sequence, while Tarjan leverages cross/back-edge classification. Both achieve optimal linear time by extracting deep structural information during the graph traversal.

---

### Master Patterns Learned

#### 1. The Tarjan's Single-Pass SCC Frame
* **Applied to:** Extracting SCCs, 2-SAT, DAG Condensation
* **The Strategy:** Maintain `dfn`, `low`, and a stack. Update `low` via DFS tree edges and back-edges to nodes currently on the stack. Extract SCC when `dfn == low`.
* **Code Pattern:**
```python
def tarjan_scc(n, adj):
    dfn = [-1] * n
    low = [-1] * n
    in_stack = [False] * n
    stack = []
    timer = 0
    sccs = []

    def dfs(u):
        nonlocal timer
        dfn[u] = low[u] = timer
        timer += 1
        stack.append(u)
        in_stack[u] = True

        for v in adj[u]:
            if dfn[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif in_stack[v]:
                low[u] = min(low[u], dfn[v])

        if dfn[u] == low[u]:
            scc = []
            while True:
                v = stack.pop()
                in_stack[v] = False
                scc.append(v)
                if u == v:
                    break
            sccs.append(scc)

    for i in range(n):
        if dfn[i] == -1:
            dfs(i)
    return sccs
```

#### 2. Kosaraju's Two-Pass SCC Frame
* **Applied to:** Extracting SCCs (often simpler to implement than Tarjan's)
* **The Strategy:** Phase 1 DFS (post-order to stack). Phase 2 DFS on transposed graph popping from stack.
* **Code Pattern:**
```python
def kosaraju_scc(n, adj):
    rev_adj = [[] for _ in range(n)]
    for u in range(n):
        for v in adj[u]:
            rev_adj[v].append(u)

    visited = [False] * n
    stack = []

    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        stack.append(u)

    def dfs2(u, scc):
        visited[u] = True
        scc.append(u)
        for v in rev_adj[u]:
            if not visited[v]:
                dfs2(v, scc)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    visited = [False] * n
    sccs = []
    while stack:
        u = stack.pop()
        if not visited[u]:
            scc = []
            dfs2(u, scc)
            sccs.append(scc)
            
    return sccs
```
