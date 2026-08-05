# Introduction to Bitmask Dynamic Programming

When a DP problem involves a state like "which items have been visited?" or "which tasks have been completed?", managing that state using arrays or sets is incredibly slow and difficult to memoize.

**Bitmask DP** uses an integer to represent the visited state, utilizing bitwise operations to update and check the state instantly.
This is heavily used in problems where $N$ is very small ($N \le 20$), such as the Traveling Salesperson Problem (TSP) or job assignment problems.

## Core Operations

1.  **Initialize the mask:** `mask = 0` (No items visited).
2.  **Check if item $i$ is visited:** `if mask & (1 << i):`
3.  **Mark item $i$ as visited:** `new_mask = mask | (1 << i)`
4.  **Mark item $i$ as unvisited:** `new_mask = mask & ~(1 << i)`
5.  **Check if ALL $N$ items are visited:** `if mask == (1 << n) - 1:` (This checks if all $N$ bits are 1).

## The Classic TSP State

In the Traveling Salesperson Problem, we need to visit all cities with minimum cost.
The DP state must track two things:
1.  **Where are we right now?** (Current city `u`).
2.  **Where have we been?** (Bitmask `visited`).

```python
def solve_tsp(n, dist):
    # Memoization table: dp[u][mask]
    memo = {}
    
    def dp(u, mask):
        # Base Case: All cities visited
        if mask == (1 << n) - 1:
            return dist[u][0] # Return to start (or 0 if path doesn't loop)
            
        if (u, mask) in memo:
            return memo[(u, mask)]
            
        ans = float('inf')
        for v in range(n):
            # If city v is NOT visited
            if not (mask & (1 << v)):
                # Visit it! OR the bit into the mask.
                cost = dist[u][v] + dp(v, mask | (1 << v))
                ans = min(ans, cost)
                
        memo[(u, mask)] = ans
        return ans
        
    # Start at city 0, with only the 0-th bit set
    return dp(0, 1 << 0)
```

The bitmask perfectly encapsulates the complex combination of visited cities into a single integer, dropping the state space from $O(N!)$ to a highly efficient $O(N \cdot 2^N)$.
