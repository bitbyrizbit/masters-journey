class Solution:
    def canPartitionKSubsets(self, nums: list[int], k: int) -> bool:
        # Bitmask DP with Memoization
        total_sum = sum(nums)
        if total_sum % k != 0:
            return False
            
        target = total_sum // k
        n = len(nums)
        
        # Sort descending to try placing larger elements first (massive heuristic optimization)
        nums.sort(reverse=True)
        
        # memo[mask] = True if this specific subset mask can be successfully partitioned
        memo = {}
        
        def dfs(mask: int, current_sum: int) -> bool:
            if mask == (1 << n) - 1:
                return True
                
            if mask in memo:
                return memo[mask]
                
            for i in range(n):
                # If element i is NOT used in the current mask
                if (mask & (1 << i)) == 0:
                    new_sum = current_sum + nums[i]
                    
                    if new_sum <= target:
                        # If placing nums[i] fills the subset exactly, the next subset starts from sum 0
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
    print(sol.canPartitionKSubsets([4, 3, 2, 3, 5, 2, 1], 4)) # True
    print(sol.canPartitionKSubsets([1, 2, 3, 4], 3))          # False
