class Solution:
    def calculateMinimumHP(self, dungeon: list[list[int]]) -> int:
        # Reverse Grid DP
        # If we start from top-left, we have two unknown constraints: HP needed to reach cell, and HP needed for the rest.
        # By starting from bottom-right (princess), we only track the minimum HP required to survive from this cell onwards.
        
        m, n = len(dungeon), len(dungeon[0])
        
        # We need a 1D array initialized to infinity. Size n+1 to handle right boundaries cleanly.
        dp = [float('inf')] * (n + 1)
        
        # Base case setup: The cell immediately to the right and immediately below the princess need 1 HP to survive.
        # This forces the calculation at the princess cell to just be what's required to survive the princess cell itself.
        dp[n-1] = 1 
        
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                # We need enough HP to survive the current cell AND the minimum of the optimal path forward (right or down)
                min_health_needed = min(dp[j], dp[j+1]) - dungeon[i][j]
                
                # If the cell has a potion (positive), min_health_needed could be <= 0.
                # However, a knight must always have at least 1 HP to be alive.
                dp[j] = max(1, min_health_needed)
                
            # After computing row i, the dummy right-boundary column must reset to infinity
            # so it doesn't artificially provide a "1 HP" escape path for rows above the princess.
            dp[n] = float('inf')
            
        return dp[0]

if __name__ == "__main__":
    sol = Solution()
    print(sol.calculateMinimumHP([[-2,-3,3],[-5,-10,1],[10,30,-5]]))  # 7
    print(sol.calculateMinimumHP([[0]]))                              # 1
