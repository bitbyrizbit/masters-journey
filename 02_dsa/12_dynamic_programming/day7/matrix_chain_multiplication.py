class Solution:
    def matrixChainMultiplication(self, arr: list[int]) -> int:
        # Interval DP: Minimizing the cost of multiplying matrices
        # Matrix i has dimensions arr[i-1] x arr[i]
        
        n = len(arr) - 1 # Number of actual matrices
        
        # dp[i][j] represents the min operations to multiply matrices from i to j
        # We need an (n+1) x (n+1) matrix initialized to 0
        dp = [[0] * (n + 1) for _ in range(n + 1)]
        
        # Traverse by interval length 'L' from 2 to n
        for L in range(2, n + 1):
            for i in range(1, n - L + 2):
                j = i + L - 1
                dp[i][j] = float('inf')
                
                # Try all possible split points 'k' between i and j-1
                for k in range(i, j):
                    # Cost = cost of left interval + cost of right interval + cost to multiply them
                    # Left interval: i to k
                    # Right interval: k+1 to j
                    # Multiplying them takes: arr[i-1] * arr[k] * arr[j] operations
                    cost = dp[i][k] + dp[k+1][j] + (arr[i-1] * arr[k] * arr[j])
                    dp[i][j] = min(dp[i][j], cost)
                    
        return dp[1][n]

if __name__ == "__main__":
    sol = Solution()
    print(sol.matrixChainMultiplication([40, 20, 30, 10, 30]))  # 26000
    print(sol.matrixChainMultiplication([10, 20, 30, 40, 30]))  # 30000
