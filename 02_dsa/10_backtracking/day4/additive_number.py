class Solution:
    def is_additive_number(self, num):
        n = len(num)
        def dfs(i, n1, n2, count):
            if i == n:
                return count >= 3
            for j in range(i, n):
                if num[i] == "0" and j > i:
                    break
                val = int(num[i:j+1])
                if n1 != -1 and n2 != -1:
                    if val == n1 + n2:
                        if dfs(j + 1, n2, val, count + 1):
                            return True
                    elif val > n1 + n2:
                        break
                elif n1 == -1:
                    if dfs(j + 1, val, n2, count + 1):
                        return True
                else:
                    if dfs(j + 1, n1, val, count + 1):
                        return True
            return False
        return dfs(0, -1, -1, 0)

num_input = "112358"
sol = Solution()
print(sol.is_additive_number(num_input))