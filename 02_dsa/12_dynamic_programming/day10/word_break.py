class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        # String DP / Prefix Feasibility
        # Convert list to set for O(1) dictionary lookups
        word_set = set(wordDict)
        n = len(s)
        
        # dp[i] = True if s[0...i-1] can be segmented into dictionary words
        dp = [False] * (n + 1)
        
        # Base case: an empty string can always be segmented
        dp[0] = True 
        
        for i in range(1, n + 1):
            # Check all possible split points j before i
            for j in range(i):
                # If the prefix up to j is valid, AND the substring from j to i is in the dictionary
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break # No need to check other splits for this 'i' once we found a valid one
                    
        return dp[n]

if __name__ == "__main__":
    sol = Solution()
    print(sol.wordBreak("leetcode", ["leet", "code"])) # True
    print(sol.wordBreak("applepenapple", ["apple", "pen"])) # True
    print(sol.wordBreak("catsandog", ["cats", "dog", "sand", "and", "cat"])) # False
