class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        
        # If the start or end is blocked, there are 0 paths
        if obstacleGrid[0][0] == 1 or obstacleGrid[m-1][n-1] == 1:
            return 0
            
        # Space-Optimized 1D Array
        dp = [0] * n
        dp[0] = 1 # Base case: 1 way to be at the start
        
        for i in range(m):
            for j in range(n):
                if obstacleGrid[i][j] == 1:
                    dp[j] = 0 # Obstacle blocks all paths passing through here
                elif j > 0:
                    dp[j] += dp[j-1] # Add paths from the left
                    
        return dp[n-1]

if __name__ == "__main__":
    sol = Solution()
    print(sol.uniquePathsWithObstacles([[0,0,0],[0,1,0],[0,0,0]]))  # 2
    print(sol.uniquePathsWithObstacles([[0,1],[0,0]]))              # 1
