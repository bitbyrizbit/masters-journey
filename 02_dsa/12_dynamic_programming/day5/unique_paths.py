class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        # Space-Optimized 1D Counting Grid DP
        # We only need the current row and previous row (or just one row overwritten)
        dp = [1] * n
        
        # Start from row 1 since row 0 is all 1s (only one way to move right on the top edge)
        for i in range(1, m):
            for j in range(1, n):
                # Number of ways to reach (i, j) is the sum of ways from top (i-1, j) and left (i, j-1)
                # dp[j] currently holds the value from the top (i-1, j)
                # dp[j-1] holds the value from the left (i, j-1)
                dp[j] += dp[j-1]
                
        return dp[n-1]

if __name__ == "__main__":
    sol = Solution()
    print(sol.uniquePaths(3, 7))  # 28
    print(sol.uniquePaths(3, 2))  # 3
