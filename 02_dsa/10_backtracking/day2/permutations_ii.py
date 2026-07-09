class Solution:
    def permute_unique(self, nums):
        res = []
        permutation = []
        count = {}
        for n in nums:
            count[n] = count.get(n, 0) + 1
        def dfs():
            if len(permutation) == len(nums):
                res.append(permutation.copy())
                return
            for n in count:
                if count[n] > 0:
                    permutation.append(n)
                    count[n] -= 1
                    dfs()
                    count[n] += 1
                    permutation.pop()
        dfs()
        return res

nums_input = [1, 1, 2]
sol = Solution()
print(sol.permute_unique(nums_input))