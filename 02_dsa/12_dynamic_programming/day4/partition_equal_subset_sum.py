class Solution:
    def canPartition(self, nums: list[int]) -> bool:
        total_sum = sum(nums)
        
        # If the total sum is odd, we cannot partition it into two equal integer subsets
        if total_sum % 2 != 0:
            return False
            
        target = total_sum // 2
        
        # 1D Space Optimized 0/1 Knapsack Boolean DP
        dp = [False] * (target + 1)
        dp[0] = True  # Base case: A subset sum of 0 is always possible (empty subset)
        
        for num in nums:
            # We must iterate backwards in 0/1 Knapsack to avoid reusing the current element
            for current_target in range(target, num - 1, -1):
                dp[current_target] = dp[current_target] or dp[current_target - num]
                
        return dp[target]

if __name__ == "__main__":
    sol = Solution()
    print(sol.canPartition([1, 5, 11, 5]))  # True (1+5+5 = 11, 11 = 11)
    print(sol.canPartition([1, 2, 3, 5]))   # False
