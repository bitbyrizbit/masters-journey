class Solution:
    def permute(self, nums):
        res = []
        def dfs(start):
            if start == len(nums):
                res.append(nums.copy())
                return
            for i in range(start, len(nums)):
                nums[start], nums[i] = nums[i], nums[start]
                dfs(start + 1)
                nums[start], nums[i] = nums[i], nums[start]
        dfs(0)
        return res

nums_input = [1, 2, 3]
sol = Solution()
print(sol.permute(nums_input))