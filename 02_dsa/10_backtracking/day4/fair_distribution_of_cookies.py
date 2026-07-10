class Solution:
    def distribute_cookies(self, cookies, k):
        cookies.sort(reverse=True)
        children = [0] * k
        self.res = float("inf")
        def dfs(i):
            if i == len(cookies):
                self.res = min(self.res, max(children))
                return
            if max(children) >= self.res:
                return
            for j in range(k):
                children[j] += cookies[i]
                dfs(i + 1)
                children[j] -= cookies[i]
                if children[j] == 0:
                    break
        dfs(0)
        return self.res

cookies_input = [8, 15, 10, 20, 8]
k_input = 2
sol = Solution()
print(sol.distribute_cookies(cookies_input, k_input))