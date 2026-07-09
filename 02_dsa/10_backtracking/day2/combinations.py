class Solution:
    def combine(self, n, k):
        res = []
        combination = []
        def dfs(start):
            if len(combination) == k:
                res.append(combination.copy())
                return
            for i in range(start, n + 1):
                combination.append(i)
                dfs(i + 1)
                combination.pop()
        dfs(1)
        return res

n_input = 4
k_input = 2
sol = Solution()
print(sol.combine(n_input, k_input))