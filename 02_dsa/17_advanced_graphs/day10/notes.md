## Tree DP

* **Problem Type:** Dynamic Programming on Tree Structures
* **Data Structure Used:** 1D or 2D DP array indexed by node ID, computed via Post-Order DFS.
* **Approach 1:** Flatten the tree into an array and try to run standard DP. This usually fails because arrays imply a strict linear sequence, whereas trees have branching structural dependencies that are lost when flattened.
* **Optimized Approach:** DP embedded directly within a Post-Order DFS. In a tree, a node's state depends entirely on the states of its children. Therefore, we must completely evaluate all children of $u$ before we can evaluate $u$. A post-order DFS natively enforces this guarantee: the recursive calls for the children return *before* the parent processes its own logic.
* **Complexity:**
  * **Time:** $O(V)$ in most cases, as we visit each node and its children exactly once.
  * **Space:** $O(V)$ for the recursion stack and DP state arrays.
* **Pointer Flow:**
```text
Maximum Independent Set (MIS) on a Tree:
Tree: root 0(w=1). Children: 1(w=3), 2(w=2). Child of 1: 3(w=4).
State: dp[u][0] = max weight in subtree u if u is NOT included.
       dp[u][1] = max weight in subtree u if u IS included.

dfs(0):
  dfs(1):
    dfs(3): leaf node!
      dp[3][0] = 0
      dp[3][1] = 4
      return
    back at 1: all children of 1 (node 3) are done.
    dp[1][0] = sum(max(dp[v][0], dp[v][1])) = max(dp[3][0], dp[3][1]) = 4
    dp[1][1] = weight[1] + sum(dp[v][0]) = 3 + dp[3][0] = 3 + 0 = 3
    return
  dfs(2): leaf node!
    dp[2][0] = 0
    dp[2][1] = 2
    return
  back at 0: all children of 0 (1, 2) are done.
  dp[0][0] = max(dp[1][0], dp[1][1]) + max(dp[2][0], dp[2][1])
           = max(4, 3) + max(0, 2) = 4 + 2 = 6
  dp[0][1] = weight[0] + dp[1][0] + dp[2][0]
           = 1 + 4 + 0 = 5
           
Final Answer: max(dp[0][0], dp[0][1]) = max(6, 5) = 6.
Optimal set: {node 3, node 2}. Weights: 4 + 2 = 6. Correct!
```
* **Pattern Recognition:**
  * Use Tree DP when:
    - The problem asks for an optimal value (max, min, count) on a tree graph.
    - Decisions at a node (e.g., coloring, including in a set) affect only its immediate parent and children.
    - You need to find the longest path (Diameter) or sum of distances in a tree.
* **Core Insight:** The core principle of Tree DP is **Post-Order State Aggregation**. There is no "for $i = 1$ to $N$" loop because the ordering isn't linear. Instead, the DFS acts as the loop. 

  **MIS Derivation:** 
  If node $u$ is included, none of its children can be included (to maintain independence). Thus: $dp[u][1] = w[u] + \sum dp[v][0]$.
  If node $u$ is not included, each child $v$ is free to be included or not independently. We should greedily take the best option for each child. Thus: $dp[u][0] = \sum \max(dp[v][0], dp[v][1])$.

  **Tree Diameter Strategy:**
  Sometimes, the answer we want isn't a state that strictly flows upward. For the tree diameter, the longest path in the entire tree might look like an inverted 'V' passing through some highest node $u$. We define the state `dp[u]` strictly as the "longest path going straight down into $u$'s subtree". 
  While evaluating children of $u$, we can compute the longest 'V' path passing through $u$ as `dp[u] + dp[v] + 1` (combining the best downward path found *so far* with the current child's downward path). We update a global `ans` with this 'V' path. Then, we update `dp[u] = max(dp[u], dp[v] + 1)`. The order here is critical: updating the global answer *before* updating `dp[u]` ensures we don't accidentally combine a child's path with itself.
* **Mistakes Made:** Updating `dp[u]` before computing the global answer in the Tree Diameter problem, which effectively double-counts the longest child branch as both the left and right sides of the 'V' path. Another common error is using a `visited` array instead of just checking `if neighbor == parent` to prevent going backwards. In trees, `visited` is unnecessary overhead since there are no cycles; a simple parent check perfectly enforces downward traversal.
* **What I Learned:** Tree DP forces a shift in thinking from linear sequence processing to hierarchical aggregation. By separating the "state passed upward" (e.g., straight downward path) from the "global optimal configuration" (e.g., inverted 'V' path), we can solve complex structural problems in a single DFS pass.

---

### Master Patterns Learned

#### 1. The Post-Order MIS Frame (Include/Exclude DP)
* **Applied to:** Maximum Independent Set, House Robber III, Vertex Cover on Trees
* **The Strategy:** Define a 2D state array (or return a tuple from DFS). Process all children recursively. Use the children's 0/1 states to compute the parent's 0/1 states.
* **Code Pattern:**
```python
def max_independent_set(n, adj, weights):
    # dp[u][0]: exclude u, dp[u][1]: include u
    dp = [[0, 0] for _ in range(n)]
    
    def dfs(u, p=-1):
        dp[u][1] = weights[u]
        
        for v in adj[u]:
            if v != p:
                dfs(v, u)
                dp[u][0] += max(dp[v][0], dp[v][1])
                dp[u][1] += dp[v][0]
                
    dfs(0)
    return max(dp[0][0], dp[0][1])
```

#### 2. The Global Answer V-Path Frame (Tree Diameter)
* **Applied to:** Tree Diameter, Longest Univalue Path, Maximum Path Sum
* **The Strategy:** `dfs(u)` returns the best straight path down. During the child loop, combine the current best down-path with the child's down-path to update a global max. Then update the best down-path.
* **Code Pattern:**
```python
def tree_diameter(n, adj):
    ans = 0
    
    def dfs(u, p=-1):
        nonlocal ans
        best_down = 0
        
        for v in adj[u]:
            if v != p:
                child_down = dfs(v, u)
                # The 'V' path passing through u
                ans = max(ans, best_down + child_down + 1)
                # The straight down path from u
                best_down = max(best_down, child_down + 1)
                
        return best_down
        
    dfs(0)
    return ans
```
