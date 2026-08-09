# Tree Dynamic Programming

Tree DP is the application of Dynamic Programming to tree structures. Unlike standard grid DP where we transition from left/top to right/bottom, Tree DP propagates values from child subtrees up to their parent nodes, usually via Post-Order DFS.

The base cases are the leaf nodes of the tree.

## The Classic State

For a node $U$ in the tree:
We compute a state representing the optimal solution for the subtree rooted at $U$.

### Example: Maximum Independent Set (MIS) on Trees
Select a subset of vertices such that no two selected vertices are adjacent, maximizing the total weight of selected vertices.

For each node $U$, we define two states:
1.  `dp[u][1]`: The maximum weight of the subtree rooted at $U$ if we **include** node $U$.
2.  `dp[u][0]`: The maximum weight of the subtree rooted at $U$ if we **exclude** node $U$.

The transitions are:
*   If we **include** $U$, we must **exclude** all its children $V$:
    `dp[u][1] = weight[u] + sum(dp[v][0])`
*   If we **exclude** $U$, we can either **include or exclude** each child $V$:
    `dp[u][0] = sum(max(dp[v][0], dp[v][1]))`

This propagates values from leaf nodes up to the root in $O(N)$ time.
