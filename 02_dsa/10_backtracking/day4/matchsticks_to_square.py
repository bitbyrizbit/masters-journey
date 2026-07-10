class Solution:
    def make_square(self, matchsticks):
        total_sum = sum(matchsticks)
        if total_sum % 4 != 0:
            return False
        target = total_sum // 4
        matchsticks.sort(reverse=True)
        sides = [0] * 4
        def dfs(i):
            if i == len(matchsticks):
                return True
            for j in range(4):
                if sides[j] + matchsticks[i] <= target:
                    sides[j] += matchsticks[i]
                    if dfs(i + 1):
                        return True
                    sides[j] -= matchsticks[i]
                if sides[j] == 0:
                    break
            return False
        return dfs(0)

matchsticks_input = [1, 1, 2, 2, 2]
sol = Solution()
print(sol.make_square(matchsticks_input))