class Solution:
    def integerBreak(self, n: int) -> int:
        # Mathematics / Bottom-up 1D DP
        
        # dp[i] = max product obtained by breaking integer 'i' into at least two positive integers
        dp = [0] * (n + 1)
        
        # Base cases: 1 and 2
        # n = 2 must be broken into 1 + 1 (product 1)
        # Note: we don't strictly need dp[1] since we only evaluate lengths >= 2
        dp[2] = 1 
        
        for i in range(3, n + 1):
            for j in range(1, i):
                # For every split point j, we have two choices for the remaining part (i - j):
                # 1. Don't break it further: just multiply j * (i - j)
                # 2. Break it further: multiply j * dp[i - j]
                dp[i] = max(dp[i], j * (i - j), j * dp[i - j])
                
        return dp[n]

if __name__ == "__main__":
    sol = Solution()
    print(sol.integerBreak(2))  # 1 (1+1)
    print(sol.integerBreak(10)) # 36 (3+3+4)
