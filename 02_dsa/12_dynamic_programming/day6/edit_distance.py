class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        
        # Space Optimization: We only need the previous row
        dp = [0] * (n + 1)
        
        # Base case initialization for row 0:
        # Converting an empty word1 into word2 of length j requires j insertions.
        for j in range(1, n + 1):
            dp[j] = j
            
        for i in range(1, m + 1):
            # The value of dp[0] for row i is i (deleting all characters of word1)
            prev = dp[0]
            dp[0] = i
            
            for j in range(1, n + 1):
                temp = dp[j]
                
                if word1[i-1] == word2[j-1]:
                    # Match: No cost, inherit from diagonal
                    dp[j] = prev
                else:
                    # Mismatch: 1 + min(Insert (left), Delete (top), Replace (diagonal))
                    dp[j] = 1 + min(dp[j-1], dp[j], prev)
                    
                prev = temp
                
        return dp[n]

if __name__ == "__main__":
    sol = Solution()
    print(sol.minDistance("horse", "ros"))      # 3 (replace h->r, delete r, delete e)
    print(sol.minDistance("intention", "execution")) # 5
