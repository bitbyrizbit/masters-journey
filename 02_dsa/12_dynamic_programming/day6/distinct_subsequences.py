class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        # String DP: Combinatorics / Counting ways 't' appears as a subsequence in 's'
        m, n = len(s), len(t)
        
        if n > m:
            return 0
            
        # dp[j] represents the number of ways to form the prefix of 't' of length j
        # Space optimized to 1D
        dp = [0] * (n + 1)
        
        # Base case: There is exactly 1 way to form an empty string 't' (delete all chars from 's')
        dp[0] = 1
        
        for i in range(1, m + 1):
            # Iterate backwards to avoid reusing the current character of 's' multiple times 
            # for the same prefix progression in 't' (similar to 0/1 Knapsack)
            for j in range(n, 0, -1):
                if s[i-1] == t[j-1]:
                    # If chars match, we can either:
                    # 1. NOT use this char from 's' (dp[j])
                    # 2. USE this char from 's' (dp[j-1] - ways to make previous prefix)
                    dp[j] += dp[j-1]
                    
        return dp[n]

if __name__ == "__main__":
    sol = Solution()
    print(sol.numDistinct("rabbbit", "rabbit"))  # 3
    print(sol.numDistinct("babgbag", "bag"))     # 5
