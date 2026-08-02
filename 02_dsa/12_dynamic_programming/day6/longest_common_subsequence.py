class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # Space-Optimized 1D Array for 2D String DP
        # We only need the previous row to compute the current row.
        
        m, n = len(text1), len(text2)
        
        # Ensure text2 is the shorter string to minimize space
        if m < n:
            text1, text2 = text2, text1
            m, n = n, m
            
        dp = [0] * (n + 1)
        
        for i in range(1, m + 1):
            prev = 0 # Holds the value of dp[i-1][j-1] (top-left diagonal)
            for j in range(1, n + 1):
                temp = dp[j] # Save current dp[j] (top neighbor) before overwrite
                
                if text1[i-1] == text2[j-1]:
                    # Characters match: Extend the LCS from the diagonal
                    dp[j] = prev + 1
                else:
                    # Characters don't match: Take max of dropping from text1 (top) or text2 (left)
                    dp[j] = max(dp[j], dp[j-1])
                    
                prev = temp # Update prev for the next column calculation
                
        return dp[n]

if __name__ == "__main__":
    sol = Solution()
    print(sol.longestCommonSubsequence("abcde", "ace"))  # 3 ("ace")
    print(sol.longestCommonSubsequence("abc", "def"))    # 0
