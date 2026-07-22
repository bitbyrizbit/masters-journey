class Solution:
    def rob(self, nums):
        prev2 = 0
        prev1 = 0
        for num in nums:
            curr = max(prev1, prev2 + num)
            prev2 = prev1
            prev1 = curr
        return prev1

nums_input = [2, 7, 9, 3, 1]
sol = Solution()
print(sol.rob(nums_input))
