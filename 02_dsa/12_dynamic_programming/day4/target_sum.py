class Solution:
    def findTargetSumWays(self, nums: list[int], target: int) -> int:
        # Transformation to Subset Sum Math:
        # Sum(Positive) - Sum(Negative) = target
        # Sum(Positive) + Sum(Negative) = total_sum
        # ----------------------------------------
        # 2 * Sum(Positive) = target + total_sum
        # Sum(Positive) = (target + total_sum) / 2
        
        total_sum = sum(nums)
        
        # Check invalid states where no subset can mathematically reach target
        if abs(target) > total_sum or (total_sum + target) % 2 != 0:
            return 0
            
        subset_target = (total_sum + target) // 2
        
        # 1D Space Optimized Counting DP
        dp = [0] * (subset_target + 1)
        dp[0] = 1 # Base case: 1 way to make sum 0 (pick no elements)
        
        for num in nums:
            # Iterate backwards (0/1 Knapsack: elements can only be used once)
            for j in range(subset_target, num - 1, -1):
                dp[j] += dp[j - num]
                
        return dp[subset_target]

if __name__ == "__main__":
    sol = Solution()
    print(sol.findTargetSumWays([1, 1, 1, 1, 1], 3))  # 5
    print(sol.findTargetSumWays([1], 1))              # 1
