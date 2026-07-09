class Solution:
    def letter_combinations(self, digits):
        if not digits:
            return []
        res = []
        digit_map = {
            "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
            "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"
        }
        
        def dfs(i, current_str):
            if len(current_str) == len(digits):
                res.append(current_str)
                return
            for char in digit_map[digits[i]]:
                dfs(i + 1, current_str + char)
        dfs(0, "")
        return res

digits_input = "23"
sol = Solution()
print(sol.letter_combinations(digits_input))