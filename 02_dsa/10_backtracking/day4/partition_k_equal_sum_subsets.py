class Solution:
    def partition_k_subsets(self, nums, k):
        total_sum = sum(nums)
        if total_sum % k != 0:
            return False
        target = total_sum // k
        nums.sort(reverse=True)
        used = [False] * len(nums)
        def dfs(i, current_k, current_sum):
            if current_k == 0:
                return True
            if current_sum == target:
                return dfs(0, current_k - 1, 0)
            for j in range(i, len(nums)):
                if used[j] or current_sum + nums[j] > target:
                    continue
                used[j] = True
                if dfs(j + 1, current_k, current_sum + nums[j]):
                    return True
                used[j] = False
                if current_sum == 0:
                    return False
            return False
        return dfs(0, k, 0)

nums_input = [4, 3, 2, 3, 5, 2, 1]
k_input = 4
sol = Solution()
print(sol.partition_k_subsets(nums_input, k_input))