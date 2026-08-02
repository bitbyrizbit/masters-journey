class Solution:
    def maxCoins(self, nums: list[int]) -> int:
        # Interval DP
        # Concept: Think about the LAST balloon to burst, not the first.
        # This isolates the subproblems cleanly.
        
        # Pad with 1s to handle boundary balloon bursts natively
        A = [1] + nums + [1]
        n = len(A)
        
        # dp[i][j] = max coins from bursting balloons STRICTLY BETWEEN i and j (exclusive).
        dp = [[0] * n for _ in range(n)]
        
        # L is the interval length
        for L in range(2, n):
            for i in range(n - L):
                j = i + L
                
                # k is the index of the balloon chosen to be burst LAST within (i, j)
                for k in range(i + 1, j):
                    # If k is burst last, its adjacent balloons are i and j (because everything between them is already burst)
                    coins = A[i] * A[k] * A[j]
                    total = coins + dp[i][k] + dp[k][j]
                    dp[i][j] = max(dp[i][j], total)
                    
        return dp[0][n-1]

if __name__ == "__main__":
    sol = Solution()
    print(sol.maxCoins([3,1,5,8]))  # 167
    print(sol.maxCoins([1,5]))      # 10
