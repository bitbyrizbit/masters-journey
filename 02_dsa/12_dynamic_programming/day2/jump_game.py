class Solution:
    def can_jump_dp(self, nums: list[int]) -> bool:
        n = len(nums)
        dp = [False] * n
        dp[n - 1] = True  
        
        for i in range(n - 2, -1, -1):
            max_jump = min(i + nums[i], n - 1)
            for j in range(i + 1, max_jump + 1):
                if dp[j]:
                    dp[i] = True
                    break
                    
        return dp[0]

    def can_jump_greedy(self, nums: list[int]) -> bool:
        goal = len(nums) - 1
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= goal:
                goal = i
        return goal == 0

nums_input = [2, 3, 1, 1, 4]
sol = Solution()
print("DP Result:", sol.can_jump_dp(nums_input))        
print("Greedy Result:", sol.can_jump_greedy(nums_input))
