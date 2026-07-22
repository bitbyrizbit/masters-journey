class Solution:
    def rob(self, nums):
        if len(nums) == 1:
            return nums[0]

        def rob_range(arr):
            prev2 = 0
            prev1 = 0
            for num in arr:
                curr = max(prev1, prev2 + num)
                prev2 = prev1
                prev1 = curr
            return prev1

        return max(rob_range(nums[:-1]), rob_range(nums[1:]))

nums_input = [2, 3, 2]
sol = Solution()
print(sol.rob(nums_input))
