class Solution:
    def add_operators(self, num, target):
        res = []
        def dfs(i, current_path, current_val, prev_val):
            if i == len(num):
                if current_val == target:
                    res.append(current_path)
                return
            for j in range(i, len(num)):
                if num[i] == "0" and j > i:
                    break
                sub_str = num[i:j+1]
                val = int(sub_str)
                if i == 0:
                    dfs(j + 1, sub_str, val, val)
                else:
                    dfs(j + 1, current_path + "+" + sub_str, current_val + val, val)
                    dfs(j + 1, current_path + "-" + sub_str, current_val - val, -val)
                    dfs(j + 1, current_path + "*" + sub_str, current_val - prev_val + (prev_val * val), prev_val * val)
        dfs(0, "", 0, 0)
        return res

num_input = "123"
target_input = 6
sol = Solution()
print(sol.add_operators(num_input, target_input))