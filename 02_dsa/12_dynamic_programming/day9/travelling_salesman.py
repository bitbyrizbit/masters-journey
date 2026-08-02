class Solution:
    def tsp(self, graph: list[list[int]]) -> int:
        # Travelling Salesman Problem (Conceptual Implementation)
        # Bitmask DP: Finding the minimum cost to visit all nodes exactly once and return to origin
        
        n = len(graph)
        # dp[mask][i] = min distance to visit all cities in 'mask', currently ending at city 'i'
        
        # We start at city 0. The mask 1 (binary 00..01) means city 0 is visited.
        # We initialize all states to infinity.
        dp = [[float('inf')] * n for _ in range(1 << n)]
        dp[1][0] = 0 
        
        # Iterate over all possible combinations of visited cities (masks)
        for mask in range(1, 1 << n):
            for i in range(n):
                # If city 'i' is actually in the current mask
                if mask & (1 << i):
                    
                    # Try to transition FROM city 'i' TO an unvisited city 'j'
                    for j in range(n):
                        # If city 'j' is NOT in the current mask
                        if not (mask & (1 << j)):
                            next_mask = mask | (1 << j)
                            # The cost to reach state (next_mask, ending at j) is the cost to reach 
                            # the current state PLUS the distance from i to j
                            dp[next_mask][j] = min(dp[next_mask][j], dp[mask][i] + graph[i][j])
                            
        # We have visited all cities. The final step is returning from the last city back to origin (city 0).
        # The mask for all cities visited is (1 << n) - 1.
        all_visited_mask = (1 << n) - 1
        min_tour_cost = float('inf')
        
        for last_city in range(1, n):
            min_tour_cost = min(min_tour_cost, dp[all_visited_mask][last_city] + graph[last_city][0])
            
        return int(min_tour_cost)

if __name__ == "__main__":
    sol = Solution()
    # Adjacency matrix representing distances between 4 cities
    graph = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    print(sol.tsp(graph)) # 80 (Path: 0 -> 1 -> 3 -> 2 -> 0)
