class Solution:
    def makesquare(self, matchsticks: list[int]) -> bool:
        # Matchsticks to Square is EXACTLY Partition to K Equal Sum Subsets where K = 4.
        
        total_sum = sum(matchsticks)
        if total_sum % 4 != 0:
            return False
            
        target = total_sum // 4
        n = len(matchsticks)
        
        # Optimization: Sort descending to trigger early failures on massive matchsticks
        matchsticks.sort(reverse=True)
        
        # A single matchstick larger than the side of a square instantly ruins it
        if matchsticks[0] > target:
            return False
            
        memo = {}
        
        def dfs(mask: int, current_sum: int) -> bool:
            # If all matchsticks are perfectly used, we win
            if mask == (1 << n) - 1:
                return True
                
            if mask in memo:
                return memo[mask]
                
            for i in range(n):
                # If matchstick i is not yet placed
                if not (mask & (1 << i)):
                    new_sum = current_sum + matchsticks[i]
                    
                    if new_sum <= target:
                        next_sum = new_sum % target
                        new_mask = mask | (1 << i)
                        
                        if dfs(new_mask, next_sum):
                            memo[mask] = True
                            return True
                            
            memo[mask] = False
            return False
            
        return dfs(0, 0)

if __name__ == "__main__":
    sol = Solution()
    print(sol.makesquare([1,1,2,2,2])) # True
    print(sol.makesquare([3,3,3,3,4])) # False
