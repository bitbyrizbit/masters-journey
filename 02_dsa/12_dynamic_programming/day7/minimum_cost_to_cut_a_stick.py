class Solution:
    def minCost(self, n: int, cuts: list[int]) -> int:
        # Interval Split DP
        
        # Sort cuts and add boundaries 0 and n to treat the stick ends identically to cuts
        cuts.sort()
        cuts = [0] + cuts + [n]
        m = len(cuts)
        
        # dp[i][j] = min cost to execute all cuts strictly between index i and index j of the cuts array
        dp = [[0] * m for _ in range(m)]
        
        # L is the interval length in the cuts array (number of cuts in the subproblem)
        for L in range(2, m):
            for i in range(m - L):
                j = i + L
                dp[i][j] = float('inf')
                
                # k is the index of the cut chosen to be executed FIRST within (i, j)
                for k in range(i + 1, j):
                    # Cost = cost of left sub-stick + cost of right sub-stick + length of current stick
                    # Length of current stick is cuts[j] - cuts[i]
                    current_cost = dp[i][k] + dp[k][j] + (cuts[j] - cuts[i])
                    dp[i][j] = min(dp[i][j], current_cost)
                    
        return dp[0][m-1]

if __name__ == "__main__":
    sol = Solution()
    print(sol.minCost(7, [1,3,4,5]))  # 16
    print(sol.minCost(9, [5,6,1,4,2])) # 22
