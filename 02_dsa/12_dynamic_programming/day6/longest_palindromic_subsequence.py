class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        # A palindrome reads the same forwards and backwards.
        # Thus, the Longest Palindromic Subsequence of a string 's'
        # is exactly equal to the Longest Common Subsequence of 's' and 'reverse(s)'.
        
        # We reuse the exact LCS logic.
        text1 = s
        text2 = s[::-1]
        n = len(s)
        
        dp = [0] * (n + 1)
        
        for i in range(1, n + 1):
            prev = 0
            for j in range(1, n + 1):
                temp = dp[j]
                if text1[i-1] == text2[j-1]:
                    dp[j] = prev + 1
                else:
                    dp[j] = max(dp[j], dp[j-1])
                prev = temp
                
        return dp[n]

if __name__ == "__main__":
    sol = Solution()
    print(sol.longestPalindromeSubseq("bbbab"))  # 4 ("bbbb")
    print(sol.longestPalindromeSubseq("cbbd"))   # 2 ("bb")
