# Binary Lifting

Binary Lifting is a technique to jump through a tree structure in logarithmic $O(\log N)$ time rather than linear $O(N)$ time by precomputing ancestors at powers of 2.

Instead of stepping up one parent at a time (e.g. `u = parent[u]`), we precompute an ancestor table `up[u][i]` which stores the $2^i$-th ancestor of node `u`.

## The Table Recurrence

The size of the table is $N \times \log N$ (where $\log N \approx 20$ for $N \le 10^6$).
*   `up[u][0] = parent[u]` (The $2^0 = 1$st ancestor is just the parent).
*   For $i > 0$:
    `up[u][i] = up[up[u][i-1]][i-1]`

### Why it works
The $2^i$-th ancestor of `u` is the $2^{i-1}$-th ancestor of the $2^{i-1}$-th ancestor of `u`.
By splitting a jump of size $2^i$ into two consecutive jumps of size $2^{i-1}$, we can build the entire table dynamically row by row using a simple DFS traversal.

## Applications
1.  Finding the Lowest Common Ancestor (LCA) in $O(\log N)$ time.
2.  Querying tree values (e.g. max edge on a path) in $O(\log N)$ time.
