class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
        m, n = len(grid), len(grid[0])
        
        # We can optimize space by just modifying the first row in place, 
        # but to keep the input immutable, we'll use a 1D array of size n.
        dp = [float('inf')] * n
        dp[0] = grid[0][0]
        
        # Initialize the first row
        for j in range(1, n):
            dp[j] = dp[j-1] + grid[0][j]
            
        # Process remaining rows
        for i in range(1, m):
            # First element of row i only comes from above (dp[0])
            dp[0] += grid[i][0]
            
            for j in range(1, n):
                # Min cost is current cell + min(cost from above, cost from left)
                dp[j] = grid[i][j] + min(dp[j], dp[j-1])
                
        return dp[n-1]

if __name__ == "__main__":
    sol = Solution()
    print(sol.minPathSum([[1,3,1],[1,5,1],[4,2,1]]))  # 7 (1->3->1->1->1)
    print(sol.minPathSum([[1,2,3],[4,5,6]]))          # 12
