class Solution:
    def split_string(self, s):
        def dfs(i, prev):
            if i == len(s):
                return True
            for j in range(i, len(s)):
                val = int(s[i:j+1])
                if val + 1 == prev and dfs(j + 1, val):
                    return True
            return False
        for i in range(len(s) - 1):
            val = int(s[:i+1])
            if dfs(i + 1, val):
                return True
        return False

s_input = "050043"
sol = Solution()
print(sol.split_string(s_input))