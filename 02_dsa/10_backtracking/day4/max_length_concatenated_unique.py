class Solution:
    def max_length(self, arr):
        def dfs(i, current_set):
            if i == len(arr):
                return len(current_set)
            res = dfs(i + 1, current_set)
            word_set = set(arr[i])
            if len(word_set) == len(arr[i]) and not (word_set & current_set):
                res = max(res, dfs(i + 1, current_set | word_set))
            return res
        return dfs(0, set())

arr_input = ["un", "iq", "ue"]
sol = Solution()
print(sol.max_length(arr_input))