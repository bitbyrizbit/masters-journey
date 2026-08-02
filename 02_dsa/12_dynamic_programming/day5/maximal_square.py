class Solution:
    def maximalSquare(self, matrix: list[list[str]]) -> int:
        if not matrix or not matrix[0]:
            return 0
            
        m, n = len(matrix), len(matrix[0])
        
        # 1D Space Optimized Neighbour-based Grid DP
        dp = [0] * (n + 1)
        max_side = 0
        prev = 0 # Stores dp[i-1][j-1] (top-left diagonal neighbor)
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                temp = dp[j] # Save current dp[j] (which acts as top neighbor for next step) before overriding
                
                if matrix[i-1][j-1] == '1':
                    # dp[j] is top, dp[j-1] is left, prev is top-left
                    dp[j] = min(dp[j-1], dp[j], prev) + 1
                    max_side = max(max_side, dp[j])
                else:
                    dp[j] = 0
                    
                prev = temp # Update prev for the next column to be the old top value
                
        return max_side * max_side

if __name__ == "__main__":
    sol = Solution()
    matrix = [["1","0","1","0","0"],
              ["1","0","1","1","1"],
              ["1","1","1","1","1"],
              ["1","0","0","1","0"]]
    print(sol.maximalSquare(matrix))  # 4
