class Solution:
    def minimumDeleteSum(self, s1: str, s2: str) -> int:
        # String DP: Minimum Cost Operations (Weighted LCS variation)
        m, n = len(s1), len(s2)
        
        # Space optimized 1D array
        dp = [0] * (n + 1)
        
        # Base case for row 0: Deleting characters from s2 to match empty string s1
        for j in range(1, n + 1):
            dp[j] = dp[j-1] + ord(s2[j-1])
            
        for i in range(1, m + 1):
            # Base case for col 0: Deleting characters from s1 to match empty string s2
            prev = dp[0]
            dp[0] += ord(s1[i-1])
            
            for j in range(1, n + 1):
                temp = dp[j]
                
                if s1[i-1] == s2[j-1]:
                    # Match: No cost to delete, inherit from diagonal
                    dp[j] = prev
                else:
                    # Mismatch: min cost of deleting from s1 (top + ord(s1)) or s2 (left + ord(s2))
                    dp[j] = min(dp[j] + ord(s1[i-1]), dp[j-1] + ord(s2[j-1]))
                    
                prev = temp
                
        return dp[n]

if __name__ == "__main__":
    sol = Solution()
    print(sol.minimumDeleteSum("sea", "eat"))  # 231 (delete 's' = 115, delete 't' = 116)
    print(sol.minimumDeleteSum("delete", "leet")) # 403
