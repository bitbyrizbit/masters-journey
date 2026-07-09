class Solution:
    def combination_sum(self, candidates, target):
        candidates.sort()
        res = []
        combination = []
        def dfs(i, current_total):
            if current_total == target:
                res.append(combination.copy())
                return
            if current_total > target or i >= len(candidates):
                return
            combination.append(candidates[i])
            dfs(i + 1, current_total + candidates[i])
            combination.pop()
            while i + 1 < len(candidates) and candidates[i] == candidates[i + 1]:
                i += 1
            dfs(i + 1, current_total)
        dfs(0, 0)
        return res

candidates_input = [10, 1, 2, 7, 6, 1, 5]
target_input = 8
sol = Solution()
print(sol.combination_sum(candidates_input, target_input))