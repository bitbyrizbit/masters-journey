class Solution:
    def restore_ip(self, s):
        res = []
        if len(s) > 12:
            return res
        def dfs(i, dots, current_ip):
            if dots == 4 and i == len(s):
                res.append(current_ip[:-1])
                return
            if dots > 4:
                return
            for j in range(i, min(i + 3, len(s))):
                if int(s[i:j+1]) < 256 and (i == j or s[i] != "0"):
                    dfs(j + 1, dots + 1, current_ip + s[i:j+1] + ".")
        dfs(0, 0, "")
        return res

s_input = "25525511135"
sol = Solution()
print(sol.restore_ip(s_input))