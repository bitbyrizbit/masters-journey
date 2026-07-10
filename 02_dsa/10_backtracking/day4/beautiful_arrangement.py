class Solution:
    def count_arrangement(self, n):
        self.res = 0
        used = [False] * (n + 1)
        def dfs(pos):
            if pos > n:
                self.res += 1
                return
            for i in range(1, n + 1):
                if not used[i] and (i % pos == 0 or pos % i == 0):
                    used[i] = True
                    dfs(pos + 1)
                    used[i] = False
        dfs(1)
        return self.res

n_input = 3
sol = Solution()
print(sol.count_arrangement(n_input))