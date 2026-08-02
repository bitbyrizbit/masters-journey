class Solution:
    def canIWin(self, maxChoosableInteger: int, desiredTotal: int) -> bool:
        # Game Theory Bitmask DP
        
        # If the largest possible integer instantly wins
        if desiredTotal <= maxChoosableInteger:
            return True
            
        # If the sum of all available integers is less than the target, no one can ever win
        if (maxChoosableInteger * (maxChoosableInteger + 1)) // 2 < desiredTotal:
            return False
            
        memo = {}
        
        # mask tracks which integers (from 1 to maxChoosableInteger) have been picked
        def dfs(mask: int, current_total: int) -> bool:
            if mask in memo:
                return memo[mask]
                
            # Iterate through all available choices
            for i in range(1, maxChoosableInteger + 1):
                # Check if integer 'i' is currently available (not in mask)
                if not (mask & (1 << i)):
                    
                    # Winning Condition A: Picking 'i' instantly reaches/exceeds the target
                    if current_total + i >= desiredTotal:
                        memo[mask] = True
                        return True
                        
                    # Winning Condition B: Picking 'i' forces the opponent into a universally losing state
                    # We pass the updated mask and total to the opponent.
                    # If the opponent's DFS returns False, it means they CANNOT win from that state,
                    # which implies WE win by putting them in that state!
                    new_mask = mask | (1 << i)
                    if not dfs(new_mask, current_total + i):
                        memo[mask] = True
                        return True
                        
            # If no available move leads to a win or forces the opponent to lose, we lose from this state
            memo[mask] = False
            return False
            
        return dfs(0, 0)

if __name__ == "__main__":
    sol = Solution()
    print(sol.canIWin(10, 11)) # False
    print(sol.canIWin(10, 0))  # True
    print(sol.canIWin(10, 1))  # True
