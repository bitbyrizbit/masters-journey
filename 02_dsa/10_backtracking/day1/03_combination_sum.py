class Solution:
    def combinationSum(self, nums, target):
        res = []
        combination = []
        def dfs(i, current_total):
            if current_total == target:
                res.append(combination.copy())
                return
            if i >= len(nums) or current_total > target:
                return
            combination.append(nums[i])
            dfs(i, current_total + nums[i])
            combination.pop()
            dfs(i + 1, current_total)
        dfs(0, 0)
        return res

nums_input = [2, 3, 6, 7]
target_input = 7
sol = Solution()
print(sol.combinationSum(nums_input, target_input))