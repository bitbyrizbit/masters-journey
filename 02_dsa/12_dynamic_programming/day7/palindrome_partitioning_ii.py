class Solution:
    def minCut(self, s: str) -> int:
        # Split DP: Finding minimum cuts to partition a string such that every substring is a palindrome.
        
        n = len(s)
        if n == 0:
            return 0
            
        # Step 1: Precompute a 2D boolean DP to instantly query if s[i:j+1] is a palindrome
        # is_pal[i][j] is True if s[i:j+1] is a palindrome
        is_pal = [[False] * n for _ in range(n)]
        
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                if s[i] == s[j] and (j - i <= 2 or is_pal[i+1][j-1]):
                    is_pal[i][j] = True
                    
        # Step 2: 1D DP to find minimum cuts
        # min_cuts[i] = minimum cuts for the prefix s[0:i+1]
        min_cuts = [0] * n
        
        for i in range(n):
            if is_pal[0][i]:
                min_cuts[i] = 0 # No cuts needed if the whole prefix is a palindrome
            else:
                min_cuts[i] = i # Max possible cuts (cut every character)
                # Try every possible split point j before i
                for j in range(i):
                    if is_pal[j+1][i]:
                        min_cuts[i] = min(min_cuts[i], min_cuts[j] + 1)
                        
        return min_cuts[n-1]

if __name__ == "__main__":
    sol = Solution()
    print(sol.minCut("aab"))  # 1 (cut between 'aa' and 'b')
    print(sol.minCut("a"))    # 0
    print(sol.minCut("ab"))   # 1
