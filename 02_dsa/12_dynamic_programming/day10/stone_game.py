class Solution:
    def stoneGame(self, piles: list[int]) -> bool:
        # Game Theory DP (Interval Minimax)
        
        # Mathematical Trick specific to Stone Game 1:
        # Because the number of piles is EVEN, and the total sum is ODD,
        # Alice can conceptually color the piles alternating black/white.
        # She can calculate whether the black piles or white piles yield more total stones.
        # Since she picks first, she can forcefully guarantee she ONLY picks black piles (or white).
        # Therefore, Alice mathematically ALWAYS wins.
        # return True
        
        # To show the actual DP logic (which applies to generalized Stone Game problems):
        n = len(piles)
        
        # dp[i][j] represents the maximum RELATIVE score difference between the first player 
        # acting on the interval [i...j] and the second player.
        dp = [[0] * n for _ in range(n)]
        
        # Base cases: Intervals of length 1 (only 1 pile left)
        # The player just takes that pile, giving them a score difference of piles[i].
        for i in range(n):
            dp[i][i] = piles[i]
            
        # Interval DP Traversal: Gap Method
        for L in range(2, n + 1):
            for i in range(n - L + 1):
                j = i + L - 1
                
                # Player can choose the left pile (piles[i]) or the right pile (piles[j]).
                # If they choose left, they gain piles[i], but the opponent will play optimally 
                # on the remaining interval [i+1...j], subtracting from the relative score.
                take_left = piles[i] - dp[i+1][j]
                
                # If they choose right, they gain piles[j], subtracting the opponent's optimal 
                # score on interval [i...j-1].
                take_right = piles[j] - dp[i][j-1]
                
                dp[i][j] = max(take_left, take_right)
                
        # If the relative score difference for the entire array is > 0, Alice wins.
        return dp[0][n-1] > 0

if __name__ == "__main__":
    sol = Solution()
    print(sol.stoneGame([5,3,4,5])) # True
    print(sol.stoneGame([3,7,2,3])) # True
